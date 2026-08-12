"""
로컬 허브 서버 — 채점 + repo 저장/커밋/푸시

GitHub Pages 대시보드(https)와 코딩살구클럽(https) 양쪽에서
http://localhost:12014 를 직접 호출한다.
(크롬은 localhost 를 안전한 출처로 취급하므로 mixed-content 차단이 없다.)

실행:
    python judge/server.py
    python judge/server.py --port 12014 --no-push
    python judge/server.py --runner /opt/pypy3.9-v7.3.9-linux64/bin/pypy3

제출 코드는 PyPy 로 실행한다(있으면 자동 탐색). 백준·코딩살구의 시간 제한이
사실상 C++/PyPy 기준이라, CPython 으로 채점하면 실제 제출 결과와 어긋난다.
서버 자신과 크롤러·빌더는 계속 CPython 을 쓴다(playwright 의존).

엔드포인트
    GET  /            서버 상태 (대시보드가 살아있는지 확인용)
    POST /judge       코딩살구 호환 채점  {sourceCode, testCases, ...}
    POST /run         임의 코드 + 케이스 채점  {code, cases:[{in,out}]}
    POST /save        풀이 저장 + git commit/push
    POST /fetch       문제 크롤링 (fetch_problem.py 위임)
    POST /delete      풀이기록/문제자료 삭제 {kind, site, no, date?}
    GET  /problems    저장된 문제 목록

/save 요청 예
    {
      "site": "BOJ", "no": "2618", "title": "경찰차",
      "url": "https://cosal.aviss.kr/problems/detail/2618",
      "code": "...", "status": "품", "date": "2026-08-12",
      "note": "다익스트라 대신 DP",
      "verdict": {"verdict":"accepted","summary":{"passed":25,"total":25}}
    }
"""
import os, re, io, sys, json, glob, time, subprocess, tempfile, argparse, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable          # 내부 스크립트(크롤러·빌더)용 — playwright 등이 필요해 CPython 고정
RUNNER = sys.executable      # 제출 코드 채점용 — PyPy 가 있으면 자동으로 그것을 쓴다
RUNNER_NAME = "CPython"


def find_runner(explicit=""):
    """제출 코드를 실행할 인터프리터를 고른다.

    백준·코딩살구의 시간 제한은 사실상 C++/PyPy 기준이라, 채점도 PyPy 로 해야
    실제 제출 결과와 어긋나지 않는다. 없으면 CPython 으로 조용히 내려간다.
    """
    import shutil
    cands = [explicit] if explicit else ["pypy3", "pypy3.9", "pypy"]
    for c in cands:
        p = c if os.path.isabs(c) else shutil.which(c)
        if not p:
            continue
        try:
            r = subprocess.run([p, "-VV"], capture_output=True, text=True, timeout=20,
                               encoding="utf-8", errors="replace")
            out = (r.stdout or "") + (r.stderr or "")
            if r.returncode == 0:
                m = re.search(r"PyPy\s+([\d.]+)", out)
                return p, ("PyPy %s" % m.group(1)) if m else "CPython"
        except Exception:
            continue
    if explicit:
        raise SystemExit("❌ 지정한 러너를 찾을 수 없습니다: %s" % explicit)
    return sys.executable, "CPython %s" % sys.version.split()[0]


PORT = 12014
VERBOSE = True
AUTO_PUSH = True
TOKEN = ""
TOKEN_FILE = os.path.join(os.path.expanduser("~"), ".algo-hub-token")


# ── 기기 속도 보정 ────────────────────────────────────────────
# 채점기가 도는 하드웨어는 제각각이다(내 PC vs 오라클 E2.1.Micro 는 실측 8.7배 차이).
# 문제의 C++ 기준 제한을 그대로 쓰면 느린 기기에서 멀쩡한 풀이가 시간초과로 찍힌다.
# 그래서 벤치를 한 번 돌려 '기준 기기 대비 몇 배 느린가'를 구해 제한에 곱한다.
#   허용시간 = 문제제한 x PY_MULT x speed_factor
# 결과는 캐시해 매 기동마다 다시 재지 않는다.
PY_MULT = 3.0          # Python 이 C++ 대비 필요로 하는 배수
BENCH_REF = 1.0        # 기준 기기의 _bench.py 합계(초)
BENCH_FILE = os.path.join(os.path.expanduser("~"), ".algo-hub-bench")
SPEED = 1.0


def measure_speed():
    """_bench.py 합계로 기준 대비 배율 산출(캐시)."""
    if os.path.exists(BENCH_FILE):
        try:
            v = float(io.open(BENCH_FILE, encoding="utf-8").read().strip())
            if v > 0:
                return max(1.0, v / BENCH_REF)
        except Exception:
            pass
    r = subprocess.run([RUNNER, os.path.join(ROOT, "judge", "_bench.py")],
                       cwd=ROOT, capture_output=True, text=True,
                       encoding="utf-8", errors="replace",
                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    m = re.search(r"합계\s+([\d.]+)\s*초", r.stdout or "")
    if not m:
        return 1.0
    v = float(m.group(1))
    try:
        io.open(BENCH_FILE, "w", encoding="utf-8", newline="").write(str(v))
    except OSError:
        pass
    return max(1.0, v / BENCH_REF)


def allowed_time(limit_sec):
    """문제 제한(초) -> 이 기기에서 허용할 실행시간(초)."""
    try:
        t = float(limit_sec or 0)
    except (TypeError, ValueError):
        t = 0.0
    if t <= 0:
        t = 2.0
    return round(t * PY_MULT * SPEED, 1)


def load_token():
    """토큰 파일이 없으면 생성. 공개 엔드포인트 보호용.

    ⚠️ 클라우드 허브와 로컬 허브는 각자 파일을 갖는다. 값이 다르면 대시보드는
    토큰을 하나만 저장하므로 한쪽이 401 이 난다. 반드시 두 허브를 같은 값으로 맞출 것.
        ssh ubuntu@<VM> 'cat ~/.algo-hub-token'   → 내 PC 의 ~/.algo-hub-token 에 그대로 저장
    """
    import secrets
    if os.path.exists(TOKEN_FILE):
        t = io.open(TOKEN_FILE, encoding="utf-8").read().strip()
        if t:
            return t
    t = secrets.token_urlsafe(24)
    io.open(TOKEN_FILE, "w", encoding="utf-8", newline="").write(t)
    try:
        os.chmod(TOKEN_FILE, 0o600)
    except OSError:
        pass
    return t

SUB = {"BOJ": "boj", "SWEA": "swea", "PGS": "programmers", "CT": "codetree"}

# 지문·예제를 저장물에서 제외할지 여부. 사용자 결정(2026-08-11)으로 기본 OFF —
# 지문·예제 입출력·테스트케이스를 그대로 커밋한다.
# 나중에 비공개로 돌리고 싶으면 True 로만 바꾸면 된다.
PUBLIC_SAFE = False
REDACT = ("statement", "samples", "testcases", "private_testcases",
          "description", "input_desc", "output_desc", "html",
          "input_spec", "output_spec")


def redact(prob):
    """공개 저장용으로 저작물 부분을 제거한 사본."""
    if not prob:
        return prob
    if not PUBLIC_SAFE:
        return prob
    out = {k: v for k, v in prob.items() if k not in REDACT}
    if prob.get("samples"):
        out["sample_count"] = len(prob["samples"])
    if prob.get("statement"):
        out["statement_len"] = len(prob["statement"])
    out["_redacted"] = "지문·예제는 저작권 문제로 저장하지 않음 (repo public)"
    return out
SITE_NAME = {"BOJ": "백준", "SWEA": "SW Expert Academy",
             "PGS": "프로그래머스", "CT": "코드트리"}


def log(*a):
    if VERBOSE:
        print(*a, flush=True)


def iso_now():
    return (datetime.datetime.now(datetime.timezone.utc)
            .isoformat(timespec="milliseconds").replace("+00:00", "Z"))


# ══════════════════════════════════════════════════════════════
# 채점
# ══════════════════════════════════════════════════════════════
def norm(s):
    return "\n".join(l.rstrip() for l in (s or "").replace("\r\n", "\n").split("\n")).rstrip()


def run_one(path, data, tl):
    t0 = time.perf_counter()
    try:
        p = subprocess.run([RUNNER, path],
                           input=data if data.endswith("\n") else data + "\n",
                           capture_output=True, text=True, timeout=tl,
                           encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return "time_limit_exceeded", "", time.perf_counter() - t0, ""
    except Exception as e:
        return "runtime_error", "", time.perf_counter() - t0, str(e)[:400]
    el = time.perf_counter() - t0
    if p.returncode != 0:
        return "runtime_error", p.stdout, el, (p.stderr or "")[-1200:]
    return "ok", p.stdout, el, ""


def syntax_error(src):
    """러너(PyPy) 기준 문법 검사. 문제 없으면 빈 문자열."""
    t = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8")
    t.write(src)
    t.close()
    try:
        r = subprocess.run(
            [RUNNER, "-c",
             "import sys;compile(open(sys.argv[1],encoding='utf-8').read(),'<solution>','exec')",
             t.name],
            capture_output=True, text=True, timeout=30, encoding="utf-8", errors="replace")
        if r.returncode == 0:
            return ""
        lines = [x for x in (r.stderr or "").strip().split("\n") if x.strip()]
        return " / ".join(lines[-2:])[:300] or "문법 오류"
    except Exception:
        return ""
    finally:
        try:
            os.unlink(t.name)
        except OSError:
            pass


def judge(src, cases, pub=0, tl=5.0):
    if not (src or "").strip():
        return {"ok": False, "error": "빈 소스코드", "verdict": "compile_error"}
    err = syntax_error(src)
    if err:
        return {"ok": True, "verdict": "compile_error",
                "summary": {"passed": 0, "total": len(cases), "firstFailedIndex": 0},
                "judgedAt": iso_now(), "elapsedSec": 0.0,
                "detail": [{"index": 0, "status": "compile_error", "message": err}]}

    tmp = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8")
    tmp.write(src)
    tmp.close()
    detail, passed, first_fail, verdict, tot_el = [], 0, None, "accepted", 0.0
    try:
        for i, c in enumerate(cases):
            din = c.get("input", c.get("in", "")) or ""
            want = c.get("output", c.get("out", "")) or ""
            st, got, el, err = run_one(tmp.name, din, tl)
            tot_el += el
            kind = "public" if i < pub else "private"
            if st == "ok" and norm(got) == norm(want):
                passed += 1
                detail.append({"index": i, "kind": kind, "status": "passed",
                               "elapsed": round(el, 3)})
                continue
            if st == "ok":
                st = "wrong_answer"
            if first_fail is None:
                first_fail, verdict = i, st
            detail.append({"index": i, "kind": kind, "status": st,
                           "elapsed": round(el, 3), "expected": norm(want)[:600],
                           "got": norm(got)[:600], "stderr": err[:600]})
            log("   ✗ #%d %s (%s)" % (i + 1, st, kind))
    finally:
        try:
            os.unlink(tmp.name)
        except OSError:
            pass
    if passed == len(cases) and cases:
        verdict = "accepted"
    return {"ok": True, "verdict": verdict,
            "summary": {"passed": passed, "total": len(cases),
                        "firstFailedIndex": first_fail},
            "judgedAt": iso_now(), "elapsedSec": round(tot_el, 3), "detail": detail}


# ══════════════════════════════════════════════════════════════
# repo 저장
# ══════════════════════════════════════════════════════════════
def git(*args, check=False):
    r = subprocess.run(["git"] + list(args), cwd=ROOT,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout or "")[:400])
    return r


def safe(s, n=40):
    return re.sub(r"[\\/:*?\"<>|]+", "_", re.sub(r"\s+", "", s or ""))[:n]


def build_header(d, verdict=None):
    site, no, title = d.get("site", "BOJ"), str(d.get("no", "")), d.get("title", "")
    L = [("%s %s  %s" % (site, no, title)).rstrip()]
    if d.get("url"):
        L.append(d["url"])
    L.append("")
    L.append("풀이일 : %s   결과: %s" % (d.get("date") or datetime.date.today().isoformat(),
                                     d.get("status") or "품"))
    p = d.get("problem") or {}
    lim = p.get("limits") or {}
    if lim:
        L.append("한도   : " + " / ".join("%s %s" % (k, v) for k, v in lim.items()))
    if p.get("level") or (p.get("stats") or {}).get("accept_rate"):
        L.append("난이도 : %s  |  정답률 %s%%" % (p.get("level", "?"),
                                             (p.get("stats") or {}).get("accept_rate", "?")))
    for c in (p.get("constraints") or [])[:6]:
        L.append("제약   : " + c)
    if d.get("tags"):
        L.append("분류   : " + ", ".join(d["tags"]))
    if verdict:
        s = verdict.get("summary") or {}
        L.append("")
        L.append("[채점] %s  %s/%s  (%ss)" % (verdict.get("verdict"), s.get("passed"),
                                            s.get("total"), verdict.get("elapsedSec")))
    if PUBLIC_SAFE:
        if p.get("statement") or p.get("samples"):
            L += ["", "[문제] 지문·예제는 저작권상 저장하지 않음 — 위 URL 참조"]
    else:
        if p.get("statement"):
            L += ["", "[문제]", p["statement"].strip()]
        for i, smp in enumerate(p.get("samples") or [], 1):
            L += ["", "[예제 %d]" % i, "입력:", smp.get("in", ""), "출력:", smp.get("out", "")]
    if d.get("note"):
        L += ["", "[메모]", d["note"].strip()]
    return '"""\n' + "\n".join(L) + '\n"""\n\n'


def save_solution(d):
    site = (d.get("site") or "BOJ").upper()
    sub = SUB.get(site, "boj")
    no = str(d.get("no") or "").strip()
    title = d.get("title") or ""
    code = d.get("code") or ""
    if not code.strip():
        return {"ok": False, "error": "코드가 비어 있음"}

    name = no if (sub == "boj" and no) else ("%s_%s" % (no, safe(title)) if no else safe(title))
    rel = "%s/%s.py" % (sub, name)
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    io.open(path, "w", encoding="utf-8", newline="").write(
        build_header(d, d.get("verdict")) + code.rstrip() + "\n")

    # 문제 메타 별도 저장
    if d.get("problem"):
        pd = os.path.join(ROOT, "problems", sub)
        os.makedirs(pd, exist_ok=True)
        io.open(os.path.join(pd, "%s.json" % (no or safe(title))), "w",
                encoding="utf-8", newline="").write(
            json.dumps(redact(d["problem"]), ensure_ascii=False, indent=1))

    # history.json 에 직접 기록.
    # 예전엔 build_heatmap 이 .py 헤더의 '풀이일' 을 긁는 것에만 의존했는데,
    # 같은 날 다른 기록이 있으면 병합에서 밀려 사라졌다. 여기서 확실히 남긴다.
    try:
        hp = os.path.join(ROOT, "_meta", "history.json")
        hist = json.load(io.open(hp, encoding="utf-8")) if os.path.exists(hp) else {}
        day = d.get("date") or datetime.date.today().isoformat()
        rec = hist.setdefault(day, {"count": 0, "items": []})
        item = {"site": site, "no": no, "title": title,
                "status": d.get("status") or "품", "file": rel}
        items = [x for x in rec["items"]
                 if not (isinstance(x, dict) and x.get("site") == site and str(x.get("no")) == no)]
        items.append(item)
        rec["items"] = items
        rec["count"] = max(len(items), rec.get("count", 0))
        io.open(hp, "w", encoding="utf-8", newline="").write(
            json.dumps(hist, ensure_ascii=False, indent=1, sort_keys=True))
        log("   📝 history.json %s (%d건)" % (day, rec["count"]))
    except Exception as e:
        log("   ⚠️ history 기록 실패:", str(e)[:150])

    # 잔디/인덱스 갱신
    for s in ("_meta/build_probindex.py", "_meta/build_heatmap.py", "_meta/build_index.py"):
        subprocess.run([PY, s], cwd=ROOT, capture_output=True,
                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})

    msg = "[%s %s] %s — %s" % (site, no, title, d.get("status") or "품")
    git("add", "-A")
    c = git("commit", "-m", msg)
    committed = c.returncode == 0
    pushed, perr = False, ""
    if committed and AUTO_PUSH:
        p = git("push")
        pushed = p.returncode == 0
        if not pushed:
            # 다른 PC·Actions 가 먼저 올렸으면 non-fast-forward 로 거절된다.
            # fetch 후 rebase 하고 한 번만 재시도한다.
            log("   ↻ push 거절 — rebase 후 재시도")
            git("fetch", "origin")
            rb = git("rebase", "origin/master")
            if rb.returncode != 0:
                git("rebase", "--abort")
                perr = "rebase 충돌 — 수동 해결 필요"
            else:
                p = git("push")
                pushed = p.returncode == 0
                perr = "" if pushed else (p.stderr or "")[-300:]
            if not pushed:
                log("   ⚠️ push 실패:", perr[:200])

    log("   💾 %s  commit=%s push=%s" % (rel, committed, pushed))
    return {"ok": True, "file": rel, "message": msg,
            "committed": committed, "pushed": pushed, "pushError": perr,
            "stdout": (c.stdout or "")[-300:] if not committed else ""}


def delete_item(d):
    """풀이 기록 / 문제 자료 삭제.

    kind="submission": history.json 에서 (date, site, no) 기록 제거.
                       그 문제의 마지막 기록이면 코드 파일(boj/1234.py)도 지운다.
    kind="problem"   : problems/<sub>/<no>.json 과 그 문제의 이미지들을 지운다.
                       (코딩살구 커리큘럼 문제는 목록에는 남고 '자료 없음' 상태가 된다)

    되돌릴 수 없으므로 무엇을 지웠는지 removed 로 돌려준다.
    """
    kind = (d.get("kind") or "").strip()
    site = (d.get("site") or "").upper()
    no = str(d.get("no") or "").strip()
    if kind not in ("submission", "problem"):
        return {"ok": False, "error": "kind 는 submission 또는 problem 이어야 합니다"}
    if not site or not no:
        return {"ok": False, "error": "site/no 가 필요합니다"}
    sub = SUB.get(site, "boj")
    removed = []

    if kind == "submission":
        date = (d.get("date") or "").strip()
        if not date:
            return {"ok": False, "error": "date 가 필요합니다"}
        hp = os.path.join(ROOT, "_meta", "history.json")
        if not os.path.exists(hp):
            return {"ok": False, "error": "history.json 없음"}
        hist = json.load(io.open(hp, encoding="utf-8"))
        rec = hist.get(date)
        if not rec:
            return {"ok": False, "error": "%s 에 기록이 없습니다" % date}
        keep, gone = [], 0
        for it in rec.get("items", []):
            if (isinstance(it, dict) and it.get("site") == site
                    and str(it.get("no")) == no):
                gone += 1
                continue
            keep.append(it)
        if not gone:
            return {"ok": False, "error": "%s 에 %s %s 기록이 없습니다" % (date, site, no)}
        rec["items"] = keep
        rec["count"] = max(0, rec.get("count", 0) - gone)
        if not keep and rec["count"] <= 0:
            hist.pop(date, None)
        removed.append("history %s: %s %s" % (date, site, no))

        # 코드 파일의 '풀이일'·실수노트에서 다시 살아나지 않도록 삭제 표식을 남긴다.
        tp = os.path.join(ROOT, "_meta", "deleted.json")
        tomb = []
        if os.path.exists(tp):
            try:
                tomb = json.load(io.open(tp, encoding="utf-8")) or []
            except Exception:
                tomb = []
        key = "%s|%s|%s" % (date, site, no)
        if key not in tomb:
            tomb.append(key)
        io.open(tp, "w", encoding="utf-8", newline="").write(
            json.dumps(sorted(tomb), ensure_ascii=False, indent=1))

        # 다른 날짜에도 이 문제 기록이 남아 있는지 확인
        still = any(isinstance(x, dict) and x.get("site") == site and str(x.get("no")) == no
                    for day in hist.values() for x in day.get("items", []))
        io.open(hp, "w", encoding="utf-8", newline="").write(
            json.dumps(hist, ensure_ascii=False, indent=1, sort_keys=True))
        if not still:
            for f in glob.glob(os.path.join(ROOT, sub, "%s.py" % no)) + \
                     glob.glob(os.path.join(ROOT, sub, "%s_*.py" % no)):
                try:
                    os.remove(f)
                    removed.append(os.path.relpath(f, ROOT).replace(os.sep, "/"))
                except OSError:
                    pass
        msg = "[삭제] %s %s 풀이기록 %s" % (site, no, date)

    else:  # problem
        pj = os.path.join(ROOT, "problems", sub, "%s.json" % no)
        imgs = []
        if os.path.exists(pj):
            try:
                imgs = json.load(io.open(pj, encoding="utf-8")).get("images") or []
            except Exception:
                imgs = []
            os.remove(pj)
            removed.append("problems/%s/%s.json" % (sub, no))
        for rel in imgs:
            fp = os.path.join(ROOT, rel.replace("/", os.sep))
            if rel and os.path.exists(fp):
                try:
                    os.remove(fp)
                    removed.append(rel)
                except OSError:
                    pass
        if not removed:
            return {"ok": False, "error": "삭제할 자료가 없습니다"}
        msg = "[삭제] %s %s 문제자료" % (site, no)

    for s in ("_meta/build_probindex.py", "_meta/build_heatmap.py", "_meta/build_index.py"):
        subprocess.run([PY, s], cwd=ROOT, capture_output=True,
                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})

    git("add", "-A")
    c = git("commit", "-m", msg)
    committed = c.returncode == 0
    pushed, perr = False, ""
    if committed and AUTO_PUSH:
        p = git("push")
        pushed = p.returncode == 0
        if not pushed:
            git("fetch", "origin")
            rb = git("rebase", "origin/master")
            if rb.returncode != 0:
                git("rebase", "--abort")
                perr = "rebase 충돌 — 수동 해결 필요"
            else:
                p = git("push")
                pushed = p.returncode == 0
                perr = "" if pushed else (p.stderr or "")[-300:]
    log("   🗑️ %s  (%d개)  commit=%s push=%s" % (msg, len(removed), committed, pushed))
    return {"ok": True, "removed": removed, "message": msg,
            "committed": committed, "pushed": pushed, "pushError": perr}


def fetch_problem(ref, save=False):
    """ref(URL 또는 BOJ 번호) 크롤링. save=True 면 problems/ 에 저장하고 커밋까지."""
    argv = [PY, "_meta/fetch_problem.py", ref, "--print"]
    if save:
        argv.append("--save")
    r = subprocess.run(argv,
                       cwd=ROOT, capture_output=True, text=True,
                       encoding="utf-8", errors="replace",
                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    out = (r.stdout or "").strip()
    i = out.find("{")
    if i < 0:
        err = (r.stderr or out or "")
        low = err.lower()
        if "playwright" in low or "executable doesn't exist" in low:
            return {"ok": False, "needsLocal": True,
                    "error": "이 허브에는 브라우저·로그인 세션이 없어 크롤링할 수 없습니다. "
                             "로그인된 내 PC의 로컬 허브에서 가져오세요."}
        return {"ok": False, "error": err[-500:]}
    try:
        prob = json.loads(out[i:])
    except Exception as e:
        return {"ok": False, "error": "파싱 실패: %s" % e}
    res = {"ok": True, "problem": prob}
    if not save:
        return res

    # 빈 페이지(로그인 만료·없는 문제)를 저장해 쓰레기 파일을 남기지 않는다.
    if not prob.get("no") or not (prob.get("statement") or "").strip():
        junk = os.path.join(ROOT, "problems",
                            SUB.get(prob.get("site", "BOJ"), "boj"),
                            "%s.json" % (prob.get("no") or "unknown"))
        if os.path.exists(junk):
            try:
                os.remove(junk)
            except OSError:
                pass
        return {"ok": False,
                "error": "문제 내용을 못 읽었습니다. 해당 사이트 로그인이 풀렸거나 "
                         "그 사이트에 없는 문제일 수 있습니다.",
                "problem": prob}

    # 저장 모드 — 색인 재생성 후 커밋/푸시해서 다른 기기·대시보드에도 반영한다.
    subprocess.run([PY, "_meta/build_probindex.py"], cwd=ROOT, capture_output=True,
                   env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    subprocess.run([PY, "_meta/build_heatmap.py"], cwd=ROOT, capture_output=True,
                   env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    git("add", "problems", "_meta", "index.html", "assets", "README.md", "HEATMAP.md")
    msg = "[문제추가] %s %s %s" % (prob.get("site", ""), prob.get("no", ""),
                                prob.get("title", ""))
    c = git("commit", "-m", msg.strip())
    res["committed"] = c.returncode == 0
    res["pushed"] = False
    if res["committed"] and AUTO_PUSH:
        p = git("push")
        if p.returncode != 0:
            git("fetch", "origin")
            rb = git("rebase", "origin/master")
            if rb.returncode != 0:
                git("rebase", "--abort")
            else:
                p = git("push")
        res["pushed"] = p.returncode == 0
    log("   ➕ %s  commit=%s push=%s" % (msg, res["committed"], res["pushed"]))
    return res


def status():
    br = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    ah = git("rev-list", "--count", "@{u}..HEAD").stdout.strip() or "0"
    dirty = bool(git("status", "--porcelain").stdout.strip())
    n = 0
    for s in ("boj", "swea", "programmers", "codetree"):
        d = os.path.join(ROOT, s)
        if os.path.isdir(d):
            n += len([f for f in os.listdir(d) if f.endswith(".py")])
    return {"ok": True, "service": "algo-hub", "language": "python", "authRequired": bool(TOKEN),
            "speedFactor": round(SPEED, 2), "pyMult": PY_MULT,
            "runner": RUNNER_NAME,
            "python": sys.version.split()[0], "repo": ROOT,
            "branch": br, "ahead": ah, "dirty": dirty, "solutions": n,
            "autoPush": AUTO_PUSH,
            "endpoints": ["/judge", "/run", "/save", "/fetch", "/delete", "/problems"]}


# ══════════════════════════════════════════════════════════════
# HTTP
# ══════════════════════════════════════════════════════════════
CORS = {"Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
        "Access-Control-Allow-Headers": "content-type, accept, x-auth-token, authorization",
        "Access-Control-Max-Age": "86400"}


class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _send(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        for k, v in CORS.items():
            self.send_header(k, v)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        for k, v in CORS.items():
            self.send_header(k, v)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self):
        p = self.path.split("?")[0].rstrip("/")
        if p in ("", "/status"):
            return self._send(200, status())
        if p == "/problems":
            out = []
            for s in ("boj", "swea", "programmers", "codetree"):
                d = os.path.join(ROOT, "problems", s)
                if not os.path.isdir(d):
                    continue
                for f in sorted(os.listdir(d)):
                    if f.endswith(".json"):
                        try:
                            out.append(json.load(io.open(os.path.join(d, f), encoding="utf-8")))
                        except Exception:
                            pass
            return self._send(200, {"ok": True, "count": len(out), "problems": out})
        return self._send(404, {"ok": False, "error": "not found"})

    def _auth_ok(self):
        if not TOKEN:
            return True
        got = (self.headers.get("X-Auth-Token")
               or self.headers.get("Authorization", "").replace("Bearer ", "").strip())
        if not got:
            from urllib.parse import urlparse, parse_qs
            got = (parse_qs(urlparse(self.path).query).get("token") or [""])[0]
        import hmac
        return hmac.compare_digest(str(got), str(TOKEN))

    def do_POST(self):
        p = self.path.split("?")[0].rstrip("/")
        if not self._auth_ok():
            log("   ⛔ 인증 실패 (%s)" % p)
            return self._send(401, {"ok": False, "error": "unauthorized",
                                    "hint": "X-Auth-Token 헤더 필요"})
        try:
            n = int(self.headers.get("Content-Length") or 0)
            body = json.loads(self.rfile.read(n).decode("utf-8") or "{}")
        except Exception as e:
            return self._send(400, {"ok": False, "error": "bad json: %s" % e})

        try:
            if p in ("/judge", ""):
                cases = body.get("testCases") or []
                try:
                    tl = allowed_time(body.get("timeLimit"))
                except (TypeError, ValueError):
                    tl = 5.0
                log("\n▶ 채점  problemId=%s  TC %d개  제한 %ss"
                    % (body.get("problemId"), len(cases), body.get("timeLimit")))
                # allowed_time() 이 이미 PY_MULT·기기보정을 반영한 값이다.
                # 예전 고정식(x3+2)을 여기서 또 곱해 허용시간이 3배로 부풀던 버그가 있었다.
                r = judge(body.get("sourceCode") or "", cases,
                          int(body.get("publicTestCaseCount") or 0), tl)
                s = r.get("summary", {})
                log("◀ %s  %s/%s" % (r.get("verdict"), s.get("passed"), s.get("total")))
                return self._send(200, r)

            if p == "/run":
                cases = body.get("cases") or []
                log("\n▶ 실행  TC %d개" % len(cases))
                return self._send(200, judge(body.get("code") or "", cases, 0,
                                             allowed_time(body.get("timeLimit"))))

            if p == "/delete":
                log("\n▶ 삭제  %s %s %s %s" % (body.get("kind"), body.get("site"),
                                             body.get("no"), body.get("date") or ""))
                return self._send(200, delete_item(body))

            if p == "/save":
                log("\n▶ 저장  %s %s %s" % (body.get("site"), body.get("no"), body.get("title")))
                return self._send(200, save_solution(body))

            if p == "/fetch":
                ref = body.get("ref") or body.get("url") or str(body.get("no") or "")
                sv = bool(body.get("save"))
                log("\n▶ 크롤링%s  %s" % (" + 저장" if sv else "", ref[:70]))
                return self._send(200, fetch_problem(ref, save=sv))
        except Exception as e:
            import traceback
            traceback.print_exc()
            return self._send(200, {"ok": False, "error": str(e)[:400]})

        return self._send(404, {"ok": False, "error": "not found"})

    def log_message(self, *a):
        pass


def main():
    global PY, PORT, VERBOSE, AUTO_PUSH
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=PORT)
    ap.add_argument("--python", default=sys.executable)
    ap.add_argument("--no-push", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--no-auth", action="store_true", help="토큰 인증 끄기(로컬 전용)")
    ap.add_argument("--runner", default="", help="제출 코드 실행 인터프리터 (기본: pypy3 자동탐색)")
    a = ap.parse_args()
    global TOKEN
    PY, PORT, VERBOSE, AUTO_PUSH = a.python, a.port, not a.quiet, not a.no_push
    TOKEN = "" if a.no_auth else load_token()
    global RUNNER, RUNNER_NAME, SPEED
    RUNNER, RUNNER_NAME = find_runner(a.runner)
    SPEED = measure_speed()

    print("=" * 64)
    print("  🐍 algo-hub  로컬 서버 (채점 + repo 저장)")
    print("=" * 64)
    print("  포트    : %d" % PORT)
    print("  repo    : %s" % ROOT)
    print("  채점러너 : %s" % RUNNER_NAME)
    print("             %s" % RUNNER)
    print("  자동푸시 : %s" % ("ON" if AUTO_PUSH else "OFF"))
    print("  속도보정 : x%.1f  (1초 제한 -> %.1f초 허용)" % (SPEED, allowed_time(1)))
    if TOKEN:
        print("  인증토큰 : %s" % TOKEN)
        print("             (%s)" % TOKEN_FILE)
        print("             ※ 클라우드 허브와 같은 값이어야 대시보드가 양쪽 다 씁니다")
    else:
        print("  인증     : 꺼짐 (--no-auth)")
    print()
    print("  대시보드 : https://undernation.github.io/algo-solutions/")
    print("  코딩살구 : IP 127.0.0.1 / 포트 %d 로 등록" % PORT)
    print()
    print("  Ctrl+C 종료")
    print("=" * 64)
    ThreadingHTTPServer(("0.0.0.0", PORT), H).serve_forever()


if __name__ == "__main__":
    main()
