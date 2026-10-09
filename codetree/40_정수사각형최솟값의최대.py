"""
CT 40  정수 사각형 최솟값의 최대
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-maximin-path-in-square/description

풀이일 : 2026-10-09   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Easy  |  정답률 56.5%
제약   : - $1 \le N \le 100$
제약   : - $1 \le A_{ij} \le 1\,000\,000$ $(1 \le i, j \le N)$

[채점] accepted  2/2  (0.507s)

[문제]
$N \times N$ 행렬이 주어졌을 때, $(1,\ 1)$에서 시작하여 인접한 오른쪽 혹은 밑 칸으로 한 칸씩만 이동하여 $(N,\ N)$으로 간다고 했을 때 거쳐간 위치에 적혀있는 정수들 중 최솟값을 최대로 하는 프로그램을 작성해보세요.

[예제 1]
입력:
3
5 2 3
3 2 1
1 2 4

출력:
2


[예제 2]
입력:
3
4 3 2
3 4 5
4 2 8

출력:
3

"""

N = int(input())
grid = [list(map(int, input().split())) for _ in range(N)]

# Please write your code here.

dp = [[0] * N for _ in range(N)]
dp[0][0] = grid[0][0]

for i in range(1, N):
    dp[i][0] = min(dp[i - 1][0], grid[i][0])

for j in range(1, N):
    dp[0][j] = min(dp[0][j - 1], grid[0][j])

for i in range(1, N):
    for j in range(1, N):

        # 위쪽
        prev1 = min(dp[i - 1][j], grid[i][j])
        # 왼쪽
        prev2 = min(dp[i][j - 1], grid[i][j])

        dp[i][j] = max(prev1, prev2)

print(dp[N - 1][N - 1])
