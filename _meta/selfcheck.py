"""
저장소 자체 점검 — 조용히 망가지는 것들을 잡는다.

  python _meta/selfcheck.py

검사 항목
  1. JSON 파일 파싱 (history / cosal_list / swea_ids / index / problems/*)
  2. history.json 구조·중복·미래 날짜·삭제표식 위반
  3. 문제 자료: 지문·예제·시간제한 누락, 예제 오염
  4. 이미지 참조 ↔ 실제 파일 일치
  5. 메모 파일 ↔ 색인 일치
  6. 풀이 파일 헤더 ↔ history 일치
  7. 대시보드 산출물(index.html)의 데이터 일관성
"""
import os, io, re, sys, json, glob, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAD, WARN = [], []


def bad(msg):
    BAD.append(msg)


def warn(msg):
    WARN.append(msg)


def load(path):
    try:
        return json.load(io.open(os.path.join(ROOT, path), encoding="utf-8"))
    except FileNotFoundError:
        return None
    except Exception as e:
        bad("%s 파싱 실패: %s" % (path, str(e)[:90]))
        return None


def main():
    today = datetime.date.today().isoformat()

    # ── 1. 핵심 JSON ─────────────────────────────────────────
    hist = load("_meta/history.json") or {}
    cat = load("_meta/cosal_list.json") or {}
    ids = load("_meta/swea_ids.json") or {}
    idx = load("problems/index.json") or {}
    tomb = set(load("_meta/deleted.json") or [])
    ep = load("_meta/endpoint.json") or {}
    cfg = load("_meta/judge_config.json") or {}

    # ── 2. history ───────────────────────────────────────────
    for day, rec in hist.items():
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day):
            bad("history 날짜 형식 이상: %r" % day)
            continue
        if day > today:
            warn("history 미래 날짜: %s (%d건)" % (day, len(rec.get("items", []))))
        seen = {}
        for it in rec.get("items", []):
            if not isinstance(it, dict):
                continue
            k = "%s/%s" % (it.get("site"), it.get("no"))
            if k in seen:
                bad("history %s 중복 항목: %s" % (day, k))
            seen[k] = 1
            if "%s|%s|%s" % (day, it.get("site"), it.get("no")) in tomb:
                bad("history %s 에 삭제 표식된 항목이 살아 있음: %s" % (day, k))
            f = it.get("file")
            if f and not os.path.exists(os.path.join(ROOT, f)):
                bad("history %s %s 의 코드 파일 없음: %s" % (day, k, f))
            p, t = it.get("passed"), it.get("total")
            if (p is None) != (t is None):
                warn("history %s %s passed/total 한쪽만 있음" % (day, k))
            if p is not None and t is not None and p > t:
                bad("history %s %s passed(%s) > total(%s)" % (day, k, p, t))
        n = len([x for x in rec.get("items", []) if isinstance(x, dict)])
        if rec.get("count", 0) < n:
            bad("history %s count(%s) < items(%d)" % (day, rec.get("count"), n))

    # ── 3. 문제 자료 ──────────────────────────────────────────
    probs = [f for f in glob.glob(os.path.join(ROOT, "problems", "*", "*.json"))
             if os.path.basename(f) != "index.json"]
    for f in probs:
        rel = os.path.relpath(f, ROOT).replace(os.sep, "/")
        try:
            d = json.load(io.open(f, encoding="utf-8"))
        except Exception as e:
            bad("%s 파싱 실패: %s" % (rel, str(e)[:70]))
            continue
        fname = os.path.splitext(os.path.basename(f))[0]
        if str(d.get("no") or "") != fname:
            bad("%s 파일명과 no 불일치 (no=%s)" % (rel, d.get("no")))
        if not (d.get("statement") or "").strip():
            bad("%s 지문 없음" % rel)
        if not (d.get("limits") or {}).get("time"):
            warn("%s 시간 제한 없음" % rel)
        ss = d.get("samples") or []
        if not ss and d.get("tc_unavailable") != "notused":
            # notused = SWEA 가 파일 자체를 안 주는 문제(1770 "Not used!",
            # 1768 정답이 "not given"). 다시 받아도 안 되므로 경고하지 않는다.
            warn("%s 예제 없음" % rel)
        # 조용히 망가지는 대표 사례: 세션이 끊겨 다운로드가 로그인/오류 HTML 을
        # 돌려주는데 그대로 예제로 저장된 것(2026-08-12 에 SWEA 8건).
        for s in ss[:2]:
            t = (s.get("in") or "")[:1500]
            if any(k in t for k in ("<!--", "<!DOCTYPE", "<html", "link href")):
                bad("%s 예제가 HTML 로 오염됨" % rel)
                break
        for s in ss:
            blob = (s.get("in") or "") + (s.get("out") or "")
            if "예제" in blob or "댓글" in blob or "다운로드" in blob:
                bad("%s 예제 오염" % rel)
            if not (s.get("in") or "").strip() or not (s.get("out") or "").strip():
                bad("%s 예제 입출력 빔" % rel)
        for h in (d.get("private_testcases") or []):
            # 출력이 비는 건 정상일 수 있다(조건 만족 결과가 없거나 push 만 하는 케이스).
            # 입력이 통째로 비면 파싱 사고다.
            if not (h.get("in") or ""):
                bad("%s 히든TC 입력이 빔" % rel)
        # 이미지
        imgs = [x for x in (d.get("images") or []) if x]
        for rel_img in imgs:
            if not os.path.exists(os.path.join(ROOT, rel_img)):
                bad("%s 이미지 파일 없음: %s" % (rel, rel_img))
        marks = set(int(m) for m in re.findall(r"\[\[IMG:(\d+)\]\]", d.get("statement") or ""))
        if marks and max(marks) > len(d.get("images") or []):
            bad("%s IMG 마커(%d)가 이미지 수(%d)보다 많음"
                % (rel, max(marks), len(d.get("images") or [])))
        if imgs and not marks:
            warn("%s 이미지는 있는데 지문에 마커가 없음" % rel)

    # 고아 이미지
    used = set()
    for f in probs:
        try:
            d = json.load(io.open(f, encoding="utf-8"))
        except Exception:
            continue
        used.update(x for x in (d.get("images") or []) if x)
    for p in glob.glob(os.path.join(ROOT, "problems", "*", "img", "*")):
        rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
        if rel not in used:
            warn("참조되지 않는 이미지: %s" % rel)

    # ── 4. 색인 ──────────────────────────────────────────────
    items = (idx or {}).get("items") or {}
    if len(items) != len(probs):
        bad("색인 %d개 ≠ 문제 파일 %d개 (build_probindex 재실행 필요)" % (len(items), len(probs)))
    for k, v in items.items():
        if not os.path.exists(os.path.join(ROOT, v.get("path", ""))):
            bad("색인 %s 의 path 없음: %s" % (k, v.get("path")))
        if v.get("note") and not os.path.exists(os.path.join(ROOT, v["note"])):
            bad("색인 %s 의 메모 파일 없음: %s" % (k, v["note"]))

    # 메모 파일이 색인에 빠졌는지
    for p in glob.glob(os.path.join(ROOT, "notes", "*", "*.md")):
        rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
        if not any(v.get("note") == rel for v in items.values()):
            warn("색인에 없는 메모 파일: %s" % rel)

    # ── 5. SWEA 매핑 ──────────────────────────────────────────
    for no, cid in ids.items():
        if not re.fullmatch(r"[A-Za-z0-9+/=_-]+", cid or ""):
            bad("swea_ids %s 의 ID 형식 이상: %r" % (no, cid))
        pf = os.path.join(ROOT, "problems", "swea", "%s.json" % no)
        if os.path.exists(pf):
            try:
                d = json.load(io.open(pf, encoding="utf-8"))
                if cid not in (d.get("url") or ""):
                    bad("SWEA %s 저장된 url 이 매핑 ID 와 다름" % no)
            except Exception:
                pass

    # ── 6. 풀이 파일 ↔ history ───────────────────────────────
    for f in glob.glob(os.path.join(ROOT, "boj", "*.py")) + \
             glob.glob(os.path.join(ROOT, "swea", "*.py")):
        rel = os.path.relpath(f, ROOT).replace(os.sep, "/")
        src = io.open(f, encoding="utf-8").read()
        m = re.search(r"풀이일\s*:\s*(\d{4}-\d{2}-\d{2})", src)
        if not m:
            warn("%s 헤더에 풀이일 없음" % rel)
            continue
        day = m.group(1)
        t = re.search(r"^\s*(BOJ|SWEA)\s+(\d+)\s", src, re.M)
        if not t:
            warn("%s 헤더에 사이트/번호 없음" % rel)
            continue
        key = "%s|%s|%s" % (day, t.group(1), t.group(2))
        inhist = any(isinstance(x, dict) and x.get("site") == t.group(1)
                     and str(x.get("no")) == t.group(2)
                     for x in hist.get(day, {}).get("items", []))
        if not inhist and key not in tomb:
            warn("%s (%s) 가 history 에 없음" % (rel, day))
        if re.search(r"^\s*print\(['\"](?:디버그|debug|test|여기)", src, re.M):
            warn("%s 에 디버그 print 흔적" % rel)

    # ── 7. 대시보드 산출물 ────────────────────────────────────
    ip = os.path.join(ROOT, "index.html")
    if os.path.exists(ip):
        h = io.open(ip, encoding="utf-8").read()
        m = re.search(r"var D=(\{.*?\});", h, re.S)
        if not m:
            bad("index.html 에서 데이터(var D)를 못 찾음")
        else:
            try:
                D = json.loads(m.group(1))
                rows = D.get("rows") or []
                dup = {}
                for r in rows:
                    k = "%s|%s|%s" % (r.get("date"), r.get("site"), r.get("no"))
                    dup[k] = dup.get(k, 0) + 1
                for k, c in dup.items():
                    if c > 1:
                        bad("대시보드 rows 중복: %s (%d회)" % (k, c))
                nd = len(D.get("probs", {}).get("items", {}))
                if nd != len(items):
                    warn("index.html 색인(%d) ≠ problems/index.json(%d) — 재빌드 필요"
                         % (nd, len(items)))
                if D.get("built") != today:
                    warn("index.html 빌드일이 오늘이 아님: %s" % D.get("built"))
            except Exception as e:
                bad("index.html 데이터 파싱 실패: %s" % str(e)[:80])
    else:
        bad("index.html 없음")

    # ── 8. 설정 ──────────────────────────────────────────────
    if ep and not str(ep.get("url", "")).startswith("https://"):
        warn("endpoint.json 의 url 이 https 가 아님: %s" % ep.get("url"))
    for k in ("pyMult", "pyAdd"):
        if k in cfg and not isinstance(cfg[k], (int, float)):
            bad("judge_config %s 가 숫자가 아님" % k)

    # ── 결과 ─────────────────────────────────────────────────
    print("=" * 66)
    print(" 자체 점검 — 문제자료 %d / history %d일 / 색인 %d / SWEA매핑 %d"
          % (len(probs), len(hist), len(items), len(ids)))
    print("=" * 66)
    if BAD:
        print("\n❌ 오류 %d건" % len(BAD))
        for x in BAD[:40]:
            print("   -", x)
        if len(BAD) > 40:
            print("   … 외 %d건" % (len(BAD) - 40))
    if WARN:
        print("\n⚠️  경고 %d건" % len(WARN))
        for x in WARN[:30]:
            print("   -", x)
        if len(WARN) > 30:
            print("   … 외 %d건" % (len(WARN) - 30))
    if not BAD and not WARN:
        print("\n✅ 이상 없음")
    print()
    return 1 if BAD else 0


if __name__ == "__main__":
    sys.exit(main())
