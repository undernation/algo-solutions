"""복원 규칙 검증. Python 표준 라이브러리만 사용한다.

python restored/ssafy_a_2026-09-15/verify.py

1번: 집을 두 그룹으로 분할하고 그룹별 최적 충전소를 독립 계산.
2번: 각 농지의 남은 성장 일수를 매일 줄이는 별도 시뮬레이션.
공식 출력이 없으므로 이 검증은 원문과의 일치를 증명하지 않는다.
"""

import ast
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import time


ROOT = Path(__file__).resolve().parent
P1 = ROOT / "1_charging_stations"
P2 = ROOT / "2_farming"


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def source_functions(path):
    """원본을 수정하지 않고 함수와 방향 상수만 읽어 파일 입력을 피한다."""
    parsed = ast.parse(path.read_text(encoding="utf-8-sig"))
    body = [node for node in parsed.body if isinstance(node, ast.FunctionDef)
            or (isinstance(node, ast.Assign) and all(
                isinstance(t, ast.Name) and t.id in ("dx", "dy")
                for t in node.targets))]
    namespace = {}
    exec(compile(ast.Module(body=body, type_ignores=[]), str(path), "exec"), namespace)
    return namespace


def read_houses(path):
    data = iter(map(int, path.read_text().split()))
    cases = []
    for _ in range(next(data)):
        cases.append([tuple(next(data) for _ in range(3))
                      for _ in range(next(data))])
    assert next(data, None) is None
    return cases


def read_farms(path):
    data = iter(map(int, path.read_text().split()))
    cases = []
    for _ in range(next(data)):
        n, days = next(data), next(data)
        cases.append(([[next(data) for _ in range(n)] for _ in range(n)], days))
    assert next(data, None) is None
    return cases


def station_oracle(houses):
    """충전소 쌍을 열거하지 않고, 집 배정의 모든 분할을 비교한다."""
    n = len(houses)
    full = (1 << n) - 1
    best = [float("inf")] * (1 << n)
    best[0] = 0
    occupied = {(x, y) for x, y, _ in houses}
    for sx, sy in itertools.product(range(-15, 16), repeat=2):
        if (sx, sy) in occupied:
            continue
        distances = [abs(sx - x) + abs(sy - y) for x, y, _ in houses]
        cover = [i for i, (_, _, d) in enumerate(houses) if distances[i] <= d]
        # 이 충전소에 배정할 수 있는 모든 집 부분집합과 그 거리 합.
        assignments = [(0, 0)]
        for i in cover:
            assignments += [(mask | (1 << i), cost + distances[i])
                            for mask, cost in assignments]
        for mask, cost in assignments:
            best[mask] = min(best[mask], cost)
    if best[full] != float("inf"):
        return best[full]
    answer = min(best[mask] + best[full ^ mask] for mask in range(1 << n))
    return -1 if answer == float("inf") else answer


def farm_oracle(grid, days, start, direction, trace=False):
    """성숙 날짜 대신 성장 카운트다운과 방향 벡터를 사용한다."""
    fields = {(r, c) for r, line in enumerate(grid)
              for c, value in enumerate(line) if value == 0}
    remaining, planted_count = {}, dict.fromkeys(fields, 0)
    pos, forward = start, direction
    harvest, log = 0, []
    for day in range(1, days + 1):
        remaining = {p: max(0, left - 1) for p, left in remaining.items()}
        dr, dc = forward
        movement = None
        for delta in ((dc, -dr), forward, (-dc, dr), (-dr, -dc)):
            target = pos[0] + delta[0], pos[1] + delta[1]
            if target in fields and remaining.get(target, 0) == 0:
                movement = target, delta
                break
        before = pos
        action = "대기"
        if pos not in remaining:
            if movement is not None:
                planted_count[pos] += 1
                remaining[pos] = 4 + planted_count[pos]
                action = f"{planted_count[pos]}번째 파종 (성숙: {day + remaining[pos]}일)"
        elif remaining[pos] == 0:
            del remaining[pos]
            harvest += 1
            action = "수확"
        if movement is not None:
            pos, forward = movement
        if trace:
            log.append({"day": day, "position": before, "action": action,
                        "next": pos, "harvest": harvest})
    return harvest, log


def farm_best(grid, days, get_trace=False):
    best, witness = -1, None
    for r, line in enumerate(grid):
        for c, value in enumerate(line):
            if value == 0:
                for direction in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                    answer, _ = farm_oracle(grid, days, (r, c), direction)
                    if answer > best:
                        best, witness = answer, ((r, c), direction)
    if witness is None:
        return 0, None
    return best, (farm_oracle(grid, days, *witness, trace=True)[1]
                  if get_trace else witness)


def run_script(path, input_bytes, cwd=None):
    start = time.perf_counter()
    result = subprocess.run([sys.executable, str(path)], input=input_bytes,
                            capture_output=True, cwd=cwd, timeout=60, check=True)
    assert not result.stderr, result.stderr.decode(errors="replace")
    return result.stdout.decode().replace("\r\n", "\n").strip(), time.perf_counter() - start


def main():
    rng = random.Random(20260915)
    started = time.perf_counter()
    one = module(P1 / "solution.py", "stations")
    two = module(P2 / "solution.py", "farming")
    source1 = source_functions(P1 / "original/sol.py")
    source1b = source_functions(P1 / "original/sol2.py")
    source2 = source_functions(P2 / "original/sol.py")
    houses = read_houses(P1 / "sample_input.txt")
    farms = read_farms(P2 / "sample_input.txt")
    expected = [[station_oracle(case) for case in houses],
                [farm_best(grid, days)[0] for grid, days in farms]]
    sample_runs = {}
    for folder, answers in ((P1, expected[0]), (P2, expected[1])):
        output = "\n".join(f"#{i} {v}" for i, v in enumerate(answers, 1))
        assert (folder / "sample_output.txt").read_text().strip() == output
        for script in [folder / "solution.py", *sorted((folder / "original").glob("sol*.py"))]:
            actual, elapsed = run_script(script, (folder / "sample_input.txt").read_bytes(),
                                         script.parent)
            assert actual == output, (script.name, actual, output)
            sample_runs[script.relative_to(ROOT).as_posix()] = round(elapsed, 4)

    # 거리 최적화보다 1개 설치 우선, 집 좌표 금지, 경계, 정확히 d, 불가능.
    boundaries = [([(0, 0, 0)], -1), ([(15, 15, 1)], 1),
                  ([(0, 0, 1), (1, 0, 1)], 2),
                  ([(0, 0, 3), (2, 0, 3), (4, 0, 3)], 5),
                  ([(-15, -15, 1), (15, 15, 1)], 2),
                  ([(-15, -15, 1), (0, 0, 1), (15, 15, 1)], -1),
                  ([(-15, 0, 1), (-13, 0, 1)], 2)]
    for case, answer in boundaries:
        assert station_oracle(case) == one.solve(case) == answer

    for case in houses + [x[0] for x in boundaries]:
        answer = one.solve(case)
        source1.update(N=len(case), data=case)
        source1b["N"] = len(case)
        assert source1["solve"]() == source1b["solve"](case) == answer

    for i in range(2000):
        n = rng.randint(1, 6)
        points = rng.sample(list(itertools.product(range(-15, 16), repeat=2)), n)
        case = [(x, y, rng.randint(0, 7)) for x, y in points]
        assert one.solve(case) == station_oracle(case), case
        # 느린 원본의 후보 961개 쌍 열거도 일부 무작위 입력에 직접 대조.
        if i < 80:
            source1.update(N=n, data=case)
            source1b["N"] = n
            assert source1["solve"]() == source1b["solve"](case) == one.solve(case)

    # 원본과 복원 풀이의 시작 상태별 결과도 확인하여 max가 오류를 가리지 않게 한다.
    farming_states = 0
    for i in range(2000):
        n, days = rng.randint(1, 4), rng.randint(1, 60)
        grid = [[int(rng.random() < .35) for _ in range(n)] for _ in range(n)]
        grid[rng.randrange(n)][rng.randrange(n)] = 0
        assert two.solve(grid, days) == farm_best(grid, days)[0], (grid, days)
        for r, line in enumerate(grid):
            for c, cell in enumerate(line):
                if cell:
                    continue
                for d, direction in enumerate(two.DIRECTIONS):
                    expected_state = farm_oracle(grid, days, (r, c), direction)[0]
                    assert two.simulate(grid, days, r, c, d) == expected_state
                    initial = [[[-1, -1] if x else [0, 0] for x in line] for line in grid]
                    assert source2["search"](r, c, (-d) % 4, initial, days) == expected_state
                    farming_states += 1

    # 모든 작은 지형과 성장 경계 날짜: 고립, 회전/후진, 재파종을 포함한다.
    exhaustive = 0
    for mask in range(1 << 4):
        grid = [[(mask >> (r * 2 + c)) & 1 for c in range(2)] for r in range(2)]
        for days in (1, 4, 5, 6, 7, 10, 11, 12, 20, 40):
            assert two.solve(grid, days) == farm_best(grid, days)[0]
            exhaustive += 1
    assert two.solve([[0]], 60) == 0

    # 공식 상한은 미확인이므로 제공 입력의 최대 크기에 맞춘 별도 부하 측정이다.
    stress_houses = [(-15, y, 15) for y in range(-2, 3)] + [(15, y, 15) for y in range(-2, 3)]
    start = time.perf_counter()
    station_stress = one.solve(stress_houses)
    station_seconds = time.perf_counter() - start
    assert station_stress == station_oracle(stress_houses)
    start = time.perf_counter()
    farm_stress = two.solve([[0] * 9 for _ in range(9)], 50)
    farm_seconds = time.perf_counter() - start
    assert farm_stress == farm_best([[0] * 9 for _ in range(9)], 50)[0]

    manifest = json.loads((ROOT / "source_manifest.json").read_text(encoding="utf-8"))
    for entry in manifest["files"]:
        actual_hash = hashlib.sha256((ROOT / entry["archived_path"]).read_bytes()).hexdigest()
        assert actual_hash == entry["sha256"], entry

    # 응시자가 기억한 '50개 합산 약 10초' 형식에 맞춘 반복 입력 측정.
    # 제공 입력을 반복했으므로 원문의 미공개/최악 테스트 통과를 의미하지 않는다.
    batches = {}
    for folder, answers in ((P1, expected[0]), (P2, expected[1])):
        original_input = (folder / "sample_input.txt").read_text().splitlines()
        repeats = 50 // len(answers)
        input50 = ("50\n" + ("\n".join(original_input[1:]).rstrip() + "\n") * repeats).encode()
        output50 = "\n".join(f"#{i} {v}" for i, v in enumerate(answers * repeats, 1))
        with tempfile.TemporaryDirectory(prefix="ssafy_a_50tc_") as scratch:
            (Path(scratch) / "input.txt").write_bytes(input50)
            for script in [folder / "solution.py", *sorted((folder / "original").glob("sol*.py"))]:
                actual, elapsed = run_script(script, input50, scratch)
                assert actual == output50
                batches[script.relative_to(ROOT).as_posix()] = round(elapsed, 4)

    _, sample_start = farm_best(*farms[0])
    report = {"seed": 20260915, "official_outputs_available": False,
              "sample_case_counts": [len(houses), len(farms)], "sample_answers": expected,
              "sample_script_seconds": sample_runs, "station_random_cases": 2000,
              "station_original_random_cases": 80, "station_boundary_cases": len(boundaries),
              "farming_random_cases": 2000, "farming_start_states": farming_states,
              "farming_exhaustive_cases": exhaustive,
              "repeated_provided_50_case_batch_seconds": batches,
              "observed_size_stress": {
                  "stations_N10": {"answer": station_stress, "seconds": round(station_seconds, 4)},
                  "farm_N9_M50": {"answer": farm_stress, "seconds": round(farm_seconds, 4)}},
              "first_farm_sample_start": {"position": sample_start[0], "direction": sample_start[1]},
              "first_farm_sample_optimal_trace": farm_best(*farms[0], get_trace=True)[1],
              "seconds": round(time.perf_counter() - started, 3)}
    (ROOT / "verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                                           encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if "trace" not in k}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
