"""소스 사이트 접근성 정찰 — 뭐가 긁히는지 확인용 (일회성)"""
import io, json, sys
from playwright.sync_api import sync_playwright

TARGETS = [
    ("cosal_2618", "https://cosal.aviss.kr/problems/detail/2618"),
    ("swea_user",  "https://swexpertacademy.com/main/code/userProblem/userProblemDetail.do?contestProbId=AZ9jCXaKviHHBITH"),
    ("codetree",   "https://www.codetree.ai/"),
]

with sync_playwright() as p:
    b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = b.contexts[0]
    pg = ctx.pages[0] if ctx.pages else ctx.new_page()
    for name, url in TARGETS:
        print("=" * 70)
        print("[%s]" % name, url[:90])
        try:
            pg.goto(url, wait_until="networkidle", timeout=60_000)
            pg.wait_for_timeout(2500)
            body = pg.evaluate("() => document.body.innerText") or ""
            io.open(r"C:/Users/solom/AppData/Local/Temp/probe_%s.txt" % name,
                    "w", encoding="utf-8").write(body)
            io.open(r"C:/Users/solom/AppData/Local/Temp/probe_%s.html" % name,
                    "w", encoding="utf-8").write(pg.content())
            print("  최종 URL :", pg.url[:95])
            print("  title    :", pg.evaluate("() => document.title")[:70])
            print("  본문 길이 :", len(body))
            low = (pg.url + body[:400]).lower()
            print("  로그인 필요 여부 :", "로그인" in body[:300] or "login" in low)
            print("  --- 본문 앞 400자 ---")
            print("  " + body[:400].replace("\n", "\n  "))
        except Exception as e:
            print("  ⚠️", str(e)[:150])
        print()
