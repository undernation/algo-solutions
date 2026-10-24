"""
PGS 67259  경주로 건설
https://school.programmers.co.kr/learn/courses/30/lessons/67259

풀이일 : 2026-10-24   결과: 품 (1회차, 사용자 요청 / 본인 코드 보존)
제약   : 3 <= N <= 25, 시작점·도착점은 빈칸, 도달 가능한 보드만 입력됨.
검증·복기 : notes/programmers/67259.md
메모   : 줄바꿈·들여쓰기와 채팅의 Markdown 이스케이프만 복원함.
"""

from collections import deque


def solution(board):
    answer = 0

    visited = dict()
    directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    N = len(board)

    q = deque()

    if board[1][0] != 1:
        visited[(1, 0, 0)] = 100
        q.append((1, 0, 0, 100))

    if board[0][1] != 1:
        visited[(0, 1, 2)] = 100
        q.append((0, 1, 2, 100))

    answer_cands = []
    while q:
        cy, cx, cur_direction, cur_cost = q.popleft()
        if cy == N - 1 and cx == N - 1:
            answer_cands.append(cur_cost)

        for last_new_direction in range(4):
            dy, dx = directions[last_new_direction]
            ny = cy + dy
            nx = cx + dx
            if not (0 <= ny < N and 0 <= nx < N):
                continue
            if board[ny][nx] == 1:
                continue

            # 방향 달라지는 경우
            if cur_direction != last_new_direction:
                new_cost = cur_cost + 600
            # 방향 같은 경우
            else:
                new_cost = cur_cost + 100

            if (ny, nx, last_new_direction) in visited and visited[(ny, nx, last_new_direction)] <= new_cost:
                continue
            visited[(ny, nx, last_new_direction)] = new_cost
            q.append((ny, nx, last_new_direction, new_cost))

        # print(visited[(ny, nx, )])
    # print(answer_cands)
    # INF = 1000000
    # debug_board = [[INF] * N for _ in range(N)]
    # for key, value in visited.items():
    #     cy, cx, cd = key
    #     debug_board[cy][cx] = min(debug_board[cy][cx], value)
    # for i in debug_board:
    #     print(i)

    return min(answer_cands)
