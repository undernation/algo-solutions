"""
현재 Cloudflare 터널 URL을 _meta/endpoint.json 으로 publish (변경 시에만 커밋/푸시).

서버(Oracle VM)에서 systemd timer 로 주기 실행한다.
quick tunnel 은 재시작마다 URL 이 바뀌므로, 대시보드가 이 파일을 읽어
자동으로 새 주소를 따라가게 하는 것이 목적.

사용법:
    python3 _meta/publish_endpoint.py
    python3 _meta/publish_endpoint.py --url https://xxx.trycloudflare.com   # 수동 지정
"""
import os, io, re, sys, json, subprocess, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "_meta", "endpoint.json")


def sh(*a, **kw):
    return subprocess.run(list(a), capture_output=True, text=True,
                          encoding="utf-8", errors="replace", **kw)


def find_url():
    if "--url" in sys.argv:
        return sys.argv[sys.argv.index("--url") + 1]
    # 1) 서비스 로그
    r = sh("journalctl", "-u", "algo-tunnel.service", "--since", "-24h", "--no-pager")
    m = re.findall(r"https://[a-z0-9-]+\.trycloudflare\.com", r.stdout or "")
    if m:
        return m[-1]
    # 2) 배포 스크립트가 남긴 파일
    p = os.path.join(ROOT, ".tunnel_url")
    if os.path.exists(p):
        return io.open(p, encoding="utf-8").read().strip()
    return ""


def main():
    url = find_url()
    if not url:
        print("⚠️ 터널 URL 을 찾지 못함")
        return 1

    # 살아있는지 확인
    alive = False
    try:
        import urllib.request
        with urllib.request.urlopen(url + "/", timeout=20) as r:
            alive = json.loads(r.read().decode()).get("ok") is True
    except Exception as e:
        print("⚠️ 응답 없음:", str(e)[:90])

    prev = {}
    if os.path.exists(OUT):
        try:
            prev = json.load(io.open(OUT, encoding="utf-8"))
        except Exception:
            pass
    if prev.get("url") == url and prev.get("alive") == alive:
        print("변경 없음:", url)
        return 0

    data = {"url": url, "alive": alive,
            "updatedAt": datetime.datetime.now(datetime.timezone.utc)
            .isoformat(timespec="seconds").replace("+00:00", "Z"),
            "note": "Cloudflare quick tunnel — 재시작 시 URL 이 바뀐다. "
                    "모든 POST 는 X-Auth-Token 헤더가 필요."}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, "w", encoding="utf-8", newline="").write(
        json.dumps(data, ensure_ascii=False, indent=1))

    sh("git", "add", "_meta/endpoint.json", cwd=ROOT)
    c = sh("git", "commit", "-m", "chore: 허브 엔드포인트 갱신", cwd=ROOT)
    if c.returncode == 0:
        # 원격이 앞서 있을 수 있으므로 rebase 후 push
        sh("git", "pull", "--rebase", "-q", cwd=ROOT)
        p = sh("git", "push", cwd=ROOT)
        print("✅ publish %s (alive=%s) push=%s" % (url, alive, p.returncode == 0))
        if p.returncode != 0:
            print("   ", (p.stderr or "")[:200])
    else:
        print("커밋할 변경 없음")
    return 0


if __name__ == "__main__":
    sys.exit(main())
