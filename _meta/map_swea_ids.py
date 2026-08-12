"""
SWEA 문제번호 -> contestProbId 매핑 수집 → _meta/swea_ids.json

SWEA 는 표시번호(2382)와 내부 ID(AWXR…)가 달라 번호만으로는 문제 페이지를 열 수 없다.
문제 목록의 검색(#searchinput + fn_Search)으로 번호를 조회해 목록 행의
fn_move_page('<ID>') 에서 ID 를 뽑는다.

사용법:
    python _meta/map_swea_ids.py                 # history.json 의 SWEA 번호 전부
    python _meta/map_swea_ids.py 2382 4013       # 특정 번호만
    python _meta/map_swea_ids.py --all --force   # 이미 있는 것도 다시

선행조건: 디버그 크롬(9222) + SWEA 로그인
"""
import os, io, re, sys, json, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "_meta", "swea_ids.json")
LIST = "https://swexpertacademy.com/main/code/problem/problemList.do"

# 목록 행에서 (contestProbId, 행 텍스트) 를 뽑는다.
ROWS_JS = (
    "() => { const out=[];"
    " document.querySelectorAll('[onclick]').forEach(e=>{"
    "  const oc=e.getAttribute('onclick')||'';"
    "  const m=oc.match(/fn_move_page\\(['\\\"]([A-Za-z0-9+/=_-]+)['\\\"]\\)/);"
    "  if(!m) return;"
    "  let card=e, txt=(e.innerText||'').trim();"
    "  for(let i=0;i<4&&card&&txt.length<8;i++){card=card.parentElement;"
    "    if(card) txt=(card.innerText||'').trim();}"
    "  out.push({id:m[1], txt:txt.slice(0,120)}); });"
    " return JSON.stringify(out); }")


def wanted():
    """history.json 의 SWEA 번호 목록(오름차순)."""
    h = json.load(io.open(os.path.join(ROOT, "_meta", "history.json"), encoding="utf-8"))
    seen = {}
    for day in sorted(h):
        for it in h[day].get("items", []):
            if isinstance(it, dict) and it.get("site") == "SWEA":
                no = str(it.get("no") or "").strip()
                if no.isdigit():
                    seen[no] = it.get("title", "")
    return seen


TABS = [
    ("Problem", "https://swexpertacademy.com/main/code/problem/problemList.do"),
    ("User", "https://swexpertacademy.com/main/code/userProblem/userProblemList.do"),
    ("Contest", "https://swexpertacademy.com/main/code/contestProblem/contestProblemList.do"),
]


def search(pg, kw):
    pg.evaluate("(k)=>{const e=document.getElementById('searchinput'); if(e) e.value=k;}", kw)
    pg.evaluate("() => (typeof fn_Search==='function') && fn_Search()")
    pg.wait_for_load_state("networkidle", timeout=60_000)
    pg.wait_for_timeout(1200)
    return json.loads(pg.evaluate(ROWS_JS))


def pick(rows, no, title):
    """번호가 정확히 일치하는 행 우선, 없으면 제목 일치, 그래도 없으면 단일 후보."""
    for r in rows:
        m = re.search(r"(?:^|\n)\s*(\d{3,6})\s*\.", r["txt"])
        if m and m.group(1) == no:
            return r
    if title:
        norm = re.sub(r"\s+", "", title)
        for r in rows:
            if norm and norm in re.sub(r"\s+", "", r["txt"]):
                return r
    return rows[0] if len(rows) == 1 else None


def find(pg, no, title):
    """번호 → 제목 순으로, 세 탭을 돌며 찾는다."""
    for tab, url in TABS:
        try:
            pg.goto(url, wait_until="networkidle", timeout=90_000)
            pg.wait_for_timeout(1200)
        except Exception:
            continue
        for kw in ([no, title] if title else [no]):
            if not kw:
                continue
            try:
                rows = search(pg, kw)
            except Exception:
                continue
            hit = pick(rows, no, title)
            if hit:
                return hit, tab
    return None, ""


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--force" in sys.argv

    ids = {}
    if os.path.exists(OUT):
        try:
            ids = json.load(io.open(OUT, encoding="utf-8"))
        except Exception:
            ids = {}

    todo = wanted()
    if args:
        todo = {k: todo.get(k, "") for k in args}
    if not force:
        todo = {k: v for k, v in todo.items() if k not in ids}
    order = sorted(todo, key=lambda x: int(x))
    print("대상 %d개 (기존 매핑 %d개)" % (len(order), len(ids)), flush=True)
    if not order:
        return

    from playwright.sync_api import sync_playwright
    ok = ng = 0
    with sync_playwright() as pw:
        b = pw.chromium.connect_over_cdp("http://127.0.0.1:9222")
        pg = b.contexts[0].new_page()
        try:
            pg.goto(LIST, wait_until="networkidle", timeout=90_000)
            pg.wait_for_timeout(2500)
            if "loginPage" in pg.url:
                raise SystemExit("❌ SWEA 로그인 필요")
            for i, no in enumerate(order, 1):
                title = todo[no]
                try:
                    hit, tab = find(pg, no, title)
                except Exception as e:
                    print("  [%d/%d] %-6s ❌ %s" % (i, len(order), no,
                                                   str(e).split("\n")[0][:60]), flush=True)
                    ng += 1
                    continue
                if hit:
                    ids[no] = hit["id"]
                    ok += 1
                    nm = re.sub(r"\s+", " ", hit["txt"])[:32]
                    print("  [%d/%d] %-6s ✅ %-22s [%s] %s"
                          % (i, len(order), no, hit["id"], tab, nm), flush=True)
                else:
                    ng += 1
                    print("  [%d/%d] %-6s ⚠️ 못 찾음 (%s)"
                          % (i, len(order), no, title[:24]), flush=True)
                if i % 5 == 0:
                    io.open(OUT, "w", encoding="utf-8", newline="").write(
                        json.dumps(ids, ensure_ascii=False, indent=1, sort_keys=True))
        finally:
            try:
                pg.close()
            except Exception:
                pass

    io.open(OUT, "w", encoding="utf-8", newline="").write(
        json.dumps(ids, ensure_ascii=False, indent=1, sort_keys=True))
    print("\n✅ 매핑 %d개 (성공 %d / 실패 %d) → _meta/swea_ids.json" % (len(ids), ok, ng))


if __name__ == "__main__":
    main()
