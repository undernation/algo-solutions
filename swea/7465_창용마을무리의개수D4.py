"""
SWEA 7465  창용 마을 무리의 개수 D4
https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AWngfZVa9XwDFAQU

풀이일 : 2026-09-10   결과: 품
한도   : time 10개 테스트케이스를 합쳐서 C의 경우 1초 / C++의 경우 1초 / Java의 경우 2초 / Python의 경우 2초 / memory 힙, 정적 메모리 합쳐서 256MB 이내, 스택 메모리 1MB 이내 / time_sec 2
난이도 : Master  |  정답률 64.80%

[채점] accepted  1/1  (0.308s)

[문제]
[제한 사항]

시간

	

10개 테스트케이스를 합쳐서 C++ 의 경우 1초 / Java 의 경우 2초 / Python 의 경우 2초

메모리

	

힙, 정적 메모리 합쳐서 256MB 이내, 스택 메모리 1MB 이내

 

창용 마을에는 N명의 사람이 살고 있다.

사람은 편의상 1번부터 N번 사람까지 번호가 붙어져 있다고 가정한다.

두 사람은 서로를 알고 있는 관계일 수 있고, 아닐 수 있다.

두 사람이 서로 아는 관계이거나 몇 사람을 거쳐서 알 수 있는 관계라면,

이러한 사람들을 모두 다 묶어서 하나의 무리라고 한다.

창용 마을에 몇 개의 무리가 존재하는지 계산하는 프로그램을 작성하라.

[예제 1]
입력:
2
6 5
1 2
2 5
5 1
3 4
4 6
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
#1 2
#2 1
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

    graph = [set() for _ in range(N + 1)]

    for m in range(M):
        first, second = map(int, input().split())

        graph[first].add(second)
        graph[second].add(first)

    visited = set()
    cnt = 0
    for i in range(1, N + 1):
        if i not in visited:
            bfs(i)
            cnt += 1
    print(f"#{test_case} {cnt}")
