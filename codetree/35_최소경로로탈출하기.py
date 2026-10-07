"""
CT 35  최소 경로로 탈출하기
https://www.codetree.ai/ko/trails/complete/curated-cards/intro-escape-with-min-distance/description

풀이일 : 2026-10-07   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 256 MB / time_sec 1
난이도 : Easy  |  정답률 55.7%
제약   : - $2 \le N,\ M \le 100$
제약   : - 격자의 각 칸의 값은 뱀이 없는 경우 $1$, 뱀이 있는 경우 $0$입니다.
제약   : - 시작 지점과 도착 지점에는 뱀이 주어지지 않음이 보장됩니다.

[채점] accepted  2/2  (0.724s)

[문제]
$N \times M$ 크기의 이차원 영역의 좌측 상단에서 출발하여 우측 하단까지 뱀에게 물리지 않고 탈출하려고 합니다. 이동을 할 때에는 반드시 상하좌우에 인접한 칸으로만 이동할 수 있으며, 뱀이 있는 칸으로는 이동을 할 수 없습니다. 예를 들어 \[그림 1]과 같이 뱀이 배치되어 있는 경우 실선과 같은 경로로 탈출을 할 수 있습니다. 탈출 가능한 경로의 최소 이동 횟수를 출력하는 코드를 작성해보세요.

![](https://contents.codetree.ai/problems/35/images/problems-2c4aafa1-b572-44fd-b25c-cc117cd55e03.png)

[예제 1]
입력:
5 5
1 0 1 1 1
1 0 1 0 1
1 0 1 1 1
1 0 1 0 1
1 1 1 0 1

출력:
12


[예제 2]
입력:
5 5
1 1 1 1 1
1 0 1 0 1
1 1 1 1 1
1 0 1 0 1
1 1 1 0 1

출력:
8

"""

from collections import deque


N, M = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(N)]

# Please write your code here.

visited_board = [[-1] * M for _ in range(N)]

q = deque()
visited_board[0][0] = 0

q.append((0, 0))

while q:
    cy, cx = q.popleft()

    for dy, dx in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
        ny = cy + dy
        nx = cx + dx
        if not (0 <= ny < N and 0 <= nx < M):
            continue

        if board[ny][nx] == 0:
            continue

        if visited_board[ny][nx] != -1:
            continue

        visited_board[ny][nx] = visited_board[cy][cx] + 1
        q.append((ny, nx))

print(visited_board[N - 1][M - 1])
