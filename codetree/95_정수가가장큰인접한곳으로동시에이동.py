"""
CT 95  정수가 가장 큰 인접한 곳으로 동시에 이동
https://www.codetree.ai/ko/trails/complete/curated-cards/intro-move-to-max-adjacent-cell-simultaneously/description

풀이일 : 2026-09-28   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Easy  |  정답률 38.7%
제약   : - $2 \le N \le 20$
제약   : - $1 \le M \le N \times N$
제약   : - $1 \le T \le 100$
제약   : - $1 \le r, c \le N$
제약   : - $1 \le \texttt{grid}_{i, j} \le 100$ ($1 \le i, j \le N$)
제약   : - 모든 구슬의 시작 위치는 서로 다릅니다.

[채점] accepted  2/2  (0.511s)

[문제]
$1$이상 $100$이하의 정수로 이루어진 $N \times N$ 크기의 격자판 정보가 주어집니다. 이때 $M$개 구슬이 서로 다른 위치에서 시작하여 $1$초에 한 번씩 상하좌우로 인접한 곳에 있는 정수들 중 가장 큰 값이 적혀 있는 위치로 동시에 이동합니다. 만약 그러한 위치가 여러 개 있는 경우, 상하좌우 방향 순서대로 우선순위를 매겨 가능한 곳 중 우선순위가 더 높은 곳으로 이동합니다. 단, 이때 격자를 벗어나서는 안 됩니다.

예를 들어, 다음 그림의 경우를 살펴봅시다. 처음에 $3$개의 구슬이 각각 $2$행 $2$열, $3$행 $4$열, $4$행 $2$열에 놓여있었다고 생각해봅시다.

![](https://contents.codetree.ai/problems/95/images/problems-1c49f133-0fe6-4658-b64b-ea8d9bd8ca9a.png)

이 그림에서 $1$초 뒤의 모습은 다음과 같습니다.

![](https://contents.codetree.ai/problems/95/images/problems-984a2bcc-f2f1-4248-b0a4-5b35d2989bb9.png)

이때, 각 구슬이 움직인 이후의 위치가 동일하지 않다면 구슬은 절대 서로 충돌하지 않습니다.

따라서 위의 경우에서 $1$초가 더 흐른 후의 모습은 다음과 같습니다.

![](https://contents.codetree.ai/problems/95/images/problems-74eb9665-428d-4dc9-a5bd-e31fce33bd60.png)

하지만, 이동한 이후 $2$개 이상의 구슬 위치가 동일하다면, 해당 위치에 있는 구슬들은 전부 사라지게 됩니다.

따라서 위의 경우에서 $1$초가 더 흐른 후의 모습은 다음과 같습니다.

![](https://contents.codetree.ai/problems/95/images/problems-e13f64b3-106c-489f-96ed-773646991d4d.png)

격자판의 정보와 초기 구슬들의 위치가 주어졌을 때, $T$초 후 남아 있는 구슬의 수를 출력하는 프로그램을 작성해보세요.

[예제 1]
입력:
4 3 1
1 2 2 3
3 5 10 15
3 8 11 2
4 5 4 4
2 2
3 4
4 2

출력:
3


[예제 2]
입력:
4 3 3
1 2 2 3
3 5 10 15
3 8 11 2
4 5 4 4
2 2
3 4
4 2

출력:
1

"""

N, M, T = map(int, input().split())

# Create n x n grid
arr = [list(map(int, input().split())) for _ in range(N)]

# Get m marble positions
marbles = [tuple(map(int, input().split())) for _ in range(M)]
r = [pos[0] for pos in marbles]
c = [pos[1] for pos in marbles]

# Please write your code here.

DIR = [[-1, 0], [1, 0], [0, -1], [0, 1]]

marbles = dict()

for m in range(M):
    cy = r[m] - 1
    cx = c[m] - 1

    if (cy, cx) not in marbles:
        marbles[(cy, cx)] = 1
    else:
        marbles[(cy, cx)] += 1

for t in range(T):
    new_marbles = dict()
    removed = set()
    for key, value in marbles.items():
        cy, cx = key
        max_val = -1
        next_y = -1
        next_x = -1

        for dy, dx in DIR:
            ny = cy + dy
            nx = cx + dx
            if not (0 <= ny < N and 0 <= nx < N):
                continue
            if arr[ny][nx] > max_val:
                next_y = ny
                next_x = nx
                max_val = arr[ny][nx]

        if next_y != -1:
            key = (next_y, next_x)
            if key not in new_marbles:
                new_marbles[key] = 1
            else:
                new_marbles[key] += 1
            if new_marbles[key] >= 2:
                removed.add(key)
        else:
            key = (cy, cx)
            if key not in new_marbles:
                new_marbles[key] = 1
            else:
                new_marbles[key] += 1
            if new_marbles[key] >= 2:
                removed.add(key)
    for key in removed:
        del new_marbles[key]
    # print(marbles)
    marbles = new_marbles
answer = 0
# print(marbles)
for key, value in marbles.items():
    answer += value
print(answer)
