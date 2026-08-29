# -*- coding: utf-8 -*-
"""원본에 가깝게: 한 테스트케이스당 명령 약 25개(init 1 + build/move 섞어서).

원문은 build 와 move 가 섞여 나온다(건물을 짓다가 중간에 move 를 부른다).
그 형태를 그대로 만들고, 각 move 의 정답은 solution 으로 구해 붙인다.
"""
import io
import random

import solution as S


def gen_case(seed, N, cols, rows, W, H, n_cmd=25, max_M=5):
    """init 1개 + (build/move 섞어) 총 n_cmd 개 명령."""
    rnd = random.Random(seed)
    S.init(N)
    lines = ["100 %d" % N]

    # 건물 후보 좌표(격자로 놓아 도로가 이어지게)
    slots = []
    for r in range(rows):
        for c in range(cols):
            slots.append((3 + c * (W + 1), 3 + r * (H + 1)))
    rnd.shuffle(slots)

    built = []
    bid = 0
    # 처음 2개는 먼저 지어야 move 가 가능
    while len(lines) - 1 < n_cmd - 1:
        remain = n_cmd - 1 - (len(lines) - 1)
        can_build = bid < len(slots)
        # 건물 2개 미만이면 무조건 build, 아니면 확률적으로
        do_build = can_build and (len(built) < 2 or rnd.random() < 0.45)
        if do_build:
            X, Y = slots[bid]
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
            lines.append("200 %d %d %d %d %d %d %d" % (mid, X, Y, W, H, dx, dy))
        else:
            s, e = rnd.sample(built, 2)
            pool = [i for i in built if i not in (s, e)]
            M = rnd.randint(0, min(max_M, len(pool)))
            via = rnd.sample(pool, M) if M else []
            ans = S.move(s, e, M, via)
            lines.append("300 %d %d %d%s %d"
                         % (s, e, M, "".join(" %d" % v for v in via), ans))
        if remain <= 1:
            break
    return lines


CASES = [
    (11, 30, 3, 2, 4, 4),
    (12, 30, 4, 1, 4, 4),
    (13, 35, 3, 3, 3, 3),
    (14, 40, 4, 3, 4, 3),
    (15, 25, 2, 2, 5, 5),
]

blocks = [gen_case(*c) for c in CASES]
out = ["%d %d" % (len(blocks), 100)]
for lines in blocks:
    out.append(str(len(lines)))
    out.extend(lines)
io.open("tc_valid.txt", "w", encoding="utf-8").write("\n".join(out) + "\n")

print("테케 %d개 생성 (테케당 명령 %s개)"
      % (len(blocks), [len(b) for b in blocks]))
for i, b in enumerate(blocks, 1):
    nb = sum(1 for l in b if l.startswith("200"))
    nm = sum(1 for l in b if l.startswith("300"))
    print("  TC%d: build %d · move %d" % (i, nb, nm))
