"""Read-only audit of the restored farm examples (not an official judge).

python -B restored/ssafy_a_2026-09-15/2_farming/audit_examples.py
Add --report to save example_audit.json next to this script.

The oracle models seed -> sprout -> ripe as separate daily transitions from
reference_statement.png. It neither imports the previous countdown oracle nor
uses an absolute maturity date to decide whether a field is ripe. Starting
position/direction selection remains a reconstruction from the supplied code.
Only the optional audit report is written; submissions and tests are read-only.
"""

import argparse
import ast
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import re
import shutil
import subprocess
import sys
import tempfile


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PROBLEM = REPO / "problems/swea/99998.json"
PRIVATE = REPO / "_meta/tc_store/swea/99998.json"
DIRECTIONS = {"E": (0, 1), "S": (1, 0), "W": (0, -1), "N": (-1, 0)}
RIGHT = {"N": "E", "E": "S", "S": "W", "W": "N"}
ORIGINAL_DIRECTION = {"E": 0, "N": 1, "W": 2, "S": 3}
RESTORED_DIRECTION = {"E": 0, "S": 1, "W": 2, "N": 3}
EXPECTED_IMAGE_SHA256 = "29feba91ad19f60be97c909bea79fe9255f884e3aca25ecbe4ecfc2c0094d7c1"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def parse_cases(text):
    tokens = iter(map(int, text.split()))
    cases = []
    for _ in range(next(tokens)):
        n, days = next(tokens), next(tokens)
        grid = [[next(tokens) for _ in range(n)] for _ in range(n)]
        assert n > 0 and days > 0
        assert all(x in (0, 1) for row in grid for x in row)
        cases.append((grid, days))
    assert next(tokens, None) is None
    return cases


def parse_answers(text):
    answers = []
    for number, line in enumerate(text.strip().splitlines(), 1):
        label, answer = line.split()
        assert label == "#{}".format(number), line
        answers.append(int(answer))
    return answers


def case_key(grid, days):
    return days, tuple(tuple(row) for row in grid)


def simulate(grid, days, position, facing):
    fields = {(r, c) for r, row in enumerate(grid)
              for c, value in enumerate(row) if value == 0}
    # value: [phase, days since sprouting]; empty fields have no crop entry.
    crops, sprout_counts = {}, dict.fromkeys(fields, 0)
    harvested, trace = 0, []

    def destinations():
        order = (RIGHT[facing], facing, RIGHT[RIGHT[RIGHT[facing]]],
                 RIGHT[RIGHT[facing]])
        for direction in order:
            dr, dc = DIRECTIONS[direction]
            target = position[0] + dr, position[1] + dc
            if target in fields and (target not in crops or crops[target][0] == "ripe"):
                yield target, direction

    for day in range(1, days + 1):
        growth = []
        for cell, crop in crops.items():
            if crop[0] == "seed":
                crop[:] = ["sprout", 0]
                sprout_counts[cell] += 1
                growth.append({"position": list(cell), "phase": "sprout"})
            elif crop[0] == "sprout":
                crop[1] += 1
                if crop[1] == 3 + sprout_counts[cell]:
                    crop[0] = "ripe"
                    growth.append({"position": list(cell), "phase": "ripe"})

        morning, action, planting_number = position, "wait", None
        if position not in crops:
            if next(destinations(), None) is not None:
                crops[position] = ["seed", 0]
                action, planting_number = "plant", sprout_counts[position] + 1
        elif crops[position][0] == "ripe":
            del crops[position]
            harvested += 1
            action = "harvest"
        else:
            raise AssertionError("robot cannot begin a day on a growing crop")

        # Select movement after morning work; only the current field changed.
        move = next(destinations(), None)
        if move is not None:
            position, facing = move
        trace.append({"day": day, "position": list(morning), "action": action,
                      "planting_number": planting_number, "next": list(position),
                      "facing_after_move": facing, "harvest": harvested,
                      "growth": growth})
    return harvested, trace


def load_restored():
    spec = importlib.util.spec_from_file_location("farm_restored_audit", HERE / "solution.py")
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def load_original():
    # Load the preserved original functions without executing its file input.
    path = HERE / "original/sol.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    body = [node for node in tree.body if isinstance(node, ast.FunctionDef)
            or (isinstance(node, ast.Assign) and all(
                isinstance(t, ast.Name) and t.id in ("dx", "dy")
                for t in node.targets))]
    namespace = {}
    exec(compile(ast.Module(body=body, type_ignores=[]), str(path), "exec"), namespace)
    return namespace


def run_batch(path, data, runner, original=False):
    with tempfile.TemporaryDirectory(prefix="farm_example_audit_") as folder:
        # Old Windows PyPy cannot reliably open a Korean filename. Execute a
        # byte-identical temporary copy; never rewrite the saved submission.
        program = Path(folder, "main.py")
        program.write_bytes(path.read_bytes())
        if original:
            Path(folder, "input.txt").write_text(data, encoding="utf-8")
        result = subprocess.run([runner, "-B", str(program)], input=data.encode("utf-8"),
                                cwd=folder, capture_output=True, timeout=60)
    assert result.returncode == 0, (str(path), result.stderr.decode(errors="replace"))
    assert not result.stderr, result.stderr.decode(errors="replace")
    return parse_answers(result.stdout.decode("utf-8"))


def check_table(text, trace, extended_trace):
    rows = [line for line in text.splitlines() if re.match(r"^\| \d+ \|", line)]
    assert len(rows) == len(trace) == 11
    assert "(2, 4)에서 북쪽" in text and "1부터 시작" in text
    for line, event in zip(rows, trace):
        columns = [v.strip() for v in line.strip("|").split("|")]
        coordinates = lambda s: tuple(map(int, re.findall(r"\d+", s)))
        assert int(columns[0]) == event["day"]
        assert coordinates(columns[1]) == tuple(x + 1 for x in event["position"])
        assert coordinates(columns[3]) == tuple(x + 1 for x in event["next"])
        assert int(columns[4]) == event["harvest"]
        if event["action"] == "harvest":
            assert columns[2] == "수확"
        else:
            assert event["action"] == "plant"
            k = event["planting_number"]
            assert ("첫 파종" if k == 1 else "두 번째 파종") in columns[2]
            ripening_day = next(future["day"] for future in extended_trace
                                if future["day"] > event["day"] and any(
                                    g["position"] == event["position"] and g["phase"] == "ripe"
                                    for g in future["growth"]))
            assert coordinates(columns[2]) == (ripening_day,)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", action="store_true")
    args = parser.parse_args()
    submitted, = list((REPO / "swea").glob("99998_*.py"))
    paths = [PROBLEM, submitted, REPO / "_meta/history.json", HERE / "README.md",
             HERE / "reference_statement.png", HERE / "solution.py", HERE / "generate_cases.py",
             HERE / "sample_input.txt", HERE / "sample_output.txt", HERE / "generated_input.txt",
             HERE / "generated_output.txt", HERE / "generated_cases.json",
             *sorted((HERE / "original").iterdir())]
    if PRIVATE.exists():
        paths.append(PRIVATE)
    before = {p.relative_to(REPO).as_posix(): digest(p) for p in paths}
    assert digest(HERE / "reference_statement.png") == EXPECTED_IMAGE_SHA256
    assert (HERE / "original/output.txt").stat().st_size == 0
    problem = read_json(PROBLEM)
    assert problem["restoration"]["official_outputs_available"] is False
    assert problem["restoration"]["statement_reference"]["sha256"] == EXPECTED_IMAGE_SHA256

    restored, original = load_restored(), load_original()
    cache, checked_states = {}, 0

    def validate(grid, days):
        nonlocal checked_states
        key = case_key(grid, days)
        if key in cache:
            return cache[key]
        scores = []
        for r, row in enumerate(grid):
            for c, value in enumerate(row):
                if value:
                    continue
                for facing in DIRECTIONS:
                    answer, _ = simulate(grid, days, (r, c), facing)
                    state = [[[-1, -1] if x else [0, 0] for x in line] for line in grid]
                    assert answer == restored.simulate(grid, days, r, c, RESTORED_DIRECTION[facing])
                    assert answer == original["search"](r, c, ORIGINAL_DIRECTION[facing], state, days)
                    scores.append(answer)
        best = max(scores, default=0)
        assert best == restored.solve(grid, days)
        checked_states += len(scores)
        cache[key] = best
        return best

    generated = read_json(HERE / "generated_cases.json")
    batch_data = {name: (HERE / (name + "_input.txt")).read_text(encoding="utf-8")
                  for name in ("sample", "generated")}
    answers, file_batches = {}, {}
    for name, data in batch_data.items():
        cases = parse_cases(data)
        answers[name] = [validate(grid, days) for grid, days in cases]
        assert answers[name] == parse_answers((HERE / (name + "_output.txt")).read_text())
        file_batches[name] = len(cases)
    stored_states = checked_states
    assert batch_data["sample"] == (HERE / "original/input.txt").read_text(encoding="utf-8")
    expected_generated = [(e["grid"], e["days"]) for e in generated["cases"]]
    assert expected_generated == parse_cases(batch_data["generated"])
    assert [e["answer"] for e in generated["cases"]] == answers["generated"]
    assert generated["official_testcases"] is False
    assert generated["generated_count"] == len(expected_generated) == 50
    generated_keys = {case_key(g, d) for g, d in expected_generated}
    sample_keys = {case_key(g, d) for g, d in parse_cases(batch_data["sample"])}
    assert len(generated_keys) == 50 and not generated_keys & sample_keys

    # Run only the input builder, never the generator's writing/timing main().
    spec = importlib.util.spec_from_file_location("farm_generator_audit", HERE / "generate_cases.py")
    generator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generator)
    rebuilt = generator.build_cases()
    assert [(e["grid"], e["days"]) for e in rebuilt] == expected_generated
    assert [(e["kind"], e["reason"]) for e in rebuilt] == [
        (e["kind"], e["reason"]) for e in generated["cases"]]
    assert dict(Counter(e["kind"] for e in rebuilt)) == generated["groups"]

    stores = [("public_problem", problem)]
    if PRIVATE.exists():
        stores.append(("ignored_local_tc_store", read_json(PRIVATE)))
    store_checks, cli_batches = {}, dict(batch_data)
    for store_name, store in stores:
        groups = {}
        for key in ("samples", "private_testcases"):
            counts = []
            for index, batch in enumerate(store.get(key, []), 1):
                cases = parse_cases(batch["in"])
                actual = [validate(grid, days) for grid, days in cases]
                assert actual == parse_answers(batch["out"]), (store_name, key, index)
                if "case_count" in batch:
                    assert batch["case_count"] == len(cases)
                counts.append(len(cases))
                if batch["in"] not in cli_batches.values():
                    cli_batches["{}_{}_{}".format(store_name, key, index)] = batch["in"]
            groups[key] = {"batches": len(counts), "cases_per_batch": counts}
        store_checks[store_name] = groups
    assert problem["samples"][0]["in"] == batch_data["sample"]
    assert problem["private_testcases"][0]["in"] == batch_data["generated"]
    assert problem["private_testcases"][0]["generated"] is True
    assert problem["private_testcases"][0]["source"] == "reconstructed_rules"
    assert problem["sample_case_count"] == 10 and problem["private_tc_count"] == 1

    grid, days = parse_cases(batch_data["sample"])[0]
    first_answer, first_trace = simulate(grid, days, (1, 3), "N")
    assert first_answer == answers["sample"][0] == 4
    check_table(problem["examples_text"], first_trace, simulate(grid, 20, (1, 3), "N")[1])
    previous = read_json(HERE.parent / "verification.json")
    assert previous["sample_answers"][1] == answers["sample"]
    assert len(previous["first_farm_sample_optimal_trace"]) == len(first_trace)
    for old, new in zip(previous["first_farm_sample_optimal_trace"], first_trace):
        assert all(old[key] == new[key] for key in ("day", "position", "next", "harvest"))
    readme = (HERE / "README.md").read_text(encoding="utf-8")
    assert "```text\n" + batch_data["sample"].strip() + "\n```" in readme
    assert "```text\n" + (HERE / "sample_output.txt").read_text().strip() + "\n```" in readme

    # Hand-checkable two-field path: maturity, entry, and harvest are distinct.
    corridor = [[1] * 6 for _ in range(6)]
    corridor[2][2] = corridor[2][3] = 0
    _, corridor_trace = simulate(corridor, 50, (2, 2), "E")
    harvest_days = [e["day"] for e in corridor_trace if e["action"] == "harvest"]
    assert harvest_days == [7, 12, 18, 24, 31, 38, 46]
    assert corridor_trace[0]["action"] == "plant"
    assert corridor_trace[1]["growth"] == [{"position": [2, 2], "phase": "sprout"}]
    assert corridor_trace[5]["growth"] == [{"position": [2, 2], "phase": "ripe"}]
    assert corridor_trace[5]["next"] == [2, 2] and corridor_trace[5]["harvest"] == 0
    assert corridor_trace[6]["position"] == corridor_trace[6]["next"]  # harvest while blocked
    boundary_answers = {}
    for day in (1, 5, 6, 7, 10, 11, 12, 17, 18, 23, 24, 30, 31, 37, 38, 45, 46, 50):
        answer = validate(corridor, day)
        assert answer == sum(d <= day for d in harvest_days)
        boundary_answers[str(day)] = answer

    # Covers no-field, isolated, all-edge, and direction cases outside unknown
    # official bounds as synthetic logic checks, not as claimed valid exam data.
    for mask in range(16):
        tiny = [[(mask >> (2 * r + c)) & 1 for c in range(2)] for r in range(2)]
        for days in range(1, 36):
            validate(tiny, days)
    rng = random.Random(2026092702)
    for _ in range(250):
        n, days = rng.randint(2, 6), rng.randint(1, 60)
        density = rng.uniform(0.15, 0.95)
        validate([[int(rng.random() > density) for _ in range(n)] for _ in range(n)], days)

    runner = shutil.which("pypy3") or sys.executable
    programs = [HERE / "solution.py", HERE / "original/sol.py", submitted]
    cli_checks = {}
    for name, data in cli_batches.items():
        expected = [validate(grid, days) for grid, days in parse_cases(data)]
        for program in programs:
            assert run_batch(program, data, runner, program.parent.name == "original") == expected
        cli_checks[name] = {"cases": len(expected), "programs_passed": len(programs)}

    after = {p.relative_to(REPO).as_posix(): digest(p) for p in paths}
    assert before == after, "An audited source changed during this run; rerun on a stable snapshot"
    report = {
        "result": "PASS: no numeric correction required",
        "official_outputs_available": False,
        "rule_evidence": {
            "reference_image_sha256": EXPECTED_IMAGE_SHA256,
            "image_confirmed": ["seed sprouts the next day", "kth sprout ripens after 3+k days",
                                "morning work then afternoon move", "right/front/left/back priority"],
            "derived_maturity_day": "planting day p + 1 day to sprout + (3+k) days = p+4+k",
            "code_reconstructed": ["maximize over all farmland starts and four facings",
                                   "face the chosen movement direction"],
            "unknown": ["full official statement and diagrams", "official outputs", "full input bounds"],
        },
        "oracle": "explicit seed/sprout/ripe phases; sprout age increments each morning",
        "sample_answers": answers["sample"],
        "generated_answers": answers["generated"],
        "stored_case_count": sum(file_batches.values()),
        "stored_start_states_checked": stored_states,
        "stores": store_checks,
        "local_private_store": {"path": PRIVATE.relative_to(REPO).as_posix(), "exists": PRIVATE.exists(),
                                "modified": False},
        "remote_private_store_checked": False,
        "generator_inputs_and_case_reasons_reproduced": True,
        "first_sample_table": {"rows_checked": 11, "start_one_based": [2, 4], "facing": "N",
                               "harvest_days": [e["day"] for e in first_trace if e["action"] == "harvest"],
                               "answer": first_answer, "trace_zero_based": first_trace},
        "two_field_harvest_days": harvest_days,
        "two_field_boundary_answers": boundary_answers,
        "synthetic_logic_checks": {"exhaustive_2x2_case_count": 16 * 35,
                                   "random_cases": 250, "random_seed": 2026092702,
                                   "claims_official_input_validity": False},
        "unique_cases_checked": len(cache),
        "total_start_states_checked": checked_states,
        "cli_batch_checks": cli_checks,
        "cli_runner": subprocess.check_output([runner, "--version"], stderr=subprocess.STDOUT).decode().strip(),
        "audited_source_hashes_unchanged": after,
        "metadata_for_parent": {
            "sample_batch_count": 1, "sample_case_count": 10,
            "generated_batch_count": 1, "generated_case_count": 50,
            "generated_flag": problem["private_testcases"][0]["generated"],
            "generated_source": problem["private_testcases"][0]["source"],
            "generated_official": problem["restoration"]["generated_testcases"]["official"],
            "public_private_tc_omitted": problem["private_tc_omitted"],
            "public_tc_stored": problem["tc_stored"],
        },
    }
    if args.report:
        (HERE / "example_audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                                                encoding="utf-8")
    print(json.dumps({k: report[k] for k in (
        "result", "sample_answers", "stored_case_count", "stored_start_states_checked",
        "local_private_store", "two_field_harvest_days", "unique_cases_checked",
        "total_start_states_checked", "cli_batch_checks", "metadata_for_parent")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
