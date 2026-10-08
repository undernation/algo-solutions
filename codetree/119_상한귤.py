"""
CT 119  상한 귤
https://www.codetree.ai/ko/trails/complete/curated-cards/test-oranges-have-gone-bad/description

풀이일 : 2026-10-08   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 72.0%
제약   : - $2 \le N \le 100$
제약   : - $1 \le K \le N \times N$
제약   : - $0 \le \texttt{주어지는 정수} \le 2$
제약   : - 격자 내 값이 $2$인 칸은 정확히 $K$개입니다.

[채점] accepted  2/2  (0.697s)

[문제]
$0$, $1$, $2$로만 이루어진 $N \times N$ 격자에서 $0$초에 $K$개의 상한 귤로부터 시작하여 $1$초에 한 번씩 모든 상한 귤로부터 상하좌우로 인접한 곳에 있는 귤이 동시에 전부 상하게 될 때, 각 귤마다 최초로 상하게 되는 시간을 구하는 프로그램을 작성해보세요. $0$은 해당 칸에 아무것도 놓여있지 않음을, $1$은 해당 칸에 귤이 놓여있음을, $2$는 해당 칸에 상한 귤이 처음부터 놓여 있음을 의미합니다.

[예제 1]
입력:
3 1
1 1 1
1 0 1
1 0 2

출력:
4 3 2
5 -1 1
6 -1 0


[예제 2]
입력:
4 2
0 0 1 0
1 1 1 2
0 2 1 0
0 0 0 1

출력:
-1 -1 2 -1
2 1 1 0
-1 0 1 -1
-1 -1 -1 -2

"""

from collections import deque

N, K = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(N)]

# Please write your code here.

visited = [[-1] * N for _ in range(N)]
q = deque()
for i in range(N):
    for j in range(N):
        if grid[i][j] == 2:
            visited[i][j] = 0
            q.append((i, j))

        elif grid[i][j] == 1:
            visited[i][j] = -2


while q:
    cy, cx = q.popleft()

    for dy, dx in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
        ny = cy + dy
        nx = cx + dx

        if not (0 <= ny < N and 0 <= nx < N):
            continue

        if grid[ny][nx] == 0:
            continue
        if visited[ny][nx] >= 0:
            continue

        visited[ny][nx] = visited[cy][cx] + 1
        q.append((ny, nx))

for i in visited:
    print(*i)
