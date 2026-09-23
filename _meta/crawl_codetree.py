"""
코드트리(codetree.ai) 문제 수집 — 트레일 6개 + 기출(삼성 SW 역량테스트 / 현대 HSAT / ACPC).

코드트리는 SPA 라 화면 텍스트를 긁지 않는다. 사이트가 스스로 부르는 API
(https://api-prod.codetree.ai/api/v2/) 를 **로그인된 디버그 크롬의 내 탭 안에서** 부른다.
비로그인이면 트레일 카드가 일부만 보이고 문제 본문은 403 이다.

사용법:
    python _meta/crawl_codetree.py list                  # 카탈로그 → _meta/codetree_list.json
    python _meta/crawl_codetree.py list --refresh        # 카드→문제번호 매핑도 전부 새로 조회
    python _meta/crawl_codetree.py fetch                 # 아직 안 받은 문제 전부
    python _meta/crawl_codetree.py fetch --group samsung-sw --limit 5
    python _meta/crawl_codetree.py fetch --no 196 --no f386 --force   # 트레일 196 · 기출 f386
    python _meta/crawl_codetree.py fetch --retry-locked  # 403(잠김)이던 것도 다시 시도
    python _meta/crawl_codetree.py all                   # list → fetch
    python _meta/crawl_codetree.py rebuild-public        # 공개/비공개 스위치를 바꾼 뒤 공개 JSON 다시 만들기
                                                         # (다시 받지 않는다 — 보관소 + 기존 메타로)
    python _meta/crawl_codetree.py rebuild-public --no f386 --no f385   # 보관소에 생성 TC 를 넣은 문제만 반영

생성 테스트케이스(2026-09-23 계약): TC 생성 파이프라인은 보관소의 private([{in,out}])·tc_generated·tc_note
    만 쓴다. 크롤러는 그 셋을 절대 지우지 않고(fetch --force 도 보존), 문제 파일에는 보관소에서 옮긴다 —
    공개 모드: private_testcases(200KB 까지 통째로)·private_tc_count·private_tc_omitted / 비공개 모드: 개수만.

결과:
    _meta/codetree_list.json            카탈로그: 트레일 챕터/레슨/카드 구조·번호·제목·URL
    problems/codetree/<no>.json         문제 파일 — 공개 모드면 지문·예제까지, 비공개 모드면 메타만
    _meta/tc_store/codetree/<no>.json   보관소(gitignore) — 지문·입출력·제약·힌트·예제. 모드와 무관하게 늘 쓴다
                                         → python _meta/sync_tc.py 로 채점 서버 ~/algo-tc 에 올린다

공개/비공개 스위치는 한 곳: _meta/judge_config.json 의 "privateSites".
    소유자 결정(2026-09-23): [] = 코드트리도 BOJ/SWEA 처럼 지문을 공개 저장한다.
    ["CT"] 로 바꾸면 repo 에는 메타만 남긴다(바꾼 뒤 rebuild-public). 설정을 못 읽으면 안전하게 비공개.
    어느 모드든 기출의 유형 태그·선수 레슨·내 진행상태는 저장하지 않는다(유형 스포 금지).

<no> — 트레일은 problem_id 그대로("196"), 기출은 앞에 f 를 붙인다("f386").
    ⚠️ 트레일과 기출의 problem_id 는 **서로 다른 번호 체계**다(2026-09-23 실측). 기출 번호는 기출
    목록의 id(1~400)와 같고, 트레일 번호(1~4766)와 106개가 겹치는데 겹친 것은 전부 별개 문제였다
    (예: 386 = 트레일 "문자열 돌리기" / 삼성 기출 "AI 로봇청소기"). 번호만 보고 합치면 기출 106개가
    엉뚱한 트레일 문제 밑으로 사라진다. 원래 번호는 항목의 pid 에 남긴다.

단건(허브 /fetch): python _meta/fetch_problem.py <코드트리 URL | ct:196 | ct:f386> --print [--save]
    → 이 파일의 fetch_one() 을 쓴다.

선행조건: 디버그 크롬(9222) + 코드트리 로그인
    python _meta/debug_chrome.py --open https://www.codetree.ai/ko/trails/complete/dashboard
Windows 콘솔: 앞에 PYTHONIOENCODING=utf-8
"""
import os, io, re, sys, json, time, argparse, datetime, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIST_PATH = os.path.join(ROOT, "_meta", "codetree_list.json")
PUB_DIR = os.path.join(ROOT, "problems", "codetree")
STORE_DIR = os.path.join(ROOT, "_meta", "tc_store", "codetree")

SITE, SUB, PLATFORM = "CT", "codetree", "코드트리"

CONFIG = os.path.join(ROOT, "_meta", "judge_config.json")


def load_private_sites():
    """지문을 repo 에 넣지 않을 사이트 — _meta/judge_config.json 의 "privateSites" (단일 스위치).

    server.py·selfcheck·훅이 같은 값을 읽는다. 파일이 없거나 깨졌거나 키가 없으면
    **안전하게 {"CT"}(비공개)** 로 본다 — 설정 사고로 유료 지문이 공개 repo 에 새는 쪽으로
    넘어지지 않게(fail-closed).
    """
    try:
        with io.open(CONFIG, encoding="utf-8") as f:
            v = json.load(f)["privateSites"]
        if not isinstance(v, list):
            raise ValueError("privateSites 가 목록이 아님")
        return set(str(x).strip().upper() for x in v)
    except Exception:
        return {"CT"}


# 모듈 상수 이름은 server.py 와 같게 두고 값만 설정에서 채운다.
PRIVATE_SITES = load_private_sites()
# 문제 내용 키 — 비공개 모드면 공개 파일에 절대 들어가면 안 된다(write_public 이 쓰기 직전에 한 번 더 막는다).
PRIVATE_KEYS = ("statement", "input_spec", "output_spec", "constraints", "hint",
                "samples", "sample_notes")

API = "https://api-prod.codetree.ai/api/v2/"
HOME = "https://www.codetree.ai/ko/trails/complete/dashboard"
CDP = "http://127.0.0.1:9222"

TREE = "trails/%s/?leaf=CuratedCard&trail_type=complete"
CARD = "curated-cards/%s/?trail_type=complete"
FLIST = "frequent-problems/problems/?page=%d&page_size=100&source_key=%s&order=-date"
FMETA = "frequent-problems/problems/%s/"
CARD_URL = "https://www.codetree.ai/ko/trails/complete/curated-cards/%s/description"
FREQ_URL = "https://www.codetree.ai/ko/frequent-problems/%s/problems/%s/description"

TRAILS = ["novice-low", "novice-mid", "novice-high",
          "intermediate-low", "intermediate-mid", "intermediate-high"]
# 기출: (source_key, 트리에 보일 이름, 그룹 순서). API 의 company/source 문구("SW 역량 테스트")를
# 그대로 쓰지 않고 알아보기 쉬운 이름으로 고정한다.
FREQ = [("samsung-sw", "삼성 SW 역량테스트", 101),
        ("hsat", "현대 HSAT", 102),
        ("acpc", "ACPC", 103)]
GROUP_KEYS = TRAILS + [k for k, _, _ in FREQ]
CODE_BLOCK = "Code block"

# ── 요청 속도 ─────────────────────────────────────────────────
# 사용자 본인 계정으로 도는 크롤링이라 **계정 보호가 속도보다 우선**이다.
# 전체(카드 매핑 1,334 + 본문 ~1,450 ≈ 2,900건)가 12~15분 걸리는 속도면 충분하다.
MAX_CONC = 3          # 동시 요청 수
MIN_GAP_MS = 250      # 요청 시작 간격 → 초당 4건 이하
STOP_429 = 2          # 429 가 연달아 이만큼이면 즉시 중단 (한 번은 15초 쉬고 재시도, 두 번째면 멈춤)
STOP_403 = 3          # 403 도 연달아 나오면 차단 신호일 수 있어 멈춘다 (잠긴 문제 한두 개는 정상)
STOP_ERR = 5          # 네트워크 오류·5xx 연속
CHUNK = 12            # 한 번의 page.evaluate 로 보내는 요청 수(진행 출력·중간 저장 단위)

RE_CARD = re.compile(r"curated-cards/([A-Za-z0-9_-]+)")
RE_FREQ = re.compile(r"frequent-problems/([A-Za-z0-9_-]+)/problems/([A-Za-z0-9_-]+)")
RE_PROB = re.compile(r"/problems/([A-Za-z0-9_-]+)")


def _out(*a):
    print(*a, flush=True)


def _err(*a):
    # 라이브러리로 쓸 때(fetch_problem.py --print)는 진행 메시지를 stderr 로 보낸다.
    # 허브는 stdout 의 첫 "{" 부터를 JSON 으로 읽으므로 stdout 에 잡담이 섞이면 안 된다.
    print(*a, file=sys.stderr, flush=True)


def _first(e):
    return (str(e).strip().split("\n") or [""])[0][:140]


def today():
    return datetime.date.today().isoformat()


# ── 오류 ──────────────────────────────────────────────────────
class CTError(Exception):
    """사용자에게 그대로 보여줄 한국어 메시지를 담는 오류."""


class LoginRequired(CTError):
    def __init__(self, why=""):
        CTError.__init__(
            self, "❌ 디버그 크롬에서 코드트리 로그인 필요%s\n"
                  "   python _meta/debug_chrome.py --open %s  → 로그인 후 다시 실행"
                  % ((" (%s)" % why) if why else "", HOME))


WHY = {"429": "429(요청 과다)", "403": "403(권한 없음·차단 의심)",
       "neterr": "네트워크 오류", "5xx": "서버 오류(5xx)"}


class Stopped(CTError):
    """코드트리가 429/403 등을 연달아 돌려줌 → 계정 보호를 위해 즉시 멈춤(재시도 폭주 금지)."""

    def __init__(self, why, where=""):
        self.why = why
        CTError.__init__(
            self, "⛔ %s 중 코드트리 응답이 연달아 %s — 계정 보호를 위해 즉시 멈췄습니다.\n"
                  "   받은 것까지는 저장했습니다. 한참 뒤 같은 명령으로 이어 받으면 됩니다(받은 건 건너뜀)."
                  % (where or "요청", WHY.get(why, why)))


# ── 브라우저 안에서 부르는 JS ─────────────────────────────────
# ⚠️ 토큰(JWT)은 절대 파이썬으로 넘기지 않는다(출력·로그·파일 저장 금지).
#    요청마다 페이지 안에서 localStorage 를 읽어 헤더에만 쓴다. 파이썬이 받는 건 만료 시각뿐.
TOKINFO_JS = r"""() => {
  const t = localStorage.getItem('CODETREE_GLOBAL_TOKEN');
  const now = Date.now() / 1000;
  if (!t) return {has: false, exp: 0, now: now};
  let exp = 0;
  try {
    const p = JSON.parse(atob(t.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')));
    exp = p.exp || 0;
  } catch (e) {}
  return {has: true, exp: exp, now: now};
}"""

# 여러 API 경로를 동시 conc 개, 시작 간격 gap(ms) 이상으로 부른다.
# st = 연속 429/403/오류 카운터 — 배치 사이에도 이어지도록 파이썬이 들고 다닌다.
# 한도에 닿으면 stop 을 세우고 **새 요청을 더 내지 않는다**(재시도 폭주 금지).
BATCH_JS = r"""async (a) => {
  const API = 'https://api-prod.codetree.ai/api/v2/';
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const st = a.st;
  const res = new Array(a.paths.length).fill(null);
  let next = 0, pauseUntil = 0, stop = '', idx = 0, n = 0;
  // JS 는 단일 스레드라 이 예약 방식에 경합이 없다. 429 가 오면 pauseUntil 로 전원이 쉰다.
  const slot = async () => {
    for (;;) {
      const now = Date.now();
      const t = Math.max(now, next, pauseUntil);
      if (t <= now) { next = now + a.gap; return; }
      await sleep(t - now);
    }
  };
  const one = async (p) => {
    for (let k = 0; k < 4; k++) {
      if (stop) return null;
      await slot();
      if (stop) return null;
      const tok = localStorage.getItem('CODETREE_GLOBAL_TOKEN');  // 요청마다 읽는다(사이트가 중간에 갱신한다)
      let r = null, b = null;
      n++;
      try {
        r = await fetch(API + p, {headers: tok ? {'Authorization': 'JWT ' + tok} : {}});
      } catch (e) {
        st.cerr++;
        if (st.cerr >= a.stopErr) { stop = 'neterr'; return {s: -1, e: String(e).slice(0, 100)}; }
        await sleep(2000 * (k + 1));
        continue;
      }
      const s = r.status;
      try { b = await r.json(); } catch (e) { b = null; }
      if (s === 401) { stop = stop || 'auth'; return {s: s}; }
      if (s === 429) {
        st.c429++;
        if (st.c429 >= a.stop429 || k >= 1) { stop = '429'; return {s: s}; }
        const ra = parseInt(r.headers.get('Retry-After') || '0', 10) || 0;
        pauseUntil = Date.now() + Math.max(ra * 1000, 15000);
        continue;
      }
      st.c429 = 0;
      if (s >= 500) {
        st.cerr++;
        if (st.cerr >= a.stopErr) { stop = '5xx'; return {s: s}; }
        if (k < 2) { await sleep(3000 * (k + 1)); continue; }
        return {s: s};
      }
      st.cerr = 0;
      if (s === 403) {
        st.c403++;
        if (st.c403 >= a.stop403) stop = stop || '403';
        return {s: s, b: (b && typeof b === 'object' && b.detail) ? {detail: String(b.detail).slice(0, 200)} : null};
      }
      st.c403 = 0;
      return {s: s, b: b};
    }
    return {s: -1, e: 'retries exhausted'};
  };
  const worker = async () => {
    while (!stop && idx < a.paths.length) {
      const i = idx++;
      res[i] = await one(a.paths[i]);
    }
  };
  const W = [];
  for (let k = 0; k < a.conc; k++) W.push(worker());
  await Promise.all(W);
  return {res: res, st: st, stop: stop, n: n};
}"""


class Session:
    """로그인된 디버그 크롬에 **내 탭 하나**를 열어 그 안에서 API 를 부른다.

    사용자의 다른 탭(오라클·SWEA·플레이 콘솔·대시보드 등)은 건드리지 않고, 끝나면 내 탭만 닫는다.
    """

    def __init__(self, log=None):
        self.log = log or _err
        self.pw = self.pg = None
        self.st = {"c429": 0, "c403": 0, "cerr": 0}
        self.nreq = 0

    def __enter__(self):
        return self.ensure()

    def __exit__(self, *exc):
        self.close()

    def ensure(self):
        if self.pg is not None:
            return self
        # playwright 는 여기서 늦게 import 한다. 클라우드 허브(VM, Python 3.8, 플레이라이트 없음)가
        # /fetch 로 fetch_problem.py 를 돌려도 SyntaxError 가 아니라 ImportError("playwright")로
        # 떨어져야 허브가 "로컬 허브에서 하세요(needsLocal)" 로 안내할 수 있다.
        from playwright.sync_api import sync_playwright
        self.pw = sync_playwright().start()
        try:
            b = self.pw.chromium.connect_over_cdp(CDP)
        except Exception as e:
            self.close()
            raise CTError("❌ 디버그 크롬(9222)에 붙지 못했습니다 → python _meta/debug_chrome.py 로 "
                          "띄우고 코드트리 로그인\n   (%s)" % _first(e))
        ctx = b.contexts[0] if b.contexts else b.new_context()
        self.pg = ctx.new_page()
        # `with Session() as s:` 에서 __enter__ 가 예외를 던지면 __exit__ 가 불리지 않는다.
        # 여기서 실패하면 내 탭을 직접 닫고 올려 보낸다(사용자 크롬에 빈 탭이 쌓이지 않게).
        try:
            self.pg.goto(HOME, wait_until="domcontentloaded", timeout=90000)
            self._wait_login()
        except CTError:
            self.close()
            raise
        except Exception as e:
            self.close()
            raise CTError("❌ 코드트리 페이지를 열지 못했습니다 (%s)" % _first(e))
        return self

    def close(self):
        try:
            if self.pg is not None:
                self.pg.close()
        except Exception:
            pass
        try:
            if self.pw is not None:
                self.pw.stop()          # CDP 연결만 끊는다(사용자 크롬은 그대로)
        except Exception:
            pass
        self.pg = self.pw = None

    def _tok(self):
        try:
            return self.pg.evaluate(TOKINFO_JS) or {}
        except Exception:
            return {}                   # 새로고침 도중이면 잠깐 실패한다

    def _wait_login(self, secs=15):
        t0 = time.time()
        while True:
            if "/accounts/login" in (self.pg.url or ""):
                raise LoginRequired("로그인 페이지로 이동됨")
            if self._tok().get("has"):
                return
            if time.time() - t0 > secs:
                raise LoginRequired("토큰 없음")
            self.pg.wait_for_timeout(500)

    def _refresh(self):
        """401 = 액세스 토큰 만료. 토큰 수명이 **15분**뿐이라 전체 크롤링 중 반드시 한 번은 만료된다.

        실측(2026-09-23): 만료 순간부터 우리 요청이 401 이 되고, 사이트 쪽이 무언가를 부를 때
        axios 인터셉터(setup-*.js)가 401 을 받고 refresh 토큰으로 새 토큰을 받아 localStorage 에 둔다.
        우리가 refresh API 를 직접 부르면 refresh 토큰이 회전될 때 사이트 로그인이 깨질 수 있어서,
        **내 탭을 새로고침**해 사이트가 스스로 갱신하게 하고 새 토큰(만료 시각이 바뀜)을 기다린다.
        """
        i = self._tok()
        if i.get("has") and i.get("exp", 0) - i.get("now", 0) > 30:
            # 401 을 받은 사이에 다른 탭(사용자의 코드트리 탭)이 이미 갱신해 둔 경우. 여기서 "바뀌길"
            # 기다리면 영영 안 바뀌어 로그인 필요로 오판한다 → 바로 다시 시도(401 이 반복되면 api_many 가 멈춘다)
            return
        old = i.get("exp", 0)
        self.log("   ↻ 코드트리 토큰 만료 — 내 탭을 새로고침해 갱신을 기다립니다")
        try:
            self.pg.reload(wait_until="domcontentloaded", timeout=90000)
        except Exception:
            pass
        t0 = time.time()
        while time.time() - t0 < 60:
            if "/accounts/login" in (self.pg.url or ""):
                raise LoginRequired("로그인 페이지로 이동됨")
            i = self._tok()
            if i.get("has") and i.get("exp", 0) != old and i["exp"] - i["now"] > 30:
                return
            self.pg.wait_for_timeout(1000)
        raise LoginRequired("토큰 갱신 실패")

    def api_many(self, paths):
        """API 경로 목록 → ([{s: status, b: body} | None, ...], 중단사유).

        None = 중단 때문에 아예 부르지 않은 것. 401 은 토큰 갱신 뒤 그 자리만 다시 부른다.
        중단사유가 있으면 받은 것까지만 돌려준다 — 호출한 쪽이 저장하고 멈춘다.
        """
        self.ensure()
        out = [None] * len(paths)
        todo = list(range(len(paths)))
        refreshes = 0
        while todo:
            r = self.pg.evaluate(BATCH_JS, {
                "paths": [paths[i] for i in todo], "gap": MIN_GAP_MS, "conc": MAX_CONC,
                "st": self.st, "stop429": STOP_429, "stop403": STOP_403, "stopErr": STOP_ERR})
            self.st = r.get("st") or self.st
            self.nreq += int(r.get("n") or 0)
            stop = r.get("stop") or ""
            again = []
            for k, i in enumerate(todo):
                x = r["res"][k]
                if x is None or x.get("s") == 401:
                    again.append(i)
                else:
                    out[i] = x
            if stop and stop != "auth":
                return out, stop
            if not again:
                return out, ""
            refreshes += 1
            if refreshes > 2:
                raise LoginRequired("토큰을 갱신해도 401")
            self._refresh()
            todo = again
        return out, ""

    def api(self, path):
        res, stop = self.api_many([path])
        if stop:
            raise Stopped(stop)
        return res[0] or {"s": -1}


# ── 파일 ──────────────────────────────────────────────────────
def ct_no(kind, pid):
    """사이트 안에서 겹치지 않는 번호. 트레일·기출은 problem_id 번호 체계가 달라 기출에 f 를 붙인다."""
    return ("f%s" % pid) if kind == "frequent" else str(pid)


def valid_no(no):
    # no 는 파일명·허브 경로에 그대로 쓰인다. 서버 정규식 [A-Za-z0-9_-]{1,12} 을 통과해야 하고,
    # 코드트리 번호는 트레일 "숫자" / 기출 "f+숫자" 뿐이다(이상하면 건너뛰고 보고).
    return bool(re.fullmatch(r"f?\d{1,11}", str(no or "")))


def pub_path(no):
    return os.path.join(PUB_DIR, "%s.json" % no)


def store_path(no):
    return os.path.join(STORE_DIR, "%s.json" % no)


def _write_json(path, obj, indent=1):
    # 중간에 끊겨도 반쪽짜리 파일이 남지 않게 임시 파일에 쓰고 바꿔 끼운다.
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with io.open(tmp, "w", encoding="utf-8", newline="") as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=indent))
    os.replace(tmp, path)


def load_list():
    if not os.path.exists(LIST_PATH):
        return None
    try:
        with io.open(LIST_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def save_list(cat):
    _write_json(LIST_PATH, cat, indent=1)


def _url_key(u):
    """카드/기출 URL → 매핑 키. 예전 카탈로그에서 '카드 → 문제번호' 를 재사용할 때 쓴다."""
    m = RE_CARD.search(u or "")
    if m:
        return ("card", m.group(1))
    m = RE_FREQ.search(u or "")
    if m:
        return ("freq", m.group(1), m.group(2))
    return None


# ── 변환 ──────────────────────────────────────────────────────
def _md(s):
    return (s or "").replace("\r\n", "\n").strip()


def _nl(s):
    # 예제는 채점에 그대로 쓰이므로 줄바꿈 형식만 맞추고 내용(끝 개행 포함)은 건드리지 않는다.
    return (s or "").replace("\r\n", "\n")


def _sec(ms):
    return "%g초" % (ms / 1000.0)


def limits_of(specs):
    """judge_specs → limits.

    "Python3" 는 PyPy 계열이고 "Python3 (CPython)" 은 따로 있으며 제한이 더 길다(1초 vs 3.5초).
    우리 채점 러너가 PyPy 이므로 Python3 제한을 time_sec 로 쓴다 — time_sec 이 있으면
    대시보드·허브가 '이미 언어별 제한'(lang-adjusted)으로 보고 Python 보정(×3+2)을 하지 않는다.
    ⚠️ time 문자열만 있고 time_sec 이 없으면 대시보드가 첫 숫자를 제한으로 읽는데,
       "Python3"·"C++17" 의 3·17 을 초로 잡는다. 그래서 Python 제한이 없으면 time 도 비운다.
    """
    specs = specs or {}
    py_key = "Python3" if (specs.get("Python3") or {}).get("time_limit") else (
        "Python3 (CPython)" if (specs.get("Python3 (CPython)") or {}).get("time_limit") else "")
    L = {}
    if not py_key:
        return L
    py = specs[py_key]
    parts = ["%s %s" % ("Python3" if py_key == "Python3" else "Python3(CPython)",
                        _sec(py["time_limit"]))]
    for ck in ("C++17", "C++20", "C++14"):
        c = specs.get(ck) or {}
        if c.get("time_limit"):
            parts.append("%s %s" % (ck, _sec(c["time_limit"])))
            break
    L["time"] = " · ".join(parts)
    if py.get("memory_limit"):
        L["memory"] = "%s MB" % py["memory_limit"]
    L["time_sec"] = round(py["time_limit"] / 1000.0, 3)
    return L


def stats_of(body):
    cc, sc = body.get("correct_count"), body.get("submission_count")
    st = {}
    if isinstance(sc, int) and sc > 0 and isinstance(cc, int):
        st["accept_rate"] = "%.1f" % (cc * 100.0 / sc)
    if isinstance(sc, int):
        st["submissions"] = str(sc)
    return st


def meta_doc(it, title=None):
    """공개해도 되는 메타만(번호·제목·URL·위치·난이도)."""
    d = {"site": SITE, "platform": PLATFORM, "no": it["no"],
         "title": title or it.get("title", ""), "url": it.get("url", ""),
         "alias": it.get("alias", "")}
    if it.get("pid") is not None:
        d["pid"] = it["pid"]
    d["group"], d["kind"] = it.get("group", ""), it.get("kind", "")
    if it.get("kind") == "trail":
        for k in ("chapter", "lesson", "card", "card_type"):
            if it.get(k):
                d[k] = it[k]
    elif it.get("origin"):
        d["origin"] = it["origin"]
    if it.get("level"):
        d["level"] = it["level"]
    if it.get("ptype"):
        d["ptype"] = it["ptype"]
    return d


CHOICE_HOW = {"Single choice": "하나 고르기", "Multiple choice": "모두 고르기",
              "Sequential choice": "순서대로 고르기"}


def _code(s):
    # 인라인 코드. 내용에 백틱이 있으면 두 겹 백틱으로 감싼다(CommonMark 규칙).
    return ("`` %s ``" % s) if "`" in s else ("`%s`" % s)


def _ws_mark(s):
    # 공백 문자를 눈에 보이는 표기로. 코드 안에서는 역슬래시가 글자 그대로 보인다.
    return s.replace("\n", "\\n").replace("\t", "\\t").replace(" ", "␣")


def _visible_ws(raw, core):
    """앞뒤 공백이 정답을 가르는 보기 → 공백을 보이게 적은 마크다운.

    수식($)이 섞였으면 수식은 코드 밖에 그대로 두고(렌더되게) 공백 표시만 코드로 붙인다.
    수식이 없으면 보기 전체를 코드로 적는다(`2.844\\n`). 원문 역슬래시는 두 번 적지 않는다.
    """
    lead = raw[:len(raw) - len(raw.lstrip())]
    trail = raw[len(raw.rstrip()):]
    if "$" in core:
        return "".join([_code(_ws_mark(lead)) if lead else "",
                        core.replace("\n", "\n   "),
                        _code(_ws_mark(trail)) if trail else ""])
    return _code(_ws_mark(lead) + core.replace("\n", "\\n") + _ws_mark(trail))


def choices_md(pt, mc):
    """객관식류 보기 → 지문 끝에 붙일 마크다운 목록.

    객관식(Single/Multiple/Sequential choice, 트레일에 283개)은 보기가 description 이 아니라
    multiple_choice.questions / sequential_choice.questions 에 따로 온다. 지문만 저장하면
    "다음 중 옳은 것은?" 만 남아 문제를 읽을 수 없어서, 보기를 지문 끝에 목록으로 붙인다.
    (정답은 API 가 주지 않으므로 채점은 못 한다 → ptype 으로 표시)
    """
    raws = []
    for q in mc.get("questions") or []:
        if isinstance(q, dict):
            q = q.get("content") or q.get("text") or q.get("question") or ""
        raws.append((q if isinstance(q, str) else json.dumps(q, ensure_ascii=False))
                    .replace("\r\n", "\n"))
    if not raws:
        return ""
    # 앞뒤 공백·줄바꿈이 **정답을 가르는** 보기가 있다 — "출력결과 42"(724)의 보기는
    # "2.844" / "2.844" / "2.844\n" 이다. 떼어 버리면 셋이 똑같이 보인다.
    # 그렇다고 공백이 붙은 보기를 전부 코드로 적으면 안 된다: 보기 대부분은 끝에 우연히 줄바꿈이
    # 붙어 있을 뿐이라, 183문제가 코드 글자가 됐고 $\mathcal{O}(1)$ 같은 수식이 렌더되지 않았다
    # (역슬래시까지 두 번 적어 \\mathcal 로 보였다 — 대시보드 담당 발견, 2026-09-23).
    # → 떼었을 때 **다른 보기와 같아지는** 경우에만 공백을 보이게 적는다. 역슬래시는 원문 그대로.
    cores = [r.strip() for r in raws]
    forms = collections.defaultdict(set)
    for r, c in zip(raws, cores):
        forms[c].add(r)
    qs = []
    for r, c in zip(raws, cores):
        if r != c and len(forms[c]) > 1:
            qs.append(_visible_ws(r, c))
        else:
            qs.append(c.replace("\n", "\n   "))       # 여러 줄 보기는 목록 항목 안으로 들여쓴다
    how = CHOICE_HOW.get(pt, "")
    if pt == "Sequential choice" and isinstance(mc.get("answers_count"), int):
        how = "순서대로 %d개 고르기" % mc["answers_count"]
    return "\n".join(["**보기**%s" % ((" — " + how) if how else ""), ""] +
                     ["%d. %s" % (i, q) for i, q in enumerate(qs, 1)])


def build_full(it, body, day=None):
    """본문 응답 → 화면용 전체 dict(메타 + 지문·예제). 파일로는 write_problem 이 나눠 쓴다."""
    cb = body.get("code_block") or {}
    tcs = sorted(cb.get("test_cases") or [], key=lambda t: t.get("order") or 0)
    samples = [{"in": _nl(t.get("input")), "out": _nl(t.get("output"))} for t in tcs]
    notes = [_md(t.get("description")) for t in tcs]
    d = meta_doc(it, title=(body.get("title") or "").strip() or None)
    pt = body.get("problem_type") or ""
    if pt and pt != CODE_BLOCK:
        d["ptype"] = pt                          # 채점 불가 표시용(객관식·서술형 등)
    elif pt == CODE_BLOCK:
        d.pop("ptype", None)
    d["limits"] = limits_of(cb.get("judge_specs"))
    st = stats_of(body)
    if st:
        d["stats"] = st
    stmt = _md(body.get("description"))
    ch = choices_md(pt, body.get("multiple_choice") or body.get("sequential_choice") or {})
    if ch:
        stmt = (stmt + "\n\n" + ch) if stmt else ch
    d["sample_count"] = len(samples)
    d["statement_len"] = len(stmt)
    d["fetched_at"] = day or today()
    d.update({"statement": stmt,
              "input_spec": _md(body.get("input_format")),
              "output_spec": _md(body.get("output_format")),
              "constraints": _md(body.get("constraints")),
              "hint": _md(body.get("hint")),
              "samples": samples,
              "sample_notes": notes if any(notes) else []})
    return d


# 보관소의 생성 테스트케이스에서 나오는 문제 파일 필드. 원본은 늘 보관소이고, 문제 파일에는
# 쓸 때마다 보관소에서 새로 만든다(예전 문제 파일에 남은 값은 믿지 않는다).
TC_KEYS = ("private_tc_count", "private_testcases", "private_tc_omitted", "tc_generated", "tc_note")
_FP = None


def cap_private_tc(tc):
    """fetch_problem.py 의 cap_private_tc(PRIV_CAP = 200KB)를 그대로 쓴다 — 상한 기준을 한 곳에만 둔다.

    케이스는 자르지 않는다(자르면 채점에 못 쓴다). 통째로 들어가는 것까지만 담고 못 담은 개수를 센다.
    (상한이 없던 시절 BOJ 2493 하나가 28MB 가 되어 Pages 빌드가 죽었다 — CLAUDE.md 0-2)
    """
    global _FP
    if _FP is None:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "fetch_problem_cap", os.path.join(ROOT, "_meta", "fetch_problem.py"))
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)                # 정의만 있는 모듈이라 부작용 없음(main 은 __main__ 일 때만)
        _FP = m
    return _FP.cap_private_tc(tc)


def tc_fields(store, private_mode):
    """보관소의 생성 테스트케이스(private)·설명 → 문제 파일에 넣을 필드.

    공개 모드: private_tc_count(전체) + private_testcases(200KB 까지 통째로) + private_tc_omitted(못 담은 수, >0 일 때)
    비공개 모드: private_tc_count 만(케이스는 빼고 개수만).
    tc_generated·tc_note 는 두 모드 모두 보관소 값을 그대로 복사한다.
    """
    st = store if isinstance(store, dict) else {}
    out = {}
    pv = st.get("private")
    if isinstance(pv, list) and pv:
        out["private_tc_count"] = len(pv)
        if not private_mode:
            keep, omitted = cap_private_tc(pv)
            if keep:
                out["private_testcases"] = keep
            if omitted:
                out["private_tc_omitted"] = omitted
    for k in ("tc_generated", "tc_note"):
        if k in st:
            out[k] = st[k]
    return out


def public_part(full, store=None):
    """repo 에 쓸 문제 파일 — 지금 스위치(PRIVATE_SITES) 기준.

    공개 모드: 메타 + 지문·입출력·제약·힌트·예제(빈 값은 뺀다 — 다른 사이트 파일과 같은 규칙)
               + 보관소의 생성 테스트케이스(tc_fields).
    비공개 모드: 메타만 + private_content=true (대시보드가 이걸 보고 허브 /prob 로 지문을 받는다)
               + 생성 테스트케이스는 개수만.
    """
    private = SITE in PRIVATE_SITES
    d = {k: v for k, v in full.items()
         if k not in PRIVATE_KEYS and k not in TC_KEYS and k != "private_content"}
    if private:
        d["private_content"] = True
    else:
        for k in PRIVATE_KEYS:
            if full.get(k) not in ("", [], None):
                d[k] = full[k]
    d.update(tc_fields(store, private))
    return d


def read_store(no):
    """보관소 파일 → dict, 없으면 None.

    있는데 못 읽으면(깨진 JSON 등) CTError — 그대로 덮어쓰면 다른 도구가 넣은 생성 테스트케이스가
    날아간다. 이 문제만 실패로 두고 파일은 건드리지 않는다.
    """
    p = store_path(no)
    if not os.path.exists(p):
        return None
    d = _load(p)
    if not isinstance(d, dict):
        raise CTError("보관소 파일을 읽지 못해 덮어쓰지 않음(생성 TC 보존): %s"
                      % os.path.relpath(p, ROOT).replace(os.sep, "/"))
    return d


def store_doc(full, old=None):
    """보관소에 쓸 내용 — 허브 TC 보관소 형식({site,no,samples,private}) + problem(지문 묶음).

    ⚠️ 보관소의 private·tc_generated·tc_note 는 **TC 생성 파이프라인이 쓰는 자리**다(삼성 기출 생성 TC,
       2026-09-23 계약). 크롤러는 samples·problem 만 새로 쓰고, 예전 파일의 나머지 키는 그대로 둔다
       — fetch --force 로 다시 받아도 생성 TC 가 지워지지 않게.
    """
    d = dict(old) if isinstance(old, dict) else {}
    d["site"], d["no"] = SITE, full["no"]
    d["samples"] = full.get("samples") or []
    if d.get("private") is None:
        d["private"] = []
    prob = {"title": full.get("title", "")}
    for k in ("statement", "input_spec", "output_spec", "constraints", "hint", "sample_notes"):
        if full.get(k):
            prob[k] = full[k]
    d["problem"] = prob
    return d


def write_public(full, store=None):
    """문제 파일(problems/codetree/<no>.json) 쓰기 — fetch·fetch_one·rebuild-public 이 모두 이것만 쓴다.
    store = 그 문제의 보관소 내용(생성 TC 반영용). 반환: 내용이 바뀌었는지."""
    if not valid_no(full.get("no")):
        raise CTError("❌ 번호 형식 이상: %r" % full.get("no"))
    pub = public_part(full, store)
    if SITE in PRIVATE_SITES:
        leak = [k for k in PRIVATE_KEYS + ("private_testcases",) if k in pub]
        if leak:                                  # 비공개 모드에서 공개 repo 로 지문이 새는 일은 무조건 막는다
            raise CTError("❌ 공개 파일에 비공개 키가 섞임: %s" % leak)
    p = pub_path(full["no"])
    new = json.dumps(pub, ensure_ascii=False, indent=1)
    try:
        with io.open(p, encoding="utf-8") as f:
            if f.read() == new:
                return False                      # 같으면 안 쓴다(git 잡음·mtime 방지)
    except (IOError, OSError):
        pass
    _write_json(p, pub, indent=1)
    return True


def write_problem(full):
    """받은 문제 하나를 보관소 + 문제 파일에 쓴다. 반환: 쓴 보관소 내용."""
    if not valid_no(full.get("no")):
        raise CTError("❌ 번호 형식 이상: %r" % full.get("no"))
    if not (full.get("statement") or "").strip():
        raise CTError("❌ 빈 지문은 보관소에 쓰지 않습니다: %s" % full.get("no"))
    st = store_doc(full, read_store(full["no"]))     # 기존 생성 TC 등은 보존
    # 보관소를 먼저 쓴다 — 공개 파일만 있고 보관소가 없는 반쪽 상태가 남지 않게.
    _write_json(store_path(full["no"]), st, indent=None)
    write_public(full, st)
    return st


def locked_doc(it, day=None):
    d = meta_doc(it)
    d["locked"] = True
    d["limits"] = {}
    d["fetched_at"] = day or today()
    return d


def write_locked(it, day=None):
    """403 — 이 계정으로는 못 여는 문제. 공개 파일에 locked 만 남기고 비공개 보관은 만들지 않는다.

    예전에 받아 둔 게 있으면(구독이 끝난 경우 등) 그 메타는 살리고 locked 만 얹는다.
    """
    p = pub_path(it["no"])
    doc = None
    if os.path.exists(p):
        try:
            with io.open(p, encoding="utf-8") as f:
                doc = json.load(f)
        except Exception:
            doc = None
    if doc and not doc.get("locked"):
        doc["locked"] = True
    else:
        doc = locked_doc(it, day)
    _write_json(p, doc, indent=1)
    return doc


def content_path(alias, kind):
    # sources 가 문제의 출처와 맞아야 한다. 트레일 문제를 sources=frequent 로(또는 반대로)
    # 부르면 403 "이 작업을 수행할 권한이 없습니다" 가 온다(실측: ai-robot, print-one-line).
    return "problems/%s/?sources=%s" % (alias, "trail" if kind == "trail" else "frequent")


def apply_result(it, x, day=None, save=True):
    """본문 응답 하나 → 파일. 반환 (상태 ok|locked|fail, dict|None, 카탈로그 변경 여부, 실패 사유).

    ⚠️ 보관소(tc_store)는 비공개 모드에서 지문의 **유일한 사본**이다(repo 에는 없다). 그래서 지문이
       비었거나 403/오류일 때는 보관소 파일을 절대 덮어쓰지 않는다 — 빈 지문으로 덮으면 허브 /prob 가
       빈 지문을 stored:true 로 내준다(허브 담당 요청, 2026-09-23). 공개 모드에서도 같은 규칙.
    """
    s = (x or {}).get("s")
    b = (x or {}).get("b")
    if not valid_no(it.get("no")):
        return "fail", None, False, "번호 형식 이상(%r)" % it.get("no")
    if s == 200 and isinstance(b, dict) and (b.get("title") or b.get("description")):
        full = build_full(it, b, day)
        if not (full.get("statement") or "").strip():
            return "fail", None, False, "빈 지문 — 보관소를 건드리지 않음"
        try:
            if save:
                st = write_problem(full)
            else:
                st = read_store(full["no"])        # --print 만: 읽기만(화면에 생성 TC 도 보이게)
        except CTError as e:
            if save:
                return "fail", None, False, str(e)   # 이 문제만 실패 — 전체 수집은 계속
            st = None
        # 화면용(--print·허브 /fetch) dict 에는 모드와 무관하게 생성 TC 를 담는다(파일은 write_public 이 모드대로).
        full.update(tc_fields(st, False))
        changed = bool(it.pop("locked", None))
        pt = full.get("ptype") or ""
        if pt != (it.get("ptype") or ""):
            if pt:
                it["ptype"] = pt
            else:
                it.pop("ptype", None)
            changed = True
        return "ok", full, changed, ""
    if s == 403:
        doc = write_locked(it, day) if save else locked_doc(it, day)
        changed = not it.get("locked")
        it["locked"] = True
        return "locked", doc, changed, ""
    if s == 200:
        return "fail", None, False, "응답에 제목·지문 없음"
    return "fail", None, False, "HTTP %s %s" % (s, ((x or {}).get("e") or "")[:60])


# ── list: 카탈로그 ─────────────────────────────────────────────
def _ord(x):
    o = x.get("order")
    return (o is None, o if isinstance(o, (int, float)) else 0)


def _chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def build_list(sess, refresh=False, log=_out):
    """트레일 6개 + 기출 3개 → _meta/codetree_list.json.

    카드 → problem_id 는 카드마다 API 를 한 번씩 불러야 알 수 있다(1,334장, 초당 4건이면 ~6분).
    그래서 예전 카탈로그에 있던 매핑은 재사용하고 새 카드만 묻는다(--refresh 면 전부 다시).
    유형 스포 금지(사용자 규칙): 기출의 tags·prerequisite_lessons 는 받더라도 저장하지 않는다.
    사용자 진행상태(progress_status)도 저장하지 않고, Passed 개수만 화면에 찍는다.
    """
    t0 = time.time()
    old = load_list()
    known, old_locked = {}, set()
    if old:
        old_locked = {it["no"] for it in old.get("items") or [] if it.get("locked")}
        if not refresh:
            for it in old.get("items") or []:
                pid = str(it.get("pid") if it.get("pid") is not None else it["no"]).lstrip("f")
                val = (pid, it.get("alias", ""), it.get("ptype") or "")
                for u in [it.get("url", "")] + [a.get("url", "") for a in it.get("also") or []]:
                    k = _url_key(u)
                    # 첫 빌드(2026-09-23)는 트레일·기출 번호를 한 체계로 보고 합쳐서, 기출이 엉뚱한
                    # 트레일 문제의 also 에 들어가 있었다. 종류가 다른 매핑은 믿지 않고 다시 묻는다.
                    if k and (k[0] == "card") == (it.get("kind") == "trail"):
                        known[k] = val
    log("코드트리 카탈로그 — 기존 매핑 재사용 %d건%s" % (len(known), " (--refresh)" if refresh else ""))

    base = ["public/trails/"] + [TREE % a for a in TRAILS] + ["frequent-problems/sources/"]
    res, stop = sess.api_many(base)
    if stop:
        raise Stopped(stop, "목록")
    for p, x in zip(base, res):
        if not x or x.get("s") != 200:
            raise CTError("❌ 목록 API 실패: %s → HTTP %s" % (p, (x or {}).get("s")))
    tmeta = {t.get("alias"): t for t in res[0]["b"] or []}
    trees = dict((a, res[1 + i]["b"] or {}) for i, a in enumerate(TRAILS))
    srcs = {s.get("source_key"): s for s in res[-1]["b"] or []}
    extra = sorted(set(tmeta) - set(TRAILS))
    if extra:
        log("   ℹ️ 새 트레일이 보입니다(카탈로그엔 안 넣음): %s" % ", ".join(extra))
    for a in TRAILS:
        if a not in tmeta:
            log("   ⚠️ public/trails 에 %s 가 없습니다" % a)

    flists = {}
    for key, _, _ in FREQ:
        if key not in srcs:
            log("   ⚠️ 기출 출처에 %s 가 없습니다" % key)
        rows, page = [], 1
        while True:
            x = sess.api(FLIST % (page, key))
            if x.get("s") != 200:
                raise CTError("❌ 기출 목록 실패: %s p%d → HTTP %s" % (key, page, x.get("s")))
            b = x["b"] or {}
            rows += b.get("results") or []
            if not b.get("next") or page >= 50:
                break
            page += 1
        cnt = (srcs.get(key) or {}).get("problem_count")
        if cnt is not None and cnt != len(rows):
            log("   ⚠️ %s: 출처 문제 수 %s ≠ 목록 %d" % (key, cnt, len(rows)))
        flists[key] = rows

    # 트리 순회 — 화면 노출 순서(트레일 → 챕터 → 레슨 → 카드), 전부 order 로 정렬
    groups, cards = [], []
    passed, total = collections.Counter(), collections.Counter()
    for i, a in enumerate(sorted(TRAILS, key=lambda a: _ord(tmeta.get(a) or {"order": 99}))):
        tm = tmeta.get(a) or {}
        groups.append({"key": a, "kind": "trail", "name": tm.get("alias_name") or a,
                       "sub": tm.get("name") or "", "order": tm.get("order") or (i + 1)})
        for ch in sorted(trees[a].get("chapters") or [], key=_ord):
            for le in sorted(ch.get("lessons") or [], key=_ord):
                for c in sorted(le.get("curated_cards") or [], key=_ord):
                    total[a] += 1
                    if c.get("progress_status") == "Passed":
                        passed[a] += 1
                    cards.append({"group": a, "chapter": ch.get("name", ""),
                                  "chapter_no": ch.get("order"), "lesson": le.get("name", ""),
                                  "lesson_no": le.get("order"), "card_no": c.get("order"),
                                  "card": c.get("alias", ""), "card_type": c.get("card_type", ""),
                                  "level": c.get("level", ""), "title": c.get("name", "")})
    fents = []
    for key, name, order in FREQ:
        groups.append({"key": key, "kind": "frequent", "name": name, "sub": "기출", "order": order})
        for r in flists[key]:
            total[key] += 1
            if r.get("progress_status") == "Passed":
                passed[key] += 1
            lv = r.get("level")
            fents.append({"group": key, "falias": r.get("alias", ""), "title": r.get("name", ""),
                          "origin": r.get("origin", ""),
                          "level": ("L%d" % lv) if isinstance(lv, int) else str(lv or "")})

    # 카드/기출 → problem_id 매핑(모르는 것만)
    stop, locked_map, failed_map = "", [], []
    need = [("card", c["card"]) for c in cards if ("card", c["card"]) not in known]
    need += [("freq", f["group"], f["falias"]) for f in fents
             if ("freq", f["group"], f["falias"]) not in known]
    need = list(collections.OrderedDict.fromkeys(need))
    if need:
        log("문제 번호 매핑: %d건 조회 (동시 %d · 초당 %d 이하)"
            % (len(need), MAX_CONC, 1000 // MIN_GAP_MS))
    done = 0
    for ch in _chunks(need, CHUNK * 2):
        paths = [(CARD % k[1]) if k[0] == "card" else (FMETA % k[2]) for k in ch]
        res, stop = sess.api_many(paths)
        for k, x in zip(ch, res):
            if x is None:
                continue
            b = x.get("b") if isinstance(x.get("b"), dict) else {}
            if x.get("s") == 200 and b.get("problem_id") is not None:
                known[k] = (str(b["problem_id"]), b.get("problem_alias") or "",
                            b.get("problem_type") or "")
            elif x.get("s") == 403:
                locked_map.append(k)
            else:
                failed_map.append((k, x.get("s")))
        done += sum(1 for x in res if x is not None)
        if done % 120 < CHUNK * 2 or done == len(need) or stop:
            log("  매핑 %4d/%d  (%.1f분)" % (done, len(need), (time.time() - t0) / 60))
        if stop:
            break

    # 조립 — 같은 problem_id 는 첫 등장만 items 에, 나머지는 also 로
    items, by_no, bad_no = [], {}, []
    newc, dup = collections.Counter(), collections.Counter()

    def put(g, kind, key, item, also):
        m = known.get(key)
        if not m:
            return
        pid, alias, pt = m
        no = ct_no(kind, pid)                     # 트레일 "386" / 기출 "f386" — 번호 체계가 다르다
        if not valid_no(no) or not alias:
            bad_no.append((key, no))              # 파일명·허브 경로로 못 쓰는 번호 → 건너뛰고 보고
            return
        if no in by_no:
            # 같은 종류 안에서 번호가 같으면 진짜 같은 문제다(alias 도 같아야 정상).
            if by_no[no].get("alias") != alias:
                log("   ⚠️ 번호 %s 에 alias 가 둘: %s / %s" % (no, by_no[no].get("alias"), alias))
            by_no[no].setdefault("also", []).append(also)
            dup[g] += 1
            return
        item["no"], item["alias"], item["pid"] = no, alias, int(pid)
        if pt and pt != CODE_BLOCK:
            item["ptype"] = pt
        if no in old_locked:
            item["locked"] = True
        items.append(item)
        by_no[no] = item
        newc[g] += 1

    for c in cards:
        url = CARD_URL % c["card"]
        put(c["group"], "trail", ("card", c["card"]),
            {"no": "", "title": c["title"], "alias": "", "pid": 0, "group": c["group"], "kind": "trail",
             "chapter": c["chapter"], "chapter_no": c["chapter_no"], "lesson": c["lesson"],
             "lesson_no": c["lesson_no"], "card_no": c["card_no"], "card": c["card"],
             "card_type": c["card_type"], "level": c["level"], "url": url},
            {"group": c["group"], "kind": "trail", "chapter": c["chapter"], "lesson": c["lesson"],
             "card": c["card"], "card_type": c["card_type"], "url": url})
    for f in fents:
        url = FREQ_URL % (f["group"], f["falias"])
        put(f["group"], "frequent", ("freq", f["group"], f["falias"]),
            {"no": "", "title": f["title"], "alias": "", "pid": 0, "group": f["group"], "kind": "frequent",
             "origin": f["origin"], "level": f["level"], "url": url},
            {"group": f["group"], "kind": "frequent", "origin": f["origin"], "url": url})

    cat = {"built": today(), "count": len(items), "groups": groups, "items": items}
    if stop or locked_map or failed_map:
        cat["partial"] = True                     # 다음 list 가 이어서 채운다
    save_list(cat)

    log("")
    log("그룹별  (카드/문제 → 신규 · 중복 · 내가 Passed)")
    for g in groups:
        log("  %-18s %4d → 신규 %4d · 중복 %3d · Passed %3d"
            % (g["key"], total[g["key"]], newc[g["key"]], dup[g["key"]], passed[g["key"]]))
    pt = collections.Counter(it["ptype"] for it in items if it.get("ptype"))
    diff_alias = sum(1 for it in items if it["kind"] == "frequent"
                     and RE_FREQ.search(it["url"]).group(2) != it["alias"])
    log("총 %d문제 (중복 %d) · 비코드 %d%s · 매핑 403 %d · 매핑 실패 %d%s"
        % (len(items), sum(dup.values()), sum(pt.values()),
           (" %s" % dict(pt)) if pt else "", len(locked_map), len(failed_map),
           (" · 기출 alias≠문제 alias %d" % diff_alias) if diff_alias else ""))
    for k, s in failed_map[:10]:
        log("   ❌ %s → HTTP %s" % ("/".join(k), s))
    if bad_no:
        log("   ⚠️ 번호 형식이 이상해 건너뜀 %d건: %s" % (len(bad_no), ", ".join(
            "%s=%r" % ("/".join(k), no) for k, no in bad_no[:10])))
    log("→ %s  (요청 %d건 · %.1f분)" % (os.path.relpath(LIST_PATH, ROOT).replace(os.sep, "/"),
                                     sess.nreq, (time.time() - t0) / 60))
    if stop:
        raise Stopped(stop, "번호 매핑")
    return cat


# ── fetch: 지문·예제 ───────────────────────────────────────────
def select_items(cat, groups=None, nos=None, limit=0, force=False, retry_locked=False):
    items = cat.get("items") or []
    if groups:
        gs = set(groups)
        items = [it for it in items if it.get("group") in gs
                 or any(a.get("group") in gs for a in it.get("also") or [])]
    if nos:
        want = [str(n).strip() for n in nos]
        have = {it["no"] for it in items}
        miss = [n for n in want if n not in have]
        if miss:
            _out("   ⚠️ 카탈로그에 없는 번호: %s" % ", ".join(miss))
        ws = set(want)
        items = [it for it in items if it["no"] in ws]
    todo, n_exist, n_locked = [], 0, 0
    for it in items:
        if not force:
            if os.path.exists(pub_path(it["no"])) and os.path.exists(store_path(it["no"])):
                n_exist += 1
                continue
            if it.get("locked") and not retry_locked:
                n_locked += 1
                continue
        todo.append(it)
    if limit:
        todo = todo[:limit]
    return todo, n_exist, n_locked


def _clean_tmp():
    # 원자적 쓰기(임시 파일 → os.replace) 도중 강제 종료되면 <no>.json.tmp 가 남는다.
    # problems/ 에 남은 것은 허브의 `git add problems` 에 딸려 커밋될 수 있어 치운다.
    # (방금 만든 것은 다른 프로세스가 쓰는 중일 수 있으니 1분 넘은 것만)
    for d in (PUB_DIR, STORE_DIR):
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            p = os.path.join(d, f)
            if f.endswith(".json.tmp") and time.time() - os.path.getmtime(p) > 60:
                try:
                    os.remove(p)
                except OSError:
                    pass


def run_fetch(sess, cat, todo, log=_out):
    _clean_tmp()
    t0 = time.time()
    n = len(todo)
    cnt = collections.Counter()
    img = math = 0
    dirty = False
    day = today()
    stop = ""
    try:
        for s0 in range(0, n, CHUNK):
            chunk = todo[s0:s0 + CHUNK]
            res, stop = sess.api_many([content_path(it["alias"], it["kind"]) for it in chunk])
            for k, (it, x) in enumerate(zip(chunk, res)):
                if x is None:
                    continue                      # 중단 때문에 못 부름 → 다음 실행에서
                st, d, ch, why = apply_result(it, x, day)
                dirty = dirty or ch
                cnt[st] += 1
                head = "  [%4d/%d] %-6s" % (s0 + k + 1, n, it["no"])
                if st == "ok":
                    stmt = d.get("statement") or ""
                    img += "![" in stmt
                    math += "$" in stmt
                    log("%s ✅ %-22s 지문%5d자 예제%d%s%s"
                        % (head, (d.get("title") or "")[:22], len(stmt), d["sample_count"],
                           ("  " + d["limits"]["time"]) if d["limits"].get("time") else "",
                           ("  [%s]" % d["ptype"]) if d.get("ptype") else ""))
                elif st == "locked":
                    log("%s 🔒 잠김(403)  %s" % (head, it.get("title", "")[:30]))
                else:
                    log("%s ❌ %s  %s" % (head, why, it.get("title", "")[:30]))
            if dirty:
                save_list(cat)
                dirty = False
            if stop:
                break
    finally:
        if dirty:
            save_list(cat)
        left = n - sum(cnt.values())
        log("")
        log("완료: 성공 %d · 잠김 %d · 실패 %d%s  (그림 포함 %d · 수식 포함 %d)  요청 %d건 · %.1f분"
            % (cnt["ok"], cnt["locked"], cnt["fail"], (" · 중단으로 남음 %d" % left) if left else "",
               img, math, sess.nreq, (time.time() - t0) / 60))
    if stop:
        raise Stopped(stop, "본문 수집")
    return cnt


# ── rebuild-public: 스위치를 바꾼 뒤 공개 파일 다시 만들기 ────────────
def _load(p):
    try:
        with io.open(p, encoding="utf-8") as f:
            return json.load(f)
    except (IOError, OSError, ValueError):
        return None


def full_from_files(pub, store):
    """공개 파일(메타 + 있으면 지문) + 보관소 → 전체 dict. 보관소에 지문이 있으면 그쪽이 원본이다.
    생성 TC 필드(TC_KEYS)는 여기서 버리고 write_public 이 보관소에서 새로 만든다."""
    full = {k: v for k, v in pub.items()
            if k not in PRIVATE_KEYS and k not in TC_KEYS and k != "private_content"}
    prob = (store or {}).get("problem") or {}
    src = prob if (prob.get("statement") or "").strip() else pub
    for k in ("statement", "input_spec", "output_spec", "constraints", "hint", "sample_notes"):
        if src.get(k):
            full[k] = src[k]
    full["samples"] = ((store or {}).get("samples") if src is prob else pub.get("samples")) or []
    if full.get("statement"):
        full["statement_len"] = len(full["statement"])
        full["sample_count"] = len(full["samples"])
    return full


def rebuild_public(nos=None, log=_out):
    """공개/비공개 스위치(judge_config.json privateSites)와 보관소에 맞춰 problems/codetree/*.json 을 다시 쓴다.

    **다시 받지 않는다.** 지문은 보관소(tc_store)에 전부 있으므로 보관소 + 기존 공개 메타로 만든다.
    보관소에 생성 테스트케이스(private·tc_generated·tc_note)를 넣은 뒤에도 이걸로 반영한다
    (nos 로 그 문제들만: rebuild-public --no f386 --no f385).
    비공개로 돌릴 때 보관소에 지문이 없으면(공개 파일이 유일한 사본) 보관소부터 채운 뒤 공개 파일에서 뺀다.
    """
    mode = "비공개(메타만)" if SITE in PRIVATE_SITES else "공개(지문 포함)"
    if nos:
        files, miss = [], []
        for n in nos:
            n = str(n).strip().lower()
            if valid_no(n) and os.path.exists(pub_path(n)):
                files.append(n + ".json")
            else:
                miss.append(n)
        files = list(collections.OrderedDict.fromkeys(files))
        if miss:
            log("   ⚠️ 문제 파일이 없거나 번호 형식이 이상해 건너뜀: %s" % ", ".join(miss))
    else:
        files = sorted(f for f in os.listdir(PUB_DIR) if f.endswith(".json")) \
            if os.path.isdir(PUB_DIR) else []
    log("문제 파일 다시 만들기 — 모드: %s  (privateSites=%s)  대상 %d개"
        % (mode, sorted(PRIVATE_SITES), len(files)))
    cnt = collections.Counter()
    for f in files:
        no = f[:-5]
        if not valid_no(no):
            cnt["bad"] += 1
            log("   ⚠️ 번호 형식 이상 — 건너뜀: %s" % f)
            continue
        pub = _load(pub_path(no))
        if not isinstance(pub, dict):
            cnt["bad"] += 1
            log("   ⚠️ 읽기 실패 — 건너뜀: %s" % f)
            continue
        try:
            store = read_store(no)
        except CTError as e:
            cnt["bad"] += 1
            log("   ⚠️ %s — 건너뜀" % e)
            continue
        full = full_from_files(pub, store)
        if (store or {}).get("private"):
            cnt["tc"] += 1
        if not (full.get("statement") or "").strip():
            # 잠긴 문제(403) 등 지문이 없는 것 — 메타만 남긴다(모드와 무관)
            cnt["locked" if pub.get("locked") else "nostmt"] += 1
            if write_public(full, store):
                cnt["changed"] += 1
            continue
        if SITE in PRIVATE_SITES and not ((store or {}).get("problem") or {}).get("statement"):
            store = store_doc(full, store)       # 생성 TC 등 기존 키는 보존
            _write_json(store_path(no), store, indent=None)
            cnt["backfill"] += 1
        if write_public(full, store):
            cnt["changed"] += 1
        cnt["ok"] += 1
    log("완료: 지문 있음 %d · 잠김 %d · 지문 없음(잠김 아님) %d · 생성TC 반영 %d · 바뀐 파일 %d%s%s"
        % (cnt["ok"], cnt["locked"], cnt["nostmt"], cnt["tc"], cnt["changed"],
           (" · 보관소 채움 %d" % cnt["backfill"]) if cnt["backfill"] else "",
           (" · 건너뜀 %d" % cnt["bad"]) if cnt["bad"] else ""))
    return cnt


# ── 단건: fetch_problem.py 가 쓰는 입구 ─────────────────────────
def parse_ref(ref):
    """ct:386(트레일) · ct:f386(기출) · ct:<alias> · 386 · 카드/기출 URL → 조회 키."""
    r = (ref or "").strip()
    if r.lower().startswith("ct:"):
        r = r[3:].strip()
        if re.fullmatch(r"[fF]\d{1,11}", r):
            return ("no", r.lower())              # ct:f386 — 기출 번호
        if r and not re.fullmatch(r"\d{1,11}", r) and "/" not in r:
            return ("alias", r)                   # ct:ai-robot
    if re.fullmatch(r"\d{1,11}", r):
        return ("no", r)
    m = RE_CARD.search(r)
    if m:
        return ("card", m.group(1))
    m = RE_FREQ.search(r)
    if m:
        return ("freq", m.group(1), m.group(2))
    m = RE_PROB.search(r)
    if m:
        return ("alias", m.group(1))
    raise CTError("❌ 코드트리 주소를 해석하지 못했습니다: %s" % r[:80])


def find_item(cat, key):
    items = (cat or {}).get("items") or []
    kind = key[0]
    for it in items:
        if kind == "no" and it.get("no") == key[1]:
            return it
        if kind == "alias" and it.get("alias") == key[1]:
            return it
        if kind in ("card", "freq"):
            for u in [it.get("url", "")] + [a.get("url", "") for a in it.get("also") or []]:
                if _url_key(u) == key:
                    return it
    return None


def lookup_item(sess, key):
    """카탈로그에 없는 카드/기출 URL → API 로 최소 항목을 만든다(새로 생긴 카드 등)."""
    if key[0] == "card":
        x = sess.api(CARD % key[1])
        b = x.get("b") if isinstance(x.get("b"), dict) else {}
        if x.get("s") != 200 or b.get("problem_id") is None:
            raise CTError("❌ 코드트리 카드를 찾지 못했습니다: %s (HTTP %s)" % (key[1], x.get("s")))
        it = {"no": ct_no("trail", b["problem_id"]), "title": b.get("name", ""),
              "alias": b.get("problem_alias", ""), "pid": b["problem_id"],
              "group": b.get("trail_alias", ""),
              "kind": "trail", "lesson": b.get("lesson_name", ""), "card": key[1],
              "card_type": b.get("card_type", ""), "level": b.get("level", ""),
              "url": CARD_URL % key[1]}
    elif key[0] == "freq":
        x = sess.api(FMETA % key[2])
        b = x.get("b") if isinstance(x.get("b"), dict) else {}
        if x.get("s") != 200 or b.get("problem_id") is None:
            raise CTError("❌ 코드트리 기출을 찾지 못했습니다: %s (HTTP %s)" % (key[2], x.get("s")))
        it = {"no": ct_no("frequent", b["problem_id"]), "title": b.get("name", ""),
              "alias": b.get("problem_alias", ""), "pid": b["problem_id"],
              "group": key[1], "kind": "frequent",
              "origin": b.get("origin", ""), "url": FREQ_URL % (key[1], key[2])}
    else:
        raise CTError("❌ 카탈로그(_meta/codetree_list.json)에 없는 문제입니다: %s\n"
                      "   코드트리 문제 URL 로 주거나 먼저 python _meta/crawl_codetree.py list"
                      % ":".join(key[1:]))
    pt = b.get("problem_type") or ""
    if pt and pt != CODE_BLOCK:
        it["ptype"] = pt
    return it


def fetch_one(ref, save=True, log=None):
    """코드트리 URL(트레일 카드·기출) 또는 번호(ct:386 트레일 / ct:f386 기출) 하나 → 전체 dict.

    돌려주는 dict 에는 화면에 그릴 지문·입출력·제약·힌트·예제가 **다 들어 있다**(허브 /fetch 용).
    save=True 면 보관소(tc_store)와 문제 파일(problems/codetree — 스위치에 따라 지문 포함/메타만)에 쓴다.
    ⚠️ 돌려받은 dict 를 그대로 repo 에 쓰지 말 것 — 문제 파일은 write_public()(= public_part) 로만.
    403(잠김)이면 locked=True 인 메타만 돌려준다(지문 없음).
    """
    log = log or _err
    key = parse_ref(ref)
    cat = load_list()
    it = find_item(cat, key)
    in_cat = it is not None
    if it is None and key[0] in ("no", "alias"):
        lookup_item(None, key)                    # 번호·alias 는 카탈로그로만 찾는다 → 브라우저 열기 전에 안내
    with Session(log) as s:
        if it is None:
            it = lookup_item(s, key)
        res, stop = s.api_many([content_path(it["alias"], it["kind"])])
        x = res[0]
    if x is None:
        raise Stopped(stop or "neterr", "문제 가져오기")
    st, d, changed, why = apply_result(it, x, save=save)
    if st == "fail":
        raise CTError("❌ 코드트리 문제를 못 받았습니다: %s → %s" % (it.get("no"), why))
    if save and in_cat and changed:
        save_list(cat)
    return d


# ── CLI ───────────────────────────────────────────────────────
def main(argv=None):
    # 콘솔이 cp949 여도 이모지 출력에서 죽지 않게(긴 크롤링이 print 하나로 끊기지 않도록).
    for f in (sys.stdout, sys.stderr):
        try:
            f.reconfigure(errors="replace")
        except Exception:
            pass
    ap = argparse.ArgumentParser(
        description="코드트리 트레일·기출 수집 (지문 공개 여부는 _meta/judge_config.json 의 privateSites)")
    sp = ap.add_subparsers(dest="cmd")
    pl = sp.add_parser("list", help="카탈로그 → _meta/codetree_list.json")
    pl.add_argument("--refresh", action="store_true", help="카드→문제번호 매핑도 전부 새로 조회")
    for name in ("fetch", "all"):
        p = sp.add_parser(name, help="지문·예제 수집" if name == "fetch" else "list → fetch")
        p.add_argument("--group", action="append", choices=GROUP_KEYS, help="그룹만(여러 번 가능)")
        p.add_argument("--no", action="append", default=[], help="문제 번호만(여러 번 가능)")
        p.add_argument("--limit", type=int, default=0, help="앞에서 N개만")
        p.add_argument("--force", action="store_true", help="이미 받은 것도 다시")
        p.add_argument("--retry-locked", action="store_true", help="403(잠김)이던 것도 다시")
        if name == "all":
            p.add_argument("--refresh", action="store_true")
    pr = sp.add_parser("rebuild-public",
                       help="privateSites 스위치·보관소(생성 TC 포함)에 맞춰 문제 파일 다시 만들기"
                            "(다시 받지 않음, 브라우저 불필요)")
    pr.add_argument("--no", action="append", default=[], help="이 번호만(여러 번 가능)")
    a = ap.parse_args(argv)
    if not a.cmd:
        ap.print_help()
        return 1
    if a.cmd == "rebuild-public":
        try:
            rebuild_public(a.no)
        except CTError as e:
            _out(str(e))
            return 1
        return 0

    sess = Session(log=_out)
    try:
        if a.cmd in ("list", "all"):
            cat = build_list(sess, refresh=a.refresh)
        if a.cmd in ("fetch", "all"):
            cat = load_list()
            if not cat:
                _out("❌ 카탈로그가 없습니다 → 먼저 python _meta/crawl_codetree.py list")
                return 1
            if cat.get("partial"):
                _out("   ⚠️ 카탈로그가 부분본입니다(list 가 중간에 멈춤) — 있는 것만 받습니다")
            todo, n_exist, n_locked = select_items(cat, a.group, a.no, a.limit, a.force,
                                                   a.retry_locked)
            _out("대상 %d문제  (이미 받음 %d · 잠김 건너뜀 %d)" % (len(todo), n_exist, n_locked))
            if todo:
                run_fetch(sess, cat, todo)
        return 0
    except Stopped as e:
        _out(str(e))
        return 3
    except CTError as e:
        _out(str(e))
        return 1
    except KeyboardInterrupt:
        _out("\n중단됨 — 받은 것까지는 저장됨(다시 실행하면 이어서)")
        return 130
    finally:
        sess.close()


if __name__ == "__main__":
    sys.exit(main())
