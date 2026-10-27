"""
BOJ 11725  트리의 부모 찾기
https://cosal.aviss.kr/problems/detail/11725

풀이일 : 2026-10-27   결과: 품
한도   : time 1 초 / memory 256 MB

[채점] accepted  16/16  (11.81s)

[문제]
루트 없는 트리가 주어진다. 이때, 트리의 루트를 1이라고 정했을 때, 각 노드의 부모를 구하는 프로그램을 작성하시오.

[예제 1]
입력:
7
1 6
6 3
3 5
4 1
2 4
4 7
출력:
4
6
1
3
1
4

[예제 2]
입력:
12
1 2
1 3
2 4
3 5
3 6
4 7
4 8
5 9
5 10
6 11
6 12
출력:
1
1
2
3
3
4
4
5
5
6
6
"""

from collections import defaultdict, deque
import heapq

N = int(input())

graph = [[] for _ in range(N + 1)]

visited = set()
for m in range(N - 1):
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
            parent[nxt] = cur

            q.append(nxt)
            visited.add(nxt)

parent = [-1] * (N + 1)

bfs(1)

for i in range(2, N + 1):
    print(parent[i])
