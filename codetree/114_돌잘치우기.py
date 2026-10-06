"""
CT 114  돌 잘 치우기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-clear-stones-well/description

풀이일 : 2026-10-06   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 54.0%
제약   : - $3 \le N \le 100$
제약   : - $1 \le K \le N \times N$
제약   : - $0 \le M \le \texttt{초기 입력에서 돌의 개수} \le 8$
제약   : - $\texttt{격자 값} \in \{0, 1\}$
제약   : - $1 \le r,\ c \le N$
제약   : - 모든 시작점 위치의 격자 값은 $0$이며, 시작점끼리 서로 겹치지 않습니다.

[채점] accepted  2/2  (0.72s)

[문제]
정수 $0$, $1$로만 이루어진 $N \times N$ 격자가 주어졌습니다.

$1$이 돌을 나타낸다 할 때, 주어진 돌 중 $M$개의 돌만 적절하게 치워 $K$개의 시작점으로부터 상하좌우 인접한 곳으로만 이동하여 도달 가능한 칸의 수를 최대로 하는 프로그램을 작성해보세요.

정수 $0$은 해당 칸이 이동할 수 있는 곳임을, 정수 $1$은 돌이 있어 해당 칸이 이동할 수 없는 곳임을 의미합니다.

[예제 1]
입력:
3 2 1
0 0 0
0 0 1
1 0 0
1 1
1 2

출력:
8


[예제 2]
입력:
4 2 2
0 1 1 0
0 1 1 0
0 1 1 1
0 1 0 0
1 4
4 4

출력:
10

"""

from collections import deque
from itertools import combinations

N, K, M = map(int, input().split())

grid = [list(map(int, input().split())) for _ in range(N)]


stones = []
answer = 0
start_pos = []
for _ in range(K):
    ri, ci = map(int, input().split())
    start_pos.append((ri - 1, ci - 1))

# Please write your code here.

for i in range(N):
    for j in range(N):
        if grid[i][j] == 1:
            stones.append((i, j))


stone_cnt = len(stones)

for comb in combinations(stones, M):

    for a, b in comb:
        grid[a][b] = 0

    q = deque()
    visited = set()

    for a, b in start_pos:
        visited.add((a, b))
        q.append((a, b))

    while q:
        cy, cx = q.popleft()

        for dy, dx in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            ny = dy + cy
            nx = cx + dx

            if not (0<= ny < N and 0 <= nx < N):
                continue

            if (ny, nx) in visited:
                continue

            if grid[ny][nx] == 1:
                continue

            visited.add((ny, nx))
            q.append((ny, nx))

    answer = max(answer, len(visited))


    for a, b in comb:
        grid[a][b] = 1

print(answer)
