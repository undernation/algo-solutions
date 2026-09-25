"""
BOJ 14002  가장 긴 증가하는 부분 수열 4
https://cosal.aviss.kr/problems/detail/14002

풀이일 : 2026-09-25   결과: 못품
한도   : time 1 초 / memory 256 MB

[채점] accepted  17/17  (4.672s)

[문제]
수열 A가 주어졌을 때, 가장 긴 증가하는 부분 수열을 구하는 프로그램을 작성하시오.

예를 들어, 수열 A = {10, 20, 10, 30, 20, 50} 인 경우에 가장 긴 증가하는 부분 수열은 A = {10, 20, 10, 30, 20, 50} 이고, 길이는 4이다.

[예제 1]
입력:
6
10 20 10 30 20 50
출력:
4
10 20 30 50
"""


N = int(input())
num_list = list(map(int, input().split()))
parent = [-1] * N
dp = [1] * N

for i in range(N):

    for j in range(i):
        if num_list[j] < num_list[i]:
            if dp[i] < dp[j] + 1:
                dp[i] = max(dp[j] + 1, dp[i])
                parent[i] = j

# print(dp)
# print(parent)

max_idx = dp.index(max(dp))

ret = []
while max_idx != -1:
    ret.append(num_list[max_idx])
    max_idx = parent[max_idx]
print(max(dp))
ret.reverse()
print(*ret)
