"""
코테 잔디 생성 → assets/heatmap.svg + assets/heatmap.html + README + HEATMAP.md

데이터 우선순위(병합):
  1) _meta/history.json           (누적 — PC가 바뀌어도 유지)
  2) 옵시디언 실수노트             (있을 때만. 전체 이력의 진실 소스)
  3) repo 풀이 파일의 '풀이일'      (boj/*.py, swea/*.py)

history.json 형식:
  {"2026-08-11": {"count": 2, "items": ["SWEA 2382 미생물 격리 (품)", ...]}}
  (구버전 int 값도 읽음)

사용법:
    python _meta/build_heatmap.py
    python _meta/build_heatmap.py --year 2026
"""
import os, re, io, json, glob, datetime, sys, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIST = os.path.join(ROOT, "_meta", "history.json")
ASSETS = os.path.join(ROOT, "assets")
SVG = os.path.join(ASSETS, "heatmap.svg")
HTML = os.path.join(ASSETS, "heatmap.html")
README = os.path.join(ROOT, "README.md")
FULL = os.path.join(ROOT, "HEATMAP.md")

VAULT_CANDIDATES = [
    r"C:/Users/solom/ObsidianVaults/동기화/_cpp_코테/실수모음 (몰랐으면 답보고 혼자 다시 짜기).md",
]

CELL, GAP, PAD_L, PAD_T = 11, 3, 30, 20
COLORS = ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"]
COLORS_DARK = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DOW = ["월", "화", "수", "목", "금", "토", "일"]


# ── 데이터 ─────────────────────────────────────────────────────
def load_history() -> dict:
    if not os.path.exists(HIST):
        return {}
    raw = json.load(io.open(HIST, encoding="utf-8"))
    out = {}
    for k, v in raw.items():
        if isinstance(v, int):                      # 구버전 호환
            out[k] = {"count": v, "items": []}
        else:
            out[k] = {"count": v.get("count", 0), "items": v.get("items", [])}
    return out


def from_vault() -> dict:
    """실수노트 → 날짜별 {count, items}."""
    path = next((p for p in VAULT_CANDIDATES if os.path.exists(p)), None)
    if not path:
        return {}
    L = io.open(path, encoding="utf-8").read().split("\n")
    heads = [i for i, l in enumerate(L) if l.startswith("## ")]
    DATEL = re.compile(r"^\s*(\d{4}-\d{2}-\d{2})\s*$")
    REC = re.compile(r"^####\s+(\d{4}-\d{2}-\d{2})\s*(?:\(([^)]*)\))?")
    STAT = re.compile(r"(못품|시간초과|틀림|맞음|품)")
    out = {}
    for n, s in enumerate(heads):
        e = heads[n + 1] if n + 1 < len(heads) else len(L)
        head = L[s][3:].strip()
        title = re.split(r"\s*\(", head)[0].strip()
        if not title or title.startswith(("추가", "왜 ", "네 말", "예시")):
            continue
        site = "SWEA" if "expert" in head.lower() else "BOJ"
        hm = re.search(r"\(([^)]*)\)\s*$", head)
        head_stat = (STAT.search(hm.group(1)).group(1)
                     if hm and STAT.search(hm.group(1)) else "")

        seen, fence = {}, False
        for x in L[s + 1:e]:
            if x.strip().startswith("```"):
                fence = not fence
                continue
            if fence:
                continue
            m = REC.match(x)
            if m:
                st = STAT.search(m.group(2) or "")
                seen[m.group(1)] = st.group(1) if st else head_stat
                continue
            m = DATEL.match(x)
            if m and m.group(1) not in seen:
                seen[m.group(1)] = head_stat
        for d, st in seen.items():
            rec = out.setdefault(d, {"count": 0, "items": []})
            rec["count"] += 1
            rec["items"].append("%s %s%s" % (site, title, " (%s)" % st if st else ""))
    return out


def from_repo() -> dict:
    out = {}
    for f in glob.glob(os.path.join(ROOT, "boj", "*.py")) + \
             glob.glob(os.path.join(ROOT, "swea", "*.py")):
        src = io.open(f, encoding="utf-8").read()
        m = re.search(r"풀이일\s*:\s*(\d{4}-\d{2}-\d{2})", src)
        if not m:
            continue
        d = m.group(1)
        t = re.search(r"^\s*(BOJ|SWEA)\s+(\d+)\s+(.*)$", src, re.M)
        label = ("%s %s %s" % (t.group(1), t.group(2), t.group(3).strip())
                 if t else os.path.basename(f))
        rec = out.setdefault(d, {"count": 0, "items": []})
        rec["count"] += 1
        rec["items"].append(label)
    return out


def merge(base: dict, add: dict) -> dict:
    for k, v in add.items():
        cur = base.setdefault(k, {"count": 0, "items": []})
        if v["count"] >= cur["count"]:
            cur["count"] = v["count"]
            if v["items"]:
                cur["items"] = v["items"]
    return base


# ── 렌더 ───────────────────────────────────────────────────────
def level(n):
    return 0 if n <= 0 else 1 if n == 1 else 2 if n == 2 else 3 if n == 3 else 4


def grid(year):
    start, end = datetime.date(year, 1, 1), datetime.date(year, 12, 31)
    g0 = start - datetime.timedelta(days=(start.weekday() + 1) % 7)
    return g0, ((end - g0).days // 7) + 1


def tip(d: datetime.date, rec: dict) -> str:
    head = "%s (%s) — %d문제" % (d.isoformat(), DOW[d.weekday()], rec["count"])
    if not rec["items"]:
        return head
    return head + "\n" + "\n".join("· " + x for x in rec["items"])


def render_svg(data, year):
    g0, weeks = grid(year)
    W = PAD_L + weeks * (CELL + GAP) + 10
    H = PAD_T + 7 * (CELL + GAP) + 24
    light = "".join(".l%d{fill:%s}" % (i, COLORS[i]) for i in range(5))
    dark = "".join(".l%d{fill:%s}" % (i, COLORS_DARK[i]) for i in range(5))
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'
           % (W, H, W, H),
           "<style>%s .lbl{fill:#57606a;font:9px -apple-system,Segoe UI,sans-serif}"
           "@media(prefers-color-scheme:dark){%s .lbl{fill:#8b949e}}</style>" % (light, dark)]
    last_m = -1
    for w in range(weeks):
        d = g0 + datetime.timedelta(days=w * 7)
        if d.year == year and d.month != last_m and d.day <= 7:
            out.append('<text class="lbl" x="%d" y="%d">%s</text>'
                       % (PAD_L + w * (CELL + GAP), PAD_T - 6, MONTHS[d.month - 1]))
            last_m = d.month
    for i, nm in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        out.append('<text class="lbl" x="0" y="%d">%s</text>'
                   % (PAD_T + i * (CELL + GAP) + CELL - 1, nm))
    total = 0
    for w in range(weeks):
        for dow in range(7):
            d = g0 + datetime.timedelta(days=w * 7 + dow)
            if d.year != year:
                continue
            rec = data.get(d.isoformat(), {"count": 0, "items": []})
            total += rec["count"]
            out.append('<rect class="l%d" x="%d" y="%d" width="%d" height="%d" rx="2">'
                       '<title>%s</title></rect>'
                       % (level(rec["count"]), PAD_L + w * (CELL + GAP),
                          PAD_T + dow * (CELL + GAP), CELL, CELL,
                          html.escape(tip(d, rec))))
    lx, ly = W - 10 - 5 * (CELL + 2) - 60, H - 12
    out.append('<text class="lbl" x="%d" y="%d">Less</text>' % (lx, ly + 8))
    for i in range(5):
        out.append('<rect class="l%d" x="%d" y="%d" width="%d" height="%d" rx="2"/>'
                   % (i, lx + 28 + i * (CELL + 2), ly, CELL, CELL))
    out.append('<text class="lbl" x="%d" y="%d">More</text>' % (lx + 28 + 5 * (CELL + 2) + 3, ly + 8))
    out.append("</svg>")
    return "\n".join(out), total


def render_html(data, year, total, active, best):
    """진짜 인터랙티브 버전 — 브라우저로 직접 열면 hover 동작."""
    g0, weeks = grid(year)
    cells = []
    for w in range(weeks):
        for dow in range(7):
            d = g0 + datetime.timedelta(days=w * 7 + dow)
            if d.year != year:
                continue
            rec = data.get(d.isoformat(), {"count": 0, "items": []})
            items = "".join("<li>%s</li>" % html.escape(x) for x in rec["items"])
            cells.append(
                '<div class="c l%d" style="grid-column:%d;grid-row:%d" '
                'data-d="%s (%s)" data-n="%d" data-i=\'%s\'></div>'
                % (level(rec["count"]), w + 1, dow + 1, d.isoformat(),
                   DOW[d.weekday()], rec["count"], html.escape(items or "<li>—</li>", quote=True)))
    return """<!doctype html><html lang="ko"><meta charset="utf-8">
<title>코테 잔디 %d</title>
<style>
 :root{--bg:#fff;--fg:#1f2328;--sub:#57606a;--c0:#ebedf0;--c1:#9be9a8;--c2:#40c463;--c3:#30a14e;--c4:#216e39}
 @media(prefers-color-scheme:dark){:root{--bg:#0d1117;--fg:#e6edf3;--sub:#8b949e;--c0:#161b22;--c1:#0e4429;--c2:#006d32;--c3:#26a641;--c4:#39d353}}
 body{background:var(--bg);color:var(--fg);font:14px -apple-system,Segoe UI,sans-serif;padding:28px;margin:0}
 h1{font-size:18px;margin:0 0 4px} .sub{color:var(--sub);font-size:12px;margin-bottom:18px}
 .grid{display:grid;grid-auto-flow:column;grid-template-rows:repeat(7,13px);gap:3px;overflow-x:auto;padding-bottom:8px}
 .c{width:13px;height:13px;border-radius:3px;cursor:pointer}
 .l0{background:var(--c0)}.l1{background:var(--c1)}.l2{background:var(--c2)}.l3{background:var(--c3)}.l4{background:var(--c4)}
 .c:hover{outline:2px solid var(--fg);outline-offset:1px}
 #tip{position:fixed;display:none;background:#1f2328;color:#fff;padding:8px 11px;border-radius:6px;
      font-size:12px;line-height:1.55;pointer-events:none;z-index:99;box-shadow:0 4px 14px rgba(0,0,0,.35);max-width:340px}
 #tip b{display:block;margin-bottom:4px}#tip ul{margin:0;padding-left:16px}
 .stat{margin-top:18px;color:var(--sub);font-size:12px}
</style>
<h1>🌱 코테 잔디 %d</h1>
<div class="sub">셀에 마우스를 올리면 그날 푼 문제가 보입니다</div>
<div class="grid">%s</div>
<div class="stat">총 <b>%d문제</b> · 활동 <b>%d일</b> · 최장 연속 <b>%d일</b></div>
<div id="tip"></div>
<script>
const tip=document.getElementById('tip');
document.querySelectorAll('.c').forEach(c=>{
  c.addEventListener('mousemove',e=>{
    tip.innerHTML='<b>'+c.dataset.d+' — '+c.dataset.n+'문제</b><ul>'+c.dataset.i+'</ul>';
    tip.style.display='block';
    const x=Math.min(e.clientX+14,innerWidth-360);
    tip.style.left=x+'px'; tip.style.top=(e.clientY+16)+'px';
  });
  c.addEventListener('mouseleave',()=>tip.style.display='none');
});
</script></html>""" % (year, year, "".join(cells), total, active, best)


def month_details(data, year, months=None):
    """월별 <details> 목록 (GitHub 마크다운에서 동작)."""
    by_month = {}
    for k in sorted(data):
        if not k.startswith(str(year)):
            continue
        if data[k]["count"] <= 0:
            continue
        by_month.setdefault(k[:7], []).append(k)
    keys = sorted(by_month, reverse=True)
    if months:
        keys = keys[:months]
    out = []
    for mk in keys:
        days = by_month[mk]
        cnt = sum(data[d]["count"] for d in days)
        rows = ["| 날짜 | 문제 |", "|---|---|"]
        for d in sorted(days, reverse=True):
            dt = datetime.date(*map(int, d.split("-")))
            items = data[d]["items"] or ["(기록 없음)"]
            rows.append("| **%s** (%s) | %s |"
                        % (d[5:], DOW[dt.weekday()], "<br>".join(items)))
        out.append("<details>\n<summary><b>%s</b> — %d일 / %d문제</summary>\n\n%s\n\n</details>"
                   % (mk, len(days), cnt, "\n".join(rows)))
    return "\n\n".join(out) if out else "_아직 없음_"


# ── main ───────────────────────────────────────────────────────
def main():
    year = 2026
    if "--year" in sys.argv:
        year = int(sys.argv[sys.argv.index("--year") + 1])

    data = load_history()
    merge(data, from_vault())
    merge(data, from_repo())

    io.open(HIST, "w", encoding="utf-8", newline="").write(
        json.dumps({k: data[k] for k in sorted(data)}, ensure_ascii=False, indent=1))

    os.makedirs(ASSETS, exist_ok=True)
    svg, total = render_svg(data, year)
    io.open(SVG, "w", encoding="utf-8", newline="").write(svg)

    ydays = [k for k in data if k.startswith(str(year)) and data[k]["count"] > 0]
    active = len(ydays)
    streak = best = 0
    d = datetime.date(year, 1, 1)
    while d <= datetime.date(year, 12, 31):
        if data.get(d.isoformat(), {"count": 0})["count"] > 0:
            streak += 1
            best = max(best, streak)
        else:
            streak = 0
        d += datetime.timedelta(days=1)

    io.open(HTML, "w", encoding="utf-8", newline="").write(
        render_html(data, year, total, active, best))

    io.open(FULL, "w", encoding="utf-8", newline="").write(
        "# 🌱 코테 잔디 — 전체 기록 (%d)\n\n"
        "![](./assets/heatmap.svg)\n\n"
        "> 총 **%d문제** · 활동 **%d일** · 최장 연속 **%d일**\n"
        "> 🖱️ 마우스 hover로 보려면 **`assets/heatmap.html`** 을 브라우저로 열 것\n\n---\n\n%s\n"
        % (year, total, active, best, month_details(data, year)))

    block = ("![코테 잔디](./assets/heatmap.svg)\n\n"
             "| %d년 | |\n|---|---|\n| 총 시도 | **%d문제** |\n"
             "| 활동일 | **%d일** |\n| 최장 연속 | **%d일** |\n\n"
             "> 🖱️ **날짜별 문제를 보려면** → 아래 월별 목록을 펼치거나, "
             "[전체 기록](./HEATMAP.md) · 마우스 hover는 [`assets/heatmap.html`](./assets/heatmap.html) 을 브라우저로\n\n"
             "%s" % (year, total, active, best, month_details(data, year, months=2)))

    t = io.open(README, encoding="utf-8").read()
    if "<!-- HEATMAP_START -->" in t:
        t = re.sub(r"<!-- HEATMAP_START -->.*?<!-- HEATMAP_END -->",
                   "<!-- HEATMAP_START -->\n%s\n<!-- HEATMAP_END -->" % block, t, flags=re.S)
    io.open(README, "w", encoding="utf-8", newline="").write(t)

    print("✅ 잔디 생성 (%d년)" % year)
    print("   총 %d문제 / 활동 %d일 / 최장연속 %d일" % (total, active, best))
    print("   history.json %d일  |  SVG + HTML + HEATMAP.md" % len(data))
    with_items = sum(1 for k in data if data[k]["items"])
    print("   문제명 보유: %d일 / %d일" % (with_items, len(data)))


if __name__ == "__main__":
    main()
