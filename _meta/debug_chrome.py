"""
크롤링용 디버그 크롬 띄우기.

코딩살구·SWEA·프로그래머스는 모두 로그인 세션이 있어야 문제를 읽을 수 있다.
그래서 크롤러는 CDP(9222)로 "로그인된 크롬"에 붙는다. 이 스크립트는 그 크롬을 띄운다.

평소 쓰는 크롬과 **프로필이 분리**되어 있어 동시에 켜도 서로 방해하지 않고,
한 번 로그인해 두면 프로필에 세션이 남아 다음에도 유지된다.

사용법:
    python _meta/debug_chrome.py              # 띄우고 상태 확인
    python _meta/debug_chrome.py --check      # 이미 떠 있는지만 확인
    python _meta/debug_chrome.py --port 9222
    python _meta/debug_chrome.py --open https://cosal.aviss.kr/problems

띄운 뒤 할 일:
    코딩살구 / SWEA 에 로그인 → 그 다음 크롤러 실행
        python _meta/crawl_all.py
"""
import os, sys, json, time, shutil, argparse, subprocess, urllib.request

PROFILE = os.path.join(os.path.expanduser("~"), "chrome-debug-profile")

# 설치 위치는 OS·환경마다 다르므로 후보를 순서대로 찾는다.
CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
]


def find_chrome():
    for c in CANDIDATES:
        if c and os.path.exists(c):
            return c
    for name in ("chrome", "google-chrome", "chromium", "chromium-browser"):
        p = shutil.which(name)
        if p:
            return p
    return ""


def alive(port):
    """CDP 가 응답하면 버전 문자열, 아니면 빈 문자열."""
    try:
        with urllib.request.urlopen("http://127.0.0.1:%d/json/version" % port,
                                    timeout=3) as r:
            return json.loads(r.read().decode()).get("Browser", "?")
    except Exception:
        return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=9222)
    ap.add_argument("--check", action="store_true", help="띄우지 않고 확인만")
    ap.add_argument("--open", default="https://cosal.aviss.kr/problems",
                    help="처음 열 주소")
    a = ap.parse_args()

    v = alive(a.port)
    if v:
        print("✅ 이미 떠 있음 — %s  (포트 %d)" % (v, a.port))
        print("   프로필: %s" % PROFILE)
        return 0
    if a.check:
        print("❌ 디버그 크롬이 떠 있지 않습니다 (포트 %d)" % a.port)
        return 1

    exe = find_chrome()
    if not exe:
        print("❌ 크롬을 찾지 못했습니다. 설치 경로를 CANDIDATES 에 추가하세요.")
        return 1

    os.makedirs(PROFILE, exist_ok=True)
    cmd = [exe,
           "--remote-debugging-port=%d" % a.port,
           "--user-data-dir=%s" % PROFILE,
           "--no-first-run", "--no-default-browser-check",
           a.open]
    print("크롬 실행: %s" % exe)
    print("프로필   : %s  (평소 크롬과 분리 — 동시 사용 가능)" % PROFILE)
    subprocess.Popen(cmd, close_fds=True)

    for _ in range(20):
        time.sleep(1)
        v = alive(a.port)
        if v:
            print("✅ CDP 연결됨 — %s  (포트 %d)" % (v, a.port))
            print()
            print("다음: 코딩살구·SWEA 에 로그인한 뒤")
            print("      python _meta/crawl_all.py")
            return 0
    print("⚠️ 떴지만 CDP 응답이 없습니다. 포트 충돌인지 확인하세요.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
