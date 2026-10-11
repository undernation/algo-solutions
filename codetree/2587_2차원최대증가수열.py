"""
CT 2587  2차원 최대 증가 수열
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-longest-increasing-sequence-2d/description

풀이일 : 2026-10-11   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 44.2%
제약   : - $3 \le N,\ M \le 50$
제약   : - $1 \le \texttt{주어지는 정수} \le 10\,000$

[채점] accepted  2/2  (0.573s)

[문제]
$N \times M$ 크기의 직사각형의 각 칸에 수들이 하나씩 적혀있습니다. 왼쪽 상단 $(1,\ 1)$에서 출발한다고 했을 때 특정 룰을 만족하면서 밟을 수 있는 칸의 최대 수를 구하는 프로그램을 작성해보세요.

아래는 특정 룰에 대한 설명입니다.

1. 이동은 항상 점프를 통해서만 가능합니다. 또, 점프 진행 시 항상 현재 위치에 적혀있는 수보다, 점프한 이후의 칸에 적혀있는 수가 더 커야만 합니다.

2. 점프 진행 시 현재 위치에서 적어도 한 칸 이상 오른쪽에 있는 위치이며 동시에 현재 위치에서 적어도 한 칸 이상 아래쪽에 있는 위치인 곳으로만 점프가 가능합니다.

[예제 1]
입력:
4 4
1 1 1 1
1 1 1 3
1 4 5 2
1 1 2 5

출력:
3


[예제 2]
입력:
5 5
1 2 3 4 5
5 4 3 2 1
1 2 3 4 5
5 4 3 2 1
1 2 3 4 3

출력:
4

"""

N, M = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(N)]

# Please write your code here.

dp = [[-1] * M for _ in range(N)]

dp[0][0] = 1

for i in range(1, N):
    for j in range(1, M):
        cur_num = grid[i][j]

        for y in range(i):
            for x in range(j):
                if dp[y][x] == -1:
                    continue

                prev_num = grid[y][x]

                if cur_num > prev_num:
                    dp[i][j] = max(dp[i][j], dp[y][x] + 1)
answer = 0
for i in range(N):
    for j in range(M):
        answer = max(answer, dp[i][j])

# for i in dp:
#     print(i)

print(answer)
