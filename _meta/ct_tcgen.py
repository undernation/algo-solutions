"""
코드트리 기출 — 생성 테스트케이스 도구.

코드트리는 히든 테스트케이스를 주지 않는다(문제 API 에는 예제 1~3개뿐).
그래서 문제마다 **서로 모르는 두 풀이(A/B)** 를 따로 짜고, 랜덤 입력 수백 개에서
둘의 답이 끝까지 일치할 때만 그 입력·출력을 테스트케이스로 남긴다.
입력은 제약을 따로 읽은 **검증기(validate.py)** 가 통과시킨 것만 쓴다
(생성기가 제약을 어기면 두 풀이가 쓰레기 입력에서 '일치'해 버리기 때문).

  python _meta/ct_tcgen.py prep   --group samsung-sw | <no>...   작업 폴더 준비(지문·예제·그림)
  python _meta/ct_tcgen.py check  <no> <sol.py>                    공식 예제로 풀이 확인
  python _meta/ct_tcgen.py cross  <no> [--small 300 --medium 60 --large 12 --max 4 --seed0 1]
  python _meta/ct_tcgen.py emit   <no> [--force]                   최종 TC → 보관소 private
  python _meta/ct_tcgen.py status [--group samsung-sw]

작업 폴더(스포일러 — repo 밖): ~/_스포주의_CT기출_참고풀이/<no>/
  statement.md  ex1.in  ex1.out  img_1.png …   prep 이 만든다
  gen.py        python gen.py <seed> <size>     size ∈ small | medium | large | max
  validate.py   stdin 입력이 제약을 지키면 exit 0, 아니면 이유를 찍고 exit 1
  sol_a.py      풀이 A (생성기 작성자)       ┐ 서로의 코드를 보지 않고 지문만 보고 작성
  sol_b.py      풀이 B (검증기 작성자)       ┘
  cross.json / emit.json                       결과 기록

🚩 풀이는 repo 에 넣지 않는다 — 사용자가 다시 풀 문제의 정답 코드라 스포일러다.
   (기존 관례: ~/_스포주의_B형_참고풀이/). repo 에는 생성된 입력·출력만 들어간다.
🚩 여기서 통과해도 코드트리 공식 채점 통과와 같지 않다. 대시보드는 '생성 TC (공식 아님)'로 표시한다.
"""
import os, io, re, sys, json, time, glob, argparse, datetime, subprocess, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE = os.path.join(ROOT, "_meta", "tc_store", "codetree")
PUBLIC = os.path.join(ROOT, "problems", "codetree")
CATALOG = os.path.join(ROOT, "_meta", "codetree_list.json")
WORK = os.path.join(os.path.expanduser("~"), "_스포주의_CT기출_참고풀이")
PY = sys.executable            # 기준 풀이는 CPython 으로 — 문법 제약 없이, 속도보다 정확성
KST = datetime.timezone(datetime.timedelta(hours=9))

# 최종 TC 구성. 작은 케이스는 손으로 따라가 볼 수 있게, 큰 케이스는 시간 제한 검사용.
PLAN = (("small", 8), ("medium", 10), ("large", 7), ("max", 5))
EMIT_SEED0 = 100000            # cross 에서 쓴 시드와 겹치지 않게
TIMEOUT = {"small": 20, "medium": 40, "large": 120, "max": 240}


# ── 공통 ────────────────────────────────────────────────────────
def jload(p, default=None):
    try:
        return json.load(io.open(p, encoding="utf-8"))
    except Exception:
        return default


def jsave(p, obj, indent=None):
    """임시파일 → rename (중간에 죽어도 반쪽 파일이 남지 않게)."""
    tmp = p + ".tmp"
    io.open(tmp, "w", encoding="utf-8", newline="").write(
        json.dumps(obj, ensure_ascii=False, indent=indent))
    os.replace(tmp, p)


def wdir(no):
    return os.path.join(WORK, no)


def norm(s):
    return "\n".join(l.rstrip() for l in (s or "").replace("\r\n", "\n").split("\n")).rstrip()


NUM = re.compile(r"^[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?$")
INT = re.compile(r"^[+-]?\d+$")


def same(got, want):
    """허브(judge/server.py same)와 같은 판정 — 토큰 단위, 실수 토큰만 1e-6 상대오차.

    정수 토큰은 정확히 같아야 한다. 이 도구를 시험하다 '큰 입력에서 +1 틀리는 풀이'가
    통과해서, 허브 채점기까지 같은 버그(정수에도 상대오차)가 있던 게 드러났다.
    """
    g, w = norm(got), norm(want)
    if g == w:
        return True
    gt, wt = g.split(), w.split()
    if not gt or len(gt) != len(wt):
        return False
    saw = False
    for a, b in zip(gt, wt):
        if a == b:
            continue
        if not (NUM.match(a) and NUM.match(b)):
            return False
        if INT.match(a) or INT.match(b):   # 교차검증은 더 엄격하게 — "3" 과 "3.0" 도 불일치로
            return False
        fa, fb = float(a), float(b)
        if abs(fa - fb) > max(1e-9, 1e-6 * abs(fb)):
            return False
        saw = True
    return saw


def run(script, data, timeout, args=()):
    """(ok, stdout, stderr, sec). ok=False 면 예외·비정상 종료·시간초과."""
    t0 = time.perf_counter()
    try:
        p = subprocess.run([PY, script] + list(args), input=data, capture_output=True,
                           text=True, timeout=timeout, encoding="utf-8", errors="replace",
                           cwd=os.path.dirname(script),
                           env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    except subprocess.TimeoutExpired:
        return False, "", "시간 초과(%ss)" % timeout, time.perf_counter() - t0
    el = time.perf_counter() - t0
    if p.returncode != 0:
        return False, p.stdout, (p.stderr or "")[-1500:], el
    return True, p.stdout, p.stderr or "", el


def examples(no):
    d = wdir(no)
    out = []
    for f in sorted(glob.glob(os.path.join(d, "ex*.in")),
                    key=lambda x: int(re.sub(r"\D", "", os.path.basename(x)) or 0)):
        o = f[:-3] + ".out"
        out.append((os.path.basename(f), io.open(f, encoding="utf-8").read(),
                    io.open(o, encoding="utf-8").read() if os.path.exists(o) else ""))
    return out


def catalog():
    return (jload(CATALOG, {}) or {}).get("items", [])


# ── prep: 작업 폴더 준비 ─────────────────────────────────────────
IMG = re.compile(r"!\[([^\]]*)\]\((https?://[^)\s]+)\)")
# 옛 기출(나무박멸·싸움땅 등 88문제)은 마크다운 대신 HTML 로 그림을 넣는다.
# 처음엔 마크다운만 잡아서 그 문제들이 '그림 0장'으로 준비됐다 — 규칙을 모르는 채
# 풀이를 짜게 되므로 둘 다 받는다.
HIMG = re.compile(r"<img[^>]*?src\s*=\s*['\"]?(https?://[^'\"\s>]+)['\"]?[^>]*>", re.I)
HTAG = re.compile(r"</?p[^>]*>|<br\s*/?>|<hr\s*/?>", re.I)


def fetch_image(url, dst_noext):
    """공개 CDN 그림을 받아 PNG 로 바꾼다(에이전트가 Read 로 볼 수 있게 — webp 는 못 읽는다)."""
    import urllib.request
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    raw = urllib.request.urlopen(req, timeout=60).read()
    try:
        from PIL import Image
        im = Image.open(io.BytesIO(raw))
        if im.mode not in ("RGB", "RGBA", "L"):
            im = im.convert("RGBA")
        p = dst_noext + ".png"
        im.save(p)
        return p
    except Exception:
        ext = os.path.splitext(url.split("?")[0])[1] or ".bin"
        p = dst_noext + ext
        io.open(p, "wb").write(raw)
        return p


def prep_one(no, meta):
    st = jload(os.path.join(STORE, "%s.json" % no))
    if not st or not (st.get("problem") or {}).get("statement"):
        return "보관소에 지문 없음"
    pr = st["problem"]
    d = wdir(no)
    os.makedirs(d, exist_ok=True)
    pub = jload(os.path.join(PUBLIC, "%s.json" % no), {}) or {}
    imgs = {}

    def local(m):
        url = m.group(2)
        if url not in imgs:
            k = len(imgs) + 1
            try:
                p = fetch_image(url, os.path.join(d, "img_%d" % k))
                imgs[url] = os.path.basename(p)
            except Exception as e:
                imgs[url] = "(그림 받기 실패: %s)" % str(e)[:60]
        return "![%s](%s)" % (m.group(1), imgs[url])

    def hlocal(m):
        class _M(object):          # IMG 와 같은 모양으로 넘겨 local() 을 그대로 쓴다
            def group(self, k):
                return "" if k == 1 else m.group(1)
        return "\n" + local(_M()) + "\n"

    def fix(s):
        s = HIMG.sub(hlocal, s or "")
        s = HTAG.sub("\n", s)
        return IMG.sub(local, s).strip()

    L = ["# %s" % (pr.get("title") or pub.get("title") or no), "",
         "- 코드트리 %s · %s" % (no, meta.get("origin") or pub.get("origin") or ""),
         "- 원문: %s" % (pub.get("url") or meta.get("url") or ""),
         "- 한도: %s / %s" % ((pub.get("limits") or {}).get("time", "?"),
                             (pub.get("limits") or {}).get("memory", "?")),
         "", "## 문제", fix(pr.get("statement")), "",
         "## 입력", fix(pr.get("input_spec")), "",
         "## 출력", fix(pr.get("output_spec")), ""]
    if (pr.get("constraints") or "").strip():
        L += ["## 제약", fix(pr.get("constraints")), ""]
    if (pr.get("hint") or "").strip():
        L += ["## 힌트", fix(pr.get("hint")), ""]
    notes = pr.get("sample_notes") or []
    for i, s in enumerate(st.get("samples") or [], 1):
        io.open(os.path.join(d, "ex%d.in" % i), "w", encoding="utf-8", newline="").write(s.get("in", ""))
        io.open(os.path.join(d, "ex%d.out" % i), "w", encoding="utf-8", newline="").write(s.get("out", ""))
        L += ["## 예제 %d  (파일: ex%d.in / ex%d.out)" % (i, i, i),
              "```", s.get("in", "").rstrip(), "```", "출력", "```", s.get("out", "").rstrip(), "```"]
        if i - 1 < len(notes) and (notes[i - 1] or "").strip():
            L += ["설명:", fix(notes[i - 1])]
        L.append("")
    if imgs:
        L += ["## 그림 파일", "이 폴더의 PNG 들 — Read 도구로 열어 보면 된다: " +
              ", ".join(v for v in imgs.values() if not v.startswith("("))]
    io.open(os.path.join(d, "statement.md"), "w", encoding="utf-8", newline="").write("\n".join(L) + "\n")
    return "ok (예제 %d, 그림 %d)" % (len(st.get("samples") or []), len(imgs))


def cmd_prep(a):
    items = catalog()
    if a.group:
        todo = [x for x in items if x.get("group") == a.group]
    else:
        want = set(a.nos)
        todo = [x for x in items if x.get("no") in want]
    os.makedirs(WORK, exist_ok=True)
    readme = os.path.join(WORK, "README.md")
    if not os.path.exists(readme):
        io.open(readme, "w", encoding="utf-8", newline="").write(
            "# ⚠️ 스포일러 — 코드트리 기출 참고 풀이\n\n"
            "생성 테스트케이스를 만들기 위한 **기준 풀이(A/B)·생성기·검증기**다.\n"
            "다시 풀 문제의 정답이 들어 있으니 풀기 전에는 열지 말 것.\n"
            "도구: `python _meta/ct_tcgen.py` (algo-solutions repo)\n")
    for x in todo:
        print("%-6s %-28s %s" % (x["no"], x.get("title", "")[:28], prep_one(x["no"], x)), flush=True)


# ── check: 공식 예제 ─────────────────────────────────────────────
def check_examples(no, sol):
    res = []
    for name, i, o in examples(no):
        ok, out, err, el = run(sol, i, 60)
        res.append({"ex": name, "pass": bool(ok and same(out, o)), "sec": round(el, 3),
                    "err": "" if ok else err[-400:],
                    "got": "" if (ok and same(out, o)) else norm(out)[:300]})
    return res


def cmd_check(a):
    sol = a.sol if os.path.isabs(a.sol) else os.path.join(wdir(a.no), a.sol)
    r = check_examples(a.no, sol)
    print(json.dumps({"no": a.no, "sol": os.path.basename(sol), "all_pass": all(x["pass"] for x in r) and bool(r),
                      "examples": r}, ensure_ascii=False, indent=1))


# ── cross: A/B 교차검증 ─────────────────────────────────────────
def gen_input(no, seed, size):
    ok, out, err, _ = run(os.path.join(wdir(no), "gen.py"), "", TIMEOUT[size], (str(seed), size))
    return (out if ok else None), err


def validate(no, data):
    v = os.path.join(wdir(no), "validate.py")
    if not os.path.exists(v):
        return True, "(검증기 없음)"
    ok, out, err, _ = run(v, data, 60)
    return ok, (out + err).strip()[-300:]


def cmd_cross(a):
    no, d = a.no, wdir(a.no)
    A, B = os.path.join(d, "sol_a.py"), os.path.join(d, "sol_b.py")
    rep = {"no": no, "ok": False, "at": datetime.datetime.now(KST).isoformat(timespec="seconds")}
    miss = [f for f in ("gen.py", "validate.py", "sol_a.py", "sol_b.py") if not os.path.exists(os.path.join(d, f))]
    if miss:
        rep["error"] = "파일 없음: " + ", ".join(miss)
        return finish(d, "cross.json", rep)
    exs = examples(no)
    rep["examples"] = {"count": len(exs),
                       "validator_accepts": [validate(no, i)[0] for _, i, _ in exs],
                       "a": [x["pass"] for x in check_examples(no, A)],
                       "b": [x["pass"] for x in check_examples(no, B)]}
    ex = rep["examples"]
    if not (all(ex["validator_accepts"]) and all(ex["a"]) and all(ex["b"]) and exs):
        rep["error"] = "공식 예제 단계 실패(검증기가 예제를 거부했거나 풀이가 예제를 틀림)"
        return finish(d, "cross.json", rep)
    plan = (("small", a.small), ("medium", a.medium), ("large", a.large), ("max", a.max))
    runs, mism, invalid, gerr, tmax, seen = 0, [], [], [], {"a": 0.0, "b": 0.0}, set()
    seed = a.seed0
    for size, n in plan:
        for _ in range(n):
            seed += 1
            data, err = gen_input(no, seed, size)
            if data is None:
                gerr.append({"seed": seed, "size": size, "err": err[-300:]})
                if len(gerr) >= 3:
                    break
                continue
            h = hashlib.md5(data.encode("utf-8")).hexdigest()
            if h in seen:
                continue
            seen.add(h)
            vok, vmsg = validate(no, data)
            if not vok:
                p = os.path.join(d, "bad_%s_%d.in" % (size, seed))
                io.open(p, "w", encoding="utf-8", newline="").write(data)
                invalid.append({"seed": seed, "size": size, "why": vmsg, "file": os.path.basename(p)})
                if len(invalid) >= 3:
                    break
                continue
            oa, xa, ea, ta = run(A, data, TIMEOUT[size])
            ob, xb, eb, tb = run(B, data, TIMEOUT[size])
            tmax["a"], tmax["b"] = max(tmax["a"], ta), max(tmax["b"], tb)
            runs += 1
            if not (oa and ob and same(xa, xb)):
                p = os.path.join(d, "mm_%s_%d" % (size, seed))
                io.open(p + ".in", "w", encoding="utf-8", newline="").write(data)
                io.open(p + ".a.out", "w", encoding="utf-8", newline="").write(xa if oa else "[A 실패] " + ea)
                io.open(p + ".b.out", "w", encoding="utf-8", newline="").write(xb if ob else "[B 실패] " + eb)
                mism.append({"seed": seed, "size": size, "file": os.path.basename(p) + ".in",
                             "a_ok": oa, "b_ok": ob, "in_len": len(data)})
                if len(mism) >= 3:
                    break
        if len(mism) >= 3 or len(invalid) >= 3 or len(gerr) >= 3:
            break
    rep.update({"runs": runs, "distinct_inputs": len(seen), "mismatches": mism,
                "invalid_inputs": invalid, "generator_errors": gerr,
                "max_sec": {k: round(v, 2) for k, v in tmax.items()},
                "ok": runs > 0 and not mism and not invalid and not gerr})
    return finish(d, "cross.json", rep)


def finish(d, name, rep):
    try:
        jsave(os.path.join(d, name), rep, indent=1)
    except Exception:
        pass
    print(json.dumps(rep, ensure_ascii=False, indent=1))
    return 0 if rep.get("ok") else 1


# ── emit: 최종 TC 를 보관소에 ───────────────────────────────────
def cmd_emit(a):
    no, d = a.no, wdir(a.no)
    cr = jload(os.path.join(d, "cross.json"), {}) or {}
    rep = {"no": no, "ok": False}
    if not cr.get("ok") and not a.force:
        rep["error"] = "cross 가 통과하지 않았다(cross.json). 먼저 python _meta/ct_tcgen.py cross %s" % no
        return finish(d, "emit.json", rep)
    A, B = os.path.join(d, "sol_a.py"), os.path.join(d, "sol_b.py")
    cases, seen, seed = [], set(), EMIT_SEED0
    for size, n in PLAN:
        got = 0
        tries = 0
        while got < n and tries < n * 6:
            tries += 1
            seed += 1
            data, err = gen_input(no, seed, size)
            if data is None:
                continue
            h = hashlib.md5(data.encode("utf-8")).hexdigest()
            if h in seen:
                continue
            vok, vmsg = validate(no, data)
            if not vok:
                rep["error"] = "생성 입력이 검증기에 걸림(%s seed %d): %s" % (size, seed, vmsg)
                return finish(d, "emit.json", rep)
            oa, xa, ea, _ = run(A, data, TIMEOUT[size])
            ob, xb, eb, _ = run(B, data, TIMEOUT[size])
            if not (oa and ob and same(xa, xb)):
                rep["error"] = "emit 중 A/B 불일치(%s seed %d) — cross 를 더 돌려 원인을 찾을 것" % (size, seed)
                io.open(os.path.join(d, "emit_mm_%d.in" % seed), "w", encoding="utf-8", newline="").write(data)
                return finish(d, "emit.json", rep)
            seen.add(h)
            cases.append({"in": data.rstrip("\n") + "\n", "out": norm(xa) + "\n", "size": size})
            got += 1
    if not cases:
        rep["error"] = "생성된 케이스가 없다"
        return finish(d, "emit.json", rep)
    sp = os.path.join(STORE, "%s.json" % no)
    st = jload(sp)
    if not st:
        rep["error"] = "보관소 파일 없음: %s" % sp
        return finish(d, "emit.json", rep)
    today = datetime.datetime.now(KST).date().isoformat()
    st["private"] = [{"in": c["in"], "out": c["out"]} for c in cases]
    st["tc_generated"] = True
    st["tc_note"] = ("생성 TC %d개 (작은 %d · 중간 %d · 큰 %d · 최대 %d) — 서로 독립으로 짠 풀이 2개가 "
                     "랜덤 입력 %d개에서 모두 일치했고, 입력은 제약 검증기를 통과했으며, 두 풀이 모두 공식 예제를 통과했다. "
                     "코드트리 공식 히든 TC 가 아니므로 여기서 맞아도 실제 채점과 다를 수 있다. (%s)"
                     % ((len(cases),) + tuple(sum(1 for c in cases if c["size"] == s) for s, _ in PLAN)
                        + (cr.get("runs", 0), today)))
    jsave(sp, st)
    size = sum(len(c["in"]) + len(c["out"]) for c in cases)
    rep.update({"ok": True, "cases": len(cases), "bytes": size, "store": os.path.relpath(sp, ROOT)})
    return finish(d, "emit.json", rep)


# ── status ──────────────────────────────────────────────────────
def cmd_status(a):
    items = [x for x in catalog() if not a.group or x.get("group") == a.group]
    rows = []
    for x in items:
        d = wdir(x["no"])
        st = jload(os.path.join(STORE, "%s.json" % x["no"]), {}) or {}
        cr = jload(os.path.join(d, "cross.json"), {}) or {}
        rows.append({"no": x["no"], "title": x.get("title"),
                     "files": "".join(k[0] for k in ("gen.py", "validate.py", "sol_a.py", "sol_b.py")
                                      if os.path.exists(os.path.join(d, k))),
                     "cross": ("ok %d" % cr.get("runs", 0)) if cr.get("ok") else ("x" if cr else "-"),
                     "tc": len(st.get("private") or []) if st.get("tc_generated") else 0})
    for r in rows:
        print("%-6s %-26s %-5s %-9s %3s" % (r["no"], (r["title"] or "")[:26], r["files"], r["cross"], r["tc"]))
    print("\nTC 생성 완료 %d / %d" % (sum(1 for r in rows if r["tc"]), len(rows)))


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd")
    p = sp.add_parser("prep"); p.add_argument("nos", nargs="*"); p.add_argument("--group")
    p = sp.add_parser("check"); p.add_argument("no"); p.add_argument("sol")
    p = sp.add_parser("cross"); p.add_argument("no")
    p.add_argument("--small", type=int, default=300); p.add_argument("--medium", type=int, default=60)
    p.add_argument("--large", type=int, default=12); p.add_argument("--max", type=int, default=4)
    p.add_argument("--seed0", type=int, default=0)
    p = sp.add_parser("emit"); p.add_argument("no"); p.add_argument("--force", action="store_true")
    p = sp.add_parser("status"); p.add_argument("--group")
    a = ap.parse_args()
    if a.cmd == "prep":
        return cmd_prep(a)
    if a.cmd == "check":
        return cmd_check(a)
    if a.cmd == "cross":
        return cmd_cross(a)
    if a.cmd == "emit":
        return cmd_emit(a)
    if a.cmd == "status":
        return cmd_status(a)
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main() or 0)
