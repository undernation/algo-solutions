"""
CT 13  벽이 있는 충돌 실험
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-collision-experiment-with-wall/description

풀이일 : 2026-10-01   결과: 못품
한도   : time Python3 7초 · C++17 1초 / memory 128 MB / time_sec 7
난이도 : Medium  |  정답률 36.6%
제약   : - $1 \le T \le 100$
제약   : - $1 \le N \le 50$
제약   : - $0 \le M \le N \times N$
제약   : - $1 \le x \le N$
제약   : - $1  \le y \le N$
제약   : - 처음부터 구슬이 겹쳐져 주어지는 경우는 없다고 가정해도 좋습니다.

[문제]
$M$개의 구슬이 $N \times N$ 격자 안에 놓여져 있고, 격자는 벽으로 둘러싸여 있습니다.

![](https://contents.codetree.ai/problems/13/images/problems-8bd32285-4723-42d5-a01d-861de1e5f22c.png)

각 구슬은 모두 $1$초에 한 칸씩 동일한 속도로 정해진 방향으로 움직이고 있습니다.

![](https://contents.codetree.ai/problems/13/images/problems-705bcdf1-a7bd-42f7-874a-42c31ee0c00e.png)

구슬이 벽에 부딪히면 움직이지 않고 움직이는 방향만 반대로 뒤집힙니다. 이때 방향을 바꾸는 작업에는 $1$초의 시간이 소요됩니다.

![](https://contents.codetree.ai/problems/13/images/problems-a7c03cea-6f85-4ae6-8ace-facdcdc8e7dd.png)

두 개 이상의 구슬이 충돌하게 되면 부딪힌 구슬 모두 사라지게 됩니다.

![](https://contents.codetree.ai/problems/13/images/problems-be79233b-ff95-4c10-aa32-f6fd205ba953.png)

이 때 충돌은 두 구슬이 이동 후 같은 위치에 있는 경우에만 일어납니다. 

예를 들어 다음과 같이 이동 중에 만나는 경우라면, 서로 충돌이 일어나지 않습니다.

![](https://contents.codetree.ai/problems/13/images/problems-fcbc7b33-66ba-4270-b49d-268d7ab69c31.png)

각 구슬의 초기상태가 주어졌을 때, 아주 오랜시간이 흐른 후에도 여전히 격자 안에 남아있는 구슬의 개수를 출력하는 프로그램을 작성해보세요.

[예제 1]
입력:
1
4 5
1 2 L
2 3 U
3 1 R
3 4 D
4 2 U

출력:
1


[예제 2]
입력:
3
2 2
1 1 L
2 2 R
2 2
1 1 D
2 2 R
2 2
1 1 L
1 2 R

출력:
2
0
2

"""

T = int(input())

DIR_DICT = {
    "U": [-1, 0],
    "D": [1, 0],
    "R": [0, 1],
    "L": [0, -1]
}

reverse_dict = {
    "U": "D",
    "D": "U",
    "R": "L",
    "L": "R"
}

for _ in range(T):
    N, M = map(int, input().split())
    x_list, y_list, d = [], [], []
    for _ in range(M):
        xi, yi, di = input().split()
        x_list.append(int(xi))
        y_list.append(int(yi))
        d.append(di)

    # Please write your code here.

    marbles = []
    for m in range(M):
        y = x_list[m] - 1
        x = y_list[m] - 1
        direction = d[m]

        marbles.append((y, x, direction))

    for time in range(2 * N):
        cnt_board = dict()
        new_marbles = []

        for cy, cx, cd in marbles:

            dy, dx = DIR_DICT[cd]
            # 이동 처리

            ny = cy + dy
            nx = cx + dx

            if not (0 <= ny < N and 0 <= nx < N):
                ny = cy
                nx = cx
                nd = reverse_dict[cd]
            else:
                nd = cd

            key = (ny, nx)
            if key not in cnt_board:
                cnt_board[key] = 1
            else:
                cnt_board[key] += 1
            new_marbles.append((ny, nx, nd))

        # 2. 충돌 제거
        marbles = [
            (y, x, d)
            for y, x, d in new_marbles
            if cnt_board[(y, x)] == 1
        ]
    print(len(marbles))
