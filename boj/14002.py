"""
BOJ 14002  가장 긴 증가하는 부분 수열 4
https://cosal.aviss.kr/problems/detail/14002

풀이일 : 2026-10-27   결과: 품
한도   : time 1 초 / memory 256 MB

[채점] accepted  17/17  (4.293s)

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

last_idx = [-1] * N

dp = [1] * N

for i in range(N):

    for j in range(i):

        # 새로 시작하는 경우
        if num_list[i] > num_list[j]:

            if dp[i] < dp[j] + 1:
                dp[i] = dp[j] + 1
                last_idx[i] = j

max_val = max(dp)
max_idx = dp.index(max_val)
print(max_val)
temp = []
cur_num = max_idx
while cur_num != -1:
    temp.append(num_list[cur_num])
    cur_num = last_idx[cur_num]

# print(temp)
temp.reverse()
print(*temp)
