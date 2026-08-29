# -*- coding: utf-8 -*-
"""99999.json → 문제지 PDF. **풀이 스포 없음** (지문·도해·예시·제약만).

풀이 핵심(BFS 상태 설계, out_mask/roads, 순열 등)은 넣지 않는다.
나중에 다시 풀 때 힌트가 되면 안 되기 때문이다.
"""
import base64
import html
import io
import json
import os
import re

from playwright.sync_api import sync_playwright

ARCHIVE = r"C:\Users\solom\algo-solutions"
prob = json.load(io.open(os.path.join(ARCHIVE, "problems", "swea", "99999.json"),
                         encoding="utf-8"))


def img_tag(idx):
    """[[IMG:n]] → base64 인라인 <img>"""
    rel = prob["images"][idx - 1]
    p = os.path.join(ARCHIVE, rel.replace("/", os.sep))
    b64 = base64.b64encode(open(p, "rb").read()).decode()
    return ('<div class="fig"><img src="data:image/png;base64,%s"></div>' % b64)


def body(text):
    """지문 텍스트 → HTML. [[IMG:n]] 치환, ■ 소제목, 들여쓴 줄은 코드블록."""
    out, buf = [], []

    def flush():
        if buf:
            out.append("<pre>" + html.escape("\n".join(buf)) + "</pre>")
            buf.clear()

    for line in text.split("\n"):
        m = re.match(r"\[\[IMG:(\d+)\]\]", line.strip())
        if m:
            flush()
            out.append(img_tag(int(m.group(1))))
            continue
        if line.startswith("■ "):
            flush()
            out.append("<h2>%s</h2>" % html.escape(line[2:]))
            continue
        if line.startswith("    ") and line.strip():
            buf.append(line[4:] if line.startswith("    ") else line)
            continue
        flush()
        if line.strip() == "":
            out.append("<div class='sp'></div>")
        else:
            out.append("<p>%s</p>" % html.escape(line))
    flush()
    return "\n".join(out)


def table(text):
    """마크다운 표 → HTML (examples_text 안의 표)"""
    rows = [l for l in text.split("\n") if l.strip().startswith("|")]
    if not rows:
        return ""
    keep = [r for r in rows if not re.match(r"^\|[\s:|-]+\|$", r.strip())]
    o = ["<table>"]
    for i, r in enumerate(keep):
        cells = [c.strip() for c in r.strip().strip("|").split("|")]
        tag = "th" if i == 0 else "td"
        o.append("<tr>" + "".join("<%s>%s</%s>" % (tag, html.escape(c), tag)
                                  for c in cells) + "</tr>")
    o.append("</table>")
    return "".join(o)


ex_text = prob["examples_text"]
ex_no_table = "\n".join(l for l in ex_text.split("\n")
                        if not l.strip().startswith("|"))
# 표를 원래 자리에 넣기 위해 표 직전 문구 뒤에 삽입
ex_html = body(ex_no_table).replace(
    "<div class='sp'></div>\n<h2>첫 번째 테스트 케이스</h2>",
    table(ex_text) + "<h2>첫 번째 테스트 케이스</h2>", 1)
if "<table>" not in ex_html:
    ex_html += table(ex_text)

lim = prob["limits"]
cons = "".join("<li>%s</li>" % html.escape(re.sub(r"^\d+\.\s*", "", c))
               for c in prob["constraints"])

CSS = """
body{font-family:'Malgun Gothic','맑은 고딕',sans-serif;font-size:11px;line-height:1.75;
 color:#1b1b1b;padding:24px 30px;max-width:800px}
h1{font-size:20px;border-bottom:2.5px solid #222;padding-bottom:7px;margin:0 0 6px}
h2{font-size:14px;margin:20px 0 6px;color:#14386e;border-left:4px solid #14386e;
 padding-left:9px;background:#f4f7fb}
p{margin:4px 0}
.sp{height:7px}
.lim{background:#f4f6f9;border:1px solid #d5dbe3;border-radius:6px;padding:9px 13px;margin:9px 0}
.warn{background:#fff8e1;border-left:4px solid #f0ad4e;padding:8px 12px;color:#665;
 margin:9px 0;font-size:10.5px}
pre{background:#f6f7f9;border:1px solid #ddd;border-radius:5px;padding:9px 12px;
 font-family:Consolas,monospace;font-size:10px;line-height:1.5;white-space:pre;margin:6px 0}
table{border-collapse:collapse;margin:9px 0;font-size:10.5px}
th,td{border:1px solid #b8bfc9;padding:4px 11px;text-align:left}
th{background:#e9eef5}
td:last-child{font-family:Consolas,monospace;color:#c0392b;font-weight:700;text-align:center}
ul{margin:5px 0;padding-left:20px}li{margin:2px 0}
.fig{text-align:center;margin:11px 0;page-break-inside:avoid}
.fig img{max-width:97%;border:1px solid #d6d6d6;border-radius:4px}
"""

HTML = """<!doctype html><meta charset="utf-8"><style>%s</style>
<h1>%s</h1>
<div class="warn">&#9888; 본 문제는 시험 후 기억을 바탕으로 <b>복원한 연습 문제</b>입니다.
실제 기출 문제와 일부 세부 조건 및 입출력 형식이 다를 수 있습니다.</div>
<div class="lim"><b>제한 시간</b> : %s<br><b>메모리</b> : %s<br>
<b>제출</b> : Main Code 고정 + User Code(init / build / move) 구현</div>
%s
<h2>예제</h2>
%s
<h2>입출력 형식</h2>
<pre>%s</pre>
<h2>제약 사항</h2>
<ul>%s</ul>
""" % (CSS, html.escape(prob["title"]), html.escape(lim["time"]),
       html.escape(lim["memory"]),
       body(prob["statement"]), ex_html,
       html.escape(prob["output_spec"]), cons)

OUT = "로봇이동_문제지.pdf"
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.set_content(HTML, wait_until="load")
    pg.pdf(path=OUT, format="A4", print_background=True,
           margin={"top": "12mm", "bottom": "12mm", "left": "12mm", "right": "12mm"})
    b.close()

import fitz
d = fitz.open(OUT)
txt = "".join(d[i].get_text() for i in range(d.page_count))
spoil = [w for w in ["BFS", "out_mask", "permutation", "순열", "visited", "다익스트라", "풀이 핵심"]
         if w in txt]
print("%s 생성: %d페이지" % (OUT, d.page_count))
print("스포 단어 검출:", spoil or "없음 (깨끗)")
