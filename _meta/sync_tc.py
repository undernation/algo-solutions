"""
전체 테스트케이스를 채점 서버로 올린다.

코딩살구의 히든 TC 는 실제 채점용이라 매우 크다(BOJ 2493 탑 = 28MB, 50만 개 숫자).
repo 에 넣으면 problems/ 가 565MB 가 되어 GitHub Pages 빌드가 실패하고,
브라우저도 문제 하나 보려고 28MB 를 받아야 한다.

  repo        200KB 로 줄인 보기용        (커밋됨)
  채점 서버    전체 테스트케이스            (~/algo-tc, 커밋 안 됨)

대시보드는 채점할 때 케이스를 올리지 않고 useStoredTC 만 보내며,
서버가 보관본으로 채점한다.

🔒 코드트리는 보관소 파일에 지문(problem)까지 들어 있다. 비공개 모드(_meta/judge_config.json
   의 privateSites 에 CT)면 repo 에 없는 지문을 클라우드 허브가 /prob 로 내주려면 여기서 같이
   올라가야 한다. 공개 모드여도 올려 두면 나중에 비공개로 돌릴 때 그대로 쓴다(모드와 무관하게 올린다).

사용법:
    python _meta/sync_tc.py                 # 없는 것만 올림
    python _meta/sync_tc.py --force         # 전부 다시
    python _meta/sync_tc.py --url http://127.0.0.1:12014   # 로컬 허브로
    python _meta/sync_tc.py --site CT       # 코드트리만
    python _meta/sync_tc.py --only codetree/386 --only codetree/196   # 콕 집어서(쉼표로 여러 개도 됨)

종료코드: 하나라도 실패하면(또는 --only 로 고른 파일이 없으면) 1.
         허브의 /fetch 가 이걸로 synced 를 판정한다.
"""
import os, io, sys, json, glob, time, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE = os.path.join(ROOT, "_meta", "tc_store")
SITE = {"boj": "BOJ", "swea": "SWEA", "programmers": "PGS", "codetree": "CT"}
SUB = dict((v, k) for k, v in SITE.items())


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


def opt_values(argv, name):
    """--name 값을 전부 모은다. 여러 번 줘도, 쉼표로 이어 줘도 된다."""
    out = []
    for i, a in enumerate(argv):
        v = None
        if a == name and i + 1 < len(argv):
            v = argv[i + 1]
        elif a.startswith(name + "="):
            v = a[len(name) + 1:]
        if v:
            out += [x.strip() for x in v.split(",") if x.strip()]
    return out


def to_sub(s):
    """'codetree' · 'CT' 둘 다 받아 하위 폴더 이름으로. 모르면 None."""
    s = (s or "").strip()
    if s.lower() in SITE:
        return s.lower()
    return SUB.get(s.upper())


def local_has_problem(f):
    """보관소 파일에 지문(problem)이 들어 있나.

    큰 BOJ 파일(수십 MB)까지 매번 JSON 으로 풀지 않도록 키 이름부터 훑는다.
    문자열 안의 따옴표는 \\" 로 이스케이프되므로 '"problem":' 는 키 자리에서만 나온다.
    """
    try:
        blob = io.open(f, "rb").read()
        if b'"problem":' not in blob:
            return False
        return bool(json.loads(blob.decode("utf-8")).get("problem"))
    except Exception:
        return False


def main():
    argv = sys.argv[1:]
    force = "--force" in argv
    url = hub_url(argv)
    tp = os.path.expanduser("~/.algo-hub-token")
    if not os.path.exists(tp):
        print("❌ 토큰 파일이 없습니다: %s  (허브의 ~/.algo-hub-token 과 같은 값)" % tp)
        return 1
    tok = io.open(tp, encoding="utf-8").read().strip()

    files = sorted(glob.glob(os.path.join(STORE, "*", "*.json")))
    missing = []
    only = opt_values(argv, "--only")
    if only:
        want = []
        for x in only:
            x = x.replace("\\", "/").strip("/")
            if x.lower().endswith(".json"):
                x = x[:-5]
            sub, _, no = x.rpartition("/")
            if not to_sub(sub) or not no:
                print("❌ --only 형식은 <sub>/<no> 입니다 (예: codetree/386): %s" % x)
                return 1
            want.append(os.path.join(STORE, to_sub(sub), "%s.json" % no))
        missing = [w for w in want if not os.path.exists(w)]
        files = [w for w in want if os.path.exists(w)]
    sites = opt_values(argv, "--site")
    if sites:
        subs = set(to_sub(s) for s in sites)
        if None in subs:
            print("❌ 모르는 사이트: %s  (BOJ/SWEA/PGS/CT)" % ", ".join(sites))
            return 1
        files = [f for f in files if os.path.basename(os.path.dirname(f)) in subs]
    for w in missing:
        print("  ❌ 로컬 보관소에 없음: %s" % os.path.relpath(w, ROOT).replace(os.sep, "/"))
    if not files:
        print("올릴 것이 없습니다: %s" % STORE)
        return 1 if missing else 0
    tot = sum(os.path.getsize(f) for f in files)
    print("허브 : %s" % url)
    print("대상 : %d문제  %.0f MB" % (len(files), tot / 1e6))

    ok = skip = ng = 0
    t0 = time.time()
    for i, f in enumerate(files, 1):
        sub = os.path.basename(os.path.dirname(f))
        no = os.path.splitext(os.path.basename(f))[0]
        site = SITE.get(sub, "BOJ")
        try:
            if not force:
                info = post(url, "/tc", {"site": site, "no": no}, tok, timeout=60)
                # 보관소 파일에 지문(problem)이 있으면 서버에도 지문이 있어야 '이미 있음'이다.
                # 예전 sync 는 problem 을 안 보냈고 예전 서버는 받아도 버렸다 — TC 만 있는
                # 채로 stored=True 라고 건너뛰면 클라우드 /prob 가 영영 비어 있게 된다.
                if info.get("stored") and (info.get("hasProblem") or not local_has_problem(f)):
                    skip += 1
                    continue
            d = json.load(io.open(f, encoding="utf-8"))
            body = {"site": site, "no": no,
                    "samples": d.get("samples") or [],
                    "private": d.get("private") or []}
            if d.get("problem"):
                body["problem"] = d["problem"]
            r = post(url, "/tcupload", body, tok)
            if r.get("ok"):
                ok += 1
                print("  [%d/%d] %s %-6s ✅ %d개%s  %.1fMB"
                      % (i, len(files), site, no, r.get("private", 0),
                         " +지문" if body.get("problem") else "",
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
          % (ok, skip, ng + len(missing), (time.time() - t0) / 60))
    return 1 if (ng or missing) else 0


if __name__ == "__main__":
    sys.exit(main())
