"""/judge 로 나가는 요청 payload 형식 추출 + 프라이빗 TC 노출 여부 확인."""
import io, re, json
from playwright.sync_api import sync_playwright

URL = "https://cosal.aviss.kr/problems/detail/2618"

with sync_playwright() as p:
    b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = b.contexts[0]
    pg = ctx.pages[0] if ctx.pages else ctx.new_page()
    pg.goto(URL, wait_until="networkidle", timeout=90_000)
    pg.wait_for_timeout(3000)

    print("=" * 72)
    print("[1] '모두 보기' 클릭 → 프라이빗 테스트케이스가 화면에 나오는가")
    before = len(pg.evaluate("() => document.body.innerText") or "")
    try:
        pg.evaluate("""() => {
            const b=[...document.querySelectorAll('button')]
              .find(x=>(x.innerText||'').includes('모두 보기'));
            if(b) b.click();
        }""")
        pg.wait_for_timeout(2500)
        t = pg.evaluate("() => document.body.innerText") or ""
        print("   본문 %d자 → %d자 (증가 %d)" % (before, len(t), len(t) - before))
        i = t.find("프라이빗")
        io.open(r"C:/Users/solom/AppData/Local/Temp/judge_tc.txt", "w",
                encoding="utf-8").write(t)
        print("   --- 프라이빗 구간 700자 ---")
        print("   " + t[i:i + 700].replace("\n", "\n   "))
    except Exception as e:
        print("   ⚠️", str(e)[:110])

    print()
    print("=" * 72)
    print("[2] JS 번들에서 /judge 요청 payload 구성부")
    html = pg.content()
    scripts = re.findall(r'src="(/_next/static/[^"]+\.js)"', html)
    pats = ["judge", "testcases", "sourceCode", "language"]
    for s in scripts:
        try:
            r = pg.evaluate("""async (u) => { const x=await fetch(u);
                return x.ok ? await x.text() : ''; }""", "https://cosal.aviss.kr" + s)
        except Exception:
            continue
        if not r or "/judge" not in r:
            continue
        print("   ── %s (%d자)" % (s[-40:], len(r)))
        for m in re.finditer(r'.{0,260}fetch\([^)]{0,120}judge.{0,420}', r):
            print("      " + re.sub(r"\s+", " ", m.group(0))[:700])
            print()
        for kw in ("testcase", "testCases", "sourceCode", "source_code", "code:"):
            for m in list(re.finditer(r".{0,90}%s.{0,180}" % kw, r))[:2]:
                print("      [%s] …%s…" % (kw, re.sub(r"\s+", " ", m.group(0))[:260]))
        break
