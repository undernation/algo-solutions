"""
CT 33  네 방향 탈출 가능 여부 판별하기
https://www.codetree.ai/ko/trails/complete/curated-cards/intro-determine-escapableness-with-4-ways/description

풀이일 : 2026-10-05   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Easy  |  정답률 61.4%
제약   : - $2 \le N,\ M \le 100$
제약   : - $A_{ij}$는 $0$ 또는 $1$입니다. $(1 \le i \le N, 1 \le j \le M)$
제약   : - 시작 칸 $(1, 1)$과 끝 칸 $(N, M)$에는 뱀이 주어지지 않습니다.

[채점] accepted  2/2  (0.711s)

[문제]
$N \times M$ 크기의 이차원 영역의 좌측 상단에서 출발하여 우측 하단까지 뱀에게 물리지 않고 탈출하려고 합니다. 이동을 할 때에는 반드시 상하좌우에 인접한 칸으로만 이동할 수 있으며, 뱀이 있는 칸으로는 이동을 할 수 없습니다. 예를 들어 <그림 1>과 같이 뱀이 배치되어 있는 경우 실선과 같은 경로로 탈출을 할 수 있습니다. 이때 뱀에게 물리지 않고 탈출 가능한 경로가 있는지 여부를 판별하는 코드를 작성해보세요.

![](https://contents.codetree.ai/problems/33/images/problems-bf87e555-f698-444a-816c-5683e094439d.png)

[예제 1]
입력:
5 5
1 0 1 1 1
1 0 1 0 1
1 0 1 1 1
1 0 1 0 1
1 1 1 0 1

출력:
1


[예제 2]
입력:
5 5
1 0 1 1 1
1 0 1 0 1
1 1 1 0 1
1 0 1 1 0
0 1 1 0 1

출력:
0

"""

from collections import deque

N, M = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]


# Please write your code here.


def bfs():
    visited = set()
    visited.add((0, 0))
    q = deque()
    q.append((0, 0))

    while q:
        cy, cx = q.popleft()
        for dy, dx in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            ny = cy + dy
            nx = cx + dx

            if not (0 <= ny < N and 0 <= nx < M):
                continue

            if (ny, nx) in visited:
                continue
            if arr[ny][nx] == 0:
                continue

            if ny == N - 1 and nx == M - 1:
                return True

            visited.add((ny, nx))
            q.append((ny, nx))

    return False


if bfs():
    print(1)
else:
    print(0)
