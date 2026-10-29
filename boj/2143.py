"""
BOJ 2143  두 배열의 합
https://cosal.aviss.kr/problems/detail/2143

풀이일 : 2026-10-29   결과: 못품
한도   : time 2 초 / memory 64 MB

[채점] accepted  15/15  (5.396s)

[문제]
한 배열 A[1], A[2], …, A[n]에 대해서, 부 배열은 A[i], A[i+1], …, A[j-1], A[j] (단, 1 ≤ i ≤ j ≤ n)을 말한다. 이러한 부 배열의 합은 A[i]+…+A[j]를 의미한다. 각 원소가 정수인 두 배열 A[1], …, A[n]과 B[1], …, B[m]이 주어졌을 때, A의 부 배열의 합에 B의 부 배열의 합을 더해서 T가 되는 모든 부 배열 쌍의 개수를 구하는 프로그램을 작성하시오.

예를 들어 A = {1, 3, 1, 2}, B = {1, 3, 2}, T=5인 경우, 부 배열 쌍의 개수는 다음의 7가지 경우가 있다.

T(=5) = A[1] + B[1] + B[2]
      = A[1] + A[2] + B[1]
      = A[2] + B[3]
      = A[2] + A[3] + B[1]
      = A[3] + B[1] + B[2]
      = A[3] + A[4] + B[3]
      = A[4] + B[2]

[예제 1]
입력:
5
4
1 3 1 2
3
1 3 2
출력:
7
"""

from collections import defaultdict

T = int(input())
N = int(input())
A = list(map(int, input().split()))

M = int(input())
B = list(map(int, input().split()))

b_dict = defaultdict(int)


for i in range(M):
    total = 0
    for j in range(i, M):
        total += B[j]

        b_dict[total] += 1


answer = 0

for i in range(N):
    total = 0
    for j in range(i, N):
        total += A[j]

        find_val = T - total

        answer += b_dict[find_val]

print(answer)
