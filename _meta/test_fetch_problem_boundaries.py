"""본문 속 낱말과 페이지 UI를 문제 섹션으로 오인하지 않는지 확인한다.

실행: python -B -m unittest discover -s _meta -p test_fetch_problem_boundaries.py
네트워크·브라우저·파일 쓰기 없이 저장된 파싱 사고를 작은 본문으로 재현한다.
"""
import unittest
from unittest.mock import patch

try:
    from .fetch_problem import apply_images, parse_cosal, parse_swea, strip_swea_footer
except ImportError:
    from fetch_problem import apply_images, parse_cosal, parse_swea, strip_swea_footer


class CosalBoundaryTests(unittest.TestCase):
    def test_test_case_words_in_all_descriptions_are_not_headings(self):
        text = """터렛
시간 2 초 · BOJ 1002 메모리 128 MB
해결
주차 목록
각 테스트 케이스의 좌표를 입력받아 출력하는 프로그램을 작성하시오.
입력
첫째 줄에 테스트 케이스의 개수 T가 주어진다.
각 테스트 케이스에는 좌표와 반지름이 주어진다.
출력
각 테스트 케이스마다 가능한 좌표의 수를 출력한다.
테스트 케이스
예제 입력 1
1
0 0 1 2 0 1
예제 출력 1
1
예제 입력 2
1
0 0 1 0 0 1
예제 출력 2
-1
프라이빗 테스트케이스
14개
코드 제출
여기는 문제 본문이 아니다.
"""
        d = parse_cosal(text, "https://cosal.aviss.kr/problems/detail/1002")
        self.assertEqual(d["input_spec"], "첫째 줄에 테스트 케이스의 개수 T가 주어진다.\n"
                         "각 테스트 케이스에는 좌표와 반지름이 주어진다.")
        self.assertEqual(d["output_spec"], "각 테스트 케이스마다 가능한 좌표의 수를 출력한다.")
        self.assertEqual(d["statement"], "각 테스트 케이스의 좌표를 입력받아 출력하는 프로그램을 작성하시오.")
        self.assertEqual(d["samples"], [
            {"in": "1\n0 0 1 2 0 1", "out": "1"},
            {"in": "1\n0 0 1 0 0 1", "out": "-1"},
        ])
        self.assertEqual(d["private_tc_count"], 14)

    def test_indented_crlf_headings_and_unnumbered_sample(self):
        text = ("합\nBOJ 1 시간 1 초 메모리 128 MB\n문자열 · 누적합 · 구현 목록\n"
                "값을 입력받아 합을 구한다.\n\t입력 \t\n두 정수를 준다.\n"
                " 출력 \n합을 출력한다.\n 테스트  케이스 \n예제 입력\n1 2\n"
                "예제 출력\n3\n 코드 제출 \n버튼").replace("\n", "\r\n")
        d = parse_cosal(text, "local-fixture")
        self.assertEqual(d["statement"], "값을 입력받아 합을 구한다.")
        self.assertEqual(d["input_spec"], "두 정수를 준다.")
        self.assertEqual(d["output_spec"], "합을 출력한다.")
        self.assertEqual(d["samples"], [{"in": "1 2", "out": "3"}])


class SweaBoundaryTests(unittest.TestCase):
    HEADER = "12712. 파리퇴치3\nD2\n시간 : Python 1초\n메모리 : 256MB\n"

    def test_bracket_heading_variants_stop_before_download_preview(self):
        for input_heading, output_heading in [
                ("[입력]", "[출력]"),
                ("[입력 형식]", "[출력 형식]"),
                ("[입력 설명]", "[출력 설명]")]:
            with self.subTest(input_heading=input_heading):
                text = (self.HEADER + "무단 복제하는 것을 금지합니다.\n문제 본문.\n"
                        "[제약 사항]\n1. N은 5 이상이다.\n" + input_heading +
                        "\nT를 입력받아 각 테스트 케이스를 읽는다.\n" + output_heading +
                        "\n답을 출력한다.\n입력\n1\n5\nin1.txt\n다운로드\n"
                        "출력\n#1 3\nout1.txt\n다운로드\n 14\n댓글(6)\n사용자 댓글")
                d = parse_swea(text, "local-fixture")
                self.assertEqual(d["statement"], "문제 본문.")
                self.assertEqual(d["constraints"], ["1. N은 5 이상이다."])
                self.assertEqual(d["input_spec"], "T를 입력받아 각 테스트 케이스를 읽는다.")
                self.assertEqual(d["output_spec"], "답을 출력한다.")
                self.assertEqual(d["samples"], [])  # 미리보기로 채점하지 않는다.

    def test_missing_output_heading_does_not_swallow_preview_or_comments(self):
        text = (self.HEADER + "문제 설명.\n[입력]\nN과 M 다음 N행의 격자를 준다.\n"
                "입력\n1\n5 2\nin1.txt\n다운로드\n출력\n#1 64\n"
                "out1.txt\n다운로드\n14\n댓글(6)\n사용자 댓글")
        d = parse_swea(text, "local-fixture")
        self.assertEqual(d["input_spec"], "N과 M 다음 N행의 격자를 준다.")
        self.assertEqual(d["output_spec"], "")

    def test_user_code_template_stays_in_input_description(self):
        template = ("입력 첫 줄에는 T가 주어진다.\n\n※ User Code는 다음의 템플릿을 사용한다.\n"
                    "user.cpp\n#define N 4\nvoid doUserImplementation(int guess[]) {\n"
                    "    // Please implement this function.\n}\n")
        text = (self.HEADER + "숫자 야구 게임을 구현하라.\n[입력]\n" + template +
                "입력\n5\n8975\nsample_input.txt\n다운로드\n출력\n#1 6\n"
                "no_sample_output.txt\n다운로드\n연관Talk 1 Talk으로 이동\n32\n댓글(5)")
        d = parse_swea(text, "local-fixture")
        self.assertEqual(d["input_spec"], template.strip())
        self.assertEqual(d["output_spec"], "")

    def test_unbracketed_specs_and_explanatory_example_are_preserved(self):
        body = ("차이의 최솟값을 구하라.\n입력\nT와 N, K를 준다.\n출력\n차이를 출력한다.\n"
                "입력\n1\n3 2\n1 2 3\nsin.txt\n다운로드\n출력\n#1 1\n\n"
                "첫 번째 예제: 주머니를 고르는 방법 중 최솟값은 1이다.\n"
                "두 번째 예제: 무조건 모든 주머니를 나눠줘야 한다.\nsout.txt\n다운로드")
        d = parse_swea(self.HEADER + body + "\n11\n댓글(11)\n정답 코드\nAbout\nSW Expert Academy",
                       "local-fixture")
        self.assertEqual(d["statement"], body)
        self.assertEqual(d["input_spec"], "")  # 설명/예제 패널을 추측해 나누지 않는다.
        self.assertEqual(d["samples"], [])

    def test_footer_cleanup_is_an_exact_prefix_except_download_vote_count(self):
        text = "설명과 숫자 123.\n입력\n5\n출력\n#1 100\nout.txt\n다운로드"
        self.assertEqual(strip_swea_footer(text + "\n\n 14\n댓글(6)\ncomment"), text)
        self.assertEqual(strip_swea_footer("필요한 마지막 값\n100\n댓글(1)\ncomment"),
                         "필요한 마지막 값\n100")

    def test_footer_fallback_and_words_inside_prose(self):
        body = "문자열 About과 댓글(5)를 출력한다.\nAbout\n이 줄도 본문이다."
        self.assertEqual(strip_swea_footer(body), body)
        self.assertEqual(strip_swea_footer(body + "\nAbout\nSW Expert Academy\nSupport"), body)
        self.assertEqual(strip_swea_footer(body + "\n연관Talk 1 Talk으로 이동\n댓글(5)"), body)

    def test_image_pass_cannot_reintroduce_swea_footer(self):
        text = "그림 설명.\n[[IMG:1]]\n[입력 형식]\n입력 설명.\n댓글(1)\ncomment"
        d = {"site": "SWEA", "no": "12712", "statement": "기존 설명"}
        with patch(apply_images.__module__ + ".collect_images", return_value=(text, ["image.png"], [100])):
            apply_images(None, d)
        self.assertEqual(d["statement"], "그림 설명.\n[[IMG:1]]")
        self.assertEqual(d["images"], ["image.png"])

    def test_image_pass_preserves_unbracketed_example_explanation(self):
        body = "그림 설명.\n[[IMG:1]]\n입력\nT를 준다.\n첫 번째 예제: 설명."
        d = {"site": "SWEA", "no": "20728"}
        with patch(apply_images.__module__ + ".collect_images", return_value=(body + "\n댓글(1)\ncomment",
                                                                 ["image.png"], [100])):
            apply_images(None, d)
        self.assertEqual(d["statement"], body)


if __name__ == "__main__":
    unittest.main()
