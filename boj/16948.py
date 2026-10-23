"""
BOJ 16948  데스 나이트
https://cosal.aviss.kr/problems/detail/16948

풀이일 : 2026-10-23   결과: 품
한도   : time 2 초 / memory 512 MB

[채점] accepted  17/17  (5.52s)

[문제]
게임을 좋아하는 큐브러버는 체스에서 사용할 새로운 말 "데스 나이트"를 만들었다. 데스 나이트가 있는 곳이 (r, c)라면, (r-2, c-1), (r-2, c+1), (r, c-2), (r, c+2), (r+2, c-1), (r+2, c+1)로 이동할 수 있다.

크기가 N×N인 체스판과 두 칸 (r1, c1), (r2, c2)가 주어진다. 데스 나이트가 (r1, c1)에서 (r2, c2)로 이동하는 최소 이동 횟수를 구해보자. 체스판의 행과 열은 0번부터 시작한다.

데스 나이트는 체스판 밖으로 벗어날 수 없다.

[예제 1]
입력:
7
6 6 0 1
출력:
4

[예제 2]
입력:
6
5 1 0 5
출력:
-1

[예제 3]
입력:
7
0 3 4 3
출력:
2
"""

from collections import deque
N = int(input())

r1, c1, r2, c2 = map(int, input().split())


INF = 10 ** 18

q = deque()

visited = [[INF] * N for _ in range(N)]

visited[r1][c1] = 0

q.append((r1, c1))

while q:
    cr, cc = q.popleft()

    for dr, dc in [[-2, -1], [-2, 1], [0, -2], [0, 2], [2, -1], [2, 1]]:
        nr = cr + dr
        nc = cc + dc


        if not (0 <= nr < N and 0 <= nc < N):
            continue

        if visited[nr][nc] > visited[cr][cc] + 1:
            visited[nr][nc] = visited[cr][cc] + 1
            q.append((nr, nc))

if visited[r2][c2] == INF:
    print(-1)
else:
    print(visited[r2][c2])
