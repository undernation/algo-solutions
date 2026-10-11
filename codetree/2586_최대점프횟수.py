"""
CT 2586  최대 점프 횟수
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-maximum-number-of-jumps/description

풀이일 : 2026-10-11   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Easy  |  정답률 63.7%
제약   : - $1 \le N \le 1\,000$
제약   : - $0 \le A_i \le 1\,000$ ($1 \le i \le N$)

[채점] accepted  2/2  (0.514s)

[문제]
각 위치로부터의 최대 점프 가능 거리를 의미하는 $N$개의 수가 주어졌을 때, 첫 번째 위치로부터 최대 몇 번 점프를 할 수 있는지를 구하는 프로그램을 작성해보세요. 단, 동일한 위치로 점프하는 것은 불가능하고 앞으로 점프하는 것만 가능합니다. 즉, $i$번 위치에서 점프하여 도착하는 위치를 $j$라 하면 $i < j \le N$이며 $j - i \le A_i$를 만족해야 합니다.

예를 들어 $N = 5$이고 주어진 $5$개의 수가 $2$, $3$, $0$, $1$, $4$인 경우에 대해 살펴보겠습니다.

![](https://contents.codetree.ai/problems/2586/images/problems-ccb71713-59a3-4190-87fd-f783da0bd754.png)

이 경우 다음과 같이 이동하면 총 $3$번 점프가 가능하며, 이때가 최대입니다.

![](https://contents.codetree.ai/problems/2586/images/problems-9b5e3f78-4551-4e05-98ee-146ea92b3871.png)

[예제 1]
입력:
5
2 3 0 1 4

출력:
3


[예제 2]
입력:
7
2 0 0 0 1 2 3

출력:
1

"""

N = int(input())
arr = list(map(int, input().split()))

# Please write your code here.
dp = [-1] * N

dp[0] = 0

for i in range(1, N):
    for j in range(i):
        if dp[j] == -1:
            continue

        prev_num = arr[j]

        if j + prev_num < i:
            continue

        dp[i] = max(dp[i], dp[j] + 1)

answer = 0

for i in range(1, N):
    answer = max(answer, dp[i])
print(answer)
