# -*- coding: utf-8 -*-
"""건물 크기가 제각각이면서도 '항상 이동 가능한' 테스트케이스 생성.

앞선 실패 원인: 슬롯을 무작위로 섞어 짓다 보니 서로 떨어진 건물만 지어진
시점이 생겨 move 가 도달 불가(INF)가 됐다. 문제 조건은 '이동 불가능한 경우는
주어지지 않는다' 이므로 그런 케이스를 만들면 안 된다.

해결:
  1) 슬롯을 격자 순서(행 우선)대로 지어 항상 직전 건물과 도로를 공유하게 한다.
  2) move 는 '실제로 도달 가능한 쌍' 만 낸다(생성 시 거리로 확인).
"""
import io
import random

import solution as S

INF = 10 ** 18


def gen_case(seed, N, col_w, row_h, n_cmd=25, max_M=5):
    rnd = random.Random(seed)
    S.init(N)
    lines = ["100 %d" % N]

    xs, x = [], 3
    for w in col_w:
        xs.append((x, w))
        x = x + w + 1          # 도로 한 칸 공유
    ys, y = [], 3
    for h in row_h:
        ys.append((y, h))
        y = y + h + 1
    assert x <= N and y <= N, "격자 초과"

    # 행 우선 순서 — 인접 건물끼리 도로가 이어진다
    slots = [(bx, by, bw, bh) for (by, bh) in ys for (bx, bw) in xs]

    built, bid = [], 0

    def add_build():
        nonlocal bid
        X, Y, W, H = slots[bid]
        bid += 1
        side = rnd.randint(0, 3)
        if side == 0:
            dx, dy = rnd.randint(0, W - 1), 0
        elif side == 1:
            dx, dy = W - 1, rnd.randint(0, H - 1)
        elif side == 2:
            dx, dy = rnd.randint(0, W - 1), H - 1
        else:
            dx, dy = 0, rnd.randint(0, H - 1)
        mid = len(built) + 1
        S.build(mid, X, Y, W, H, dx, dy)
        built.append(mid)
        return "200 %d %d %d %d %d %d %d" % (mid, X, Y, W, H, dx, dy)

    def add_move():
        """도달 가능한 조합만 고른다(최대 30번 시도)."""
        for _ in range(30):
            s, e = rnd.sample(built, 2)
            pool = [i for i in built if i not in (s, e)]
            M = rnd.randint(0, min(max_M, len(pool)))
            via = rnd.sample(pool, M) if M else []
            ans = S.move(s, e, M, via)
            if ans < INF:
                return "300 %d %d %d%s %d" % (s, e, M, "".join(" %d" % v for v in via), ans)
        return None

    while len(lines) - 1 < n_cmd - 1:
        can_build = bid < len(slots)
        do_build = can_build and (len(built) < 2 or rnd.random() < 0.45)
        if do_build:
            lines.append(add_build())
        else:
            mv = add_move()
            if mv is None:
                if can_build:
                    lines.append(add_build())
                else:
                    break
            else:
                lines.append(mv)
    return lines


CASES = [
    (31, 30, [5, 3, 4],       [4, 2, 3]),     # TC1 — 크기 제각각
    (32, 30, [2, 6, 3],       [3, 5]),
    (33, 35, [4, 2, 5, 3],    [2, 4, 3]),
    (34, 40, [3, 5, 2, 4],    [4, 3, 5]),
    (35, 28, [6, 2],          [6, 2, 3]),
]

blocks = [gen_case(*c) for c in CASES]
out = ["%d %d" % (len(blocks), 100)]
for lines in blocks:
    out.append(str(len(lines)))
    out.extend(lines)
io.open("tc_valid.txt", "w", encoding="utf-8").write("\n".join(out) + "\n")

print("테케 %d개 (명령 %s개)" % (len(blocks), [len(b) for b in blocks]))
for i, b in enumerate(blocks, 1):
    sizes = sorted({(int(l.split()[4]), int(l.split()[5]))
                    for l in b if l.startswith("200")})
    nb = sum(1 for l in b if l.startswith("200"))
    nm = sum(1 for l in b if l.startswith("300"))
    print("  TC%d: build %2d · move %2d · 크기 %s"
          % (i, nb, nm, ",".join("%dx%d" % s for s in sizes)))
