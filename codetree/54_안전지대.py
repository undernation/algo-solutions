"""
CT 54  안전 지대
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-comfort-zone/description

풀이일 : 2026-10-05   결과: 품
한도   : time Python3 7.5초 · C++17 0.5초 / memory 512 MB / time_sec 7.5
난이도 : Medium  |  정답률 35.1%
제약   : - $1 \le N,\ M \le 50$
제약   : - $1 \le \texttt{각 집의 높이} \le 100$

[채점] accepted  2/2  (0.506s)

[문제]
$N \times M$ 크기의 격자로 구성된 마을이 있습니다. 격자마다 한 집을 의미하며, 각 집의 높이는 $1$ 이상 $100$ 이하의 정수입니다.

![](https://contents.codetree.ai/problems/54/images/problems-8e36f981-2e8c-4e44-8cfa-61d1181406a3.png)

이런 상황에서 만약 비가 $K$ ($1$ 이상의 정수)만큼 온다고 한다면, 마을에 있는 집들 중 높이가 $K$ 이하인 집들은 전부 물에 잠기게 되기 때문에, 대책을 세우기 위해 미리 각 $K$에 따라 안전 영역의 개수가 어떻게 달라지는지를 보려고 합니다. 여기서 안전 영역이란 잠기지 않은 집들로 이루어져 있으며, 잠기지 않은 집들끼리 상하좌우로 인접해 있는 경우 동일한 안전 영역에 있는 것으로 봅니다.

위의 예에서 $K = 1$인 경우에는 안전한 영역은 $1$개 입니다.

![](https://contents.codetree.ai/problems/54/images/problems-d5ae4918-c554-4594-bb42-7060fa296818.png)

$K = 3$인 경우에는 안전 영역의 수가 $3$이 되며

![](https://contents.codetree.ai/problems/54/images/problems-c53fe1b9-9f8a-4345-b781-c6dc91bb95b6.png)

$K = 4$일 때는 안전 영역의 수가 $4$가 됩니다.

![](https://contents.codetree.ai/problems/54/images/problems-9312cca1-c78d-410d-ab18-09d1958a1a12.png)


이런 상황에서 안전 영역의 수가 최대가 될 때의 $K$와 그때의 안전 영역의 수를 구해주는 프로그램을 작성해보세요.

위의 예에서는 $K = 4$일 때 안전 영역의 수가 $4$로 최대가 됩니다.

[예제 1]
입력:
4 5
1 2 4 7 5
4 2 5 5 2
5 7 3 2 6
6 7 4 5 1

출력:
4 4


[예제 2]
입력:
3 2
1 2
2 2
1 1

출력:
1 1

"""

import sys
sys.setrecursionlimit(10**6)

N, M = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(N)]

# Please write your code here.

max_K = -1
for i in grid:
    max_K = max(max_K, max(i))


def check(K):
    visited = [[False] * M for _ in range(N)]
    cnt = 0

    def dfs(cy, cx):
        nonlocal cnt, visited
        for dy, dx in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            ny = cy + dy
            nx = cx + dx

            if not (0 <= ny < N and 0 <= nx < M):
                continue
            if visited[ny][nx]:
                continue
            if grid[ny][nx] <= K:
                continue

            visited[ny][nx] = True
            dfs(ny, nx)

    for i in range(N):
        for j in range(M):
            if not visited[i][j] and grid[i][j] > K:
                visited[i][j] = True
                dfs(i, j)
                cnt += 1
    return cnt


cands = []
for k in range(1, max_K + 1):
    safety_val = check(k)
    cands.append([-safety_val, k])

cands.sort()
print(cands[0][1], -cands[0][0])
