"""
CT 99  합쳐지는 구슬들
https://www.codetree.ai/ko/trails/complete/curated-cards/test-merge-marbles/description

풀이일 : 2026-09-29   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 48.0%
제약   : - $1 \le N \le 50$
제약   : - $1 \le M \le N \times N$
제약   : - $1 \le T \le 100$
제약   : - $1 \le r, c \le N$
제약   : - $1 \le w \le 100$
제약   : - $d \in \{\text{'U'}, \text{'D'}, \text{'R'}, \text{'L'}\}$

[채점] accepted  2/2  (0.687s)

[문제]
$M$개의 구슬이 $N \times N$ 격자 안에 놓여져 있고, 격자는 벽으로 둘러싸여 있습니다. 각 구슬은 상하좌우 중 한 방향으로 이동하고 $1$초에 한 칸씩 움직입니다. 각 구슬에는 번호가 매겨져 있고, 구슬마다의 무게가 주어져 있습니다. 아래 그림에서 하얀색으로 적혀 있는 숫자는 무게를 의미합니다.

![](https://contents.codetree.ai/problems/99/images/problems-d87e3a70-a2b4-438a-b7ca-31e635a88aee.png)

구슬이 벽에 부딪히면 움직이는 방향이 반대로 뒤집혀 동일한 속도로 움직이는 것을 반복합니다. 이때 방향을 바꾸는 데 역시 $1$초의 시간이 소요됩니다.

![](https://contents.codetree.ai/problems/99/images/problems-979003ee-63cf-4f50-be7d-1cfc9e816193.png)

또, 아래처럼 칸에서 충돌하는 게 아닌 경우는 충돌로 간주하지 않음에 유의합니다.
![](https://contents.codetree.ai/problems/99/images/problems-4f012709-aebb-411d-9a52-624b8574ce29.png)

하지만 만약 $1$초의 시간이 지난 후 두 개 이상의 구슬이 같은 위치로 오게 된다면 이는 충돌이 발생하게 되고, 충돌이 일어나면 해당 위치에 있던 구슬들은 전부 합쳐지게 됩니다. 이 구슬들이 합쳐지게 되면 하나의 구슬이 만들어지게 되고, 이 구슬의 무게는 해당 위치에 모인 모든 구슬의 합으로 결정되고, 방향은 합쳐진 구슬들 중 가장 큰 번호가 매겨져 있는 구슬의 방향을 따르게 되고, 번호는 마찬가지로 충돌이 일어난 구슬들 중 가장 큰 번호를 갖게 됩니다.

예를 들어 다음의 경우에 $1$초의 시간이 흐르게 되면 무게 $8$을 갖고 번호가 $4$인 구슬이 오른쪽 방향으로 움직이게 됩니다.

![](https://contents.codetree.ai/problems/99/images/problems-53a025ac-3c47-4ab3-bf1d-f5b129d204bd.png)


처음 주어진 그림을 예로 $1$초 뒤의 모습을 그려보면 다음과 같습니다.

![](https://contents.codetree.ai/problems/99/images/problems-ac3b9aa6-e7cf-4604-9ab8-3448b35c844d.png)

그리고 다시 $1$초 뒤의 모습을 그려보면 다음과 같습니다.

![](https://contents.codetree.ai/problems/99/images/problems-e5389410-4e2f-479c-a6c0-0170a02c17b9.png)

각 구슬의 초기상태가 주어졌을 때, $T$초가 지난 이후에도 여전히 격자 안에 남아 있는 구슬의 개수와 가장 무거운 구슬의 무게를 출력하는 프로그램을 작성해보세요.

[예제 1]
입력:
4 5 2
1 2 L 5
2 3 U 2
3 1 R 2
4 2 U 3
3 4 D 5

출력:
4 5


[예제 2]
입력:
4 5 3
1 2 L 5
2 3 U 2
3 1 R 2
4 2 U 3
3 4 D 5

출력:
3 10

"""

from collections import defaultdict

N, M, T = map(int, input().split())

r = []
c = []
d = []
w = []

for _ in range(M):
    ri, ci, di, wi = input().split()
    r.append(int(ri))
    c.append(int(ci))
    d.append(di)
    w.append(int(wi))

# Please write your code here.

marbles = dict()

for cur_id in range(M):
    cur_y = r[cur_id] - 1
    cur_x = c[cur_id] - 1
    cur_direction = d[cur_id]
    cur_weight = w[cur_id]

    marbles[cur_id] = [cur_y, cur_x, cur_direction, cur_weight]

directions = {
    "L": (0, -1),
    "R": (0, 1),
    "U": (-1, 0),
    "D": (1, 0)
}

reverse_direction = {
    "R": "L",
    "L": "R",
    "U": "D",
    "D": "U"
}


def move(cy, cx, direction):
    dy, dx = directions[direction]
    return cy + dy, cx + dx


for time in range(T):
    # 구슬 이동 해주기
    new_marbles = dict()
    board = defaultdict(list)
    # print("debug", marbles)
    for marble_id, marble_info in marbles.items():
        cur_y, cur_x, cur_direction, cur_weight = marble_info

        ny, nx = move(cur_y, cur_x, cur_direction)
        # 벗어나면 위치는 그대로 두고 방향만 바꿔주기
        if not (0 <= ny < N and 0 <= nx < N):
            ny = cur_y
            nx = cur_x
            marble_info[2] = reverse_direction[cur_direction]
        board[(ny, nx)].append(marble_id)

    # 구슬 합치기
    for pos, marble_list in board.items():
        max_id = -1
        max_direction = -1

        total_size = 0
        for marble_id in marble_list:
            cur_y, cur_x, cur_direction, cur_weight = marbles[marble_id]
            total_size += cur_weight
            if max_id < marble_id:
                max_id = marble_id
                max_direction = cur_direction
        cy, cx = pos
        new_marbles[max_id] = [cy, cx, max_direction, total_size]

    marbles = new_marbles
max_weight = 0
cnt = 0
for marble_id, marble_info in marbles.items():
    cnt += 1
    [cy, cx, max_direction, total_size] = marble_info
    max_weight = max(max_weight, total_size)

print(cnt, max_weight)
