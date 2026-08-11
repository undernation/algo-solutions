"""
README.md 의 현황 표 + 인덱스를 풀이 파일에서 자동 생성.

사용법:
    python _meta/build_index.py
"""
import os, re, io, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")

HEADER_PAT = re.compile(r'"""(.*?)"""', re.S)


def parse_file(path: str) -> dict:
    src = io.open(path, encoding="utf-8").read()
    m = HEADER_PAT.search(src)
    head = m.group(1) if m else ""
    d = {"path": os.path.relpath(path, ROOT).replace(os.sep, "/")}

    m = re.search(r"^\s*(BOJ|SWEA)\s+(\d+)\s+(.*)$", head, re.M)
    if m:
        d["site"], d["number"], d["title"] = m.group(1), m.group(2), m.group(3).strip()
    else:
        base = os.path.basename(path).replace(".py", "")
        d["site"] = "SWEA" if "/swea/" in d["path"] else "BOJ"
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
    files = sorted(glob.glob(os.path.join(ROOT, "boj", "*.py"))) + \
            sorted(glob.glob(os.path.join(ROOT, "swea", "*.py")))
    items = [parse_file(f) for f in files]
    boj = [x for x in items if x["site"] == "BOJ"]
    swea = [x for x in items if x["site"] == "SWEA"]

    rows = ["| 사이트 | 번호 | 제목 | 결과 | 풀이일 | 분류 |",
            "|---|---|---|---|---|---|"]
    for x in sorted(items, key=lambda v: (v.get("date") or "", v["number"]), reverse=True):
        rows.append("| %s | [%s](%s) | %s | %s | %s | %s |" % (
            x["site"], x["number"], x["path"], x.get("title", "")[:40],
            x.get("result", ""), x.get("date", ""), x.get("tag", "")[:30]))
    index = "\n".join(rows) if items else "_아직 없음_"

    stat = ("| | |\n|---|---|\n| 총 풀이 | %d |\n| BOJ | %d |\n| SWEA | %d |"
            % (len(items), len(boj), len(swea)))

    t = io.open(README, encoding="utf-8").read()
    t = re.sub(r"\| \| \|\n\|---\|---\|\n\| 총 풀이 \|.*?\| SWEA \| \d+ \|", stat, t, flags=re.S)
    t = re.sub(r"<!-- INDEX_START -->.*?<!-- INDEX_END -->",
               "<!-- INDEX_START -->\n%s\n<!-- INDEX_END -->" % index, t, flags=re.S)
    io.open(README, "w", encoding="utf-8", newline="").write(t)
    print("✅ README 갱신: 총 %d (BOJ %d / SWEA %d)" % (len(items), len(boj), len(swea)))


if __name__ == "__main__":
    main()
