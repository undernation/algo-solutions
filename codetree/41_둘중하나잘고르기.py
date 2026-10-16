"""
CT 41  둘 중 하나 잘 고르기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-choose-one-of-two-points/description

풀이일 : 2026-10-16   결과: 틀림
한도   : time Python3 1초 · C++17 0.5초 / memory 256 MB / time_sec 1
난이도 : Easy  |  정답률 73.2%
제약   : - $1 \le N \le 100$
제약   : - $1 \le R_i, B_i \le 1\,000$ $(1 \le i \le 2N)$

[문제]
$2 \times N$ 번에 걸쳐 시행을 반복하며 매 시행마다 빨간색, 파란색 총 $2$개의 카드가 주어지고 항상 두 색깔의 카드 중 하나의 카드를 선택해야만 합니다. 각 카드에는 정수가 적혀 있고, 적절하게 카드를 골라 결과적으로 빨간색 카드를 $N$개, 파란색 카드를 $N$개 고른다고 했을 때 뽑힌 정수들의 합을 최대로 하는 프로그램을 작성합니다.

[예제 1]
입력:
2
5 4
5 2
6 4
3 3

출력:
18


[예제 2]
입력:
2
10 9
1 1
7 1
7 1

출력:
24

"""

N = int(input())

cards = [list(map(int, input().split())) for _ in range(2 * N)]

# dp 빨간카드 n 장, 파란카드 n 장을 택 했을 때 적힌수의 합의 최댓값
INT_MIN = -1
dp = [[INT_MIN] * (N + 1) for _ in range(N + 1)]

dp[0][0] = 0
# print(cards)

for idx in range(2 * N):
    # 빨간 카드 선택하는 경우
    cur_num = idx + 1

    for red in range(cur_num + 1):
        blue = cur_num - red

        # 빨강 선택한 경우
        if 1 <= red <= N and blue <= N:
            dp[red][blue] = max(
                dp[red][blue],
                dp[red - 1][blue] + cards[idx][0]
            )

        if 1 <= blue <= N and red <= N:
            dp[red][blue] = max(
                dp[red][blue],
                dp[red][blue - 1] + cards[idx][1]
            )

print(dp[N][N])

# 파란 카드 선택하는 경우
