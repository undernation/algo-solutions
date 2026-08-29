# -*- coding: utf-8 -*-
"""성능 검수 — 정석 풀이가 제한(25 TC 합쳐 Python 8초) 안에 드는가.

두 가지를 잰다.
 1) 지금 tc_valid.txt 25개를 전부 도는 실제 시간
 2) 문제 제약 상한(build 최대 약 1000, move 최대 약 100)에 가까운
    최악 케이스를 따로 만들어 재는 시간
"""
import io
import random
import time

import solution as S

INF = 10 ** 18


def run_file(path):
    """main.py 와 같은 방식으로 파일 전체를 돌린다(출력 없이)."""
    toks = io.open(path, encoding="utf-8").read().split()
    it = iter(toks)
    T = int(next(it)); next(it)
    t0 = time.perf_counter()
    nmove = nbuild = 0
    for _ in range(T):
        Q = int(next(it))
        for _ in range(Q):
            c = int(next(it))
            if c == 100:
                S.init(int(next(it)))
            elif c == 200:
                S.build(*[int(next(it)) for _ in range(7)])
                nbuild += 1
            else:
                s = int(next(it)); e = int(next(it)); M = int(next(it))
                via = [int(next(it)) for _ in range(M)]
                next(it)                      # 정답
                S.move(s, e, M, via)
                nmove += 1
    return time.perf_counter() - t0, T, nbuild, nmove


print("=" * 62)
print(" 1) 배포 테스트케이스 (tc_valid.txt)")
print("=" * 62)
el, T, nb, nm = run_file("tc_valid.txt")
print("  TC %d개 · build %d · move %d" % (T, nb, nm))
print("  걸린 시간: %.2f 초   (제한 8초)" % el)
print("  판정:", "통과" if el < 8 else "초과")


# ── 최악 케이스 만들기 ───────────────────────────────────────────────
def worst_case(N, n_build, n_move, seed=7):
    """제약 상한에 가까운 한 케이스. 건물을 격자로 촘촘히 채운다."""
    rnd = random.Random(seed)
    S.init(N)
    built = []
    W = H = 2                       # 작은 건물을 최대한 많이
    step = W + 1                    # 도로 한 칸 공유
    for y in range(1, N - H - 1, step):
        for x in range(1, N - W - 1, step):
            if len(built) >= n_build:
                break
            mid = len(built) + 1
            S.build(mid, x, y, W, H, rnd.randint(0, W - 1), 0)
            built.append(mid)
        if len(built) >= n_build:
            break
    t0 = time.perf_counter()
    done = 0
    for _ in range(n_move):
        s, e = rnd.sample(built, 2)
        pool = [i for i in built if i not in (s, e)]
        M = min(5, len(pool))       # 경유지 최대 5 = 순열 120
        via = rnd.sample(pool, M)
        S.move(s, e, M, via)
        done += 1
    return time.perf_counter() - t0, len(built), done


print()
print("=" * 62)
print(" 2) 제약 상한 근처 최악 케이스 (한 TC 기준)")
print("=" * 62)
for N, nb_, nm_ in [(50, 200, 20), (70, 500, 20), (100, 1000, 20)]:
    el2, gb, gm = worst_case(N, nb_, nm_)
    per = el2 / gm if gm else 0
    print("  N=%-4d build %-5d move %2d (경유 5개)  →  %.2f 초  (move 1회 %.3f초)"
          % (N, gb, gm, el2, per))
    print("      이 규모로 move 100회면 약 %.1f 초" % (per * 100))
