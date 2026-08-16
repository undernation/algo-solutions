"""
BOJ 17140  이차원 배열과 연산
https://cosal.aviss.kr/problems/detail/17140

풀이일 : 2026-08-16   결과: 품
한도   : time 0.5 초 / memory 512 MB

[채점] accepted  20/20  (8.111s)

[문제]
크기가 3×3인 배열 A가 있다. 배열의 인덱스는 1부터 시작한다. 1초가 지날때마다 배열에 연산이 적용된다.

R 연산: 배열 A의 모든 행에 대해서 정렬을 수행한다. 행의 개수 ≥ 열의 개수인 경우에 적용된다. C 연산: 배열 A의 모든 열에 대해서 정렬을 수행한다. 행의 개수 < 열의 개수인 경우에 적용된다.

한 행 또는 열에 있는 수를 정렬하려면, 각각의 수가 몇 번 나왔는지 알아야 한다. 그 다음, 수의 등장 횟수가 커지는 순으로, 그러한 것이 여러가지면 수가 커지는 순으로 정렬한다. 그 다음에는 배열 A에 정렬된 결과를 다시 넣어야 한다. 정렬된 결과를 배열에 넣을 때는, 수와 등장 횟수를 모두 넣으며, 순서는 수가 먼저이다.

예를 들어, [3, 1, 1]에는 3이 1번, 1가 2번 등장한다. 따라서, 정렬된 결과는 [3, 1, 1, 2]가 된다. 다시 이 배열에는 3이 1번, 1이 2번, 2가 1번 등장한다. 다시 정렬하면 [2, 1, 3, 1, 1, 2]가 된다.

정렬된 결과를 배열에 다시 넣으면 행 또는 열의 크기가 달라질 수 있다. R 연산이 적용된 경우에는 가장 큰 행을 기준으로 모든 행의 크기가 변하고, C 연산이 적용된 경우에는 가장 큰 열을 기준으로 모든 열의 크기가 변한다. 행 또는 열의 크기가 커진 곳에는 0이 채워진다. 수를 정렬할 때 0은 무시해야 한다. 예를 들어, [3, 2, 0, 0]을 정렬한 결과는 [3, 2]를 정렬한 결과와 같다.

행 또는 열의 크기가 100을 넘어가는 경우에는 처음 100개를 제외한 나머지는 버린다.

배열 A에 들어있는 수와 r, c, k가 주어졌을 때, A[r][c]에 들어있는 값이 k가 되기 위한 최소 시간을 구해보자.

[예제 1]
입력:
1 2 2
1 2 1
2 1 3
3 3 3
출력:
0

[예제 2]
입력:
1 2 1
1 2 1
2 1 3
3 3 3
출력:
1

[예제 3]
입력:
1 2 3
1 2 1
2 1 3
3 3 3
출력:
2

[예제 4]
입력:
1 2 4
1 2 1
2 1 3
3 3 3
출력:
52

[예제 5]
입력:
1 2 5
1 2 1
2 1 3
3 3 3
출력:
-1

[예제 6]
입력:
3 3 3
1 1 1
1 1 1
1 1 1
출력:
2
"""

import sys
input = sys.stdin.readline
from collections import defaultdict

R, C, K = map(int, input().split())
real_board = [[0] * 100 for _ in range(100)]

board = [list(map(int, input().split())) for _ in range(3)]

for i in range(3):
    for j in range(3):
        real_board[i][j] = board[i][j]

row_num = 3
col_num = 3

time = 1
if real_board[R - 1][C - 1] == K:
    print(0)
else:
    while True:
        if row_num >= col_num:
            # 모든 행에 대해 정렬 수행.
            for i in range(row_num):
                ddict = defaultdict(int)
                for j in range(100):
                    ddict[real_board[i][j]] += 1
                new_list = []
                for key, value in ddict.items():
                    if key == 0:
                        continue
                    new_list.append([key, value])
                idx = 0
                final_new_list = [0] * 100
                new_list.sort(key=lambda x: (x[1], x[0]))
                for a, b in new_list:
                    final_new_list[idx] = a
                    idx += 1
                    final_new_list[idx] = b
                    idx += 1
                    if idx >= 100:
                        break
                real_board[i] = final_new_list
                col_num = max(col_num, idx)
        else:
            for j in range(col_num):
                ddict = defaultdict(int)
                for i in range(100):
                    ddict[real_board[i][j]] += 1
                new_list = []
                for key, value in ddict.items():
                    if key == 0:
                        continue
                    new_list.append([key, value])
                idx = 0
                new_list.sort(key=lambda x: (x[1], x[0]))
                final_new_list = [0] * 100
                for a, b in new_list:
                    final_new_list[idx] = a
                    idx += 1
                    final_new_list[idx] = b
                    idx += 1
                    if idx >= 100:
                        break
                for i in range(100):
                    real_board[i][j] = final_new_list[i]
                row_num = max(row_num, idx)

        if real_board[R - 1][C - 1] == K:
            break
        
        if time == 100:
            time = -1
            break
        time += 1

    print(time)
