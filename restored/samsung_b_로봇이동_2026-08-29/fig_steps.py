# -*- coding: utf-8 -*-
"""첫 테스트 케이스를 '명령 순서 표 + 단계별 그림' 으로 만든다.

- 표  : 순서 / 함수 / 반환값  (실제 SWEA 문제의 [Table] 형식)
- 그림: build 로 도시가 자라는 모습, move 마다 최단경로
        한 장에 몰아 그리지 않고 단계별로 나눠 그린다.
"""
import io
import os

import solution as S
from render import svg_grid, trace_path
from playwright.sync_api import sync_playwright

ARCHIVE = r"C:\Users\solom\algo-solutions"
IMGDIR = os.path.join(ARCHIVE, "problems", "swea", "img")
os.makedirs(IMGDIR, exist_ok=True)

# ── 첫 TC 읽기 ──────────────────────────────────────────────────────
lines = io.open("tc_valid.txt", encoding="utf-8").read().splitlines()
Q = int(lines[1])
cmds = [list(map(int, l.split())) for l in lines[2:2 + Q]]

N = cmds[0][1]
S.init(N)

rows = []          # (순서, 함수문자열, 반환값)
shots = []         # (파일이름, 제목, path or None) — 그릴 시점
builds = []

for i, p in enumerate(cmds, 1):
    if p[0] == 100:
        rows.append((i, "init(%d)" % p[1], ""))
    elif p[0] == 200:
        mID, mX, mY, mW, mH, dX, dY = p[1:8]
        S.build(mID, mX, mY, mW, mH, dX, dY)
        builds.append((mX, mY, mW, mH))
        rows.append((i, "build(%d, %d, %d, %d, %d, %d, %d)"
                     % (mID, mX, mY, mW, mH, dX, dY), ""))
        shots.append(("build", i, mID, None))
    else:
        s, e, M = p[1], p[2], p[3]
        via = p[4:4 + M]
        ans = p[4 + M]
        vs = "{%s}" % ", ".join(map(str, via))
        rows.append((i, "move(%d, %d, %d, %s)" % (s, e, M, vs), str(ans)))
        shots.append(("move", i, (s, e, via, ans), None))

# 그릴 범위(모든 건물 + 도로)
xs = [b[0] for b in builds] + [b[0] + b[2] for b in builds]
ys = [b[1] for b in builds] + [b[1] + b[3] for b in builds]
X0, X1 = max(0, min(xs) - 2), min(N - 1, max(xs) + 1)
Y0, Y1 = max(0, min(ys) - 2), min(N - 1, max(ys) + 1)


def snap(pg, svg, name):
    pg.set_content('<!doctype html><meta charset="utf-8">'
                   '<body style="margin:0;display:inline-block">%s</body>' % svg,
                   wait_until="load")
    pg.query_selector("svg").screenshot(path=os.path.join(IMGDIR, name))


made = []
with sync_playwright() as p:
    br = p.chromium.launch()
    pg = br.new_page(device_scale_factor=2)

    # ── 1) build 단계: 도시가 자라는 모습 (3 컷) ─────────────────────
    S.init(N)
    step_at = []          # 몇 번째 build 후에 찍을지
    nb = len(builds)
    step_at = [2, (nb + 2) // 2, nb]      # 초반 / 중반 / 전체
    done = 0
    for p2 in cmds:
        if p2[0] != 200:
            continue
        S.build(*p2[1:8])
        done += 1
        if done in step_at:
            k = step_at.index(done) + 1
            fn = "99999_s%d.png" % k
            snap(pg, svg_grid(X0, Y0, X1, Y1, cell=30,
                              title="[Fig. %d] 건물 %d개를 지은 뒤" % (2 + k, done)), fn)
            made.append((fn, "건물 %d개" % done))

    # ── 2) move 단계: 대표 3건의 경로 ────────────────────────────────
    moves = [(x[2][0], x[2][1], x[2][2], x[2][3], x[1])
             for x in shots if x[0] == "move"]
    pick = [moves[0]]                                   # 첫 move
    pick += [m for m in moves if len(m[2]) == 1][:1]     # 경유 1곳
    pick += [m for m in moves if len(m[2]) >= 4][:1]     # 경유 많은 것
    for j, (s, e, via, ans, order) in enumerate(pick, 1):
        path, direct = trace_path(s, e)
        vs = "{%s}" % ", ".join(map(str, via))
        title = ("[Fig. %d] 명령 %d: move(%d, %d, %d, %s) = %d"
                 % (5 + j, order, s, e, len(via), vs, ans))
        if via:
            title += "   (그림은 경유 없는 %d→%d 최단경로 %d)" % (s, e, direct)
        fn = "99999_m%d.png" % j
        snap(pg, svg_grid(X0, Y0, X1, Y1, path=path, cell=30, title=title), fn)
        made.append((fn, "move %d→%d" % (s, e)))
    br.close()

# ── 표를 마크다운으로 ────────────────────────────────────────────────
tbl = ["| 순서 | 함수 | 반환값 |", "| --- | --- | --- |"]
for i, f, r in rows:
    tbl.append("| %d | %s | %s |" % (i, f, r))
io.open("_tc1_table.md", "w", encoding="utf-8").write("\n".join(tbl))

print("표 %d행 → _tc1_table.md" % len(rows))
print("그림 %d장:" % len(made))
for fn, d in made:
    print("   %s  (%s)" % (fn, d))
