"""
BOJ 17143  낚시왕
https://cosal.aviss.kr/problems/detail/17143

풀이일 : 2026-08-18   결과: 품
한도   : time 1 초 / memory 512 MB

[채점] accepted  20/20  (5.831s)

[문제]
낚시왕이 상어 낚시를 하는 곳은 크기가 R×C인 격자판으로 나타낼 수 있다. 격자판의 각 칸은 (r, c)로 나타낼 수 있다. r은 행, c는 열이고, (R, C)는 아래 그림에서 가장 오른쪽 아래에 있는 칸이다. 칸에는 상어가 최대 한 마리 들어있을 수 있다. 상어는 크기와 속도를 가지고 있다.

[[IMG:1]]

낚시왕은 처음에 1번 열의 한 칸 왼쪽에 있다. 다음은 1초 동안 일어나는 일이며, 아래 적힌 순서대로 일어난다. 낚시왕은 가장 오른쪽 열의 오른쪽 칸에 이동하면 이동을 멈춘다.
- 낚시왕이 오른쪽으로 한 칸 이동한다.
- 낚시왕이 있는 열에 있는 상어 중에서 땅과 제일 가까운 상어를 잡는다. 상어를 잡으면 격자판에서 잡은 상어가 사라진다.
- 상어가 이동한다.
상어는 입력으로 주어진 속도로 이동하고, 속도의 단위는 칸/초이다. 상어가 이동하려고 하는 칸이 격자판의 경계를 넘는 경우에는 방향을 반대로 바꿔서 속력을 유지한채로 이동한다.
왼쪽 그림의 상태에서 1초가 지나면 오른쪽 상태가 된다. 상어가 보고 있는 방향이 속도의 방향, 왼쪽 아래에 적힌 정수는 속력이다. 왼쪽 위에 상어를 구분하기 위해 문자를 적었다.

[[IMG:2]]

상어가 이동을 마친 후에 한 칸에 상어가 두 마리 이상 있을 수 있다. 이때는 크기가 가장 큰 상어가 나머지 상어를 모두 잡아먹는다.
낚시왕이 상어 낚시를 하는 격자판의 상태가 주어졌을 때, 낚시왕이 잡은 상어 크기의 합을 구해보자.

[예제 1]
입력:
4 6 8
4 1 3 3 8
1 3 5 2 9
2 4 8 4 1
4 5 0 1 4
3 3 1 2 7
1 5 8 4 3
3 6 2 1 2
2 2 2 3 5
출력:
22

[예제 2]
입력:
100 100 0
출력:
0

[예제 3]
입력:
4 5 4
4 1 3 3 8
1 3 5 2 9
2 4 8 4 1
4 5 0 1 4
출력:
22

[예제 4]
입력:
2 2 4
1 1 1 1 1
2 2 2 2 2
1 2 1 2 3
2 1 2 1 4
출력:
4
"""

import sys

# sys.stdin = open("input.txt", "r")

input = sys.stdin.readline

R, C, M = map(int, input().split())

board = {}

dydx = [[-1, 0], [1, 0], [0, 1], [0, -1]]

sharks = []

for num in range(M):
    r, c, s, d, z = map(int, input().split())
    r -= 1
    c -= 1
    d -= 1

    sharks.append([num, r, c, s, d, z])
    temp = board.get((r, c), -1)

    if temp == -1:
        board[(r, c)] = []
        board[(r, c)].append(num)
    else:
        board[(r, c)].append(num)
is_alive = [True] * M

answer = 0

def change_dir(cur_dir):
    if cur_dir == 0:
        return 1

    elif cur_dir == 1:
        return 0

    elif cur_dir == 2:
        return 3

    else:
        return 2


def move(sy, sx, direction, speed):
    cy = sy
    cx = sx
    dy, dx = dydx[direction]
    for _ in range(speed):
        ny = cy + dy
        nx = cx + dx
        if not (0 <= ny < R and 0 <= nx < C):
            # 방향 바꿔서 이동
            direction = change_dir(direction)
            dy, dx = dydx[direction]
            ny = cy + dy
            nx = cx + dx
        cy = ny
        cx = nx
    return cy, cx, direction

def debug():
    board = [[-1] * C for _ in range(R)]
    for i in range(M):
        if not is_alive[i]:
            continue
        num, r, c, s, d, z = sharks[i]
        board[r][c] = [num, d, s]
    print("debug")
    for i in board:
        print(i)
# print("sharks",sharks)
for idx in range(C):
    # debug()
    # 현재 idx 에 있음.
    # r 0 부터 올려가면서 낚기

    for i in range(R):
        temp = board.get((i, idx), -1)
        if temp != -1:
            for a in temp:
                # 상어 잡기
                is_alive[a] = False
                answer += sharks[a][5]
            break

    # 살아 있는 상어들 움직이기

    new_board = {}

    for i in range(M):
        if not is_alive[i]:
            continue

        num, r, c, s, d, z = sharks[i]
        nr, nc, nd = move(r, c, d, s)
        temp = new_board.get((nr, nc), -1)
        sharks[i] = [num, nr, nc, s, nd, z]
        if temp == -1:
            new_board[(nr, nc)] = []
            new_board[(nr, nc)].append(num)
        else:
            new_board[(nr, nc)].append(num)

    # 상어들끼리 잡아먹기.

    for key, value in new_board.items():
        if len(value) >= 2:
            sizes = []
            for num in value:
                sizes.append(sharks[num][5])
            max_val = max(sizes)
            surviver = sizes.index(max_val)
            # surviver 뻬고 다 죽음 처리.
            # 배열 교체도 하기.
            
            for i in range(len(value)):
                if i == surviver:
                    continue
                is_alive[value[i]] = False
            surviver_val = value[surviver]
            new_board[key] = [surviver_val]
    board = new_board
    # print("sharks", sharks)
    # print("alive", is_alive)
print(answer)
