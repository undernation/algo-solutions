"""
삼성 SW 역량테스트 B형 (복원)  ―  로봇 이동
시험일 : 2026-08-29   결과: 못품 (시험장)   복원+검증: 2026-08-29
한도   : Python 8초 (25 TC 합산)

분류   : 방향 상태 BFS  visited[y][x][dir]  +  roads(셀별 가능방향 set)  +  경유지 순열(≤120)
핵심   : 일반도로=현재 방향만 진행 / 교차로=roads[y][x]의 모든 방향으로 분기.
         출입구 진입은 진행방향 오른쪽 한 칸.

⚠️ 복원 주의 : '건물 하나만 있어도 도로 네 꼭짓점이 교차로'로 모델링했다.
   원문이 '여러 건물 도로가 만나는 곳만 교차로'라면 경로가 달라진다(미확정).

[검증] mask 버전과 set 버전이 유효 테케 22개 move 전부 일치.
       유효 테케 5개 자기채점 전부 100점.
"""

from collections import deque
from itertools import permutations

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

dy = [-1, 0, 1, 0]
dx = [0, 1, 0, -1]

g_N = 0
roads = []      # roads[y][x] = {가능한 시계방향 방향들의 set}
cross = []
buildings = {}


class Building:
    def __init__(self, x, y, w, h, door_y, door_x, road_y, road_x, start_dir):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.door_y = door_y
        self.door_x = door_x
        self.road_y = road_y
        self.road_x = road_x
        self.start_dir = start_dir


def init(N):
    global g_N, roads, cross, buildings
    g_N = N
    roads = [[set() for _ in range(N)] for _ in range(N)]
    cross = [[False] * N for _ in range(N)]
    buildings = {}


def build(mID, mX, mY, mW, mH, mDoorX, mDoorY):
    L = mX - 1
    R = mX + mW
    T = mY - 1
    B = mY + mH

    for x in range(L, R):
        roads[T][x].add(RIGHT)
    for y in range(T, B):
        roads[y][R].add(DOWN)
    for x in range(R, L, -1):
        roads[B][x].add(LEFT)
    for y in range(B, T, -1):
        roads[y][L].add(UP)

    cross[T][L] = True
    cross[T][R] = True
    cross[B][R] = True
    cross[B][L] = True

    door_x = mX + mDoorX
    door_y = mY + mDoorY

    if mDoorY == 0:
        road_y = door_y - 1
        road_x = door_x
        start_dir = RIGHT
    elif mDoorX == mW - 1:
        road_y = door_y
        road_x = door_x + 1
        start_dir = DOWN
    elif mDoorY == mH - 1:
        road_y = door_y + 1
        road_x = door_x
        start_dir = LEFT
    else:
        road_y = door_y
        road_x = door_x - 1
        start_dir = UP

    buildings[mID] = Building(mX, mY, mW, mH, door_y, door_x,
                              road_y, road_x, start_dir)


def bfs_all(start_id, target_ids):
    start = buildings[start_id]
    target_set = set(target_ids)
    result = {}

    if start_id in target_set:
        result[start_id] = 0

    door_map = {}
    for target_id in target_set:
        if target_id == start_id:
            continue
        target = buildings[target_id]
        door_map[(target.door_y, target.door_x)] = target_id

    if len(result) == len(target_set):
        return result

    visited = [[[-1] * 4 for _ in range(g_N)] for _ in range(g_N)]
    q = deque()

    sy = start.road_y
    sx = start.road_x
    sd = start.start_dir
    visited[sy][sx][sd] = 1
    q.append((sy, sx, sd))

    while q:
        y, x, d = q.popleft()
        cur_dist = visited[y][x][d]

        right_dir = (d + 1) % 4
        door_y = y + dy[right_dir]
        door_x = x + dx[right_dir]
        target_id = door_map.get((door_y, door_x))
        if target_id is not None and target_id not in result:
            result[target_id] = cur_dist + 1
            if len(result) == len(target_set):
                return result

        if cross[y][x]:
            for nd in roads[y][x]:
                ny = y + dy[nd]
                nx = x + dx[nd]
                if not (0 <= ny < g_N and 0 <= nx < g_N):
                    continue
                if visited[ny][nx][nd] != -1:
                    continue
                visited[ny][nx][nd] = cur_dist + 1
                q.append((ny, nx, nd))
        else:
            if d not in roads[y][x]:
                continue
            ny = y + dy[d]
            nx = x + dx[d]
            if not (0 <= ny < g_N and 0 <= nx < g_N):
                continue
            if visited[ny][nx][d] != -1:
                continue
            visited[ny][nx][d] = cur_dist + 1
            q.append((ny, nx, d))

    return result


def move(mStart, mEnd, M, mID):
    via = mID[:M]
    nodes = [mStart] + via + [mEnd]
    unique_nodes = list(dict.fromkeys(nodes))

    INF = 10 ** 18
    pair_dist = {}
    for src in unique_nodes:
        result = bfs_all(src, unique_nodes)
        for dst in unique_nodes:
            pair_dist[(src, dst)] = result.get(dst, INF)

    if M == 0:
        return pair_dist[(mStart, mEnd)]

    answer = INF
    for order in permutations(via):
        cur = mStart
        total = 0
        for nxt in order:
            total += pair_dist[(cur, nxt)]
            if total >= answer:
                break
            cur = nxt
        else:
            total += pair_dist[(cur, mEnd)]
            answer = min(answer, total)
    return answer
