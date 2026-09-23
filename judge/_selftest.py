"""채점서버 자가 테스트 — 실제 BOJ 2618 정답/오답 코드로 검증.

    python judge/_selftest.py                         # BOJ 채점 + same() 비교 규칙 + 코드트리 공개/비공개(오프라인)
    python judge/_selftest.py --ct                    # + 코드트리 보관소·/prob·채점 (허브 필요)
    python judge/_selftest.py --offline               # 허브 없이 오프라인 검사만
    python judge/_selftest.py --url http://127.0.0.1:12098 --ct

--ct 는 허브의 TC 보관소에 가짜 문제 CT/_selftest 를 올린다(repo 는 안 건드린다).
토큰은 ~/.algo-hub-token 이 있으면 붙여 보낸다(--no-auth 허브면 무시된다).
"""
import json, urllib.request, io, os, sys

HUB = "http://127.0.0.1:12014"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []

# 실제 BOJ 2618 정답 (경찰차 DP)
AC = r'''
import sys
input = sys.stdin.readline

def main():
    N = int(input())
    W = int(input())
    ev = [tuple(map(int, input().split())) for _ in range(W)]
    P1, P2 = (1, 1), (N, N)

    def dist(a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    INF = float('inf')
    dp = [[INF]*(W+1) for _ in range(W+1)]
    ch = [[0]*(W+1) for _ in range(W+1)]
    dp[W][W] = 0
    for i in range(W, -1, -1):
        for j in range(W, -1, -1):
            if i == W and j == W:
                continue
            nxt = max(i, j)
            if nxt >= W:
                dp[i][j] = 0
                continue
            a = P1 if i == 0 else ev[i-1]
            b = P2 if j == 0 else ev[j-1]
            c1 = dist(a, ev[nxt]) + dp[nxt+1][j]
            c2 = dist(b, ev[nxt]) + dp[i][nxt+1]
            if c1 < c2:
                dp[i][j], ch[i][j] = c1, 1
            else:
                dp[i][j], ch[i][j] = c2, 2

    out = [str(dp[0][0])]
    i = j = 0
    while max(i, j) < W:
        nxt = max(i, j)
        if ch[i][j] == 1:
            out.append('1'); i = nxt+1
        else:
            out.append('2'); j = nxt+1
    sys.stdout.write('\n'.join(out))

main()
'''

WA = "print(0)"
RE = "import sys\nraise ValueError('boom')"
TLE = "while True:\n    pass"
CE = "def f(:\n  pass"


def token():
    p = os.path.expanduser("~/.algo-hub-token")
    try:
        return io.open(p, encoding="utf-8").read().strip()
    except OSError:
        return ""


def post(body, path="/judge"):
    h = {"content-type": "application/json"}
    if token():
        h["X-Auth-Token"] = token()
    req = urllib.request.Request(
        HUB + path, data=json.dumps(body).encode(), method="POST", headers=h)
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode())


def check(name, ok, extra=""):
    print("  %-34s %s" % (name, "✅" if ok else "❌ %s" % extra))
    if not ok:
        FAILS.append(name)


def load_cases():
    p = os.path.join(ROOT, "problems", "boj", "2618.json")
    d = json.load(io.open(p, encoding="utf-8"))
    return [{"input": s["in"], "output": s["out"]} for s in d.get("samples", [])]


def boj_judge():
    cases = load_cases()
    print("문제 예제 %d개 로드" % len(cases))
    # 손으로 만든 추가 케이스 (검증용)
    cases = cases + [
        {"input": "5\n1\n3 3", "output": "4\n2"},
    ]
    print("총 %d 케이스로 테스트\n" % len(cases))

    for name, code, expect in (("정답", AC, "accepted"),
                               ("오답", WA, "wrong_answer"),
                               ("런타임에러", RE, "runtime_error"),
                               ("컴파일에러", CE, "compile_error"),
                               ("시간초과", TLE, "time_limit_exceeded")):
        r = post({"problemId": "2618", "sourceCode": code,
                  "testCases": cases, "publicTestCaseCount": 1,
                  "timeLimit": 1, "memoryLimit": 128})
        s = r.get("summary", {})
        ok = r.get("verdict") == expect
        print("  %-6s → %-22s %s/%s  %s" % (
            name, r.get("verdict"), s.get("passed"), s.get("total"),
            "✅" if ok else "❌ (기대 %s)" % expect))
        if not ok:
            FAILS.append("BOJ " + name)
            print("        ", json.dumps(r, ensure_ascii=False)[:260])


# ── 채점 비교 규칙 server.same() ─────────────────────────────────────
# 2026-09-23 에 정수 답에도 상대오차 1e-6 이 적용돼 1000001 이 1000000 의 정답으로 통과하던
# 것을 고쳤다. 그 회귀와, 원래 지키던 두 규칙(실수만 오차 허용 · 줄바꿈/공백 배치 차이는 오답)을 묶어 둔다.
SAME_CASES = (
    ("1000001", "1000000", False, "정수 ±1 (100만 이상)"),
    ("123456789013", "123456789012", False, "정수 ±1 (12자리)"),
    ("-7", "7", False, "정수 부호만 다름"),
    ("5.0", "5", False, "정답이 정수인데 실수로 출력"),
    ("1000000", "1000000", True, "정수 같음"),
    ("0.5265618908306351", "0.52656189", True, "실수 오차 안(8e-10)"),
    ("3.0000001", "3.0", True, "실수 상대오차 안"),
    ("0.5266", "0.5265618908306351", False, "실수 오차 밖"),
    ("YES 0.50000001", "YES 0.5", True, "글자+실수 섞임, 오차 안"),
    ("NO 0.5", "YES 0.5", False, "글자 다름"),
    ("1 2", "1\n2", False, "줄바꿈 배치만 다름"),
    ("1  2", "1 2", False, "공백 개수만 다름"),
    ("1 2  \n\n", "1 2", True, "줄 끝 공백·끝 빈 줄 무시"),
    ("1\r\n2\r\n", "1\n2", True, "CRLF 줄바꿈"),
    ("", "0", False, "빈 출력"),
    ("1 2 3", "1 2", False, "토큰 수 다름"),
)


def same_cases():
    """허브 없이 — server.same() 비교 규칙."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import server
    print("\n[채점 비교 same() — 오프라인]")
    for got, want, exp, why in SAME_CASES:
        check("%s → %s" % (why, "통과" if exp else "오답"), server.same(got, want) is exp,
              (got, want, server.same(got, want)))


# ── 코드트리 (공개/비공개 스위치: _meta/judge_config.json privateSites) ──────────
# 지문이 들어가면 안 되는 자리마다 같은 표식 문자열을 심어 두고, 결과물에 남았는지 본다.
# 두 모드를 다 보려고 테스트 안에서 server.PRIVATE_SITES 를 잠깐 바꿨다가 되돌린다.
SECRET = "SECRET-지문-7f3a"
CT_PROB = {"site": "CT", "no": "386", "title": "가짜 로봇청소기",
           "url": "https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/x/description",
           "level": "L13", "origin": "2025 하반기 오후 1번 문제",
           "limits": {"time": "Python3 1초 · C++ 0.5초", "memory": "64 MB", "time_sec": 1.0},
           "stats": {"accept_rate": "89.0", "submissions": "21545"},
           "statement": SECRET + " 본문", "input_spec": SECRET + " 입력",
           "output_spec": SECRET + " 출력", "constraints": SECRET + " $1 \\le N$",
           "hint": SECRET + " 힌트", "sample_notes": [SECRET + " 설명"],
           "samples": [{"in": SECRET + " in", "out": SECRET + " out"}],
           "tags": ["시뮬레이션"], "prerequisite_lessons": ["x"],
           "code_block": {"test_cases": [{"input": SECRET}]}}


def ct_switch(server):
    """스위치(judge_config.json privateSites) 읽기 — 못 읽으면 CT 비공개로 넘어져야 한다."""
    import tempfile, shutil
    cfg, why = server.CONFIG_FILE, server.PRIVATE_WHY
    tmp = tempfile.mkdtemp()
    p = os.path.join(tmp, "judge_config.json")
    try:
        server.CONFIG_FILE = p
        for name, text, want in (("[] → 전부 공개", '{"privateSites": []}', set()),
                                 ('["ct"] → CT', '{"privateSites": ["ct"]}', {"CT"}),
                                 ("키 없음 → CT", '{"pyMult": 3}', {"CT"}),
                                 ("목록 아님 → CT", '{"privateSites": "CT"}', {"CT"}),
                                 ("깨진 파일 → CT", '{"privateSites": [', {"CT"}),
                                 ("파일 없음 → CT", None, {"CT"})):
            if text is None:
                os.remove(p)
            else:
                io.open(p, "w", encoding="utf-8").write(text)
            got = server.load_private_sites()
            check("privateSites %s" % name, got == want, got)
    finally:
        server.CONFIG_FILE, server.PRIVATE_WHY = cfg, why
        shutil.rmtree(tmp, ignore_errors=True)


def ct_offline():
    """허브 없이 — 풀이 헤더·공개 JSON. 비공개/공개 두 모드를 다 본다(지금 설정과 무관하게)."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import server
    now = set(server.PRIVATE_SITES)
    print("\n[코드트리 — 오프라인]  지금 설정의 비공개 사이트: %s" % (", ".join(sorted(now)) or "없음"))
    ct_switch(server)
    try:
        server.PRIVATE_SITES = {"CT"}
        ct_private_mode(server)
        server.PRIVATE_SITES = set()
        ct_public_mode(server)
    finally:
        server.PRIVATE_SITES = now
    # 회귀: BOJ 는 예전처럼 지문·예제가 그대로 들어간다(소유자 결정, PUBLIC_SAFE=False)
    bp = {"site": "BOJ", "statement": "BOJ 본문", "samples": [{"in": "1", "out": "2"}],
          "constraints": ["1 ≤ N ≤ 10"]}
    h = server.build_header({"site": "BOJ", "no": "1", "title": "t", "problem": bp})
    check("BOJ 헤더는 지문·예제·제약 유지", "[문제]\nBOJ 본문" in h and "[예제 1]" in h
          and "제약   : 1 ≤ N ≤ 10" in h, h[:300])
    check("BOJ redact 는 그대로", server.redact(bp) == bp)


def ct_public_mode(server):
    """privateSites=[] — 코드트리도 BOJ/SWEA 처럼 지문·예제를 넣되, 힌트는 빼고 제약은 줄 단위."""
    print("  (공개 모드)")
    h = server.build_header({"site": "CT", "no": "386", "title": "t", "problem": CT_PROB})
    check("공개: 헤더에 [문제] 지문·[예제]", "[문제]\n" + CT_PROB["statement"] in h
          and "[예제 1]\n입력:\n" + SECRET + " in" in h, h[:300])
    check("공개: 힌트·예제 설명은 헤더에 없음", CT_PROB["hint"] not in h
          and CT_PROB["sample_notes"][0] not in h and "지문은 비공개" not in h, h[:400])
    md = dict(CT_PROB, constraints="$1 \\le N \\le 100$\n\n  - 두 번째 줄  \n3\n4\n5\n6\n7번째는 안 나옴")
    h = server.build_header({"site": "CT", "no": "386", "title": "t", "problem": md})
    lines = [x for x in h.split("\n") if x.startswith("제약")]
    check("공개: 마크다운 제약은 줄 단위·최대 6줄", lines[:2] == ["제약   : $1 \\le N \\le 100$",
          "제약   : - 두 번째 줄"] and len(lines) == 6 and "7번째" not in h, lines)
    check("공개: redact 는 손대지 않음", server.redact(CT_PROB, "CT") == CT_PROB)


def ct_private_mode(server):
    print("  (비공개 모드)")
    for s in ("CT", "ct", " Ct "):
        h = server.build_header({"site": s, "no": "386", "title": "t", "url": "u",
                                 "problem": CT_PROB, "note": "내 메모"})
        check("헤더에 지문 없음 (site=%r)" % s, SECRET not in h, h[:200])
        check("헤더에 비공개 안내 (site=%r)" % s, "[문제] 코드트리 지문은 비공개" in h, h[:200])
    h = server.build_header({"site": "BOJ", "no": "1", "title": "t", "problem": CT_PROB})
    check("헤더 — 문제 dict 의 site 로도 판정", SECRET not in h, h[:200])
    h = server.build_header({"site": "CT", "no": "386", "title": "t", "problem": CT_PROB})
    check("헤더에 한도·난이도는 남음", "한도   : " in h and "난이도 : L13" in h, h[:300])
    pub = server.redact(CT_PROB, "CT")
    leak = [k for k in pub if k in server.PRIVATE_REDACT]
    check("공개 JSON 에 비공개 키 없음", not leak and SECRET not in json.dumps(
        pub, ensure_ascii=False), leak)
    check("공개 JSON 표식·개수", pub.get("private_content") is True and
          pub.get("sample_count") == 1 and pub.get("statement_len") == len(CT_PROB["statement"]),
          pub)
    check("공개 JSON 메타 유지", pub.get("limits") == CT_PROB["limits"] and
          pub.get("origin") == CT_PROB["origin"], pub)


def ct_online():
    """허브에 붙어서 — 보관소(problem 보존)·/prob·useStoredTC 채점."""
    print("\n[코드트리 보관소 — %s]" % HUB)
    no = "_selftest"
    prob = {"title": "두 수의 합", "statement": "두 수를 더하라", "input_spec": "a b",
            "output_spec": "a+b", "constraints": "", "hint": "", "sample_notes": []}
    smp = [{"in": "1 2", "out": "3"}, {"in": "5 7", "out": "12"}]
    r = post({"site": "CT", "no": no, "samples": smp, "private": [], "problem": prob},
             "/tcupload")
    check("/tcupload + problem", r.get("ok") and r.get("hasProblem"), r)
    r = post({"site": "CT", "no": no, "samples": smp, "private": []}, "/tcupload")
    check("/tcupload problem 생략 → 보존", r.get("ok") and r.get("hasProblem"), r)
    r = post({"site": "CT", "no": no}, "/tc")
    check("/tc hasProblem", r.get("stored") and r.get("hasProblem") is True, r)
    r = post({"site": "CT", "no": no}, "/prob")
    check("/prob stored", r.get("stored") and (r.get("problem") or {}).get("statement")
          == prob["statement"] and len(r.get("samples") or []) == 2, r)
    r = post({"site": "CT", "no": "nope_404"}, "/prob")
    check("/prob 없는 문제 → stored=false", r.get("ok") and r.get("stored") is False, r)
    r = post({"site": "CT", "no": "../x"}, "/prob")
    check("/prob 이상한 번호 → 거절", r.get("ok") is False, r)
    # 보관소 밖으로 나가는 번호는 읽는 길마다 막혀야 한다(/tc 정보·미리보기, /tcfile, 보관본 채점)
    for name, path, body in (("/tc 정보 ../../x → 거절", "/tc", {"site": "CT", "no": "../../x"}),
                             ("/tc 미리보기 ../../x → 거절", "/tc",
                              {"site": "CT", "no": "../../x", "index": 0}),
                             ("/tcfile ../../x → 거절", "/tcfile",
                              {"site": "CT", "no": "../../x", "kind": "in"}),
                             ("/tc 모르는 사이트 → 거절", "/tc", {"site": "XX", "no": no})):
        r = post(body, path)
        check(name, r.get("ok") is False, r)
    # 지우기도 같은 검사를 탄다. ⚠️ 검사가 없는 옛 허브에 돌려도 아무 일이 없게, 있을 수 없는
    # 파일 이름만 쓰고 오류 문구로 판정한다(/note 는 옛 허브면 repo 에 파일을 써서 뺐다).
    for name, body, want in (("/delete problem ../ → 번호 거절",
                              {"kind": "problem", "site": "CT", "no": "../../zz-selftest-none"},
                              "문제 번호가 이상합니다"),
                             ("/delete 모르는 사이트 → 거절",
                              {"kind": "submission", "site": "XX", "no": no, "date": "2000-01-01"},
                              "알 수 없는 사이트입니다")):
        r = post(body, "/delete")
        check(name, r.get("ok") is False and r.get("error") == want, r)
    for name, code, expect in (("정답", "a,b=map(int,input().split())\nprint(a+b)", "accepted"),
                               ("오답", "print(0)", "wrong_answer")):
        r = post({"problemId": no, "site": "CT", "sourceCode": code, "testCases": [],
                  "useStoredTC": True, "timeLimit": 1, "langAdjusted": True})
        s = r.get("summary") or {}
        check("CT 채점 %s → %s" % (name, expect),
              r.get("verdict") == expect and s.get("total") == 2, r)
    r = post({"problemId": "nope_404", "site": "CT", "sourceCode": "print(1)",
              "testCases": [], "useStoredTC": True, "timeLimit": 1})
    check("보관본 없음 → accepted 아님", r.get("verdict") != "accepted", r)
    r = post({"problemId": "../../x", "site": "CT", "sourceCode": "print(1)",
              "testCases": [], "useStoredTC": True, "timeLimit": 1})
    check("보관본 채점 이상한 번호 → no_testcases", r.get("verdict") == "no_testcases", r)


def main():
    global HUB
    argv = sys.argv[1:]
    if "--url" in argv:
        HUB = argv[argv.index("--url") + 1].rstrip("/")
    if "--offline" not in argv:
        boj_judge()
    same_cases()
    ct_offline()
    if "--ct" in argv and "--offline" not in argv:
        ct_online()
    print("\n%s" % ("✅ 전부 통과" if not FAILS else "❌ 실패 %d: %s" % (len(FAILS), FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
