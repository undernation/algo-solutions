"""
BOJ 20125  쿠키의 신체 측정
https://cosal.aviss.kr/problems/detail/20125

풀이일 : 2026-08-22   결과: 품
한도   : time 1 초 / memory 1024 MB

[채점] accepted  17/17  (4.493s)

[문제]
쿠키런은 데브시스터즈에서 제작한 모바일 러닝 액션 게임이다. 마녀의 오븐에서 탈출한 쿠키들과 함께 모험을 떠나는 게임으로, 점프와 슬라이드 2가지 버튼만으로 손쉽게 플레이할 수 있는 것이 특징이다.
연세대학교를 졸업한 김강산 선배님이 데브시스터즈에 취직하면서 주변 사람들에게 쿠키런을 전파시켰다. 하지만 게임을 전파하던 중에 쿠키들에게 신체적으로 이상이 생기는 것을 발견하였다. 팔, 다리 길이가 임의적으로 변한 것이다. 때문에 긴급하게 각 쿠키들의 신체들을 측정하려고 한다.
쿠키들은 신체를 측정하기 위해서 한 변의 길이가 N인 정사각형 판 위에 누워있으며, 어느 신체 부위도 판 밖으로 벗어나지 않는다. 판의 x번째 행, y번째 열에 위치한 곳을 (x, y)로 지칭한다. 판의 맨 왼쪽 위 칸을 (1, 1), 오른쪽 아래 칸을 (N, N)으로 나타낼 수 있다.

[[IMG:1]]

그림과 같이 쿠키의 신체는 머리, 심장, 허리, 그리고 좌우 팔, 다리로 구성되어 있다. 그림에서 빨간 곳으로 칠해진 부분이 심장이다. 머리는 심장 바로 윗 칸에 1칸 크기로 있다. 왼쪽 팔은 심장 바로 왼쪽에 붙어있고 왼쪽으로 뻗어 있으며, 오른쪽 팔은 심장 바로 오른쪽에 붙어있고 오른쪽으로 뻗어있다. 허리는 심장의 바로 아래 쪽에 붙어있고 아래 쪽으로 뻗어 있다. 왼쪽 다리는 허리의 왼쪽 아래에, 오른쪽 다리는 허리의 오른쪽 아래에 바로 붙어있고, 각 다리들은 전부 아래쪽으로 뻗어 있다. 각 신체 부위들은 절대로 끊겨있지 않으며 굽혀진 곳도 없다. 또한, 허리, 팔, 다리의 길이는 1 이상이며, 너비는 무조건 1이다.
쿠키의 신체가 주어졌을 때 심장의 위치와 팔, 다리, 허리의 길이를 구하여라.

[예제 1]
입력:
5
_____
__*__
_***_
__*__
_*_*_
출력:
3 3
1 1 1 1 1

[예제 2]
입력:
10
__________
_____*____
__******__
_____*____
_____*____
_____*____
____*_*___
____*_____
____*_____
____*_____
출력:
3 6
3 2 3 4 1

[예제 3]
입력:
9
____*____
*********
____*____
____*____
____*____
___*_*___
___*_*___
___*_*___
___*_*___
출력:
2 5
4 4 3 4 4
"""

import sys

input = sys.stdin.readline

N = int(input())
board = [list(input().strip()) for _ in range(N)]

head_pos = []
for i in range(N):
    for j in range(N):
        if board[i][j] == "*":
            head_pos = [i, j]
            break
    if head_pos:
        break

heart_pos = [head_pos[0] + 1, head_pos[1]]
answer = [0] * 5
# 왼쪽 팔 길이 산출
# 동 서 남 북
dydx = [[0, 1], [0, -1], [1, 0], [-1, 0]]
def check_length(direction, sy, sx):
    cnt = 1
    cy, cx = sy, sx
    dy, dx = dydx[direction]

    while True:
        ny = cy + dy
        nx = cx + dx
        if not (0 <= ny < N and 0 <= nx < N):
            break
        if board[ny][nx] == "*":
            cnt += 1
            cy = ny
            cx = nx
        else:
            break
    return cnt, cy, cx

left_start = [heart_pos[0], heart_pos[1] - 1]
answer[0], _, _ = check_length(1, left_start[0], left_start[1])
right_start = [heart_pos[0], heart_pos[1] + 1]
answer[1], _, _ = check_length(0, right_start[0], right_start[1])
waist_start = [heart_pos[0] + 1, heart_pos[1]]
answer[2], cy, cx = check_length(2, waist_start[0], waist_start[1])
left_start = [cy + 1, cx - 1]
answer[3], _, _ = check_length(2, left_start[0], left_start[1])
right_start = [cy + 1, cx + 1]
answer[4], _, _ = check_length(2, right_start[0], right_start[1])

heart_pos[0] += 1
heart_pos[1] += 1

print(*heart_pos)
print(*answer)
