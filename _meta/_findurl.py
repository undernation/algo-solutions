"""코드트리 / 프로그래머스 문제 상세 URL 패턴 찾기."""
import io, re, json
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = b.contexts[0]
    pg = ctx.pages[0] if ctx.pages else ctx.new_page()

    print("=" * 70)
    print("[코드트리] trail 페이지에서 문제 링크 패턴 찾기")
    for u in ("https://www.codetree.ai/ko/trails/complete/dashboard/codetree-101",
              "https://www.codetree.ai/ko/trail-info"):
        try:
            pg.goto(u, wait_until="networkidle", timeout=60_000)
            pg.wait_for_timeout(3000)
            h = pg.content()
            hrefs = set(re.findall(r'href="(/ko/[^"]{5,90})"', h))
            pats = {}
            for x in hrefs:
                pats.setdefault(re.sub(r"[0-9a-f]{6,}|\d+", "*", x), []).append(x)
            print("  " + u[-46:])
            for k, v in sorted(pats.items(), key=lambda t: -len(t[1]))[:10]:
                print("    %3d  %-46s ex: %s" % (len(v), k[:46], v[0][:52]))
        except Exception as e:
            print("  ⚠️", str(e)[:90])

    print()
    print("=" * 70)
    print("[프로그래머스] 문제 목록에서 링크 패턴")
    try:
        pg.goto("https://school.programmers.co.kr/learn/challenges?order=recent",
                wait_until="networkidle", timeout=60_000)
        pg.wait_for_timeout(3500)
        h = pg.content()
        hrefs = set(re.findall(r'href="(/learn/courses/[^"]{5,70})"', h))
        print("  lessons 링크 %d개" % len(hrefs))
        for x in list(hrefs)[:6]:
            print("    ", x)
        # 내 풀이 이력 후보 경로
        print()
        print("  내 기록 페이지 후보 탐색:")
        for u in ("https://school.programmers.co.kr/my_courses/service",
                  "https://school.programmers.co.kr/learn/challenges?statuses=solved",
                  "https://programmers.co.kr/my/challenges"):
            try:
                pg.goto(u, wait_until="domcontentloaded", timeout=40_000)
                pg.wait_for_timeout(2500)
                t = pg.evaluate("() => document.body.innerText") or ""
                print("    %-52s %d자 → %s" % (u.split(".kr")[1][:52], len(t), pg.url[:58]))
            except Exception as e:
                print("    ⚠️", str(e)[:70])
    except Exception as e:
        print("  ⚠️", str(e)[:90])
