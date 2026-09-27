"""CT 1 축약 출력 회귀 검사. 실행: python -B -m unittest _meta.test_codetree_sample_preview -v"""
import ast
import copy
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from _meta import crawl_codetree as ct


ROOT = Path(__file__).resolve().parents[1]
SOURCE = json.loads((ROOT / "problems/codetree/1.json").read_text(encoding="utf-8"))
PREVIEW = SOURCE["samples"][0].get("original_output_preview", SOURCE["samples"][0]["out"])


def raw_problem():
    doc = copy.deepcopy(SOURCE)
    doc["samples"] = [{"in": "", "out": PREVIEW}]
    doc["sample_notes"] = ["원본 예제 설명"]
    return doc


def api_body():
    return {
        "title": SOURCE["title"], "description": SOURCE["statement"],
        "problem_type": "Code block", "input_format": SOURCE["input_spec"],
        "output_format": SOURCE["output_spec"],
        "code_block": {"test_cases": [{"input": "", "output": PREVIEW,
                                       "description": "원본 예제 설명"}]},
    }


def judge_comparator():
    # 서버 시작/파일·네트워크 부작용 없이 실제 채점 비교 함수만 읽어서 실행한다.
    path = ROOT / "judge/server.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    nodes = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in ("norm", "same"):
            nodes.append(node)
        elif isinstance(node, ast.Assign):
            names = {n.id for t in node.targets for n in ast.walk(t) if isinstance(n, ast.Name)}
            if names.intersection(("NUM", "INT", "EPS_ABS", "EPS_REL")):
                nodes.append(node)
    scope = {"re": re}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), "exec"), scope)
    return scope["same"]


class SamplePreviewTests(unittest.TestCase):
    def normalized(self):
        doc = raw_problem()
        self.assertTrue(ct.normalize_sample_preview(doc))
        return doc

    def test_all_361_products_have_exact_format_and_190_lines(self):
        output = self.normalized()["samples"][0]["out"]
        lines = output.splitlines()
        self.assertEqual(len(lines), 190)
        self.assertTrue(output.endswith("\n"))
        self.assertFalse(output.endswith("\n\n"))
        products = []
        for index, line in enumerate(lines):
            self.assertEqual(line, line.rstrip())
            parts = line.split(" / ")
            self.assertEqual(len(parts), 1 if index % 10 == 9 else 2)
            for offset, part in enumerate(parts):
                match = re.fullmatch(r"(\d+) \* (\d+) = (\d+)", part)
                self.assertIsNotNone(match, part)
                dan, multiplier, product = map(int, match.groups())
                self.assertEqual(dan, index // 10 + 1)
                self.assertEqual(multiplier, index % 10 * 2 + offset + 1)
                self.assertEqual(product, dan * multiplier)
                products.append((dan, multiplier))
        self.assertEqual(len(set(products)), 361)
        self.assertEqual(lines[0], "1 * 1 = 1 / 1 * 2 = 2")
        self.assertEqual(lines[8], "1 * 17 = 17 / 1 * 18 = 18")
        self.assertEqual(lines[9], "1 * 19 = 19")
        self.assertEqual(lines[10], "2 * 1 = 2 / 2 * 2 = 4")
        self.assertEqual(lines[-2], "19 * 17 = 323 / 19 * 18 = 342")
        self.assertEqual(lines[-1], "19 * 19 = 361")

    def test_real_comparator_accepts_complete_program_rejects_preview_and_errors(self):
        # 한 항씩 출력하는 독립 프로그램을 실행한다(정규화 함수는 두 항을 묶어서 만든다).
        code = ("for a in range(1, 20):\n"
                "    for b in range(1, 20):\n"
                "        print(a, '*', b, '=', a*b, "
                "end='\\n' if b % 2 == 0 or b == 19 else ' / ')\n")
        result = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True,
                                text=True, check=True)
        expected = self.normalized()["samples"][0]["out"]
        same = judge_comparator()
        self.assertEqual(len(result.stdout.splitlines()), 190)
        self.assertTrue(same(result.stdout, expected))
        for wrong in (PREVIEW, expected.replace("= 361", "= 360"),
                      expected.replace(" / ", "/"),
                      "\n".join(expected.splitlines()[:-1]) + "\n"):
            with self.subTest(output=wrong[-70:]):
                self.assertFalse(same(wrong, expected))

    def test_provenance_notes_idempotence_and_original_bytes(self):
        doc = self.normalized()
        sample = doc["samples"][0]
        self.assertEqual(len(PREVIEW.splitlines()), 9)
        self.assertEqual(PREVIEW.count("....(생략)...."), 2)
        self.assertEqual(sample["original_output_preview"].encode("utf-8"), PREVIEW.encode("utf-8"))
        self.assertEqual(sample["output_provenance"]["kind"], "local_reconstruction")
        self.assertFalse(sample["output_provenance"]["official_full_output_available"])
        self.assertEqual(sample["output_provenance"]["line_count"], 190)
        self.assertEqual(doc["statement"], SOURCE["statement"])
        self.assertTrue(doc["sample_notes"][0].startswith("원본 예제 설명\n\n"))
        self.assertIn("공식 원본 전체 출력 아님", doc["sample_notes"][0])
        self.assertEqual(doc["sample_notes"][0].count(ct.NINETEEN_SAMPLE_NOTE), 1)
        before = copy.deepcopy(doc)
        self.assertFalse(ct.normalize_sample_preview(doc))
        self.assertEqual(doc, before)

    def test_guard_requires_exact_problem_alias_marker_and_matching_visible_lines(self):
        cases = []
        for key, value in (("site", "BOJ"), ("no", "f1"), ("no", "2"),
                           ("kind", "frequent"), ("alias", "nineteen-times-table-other"),
                           ("statement", "")):
            doc = raw_problem()
            doc[key] = value
            cases.append(doc)
        for preview in (PREVIEW.replace("....(생략)....", "..."),
                        PREVIEW.replace("....(생략)....", "문자 ....(생략)...."),
                        PREVIEW.replace("19 * 19 = 361", "19 * 19 = 360")):
            doc = raw_problem()
            doc["samples"][0]["out"] = preview
            cases.append(doc)
        doc = raw_problem()
        doc["samples"][0]["in"] = "2\n"
        cases.append(doc)
        for doc in cases:
            before = copy.deepcopy(doc)
            with self.subTest(alias=doc.get("alias"), no=doc.get("no")):
                self.assertFalse(ct.normalize_sample_preview(doc))
                self.assertEqual(doc, before)

    def test_other_samples_and_shared_source_objects_are_unchanged(self):
        doc = raw_problem()
        extra = {"in": "", "out": "별도의 출력\n"}
        doc["samples"].append(extra)
        doc["sample_notes"].append("두 번째 설명")
        old_samples = copy.deepcopy(doc["samples"])
        shared_samples = doc["samples"]
        self.assertTrue(ct.normalize_sample_preview(doc))
        self.assertEqual(shared_samples, old_samples)
        self.assertEqual(doc["samples"][1], extra)
        self.assertEqual(doc["sample_notes"][1], "두 번째 설명")

    def test_existing_other_codetree_problems_are_unchanged(self):
        count = 0
        for path in (ROOT / "problems/codetree").glob("*.json"):
            if path.name == "1.json":
                continue
            doc = json.loads(path.read_text(encoding="utf-8"))
            before = copy.deepcopy(doc)
            self.assertFalse(ct.normalize_sample_preview(doc), path.name)
            self.assertEqual(doc, before, path.name)
            count += 1
        self.assertGreater(count, 1000)

    def test_api_fetch_read_only_also_returns_reconstructed_output(self):
        with patch.object(ct, "read_store", return_value=None), patch.object(ct, "write_problem") as write:
            status, full, _, _ = ct.apply_result(copy.deepcopy(SOURCE), {"s": 200, "b": api_body()}, save=False)
        self.assertEqual(status, "ok")
        self.assertEqual(len(full["samples"][0]["out"].splitlines()), 190)
        self.assertEqual(full["samples"][0]["original_output_preview"], PREVIEW)
        write.assert_not_called()

    def test_rebuild_and_forced_recrawl_repair_both_files_preserving_store_fields(self):
        for private in (set(), {"CT"}):
            with self.subTest(private=bool(private)), tempfile.TemporaryDirectory() as tmp:
                pub_dir, store_dir = Path(tmp) / "public", Path(tmp) / "store"
                pub_dir.mkdir()
                store_dir.mkdir()
                pub_path, store_path = pub_dir / "1.json", store_dir / "1.json"
                raw = raw_problem()
                store = ct.store_doc(raw)
                store.update({"private": [{"in": "private", "out": "kept"}],
                              "tc_generated": "existing-source", "tc_note": "기존 생성 TC 설명",
                              "pipeline_metadata": {"preserve": True}})
                pub_path.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
                store_path.write_text(json.dumps(store, ensure_ascii=False), encoding="utf-8")
                with patch.multiple(ct, PUB_DIR=str(pub_dir), STORE_DIR=str(store_dir), PRIVATE_SITES=private), \
                        patch.object(ct, "cap_private_tc", side_effect=lambda tc: (tc, 0)):
                    counts = ct.rebuild_public(["1"], log=lambda *args: None)
                    self.assertEqual(counts["normalized"], 1)
                    pub = json.loads(pub_path.read_text(encoding="utf-8"))
                    fixed = json.loads(store_path.read_text(encoding="utf-8"))
                    self.assertEqual(len(fixed["samples"][0]["out"].splitlines()), 190)
                    self.assertIn(ct.NINETEEN_SAMPLE_NOTE, fixed["problem"]["sample_notes"][0])
                    if private:
                        self.assertNotIn("samples", pub)
                        self.assertNotIn("sample_notes", pub)
                        self.assertNotIn("original_output_preview", json.dumps(pub))
                    else:
                        self.assertEqual(pub["samples"], fixed["samples"])
                        self.assertEqual(pub["sample_notes"], fixed["problem"]["sample_notes"])
                    snapshots = (pub_path.read_bytes(), store_path.read_bytes())
                    again = ct.rebuild_public(["1"], log=lambda *args: None)
                    self.assertEqual(again["changed"], 0)
                    self.assertEqual(again["normalized"], 0)
                    self.assertEqual((pub_path.read_bytes(), store_path.read_bytes()), snapshots)
                    status, full, _, _ = ct.apply_result(copy.deepcopy(SOURCE),
                                                        {"s": 200, "b": api_body()}, save=True)
                    self.assertEqual(status, "ok")
                    refetched = json.loads(store_path.read_text(encoding="utf-8"))
                    self.assertEqual(refetched["samples"], full["samples"])
                    self.assertEqual(len(full["samples"][0]["out"].splitlines()), 190)
                    for key in ("private", "tc_generated", "tc_note", "pipeline_metadata"):
                        self.assertEqual(refetched[key], store[key])


if __name__ == "__main__":
    unittest.main()
