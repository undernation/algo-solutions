"""
CT 2495  정수 사각형 최소 합
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-minimum-sum-path-in-square/description

풀이일 : 2026-10-09   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Easy  |  정답률 81.6%
제약   : - $1 \le N \le 100$
제약   : - $1 \le \texttt{행렬에 주어지는 정수} \le 1\,000\,000$

[채점] accepted  2/2  (0.503s)

[문제]
$N \times N$ 행렬이 주어졌을 때, $(1,\ N)$에서 시작하여 왼쪽 혹은 밑으로만 이동하여 $(N,\ 1)$로 간다고 했을 때 거쳐간 위치에 적혀있는 정수의 합을 최소로 하는 프로그램을 작성해보세요.

[예제 1]
입력:
3
5 2 1
1 9 1
1 8 9

출력:
10


[예제 2]
입력:
3
2 3 1
5 4 3
1 2 4

출력:
11

"""

N = int(input())
grid = [list(map(int, input().split())) for _ in range(N)]

# Please write your code here.

dp = [[0] * N for _ in range(N)]

dp[0][N - 1] = grid[0][N - 1]

for j in range(N - 2, -1, -1):
    dp[0][j] = dp[0][j + 1] + grid[0][j]

for i in range(1, N):
    dp[i][N - 1] = dp[i - 1][N - 1] + grid[i][N - 1]



for i in range(1, N):
    for j in range(N - 2, -1, -1):
        dp[i][j] = min(dp[i][j + 1] + grid[i][j], dp[i - 1][j] + grid[i][j])

print(dp[N - 1][0])
