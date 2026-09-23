"""
problems/ 아래 크롤링된 문제 JSON을 한 파일로 색인.

GitHub Pages 는 디렉터리 목록을 주지 않으므로, 대시보드가 "어떤 문제 자료가 있는지"
알려면 색인이 필요하다. 지문 전문은 넣지 않고(용량), 목록/트리에 필요한 것만 담는다.

비공개 문제(파일에 "private_content": true — judge_config.json 의 privateSites 에 든 사이트)는
지문·예제가 repo 에 없다. 허브 TC 보관소에만 있고, 크롤러가 개수·길이만
sample_count / statement_len 으로 남긴다. 색인에는 "priv": 1 을 달아 대시보드가
허브(/prob)에서 지문을 받아 오게 한다. 공개(지금 기본값 — 코드트리도 공개 저장)면
다른 사이트와 똑같이 실제 samples·statement 로 smp·len 을 센다.

출력: problems/index.json
"""
import os, io, json, glob, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROB = os.path.join(ROOT, "problems")
SITE = {"boj": "BOJ", "swea": "SWEA", "programmers": "PGS", "codetree": "CT"}


def _num(v) -> int:
    """개수 필드를 정수로. 이상한 값 하나 때문에 색인 전체가 죽으면 안 된다
    (클라우드 허브가 저장할 때마다 이 스크립트를 돌린다)."""
    try:
        return max(0, int(v or 0))
    except (TypeError, ValueError):
        return 0


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
        has_note = os.path.exists(os.path.join(ROOT, "notes", sub, "%s.md" % no))
        note = ("notes/%s/%s.md" % (sub, no)) if has_note else ""
        path = "problems/%s/%s" % (sub, os.path.basename(f))
        if d.get("private_content"):
            # 비공개 사이트: 지문·예제가 repo 에 없다. 개수·길이는 크롤러가 남긴 값으로.
            # 비공개 여부는 사이트를 못박지 않고 파일의 플래그를 따른다 — 스위치
            # (judge_config.json privateSites)를 바꾸면 크롤러가 파일을 다시 쓰고 색인이 따라온다.
            e = {"note": note, "site": site, "no": no,
                 "title": d.get("title", ""),
                 "limits": d.get("limits", {}),
                 "smp": _num(d.get("sample_count")),
                 "len": _num(d.get("statement_len")),
                 "path": path,
                 "priv": 1}
        else:
            e = {"note": note,
                 "site": site, "no": no,
                 "title": d.get("title", ""),
                 "label": d.get("label", ""),
                 "limits": d.get("limits", {}),
                 "tc": d.get("private_tc_count", 0),
                 "htc": len(d.get("private_testcases") or []),
                 "smp": len(d.get("samples") or []),
                 "len": len(d.get("statement") or ""),
                 "path": path}
            if site == "CT":
                # 코드트리는 1,400문제가 넘고 이 색인은 index.html 에 통째로 박힌다.
                # 코드트리엔 늘 비어 있는 label·tc·htc 는 빈 값일 때 뺀다(실데이터 1,451문제 기준 46KB).
                # 대시보드는 없는 값을 ''/0 과 똑같이 다룬다(m.tc 는 삭제 확인 문구 하나뿐).
                for k in ("label", "tc", "htc"):
                    if not e[k]:
                        del e[k]
        if d.get("locked"):
            # 403 으로 못 연 문제(크롤러가 locked 만 달고 지문·한도를 비워 둔다).
            # 허브 보관소에도 없으니 대시보드가 /prob 를 물어볼 필요가 없다.
            e["locked"] = 1
        out["%s/%s" % (site, no)] = e
    io.open(os.path.join(PROB, "index.json"), "w", encoding="utf-8", newline="").write(
        json.dumps({"built": datetime.date.today().isoformat(),
                    "count": len(out), "items": out}, ensure_ascii=False))
    print("✅ 문제 색인 %d개 → problems/index.json" % len(out))


if __name__ == "__main__":
    main()
