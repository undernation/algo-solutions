"""
CT 87  단 한 번의 2048 시도
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-one-trial-of-2048-game/description

풀이일 : 2026-09-26   결과: 못품
한도   : time Python3 1초 · C++17 0.5초 / memory 64 MB / time_sec 1
난이도 : Medium  |  정답률 59.4%
제약   : - 격자에 주어진 값은 $0$ 또는 $2$ 이상 $2048$ 이하의 $2$의 거듭제곱입니다.
제약   : - $dir$은 `L`, `R`, `U`, `D` 중 하나입니다.

[채점] accepted  2/2  (0.571s)

[문제]
$2048$게임은 $4 \times 4$ 격자 안에서 이루어지는 게임입니다. 이 $2048$ 게임에서는 상하좌우 중 한 방향을 정하게 되면, 모든 값들이 해당 방향으로 전부 밀리게 됩니다.

예를 들어 다음 판에서 밑으로 방향을 정하게 되면, 다음과 같이 아래로 중력이 작용한 이후의 결과를 얻게 됩니다.

![](https://contents.codetree.ai/problems/87/images/problems-f6c01647-5412-4f91-8df7-5fccbb73cb09.png)

하지만 $2048$ 게임에서는 같은 값끼리 만나게 되는 경우 두 값이 합쳐지게 됩니다. 다음의 경우 아래로 움직이는 예를 보면 값 $2$ 두 개가 합쳐서 값 $4$가 됩니다.

![](https://contents.codetree.ai/problems/87/images/problems-19574441-5f88-4bce-b686-c026f9d66ba1.png)

또한, 단 한 번의 중력작용으로 이미 합쳐진 값이 연쇄적으로 합쳐지진 않습니다. 다음의 경우 아래로 움직이는 예를 보면 값 $2$ 두 개가 이미 한번 합쳐져 $4$가 되었기 때문에, 위의 $4$와 다시 합쳐지진 않습니다.

![](https://contents.codetree.ai/problems/87/images/problems-e7bbb22a-0b4d-43a8-8aaf-ba685f7c5a2a.png)

그리고 세 개 이상의 같은 값이 중력작용 방향으로 놓여 있으면, 중력에 의해 부딪히게 될 벽(바닥)에서 가까운 값부터 두 개씩만 합쳐집니다. 즉, 서너개 이상의 값이 하나로 합쳐질 순 없고 아래 예시처럼 바닥에 가까운 순서대로 한 쌍씩 짝을 이뤄 합쳐집니다. 다음 예시는 아래로 중력이 작용해서 값 $2$ 네개가 $4$ 두개로 합쳐진 것입니다.

![](https://contents.codetree.ai/problems/87/images/problems-94033b88-e306-4653-a201-f3de16f2096e.png)

$2$, $4$, $8$, $16$ 등 $2$의 거듭제곱꼴로 나타나는 $2$ 이상 $2048$ 이하의 값들로 구성된 $4 \times 4$ 격자 판이 주어졌을 때, 특정 방향으로 움직인 이후의 결과를 구하는 프로그램을 작성해보세요.

예를 들어 다음의 경우 오른쪽으로 이동하게 되면, 다음과 같은 결과를 얻게 됩니다.

![](https://contents.codetree.ai/problems/87/images/problems-9c0033d3-e34f-4011-a2fb-d40548d345dd.png)

[예제 1]
입력:
4 2 0 8
4 2 2 4
0 8 8 2
4 2 2 2
R

출력:
0 4 2 8
0 4 4 4
0 0 16 2
0 4 2 4


[예제 2]
입력:
4 2 0 8
4 2 2 4
0 8 8 2
4 2 2 2
L

출력:
4 2 8 0
4 4 4 0
16 2 0 0
4 4 2 0

"""

grid = [list(map(int, input().split())) for _ in range(4)]
direction = input()

N = 4


def merge(line):
    nums = [x for x in line if x != 0]

    result = []
    i = 0

    while i < len(nums):
        if i + 1 < len(nums) and nums[i] == nums[i + 1]:
            result.append(nums[i] * 2)
            i += 2
        else:
            result.append(nums[i])
            i += 1

    result += [0] * (N - len(result))
    return result


new_grid = [[0] * N for _ in range(N)]

if direction == "L":
    for i in range(N):
        new_grid[i] = merge(grid[i])

elif direction == "R":
    for i in range(N):
        line = grid[i][::-1]
        new_grid[i] = merge(line)[::-1]

elif direction == "U":
    for j in range(N):
        line = [grid[i][j] for i in range(N)]
        merged = merge(line)

        for i in range(N):
            new_grid[i][j] = merged[i]

elif direction == "D":
    for j in range(N):
        line = [grid[i][j] for i in range(N - 1, -1, -1)]
        merged = merge(line)

        for i in range(N):
            new_grid[N - 1 - i][j] = merged[i]


for row in new_grid:
    print(*row)
