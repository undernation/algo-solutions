"""
통합 문제 크롤러 — URL(또는 BOJ 번호) 하나로 4개 사이트에서 문제 정보 추출.

사용법:
    python _meta/fetch_problem.py 2618                     # BOJ 번호 → 코딩살구
    python _meta/fetch_problem.py https://cosal.aviss.kr/problems/detail/2618
    python _meta/fetch_problem.py "https://swexpertacademy.com/...contestProbId=AWIe..."
    python _meta/fetch_problem.py https://school.programmers.co.kr/learn/courses/30/lessons/12345
    python _meta/fetch_problem.py https://www.codetree.ai/...      # 코드트리
    python _meta/fetch_problem.py 2618 --print                     # 저장 없이 출력만

결과: problems/<site>/<no>.json

선행조건: 디버그 크롬(9222) + 각 사이트 로그인
    python C:/Users/solom/crawler.py chrome
"""
import os, re, io, sys, json, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROB = os.path.join(ROOT, "problems")

COSAL = "https://cosal.aviss.kr/problems/detail/%s"
SWEA = "https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=%s"


# ── 공통 유틸 ──────────────────────────────────────────────────
def sect(text, start, *ends):
    """start 이후 ~ ends 중 가장 먼저 나오는 것 전까지."""
    i = text.find(start)
    if i < 0:
        return ""
    i += len(start)
    j = len(text)
    for e in ends:
        k = text.find(e, i)
        if 0 <= k < j:
            j = k
    return text[i:j].strip()


def clean(s):
    return re.sub(r"\n{3,}", "\n\n", s or "").strip()


def parse_samples(tc):
    """'예제 입력 1 … 예제 출력 1 … 예제 입력 2 …' 블록을 쌍으로 분리.

    예제가 1개면 번호가 없고("예제 입력"), 2개 이상이면 번호가 붙는다("예제 입력 1").
    번호를 데이터로 잘못 삼키거나 다음 예제를 뒤에 이어붙이지 않도록 헤딩 기준으로 자른다.
    """
    if not tc:
        return []
    heads = list(re.finditer(r"(?m)^[ \t]*예제[ \t]*(입력|출력)[ \t]*(\d*)[ \t]*$", tc))
    if not heads:
        return []
    blocks = []
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(tc)
        blocks.append((h.group(1), h.group(2) or "1", tc[h.end():end].strip("\n").rstrip()))
    ins, outs = {}, {}
    for kind, idx, body in blocks:
        (ins if kind == "입력" else outs)[idx] = body
    out = []
    for idx in sorted(ins, key=lambda x: int(x) if x.isdigit() else 0):
        if ins[idx].strip():
            out.append({"in": ins[idx], "out": outs.get(idx, "")})
    return out


def open_page(url, wait=2600):
    from playwright.sync_api import sync_playwright
    pw = sync_playwright().start()
    b = pw.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = b.contexts[0]
    pg = ctx.pages[0] if ctx.pages else ctx.new_page()
    pg.goto(url, wait_until="networkidle", timeout=90_000)
    pg.wait_for_timeout(wait)
    return pw, pg


# ── 코딩살구 (BOJ) ─────────────────────────────────────────────
def parse_cosal(t, url):
    d = {"site": "BOJ", "platform": "코딩살구", "url": url}

    m = re.search(r"^(.+?)\n+\s*([\d\-\sA-Z]*·\s*BOJ\s*(\d+).*)$", t, re.M)
    meta_line, title = "", ""
    mm = re.search(r"(?:^|\n)([^\n]*BOJ\s*(\d+)[^\n]*)", t)
    if mm:
        meta_line, d["no"] = mm.group(1).strip(), mm.group(2)
        before = t[:mm.start()].rstrip().split("\n")
        title = next((x.strip() for x in reversed(before)
                      if x.strip() and x.strip() not in ("로그아웃", "코딩테스트")), "")
    d["title"] = title
    d["source_url"] = "https://www.acmicpc.net/problem/%s" % d.get("no", "")

    lim = {}
    mt = re.search(r"시간\s*([\d.]+\s*\S+)", meta_line)
    mem = re.search(r"메모리\s*([\d.]+\s*\S+)", meta_line)
    if mt:
        lim["time"] = mt.group(1)
    if mem:
        lim["memory"] = mem.group(1)
    d["limits"] = lim
    mw = re.match(r"\s*([\d]+\s*-\s*[A-Z])", meta_line)
    if mw:
        d["label"] = mw.group(1).replace(" ", "")

    # 본문 시작 앵커는 "…목록" 링크 줄이다. 주차 문제는 "주차 목록",
    # 개념별 전용 문제는 "문자열 · 누적합 · 구현 목록" 처럼 트랙명이 들어간다.
    ml = re.search(r"\n([^\n]{0,40}목록)\n", t)
    anchor = ml.group(1) if ml else "주차 목록"
    d["solved"] = "해결" in sect(t, meta_line, anchor)[:40]
    body = sect(t, anchor, "테스트 케이스", "코드 제출")
    d["statement"] = clean(sect(body, "", "입력") or body)
    d["input_spec"] = clean(sect(body, "\n입력\n", "\n출력\n"))
    d["output_spec"] = clean(sect(body, "\n출력\n", "테스트 케이스"))

    tc = sect(t, "테스트 케이스", "프라이빗 테스트케이스", "코드 제출")
    d["samples"] = parse_samples(tc)

    mp = re.search(r"프라이빗 테스트케이스\s*\n?\s*(\d+)\s*개", t)
    if mp:
        d["private_tc_count"] = int(mp.group(1))
    return d


# ── SWEA ──────────────────────────────────────────────────────
def parse_swea(t, url):
    d = {"site": "SWEA", "platform": "SW Expert Academy", "url": url}
    m = re.search(r"^\s*(\d{3,5})\.\s*(.+?)\s*$", t, re.M)
    if m:
        d["no"], d["title"] = m.group(1), m.group(2).strip()
    m = re.search(r"\n(D\d|Master|Expert|Professional|Senior|Junior|Novice)\s*\n", t)
    if m:
        d["level"] = m.group(1)
    stat = {}
    for k, pat in (("participants", r"([\d,]+)\s*\n\s*참여자"),
                   ("submissions", r"([\d,]+)\s*\n\s*제출"),
                   ("accepted", r"([\d,]+)\s*\n\s*정답\s*\n"),
                   ("accept_rate", r"([\d.]+)\s*\n\s*정답률"),
                   ("point", r"([\d,]+)\s*\n\s*Point")):
        mm = re.search(pat, t)
        if mm:
            stat[k] = mm.group(1)
    d["stats"] = stat
    lim = {}
    mm = re.search(r"시간\s*:\s*(.+)", t)
    if mm:
        lim["time"] = mm.group(1).strip()
    mm = re.search(r"메모리\s*:\s*(.+)", t)
    if mm:
        lim["memory"] = mm.group(1).strip()
    d["limits"] = lim
    mm = re.search(r"\[제약사항\](.*?)(?:\[입력\]|\Z)", t, re.S)
    if mm:
        d["constraints"] = [x.strip() for x in mm.group(1).split("\n") if x.strip()]
    d["statement"] = clean(sect(t, "무단 복제하는 것을 금지합니다.", "[제약사항]", "[입력]"))
    d["input_spec"] = clean(sect(t, "[입력]", "[출력]"))
    d["output_spec"] = clean(sect(t, "[출력]", "입력\n", "sample_input"))
    si = clean(sect(t, "\n입력\n", "\n출력\n", "sample_input"))
    so = clean(sect(t, "\n출력\n", "sample_input", "\n목록\n"))
    d["samples"] = [{"in": si, "out": so}] if si else []
    if "sample_input.txt" in t:
        d["testcase_file"] = "sample_input.txt (사이트에서 다운로드)"
    return d


# ── 프로그래머스 ───────────────────────────────────────────────
def parse_pgs(t, url):
    d = {"site": "PGS", "platform": "프로그래머스", "url": url}
    m = re.search(r"/lessons/(\d+)", url)
    if m:
        d["no"] = m.group(1)
    m = re.search(r"코딩테스트 연습\s*\n\s*(.+?)\s*\n", t)
    d["title"] = m.group(1).strip() if m else ""
    if not d["title"]:
        for line in t.split("\n"):
            s = line.strip()
            if s and s not in ("문제 설명", "제한사항") and len(s) < 60:
                d["title"] = s
                break
    d["statement"] = clean(sect(t, "문제 설명", "제한 사항", "제한사항", "입출력 예"))
    d["constraints"] = [x.strip() for x in
                        clean(sect(t, "제한사항", "입출력 예") or
                              sect(t, "제한 사항", "입출력 예")).split("\n") if x.strip()]
    d["samples_raw"] = clean(sect(t, "입출력 예", "※", "다른 사람의 풀이"))
    d["samples"] = []
    return d


# ── 코드트리 ──────────────────────────────────────────────────
def parse_codetree(t, url):
    d = {"site": "CT", "platform": "코드트리", "url": url}
    lines = [x.strip() for x in t.split("\n") if x.strip()]
    d["title"] = next((x for x in lines[:25] if 2 < len(x) < 50
                       and x not in ("코드트리", "문제", "제출", "채점")), "")
    d["statement"] = clean(sect(t, "문제", "입력 형식", "입력형식"))
    d["input_spec"] = clean(sect(t, "입력 형식", "출력 형식") or sect(t, "입력형식", "출력형식"))
    d["output_spec"] = clean(sect(t, "출력 형식", "예제") or sect(t, "출력형식", "예제"))
    si = clean(sect(t, "예제 입력 1", "예제 출력 1") or sect(t, "예제 입력", "예제 출력"))
    so = clean(sect(t, "예제 출력 1", "해설", "제출") or sect(t, "예제 출력", "해설", "제출"))
    d["samples"] = [{"in": si, "out": so}] if si else []
    return d


# ── 라우팅 ────────────────────────────────────────────────────
def resolve(ref):
    ref = ref.strip()
    if re.fullmatch(r"\d{3,6}", ref):
        return COSAL % ref, parse_cosal
    if ref.startswith("boj:"):
        return COSAL % ref[4:], parse_cosal
    if ref.startswith("swea:"):
        return SWEA % ref[5:], parse_swea
    low = ref.lower()
    if "cosal.aviss.kr" in low:
        return ref, parse_cosal
    if "swexpertacademy" in low:
        return ref, parse_swea
    if "programmers.co.kr" in low:
        return ref, parse_pgs
    if "codetree.ai" in low:
        return ref, parse_codetree
    raise SystemExit("❌ 알 수 없는 소스: %s" % ref[:70])


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(1)
    url, parser = resolve(args[0])

    pw = pg = None
    try:
        pw, pg = open_page(url)
        if any(k in pg.url.lower() for k in ("login", "sign_in", "anonymous")):
            raise SystemExit("❌ 로그인 필요: %s" % pg.url[:80])
        t = pg.evaluate("() => document.body.innerText") or ""
        d = parser(t, pg.url)
    finally:
        if pw:
            pw.stop()

    d["fetched_at"] = datetime.date.today().isoformat()
    d = {k: v for k, v in d.items() if v not in ("", [], {}, None)}

    if "--print" in sys.argv:
        print(json.dumps(d, ensure_ascii=False, indent=2))
        return d

    sub = {"BOJ": "boj", "SWEA": "swea", "PGS": "programmers", "CT": "codetree"}[d["site"]]
    os.makedirs(os.path.join(PROB, sub), exist_ok=True)
    key = d.get("no") or re.sub(r"[^\w가-힣]+", "_", d.get("title", "unknown"))[:40]
    path = os.path.join(PROB, sub, "%s.json" % key)
    io.open(path, "w", encoding="utf-8", newline="").write(
        json.dumps(d, ensure_ascii=False, indent=1))

    print("✅ %s %s  %s" % (d["site"], d.get("no", ""), d.get("title", "")))
    if d.get("limits"):
        print("   한도  :", " / ".join("%s %s" % (k, v) for k, v in d["limits"].items()))
    if d.get("constraints"):
        print("   제약  :", d["constraints"][0][:70])
    print("   지문  : %d자" % len(d.get("statement", "")))
    print("   예제  : %d개" % len(d.get("samples", [])))
    if d.get("private_tc_count"):
        print("   비공개TC:", d["private_tc_count"], "개")
    print("   저장  :", os.path.relpath(path, ROOT).replace(os.sep, "/"))
    return d


if __name__ == "__main__":
    main()
