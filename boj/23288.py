"""
BOJ 23288  주사위 굴리기 2
https://cosal.aviss.kr/problems/detail/23288

풀이일 : 2026-08-30   결과: 품
한도   : time 2 초 / memory 1024 MB

[채점] accepted  22/22  (7.361s)

[문제]
크기가 N×M인 지도가 존재한다. 지도의 오른쪽은 동쪽, 위쪽은 북쪽이다. 지도의 좌표는 (r, c)로 나타내며, r는 북쪽으로부터 떨어진 칸의 개수, c는 서쪽으로부터 떨어진 칸의 개수이다. 가장 왼쪽 위에 있는 칸의 좌표는 (1, 1)이고, 가장 오른쪽 아래에 있는 칸의 좌표는 (N, M)이다. 이 지도의 위에 주사위가 하나 놓여져 있으며, 주사위의 각 면에는 1보다 크거나 같고, 6보다 작거나 같은 정수가 하나씩 있다. 주사위 한 면의 크기와 지도 한 칸의 크기는 같고, 주사위의 전개도는 아래와 같다.

  2
4 1 3
  5
  6

주사위는 지도 위에 윗 면이 1이고, 동쪽을 바라보는 방향이 3인 상태로 놓여져 있으며, 놓여져 있는 곳의 좌표는 (1, 1) 이다. 지도의 각 칸에도 정수가 하나씩 있다. 가장 처음에 주사위의 이동 방향은 동쪽이다. 주사위의 이동 한 번은 다음과 같은 방식으로 이루어진다.

주사위가 이동 방향으로 한 칸 굴러간다. 만약, 이동 방향에 칸이 없다면, 이동 방향을 반대로 한 다음 한 칸 굴러간다. 주사위가 도착한 칸 (x, y)에 대한 점수를 획득한다. 주사위의 아랫면에 있는 정수 A와 주사위가 있는 칸 (x, y)에 있는 정수 B를 비교해 이동 방향을 결정한다. A > B인 경우 이동 방향을 90도 시계 방향으로 회전시킨다. A < B인 경우 이동 방향을 90도 반시계 방향으로 회전시킨다. A = B인 경우 이동 방향에 변화는 없다.

칸 (x, y)에 대한 점수는 다음과 같이 구할 수 있다. (x, y)에 있는 정수를 B라고 했을때, (x, y)에서 동서남북 방향으로 연속해서 이동할 수 있는 칸의 수 C를 모두 구한다. 이때 이동할 수 있는 칸에는 모두 정수 B가 있어야 한다. 여기서 점수는 B와 C를 곱한 값이다.

보드의 크기와 각 칸에 있는 정수, 주사위의 이동 횟수 K가 주어졌을때, 각 이동에서 획득하는 점수의 합을 구해보자.

이 문제의 예제 1부터 7은 같은 지도에서 이동하는 횟수만 증가시키는 방식으로 구성되어 있다. 예제 8은 같은 지도에서 이동하는 횟수를 매우 크게 만들었다.

[예제 1]
입력:
4 5 1
4 1 2 3 3
6 1 1 3 3
5 6 1 3 2
5 5 6 5 5
출력:
4

[예제 2]
입력:
4 5 2
4 1 2 3 3
6 1 1 3 3
5 6 1 3 2
5 5 6 5 5
출력:
8

[예제 3]
입력:
4 5 3
4 1 2 3 3
6 1 1 3 3
5 6 1 3 2
5 5 6 5 5
출력:
14

[예제 4]
입력:
4 5 4
4 1 2 3 3
6 1 1 3 3
5 6 1 3 2
5 5 6 5 5
출력:
18

[예제 5]
입력:
4 5 5
4 1 2 3 3
6 1 1 3 3
5 6 1 3 2
5 5 6 5 5
출력:
24

[예제 6]
입력:
4 5 6
4 1 2 3 3
6 1 1 3 3
5 6 1 3 2
5 5 6 5 5
출력:
28

[예제 7]
입력:
4 5 7
4 1 2 3 3
6 1 1 3 3
5 6 1 3 2
5 5 6 5 5
출력:
43

[예제 8]
입력:
4 5 1000
4 1 2 3 3
6 1 1 3 3
5 6 1 3 2
5 5 6 5 5
출력:
3901
"""

import sys
from collections import deque
input = sys.stdin.readline

N, M, K = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(N)]

dice = [0] * 6

for i in range(1, 7):
    dice[i - 1] = i - 1

EAST = 0
SOUTH = 1
WEST = 2
NORTH = 3

north_dict = {
    0: 4,
    1: 0,
    2: 2,
    3: 3,
    4: 5,
    5: 1
}
south_dict = {
    0: 1,
    1: 5,
    2: 2,
    3: 3,
    4: 0,
    5: 4
}
east_dict = {
    0: 3,
    1: 1,
    2: 0,
    3: 5,
    4: 4,
    5: 2
}
#   1
# 3 0 2
#   4
#   5
west_dict = {
    0: 2,
    1: 1,
    2: 5,
    3: 0,
    4: 4,
    5: 3
}

dice_changer = {
    0: east_dict,
    1: south_dict,
    2: west_dict,
    3: north_dict
}


def move(direction):
    cur_dict = dice_changer[direction]

    new_dice = [0] * 6
    for key, value in cur_dict.items():
        new_dice[key] = dice[value]

    return new_dice


# 5 가 바닥임
def rotate(cur_dir):
    return (cur_dir + 1) % 4


def re_rotate(cur_dir):
    return (cur_dir + 3) % 4

first_dir = 0

dydx = [[0, 1], [1, 0], [0, -1], [-1, 0]]
total_score = 0

score_board = [[0] * M for _ in range(N)]

def make_score_board(sy, sx):
    visited = set()
    visited.add((sy, sx))
    q = deque()
    q.append((sy, sx))
    cnt = 1
    start_num = board[sy][sx]
    while q:
        cy, cx = q.popleft()
        for dy, dx in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            ny = cy + dy
            nx = cx + dx
            if not (0 <= ny < N and 0 <= nx < M):
                continue
            if board[ny][nx] != start_num:
                continue
            if (ny, nx) in visited:
                continue
            visited.add((ny, nx))
            q.append((ny, nx))
            cnt += 1
    for y, x in visited:
        score_board[y][x] = cnt * start_num

for y in range(N):
    for x in range(M):
        if score_board[y][x] == 0:
            make_score_board(y, x)

# for i in score_board:
#     print(i)

cy = 0
cx = 0

def move_dice(sy, sx, cur_dir):
    global first_dir, total_score, cy, cx, dice
    dy, dx = dydx[cur_dir]
    ny = sy + dy
    nx = sx + dx
    if not (0 <= ny < N and 0 <= nx < M):
        ny = sy - dy
        nx = sx - dx
        first_dir = (first_dir + 2) % 4
    total_score += score_board[ny][nx]
    dice = move(first_dir)
    if (dice[5] + 1) > board[ny][nx]:
        first_dir = rotate(first_dir)
    elif (dice[5] + 1) < board[ny][nx]:
        first_dir = re_rotate(first_dir)
    cy = ny
    cx = nx
#
# print("debug score board")
# for i in score_board:
#     print(i)

for k in range(K):
    move_dice(cy, cx, first_dir)
    # print(cy, cx)

print(total_score)
