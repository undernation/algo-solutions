"""End-to-End 테스트: 크롤링 → 채점 → 저장/커밋 전체 흐름."""
import json, urllib.request, io, os

BASE = "http://127.0.0.1:12014"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CODE = r'''import sys
input = sys.stdin.readline

def main():
    N = int(input()); W = int(input())
    ev = [tuple(map(int, input().split())) for _ in range(W)]
    P1, P2 = (1, 1), (N, N)
    d = lambda a, b: abs(a[0]-b[0]) + abs(a[1]-b[1])
    INF = float('inf')
    dp = [[INF]*(W+1) for _ in range(W+1)]
    ch = [[0]*(W+1) for _ in range(W+1)]
    for i in range(W, -1, -1):
        for j in range(W, -1, -1):
            nxt = max(i, j)
            if nxt >= W:
                dp[i][j] = 0; continue
            a = P1 if i == 0 else ev[i-1]
            b = P2 if j == 0 else ev[j-1]
            c1 = d(a, ev[nxt]) + dp[nxt+1][j]
            c2 = d(b, ev[nxt]) + dp[i][nxt+1]
            if c1 < c2: dp[i][j], ch[i][j] = c1, 1
            else:       dp[i][j], ch[i][j] = c2, 2
    out = [str(dp[0][0])]
    i = j = 0
    while max(i, j) < W:
        nxt = max(i, j)
        if ch[i][j] == 1: out.append('1'); i = nxt+1
        else:             out.append('2'); j = nxt+1
    sys.stdout.write('\n'.join(out))

main()
'''


def post(path, body, timeout=300):
    req = urllib.request.Request(BASE + path, data=json.dumps(body).encode(),
                                 method="POST",
                                 headers={"content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


print("─" * 62)
print("① 문제 크롤링  POST /fetch  {ref: 2618}")
r = post("/fetch", {"ref": "2618"})
if not r.get("ok"):
    raise SystemExit("  ❌ " + str(r)[:200])
prob = r["problem"]
print("   ✅ %s %s  %s" % (prob["site"], prob["no"], prob["title"]))
print("      한도 %s | 지문 %d자 | 예제 %d개 | 비공개TC %s개"
      % (prob.get("limits"), len(prob.get("statement", "")),
         len(prob.get("samples", [])), prob.get("private_tc_count")))

print()
print("─" * 62)
print("② 채점  POST /judge (코딩살구 호환 규격)")
cases = [{"input": s["in"], "output": s["out"]} for s in prob.get("samples", [])]
cases += [{"input": "5\n1\n3 3", "output": "4\n2"},
          {"input": "5\n2\n2 3\n5 5", "output": "3\n1\n2"}]
r = post("/judge", {"problemId": "2618", "sourceCode": CODE, "testCases": cases,
                    "publicTestCaseCount": 1, "timeLimit": 1, "memoryLimit": 128})
s = r.get("summary", {})
print("   %s  %s/%s  (%ss)" % (r.get("verdict"), s.get("passed"),
                               s.get("total"), r.get("elapsedSec")))
verdict = r

print()
print("─" * 62)
print("③ 저장 + 커밋  POST /save")
r = post("/save", {
    "site": "BOJ", "no": "2618", "title": "경찰차",
    "url": prob["url"], "code": CODE, "status": "품",
    "date": "2026-08-12", "tags": ["DP", "두 상태 추적"],
    "note": "E2E 파이프라인 테스트로 생성됨",
    "problem": prob, "verdict": verdict,
})
print("   ", json.dumps(r, ensure_ascii=False)[:300])

f = os.path.join(ROOT, r.get("file", ""))
if os.path.exists(f):
    head = io.open(f, encoding="utf-8").read()[:700]
    print()
    print("   --- 생성된 파일 앞부분 ---")
    print("   " + head.replace("\n", "\n   ")[:700])
