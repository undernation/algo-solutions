"""
코딩살구클럽 전체 문제 목록 수집 → _meta/cosal_list.json

주차별(/week/1..N) + 개념별심화학습(/concepts) + 코딩테스트(/codingtest) 를 훑어
번호·제목·라벨·소속(주차/섹션)·해결여부를 모은다.
문제 지문은 여기서 받지 않는다(crawl_all.py 담당).

사용법:
    python _meta/crawl_cosal_list.py
선행조건: 디버그 크롬(9222) + 코딩살구 로그인
"""
import os, io, re, sys, json, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "_meta", "cosal_list.json")

# 링크 하나마다 (번호, 제목, 라벨, 해결여부) 를 뽑는 브라우저측 함수.
# 라벨(1-A 등)·해결표시는 링크의 조상 카드 안에 텍스트로 들어 있다.
JS = """
() => {
  const out = [];
  const seen = new Set();
  document.querySelectorAll('a[href^="/problems/detail/"]').forEach(a => {
    const no = a.getAttribute('href').split('/').pop();
    const title = (a.innerText || '').trim();
    if (!no || !title) return;
    if (seen.has(no + '|' + title)) return;
    seen.add(no + '|' + title);
    let card = a, txt = '';
    for (let i = 0; i < 6 && card; i++) {
      card = card.parentElement;
      if (!card) break;
      txt = (card.innerText || '');
      if (txt.length > title.length + 6) break;
    }
    const lab = txt.match(/\\b(\\d{1,2}-[A-Z]{1,2})\\b/);
    out.push({
      no: no,
      title: title,
      label: lab ? lab[1] : '',
      /* 해결여부는 페이지 전역 문구와 섞여 신뢰할 수 없어 쓰지 않는다.
         푼 문제 판정은 옵시디언 실수노트 기반 history.json 으로 한다. */
    });
  });
  return JSON.stringify(out);
}
"""


def scrape(pg, url, section):
    pg.goto(url, wait_until="networkidle", timeout=90_000)
    pg.wait_for_timeout(2600)
    if "login" in pg.url.lower():
        raise SystemExit("❌ 코딩살구 로그인 필요")
    items = json.loads(pg.evaluate(JS))
    for it in items:
        it["section"] = section
    return items


def main():
    from playwright.sync_api import sync_playwright
    all_items, order = {}, []
    with sync_playwright() as pw:
        b = pw.chromium.connect_over_cdp("http://127.0.0.1:9222")
        pg = b.contexts[0].new_page()
        try:
            # 주차 개수 파악
            pg.goto("https://cosal.aviss.kr/problems", wait_until="networkidle", timeout=90_000)
            pg.wait_for_timeout(2600)
            weeks = sorted({int(m) for m in re.findall(
                r'/week/(\d+)', pg.evaluate(
                    "() => [...document.querySelectorAll('a[href]')]"
                    ".map(a=>a.getAttribute('href')).join(' ')"))})
            print("주차: %s" % (weeks or "없음"), flush=True)

            pages = [("https://cosal.aviss.kr/week/%d" % w, "주차별/%d주차" % w) for w in weeks]

            # 개념별 심화학습 — 하위 트랙 페이지들
            pg.goto("https://cosal.aviss.kr/concepts", wait_until="networkidle", timeout=90_000)
            pg.wait_for_timeout(2400)
            slugs = []
            for h in re.findall(r'/concepts/([a-z\-]+)', pg.evaluate(
                    "() => [...document.querySelectorAll('a[href]')]"
                    ".map(a=>a.getAttribute('href')).join(' ')")):
                if h not in slugs:
                    slugs.append(h)
            CN = {"impl": "문자열·누적합·구현", "graph": "그래프·DFS·BFS",
                  "bruteforce": "완전탐색·백트래킹", "bitmask": "비트마스킹",
                  "greedy": "그리디·라인스위핑·투포인터", "binary-search": "이분탐색·LIS",
                  "dp": "DP", "advanced": "펜윅트리·최단거리"}
            print("개념 트랙: %s" % (slugs or "없음"), flush=True)
            pages += [("https://cosal.aviss.kr/concepts/%s" % s2,
                       "개념별/" + CN.get(s2, s2)) for s2 in slugs]
            pages += [("https://cosal.aviss.kr/codingtest", "코딩테스트")]

            for url, sec in pages:
                try:
                    items = scrape(pg, url, sec)
                except Exception as e:
                    print("  %-16s ❌ %s" % (sec, str(e).split("\n")[0][:60]), flush=True)
                    continue
                new = 0
                for it in items:
                    k = it["no"]
                    if k not in all_items:
                        all_items[k] = it
                        order.append(k)
                        new += 1
                    elif it.get("label") and not all_items[k].get("label"):
                        all_items[k]["label"] = it["label"]
                print("  %-16s %3d개 (신규 %d)" % (sec, len(items), new), flush=True)
        finally:
            try:
                pg.close()
            except Exception:
                pass

    data = {"built": datetime.date.today().isoformat(),
            "count": len(all_items),
            "items": [all_items[k] for k in order]}
    io.open(OUT, "w", encoding="utf-8", newline="").write(
        json.dumps(data, ensure_ascii=False, indent=1))
    solved = sum(1 for k in all_items if all_items[k].get("solved"))
    print("\n✅ 총 %d문제 (해결 표시 %d) → _meta/cosal_list.json" % (len(all_items), solved))


if __name__ == "__main__":
    main()
