"""
CT 86  십자 모양 폭발
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-cross-shape-bomb/description

풀이일 : 2026-09-25   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Easy  |  정답률 63.5%
제약   : - $1 \le N \le 200$
제약   : - $1 \le r, c \le N$
제약   : - $1 \le \texttt{grid}_{i, j} \le 100$ ($1 \le i, j \le N$)

[문제]
$1$이상 $100$이하의 정수로 구성된 $N \times N$ 크기의 격자판이 주어집니다. 이때 특정 위치를 선택하면, 그 위치를 중심으로 십자 모양으로 폭탄이 터지게 됩니다. 십자 모양의 크기는 선택된 위치에 적혀있는 정수로 정해지며, 터진 이후에는 중력에 의해 정수들이 아래로 떨어지게 됩니다.

십자 모양의 크기는 선택된 정수에 비례하여 커집니다. 선택된 정수가 $1$인 경우에는 자기 자신만 터지게 되고, 선택한 정수가 $2$인 경우에는 자신을 포함하여 인접한 $4$개의 격자 역시 터지게 되며, $3$인 경우에는 자신을 포함한 상하좌우 방향으로 각각 $2$개씩이 더 터지게 됩니다. 정수가 $4$ 이상인 경우에도 마찬가지의 규칙에 따라 해당 범위만큼 터지게 됩니다.

![](https://contents.codetree.ai/problems/86/images/problems-fa99650e-02f7-4697-8cca-88d08381bb0c.png)

예를 들어 다음 위치를 선택하게 되면, 폭탄이 터지고 중력이 작용한 이후의 결과가 다음과 같이 나타나게 됩니다.

![](https://contents.codetree.ai/problems/86/images/problems-aa9c80d9-b295-4171-bb9e-a40879bf47f6.png)

또 다른 예로 다음 위치를 선택하게 되었을 때 결과는 다음과 같습니다.

![](https://contents.codetree.ai/problems/86/images/problems-ad381cdc-5022-4870-9115-f1e596269841.png)

만약 다음과 같이 폭탄이 터져야 하는 범위가 격자 판을 벗어나게 되더라도, 격자 안에서만 폭탄이 터지게 됩니다.

![](https://contents.codetree.ai/problems/86/images/problems-16539541-bca1-4a11-a078-c262a280338f.png)

초기 격자판의 상태와 폭탄이 터질 곳의 중심 위치가 주어졌을 때, 폭탄이 터진 뒤 중력이 작용하고 나서의 결과를 출력하는 프로그램을 작성해보세요.

[예제 1]
입력:
4
1 2 4 3
3 2 2 3
3 1 6 2
4 5 4 4
2 3

출력:
1 0 0 0
3 2 0 3
3 1 0 2
4 5 4 4


[예제 2]
입력:
4
1 2 4 3
3 2 2 3
3 1 6 2
4 5 4 4
3 3

출력:
0 0 0 0
1 2 0 3
3 2 0 3
4 5 0 4

"""

N = int(input())
grid = [list(map(int, input().split())) for _ in range(N)]
r, c = map(int, input().split())

# Please write your code here.
r -= 1
c -= 1


def explode(sy, sx):
    cur_num = grid[sy][sx]
    cur_num -= 1
    # 상 하 좌 우
    grid[sy][sx] = 0
    for dy, dx in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
        cy = sy
        cx = sx

        for idx in range(cur_num):
            ny = cy + dy
            nx = cx + dx
            if not (0 <= ny < N and 0 <= nx < N):
                break
            grid[ny][nx] = 0
            cy = ny
            cx = nx


explode(r, c)

for j in range(N):
    temp = [0] * N
    idx = N - 1
    for i in range(N - 1, -1, -1):
        if grid[i][j] != 0:
            temp[idx] = grid[i][j]
            idx -= 1

    for i in range(N - 1, -1, -1):
        grid[i][j] = temp[i]

for i in grid:
    print(*i)
