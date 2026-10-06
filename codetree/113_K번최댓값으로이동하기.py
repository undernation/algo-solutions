"""
CT 113  K번 최댓값으로 이동하기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-move-to-max-k-times/description

풀이일 : 2026-10-06   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 56.7%
제약   : - $1 \le N,\ K \le 100$
제약   : - $1 \le \texttt{격자 값} \le 100$
제약   : - $1 \le r,\ c \le N$

[채점] accepted  2/2  (0.759s)

[문제]
각 칸이 $1$ 이상 $100$ 이하의 정수로 이루어진 $N \times N$ 크기의 격자가 주어져 있습니다.

이때 특정 위치에서 시작하여 아래 조건을 만족하는 위치를 찾아 상하좌우로만 이동한다고 합니다.

이렇게 이동하는 것을 $K$번 반복한 이후의 위치를 구하는 프로그램을 작성해보세요.

만약 아직 $K$번을 반복하지 못했지만, 더 이상 새로 이동할 위치가 없다면 움직이는 것을 종료합니다.

이동하기 위한 조건은 다음과 같습니다.

1. 시작 위치에 적혀있는 정수를 $x$라고 했을 때, 시작 위치에서 출발하여 상하좌우로만 이동하되, 이동 경로 상의 모든 칸에 적힌 정수가 $x$보다 작아야 합니다. 이렇게 도달할 수 있는 모든 칸을 이동 가능한 칸으로 정의합니다.

  다음 그림을 예로 들어보겠습니다. 시작 위치가 $4$행 $3$열이고 이 칸에 적힌 정수가 $10$이라고 했을 때, $10$보다 큰 $11$을 제외한 인접한 모든 칸으로 이동이 가능합니다.

![](https://contents.codetree.ai/problems/113/images/problems-776c85b6-f174-423e-93c7-b072216c2f17.png)

  1-1. 하지만 만약에 아래 그림처럼 시작 위치의 상하좌우가 시작 위치의 정수($= 10$)보다 큰 정수들($= 11$)로 둘러싸여 있으면 이동이 불가합니다.

  ![](https://contents.codetree.ai/problems/113/images/problems-f4834838-855d-4719-9092-a9ac4ea08e2e.png)

2. $1$번 조건을 만족하며 도달할 수 있는 칸들에 적혀있는 정수 중 최댓값으로 이동합니다.

![](https://contents.codetree.ai/problems/113/images/problems-51d233e3-6326-4139-adea-d598768f9943.png)

 위 그림과 같이 시작 위치에 적혀있는 정수 $10$에서 출발하여 도달 가능한 칸들 중 $10$보다 작지만 그 중 최댓값인 $9$로 이동을 고려합니다.

3. $2$번 조건을 만족하는 위치가 여러 개일 경우, 행 번호가 가장 작은 곳으로 이동합니다. 아래 그림과 같이 $2$행에 있는 최댓값($= 9$)이 두 개 있습니다.

![](https://contents.codetree.ai/problems/113/images/problems-fe37dfb3-7e22-43e3-81cc-0fda743edf94.png)

4. $2$번 조건을 만족하고, 행 번호도 같은 위치가 여러 개일 경우, 열 번호가 가장 작은 곳으로 이동합니다.

![](https://contents.codetree.ai/problems/113/images/problems-af51f634-c9a3-4140-96c6-0febc73c0c47.png)

결론적으로 $4$행 $3$열에서 시작하여 인접한 칸을 따라 $10$보다 작은 곳들로 이동했을 때 갈 수 있는 칸들 중 최댓값은 $9$이고, 그 중 우선순위가 가장 높은 곳은 $2$행 $2$열입니다. 따라서 $2$행 $2$열 위치로 이동하게 됩니다.

$2$행 $2$열 위치를 시작으로 한번 더 움직임을 반복해보면, $2$행 $2$열에서 시작하여 인접한 칸을 따라 $9$보다 작은 곳들로 이동했을 때 갈 수 있는 칸들 중 최댓값은 $6$이고, 그 중 우선순위가 가장 높은 곳은 $2$행 $3$열입니다. 따라서 $2$행 $3$열 위치로 이동하게 됩니다.

![](https://contents.codetree.ai/problems/113/images/problems-033ec049-fe7b-43bc-93fa-793cfbc96bc5.png)

$2$행 $3$열 위치를 시작으로 한번 더 움직임을 반복해보면, $2$행 $3$열에서 시작하여 인접한 칸을 따라 $6$보다 작은 곳들로 이동했을 때 갈 수 있는 칸들 중 최댓값은 $4$이고, $4$는 $2$행 $1$열에 있습니다. 따라서 $2$행 $1$열 위치로 이동하게 됩니다.

![](https://contents.codetree.ai/problems/113/images/problems-0962e095-9179-4632-a6b4-9cc501f75774.png)

이렇게 이동하는 것을 $K$번 반복한 후의 위치를 구하는 프로그램을 작성해보세요. 아직 $K$번을 반복하지 못했더라도, 더 이상 새로 이동할 위치가 없다면 움직이는 것을 종료해야함에 유의합니다.

[예제 1]
입력:
4 2
1 3 2 11
4 9 6 9
2 6 9 8
1 9 10 7
4 3

출력:
2 3


[예제 2]
입력:
4 4
1 3 2 11
4 9 6 9
2 6 9 8
1 9 10 7
4 3

출력:
1 2

"""

from collections import deque

N, K = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(N)]
r, c = map(int, input().split())


# Please write your code here.

def move(sy, sx):
    start_num = grid[sy][sx]
    cands = []

    visited = set()

    q = deque()

    visited.add((sy, sx))
    q.append((sy, sx))

    while q:
        cy, cx = q.popleft()

        for dy, dx in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            ny = cy + dy
            nx = cx + dx

            if not (0 <= ny < N and 0 <= nx < N):
                continue
            if (ny, nx) in visited:
                continue

            if grid[ny][nx] >= start_num:
                continue

            visited.add((ny, nx))
            q.append((ny, nx))
            cands.append((-grid[ny][nx], ny, nx))
    # print("debug", cands)
    cands.sort()
    if len(cands) >= 1:

        return cands[0][1], cands[0][2]
    else:
        return sy, sx


cy, cx = r - 1, c - 1
for k in range(K):
    ny, nx = move(cy, cx)
    cy = ny
    cx = nx

print(cy + 1, cx + 1)
