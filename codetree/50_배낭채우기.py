"""
CT 50  배낭 채우기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-knapsack/description

풀이일 : 2026-10-13   결과: 틀림
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 62.9%
제약   : - $1 \le N \le 100$
제약   : - $1 \le M \le 10\,000$
제약   : - $1 \le w_i \le 10\,000$ $(1 \le i \le N)$
제약   : - $1 \le v_i \le 10\,000$ $(1 \le i \le N)$

[문제]
$N$개의 보석의 정보가 주어졌을 때, 각 보석을 최대 한 번씩만 선택하여 무게의 합이 $M$을 넘지 않도록 하면서 가치의 합은 최대가 되도록 하는 프로그램을 작성해보세요.

예를 들어 $N = 4$, $M = 20$, 보석의 종류가 다음과 같이 주어졌다고 생각해봅시다.

![](https://contents.codetree.ai/problems/50/images/problems-f4e4aa5e-b104-424a-9cc2-10c38f390129.png)

$1$, $2$번 보석을 고르게 되면 고른 보석 무게의 총 합이 $25$가 되어 $M$을 넘게 되므로 불가능합니다.

$1$, $4$번 보석을 고르게 되면 무게가 $M$을 넘지 않으면서 총 $39$만큼의 가치를 얻게 됩니다.

$2$, $3$번 보석을 고르게 되면 무게가 $M$을 넘지 않으면서 총 $40$만큼의 가치를 얻게 됩니다.

[예제 1]
입력:
3 7
5 8
3 6
4 4

출력:
10


[예제 2]
입력:
4 20
10 20
15 25
5 15
9 19

출력:
40

"""

N, M = map(int, input().split())
w, v = zip(*[tuple(map(int, input().split())) for _ in range(N)])
w, v = list(w), list(v)

# Please write your code here.

dp = [-1] * (M + 1)
dp[0] = 0

for jewel in range(N):

    for m in range(M, -1, -1):

        cur = m + w[jewel]

        if cur <= M:
            if dp[m] == -1:
                continue

            dp[cur] = max(dp[cur], dp[m] + v[jewel])

print(max(dp))
