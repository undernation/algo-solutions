"""
CT 90  정수가 더 큰 인접한 곳으로 이동
https://www.codetree.ai/ko/trails/complete/curated-cards/intro-move-to-larger-adjacent-cell/description

풀이일 : 2026-09-27   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 64 MB / time_sec 1
난이도 : Easy  |  정답률 60.6%
제약   : - $1 \le N \le 100$
제약   : - $1 \le r, c \le N$
제약   : - $1 \le \texttt{grid}_{i, j} \le 100$ ($1 \le i, j \le N$)

[채점] accepted  2/2  (0.51s)

[문제]
$1$이상 $100$이하의 정수로 이루어진 $N \times N$ 크기의 격자판 정보가 주어집니다. 이때 특정 위치에서 시작하여, 상하좌우로 인접한 곳에 있는 정수들 중 현재 위치에 있는 정수보다 더 큰 위치로 끊임없이 이동합니다. 만약 그러한 위치가 여러 개 있는 경우, 상하좌우 방향 순서대로 우선순위를 매겨 가능한 곳 중 우선순위가 더 높은 곳으로 이동합니다. 격자를 벗어나서는 안 되며, 더 이상 움직일 수 없을 때까지 반복합니다.

위의 규칙에 따라 방문하게 되는 위치에 적힌 정수를 순서대로 출력하는 프로그램을 작성해보세요.

예를 들어, 다음 그림의 경우를 살펴봅시다.

![](https://contents.codetree.ai/problems/90/images/problems-30369111-eb5a-459f-a447-05a9e9c8245b.png)

상하좌우 인접한 정수들 중 $5$보다 큰 정수는 $8$과 $10$ $2$개가 있지만, 아래 방향이 우선순위가 더 높으므로 정수 $8$이 있는 위치로 이동하게 됩니다.

![](https://contents.codetree.ai/problems/90/images/problems-a1d68086-8be4-4e55-93fb-8dd96cb67cfe.png)

$8$ 위치에서는 오른쪽 방향으로만 이동이 가능하므로 정수 $11$이 적혀 있는 위치로 이동하게 됩니다.

![](https://contents.codetree.ai/problems/90/images/problems-5fcc1ed9-ec4b-4a47-aaa3-4971c381bc8f.png)

이때는 $11$보다 큰 정수가 인접한 곳에 없으므로 이동을 멈추게 됩니다.

[예제 1]
입력:
4 2 2
1 2 2 3
3 5 10 15
3 8 11 2
4 5 4 4

출력:
5 8 11


[예제 2]
입력:
4 1 1
1 2 2 3
3 5 10 15
3 8 11 2
4 5 4 4

출력:
1 3 5 8 11

"""

N, R, C = map(int, input().split())
arr = [[0] * (N + 1) for _ in range(N + 1)]

for i in range(1, N + 1):
    row = list(map(int, input().split()))
    for j in range(1, N + 1):
        arr[i][j] = row[j - 1]

# Please write your code here.
answer = []

DIR = [[-1, 0], [1, 0], [0, -1], [0, 1]]

def move(cy, cx):
    cur_num = arr[cy][cx]
    max_num = -1
    next_y = -1
    next_x = -1

    for dy, dx in DIR:
        ny = cy + dy
        nx = cx + dx
        if not (1 <= ny < N + 1 and 1 <= nx < N + 1):
            continue
        if arr[ny][nx] > cur_num and arr[ny][nx] > max_num:
            max_num = arr[ny][nx]
            next_y = ny
            next_x = nx
            break

    return max_num, next_y, next_x
cy = R
cx = C
answer.append(arr[cy][cx])
while True:
    max_num, ny, nx = move(cy, cx)
    if max_num == -1:
        break
    answer.append(max_num)
    cy = ny
    cx = nx

print(*answer)
