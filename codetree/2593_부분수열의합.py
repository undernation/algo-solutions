"""
CT 2593  부분 수열의 합
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-the-sum-of-the-subsequences/description

풀이일 : 2026-10-13   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Easy  |  정답률 68.9%
제약   : - $1 \le N \le 100$
제약   : - $1 \le M \le 10\,000$
제약   : - $1 \le \texttt{원소 값} \le 10\,000$
제약   : - 주어진 $N$개의 수는 모두 다릅니다.

[채점] accepted  2/2  (0.527s)

[문제]
$N$개의 원소로 이루어진 수열 $A$가 주어졌을 때, 수열 $A$의 부분 수열 내 원소의 합이 $M$이 되는 경우가 있는지를 판단하는 프로그램을 작성해보세요. 
부분 수열이란 수열에서 순서대로 원소를 골랐을 때 나올 수 있는 수열을 뜻합니다. 예를 들어 $A$ = [$5$, $1$, $20$, $3$, $4$] 일 때,  [$1$, $5$, $3$]은 $1$, $5$, $3$이 수열 $A$에 차례대로 존재하지 않으므로 부분 수열이 아니지만, [$5$, $1$, $4$]는 $5$, $1$, $4$가 차례대로 수열 $A$에 존재하므로 부분 수열입니다.

$A$ = [$5$, $2$, $4$, $9$, $1$], $N = 5$, $M = 12$인 경우에 대해 생각해보겠습니다.

이 경우 부분 수열 [$5$, $2$, $4$, $1$]을 고르면 원소들의 합이 $12$가 됩니다.

[예제 1]
입력:
5 12
5 2 4 9 1

출력:
Yes


[예제 2]
입력:
5 25
5 2 4 9 1

출력:
No

"""

N, M = map(int, input().split())
num_list = list(map(int, input().split()))

# Please write your code here.

dp = [-1] * (M + 1)
dp[0] = 1

for num in num_list:

    for i in range(M, -1, -1):

        if num + i <= M:
            if dp[i] == -1:
                continue

            dp[num + i] = max(dp[num + i], dp[i] + 1)

if dp[M] == -1:
    print("No")
else:
    print("Yes")
