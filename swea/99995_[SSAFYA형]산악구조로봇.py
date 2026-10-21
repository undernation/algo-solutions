"""
SWEA 99995  [SSAFY A형] 산악 구조 로봇
https://lab.ssafy.com/s16/b06/lectures/-/blob/2fdc0ae590f6731564ff0014568d70833c474f2a/99_exam/A/%EC%82%B0%EC%95%85%EA%B5%AC%EC%A1%B0%EB%A1%9C%EB%B4%87/%EC%82%B0%EC%95%85%EA%B5%AC%EC%A1%B0%EB%A1%9C%EB%B4%87.md

풀이일 : 2026-10-21   결과: 품
한도   : time 50개 테스트케이스 합산 C/C++ 3초, Java 3초, Python 5초 / time_sec 5 / memory 256MB (스택 최대 1MB) / time_scope all_testcases / runtime Python / time_source source_markdown
제약   : 4 ≤ N ≤ 30
제약   : 각 칸의 높이는 0 이상 9 이하의 정수이다.
제약   : 대각선으로는 이동할 수 없다.

[채점] accepted  2/2  (0.707s)

[문제]
강의자료의 설명 MD를 옮긴 A형 연습 문제입니다. 99995는 아카이브 내부 번호이며 공식 SWEA 번호가 아닙니다.

MD에 제시된 첫 두 케이스는 예제 입력의 T를 2로 맞췄습니다. 제공 입력의 나머지 3개는 추가 연습 케이스로 등록했습니다.

산악 구조를 위한 로봇이 있다. 로봇은 연료 소모를 최소화하면서 조난자가 있는 위치까지 이동하려고 한다.

N × N 크기의 정방형 지도가 주어지고, 각 칸에는 해당 땅의 높이가 적혀 있다.

로봇은 상, 하, 좌, 우로만 이동할 수 있으며, 이동할 때 소모되는 연료는 다음과 같다.

| 이동 조건 | 소모 연료 |
|---|---:|
| 현재 위치와 높이가 같은 칸으로 이동 | 1 |
| 현재 위치보다 낮은 칸으로 이동 | 0 |
| 현재 위치보다 높은 칸으로 이동 | 높이 차이 × 2 |

로봇은 (1, 1)에서 출발하며, 조난자는 (N, N)에 있다. 조난자 위치까지 이동하는 경로 중 소모 연료의 최솟값을 구하라.

[예제 1]
입력:
2
4
9 5 7 9
8 4 2 5
7 6 5 4
8 8 9 5
6
1 1 1 1 1 1
9 9 9 9 9 1
9 9 1 1 1 1
9 9 1 9 9 9
9 9 1 9 9 9
9 9 1 1 1 1

출력:
#1 2
#2 16

"""

from collections import deque
T = int(input())
for tc in range(1, T + 1):
    N = int(input())
    board = [list(map(int, input().split())) for _ in range(N)]
    
    sy, sx = 0, 0
    
    INF = 10 ** 18
    cost_board = [[INF] * N for _ in range(N)]
    
    cost_board[0][0] = 0
    
    q = deque()
    q.append((sy, sx))
    
    while q:
        cy, cx = q.popleft()
        cur_cost = cost_board[cy][cx]
    
        for dy, dx in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            ny = cy + dy
            nx = cx + dx
    
            if not (0 <= ny < N and 0 <= nx < N):
                continue
    
            cur_num = board[cy][cx]
            nxt_num = board[ny][nx]
            nxt_cost = cost_board[ny][nx]
            if cur_num == nxt_num:
                new_cost = cur_cost + 1
            elif nxt_num < cur_num:
                new_cost = cur_cost
            else:
                new_cost = cur_cost + (nxt_num - cur_num) * 2
    
    
            if nxt_cost > new_cost:
                cost_board[ny][nx] = new_cost
                q.append((ny, nx))
    
    
    
    print(f"#{tc} {cost_board[N - 1][N - 1]}")
