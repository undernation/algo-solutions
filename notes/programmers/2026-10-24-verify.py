"""Independent verification for PGS 67259 and 150366 (standard library only).

Run from any directory: python notes/programmers/2026-10-24-verify.py
Writes the two sibling *-verification.json reports after all assertions pass.
"""

import ast
import copy
import hashlib
import heapq
import json
from pathlib import Path
import random
import re
import time

ROOT = Path(__file__).resolve().parents[2]
REPORTS = Path(__file__).resolve().parent
DATE = '2026-10-24'
INF = 10**18


def load_function(source):
    namespace = {}
    exec(compile(source, '<archived solution>', 'exec'), namespace)
    return namespace['solution']


def no_active_print(source):
    return not any(isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                   and node.func.id == 'print' for node in ast.walk(ast.parse(source)))


def road_brute(board):
    """Enumerate simple cell paths, without a direction-state distance table."""
    n = len(board)
    target = n*n - 1
    best = INF

    def visit(y, x, previous_axis, cost, used):
        nonlocal best
        if y*n + x == target:
            best = min(best, cost)
            return
        if cost + 100 * (2*n - 2 - y - x) >= best:
            return
        for dy, dx, axis in ((1, 0, 0), (0, 1, 1), (-1, 0, 0), (0, -1, 1)):
            ny, nx = y+dy, x+dx
            if not (0 <= ny < n and 0 <= nx < n) or board[ny][nx]:
                continue
            bit = 1 << (ny*n + nx)
            if used & bit:
                continue
            extra = 100 + (500 if previous_axis is not None and axis != previous_axis else 0)
            visit(ny, nx, axis, cost+extra, used | bit)

    visit(0, 0, None, 0, 1)
    return None if best == INF else best


def road_dijkstra(board):
    """Priority queue + two axes, independently of the submitted four directions."""
    n = len(board)
    distance = [[[INF, INF] for _ in range(n)] for _ in range(n)]
    distance[0][0] = [0, 0]
    heap = [(0, 0, 0, 0), (0, 0, 0, 1)]
    while heap:
        cost, y, x, axis = heapq.heappop(heap)
        if cost != distance[y][x][axis]:
            continue
        if (y, x) == (n-1, n-1):
            return cost
        for dy, dx, next_axis in ((0, -1, 1), (0, 1, 1), (-1, 0, 0), (1, 0, 0)):
            ny, nx = y+dy, x+dx
            if 0 <= ny < n and 0 <= nx < n and board[ny][nx] == 0:
                new_cost = cost + 100 + 500*(axis != next_axis)
                if new_cost < distance[ny][nx][next_axis]:
                    distance[ny][nx][next_axis] = new_cost
                    heapq.heappush(heap, (new_cost, ny, nx, next_axis))
    return None


def verify_road():
    source = (ROOT / 'programmers/67259_경주로건설.py').read_text(encoding='utf-8')
    solution = load_function(source)
    assert no_active_print(source)
    problem = json.loads((ROOT / 'problems/programmers/67259.json').read_text(encoding='utf-8'))

    def check(board, expected):
        saved = copy.deepcopy(board)
        actual = solution(board)
        assert actual == expected, {'board': board, 'expected': expected, 'actual': actual}
        assert board == saved, 'The board was mutated'
        return actual

    for sample in problem['samples']:
        board = sample['args'][0]
        expected = sample['expected']
        assert road_dijkstra(board) == expected
        check(board, expected)
    print('67259: official samples 4/4', flush=True)

    exhaustive = []
    for n in (3, 4):
        tested = excluded = 0
        for mask in range(1 << (n*n-2)):
            board = [[0]*n for _ in range(n)]
            for cell in range(1, n*n-1):
                board[cell//n][cell % n] = (mask >> (cell-1)) & 1
            expected = road_brute(board)
            # Cross-check the second oracle before trusting it on larger boards.
            assert road_dijkstra(board) == expected
            if expected is None:
                excluded += 1
                continue  # Official inputs guarantee a path.
            check(board, expected)
            tested += 1
        exhaustive.append({'n': n, 'all_wall_patterns': 1 << (n*n-2),
                           'valid_boards_checked': tested, 'unreachable_excluded': excluded})
        print(f'67259: N={n}, {tested} reachable exhaustive boards, {excluded} invalid boards excluded', flush=True)

    rng = random.Random(20261024)
    random_cases = 3000
    for case in range(random_cases):
        n = rng.randint(3, 25)
        wall_rate = rng.uniform(0.05, 0.55)
        board = [[int(rng.random() < wall_rate) for _ in range(n)] for _ in range(n)]
        board[0][0] = board[-1][-1] = 0
        if case % 2:
            steps = [(1, 0)]*(n-1) + [(0, 1)]*(n-1)
            rng.shuffle(steps)
            y = x = 0
            for dy, dx in steps:
                y, x = y+dy, x+dx
                board[y][x] = 0
        expected = road_dijkstra(board)
        if expected is None:
            # The fully open top row and right column guarantee a legal path.
            board[0] = [0]*n
            for row in board:
                row[-1] = 0
            expected = road_dijkstra(board)
        check(board, expected)
    print(f'67259: random {random_cases}/{random_cases}', flush=True)

    n = 25
    open_board = [[0]*n for _ in range(n)]
    right_only = copy.deepcopy(open_board)
    right_only[1][0] = 1
    down_only = copy.deepcopy(open_board)
    down_only[0][1] = 1
    snake = [[1]*n for _ in range(n)]
    for row in range(0, n, 2):
        snake[row] = [0]*n
        if row+1 < n:
            snake[row+1][n-1 if (row//2) % 2 == 0 else 0] = 0
    large = []
    for name, board in [('open', open_board), ('right_only', right_only),
                        ('down_only', down_only), ('snake_corridor', snake)]:
        expected = road_dijkstra(board)
        start = time.perf_counter()
        result = check(board, expected)
        elapsed = time.perf_counter() - start
        large.append({'name': name, 'n': n, 'result': result, 'seconds': round(elapsed, 6)})

    return {'date': DATE, 'problem': 'PGS/67259',
            'status': '품', 'status_basis': 'user_reported_solved_and_requested_status',
            'platform_verdict': 'not_independently_observed',
            'source_sha256': hashlib.sha256(source.encode()).hexdigest(),
            'oracles': ['simple-path exhaustive search for N=3,4', 'heap Dijkstra with two orientation axes'],
            'official_samples': {'passed': 4, 'total': 4}, 'exhaustive': exhaustive,
            'random_seed': 20261024, 'random_cases': random_cases,
            'crosscheck_total': 4 + sum(row['valid_boards_checked'] for row in exhaustive) + random_cases + len(large),
            'mismatches': 0, 'large_cases': large, 'active_debug_prints': 0,
            'input_mutation': False,
            'normalization': 'Restored pasted line breaks/indentation and Markdown escapes; algorithm unchanged.'}


def table_oracle(commands):
    """Explicit group member sets and per-cell values; no Union-Find or find()."""
    parsed = [command.split() for command in commands]
    positions = set()
    for parts in parsed:
        if parts[0] == 'MERGE':
            positions.update([(int(parts[1]), int(parts[2])), (int(parts[3]), int(parts[4]))])
        elif not (parts[0] == 'UPDATE' and len(parts) == 3):
            positions.add((int(parts[1]), int(parts[2])))
    groups = {p: {p} for p in positions}
    values = {p: None for p in positions}
    result = []
    for parts in parsed:
        op = parts[0]
        if op == 'UPDATE' and len(parts) == 3:
            before, after = parts[1:]
            for p in positions:
                if values[p] == before:
                    values[p] = after
            continue
        p = int(parts[1]), int(parts[2])
        if op == 'UPDATE':
            for cell in groups[p]:
                values[cell] = parts[3]
        elif op == 'MERGE':
            q = int(parts[3]), int(parts[4])
            if groups[p] is groups[q]:
                continue
            merged_value = values[p] if values[p] is not None else values[q]
            merged = groups[p] | groups[q]
            for cell in merged:
                groups[cell] = merged
                values[cell] = merged_value
        elif op == 'UNMERGE':
            saved_value = values[p]
            members = list(groups[p])
            for cell in members:
                groups[cell] = {cell}
                values[cell] = None
            values[p] = saved_value
        elif op == 'PRINT':
            result.append('EMPTY' if values[p] is None else values[p])
        else:
            raise AssertionError(parts)
    return result


def verify_table():
    source = (ROOT / 'programmers/150366_표병합.py').read_text(encoding='utf-8')
    original = load_function(source)
    assert no_active_print(source)
    note = (REPORTS / '150366.md').read_text(encoding='utf-8')
    reference_source = re.search(r'```python\n(.*?)```', note, flags=re.S).group(1)
    reference = load_function(reference_source)
    assert no_active_print(reference_source)
    problem = json.loads((ROOT / 'problems/programmers/150366.json').read_text(encoding='utf-8'))
    official_original = []
    for sample in problem['samples']:
        commands = sample['args'][0]
        expected = sample['expected']
        assert table_oracle(commands) == expected
        assert reference(commands) == expected
        actual = original(commands)
        official_original.append({'actual': actual, 'expected': expected, 'passed': actual == expected})

    counterexamples = []
    for name, commands in [
        ('bulk_update_missing', ['UPDATE 1 1 a', 'UPDATE a b', 'PRINT 1 1']),
        ('immediate_parent_is_not_root', ['UPDATE 1 1 a', 'MERGE 1 1 1 2', 'MERGE 1 3 1 1', 'PRINT 1 2']),
    ]:
        expected = table_oracle(commands)
        actual = original(commands)
        assert actual != expected
        assert reference(commands) == expected
        counterexamples.append({'name': name, 'commands': commands, 'actual': actual, 'expected': expected})

    targeted = [
        ['PRINT 50 50'],
        ['UPDATE 1 1 a', 'MERGE 1 1 1 1', 'PRINT 1 1'],
        ['UPDATE 1 1 a', 'MERGE 1 1 1 2', 'MERGE 1 2 1 1', 'PRINT 1 1'],
        ['UPDATE 1 1 a', 'UPDATE 50 50 b', 'MERGE 1 1 50 50', 'PRINT 50 50'],
        ['UPDATE 50 50 b', 'MERGE 1 1 50 50', 'UNMERGE 50 50', 'PRINT 1 1', 'PRINT 50 50'],
        ['UPDATE 1 1 a', 'MERGE 1 1 1 2', 'MERGE 1 3 1 1', 'UNMERGE 1 2', 'PRINT 1 1', 'PRINT 1 2', 'PRINT 1 3'],
        ['UPDATE 1 1 a', 'UPDATE a a', 'PRINT 1 1'],
    ]
    for commands in targeted:
        assert reference(commands) == table_oracle(commands)

    rng = random.Random(15036620261024)
    random_cases = 2000
    original_mismatches = 0
    for _ in range(random_cases):
        commands = []
        cells = [(r, c) for r in range(1, 5) for c in range(1, 5)] + [(50, 50), (1, 50), (50, 1)]
        for _ in range(rng.randint(20, 80)):
            op = rng.randrange(5)
            r, c = rng.choice(cells)
            if op == 0:
                commands.append(f'UPDATE {r} {c} {rng.choice(["a", "b", "c", "0", "v123456789"])}')
            elif op == 1:
                commands.append(f'UPDATE {rng.choice(["a", "b", "c", "0"])} {rng.choice(["a", "b", "c", "0"])}')
            elif op == 2:
                r2, c2 = rng.choice(cells)
                commands.append(f'MERGE {r} {c} {r2} {c2}')
            elif op == 3:
                commands.append(f'UNMERGE {r} {c}')
            else:
                commands.append(f'PRINT {r} {c}')
        commands.extend(f'PRINT {r} {c}' for r, c in cells)
        expected = table_oracle(commands)
        assert reference(commands) == expected, commands
        original_mismatches += original(commands) != expected
    print(f'150366: reference random {random_cases}/{random_cases}; original mismatches {original_mismatches}', flush=True)

    # Exactly 1,000 legal commands, including at least one PRINT in each case.
    cells = [(r, c) for r in range(1, 51) for c in range(1, 51)]
    merge_chain = ['UPDATE 1 1 a']
    for r, c in cells[1:999]:
        merge_chain.append(f'MERGE {r} {c} 1 1')
    merge_chain.append('PRINT 1 1')
    unmerge_scan = ['UNMERGE 50 50'] * 999 + ['PRINT 50 50']
    bulk_scan = ['UPDATE 50 50 a'] + ['UPDATE a b', 'UPDATE b a']*499 + ['PRINT 50 50']
    large = []
    for name, commands in [('deep_merge_chain', merge_chain), ('repeated_unmerge', unmerge_scan), ('repeated_bulk_update', bulk_scan)]:
        assert len(commands) == 1000
        expected = table_oracle(commands)
        start = time.perf_counter()
        actual = reference(commands)
        elapsed = time.perf_counter() - start
        assert actual == expected
        large.append({'name': name, 'command_count': len(commands), 'result': actual, 'seconds': round(elapsed, 6)})

    # Both functions are called repeatedly above; confirm empty-table reset explicitly.
    assert reference(['UPDATE 1 1 a', 'PRINT 1 1']) == ['a']
    assert reference(['PRINT 1 1']) == ['EMPTY']
    return {'date': DATE, 'problem': 'PGS/150366', 'status': '못품',
            'status_basis': 'user_reported_unsolved; reference viewed; no independent re-solve',
            'source_sha256': hashlib.sha256(source.encode()).hexdigest(),
            'reference_sha256': hashlib.sha256(reference_source.encode()).hexdigest(),
            'oracle': 'explicit group member sets and per-cell values; no Union-Find',
            'official_samples': {'reference_passed': 2, 'total': 2, 'original_results': official_original},
            'counterexamples': counterexamples, 'targeted_reference_cases': len(targeted),
            'random_seed': 15036620261024, 'random_cases': random_cases,
            'original_random_mismatches': original_mismatches, 'reference_mismatches': 0,
            'large_cases': large, 'active_debug_prints': 0,
            'platform_verdict': 'not_observed; local verification only',
            'normalization': 'Removed trailing chat question and trailing spaces only; own code errors preserved.'}


if __name__ == '__main__':
    road = verify_road()
    table = verify_table()
    for no, report in [('67259', road), ('150366', table)]:
        (REPORTS / f'{no}-verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'road_crosschecks': road['crosscheck_total'], 'road_mismatches': road['mismatches'],
                      'road_large_cases': road['large_cases'], 'table_counterexamples': table['counterexamples'],
                      'table_reference_mismatches': table['reference_mismatches']}, ensure_ascii=False, indent=2), flush=True)
