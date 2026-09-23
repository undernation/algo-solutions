"""
저장소 자체 점검 — 조용히 망가지는 것들을 잡는다.

  python _meta/selfcheck.py
  python _meta/selfcheck.py --leak-only            # 🔒 공개 금지 검사만 (워킹트리)
  python _meta/selfcheck.py --leak-only --staged   # 🔒 이번 커밋에 들어갈 내용만 (pre-commit 훅)

검사 항목
  1. JSON 파일 파싱 (history / cosal_list / swea_ids / index / problems/*)
  2. history.json 구조·중복·미래 날짜·삭제표식 위반
  3. 문제 자료: 지문·예제·시간제한 누락, 예제 오염
  4. 이미지 참조 ↔ 실제 파일 일치
  5. 메모 파일 ↔ 색인 일치
  6. 풀이 파일 헤더 ↔ history 일치
  7. 대시보드 산출물(index.html)의 데이터 일관성
  9. 🔒 공개 금지 — 코드트리 유형 태그·진행상태(항상) / privateSites 사이트의 지문·예제 /
     TC 보관소 gitignore — + 코드트리 카탈로그 형식

--leak-only 종료 코드: 0 깨끗함 / 1 공개 금지 항목 발견 / 2 검사 자체 실패
"""
import os, io, re, sys, json, glob, datetime, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAD, WARN = [], []


# ── 🔒 공개 금지 검사 (코드트리 · TC 보관소) ─────────────────────────
# repo 는 public 이라 한 번 push 한 건 히스토리·포크·캐시에 남는다. 되돌리려면 히스토리
# 재작성밖에 없다(2026-08-12 에 한 번 해 봤다 — clone 206MB 사고). 그래서 이 검사만은
# pre-commit 훅이 **커밋을 막는다** (나머지 훅 단계는 실패해도 통과). 두 겹이다.
#  (1) 항상 — 공개 여부와 무관한 규칙(ct_spec §3-0):
#      · 유형 스포(tags·prerequisite_lessons)·내 진행상태(progress_status)는 코드트리
#        카탈로그·문제 파일 어디에도 두지 않는다(사용자 규칙 '유형 스포 금지').
#      · TC 보관소(_meta/tc_store/)는 gitignore 돼 있어야 하고 추적 중인 파일이 없어야 한다
#        (전체 TC 564MB — Pages 가 죽었던 사고. 비공개 사이트 원문도 여기 있다).
#  (2) 비공개 사이트일 때만 — 지문·입출력 설명·제약·힌트·예제가 repo 에 들어가면 안 된다.
#      어느 사이트가 비공개인지는 _meta/judge_config.json 의 "privateSites" 한 곳이 정한다
#      (소유자 결정 2026-09-23: [] = 코드트리도 BOJ/SWEA 처럼 공개 저장). 파일·키를 못 읽으면
#      ["CT"] 로 본다 — 설정이 깨졌다고 검사가 꺼지는 쪽으로 실패하지 않게.
#      비공개로 되돌렸을 때 실제로 새는 길(확인함):
#        · fetch_problem.py 의 parse_codetree 는 지문·입출력·예제를 problems/codetree/ 에 쓴다.
#        · server.build_header 는 비공개 처리가 없으면 [문제] 지문·[예제]·제약 줄을 헤더에 넣는다.
#        · CLAUDE.md 의 풀이 파일 템플릿이 "제약 :"·"[문제] (지문)" 을 손으로 적게 되어 있다.
SUB = {"BOJ": "boj", "SWEA": "swea", "PGS": "programmers", "CT": "codetree"}
CONFIG = "_meta/judge_config.json"
# 유형 스포·진행상태 — 공개 여부와 무관하게 코드트리 파일에 있으면 안 된다.
SPOILER_KEYS = frozenset(("tags", "prerequisite_lessons", "progress_status"))
# 비공개 사이트의 problems/<sub>/<no>.json 에 있으면 안 되는 지문 키(중첩까지 본다).
# ct_spec §4-2 의 금지 키 + 코드트리 API 원본 이름(그대로 덤프한 경우) + 다른 사이트 형식의 지문 키.
CONTENT_KEYS = frozenset((
    "statement", "samples", "input_spec", "output_spec", "constraints", "hint",
    "sample_notes", "problem", "private_testcases",
    "description", "input_format", "output_format", "code_block", "test_cases",
    "testcases", "examples_text", "samples_raw", "tc_preview", "html",
    "input_desc", "output_desc"))
# 카탈로그의 지문 키. 트레일 소개문(description)은 비로그인 공개 API 라 막지 않는다.
CAT_CONTENT_KEYS = frozenset((
    "statement", "samples", "input_spec", "output_spec", "constraints", "hint",
    "sample_notes", "private_testcases", "input_format", "output_format",
    "code_block", "test_cases"))
CT_CAT = "_meta/codetree_list.json"
TC_STORE = "_meta/tc_store/"
# 풀이 헤더에 있으면 안 되는 것. 허용되는 건 build_header 가 쓰는 안내 한 줄뿐:
#   [문제] 코드트리 지문은 비공개(허브 보관) — 위 URL 참조
_HDR_BAD_SECT = re.compile(r"^\[(?:예제|입력|출력|힌트|제약)")
_HDR_CONSTR = re.compile(r"^제약\s*:")
_HDR_NEXT_SECT = re.compile(r"^\[[^\]\n]{1,10}\]")     # [메모] [검증] [채점] … 다음 절 머리


def private_sites(staged=False):
    """judge_config.json 의 privateSites → (사이트 집합, 근거). 못 읽으면 ({"CT"}, 기본값).

    규칙은 server.load_private_sites · crawl_codetree.load_private_sites 와 똑같이 맞춘다
    (없음·깨짐·키 없음·목록 아님 → {"CT"}). 셋 중 이 검사만 더 너그러우면, 서버·크롤러는
    비공개로 보는데 훅은 지문 커밋을 통과시키는 틈이 생긴다. 그래서 BOM 도 봐주지 않는다
    (json.load 가 BOM 을 오류로 보므로 다른 둘은 그때 비공개로 동작한다).
    staged=True(훅)면 이번 커밋에 들어갈 설정을 먼저 본다 — 스위치를 비공개로 되돌리는
    커밋에 지문이 같이 실려 있으면 그 커밋의 설정 기준으로 막아야 한다.
    """
    raw = _staged_blobs([CONFIG]).get(CONFIG) if staged else None
    if raw is None:
        try:
            raw = io.open(os.path.join(ROOT, CONFIG), "rb").read()
        except Exception:
            raw = None
    try:
        v = json.loads(raw.decode("utf-8"))["privateSites"]
        if isinstance(v, list):
            return set(str(x).strip().upper() for x in v if str(x).strip()), CONFIG
    except Exception:
        pass
    return {"CT"}, "기본값 — %s 의 privateSites 를 못 읽음" % CONFIG


def _git(args, data=None):
    """git 실행 → (종료코드, stdout 바이트). git 이 없으면 (None, b"")."""
    try:
        r = subprocess.run(["git"] + list(args), cwd=ROOT, input=data,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return r.returncode, r.stdout
    except Exception:
        return None, b""


def _json_keys(o, acc):
    if isinstance(o, dict):
        for k, v in o.items():
            acc.add(k)
            _json_keys(v, acc)
    elif isinstance(o, list):
        for v in o:
            _json_keys(v, acc)
    return acc


def json_leaks(text, banned, check_images=False):
    """JSON 원문 → 들어 있으면 안 되는 키들. 깨진 JSON 이라고 통과시키면 그게 곧 구멍이라,
    파싱이 안 되면 원문에서 "키": 모양을 찾는다."""
    try:
        d = json.loads(text)
    except ValueError:
        found = [k for k in sorted(banned) if re.search(r'"%s"\s*:' % re.escape(k), text)]
        if check_images and re.search(r'"images"\s*:\s*\[\s*"', text):
            found.append("images")
        return found
    found = sorted(k for k in _json_keys(d, set()) if k in banned)
    # 그림도 지문의 일부다(코드트리 그림은 지문 마크다운 속 CDN 주소로만 둔다).
    if check_images and isinstance(d, dict) and d.get("images"):
        found.append("images")
    return found


def header_leaks(src):
    """비공개 사이트 풀이 파일(.py) 맨 앞 docstring 헤더 → 누출 사유 목록."""
    m = re.search(r'("""|\'\'\')(.*?)\1', src, re.S)
    if not m:
        return []
    L = [x.strip() for x in m.group(2).split("\n")]

    def nonblank(j):
        while j < len(L) and not L[j]:
            j += 1
        return j

    why = []
    for i, s in enumerate(L):
        if _HDR_BAD_SECT.match(s):
            why.append("헤더에 %s… 절" % s[:6])
        elif _HDR_CONSTR.match(s):
            why.append("헤더에 제약 줄(%s…)" % s[:14])
        elif s.startswith("[문제]"):
            rest, j = s[len("[문제]"):].strip(), i + 1
            if not rest:                        # 안내문이 다음 줄에 따로 있어도 받는다
                j = nonblank(j)
                if j >= len(L) or _HDR_NEXT_SECT.match(L[j]):
                    continue                    # 빈 [문제] 절 — 새는 게 없다
                rest, j = L[j], j + 1
            if "비공개" not in rest:
                why.append("헤더 [문제] 절에 지문")
                continue
            j = nonblank(j)
            if j < len(L) and not _HDR_NEXT_SECT.match(L[j]):
                why.append("헤더 [문제] 안내문 뒤에 본문(%s…)" % L[j][:14])
    return why


def leak_kind(rel, subs):
    """repo 상대경로 → 검사 종류(없으면 None). subs = 비공개 사이트 폴더들.
    store=TC 보관소 / cat=카탈로그 / prob=비공개 사이트 문제 JSON / spoil=공개 코드트리 문제 JSON
    / sol=비공개 사이트 풀이 / odd=비공개 사이트 폴더에 있으면 안 되는 파일"""
    if rel.startswith(TC_STORE):
        return "store"
    if rel == CT_CAT:
        return "cat"
    parts = rel.split("/")
    if len(parts) >= 3 and parts[0] == "problems":
        if parts[1] in subs:
            if len(parts) == 3 and parts[2].endswith(".json"):
                return "prob"
            # 그림·TC 조각 등 — 비공개 사이트는 공개 JSON 한 장 말고는 둘 게 없다.
            return None if parts[-1] == ".gitkeep" else "odd"
        if parts[1] == "codetree" and len(parts) == 3 and parts[2].endswith(".json"):
            return "spoil"                  # 공개여도 유형 태그·진행상태는 안 된다
        return None
    if len(parts) >= 2 and parts[0] in subs:
        if len(parts) == 2 and parts[1].endswith(".py"):
            return "sol"
        # 예제 입력(input.txt 같은)을 옆에 두면 그대로 공개된다. boj/·swea/ 에도 .py 말곤 없다.
        return None if parts[-1] == ".gitkeep" else "odd"
    return None


def _key_reasons(found):
    """금지 키 목록 → 사유 문장(유형 스포와 지문을 나눠 적는다 — 고칠 곳이 다르다)."""
    sp = [k for k in found if k in SPOILER_KEYS]
    ct = [k for k in found if k not in SPOILER_KEYS]
    out = []
    if sp:
        out.append("유형 스포·진행상태 필드 %s (공개 여부와 무관하게 금지)" % ", ".join(sp))
    if ct:
        out.append("비공개 사이트인데 지문 필드 %s" % ", ".join(ct))
    return out


def leak_reasons(rel, kind, data, subs=()):
    """한 파일의 사유 목록. data 는 바이트(None 이면 못 읽음)."""
    if kind == "store":
        return ["TC 보관소 파일이 커밋 대상 (git rm --cached / git reset 으로 내릴 것)"]
    if kind == "odd":
        return ["비공개 사이트 폴더에 허용되지 않은 파일 (공개 JSON·풀이 .py 만 둔다)"]
    if data is None:
        return []
    text = data.decode("utf-8-sig", "replace")
    if kind == "prob":
        return _key_reasons(json_leaks(text, CONTENT_KEYS | SPOILER_KEYS, check_images=True))
    if kind == "spoil":
        return _key_reasons(json_leaks(text, SPOILER_KEYS))
    if kind == "cat":
        banned = SPOILER_KEYS | (CAT_CONTENT_KEYS if "codetree" in subs else frozenset())
        return _key_reasons(json_leaks(text, banned))
    if kind == "sol":
        return header_leaks(text)
    return []


def _tc_store_rules(skip=()):
    """TC 보관소가 gitignore 되어 있고, 추적 중인 파일이 없는지. (사유 목록, 경고 목록)
    skip: 이미 '커밋 대상' 으로 보고한 경로(같은 파일을 두 번 적지 않게)."""
    why, warns = [], []
    rc, _ = _git(["check-ignore", "-q", TC_STORE + "codetree/_probe.json"])
    if rc == 1:
        why.append("%s 가 .gitignore 에서 빠졌다 — git add -A 한 번에 지문·전체 TC 가 올라간다"
                   % TC_STORE)
    elif rc != 0:
        warns.append("git check-ignore 실패 — TC 보관소 gitignore 여부를 확인 못 함")
    # 한 번 강제로(git add -f) 들어간 파일은 .gitignore 가 있어도 계속 추적된다.
    rc, out = _git(["ls-files", "-z", "--", TC_STORE])
    tracked = [p.decode("utf-8", "replace") for p in out.split(b"\0") if p] if rc == 0 else []
    tracked = [p for p in tracked if p not in skip]
    for p in tracked[:5]:
        why.append("추적 중인 TC 보관소 파일: %s" % p)
    if len(tracked) > 5:
        why.append("… 추적 중인 TC 보관소 파일 %d개 더" % (len(tracked) - 5))
    return why, warns


def _staged_blobs(paths):
    """스테이징된(이번 커밋에 들어갈) 내용 → {경로: 바이트}. cat-file 한 번으로 읽는다
    (파일마다 git show 를 부르면 1,400개 첫 커밋에서 수십 초 걸린다)."""
    if not paths:
        return {}
    rc, out = _git(["cat-file", "--batch"],
                   b"".join(b":" + p.encode("utf-8") + b"\n" for p in paths))
    got, pos = {}, 0
    if rc != 0:
        return got
    for p in paths:
        nl = out.find(b"\n", pos)
        if nl < 0:
            break
        head = out[pos:nl].split(b" ")
        pos = nl + 1
        if len(head) != 3 or not head[2].isdigit():
            continue                                  # "<이름> missing" 등
        n = int(head[2])
        got[p] = out[pos:pos + n]
        pos += n + 1
    return got


def leak_scan(staged=False):
    """공개 금지 검사. staged=True 면 이번 커밋에 들어갈 내용만, 아니면 워킹트리 전체.
    반환: (문제 [(경로, 사유)], 경고 [문장], 비공개 설정 설명)"""
    sites, basis = private_sites(staged)
    subs = set(SUB.get(s, s.lower()) for s in sites)
    mode = "비공개 사이트: %s (%s)" % (", ".join(sorted(sites)) or "없음", basis)
    leaks, warns = [], []
    READ = ("prob", "spoil", "cat", "sol")           # 내용을 봐야 하는 종류
    if staged:
        rc, out = _git(["diff", "--cached", "--name-only", "-z", "--diff-filter=ACMRT"])
        if rc != 0:
            raise RuntimeError("git diff --cached 실패 (rc=%s)" % rc)
        names = [p.decode("utf-8", "replace") for p in out.split(b"\0") if p]
        cand = [(p, leak_kind(p, subs)) for p in names]
        cand = [(p, k) for p, k in cand if k]
        blobs = _staged_blobs([p for p, k in cand if k in READ])
        for p, k in cand:
            data = blobs.get(p)
            if data is None and k in READ:
                try:                                  # 스테이징본을 못 읽으면 워킹트리로라도
                    data = io.open(os.path.join(ROOT, p), "rb").read()
                    warns.append("%s 스테이징본을 못 읽어 워킹트리 파일로 검사함" % p)
                except Exception:
                    # 못 읽은 걸 '깨끗함' 으로 칠 수는 없다 — 막고 사람이 보게 한다.
                    leaks.append((p, "내용을 읽지 못해 공개해도 되는지 확인 못 함"))
            for r in leak_reasons(p, k, data, subs):
                leaks.append((p, r))
    else:
        cand = []
        tops = ["problems/%s" % s for s in sorted(subs | {"codetree"})] + sorted(subs)
        for top in tops:
            for dp, dns, fns in os.walk(os.path.join(ROOT, top)):
                dns[:] = [d for d in dns if d != "__pycache__"]
                for fn in fns:
                    rel = os.path.relpath(os.path.join(dp, fn), ROOT).replace(os.sep, "/")
                    k = leak_kind(rel, subs)
                    if k:
                        cand.append((rel, k))
        if os.path.exists(os.path.join(ROOT, CT_CAT)):
            cand.append((CT_CAT, "cat"))
        # 커밋될 일 없는 파일(.gitignore 대상)은 공개 파일이 아니다.
        if cand:
            rc, out = _git(["check-ignore", "-z", "--stdin"],
                           b"".join(p.encode("utf-8") + b"\0" for p, _ in cand))
            if rc in (0, 1):
                ign = set(x.decode("utf-8", "replace") for x in out.split(b"\0") if x)
                cand = [(p, k) for p, k in cand if p not in ign]
        for p, k in cand:
            try:
                data = io.open(os.path.join(ROOT, p), "rb").read()
            except Exception:
                data = None
            for r in leak_reasons(p, k, data, subs):
                leaks.append((p, r))
    why, w2 = _tc_store_rules(set(p for p, _ in leaks))
    leaks += [(TC_STORE, r) for r in why]
    return leaks, warns + w2, mode


def leak_main(staged):
    """--leak-only: 0 깨끗함 / 1 공개 금지 항목 발견 / 2 검사 자체 실패."""
    try:
        leaks, warns, mode = leak_scan(staged)
    except Exception as e:
        print("⛔ 공개 금지 검사(코드트리·TC 보관소) 자체가 실패했습니다: %s" % str(e)[:200])
        return 2
    for w in warns:
        print("⚠️  %s" % w)
    if not leaks:
        print("🔒 공개 금지 검사 통과%s — %s" % (" (스테이징)" if staged else "", mode))
        return 0
    print("⛔ 공개하면 안 되는 내용 %d건 — repo 는 public 이라 push 하면 되돌릴 수 없다" % len(leaks))
    print("   (%s)" % mode)
    for p, r in leaks[:40]:
        print("   - %s: %s" % (p, r))
    if len(leaks) > 40:
        print("   … 외 %d건" % (len(leaks) - 40))
    print("   유형 태그·진행상태는 어디에도 두지 않고, 비공개 사이트 지문·예제는 _meta/tc_store/"
          " (git 밖)에만 둔다. (ct_spec §3-0)")
    return 1


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
    # cp949 콘솔에서 PYTHONIOENCODING 없이 돌리면 이모지 print 가 UnicodeEncodeError 로
    # 죽는다. 그러면 종료코드가 1 이 되어 훅은 '누출' 로 읽는다 — 글자만 깨지게 둔다.
    try:
        sys.stdout.reconfigure(errors="replace")
    except Exception:
        pass
    if "--leak-only" in sys.argv[1:]:
        return leak_main(staged="--staged" in sys.argv[1:])
    today = datetime.date.today().isoformat()

    # ── 1. 핵심 JSON ─────────────────────────────────────────
    hist = load("_meta/history.json") or {}
    cat = load("_meta/cosal_list.json") or {}
    ctcat = load(CT_CAT)            # 없으면 None — 코드트리 크롤링 전
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
            # 번호 없는 기록은 제목으로 가른다 — build_heatmap._ikey·대시보드 key() 와 같은 규칙.
            # (예전처럼 "BOJ/" 로 보면 같은 날 서로 다른 제목 기록이 전부 '중복' 으로 잡힌다)
            no = str(it.get("no") or "").strip()
            k = "%s/%s" % (it.get("site"), no or "~" + ((it.get("title") or "").strip() or "이름없음"))
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
    psubs = set(SUB.get(s, s.lower()) for s in private_sites()[0])
    priv_nolen = []          # 비공개 문제인데 지문 길이 0 — 크롤러가 지문을 못 받은 것
    stale_priv = []          # 공개로 바꿨는데 아직 비공개 형식(지문 없음)으로 남은 파일
    for f in probs:
        rel = os.path.relpath(f, ROOT).replace(os.sep, "/")
        try:
            d = json.load(io.open(f, encoding="utf-8"))
        except Exception as e:
            bad("%s 파싱 실패: %s" % (rel, str(e)[:70]))
            continue
        fname = os.path.splitext(os.path.basename(f))[0]
        sub = os.path.basename(os.path.dirname(f))
        if str(d.get("no") or "") != fname:
            bad("%s 파일명과 no 불일치 (no=%s)" % (rel, d.get("no")))
        if sub == "codetree" and d.get("site") != "CT":
            bad("%s site 가 CT 가 아님 (site=%s)" % (rel, d.get("site")))
        if d.get("private_content") or d.get("locked"):
            # 비공개 사이트: 지문·예제는 repo 에 없는 게 정상이다(허브 보관소에 있다).
            # 여기서 '지문 없음' 으로 잡으면 1,400건이 전부 오류가 된다. 대신 들어 있으면
            # 안 되는 것은 9번(공개 금지 검사)이 본다. 403 으로 못 연 문제(locked)는 크롤러가
            # private_content 없이 locked 만 달고, 지문도 한도도 없다.
            # 객관식·서술형(ptype)은 채점 스펙이 없어 한도가 원래 비어 있다.
            if not d.get("locked") and not d.get("ptype") \
                    and not (d.get("limits") or {}).get("time"):
                warn("%s 시간 제한 없음" % rel)
            if not d.get("locked") and not d.get("statement_len"):
                priv_nolen.append(rel)
            if d.get("private_content") and sub not in psubs:
                stale_priv.append(rel)
            continue
        if not (d.get("statement") or "").strip():
            bad("%s 지문 없음" % rel)
        # 코드트리의 객관식·서술형(ptype)은 채점 스펙도 예제도 원래 없다(283문제).
        if not d.get("ptype") and not (d.get("limits") or {}).get("time"):
            warn("%s 시간 제한 없음" % rel)
        ss = d.get("samples") or []
        if not ss and d.get("tc_unavailable") != "notused" and not d.get("ptype"):
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
        # 코드트리 예제는 HTML 을 잘라 만든 게 아니라 API(code_block.test_cases) 그대로라,
        # 입력이 빈 건 파싱 사고가 아니라 '입력 없는 출력 문제'다(19단 출력·한줄 출력 등
        # 실데이터 41문제). 출력이 빈 것만 의심한다.
        empty_in_ok = sub == "codetree"
        for s in ss:
            blob = (s.get("in") or "") + (s.get("out") or "")
            if "예제" in blob or "댓글" in blob or "다운로드" in blob:
                bad("%s 예제 오염" % rel)
            if (not (s.get("in") or "").strip() and not empty_in_ok) \
                    or not (s.get("out") or "").strip():
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
        # 마커는 지문에만 있는 게 아니다. SWEA B형은 그림이 전부 "예제" 절에 붙는다
        # (24992·24995·25010·25964·26416). statement 만 보면 멀쩡한 걸 경고한다.
        marked = (d.get("statement") or "") + (d.get("examples_text") or "")
        marks = set(int(m) for m in re.findall(r"\[\[IMG:(\d+)\]\]", marked))
        if marks and max(marks) > len(d.get("images") or []):
            bad("%s IMG 마커(%d)가 이미지 수(%d)보다 많음"
                % (rel, max(marks), len(d.get("images") or [])))
        if imgs and not marks:
            warn("%s 이미지는 있는데 지문·예제 어디에도 마커가 없음" % rel)
    # 문제마다 한 줄씩 찍으면 경고창이 이걸로 도배된다. 개수와 몇 개만.
    if priv_nolen:
        warn("비공개 문제 %d개가 지문 길이 0 (보관소에 지문 없음?): %s%s"
             % (len(priv_nolen), ", ".join(os.path.basename(x) for x in priv_nolen[:5]),
                " …" if len(priv_nolen) > 5 else ""))
    if stale_priv:
        warn("공개 설정(privateSites 에 없음)인데 지문 없는 비공개 형식 파일 %d개 — "
             "python _meta/crawl_codetree.py 로 다시 만들 것: %s%s"
             % (len(stale_priv), ", ".join(os.path.basename(x) for x in stale_priv[:5]),
                " …" if len(stale_priv) > 5 else ""))

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
    for f in [x for s in ("boj", "swea", "codetree")
              for x in glob.glob(os.path.join(ROOT, s, "*.py"))]:
        rel = os.path.relpath(f, ROOT).replace(os.sep, "/")
        src = io.open(f, encoding="utf-8").read()
        m = re.search(r"풀이일\s*:\s*(\d{4}-\d{2}-\d{2})", src)
        if not m:
            warn("%s 헤더에 풀이일 없음" % rel)
            continue
        day = m.group(1)
        t = re.search(r"^\s*(CT)\s+([A-Za-z0-9_-]{1,12})\s" if rel.startswith("codetree/")
                      else r"^\s*(BOJ|SWEA)\s+(\d+)\s", src, re.M)
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
                # 같은 날 같은 문제가 여러 줄인 건 정상이다 — 2026-08-14 부터
                # 제출 1회 = 1줄(attempts)로 바뀌었다. "틀림 -> 품" 이 그 예다.
                # 그래서 결과·시간·파일까지 똑같이 겹칠 때만 의심한다.
                dup = {}
                for r in rows:
                    # 제목도 넣는다 — 번호 없는 기록은 제목만 달라서, 빼면 같은 날 상태가 같은
                    # 서로 다른 문제(5월 프로그래머스 연습)가 '완전 동일' 로 잡힌다.
                    k = "%s %s|%s|%s|%s|%s회|%s|%s|%s/%s|%s" % (
                        r.get("date"), r.get("at"), r.get("site"), r.get("no"), r.get("title"),
                        r.get("try"), r.get("status"), r.get("elapsed"),
                        r.get("passed"), r.get("total"), r.get("file"))
                    dup[k] = dup.get(k, 0) + 1
                for k, c in dup.items():
                    if c > 1:
                        warn("대시보드 rows 완전 동일 %d줄: %s" % (c, k))
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

    # ── 9. 🔒 공개 금지(코드트리·TC 보관소) · 카탈로그 ───────────
    try:
        leaks, lw, _mode = leak_scan(staged=False)
        for p, r in leaks:
            bad("🔒 %s: %s" % (p, r))
        for w in lw:
            warn(w)
    except Exception as e:
        bad("🔒 공개 금지 검사 실패: %s" % str(e)[:120])
    ctn = 0
    if isinstance(ctcat, dict):
        groups = set(g.get("key") for g in (ctcat.get("groups") or []) if isinstance(g, dict))
        seen_no = set()
        for i, it in enumerate(ctcat.get("items") or []):
            if not isinstance(it, dict):
                bad("codetree_list items[%d] 가 객체가 아님" % i)
                continue
            ctn += 1
            miss = [k for k in ("no", "title", "group", "url") if not it.get(k)]
            no = str(it.get("no") or "")
            if miss:
                bad("codetree_list items[%d] (%s) 에 %s 없음" % (i, no or "?", "/".join(miss)))
            # 같은 문제가 여러 곳에 나오면 첫 번째만 items 에 두고 나머지는 also (ct_spec §4-1)
            if no and no in seen_no:
                bad("codetree_list 에 같은 번호가 두 번: %s" % no)
            seen_no.add(no)
            if no and not re.fullmatch(r"[A-Za-z0-9_-]{1,12}", no):
                bad("codetree_list 번호 형식 이상(허브가 거부함): %r" % no)
            if groups and it.get("group") and it.get("group") not in groups:
                warn("codetree_list %s 의 group(%s)이 groups 에 없음" % (no, it.get("group")))
    elif ctcat is not None:
        bad("codetree_list.json 최상위가 객체가 아님")

    # ── 결과 ─────────────────────────────────────────────────
    print("=" * 66)
    print(" 자체 점검 — 문제자료 %d / history %d일 / 색인 %d / SWEA매핑 %d / 코드트리 %d"
          % (len(probs), len(hist), len(items), len(ids), ctn))
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
