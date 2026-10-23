"""
BOJ 2206  벽 부수고 이동하기
https://cosal.aviss.kr/problems/detail/2206

풀이일 : 2026-10-23   결과: 품
한도   : time 2 초 / memory 192 MB

[채점] accepted  16/16  (8.183s)

[문제]
N×M의 행렬로 표현되는 맵이 있다. 맵에서 0은 이동할 수 있는 곳을 나타내고, 1은 이동할 수 없는 벽이 있는 곳을 나타낸다. 당신은 (1, 1)에서 (N, M)의 위치까지 이동하려 하는데, 이때 최단 경로로 이동하려 한다. 최단경로는 맵에서 가장 적은 개수의 칸을 지나는 경로를 말하는데, 이때 시작하는 칸과 끝나는 칸도 포함해서 센다.

만약에 이동하는 도중에 한 개의 벽을 부수고 이동하는 것이 좀 더 경로가 짧아진다면, 벽을 한 개 까지 부수고 이동하여도 된다.

한 칸에서 이동할 수 있는 칸은 상하좌우로 인접한 칸이다.

맵이 주어졌을 때, 최단 경로를 구해 내는 프로그램을 작성하시오.

[예제 1]
입력:
6 4
0100
1110
1000
0000
0111
0000
출력:
15

[예제 2]
입력:
4 4
0111
1111
1111
1110
출력:
-1
"""

from collections import deque

N, M = map(int, input().split())

board = [list(input()) for _ in range(N)]


INF = 10 ** 18

visited = [list([INF] * 2 for _ in range(M)) for _ in range(N)]

visited[0][0][0] = 1

q = deque()
q.append((0, 0, 0))

while q:
    cy, cx, is_used = q.popleft()
    new_cnt = visited[cy][cx][is_used] + 1
    for dy, dx in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
        ny = cy + dy
        nx = cx + dx

        if not (0 <= ny < N and 0 <= nx < M):
            continue

        if board[ny][nx] == '1':
            if is_used == 1:
                continue
            else:
                nxt_cnt = visited[ny][nx][1]
                if nxt_cnt > new_cnt:
                    visited[ny][nx][1] = new_cnt
                    q.append((ny, nx, 1))
        else:
            nxt_cnt = visited[ny][nx][is_used]
            if nxt_cnt > new_cnt:
                visited[ny][nx][is_used] = new_cnt
                q.append((ny, nx, is_used))

answer = min(visited[N - 1][M - 1])

if answer == INF:
    print(-1)
else:
    print(answer)
