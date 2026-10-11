"""
CT 2488  정수 사각형 최댓값의 최소
https://www.codetree.ai/ko/trails/complete/curated-cards/test-minimax-path-in-square/description

풀이일 : 2026-10-11   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Easy  |  정답률 64.0%
제약   : - $1 \le N \le 100$
제약   : - $1 \le \texttt{행렬에 주어지는 수} \le 1\,000\,000$

[채점] accepted  2/2  (0.527s)

[문제]
$N \times N$ 행렬이 주어졌을 때, $(1, 1)$에서 시작하여 오른쪽 혹은 밑으로만 이동하여 $(N, N)$으로 간다고 했을 때 거쳐간 위치에 적혀있는 수들 중 최댓값을 최소로 하는 프로그램을 작성해보세요.

[예제 1]
입력:
3
1 4 3
3 4 5
5 4 2

출력:
4


[예제 2]
입력:
3
5 6 7
6 5 4
5 7 1

출력:
6

"""

N = int(input())
grid = [list(map(int, input().split())) for _ in range(N)]

# Please write your code here.

dp = [[0] * N for _ in range(N)]

dp[0][0] = grid[0][0]

for i in range(1, N):
    dp[i][0] = max(dp[i - 1][0], grid[i][0])

for j in range(1, N):
    dp[0][j] = max(dp[0][j - 1], grid[0][j])

for i in range(1, N):
    for j in range(1, N):
        num1 = max(dp[i - 1][j], grid[i][j])
        num2 = max(dp[i][j - 1], grid[i][j])

        dp[i][j] = min(num1, num2)

print(dp[N - 1][N - 1])
