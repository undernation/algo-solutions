"""
CT 46  M개의 구간을 선택하기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-select-m-sections/description

풀이일 : 2026-10-17   결과: 못품
한도   : time Python3 3초 · C++17 0.5초 / memory 128 MB / time_sec 3
난이도 : Hard  |  정답률 34.4%
제약   : - $1 \le N \le 500$
제약   : - $1 \le M \le \lfloor \frac{N+1}{2} \rfloor$
제약   : - $-1\,000 \le A_i \le 1\,000$ $(1 \le i \le N)$

[문제]
길이 $N$인 정수 수열 $A_1, A_2, \dots, A_N$이 주어졌을 때, 정확히 $M$개의 **비어 있지 않은 연속 부분 구간** $[l, r]$ (즉 $A_l, A_{l+1}, \dots, A_r$, $1 \le l \le r \le N$)을 선택해 각 구간에 속한 원소들의 총 합이 최대가 되도록 하는 프로그램을 작성해보세요. 단, 선택한 두 구간 $[l_1, r_1]$과 $[l_2, r_2]$($l_1 \le l_2$)는 서로 겹치지도 않고 붙어 있지도 않아야 합니다. 즉 $r_1 + 1 < l_2$가 성립해야 하며, 두 구간 사이에 선택되지 않은 원소가 적어도 하나는 존재해야 합니다.

예를 들어 $N = 5$, $M = 2$일 때 주어진 수열이 $A = [1, 5, 2, 4, 3]$이라면

구간을 $[1, 2]$, $[3, 4]$ (값은 $[1, 5]$와 $[2, 4]$)로 잡으면 두 구간이 서로 붙어 있으므로 불가능한 경우입니다.

구간을 $[1, 1]$, $[4, 5]$ (값은 $[1]$과 $[4, 3]$)로 잡으면 문제 조건을 충족하며 총 합이 $8$이 됩니다.

구간을 $[1, 2]$, $[4, 5]$ (값은 $[1, 5]$와 $[4, 3]$)로 잡으면 문제 조건을 충족하며 최대의 합인 $13$을 얻게 됩니다.

[예제 1]
입력:
5 2
1 5 2 4 3

출력:
13


[예제 2]
입력:
6 3
1 20 2 -4 3 2

출력:
19

"""

N, M = map(int, input().split())
numbers = list(map(int, input().split()))

# Please write your code here.
# 구간을 3개로 나누면 될것같은데 맨처음이랑 맨 뒷 구간만 더하고

NEG = -10 ** 18

skip = [[NEG] * (M + 1) for _ in range(N + 1)]
take = [[NEG] * (M + 1) for _ in range(N + 1)]

skip[0][0] = 0

for i in range(1, N + 1):
    num = numbers[i - 1]

    for j in range(M + 1):
        skip[i][j] = max(
            skip[i - 1][j],
            take[i - 1][j]
        )

        if j > 0:
            take[i][j] = max(
                take[i - 1][j],
                skip[i - 1][j - 1]
            ) + num

print(max(skip[N][M], take[N][M]))
