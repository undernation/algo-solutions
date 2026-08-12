"""
전체 테스트케이스를 채점 서버로 올린다.

코딩살구의 히든 TC 는 실제 채점용이라 매우 크다(BOJ 2493 탑 = 28MB, 50만 개 숫자).
repo 에 넣으면 problems/ 가 565MB 가 되어 GitHub Pages 빌드가 실패하고,
브라우저도 문제 하나 보려고 28MB 를 받아야 한다.

  repo        200KB 로 줄인 보기용        (커밋됨)
  채점 서버    전체 테스트케이스            (~/algo-tc, 커밋 안 됨)

대시보드는 채점할 때 케이스를 올리지 않고 useStoredTC 만 보내며,
서버가 보관본으로 채점한다.

사용법:
    python _meta/sync_tc.py                 # 없는 것만 올림
    python _meta/sync_tc.py --force         # 전부 다시
    python _meta/sync_tc.py --url http://127.0.0.1:12014   # 로컬 허브로
"""
import os, io, sys, json, glob, time, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE = os.path.join(ROOT, "_meta", "tc_store")


def hub_url(argv):
    if "--url" in argv:
        return argv[argv.index("--url") + 1].rstrip("/")
    p = os.path.join(ROOT, "_meta", "endpoint.json")
    if os.path.exists(p):
        u = json.load(io.open(p, encoding="utf-8")).get("url")
        if u:
            return u.rstrip("/")
    return "http://127.0.0.1:12014"


def post(url, path, body, tok, timeout=300):
    r = urllib.request.Request(
        url + path, data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"content-type": "application/json; charset=utf-8", "X-Auth-Token": tok})
    return json.load(urllib.request.urlopen(r, timeout=timeout))


def main():
    argv = sys.argv[1:]
    force = "--force" in argv
    url = hub_url(argv)
    tok = io.open(os.path.expanduser("~/.algo-hub-token"), encoding="utf-8").read().strip()

    files = sorted(glob.glob(os.path.join(STORE, "*", "*.json")))
    if not files:
        print("올릴 것이 없습니다: %s" % STORE)
        return 0
    tot = sum(os.path.getsize(f) for f in files)
    print("허브 : %s" % url)
    print("대상 : %d문제  %.0f MB" % (len(files), tot / 1e6))

    ok = skip = ng = 0
    t0 = time.time()
    for i, f in enumerate(files, 1):
        sub = os.path.basename(os.path.dirname(f))
        no = os.path.splitext(os.path.basename(f))[0]
        site = {"boj": "BOJ", "swea": "SWEA",
                "programmers": "PGS", "codetree": "CT"}.get(sub, "BOJ")
        try:
            if not force:
                info = post(url, "/tc", {"site": site, "no": no}, tok, timeout=60)
                if info.get("stored"):
                    skip += 1
                    continue
            d = json.load(io.open(f, encoding="utf-8"))
            r = post(url, "/tcupload",
                     {"site": site, "no": no,
                      "samples": d.get("samples") or [],
                      "private": d.get("private") or []}, tok)
            if r.get("ok"):
                ok += 1
                print("  [%d/%d] %s %-6s ✅ %d개  %.1fMB"
                      % (i, len(files), site, no, r.get("private", 0),
                         os.path.getsize(f) / 1e6), flush=True)
            else:
                ng += 1
                print("  [%d/%d] %s %-6s ❌ %s"
                      % (i, len(files), site, no, str(r.get("error"))[:50]), flush=True)
        except Exception as e:
            ng += 1
            print("  [%d/%d] %s %-6s ❌ %s"
                  % (i, len(files), site, no, str(e).split("\n")[0][:60]), flush=True)

    print("\n완료: 올림 %d / 이미있음 %d / 실패 %d / %.1f분"
          % (ok, skip, ng, (time.time() - t0) / 60))
    return 0


if __name__ == "__main__":
    sys.exit(main())
