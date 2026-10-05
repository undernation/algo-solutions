"""
CT 111  뿌요뿌요
https://www.codetree.ai/ko/trails/complete/curated-cards/test-puyo-puyo/description

풀이일 : 2026-10-05   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 61.2%
제약   : - $1 \le N \le 100$
제약   : - $1 \le \texttt{주어지는 수} \le 100$

[채점] accepted  3/3  (0.807s)

[문제]
각 칸에 $1$이상 $100$이하의 정수가 적힌 $N \times N$ 크기의 격자가 주어집니다. 

이때 상하좌우로 인접한 칸끼리 같은 정수로 이루어져 있는 경우 하나의 블럭으로 생각하며, 블럭을 이루고 있는 칸의 수가 $4$개 이상인 경우 해당 블럭은 터지게 됩니다.

초기 상태가 주어졌을 때,
터지게 되는 블럭은 몇 개인지,
그리고 가장 큰 블럭의 크기는 얼마인지
구하는 프로그램을 작성해보세요.

[예제 1]
입력:
3
1 1 1
2 1 2
1 1 1

출력:
1 7


[예제 2]
입력:
3
1 2 2
1 2 2
1 1 1

출력:
2 5


[예제 3]
입력:
3
1 2 4
1 2 2
3 1 1

출력:
0 3

"""

N = int(input())
grid = [list(map(int, input().split())) for _ in range(N)]

# Please write your code here.

max_block_size = 0

total_cnt = 0
visited = [[False] * N for _ in range(N)]


def dfs(cy, cx, cur_num):
    global cnt, visited

    for dy, dx in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
        ny = cy + dy
        nx = cx + dx

        if not (0 <= ny < N and 0 <= nx < N):
            continue

        if visited[ny][nx]:
            continue
        if grid[ny][nx] != cur_num:
            continue

        visited[ny][nx] = True

        dfs(ny, nx, cur_num)
        cnt += 1


for i in range(N):
    for j in range(N):
        if visited[i][j]:
            continue

        cur_num = grid[i][j]
        cnt = 1
        visited[i][j] = True

        dfs(i, j, cur_num)
        max_block_size = max(max_block_size, cnt)
        if cnt >= 4:
            total_cnt += 1

print(total_cnt, max_block_size)
