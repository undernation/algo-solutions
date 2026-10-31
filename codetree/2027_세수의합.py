"""
CT 2027  세 수의 합
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-sum-of-three-num/description

풀이일 : 2026-10-31   결과: 못품
한도   : time Python3 2초 · C++17 1초 / memory 128 MB / time_sec 2
난이도 : Medium  |  정답률 64.9%
제약   : - $1 \le N \le 5\,000$
제약   : - $-5 \times 10^8 \le K \le 5 \times 10^8$
제약   : - $-5 \times 10^8 \le \texttt{정수} \le 5 \times 10^8$

[문제]
$N$개의 정수가 입력으로 주어지고, 이 중 서로 다른 세 개의 위치를 골라 각 위치에 있는 세 수를 더했을 때 $K$가 되는 서로 다른 조합의 개수를 출력하는 코드를 작성해보세요.

[예제 1]
입력:
5 4
1 2 1 4 -1

출력:
3
"""

from collections import defaultdict

N, K = map(int, input().split())
arr = list(map(int, input().split()))

# Please write your code here.
answer = 0


for num1_idx in range(N):
    temp_dict = defaultdict(int)
    for num2_idx in range(num1_idx + 1, N):
        diff = K - arr[num1_idx] - arr[num2_idx]

        if diff in temp_dict:
            answer += temp_dict[diff]


        temp_dict[arr[num2_idx]] += 1

print(answer)
