"""
SWEA 문제 페이지 → 구조화된 메타 추출

사용법:
    python _meta/fetch_swea.py AWIeUtVakTMDFAVH
    python _meta/fetch_swea.py AWIeUtVakTMDFAVH --json

선행조건: 디버그 크롬이 9222 포트로 떠 있고 SWEA 로그인 상태여야 함
    python C:/Users/solom/crawler.py chrome
"""
import sys, re, json, io

URL = "https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=%s"


def fetch(prob_id: str) -> str:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = b.contexts[0]
        pg = ctx.pages[0] if ctx.pages else ctx.new_page()
        pg.goto(URL % prob_id, wait_until="networkidle", timeout=90_000)
        pg.wait_for_timeout(2500)
        if "login" in pg.url.lower():
            raise RuntimeError("SWEA 로그인 필요")
        return pg.evaluate("() => document.body.innerText") or ""


def parse(body: str) -> dict:
    d = {}

    # "4012. [모의 SW 역량테스트] 요리사"
    m = re.search(r"^\s*(\d{3,5})\.\s*(.+?)\s*$", body, re.M)
    if m:
        d["number"], d["title"] = m.group(1), m.group(2).strip()

    # 난이도 (Master / Expert / …)
    m = re.search(r"\n(D\d|Master|Expert|Professional|Senior|Junior|Novice)\s*\n", body)
    if m:
        d["level"] = m.group(1)

    # 통계 블록: 참여자 / 제출 / 정답 / 정답률 / Point
    for key, pat in (
        ("participants", r"([\d,]+)\s*\n\s*참여자"),
        ("submissions",  r"([\d,]+)\s*\n\s*제출"),
        ("accepted",     r"([\d,]+)\s*\n\s*정답\s*\n"),
        ("accept_rate",  r"([\d.]+)\s*\n\s*정답률"),
        ("point",        r"([\d,]+)\s*\n\s*Point"),
    ):
        m = re.search(pat, body)
        if m:
            d[key] = m.group(1)

    # 시간/메모리 한도
    m = re.search(r"시간\s*:\s*(.+)", body)
    if m:
        d["time_limit"] = m.group(1).strip()
    m = re.search(r"메모리\s*:\s*(.+)", body)
    if m:
        d["memory_limit"] = m.group(1).strip()

    # 제약사항 블록
    m = re.search(r"\[제약사항\](.*?)(?:\[입력\]|\Z)", body, re.S)
    if m:
        lines = [x.strip() for x in m.group(1).split("\n") if x.strip()]
        d["constraints"] = lines

    # 본문 (저작권 고지 이후 ~ [제약사항] 전)
    m = re.search(r"무단 복제하는 것을 금지합니다\.?\s*(.*?)(?:\[제약사항\]|\Z)", body, re.S)
    if m:
        d["statement"] = re.sub(r"\n{3,}", "\n\n", m.group(1)).strip()

    return d


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    prob_id = sys.argv[1]
    body = fetch(prob_id)
    d = parse(body)
    d["prob_id"] = prob_id
    d["url"] = URL % prob_id

    if "--json" in sys.argv:
        print(json.dumps(d, ensure_ascii=False, indent=2))
        return

    print("번호   :", d.get("number", "?"))
    print("제목   :", d.get("title", "?"))
    print("난이도 :", d.get("level", "?"))
    print("정답률 :", d.get("accept_rate", "?"), "%  /  Point", d.get("point", "?"))
    print("시간   :", d.get("time_limit", "?"))
    print("메모리 :", d.get("memory_limit", "?"))
    print()
    for c in d.get("constraints", [])[:8]:
        print("  -", c[:100])


if __name__ == "__main__":
    main()
