"""
CT 2589  겹치지 않게 선분 고르기 2
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-select-segments-without-overlap-2/description

풀이일 : 2026-10-11   결과: 못품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 57.3%
제약   : - $1 \le N \le 1\,000$
제약   : - $1 \le x_1 \lt x_2 \le 1\,000$

[문제]
수직선상에 $N$개의 선분이 주어졌을 때, 겹치지 않게 가장 많은 수의 선분을 고르는 프로그램을 작성해보세요. 단, 끝점을 공유하는 것 역시 겹친 것으로 생각합니다.

[예제 1]
입력:
3
1 2
3 4
5 6

출력:
3


[예제 2]
입력:
3
1 2
1 4
3 4

출력:
2

"""

N = int(input())
lines = []
for _ in range(N):
    a, b = map(int, input().split())
    lines.append((a, b))

# Please write your code here.

lines.sort()

dp = [1] * N

for i in range(N):
    cur_line = lines[i]
    c1, c2 = cur_line
    for j in range(i):
        prev_line = lines[j]
        p1, p2 = prev_line

        if c1 > p2:
            dp[i] = max(dp[i], dp[j] + 1)


print(max(dp))
