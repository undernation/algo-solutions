"""
코딩살구(백준 지문) 그림의 '보여 주는 폭'을 모아 problems/boj/<no>.json 의 image_widths 에 넣는다.

왜: 백준 지문 그림은 원본이 크다(중앙값 752px, 최대 2195px). 코딩살구는 그림마다
원문에 적힌 폭(<img width="506"> 등)으로 줄여 보여 주는데, 우리 크롤러는 원본만 받아서
대시보드에서 칸 폭(1080px)까지 커졌다(2026-09-23 사용자 지적: "그림이 너무 크다").
예) 17143: 원본 1660px → 코딩살구 506px, 2048px → 1000px / 2618: 414px → 207px.

  python _meta/crawl_img_widths.py            # 그림 있는 문제 전부(없는 것만)
  python _meta/crawl_img_widths.py --force    # 이미 있는 것도 다시
  python _meta/crawl_img_widths.py 17143 2618 # 지정한 문제만

선행조건: 디버그 크롬(9222) + 코딩살구 로그인.
🚩 순서 맞추기: fetch_problem.py 의 WALK_JS 와 **같은 필터**(60x40 미만·아이콘 제외)로 같은 순서를 센다.
   개수가 저장된 images 와 다르면 어긋난 것이므로 쓰지 않고 보고만 한다.
"""
import os, io, sys, json, glob, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROB = os.path.join(ROOT, "problems", "boj")

JS = r"""async () => {
  const imgsAll = [...document.querySelectorAll('img')];
  imgsAll.forEach(i => { i.loading = 'eager'; });
  const wait = ms => new Promise(r => setTimeout(r, ms));
  for (let k = 0; k < 24; k++) {
    if (!imgsAll.filter(i => !i.complete || i.naturalWidth === 0).length) break;
    await wait(250);
  }
  const root = document.querySelector('.salgu-description');
  if (!root) return JSON.stringify({err: 'no-root'});
  const out = [];
  for (const n of root.querySelectorAll('img')) {
    const w = n.naturalWidth || 0, h = n.naturalHeight || 0;
    if (w < 60 || h < 40) continue;                                   // WALK_JS 와 같은 필터
    const src = n.getAttribute('src') || '';
    if (!src.startsWith('data:') && /profileImage|avatar|icon|logo/i.test(src)) continue;
    const attr = parseInt(n.getAttribute('width') || '0', 10) || 0;
    const shown = Math.round(n.getBoundingClientRect().width);
    out.push({nat: w, attr: attr, shown: shown});
  }
  return JSON.stringify({imgs: out});
}"""


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--force" in sys.argv
    todo = []
    for f in sorted(glob.glob(os.path.join(PROB, "*.json"))):
        no = os.path.splitext(os.path.basename(f))[0]
        if args and no not in args:
            continue
        d = json.load(io.open(f, encoding="utf-8"))
        if not [x for x in (d.get("images") or []) if x]:
            continue
        if d.get("image_widths") and not force:
            continue
        todo.append((no, f, d))
    print("대상 %d문제" % len(todo), flush=True)
    if not todo:
        return 0
    from playwright.sync_api import sync_playwright
    ok = skip = bad = 0
    with sync_playwright() as pw:
        b = pw.chromium.connect_over_cdp("http://127.0.0.1:9222")
        pg = b.contexts[0].new_page()                  # 사용자 탭은 건드리지 않는다
        pg.set_viewport_size({"width": 1440, "height": 900})
        try:
            for i, (no, f, d) in enumerate(todo, 1):
                pg.goto("https://cosal.aviss.kr/problems/detail/%s" % no, wait_until="networkidle", timeout=90000)
                pg.wait_for_timeout(1200)
                if "login" in pg.url:
                    print("❌ 코딩살구 로그인 필요 — 디버그 크롬에서 로그인 후 다시", flush=True)
                    return 2
                r = json.loads(pg.evaluate(JS))
                if r.get("err"):
                    print("  [%d/%d] %s ⚠️ %s" % (i, len(todo), no, r["err"]), flush=True)
                    skip += 1
                    continue
                got = r["imgs"]
                want = len(d.get("images") or [])
                if len(got) != want:
                    print("  [%d/%d] %s ⚠️ 그림 수 불일치(저장 %d / 페이지 %d) — 안 씀" % (i, len(todo), no, want, len(got)), flush=True)
                    bad += 1
                    continue
                # 원문 width 속성이 있으면 그것, 없으면 1440 창에서 실제로 보인 폭(원본보다 크게는 안 함)
                widths = [min(g["attr"] or g["shown"] or g["nat"], g["nat"]) for g in got]
                d["image_widths"] = widths
                tmp = f + ".tmp"
                io.open(tmp, "w", encoding="utf-8", newline="").write(json.dumps(d, ensure_ascii=False, indent=1))
                os.replace(tmp, f)
                ok += 1
                print("  [%d/%d] %s ✅ %s" % (i, len(todo), no, ", ".join("%d→%d" % (g["nat"], w) for g, w in zip(got, widths))), flush=True)
                time.sleep(1.5)                          # 사이트 부담 줄이기
        finally:
            pg.close()
    print("\n완료: 기록 %d / 불일치 %d / 건너뜀 %d" % (ok, bad, skip))
    return 0


if __name__ == "__main__":
    sys.exit(main())
