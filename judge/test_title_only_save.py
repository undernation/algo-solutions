"""번호 없는 옛 기록의 실제 파일 저장·커밋·이력 병합 회귀 검사.

python3 -m unittest discover -s judge -p 'test_title_only_save.py'
실제 저장소·네트워크 대신 임시 git 저장소에만 쓴다.
"""
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


server = load("title_save_server", ROOT / "judge/server.py")
heatmap = load("title_save_heatmap", ROOT / "_meta/build_heatmap.py")


class TitleOnlySaveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "_meta").mkdir()
        for args in (("init", "-q"), ("config", "user.name", "Test"),
                     ("config", "user.email", "test@example.invalid")):
            subprocess.run(["git"] + list(args), cwd=str(self.root), check=True,
                           capture_output=True)
        for attr, value in (("ROOT", str(self.root)), ("AUTO_PUSH", False),
                            ("VERBOSE", False)):
            mock = patch.object(server, attr, value)
            mock.start()
            self.addCleanup(mock.stop)
        # 생성 화면 빌드는 별도로 검증하고, 파일 저장과 git 커밋은 실제 실행한다.
        original_run = subprocess.run

        def run(args, *pos, **kwargs):
            if len(args) > 1 and str(args[1]).startswith("_meta/build_"):
                return subprocess.CompletedProcess(args, 0, "", "")
            return original_run(args, *pos, **kwargs)

        mock = patch.object(server.subprocess, "run", side_effect=run)
        mock.start()
        self.addCleanup(mock.stop)

    def save(self, title, no="", code="print(1)\n"):
        return server.save_solution({"site": "BOJ", "no": no, "title": title,
                                     "code": code, "date": "2026-10-21", "status": "품"})

    def history(self):
        return json.loads((self.root / "_meta/history.json").read_text())

    def test_legacy_route_is_saved_without_synthetic_number(self):
        title = "프로그래머스 퍼즐조각 채우기"
        result = self.save(title, "~" + title)
        self.assertTrue(result["ok"], result)
        self.assertTrue(result["committed"], result)
        self.assertEqual(result["file"], "boj/프로그래머스퍼즐조각채우기.py")
        text = (self.root / result["file"]).read_text()
        self.assertIn("BOJ   " + title, text)
        self.assertNotIn("~" + title, text)
        item = self.history()["2026-10-21"]["items"][0]
        self.assertEqual((item["no"], item["title"]), ("", title))
        with patch.object(heatmap, "ROOT", str(self.root)):
            rebuilt = heatmap.from_repo()["2026-10-21"]["items"][0]
        self.assertEqual(heatmap._ikey(rebuilt), "BOJ/~" + title)

    def test_same_day_titles_remain_separate_and_retries_append(self):
        first = "프로그래머스 퍼즐조각 채우기"
        second = "프로그래머스 타겟 넘버"
        for title, code in ((first, "print(1)"), (second, "print(2)"),
                            (first, "print(3)")):
            self.assertTrue(self.save(title, code=code)["ok"])
        day = self.history()["2026-10-21"]
        self.assertEqual(day["count"], 2)
        items = {item["title"]: item for item in day["items"]}
        self.assertEqual(len(items[first]["attempts"]), 2)
        self.assertEqual(len(items[second]["attempts"]), 1)
        self.assertIn("print(2)", (self.root / items[second]["file"]).read_text())

    def test_union_preserves_different_title_only_problems(self):
        def history(title):
            return json.dumps({"2026-10-21": {"count": 1, "items": [
                {"site": "BOJ", "no": "", "title": title}]}})
        merged = json.loads(server.union_history(history("첫 문제"), history("다른 문제")))
        self.assertEqual(len(merged["2026-10-21"]["items"]), 2)

    def test_invalid_numbers_are_still_rejected_before_writing(self):
        for no in ("../../outside", "bad number", "a" * 13, "~다른 제목"):
            with self.subTest(no=no):
                self.assertFalse(self.save("테스트", no)["ok"])
        self.assertFalse(self.save("", "")["ok"])
        self.assertFalse((self.root / "boj").exists())

    def test_numbered_save_keeps_existing_identity(self):
        result = self.save("탑", "2493")
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["file"], "boj/2493.py")
        self.assertEqual(self.history()["2026-10-21"]["items"][0]["no"], "2493")


if __name__ == "__main__":
    unittest.main()
