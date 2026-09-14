"""
SWEA 5251  [S/W 문제해결 구현] 7일차 - 최소 이동 거리 D4
https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AWUS6BAaI4oDFAVT

풀이일 : 2026-09-14   결과: 품
한도   : time 10개 테스트케이스를 합쳐서 Python의 경우 2초 / memory 힙, 정적 메모리 합쳐서 256MB 이내, 스택 메모리 1MB 이내 / time_sec 2
난이도 : Master  |  정답률 61.26%

[채점] accepted  1/1  (0.288s)

[문제]
※ SW Expert 아카데미의 문제를 무단 복제하는 것을 금지합니다.

A도시에는 E개의 일방통행 도로 구간이 있으며, 각 구간이 만나는 연결지점에는 0부터 N번까지의 번호가 붙어있다.

구간의 시작과 끝의 연결 지점 번호, 구간의 길이가 주어질 때, 0번 지점에서 N번 지점까지 이동하는데 걸리는 최소한의 거리가 얼마인지 출력하는 프로그램을 만드시오.

모든 연결 지점을 거쳐가야 하는 것은 아니다.

[[IMG:1]]

그림은 입력인 N=2, E=3, 시작과 끝 지점, 구간 거리가 아래와 같은 경우의 예이다.

0 1 1

0 2 6

1 2 1

[예제 1]
입력:
3
2 3
0 1 1
0 2 6
1 2 1
4 7
0 1 9
0 2 3
0 3 7
1 4 2
2 3 8
2 4 1
3 4 8
4 6
0 1 10
0 2 7
1 4 2
2 3 10
2 4 3
3 4 10
출력:
#1 2
#2 4
#3 10
"""

import heapq


T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    N, E = map(int, input().split())
    INF = 10 ** 18
    graph = [set() for _ in range(N + 1)]
    cost = dict()
    for e in range(E):
        start, end, w = map(int, input().split())
        graph[start].add(end)
        cost[(start, end)] = w

    dist = [INF for _ in range(N + 1)]

    hq = []
    heapq.heappush(hq, (0, 0))

    while hq:
        cur_cost, cur_node = heapq.heappop(hq)
        if dist[cur_node] < cur_cost:
            continue
        for nxt in graph[cur_node]:
            nxt_cost = cost[(cur_node, nxt)]
            new_cost = nxt_cost + cur_cost
            if dist[nxt] > new_cost:
                dist[nxt] = new_cost
                heapq.heappush(hq, (new_cost, nxt))

    answer = dist[N]

    print(f"#{test_case} {answer}")
