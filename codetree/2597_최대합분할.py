"""
CT 2597  최대 합 분할
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-maximum-sum-partition/description

풀이일 : 2026-10-14   결과: 못품
한도   : time Python3 3초 · C++17 1초 / memory 512 MB / time_sec 3
난이도 : Hard  |  정답률 52.4%
제약   : - $1 \le N \le 100$
제약   : - $1 \le \texttt{주어지는 수} \le 1\,000$

[문제]
$N$개의 수가 주어졌을 때 이를 정확히 $3$개의 그룹 $A$, $B$, $C$로 나누어 $A$에 들어있는 수들의 합과 $B$에 들어있는 수들의 합이 같아지게 만들되, 그 합이 최대가 되도록 하는 프로그램을 작성해보세요. 단, 주어진 $N$개의 수는 각각 $A$, $B$ 또는 $C$ 중 정확히 한 곳에만 속해야 하며, 아무런 수도 포함하고 있지 않은 그룹 내 수들의 합은 $0$으로 정의됨에 유의합니다.

[예제 1]
입력:
4
2 2 1 5

출력:
5


[예제 2]
입력:
5
4 7 8 9 5

출력:
13


[예제 3]
입력:
2
4 5

출력:
0

"""

N = int(input())
arr = list(map(int, input().split()))

# Please write your code here.

# num 순회하면서 a 에 들어있는 수를 뽑는 방식으로 한다.
# 그다음은 b 랑 c 로 나누는걸 구현 못하겠다.


dp = {0: 0}

for num in arr:
    next_dp = dp.copy()

    for diff, a_sum in dp.items():
        new_diff = diff + num
        new_sum = a_sum + num

        next_dp[new_diff] = max(
            next_dp.get(new_diff, float('-inf')),
            new_sum
        )

        new_diff = diff - num

        next_dp[new_diff] = max(
            next_dp.get(new_diff, float('-inf')),
            a_sum
        )

        dp = next_dp

print(dp[0])
