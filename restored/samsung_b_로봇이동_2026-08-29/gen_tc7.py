# -*- coding: utf-8 -*-
"""최종 테스트케이스 — 25개, 최대 규모 케이스 포함, 25개 합쳐 8초 이내.

구성
  TC1~TC3   : 최대 규모 (건물 상한 근처 + move 100회 + 경유 5개)
  TC4~TC25  : 다양한 중소 규모 (자유 배치, 크기 제각각)

'최대'의 기준은 문제 제약: build 최대 약 1,000회, move 최대 약 100회, 경유 M<=5.
격자 N 은 건물 1,000개가 도로까지 들어가려면 최소 (2+1)*sqrt(1000) ~ 96 이므로
N=100 을 쓴다.
"""
import io
import random
import time

import solution as S

INF = 10 ** 18


# ── 공용 유틸 ────────────────────────────────────────────────────────
def rect_ok(cand, placed, N):
    X, Y, W, H = cand
    if not (1 <= X and 1 <= Y and X + W < N and Y + H < N):
        return False
    for (px, py, pw, ph) in placed:
        if not (X > px + pw or px > X + W or Y > py + ph or py > Y + H):
            return False
    return True


def roads_of(X, Y, W, H):
    L, R, T, B = X - 1, X + W, Y - 1, Y + H
    s = set()
    for x in range(L, R + 1):
        s.add((T, x)); s.add((B, x))
    for y in range(T, B + 1):
        s.add((y, L)); s.add((y, R))
    return s


def door_of(rnd, W, H):
    side = rnd.randint(0, 3)
    if side == 0:   return rnd.randint(0, W - 1), 0
    if side == 1:   return W - 1, rnd.randint(0, H - 1)
    if side == 2:   return rnd.randint(0, W - 1), H - 1
    return 0, rnd.randint(0, H - 1)


# ── 최대 규모 케이스 ─────────────────────────────────────────────────
def gen_max_case(seed, N, n_build, n_move, size=2):
    """건물을 격자로 촘촘히 최대한 짓고, move 를 n_move 회(경유 5개) 낸다.

    🚩 크기를 섞으면 안 된다. 간격을 '최대 폭+1' 로 잡으면 작은 건물끼리는
       도로가 한 칸 벌어져 끊기고, move 가 전부 도달 불가가 된다(실제로 겪음).
       최대 규모 케이스는 크기를 고정(size)하고 간격을 size+1 로 두어
       모든 이웃이 도로를 정확히 한 칸씩 공유하게 한다.
       N=100, size=2, step=3 이면 32x32 = 1024개까지 들어간다."""
    rnd = random.Random(seed)
    S.init(N)
    lines = ["100 %d" % N]
    built = []
    W = H = size
    step = size + 1
    for y in range(1, N - H - 1, step):
        for x in range(1, N - W - 1, step):
            if len(built) >= n_build:
                break
            dx, dy = door_of(rnd, W, H)
            mid = len(built) + 1
            S.build(mid, x, y, W, H, dx, dy)
            built.append(mid)
            lines.append("200 %d %d %d %d %d %d %d" % (mid, x, y, W, H, dx, dy))
        if len(built) >= n_build:
            break

    made = 0
    tries = 0
    while made < n_move and tries < n_move * 6:
        tries += 1
        s, e = rnd.sample(built, 2)
        pool = [i for i in built if i not in (s, e)]
        M = min(5, len(pool))
        via = rnd.sample(pool, M)
        ans = S.move(s, e, M, via)
        if ans >= INF:
            continue
        lines.append("300 %d %d %d%s %d"
                     % (s, e, M, "".join(" %d" % v for v in via), ans))
        made += 1
    return lines, len(built), made


# ── 일반 케이스 (자유 배치) ──────────────────────────────────────────
def gen_case(seed, N, n_build, n_cmd, max_M=5, wrange=(2, 6), hrange=(2, 6)):
    rnd = random.Random(seed)
    S.init(N)
    lines = ["100 %d" % N]
    placed, all_roads, built = [], set(), []

    def try_place():
        for _ in range(3000):
            W = rnd.randint(*wrange); H = rnd.randint(*hrange)
            X = rnd.randint(1, N - W - 1); Y = rnd.randint(1, N - H - 1)
            if not rect_ok((X, Y, W, H), placed, N):
                continue
            r = roads_of(X, Y, W, H)
            if placed and not (r & all_roads):
                continue
            dx, dy = door_of(rnd, W, H)
            mid = len(built) + 1
            S.build(mid, X, Y, W, H, dx, dy)
            placed.append((X, Y, W, H)); all_roads.update(r); built.append(mid)
            return "200 %d %d %d %d %d %d %d" % (mid, X, Y, W, H, dx, dy)
        return None

    def try_move():
        for _ in range(50):
            s, e = rnd.sample(built, 2)
            pool = [i for i in built if i not in (s, e)]
            M = rnd.randint(0, min(max_M, len(pool)))
            via = rnd.sample(pool, M) if M else []
            ans = S.move(s, e, M, via)
            if ans < INF:
                return "300 %d %d %d%s %d" % (s, e, M, "".join(" %d" % v for v in via), ans)
        return None

    while len(built) < 2:
        b = try_place()
        if b is None:
            raise RuntimeError("seed %d 초기 배치 실패" % seed)
        lines.append(b)
    while len(lines) - 1 < n_cmd - 1:
        if len(built) < n_build and rnd.random() < 0.45:
            b = try_place()
            if b:
                lines.append(b); continue
        m = try_move()
        if m:
            lines.append(m)
        else:
            b = try_place()
            if b: lines.append(b)
            else: break
    return lines


blocks = []

# TC1 : 문제지 도해로 보여줄 작은 케이스 (명령 25개, 건물 6~8개)
#       그림으로 규칙을 설명해야 하므로 첫 케이스는 일부러 작게 잡는다.
blocks.append(gen_case(777, 24, 7, 25))
nb1 = sum(1 for l in blocks[0] if l.startswith("200"))
nm1 = sum(1 for l in blocks[0] if l.startswith("300"))
print("  TC1 (도해용): 명령 25 · build %d · move %d" % (nb1, nm1))

# TC2~TC22 : 일반 (다양한 중소 규모)
for i in range(21):
    seed = 400 + i
    N = 20 + (i % 5) * 4
    n_build = 5 + (i % 7)
    n_cmd = 20 + (i % 6) * 3
    blocks.append(gen_case(seed, N, n_build, n_cmd))

# TC23~TC25 : 규모가 큰 케이스 — 마지막에 둔다(제약 상한 포함)
t0 = time.perf_counter()
for i, (N, nb, nm) in enumerate([(50, 200, 30), (70, 350, 40), (100, 1000, 60)]):
    lines, gb, gm = gen_max_case(300 + i, N, nb, nm)
    blocks.append(lines)
    print("  큰 TC%d: N=%d build=%d move=%d" % (23 + i, N, gb, gm))
print("  (큰 케이스 생성에 %.1f초)" % (time.perf_counter() - t0))

out = ["%d %d" % (len(blocks), 100)]
for lines in blocks:
    out.append(str(len(lines)))
    out.extend(lines)
io.open("tc_valid.txt", "w", encoding="utf-8").write("\n".join(out) + "\n")

nb = sum(sum(1 for l in b if l.startswith("200")) for b in blocks)
nm = sum(sum(1 for l in b if l.startswith("300")) for b in blocks)
print("\n테스트케이스 %d개 · 총 build %d · 총 move %d" % (len(blocks), nb, nm))
print("파일 크기: %.1f KB" % (len("\n".join(out)) / 1024))
