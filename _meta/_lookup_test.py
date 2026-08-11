"""4개 사이트 역조회 방법 테스트 — 번호/이름으로 문제를 찾을 수 있는가."""
import io, re, json
from playwright.sync_api import sync_playwright

def txt(pg):
    return pg.evaluate("() => document.body.innerText") or ""

with sync_playwright() as p:
    b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = b.contexts[0]
    pg = ctx.pages[0] if ctx.pages else ctx.new_page()

    # ── 1. 코딩살구(BOJ): 번호로 직접 접근 ──────────────────
    print("=" * 70)
    print("[1] 코딩살구 — /problems/detail/{번호} 직접 접근")
    for no in ("2618", "1285"):
        try:
            pg.goto("https://cosal.aviss.kr/problems/detail/%s" % no,
                    wait_until="networkidle", timeout=60_000)
            pg.wait_for_timeout(2500)
            t = txt(pg)
            ok = "login" not in pg.url.lower() and len(t) > 300
            print("   %s → %s (%d자) %s" % (no, "✅" if ok else "❌", len(t), pg.url[:60]))
            if no == "2618":
                io.open(r"C:/Users/solom/AppData/Local/Temp/lk_cosal.txt", "w",
                        encoding="utf-8").write(t)
                io.open(r"C:/Users/solom/AppData/Local/Temp/lk_cosal.html", "w",
                        encoding="utf-8").write(pg.content())
                print("   --- 앞 500자 ---")
                print("   " + t[:500].replace("\n", "\n   "))
        except Exception as e:
            print("   %s ⚠️ %s" % (no, str(e)[:80]))

    # ── 2. SWEA: 검색으로 번호 조회 ────────────────────────
    print()
    print("=" * 70)
    print("[2] SWEA — problemList 검색으로 번호 조회")
    try:
        pg.goto("https://swexpertacademy.com/main/code/problem/problemList.do",
                wait_until="networkidle", timeout=60_000)
        pg.wait_for_timeout(2000)
        # 검색 input 찾기
        info = pg.evaluate("""() => JSON.stringify(
            Array.from(document.querySelectorAll('input,select')).map(e=>({
                t:e.tagName, ty:e.type||'', id:e.id||'', nm:e.name||'', ph:e.placeholder||''
            })).slice(0,15))""")
        print("   입력 요소:", info[:400])
    except Exception as e:
        print("   ⚠️", str(e)[:100])

    # ── 3. 코드트리 검색 ──────────────────────────────────
    print()
    print("=" * 70)
    print("[3] 코드트리 — 문제 검색 페이지 탐색")
    for u in ("https://www.codetree.ai/ko/search?q=%EC%97%AC%EC%99%95%EA%B0%9C%EB%AF%B8",
              "https://www.codetree.ai/ko/missions",
              "https://www.codetree.ai/ko/problems"):
        try:
            pg.goto(u, wait_until="domcontentloaded", timeout=45_000)
            pg.wait_for_timeout(2500)
            t = txt(pg)
            print("   %s → %d자 | %s" % (u.split("/ko/")[1][:34], len(t), pg.url[:64]))
        except Exception as e:
            print("   %s ⚠️ %s" % (u[-30:], str(e)[:60]))

    # ── 4. 프로그래머스 ───────────────────────────────────
    print()
    print("=" * 70)
    print("[4] 프로그래머스 — 내 풀이/문제 검색")
    for u in ("https://school.programmers.co.kr/learn/challenges?order=recent&search=%EA%B4%84%ED%98%B8%20%EB%B3%80%ED%99%98",
              "https://school.programmers.co.kr/my_courses/service"):
        try:
            pg.goto(u, wait_until="domcontentloaded", timeout=45_000)
            pg.wait_for_timeout(3000)
            t = txt(pg)
            print("   %s → %d자 | %s" % (u.split(".kr/")[1][:36], len(t), pg.url[:62]))
            if "challenges" in u:
                io.open(r"C:/Users/solom/AppData/Local/Temp/lk_pgs.txt", "w",
                        encoding="utf-8").write(t)
                print("   --- 앞 300자 ---")
                print("   " + t[:300].replace("\n", "\n   "))
        except Exception as e:
            print("   ⚠️", str(e)[:80])
