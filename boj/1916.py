"""
BOJ 1916  최소비용 구하기
https://cosal.aviss.kr/problems/detail/1916

풀이일 : 2026-10-28   결과: 틀림
한도   : time 0.5 초 / memory 128 MB

[채점] accepted  15/15  (5.687s)

[문제]
N개의 도시가 있다. 그리고 한 도시에서 출발하여 다른 도시에 도착하는 M개의 버스가 있다. 우리는 A번째 도시에서 B번째 도시까지 가는데 드는 버스 비용을 최소화 시키려고 한다. A번째 도시에서 B번째 도시까지 가는데 드는 최소비용을 출력하여라. 도시의 번호는 1부터 N까지이다.

[예제 1]
입력:
5
8
1 2 2
1 3 3
1 4 1
1 5 10
2 4 2
3 4 1
3 5 1
4 5 3
1 5
출력:
4
"""

import heapq

N = int(input())

M = int(input())

graph = [[] for _ in range(N + 1)]
cost_dict = dict()

for _ in range(M):
    a, b, c = map(int, input().split())
    graph[a].append((b, c))


start, end = map(int, input().split())
INF = 10 ** 18
cost = [INF] * (N + 1)

cost[start] = 0


hq = []

heapq.heappush(hq, (0, start))

while hq:
    cur_cost, cur_node = heapq.heappop(hq)

    if cost[cur_node] < cur_cost:
        continue

    for nxt, nxt_cost in graph[cur_node]:
        new_cost = cur_cost + nxt_cost

        if cost[nxt] > new_cost:
            cost[nxt] = new_cost
            heapq.heappush(hq, (new_cost, nxt))
# print(cost)
print(cost[end])
