"""
SWEA 5248  [S/W 문제해결 구현] 6일차 - 그룹 나누기 D3
https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AWUS2OVaIpgDFAVT

풀이일 : 2026-09-10   결과: 품
한도   : time 10개 테스트케이스를 합쳐서 Python의 경우 2초 / memory 힙, 정적 메모리 합쳐서 256MB 이내, 스택 메모리 1MB 이내 / time_sec 2
난이도 : Master  |  정답률 45.07%

[채점] accepted  1/1  (0.318s)

[문제]
수업에서 같은 조에 참여하고 싶은 사람끼리 두 사람의 출석 번호를 종이에 적어 제출하였다.

한 조의 인원에 제한을 두지 않았기 때문에, 한 사람이 여러 장의 종이를 제출하거나 여러 사람이 한 사람을 지목한 경우 모두 같은 조가 된다.

예를 들어 1번-2번, 1번-3번이 같은 조가 되고 싶다고 하면, 1-2-3번이 같은 조가 된다. 번호를 적지도 않고 다른 사람에게 지목되지도 않은 사람은 단독으로 조를 구성하게 된다.

1번부터 N번까지의 출석번호가 있고, M 장의 신청서가 제출되었을 때 전체 몇 개의 조가 만들어지는지 출력하는 프로그램을 만드시오.

[예제 1]
입력:
3
5 2
1 2 3 4
5 3
1 2 2 3 4 5
7 4
2 3 4 5 4 6 7 4
출력:
#1 3
#2 2
#3 3
"""

from collections import deque


def bfs(start):
    visited.add(start)
    q = deque()
    q.append(start)

    while q:
        cur_node = q.popleft()
        for nxt_node in graph[cur_node]:
            if nxt_node in visited:
                continue
            visited.add(nxt_node)
            q.append(nxt_node)


T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    N, M = map(int, input().split())

    num_list = list(map(int, input().split()))
    graph = [set() for _ in range(N + 1)]

    for m in range(M):
        cur_first = m * 2
        cur_nxt = m * 2 + 1
        first_num = num_list[cur_first]
        nxt_num = num_list[cur_nxt]

        graph[first_num].add(nxt_num)
        graph[nxt_num].add(first_num)

    visited = set()
    cnt = 0
    for i in range(1, N + 1):
        if i not in visited:
            bfs(i)
            cnt += 1
    print(f"#{test_case} {cnt}")
