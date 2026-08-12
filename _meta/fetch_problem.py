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


# ── 지문 이미지 ────────────────────────────────────────────────
# 지문 중간의 그림(격자·다이어그램)이 빠지면 문제를 못 읽는 경우가 많다.
# 본문 컨테이너를 DOM 으로 훑어 텍스트에 [[IMG:n]] 자리표시를 심고,
# 이미지 바이트는 로그인 세션으로 받아 problems/<site>/img/ 에 저장한다.
# 사이트별 본문 컨테이너 후보(앞에서부터 시도). SWEA 의 .problem_box 는
# 껍데기(45자)뿐이고 실제 지문·그림은 .box4 안에 있다.
STMT_ROOT = {
    "BOJ": [".salgu-description"],                  # 코딩살구
    "SWEA": [".box4", ".problem_box", ".tabcon"],   # SW Expert Academy
}

WALK_JS = r"""(sel) => {
  const root = document.querySelector(sel);
  if (!root) return JSON.stringify({text: "", imgs: []});
  const imgs = [];
  const BLOCK = /^(P|DIV|BR|TR|LI|H[1-6]|TABLE|FIGURE|SECTION|UL|OL|PRE)$/;
  const walk = (n) => {
    if (n.nodeType === 3) return n.nodeValue || "";
    if (n.nodeType !== 1) return "";
    const tag = n.tagName;
    if (tag === "SCRIPT" || tag === "STYLE" || tag === "NOSCRIPT") return "";
    if (tag === "IMG") {
      const w = n.naturalWidth || 0, h = n.naturalHeight || 0;
      if (w < 60 || h < 40) return "";
      const src = n.getAttribute("src") || "";
      if (/profileImage|avatar|icon|logo/i.test(src)) return "";
      imgs.push({src: src, w: w, h: h});
      return "\n[[IMG:" + imgs.length + "]]\n";
    }
    let s = "";
    for (const c of n.childNodes) s += walk(c);
    if (BLOCK.test(tag)) s += "\n";
    return s;
  };
  return JSON.stringify({text: walk(root), imgs: imgs});
}"""

# 이미지 바이트를 세션 쿠키로 받아 base64 로 넘긴다(자산 다운로드도 인증이 필요).
GRAB_JS = r"""async (srcs) => {
  const out = [];
  for (const s of srcs) {
    try {
      if (s.startsWith("data:")) { out.push(s); continue; }
      const r = await fetch(s, {credentials: "include"});
      if (!r.ok) { out.push(""); continue; }
      const b = await r.blob();
      const d = await new Promise(res => {
        const f = new FileReader(); f.onload = () => res(f.result); f.readAsDataURL(b);
      });
      out.push(d);
    } catch (e) { out.push(""); }
  }
  return JSON.stringify(out);
}"""

EXT = {"image/png": "png", "image/jpeg": "jpg", "image/gif": "gif",
       "image/webp": "webp", "image/svg+xml": "svg"}


def collect_images(pg, site, no):
    """본문을 [[IMG:n]] 마커가 박힌 텍스트로 만들고 이미지 파일을 저장.

    반환 (text, [상대경로...]). 컨테이너를 못 찾으면 ("", []).
    """
    got, imgs, text = None, [], ""
    for sel in STMT_ROOT.get(site) or []:
        try:
            g = json.loads(pg.evaluate(WALK_JS, sel))
        except Exception:
            continue
        if g.get("imgs"):                      # 그림이 잡히는 컨테이너를 채택
            got, imgs = g, g["imgs"]
            text = clean(re.sub(r"[ \t]+\n", "\n", g.get("text") or ""))
            break
        if got is None and (g.get("text") or "").strip():
            got = g
            text = clean(re.sub(r"[ \t]+\n", "\n", g.get("text") or ""))
    if not imgs:
        return text, []
    try:
        datas = json.loads(pg.evaluate(GRAB_JS, [i["src"] for i in imgs]))
    except Exception:
        return text, []

    sub = {"BOJ": "boj", "SWEA": "swea", "PGS": "programmers", "CT": "codetree"}.get(site, "boj")
    outdir = os.path.join(PROB, sub, "img")
    os.makedirs(outdir, exist_ok=True)
    paths = []
    import base64
    for i, d in enumerate(datas, 1):
        if not d or not d.startswith("data:"):
            paths.append("")
            continue
        head, _, b64 = d.partition(",")
        mime = head[5:].split(";")[0]
        ext = EXT.get(mime, "png")
        rel = "problems/%s/img/%s_%d.%s" % (sub, no, i, ext)
        try:
            with open(os.path.join(ROOT, rel), "wb") as f:
                f.write(base64.b64decode(b64))
            paths.append(rel)
        except Exception:
            paths.append("")
    return text, paths


def apply_images(pg, d):
    """수집한 이미지·마커 지문을 문제 dict 에 반영(그림이 없으면 아무것도 안 함)."""
    if not d.get("no"):
        return
    txt, paths = collect_images(pg, d.get("site", ""), str(d["no"]))
    if not any(paths):
        return
    d["images"] = paths
    # 마커가 박힌 본문에서 지문 구간만 다시 잘라 쓴다(입력/출력 설명은 기존 값 유지).
    body = sect(txt, "", "[제약사항]", "[입력]", "\n입력\n") or txt
    if body and "[[IMG:" in body:
        d["statement"] = clean(body)


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
    # 지문 시작 앵커: 저작권 고지가 있는 페이지도 없는 페이지도 있다.
    # 없으면 "메모리 : …" 줄 다음부터를 본문으로 본다.
    st = clean(sect(t, "무단 복제하는 것을 금지합니다.", "[제약사항]", "[입력]"))
    if not st:
        mm = re.search(r"메모리\s*:\s*[^\n]*\n", t)
        if mm:
            st = clean(sect(t[mm.end():], "", "[제약사항]", "[입력]"))
    d["statement"] = st
    d["input_spec"] = clean(sect(t, "[입력]", "[출력]"))
    d["output_spec"] = clean(sect(t, "[출력]", "입력\n", "sample_input"))
    # 페이지에 보이는 예제는 "…" 로 잘린 미리보기이고, 뒤에 주석·다운로드 버튼·
    # 댓글까지 딸려온다. 실제 테스트케이스는 contestProbDown.do 로 받는다.
    d["samples"] = []
    if "sample_input.txt" in t:
        d["testcase_file"] = "sample_input.txt / sample_output.txt (다운로드로 수집)"
    return d


def swea_time_limit(text):
    """SWEA 한도 문장에서 Python 기준 초를 뽑는다.

    예) "50개 테스트케이스를 합쳐서 C의 경우 5초 / ... / Python의 경우 10초" -> 10.0
    """
    if not text:
        return None
    m = re.search(r"[Pp]ython[^\d]{0,10}([\d.]+)\s*초", text)
    if not m:
        m = re.search(r"([\d.]+)\s*초", text)
    return float(m.group(1)) if m else None


def fetch_swea_tc(pg, cid):
    """SWEA 공식 sample_input/output 을 로그인 세션으로 내려받아 케이스로 변환.

    SWEA 는 한 파일에 여러 테스트케이스를 담고 출력은 "#k 답" 형식이라,
    파일 전체를 입력 1건 / 출력 1건으로 다루는 것이 실제 채점과 동일하다.
    """
    js = ("async (id) => {"
          " const base='/main/common/contestProb/contestProbDown.do?downType=';"
          " const q='&contestProbId='+id+'&_menuId=AVtnUz06AA3w6KZN&_menuF=true';"
          " const out={};"
          " for (const k of ['in','out']) {"
          "   try { const r = await fetch(base+k+q, {credentials:'include'});"
          "         out[k] = r.ok ? await r.text() : ''; }"
          "   catch(e) { out[k]=''; } }"
          " return JSON.stringify(out); }")
    try:
        raw = json.loads(pg.evaluate(js, cid))
    except Exception:
        return []
    si = (raw.get("in") or "").replace("\r\n", "\n").rstrip()
    so = (raw.get("out") or "").replace("\r\n", "\n").rstrip()
    return [{"in": si, "out": so}] if (si and so) else []


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
        apply_images(pg, d)
        # SWEA 는 공식 테스트케이스 파일을 받아 채점 가능한 형태로 만든다.
        if d.get("site") == "SWEA":
            m = re.search(r"contestProbId=([A-Za-z0-9+/=]+)", pg.url)
            if m:
                d["samples"] = fetch_swea_tc(pg, m.group(1)) or d.get("samples") or []
            tl = swea_time_limit((d.get("limits") or {}).get("time"))
            if tl:
                d.setdefault("limits", {})["time_sec"] = tl
    finally:
        if pw:
            pw.stop()

    d["fetched_at"] = datetime.date.today().isoformat()
    d = {k: v for k, v in d.items() if v not in ("", [], {}, None)}

    # --print 는 출력만, --save 를 같이 주면 저장도 한다(대시보드의 "새 문제 추가" 경로).
    if "--print" in sys.argv and "--save" not in sys.argv:
        print(json.dumps(d, ensure_ascii=False, indent=2))
        return d

    sub = {"BOJ": "boj", "SWEA": "swea", "PGS": "programmers", "CT": "codetree"}[d["site"]]
    os.makedirs(os.path.join(PROB, sub), exist_ok=True)
    key = d.get("no") or re.sub(r"[^\w가-힣]+", "_", d.get("title", "unknown"))[:40]
    path = os.path.join(PROB, sub, "%s.json" % key)
    io.open(path, "w", encoding="utf-8", newline="").write(
        json.dumps(d, ensure_ascii=False, indent=1))

    # SWEA 는 표시번호로 역검색이 안 되므로 번호→contestProbId 매핑을 남겨둔다.
    if d["site"] == "SWEA" and d.get("no"):
        m = re.search(r"contestProbId=([A-Za-z0-9+/=]+)", d.get("url", ""))
        if m:
            ip = os.path.join(ROOT, "_meta", "swea_ids.json")
            ids = {}
            if os.path.exists(ip):
                try:
                    ids = json.load(io.open(ip, encoding="utf-8"))
                except Exception:
                    ids = {}
            if ids.get(d["no"]) != m.group(1):
                ids[d["no"]] = m.group(1)
                io.open(ip, "w", encoding="utf-8", newline="").write(
                    json.dumps(ids, ensure_ascii=False, indent=1, sort_keys=True))

    if "--print" in sys.argv:
        print(json.dumps(d, ensure_ascii=False, indent=2))
        return d

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
