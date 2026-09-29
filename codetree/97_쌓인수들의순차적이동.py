"""
CT 97  쌓인 수들의 순차적 이동
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-sequential-movement-of-stacked-numbers/description

풀이일 : 2026-09-29   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 67.5%
제약   : - $2 \le N \le 20$
제약   : - $1 \le M \le 100$
제약   : - $1 \le \texttt{주어지는 수} \le N \times N$
제약   : - $1$ 이상 $N \times N$ 이하의 정수가 정확히 한 번씩만 나온다고 가정해도 좋습니다.

[채점] accepted  2/2  (0.512s)

[문제]
$1$ 이상 $N \times N$ 이하의 정수들이 정확히 한 번씩만 등장하는 $N \times N$ 크기의 격자판 정보가 주어집니다. 이때 $M$번에 걸쳐 정수들을 이동하려고 합니다. 이동할 정수들의 번호가 주어지고, 각 정수들은 특정 조건에 맞춰 움직이게 됩니다. 이 조건이란, 각 위치에서 여덟방향으로 인접한 칸들 중 가장 큰 값이 적혀있는 정수가 있는 곳으로 이동을 하는 것을 의미합니다. 이때 인접한 칸에 여러 정수가 쌓여 있다면 스택의 어느 위치에 있든 관계없이 모든 정수를 대상으로 가장 큰 값을 찾습니다.

이때 이동할 정수 위에 다른 정수들이 쌓여 있는 경우, 위에 쌓여있는 정수들도 순서를 유지한 채 함께 이동하며, 이동할 정수 아래에 깔려 있던 정수들은 그 자리에 그대로 남습니다. 이동한 위치에 이미 다른 정수가 있는 경우에는 옮겨진 정수들이 그 위에 순서대로 쌓이게 됩니다.

여덟방향으로 인접한 위치란, 예를 들어 다음 노란색 위치를 기준으로 회색 위치를 의미합니다.

![](https://contents.codetree.ai/problems/97/images/problems-5d08ffbe-af6c-4ee6-a4c7-e7f6ab31d6a6.png)

예를 들어 아래 그림을 살펴봅시다. $M$이 $4$이고, 움직일 정수들이 순서대로 $1, 7, 4, 1$ 라고 해봅시다.

![](https://contents.codetree.ai/problems/97/images/problems-d5d8fe95-19d0-4bff-ab6c-6aa42a4f05e0.png)

먼저 정수 $1$이 움직입니다. 이 경우 여덟방향으로 인접한 정수들 중 가장 큰 값인 $7$이 있는 위치로 움직이게 됩니다. 이때, 이 경우처럼 움직인 위치에 이미 다른 정수가 있는 경우에는 해당 정수들 중 가장 위에 위치하게 됩니다.

![](https://contents.codetree.ai/problems/97/images/problems-41afcc75-d341-4a22-8619-e41aa29777f5.png)

그 다음 정수 $7$을 움직입니다. 정수 $7$은 $6$이 있는 위치로 이동을 하게 되지만, 이때 위에 정수 $1$이 있기 때문에 $1$도 같이 움직이게 됩니다. 그 결과는 다음과 같습니다.

![](https://contents.codetree.ai/problems/97/images/problems-22b93475-f05b-4833-be11-1d7794f88a65.png)

그 다음 정수 $4$를 움직입니다. 정수 $4$는 인접한 정수 중 가장 큰 $7$이 있는 위치로 이동하게 됩니다.

![](https://contents.codetree.ai/problems/97/images/problems-0e34b188-03be-4ba5-86e9-30222fa1433f.png)

끝으로 정수 $1$을 다시 한 번 움직입니다. 이 경우 $9$가 있는 위치로 정수 $4$와 함께 이동하게 됩니다.

![](https://contents.codetree.ai/problems/97/images/problems-f89baa7c-35ad-49e8-93ee-234cc433c56c.png)

만약 선택된 정수의 인접한 여덟방향에 아무 정수도 없다면, 그때는 움직이지 않습니다.

$M$번의 움직임 이후의 상태를 출력하는 프로그램을 작성해보세요.

[예제 1]
입력:
3 4
7 1 4
2 6 3
9 8 5
1 7 4 1

출력:
None
None
None
2
7 6
3
4 1 9
8
5


[예제 2]
입력:
3 4
7 1 4
2 6 3
9 8 5
1 2 6 1

출력:
1 7
None
4
None
None
3
6 2 9
8
5

"""

N, M = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(N)]
move_nums = list(map(int, input().split()))

new_grid = [list([] for _ in range(N)) for _ in range(N)]

for i in range(N):
    for j in range(N):
        new_grid[i][j].append(grid[i][j])


def find(num):
    for i in range(N):
        for j in range(N):
            cur_list = new_grid[i][j]
            if num in cur_list:
                cur_idx = cur_list.index(num)
                return i, j, cur_idx


def check(cy, cx):
    max_val = -1
    max_y = -1
    max_x = -1

    for dy, dx in [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [-1, -1], [1, -1]]:
        ny = cy + dy
        nx = cx + dx
        if not (0 <= ny < N and 0 <= nx < N):
            continue
        cur_max_val = -1
        if new_grid[ny][nx]:
            cur_max_val = max(new_grid[ny][nx])

        if cur_max_val > max_val:
            max_val = cur_max_val
            max_y = ny
            max_x = nx

    return max_y, max_x


def stack(cy, cx, cur_idx, ny, nx):
    cur_list = new_grid[cy][cx][cur_idx:].copy()
    new_grid[ny][nx].extend(cur_list)
    del new_grid[cy][cx][cur_idx:]


for num in move_nums:
    cy, cx, cur_idx = find(num)

    ny, nx = check(cy, cx)
    if ny == -1:
        continue
    else:
        stack(cy, cx, cur_idx, ny, nx)

for i in range(N):
    for j in range(N):
        if len(new_grid[i][j]) == 0:
            print("None")
        else:
            new_grid[i][j].reverse()
            print(*new_grid[i][j])
