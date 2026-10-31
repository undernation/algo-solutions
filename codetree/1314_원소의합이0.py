"""
CT 1314  원소의 합이 0
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-the-sum-of-the-elements-is-0/description

풀이일 : 2026-10-31   결과: 품
한도   : time Python3 1초 · C++17 1초 / memory 120 MB / time_sec 1
난이도 : Hard  |  정답률 63.3%
제약   : - $1 \leq N \leq 5\,000$
제약   : - $-1\,000\,000\,000 \leq \texttt{원소의 크기} \leq  1\,000\,000\,000$

[채점] accepted  1/1  (0.348s)

[문제]
네 개의 수열 $A$, $B$, $C$, $D$에서 각각 원소를 하나씩 골라 더하였을 때 합이 $0$이되는 경우의 수를 구하는 프로그램을 작성해보세요.

[예제 1]
입력:
6
-45 -41 -36 -36 26 -32
22 -27 53 30 -38 -54
42 56 -37 -75 -10 -6
-16 30 77 -46 62 45

출력:
5

"""

from collections import defaultdict

N = int(input())
A = list(map(int, input().split()))
B = list(map(int, input().split()))
C = list(map(int, input().split()))
D = list(map(int, input().split()))

# Please write your code here.


temp = defaultdict(int)

for a in A:
    for b in B:
        diff = 0 - a - b
        temp[diff] += 1

answer = 0

for c in C:
    for d in D:
        answer += temp[c + d]

print(answer)
