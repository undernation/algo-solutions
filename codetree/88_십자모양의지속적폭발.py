"""
CT 88  십자 모양의 지속적 폭발
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-cross-shape-continuous-bomb/description

풀이일 : 2026-09-26   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Hard  |  정답률 75.9%
제약   : - $1 \le N \le 200$
제약   : - $1 \le M \le 10$
제약   : - $1 \le A_{ij} \le 100$ $(1 \le i, j \le N)$
제약   : - $1 \le c \le N$

[채점] accepted  2/2  (0.519s)

[문제]
$1$이상 $100$이하의 정수로 구성된 $N \times N$ 크기의 격자판이 주어집니다. 이때 특정 열을 선택하면, 해당 열에 정수가 적혀있는 위치 중 가장 위에 있는 칸을 중심으로 십자 모양으로 폭탄이 터지게 됩니다. 십자 모양의 크기는 선택된 칸에 적혀있는 정수로 정해지며, 터진 이후에는 중력에 의해 정수들이 아래로 떨어지게 됩니다.

십자 모양의 크기는 선택된 정수에 비례하여 커집니다. 선택된 정수가 $1$인 경우에는 자기 자신만 터지게 되고, 선택한 정수가 $2$인 경우에는 자신을 포함하여 인접한 $4$개의 격자 역시 터지게 되며, $3$인 경우에는 자신을 포함한 상하좌우 방향으로 각각 $2$개씩이 더 터지게 됩니다. 정수가 $4$ 이상인 경우에도 마찬가지의 규칙에 따라 해당 범위만큼 터지게 됩니다.

![](https://contents.codetree.ai/problems/88/images/problems-f6d2e0d8-6556-4239-b804-0b8c25428b98.png)

예를 들어 다음 격자판에서 $2$번째 열을 선택하게 되면, 폭탄이 터지고 중력이 작용한 이후의 결과가 다음과 같이 나타나게 됩니다.

![](https://contents.codetree.ai/problems/88/images/problems-0f95533c-a36a-448b-9b82-a479c7d70f44.png)

그 이후에 연달아 $2$번째 열을 다시 선택하게 되면, 다음과 같은 결과를 얻게 됩니다.

![](https://contents.codetree.ai/problems/88/images/problems-fb0483d5-d182-46ce-9bec-8ab9ecd613fc.png)

만약 또다시 $2$번째 열을 선택하게 되면, 다음과 같이 폭탄이 터져야 하는 범위가 격자판을 벗어나게 되지만, 이 경우에는 격자 안에서만 폭탄이 터지게 됩니다.

![](https://contents.codetree.ai/problems/88/images/problems-e904766d-b697-4ad5-9055-162f770f1776.png)

이때 또 $2$번째 열을 선택하게 되면 두 번째 열에서는 더 이상 터질 폭탄이 없습니다. 이러한 경우에는 아무 변화가 일어나지 않습니다.

초기 격자판의 상태와 폭탄이 터질 곳의 열의 위치가 순서대로 주어졌을 때, 순서대로 폭탄을 터뜨리고 중력이 작용하는 것을 반복한 이후의 결과를 출력하는 프로그램을 작성해보세요.

[예제 1]
입력:
4 4
1 1 2 3
3 2 2 3
3 1 6 2
4 5 4 4
2
2
2
2

출력:
0 0 0 0
0 0 0 3
1 0 2 3
3 0 6 2


[예제 2]
입력:
4 3
1 2 4 3
3 2 2 3
3 1 6 2
4 5 4 4
2
2
2

출력:
0 0 0 0
0 0 0 3
3 0 2 3
3 0 6 2

"""

N, M = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(N)]
commands = [int(input()) for _ in range(M)]


# Please write your code here.

def explode(sy, sx):
    cur_num = grid[sy][sx]
    cur_num -= 1
    grid[sy][sx] = 0
    for dy, dx in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
        cy = sy
        cx = sx

        for n in range(cur_num):
            ny = cy + dy
            nx = cx + dx
            if not (0 <= ny < N and 0 <= nx < N):
                break
            cy = ny
            cx = nx
            grid[cy][cx] = 0


def push_down():
    for j in range(N):
        temp = [0] * N
        idx = N - 1
        for i in range(N - 1, -1, -1):
            if grid[i][j] != 0:
                temp[idx] = grid[i][j]
                idx -= 1

        for i in range(N):
            grid[i][j] = temp[i]

def select(col_num):
    for i in range(N):
        if grid[i][col_num] != 0:
            return i
    return -1

# print(0 == False)

for command in commands:
    row = select(command - 1)
    if row == -1:
        continue
    explode(row, command - 1)
    push_down()

for i in grid:
    print(*i)
