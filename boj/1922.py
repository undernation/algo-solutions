"""
BOJ 1922  네트워크 연결
https://cosal.aviss.kr/problems/detail/1922

풀이일 : 2026-10-27   결과: 품
한도   : time 2 초 / memory 256 MB

[채점] accepted  15/15  (7.435s)

[문제]
도현이는 컴퓨터와 컴퓨터를 모두 연결하는 네트워크를 구축하려 한다. 하지만 아쉽게도 허브가 있지 않아 컴퓨터와 컴퓨터를 직접 연결하여야 한다. 그런데 모두가 자료를 공유하기 위해서는 모든 컴퓨터가 연결이 되어 있어야 한다. (a와 b가 연결이 되어 있다는 말은 a에서 b로의 경로가 존재한다는 것을 의미한다. a에서 b를 연결하는 선이 있고, b와 c를 연결하는 선이 있으면 a와 c는 연결이 되어 있다.)

그런데 이왕이면 컴퓨터를 연결하는 비용을 최소로 하여야 컴퓨터를 연결하는 비용 외에 다른 곳에 돈을 더 쓸 수 있을 것이다. 이제 각 컴퓨터를 연결하는데 필요한 비용이 주어졌을 때 모든 컴퓨터를 연결하는데 필요한 최소비용을 출력하라. 모든 컴퓨터를 연결할 수 없는 경우는 없다.

[예제 1]
입력:
6
9
1 2 5
1 3 4
2 3 2
2 4 7
3 4 6
3 5 11
4 5 3
4 6 8
5 6 8
출력:
23
"""

from collections import defaultdict, deque
import heapq

N = int(input())
M = int(input())

cost_dict = dict()

graph = defaultdict(list)

for m in range(M):
    a, b, c = map(int, input().split())

    graph[a].append((c, b))
    graph[b].append((c, a))

    INF = 10 ** 18
    visited = [False] * (N + 1)
    visited[0] = True

    hq = [(0, 1)]

    answer = 0
    cnt = 0

while hq:
    cost, cur = heapq.heappop(hq)

    if visited[cur]:
        continue

    visited[cur] = True
    answer += cost
    cnt += 1

    for nxt_cost, nxt in graph[cur]:
        if not visited[nxt]:
            heapq.heappush(hq, (nxt_cost, nxt))

    if cnt == N:
        break

print(answer)
