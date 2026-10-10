"""
CT 2504  정수 사각형 최장 증가 수열
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-lis-on-the-integer-grid/description

풀이일 : 2026-10-10   결과: 틀림
한도   : time Python3 8초 · C++17 1초 / memory 512 MB / time_sec 8
난이도 : Medium  |  정답률 49.6%
제약   : - $1 \le N \le 500$
제약   : - $1 \le \texttt{주어지는 정수} \le 10^9$

[문제]
$N \times N$ 크기의 격자 정보가 주어졌을 때, 시작점을 적절하게 잡아 상하좌우로 인접한 칸으로 계속 칸에 적혀있는 정수값이 커지도록 이동한다고 했을 때 밟고 지나갈 수 있는 최대 칸의 수를 구하는 프로그램을 작성해보세요.

[예제 1]
입력:
3
2 2 1
3 1 2
4 1 2

출력:
3


[예제 2]
입력:
3
5 1 3
6 1 4
7 2 3

출력:
4

"""

import sys
sys.setrecursionlimit(10**6)

N = int(input())
grid = [list(map(int, input().split())) for _ in range(N)]

memo = [[0] * N for _ in range(N)]


def dfs(y, x):

    if memo[y][x] != 0:
        return memo[y][x]

    memo[y][x] = 1

    for dy, dx in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
        ny = y + dy
        nx = x + dx

        if not (0 <= ny < N and 0 <= nx < N):
            continue

        if grid[ny][nx] >= grid[y][x]:
            continue

        memo[y][x] = max(
            memo[y][x],
            dfs(ny, nx) + 1
        )

    return memo[y][x]


answer = 0

for i in range(N):
    for j in range(N):
        answer = max(answer, dfs(i, j))

print(answer)
