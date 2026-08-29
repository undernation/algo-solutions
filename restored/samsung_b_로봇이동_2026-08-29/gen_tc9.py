# -*- coding: utf-8 -*-
"""최종 테스트케이스 생성 — 출입구 제약을 지킨다.

문제 조건:
  "출입구는 교차로와 인접한 자리에 배정되지 않으며,
   이후 새로운 건물이 추가되어 교차로가 생기더라도 이 조건은 유지된다."

여기서 '인접'은 대각선을 포함한 여덟 방향으로 본다. 그래서
  · 출입구가 건물의 모서리 칸에 오는 일이 없다
    (모서리 출입구는 자기 건물 도로의 꼭짓점 교차로와 대각으로 붙는다)
  · 출입구가 나가는 도로 칸도 당연히 교차로가 아니다
  · 어느 변에 있는 출입구인지가 항상 하나로 정해진다

건물을 놓을 때마다 두 가지를 함께 본다.
  (a) 새 건물 출입구 둘레 8칸에 기존 교차로가 없을 것
  (b) 새 건물이 만드는 교차로 4곳이 기존 어떤 출입구의 둘레 8칸에도 없을 것
(b) 를 매번 지키면 '미래 건물이 들어와도 유지' 가 귀납적으로 성립한다.

구성
  TC1       : 문제지 도해용 작은 케이스 (명령 25개)
  TC2~TC22  : 다양한 중소 규모 (자유 배치, 크기 제각각)
  TC23~TC25 : 큰 케이스 — 제약 상한(build 1,000 · 경유 5) 포함
"""
import io
import random
import time

import solution as S

INF = 10 ** 18


# ── 기하 유틸 ────────────────────────────────────────────────────────
def around8(y, x):
    return [(y + dy, x + dx)
            for dy in (-1, 0, 1) for dx in (-1, 0, 1)]


def corners(X, Y, W, H):
    L, R, T, B = X - 1, X + W, Y - 1, Y + H
    return [(T, L), (T, R), (B, R), (B, L)]


def roads_of(X, Y, W, H):
    L, R, T, B = X - 1, X + W, Y - 1, Y + H
    s = set()
    for x in range(L, R + 1):
        s.add((T, x)); s.add((B, x))
    for y in range(T, B + 1):
        s.add((y, L)); s.add((y, R))
    return s


def rect_ok(cand, placed, N):
    X, Y, W, H = cand
    if not (1 <= X and 1 <= Y and X + W < N and Y + H < N):
        return False
    for (px, py, pw, ph) in placed:
        if not (X > px + pw or px > X + W or Y > py + ph or py > Y + H):
            return False
    return True


def door_candidates(rnd, W, H):
    """가장자리 중 '모서리가 아닌' 칸만 출입구 후보로 쓴다.
    윗변·아랫변은 W >= 3, 좌우변은 H >= 3 이어야 후보가 생긴다."""
    cand = []
    for x in range(1, W - 1):
        cand.append((x, 0))
        cand.append((x, H - 1))
    for y in range(1, H - 1):
        cand.append((0, y))
        cand.append((W - 1, y))
    cand = list(dict.fromkeys(cand))
    rnd.shuffle(cand)
    return cand


class Builder:
    def __init__(self, seed, N):
        self.rnd = random.Random(seed)
        self.N = N
        S.init(N)
        self.lines = ["100 %d" % N]
        self.placed = []
        self.roads = set()
        self.cross = set()
        self.door_zone = set()      # 각 출입구의 둘레 8칸 + 자신
        self.built = []

    def _door_ok(self, X, Y, W, H, dx, dy):
        dz = set(around8(Y + dy, X + dx))
        if dz & self.cross:                               # (a)
            return None
        for c in corners(X, Y, W, H):                     # (b)
            if c in self.door_zone:
                return None
        return dz

    def _commit(self, X, Y, W, H, dx, dy, dz):
        mid = len(self.built) + 1
        S.build(mid, X, Y, W, H, dx, dy)
        self.placed.append((X, Y, W, H))
        self.roads.update(roads_of(X, Y, W, H))
        self.cross.update(corners(X, Y, W, H))
        self.door_zone.update(dz)
        self.built.append(mid)
        self.lines.append("200 %d %d %d %d %d %d %d" % (mid, X, Y, W, H, dx, dy))
        return mid

    def place_free(self, wrange, hrange, tries=8000):
        rnd = self.rnd
        for _ in range(tries):
            W = rnd.randint(*wrange); H = rnd.randint(*hrange)
            if W < 3 and H < 3:
                continue                     # 출입구 후보가 없다
            X = rnd.randint(1, self.N - W - 1); Y = rnd.randint(1, self.N - H - 1)
            if not rect_ok((X, Y, W, H), self.placed, self.N):
                continue
            if self.placed and not (roads_of(X, Y, W, H) & self.roads):
                continue
            for dx, dy in door_candidates(rnd, W, H):
                dz = self._door_ok(X, Y, W, H, dx, dy)
                if dz is not None:
                    return self._commit(X, Y, W, H, dx, dy, dz)
        return None

    def place_at(self, X, Y, W, H):
        for dx, dy in door_candidates(self.rnd, W, H):
            dz = self._door_ok(X, Y, W, H, dx, dy)
            if dz is not None:
                return self._commit(X, Y, W, H, dx, dy, dz)
        return None

    def make_move(self, max_M=5, tries=60):
        rnd = self.rnd
        for _ in range(tries):
            s, e = rnd.sample(self.built, 2)
            pool = [i for i in self.built if i not in (s, e)]
            M = rnd.randint(0, min(max_M, len(pool)))
            via = rnd.sample(pool, M) if M else []
            ans = S.move(s, e, M, via)
            if ans < INF:
                self.lines.append("300 %d %d %d%s %d"
                                  % (s, e, M, "".join(" %d" % v for v in via), ans))
                return True
        return False


def gen_case(seed, N, n_build, n_cmd, wrange=(3, 6), hrange=(3, 6)):
    b = Builder(seed, N)
    while len(b.built) < 2:
        if b.place_free(wrange, hrange) is None:
            raise RuntimeError("seed %d 초기 배치 실패" % seed)
    while len(b.lines) - 1 < n_cmd - 1:
        if len(b.built) < n_build and b.rnd.random() < 0.45:
            if b.place_free(wrange, hrange) is not None:
                continue
        if not b.make_move():
            if b.place_free(wrange, hrange) is None:
                break
    return b.lines


def gen_grid_case(seed, N, n_build, n_move, size=3, max_M=5):
    """큰 케이스. 크기 고정 + 간격 size+1 이라 도로가 전부 이어진다.
    출입구는 모서리를 못 쓰므로 한 변이 3 이상이어야 한다."""
    b = Builder(seed, N)
    step = size + 1
    for y in range(1, N - size - 1, step):
        for x in range(1, N - size - 1, step):
            if len(b.built) >= n_build:
                break
            b.place_at(x, y, size, size)
        if len(b.built) >= n_build:
            break
    made = tries = 0
    while made < n_move and tries < n_move * 6:
        tries += 1
        if b.make_move(max_M=max_M):
            made += 1
    return b.lines, len(b.built), made


blocks = []
blocks.append(gen_case(777, 26, 7, 25))
print("  TC1 (도해용): build %d · move %d"
      % (sum(1 for l in blocks[0] if l.startswith("200")),
         sum(1 for l in blocks[0] if l.startswith("300"))))

for i in range(21):
    blocks.append(gen_case(400 + i, 22 + (i % 5) * 4, 5 + (i % 7), 20 + (i % 6) * 3))

t0 = time.perf_counter()
# 건물 1,000개: 크기 3 · 간격 4 이므로 N=130 이면 32x32 = 1024 자리
for i, (N, nb, nm) in enumerate([(55, 150, 30), (80, 350, 40), (130, 1000, 60)]):
    lines, gb, gm = gen_grid_case(300 + i, N, nb, nm)
    blocks.append(lines)
    print("  큰 TC%d: N=%d build=%d move=%d" % (23 + i, N, gb, gm))
print("  (큰 케이스 %.1f초)" % (time.perf_counter() - t0))

out = ["%d %d" % (len(blocks), 100)]
for lines in blocks:
    out.append(str(len(lines)))
    out.extend(lines)
io.open("tc_valid.txt", "w", encoding="utf-8").write("\n".join(out) + "\n")
print("\nTC %d개 · build %d · move %d"
      % (len(blocks),
         sum(sum(1 for l in b if l.startswith("200")) for b in blocks),
         sum(sum(1 for l in b if l.startswith("300")) for b in blocks)))
