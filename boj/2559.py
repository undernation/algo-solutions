"""
BOJ 2559  수열
https://cosal.aviss.kr/problems/detail/2559

풀이일 : 2026-08-16   결과: 틀림
한도   : time 1 초 / memory 128 MB

[채점] accepted  18/18  (4.571s)

[문제]
매일 아침 9시에 학교에서 측정한 온도가 어떤 정수의 수열로 주어졌을 때, 연속적인 며칠 동안의 온도의 합이 가장 큰 값을 알아보고자 한다.
예를 들어, 아래와 같이 10일 간의 온도가 주어졌을 때,
3 -2 -4 -9 0 3 7 13 8 -3
모든 연속적인 이틀간의 온도의 합은 아래와 같다.

[[IMG:1]]

이때, 온도의 합이 가장 큰 값은 21이다.
또 다른 예로 위와 같은 온도가 주어졌을 때, 모든 연속적인 5일 간의 온도의 합은 아래와 같으며,

[[IMG:2]]

이때, 온도의 합이 가장 큰 값은 31이다.
매일 측정한 온도가 정수의 수열로 주어졌을 때, 연속적인 며칠 동안의 온도의 합이 가장 큰 값을 계산하는 프로그램을 작성하시오.

[예제 1]
입력:
10 2
3 -2 -4 -9 0 3 7 13 8 -3
출력:
21

[예제 2]
입력:
10 5
3 -2 -4 -9 0 3 7 13 8 -3
출력:
31
"""

import sys
input = sys.stdin.readline

N, K = map(int, input().split())
num_list = list(map(int, input().split()))
INF = 10 ** 18

answer = -INF

cur_val = 0
for i in range(K):
    cur_val += num_list[i]
answer = max(answer, cur_val)

for i in range(K, N):
    # 새거 넣어주고, 빼기
    cur_val += num_list[i]
    cur_val -= num_list[i - K]
    answer = max(answer, cur_val)
print(answer)
