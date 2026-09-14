"""
SWEA 5263  [S/W 문제해결 최적화] 4일차 - 그래프 최소 비용 D4
https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AWUTcNKKLV0DFAVT

풀이일 : 2026-09-14   결과: 못품
한도   : time 10개 테스트케이스를 합쳐서 Python의 경우 2초 / memory 힙, 정적 메모리 합쳐서 256MB 이내, 스택 메모리 1MB 이내 / time_sec 2
난이도 : Master  |  정답률 84.21%

[채점] accepted  1/1  (0.28s)

[문제]
※ SW Expert 아카데미의 문제를 무단 복제하는 것을 금지합니다.

N개의 노드로 구성된 유향 그래프에 대해 인접 노드로 이동하는 비용을 기록한 인접 행렬이 주어진다.

모든 노드 i에 대해 다른 노드 j로 이동하는 경로가 있는 경우 최소 이동 비용을 구했을 때, 이 중 가장 큰 값을 출력하는 프로그램을 만드시오.

i에서 j로 이동할 때 다른 모든 노드를 지나야 하는 것은 아니며, 인접한 노드 사이 비용이 음수인 경우는 있으나 출발한 노드로 돌아왔을 때의 비용이 음수인 사이클은 존재하지 않는다.

다음과 같은 그래프가 있을 때 인접 행렬과 이동 비용은 다음과 같다.

[[IMG:1]]

 

			0

			27

			44

			-5

			0

			62

			0

			99

			0

[예제 1]
입력:
3
3
0 27 44
-5 0 62
0 99 0
5
0 0 1 0 0
88 0 39 0 75
71 56 0 43 0
23 0 -21 0 92
22 -1 48 0 0
10
0 94 98 0 23 0 31 0 85 0
10 0 78 19 83 0 91 0 82 -7
70 0 0 24 0 66 0 0 46 0
0 40 90 0 82 77 0 0 0 0
72 0 61 16 0 99 0 58 -9 44
82 84 61 76 29 0 30 28 20 72
39 78 76 0 0 11 0 54 58 39
0 0 25 40 10 0 57 0 19 38
68 5 81 78 87 54 60 -7 0 0
67 56 83 74 0 36 0 55 0 0
출력:
#1 99
#2 132
#3 92
"""

T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    N = int(input())
    INF = 10 ** 18
    dist = [list(map(int, input().split())) for _ in range(N)]

    for i in range(N):
        for j in range(N):
            if i == j:
                dist[i][j] = 0
            elif dist[i][j] == 0:
                dist[i][j] = INF

    for k in range(N):
        for i in range(N):
            for j in range(N):
                dist[i][j] = min(
                    dist[i][j],
                    dist[i][k] + dist[k][j]
                )

    answer = -INF

    for i in range(N):
        for j in range(N):
            if i != j:
                answer = max(answer, dist[i][j])
    print(f"#{test_case} {answer}")
