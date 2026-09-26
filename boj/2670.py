"""
BOJ 2670  연속부분최대곱
https://cosal.aviss.kr/problems/detail/2670

풀이일 : 2026-09-26   결과: 품
한도   : time 1 초 / memory 128 MB

[채점] accepted  27/27  (7.425s)

[문제]
N개의 실수가 있을 때, 한 개 이상의 연속된 수들의 곱이 최대가 되는 부분을 찾아, 그 곱을 출력하는 프로그램을 작성하시오. 예를 들어 아래와 같이 8개의 양의 실수가 주어진다면,

[[IMG:1]]

색칠된 부분의 곱이 최대가 되며, 그 값은 1.638이다.

[예제 1]
입력:
8
1.1
0.7
1.3
0.9
1.4
0.8
0.7
1.4
출력:
1.638
"""



N = int(input())
num_list = []

for _ in range(N):
    num_list.append(float(input()))

dp = [0.0] * N
dp[0] = num_list[0]
for idx in range(1, N):
    dp[idx] = max(num_list[idx], dp[idx - 1] * num_list[idx])

answer = max(dp)

print(f"{answer:.3f}")
