"""
CT 2494  계단 오르기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-climbing-stairs/description

풀이일 : 2026-10-08   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 64 MB / time_sec 1
난이도 : Easy  |  정답률 45.0%
제약   : - $2 \le N \le 1\,000$

[채점] accepted  2/2  (0.51s)

[문제]
$N$층 높이의 계단을 오르려고 합니다. 한 번에 정확히 $2$계단 혹은 $3$계단 단위로만 올라갈 수 있다고 했을 때, $N$층 높이의 계단에 올라가기 위한 서로 다른 방법의 수를 구하는 프로그램을 작성해보세요. 단, 항상 $2$계단 혹은 $3$계단 단위로만 올라갈 수 있기에 $N$층까지 정확히 $1$계단이 남은 상황에서는 $N$층으로 올라갈 수 있는 방법이 전혀 없음에 유의합니다.

예로 $N = 5$일 때는 다음과 같이 $2$가지 방법이 가능합니다.

![](https://contents.codetree.ai/problems/2494/images/problems-7bee60e2-949c-4cba-b0ae-3399136249fc.svg)

[예제 1]
입력:
2

출력:
1


[예제 2]
입력:
5

출력:
2

"""

N = int(input())

# Please write your code here.

dp = [0] * (N + 1)

dp[0] = 1

for i in range(1, N + 1):

    prev1 = i - 2

    if prev1 >= 0:
        dp[i] += dp[prev1]

    prev2 = i - 3

    if prev2 >= 0:
        dp[i] += dp[prev2]

print(dp[N] % 10007)
