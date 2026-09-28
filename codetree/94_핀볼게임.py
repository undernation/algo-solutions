"""
CT 94  핀볼게임
https://www.codetree.ai/ko/trails/complete/curated-cards/test-pinball-game/description

풀이일 : 2026-09-28   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 43.4%
제약   : - $1 \le N \le 100$
제약   : - $\texttt{격자 값} \in \{0, 1, 2\}$

[채점] accepted  2/2  (0.507s)

[문제]
$0, 1, 2$ 수들로만 이루어진 $N \times N$ 크기의 격자판에서 핀볼 게임을 진행해보려고 합니다. $0$은 빈 공간을, $1$은 / 모양을, $2$는 \ 모양을 의미합니다. 값이 $1$이나 $2$일 경우 구슬이 해당 위치로 진입했을 때, 바에 부딪혀 진행방향이 바뀌게 되며, 진행하던 구슬이 격자 밖으로 나가게 되면 게임이 끝나게 됩니다. 구슬이 한 칸 움직이는 데는 $1$초의 시간이 소요되며, 격자 안으로 들어가는 시간과 격자 밖으로 나오는 시간까지 포함하여 계산합니다.

![](https://contents.codetree.ai/problems/94/images/problems-2503aeed-ab8f-4f58-b16e-a7be7e5cebcc.png)

구슬은 단 하나만 이용하며, 다음과 같이 $4 \times N$개의 지점 중 한 곳에서 정해진 방향으로만 시작이 가능합니다.

![](https://contents.codetree.ai/problems/94/images/problems-7e5a2987-92dd-4cd6-9fa8-89af41b7a626.png)

만약 구슬을 다음 위치에 두고 게임을 시작하게 된다면, $8$초 후 격자 밖으로 나오게 됩니다.

![](https://contents.codetree.ai/problems/94/images/problems-6eeb1500-554f-4e5e-b0ce-d53221ea6043.png)

하지만 다음 위치에서 시작을 하면, $10$초 후 격자 밖으로 나오게 됩니다.

![](https://contents.codetree.ai/problems/94/images/problems-3aff787b-6911-4640-9a33-7152b235fee7.png)

격자판의 상태가 주어졌을 때, 시작점을 적절하게 선택하여 격자 밖으로 나오는 데까지 걸리는 시간이 최대가 되도록 하는 프로그램을 작성해보세요.

[예제 1]
입력:
5
0 0 0 0 0
0 0 0 0 0
1 0 1 0 2
0 0 0 0 0
0 0 1 0 2

출력:
10


[예제 2]
입력:
5
1 1 1 1 1
1 1 1 1 1
1 1 1 1 1
1 1 1 1 1
1 1 1 1 1

출력:
10

"""

N = int(input())
grid = [list(map(int, input().split())) for _ in range(N)]

# Please write your code here.

DIR = [[1, 0], [-1, 0], [0, 1], [0, -1]]

one_dict = {
    3: 0,
    2: 1,
    1: 2,
    0: 3
}
two_dict = {
    3: 1,
    2: 0,
    1: 3,
    0: 2
}

answer = 0


def simulation(sy, sx, sd):
    time = 1
    cy, cx, cd = sy, sx, sd

    while True:
        if not (0 <= cy < N and 0 <= cx < N):
            return time
        # print(cy, cx)
        if grid[cy][cx] == 0:
            nd = cd
            pass
        elif grid[cy][cx] == 1:
            nd = one_dict[cd]
        else:
            nd = two_dict[cd]

        dy, dx = DIR[nd]
        ny = cy + dy
        nx = cx + dx

        cy = ny
        cx = nx
        cd = nd
        time += 1
# i = 4
# j = 0
# answer = max(answer, simulation(i, j, 2))
for j in range(N):
    i = 0
    answer = max(answer, simulation(i, j, 0))

    i = N - 1
    answer = max(answer, simulation(i, j, 1))

for i in range(N):
    j = 0
    answer = max(answer, simulation(i, j, 2))

    j = N - 1
    answer = max(answer, simulation(i, j, 3))
print(answer)
