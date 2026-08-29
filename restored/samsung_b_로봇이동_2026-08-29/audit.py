# -*- coding: utf-8 -*-
"""테스트케이스 전수 검수.

solution 으로 만든 정답을 solution 으로 채점하면 순환논리다. 그래서
**독립 구현(브루트포스 성격의 다익스트라 + 경유지 전탐색)** 을 따로 짜서 대조한다.
그 밖에 케이스 자체가 문제 조건을 지키는지도 전부 검사한다.
"""
import io
import itertools
from collections import deque
from heapq import heappop, heappush

import solution as S

UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3
DY = [-1, 0, 1, 0]
DX = [0, 1, 0, -1]


# ── 독립 구현 ────────────────────────────────────────────────────────
class Ref:
    """solution 과 완전히 별개로 짠 참조 구현.
    도로 그래프를 (셀,방향) 노드로 펼쳐 다익스트라로 푼다(BFS 대신)."""

    def __init__(self, N):
        self.N = N
        self.dirs = {}           # (y,x) -> set(방향)
        self.cross = set()
        self.b = {}              # id -> dict

    def build(self, mID, mX, mY, mW, mH, mDoorX, mDoorY):
        L, R, T, B = mX - 1, mX + mW, mY - 1, mY + mH
        for x in range(L, R):
            self.dirs.setdefault((T, x), set()).add(RIGHT)
        for y in range(T, B):
            self.dirs.setdefault((y, R), set()).add(DOWN)
        for x in range(R, L, -1):
            self.dirs.setdefault((B, x), set()).add(LEFT)
        for y in range(B, T, -1):
            self.dirs.setdefault((y, L), set()).add(UP)
        for c in ((T, L), (T, R), (B, R), (B, L)):
            self.cross.add(c)
        dxp, dyp = mX + mDoorX, mY + mDoorY
        if mDoorY == 0:
            road, sd = (dyp - 1, dxp), RIGHT
        elif mDoorX == mW - 1:
            road, sd = (dyp, dxp + 1), DOWN
        elif mDoorY == mH - 1:
            road, sd = (dyp + 1, dxp), LEFT
        else:
            road, sd = (dyp, dxp - 1), UP
        self.b[mID] = {"door": (dyp, dxp), "road": road, "sd": sd,
                       "rect": (mX, mY, mW, mH), "drel": (mDoorX, mDoorY)}

    def dist(self, a, bid):
        """건물 a 출입구 -> 건물 bid 출입구 최단거리 (다익스트라)."""
        if a == bid:
            return 0
        sy, sx = self.b[a]["road"]
        sd = self.b[a]["sd"]
        goal = self.b[bid]["door"]
        INF = float("inf")
        best = {}
        pq = [(1, sy, sx, sd)]        # Door->도로 = 1
        while pq:
            d, y, x, dr = heappop(pq)
            if best.get((y, x, dr), INF) <= d:
                continue
            best[(y, x, dr)] = d
            # 오른쪽 칸이 목표 Door면 진입
            rd = (dr + 1) % 4
            if (y + DY[rd], x + DX[rd]) == goal:
                return d + 1
            outs = self.dirs.get((y, x), set())
            nds = outs if (y, x) in self.cross else (outs & {dr})
            for nd in nds:
                ny, nx = y + DY[nd], x + DX[nd]
                if not (0 <= ny < self.N and 0 <= nx < self.N):
                    continue
                if best.get((ny, nx, nd), INF) <= d + 1:
                    continue
                heappush(pq, (d + 1, ny, nx, nd))
        return INF

    def move(self, s, e, M, via):
        via = list(via[:M])
        nodes = list(dict.fromkeys([s] + via + [e]))
        D = {(a, b): self.dist(a, b) for a in nodes for b in nodes}
        if not via:
            return D[(s, e)]
        best = float("inf")
        for order in itertools.permutations(via):
            tot, cur = 0, s
            for nx in order:
                tot += D[(cur, nx)]
                cur = nx
            tot += D[(cur, e)]
            best = min(best, tot)
        return best


# ── 케이스 파싱 + 검수 ───────────────────────────────────────────────
def audit(path):
    toks = io.open(path, encoding="utf-8").read().split()
    it = iter(toks)
    T = int(next(it))
    MARK = int(next(it))
    print("테스트케이스 %d개, 배점 %d\n" % (T, MARK))
    allok = True

    for tc in range(1, T + 1):
        Q = int(next(it))
        cmds = []
        for _ in range(Q):
            c = int(next(it))
            if c == 100:
                cmds.append((100, int(next(it))))
            elif c == 200:
                cmds.append((200, [int(next(it)) for _ in range(7)]))
            else:
                s = int(next(it)); e = int(next(it)); M = int(next(it))
                via = [int(next(it)) for _ in range(M)]
                exp = int(next(it))
                cmds.append((300, (s, e, M, via, exp)))

        issues = []
        rects = []     # (x,y,w,h,id)
        ref = None
        nmove = nbuild = 0
        N = None

        for kind, arg in cmds:
            if kind == 100:
                N = arg
                S.init(N)
                ref = Ref(N)
            elif kind == 200:
                mID, mX, mY, mW, mH, dX, dY = arg
                nbuild += 1
                # (a) 격자 안에 도로까지 들어오나
                if not (1 <= mX and 1 <= mY and mX + mW < N and mY + mH < N):
                    issues.append("build %d: 도로가 격자를 벗어남 (%d,%d,%dx%d, N=%d)"
                                  % (mID, mX, mY, mW, mH, N))
                # (b) Door 가 가장자리인가
                on_edge = (dY == 0 or dY == mH - 1 or dX == 0 or dX == mW - 1)
                if not on_edge:
                    issues.append("build %d: Door(%d,%d)가 가장자리가 아님" % (mID, dX, dY))
                # (c) 건물끼리 겹치거나 맞닿는가 (도로는 겹쳐도 됨)
                for (px, py, pw, ph, pid) in rects:
                    if (mX <= px + pw and px <= mX + mW - 1 + 1 and
                            mY <= py + ph and py <= mY + mH - 1 + 1):
                        # 실제 '건물 영역 + 1칸' 이 겹치면 맞닿음
                        if not (mX > px + pw or px > mX + mW or
                                mY > py + ph or py > mY + mH):
                            issues.append("build %d: 건물 %d 와 겹치거나 맞닿음" % (mID, pid))
                        break
                rects.append((mX, mY, mW, mH, mID))
                S.build(*arg)
                ref.build(*arg)
            else:
                s, e, M, via, exp = arg
                nmove += 1
                got = S.move(s, e, M, list(via))
                ok_ref = ref.move(s, e, M, via)
                if got != exp:
                    issues.append("move(%d,%d,%d,%s): 저장된 정답 %d ≠ solution %d"
                                  % (s, e, M, via, exp, got))
                if ok_ref != exp:
                    issues.append("move(%d,%d,%d,%s): 저장된 정답 %d ≠ 독립구현 %s"
                                  % (s, e, M, via, exp, ok_ref))
                if exp <= 0 and s != e:
                    issues.append("move(%d,%d): 거리 %d 가 비정상" % (s, e, exp))
                if M > 5:
                    issues.append("move: 경유지 %d > 5" % M)
                if len(set(via)) != len(via):
                    issues.append("move: 경유지 중복 %s" % via)
                if s in via or e in via:
                    issues.append("move: 경유지에 출발/도착 포함 %s" % via)

        # 도로 겹침(문제의 핵심 성질)이 실제로 있는지
        shared = sum(1 for k, v in ref.dirs.items() if len(v) > 1)
        sizes = sorted({(r[2], r[3]) for r in rects})

        status = "OK  " if not issues else "실패"
        print("%s TC%d: 명령 %d (build %d / move %d) · 건물크기 %s · 도로공유칸 %d"
              % (status, tc, Q, nbuild, nmove,
                 ",".join("%dx%d" % s for s in sizes), shared))
        if shared == 0:
            print("      ⚠ 도로가 전혀 겹치지 않음 — 이 문제의 핵심 성질이 안 나온다")
            allok = False
        for m in issues[:6]:
            print("      ✗", m)
        if issues:
            allok = False

    print("\n전체 판정:", "이상 없음" if allok else "문제 있음")
    return allok


if __name__ == "__main__":
    audit("tc_valid.txt")
