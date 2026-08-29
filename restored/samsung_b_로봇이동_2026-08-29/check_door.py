# -*- coding: utf-8 -*-
"""출입구 제약 위반 검사.

조건: 출입구는 교차로와 인접(대각 포함 8방향)한 자리에 배정되지 않으며,
      이후 새 건물이 추가되어 교차로가 생겨도 유지된다.
따라서 모서리 출입구도 금지된다(자기 건물 꼭짓점과 대각으로 붙는다).
"""
import io

import solution as S


def around8(y, x):
    return [(y + dy, x + dx) for dy in (-1, 0, 1) for dx in (-1, 0, 1)]


def check(path, quiet=False):
    toks = io.open(path, encoding="utf-8").read().split()
    it = iter(toks)
    T = int(next(it)); next(it)
    bad_now = bad_final = bad_corner = 0

    for tc in range(1, T + 1):
        Q = int(next(it)); cmds = []
        for _ in range(Q):
            c = int(next(it))
            if c == 100:
                cmds.append((100, [int(next(it))]))
            elif c == 200:
                cmds.append((200, [int(next(it)) for _ in range(7)]))
            else:
                s = int(next(it)); e = int(next(it)); M = int(next(it))
                via = [int(next(it)) for _ in range(M)]
                cmds.append((300, [s, e, M, via, int(next(it))]))

        doors = {}
        nb_now = nb_cor = 0
        for kind, a in cmds:
            if kind == 100:
                S.init(a[0])
            elif kind == 200:
                mID, X, Y, W, H, dx, dy = a
                S.build(*a)
                doors[mID] = (Y + dy, X + dx)
                if (dx in (0, W - 1)) and (dy in (0, H - 1)):
                    nb_cor += 1            # 모서리 출입구
                for (cy, cx) in around8(Y + dy, X + dx):
                    if 0 <= cy < S.g_N and 0 <= cx < S.g_N and S.cross[cy][cx]:
                        nb_now += 1
                        break

        nb_fin = 0
        for mID, (dy_, dx_) in doors.items():
            for (cy, cx) in around8(dy_, dx_):
                if 0 <= cy < S.g_N and 0 <= cx < S.g_N and S.cross[cy][cx]:
                    nb_fin += 1
                    break

        bad_now += nb_now; bad_final += nb_fin; bad_corner += nb_cor
        if (nb_now or nb_fin or nb_cor) and not quiet:
            print("  TC%-2d 건물 %4d | 지을때 %3d | 최종 %3d | 모서리출입구 %3d"
                  % (tc, len(doors), nb_now, nb_fin, nb_cor))

    print()
    print("  지을 당시 위반 %d / 최종(미래 포함) 위반 %d / 모서리 출입구 %d"
          % (bad_now, bad_final, bad_corner))
    print("  판정:", "이상 없음" if (bad_now or bad_final or bad_corner) == 0 else "위반 있음")
    return bad_now, bad_final, bad_corner


if __name__ == "__main__":
    check("tc_valid.txt")
