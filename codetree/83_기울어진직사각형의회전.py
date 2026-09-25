"""
CT 83  기울어진 직사각형의 회전
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-rotate-slanted-rectangle/description

풀이일 : 2026-09-25   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Hard  |  정답률 71.5%
제약   : - $3 \le N \le 100$
제약   : - $1 \le A_{i,j} \le 100$ $(1 \le i, j \le N)$
제약   : - $1 \le r, c \le N$
제약   : - $1 \le m_1, m_2, m_3, m_4 \le N-1$
제약   : - $m_1 = m_3,\ m_2 = m_4$
제약   : - $dir \in \{0, 1\}$

[채점] accepted  2/2  (0.559s)

[문제]
$1$ 이상 $100$ 이하의 정수로만 이루어져 있는 $N \times N$ 크기의 격자 정보가 주어집니다.

![](https://contents.codetree.ai/problems/83/images/problems-8fcfe0ab-9f15-48a1-9a00-5f80356edd73.png)

이때, 이 격자 내에 있는 임의의 기울어진 직사각형을 잡아 회전시키려고 합니다.

기울어진 직사각형이란, 격자내에 있는 한 지점으로부터 체스의 비숍처럼 대각선으로 움직이며 반시계 순회를 했을 때 지나왔던 지점들의 집합을 일컫습니다. 이 때 반드시 아래에서 시작해서 $1$, $2$, $3$, $4$번 방향순으로 순회해야하며 각 방향으로 최소 $1$번은 움직여야 합니다. 또한, 이동하는 도중 격자 밖으로 넘어가서는 안됩니다.

![](https://contents.codetree.ai/problems/83/images/problems-3b947b0b-2be9-4f4b-85dc-e03e10f006de.png)

예를 들어 위의 규칙에 따라 다음과 같이 기울어진 직사각형을 잡아볼 수 있습니다.

![](https://contents.codetree.ai/problems/83/images/problems-eda92fb0-b4a4-41f9-83e7-e55fcb572873.png)

위의 기울어진 직사각형의 경우 $4$행 $2$열 위치에서 시작하여 순서대로 $1$번 방향으로 $2$칸, $2$번 방향으로 $1$칸, $3$번 방향으로 $2$칸, $4$번 방향으로 $1$칸 이동했으므로 이는 편의상 $4$, $2$, $2$, $1$, $2$, $1$로 나타낼 수 있습니다. 만약 이 직사각형의 순회경로상에 있는 색칠된 정수들에 대해서만 반시계 방향으로 한 칸씩 정수들을 움직이게 된다면, 다음과 같이 정수들이 바뀌게 됩니다.

![](https://contents.codetree.ai/problems/83/images/problems-2b7286fc-1cda-479b-a5b9-67ee368ddfb9.png)

초기 격자의 정보와 특정 기울어진 사각형에 대해서 반시계 혹은 시계 방향으로 회전해야 하는 정보가 주어졌을 때, 회전 이후의 결과를 출력하는 프로그램을 작성해보세요.

[예제 1]
입력:
5
1 2 2 2 2
1 3 4 4 4
1 2 3 3 3
1 2 3 3 3
1 2 3 3 3
4 2 2 1 2 1 0

출력:
1 2 4 2 2
1 2 4 3 4
3 2 2 3 3
1 1 3 3 3
1 2 3 3 3


[예제 2]
입력:
5
1 2 2 2 2
1 3 4 4 4
1 2 3 3 3
1 2 3 3 3
1 2 3 3 3
4 2 2 1 2 1 1

출력:
1 2 3 2 2
1 1 4 2 4
2 2 4 3 3
1 3 3 3 3
1 2 3 3 3

"""

N = int(input())
grid = [list(map(int, input().split())) for _ in range(N)]
r, c, m1, m2, m3, m4, dir = map(int, input().split())

# Please write your code here.

def re_rotate(sy, sx, length, height):
    temp = grid[sy - 1][sx - 1]

    targets = []

    cy, cx = sy, sx
    targets.append((cy, cx))
    # 아랫변
    dy = -1
    dx = 1
    # 맨 마지막 이전까지 넣어주기
    for i in range(length):
        ny = cy + dy
        nx = cx + dx
        targets.append((ny, nx))
        cy, cx = ny, nx

    # 오른쪽
    dy = -1
    dx = -1
    for i in range(height):
        ny = cy + dy
        nx = cx + dx
        targets.append((ny, nx))
        cy, cx = ny, nx

    # 윗변
    dy = 1
    dx = -1
    for i in range(length):
        ny = cy + dy
        nx = cx + dx
        targets.append((ny, nx))
        cy, cx = ny, nx

    dy = 1
    dx = 1
    for i in range(height - 1):
        ny = cy + dy
        nx = cx + dx
        targets.append((ny, nx))
        cy, cx = ny, nx

    len_N = len(targets)

    for n in range(len_N - 1, 0, -1):
        cy, cx = targets[n]
        ny, nx = targets[n - 1]
        grid[cy][cx] = grid[ny][nx]

    grid[sy][sx] = temp

def rotate(sy, sx, length, height):
    temp = grid[sy - 1][sx + 1]

    targets = []

    cy, cx = sy, sx
    targets.append((cy, cx))
    # 아랫변
    dy = -1
    dx = -1
    # 맨 마지막 이전까지 넣어주기
    for i in range(height):
        ny = cy + dy
        nx = cx + dx
        targets.append((ny, nx))
        cy, cx = ny, nx

    # 오른쪽
    dy = -1
    dx = 1
    for i in range(length):
        ny = cy + dy
        nx = cx + dx
        targets.append((ny, nx))
        cy, cx = ny, nx

    # 윗변
    dy = 1
    dx = 1
    for i in range(height):
        ny = cy + dy
        nx = cx + dx
        targets.append((ny, nx))
        cy, cx = ny, nx

    dy = 1
    dx = -1
    for i in range(length - 1):
        ny = cy + dy
        nx = cx + dx
        targets.append((ny, nx))
        cy, cx = ny, nx

    len_N = len(targets)

    for n in range(len_N - 1, 0, -1):
        cy, cx = targets[n]
        ny, nx = targets[n - 1]
        grid[cy][cx] = grid[ny][nx]

    grid[sy][sx] = temp

if dir == 0:
    re_rotate(r - 1, c - 1, m1, m2)

else:
    rotate(r - 1, c - 1, m1, m2)

for i in grid:
    print(*i)
