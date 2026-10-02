"""
CT 109  방향에 맞춰 최대로 움직이기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-max-movements-with-direction/description

풀이일 : 2026-10-02   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 79.1%
제약   : - $1 \le N \le 4$
제약   : - $1 \le \texttt{격자 값} \le N \times N$
제약   : - 격자 값은 서로 중복되지 않으며 $1$부터 $N \times N$까지의 정수가 모두 정확히 한 번씩 등장합니다.
제약   : - $1 \le \texttt{방향 값} \le 8$
제약   : - $1 \le r,\ c \le N$

[채점] accepted  2/2  (0.602s)

[문제]
각 칸이 $1$이상 $N \times N$이하의 정수와 여덟 방향 중 한 방향으로 이루어진 $N \times N$ 크기의 격자가 주어집니다.

수는 중복없이 단 한 번씩만 주어지며, 방향은 아래 그림에서 왼쪽에 적혀있는대로 여덟 방향 중 하나입니다.

![](https://contents.codetree.ai/problems/109/images/problems-4a09fb46-0386-4147-a568-037b95226a36.png)

이때 특정 위치에서 시작하여 현재 위치에 적혀있는 방향에 있는 수들 중 현재 수보다 더 큰 수가 적혀있는 곳으로 이동하는 것을 최대한 많이 반복해보려고 합니다.

아래 그림을 살펴봅시다. 이 경우는 $N = 3$이고, 시작 위치가 $3$행 $3$열인 예입니다.

![](https://contents.codetree.ai/problems/109/images/problems-c4890366-03cb-4f04-bb30-1698aa243cf6.png)

$5$에서는 $5$보다 크면서 해당 방향에 있는 수 $6, 7$에 모두 갈 수 있습니다.

$6$으로 이동하게 될 경우에는 더 이상 조건을 만족하며 움직일 수 없게 됩니다.

하지만 $7$로 이동하게 된 경우, 조건을 만족하며 $9$로 이동이 가능하기 때문에 $5$에서 시작하여 총 $2$번 이동이 가능하게 됩니다.

$N \times N$ 격자의 초기 상태가 주어졌을 때, 시작 위치로부터 조건을 만족하며 최대 몇 번 이동할 수 있는지를 구하는 프로그램을 작성해보세요.

[예제 1]
입력:
3
7 1 4
2 6 3
9 8 5
5 3 1
6 3 7
2 4 8
3 3

출력:
2


[예제 2]
입력:
3
2 8 9
6 4 5
3 7 1
5 3 1
6 3 7
2 4 8
3 3

출력:
5

"""

N = int(input())
num = [list(map(int, input().split())) for _ in range(N)]
move_dir = [list(map(int, input().split())) for _ in range(N)]
R, C = map(int, input().split())

# Please write your code here.
dir_dict = {
    1: (-1, 0),
    2: (-1, 1),
    3: (0, 1),
    4: (1, 1),
    5: (1, 0),
    6: (1, -1),
    7: (0, -1),
    8: (-1, -1)

}


# 다음거 확인하고 넘어가기....

# 목록 찾기 그리고 백트래킹
answer = 0
def dfs(idx, sy, sx, cd):
    # 더 갈수있는 곳 없으면 리턴해주기
    global answer
    answer = max(answer, idx)
    cands = []

    cy = sy
    cx = sx
    cur_num = num[cy][cx]
    dy, dx = dir_dict[cd]

    while True:
        # print("wow")
        ny = cy + dy
        nx = cx + dx
        if not (0 <= ny < N and 0 <= nx < N):
            break

        if num[ny][nx] < cur_num:
            cy = ny
            cx = nx
            continue
        cands.append([ny, nx])
        cy = ny
        cx = nx

    if len(cands) == 0:
        return

    for ny, nx in cands:
        nd = move_dir[ny][nx]
        dfs(idx + 1, ny, nx, nd)


    return

dfs(0, R - 1, C - 1, move_dir[R - 1][C - 1])
print(answer)
