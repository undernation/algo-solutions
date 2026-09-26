"""
CT 89  최적의 십자 모양 폭발
https://www.codetree.ai/ko/trails/complete/curated-cards/test-best-cross-shape-bomb/description

풀이일 : 2026-09-26   결과: 품
한도   : time Python3 3.5초 · C++17 1초 / memory 256 MB / time_sec 3.5
난이도 : Medium  |  정답률 55.4%
제약   : - $1 \le N \le 50$
제약   : - $1 \le A_{ij} \le 100$ $(1 \le i, j \le N)$

[채점] accepted  2/2  (0.517s)

[문제]
정수로 구성된 $N \times N$ 크기의 격자판이 주어집니다. 이때 특정 위치를 선택하면, 그 위치를 중심으로 십자 모양으로 폭탄이 터지게 됩니다. 십자 모양의 크기는 선택된 위치에 적혀있는 정수로 정해지며, 터진 이후에는 중력에 의해 정수들이 아래로 떨어지게 됩니다.

십자 모양의 크기는 선택된 정수에 비례하여 커집니다. 선택된 정수가 $1$인 경우에는 자기 자신만 터지게 되고, 선택한 정수가 $2$인 경우에는 자신을 포함하여 인접한 $4$개의 격자 역시 터지게 되며, 3인 경우에는 자신을 제외한 상하좌우 방향으로 각각 $2$개씩이 더 터지게 됩니다. 정수가 $4$ 이상인 경우에도 마찬가지의 규칙에 따라 해당 범위만큼 터지게 됩니다.

![](https://contents.codetree.ai/problems/89/images/problems-82938cf5-da12-4114-b12e-78abdf1cc251.png)

예를 들어 다음 위치를 선택하게 되면, 폭탄이 터지고 중력이 작용한 이후의 결과가 다음과 같이 나타나게 됩니다.

![](https://contents.codetree.ai/problems/89/images/problems-4c983ca5-a394-405b-ab70-465996d470a7.png)

또 다른 예로 다음 위치를 선택하게 되었을 때 결과는 다음과 같습니다.

![](https://contents.codetree.ai/problems/89/images/fef1a7ad-62cf-4541-bbd1-22152306b9b2.png)

만약 다음과 같이 폭탄이 터져야 하는 범위가 격자판을 벗어나게 되더라도, 격자 안에서만 폭탄이 터집니다.

![](https://contents.codetree.ai/problems/89/images/problems-aaf9695d-a84f-46d5-b678-3209010b1703.png)

최적의 십자 모양 폭발이란, 특정 위치를 선택하여 폭탄이 터진 뒤 중력이 작용한 이후에 상하좌우로 인접한 격자끼리 적혀있는 정수가 동일한 쌍의 수가 최대가 되도록 하는 폭발을 의미합니다. 여기서 쌍은 변을 공유하는 두 칸의 무순서 쌍을 의미하며, 이러한 쌍을 각각 하나로 셉니다.

만약 $3$행 $3$열을 중심으로 터뜨리게 된다면, 인접한 곳끼리 정수가 동일한 쌍의 수가 총 $2$개가 됩니다.

![](https://contents.codetree.ai/problems/89/images/problems-dc1913b8-4fb1-4f96-8f81-35356b9fb54f.png)
하지만 만약 $3$행 $2$열을 중심으로 터뜨리게 된다면, 조건을 만족하는 쌍의 수는 $5$개로 최대가 됩니다.

![](https://contents.codetree.ai/problems/89/images/problems-3d21d96d-f2dc-46f5-b4d3-517dd9f7d934.png)

초기 격자판의 상태가 주어졌을 때 폭탄이 터질 중심 위치를 적절하게 골라, 폭탄이 터진 뒤 중력이 작용하고 나서 조건을 만족하는 쌍의 개수가 최대가 되도록 하는 프로그램을 작성해보세요.

[예제 1]
입력:
4
1 2 4 3
3 2 2 3
3 1 6 2
4 5 4 4

출력:
5


[예제 2]
입력:
3
1 2 1
4 5 6
1 8 1

출력:
2

"""

N = int(input())
grid = [list(map(int, input().split())) for _ in range(N)]

# Please write your code here.

def explode(sy, sx, cur_grid):
    cur_num = cur_grid[sy][sx]

    cur_num -= 1
    cur_grid[sy][sx] = 0

    for dy, dx in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
        cy = sy
        cx = sx

        for _ in range(cur_num):
            ny = cy + dy
            nx = cx + dx
            if not (0 <= ny < N and 0 <= nx < N):
                continue
            cur_grid[ny][nx] = 0
            cy = ny
            cx = nx

def down(cur_grid):
    for j in range(N):
        ret = []
        for i in range(N):
            if cur_grid[i][j] != 0:
                ret.append(cur_grid[i][j])
        len_ret = len(ret)
        temp = [0] * (N - len_ret) + ret

        for i in range(N):
            cur_grid[i][j] = temp[i]

def check_pair(cur_grid):
    pairs = set()

    for i in range(N):
        for j in range(N):
            if cur_grid[i][j] == 0:
                continue
            cy = i
            cx = j
            cur_num = cur_grid[cy][cx]

            for dy, dx in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
                ny = cy + dy
                nx = cx + dx

                if not (0 <= ny < N and 0 <= nx < N):
                    continue
                nxt_num = cur_grid[ny][nx]

                if cur_num == nxt_num:
                    pairs.add((cy, cx, ny, nx))
                    pairs.add((ny, nx, cy, cx))

    return (len(pairs) // 2)
answer = 0

for i in range(N):
    for j in range(N):
        new_grid = [row[:] for row in grid]
        explode(i, j, new_grid)
        down(new_grid)
        answer = max(answer, check_pair(new_grid))

print(answer)
