"""
CT 117  K개의 벽 없애기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-remove-k-walls/description

풀이일 : 2026-10-07   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 65.7%
제약   : - $3 \le N \le 100$
제약   : - $0 \le K \le \texttt{입력으로 주어지는 초기 벽의 개수} \le 8$
제약   : - $1 \le r_1,\ c_1,\ r_2,\ c_2 \le N$
제약   : - 시작 위치 $(r_1, c_1)$과 도착 위치 $(r_2, c_2)$의 칸 값은 항상 $0$입니다.

[채점] accepted  2/2  (0.779s)

[문제]
정수 $0$, $1$로만 이루어진 $N \times N$ 격자가 주어졌을 때, $K$개의 벽을 적절하게 없애 시작점으로부터 상하좌우 인접한 곳으로만 계속 이동하여 도착점까지 도달하는 데 걸리는 시간을 최소로 하는 프로그램을 작성해보세요. 정수 $0$은 해당 칸이 이동할 수 있는 곳임을, 정수 $1$은 벽이 있어 해당 칸이 이동할 수 없는 곳임을 의미합니다. 한 칸을 이동하는 데에는 정확히 $1$초의 시간이 소요됩니다.

[예제 1]
입력:
4 2
0 0 0 0
0 1 1 1
1 1 1 1
0 1 0 0
1 1
4 4

출력:
6


[예제 2]
입력:
4 2
0 1 0 0
1 0 0 1
0 0 1 1
0 1 1 0
1 1
4 4

출력:
-1

"""

from collections import deque
from itertools import combinations

N, K = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(N)]
r1, c1 = map(int, input().split())
r2, c2 = map(int, input().split())

r1 -= 1
c1 -= 1
r2 -= 1
c2 -= 1

# Please write your code here.

walls = []
for i in range(N):
    for j in range(N):
        if grid[i][j] == 1:
            walls.append((i, j))

answer = 10 ** 18


def bfs():
    q = deque()
    visited = [[-1] * N for _ in range(N)]

    q.append((r1, c1))
    visited[r1][c1] = 0

    while q:
        cy, cx = q.popleft()
        for dy, dx in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            ny = cy + dy
            nx = cx + dx
            if not (0 <= ny < N and 0 <= nx < N):
                continue

            if visited[ny][nx] != -1:
                continue
            if grid[ny][nx] == 1:
                continue
            visited[ny][nx] = visited[cy][cx] + 1
            if ny == r2 and nx == c2:
                return visited[ny][nx]
            q.append((ny, nx))

    return 10 ** 18


for combi in combinations(walls, K):

    for a, b in combi:
        grid[a][b] = 0

    answer = min(answer, bfs())

    for a, b in combi:
        grid[a][b] = 1

if answer == 10 ** 18:
    print(-1)
else:
    print(answer)
