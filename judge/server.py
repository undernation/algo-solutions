"""
로컬 허브 서버 — 채점 + repo 저장/커밋/푸시

GitHub Pages 대시보드(https)와 코딩살구클럽(https) 양쪽에서
http://localhost:12014 를 직접 호출한다.
(크롬은 localhost 를 안전한 출처로 취급하므로 mixed-content 차단이 없다.)

실행:
    python judge/server.py
    python judge/server.py --port 12014 --no-push

엔드포인트
    GET  /            서버 상태 (대시보드가 살아있는지 확인용)
    POST /judge       코딩살구 호환 채점  {sourceCode, testCases, ...}
    POST /run         임의 코드 + 케이스 채점  {code, cases:[{in,out}]}
    POST /save        풀이 저장 + git commit/push
    POST /fetch       문제 크롤링 (fetch_problem.py 위임)
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
import os, re, io, sys, json, time, subprocess, tempfile, argparse, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable
PORT = 12014
VERBOSE = True
AUTO_PUSH = True
TOKEN = ""
TOKEN_FILE = os.path.join(os.path.expanduser("~"), ".algo-hub-token")


def load_token():
    """토큰 파일이 없으면 생성. 공개 엔드포인트 보호용."""
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
        p = subprocess.run([PY, path],
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


def judge(src, cases, pub=0, tl=5.0):
    if not (src or "").strip():
        return {"ok": False, "error": "빈 소스코드", "verdict": "compile_error"}
    try:
        compile(src, "<solution>", "exec")
    except SyntaxError as e:
        return {"ok": True, "verdict": "compile_error",
                "summary": {"passed": 0, "total": len(cases), "firstFailedIndex": 0},
                "judgedAt": iso_now(), "elapsedSec": 0.0,
                "detail": [{"index": 0, "status": "compile_error",
                            "message": "%s (line %s)" % (e.msg, e.lineno)}]}

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


def fetch_problem(ref):
    r = subprocess.run([PY, "_meta/fetch_problem.py", ref, "--print"],
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
        return {"ok": True, "problem": json.loads(out[i:])}
    except Exception as e:
        return {"ok": False, "error": "파싱 실패: %s" % e}


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
            "python": sys.version.split()[0], "repo": ROOT,
            "branch": br, "ahead": ah, "dirty": dirty, "solutions": n,
            "autoPush": AUTO_PUSH,
            "endpoints": ["/judge", "/run", "/save", "/fetch", "/problems"]}


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
                    tl = float(body.get("timeLimit") or 0) or 5.0
                except (TypeError, ValueError):
                    tl = 5.0
                log("\n▶ 채점  problemId=%s  TC %d개  제한 %ss"
                    % (body.get("problemId"), len(cases), body.get("timeLimit")))
                r = judge(body.get("sourceCode") or "", cases,
                          int(body.get("publicTestCaseCount") or 0), max(tl, 1.0) * 3 + 2)
                s = r.get("summary", {})
                log("◀ %s  %s/%s" % (r.get("verdict"), s.get("passed"), s.get("total")))
                return self._send(200, r)

            if p == "/run":
                cases = body.get("cases") or []
                log("\n▶ 실행  TC %d개" % len(cases))
                return self._send(200, judge(body.get("code") or "", cases, 0,
                                             float(body.get("timeLimit") or 5) * 3 + 2))

            if p == "/save":
                log("\n▶ 저장  %s %s %s" % (body.get("site"), body.get("no"), body.get("title")))
                return self._send(200, save_solution(body))

            if p == "/fetch":
                ref = body.get("ref") or body.get("url") or str(body.get("no") or "")
                log("\n▶ 크롤링  %s" % ref[:70])
                return self._send(200, fetch_problem(ref))
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
    a = ap.parse_args()
    global TOKEN
    PY, PORT, VERBOSE, AUTO_PUSH = a.python, a.port, not a.quiet, not a.no_push
    TOKEN = "" if a.no_auth else load_token()

    print("=" * 64)
    print("  🐍 algo-hub  로컬 서버 (채점 + repo 저장)")
    print("=" * 64)
    print("  포트    : %d" % PORT)
    print("  repo    : %s" % ROOT)
    print("  자동푸시 : %s" % ("ON" if AUTO_PUSH else "OFF"))
    if TOKEN:
        print("  인증토큰 : %s" % TOKEN)
        print("             (%s)" % TOKEN_FILE)
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
