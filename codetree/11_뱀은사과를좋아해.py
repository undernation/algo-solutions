"""
CT 11  뱀은 사과를 좋아해
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-snake-loves-apples/description

풀이일 : 2026-10-09   결과: 품
한도   : time Python3 1.5초 · C++17 1초 / memory 128 MB / time_sec 1.5
난이도 : Hard  |  정답률 41.9%
제약   : - $1 \le N \le 100$
제약   : - $0 \le M \lt N \times N$
제약   : - $0 \le K \le 1\,000$
제약   : - $1 \le x \le N$
제약   : - $1 \le y \le N$
제약   : - $1 \le  p \le 100$

[채점] accepted  3/3  (1.01s)

[문제]
$N \times N$ 크기의 격자 안에서 사과들의 위치와 뱀의 움직임이 주어졌을 때, 게임이 끝나는데 몇 초가 걸리는지를 구하는 프로그램을 작성해보세요.

뱀은 처음에 좌측 상단 $(1,\ 1)$에서 길이 $1$의 상태로 있습니다.

![](https://contents.codetree.ai/problems/11/images/problems-a19c5881-1b86-4d2b-a726-959c5ff0a280.png)

일반적으로 뱀은 이동시에 머리를 특정 방향으로 한 칸 옮기게 되고, 가장 끝에 있던 꼬리가 사라지게 되며 이 과정은 동시에 일어납니다. 특히 새로 이동한 머리 자리가 이번 이동으로 사라지는 꼬리 자리와 같더라도, 꼬리가 먼저 빠지는 것으로 간주하여 몸이 겹치지 않은 것으로 처리합니다.

![](https://contents.codetree.ai/problems/11/images/problems-c4953ae1-3bbb-4a6c-9351-66c57b6ae6c1.png)


이때 만약 움직인 장소에 사과가 존재한다면 꼬리가 사라지지 않고 몸의 길이가 1 늘어나게 됩니다. 또, 사과는 먹는 즉시 사라지게 됩니다.

![](https://contents.codetree.ai/problems/11/images/problems-e06f4244-81f6-417d-b1ef-177357607336.png)


뱀이 움직이는 데에는 $1$초의 시간이 소요됩니다.

게임은 주어진 $K$개의 명령을 모두 수행했거나, 움직이는 도중 격자를 벗어났거나, 움직이는 도중 몸이 꼬여 서로 겹쳐졌을 경우 종료됩니다.

[예제 1]
입력:
3 0 2
R 2
D 2

출력:
4


[예제 2]
입력:
2 0 2
R 3
D 2

출력:
2


[예제 3]
입력:
5 4 5
1 2
1 3
1 4
1 5
R 4
D 1
L 1
U 1
L 2

출력:
7

"""

from collections import deque

N, M, K = map(int, input().split())
board = [[0] * N for _ in range(N)]

DIR = {
    "U": (-1, 0),
    "D": (1, 0),
    "R": (0, 1),
    "L": (0, -1)
}


for _ in range(M):
    xi, yi = map(int, input().split())
    xi -= 1
    yi -= 1
    board[xi][yi] = 2

commands = []
for _ in range(K):
    di, pi = input().split()
    commands.append((di, int(pi)))

# Please write your code here.

board[0][0] = 1
snake = deque()
snake.append((0, 0))

def move(direction):
    hy, hx = snake[0]
    is_over = False

    ty, tx = snake[-1]

    dy, dx = DIR[direction]
    ny = hy + dy
    nx = hx + dx

    board[ty][tx] = 0

    # 밖으로 나간 경우
    if not (0 <= ny < N and 0 <= nx < N):
        return True
    # 몸통인경우
    if board[ny][nx] == 1:
        return True
    # 사과 인 경우
    elif board[ny][nx] == 2:
        # 꼬리 다시 붙여주기
        board[ty][tx] = 1
        snake.appendleft((ny, nx))
        board[ny][nx] = 1
        return False
    else:
        snake.appendleft((ny, nx))
        board[ny][nx] = 1
        snake.pop()
        return False
is_over = False
time = 0
for direction, num in commands:

    for n in range(num):
        time += 1
        ret = move(direction)
        if ret:
            is_over = True
            break

    if is_over:
        break
print(time)
