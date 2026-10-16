"""
CT 42  올바른 등식 만들기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-right-equality/description

풀이일 : 2026-10-16   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 43.4%
제약   : - $1 \le N \le 100$
제약   : - $-20 \le M \le 20$
제약   : - $0 \le A_i \le 9$ $(1 \le i \le N)$
제약   : - 답은 $2^{63} - 1$을 넘지 않음이 보장됩니다.

[채점] accepted  2/2  (0.691s)

[문제]
$N$개의 $0$이상 $9$이하의 정수들이 주어졌을 때, 가장 처음 주어진 정수부터 $N$번째 정수까지 순서대로 각각의 정수를 더하거나 빼서 그 합이 $M$이 되도록 하는 서로 다른 가짓수를 구하는 프로그램을 작성해보세요. 단, 더하거나 빼는 과정속에서 그 결과가 $-20$보다 작아지거나 $20$보다 커지면 안됩니다.

예를 들어 $N = 5$, $M = 9$, 입력으로 주어진 정수가 $1$, $9$, $3$, $8$, $6$이었을 때

$1 + 9 + 3 + 8 - 6$ 이렇게 계산을 하면 계산을 하는 도중 $+8$을 했을 때 값이 $21$이 되어 $20$보다 커지게 되므로 잘못된 식입니다.

$-1 - 9 - 3 - 8 - 6$ 이렇게 계산을 하면 계산 도중 $-8$을 했을 때 값이 $-21$이 되어 $-20$보다 작아지게 되므로 잘못된 식입니다.

$1 + 9 - 3 + 8 - 6$ 이렇게 계산을 하면 더하거나 빼는 과정 속에서 값이 항상 $-20$이상 $20$이하에 있으며 최종 결과가 $M$인 $9$가 되므로 올바른 식입니다.

[예제 1]
입력:
3 1
1 1 1

출력:
3


[예제 2]
입력:
5 9
1 9 3 8 6

출력:
3

"""

import sys

input = sys.stdin.readline

N, M = map(int, input().split())

num_list = list(map(int, input().split()))

dp = [[0] * 41 for _ in range(N + 1)]

dp[0][20] = 1

for idx in range(1, N + 1):
    cur_num = num_list[idx - 1]

    for i in range(41):
        cur = i - cur_num

        # 뺀 경우
        if 0 <= cur <= 40:
            if dp[idx - 1][i] == -1:
                continue

            dp[idx][cur] += dp[idx - 1][i]

        cur = i + cur_num

        if 0 <= cur <= 40:
            if dp[idx - 1][i] == -1:
                continue

            dp[idx][cur] += dp[idx - 1][i]

print(dp[N][M + 20])

# for i in dp:
#     print(i)
