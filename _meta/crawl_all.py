"""
푼 문제 전체를 미리 크롤링해 problems/<site>/<no>.json 으로 저장.

대시보드가 문제를 "누르면 바로" 보여주려면 미리 받아둬야 한다.
(허브 /fetch 는 로그인 세션이 필요해 클라우드에선 못 돌린다.)

사용법:
    python _meta/crawl_all.py                # 없는 것만 (BOJ 전체)
    python _meta/crawl_all.py --site BOJ     # 특정 사이트만
    python _meta/crawl_all.py --limit 30     # 앞에서 N개만
    python _meta/crawl_all.py --force        # 이미 있는 것도 다시
    python _meta/crawl_all.py --empty        # 지문이 빈 것만 다시 (파서 수정 후 복구)
    python _meta/crawl_all.py --bad          # 예제가 오염된 것만 다시
    python _meta/crawl_all.py --htc          # 히든 테스트케이스만 채우기

선행조건: 디버그 크롬(9222) + 코딩살구 로그인
    python C:/Users/solom/crawler.py chrome
"""
import os, io, re, sys, json, time, datetime, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROB = os.path.join(ROOT, "problems")
SUB = {"BOJ": "boj", "SWEA": "swea", "PGS": "programmers", "CT": "codetree"}

spec = importlib.util.spec_from_file_location(
    "fp", os.path.join(ROOT, "_meta", "fetch_problem.py"))
fp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fp)


def targets():
    """크롤링 대상: ① 코딩살구 전체 카탈로그  ② 내가 푼 기록(history.json).

    ①이 먼저 오도록 해 커리큘럼 문제부터 채운다.
    """
    seen, out = set(), []

    # ① 코딩살구 전체 문제 (crawl_cosal_list.py 산출물)
    cl = os.path.join(ROOT, "_meta", "cosal_list.json")
    if os.path.exists(cl):
        for it in json.load(io.open(cl, encoding="utf-8")).get("items", []):
            no = str(it.get("no") or "").strip()
            if not no or ("BOJ", no) in seen:
                continue
            seen.add(("BOJ", no))
            out.append({"site": "BOJ", "no": no, "title": it.get("title", ""),
                        "url": fp.COSAL % no})

    # ② SWEA 매핑에 등록된 문제 전부 (내가 아직 안 푼 추천 세트도 포함)
    ip = os.path.join(ROOT, "_meta", "swea_ids.json")
    if os.path.exists(ip):
        for no, cid in sorted(json.load(io.open(ip, encoding="utf-8")).items(),
                              key=lambda kv: int(kv[0]) if kv[0].isdigit() else 0):
            if ("SWEA", no) in seen:
                continue
            seen.add(("SWEA", no))
            out.append({"site": "SWEA", "no": no, "title": "", "url": fp.SWEA % cid})

    out += _from_history(seen)
    return out


def _from_history(seen):
    """history.json + swea_ids.json 에서 (site, no, title, url) 목록."""
    hist = json.load(io.open(os.path.join(ROOT, "_meta", "history.json"), encoding="utf-8"))
    ids = {}
    p = os.path.join(ROOT, "_meta", "swea_ids.json")
    if os.path.exists(p):
        ids = json.load(io.open(p, encoding="utf-8"))

    out = []
    for day in sorted(hist, reverse=True):
        for it in hist[day].get("items", []):
            if not isinstance(it, dict):
                continue
            site, no = it.get("site", ""), str(it.get("no", "")).strip()
            if not site or not no or (site, no) in seen:
                continue
            seen.add((site, no))
            url = ""
            if site == "BOJ":
                url = fp.COSAL % no
            elif site == "SWEA":
                cid = ids.get(no)
                if not cid:
                    continue                      # contestProbId 모르면 건너뜀
                url = fp.SWEA % cid
            else:
                continue
            out.append({"site": site, "no": no, "title": it.get("title", ""), "url": url})
    return out


def main():
    a = sys.argv[1:]
    only = a[a.index("--site") + 1].upper() if "--site" in a else ""
    lim = int(a[a.index("--limit") + 1]) if "--limit" in a else 0
    force = "--force" in a

    todo = targets()
    if only:
        todo = [t for t in todo if t["site"] == only]
    if "--htc" in a:
        # 히든 테스트케이스가 있다고 표기됐는데 아직 수집 안 된 것만
        def need_htc(t):
            f = os.path.join(PROB, SUB[t["site"]], t["no"] + ".json")
            if not os.path.exists(f):
                return False
            try:
                d = json.load(io.open(f, encoding="utf-8"))
            except Exception:
                return False
            return bool(d.get("private_tc_count")) and not d.get("private_testcases")
        todo = [t for t in todo if need_htc(t)]
    elif "--empty" in a or "--bad" in a:
        # 파서 수정 후 복구용.
        #   --empty : 지문이 비어 저장된 것
        #   --bad   : 예제에 "예제 입력/출력" 헤딩이 섞여 오염된 것
        want_empty, want_bad = "--empty" in a, "--bad" in a

        def broken(t):
            f = os.path.join(PROB, SUB[t["site"]], t["no"] + ".json")
            if not os.path.exists(f):
                return False
            try:
                d = json.load(io.open(f, encoding="utf-8"))
            except Exception:
                return True
            # 지문이 아예 비었거나, 잘려서 토막만 남은 것도 복구 대상.
            # (본문의 "…을 입력받아" 에서 끊기던 버그로 9건이 20자 안팎만 저장됐었다.
            #  정상 문제는 최소 33자였으므로 30자를 경계로 둔다.)
            if want_empty and len((d.get("statement") or "").strip()) < 30:
                return True
            if want_bad:
                txt = "".join((s.get("in", "") + s.get("out", ""))
                              for s in (d.get("samples") or []))
                if "예제" in txt:
                    return True
                # SWEA 는 TC 를 파일로 받는데, 세션이 끊기면 로그인/오류 **HTML**
                # 이 그대로 저장된다(실제 8건). 그 상태로 채점하면 HTML 과 비교해
                # 무조건 틀린다. 눈에 잘 안 띄므로 여기서 잡는다.
                head = txt[:1500]
                if any(k in head for k in ("<!--", "<!DOCTYPE", "<html",
                                           "link href", "<script", "stylesheet")):
                    return True
                # SWEA 정답 파일은 "#1 ..." 형식이다. 아니면 뭔가 잘못 받은 것.
                if t["site"] == "SWEA":
                    out = "".join(s.get("out", "") for s in (d.get("samples") or []))
                    if out.strip() and not re.match(r"\s*#1\b", out):
                        return True
                    # 예제가 아예 없는 것도 복구 대상. 단 SWEA 가 파일을 제공하지
                    # 않는 문제(Not used!)는 아무리 다시 받아도 안 되므로 제외한다.
                    if not (d.get("samples") or []) and d.get("tc_unavailable") != "notused":
                        return True
            return False
        todo = [t for t in todo if broken(t)]
    elif not force:
        todo = [t for t in todo
                if not os.path.exists(os.path.join(PROB, SUB[t["site"]], t["no"] + ".json"))]
    if lim:
        todo = todo[:lim]

    print("대상 %d개  (BOJ %d / SWEA %d)" % (
        len(todo), sum(t["site"] == "BOJ" for t in todo), sum(t["site"] == "SWEA" for t in todo)),
        flush=True)
    if not todo:
        return

    from playwright.sync_api import sync_playwright
    okc = ng = 0
    t0 = time.time()
    with sync_playwright() as pw:
        b = pw.chromium.connect_over_cdp("http://127.0.0.1:9222")
        pg = b.contexts[0].new_page()
        try:
            for i, t in enumerate(todo, 1):
                try:
                    pg.goto(t["url"], wait_until="networkidle", timeout=60_000)
                    pg.wait_for_timeout(1500 if t["site"] == "BOJ" else 2200)
                    if any(k in pg.url.lower() for k in ("loginpage", "sign_in")):
                        # 연속 요청이 많으면 일시적으로 로그인 페이지로 튄다. 한 번 쉬고 재시도.
                        time.sleep(8)
                        pg.goto(t["url"], wait_until="networkidle", timeout=60_000)
                        pg.wait_for_timeout(2000)
                        if any(k in pg.url.lower() for k in ("loginpage", "sign_in")):
                            ng += 1
                            print("  [%d/%d] %s %-6s ⚠️ 로그인 페이지로 튐 — 건너뜀"
                                  % (i, len(todo), t["site"], t["no"]), flush=True)
                            continue
                    txt = pg.evaluate("() => document.body.innerText") or ""
                    parser = fp.parse_cosal if t["site"] == "BOJ" else fp.parse_swea
                    d = parser(txt, pg.url)
                    # ⚠️ SWEA TC 다운로드를 이미지 수집보다 **먼저** 한다.
                    #    apply_images 가 지연 이미지를 강제로 다 불러오는데, 그 직후
                    #    contestProbDown.do 를 치면 SWEA 가 error.jsp 로 거절한다
                    #    (단독 실행은 되는데 크롤에서만 실패하던 원인, 2026-08-12).
                    if t["site"] == "SWEA":
                        cid0 = re.search(r"contestProbId=([A-Za-z0-9+/=_-]+)", t["url"])
                        if cid0:
                            sm, why = fp.fetch_swea_tc(pg, cid0.group(1))
                            d["samples"] = sm or []
                            if why:
                                d["tc_unavailable"] = why
                    fp.apply_images(pg, d)      # 지문 중간 그림 수집 + [[IMG:n]] 마커
                    if t["site"] == "BOJ" and d.get("private_tc_count"):
                        # "모두 보기"로 펼쳐지는 히든 테스트케이스 — 채점 정확도가 크게 올라간다
                        tc, om = fp.cap_private_tc(fp.fetch_private_tc(pg, t["no"]))
                        d["private_testcases"] = tc
                        if om:
                            d["private_tc_omitted"] = om
                    if t["site"] == "SWEA":
                        # 예제(공식 sample_input/output)는 위에서 이미 받았다.
                        tl = fp.swea_time_limit((d.get("limits") or {}).get("time"))
                        if tl:
                            d.setdefault("limits", {})["time_sec"] = tl
                    if not d.get("title") and not d.get("statement"):
                        ng += 1
                        print("  [%d/%d] %s %-6s ⚠️ 내용 없음" % (i, len(todo), t["site"], t["no"]),
                              flush=True)
                        continue
                    # 번호 대조 — SWEA 는 ID 매핑이 틀리면 엉뚱한 문제를 저장하게 된다.
                    got_no = str(d.get("no") or "").strip()
                    if got_no and got_no != t["no"]:
                        ng += 1
                        print("  [%d/%d] %s %-6s ❌ 번호 불일치 → 페이지는 %s (%s) — 건너뜀"
                              % (i, len(todo), t["site"], t["no"], got_no,
                                 (d.get("title") or "")[:20]), flush=True)
                        continue
                    d["fetched_at"] = datetime.date.today().isoformat()
                    if t["title"] and not d.get("title"):
                        d["title"] = t["title"]
                    d = {k: v for k, v in d.items() if v not in ("", [], {}, None)}
                    dd = os.path.join(PROB, SUB[t["site"]])
                    os.makedirs(dd, exist_ok=True)
                    io.open(os.path.join(dd, "%s.json" % t["no"]), "w",
                            encoding="utf-8", newline="").write(
                        json.dumps(d, ensure_ascii=False, indent=1))
                    okc += 1
                    htc = len(d.get("private_testcases") or [])
                    print("  [%d/%d] %s %-6s ✅ %-20s 지문%5d자 예제%d%s"
                          % (i, len(todo), t["site"], t["no"], (d.get("title") or "")[:20],
                             len(d.get("statement") or ""), len(d.get("samples") or []),
                             (" 히든%d" % htc) if htc else ""),
                          flush=True)
                except Exception as e:
                    ng += 1
                    print("  [%d/%d] %s %-6s ❌ %s" % (i, len(todo), t["site"], t["no"],
                                                      str(e).split("\n")[0][:70]), flush=True)
        finally:
            try:
                pg.close()
            except Exception:
                pass
    print("\n완료: 성공 %d / 실패 %d / %.1f분" % (okc, ng, (time.time() - t0) / 60), flush=True)


if __name__ == "__main__":
    main()
