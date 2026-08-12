"""
problems/ 아래 크롤링된 문제 JSON을 한 파일로 색인.

GitHub Pages 는 디렉터리 목록을 주지 않으므로, 대시보드가 "어떤 문제 자료가 있는지"
알려면 색인이 필요하다. 지문 전문은 넣지 않고(용량), 목록/트리에 필요한 것만 담는다.

출력: problems/index.json
"""
import os, io, json, glob, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROB = os.path.join(ROOT, "problems")
SITE = {"boj": "BOJ", "swea": "SWEA", "programmers": "PGS", "codetree": "CT"}


def main():
    out = {}
    for f in sorted(glob.glob(os.path.join(PROB, "*", "*.json"))):
        if os.path.basename(f) == "index.json":
            continue
        sub = os.path.basename(os.path.dirname(f))
        try:
            d = json.load(io.open(f, encoding="utf-8"))
        except Exception:
            continue
        site = d.get("site") or SITE.get(sub, sub.upper())
        no = str(d.get("no") or os.path.splitext(os.path.basename(f))[0])
        note = os.path.join(ROOT, "notes", sub, "%s.md" % no)
        out["%s/%s" % (site, no)] = {
            "note": ("notes/%s/%s.md" % (sub, no)) if os.path.exists(note) else "",
            "site": site, "no": no,
            "title": d.get("title", ""),
            "label": d.get("label", ""),
            "limits": d.get("limits", {}),
            "tc": d.get("private_tc_count", 0),
            "htc": len(d.get("private_testcases") or []),
            "smp": len(d.get("samples") or []),
            "len": len(d.get("statement") or ""),
            "path": "problems/%s/%s" % (sub, os.path.basename(f)),
        }
    io.open(os.path.join(PROB, "index.json"), "w", encoding="utf-8", newline="").write(
        json.dumps({"built": datetime.date.today().isoformat(),
                    "count": len(out), "items": out}, ensure_ascii=False))
    print("✅ 문제 색인 %d개 → problems/index.json" % len(out))


if __name__ == "__main__":
    main()
