"""
CT 49  동전 거슬러주기
https://www.codetree.ai/ko/trails/complete/curated-cards/intro-coin-change/description

풀이일 : 2026-10-12   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Easy  |  정답률 49.6%
제약   : - $1 \le N \le 100$
제약   : - $1 \le M \le 10\,000$
제약   : - $1 \le c_i \le 10\,000$ $(1 \le i \le N)$
제약   : - 각 동전의 금액은 서로 다릅니다.

[채점] accepted  2/2  (0.587s)

[문제]
$N$개의 동전의 종류가 주어졌을 때, 금액 $M$을 거슬러주기 위해 필요한 최소 동전의 수를 구해주는 프로그램을 작성해보세요. 단, 같은 종류의 동전을 여러 번 사용하여 거슬러 줄 수 있습니다.

예를 들어 $N = 3$, $M = 8$, 동전의 종류는 $1$, $4$, $5$ 일 때

$8 = 1 + 1 + 1 + 5$ 이렇게 거슬러주면 총 $4$개의 동전이 필요하지만

$8 = 4 + 4$ 이렇게 거슬러 주면 총 $2$개의 동전으로 돈을 거슬러 줄 수 있습니다.

[예제 1]
입력:
3 8
1 4 5

출력:
2


[예제 2]
입력:
3 9
1 3 8

출력:
2

"""

N, M = map(int, input().split())
coins = list(map(int, input().split()))

# Please write your code here.
INF = 10 ** 18
dp = [INF] * (M + 1)
dp[0] = 0
for i in range(1, M + 1):

    for coin in coins:

        if i - coin >= 0:
            dp[i] = min(dp[i], dp[i - coin] + 1)

if dp[M] == INF:
    print(-1)
else:
    print(dp[M])
