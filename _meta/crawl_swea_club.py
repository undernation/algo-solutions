"""SWEA Solving Club(B형 기출) 문제 수집.

이 문제들은 일반 problemDetail.do 로는 "접근이 제한된 컨텐츠입니다" 가 뜬다.
클럽 컨텍스트(problemView.do + solveclubId + probBoxId)로만 열린다.

⚠️ 테스트케이스가 매우 크다. 31문제 합계 약 108MB (한 문제 입력이 최대 10MB).
   repo 에 그대로 넣으면 problems/ 가 터지고 Pages 빌드가 실패한다(2026-08-12 전례).
   그래서 BOJ 히든 TC 와 같은 방식으로 나눈다.

     repo  problems/swea/<no>.json        앞부분만 잘라낸 보기용 (커밋됨)
     로컬  _meta/tc_store/swea/<no>.json  전체 (gitignore) → sync_tc.py 로 채점서버

사용법:
    python _meta/crawl_swea_club.py            # 없는 것만
    python _meta/crawl_swea_club.py --force    # 전부 다시
    python _meta/crawl_swea_club.py --only 25958,24615
    python _meta/crawl_swea_club.py --no-tc    # 지문만 다시 (TC 는 기존 값 유지)

선행: python _meta/debug_chrome.py 로 띄운 크롬에서 SWEA 로그인
"""
import os, io, re, sys, json, time, datetime, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROB = os.path.join(ROOT, "problems", "swea")
STORE = os.path.join(ROOT, "_meta", "tc_store", "swea")
LIST = os.path.join(ROOT, "_meta", "swea_club.json")

# repo 에 남길 예제 미리보기 길이. 전체본은 tc_store → 채점서버에 있고
# 화면에서는 '어떤 형식인지' 만 보면 되므로 짧게 자른다.
# (200KB 로 두면 31문제에 6.5MB — 볼 일도 없는 데이터가 repo 에 쌓인다)
TC_CAP = 20_000

_spec = importlib.util.spec_from_file_location(
    "fp", os.path.join(ROOT, "_meta", "fetch_problem.py"))
fp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fp)

VIEW = ("https://swexpertacademy.com/main/talk/solvingClub/problemView.do"
        "?solveclubId=%s&contestProbId=%s&probBoxId=%s&type=PROBLEM")

DOWN = ("async (id) => {"
        " const base='/main/common/contestProb/contestProbDown.do?downType=';"
        " const o={};"
        " for (const k of ['in','out']) {"
        "   try { const r = await fetch(base+k+'&contestProbId='+id,"
        "                              {credentials:'include'});"
        "         o[k] = r.ok ? await r.text() : ''; }"
        "   catch(e) { o[k] = ''; } }"
        " return JSON.stringify(o); }")

# 다열 표를 마크다운 표로 바꿔 둔다. innerText 로 그냥 읽으면 셀이 탭으로 뭉개져
# 예제 표("Order / Function / return")가 통째로 읽을 수 없게 된다.
# 1열짜리는 레이아웃용(API 명세 블록)이라 손대지 않는다.
TABLES_JS = r"""() => {
  const NB = String.fromCharCode(160);
  const cell = td => (td.innerText || '')
      .split(NB).join(' ').replace(/\|/g, '/').replace(/\s+/g, ' ').trim();
  let n = 0;
  document.querySelectorAll('table').forEach(t => {
    if (t.querySelector('table')) return;          // 중첩 표는 안쪽부터 잡힌다
    // 그림이 든 표는 건드리지 않는다. innerText 로 셀을 읽으면 <img> 가 통째로
    // 사라져서, 표만 예뻐지고 그림이 없어진다(25003 이 그렇게 3장을 잃었다).
    if (t.querySelector('img')) return;
    const rows = [...t.rows].map(r => [...r.cells].map(cell));
    const cols = Math.max(0, ...rows.map(r => r.length));
    if (cols < 2 || rows.length < 2) return;
    const pad = r => { const c = r.slice();
                       while (c.length < cols) c.push(''); return c; };
    const md = ['| ' + pad(rows[0]).join(' | ') + ' |',
                '|' + pad(rows[0]).map(() => ' --- ').join('|') + '|'];
    rows.slice(1).forEach(r => md.push('| ' + pad(r).join(' | ') + ' |'));
    const pre = document.createElement('pre');
    pre.textContent = '\n' + md.join('\n') + '\n';
    t.replaceWith(pre);
    n++;
  });
  return n;
}"""

# 모든 <img> 가 디코딩될 때까지 기다린다. 안 그러면 naturalWidth 가 0 이라
# "너무 작은 그림" 으로 오인돼 지문에서 그림이 통째로 사라진다(25003 이 그랬다).
WAIT_IMGS_JS = r"""async () => {
  const ims = [...document.images];
  ims.forEach(i => { i.loading = 'eager'; });
  await Promise.all(ims.map(i => {
    if (i.complete && i.naturalWidth) return null;
    return Promise.race([
      i.decode().catch(() => null),
      new Promise(r => setTimeout(r, 4000))
    ]);
  }));
  return ims.filter(i => i.naturalWidth > 60 && i.naturalHeight > 40).length;
}"""

NBSP = u" "
ZWSP = u"​"


def tidy(s):
    """읽기 좋게 다듬는다.

    표 셀에서 딸려온 탭 들여쓰기, 줄 끝 공백, 빈 줄 남발, 줄바꿈 없는 공백을
    정리한다. 마크다운 표 줄(| 로 시작)은 정렬이 깨지므로 양끝만 다듬고 둔다.
    """
    if not s:
        return s
    s = s.replace(NBSP, " ").replace(ZWSP, "")
    out = []
    for ln in s.split("\n"):
        if ln.lstrip().startswith("|"):
            out.append(ln.strip())
            continue
        ln = ln.replace("\t", " ")
        ln = re.sub(r"[ ]{2,}", " ", ln).strip()
        out.append(ln)
    s = "\n".join(out)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def looks_html(t):
    return any(k in t[:1500] for k in
               ("<!--", "<!DOCTYPE", "<html", "link href", "<script"))


def between(t, a, *ends):
    return fp.clean(fp.sect(t, a, *ends))


def langs_of(time_line):
    """한도 문장에 이름이 나오는 언어들. 파이썬이 없으면 그 언어로는 못 낸다."""
    out = []
    for name, pat in (("C++", r"C\+\+"),
                      ("Java", r"Java"),
                      ("Python", r"Python")):
        if re.search(pat, time_line or "", re.I):
            out.append(name)
    return out


def parse(t, url, meta):
    d = {"site": "SWEA", "platform": "SW Expert Academy", "url": url,
         "no": meta["no"], "title": meta["title"], "level": meta["level"],
         "club": meta.get("club", "")}
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
    mm = re.search(r"시간\s*[:：]\s*(.+)", t)
    if mm:
        lim["time"] = tidy(mm.group(1))
    mm = re.search(r"메모리\s*[:：]\s*(.+)", t)
    if mm:
        lim["memory"] = tidy(mm.group(1))
    tl = fp.swea_time_limit(lim.get("time"))
    if tl:
        lim["time_sec"] = tl
    d["limits"] = lim
    d["languages"] = langs_of(lim.get("time", ""))
    # 파이썬이 한도 문장에 없으면 제출 자체가 안 된다 — 화면에 배지로 띄운다.
    d["python_supported"] = "Python" in d["languages"]

    d["statement"] = tidy(between(t, "[문제 설명]", "[예제]", "[제약사항]", "[입출력]"))
    ex = tidy(between(t, "[예제]", "[제약사항]", "[입출력]"))
    if ex:
        d["examples_text"] = ex
    cons = tidy(between(t, "[제약사항]", "[입출력]"))
    if cons:
        d["constraints"] = [x.strip() for x in cons.split("\n") if x.strip()]
    io_spec = tidy(between(t, "[입출력]", "입력\nsample_input", "sample_input.txt"))
    if io_spec:
        d["output_spec"] = io_spec
    return d


def grab_tc(pg, cid):
    """(전체 케이스, 사유). 레이트 리밋에 걸리면 쉬었다 다시 시도한다."""
    for attempt in range(5):
        try:
            raw = json.loads(pg.evaluate(DOWN, cid))
        except Exception:
            return [], "error"
        si = (raw.get("in") or "").replace("\r\n", "\n").rstrip()
        so = (raw.get("out") or "").replace("\r\n", "\n").rstrip()
        if si.strip().lower() in ("not used!", "not given") or \
           so.strip().lower() in ("not used!", "not given"):
            return [], "notused"
        if looks_html(si) or looks_html(so):
            time.sleep(5 + attempt * 5)
            continue
        if not si:
            return [], "empty"
        return [{"in": si, "out": so}], ""
    return [], "blocked"


def main():
    argv = sys.argv[1:]
    force = "--force" in argv
    no_tc = "--no-tc" in argv
    only = None
    if "--only" in argv:
        only = set(argv[argv.index("--only") + 1].split(","))

    rows = json.load(io.open(LIST, encoding="utf-8"))
    os.makedirs(PROB, exist_ok=True)
    os.makedirs(STORE, exist_ok=True)

    from playwright.sync_api import sync_playwright
    pw = sync_playwright().start()
    b = pw.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = b.contexts[0]
    pg = ctx.pages[0] if ctx.pages else ctx.new_page()

    ok = skip = ng = 0
    try:
        for i, r in enumerate(rows, 1):
            no = r["no"]
            if only and no not in only:
                continue
            out = os.path.join(PROB, "%s.json" % no)
            if os.path.exists(out) and not (force or no_tc):
                skip += 1
                continue
            url = VIEW % (r["solveclubId"], r["cid"], r["probBoxId"])
            try:
                pg.goto(url, wait_until="load", timeout=90_000)
                pg.wait_for_timeout(3000)
                try:
                    ntbl = pg.evaluate(TABLES_JS)     # 표 → 마크다운 (DOM 을 바꾼다)
                except Exception:
                    ntbl = 0
                t = pg.inner_text("body") or ""
                if "접근이 제한된" in t:
                    print("  [%2d/%d] %-6s ❌ 접근 제한" % (i, len(rows), no), flush=True)
                    ng += 1
                    continue

                d = parse(t, url, r)
                # apply_images 는 BOJ 배치를 가정해 지문을 통째로 덮어쓴다.
                # 마커가 박힌 본문에서 [문제 설명] 구간만 다시 잘라 온다.
                before, before_ex = d.get("statement"), d.get("examples_text")
                # 그림이 아직 디코딩되기 전이면 naturalWidth 가 0 이라
                # collect_images 의 크기 필터에 걸려 통째로 빠진다(25003 이 그랬다).
                try:
                    pg.evaluate(WAIT_IMGS_JS)
                except Exception:
                    pass
                fp.apply_images(pg, d)
                if d.get("images"):
                    # apply_images 가 d["statement"] 에 [[IMG:n]] 이 박힌 본문을 통째로
                    # 넣어 준다. 지문뿐 아니라 **예제도 그 본문에서** 잘라야 한다 —
                    # 원본 텍스트에서 자르면 [Fig. 2] 글자만 남고 그림이 사라진다.
                    marked = d.get("statement") or ""
                    st = tidy(between(marked, "[문제 설명]", "[예제]", "[제약사항]", "[입출력]"))
                    ex = tidy(between(marked, "[예제]", "[제약사항]", "[입출력]"))
                    d["statement"] = st or before
                    if ex:
                        d["examples_text"] = ex
                else:
                    d["statement"] = before
                    if before_ex:
                        d["examples_text"] = before_ex

                if no_tc and os.path.exists(out):
                    old = json.load(io.open(out, encoding="utf-8"))
                    for k in ("samples", "tc_stored", "tc_full_bytes",
                              "tc_preview", "tc_unavailable"):
                        if k in old:
                            d[k] = old[k]
                elif not no_tc:
                    cases, why = grab_tc(pg, r["cid"])
                    if why:
                        d["tc_unavailable"] = why
                    if cases:
                        full = sum(len(c["in"]) + len(c["out"]) for c in cases)
                        # 전체본은 repo 밖 → sync_tc.py 가 채점서버로 올린다
                        io.open(os.path.join(STORE, "%s.json" % no), "w",
                                encoding="utf-8", newline="").write(
                            json.dumps({"samples": cases, "private": []},
                                       ensure_ascii=False))
                        d["samples"] = [{"in": cases[0]["in"][:TC_CAP],
                                         "out": cases[0]["out"][:TC_CAP]}]
                        d["tc_stored"] = True             # 채점은 서버 보관본으로
                        d["tc_full_bytes"] = full
                        d["tc_preview"] = full > TC_CAP   # 화면에 '일부만' 표시

                d["fetched_at"] = datetime.date.today().isoformat()
                d = {k: v for k, v in d.items() if v not in ("", [], {}, None)}
                io.open(out, "w", encoding="utf-8", newline="").write(
                    json.dumps(d, ensure_ascii=False, indent=1))
                ok += 1
                print("  [%2d/%d] %-6s ✅ %-20s 지문 %5d자 · 표 %d · TC %5.1fMB%s"
                      % (i, len(rows), no, d["title"][:20],
                         len(d.get("statement") or ""), ntbl,
                         (d.get("tc_full_bytes") or 0) / 1e6,
                         "" if d.get("python_supported") else "  ⚠️Python 미지원"),
                      flush=True)
            except Exception as e:
                ng += 1
                print("  [%2d/%d] %-6s ❌ %s"
                      % (i, len(rows), no, str(e).split("\n")[0][:70]), flush=True)
            time.sleep(0.8)
    finally:
        pw.stop()

    print("\n완료: 성공 %d / 건너뜀 %d / 실패 %d" % (ok, skip, ng))
    if os.path.isdir(STORE):
        tot = sum(os.path.getsize(os.path.join(STORE, f)) for f in os.listdir(STORE))
        print("tc_store/swea : %.1f MB (커밋 안 됨)" % (tot / 1e6))
    return 0 if not ng else 1


if __name__ == "__main__":
    sys.exit(main())
