"""
CT 100  단순한 동전 챙기기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-collect-coins-easy/description

풀이일 : 2026-10-03   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 64 MB / time_sec 1
난이도 : Medium  |  정답률 57.7%
제약   : - $2 \le N \le 20$
제약   : - 시작점과 도착점은 각각 정확히 하나씩 주어집니다.
제약   : - 같은 숫자를 지닌 동전은 주어지지 않습니다.

[채점] accepted  2/2  (0.511s)

[문제]
$'.'$ (빈 공간), $'S'$ (시작점), $'E'$ (도착점) 그리고 $1$ 이상 $9$ 이하의 숫자로 이루어진 $N \times N$ 격자 정보가 주어집니다. 숫자가 쓰여 있으면 해당 위치에 동전이 놓여 있음을 뜻하고, 각 숫자는 해당 동전의 번호를 의미합니다. 동전은 해당 위치에 도달해야 얻을 수 있으며, 동전은 각 위치에 최대 하나씩만 놓여 있기 때문에 같은 위치에서 $2$개 이상의 동전을 얻을 수는 없습니다. 이때, 시작점에서 출발하여 적절하게 이동하여 최소 $3$개의 동전을 수집하여 도착점으로 도달하려고 합니다. 동전을 수집할 시에는 꼭 번호가 증가하는 순서대로 수집해야만 합니다. 또, 해당 위치를 지나가더라도 동전을 수집하지 않아도 되며 같은 위치를 $2$번 이상 지나가는 것 역시 허용됩니다.

한 번의 이동은 현재 위치에서 상하좌우로 인접한 칸 중 하나로 이동하는 것을 의미합니다. 격자 안에 있는 모든 칸(빈 공간, 시작점, 도착점, 동전이 놓인 칸)은 자유롭게 지나갈 수 있습니다.

다음 그림을 예로 들어봅시다.

![](https://contents.codetree.ai/problems/100/images/problems-1fefb10b-9719-438d-aac6-928001d401e7.png)

$1 \to 4 \to 5$ 순서로 동전을 주워 도착점으로 가게 되는 경우 최소 $12$번의 이동을 통해 도착점에 도달하게 됩니다.

![](https://contents.codetree.ai/problems/100/images/problems-eb2eec66-f1c3-4a34-b671-2a8936bef7dd.png)

하지만 $1 \to 2 \to 3$ 순서로 동전을 주워 도착점으로 가게 되는 경우 $8$번의 이동만으로도 도착점에 도달할 수 있게 됩니다.

![](https://contents.codetree.ai/problems/100/images/problems-8403c098-6f44-4c46-a95d-b3c567456315.png)

$N \times N$ 크기의 격자 상태가 주어졌을 때 동전의 숫자가 증가하는 순서대로 최소 $3$개의 동전을 수집해 도착지에 도달하기 위해 필요한 최소 이동 횟수를 구하는 프로그램을 작성해보세요.

[예제 1]
입력:
4
..3.
2..E
.1..
5S.4

출력:
8


[예제 2]
입력:
4
..3.
...E
.1..
.S..

출력:
-1

"""

N = int(input())
grid = [list(input()) for _ in range(N)]

# Please write your code here.

numbers = "123456789"
board_dict = dict()
num_list = []
for i in range(N):
    for j in range(N):
        if grid[i][j] == "S":
            board_dict["S"] = (i, j)
        elif grid[i][j] == "E":
            board_dict["E"] = (i, j)
        elif grid[i][j] in numbers:
            board_dict[grid[i][j]] = (i, j)

            num_list.append(grid[i][j])

num_list.sort()

def calc(pos1, pos2):
    y1, x1 = board_dict[pos1]
    y2, x2 = board_dict[pos2]

    return abs(y1 - y2) + abs(x1 - x2)


def calc_dist(num_list):
    dist = 0

    dist += calc("S", num_list[0])
    num_N = len(num_list)

    for idx in range(1, num_N):
        dist += calc(num_list[idx - 1], num_list[idx])

    dist += calc("E", num_list[-1])
    return dist

answer = 10 ** 18
ret = []
def dfs(idx, cnt):
    global answer
    if cnt == 3:
        answer = min(answer, calc_dist(ret))
        return

    if idx == len(num_list):
        return

    ret.append(num_list[idx])
    dfs(idx + 1, cnt + 1)
    ret.pop()

    dfs(idx + 1, cnt)



if len(num_list) < 3:
    print(-1)
else:
    dfs(0, 0)
    print(answer)
