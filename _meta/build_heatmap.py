"""
코테 잔디 SVG 생성 → assets/heatmap.svg + README 삽입

데이터 우선순위(병합):
  1) _meta/history.json           (누적 — PC가 바뀌어도 유지)
  2) 옵시디언 실수노트             (있을 때만. 전체 이력의 진실 소스)
  3) repo 풀이 파일의 '풀이일'      (boj/*.py, swea/*.py)

사용법:
    python _meta/build_heatmap.py
    python _meta/build_heatmap.py --year 2026
"""
import os, re, io, json, glob, datetime, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIST = os.path.join(ROOT, "_meta", "history.json")
ASSETS = os.path.join(ROOT, "assets")
SVG = os.path.join(ASSETS, "heatmap.svg")
README = os.path.join(ROOT, "README.md")

VAULT_CANDIDATES = [
    r"C:/Users/solom/ObsidianVaults/동기화/_cpp_코테/실수모음 (몰랐으면 답보고 혼자 다시 짜기).md",
]

CELL, GAP, PAD_L, PAD_T = 11, 3, 30, 20
COLORS = ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"]
COLORS_DARK = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


# ── 데이터 수집 ────────────────────────────────────────────────
def load_history() -> dict:
    if os.path.exists(HIST):
        return json.load(io.open(HIST, encoding="utf-8"))
    return {}


def from_vault() -> dict:
    """실수노트에서 날짜별 '시도 문제 수' 집계."""
    path = next((p for p in VAULT_CANDIDATES if os.path.exists(p)), None)
    if not path:
        return {}
    L = io.open(path, encoding="utf-8").read().split("\n")
    heads = [i for i, l in enumerate(L) if l.startswith("## ")]
    DATEL = re.compile(r"^\s*(\d{4}-\d{2}-\d{2})\s*$")
    REC = re.compile(r"^####\s+(\d{4}-\d{2}-\d{2})")
    counts = {}
    for n, s in enumerate(heads):
        e = heads[n + 1] if n + 1 < len(heads) else len(L)
        seen, fence = set(), False
        for x in L[s + 1:e]:
            if x.strip().startswith("```"):
                fence = not fence
                continue
            if fence:
                continue
            m = DATEL.match(x) or REC.match(x)
            if m:
                seen.add(m.group(1))
        for d in seen:                       # 한 문제가 같은 날 여러 번 나와도 1회
            counts[d] = counts.get(d, 0) + 1
    return counts


def from_repo() -> dict:
    counts = {}
    for f in glob.glob(os.path.join(ROOT, "boj", "*.py")) + \
             glob.glob(os.path.join(ROOT, "swea", "*.py")):
        src = io.open(f, encoding="utf-8").read()
        m = re.search(r"풀이일\s*:\s*(\d{4}-\d{2}-\d{2})", src)
        if m:
            counts[m.group(1)] = counts.get(m.group(1), 0) + 1
    return counts


# ── SVG ────────────────────────────────────────────────────────
def level(n: int) -> int:
    return 0 if n <= 0 else 1 if n == 1 else 2 if n == 2 else 3 if n == 3 else 4


def render(counts: dict, year: int) -> str:
    start = datetime.date(year, 1, 1)
    end = datetime.date(year, 12, 31)
    # 그리드 시작 = 그 해 첫 일요일 이전 일요일
    grid0 = start - datetime.timedelta(days=(start.weekday() + 1) % 7)
    weeks = ((end - grid0).days // 7) + 1
    W = PAD_L + weeks * (CELL + GAP) + 10
    H = PAD_T + 7 * (CELL + GAP) + 24

    css = []
    for i in range(5):
        css.append(".l%d{fill:%s}" % (i, COLORS[i]))
    dark = "".join(".l%d{fill:%s}" % (i, COLORS_DARK[i]) for i in range(5))
    style = ("<style>%s .lbl{fill:#57606a;font:9px -apple-system,Segoe UI,sans-serif}"
             "@media(prefers-color-scheme:dark){%s .lbl{fill:#8b949e}}</style>"
             % ("".join(css), dark))

    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
           'viewBox="0 0 %d %d">' % (W, H, W, H), style]

    # 월 라벨
    last_m = -1
    for w in range(weeks):
        d = grid0 + datetime.timedelta(days=w * 7)
        if d.year == year and d.month != last_m and d.day <= 7:
            out.append('<text class="lbl" x="%d" y="%d">%s</text>'
                       % (PAD_L + w * (CELL + GAP), PAD_T - 6, MONTHS[d.month - 1]))
            last_m = d.month
    # 요일 라벨
    for i, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        out.append('<text class="lbl" x="0" y="%d">%s</text>'
                   % (PAD_T + i * (CELL + GAP) + CELL - 1, name))

    total = 0
    for w in range(weeks):
        for dow in range(7):
            d = grid0 + datetime.timedelta(days=w * 7 + dow)
            if d.year != year:
                continue
            key = d.isoformat()
            n = counts.get(key, 0)
            total += n
            out.append('<rect class="l%d" x="%d" y="%d" width="%d" height="%d" rx="2">'
                       '<title>%s — %d문제</title></rect>'
                       % (level(n), PAD_L + w * (CELL + GAP), PAD_T + dow * (CELL + GAP),
                          CELL, CELL, key, n))

    # 범례
    lx = W - 10 - 5 * (CELL + 2) - 60
    ly = H - 12
    out.append('<text class="lbl" x="%d" y="%d">Less</text>' % (lx, ly + 8))
    for i in range(5):
        out.append('<rect class="l%d" x="%d" y="%d" width="%d" height="%d" rx="2"/>'
                   % (i, lx + 28 + i * (CELL + 2), ly, CELL, CELL))
    out.append('<text class="lbl" x="%d" y="%d">More</text>'
               % (lx + 28 + 5 * (CELL + 2) + 3, ly + 8))
    out.append("</svg>")
    return "\n".join(out), total


# ── main ───────────────────────────────────────────────────────
def main():
    year = 2026
    if "--year" in sys.argv:
        year = int(sys.argv[sys.argv.index("--year") + 1])

    counts = load_history()
    v, r = from_vault(), from_repo()
    for src in (v, r):
        for k, n in src.items():
            counts[k] = max(counts.get(k, 0), n)     # 병합: 큰 값 유지

    os.makedirs(os.path.dirname(HIST), exist_ok=True)
    io.open(HIST, "w", encoding="utf-8", newline="").write(
        json.dumps(dict(sorted(counts.items())), ensure_ascii=False, indent=1))

    os.makedirs(ASSETS, exist_ok=True)
    svg, total = render(counts, year)
    io.open(SVG, "w", encoding="utf-8", newline="").write(svg)

    ydays = [k for k in counts if k.startswith(str(year))]
    active = len([k for k in ydays if counts[k] > 0])

    # 연속 일수
    streak = best = 0
    d = datetime.date(year, 1, 1)
    while d <= datetime.date(year, 12, 31):
        if counts.get(d.isoformat(), 0) > 0:
            streak += 1
            best = max(best, streak)
        else:
            streak = 0
        d += datetime.timedelta(days=1)

    block = ("![코테 잔디](./assets/heatmap.svg)\n\n"
             "| %d년 | |\n|---|---|\n| 총 시도 | **%d문제** |\n"
             "| 활동일 | **%d일** |\n| 최장 연속 | **%d일** |"
             % (year, total, active, best))

    t = io.open(README, encoding="utf-8").read()
    if "<!-- HEATMAP_START -->" in t:
        t = re.sub(r"<!-- HEATMAP_START -->.*?<!-- HEATMAP_END -->",
                   "<!-- HEATMAP_START -->\n%s\n<!-- HEATMAP_END -->" % block, t, flags=re.S)
    else:
        t = t.replace("## 📊 현황",
                      "## 🌱 코테 잔디\n\n<!-- HEATMAP_START -->\n%s\n<!-- HEATMAP_END -->\n\n---\n\n## 📊 현황"
                      % block)
    io.open(README, "w", encoding="utf-8", newline="").write(t)

    print("✅ heatmap.svg 생성")
    print("   %d년 총 %d문제 / 활동 %d일 / 최장연속 %d일" % (year, total, active, best))
    print("   실수노트 %d일치, repo %d일치 병합 → history.json %d일" % (len(v), len(r), len(counts)))


if __name__ == "__main__":
    main()
