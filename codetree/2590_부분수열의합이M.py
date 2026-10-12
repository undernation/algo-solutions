"""
CT 2590  부분 수열의 합이 M
https://www.codetree.ai/ko/trails/complete/curated-cards/intro-the-sum-of-the-subsequences-is-m/description

풀이일 : 2026-10-12   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 64 MB / time_sec 1
난이도 : Easy  |  정답률 68.1%
제약   : - $1 \le N \le 100$
제약   : - $1 \le M \le 10\,000$
제약   : - $1 \le \texttt{원소 값} \le 10\,000$
제약   : - 주어진 모든 원소는 다름을 가정해도 좋습니다.

[채점] accepted  2/2  (0.517s)

[문제]
$N$개의 원소로 이루어진 수열 $A$가 주어졌을 때, 수열 $A$의 부분 수열 내 원소의 합이 $M$이 되는 경우 중 가능한 최소 수열의 길이를 구하는 프로그램을 작성해보세요. 수열의 길이란, 수열 내 원소의 개수를 의미합니다.

부분 수열이란 수열에서 순서대로 원소를 골랐을 때 나올 수 있는 수열을 뜻합니다. 예를 들어 $A = [5, 1, 20, 3, 4]$일 때, $[1, 5, 3]$은 $1$, $5$, $3$이 수열 $A$에 차례대로 존재하지 않으므로 부분 수열이 아니지만, $[5, 1, 4]$는 $5$, $1$, $4$가 차례대로 수열 $A$에 존재하므로 부분 수열입니다.

$A = [5, 2, 4, 1, 6]$, $N = 5$, $M = 12$인 경우에 대해 생각해보겠습니다.

부분 수열 $[5, 2, 4, 1]$은 원소들의 합이 $12$이면서 길이가 $4$이지만,  
부분 수열 $[2, 4, 6]$은 원소들의 합이 $12$이면서 길이가 $3$이기에 최소 길이가 됩니다.

[예제 1]
입력:
5 12
5 2 4 1 6

출력:
3


[예제 2]
입력:
5 21
8 3 5 4 7

출력:
-1

"""

N, M = map(int, input().split())
num_list = list(map(int, input().split()))

# Please write your code here.

num_list = [0] + num_list
INF = 10 ** 18
dp = [INF] * (M + 1)

dp[0] = 0

for i in range(1, N + 1):

    for j in range(M, -1, -1):
        if j - num_list[i] >= 0:
            # if dp[j - num_list[i]] == INF:
            #     continue
            dp[j] = min(dp[j], dp[j - num_list[i]] + 1)

if dp[M] == INF:
    print(-1)
else:
    print(dp[M])
