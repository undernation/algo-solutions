# -*- coding: utf-8 -*-
"""첫 테스트케이스를 시각화한다 — 건물 배치 전체 + 대표 move 한 건의 경로."""
import io
import os

import solution as S
from render import svg_grid, trace_path
from playwright.sync_api import sync_playwright

ARCHIVE = r"C:\Users\solom\algo-solutions"
IMGDIR = os.path.join(ARCHIVE, "problems", "swea", "img")

# ── 첫 테케 재생(build 만) ───────────────────────────────────────────
lines = io.open("tc_valid.txt", encoding="utf-8").read().splitlines()
it = iter(lines)
next(it)                      # "T MARK"
Q = int(next(it))
cmds = [next(it) for _ in range(Q)]

builds, moves = [], []
for c in cmds:
    p = list(map(int, c.split()))
    if p[0] == 100:
        S.init(p[1])
        N = p[1]
    elif p[0] == 200:
        S.build(*p[1:8])
        builds.append(p[1:8])
    elif p[0] == 300:
        s, e, M = p[1], p[2], p[3]
        via = p[4:4 + M]
        moves.append((s, e, M, via, p[4 + M]))

# 그릴 범위: 건물 도로까지 포함
xs = [b[1] for b in builds] + [b[1] + b[3] for b in builds]
ys = [b[2] for b in builds] + [b[2] + b[4] for b in builds]
x0, x1 = max(0, min(xs) - 2), min(N - 1, max(xs) + 1)
y0, y1 = max(0, min(ys) - 2), min(N - 1, max(ys) + 1)

FIG_A = svg_grid(x0, y0, x1, y1, cell=30,
                 title="[Fig. 3] 첫 번째 테스트 케이스의 건물 배치 (건물 %d개)" % len(builds))

# 대표 move: 경유지가 있는 것 중 첫 번째 (없으면 첫 move)
rep = next((m for m in moves if m[2] > 0), moves[0])
s, e, M, via, ans = rep
path, dist = trace_path(s, e)      # 직행 경로(경유 없는 최단) — 그림용
FIG_B = svg_grid(x0, y0, x1, y1, path=path, cell=30,
                 title="[Fig. 4] move(%d, %d, 0, {}) = %d 의 최단경로" % (s, e, dist))


def svg_to_png(pg, svg, path):
    pg.set_content('<!doctype html><meta charset="utf-8">'
                   '<body style="margin:0;display:inline-block">%s</body>' % svg,
                   wait_until="load")
    pg.query_selector("svg").screenshot(path=path)


with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(device_scale_factor=2)
    svg_to_png(pg, FIG_A, os.path.join(IMGDIR, "99999_3.png"))
    svg_to_png(pg, FIG_B, os.path.join(IMGDIR, "99999_4.png"))
    b.close()

print("첫 테케 시각화 2장 저장 (99999_3.png, 99999_4.png)")
print("  건물 %d개 / move %d회" % (len(builds), len(moves)))
print("  대표 move: move(%d, %d, %d, %s) = %d" % (s, e, M, via, ans))
print("  Fig.4 는 직행 move(%d,%d)=%d 경로" % (s, e, dist))

# 예시 표에 넣을 앞부분 명령 목록
rows = []
for c in cmds[:12]:
    p = list(map(int, c.split()))
    if p[0] == 100:
        rows.append(("init(%d)" % p[1], ""))
    elif p[0] == 200:
        rows.append(("build(%d, %d, %d, %d, %d, %d, %d)" % tuple(p[1:8]), ""))
    else:
        s2, e2, M2 = p[1], p[2], p[3]
        v2 = p[4:4 + M2]
        vs = "{%s}" % ", ".join(map(str, v2))
        rows.append(("move(%d, %d, %d, %s)" % (s2, e2, M2, vs), str(p[4 + M2])))
io.open("_tc1_rows.txt", "w", encoding="utf-8").write(
    "\n".join("%s\t%s" % r for r in rows))
print("  예시 표 %d행 → _tc1_rows.txt" % len(rows))
