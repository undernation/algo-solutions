"""
BOJ 11724  연결 요소의 개수
https://cosal.aviss.kr/problems/detail/11724

풀이일 : 2026-10-27   결과: 품
한도   : time 3 초 / memory 512 MB

[채점] accepted  16/16  (5.602s)

[문제]
방향 없는 그래프가 주어졌을 때, 연결 요소 (Connected Component)의 개수를 구하는 프로그램을 작성하시오.

[예제 1]
입력:
6 5
1 2
2 5
5 1
3 4
4 6
출력:
2

[예제 2]
입력:
6 8
1 2
2 5
5 1
3 4
4 6
5 4
2 4
2 3
출력:
1
"""

from collections import defaultdict, deque
import heapq

N, M = map(int, input().split())

graph = [[] for _ in range(N + 1)]

visited = set()
for m in range(M):
    a, b = map(int, input().split())

    graph[a].append(b)
    graph[b].append(a)


def bfs(start):
    visited.add(start)
    q = deque()
    q.append(start)
    while q:
        cur = q.popleft()

        for nxt in graph[cur]:
            if nxt in visited:
                continue

            q.append(nxt)
            visited.add(nxt)

answer = 0
for i in range(1, N + 1):

    if i in visited:
        continue

    bfs(i)
    answer += 1

print(answer)
