"""
SWEA 1767  [SW Test 샘플문제] 프로세서 연결하기
https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AV4suNtaXFEDFAUf

풀이일 : 2026-09-20   결과: 품
한도   : time 60개 테스트케이스를 합쳐서 C++의 경우 2초 / Java의 경우 4초 / Python의 경우 8초 / memory 힙, 정적 메모리 합쳐서 256MB 이내, 스택 메모리 1MB 이내 / time_sec 8
난이도 : Master  |  정답률 42.38%

[채점] accepted  1/1  (0.81s)

[문제]
※ SW Expert 아카데미의 문제를 무단 복제하는 것을 금지합니다.

삼성에서 개발한 최신 모바일 프로세서 멕시노스는 가로 N개 x 세로 N개의 cell로 구성되어 있다.

[[IMG:1]]

1개의 cell에는 1개의 Core 혹은 1개의 전선이 올 수 있다.

[[IMG:2]]

멕시노스의 가장 자리에는 전원이 흐르고 있다.

[[IMG:3]]

Core와 전원을 연결하는 전선은 직선으로만 설치가 가능하며,

[[IMG:4]]

전선은 절대로 교차해서는 안 된다.

[[IMG:5]]

초기 상태로는 아래와 같이 전선을 연결하기 전 상태의 멕시노스 정보가 주어진다.

(멕시노스의 가장자리에 위치한 Core는 이미 전원이 연결된 것으로 간주한다.)

[[IMG:6]]

[[IMG:7]]

▶ 최대한 많은 Core에 전원을 연결하였을 경우, 전선 길이의 합을 구하고자 한다.

   단, 여러 방법이 있을 경우, 전선 길이의 합이 최소가 되는 값을 구하라.

위 예제의 정답은 12가 된다.

[제약 사항]

1. 7 ≤  N ≤ 12

2. Core의 개수는 최소 1개 이상 12개 이하이다.

3. 최대한 많은 Core에 전원을 연결해도, 전원이 연결되지 않는 Core가 존재할 수 있다.

[예제 1]
입력:
3
7
0 0 1 0 0 0 0
0 0 1 0 0 0 0
0 0 0 0 0 1 0
0 0 0 0 0 0 0
1 1 0 1 0 0 0
0 1 0 0 0 0 0
0 0 0 0 0 0 0
9
0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 1
1 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0
0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0
0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 1
11
0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1
0 0 0 1 0 0 0 0 1 0 0
0 1 0 1 1 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
출력:
#1 12
#2 10
#3 24
"""


T = int(input())
DIR = [[0, 1], [0, -1], [1, 0], [-1, 0]]
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    N = int(input())
    board = [list(map(int, input().split())) for _ in range(N)]


    def check_boundary(cy, cx):
        if cy == 0 or cy == N - 1:
            return True
        elif cx == 0 or cx == N - 1:
            return True

        return False


    def check_connect(cy, cx, direction):

        dy, dx = DIR[direction]

        while True:
            ny = cy + dy
            nx = cx + dx
            if not (0 <= ny < N and 0 <= nx < N):
                return True
            if board[ny][nx] != 0:
                return False
            cy = ny
            cx = nx


    def connect(cy, cx, direction):
        dy, dx = DIR[direction]
        cnt = 0
        while True:
            ny = cy + dy
            nx = cx + dx
            if not (0 <= ny < N and 0 <= nx < N):
                break
            board[ny][nx] = 2
            cy = ny
            cx = nx
            cnt += 1
        return cnt


    def unconnect(cy, cx, direction):
        dy, dx = DIR[direction]
        while True:
            ny = cy + dy
            nx = cx + dx
            if not (0 <= ny < N and 0 <= nx < N):
                break
            board[ny][nx] = 0
            cy = ny
            cx = nx


    processors = []
    for i in range(N):
        for j in range(N):
            if board[i][j] == 1:
                processors.append((i, j))
    core_cnt = len(processors)
    max_core = 0
    min_val = 10 ** 18


    def dfs(idx, connected, length):
        global min_val, max_core
        if idx == core_cnt:
            if connected > max_core:
                min_val = length
                max_core = connected
            elif connected == max_core:
                min_val = min(length, min_val)
            return


        cy, cx = processors[idx]
        if check_boundary(cy, cx):
            dfs(idx + 1, connected + 1, length)
        else:
            for direction in range(4):

                # 해당 방향으로 연결가능 확인
                if check_connect(cy, cx, direction):
                    # print("wow")
                    # 실제로 연결해주기
                    cnt = connect(cy, cx, direction)
                    dfs(idx + 1, connected + 1, length + cnt)
                    unconnect(cy, cx, direction)

            # 그냥 연결 안하는 경우의 수
            dfs(idx + 1, connected, length)


    dfs(0, 0, 0)

    answer = min_val

    print(f"#{test_case} {answer}")
