"""
BOJ 1726  로봇 (정올 1006)
https://jungol.co.kr/problem/1006

풀이일 : 2026-10-23   결과: 품
한도   : time 1 초 / time_sec 1 / memory 64 MB
제약   : 1 ≤ M, N ≤ 100
제약   : 출발 지점에서 도착 지점으로 이동 가능한 입력만 주어진다.

[문제]
정올 1006번 ‘로봇’과 같은 문제이며, 아카이브에서는 백준 1726번으로 관리한다.

로봇은 직사각형 격자에서 동·서·남·북 중 한 방향을 바라본다. 0인 칸을 이동할 수 있고, 1인 칸은 통과할 수 없다.

한 번의 명령으로 다음 중 하나를 실행한다.
- Go k: 바라보는 방향으로 1, 2, 3칸 중 선택한 거리만큼 전진한다. 이동 중 지나는 모든 칸도 이동 가능해야 한다.
- Turn left / Turn right: 현재 칸에서 왼쪽 또는 오른쪽으로 90도 회전한다.

출발 위치·방향에서 목표 위치·방향에 도달하는 데 필요한 최소 명령 수를 구한다. 아래 예제의 최소 명령 수는 9이다.

[예제 1]
입력:
5 6
0 0 0 0 0 0
0 1 1 0 1 0
0 1 0 0 0 0
0 0 1 1 1 0
1 0 0 0 0 0 
4 2 3
2 4 1
출력:
9
[채점] accepted  250/250  (6.055s)

[검증]
정올 공식 예제 1개, 독립 Dijkstra와 무작위 3,000개·경계 188개 대조: 모두 일치.
최대 100×100 빈 격자 0.1284초, 긴 통로 0.0665초 (로컬 Python, 프로세스 시작 포함).
정올 사이트에 대신 제출한 기록은 아니며, 위 검증을 거친 사용자 원본 풀이를 보관한다.
"""

from collections import deque

M, N = map(int, input().split())

board = [list(map(int, input().split())) for _ in range(M)]

sy, sx, sd = map(int, input().split())

ey, ex, ed = map(int, input().split())

sy -= 1
sx -= 1
ey -= 1
ex -= 1

rotate_dict = {
    1:3,
    2:4,
    3:2,
    4:1
}

rerotate_dict = {
    1:4,
    2:3,
    3:1,
    4:2
}

directions = {
    1: (0, 1),
    2: (0, -1),
    3: (1, 0),
    4: (-1, 0)
}

visited = dict()

visited[(sy, sx, sd)] = 0

q = deque()
q.append((sy, sx, sd))

while q:
    cy, cx, cd = q.popleft()
    if (cy, cx, cd) == (ey, ex, ed):
        print(visited[(cy, cx, cd)])
        break
    cur_order_cnt = visited[(cy, cx, cd)]
    new_order_cnt = cur_order_cnt + 1
    # 현재 방향으로 1 2 3 번 잉동하기
    for k in range(1, 4):
        dy, dx = directions[cd]

        ny = cy + dy * k
        nx = cx + dx * k
        nd = cd
        if not (0 <= ny < M and 0 <= nx < N):
            continue
        if board[ny][nx] == 1:
            break

        if (ny, nx, nd) in visited and visited[(ny, nx, nd)] <= new_order_cnt:
            continue

        q.append((ny, nx, nd))
        visited[(ny, nx, nd)] = new_order_cnt

    # 오른쪽 회전
    nd = rotate_dict[cd]
    ny = cy
    nx = cx
    if (ny, nx, nd) in visited and visited[(ny, nx, nd)] <= new_order_cnt:
        pass
    else:
        q.append((ny, nx, nd))
        visited[(ny, nx, nd)] = new_order_cnt

    # 왼쪽 회전
    nd = rerotate_dict[cd]
    if (ny, nx, nd) in visited and visited[(ny, nx, nd)] <= new_order_cnt:
        pass
    else:
        q.append((ny, nx, nd))
        visited[(ny, nx, nd)] = new_order_cnt

# print(visited)
