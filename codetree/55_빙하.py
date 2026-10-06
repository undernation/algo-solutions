"""
CT 55  빙하
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-glacier/description

풀이일 : 2026-10-06   결과: 품
한도   : time Python3 3초 · C++17 1초 / memory 128 MB / time_sec 3
난이도 : Hard  |  정답률 52.9%
제약   : - $3 \le N \le 200$
제약   : - $3 \le M \le 200$
제약   : - 격자의 각 원소는 $0$ 또는 $1$입니다.
제약   : - 격자의 가장 바깥 부분(첫 번째·마지막 행, 첫 번째·마지막 열)은 항상 물($0$)입니다.
제약   : - 입력으로 주어지는 초기 빙하의 크기는 $1$ 이상입니다.

[채점] accepted  2/2  (0.696s)

[문제]
$N \times M$ 크기의 격자 안에 빙하의 정보가 주어집니다. 격자의 가장 바깥 부분은 항상 빙하가 아니고, 빙하를 제외한 나머지 위치에는 전부 물이 채워져 있습니다. 정수 $1$은 빙하를, 정수 $0$은 물을 나타냅니다.

![](https://contents.codetree.ai/problems/55/images/problems-3c4f6ce1-0faa-481a-96cd-1c62e47c37b8.png)

여기서 어떤 물 칸이 격자의 가장자리에 있는 물 칸에서 물끼리 상하좌우로만 이동해 도달할 수 있으면 이를 바깥물이라 부르고, 그렇지 않으면 (즉 사방이 빙하로 막혀 도달할 수 없으면) 빙하로 둘러싸인 물이라 부릅니다. 빙하로 둘러싸인 물은 빙하를 녹이지 못하며, 오직 바깥물에 상하좌우로 인접한 빙하 칸만이 녹습니다.

빙하는 다음과 같은 규칙으로 매초 녹습니다.

+ 매초 시작 시점의 격자 상태를 기준으로, 바깥물에 상하좌우로 인접한 모든 빙하 칸을 동시에 녹입니다.
+ 이번 초에 녹은 빙하 칸들은 다음 초부터 물로 취급됩니다. 즉 같은 초 안에서는 연쇄적으로 추가로 녹지 않습니다.

다음의 경우 역시 안쪽에 있는 $0$들은 빙하로 둘러싸인 물이므로 빙하가 녹는데 영향을 주지 못합니다.

![](https://contents.codetree.ai/problems/55/images/problems-3822d834-9438-43d9-b862-f0688c571a7a.png)

맨 위에서 주어진 예시의 경우 안쪽에 있는 $0$은 빙하로 둘러싸여 있으므로 바깥쪽에 있는 $0$만이 빙하가 녹는데 영향을 미칩니다.

![](https://contents.codetree.ai/problems/55/images/problems-6ba22421-4676-4639-b340-868fc9a7478c.png)

빙하가 전부 녹는데 걸리는 시간과, 마지막 초에 녹아 사라지는 빙하 칸의 수($1$의 개수)를 구하는 프로그램을 작성합니다.

위의 예에서는 빙하가 녹는데 $2$초의 시간이 소요되며, 마지막 초에 녹는 빙하 칸이 $4$개입니다.

[예제 1]
입력:
3 3
0 0 0
0 1 0
0 0 0

출력:
1 1


[예제 2]
입력:
6 7
0 0 0 0 0 0 0
0 1 1 1 1 0 0
0 1 1 0 1 1 0
0 1 0 1 1 1 0
0 1 1 1 1 1 0
0 0 0 0 0 0 0

출력:
2 4

"""

from collections import deque

N, M = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(N)]

# Please write your code here.


visited = set()

last_cnt = 0

q = deque()
visited.add((0, 0))
q.append((0, 0))
nxt_q = deque()


def bfs():
    global last_cnt, q, nxt_q
    nxt_q = deque()

    while q:
        cy, cx = q.popleft()

        for dy, dx in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            ny = cy + dy
            nx = cx + dx

            if not (0 <= ny < N and 0 <= nx < M):
                continue

            if (ny, nx) in visited:
                continue

            # 다음게 1인경우
            if board[ny][nx] == 1:
                visited.add((ny, nx))
                nxt_q.append((ny, nx))
                board[ny][nx] = 0
            # 다음게 0 인 경우
            else:
                visited.add((ny, nx))
                q.append((ny, nx))


time = 0

while True:

    bfs()


    # print("debug")
    # for i in board:
    #     print(i)

    if len(nxt_q) == 0:
        print(time, last_cnt)
        break
    else:
        last_cnt = len(nxt_q)

    q = nxt_q.copy()
    time += 1
