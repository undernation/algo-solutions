"""
로컬 허브 서버 — 채점 + repo 저장/커밋/푸시

GitHub Pages 대시보드(https)와 코딩살구클럽(https) 양쪽에서
http://localhost:12014 를 직접 호출한다.
(크롬은 localhost 를 안전한 출처로 취급하므로 mixed-content 차단이 없다.)

실행:
    python judge/server.py
    python judge/server.py --port 12014 --no-push
    python judge/server.py --runner /opt/pypy3.9-v7.3.9-linux64/bin/pypy3
    python judge/server.py --no-push --sync-url http://127.0.0.1:12099   # 동기화 대상 지정(테스트)

제출 코드는 PyPy 로 실행한다(있으면 자동 탐색). 백준·코딩살구의 시간 제한이
사실상 C++/PyPy 기준이라, CPython 으로 채점하면 실제 제출 결과와 어긋난다.
서버 자신과 크롤러·빌더는 계속 CPython 을 쓴다(playwright 의존).

엔드포인트
    GET  /            서버 상태 (대시보드가 살아있는지 확인용)
    POST /judge       코딩살구 호환 채점  {sourceCode, testCases, ...}
    POST /run         임의 코드 + 케이스 채점  {code, cases:[{in,out}]}
    POST /save        풀이 저장 + git commit/push
    POST /fetch       문제 크롤링 (fetch_problem.py 위임)
    POST /tc          보관된 전체 테스트케이스 정보/미리보기 {site, no, index?}
    POST /tcupload    전체 테스트케이스 업로드 {site, no, samples, private, problem?}
    POST /prob        보관소의 지문·예제 {site, no}  — 비공개 사이트(privateSites)는 여기서만 나온다
    POST /note        복기 메모 저장 {site, no, date, status, body, mode}
    POST /delete      풀이기록/문제자료 삭제 {kind, site, no, date?}
    POST /toolinfo    배포용 도구 파일 정보 {name?}
    POST /tool        배포용 도구 파일 내려받기 {name?}  → zip 바이트
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
import os, re, io, sys, json, glob, time, subprocess, tempfile, argparse, datetime, threading
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
PY_MULT = 2.0          # PyPy 가 C++ 기준 제한 대비 받는 배수 (정책값 — 아래 설명)
PY_ADD = 1.0           # 가산 초
NATIVE_MARGIN = 1.5    # 언어별 제한이 명시된 문제(SWEA)에 줄 여유 — 아래 설명
BENCH_REF = 1.0        # 기준 기기의 _bench.py 합계(초)
BENCH_FILE = os.path.join(os.path.expanduser("~"), ".algo-hub-bench")
CONFIG_FILE = os.path.join(ROOT, "_meta", "judge_config.json")
SPEED = 1.0


def load_config():
    """_meta/judge_config.json 에서 pyMult/pyAdd/machineFactor 를 읽는다.

    ⚠️ pyMult/pyAdd 는 '백준이 이렇게 준다'는 확인된 사실이 아니다.
       코딩살구는 언어별 추가시간을 제공하지 않고(C++ 단일 기준),
       백준 본 사이트는 서비스 종료라 공식 배수를 확인할 수 없었다.
       이 채점기의 정책값이므로 설정 파일에서 자유롭게 바꾼다.
    privateSites(PRIVATE_SITES)도 여기서 다시 읽는다 — 못 읽으면 {"CT"}.
    """
    global PY_MULT, PY_ADD, NATIVE_MARGIN, PRIVATE_SITES
    PRIVATE_SITES = load_private_sites()
    fixed = None
    if os.path.exists(CONFIG_FILE):
        try:
            c = json.load(io.open(CONFIG_FILE, encoding="utf-8"))
            PY_MULT = float(c.get("pyMult", PY_MULT))
            PY_ADD = float(c.get("pyAdd", PY_ADD))
            NATIVE_MARGIN = float(c.get("nativeMargin", NATIVE_MARGIN))
            mf = c.get("machineFactor")
            fixed = float(mf) if mf not in (None, "", False) else None
        except Exception as e:
            log("⚠️ judge_config.json 읽기 실패:", str(e)[:120])
    return fixed


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


def allowed_time(limit_sec, lang_adjusted=False, margin=None):
    """문제 제한(초) -> 이 기기에서 허용할 실행시간(초).

    lang_adjusted=True 면 그 제한이 이미 Python/PyPy 기준이라는 뜻이다
    (예: SWEA 의 "Python의 경우 10초"). 이때는 언어 보정을 다시 적용하지 않고
    기기 속도 보정만 곱한다. 안 그러면 10초 문제에 46초를 주게 된다.
    """
    try:
        t = float(limit_sec or 0)
    except (TypeError, ValueError):
        t = 0.0
    if t <= 0:
        t = 2.0
    # 언어별 제한이 명시된 문제(SWEA "Python의 경우 N초")라도 그 N 은 SWEA 채점기
    # 기준이다. 이 VM 은 그보다 느려서, SWEA 에서 정답 처리된 코드가 여기서만
    # 시간초과로 잡히는 일이 실제로 있었다.
    #   SWEA 24703 어항물채우기 — 제한 8초 / 이 VM 의 pypy3 로 10.31초
    # 그래서 여유를 곱한다. _bench.py 는 이 워크로드를 대변하지 못한다
    # (에라토스테네스·루프 위주라 VM 이 오히려 빠르게 나와 보정이 1.0 으로 깎였다).
    # margin 을 주면 그 값을 쓴다(대시보드에서 채점할 때 조절). 0.5~5 로 묶는다.
    nm = NATIVE_MARGIN
    if margin is not None:
        try:
            nm = min(5.0, max(0.5, float(margin)))
        except (TypeError, ValueError):
            nm = NATIVE_MARGIN
    base = t * nm if lang_adjusted else (t * PY_MULT + PY_ADD)
    return round(base * SPEED, 1)


def uses_total_time(site, no, body=None):
    """이 문제의 시간 제한이 '전 케이스 합계' 기준인가.

    근거는 크롤링해 둔 문제 원문이다. SWEA 는 limits.time 에
        "10개 테스트케이스를 합쳐서 C++의 경우 10초 / Java 20초 / Python 30초"
    처럼 적혀 있다. BOJ/코딩살구는 데이터 파일 하나마다라 해당 없음.
    브라우저가 보낸 값을 그대로 믿지 않고 서버가 원문으로 판단한다
    (클라이언트만 고쳐도 채점 기준이 흔들리면 안 되므로).
    """
    if body is not None and body.get("totalTime") is not None:
        return bool(body["totalTime"])
    # site·no 가 이상하면(경로 조작) 원문을 읽지 않고 '못 찾음'과 똑같이 사이트 관례로 간다.
    # SUB·site_no_error 는 아래에서 정의된다(호출 시점엔 존재).
    if not site_no_error(site, no):
        f = os.path.join(ROOT, "problems", SUB[site], "%s.json" % no)
        try:
            d = json.load(io.open(f, encoding="utf-8"))
            t = str(((d.get("limits") or {}).get("time")) or "")
            if "합쳐서" in t or "합산" in t:
                return True
        except Exception:
            pass
    # 원문을 못 찾으면 사이트 관례를 따른다. SWEA 는 합계가 기본이다.
    return site == "SWEA"


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
NO_RE = re.compile(r"[A-Za-z0-9_-]{1,12}")      # 문제 번호 — 파일 이름(<no>.json·<no>.md·<no>_*.py)에 그대로 들어간다


def site_no_error(site, no):
    """경로에 들어갈 site·no 검사. 이상하면 오류 응답(dict), 괜찮으면 None.

    no 는 파일 이름으로, site 는 SUB 를 거쳐 폴더 이름으로 그대로 들어간다. 예전엔
    tc_upload·save_solution 만 번호를 검사하고 나머지는 그냥 경로를 만들어서,
    no="../../x" 로 보관소 밖의 아무 .json 이나 읽혔다(/tc·/tcfile·/judge 의 useStoredTC,
    2026-09-23 확인). 같은 식으로 /note 는 notes/ 밖에 .md 를 쓰고, /delete 는
    problems/<sub>/ 밖의 .json 을 지울 수 있었다. 토큰 뒤라 나만 쓸 수 있지만 막는다.
    site 도 모르는 값이면 예전엔 조용히 boj 폴더를 썼다.
    """
    if site not in SUB:
        return {"ok": False, "error": "알 수 없는 사이트입니다"}
    if not NO_RE.fullmatch(str(no or "")):
        return {"ok": False, "error": "문제 번호가 이상합니다"}
    return None


def _inside(path, base):
    """path 가 base 폴더 '아래'에 있나(base 자체는 아님).

    '..'·절대경로·다른 드라이브로 빠져나가는 것을 막는다. 대소문자·심볼릭 링크를
    정리한 실제 경로끼리 비교한다(Windows 는 C:\\A 와 c:\\a 가 같다).
    """
    p = os.path.normcase(os.path.realpath(path))
    b = os.path.normcase(os.path.realpath(base))
    try:
        return p != b and os.path.commonpath([p, b]) == b
    except ValueError:                 # Windows 에서 드라이브가 다르면
        return False

# 지문·예제를 저장물에서 제외할지 여부. 사용자 결정(2026-08-11)으로 기본 OFF —
# 지문·예제 입출력·테스트케이스를 그대로 커밋한다.
# 나중에 비공개로 돌리고 싶으면 True 로만 바꾸면 된다.
PUBLIC_SAFE = False
REDACT = ("statement", "samples", "testcases", "private_testcases",
          "description", "input_desc", "output_desc", "html",
          "input_spec", "output_spec")

# 🔒 지문을 repo 에 쓰지 않는 사이트 — 스위치는 한 곳, _meta/judge_config.json 의 "privateSites".
# 비공개 사이트는 PUBLIC_SAFE 와 상관없이 지문·입출력 설명·제약·힌트·예제를 repo 에 넣지 않고
# (풀이 파일 헤더의 [문제]/[예제]/제약 줄, problems/<sub>/<no>.json 둘 다) TC 보관소(git 밖)에만
# 둔다 — 내 PC 는 _meta/tc_store/(gitignore), 클라우드 VM 은 ~/algo-tc/. 대시보드는 토큰이
# 있을 때 POST /prob 로 받아 그린다.
# 2026-09-23 코드트리를 붙이며 처음엔 여기 {"CT"} 로 박았다(트레일은 유료 콘텐츠). 같은 날
# 소유자가 위험(재배포 → DMCA 로 repo·Pages 삭제·계정 정지)을 알고도 BOJ/SWEA 처럼 공개 저장하기로
# 해서 설정값(지금 [])으로 옮겼다. 크롤러(crawl_codetree.load_private_sites)·selfcheck·훅도 같은 값을 본다.
# 파일·키를 못 읽으면 {"CT"}(비공개)로 넘어진다 — 설정 사고로 유료 지문이 새는 쪽으로 넘어지지 않게.
# import 시점에 읽는다(main() 없이 쓰는 테스트·도구도 같은 값을 보게). load_config() 가 다시 읽는다.
# ⚠️ 비공개로 되돌려도 이미 push 된 지문은 히스토리·포크·캐시에 남는다(2026-08-12 재작성 참고).
PRIVATE_WHY = ""        # 설정을 못 읽어 {"CT"} 로 넘어졌으면 그 이유(시작 로그에 찍는다)


def load_private_sites():
    """judge_config.json 의 privateSites → {"CT", ...}. 못 읽으면 {"CT"}(fail-closed)."""
    global PRIVATE_WHY
    try:
        with io.open(CONFIG_FILE, encoding="utf-8") as f:
            v = json.load(f)["privateSites"]
        if not isinstance(v, list):
            raise ValueError("privateSites 가 목록이 아님")
        PRIVATE_WHY = ""
        return set(str(x).strip().upper() for x in v if str(x).strip())
    except Exception as e:
        PRIVATE_WHY = "%s: %s" % (type(e).__name__, str(e)[:80])
        return {"CT"}


PRIVATE_SITES = load_private_sites()
# 문제 JSON(problems/<sub>/<no>.json)을 크롤러가 관리하는 사이트 — 공개/비공개와 상관없이
# /save 가 이미 있는 파일을 덮지 않는다(크롤러가 채운 트레일·출처·한도가 날아가지 않게).
KEEP_PROBLEM_FILE = {"CT"}
# 공개 여부와 상관없이 저장하지 않는 키 — 기출의 유형 태그·선수 레슨(유형 스포 금지), 내 진행상태.
SPOILER_KEYS = ("tags", "prerequisite_lessons", "progress_status")
# 비공개 사이트에서 빼는 키. 코드트리는 제약·힌트까지 마크다운 원문(저작물)이라 REDACT 보다 넓다.
# input_format/output_format/code_block 은 코드트리 API 원본 이름이다 — 원본 dict 가 그대로
# 흘러들어와도 걸러지게 같이 둔다(code_block 안에 test_cases 가 통째로 들어 있다).
# tags·prerequisite_lessons 는 유형 스포(사용자 규칙), progress_status 는 내 진행상태라 뺀다.
PRIVATE_REDACT = REDACT + (
    "constraints", "hint", "sample_notes", "problem", "examples_text", "samples_raw",
    "input_format", "output_format", "code_block", "tc_preview") + SPOILER_KEYS
# 보관소 파일의 "problem" 에 담기는 필드(계약: _meta/tc_store/<sub>/<no>.json)
PRIVATE_PROBLEM_KEYS = ("title", "statement", "input_spec", "output_spec",
                        "constraints", "hint", "sample_notes")


def is_private(site):
    """지문을 repo 에 쓰면 안 되는 사이트인가.

    대시보드·크롤러가 "ct" 처럼 소문자로 보내도 새지 않게 여기서 정규화한다
    (build_header 는 요청의 site 를 대문자로 바꾸지 않고 그대로 쓴다).
    """
    return str(site or "").strip().upper() in PRIVATE_SITES


def redact_private(prob):
    """비공개 사이트용 공개 사본 — 메타데이터만 남기고 예제 수·지문 길이만 적어 둔다."""
    if not isinstance(prob, dict):
        return {"private_content": True}
    out = {k: v for k, v in prob.items() if k not in PRIVATE_REDACT}
    smp = prob.get("samples")
    if isinstance(smp, list) and smp:
        out["sample_count"] = len(smp)
    st = prob.get("statement")
    if isinstance(st, str) and st.strip():
        out["statement_len"] = len(st)
    out["private_content"] = True
    return out


def redact(prob, site=None):
    """공개 저장용으로 저작물 부분을 제거한 사본.

    비공개 사이트(PRIVATE_SITES)는 PUBLIC_SAFE 와 상관없이 항상 걸러낸다.
    요청의 site 와 문제 dict 의 site 중 하나라도 비공개면 비공개로 본다.
    """
    if not prob:
        return prob
    if is_private(site) or (isinstance(prob, dict) and is_private(prob.get("site"))):
        return redact_private(prob)
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


def slog(*a):
    """보안 관련 기록 — --quiet 여도 남긴다.

    누가 무엇을 받아 갔는지, 인증이 몇 번 틀렸는지는 조용해지면 안 되는 정보다.
    서비스가 --quiet 로 떠 있어서 한동안 이게 통째로 비어 있었다.
    토큰·비밀번호·파일 내용은 여기에도 남기지 않는다.
    """
    print(*a, flush=True)


KST = datetime.timezone(datetime.timedelta(hours=9))


def today_kst():
    """오늘 날짜(KST). 클라우드 VM 은 UTC 라 새벽 0~9시에 하루 밀린다."""
    return datetime.datetime.now(KST).date().isoformat()


def now_kst_time():
    """제출 시각(KST) "HH:MM:SS". 같은 날 여러 번 제출해도 순서를 알 수 있게.

    예전엔 날짜만 남겨서 하루 안에서는 정렬이 불가능했다(최근 제출 순서가 뒤죽박죽).
    밀리초까지는 필요 없어 초 단위로 둔다.
    """
    return datetime.datetime.now(KST).strftime("%H:%M:%S")


def iso_now():
    return (datetime.datetime.now(datetime.timezone.utc)
            .isoformat(timespec="milliseconds").replace("+00:00", "Z"))


# ══════════════════════════════════════════════════════════════
# 채점
# ══════════════════════════════════════════════════════════════
def norm(s):
    return "\n".join(l.rstrip() for l in (s or "").replace("\r\n", "\n").split("\n")).rstrip()


NUM = re.compile(r"^[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?$")
INT = re.compile(r"^[+-]?\d+$")
EPS_ABS, EPS_REL = 1e-9, 1e-6


def same(got, want):
    """정답 비교. 문자열이 같으면 통과.

    다르면 토큰 단위로 보되, **정답 토큰이 실수**(소수점·지수 표기)일 때만 허용오차
    안이면 같다고 본다. 실수를 출력하는 문제(예: BOJ 1344 축구 → 0.5265618908306351)를
    정확일치로만 보면 맞는 풀이가 오답으로 찍힌다.

    🚩 정답 토큰이 정수면 오차를 주지 않는다(2026-09-23 수정). 예전엔 정수에도 상대오차
    1e-6 을 적용해서, 답이 100만 이상이면 ±1 틀린 답이 '맞았습니다'로 나갔다
    (1000001 vs 1000000 → 통과, 123456789013 vs 123456789012 → 통과). 원래 주석은
    "정수만 있는 출력은 문자열 비교와 동일하게 동작한다"였는데 사실이 아니었다 —
    코드트리 생성 TC 도구를 시험하다 일부러 틀린 풀이가 통과해서 드러났다.
    """
    g, w = norm(got), norm(want)
    if g == w:
        return True
    gt, wt = g.split(), w.split()
    if not gt or len(gt) != len(wt):
        return False
    saw_float = False
    for a, b in zip(gt, wt):
        if a == b:
            continue
        if not (NUM.match(a) and NUM.match(b)):
            return False
        if INT.match(b):             # 정답이 정수인데 글자가 다르면 그냥 오답
            return False
        try:
            fa, fb = float(a), float(b)
        except ValueError:
            return False
        if abs(fa - fb) > max(EPS_ABS, EPS_REL * abs(fb)):
            return False
        saw_float = True
    # 실수 오차 때문에 다른 경우에만 통과시킨다. 줄바꿈/공백 배치만 다른 출력은
    # 예전처럼 오답으로 둔다(느슨해지면 형식 실수를 못 잡는다).
    return saw_float


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


def scratch_run(src, stdin_data, tl):
    """연습장 실행 — 정답 대조 없이 코드를 돌려 출력만 돌려준다.

    /judge·/run 은 기대출력과 비교해 '틀렸습니다'로 표시하므로, 그냥 찍어보고
    싶을 때 쓰기 불편했다. 여기서는 stdout/stderr 를 그대로 보여준다.
    """
    if not (src or "").strip():
        return {"ok": False, "error": "빈 코드"}
    err = syntax_error(src)
    if err:
        return {"ok": True, "status": "compile_error", "stdout": "",
                "stderr": err, "elapsed": 0.0, "runner": RUNNER_NAME}
    t = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8")
    t.write(src)
    t.close()
    try:
        st, out, el, se = run_one(t.name, stdin_data or "", tl)
    finally:
        try:
            os.unlink(t.name)
        except OSError:
            pass
    cap = 20000                      # 무한 출력 루프가 브라우저를 죽이지 않게
    trimmed = len(out) > cap
    return {"ok": True, "status": st, "stdout": out[:cap], "truncated": trimmed,
            "outBytes": len(out), "stderr": (se or "")[:4000],
            "elapsed": round(el, 3), "allowedTime": round(tl, 2),
            "runner": RUNNER_NAME}


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


def judge(src, cases, pub=0, tl=5.0, total_time=False):
    """total_time=True 면 제한을 '전 케이스 합계'에 건다(SWEA 방식).

    SWEA 는 문제에 "10개 테스트케이스를 **합쳐서** Python 30초" 처럼 적혀 있어
    케이스마다 30초를 주면 실제 채점보다 10배 후해진다.
    BOJ/코딩살구는 데이터 파일 하나마다 제한이 걸리므로 기본값은 False.
    """
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
            # 합계 방식이면 남은 예산만큼만 준다. 한 케이스가 예산을 다 쓰면
            # 그 자리에서 시간초과가 나고, 뒤 케이스는 0초라 바로 끊긴다.
            budget = max(tl - tot_el, 0.0) if total_time else tl
            if total_time and budget <= 0:
                st, got, el, err = "time_limit_exceeded", "", 0.0, ""
            else:
                st, got, el, err = run_one(tmp.name, din, budget)
            tot_el += el
            kind = "public" if i < pub else "private"
            if total_time and st == "ok" and tot_el > tl:
                st = "time_limit_exceeded"      # 합계가 제한을 넘긴 순간 탈락
            if st == "ok" and same(got, want):
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
    # allowedTime: 케이스 하나에 허용한 시간(합계 방식이면 전체 예산).
    # 대시보드가 "최대 x초 / 허용 y초"로 보여준다. elapsedSec 는 전 케이스 합계라
    # 케이스별 방식에서 이것만 띄우면 제한을 넘긴 것처럼 보인다.
    return {"ok": True, "verdict": verdict, "allowedTime": tl,
            "totalTime": bool(total_time),
            "summary": {"passed": passed, "total": len(cases),
                        "firstFailedIndex": first_fail},
            "judgedAt": iso_now(), "elapsedSec": round(tot_el, 3), "detail": detail}


# ══════════════════════════════════════════════════════════════
# repo 저장
# ══════════════════════════════════════════════════════════════
def git(*args, check=False):
    # 서버에는 붙은 터미널이 없다. rebase --continue 등이 에디터를 열면 그대로 멈춘다.
    env = {**os.environ, "GIT_EDITOR": "true", "GIT_TERMINAL_PROMPT": "0"}
    r = subprocess.run(["git"] + list(args), cwd=ROOT, env=env,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout or "")[:400])
    return r


HIST_REL = "_meta/history.json"


def sync_before_write():
    """저장을 시작하기 전에 원격을 따라잡는다.

    예전엔 커밋한 뒤에야 push 가 거절되는 걸 알고 rebase 를 시도했는데,
    history.json 이 충돌해 rebase --abort 로 끝나면서 저장이 통째로
    GitHub 에 안 올라갔다(로컬엔 남아 사용자는 성공한 줄 안다).
    작업트리가 깨끗할 때 미리 당겨두면 대부분의 분기를 예방한다.
    """
    if git("status", "--porcelain").stdout.strip():
        return False                       # 뭔가 작업 중 — 건드리지 않는다
    git("fetch", "origin")
    return git("merge", "--ff-only", "origin/master").returncode == 0


def union_history(ours_text, theirs_text):
    """충돌한 history.json 두 벌을 (날짜 → (site,no)) 합집합으로 합친다.

    한쪽을 버리면 다른 PC 에서 올린 기록이 사라진다. 항목이 더 많은(=정보가
    더 붙은) 쪽을 남기고, 없는 것은 그대로 가져온다.
    """
    a = json.loads(ours_text or "{}")
    b = json.loads(theirs_text or "{}")
    out = dict(a)
    for day, v in b.items():
        cur = out.setdefault(day, {"count": 0, "items": []})
        seen = {}
        order = []
        for it in list(cur.get("items") or []) + list(v.get("items") or []):
            k = it if isinstance(it, str) else "%s/%s" % (it.get("site"), it.get("no"))
            if k not in seen:
                seen[k] = it
                order.append(k)
            elif isinstance(it, dict) and isinstance(seen[k], dict):
                merged = dict(seen[k])
                for kk, vv in it.items():
                    if vv and not merged.get(kk):
                        merged[kk] = vv
                seen[k] = merged
        cur["items"] = [seen[k] for k in order]
        cur["count"] = max(len(cur["items"]), cur.get("count", 0), v.get("count", 0))
    return json.dumps({k: out[k] for k in sorted(out)},
                      ensure_ascii=False, indent=1, sort_keys=True)


def resolve_conflicts():
    """rebase 충돌을 자동 해소한다. 해소 못 하면 False.

    history.json 만 합쳐 주면 된다. index.html·잔디 등 나머지 생성물은
    .gitattributes 의 merge=ours 로 이미 자동 해결된다.
    """
    bad = [x for x in git("diff", "--name-only", "--diff-filter=U").stdout.split("\n") if x.strip()]
    if not bad:
        return True
    if bad != [HIST_REL]:
        log("   ⚠️ 자동 해소 불가한 충돌:", ", ".join(bad)[:200])
        return False
    try:
        ours = git("show", ":2:" + HIST_REL).stdout
        theirs = git("show", ":3:" + HIST_REL).stdout
        io.open(os.path.join(ROOT, HIST_REL), "w", encoding="utf-8",
                newline="").write(union_history(ours, theirs))
        git("add", HIST_REL)
        log("   ♻️ history.json 충돌을 합집합으로 해소")
        return True
    except Exception as e:
        log("   ⚠️ history 병합 실패:", str(e)[:160])
        return False


def safe(s, n=40):
    return re.sub(r"[\\/:*?\"<>|]+", "_", re.sub(r"\s+", "", s or ""))[:n]


def build_header(d, verdict=None):
    site, no, title = d.get("site", "BOJ"), str(d.get("no", "")), d.get("title", "")
    L = [("%s %s  %s" % (site, no, title)).rstrip()]
    if d.get("url"):
        L.append(d["url"])
    L.append("")
    L.append("풀이일 : %s   결과: %s" % (d.get("date") or today_kst(),
                                     d.get("status") or "품"))
    p = d.get("problem") if isinstance(d.get("problem"), dict) else {}
    # 🔒 비공개 사이트(코드트리)는 풀이 파일도 public repo 에 커밋되므로 지문·예제·제약을
    #    헤더에 넣지 않는다. 브라우저가 실수로 지문을 실어 보내도 여기서 걸러진다.
    priv = is_private(site) or is_private(p.get("site"))
    lim = p.get("limits") or {}
    if lim:
        L.append("한도   : " + " / ".join("%s %s" % (k, v) for k, v in lim.items()))
    if p.get("level") or (p.get("stats") or {}).get("accept_rate"):
        L.append("난이도 : %s  |  정답률 %s%%" % (p.get("level", "?"),
                                             (p.get("stats") or {}).get("accept_rate", "?")))
    # 제약: BOJ/SWEA 는 줄 목록인데 코드트리는 마크다운 문자열 한 덩어리다. 문자열을 그대로
    # 돌리면 앞 6'글자'가 한 줄씩 찍힌다(옛 서버로 확인) — 줄로 나눠 빈 줄을 뺀 앞 6줄만 쓴다.
    # 비공개 사이트는 통째로 뺀다.
    cons = [] if priv else (p.get("constraints") or [])
    if isinstance(cons, str):
        cons = [x.strip() for x in cons.splitlines() if x.strip()]
    for c in cons[:6]:
        L.append("제약   : " + c)
    if d.get("tags"):
        L.append("분류   : " + ", ".join(d["tags"]))
    if verdict:
        s = verdict.get("summary") or {}
        L.append("")
        L.append("[채점] %s  %s/%s  (%ss)" % (verdict.get("verdict"), s.get("passed"),
                                            s.get("total"), verdict.get("elapsedSec")))
    if priv:
        ps = str(site if is_private(site) else p.get("site")).strip().upper()
        L += ["", "[문제] %s 지문은 비공개(허브 보관) — 위 URL 참조" % SITE_NAME.get(ps, ps)]
    elif PUBLIC_SAFE:
        if p.get("statement") or p.get("samples"):
            L += ["", "[문제] 지문·예제는 저작권상 저장하지 않음 — 위 URL 참조"]
    else:
        # 지문·예제만 넣는다. 힌트(코드트리 hint)는 공개 모드여도 넣지 않는다 —
        # 다시 풀 때 파일을 열면 풀이 방향이 바로 보이는 스포다.
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
    # 번호·제목이 둘 다 없으면 boj/.py 같은 이름 없는 파일이 만들어져 커밋된다.
    if not no and not (title or "").strip():
        return {"ok": False, "error": "문제 번호나 제목이 필요합니다"}
    if no and not re.fullmatch(r"[A-Za-z0-9_-]{1,12}", no):
        return {"ok": False, "error": "문제 번호 형식이 이상합니다: %r" % no[:20]}

    # 쓰기 전에 원격을 따라잡아 둔다(분기 예방). 실패해도 저장은 계속한다.
    if AUTO_PUSH:
        sync_before_write()

    name = no if (sub == "boj" and no) else ("%s_%s" % (no, safe(title)) if no else safe(title))
    rel = "%s/%s.py" % (sub, name)
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # 헤더를 먼저 만든다. open(...,"w") 안에서 만들다 예외가 나면 기존 풀이 파일이
    # 빈 파일로 잘린 채 남는다(open 이 인자보다 먼저 평가된다).
    text = build_header(d, d.get("verdict")) + code.rstrip() + "\n"
    io.open(path, "w", encoding="utf-8", newline="").write(text)

    # 문제 메타 별도 저장
    prob = d.get("problem")
    if prob:
        priv = is_private(site) or (isinstance(prob, dict) and is_private(prob.get("site")))
        own = priv or site in KEEP_PROBLEM_FILE
        pj = os.path.join(ROOT, "problems", sub, "%s.json" % (no or safe(title)))
        # 코드트리는 문제 JSON 을 크롤러가 관리한다(트레일·출처·한도 …). 이미 있으면 덮지 않는다 —
        # 브라우저가 보낸 dict 로 덮으면 크롤러가 채운 필드가 날아가거나, 비공개 모드면 빼먹은
        # 비공개 필드가 섞여 커밋될 수 있다. 없을 때만 새로 만든다(대시보드가 문제 페이지를 열 수 있게).
        # 비공개면 공개 필드만(redact), 공개면 그대로 — 유형 태그·진행상태는 어느 쪽이든 뺀다.
        if not (own and os.path.exists(pj)):
            pub = redact(prob, site)
            if own and isinstance(pub, dict):
                pub = {k: v for k, v in pub.items() if k not in SPOILER_KEYS}
                for k, v in (("site", site), ("platform", SITE_NAME.get(site, site)),
                             ("no", no), ("title", title), ("url", d.get("url") or "")):
                    if v and not pub.get(k):
                        pub[k] = v
            os.makedirs(os.path.dirname(pj), exist_ok=True)
            io.open(pj, "w", encoding="utf-8", newline="").write(
                json.dumps(pub, ensure_ascii=False, indent=1))

    # history.json 에 직접 기록.
    # 예전엔 build_heatmap 이 .py 헤더의 '풀이일' 을 긁는 것에만 의존했는데,
    # 같은 날 다른 기록이 있으면 병합에서 밀려 사라졌다. 여기서 확실히 남긴다.
    at = now_kst_time()          # try 안에서 만들면 예외 시 아래 return 에서 터진다
    # 지웠던 기록을 같은 날 다시 저장하면 삭제 표식을 걷어낸다.
    # 안 그러면 build_heatmap 의 apply_tombstones 가 매번 지워서 영영 안 뜬다
    # (실제로 이것 때문에 저장은 성공하는데 목록에 안 나타났다).
    try:
        tp = os.path.join(ROOT, "_meta", "deleted.json")
        if os.path.exists(tp):
            tomb = json.load(io.open(tp, encoding="utf-8")) or []
            k = "%s|%s|%s" % (d.get("date") or today_kst(), site, no)
            if k in tomb:
                tomb = [x for x in tomb if x != k]
                io.open(tp, "w", encoding="utf-8", newline="").write(
                    json.dumps(sorted(tomb), ensure_ascii=False, indent=1))
                log("   ♻️ 삭제 표식 해제 %s" % k)
    except Exception as e:
        log("   ⚠️ 삭제 표식 해제 실패:", str(e)[:120])
    try:
        hp = os.path.join(ROOT, "_meta", "history.json")
        hist = json.load(io.open(hp, encoding="utf-8")) if os.path.exists(hp) else {}
        day = d.get("date") or today_kst()
        rec = hist.setdefault(day, {"count": 0, "items": []})
        item = {"site": site, "no": no, "title": title,
                "status": d.get("status") or "품", "file": rel,
                "at": at}
        # 채점 결과(통과 수 / 전체, 소요 시간)를 제출 기록에 남긴다.
        v = d.get("verdict") or {}
        if v:
            sm = v.get("summary") or {}
            item["verdict"] = v.get("verdict") or ""
            if sm.get("total") is not None:
                item["passed"] = sm.get("passed")
                item["total"] = sm.get("total")
            if v.get("elapsedSec") is not None:
                item["elapsed"] = v.get("elapsedSec")
        # 같은 날 같은 문제를 다시 내면 기록은 하나로 묶되, 제출마다 attempts 에 쌓는다.
        # 예전엔 이전 기록을 지우고 새로 넣어서 "틀림 → 다시 풀어 품" 의 앞부분이
        # 흔적 없이 사라졌다(잔디 count 는 '그날 시도한 문제 수'라 묶음은 유지해야 한다).
        prev = None
        for x in rec["items"]:
            if isinstance(x, dict) and x.get("site") == site and str(x.get("no")) == no:
                prev = x
                break
        att = {"at": at, "status": item["status"], "file": rel}
        for k in ("verdict", "passed", "total", "elapsed"):
            if item.get(k) is not None:
                att[k] = item[k]
        if prev is None:
            item["attempts"] = [att]
            rec["items"].append(item)
        else:
            # ⚠️ 이름을 hist 로 두지 말 것 — 바깥의 history 딕셔너리를 가려서
            #    history.json 을 attempts 배열로 통째로 덮어쓴다(실제로 겪음).
            tries = [a for a in (prev.get("attempts") or []) if isinstance(a, dict)]
            if not tries:
                # attempts 가 없던 옛 기록이면 지금 내용을 1회차로 되살려 둔다.
                old = {k: prev[k] for k in ("at", "status", "file", "verdict",
                                            "passed", "total", "elapsed")
                       if prev.get(k) is not None}
                if old:
                    tries.append(old)
            tries.append(att)
            prev.update(item)          # 문제 대표값은 가장 최근 제출로
            prev["attempts"] = tries
        # count 는 '문제 수'다. items 는 문제당 하나이므로 길이가 곧 문제 수.
        rec["count"] = max(len(rec["items"]), rec.get("count", 0))
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
    guard_private_staged()
    c = git("commit", "-m", msg)
    committed = c.returncode == 0
    pushed, perr = False, ""
    if committed and AUTO_PUSH:
        p = git("push")
        pushed = p.returncode == 0
        if not pushed:
            # 다른 PC·Actions 가 먼저 올렸으면 non-fast-forward 로 거절된다.
            # fetch 후 rebase 하고 재시도한다. history.json 은 충돌이 잦아
            # (양쪽이 파일 전체를 다시 쓴다) 자동으로 합집합 병합한다.
            log("   ↻ push 거절 — rebase 후 재시도")
            git("fetch", "origin")
            rb = git("rebase", "origin/master")
            for _ in range(6):             # 밀린 커밋이 여럿일 수 있다
                if rb.returncode == 0:
                    break
                if not resolve_conflicts():
                    break
                rb = git("rebase", "--continue")
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
    return {"ok": True, "file": rel, "message": msg, "at": at,
            "committed": committed, "pushed": pushed, "pushError": perr,
            "commitError": commit_error(c),
            "stdout": (c.stdout or "")[-300:] if not committed else ""}


def note_path(site, no):
    # 쓰는 경로라 여기서 막는다 — 예전엔 no="../../x" 면 notes/ 밖에 .md 를 쓰고
    # 그대로 git add -A 로 커밋까지 했다. 호출하는 쪽이 검사를 빼먹어도 밖으로 못 나간다.
    if site_no_error(site, no):
        raise ValueError("메모 경로 키가 이상합니다: %r / %r" % (site, str(no)[:20]))
    return os.path.join(ROOT, "notes", SUB[site], "%s.md" % no)


def read_note(site, no):
    if site_no_error(site, no):
        return ""
    p = note_path(site, no)
    return io.open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def save_note(d):
    """복기 메모 저장. 실수노트와 같은 구조로 날짜별 항목을 쌓는다.

        ## BOJ 2618 경찰차
        #### 2026-08-12 (틀림)
        본문…
        #### 2026-08-13 (품)
        본문…

    mode="append"(기본)  같은 날짜 항목이 있으면 그 본문을 교체, 없으면 뒤에 추가
    mode="replace"       파일 전체를 body 로 덮어씀(직접 편집용)
    """
    site = (d.get("site") or "BOJ").upper()
    no = str(d.get("no") or "").strip()
    body = (d.get("body") or "").rstrip()
    if not no:
        return {"ok": False, "error": "no 가 필요합니다"}
    err = site_no_error(site, no)
    if err:
        return err
    mode = d.get("mode") or "append"
    date = (d.get("date") or today_kst()).strip()
    status = (d.get("status") or "").strip()
    title = (d.get("title") or "").strip()

    p = note_path(site, no)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    cur = read_note(site, no)

    if mode == "replace":
        text = body + "\n"
    else:
        head = ("## %s %s %s" % (site, no, title)).rstrip()
        if not cur.strip():
            cur = head + "\n"
        elif not cur.lstrip().startswith("##"):
            cur = head + "\n\n" + cur
        hdr = "#### %s%s" % (date, (" (%s)" % status) if status else "")
        # 같은 날짜 항목이 이미 있으면 그 구간만 교체
        pat = re.compile(r"(?m)^####\s*" + re.escape(date) + r"[^\n]*\n")
        m = pat.search(cur)
        if m:
            nxt = re.compile(r"(?m)^####\s").search(cur, m.end())
            end = nxt.start() if nxt else len(cur)
            cur = cur[:m.start()] + hdr + "\n" + body + "\n\n" + cur[end:]
        else:
            cur = cur.rstrip() + "\n\n" + hdr + "\n" + body + "\n"
        text = re.sub(r"\n{4,}", "\n\n\n", cur).rstrip() + "\n"

    if not body.strip() and mode == "append":
        return {"ok": False, "error": "메모 내용이 비어 있습니다"}

    io.open(p, "w", encoding="utf-8", newline="").write(text)
    rel = os.path.relpath(p, ROOT).replace(os.sep, "/")

    # 🚩 메모에도 상태(품/못품/틀림)가 들어간다. build_heatmap 은 실수노트·메모를
    #    읽어 잔디와 대시보드(index.html)를 만들므로, 메모만 저장하고 빌드를 건너뛰면
    #    사이트에 반영되지 않는다(2026-08-29 발견 — 그전 메모 커밋 10건이 전부
    #    index.html 을 안 건드렸다). /save 와 똑같이 세 빌드를 모두 돌린다.
    for s in ("_meta/build_probindex.py", "_meta/build_heatmap.py", "_meta/build_index.py"):
        subprocess.run([PY, s], cwd=ROOT, capture_output=True,
                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    git("add", "-A")
    guard_private_staged()
    c = git("commit", "-m", "[메모] %s %s %s" % (site, no, date))
    committed = c.returncode == 0
    pushed, perr = False, ""
    if committed and AUTO_PUSH:
        p2 = git("push")
        pushed = p2.returncode == 0
        if not pushed:
            git("fetch", "origin")
            rb = git("rebase", "origin/master")
            if rb.returncode != 0:
                git("rebase", "--abort")
                perr = "rebase 충돌 — 수동 해결 필요"
            else:
                p2 = git("push")
                pushed = p2.returncode == 0
                perr = "" if pushed else (p2.stderr or "")[-300:]
    log("   📝 %s  commit=%s push=%s" % (rel, committed, pushed))
    return {"ok": True, "file": rel, "text": text,
            "committed": committed, "pushed": pushed, "pushError": perr,
            "commitError": commit_error(c)}


# ── 전체 테스트케이스 보관소 ────────────────────────────────
# 코딩살구의 히든 TC 는 실제 채점용이라 매우 크다(BOJ 2493 탑 = 28MB, 50만 개 숫자).
# repo 에 넣으면 problems/ 가 565MB 가 되어 GitHub Pages 빌드가 실패하고,
# 브라우저가 문제 하나 보려고 28MB 를 받아야 한다.
# 그래서 repo 에는 200KB 로 줄인 보기용만 두고, 전체는 채점 서버에만 둔다.
#   ~/algo-tc/<sub>/<no>.json   {"samples":[...], "private":[...]}
# 서버(클라우드)는 ~/algo-tc, 내 PC 는 repo 의 _meta/tc_store 를 그대로 쓴다
# (564MB 를 두 벌 두지 않기 위해).
TC_STORE = os.path.join(os.path.expanduser("~"), "algo-tc")
TC_STORE_ALT = os.path.join(ROOT, "_meta", "tc_store")


def tc_path(site, no, write=False):
    # 경로를 만드는 곳에서 한 번 더 막는다 — 호출하는 쪽이 검사를 빼먹어도 밖으로 못 나간다.
    if site_no_error(site, no):
        raise ValueError("보관소 키가 이상합니다: %r / %r" % (site, str(no)[:20]))
    sub = SUB[site]
    primary = os.path.join(TC_STORE, sub, "%s.json" % no)
    if write or os.path.exists(primary):
        return primary
    alt = os.path.join(TC_STORE_ALT, sub, "%s.json" % no)
    return alt if os.path.exists(alt) else primary


def load_stored_tc(site, no):
    """보관된 전체 테스트케이스. 없거나 site·no 가 이상하면 None.

    읽는 길은 전부 여기를 지난다 — /judge(useStoredTC)·/tc·/tcfile·/prob·tc_upload(지문 보존).
    """
    if site_no_error(site, no):
        return None
    p = tc_path(site, no)
    if not os.path.exists(p):
        return None
    try:
        return json.load(io.open(p, encoding="utf-8"))
    except Exception:
        return None


def tc_info(site, no):
    err = site_no_error(site, no)
    if err:
        return err
    d = load_stored_tc(site, no)
    if not d:
        return {"ok": True, "stored": False, "hasProblem": False}
    pv = d.get("private") or []
    cases = [{"i": i, "in": len(t.get("in", "")), "out": len(t.get("out", ""))}
             for i, t in enumerate(pv)]
    # hasProblem: 비공개 사이트 지문이 보관돼 있나. sync_tc.py 가 이걸 보고 TC 만 있고
    # 지문이 빠진 항목(예전 sync 로 올라간 것)을 '이미 있음'으로 건너뛰지 않는다.
    return {"ok": True, "stored": True,
            "samples": len(d.get("samples") or []), "private": len(pv),
            "bytes": sum(c["in"] + c["out"] for c in cases),
            "cases": cases, "hasProblem": bool(d.get("problem"))}


def tc_preview(site, no, idx, limit=200_000, full=False):
    """케이스 하나를 미리보기용으로 잘라서 준다(브라우저 표시용)."""
    err = site_no_error(site, no)
    if err:
        return err
    d = load_stored_tc(site, no)
    if not d:
        return {"ok": False, "error": "보관된 테스트케이스가 없습니다"}
    pv = d.get("private") or []
    if not (0 <= idx < len(pv)):
        return {"ok": False, "error": "범위를 벗어난 인덱스"}
    t = pv[idx]
    a, b = t.get("in", ""), t.get("out", "")
    if full:
        return {"ok": True, "index": idx, "total": len(pv),
                "in": a, "out": b, "inFull": len(a), "outFull": len(b),
                "truncated": False}
    return {"ok": True, "index": idx, "total": len(pv),
            "in": a[:limit], "out": b[:limit],
            "inFull": len(a), "outFull": len(b),
            "truncated": len(a) > limit or len(b) > limit}


def tc_file(site, no, kind, idx=0):
    """sample_input.txt / sample_output.txt 를 원본 그대로 준다.

    SWEA B형(Pro) 문제는 제공되는 Main 코드가 표준입력을 파일로 돌려서 읽는다.
    로컬에서 돌려보려면 파일 자체가 필요해서, 브라우저가 받아 저장할 수 있게 연다.
    (repo 에는 앞부분 미리보기만 있고 전체본은 여기 보관소에만 있다)
    """
    err = site_no_error(site, no)
    if err:
        return err
    d = load_stored_tc(site, no)
    if not d:
        return {"ok": False, "error": "보관된 테스트케이스가 없습니다"}
    src = (d.get("samples") or []) or (d.get("private") or [])
    if not (0 <= idx < len(src)):
        return {"ok": False, "error": "범위를 벗어난 인덱스"}
    t = src[idx]
    inp = kind != "out"
    return {"ok": True,
            "text": t.get("in" if inp else "out", ""),
            "name": "sample_input.txt" if inp else "sample_output.txt"}


def tc_upload(d):
    """로컬에서 크롤링한 전체 TC 를 보관소에 저장.

    problem(선택): 비공개 사이트(코드트리)의 지문·입출력 설명·제약·힌트.
    repo 에 못 넣는 것이라 여기가 유일한 보관처다. 요청에 problem 이 없으면 이미 보관된
    것을 그대로 둔다 — TC 만 다시 올렸다고 지문이 지워지면 안 되기 때문이다.
    """
    site = (d.get("site") or "BOJ").upper()
    no = str(d.get("no") or "").strip()
    err = site_no_error(site, no)
    if err:
        return err
    prob = d.get("problem")
    if prob is not None and not isinstance(prob, dict):
        return {"ok": False, "error": "problem 은 객체(dict)여야 합니다"}
    p = tc_path(site, no, write=True)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    body = {"site": site, "no": no,
            "samples": d.get("samples") or [], "private": d.get("private") or []}
    if prob:
        body["problem"] = prob
    else:
        old = load_stored_tc(site, no) or {}
        if isinstance(old.get("problem"), dict) and old["problem"]:
            body["problem"] = old["problem"]
    io.open(p, "w", encoding="utf-8", newline="").write(
        json.dumps(body, ensure_ascii=False))
    return {"ok": True, "path": os.path.relpath(p, TC_STORE).replace(os.sep, "/"),
            "private": len(body["private"]), "hasProblem": "problem" in body}


def prob_info(site, no):
    """POST /prob — 보관소에 있는 비공개 지문·예제를 내준다(토큰 뒤).

    코드트리 지문은 repo 에 없으므로(PRIVATE_SITES) 대시보드는 문제 페이지를 열 때
    공개 JSON 의 private_content 를 보고 여기서 받아 그린다. 보관소에 TC 만 있고
    지문이 없으면 stored=False 다(그릴 지문이 없으니까).
    """
    site = (site or "").strip().upper()
    no = str(no or "").strip()
    err = site_no_error(site, no)
    if err:
        return err
    d = load_stored_tc(site, no) or {}
    if not isinstance(d.get("problem"), dict) or not d["problem"]:
        return {"ok": True, "stored": False}
    return {"ok": True, "stored": True, "problem": d["problem"],
            "samples": d.get("samples") or []}


def keep_private_copy(site, no, prob):
    """공개 파일에 섞여 들어온 비공개 부분을 보관소로 옮겨 둔다(보관소에 지문이 없을 때만).

    guard_private_staged() 가 공개 파일을 걸러 다시 쓰기 직전에 부른다. 크롤러가
    보관소 쓰기까지 빼먹은 상태라면, 걸러내는 순간 지문이 어디에도 안 남기 때문이다.
    """
    if site_no_error(site, no):         # 번호가 이상하면 옮기지 않는다(공개 파일 걸러내기는 그대로 한다)
        return False
    cur = load_stored_tc(site, no) or {}
    if cur.get("problem"):
        return False
    pp = {k: prob[k] for k in PRIVATE_PROBLEM_KEYS if prob.get(k)}
    if not pp.get("statement"):
        return False
    # 읽는 쪽(load_stored_tc)이 보는 파일에 쓴다. 둘 다 없으면 내 PC 의 보관소
    # (_meta/tc_store — sync_tc.py 가 올리는 곳)에 둔다. 클라우드에서도 폴백으로 읽힌다.
    p = tc_path(site, no)
    if not os.path.exists(p):
        p = os.path.join(TC_STORE_ALT, SUB.get(site, "boj"), "%s.json" % no)
    body = dict(cur)
    body.update({"site": site, "no": no, "problem": pp,
                 "samples": cur.get("samples") or prob.get("samples") or [],
                 "private": cur.get("private") or []})
    os.makedirs(os.path.dirname(p), exist_ok=True)
    io.open(p, "w", encoding="utf-8", newline="").write(json.dumps(body, ensure_ascii=False))
    return True


def guard_private_staged():
    """커밋 직전 마지막 관문 — 비공개 자료가 스테이징됐으면 걷어낸다. 걷어낸 경로 목록 반환.

    정상이라면 걸릴 일이 없다. _meta/tc_store/ 는 .gitignore 에 있고, 비공개 사이트의
    공개 JSON 은 크롤러와 save_solution 이 이미 걸러서 쓴다. 그래도 .gitignore 한 줄이나
    크롤러 버그 하나로 유료 지문이 통째로 public repo 에 올라가는 구조라(한 번 push 하면
    되돌릴 수 없다), 커밋하는 쪽인 허브가 한 번 더 막는다.
      1) _meta/tc_store/ 아래가 스테이징돼 있으면 내린다.
      2) problems/<비공개 sub>/<no>.json 에 지문·예제 키가 있으면, 보관소에 옮겨 두고
         공개 필드만 남겨 다시 쓴 뒤 다시 스테이징한다.
    """
    r = git("-c", "core.quotepath=false", "diff", "--cached", "--name-only")
    names = [x.strip() for x in (r.stdout or "").split("\n") if x.strip()]
    fixed = [x for x in names if x.startswith("_meta/tc_store/")]
    if fixed:
        git("reset", "-q", "--", "_meta/tc_store")
    subs = dict((SUB[s], s) for s in PRIVATE_SITES if s in SUB)
    for x in names:
        m = re.match(r"problems/([^/]+)/([^/]+)\.json$", x)
        if not m or m.group(1) not in subs:
            continue
        fp = os.path.join(ROOT, x.replace("/", os.sep))
        try:
            pd = json.load(io.open(fp, encoding="utf-8"))
        except Exception:
            continue                       # 삭제 커밋이라 파일이 없는 경우 등
        if not isinstance(pd, dict) or not any(pd.get(k) for k in PRIVATE_REDACT):
            continue
        site = subs[m.group(1)]
        keep_private_copy(site, str(pd.get("no") or m.group(2)), pd)
        io.open(fp, "w", encoding="utf-8", newline="").write(
            json.dumps(redact(pd, site), ensure_ascii=False, indent=1))
        git("add", "--", x)
        fixed.append(x)
    if fixed:
        slog("   🔒 비공개 자료가 커밋에 섞여 걷어냄: %s" % ", ".join(fixed)[:400])
    return fixed


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
    # no 는 지울 파일 이름(problems/<sub>/<no>.json · <sub>/<no>_*.py)에 그대로 들어간다.
    # 예전엔 검사가 없어 kind=problem, no="../../_meta/history" 로 history.json 이 지워지고,
    # 빌드가 다시 만든 빈약한 판(-3,816/+2,131줄)이 그대로 커밋됐다(2026-09-23 버리는
    # 클론에서 확인). 알려진 사이트 + 번호 규칙일 때만 지운다.
    # (번호가 빈 옛 제목 전용 기록은 위에서 예전처럼 'site/no 가 필요합니다' 로 끝난다)
    err = site_no_error(site, no)
    if err:
        return err
    sub = SUB[site]
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
        # at 이 오면 '그 회차 하나'만 지운다. 같은 날 여러 번 제출했을 때
        # 하나 지우려다 그날 전부가 날아가면 안 된다.
        at = (d.get("at") or "").strip()
        if at:
            tgt = None
            for it in rec.get("items", []):
                if (isinstance(it, dict) and it.get("site") == site
                        and str(it.get("no")) == no):
                    tgt = it
                    break
            if tgt is None:
                return {"ok": False, "error": "%s 에 %s %s 기록이 없습니다" % (date, site, no)}
            tries = [a for a in (tgt.get("attempts") or []) if isinstance(a, dict)]
            left = [a for a in tries if (a.get("at") or "") != at]
            if len(left) == len(tries):
                return {"ok": False,
                        "error": "%s 에 %s 회차 기록이 없습니다" % (date, at)}
            if left:
                # 회차가 남았으면 기록은 유지하고 대표값만 최신 회차로 맞춘다.
                # count(그날 시도한 문제 수)도 그대로다 — 문제는 여전히 풀었으니까.
                last = sorted(left, key=lambda a: a.get("at") or "")[-1]
                for k in ("at", "status", "file", "verdict", "passed", "total", "elapsed"):
                    if last.get(k) is not None:
                        tgt[k] = last[k]
                tgt["attempts"] = left
                io.open(hp, "w", encoding="utf-8", newline="").write(
                    json.dumps(hist, ensure_ascii=False, indent=1, sort_keys=True))
                for s in ("_meta/build_probindex.py", "_meta/build_heatmap.py",
                          "_meta/build_index.py"):
                    subprocess.run([PY, s], cwd=ROOT, capture_output=True,
                                   env={**os.environ, "PYTHONIOENCODING": "utf-8"})
                msg = "[삭제] %s %s %s %s 회차" % (site, no, date, at)
                return _commit_delete(msg, ["history %s %s: %s %s 회차"
                                            % (date, site, no, at)])
            # 마지막 회차였다면 아래 통째 삭제 경로로 내려간다(코드 파일·표식 포함).

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
        # 보관소(_meta/tc_store · ~/algo-tc)는 일부러 안 건드린다. 코드트리 지문은 repo 에
        # 없어서 보관소가 유일한 사본이다 — 공개 JSON 만 지우고 다시 가져오면 그대로 이어진다.
        pj = os.path.join(ROOT, "problems", sub, "%s.json" % no)
        imgs = []
        if os.path.exists(pj):
            try:
                imgs = json.load(io.open(pj, encoding="utf-8")).get("images") or []
            except Exception:
                imgs = []
            os.remove(pj)
            removed.append("problems/%s/%s.json" % (sub, no))
        # images 목록은 문제 JSON 안의 값이라 그대로 믿지 않는다 — 이 문제 폴더의
        # img/ 아래 파일만 지운다("../../_meta/history.json" 이 들어 있어도 안 지운다).
        img_dir = os.path.join(ROOT, "problems", sub, "img")
        for rel in imgs:
            if not isinstance(rel, str) or not rel:
                continue
            fp = os.path.join(ROOT, rel.replace("/", os.sep))
            if not _inside(fp, img_dir):
                log("   ⚠️ 이미지 경로가 %s/img 밖이라 안 지움: %s" % (sub, rel[:120]))
                continue
            if os.path.isfile(fp):
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

    return _commit_delete(msg, removed)


def commit_error(c):
    """커밋이 '변경 없음'이 아닌 이유로 실패했으면 그 이유(없으면 빈 문자열).

    pre-commit 훅(공개 금지 검사)이 커밋을 막으면 git 은 이유를 **stderr** 로 낸다.
    예전 응답은 stdout 만 실어서, 대시보드에는 '변경 없음'처럼 보이고 이유가 사라졌다.
    """
    if c.returncode == 0:
        return ""
    t = ((c.stderr or "") + "\n" + (c.stdout or "")).strip()
    if "nothing to commit" in t or "nothing added to commit" in t or "no changes added" in t:
        return ""
    log("   ⛔ 커밋 실패:", t[-300:])
    return t[-600:]


def _commit_delete(msg, removed):
    """삭제 후 커밋·푸시. 회차 하나만 지우는 경로에서도 그대로 쓴다."""
    git("add", "-A")
    guard_private_staged()
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
            "committed": committed, "pushed": pushed, "pushError": perr,
            "commitError": commit_error(c)}


SYNC_URL = ""      # --sync-url. 비우면 sync_tc.py 가 _meta/endpoint.json(클라우드 터널)을 따른다


def sync_private(site, no):
    """로컬 보관소의 문제 하나를 클라우드 허브로 올린다(best-effort). (성공 여부, 사유) 반환.

    비공개 사이트(코드트리)의 지문·예제는 repo 로 퍼지지 않으므로, 크롤링한 내 PC 의
    _meta/tc_store/ 에만 있다. 클라우드 허브가 /prob·채점을 하려면 거기도 있어야 해서
    크롤링 직후 바로 올린다. 크롤링 직후라 내용이 바뀌었을 수 있어 --force 로 덮는다.
    --no-push 로 띄웠으면(테스트) --sync-url 을 따로 주지 않는 한 밖으로 보내지 않는다.
    """
    if not AUTO_PUSH and not SYNC_URL:
        return False, "--no-push 라 클라우드 동기화 생략 (--sync-url 로 지정 가능)"
    if site_no_error(site, no):
        return False, "사이트/문제 번호가 이상합니다"
    argv = [PY, "_meta/sync_tc.py", "--only", "%s/%s" % (SUB[site], no), "--force"]
    if SYNC_URL:
        argv += ["--url", SYNC_URL]
    try:
        r = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True, timeout=90,
                           encoding="utf-8", errors="replace",
                           env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    except subprocess.TimeoutExpired:
        return False, "동기화 시간 초과(90초)"
    except Exception as e:
        return False, str(e)[:200]
    if r.returncode == 0:
        return True, ""
    return False, ((r.stdout or "") + (r.stderr or "")).strip()[-300:]


def fetch_problem(ref, save=False):
    """ref(URL 또는 BOJ 번호) 크롤링. save=True 면 problems/ 에 저장하고 커밋까지.

    코드트리(비공개 사이트)는 크롤러가 공개 JSON(problems/)과 비공개 보관본
    (_meta/tc_store/, gitignore)을 나눠 쓰고, stdout 에는 지문까지 든 전체 dict 를 찍는다.
    브라우저(토큰 보유자)에는 전체를 돌려주되, 커밋은 공개 파일만 하고
    보관본은 클라우드 허브로 올린다(synced).
    """
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
        js = str(prob.get("site") or "BOJ").strip().upper()
        jn = str(prob.get("no") or "unknown")
        junk = os.path.join(ROOT, "problems", SUB.get(js, "boj"), "%s.json" % jn)
        # 크롤러가 준 번호로 파일을 지우므로 같은 검사를 건다(problems/ 밖을 지우지 않게).
        if not site_no_error(js, jn) and os.path.exists(junk):
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
    # "_meta" 를 통째로 add 해도 _meta/tc_store/ 는 .gitignore 라 안 들어간다.
    # 그 한 줄에만 기대지 않도록 커밋 직전에 guard_private_staged() 로 한 번 더 거른다.
    git("add", "problems", "_meta", "index.html", "assets", "README.md", "HEATMAP.md")
    guard_private_staged()
    msg = "[문제추가] %s %s %s" % (prob.get("site", ""), prob.get("no", ""),
                                prob.get("title", ""))
    c = git("commit", "-m", msg.strip())
    res["committed"] = c.returncode == 0
    res["commitError"] = commit_error(c)
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
    # 동기화 실패로 요청을 실패시키지 않는다 — 공개 파일은 이미 커밋됐고,
    # 나중에 python _meta/sync_tc.py --site CT 로 다시 올리면 된다.
    if is_private(prob.get("site")):
        res["synced"], why = sync_private(str(prob.get("site")).strip().upper(),
                                          str(prob.get("no")))
        if why:
            res["syncError"] = why
        log("   ☁️ 보관소 동기화 %s%s" % (res["synced"], ("  (%s)" % why[:120]) if why else ""))
    return res


# ── 도구 배포 (/tool) ────────────────────────────────────────────────
# 다른 PC 에서 대시보드만 열면 개인 도구를 바로 받게 한다.
#
# 🚩 파일은 **repo 밖**(~/algo-tools)에 둔다. algo-solutions 는 public 이라
#    repo 안에 넣는 순간 GitHub Pages 로 그대로 공개된다. 배포하는 zip 에는
#    API 키가 들어 있으므로 이 구분이 곧 보안선이다.
# 🚩 GET 으로 열지 않는다. 모든 POST 가 지나는 _auth_ok() 뒤에 두어
#    토큰 보유자(=나)만 받을 수 있게 한다.
TOOLS_DIR = os.environ.get("ALGO_TOOLS_DIR") or os.path.expanduser("~/algo-tools")

# 도구 내려받기 전용 비밀번호. 토큰을 새 PC 마다 옮기는 게 번거로워서 열어 둔 길이다.
#
# 🚩 값을 코드에 적지 않는다 — 이 저장소는 public 이라 적는 순간 비밀번호가 아니다.
#    서버의 ~/.algo-tool-pass 에 한 줄로 넣어 둔다(없으면 이 길은 아예 닫힌다).
# 🚩 이 비밀번호로 열리는 것은 /tool · /toolinfo 뿐이다. 채점·저장·실행은
#    토큰 전용으로 남긴다 — 그쪽은 VM 에서 코드를 돌리는 권한이다.
TOOL_PASS_PATH = os.environ.get("ALGO_TOOL_PASS_FILE") or \
                 os.path.expanduser("~/.algo-tool-pass")


def load_tool_pass():
    try:
        return io.open(TOOL_PASS_PATH, encoding="utf-8").read().strip()
    except Exception:
        return ""


TOOL_PASS = load_tool_pass()


def tool_path(name=""):
    """배포할 파일 경로. 이름을 안 주면 가장 최근에 올린 zip 을 고른다."""
    if not os.path.isdir(TOOLS_DIR):
        return ""
    if name:
        # 파일명만 받는다 — "../../.ssh/id_rsa" 같은 경로 조작을 여기서 끊는다
        p = os.path.join(TOOLS_DIR, os.path.basename(name))
        return p if os.path.isfile(p) else ""
    zs = [os.path.join(TOOLS_DIR, f) for f in os.listdir(TOOLS_DIR)
          if f.lower().endswith(".zip")]
    return max(zs, key=os.path.getmtime) if zs else ""


def tool_info(name=""):
    """받기 전에 무엇을 받는지 보여 주기 위한 정보. 파일 내용은 담지 않는다."""
    p = tool_path(name)
    if not p:
        return {"ok": False, "error": "배포할 파일이 없습니다 (%s 에 zip 을 올려 두세요)"
                                      % TOOLS_DIR}
    import hashlib
    h = hashlib.sha256()
    with io.open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    st = os.stat(p)
    return {"ok": True,
            "name": os.path.basename(p),
            "size": st.st_size,
            "sha256": h.hexdigest()[:16],
            "mtime": datetime.datetime.fromtimestamp(st.st_mtime, KST)
                                      .strftime("%Y-%m-%d %H:%M")}


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
            "speedFactor": round(SPEED, 2), "pyMult": PY_MULT, "pyAdd": PY_ADD,
            "nativeMargin": NATIVE_MARGIN,
            "runner": RUNNER_NAME,
            # repo 절대경로(/home/<계정>/...)는 익명에게 굳이 알릴 게 아니다.
            "python": sys.version.split()[0], "repo": os.path.basename(ROOT),
            "branch": br, "ahead": ah, "dirty": dirty, "solutions": n,
            "autoPush": AUTO_PUSH,
            "endpoints": ["/judge", "/run", "/exec", "/save", "/fetch", "/note",
                          "/tc", "/tcfile", "/tcupload", "/prob", "/delete", "/problems"],
            "tcStore": (len(glob.glob(os.path.join(TC_STORE, "*", "*.json"))) +
                        len(glob.glob(os.path.join(TC_STORE_ALT, "*", "*.json"))))}


# ══════════════════════════════════════════════════════════════
# HTTP
# ══════════════════════════════════════════════════════════════
CORS = {"Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
        "Access-Control-Allow-Headers": "content-type, accept, x-auth-token, x-tool-pass, authorization",
        "Access-Control-Max-Age": "86400"}


_FAILS = {}                 # ip -> 연속 인증 실패 횟수
_LOCKED = {}                # ip -> 잠금 해제 시각(epoch). 짧은 비밀번호를 지키는 장치다.
LOCK_AFTER = 10             # 이만큼 연속 실패하면
LOCK_SECS = 600             # 이 시간 동안 아무것도 받지 못한다
_FAIL_LOCK = threading.Lock()


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

    def _send_bytes(self, data, ctype, filename):
        """파일 응답. 받은 흔적이 남지 않도록 캐시를 전부 끈다.

        no-store 가 없으면 zip 이 브라우저 디스크 캐시와 중간 프록시에 남는다.
        내용에 API 키가 들어 있으므로 '한 번 받고 흔적은 안 남기는' 쪽을 택했다.
        """
        self.send_response(200)
        for k, v in CORS.items():
            self.send_header(k, v)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Content-Disposition",
                         'attachment; filename="%s"' % filename)
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, private")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(data)

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
            # 지문 자체는 Pages 에 이미 공개돼 있다(소유자 결정). 여기서 막는 이유는
            # 비밀 유지가 아니라 부하다 — 한 번에 574개 파일을 읽어 18MB 를 만든다.
            # 대시보드는 이걸 안 쓰고 Pages 의 problems/<sub>/<no>.json 을 직접 읽는다.
            if not self._auth_ok():
                return self._reject(p)
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

    def _client_ip(self):
        # 터널을 거치면 client_address 는 항상 127.0.0.1 이다. 실제 IP 는
        # cloudflared 가 넣어주는 CF-Connecting-IP 에 있고, Cloudflare 가
        # 덮어쓰므로 터널 경유 요청은 이 헤더를 위조할 수 없다.
        return (self.headers.get("CF-Connecting-IP")
                or self.headers.get("X-Forwarded-For", "").split(",")[0].strip()
                or self.client_address[0] or "?")

    def _drain(self):
        """본문을 읽어 버린다.

        401 을 던지면서 POST 본문을 소켓에 남겨두면 keep-alive 연결이 어긋나
        '다음' 요청이 엉뚱하게 400 으로 깨진다. 실제로 인증 검사 결과가
        401/400 으로 번갈아 나와 '인증이 뚫린 것처럼' 보였다.
        """
        try:
            n = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            n = 0
        while n > 0:
            chunk = self.rfile.read(min(n, 65536))
            if not chunk:
                break
            n -= len(chunk)

    def _locked(self):
        """이 IP 가 잠겨 있나. 짧은 비밀번호는 이게 없으면 금방 뚫린다."""
        left = _LOCKED.get(self._client_ip(), 0) - time.time()
        return left if left > 0 else 0

    def _reject(self, path):
        """인증 실패 처리 — 본문 비우고, 반복되면 점점 느리게 답하다가 잠근다."""
        ip = self._client_ip()
        with _FAIL_LOCK:
            n = _FAILS.get(ip, 0) + 1
            _FAILS[ip] = n
            if n >= LOCK_AFTER:
                _LOCKED[ip] = time.time() + LOCK_SECS
        self._drain()
        if n > 3:                       # 토큰 대입 시도를 실질적으로 무의미하게
            time.sleep(min(0.5 * (2 ** min(n - 3, 5)), 15.0))
        left = self._locked()
        if left:
            slog("   🔒 잠금 (%s) from %s  누적 %d회 · %d초 남음"
                % (path, ip, n, int(left)))
            return self._send(429, {"ok": False, "error": "too many attempts",
                                    "retryAfter": int(left)})
        slog("   ⛔ 인증 실패 (%s) from %s  누적 %d회" % (path, ip, n))
        return self._send(401, {"ok": False, "error": "unauthorized",
                                "hint": "X-Auth-Token 헤더 필요"})

    def _auth_ok(self):
        if not TOKEN:
            return True
        # 헤더로만 받는다. 예전엔 ?token= 쿼리도 받았는데, URL 은 프록시 로그·
        # 브라우저 히스토리·Referer 에 그대로 남아 토큰이 새는 통로였다.
        got = (self.headers.get("X-Auth-Token")
               or self.headers.get("Authorization", "").replace("Bearer ", "").strip())
        import hmac
        if not hmac.compare_digest(str(got), str(TOKEN)):
            return False
        with _FAIL_LOCK:
            _FAILS.pop(self._client_ip(), None)
        return True

    def _tool_pass_ok(self):
        """도구 내려받기 전용 비밀번호. 토큰과 마찬가지로 헤더로만 받는다."""
        if not TOOL_PASS or self._locked():
            return False
        got = self.headers.get("X-Tool-Pass", "")
        import hmac
        if not hmac.compare_digest(str(got), str(TOOL_PASS)):
            return False
        with _FAIL_LOCK:
            _FAILS.pop(self._client_ip(), None)
        return True

    def do_POST(self):
        p = self.path.split("?")[0].rstrip("/")
        # 도구 내려받기 두 곳만 비밀번호로도 연다. 나머지는 토큰 전용.
        if not self._auth_ok():
            if not (p in ("/tool", "/toolinfo") and self._tool_pass_ok()):
                return self._reject(p)
        try:
            n = int(self.headers.get("Content-Length") or 0)
            body = json.loads(self.rfile.read(n).decode("utf-8") or "{}")
        except Exception as e:
            return self._send(400, {"ok": False, "error": "bad json: %s" % e})

        try:
            if p in ("/judge", ""):
                cases = body.get("testCases") or []
                # useStoredTC: 브라우저가 거대한 TC 를 올리지 않고, 서버가 보관본으로 채점한다.
                nstored = 0
                if body.get("useStoredTC"):
                    st = load_stored_tc((body.get("site") or "BOJ").upper(),
                                        str(body.get("problemId") or ""))
                    if st:
                        pub = [{"input": c.get("in", ""), "output": c.get("out", "")}
                               for c in (st.get("samples") or [])]
                        prv = [{"input": c.get("in", ""), "output": c.get("out", "")}
                               for c in (st.get("private") or [])]
                        cases = pub + prv
                        nstored = len(prv)
                        body["publicTestCaseCount"] = len(pub)
                if not cases:
                    # 케이스가 하나도 없다(보관본이 없는데 브라우저도 안 보냈거나, 예제 0개 보관본).
                    # 이대로 judge() 에 넘기면 빈 루프라 초기값 그대로 0/0 'accepted' 가 나온다
                    # (2026-09-23 확인). 코드트리는 예제가 보관소에만 있어서, 클라우드에 동기화가
                    # 안 된 문제를 채점하면 이 길로 '맞았습니다'가 뜬다 — 봐주기 금지라 여기서 끊는다.
                    log("\n▶ 채점  problemId=%s  테스트케이스 없음" % body.get("problemId"))
                    return self._send(200, {
                        "ok": False, "verdict": "no_testcases",
                        "error": ("이 허브에 보관된 테스트케이스가 없습니다. "
                                  "python _meta/sync_tc.py 로 올린 뒤 다시 채점하세요."
                                  if body.get("useStoredTC") else "채점할 테스트케이스가 없습니다."),
                        "summary": {"passed": 0, "total": 0, "firstFailedIndex": None},
                        "judgedAt": iso_now(), "elapsedSec": 0.0, "detail": []})
                try:
                    tl = allowed_time(body.get("timeLimit"),
                                      bool(body.get("langAdjusted")),
                                      body.get("timeMargin"))
                except (TypeError, ValueError):
                    tl = 5.0
                tt = uses_total_time((body.get("site") or "BOJ").upper(),
                                     str(body.get("problemId") or ""), body)
                log("\n▶ 채점  problemId=%s  TC %d개  제한 %ss%s"
                    % (body.get("problemId"), len(cases), body.get("timeLimit"),
                       "  (합계 방식)" if tt else ""))
                # allowed_time() 이 이미 PY_MULT·기기보정을 반영한 값이다.
                # 예전 고정식(x3+2)을 여기서 또 곱해 허용시간이 3배로 부풀던 버그가 있었다.
                r = judge(body.get("sourceCode") or "", cases,
                          int(body.get("publicTestCaseCount") or 0), tl,
                          total_time=tt)
                s = r.get("summary", {})
                log("◀ %s  %s/%s" % (r.get("verdict"), s.get("passed"), s.get("total")))
                return self._send(200, r)

            if p == "/run":
                cases = body.get("cases") or []
                log("\n▶ 실행  TC %d개" % len(cases))
                return self._send(200, judge(body.get("code") or "", cases, 0,
                                             allowed_time(body.get("timeLimit"),
                                                          bool(body.get("langAdjusted")))))

            if p == "/exec":
                try:
                    tl = min(max(float(body.get("timeLimit") or 5), 0.5), 30.0)
                except (TypeError, ValueError):
                    tl = 5.0
                log("\n▶ 연습장 실행  제한 %.1fs" % tl)
                r = scratch_run(body.get("code") or "", body.get("stdin") or "", tl)
                log("◀ %s  %.3fs" % (r.get("status"), r.get("elapsed") or 0))
                return self._send(200, r)

            if p == "/tc":
                site = (body.get("site") or "BOJ").upper()
                no = str(body.get("no") or "")
                if body.get("index") is not None:
                    return self._send(200, tc_preview(
                        site, no, int(body["index"]),
                        limit=int(body.get("limit") or 200_000),
                        full=bool(body.get("full"))))
                return self._send(200, tc_info(site, no))

            if p == "/tcfile":
                return self._send(200, tc_file(
                    (body.get("site") or "BOJ").upper(), str(body.get("no") or ""),
                    body.get("kind") or "in", int(body.get("index") or 0)))

            if p == "/tcupload":
                return self._send(200, tc_upload(body))

            if p == "/prob":
                return self._send(200, prob_info(body.get("site"), body.get("no")))

            if p == "/note":
                log("\n▶ 메모  %s %s %s" % (body.get("site"), body.get("no"),
                                          body.get("date") or ""))
                return self._send(200, save_note(body))

            if p == "/delete":
                log("\n▶ 삭제  %s %s %s %s" % (body.get("kind"), body.get("site"),
                                             body.get("no"), body.get("date") or ""))
                return self._send(200, delete_item(body))

            if p == "/save":
                log("\n▶ 저장  %s %s %s" % (body.get("site"), body.get("no"), body.get("title")))
                return self._send(200, save_solution(body))

            if p == "/toolinfo":
                d = tool_info(body.get("name") or "")
                d["byPass"] = not self._auth_ok()   # 비밀번호로 들어왔는지
                return self._send(200, d)

            if p == "/tool":
                path = tool_path(body.get("name") or "")
                if not path:
                    return self._send(404, tool_info(body.get("name") or ""))
                data = io.open(path, "rb").read()
                # 디버깅용 로그 — 언제·어디서·무엇을 받았는지만 남긴다.
                # 토큰과 파일 내용은 절대 남기지 않는다.
                slog("\n▶ 도구 내려받기  %s  %.1f KB  (%s) from %s"
                     % (os.path.basename(path), len(data) / 1024.0,
                        "토큰" if self._auth_ok() else "비밀번호",
                        self._client_ip()))
                return self._send_bytes(data, "application/zip",
                                        os.path.basename(path))

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
    # 예전 기본값은 0.0.0.0 이라 사내망·공용 와이파이에 그대로 노출됐다.
    # 클라우드는 터널(localhost)로만 들어오고, 로컬은 같은 PC 브라우저가 쓰므로
    # 127.0.0.1 로 충분하다. LAN 에서 붙어야 하면 --bind 0.0.0.0.
    ap.add_argument("--bind", default="127.0.0.1", help="바인딩 주소 (기본 127.0.0.1)")
    ap.add_argument("--sync-url", default="",
                    help="코드트리 보관본을 올릴 허브 (기본: _meta/endpoint.json 의 클라우드)")
    a = ap.parse_args()
    global TOKEN, SYNC_URL
    PY, PORT, VERBOSE, AUTO_PUSH = a.python, a.port, not a.quiet, not a.no_push
    SYNC_URL = a.sync_url.strip().rstrip("/")
    TOKEN = "" if a.no_auth else load_token()
    global RUNNER, RUNNER_NAME, SPEED
    RUNNER, RUNNER_NAME = find_runner(a.runner)
    fixed = load_config()
    SPEED = fixed if fixed else measure_speed()

    print("=" * 64)
    print("  🐍 algo-hub  로컬 서버 (채점 + repo 저장)")
    print("=" * 64)
    print("  주소    : %s:%d" % (a.bind, PORT))
    print("  repo    : %s" % ROOT)
    print("  채점러너 : %s" % RUNNER_NAME)
    print("             %s" % RUNNER)
    print("  자동푸시 : %s" % ("ON" if AUTO_PUSH else "OFF"))
    print("  비공개 사이트: %s%s" % (", ".join(sorted(PRIVATE_SITES)) or "없음",
                                   ("  ⚠️ 설정을 못 읽어 안전하게 비공개 (%s)" % PRIVATE_WHY)
                                   if PRIVATE_WHY else "  (_meta/judge_config.json privateSites)"))
    print("  허용식   : (제한 x %.1f + %.1f) x 기기보정 %.2f" % (PY_MULT, PY_ADD, SPEED))
    print("             1초 제한 -> %.1f초  |  언어별 제한 명시 시 -> 제한 x %.2f"
          % (allowed_time(1), SPEED))
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
    ThreadingHTTPServer((a.bind, PORT), H).serve_forever()


if __name__ == "__main__":
    main()
