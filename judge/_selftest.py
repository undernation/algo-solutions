"""채점서버 자가 테스트 — 실제 BOJ 2618 정답/오답 코드로 검증."""
import json, urllib.request, io, os, sys

URL = "http://127.0.0.1:12014/judge"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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


def post(body):
    req = urllib.request.Request(
        URL, data=json.dumps(body).encode(), method="POST",
        headers={"content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode())


def load_cases():
    p = os.path.join(ROOT, "problems", "boj", "2618.json")
    d = json.load(io.open(p, encoding="utf-8"))
    return [{"input": s["in"], "output": s["out"]} for s in d.get("samples", [])]


def main():
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
            print("        ", json.dumps(r, ensure_ascii=False)[:260])


if __name__ == "__main__":
    main()
