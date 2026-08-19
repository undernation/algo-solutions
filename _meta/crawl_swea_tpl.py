"""SWEA B형(Pro) 문제의 Main / User Code 기본 코드를 수집한다.

B형은 한 파일짜리 풀이가 아니다. 풀이 화면이 두 칸으로 나뉘어 있다.

  Main       수정 불가. 입력을 읽어 User 함수를 부르고 "#TC 점수" 를 찍는다.
  User Code  응시자가 채우는 부분. 표준 입출력을 쓰면 안 된다.

Main 은 `from solution import init, addTower, ...` 로 User 쪽을 가져온다.
그 import 줄만 걷어내고 [User + Main] 순서로 이어 붙이면 한 파일로 채점된다.

수집 결과는 problems/swea/<no>.json 에 들어간다:
    api_style : true            (B형 — 두 칸 편집기로 열라는 표시)
    template  : {main, user}    (파이썬 기준. 미지원이면 없음)

사용법:
    python _meta/crawl_swea_tpl.py            # 없는 것만
    python _meta/crawl_swea_tpl.py --force
    python _meta/crawl_swea_tpl.py --only 25958

선행: python _meta/debug_chrome.py 로 띄운 크롬에서 SWEA 로그인
"""
import os, io, re, sys, json, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROB = os.path.join(ROOT, "problems", "swea")
LIST = os.path.join(ROOT, "_meta", "swea_club.json")

VIEW = ("https://swexpertacademy.com/main/talk/solvingClub/problemView.do"
        "?solveclubId=%s&contestProbId=%s&probBoxId=%s&type=PROBLEM")

# CodeMirror 가 textarea 를 감싸고 있어서 textarea.value 는 낡아 있다.
GET = """() => {
  const g = id => { const t = document.getElementById(id); if (!t) return null;
    let e = t.nextElementSibling;
    while (e && !e.classList.contains('CodeMirror')) e = e.nextElementSibling;
    return (e && e.CodeMirror) ? e.CodeMirror.getValue() : t.value; };
  const s = document.getElementById('sel_lang');
  return JSON.stringify({
    lang: s ? s.value : '',
    opts: s ? [...s.options].map(o => o.value) : [],
    main: g('mainSource'), user: g('textSource')});
}"""

# "언어 변경 시 작성 중인 코드가 지워집니다" 확인 팝업
CONFIRM = """() => {
  let n = 0;
  document.querySelectorAll('.popup_layer.show, .layer_alert').forEach(l => {
    if (!l.offsetHeight) return;
    const b = [...l.querySelectorAll('a,button')]
      .find(x => (x.textContent || '').trim() === '확인');
    if (b) { b.click(); n++; }
  });
  return n;
}"""

IMPORT_RE = re.compile(r"^\s*from\s+solution\s+import\s+.*$", re.M)


def merge(main, user):
    """Main 의 `from solution import ...` 를 걷어내고 [User + Main] 으로 잇는다."""
    m = IMPORT_RE.sub("# (합칠 때 제거) from solution import ...", main or "")
    return (user or "").rstrip() + "\n\n\n" + m.lstrip("\n")


def close_ide(ctx):
    for q in list(ctx.pages):
        if "solvingProblem.do" in q.url:
            try:
                q.close()
            except Exception:
                pass


def fetch(ctx, cid):
    """(main, user, langs). 파이썬이 없으면 main/user 는 None."""
    close_ide(ctx)
    pg = ctx.new_page()
    try:
        pg.goto(VIEW % (CLUB, cid, BOX), wait_until="load", timeout=90_000)
        pg.wait_for_timeout(2200)
        pg.evaluate("goProblem()")
        pg.wait_for_timeout(1500)
        ide = None
        for _ in range(25):
            ide = next((q for q in ctx.pages if "solvingProblem.do" in q.url), None)
            if ide:
                break
            time.sleep(0.7)
        if not ide:
            return None, None, []
        ide.bring_to_front()
        # 탭은 먼저 열리고 내용은 뒤에 온다. 언어 선택이 생길 때까지 기다린다
        # (안 기다리면 opts 가 빈 채로 "파이썬 미지원" 으로 잘못 읽힌다).
        try:
            ide.wait_for_load_state("load", timeout=60_000)
        except Exception:
            pass
        for _ in range(30):
            try:
                if ide.evaluate("() => !!document.getElementById('sel_lang')"):
                    break
            except Exception:
                pass
            ide.wait_for_timeout(1000)
        ide.wait_for_timeout(3000)
        d = json.loads(ide.evaluate(GET))
        if not (d.get("opts") or []):
            ide.close()
            raise RuntimeError("풀이 화면을 못 읽음(언어 목록 비어 있음)")
        if "Y" not in (d.get("opts") or []):
            ide.close()
            return None, None, d.get("opts") or []
        if d.get("lang") != "Y":
            ide.evaluate("() => { const s=document.getElementById('sel_lang');"
                         " s.value='Y'; codeLangOnChange('Y'); }")
            for _ in range(6):
                ide.wait_for_timeout(900)
                if ide.evaluate(CONFIRM):
                    break
            ide.wait_for_timeout(4500)
            d = json.loads(ide.evaluate(GET))
        ide.close()
        return d.get("main"), d.get("user"), d.get("opts") or []
    finally:
        try:
            pg.close()
        except Exception:
            pass


CLUB = BOX = None


def main():
    global CLUB, BOX
    argv = sys.argv[1:]
    force = "--force" in argv
    only = None
    if "--only" in argv:
        only = set(argv[argv.index("--only") + 1].split(","))

    rows = json.load(io.open(LIST, encoding="utf-8"))
    CLUB, BOX = rows[0]["solveclubId"], rows[0]["probBoxId"]

    from playwright.sync_api import sync_playwright
    pw = sync_playwright().start()
    b = pw.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = b.contexts[0]

    ok = skip = nopy = ng = 0
    try:
        for i, r in enumerate(rows, 1):
            no = r["no"]
            if only and no not in only:
                continue
            path = os.path.join(PROB, "%s.json" % no)
            if not os.path.exists(path):
                continue
            d = json.load(io.open(path, encoding="utf-8"))
            if d.get("template") and not force:
                skip += 1
                continue
            try:
                m, u, langs = fetch(ctx, r["cid"])
                d["api_style"] = True          # B형 — 두 칸 편집기로 연다
                if m and u:
                    d["template"] = {"main": m, "user": u}
                    ok += 1
                    mark = "✅ main %4d자 / user %3d자" % (len(m), len(u))
                else:
                    d.pop("template", None)
                    nopy += 1
                    mark = "➖ 파이썬 미지원 (%s)" % ",".join(langs)
                io.open(path, "w", encoding="utf-8", newline="").write(
                    json.dumps(d, ensure_ascii=False, indent=1))
                print("  [%2d/%d] %-6s %-18s %s"
                      % (i, len(rows), no, r["title"][:18], mark), flush=True)
            except Exception as e:
                ng += 1
                print("  [%2d/%d] %-6s ❌ %s"
                      % (i, len(rows), no, str(e).split("\n")[0][:70]), flush=True)
            time.sleep(0.8)
    finally:
        close_ide(ctx)
        pw.stop()

    print("\n완료: 수집 %d / 파이썬없음 %d / 건너뜀 %d / 실패 %d"
          % (ok, nopy, skip, ng))
    return 0 if not ng else 1


if __name__ == "__main__":
    sys.exit(main())
