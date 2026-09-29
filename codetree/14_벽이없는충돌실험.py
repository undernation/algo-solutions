"""
CT 14  벽이 없는 충돌 실험
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-collision-experiment-without-wall/description

풀이일 : 2026-09-29   결과: 시간초과
한도   : time Python3 3.5초 · C++17 2초 / memory 512 MB / time_sec 3.5
난이도 : Hard  |  정답률 31.7%
제약   : - $1 \le T \le 100$
제약   : - $1 \le N \le 100$
제약   : - $-1000 \le x \le 1000$
제약   : - $-1000 \le y \le 1000$
제약   : - $1 \le w \le 1000$
제약   : - $d \in \{\texttt{U}, \texttt{D}, \texttt{R}, \texttt{L}\}$

[채점] accepted  2/2  (1.272s)

[문제]
$N$개의 구슬이 좌표 평면 위에 놓여져 있습니다. 각 구슬은 무게를 갖고 있습니다

![](https://contents.codetree.ai/problems/14/images/problems-555cd8ba-d2c2-4d82-99db-ea7d793439cf.png)

각 구슬은 모두 $2$초에 한 칸씩 동일한 속도로 정해진 방향으로 움직이고 있습니다.

![](https://contents.codetree.ai/problems/14/images/problems-5fcfeee2-7711-4bcf-8f6b-bdb22ad145f8.png)

진행 도중 두 개 이상의 구슬이 충돌하게 되면 충돌한 구슬 중 영향력이 큰 구슬 하나만 남게 됩니다. 이때 영향력이 크다 함은 무게가 가장 크거나, 무게가 같은 구슬이 여러 개일 경우 구슬의 번호가 가장 클 경우를 의미합니다.

![](https://contents.codetree.ai/problems/14/images/problems-3028de9c-e974-401d-a6e1-b93bce3bedc2.png)

이 때 충돌은 두 구슬이 이동하는 도중에 발생할 수도 있습니다.

예를 들어 다음과 같이 이동 중에 만나는 경우라면, 중간 지점에서 충돌이 일어나게 되어 더 영향력이 큰 구슬만 남게 됩니다.

![](https://contents.codetree.ai/problems/14/images/problems-e028ba32-a2d3-4a4b-955e-0b53478b0da7.png)

다음과 같은 경우라면 $1$초 뒤에 첫 번째 충돌이 일어나고, 그 다음 $1$초 뒤에 다시 두 번째 충돌이 일어나게 됩니다.

![](https://contents.codetree.ai/problems/14/images/problems-7240ab9f-2e43-4fad-bb52-5cde46a306c0.png)

각 구슬의 초기상태가 주어졌을 때, 가장 마지막으로 충돌이 일어난 시간이 언제인지를 출력하는 프로그램을 작성해보세요.

[예제 1]
입력:
2
5
0 1 3 R
1 0 3 U
0 2 6 U
-1 -1 2 R
2 -1 3 U
3
0 0 4 U
0 1 1 R
1 1 2 L

출력:
2
2


[예제 2]
입력:
2
2
-1 -1 1 D
-1 0 1 U
3
1 0 3 U
0 1 3 R
2 -1 3 U

출력:
-1
4

"""

from collections import defaultdict
T = int(input())

directions = {
    "U": (0, 1),
    "D": (0, -1),
    "L": (-1, 0),
    "R": (1, 0)
}

for _ in range(T):
    N = int(input())
    x, y, w, d = [], [], [], []

    for i in range(N):
        xi, yi, wi, di = input().split()
        x.append(int(xi) * 2)
        y.append(int(yi) * 2)
        w.append(int(wi))
        d.append(di)

    # Please write your code here.

    marbles = []

    for cur_id in range(N):
        cur_x = x[cur_id]
        cur_y = y[cur_id]
        cur_w = w[cur_id]
        cur_direction = d[cur_id]

        marbles.append([cur_id, cur_x, cur_y, cur_w, cur_direction])

    last_collision = -1

    def move(cx, cy, cur_direction):

        dx, dy = directions[cur_direction]

        return cx + dx, cy + dy


    for time in range(1, 4001):
        cnt_board = defaultdict(list)
        is_collision = False

        new_marbles = []

        for idx in range(len(marbles)):
            cur_id, cur_x, cur_y, cur_w, cur_direction = marbles[idx]

            nx, ny = move(cur_x, cur_y, cur_direction)
            if not (-2000 <= nx <= 2000 and -2000 <= ny <= 2000):
                continue
            marbles[idx] = [cur_id, nx, ny, cur_w, cur_direction]
            cnt_board[(nx, ny)].append([-cur_w, -cur_id])
        survived = set()
        # 충돌 처리해주기
        for pos, marble_list in cnt_board.items():
            marble_list.sort()
            final_id = -marble_list[0][1]
            survived.add(final_id)
            if len(marble_list) >= 2:
                last_collision = time

        for idx in range(len(marbles)):
            cur_id, cur_x, cur_y, cur_w, cur_direction = marbles[idx]
            if cur_id in survived:
                new_marbles.append([cur_id, cur_x, cur_y, cur_w, cur_direction])

        marbles = new_marbles

    print(last_collision)
