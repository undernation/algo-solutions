"""
BOJ 1100  하얀 칸
https://cosal.aviss.kr/problems/detail/1100

풀이일 : 2026-08-15   결과: 품
한도   : time 2 초 / memory 128 MB

[채점] accepted  18/18  (4.39s)

[문제]
체스판은 8×8크기이고, 검정 칸과 하얀 칸이 번갈아가면서 색칠되어 있다. 가장 왼쪽 위칸 (0,0)은 하얀색이다. 체스판의 상태가 주어졌을 때, 하얀 칸 위에 말이 몇 개 있는지 출력하는 프로그램을 작성하시오.

[예제 1]
입력:
.F.F...F
F...F.F.
...F.F.F
F.F...F.
.F...F..
F...F.F.
.F.F.F.F
..FF..F.
출력:
1

[예제 2]
입력:
........
........
........
........
........
........
........
........
출력:
0

[예제 3]
입력:
FFFFFFFF
FFFFFFFF
FFFFFFFF
FFFFFFFF
FFFFFFFF
FFFFFFFF
FFFFFFFF
FFFFFFFF
출력:
32

[예제 4]
입력:
........
..F.....
.....F..
.....F..
........
........
.......F
.F......
출력:
2
"""

import sys
input = sys.stdin.readline

board = [list(input().strip()) for _ in range(8)]
# print(board)
cnt = 0
for i in range(8):
    if i % 2== 0:
        for j in range(8):
            if j % 2 == 0:
                if board[i][j] == "F":
                    cnt += 1
    else:
        for j in range(8):
            if j % 2 == 1:
                if board[i][j] == "F":
                    cnt += 1
print(cnt)
