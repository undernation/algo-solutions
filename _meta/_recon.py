"""각 사이트에서 '내가 푼 문제 / 제출내역'이 어디에 있는지 정찰."""
import io, json, re
from playwright.sync_api import sync_playwright

OUT = r"C:/Users/solom/AppData/Local/Temp/recon_%s.txt"

TARGETS = [
    # (이름, URL, 설명)
    ("swea_mypage",   "https://swexpertacademy.com/main/myPage/myPage.do", "SWEA 마이페이지"),
    ("swea_solved",   "https://swexpertacademy.com/main/code/problem/problemList.do", "SWEA 문제목록(해결여부)"),
    ("cosal_problems","https://cosal.aviss.kr/problems", "코딩살구 문제목록"),
    ("cosal_2618",    "https://cosal.aviss.kr/problems/detail/2618", "코딩살구 문제상세"),
    ("ct_dash",       "https://www.codetree.ai/ko/trails/complete/dashboard/codetree-101", "코드트리 대시보드"),
]


def dump(pg, key, desc):
    print("=" * 72)
    print("[%s] %s" % (key, desc))
    try:
        pg.goto_url  # noqa
    except Exception:
        pass


with sync_playwright() as p:
    b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = b.contexts[0]
    pg = ctx.pages[0] if ctx.pages else ctx.new_page()

    for key, url, desc in TARGETS:
        print("=" * 72)
        print("[%s] %s" % (key, desc))
        print("  ", url[:95])
        try:
            pg.goto(url, wait_until="networkidle", timeout=70_000)
            pg.wait_for_timeout(3000)
            body = pg.evaluate("() => document.body.innerText") or ""
            html = pg.content()
            io.open(OUT % key, "w", encoding="utf-8").write(body)
            io.open((OUT % key).replace(".txt", ".html"), "w", encoding="utf-8").write(html)
            print("   최종 URL:", pg.url[:88])
            print("   본문 %d자 / HTML %d자" % (len(body), len(html)))
            # 링크 패턴 힌트
            hrefs = re.findall(r'href="([^"]{5,90})"', html)
            pats = {}
            for h in hrefs:
                k = re.sub(r"\d+", "N", h)
                pats[k] = pats.get(k, 0) + 1
            top = sorted(pats.items(), key=lambda x: -x[1])[:8]
            print("   링크 패턴 top8:")
            for k, c in top:
                print("     %3d  %s" % (c, k[:80]))
            print("   --- 본문 앞 350자 ---")
            print("   " + body[:350].replace("\n", "\n   "))
        except Exception as e:
            print("   ⚠️", str(e)[:130])
        print()
