"""로그인용 탭 열기 (일회성)"""
from playwright.sync_api import sync_playwright

URLS = [
    ("SWEA",     "https://swexpertacademy.com/main/login.do"),
    ("코딩살구", "https://cosal.aviss.kr/login"),
    ("코드트리", "https://www.codetree.ai/login"),
]

with sync_playwright() as p:
    b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = b.contexts[0]
    for pg in list(ctx.pages)[1:]:
        try:
            pg.close()
        except Exception:
            pass
    first = ctx.pages[0] if ctx.pages else ctx.new_page()
    for i, (name, u) in enumerate(URLS):
        pg = first if i == 0 else ctx.new_page()
        try:
            pg.goto(u, wait_until="domcontentloaded", timeout=45_000)
            print("  ✅ %-8s %s" % (name, pg.url[:80]))
        except Exception as e:
            print("  ⚠️ %-8s %s" % (name, str(e)[:70]))
    first.bring_to_front()
