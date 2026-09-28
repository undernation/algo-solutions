"""
CT 96  수의 순차적 이동
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-sequential-movement-of-numbers/description

풀이일 : 2026-09-28   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Easy  |  정답률 83.2%
제약   : - $2 \le N \le 20$
제약   : - $1 \le M \le 100$
제약   : - $1$ 이상 $N \times N$ 이하의 수가 정확히 한 번씩만 나온다고 가정해도 좋습니다.

[채점] accepted  2/2  (0.507s)

[문제]
$1$이상 $N \times N$이하의 수들이 정확히 한번씩만 등장하는 $N \times N$ 크기의 격자판 정보가 주어집니다. 이때 $M$번의 턴에 걸쳐 수들을 이동하려고 합니다. 한 번의 턴에는 수 $1$이 적힌 위치에서부터 수 $N \times N$이 적힌 위치까지 순서대로 하나씩 보면서 특정 조건에 맞춰 다들 한번씩 움직입니다. 이 조건이란, 각 위치에서 여덟방향으로 인접한 칸들 중 가장 큰 수와 가운데 칸의 수를 교환하는 것입니다. 여덟방향으로 인접한 위치란, 예를 들어 아래 그림에서 노란색 위치를 기준으로 회색 위치를 의미합니다.

![](https://contents.codetree.ai/problems/96/images/problems-2f12c85d-228d-48cc-a2a8-c650c35c1fc5.png)

아래 그림을 살펴봅시다.

![](https://contents.codetree.ai/problems/96/images/problems-8c7b120d-7448-4890-a927-cc64804bb2e3.png)

첫 번째 턴에 대해 다음 과정을 밟게 됩니다.

먼저 수 $1$부터 시작합니다. 이 경우 여덟방향으로 인접한 수들 중 가장 큰 값인 $13$과 위치를 바꾸게 됩니다.

![](https://contents.codetree.ai/problems/96/images/problems-f9333e7b-1a61-460b-9172-84f6f1ec9b9e.png)

그 다음 수 $2$를 움직입니다. 이 경우 여덟방향으로 인접한 수들 중 가장 큰 값인 $14$와 위치를 바꾸게 됩니다.

![](https://contents.codetree.ai/problems/96/images/problems-cc9c1082-8527-4bbb-9bed-c8c7888e68fc.png)

이 과정을 순차적으로 수 $16$까지 각각 한번씩 반복하게 되면, 결과는 다음과 같이 나오게 되며 이 과정을 거친 것을 한 번의 턴 이라고 부릅니다.

![](https://contents.codetree.ai/problems/96/images/problems-b33bf0f2-b541-4ad8-8d9f-cba186c9a84a.png)

$M$번의 턴을 거친 이후 격자판의 상태를 출력하는 프로그램을 작성해보세요.

[예제 1]
입력:
4 1
15 13 1 11
4 8 3 5
2 12 16 7
14 6 9 10

출력:
4 1 13 11
8 12 5 7
6 15 3 9
2 14 16 10


[예제 2]
입력:
4 2
15 13 1 11
4 8 3 5
2 12 16 7
14 6 9 10

출력:
13 4 1 9
12 15 7 11
14 2 5 16
6 8 3 10

"""

N, M = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(N)]


# Please write your code here.

def switch(cy, cx):
    cur_num = grid[cy][cx]

    max_val = 0
    max_y = -1
    max_x = -1

    for dy, dx in [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]:
        ny = cy + dy
        nx = cx + dx
        if not (0 <= ny < N and 0 <= nx < N):
            continue
        if grid[ny][nx] > max_val:
            max_val = grid[ny][nx]
            max_y = ny
            max_x = nx

    grid[cy][cx] = max_val
    grid[max_y][max_x] = cur_num

for m in range(M):
    for num in range(1, N * N + 1):
        cur_num = num
        is_change = False
        for i in range(N):
            for j in range(N):
                if grid[i][j] == cur_num:
                    switch(i, j)
                    is_change = True
                    break
            if is_change:
                break
                

for i in grid:
    print(*i)
