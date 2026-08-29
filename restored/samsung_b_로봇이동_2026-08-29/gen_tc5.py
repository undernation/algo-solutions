# -*- coding: utf-8 -*-
"""실전에 가까운 테스트케이스 생성 — 자유 배치.

앞선 생성기의 문제:
  건물을 격자(열=같은 너비, 행=같은 높이)로만 놓아서
  1) 같은 행의 건물 높이가 전부 같고
  2) 한 건물의 도로 꼭짓점(교차로)이 다른 건물의 '변 중간'에 걸리는 상황이
     한 번도 안 나왔다. 이게 이 문제의 핵심 난이도인데 빠져 있었다.

이 생성기:
  - 건물마다 크기(W,H)와 위치를 무작위로 뽑는다.
  - 조건 검사: 건물끼리 겹치거나 맞닿지 않을 것(도로는 겹쳐도 됨),
    격자 안에 도로까지 들어올 것, 도로가 기존 건물과 반드시 연결될 것.
  - 그래서 자연스럽게 '변 중간 교차로'와 서로 다른 높이의 이웃이 생긴다.
"""
import io
import random

import solution as S

INF = 10 ** 18


def rect_ok(cand, placed, N):
    """건물끼리 겹치거나 맞닿지 않는지 + 도로가 격자 안인지."""
    X, Y, W, H = cand
    if not (1 <= X and 1 <= Y and X + W < N and Y + H < N):
        return False
    for (px, py, pw, ph) in placed:
        # 건물 사이에 최소 한 칸(도로) 이상 간격이 있어야 한다 = 맞닿음 금지
        if not (X > px + pw or px > X + W or Y > py + ph or py > Y + H):
            return False
    return True


def roads_of(X, Y, W, H):
    """이 건물이 만드는 도로 칸 집합."""
    L, R, T, B = X - 1, X + W, Y - 1, Y + H
    s = set()
    for x in range(L, R + 1):
        s.add((T, x))
        s.add((B, x))
    for y in range(T, B + 1):
        s.add((y, L))
        s.add((y, R))
    return s


def gen_case(seed, N, n_build, n_cmd=25, max_M=5, wrange=(2, 6), hrange=(2, 6)):
    rnd = random.Random(seed)
    S.init(N)
    lines = ["100 %d" % N]
    placed = []          # (X,Y,W,H)
    all_roads = set()
    built = []

    def try_place():
        """조건을 만족하고 기존 도로와 이어지는 건물 하나를 찾아 짓는다."""
        for _ in range(4000):
            W = rnd.randint(*wrange)
            H = rnd.randint(*hrange)
            X = rnd.randint(1, N - W - 1)
            Y = rnd.randint(1, N - H - 1)
            if not rect_ok((X, Y, W, H), placed, N):
                continue
            r = roads_of(X, Y, W, H)
            if placed and not (r & all_roads):
                continue           # 기존 도로와 안 이어지면 버린다
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
            placed.append((X, Y, W, H))
            all_roads.update(r)
            built.append(mid)
            return "200 %d %d %d %d %d %d %d" % (mid, X, Y, W, H, dx, dy)
        return None

    def try_move():
        for _ in range(60):
            s, e = rnd.sample(built, 2)
            pool = [i for i in built if i not in (s, e)]
            M = rnd.randint(0, min(max_M, len(pool)))
            via = rnd.sample(pool, M) if M else []
            ans = S.move(s, e, M, via)
            if ans < INF:
                return "300 %d %d %d%s %d" % (s, e, M, "".join(" %d" % v for v in via), ans)
        return None

    # 먼저 건물 2개는 확보
    while len(built) < 2:
        b = try_place()
        if b is None:
            raise RuntimeError("seed %d: 초기 건물 배치 실패" % seed)
        lines.append(b)

    while len(lines) - 1 < n_cmd - 1:
        want_build = len(built) < n_build and rnd.random() < 0.45
        if want_build:
            b = try_place()
            if b:
                lines.append(b)
                continue
        m = try_move()
        if m:
            lines.append(m)
        else:
            b = try_place()
            if b:
                lines.append(b)
            else:
                break
    return lines


CASES = [
    (101, 26, 9),
    (102, 24, 7),
    (103, 30, 11),
    (104, 32, 12),
    (105, 22, 6),
]

blocks = []
for cfg in CASES:
    blocks.append(gen_case(*cfg))

out = ["%d %d" % (len(blocks), 100)]
for lines in blocks:
    out.append(str(len(lines)))
    out.extend(lines)
io.open("tc_valid.txt", "w", encoding="utf-8").write("\n".join(out) + "\n")

print("테케 %d개 (명령 %s)" % (len(blocks), [len(b) for b in blocks]))
for i, b in enumerate(blocks, 1):
    bs = [list(map(int, l.split()[1:])) for l in b if l.startswith("200")]
    sizes = ["%dx%d" % (x[3], x[4]) for x in bs]
    nm = sum(1 for l in b if l.startswith("300"))
    print("  TC%d: build %2d · move %2d · 크기 %s"
          % (i, len(bs), nm, " ".join(sizes)))
