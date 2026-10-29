"""
BOJ 1149  RGB거리
https://cosal.aviss.kr/problems/detail/1149

풀이일 : 2026-10-29   결과: 품
한도   : time 0.5 초 / memory 128 MB

[채점] accepted  19/19  (6.001s)

[문제]
RGB거리에는 집이 N개 있다. 거리는 선분으로 나타낼 수 있고, 1번 집부터 N번 집이 순서대로 있다.

집은 빨강, 초록, 파랑 중 하나의 색으로 칠해야 한다. 각각의 집을 빨강, 초록, 파랑으로 칠하는 비용이 주어졌을 때, 아래 규칙을 만족하면서 모든 집을 칠하는 비용의 최솟값을 구해보자.

1번 집의 색은 2번 집의 색과 같지 않아야 한다. N번 집의 색은 N-1번 집의 색과 같지 않아야 한다. i(2 ≤ i ≤ N-1)번 집의 색은 i-1번, i+1번 집의 색과 같지 않아야 한다.

[예제 1]
입력:
3
26 40 83
49 60 57
13 89 99
출력:
96

[예제 2]
입력:
3
1 100 100
100 1 100
100 100 1
출력:
3

[예제 3]
입력:
3
1 100 100
100 100 100
1 100 100
출력:
102

[예제 4]
입력:
6
30 19 5
64 77 64
15 19 97
4 71 57
90 86 84
93 32 91
출력:
208

[예제 5]
입력:
8
71 39 44
32 83 55
51 37 63
89 29 100
83 58 11
65 13 15
47 25 29
60 66 19
출력:
253
"""


N = int(input())

board = [list(map(int, input().split())) for _ in range(N)]

# print(board)
INF = 10 ** 18
dp = [[INF] * 3 for _ in range(N)]

for i in range(3):
    dp[0][i] = board[0][i]

for idx in range(1, N):

    for i in range(3):
        for j in range(3):
            if i == j:
                continue

            dp[idx][j] = min(dp[idx][j], dp[idx- 1][i] + board[idx][j])

print(min(dp[N - 1]))
