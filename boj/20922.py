"""
BOJ 20922  겹치는 건 싫어
https://cosal.aviss.kr/problems/detail/20922

풀이일 : 2026-10-28   결과: 품
한도   : time 1 초 / memory 1024 MB

[채점] accepted  16/16  (5.698s)

[문제]
홍대병에 걸린 도현이는 겹치는 것을 매우 싫어한다. 특히 수열에서 같은 원소가 여러 개 들어 있는 수열을 싫어한다. 도현이를 위해 같은 원소가 K개 이하로 들어 있는 최장 연속 부분 수열의 길이를 구하려고 한다.

100\,000 이하의 양의 정수로 이루어진 길이가 N인 수열이 주어진다. 이 수열에서 같은 정수를 K개 이하로 포함한 최장 연속 부분 수열의 길이를 구하는 프로그램을 작성해보자.

[예제 1]
입력:
9 2
3 2 5 5 6 4 4 5 7
출력:
7

[예제 2]
입력:
10 1
1 2 3 4 5 6 6 7 8 9
출력:
6
"""

from collections import defaultdict

N, K = map(int, input().split())


num_list = list(map(int, input().split()))

num_dict = defaultdict(int)


start = 0
end = 0

answer = 1
num_dict[num_list[start]] += 1

while end < N - 1:


    end += 1

    num_dict[num_list[end]] += 1

    # 만약
    while num_dict[num_list[end]] > K:
        num_dict[num_list[start]] -= 1
        start += 1

    answer = max(answer, end - start + 1)

print(answer)
