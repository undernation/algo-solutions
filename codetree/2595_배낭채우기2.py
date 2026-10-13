"""
CT 2595  배낭 채우기 2
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-knapsack-2/description

풀이일 : 2026-10-13   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 86.9%
제약   : - $1 \le N \le 100$
제약   : - $1 \le M \le 10\,000$
제약   : - $1 \le w_i, v_i \le 10\,000$ ($1 \le i \le N$)

[채점] accepted  2/2  (0.509s)

[문제]
$N$개의 보석의 정보가 주어졌을 때, 보석을 적절하게 골라 무게의 합이 $M$을 넘지 않도록 하면서 가치의 합은 최대가 되도록 하는 프로그램을 작성해보세요. 각 종류의 보석은 $0$개 이상 원하는 만큼 고를 수 있으며, 아무 보석도 고르지 않는 것 역시 가능합니다. 특히 모든 보석의 무게가 $M$보다 커서 아무 보석도 고를 수 없는 경우 총 가치는 $0$이 됩니다.

예를 들어 $N = 4$, $M = 22$, 보석의 종류가 다음과 같이 주어졌다고 생각해봅시다.

![](https://contents.codetree.ai/problems/2595/images/problems-9cdea872-e6d5-4b18-9a27-8ffd394b12c2.png)

| 종류 | 무게 $w$ | 가치 $v$ |
| :---: | :---: | :---: |
| $1$ | $7$ | $20$ |
| $2$ | $9$ | $26$ |
| $3$ | $8$ | $15$ |
| $4$ | $4$ | $9$ |

$1$번 보석을 $3$개 고르게 되면 무게가 $M$을 넘지 않으면서 $60$만큼의 가치를 얻게 됩니다.

$2$번 보석 $2$개와 $4$번 보석 $1$개를 고르게 되면 무게가 $M$을 넘지 않으면서 총 $61$만큼의 가치를 얻게 됩니다.

[예제 1]
입력:
3 7
5 8
3 6
4 4

출력:
12


[예제 2]
입력:
4 22
7 20
9 26
8 15
4 9

출력:
61

"""

N, M = map(int, input().split())
w, v = zip(*[tuple(map(int, input().split())) for _ in range(N)])
w, v = list(w), list(v)

# Please write your code here.

dp = [-1] * (M + 1)
dp[0] = 0

for jewel_idx in range(N):
    cur_value = v[jewel_idx]
    cur_weight = w[jewel_idx]

    for weight in range(M + 1):
        cur = weight + cur_weight

        if cur <= M:
            dp[cur] = max(dp[cur], dp[weight] + cur_value)

# print(dp)
print(max(dp))
