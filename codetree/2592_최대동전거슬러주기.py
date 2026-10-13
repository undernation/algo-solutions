"""
CT 2592  최대 동전 거슬러주기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-max-coin-change/description

풀이일 : 2026-10-13   결과: 틀림
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Easy  |  정답률 50.7%
제약   : - $1 \le N \le 100$
제약   : - $1 \le M \le 10\,000$
제약   : - $1 \le \texttt{동전의 금액} \le 10\,000$
제약   : - 주어지는 동전의 금액은 모두 서로 다릅니다.

[문제]
$N$개의 동전의 종류가 주어졌을 때, 금액이 정확히 $M$이 되도록 거슬러주는 방법 중 가능한 최대 동전의 수를 구해주는 프로그램을 작성해보세요. 단, 같은 종류의 동전을 여러 번 사용하여 거슬러 줄 수 있습니다.

예를 들어 $N = 3$, $M = 10$, 동전의 종류는 $3$, $4$, $5$일 때

$10 = 5 + 5$ 이렇게 거슬러주면 총 $2$개의 동전이 사용되지만

$10 = 3 + 3 + 4$ 이렇게 거슬러 주면 총 $3$개의 동전으로 돈을 거슬러 줄 수 있습니다.

[예제 1]
입력:
3 10
3 4 5

출력:
3


[예제 2]
입력:
4 19
4 6 7 9

출력:
4

"""

N, M = map(int, input().split())
coins = list(map(int, input().split()))

# Please write your code here.

dp = [-1] * (M + 1)

dp[0] = 0

for i in range(1, M + 1):

    for coin in coins:
        cur = i - coin
        if cur >= 0:
            if dp[cur] == -1:
                continue

            dp[i] = max(dp[i], dp[cur] + 1)


print(dp[M])
