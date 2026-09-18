"""충전소 설치의 서로 다른 연습용 50개 입력과 검증 결과를 재생성한다.

설치 좌표 -15..15, 제공 입력에서 관찰한 N=2..10, d=1..11 안에서
기존 경계/고부하 입력을 재현한다. 이후 응시자가 확인한 제한
N<=20, d<=30의 최대 경계까지 다루는 생성기는 아니다.
공식 히든 테스트가 아니며 원본 예제 5개와 중복되지 않는다.
"""

from collections import Counter
import hashlib
import itertools
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
from verify import module, read_houses, source_functions, station_oracle

SEED = 2026091501
RUNNER = shutil.which("pypy3")


def case_key(houses):
    return tuple(sorted(tuple(h) for h in houses))


def encode_cases(cases):
    lines = [str(len(cases))]
    for houses in cases:
        lines.append(str(len(houses)))
        lines.extend("%d %d %d" % tuple(h) for h in houses)
    return "\n".join(lines) + "\n"


def coverage_profile(houses):
    """단일 설치 가능 여부와 입력 순서에 따른 쌍 탐색 작업량을 계산한다."""
    n = len(houses)
    full = (1 << n) - 1
    occupied = {(x, y) for x, y, _ in houses}
    counts = Counter()
    one_cost = float("inf")
    for sx, sy in itertools.product(range(-15, 16), repeat=2):
        if (sx, sy) in occupied:
            continue
        mask, cost = 0, 0
        for i, (x, y, d) in enumerate(houses):
            distance = abs(x - sx) + abs(y - sy)
            cost += distance
            if distance <= d:
                mask |= 1 << i
        counts[mask] += 1
        if mask == full:
            one_cost = min(one_cost, cost)
    checks = feasible_pairs = 0
    if not counts[full]:
        entries = list(counts.items())
        for a, (ma, ca) in enumerate(entries):
            for b in range(a, len(entries)):
                mb, cb = entries[b]
                weight = ca * cb if a != b else ca * (ca - 1) // 2
                missing = full ^ (ma | mb)
                inspected = (missing & -missing).bit_length() if missing else n
                checks += weight * inspected
                if not missing:
                    feasible_pairs += weight
    return {"n": n, "one_station_candidates": counts[full],
            "one_station_cost": None if one_cost == float("inf") else one_cost,
            "valid_station_positions": 961 - n,
            "all_grid_pairs_enumerated_by_user": 0 if counts[full] else 961 * 960 // 2,
            "house_checks_in_user_pair_loop": checks, "feasible_station_pairs": feasible_pairs}


def one_station_case(rng, max_n=10):
    n = rng.randint(2, max_n)
    sx, sy = rng.randint(-11, 11), rng.randint(-11, 11)
    options = [(x, y) for x in range(max(-15, sx - 4), min(15, sx + 4) + 1)
               for y in range(max(-15, sy - 4), min(15, sy + 4) + 1)
               if 1 <= abs(x - sx) + abs(y - sy) <= 7]
    return [(x, y, min(11, abs(x - sx) + abs(y - sy) + rng.randint(0, 3)))
            for x, y in rng.sample(options, n)]


def build_cases():
    rng = random.Random(SEED)
    seen = {case_key(x) for x in read_houses(HERE / "sample_input.txt")}
    result = []

    def add(kind, reason, houses):
        key = case_key(houses)
        assert key not in seen, (kind, reason)
        assert 2 <= len(houses) <= 10 and len({(x, y) for x, y, _ in houses}) == len(houses)
        assert all(-15 <= x <= 15 and -15 <= y <= 15 and 1 <= d <= 11 for x, y, d in houses)
        seen.add(key)
        result.append({"kind": kind, "reason": reason, "houses": houses})

    designs = [
        ("양 끝 모서리와 최소 허용 거리", [(-15, -15, 1), (15, 15, 1)]),
        ("인접한 두 집 위에는 설치 불가", [(0, 0, 1), (1, 0, 1)]),
        ("경계선 위의 유일한 공통 위치", [(-15, -1, 1), (-15, 1, 1)]),
        ("모서리 부근과 동률 최적 위치", [(-15, -15, 2), (-14, -14, 2)]),
        ("거리 합보다 설치 1개를 우선", [(-2, 0, 3), (0, 0, 3), (2, 0, 3)]),
        ("허용 거리와 정확히 같은 위치", [(-1, 0, 1), (1, 0, 1), (0, 1, 1)]),
        ("서로 떨어진 세 권역은 2개로 불가능", [(-15, -15, 1), (0, 0, 1), (15, 15, 1)]),
        ("공통 교점이 집으로 막힘", [(-1, 0, 1), (1, 0, 1), (0, 0, 1)]),
        ("밀집한 집 때문에 중앙 집의 허용 위치 없음", [(x, y, 1) for x in (-1, 0, 1) for y in (-1, 0, 1)]),
        ("N=10 직선 배치와 짝수 개 중앙값", [(0, y, 11) for y in range(-5, 5)]),
        ("좌표 양쪽 경계의 두 군집", [(-15, -2, 2), (-15, 2, 2), (15, -2, 2), (15, 2, 2)]),
        ("집마다 다른 허용 거리", [(-7, 0, 1), (-6, 1, 3), (7, 0, 1), (6, -1, 3), (0, 0, 11)]),
    ]
    for reason, houses in designs:
        add("boundary", reason, houses)
    for i in range(10):
        add("one_station", f"단일 충전소를 보장한 무작위 배치 {i + 1}", one_station_case(rng))
    for i in range(10):
        n = rng.randint(4, 10)
        houses = []
        for center, count in (((-12, rng.randint(-8, 8)), n // 2),
                              ((12, rng.randint(-8, 8)), n - n // 2)):
            sx, sy = center
            offsets = [(dx, dy) for dx in range(-2, 3) for dy in range(-2, 3) if 1 <= abs(dx) + abs(dy) <= 3]
            for dx, dy in rng.sample(offsets, count):
                houses.append((sx + dx, sy + dy, abs(dx) + abs(dy) + rng.randint(0, 2)))
        add("two_stations", f"분리된 두 군집과 서로 다른 허용 거리 {i + 1}", houses)
    for i in range(8):
        n = rng.randint(6, 10)
        group_sizes = [n // 3, n // 3, n - 2 * (n // 3)]
        houses = []
        for (sx, sy), count in zip(((-13, -13), (13, -13), (0, 13)), group_sizes):
            options = [(dx, dy) for dx in range(-1, 2) for dy in range(-1, 2) if (dx, dy) != (0, 0)]
            houses.extend((sx + dx, sy + dy, rng.randint(1, 3)) for dx, dy in rng.sample(options, count))
        add("impossible", f"세 권역을 각각 담당해야 하는 배치 {i + 1}", houses)
    centers = [(0, 0), (2, 0), (-2, 1), (0, -2), (4, 3), (-4, -3), (2, -4), (-3, 4), (5, -5), (-5, 5)]
    for i, (cx, cy) in enumerate(centers):
        dense = [(cx + dx, cy + dy, 11) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
        if i < 7:
            far = (-15 if cx >= 0 else 15, -15 if cy >= 0 else 15, 1 + i % 2)
            houses = dense + [far]
            reason = "N=10, 앞 9개는 넓은 허용 거리, 마지막 먼 집에서 늦게 탈락"
        else:
            houses = dense[:7] + [(-15, -15, 1), (15, -15, 1), (0, 15, 1)]
            reason = "N=10, 앞 7개 검사 후 뒤의 세 권역 때문에 설치 불가능"
        add("stress", f"{reason} ({i + 1})", houses)
    assert len(result) == 50
    return result


def run(path, data, timeout=180, cwd=None):
    start = time.perf_counter()
    assert RUNNER, "PyPy3 is required for the requested timing check"
    # 설치된 구버전 Windows PyPy의 한글 경로 문제를 피해 동일한 바이트를 실행한다.
    with tempfile.TemporaryDirectory(prefix="ssafy_pypy_") as scratch:
        executable_source = Path(scratch) / "main.py"
        executable_source.write_bytes(path.read_bytes())
        completed = subprocess.run([RUNNER, str(executable_source)], input=data.encode(),
                                   capture_output=True, cwd=cwd, timeout=timeout, check=True)
    assert not completed.stderr, completed.stderr.decode(errors="replace")
    return completed.stdout.decode().replace("\r\n", "\n").strip(), round(time.perf_counter() - start, 4)


def main():
    entries = build_cases()
    solution = module(HERE / "solution.py", "charging_solution")
    original = source_functions(HERE / "original/sol.py")
    original2 = source_functions(HERE / "original/sol2.py")
    print("50 unique cases generated; checking independent oracle and both original solutions...", flush=True)
    for i, entry in enumerate(entries, 1):
        houses = entry["houses"]
        answer = station_oracle(houses)
        original.update(N=len(houses), data=houses)
        original2["N"] = len(houses)
        assert solution.solve(houses) == original["solve"]() == original2["solve"](houses) == answer, i
        profile = coverage_profile(houses)
        branch = "one" if profile["one_station_candidates"] else "impossible" if answer == -1 else "two"
        if entry["kind"] == "one_station":
            assert branch == "one"
        if entry["kind"] == "two_stations":
            assert branch == "two"
        if entry["kind"] == "impossible":
            assert branch == "impossible"
        entry.update(id=i, answer=answer, branch=branch, profile=profile)
    all_input = encode_cases([e["houses"] for e in entries])
    all_output = "\n".join(f"#{e['id']} {e['answer']}" for e in entries) + "\n"
    (HERE / "generated_input.txt").write_text(all_input, encoding="utf-8")
    (HERE / "generated_output.txt").write_text(all_output, encoding="utf-8")

    user_files = list((REPO / "swea").glob("99997_*.py"))
    assert len(user_files) == 1
    user_path = user_files[0]
    print("Answers verified. Timing the user's exact saved code on the 50-case batch...", flush=True)
    user_output, user_seconds = run(user_path, all_input)
    assert user_output == all_output.strip(), "user code differs on generated 50"
    ref_output, ref_seconds = run(HERE / "solution.py", all_input)
    assert ref_output == all_output.strip()
    original_output, original_seconds = run(user_path, (HERE / "sample_input.txt").read_text())
    assert original_output == (HERE / "sample_output.txt").read_text().strip()
    stress = [e for e in entries if e["kind"] == "stress"] * 5
    stress_output = "\n".join(f"#{i} {e['answer']}" for i, e in enumerate(stress, 1))
    stress_actual, stress_seconds = run(user_path, encode_cases([e["houses"] for e in stress]))
    assert stress_actual == stress_output
    print(f"User code: 50/50 correct, {user_seconds}s; original 5/5 correct. Checking 2,000 additional single-station random cases...", flush=True)

    # 그대로 컴파일한 제출 코드에 입력/출력 함수만 제공한다. 범위와 계산은 변경하지 않는다.
    compiled_user = compile(user_path.read_text(encoding="utf-8"), str(user_path), "exec")
    rng = random.Random(SEED + 1)
    for _ in range(2000):
        houses = one_station_case(rng, max_n=6)
        expected = station_oracle(houses)
        values, lines = iter(encode_cases([houses]).splitlines()), []
        exec(compiled_user, {"input": lambda: next(values), "print": lambda *args: lines.append(" ".join(map(str, args)))})
        assert lines == [f"#1 {expected}"], houses

    # 원문이 없으므로 중복 좌표 허용 여부는 별도 조건으로 기록한다.
    duplicate = [(0, 0, 1), (0, 0, 1)]
    duplicate_output, _ = run(user_path, encode_cases([duplicate]))
    duplicate_reference = station_oracle(duplicate)

    report = {
        "seed": SEED, "generated_count": 50, "distinct_from_original": True,
        "official_testcases": False,
        "bounds": {"n": [2, 10], "coordinates": [-15, 15], "d": [1, 11],
                   "note": "N and d use observed sample bounds; official maxima are unknown"},
        "groups": dict(Counter(e["kind"] for e in entries)),
        "answers_by_branch": dict(Counter(e["branch"] for e in entries)),
        "oracle": "independent partition of houses; all grid coordinates examined",
        "reference_implementations": ["independent partition oracle", "solution.py", "original/sol.py", "original/sol2.py"],
        "user_code": {"file": user_path.relative_to(REPO).as_posix(),
                      "sha256": hashlib.sha256(user_path.read_bytes()).hexdigest(),
                      "original_sample_passed": 5, "generated_passed": 50,
                      "additional_single_station_random_passed": 2000,
                      "correctness_assumption": "all house coordinates are distinct; original guarantee unknown",
                      "conditional_duplicate_coordinate_case": {
                          "houses": duplicate, "reference_answer": duplicate_reference,
                          "user_output": duplicate_output, "included_in_published_tests": False},
                      "runtime": subprocess.check_output([RUNNER, "--version"], stderr=subprocess.STDOUT).decode().strip(),
                      "generated_batch_seconds": user_seconds,
                      "sample_batch_seconds": original_seconds, "time_limit_seconds": 15,
                      "within_15_seconds_on_this_machine": user_seconds <= 15,
                      "stress_50_repeated_seconds": stress_seconds,
                      "stress_50_note": "10 distinct stress cases repeated five times; separate timing check, not the published dataset",
                      "stress_within_15_seconds_on_this_machine": stress_seconds <= 15},
        "reference_batch_seconds": ref_seconds,
        "cases": entries,
    }
    (HERE / "generated_cases.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # SWEA처럼 한 프로세스에서 T=50을 처리한다. 케이스마다 PyPy를 재시작하면
    # JIT 초기화가 반복되어 시험과 다른 시간 초과가 생길 수 있다.
    problem_path = REPO / "problems/swea/99997.json"
    problem = json.loads(problem_path.read_text(encoding="utf-8"))
    problem["private_testcases"] = [
        {"in": all_input, "out": all_output, "generated": True,
         "source": "reconstructed_rules", "case_count": 50}]
    problem["private_tc_count"] = 1
    problem["tc_stored"] = False
    problem["private_tc_omitted"] = 0
    problem["restoration"]["generated_testcases"] = {
        "count": 50, "input_batches": 1, "seed": SEED, "official": False,
        "verification": "restored/ssafy_a_2026-09-15/1_charging_stations/generated_cases.json"}
    problem_path.write_text(json.dumps(problem, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "cases"}, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
