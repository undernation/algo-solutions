"""
CT 56  4가지 연산을 이용하여 1 만들기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-make-one-using-four-operations/description

풀이일 : 2026-10-07   결과: 품
한도   : time Python3 2초 · C++17 0.5초 / memory 256 MB / time_sec 2
난이도 : Hard  |  정답률 48.1%
제약   : - $1 \le N \le 1\,000\,000$

[채점] accepted  2/2  (0.68s)

[문제]
정수 $N$이 주어졌을 때, 다음 $4$가지 연산을 적절히 사용하여 연산의 횟수를 최소화 하여 $1$을 만들어 내려고 합니다.

- 현재 수에서 $1$을 뺍니다.
- 현재 수에 $1$을 더합니다.
- 현재 수가 $2$로 나누어 떨어질 경우, 현재 수를 $2$로 나눕니다.
- 현재 수가 $3$으로 나누어 떨어질 경우, 현재 수를 $3$으로 나눕니다.

예를 들어 수 $11$에서 시작하여 수 $1$을 만들어 내기 위해서는 최소 $4$번의 연산이 필요합니다.

![](https://contents.codetree.ai/problems/56/images/problems-d29709de-c7a4-408c-83a2-3e266a5bf73c.png)

$1$을 만들기 위해 필요한 최소 연산 횟수를 구하는 프로그램을 작성해보세요.

[예제 1]
입력:
11

출력:
4


[예제 2]
입력:
15

출력:
4

"""

from collections import deque

N = int(input())
INF = 10 ** 18
# Please write your code here.
visited = [INF] * (2 * N)


def is_ok(cur_num):
    return 0 <= cur_num < 2 * N


def bfs(start_num):
    q = deque()
    visited[start_num] = 0
    q.append(start_num)

    while q:
        cur_num = q.popleft()
        for nxt_num in [cur_num - 1, cur_num + 1]:
            if is_ok(nxt_num):
                if visited[nxt_num] > visited[cur_num] + 1:
                    visited[nxt_num] = visited[cur_num] + 1
                    q.append(nxt_num)

        if cur_num % 2 == 0:

            nxt_num = cur_num // 2
            if is_ok(nxt_num):
                if visited[nxt_num] > visited[cur_num] + 1:
                    visited[nxt_num] = visited[cur_num] + 1
                    q.append(nxt_num)
        if cur_num % 3 == 0:
            nxt_num = cur_num // 3
            if is_ok(nxt_num):
                if visited[nxt_num] > visited[cur_num] + 1:
                    visited[nxt_num] = visited[cur_num] + 1
                    q.append(nxt_num)


bfs(N)
# print(visited[12], visited[6], visited[2], visited[1])
print(visited[1])
