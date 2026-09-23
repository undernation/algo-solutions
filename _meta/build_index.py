"""
README.md 의 현황 표 + 인덱스를 풀이 파일에서 자동 생성.

사용법:
    python _meta/build_index.py
"""
import os, re, io, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")

HEADER_PAT = re.compile(r'"""(.*?)"""', re.S)
# 풀이 폴더. 코드트리(2026-09-23~)는 codetree/<no>_<제목>.py — 트레일 "196", 기출 "f386"
# (기출 problem_id 가 트레일과 겹쳐 f 를 붙인다). 헤더는 "CT f386  AI 로봇청소기".
SOL_DIRS = ("boj", "swea", "codetree")
# 현황 표. 코드트리 줄은 풀이가 하나라도 생긴 뒤에만 붙인다(그 전엔 README 가 예전과 똑같다).
# 치환 패턴은 CT 줄이 있는 표·없는 표 둘 다 잡아야 한다 — 안 그러면 CT 가 처음 생기는
# 빌드 뒤로 표가 두 벌로 불어나거나, 다 지웠을 때 CT 줄만 남는다.
STAT_PAT = re.compile(r"\| \| \|\n\|---\|---\|\n\| 총 풀이 \|.*?\| SWEA \| \d+ \|(?:\n\| CT \| \d+ \|)?",
                      re.S)


def parse_file(path: str) -> dict:
    src = io.open(path, encoding="utf-8").read()
    m = HEADER_PAT.search(src)
    head = m.group(1) if m else ""
    d = {"path": os.path.relpath(path, ROOT).replace(os.sep, "/")}

    if d["path"].startswith("codetree/"):
        # 코드트리 번호는 숫자로 못박지 않는다(서버 허용 형식). BOJ/SWEA 는 예전 정규식 그대로.
        m = re.search(r"^\s*(CT)\s+([A-Za-z0-9_-]{1,12})\s+(.*)$", head, re.M)
    else:
        m = re.search(r"^\s*(BOJ|SWEA)\s+(\d+)\s+(.*)$", head, re.M)
    if m:
        d["site"], d["number"], d["title"] = m.group(1), m.group(2), m.group(3).strip()
    else:
        base = os.path.basename(path).replace(".py", "")
        d["site"] = "CT" if d["path"].startswith("codetree/") else \
            ("SWEA" if "/swea/" in d["path"] else "BOJ")
        parts = base.split("_", 1)
        d["number"] = parts[0]
        d["title"] = parts[1] if len(parts) > 1 else ""

    m = re.search(r"풀이일\s*:\s*([\d-]+)\s*결과\s*:\s*(\S+)", head)
    if m:
        d["date"], d["result"] = m.group(1), m.group(2)
    m = re.search(r"\((\S*?자력\S*?|\S*?회차)\s*,?\s*(\d+)회차\)", head)
    if m:
        d["round"] = m.group(2)
    m = re.search(r"분류\s*:\s*(.+)", head)
    if m:
        d["tag"] = m.group(1).strip()
    return d


def main():
    files = [f for s in SOL_DIRS for f in sorted(glob.glob(os.path.join(ROOT, s, "*.py")))]
    items = [parse_file(f) for f in files]
    boj = [x for x in items if x["site"] == "BOJ"]
    swea = [x for x in items if x["site"] == "SWEA"]
    ct = [x for x in items if x["site"] == "CT"]

    rows = ["| 사이트 | 번호 | 제목 | 결과 | 풀이일 | 분류 |",
            "|---|---|---|---|---|---|"]
    for x in sorted(items, key=lambda v: (v.get("date") or "", v["number"]), reverse=True):
        rows.append("| %s | [%s](%s) | %s | %s | %s | %s |" % (
            x["site"], x["number"], x["path"], x.get("title", "")[:40],
            x.get("result", ""), x.get("date", ""), x.get("tag", "")[:30]))
    index = "\n".join(rows) if items else "_아직 없음_"

    stat = ("| | |\n|---|---|\n| 총 풀이 | %d |\n| BOJ | %d |\n| SWEA | %d |"
            % (len(items), len(boj), len(swea)))
    if ct:
        stat += "\n| CT | %d |" % len(ct)

    t = io.open(README, encoding="utf-8").read()
    # 함수형 치환: stat 문자열의 '\' 나 그룹 참조가 치환 문법으로 읽히지 않게.
    t = STAT_PAT.sub(lambda _m: stat, t)
    t = re.sub(r"<!-- INDEX_START -->.*?<!-- INDEX_END -->",
               "<!-- INDEX_START -->\n%s\n<!-- INDEX_END -->" % index, t, flags=re.S)
    io.open(README, "w", encoding="utf-8", newline="").write(t)
    print("✅ README 갱신: 총 %d (BOJ %d / SWEA %d / CT %d)"
          % (len(items), len(boj), len(swea), len(ct)))


if __name__ == "__main__":
    main()
