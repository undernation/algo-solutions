"""
코테 잔디 생성 → assets/heatmap.svg + assets/heatmap.html + README + HEATMAP.md

데이터 우선순위(병합):
  1) _meta/history.json           (누적 — PC가 바뀌어도 유지)
  2) 옵시디언 실수노트             (있을 때만. 전체 이력의 진실 소스)
  3) repo 풀이 파일의 '풀이일'      (boj/*.py, swea/*.py, codetree/*.py)

history.json 형식:
  {"2026-08-11": {"count": 2, "items": ["SWEA 2382 미생물 격리 (품)", ...]}}
  (구버전 int 값도 읽음)

사용법:
    python _meta/build_heatmap.py
    python _meta/build_heatmap.py --year 2026
"""
import os, re, io, json, glob, datetime, sys, html, subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIST = os.path.join(ROOT, "_meta", "history.json")
# 삭제 표식. 사용자가 지운 기록은 코드 파일이 남아 있어도 되살아나면 안 된다.
# 형식: ["2026-08-12|BOJ|1159", ...]
TOMB = os.path.join(ROOT, "_meta", "deleted.json")
# 코드트리 전체 문제 카탈로그(크롤러 산출물). 번호 없는 옛 기록을 문제에 연결할 때만 읽는다.
CT_LIST = os.path.join(ROOT, "_meta", "codetree_list.json")
ASSETS = os.path.join(ROOT, "assets")
SVG = os.path.join(ASSETS, "heatmap.svg")
HTML = os.path.join(ASSETS, "heatmap.html")
README = os.path.join(ROOT, "README.md")
FULL = os.path.join(ROOT, "HEATMAP.md")

VAULT_CANDIDATES = [
    r"C:/Users/solom/ObsidianVaults/동기화/_cpp_코테/실수모음 (몰랐으면 답보고 혼자 다시 짜기).md",
]

CELL, GAP, PAD_L, PAD_T = 11, 3, 30, 20
COLORS = ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"]
COLORS_DARK = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DOW = ["월", "화", "수", "목", "금", "토", "일"]


# ── 데이터 ─────────────────────────────────────────────────────
def load_history() -> dict:
    if not os.path.exists(HIST):
        return {}
    raw = json.load(io.open(HIST, encoding="utf-8"))
    out = {}
    for k, v in raw.items():
        if isinstance(v, int):                      # 구버전 호환
            out[k] = {"count": v, "items": []}
        else:
            items = []
            for it in v.get("items", []):
                if isinstance(it, dict):
                    items.append(it)
                else:                                   # 구버전 문자열
                    m = re.match(r"(BOJ|SWEA)\s+(\d+)?\s*(.*?)\s*(?:\(([^)]*)\))?$", it)
                    items.append({"site": m.group(1) if m else "BOJ",
                                  "no": (m.group(2) or "") if m else "",
                                  "title": (m.group(3) or "") if m else it,
                                  "status": (m.group(4) or "?") if m else "?"})
            out[k] = {"count": v.get("count", 0), "items": items}
    return out


# 날짜 줄에 "(품)" 같은 괄호 상태가 없고, 바로 다음 줄에 자유 문장으로
# 결과를 적어 둔 기록이 많다. 예:
#     #### 2026-04-06
#     쉽게 풀었음 (못푼문제에서 삭제)
# 예전엔 이런 걸 전부 "?" 로 흘려서 재도전 큐가 부풀었다(28건).
#
# 🚩 이 추론은 **괄호에도 헤딩에도 상태가 전혀 없을 때만** 쓴다.
# 실수노트 본문은 결과가 아니라 과정을 적은 서술문이라, 판정 근거로 쓰면 크게 틀린다:
#   1450  "일반 냅색으로 풀었는데 메모리 초과 발생함"      → '풀었' 만 보면 품(실제 틀림)
#   15972 "답을 봐도 어떻게 풀었는지 이해가 안 간다"       → '풀었'      (실제 못품)
#   19942 "나름 잘 풀었는데 / 틀린 핵심 이유는…"          → '풀었'      (실제 틀림)
#   1463  "아직 dp 개념이 박히지 못했다"                → '못했'      (실제 틀림)
# 실제로 우선순위를 안 두고 돌렸다가 16건이 잘못 뒤집혔다.
#
# 판정 순서 — 한 문장에 여러 단어가 섞이기 때문:
#   "답보고 겨우 풀었다"        → 답을 봤으므로 못품 ("풀었" 보다 앞서 잡아야 함)
#   "틀림 + 시간초과(15분 초과)"  → 틀림
#   "시간초과 … 필요성을 못느껴 삭제" → 못푼문제에서 뺐으므로 품 (소유자 판단, 4659)
# "못푼문제" 의 '푼' 은 '품' 과 다른 글자라 못품 패턴에 걸리지 않는다.
_VS = [
    (re.compile(r"답\s*보고|답봄|답\s*을?\s*봄"), "못품"),
    (re.compile(r"못품|못했|못\s*풀"), "못품"),
    (re.compile(r"삭제"), "품"),
    (re.compile(r"틀림|틀렸"), "틀림"),
    (re.compile(r"시간\s*초과"), "시간초과"),
    (re.compile(r"풀었|풀렸|해결"), "품"),
]


def infer_status(text: str) -> str:
    """날짜 줄 뒤에 붙은 자유 문장에서 결과를 읽는다. 못 읽으면 빈 문자열."""
    for rx, st in _VS:
        if rx.search(text):
            return st
    return ""


_STAT = re.compile(r"(못품|시간초과|틀림|맞음|품)")


def paren_status(text: str) -> str:
    """괄호 안 문구에서 상태를 읽는다. "(시간 초과)" 처럼 띄어쓴 것도 받는다.

    다만 공백만 지우고 부분일치를 허용하면 "(푸는시간 초과)"(= 푸는 데 걸린 시간이
    초과됐다는 본인 표기, 2529)까지 채점 시간초과로 잘못 읽는다. 그래서 상태어가
    한글 뒤에 이어붙은 경우는 배제한다.
    """
    for cand in (text, text.replace(" ", "")):
        m = _STAT.search(cand or "")
        if not m:
            continue
        if m.start() > 0 and re.match(r"[가-힣]", cand[m.start() - 1]):
            continue          # 다른 낱말의 꼬리 — 상태어가 아니다
        return m.group(1)
    return ""


def from_vault() -> dict:
    """실수노트 → 날짜별 {count, items}."""
    path = next((p for p in VAULT_CANDIDATES if os.path.exists(p)), None)
    if not path:
        return {}
    L = io.open(path, encoding="utf-8").read().split("\n")
    heads = [i for i, l in enumerate(L) if l.startswith("## ")]
    # 날짜만 있는 줄과 "2026-04-06 (틀림)" 처럼 괄호 상태가 붙은 줄 둘 다 받는다.
    # (#### 없이 날짜만 적어 둔 초기 기록이 많다)
    DATEL = re.compile(r"^\s*(\d{4}-\d{2}-\d{2})\s*(?:\(([^)]*)\))?\s*$")
    REC = re.compile(r"^####\s+(\d{4}-\d{2}-\d{2})\s*(?:\(([^)]*)\))?")
    STAT = re.compile(r"(못품|시간초과|틀림|맞음|품)")
    out = {}
    for n, s in enumerate(heads):
        e = heads[n + 1] if n + 1 < len(heads) else len(L)
        head = L[s][3:].strip()
        title = re.split(r"\s*\(", head)[0].strip()
        if not title or title.startswith(("추가", "왜 ", "네 말", "예시")):
            continue
        site = "SWEA" if "expert" in head.lower() else "BOJ"
        # 헤딩 괄호를 전부 훑어 상태를 찾는다. 마지막 것을 쓴다.
        #   "## 2869 (품) (python)"   → 품   (끝 괄호만 보면 python 이라 놓쳤다)
        #   "## 3197 (시간초과) (못품)" → 못품
        head_stat = ""
        for g in re.findall(r"\(([^)]*)\)", head):
            head_stat = paren_status(g) or head_stat

        def tail(i):
            """날짜 줄 i 다음의 설명 두 줄(빈 줄·코드펜스 제외)을 이어 붙인다."""
            got, j = [], i + 1
            while j < e and len(got) < 2:
                t = L[j].strip()
                j += 1
                if not t:
                    continue
                if t.startswith("```") or t.startswith("## ") or \
                        REC.match(L[j - 1]) or DATEL.match(L[j - 1]):
                    break
                got.append(t)
            return " ".join(got)

        seen, fence = {}, False
        for i in range(s + 1, e):
            x = L[i]
            if x.strip().startswith("```"):
                fence = not fence
                continue
            if fence:
                continue
            m = REC.match(x) or DATEL.match(x)
            if not m:
                continue
            # 신뢰 순서: 날짜 줄 괄호(3) > 헤딩 괄호(2) > 다음 줄 자유 문장(1).
            # 자유 문장은 근거가 아예 없을 때의 마지막 수단이다(위 주석 참고).
            # 같은 날짜가 두 번 적힌 경우(1486 은 "#### 06-09 (못품)" 과 맨 날짜줄이
            # 둘 다 있다) 근거가 약한 쪽이 덮어쓰지 않도록 등급으로 막는다.
            ps = paren_status(m.group(2) or "")
            if ps:
                st, rank = ps, 3
            elif head_stat:
                st, rank = head_stat, 2
            else:
                st, rank = infer_status(tail(i)), 1
            d0 = m.group(1)
            if d0 not in seen or rank > seen[d0][1]:
                seen[d0] = (st, rank)
        m = re.match(r"(\d+)\s*\.?\s*(.*)", title)
        no, nm = (m.group(1), m.group(2).strip()) if m else ("", title)
        for d, (st, _rank) in seen.items():
            rec = out.setdefault(d, {"count": 0, "items": []})
            rec["count"] += 1
            rec["items"].append({"site": site, "no": no, "title": nm, "status": st or "?"})
    return out


# 풀이 파일 폴더. 헤더 첫 줄은 "<SITE> <번호>  <제목>" 이다(server.build_header).
# 코드트리(2026-09-23~)는 codetree/<no>_<제목>.py — 헤더가 "CT f386  AI 로봇청소기".
# 코드트리 번호는 숫자로 못박지 않는다: 기출 problem_id 가 트레일 problem_id 와 106개 겹쳐
# (342 = 트레일 '직사각형 별표 출력하기' = 기출 '고대 문명 유적 탐사') 기출은 "f"+id 를 쓴다.
# 서버가 받는 번호 형식은 [A-Za-z0-9_-]{1,12}. BOJ/SWEA 정규식은 예전 그대로 둔다
# (codetree/ 폴더 파일에만 CT 정규식을 쓴다).
SOL_DIRS = ("boj", "swea", "codetree")
_SOL_HEAD = re.compile(r"^\s*(BOJ|SWEA)\s+(\d+)\s+(.*)$", re.M)
_CT_HEAD = re.compile(r"^\s*(CT)\s+([A-Za-z0-9_-]{1,12})\s+(.*)$", re.M)


def from_repo() -> dict:
    out = {}
    for f in [x for s in SOL_DIRS for x in glob.glob(os.path.join(ROOT, s, "*.py"))]:
        src = io.open(f, encoding="utf-8").read()
        m = re.search(r"풀이일\s*:\s*(\d{4}-\d{2}-\d{2})", src)
        if not m:
            continue
        d = m.group(1)
        ct_dir = os.path.basename(os.path.dirname(f)) == "codetree"
        t = (_CT_HEAD if ct_dir else _SOL_HEAD).search(src)
        st = re.search(r"결과\s*:\s*(\S+)", src)
        base = os.path.basename(f)
        # 헤더를 못 읽으면 예전처럼 BOJ 로 둔다. 코드트리 폴더만은 폴더가 곧 사이트이고
        # 파일명 앞부분이 번호라서 그걸 쓴다 — BOJ 로 두면 엉뚱한 백준 문제가 된다.
        fm = re.match(r"([A-Za-z0-9-]{1,12})_", base) if (ct_dir and not t) else None
        item = {"site": t.group(1) if t else ("CT" if ct_dir else "BOJ"),
                "no": t.group(2) if t else (fm.group(1) if fm else ""),
                "title": t.group(3).strip() if t else base,
                "status": st.group(1) if st else "?",
                "file": os.path.relpath(f, ROOT).replace(os.sep, "/")}
        rec = out.setdefault(d, {"count": 0, "items": []})
        rec["count"] += 1
        rec["items"].append(item)
    return out


def _ikey(it):
    """item 동일성 판정 키. 문자열 item(구버전)은 원문 그대로.

    번호 없는 기록(실수노트 '## 여왕개미', '## 프로그래머스 타겟 넘버' …)은 제목으로 가른다 —
    대시보드 key() 와 같은 모양 "BOJ/~제목". 예전엔 전부 "BOJ/" 라, 같은 날 두 개 이상이면
    merge 가 하나로 뭉갰다: 제목은 앞 기록, 상태는 뒤 기록이 남고 나머지는 목록에서 사라졌다
    (count 만 실수노트 값으로 맞아 보였다). 2026-05 프로그래머스 연습 22일치가 그랬고,
    06-19 '자물쇠와 열쇠' 는 옆 기록의 (품)을 달고 있었다(실수노트엔 (틀림)). 2026-09-23 수정.
    번호 있는 항목은 예전 키 그대로다(삭제 표식·허브 저장분과 맞물려 있다).
    """
    if isinstance(it, str):
        return it.strip()
    no = it.get("no", "")
    if no is None or not str(no).strip():
        return "%s/~%s" % (it.get("site", ""), (it.get("title") or "").strip() or "이름없음")
    return "%s/%s" % (it.get("site", ""), no)


def load_tombstones():
    if not os.path.exists(TOMB):
        return set()
    try:
        return set(json.load(io.open(TOMB, encoding="utf-8")) or [])
    except Exception:
        return set()


def apply_tombstones(data: dict, tomb: set) -> dict:
    """삭제 표식에 해당하는 기록을 제거(빈 날짜는 통째로 삭제)."""
    if not tomb:
        return data
    for day in list(data):
        rec = data[day]
        keep = []
        for it in rec.get("items", []):
            if isinstance(it, dict):
                k = "%s|%s|%s" % (day, it.get("site", ""), it.get("no", ""))
                if k in tomb:
                    continue
            keep.append(it)
        gone = len(rec.get("items", [])) - len(keep)
        if gone:
            rec["items"] = keep
            rec["count"] = max(0, rec.get("count", 0) - gone)
            if not keep and rec["count"] <= 0:
                data.pop(day, None)
    return data


def _fill(a, b, status_first):
    """같은 문제의 두 기록을 합친다. 어느 쪽 정보도 버리지 않는다.

    통째로 갈아끼우면 허브가 저장한 채점 결과(file·passed·elapsed)가 날아간다.
    그래서 빈 칸만 채우고, 상태만 우선순위로 고른다.
    status_first=True 는 "실수노트가 진실의 소스" 라는 규칙을 반영한 것 —
    캐시(history.json)에 남은 옛 판정보다 방금 읽은 실수노트를 앞세운다.
    (실제 사고: 15926 이 실수노트에 "(맞음)" 인데 캐시의 "못품" 이 계속 이겼다)
    """
    if not isinstance(a, dict):
        return b if isinstance(b, dict) else a
    if not isinstance(b, dict):
        return a
    out = dict(a)
    for k, v in b.items():
        if k != "status" and k != "attempts" and v and not out.get(k):
            out[k] = v
    # 제출 회차는 어느 쪽도 버리지 않고 합집합으로 모은다. 빈 칸 채우기 규칙에
    # 맡기면 한쪽 attempts 가 이미 있다는 이유로 다른 쪽이 통째로 버려진다.
    att, seen_at = [], set()
    for src in (a.get("attempts"), b.get("attempts")):
        for x in (src or []):
            if not isinstance(x, dict):
                continue
            k2 = (x.get("at") or "", x.get("status") or "")
            if k2 in seen_at:
                continue
            seen_at.add(k2)
            att.append(x)
    if att:
        out["attempts"] = sorted(att, key=lambda x: x.get("at") or "")
    sa = a.get("status") or "?"
    sb = b.get("status") or "?"
    if sb != "?" and (status_first or sa == "?"):
        out["status"] = sb
    else:
        out["status"] = sa if sa != "?" else sb
    return out


def merge(base: dict, add: dict, status_first: bool = False) -> dict:
    """날짜별로 item 을 (site, no) 기준 합집합으로 병합.

    예전엔 count 가 큰 쪽 items 로 통째로 갈아끼웠는데, 그러면
    같은 날 실수노트 2건 + 허브 저장 1건 일 때 허브 저장분이 통째로 사라졌다.
    (실제 사고: 2026-08-11 BOJ 1159 가 대시보드에 안 뜸)
    정보가 더 많은 item(제목·상태·파일 있는 쪽)을 우선 채택한다.
    """
    for k, v in add.items():
        cur = base.setdefault(k, {"count": 0, "items": []})
        seen = {}
        order = []
        for it in list(cur["items"]):
            key = _ikey(it)
            if key not in seen:
                seen[key] = it
                order.append(key)
        for it in list(v["items"]):
            key = _ikey(it)
            if key not in seen:
                seen[key] = it
                order.append(key)
            else:
                seen[key] = _fill(seen[key], it, status_first)
        cur["items"] = [seen[k2] for k2 in order]
        # items 없이 count 만 있는 구버전 기록도 있으므로 셋 중 최대값을 쓴다.
        cur["count"] = max(len(cur["items"]), cur["count"], v["count"])
    return base


# ── 번호 없는 옛 기록 → 코드트리 문제 연결 (2026-09-23) ──────────────
# 실수노트(SSOT)의 코드트리 기록은 "## 코드트리 나무박멸 (틀림)", "## 여왕개미" 처럼
# 번호가 없다. from_vault() 는 번호가 없으면 site="BOJ", no="" 인 '제목만 있는 항목'을
# 만들어서, 대시보드에선 백준 칸에 번호 없이 떠 있고 문제 페이지로도 못 간다(61건).
# 코드트리 카탈로그의 제목과 맞춰 CT 번호를 붙인다.
#
# 보수적으로만 붙인다. 같은 '제목만 있는 항목' 에 프로그래머스(타겟 넘버·피로도·조이스틱…)와
# SWEA 기록이 섞여 있어서, 헐겁게 맞추면 남의 문제가 코드트리로 둔갑한다.
#   · site 가 BOJ 이고 no 가 빈 항목만. 제목에 프로그래머스/SW Expert 가 있으면 손대지 않는다.
#   · 제목에 '코드트리' 가 있으면 카탈로그 전체(트레일+기출)에서, 없으면 기출에서만 찾는다.
#     실수노트에 번호 없이 적은 건 기출(삼성·HSAT)이었고, 트레일은 입문 연습문제가 천 개가
#     넘어 흔한 제목이 우연히 겹칠 수 있다.
#   · 정규화한 제목이 '정확히 한 문제' 와 맞을 때만. 원래 제목은 title_raw 로 남긴다.
# history.json 과 실수노트 양쪽에 merge '전에' 같은 규칙을 적용해야 한다 — 한쪽만 바꾸면
# (site, no) 키가 달라 같은 날 CT 항목과 BOJ 제목 항목이 둘 다 남는다(잔디 count +1).
# 카탈로그가 없으면(크롤링 전) 아무것도 안 한다 = 예전 동작 그대로.
# (이 작업 중에 번호 없는 항목끼리 키가 "BOJ/" 로 같아 뭉개지던 것도 드러나 _ikey 에서 고쳤다.)
_CT_WORD = re.compile(r"코드\s*트리")
_CT_NOISE = re.compile(r"\(\s*코드\s*트리\s*\)|코드\s*트리")
# 번호도 괄호도 없이 "## 해적선장 코디 못품." 처럼 상태를 제목 끝에 붙여 쓴 기록이 있다.
# 띄어쓴 경우만 뗀다 — 붙여 쓴 "…작품" 같은 제목 끝 글자를 상태어로 오인하지 않게.
_CT_TAIL = re.compile(r"\s+(?:못품|품|틀림|맞음|시간\s*초과)$")
_CT_PUNCT = re.compile(r"[\s.,:;·\-‐–—~'\"‘’“”!?！？：]+")
_CT_SKIP = re.compile(r"프로그래머스|programmers|sw\s*expert|swea|백준", re.I)


def ct_norm(title) -> str:
    """제목 대조용 정규화. 카탈로그 쪽과 기록 쪽에 반드시 같은 함수를 쓴다."""
    s = _CT_NOISE.sub(" ", title or "").strip().rstrip(".").strip()
    s = _CT_TAIL.sub("", s).strip().rstrip(".")
    return _CT_PUNCT.sub("", s).lower()


def load_ct_titles():
    """카탈로그 → (전체, 기출) 두 표. 표 = 정규화 제목 → {problem_id: 카탈로그 제목}.

    같은 문제가 트레일과 기출에 둘 다 나오면 카탈로그는 첫 번째(트레일)만 items 에 두고
    기출 쪽은 also 로 붙인다(ct_spec §4-1). 그래서 기출 여부는 also 까지 봐야 한다.
    """
    try:
        cat = json.load(io.open(CT_LIST, encoding="utf-8"))
    except Exception:
        return {}, {}
    if not isinstance(cat, dict):
        return {}, {}
    freq_groups = set(g.get("key") for g in (cat.get("groups") or [])
                      if isinstance(g, dict) and g.get("kind") == "frequent")
    every, freq = {}, {}
    for it in cat.get("items") or []:
        if not isinstance(it, dict):
            continue
        no, title = str(it.get("no") or "").strip(), (it.get("title") or "").strip()
        k = ct_norm(title)
        if not no or not k:
            continue
        every.setdefault(k, {})[no] = title
        if any(isinstance(x, dict) and (x.get("kind") == "frequent" or x.get("group") in freq_groups)
               for x in [it] + list(it.get("also") or [])):
            freq.setdefault(k, {})[no] = title
    return every, freq


def ct_sticky(data: dict) -> dict:
    """이전 빌드가 붙여 둔 짝: 정규화 title_raw → {problem_id: 제목}.

    붙인 결과는 history.json 에 남는다. 나중에 카탈로그에 같은 제목의 새 문제가 생기거나
    (모호해짐) 카탈로그가 잠깐 없거나 덜 받아진 상태면, 실수노트 쪽만 못 붙어 같은 날
    CT 항목과 BOJ 제목 항목이 겹친다. 그때 이 짝을 빌려 쓴다.
    ⚠️ 카탈로그보다 앞세우지는 않는다. 카탈로그가 '정확히 한 문제' 를 대면 그게 이기고,
    예전에 붙인 항목도 따라 옮긴다(link_codetree). 번호 체계가 바뀌는 일이 실제로
    있었다 — 기출 problem_id 가 트레일 problem_id 와 겹치는 게 확인돼(342 = 트레일
    '직사각형 별표 출력하기' = 기출 '고대 문명 유적 탐사') 기출 번호를 바꿔야 했다.
    짝을 앞세웠다면 옛 번호가 history.json 에 영영 박혔을 것이다.
    """
    out = {}
    for rec in data.values():
        for it in rec.get("items", []):
            if isinstance(it, dict) and it.get("site") == "CT" and it.get("title_raw") \
                    and str(it.get("no") or "").strip():
                out.setdefault(ct_norm(it["title_raw"]), {})[str(it["no"]).strip()] = \
                    it.get("title") or ""
    return out


def link_codetree(data: dict, every: dict, freq: dict, sticky: dict) -> int:
    """번호 없는 BOJ 제목 항목 중 코드트리 문제로 확실한 것에 CT 번호를 붙인다(제자리 수정).

    예전 빌드가 붙인 항목(title_raw 있음)도 다시 본다 — 카탈로그가 다른 번호를 '정확히
    하나' 대면 따라 옮기고, 카탈로그가 못 정하면 그대로 둔다. 실수노트 쪽도 같은 제목이라
    같은 답이 나오므로 양쪽이 어긋나지 않는다.
    site·no·title 만 바꾸고 status·attempts·file 등은 건드리지 않는다. 바꾼 개수를 돌려준다.
    """
    n = 0
    for rec in data.values():
        hit_day = False
        for it in rec.get("items", []):
            if not isinstance(it, dict):
                continue
            if it.get("site") == "BOJ" and not str(it.get("no") or "").strip():
                raw = it.get("title") or ""
            elif it.get("site") == "CT" and it.get("title_raw"):
                raw = it["title_raw"]
            else:
                continue
            k = ct_norm(raw)
            if not k or _CT_SKIP.search(raw):
                continue
            hit = (every if _CT_WORD.search(raw) else freq).get(k) or {}
            if len(hit) != 1:
                hit = sticky.get(k) or {}     # 카탈로그가 못 정하면 예전에 붙인 짝
            if len(hit) != 1:
                continue                      # 없거나 둘 이상 — 모르면 안 붙인다
            no, title = next(iter(hit.items()))
            title = title or raw
            if it.get("site") == "CT" and str(it.get("no")) == no and it.get("title") == title:
                continue                      # 이미 그대로
            it["site"], it["no"], it["title"] = "CT", no, title
            it["title_raw"] = raw
            n += 1
            hit_day = True
        if hit_day:
            # 같은 날 이미 CT 항목(허브 저장분)이 있었거나 제목 두 개가 같은 문제로 붙었으면
            # 키가 겹친다. merge() 는 base 쪽 중복을 _fill 없이 버리고, 실수노트가 없는
            # 날(Actions·클라우드)엔 merge 자체가 그 날을 안 지나가 중복이 그대로 남는다.
            # 여기서 합쳐 둔다. count 는 줄이지 않는다(잔디는 '큰 값 채택' 규칙).
            # CT 키만 본다 — 이번에 새로 겹칠 수 있는 건 방금 CT 로 붙인 항목뿐이고,
            # 나머지 항목의 중복 처리는 예전처럼 merge() 에 맡긴다.
            pos, items = {}, []
            for it in rec["items"]:
                key = _ikey(it) if isinstance(it, dict) and it.get("site") == "CT" else None
                if key is None or key not in pos:
                    if key is not None:
                        pos[key] = len(items)
                    items.append(it)
                else:
                    items[pos[key]] = _fill(items[pos[key]], it, False)
            rec["items"] = items
    return n


def build_rows(data: dict) -> list:
    """날짜별 기록 → 대시보드용 '제출 이력' 목록(최신 날짜 먼저).

    한 문제를 같은 날 여러 번 냈으면 **회차마다 한 줄**을 만든다.
    items 는 잔디 count(= 그날 시도한 '문제 수') 때문에 문제당 하나로 묶여 있고,
    회차는 그 안의 attempts 에 들어 있다. 예전엔 허브가 재제출 때 이전 기록을
    지우고 새로 넣어서 "틀렸다가 다시 풀어 맞힘" 의 앞부분이 사라졌다.
    """
    rows = []
    for dk in sorted(data, reverse=True):
        for it in data[dk]["items"]:
            if isinstance(it, str):
                continue
            base = {"date": dk, "site": it.get("site", ""),
                    "no": it.get("no", ""), "title": it.get("title", ""),
                    "status": it.get("status", "?"), "file": it.get("file", ""),
                    "passed": it.get("passed"), "total": it.get("total"),
                    "elapsed": it.get("elapsed"), "verdict": it.get("verdict", ""),
                    # 허브로 저장한 기록에만 있다. 옛 기록·실수노트 유래는 빈 값.
                    "at": it.get("at", "")}
            att = [x for x in (it.get("attempts") or []) if isinstance(x, dict)]
            if len(att) < 2:
                rows.append(base)
                continue
            for i, a in enumerate(sorted(att, key=lambda x: x.get("at") or "")):
                r = dict(base)
                r.update({"status": a.get("status") or base["status"],
                          "at": a.get("at") or "",
                          "file": a.get("file") or base["file"],
                          "passed": a.get("passed"), "total": a.get("total"),
                          "elapsed": a.get("elapsed"),
                          "verdict": a.get("verdict", ""),
                          # 몇 회차 제출인지. 대시보드가 "2/3회" 배지로 보여준다.
                          "try": i + 1, "tries": len(att)})
                rows.append(r)
    return rows


# ── 회차별 코드: 그 시각의 커밋 ──────────────────────────────────
# 풀이 파일은 문제당 하나라 재제출하면 덮어써진다. 그래서 '제출 이력' 의 옛 회차
# "보기" 가 전부 최신 코드를 보여줬다(2026-09-10, 27183 에서 발견). 허브는 저장마다
# 커밋하므로 옛 회차의 코드는 git 이력에 그대로 있다. 회차마다 그 시각의 커밋을
# 붙여 두면 대시보드가 raw.githubusercontent 에서 그 커밋의 파일을 연다.
# 최신 커밋(= 현재 파일)인 회차에는 붙이지 않는다 — 로컬 파일이 더 빠르고 CDN 지연이 없다.
# Actions 는 fetch-depth 0 이어야 한다(얕은 클론이면 git log 가 비어 그냥 건너뛴다).
_COMMITS = {}


def _file_commits(rel: str) -> list:
    """파일을 건드린 커밋 [(short_sha, 작성시각 UTC naive)] — 오래된 것부터."""
    if rel in _COMMITS:
        return _COMMITS[rel]
    out = []
    try:
        r = subprocess.run(["git", "log", "--format=%h|%aI", "--", rel], cwd=ROOT,
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        for line in (r.stdout or "").splitlines():
            if "|" not in line:
                continue
            sha, iso = line.split("|", 1)
            iso = iso.strip()
            # git 은 UTC 커밋(클라우드 허브·Actions 가 만든 것)을 "…T04:04:24Z" 로 찍는데,
            # fromisoformat 은 3.11 부터 'Z' 를 읽는다. 클라우드 VM 은 3.8 이라 그런 커밋이
            # 전부 ValueError 로 빠져 회차 ↔ 커밋 짝이 어긋났다(2026-09-23 PyPy 3.7 대조로 발견).
            if iso.endswith("Z"):
                iso = iso[:-1] + "+00:00"
            try:
                t = datetime.datetime.fromisoformat(iso)
            except ValueError:
                continue
            if t.tzinfo is not None:
                t = t.astimezone(datetime.timezone.utc).replace(tzinfo=None)
            out.append((sha.strip(), t))
    except Exception:
        out = []
    out.sort(key=lambda x: x[1])
    _COMMITS[rel] = out
    return out


def annotate_commits(rows: list) -> None:
    """허브로 저장한 회차(at 있음)에 그 회차의 커밋 해시를 붙인다.

    회차 시각은 KST, 커밋 시각은 UTC 로 비교한다. at 은 파일을 쓰기 전에 찍히므로
    커밋은 그 몇 초~몇 분 뒤다. 같은 파일의 회차 수와 커밋 수가 같으면 순서대로
    짝짓고(날짜를 과거로 고쳐 저장한 경우도 맞는다), 아니면 시각 창으로 찾는다.
    """
    by_file = {}
    for r in rows:
        if r.get("file") and r.get("at"):
            by_file.setdefault(r["file"], []).append(r)
    for rel, rs in by_file.items():
        commits = _file_commits(rel)
        if len(commits) < 2:
            continue
        latest = commits[-1][0]
        rs.sort(key=lambda x: (x.get("date", ""), x.get("at", "")))
        if len(rs) == len(commits):
            pairs = list(zip(rs, commits))
        else:
            pairs = []
            for r in rs:
                try:
                    t = datetime.datetime.strptime("%s %s" % (r["date"], r["at"]), "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    continue
                t_utc = t - datetime.timedelta(hours=9)
                cand = [c for c in commits
                        if t_utc - datetime.timedelta(seconds=90) <= c[1] <= t_utc + datetime.timedelta(hours=12)]
                if cand:
                    pairs.append((r, cand[0]))
        for r, (sha, _) in pairs:
            if sha != latest:
                r["commit"] = sha


# ── 렌더 ───────────────────────────────────────────────────────
def fmt(it) -> str:
    """구조화 item -> 표시 문자열"""
    if isinstance(it, str):
        return it
    no = (" " + it["no"]) if it.get("no") else ""
    st = (" (%s)" % it["status"]) if it.get("status") and it["status"] != "?" else ""
    return "%s%s %s%s" % (it.get("site", ""), no, it.get("title", ""), st)


def level(n):
    return 0 if n <= 0 else 1 if n == 1 else 2 if n == 2 else 3 if n == 3 else 4


def grid(year):
    start, end = datetime.date(year, 1, 1), datetime.date(year, 12, 31)
    g0 = start - datetime.timedelta(days=(start.weekday() + 1) % 7)
    return g0, ((end - g0).days // 7) + 1


def tip(d: datetime.date, rec: dict) -> str:
    head = "%s (%s) — %d문제" % (d.isoformat(), DOW[d.weekday()], rec["count"])
    if not rec["items"]:
        return head
    return head + "\n" + "\n".join("· " + fmt(x) for x in rec["items"])


def render_svg(data, year):
    g0, weeks = grid(year)
    W = PAD_L + weeks * (CELL + GAP) + 10
    H = PAD_T + 7 * (CELL + GAP) + 24
    light = "".join(".l%d{fill:%s}" % (i, COLORS[i]) for i in range(5))
    dark = "".join(".l%d{fill:%s}" % (i, COLORS_DARK[i]) for i in range(5))
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'
           % (W, H, W, H),
           "<style>%s .lbl{fill:#57606a;font:9px -apple-system,Segoe UI,sans-serif}"
           "@media(prefers-color-scheme:dark){%s .lbl{fill:#8b949e}}</style>" % (light, dark)]
    last_m = -1
    for w in range(weeks):
        d = g0 + datetime.timedelta(days=w * 7)
        if d.year == year and d.month != last_m and d.day <= 7:
            out.append('<text class="lbl" x="%d" y="%d">%s</text>'
                       % (PAD_L + w * (CELL + GAP), PAD_T - 6, MONTHS[d.month - 1]))
            last_m = d.month
    for i, nm in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        out.append('<text class="lbl" x="0" y="%d">%s</text>'
                   % (PAD_T + i * (CELL + GAP) + CELL - 1, nm))
    total = 0
    for w in range(weeks):
        for dow in range(7):
            d = g0 + datetime.timedelta(days=w * 7 + dow)
            if d.year != year:
                continue
            rec = data.get(d.isoformat(), {"count": 0, "items": []})
            total += rec["count"]
            out.append('<rect class="l%d" x="%d" y="%d" width="%d" height="%d" rx="2">'
                       '<title>%s</title></rect>'
                       % (level(rec["count"]), PAD_L + w * (CELL + GAP),
                          PAD_T + dow * (CELL + GAP), CELL, CELL,
                          html.escape(tip(d, rec))))
    lx, ly = W - 10 - 5 * (CELL + 2) - 60, H - 12
    out.append('<text class="lbl" x="%d" y="%d">Less</text>' % (lx, ly + 8))
    for i in range(5):
        out.append('<rect class="l%d" x="%d" y="%d" width="%d" height="%d" rx="2"/>'
                   % (i, lx + 28 + i * (CELL + 2), ly, CELL, CELL))
    out.append('<text class="lbl" x="%d" y="%d">More</text>' % (lx + 28 + 5 * (CELL + 2) + 3, ly + 8))
    out.append("</svg>")
    return "\n".join(out), total


def render_html(data, year, total, active, best):
    """백준 프로필 스타일 대시보드 (GitHub Pages 진입점)."""
    from _dashboard_tpl import render_dashboard
    g0, weeks = grid(year)
    cells = []
    for w in range(weeks):
        for dow in range(7):
            d = g0 + datetime.timedelta(days=w * 7 + dow)
            if d.year != year:
                continue
            rec = data.get(d.isoformat(), {"count": 0, "items": []})
            # 그 달이 시작되는 주 열에 월 라벨을 달아준다(GitHub 잔디와 같은 방식)
            cells.append({"w": w + 1, "r": dow + 1, "d": d.isoformat(),
                          "m": (d.month if d.day <= 7 and dow == 0 else 0),
                          "dw": DOW[d.weekday()], "n": rec["count"],
                          "lv": level(rec["count"])})
    rows = build_rows(data)
    annotate_commits(rows)
    # 크롤링된 문제 자료 색인 + 코딩살구 전체 문제 카탈로그
    probs, cat = {"count": 0, "items": {}}, []
    try:
        pi = os.path.join(ROOT, "problems", "index.json")
        if os.path.exists(pi):
            probs = json.load(io.open(pi, encoding="utf-8"))
    except Exception:
        pass
    try:
        cl = os.path.join(ROOT, "_meta", "cosal_list.json")
        if os.path.exists(cl):
            cat = json.load(io.open(cl, encoding="utf-8")).get("items", [])
    except Exception:
        pass
    return render_dashboard(data, year, total, active, best, cells, rows, probs, cat)


def month_details(data, year, months=None):
    """월별 <details> 목록 (GitHub 마크다운에서 동작)."""
    by_month = {}
    for k in sorted(data):
        if not k.startswith(str(year)):
            continue
        if data[k]["count"] <= 0:
            continue
        by_month.setdefault(k[:7], []).append(k)
    keys = sorted(by_month, reverse=True)
    if months:
        keys = keys[:months]
    out = []
    for mk in keys:
        days = by_month[mk]
        cnt = sum(data[d]["count"] for d in days)
        rows = ["| 날짜 | 문제 |", "|---|---|"]
        for d in sorted(days, reverse=True):
            dt = datetime.date(*map(int, d.split("-")))
            items = [fmt(x) for x in data[d]["items"]] or ["(기록 없음)"]
            rows.append("| **%s** (%s) | %s |"
                        % (d[5:], DOW[dt.weekday()], "<br>".join(items)))
        out.append("<details>\n<summary><b>%s</b> — %d일 / %d문제</summary>\n\n%s\n\n</details>"
                   % (mk, len(days), cnt, "\n".join(rows)))
    return "\n\n".join(out) if out else "_아직 없음_"


# ── main ───────────────────────────────────────────────────────
def main():
    # 올해를 자동으로 쓴다. 해가 바뀌면 잔디도 따라 넘어간다.
    # (KST 기준 — 빌드가 UTC 서버에서 돌아도 새해 첫날 하루가 밀리지 않게)
    KST = datetime.timezone(datetime.timedelta(hours=9))
    year = datetime.datetime.now(KST).year
    if "--year" in sys.argv:
        year = int(sys.argv[sys.argv.index("--year") + 1])

    data = load_history()
    # 번호 없는 코드트리 기록을 문제에 연결 — history·실수노트 '양쪽 모두 merge 전에'.
    # (한쪽만 바꾸면 같은 날 CT 항목과 BOJ 제목 항목이 겹친다. 위 주석 참고)
    every, freq = load_ct_titles()
    sticky = ct_sticky(data)
    ct_h = link_codetree(data, every, freq, sticky)
    vault = from_vault()
    ct_v = link_codetree(vault, every, freq, sticky)
    # 실수노트가 상태의 진실 소스다(CLAUDE.md). repo 헤더는 보조.
    merge(data, vault, status_first=True)
    merge(data, from_repo())
    # 사용자가 지운 기록은 코드 파일·실수노트에 남아 있어도 되살리지 않는다.
    apply_tombstones(data, load_tombstones())

    io.open(HIST, "w", encoding="utf-8", newline="").write(
        # sort_keys — 허브(server.save_solution·delete_item)도 키를 정렬해서 쓴다.
        # 여기만 안 정렬하면 빌드와 저장이 번갈아 파일 전체의 키 순서를 뒤집어서,
        # 한 문제 저장이 989줄 diff 가 됐다(2026-09-23 E2E 에서 발견 — 실제 변경은 1건).
        json.dumps({k: data[k] for k in sorted(data)}, ensure_ascii=False, indent=1,
                   sort_keys=True))

    os.makedirs(ASSETS, exist_ok=True)
    svg, total = render_svg(data, year)
    io.open(SVG, "w", encoding="utf-8", newline="").write(svg)

    ydays = [k for k in data if k.startswith(str(year)) and data[k]["count"] > 0]
    active = len(ydays)
    streak = best = 0
    d = datetime.date(year, 1, 1)
    while d <= datetime.date(year, 12, 31):
        if data.get(d.isoformat(), {"count": 0})["count"] > 0:
            streak += 1
            best = max(best, streak)
        else:
            streak = 0
        d += datetime.timedelta(days=1)

    page = render_html(data, year, total, active, best)
    io.open(HTML, "w", encoding="utf-8", newline="").write(page)
    # GitHub Pages 진입점 (repo 루트)
    io.open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8", newline="").write(page)

    # 열어둔 탭이 낡았는지 브라우저가 알 수 있게 하는 작은 표식.
    # 데이터가 index.html 안에 박혀 있어, 어제 열어둔 탭은 오늘 기록을
    # "0문제 · 색 없음"으로 조용히 보여준다(2026-08-13 실제 사고).
    # 페이지가 이 파일을 주기적으로 읽어 stamp 가 다르면 새로고침을 권한다.
    m = re.search(r'"stamp":\s*"([^"]+)"', page)
    io.open(os.path.join(ROOT, "_meta", "built.json"), "w",
            encoding="utf-8", newline="").write(
        json.dumps({"stamp": m.group(1) if m else "",
                    "total": total, "active": active}, ensure_ascii=False))

    io.open(FULL, "w", encoding="utf-8", newline="").write(
        "# 🌱 코테 잔디 — 전체 기록 (%d)\n\n"
        "![](./assets/heatmap.svg)\n\n"
        "> 총 **%d문제** · 활동 **%d일** · 최장 연속 **%d일**\n"
        "> 🖱️ 마우스 hover로 보려면 **`assets/heatmap.html`** 을 브라우저로 열 것\n\n---\n\n%s\n"
        % (year, total, active, best, month_details(data, year)))

    block = ("![코테 잔디](./assets/heatmap.svg)\n\n"
             "| %d년 | |\n|---|---|\n| 총 시도 | **%d문제** |\n"
             "| 활동일 | **%d일** |\n| 최장 연속 | **%d일** |\n\n"
             "> 🖱️ **날짜별 문제를 보려면** → 아래 월별 목록을 펼치거나, "
             "[전체 기록](./HEATMAP.md) · 마우스 hover는 [`assets/heatmap.html`](./assets/heatmap.html) 을 브라우저로\n\n"
             "%s" % (year, total, active, best, month_details(data, year, months=2)))

    # README 의 잔디 블록은 사용자 요청으로 제거했다(대시보드에서 보므로 중복).
    # HEATMAP_START 마커가 남아 있는 저장소에서만 갱신하고, 없으면 건드리지 않는다.
    t = io.open(README, encoding="utf-8").read()
    if "<!-- HEATMAP_START -->" in t:
        t = re.sub(r"<!-- HEATMAP_START -->.*?<!-- HEATMAP_END -->",
                   "<!-- HEATMAP_START -->\n%s\n<!-- HEATMAP_END -->" % block, t, flags=re.S)
        io.open(README, "w", encoding="utf-8", newline="").write(t)

    print("✅ 잔디 생성 (%d년)" % year)
    print("   총 %d문제 / 활동 %d일 / 최장연속 %d일" % (total, active, best))
    print("   history.json %d일  |  SVG + HTML + HEATMAP.md" % len(data))
    with_items = sum(1 for k in data if data[k]["items"])
    print("   문제명 보유: %d일 / %d일" % (with_items, len(data)))
    if every or sticky:
        print("   코드트리 번호 연결: history %d건 · 실수노트 %d건" % (ct_h, ct_v))


if __name__ == "__main__":
    main()
