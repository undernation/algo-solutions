# -*- coding: utf-8 -*-
"""제약사항 전 항목 독립 검증.

solution.py 의 내부 상태(out_mask/cross/buildings)를 쓰지 않고
입력 파일의 숫자만으로 기하를 직접 계산해 검사한다.
정답 대조는 audit.py 의 독립 구현(다익스트라)을 쓴다.
"""
import io
import sys

from audit import Ref

LIMIT_BUILD = 1000
LIMIT_MOVE = 100
LIMIT_M = 5


def corners(X, Y, W, H):
    L, R, T, B = X - 1, X + W, Y - 1, Y + H
    return [(T, L), (T, R), (B, R), (B, L)]


def around8(y, x):
    return [(y + a, x + b) for a in (-1, 0, 1) for b in (-1, 0, 1)]


def parse(path):
    toks = io.open(path, encoding="utf-8").read().split()
    it = iter(toks)
    T = int(next(it)); MARK = int(next(it))
    cases = []
    for _ in range(T):
        Q = int(next(it))
        cmds = []
        for _ in range(Q):
            c = int(next(it))
            if c == 100:
                cmds.append(("init", [int(next(it))]))
            elif c == 200:
                cmds.append(("build", [int(next(it)) for _ in range(7)]))
            elif c == 300:
                s = int(next(it)); e = int(next(it)); M = int(next(it))
                via = [int(next(it)) for _ in range(M)]
                cmds.append(("move", [s, e, M, via, int(next(it))]))
            else:
                cmds.append(("??", [c]))
        cases.append(cmds)
    return T, MARK, cases


def main(path):
    T, MARK, cases = parse(path)
    print("파일: %s  ·  TC %d개 · 배점 %d" % (path, T, MARK))
    bad = []

    def err(tc, msg):
        bad.append("TC%d: %s" % (tc, msg))

    for tc, cmds in enumerate(cases, 1):
        # ── 형식 ──
        if not cmds or cmds[0][0] != "init":
            err(tc, "init 이 맨 앞에 없다")
            continue
        if sum(1 for k, _ in cmds if k == "init") != 1:
            err(tc, "init 이 한 번이 아니다")
        if any(k == "??" for k, _ in cmds):
            err(tc, "알 수 없는 명령")

        N = cmds[0][1][0]
        rects = {}          # id -> (X,Y,W,H,dx,dy)
        cross = set()
        doors = {}          # id -> (door_y, door_x)
        ref = Ref(N)
        nb = nm = 0

        for kind, a in cmds:
            if kind == "build":
                mID, X, Y, W, H, dx, dy = a
                nb += 1
                # (1) ID 중복
                if mID in rects:
                    err(tc, "건물 ID %d 중복" % mID)
                # (2) 도로까지 격자 안
                if not (1 <= X and 1 <= Y and X + W < N and Y + H < N):
                    err(tc, "건물 %d 도로가 격자 밖 (%d,%d %dx%d N=%d)"
                        % (mID, X, Y, W, H, N))
                # (3) 건물끼리 겹치거나 맞닿음 (사이에 도로 한 칸 이상 필요)
                for oid, (oX, oY, oW, oH, _, _) in rects.items():
                    if not (X > oX + oW or oX > X + W or
                            Y > oY + oH or oY > Y + H):
                        err(tc, "건물 %d 가 건물 %d 와 겹치거나 맞닿음" % (mID, oid))
                # (4) 출입구가 가장자리 칸
                if not (0 <= dx < W and 0 <= dy < H):
                    err(tc, "건물 %d 출입구가 건물 밖" % mID)
                elif not (dx in (0, W - 1) or dy in (0, H - 1)):
                    err(tc, "건물 %d 출입구가 가장자리가 아님" % mID)
                # (5) 출입구가 모서리 칸이면 어느 변인지 정해지지 않는다
                if dx in (0, W - 1) and dy in (0, H - 1):
                    err(tc, "건물 %d 출입구가 모서리 칸 (%d,%d)" % (mID, dx, dy))
                # (6) 지을 당시 출입구가 교차로와 인접
                d = (Y + dy, X + dx)
                hit = [c for c in around8(*d) if c in cross]
                if hit:
                    err(tc, "건물 %d 출입구가 지을 당시 교차로와 인접 %s" % (mID, hit[:2]))

                rects[mID] = (X, Y, W, H, dx, dy)
                doors[mID] = d
                cross.update(corners(X, Y, W, H))
                ref.build(mID, X, Y, W, H, dx, dy)

            elif kind == "move":
                s, e, M, via, exp = a
                nm += 1
                # (7) 경유 조건
                if M != len(via):
                    err(tc, "M(%d) 과 경유 개수(%d) 불일치" % (M, len(via)))
                if M > LIMIT_M:
                    err(tc, "경유 %d > %d" % (M, LIMIT_M))
                if len(set(via)) != len(via):
                    err(tc, "경유 중복 %s" % via)
                if s in via or e in via:
                    err(tc, "경유에 출발/도착 포함 %s" % via)
                for b_ in [s, e] + via:
                    if b_ not in rects:
                        err(tc, "없는 건물 %d 를 move 에서 사용" % b_)
                # (8) 정답이 독립 구현과 같은가 · 도달 가능한가
                got = ref.move(s, e, M, via)
                if got == float("inf"):
                    err(tc, "move(%d,%d,%s) 도달 불가인데 문제에 포함" % (s, e, via))
                elif got != exp:
                    err(tc, "move(%d,%d,%s) 정답 %d ≠ 독립구현 %s" % (s, e, via, exp, got))

        # (9) 최종 상태에서 출입구가 교차로와 인접 (미래 건물 포함)
        for mID, d in doors.items():
            hit = [c for c in around8(*d) if c in cross]
            if hit:
                err(tc, "건물 %d 출입구가 최종적으로 교차로와 인접 %s" % (mID, hit[:2]))

        # (10) 호출 횟수 상한
        if nb > LIMIT_BUILD:
            err(tc, "build %d > %d" % (nb, LIMIT_BUILD))
        if nm > LIMIT_MOVE:
            err(tc, "move %d > %d" % (nm, LIMIT_MOVE))

        print("  TC%-2d N=%-4d build %4d  move %3d  %s"
              % (tc, N, nb, nm, "OK" if not [b for b in bad if b.startswith("TC%d:" % tc)] else "실패"))

    print()
    if bad:
        print("위반 %d건:" % len(bad))
        for b in bad[:25]:
            print("   ✗", b)
    else:
        print("제약사항 전 항목 위반 0건 — 이상 없음")
    return len(bad)


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1] if len(sys.argv) > 1 else "tc_valid.txt") else 0)
