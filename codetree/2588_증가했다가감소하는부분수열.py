"""
CT 2588  증가했다가 감소하는 부분 수열
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-increasing-and-descreasing-subsequence/description

풀이일 : 2026-10-12   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Hard  |  정답률 63.1%
제약   : - $1 \le N \le 1\,000$
제약   : - $1 \le \texttt{수열의 원소} \le 10\,000$

[채점] accepted  2/2  (0.509s)

[문제]
$N$개의 정수가 주어졌을 때, 가장 긴 증가-감소 부분 수열의 길이를 구하는 프로그램을 작성해보세요.

부분 수열이란 수열의 원소들 중 임의로 몇 개를 골라 순서대로 나열한 수열을 의미합니다. 증가-감소 부분수열은 순서대로 나열했을 때 원소들이 엄격하게 증가하다가 특정 순간부터는 엄격하게 감소하기 시작하는 수열을 증가-감소 부분 수열이라고 합니다. 단, 처음부터 끝까지 엄격하게 증가만 하거나 엄격하게 감소만 하는 부분수열 역시 증가-감소 부분수열임에 유의합니다.

예를 들어, $N = 7$, 주어진 수열이 [$1$, $4$, $2$, $5$, $6$, $2$, $1$] 이라 했을 때

[$2$, $4$, $5$, $2$]는 순서대로 나열해 만들 수 없으므로 부분 수열이라 할 수 없습니다.

[$1$, $4$, $2$, $5$]는 부분 수열이지만 증가, 감소 후 다시 값이 증가하였기에 증가-감소 부분 수열이 아닙니다.

[$1$, $4$, $5$]는 부분 수열이고 엄격하게 증가만 일어났기에 증가-감소 부분 수열입니다.

[$4$, $2$]는 부분 수열이고 엄격하게 감소만 일어났기에 증가-감소 부분 수열입니다.

[$1$, $2$, $5$, $6$, $2$, $1$]은 엄격하게 증가하다가 $6$에서부터 엄격하게 감소만 하기에 증가-감소 부분 수열입니다.

[예제 1]
입력:
7
1 4 2 5 6 2 1

출력:
6


[예제 2]
입력:
6
6 5 4 3 4 5

출력:
4

"""

N = int(input())
sequence = list(map(int, input().split()))

# Please write your code here.

dp1 = [1] * N
dp2 = [0] * N

for i in range(N):
    cur_num = sequence[i]

    # 증가한 부분 처리
    for j in range(i):
        prev_num = sequence[j]

        if prev_num < cur_num:
            dp1[i] = max(dp1[i], dp1[j] + 1)

for i in range(N - 1, -1, -1):
    cur_num = sequence[i]
    for k in range(N - 1, i, -1):
        nxt_num = sequence[k]

        if nxt_num < cur_num:
            dp2[i] = max(dp2[i], dp2[k] + 1)

# print(dp1, dp2)
answer = 1

for i in range(N):
    answer = max(answer, dp1[i] + dp2[i])

print(answer)
