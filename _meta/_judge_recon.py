"""코딩살구 채점서버 연동 규격 정찰 — /judge 요청 형식, 언어 지원, repo 링크."""
import io, re, json
from playwright.sync_api import sync_playwright

URL = "https://cosal.aviss.kr/problems/detail/2618"

with sync_playwright() as p:
    b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = b.contexts[0]
    pg = ctx.pages[0] if ctx.pages else ctx.new_page()
    pg.goto(URL, wait_until="networkidle", timeout=90_000)
    pg.wait_for_timeout(3000)

    html = pg.content()
    io.open(r"C:/Users/solom/AppData/Local/Temp/judge.html", "w", encoding="utf-8").write(html)

    print("=" * 70)
    print("[1] repo / github 링크")
    for m in sorted(set(re.findall(r'https?://[^\s"\'<>]*(?:github|gitlab)[^\s"\'<>]*', html))):
        print("   ", m[:110])
    print()

    print("[2] judge / localhost 관련 문자열")
    for m in sorted(set(re.findall(r'[^\s"\'<>]{0,40}(?:localhost|/judge|judge_|judgeServer)[^\s"\'<>]{0,50}', html)))[:20]:
        print("   ", m[:110])
    print()

    print("[3] 언어 선택 UI 존재 여부")
    sel = pg.evaluate("""() => JSON.stringify(
      Array.from(document.querySelectorAll('select,button,[role=tab],[class*=lang]'))
        .map(e=>({t:e.tagName,c:(e.className||'').slice(0,40),x:(e.innerText||'').trim().slice(0,30)}))
        .filter(o=>o.x).slice(0,25))""")
    print("   ", (sel or "")[:900])
    print()

    print("[4] 페이지 JS 번들에서 judge 호출부 찾기")
    scripts = re.findall(r'src="(/_next/static/[^"]+\.js)"', html)
    print("    번들 %d개" % len(scripts))
    found = 0
    for s in scripts[:40]:
        try:
            r = pg.evaluate("""async (u) => {
                const res = await fetch(u); if(!res.ok) return '';
                return await res.text(); }""", "https://cosal.aviss.kr" + s)
        except Exception:
            continue
        if not r or "judge" not in r:
            continue
        found += 1
        print("    ── %s" % s[-42:])
        for m in re.finditer(r".{140}judge.{220}", r):
            frag = re.sub(r"\s+", " ", m.group(0))
            print("       …%s…" % frag[:340])
            break
        if found >= 3:
            break
