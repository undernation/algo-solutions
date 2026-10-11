"""
CT 2585  최대 감소 부분 수열
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-longest-decreasing-subsequence/description

풀이일 : 2026-10-11   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Easy  |  정답률 76.8%
제약   : - $1 \le N \le 1\,000$
제약   : - $1 \le \texttt{수열의 원소} \le 10\,000$

[채점] accepted  2/2  (0.52s)

[문제]
$N$개의 정수가 주어졌을 때, 가장 긴 감소 부분 수열의 길이를 구하는 프로그램을 작성해보세요

부분 수열이란 수열의 원소들 중 임의로 몇 개를 골라 순서대로 나열한 수열을 의미하고, 이때 순서대로 나열했을 때 원소들이 계속 감소한다면 이 수열을 감소 부분 수열이라고 합니다.

예를 들어, $N = 6$, 주어진 수열이 [$9$, $4$, $6$, $7$, $1$, $7$] 이라 했을 때

[$9$, $7$, $4$]은 순서대로 나열해 만들 수 없으므로 부분 수열이라 할 수 없습니다.

[$9$, $4$, $7$]은 부분 수열이지만 계속 감소하는 수열이 아니므로 감소 부분 수열은 아닙니다.

[$9$, $7$, $7$]은 부분 수열이지만 역시 마찬가지로 계속 감소하는 수열이 아니므로 감소 부분 수열은 아닙니다.

[$9$, $6$, $1$]는 계속 감소하는 부분 수열이므로 감소 부분 수열입니다.

[예제 1]
입력:
4
4 2 3 1

출력:
3


[예제 2]
입력:
6
9 4 6 7 1 7

출력:
3

"""

N = int(input())
num_list = list(map(int, input().split()))

# Please write your code here.

dp = [1] * N

for i in range(1, N):

    for j in range(i):
        num1 = num_list[i]
        num2 = num_list[j]
        if num1 < num2:

            dp[i] = max(dp[i], dp[j] + 1)

print(max(dp))
