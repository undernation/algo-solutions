"""
CT 118  비를 피하기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-stay-out-of-rain/description

풀이일 : 2026-10-07   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 66.5%
제약   : - $2 \le N \le 100$
제약   : - $1 \le H,\ M \le N \times N$
제약   : - $H + M \le N \times N$
제약   : - $\texttt{격자 값} \in \{0, 1, 2, 3\}$
제약   : - 격자 내 값이 $2$인 칸은 정확히 $H$개, 값이 $3$인 칸은 정확히 $M$개입니다.

[채점] accepted  2/2  (0.693s)

[문제]
정수 $0$, $1$, $2$, $3$로만 이루어진 $N \times N $격자에서 사람이 $H$명 겹치지 않게 서 있고, 비를 피할 수 있는 공간의 위치 $M$개가 주어졌을 때 각 사람마다 비를 피할 수 있는 가장 가까운 공간까지의 거리를 구하는 프로그램을 작성해보세요. 정수 $0$은 해당 칸이 이동할 수 있는 곳임을, 정수 $1$은 벽이 있어 해당 칸이 이동할 수 없는 곳임을 의미합니다. 정수 $2$는 해당 칸에 사람이 서있음을 의미하고, 정수 $3$은 해당 공간이 비를 피할 수 있는 공간임을 의미합니다. 사람은 상하좌우 인접한 곳으로만 움직일 수 있으며 한 칸 움직이는 데 정확히 $1$초가 소요됩니다. 벽이 아닌 곳은 전부 이동이 가능합니다.

[예제 1]
입력:
3 1 1
1 2 0
3 1 0
0 0 0

출력:
0 6 0
0 0 0
0 0 0


[예제 2]
입력:
4 5 2
1 2 0 1
3 1 1 2
2 1 2 0
2 0 0 3

출력:
0 -1 0 0
0 0 0 2
1 0 2 0
2 0 0 0

"""

from collections import deque

N, H, M = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(N)]

# Please write your code here.

humans = []
spaces = []
for i in range(N):
    for j in range(N):
        if grid[i][j] == 2:
            humans.append((i, j))
        elif grid[i][j] == 3:
            spaces.append((i, j))
INF = 10 ** 18
ans_board = [[INF] * N for _ in range(N)]


def bfs(sy, sx):
    global ans_board

    q = deque()
    q.append((sy, sx))
    ans_board[sy][sx] = 0

    while q:
        cy, cx = q.popleft()
        for dy, dx in [[1, 0], [-1, 0], [0, -1], [0, 1]]:
            ny = cy + dy
            nx = cx + dx
            if not (0 <= ny < N and 0 <= nx < N):
                continue

            if grid[ny][nx] == 1:
                continue

            if ans_board[ny][nx] > ans_board[cy][cx] + 1:
                ans_board[ny][nx] = ans_board[cy][cx] + 1
                q.append((ny, nx))



real_answer = [[0] * N for _ in range(N)]
for i, j in spaces:
    bfs(i, j)
# for i in ans_board:
#     print(i)
for i, j in humans:
    if ans_board[i][j] != INF:
        real_answer[i][j] = ans_board[i][j]
    else:
        real_answer[i][j] = -1

for i in real_answer:
    print(*i)
