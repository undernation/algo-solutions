"""4개 소스 로그인 상태 확인 + 미로그인 사이트는 로그인 페이지로."""
from playwright.sync_api import sync_playwright

CHECK = [
    ("SWEA",       "https://swexpertacademy.com/main/code/problem/problemList.do",
     "https://swexpertacademy.com/main/login.do"),
    ("코딩살구",    "https://cosal.aviss.kr/problems",
     "https://cosal.aviss.kr/login"),
    ("코드트리",    "https://www.codetree.ai/trails",
     "https://www.codetree.ai/login"),
    ("프로그래머스", "https://school.programmers.co.kr/learn/challenges",
     "https://programmers.co.kr/account/sign_in"),
]

with sync_playwright() as p:
    b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = b.contexts[0]
    for pg in list(ctx.pages)[1:]:
        try:
            pg.close()
        except Exception:
            pass
    base = ctx.pages[0] if ctx.pages else ctx.new_page()

    need = []
    for i, (name, probe, login) in enumerate(CHECK):
        pg = base if i == 0 else ctx.new_page()
        try:
            pg.goto(probe, wait_until="domcontentloaded", timeout=45_000)
            pg.wait_for_timeout(2000)
            url = pg.url.lower()
            body = (pg.evaluate("() => document.body.innerText") or "")[:400]
            ok = not any(k in url for k in ("login", "sign_in", "anonymous"))
            ok = ok and "로그인" not in body[:120]
            print("  %-8s %s  %s" % (name, "✅ 로그인됨" if ok else "❌ 필요", pg.url[:70]))
            if not ok:
                need.append((name, login, pg))
        except Exception as e:
            print("  %-8s ⚠️ %s" % (name, str(e)[:60]))

    for name, login, pg in need:
        try:
            pg.goto(login, wait_until="domcontentloaded", timeout=45_000)
        except Exception:
            pass
    if need:
        print("\n  → 로그인 필요: " + ", ".join(n for n, _, _ in need))
        base.bring_to_front()
