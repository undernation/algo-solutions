"""
CT 112  갈 수 있는 곳들
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-places-can-go/description

풀이일 : 2026-10-06   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Easy  |  정답률 63.2%
제약   : - $1 \le N \le 100$
제약   : - $1 \le K \le N \times N$
제약   : - $1 \le i \le K$
제약   : - $1 \le r_i, c_i \le N$
제약   : - 격자의 각 칸의 값은 $0$ 또는 $1$
제약   : - 모든 시작점은 서로 다른 위치이며, 시작점의 격자 값은 $0$

[채점] accepted  2/2  (0.697s)

[문제]
정수 $0$, $1$로만 이루어진 $N \times N$ 격자가 주어졌을 때, $K$개의 시작점으로부터 상하좌우 인접한 곳으로만 이동하여 도달 가능한 칸의 수를 구하는 프로그램을 작성해보세요. 

정수 $0$은 해당 칸이 이동할 수 있는 곳임을, 정수 $1$은 해당 칸이 이동할 수 없는 곳임을 의미합니다.

[예제 1]
입력:
3 2
0 0 0
0 0 1
1 0 0
1 1
1 2

출력:
7


[예제 2]
입력:
4 2
0 1 0 0
0 1 0 0
0 1 1 1
0 1 0 0
1 4
4 4

출력:
6

"""

from collections import deque

N, K = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(N)]
points = [tuple(map(int, input().split())) for _ in range(K)]

# Please write your code here.


visited = set()

q = deque()

for a, b in points:
    q.append((a - 1, b - 1))
    visited.add((a - 1, b - 1))

while q:
    cy, cx = q.popleft()

    for dy, dx in [[1, 0], [-1, 0], [0, -1], [0, 1]]:
        ny = cy + dy
        nx = cx + dx
        if not (0 <= ny < N and 0 <= nx < N):
            continue

        if (ny, nx) in visited:
            continue
        if grid[ny][nx] == 1:
            continue

        q.append((ny, nx))
        visited.add((ny, nx))

print(len(visited))
