"""
CT 2596  최소 차 분할
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-minimum-diff-partition/description

풀이일 : 2026-10-14   결과: 못품
한도   : time Python3 1초 · C++17 0.5초 / memory 192 MB / time_sec 1
난이도 : Medium  |  정답률 62.4%
제약   : - $2 \le N \le 100$
제약   : - $1 \le A_i \le 1\,000$ $(1 \le i \le N)$
제약   : - 주어진 $N$개의 정수는 각각 그룹 $A$ 또는 $B$ 중 정확히 한 곳에만 속해야 합니다.
제약   : - 각 그룹은 최소 $1$개 이상의 정수를 포함해야 합니다.

[문제]
$N$개의 정수가 주어졌을 때 이를 정확히 $2$개의 그룹 $A$, $B$로 나누어 $A$에 들어있는 수들의 합과 $B$에 들어있는 수들의 합 간의 차이가 최소가 되도록 하는 프로그램을 작성해보세요. 단, 주어진 $N$개의 정수는 각각 $A$ 또는 $B$ 중 정확히 한 곳에만 속해야 하며, 각 그룹은 최소 $1$개 이상의 정수를 포함하고 있어야 함에 유의합니다.

[예제 1]
입력:
4
2 2 1 5

출력:
0


[예제 2]
입력:
5
4 7 8 9 5

출력:
1

"""

N = int(input())
arr = list(map(int, input().split()))

# Please write your code here.

total = sum(arr)

dp = [False] * (total + 1)
dp[0] = True

for num in arr:
    for s in range(total, num - 1, -1):
        if dp[s - num]:
            dp[s] = True

answer = float('inf')

for s in range(1, total):
    if dp[s]:
        answer = min(answer, abs(2 * s - total))

print(answer)
