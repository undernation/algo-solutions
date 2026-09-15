"""농지 이동과 수확의 서로 다른 연습용 50개 입력을 생성하고 검증한다.

제공 입력에서 관찰한 N=6..9, M=10..50, 산으로 둘러싸인 지도만 사용한다.
공식 상한은 미확인이며, 이 입력은 공식 히든 테스트가 아니다.
검증기는 절대 성숙 날짜 대신 성장 카운트다운을 사용한다.
"""

from collections import Counter
import json
from pathlib import Path
import random
import shutil
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parent.parent
sys.path.insert(0, str(ROOT))
from verify import farm_oracle, module, read_farms, source_functions

SEED = 2026091502
RUNNER = shutil.which("pypy3")


def case_key(grid, days):
    return days, tuple(tuple(row) for row in grid)


def field_map(n, fields):
    grid = [[1] * n for _ in range(n)]
    for r, c in fields:
        assert 0 < r < n - 1 and 0 < c < n - 1
        grid[r][c] = 0
    return grid


def encode_cases(cases):
    lines = [str(len(cases))]
    for grid, days in cases:
        lines.append(f"{len(grid)} {days}")
        lines.extend(" ".join(map(str, row)) for row in grid)
    return "\n".join(lines) + "\n"


def build_cases():
    rng = random.Random(SEED)
    seen = {case_key(g, m) for g, m in read_farms(HERE / "sample_input.txt")}
    entries = []

    def add(kind, reason, grid, days):
        n = len(grid)
        key = case_key(grid, days)
        assert key not in seen, (kind, reason)
        assert 6 <= n <= 9 and 10 <= days <= 50
        assert all(len(row) == n and all(x in (0, 1) for x in row) for row in grid)
        assert all(grid[0][i] == grid[-1][i] == grid[i][0] == grid[i][-1] == 1 for i in range(n))
        assert any(0 in row for row in grid)
        seen.add(key)
        entries.append({"kind": kind, "reason": reason, "grid": grid, "days": days})

    shapes = [
        ("고립된 농지는 이동·파종 불가", 6, 10, [(2, 2)]),
        ("서로 고립된 여러 농지에서 시작 상태 초기화", 9, 50,
         [(r, c) for r in range(1, 8) for c in range(1, 8) if (r + c) % 2 == 0]),
        ("일자 통로의 후진과 성장 대기", 7, 20, [(r, 3) for r in range(1, 6)]),
        ("꺾인 통로의 회전과 마지막 날 수확", 6, 12,
         [(1, c) for c in range(1, 5)] + [(r, 4) for r in range(2, 5)]),
        ("T자 분기에서 방향 우선순위", 7, 25,
         [(2, c) for c in range(1, 6)] + [(r, 3) for r in range(3, 6)]),
        ("십자 분기와 네 방향 시작", 9, 30,
         [(4, c) for c in range(1, 8)] + [(r, 4) for r in range(1, 8)]),
        ("고리 모양 길의 순환과 재파종", 8, 35,
         [(r, c) for r in range(1, 7) for c in range(1, 7) if r in (1, 6) or c in (1, 6)]),
        ("작은 사각형에서 성숙 농지 진입", 6, 11,
         [(r, c) for r in (2, 3) for c in (2, 3)]),
        ("긴 뱀 모양 통로와 반복 후진", 9, 49,
         [(r, c) for r in (1, 3, 5, 7) for c in range(1, 8)] + [(2, 7), (4, 1), (6, 7)]),
        ("연결되지 않은 두 농장 중 최적 시작 선택", 8, 30,
         [(r, c) for r in (1, 2) for c in (1, 2)] + [(r, 6) for r in range(1, 7)]),
        ("비대칭 분기에서 오른쪽·앞·왼쪽 선택", 8, 38,
         [(3, c) for c in range(1, 7)] + [(r, 2) for r in (1, 2, 4, 5, 6)] + [(4, 5), (5, 5), (5, 6)]),
        ("작은 방과 막다른 출구의 재방문", 7, 50,
         [(r, c) for r in range(1, 4) for c in range(1, 4)] + [(3, 4), (3, 5), (4, 5), (5, 5)]),
    ]
    for reason, n, days, fields in shapes:
        add("boundary", reason, field_map(n, fields), days)

    # 두 칸에서는 12/18/24일에 수확한다. 전날과 당일을 모두 포함한다.
    corridor = field_map(6, [(2, 2), (2, 3)])
    for days in (10, 11, 12, 17, 18, 23, 24, 50):
        add("growth_boundary", f"두 칸 통로, M={days}: 성숙·진입·다음 날 수확과 누적 파종", corridor, days)

    for i in range(15):
        n = 6 + i % 4
        days = (10, 19, 27, 40, 50)[i % 5]
        density = (.18, .4, .68, .9)[i % 4]
        fields = [(r, c) for r in range(1, n - 1) for c in range(1, n - 1) if rng.random() < density]
        fields = fields or [(n // 2, n // 2)]
        add("random", f"농지 밀도 {density:.0%}의 무작위 지도 {i + 1}", field_map(n, fields), days)

    all_fields = {(r, c) for r in range(1, 8) for c in range(1, 8)}
    add("stress", "N=9, M=50, 내부 49칸 전부 농지: 시작 상태 196개", field_map(9, all_fields), 50)
    for obstacle in ((1, 1), (1, 4), (2, 3), (3, 3), (4, 4), (5, 2)):
        add("stress", f"N=9, M=50, 내부 장애물 {obstacle}과 농지 48칸", field_map(9, all_fields - {obstacle}), 50)
    for gap in (2, 6):
        barrier = {(r, 4) for r in range(1, 8) if r != gap}
        add("stress", f"N=9, M=50, 좁은 출입구가 {gap}행에 있는 장벽", field_map(9, all_fields - barrier), 50)
    for i in range(6):
        obstacles = set(rng.sample(sorted(all_fields), 2 + i))
        add("stress", f"N=9, M=50, 장애물 {len(obstacles)}개와 많은 시작 상태", field_map(9, all_fields - obstacles), 50)

    assert len(entries) == 50
    return entries


def run_pypy(path, data, original=False):
    assert RUNNER, "PyPy3 is required for the timing check"
    start = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="ssafy_farm_pypy_") as scratch:
        source = Path(scratch) / "main.py"
        source.write_bytes(path.read_bytes())
        if original:
            (Path(scratch) / "input.txt").write_text(data, encoding="utf-8")
        result = subprocess.run([RUNNER, str(source)], input=data.encode(), cwd=scratch,
                                capture_output=True, check=True, timeout=60)
    assert not result.stderr, result.stderr.decode(errors="replace")
    return result.stdout.decode().replace("\r\n", "\n").strip(), round(time.perf_counter() - start, 4)


def main():
    entries = build_cases()
    solution = module(HERE / "solution.py", "farming_solution")
    original = source_functions(HERE / "original/sol.py")
    total_states = 0
    print("50 unique farm cases generated; checking every start position and direction...", flush=True)
    for i, entry in enumerate(entries, 1):
        grid, days = entry["grid"], entry["days"]
        best, witness, scores = -1, None, []
        for r, line in enumerate(grid):
            for c, cell in enumerate(line):
                if cell:
                    continue
                for d, direction in enumerate(solution.DIRECTIONS):
                    answer, _ = farm_oracle(grid, days, (r, c), direction)
                    initial = [[[-1, -1] if x else [0, 0] for x in row] for row in grid]
                    assert answer == solution.simulate(grid, days, r, c, d), (i, r, c, d)
                    assert answer == original["search"](r, c, (-d) % 4, initial, days), (i, r, c, d)
                    scores.append(answer)
                    if answer > best:
                        best, witness = answer, ((r, c), direction)
        assert best == solution.solve(grid, days), i
        trace = farm_oracle(grid, days, *witness, trace=True)[1]
        planted = Counter(tuple(t["position"]) for t in trace if "번째 파종" in t["action"])
        profile = {"n": len(grid), "days": days, "farmland": len(scores) // 4,
                   "start_states_checked": len(scores), "simulated_days_per_implementation": len(scores) * days,
                   "minimum_over_start_states": min(scores), "maximum_over_start_states": best,
                   "best_start_zero_based": {"position": witness[0], "direction_vector": witness[1]},
                   "best_path_stationary_days": sum(t["position"] == t["next"] for t in trace),
                   "best_path_max_sowings_in_one_cell": max(planted.values(), default=0)}
        entry.update(id=i, answer=best, profile=profile)
        total_states += len(scores)

    assert any(e["profile"]["farmland"] == 49 and e["days"] == 50 for e in entries)
    assert any(e["profile"]["best_path_max_sowings_in_one_cell"] >= 4 for e in entries)
    assert any(e["profile"]["minimum_over_start_states"] < e["answer"] for e in entries)
    answers_by_day = {e["days"]: e["answer"] for e in entries if e["kind"] == "growth_boundary"}
    assert answers_by_day[11] + 1 == answers_by_day[12]
    assert answers_by_day[17] + 1 == answers_by_day[18]
    assert answers_by_day[23] + 1 == answers_by_day[24]

    all_input = encode_cases([(e["grid"], e["days"]) for e in entries])
    all_output = "\n".join(f"#{e['id']} {e['answer']}" for e in entries) + "\n"
    print(f"All {total_states} start states agree. Timing the 50-case PyPy3 batch...", flush=True)
    timings = {}
    for path in (HERE / "solution.py", HERE / "original/sol.py"):
        actual, elapsed = run_pypy(path, all_input, path.parent.name == "original")
        assert actual == all_output.strip()
        timings[path.relative_to(HERE).as_posix()] = elapsed
    (HERE / "generated_input.txt").write_text(all_input, encoding="utf-8")
    (HERE / "generated_output.txt").write_text(all_output, encoding="utf-8")
    report = {"seed": SEED, "generated_count": 50, "distinct_from_original": True,
              "official_testcases": False,
              "bounds": {"n": [6, 9], "days": [10, 50], "mountain_border": True,
                         "note": "Only observed sample bounds are used; official maxima are unknown"},
              "groups": dict(Counter(e["kind"] for e in entries)),
              "oracle": "daily growth countdown and direction-vector rotations",
              "reference_implementations": ["independent countdown oracle", "solution.py", "original/sol.py"],
              "start_states_checked": total_states,
              "runtime": subprocess.check_output([RUNNER, "--version"], stderr=subprocess.STDOUT).decode().strip(),
              "generated_batch_seconds": timings, "time_limit_seconds": 15,
              "within_15_seconds_on_this_machine": all(t <= 15 for t in timings.values()),
              "cases": entries}
    (HERE / "generated_cases.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    problem_path = REPO / "problems/swea/99998.json"
    problem = json.loads(problem_path.read_text(encoding="utf-8"))
    # 한 번 실행하여 50개를 순서대로 처리하도록 원래 SWEA 입력 형식을 유지한다.
    problem["private_testcases"] = [
        {"in": all_input, "out": all_output, "generated": True,
         "source": "reconstructed_rules", "case_count": 50}]
    problem["private_tc_count"] = 1
    problem["tc_stored"] = False
    problem["private_tc_omitted"] = 0
    problem["restoration"]["generated_testcases"] = {
        "count": 50, "input_batches": 1, "seed": SEED, "official": False,
        "verification": "restored/ssafy_a_2026-09-15/2_farming/generated_cases.json"}
    problem_path.write_text(json.dumps(problem, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "cases"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
