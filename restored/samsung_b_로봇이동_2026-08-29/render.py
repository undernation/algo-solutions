# -*- coding: utf-8 -*-
"""격자 도해 SVG + worked example 경로 그림을 그려 문제지 HTML→PDF 를 만든다."""
import io
from collections import deque

import solution as S


# ── 경로 추적 BFS (solution 과 같은 규칙 + 부모 기록) ────────────────
def trace_path(start_id, end_id):
    """start 건물 Door → end 건물 Door 최단경로의 도로 셀 목록과 거리."""
    st = S.buildings[start_id]
    en = S.buildings[end_id]
    door_goal = (en.door_y, en.door_x)

    N = S.g_N
    par = {}
    dist = [[[-1] * 4 for _ in range(N)] for _ in range(N)]
    sy, sx, sd = st.road_y, st.road_x, st.start_dir
    dist[sy][sx][sd] = 1
    par[(sy, sx, sd)] = None
    q = deque([(sy, sx, sd)])
    end_state = None

    while q:
        y, x, d = q.popleft()
        cur = dist[y][x][d]
        rd = (d + 1) % 4
        gy, gx = y + S.dy[rd], x + S.dx[rd]
        if (gy, gx) == door_goal:
            end_state = (y, x, d)
            total = cur + 1
            break
        if S.cross[y][x]:
            for nd in range(4):
                if not (S.out_mask[y][x] & (1 << nd)):
                    continue
                ny, nx = y + S.dy[nd], x + S.dx[nd]
                if not (0 <= ny < N and 0 <= nx < N):
                    continue
                if dist[ny][nx][nd] != -1:
                    continue
                dist[ny][nx][nd] = cur + 1
                par[(ny, nx, nd)] = (y, x, d)
                q.append((ny, nx, nd))
        else:
            if not (S.out_mask[y][x] & (1 << d)):
                continue
            ny, nx = y + S.dy[d], x + S.dx[d]
            if not (0 <= ny < N and 0 <= nx < N):
                continue
            if dist[ny][nx][d] != -1:
                continue
            dist[ny][nx][d] = cur + 1
            par[(ny, nx, d)] = (y, x, d)
            q.append((ny, nx, d))

    # 역추적: Door(start) → 도로들 → Door(end)
    cells = []
    s = end_state
    while s is not None:
        cells.append((s[0], s[1]))
        s = par[s]
    cells.reverse()
    # 앞뒤에 Door 셀 붙이기
    path = [(st.door_y, st.door_x)] + cells + [(en.door_y, en.door_x)]
    return path, total


# ── SVG 격자 렌더 ────────────────────────────────────────────────────
ARROW = {0: (0, -1), 1: (1, 0), 2: (0, 1), 3: (0, 1)}  # placeholder


def svg_grid(x0, y0, x1, y1, path=None, title="", cell=30):
    """[x0..x1] x [y0..y1] 범위를 SVG 로. path 는 (y,x) 셀 목록(빨간 선)."""
    W = (x1 - x0 + 1) * cell
    H = (y1 - y0 + 1) * cell
    out = ['<svg width="%d" height="%d" viewBox="0 0 %d %d" '
           'style="border:1px solid #ccc;background:#fff">' % (W, H + (58 if W < 470 else 40), W, H + (58 if W < 470 else 40))]
    if title:
        out.append('<text x="4" y="13" font-size="12" fill="#333" '
                   'font-weight="bold">%s</text>' % title)
    oy = 16

    def cx(x):
        return (x - x0) * cell + cell / 2

    def cy(y):
        return (y - y0) * cell + cell / 2 + oy

    # 건물 내부(회색)
    for bid, b in S.buildings.items():
        rx = (b.x - x0) * cell
        ry = (b.y - y0) * cell + oy
        out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#d0d4da" '
                   'stroke="#888"/>' % (rx, ry, b.w * cell, b.h * cell))
        out.append('<text x="%d" y="%d" font-size="12" fill="#555" '
                   'text-anchor="middle">B%d</text>'
                   % (cx(b.x + (b.w - 1) / 2.0), cy(b.y + (b.h - 1) / 2.0) - oy + oy + 4, bid))

    # 도로 화살표.
    #
    # 🚩 한 칸에 두 방향(예: UP+DOWN)이 있어도 그것은 '두 건물의 서로 다른 도로가
    #    겹쳐 있다'는 뜻이지, 그 자리에서 방향을 바꿀 수 있다는 뜻이 아니다.
    #    그래서 ↕ 같은 양방향 화살표로 그리지 않고, 화살표를 셀 안에서 나란히
    #    비켜 그려 '별개의 도로 두 개'로 보이게 한다.
    #    방향 전환이 가능한 곳은 교차로뿐이므로 거기만 크게 강조한다.
    adir = {0: (0, -1), 1: (1, 0), 2: (0, 1), 3: (-1, 0)}  # UP,RIGHT,DOWN,LEFT (dx,dy)
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            m = S.out_mask[y][x] if 0 <= y < S.g_N and 0 <= x < S.g_N else 0
            if not m:
                continue
            ccx, ccy = cx(x), cy(y)
            out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" '
                       'stroke="#eee"/>' % ((x - x0) * cell, (y - y0) * cell + oy, cell, cell))
            ds = [d for d in range(4) if m & (1 << d)]
            vert = [d for d in ds if d in (0, 2)]     # UP/DOWN
            horz = [d for d in ds if d in (1, 3)]     # RIGHT/LEFT
            for d in ds:
                ddx, ddy = adir[d]
                r = cell * 0.30
                # 같은 축에 두 방향이 겹치면 서로 어긋나게 비켜 그린다
                ox = oyy = 0.0
                if d in (0, 2) and len(vert) > 1:
                    ox = -cell * 0.16 if d == 0 else cell * 0.16
                if d in (1, 3) and len(horz) > 1:
                    oyy = -cell * 0.16 if d == 1 else cell * 0.16
                bx, by = ccx + ox, ccy + oyy
                x2, y2 = bx + ddx * r, by + ddy * r
                x1a, y1a = bx - ddx * r, by - ddy * r
                out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                           'stroke="#5b8def" stroke-width="1.5" '
                           'marker-end="url(#ah)"/>' % (x1a, y1a, x2, y2))
            if S.cross[y][x]:
                # 교차로 = 이 칸에서만 다른 건물 도로로 갈아탈 수 있다
                out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#fff" '
                           'stroke="#e8890c" stroke-width="2.2" opacity="0.95"/>'
                           % (ccx, ccy, cell * 0.20))
                out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#e8890c"/>'
                           % (ccx, ccy, cell * 0.085))

    # Door
    for bid, b in S.buildings.items():
        dxp = (b.door_x - x0) * cell
        dyp = (b.door_y - y0) * cell + oy
        out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#2e7d32" '
                   'opacity="0.85"/>' % (dxp, dyp, cell, cell))
        out.append('<text x="%.1f" y="%.1f" font-size="13" fill="#fff" '
                   'text-anchor="middle" font-weight="bold">D%d</text>'
                   % (cx(b.door_x), cy(b.door_y) + 4, bid))

    # 경로(빨간 선)
    if path:
        pts = " ".join("%.1f,%.1f" % (cx(x), cy(y)) for (y, x) in path)
        out.append('<polyline points="%s" fill="none" stroke="#e03131" '
                   'stroke-width="2.6" stroke-linejoin="round" opacity="0.85"/>' % pts)
        for i, (y, x) in enumerate(path):
            out.append('<circle cx="%.1f" cy="%.1f" r="2.4" fill="#e03131"/>'
                       % (cx(x), cy(y)))

    out.append('<defs><marker id="ah" markerWidth="6" markerHeight="6" refX="5" '
               'refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#5b8def"/>'
               '</marker></defs>')
    # 범례 — 화살표 두 개가 나란한 칸은 '두 건물의 도로가 겹친 것'이지
    # 그 자리에서 방향을 바꿀 수 있다는 뜻이 아니다.
    # 그림이 좁으면 한 줄에 두 항목이 안 들어가 글자가 잘린다. 그럴 땐 두 줄로 쓴다.
    two_line = W < 470
    ly = H + oy - (18 if two_line else 4)
    out.append('<line x1="8" y1="%d" x2="26" y2="%d" stroke="#5b8def" '
               'stroke-width="1.5" marker-end="url(#ah)"/>' % (ly, ly))
    out.append('<text x="30" y="%.1f" font-size="10" fill="#555">'
               '시계방향 도로(방향 고정)</text>' % (ly + 3.5))
    if two_line:
        cx2, cy2 = 14, ly + 17
    else:
        cx2, cy2 = int(W * 0.50), ly
    out.append('<circle cx="%d" cy="%d" r="5.5" fill="#fff" stroke="#e8890c" '
               'stroke-width="2.2"/>' % (cx2, cy2))
    out.append('<circle cx="%d" cy="%d" r="2.3" fill="#e8890c"/>' % (cx2, cy2))
    out.append('<text x="%d" y="%.1f" font-size="10" fill="#555">'
               '교차로 — 여기서만 다른 도로로 갈아탈 수 있다</text>'
               % (cx2 + 10, cy2 + 3.5))
    out.append("</svg>")
    return "".join(out)


if __name__ == "__main__":
    # 개념 도해: 건물 1개
    S.init(10)
    S.build(1, 3, 3, 4, 4, 1, 0)
    concept = svg_grid(1, 1, 8, 8, title="건물 1개 · 도로는 시계방향(파란 화살표) · ● 교차로 · D 출입구")

    # 예시: 건물 2개, move(1->2) 경로
    S.init(15)
    S.build(1, 3, 3, 4, 4, 1, 0)
    S.build(2, 8, 3, 4, 4, 3, 3)
    p12, d12 = trace_path(1, 2)
    ex1 = svg_grid(1, 1, 13, 8, path=p12,
                   title="예시: D1 출발 → D2 도착 (빨간 경로), move(1,2,0)=%d" % d12)
    d21 = S.move(2, 1, 0, [])

    io.open("_svg_concept.txt", "w", encoding="utf-8").write(concept)
    io.open("_svg_ex1.txt", "w", encoding="utf-8").write(ex1)
    print("도해 SVG 생성. move(1,2)=%d, move(2,1)=%d, 경로길이=%d칸" % (d12, d21, len(p12)))
