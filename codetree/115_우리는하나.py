"""
CT 115  우리는 하나
https://www.codetree.ai/ko/trails/complete/curated-cards/test-we-are-the-one/description

풀이일 : 2026-10-06   결과: 품
한도   : time Python3 4초 · C++17 1초 / memory 192 MB / time_sec 4
난이도 : Medium  |  정답률 58.7%
제약   : - $1 \le N \le 8$
제약   : - $1 \le K \le \min(N,\ 3)$
제약   : - $0 \le U \le D \le 100$
제약   : - $1 \le \texttt{입력으로 주어지는 정수} \le 100$

[채점] accepted  3/3  (1.065s)

[문제]
$N \times N$ 크기의 격자로 이루어져 있는 나라의 정보가 주어집니다. 각 칸마다 하나의 도시가 있고, 각 도시마다의 높이 정보가 주어집니다. 이때 $K$개의 도시를 겹치지 않게 적절하게 골라, 골라진 $K$개의 도시로부터 갈 수 있는 서로 다른 도시의 수를 최대화 하고자 합니다. 이때 이동은 상하좌우로 인접한 도시간의 이동만 가능하며, 그 중에서도 두 도시간의 높이의 차가 $U$ 이상 $D$ 이하인 경우에만 가능합니다.

$K$개의 도시를 적절하게 골라 갈 수 있는 서로 다른 도시의 수를 최대로 하는 프로그램을 작성해보세요. (시작 도시를 포함하여 셉니다)

[예제 1]
입력:
3 1 2 3
1 2 3
2 4 5
2 1 5

출력:
4


[예제 2]
입력:
3 2 2 3
1 2 3
2 4 5
2 1 5

출력:
6


[예제 3]
입력:
3 1 2 3
1 3 5
3 5 7
5 7 9

출력:
9

"""

from itertools import combinations
from collections import deque
N, K, U, D = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(N)]

# Please write your code here.


cities = [i for i in range(N * N)]
# print(cities)


def decoder(num):
    return num // N, num % N

def encoder(cy, cx):
    return cy * N + cx

answer = 0

for combi in combinations(cities, K):

    visited = set()
    q = deque()

    for i in combi:
        cy, cx = decoder(i)
        visited.add((cy, cx))
        q.append((cy, cx))

    while q:
        cy, cx = q.popleft()

        for dy, dx in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            ny = cy + dy
            nx = cx + dx
            if not (0 <= ny < N and 0 <= nx < N):
                continue

            if (ny, nx) in visited:
                continue

            cur_num = grid[cy][cx]
            nxt_num = grid[ny][nx]

            if U <= abs(cur_num - nxt_num) <= D:
                q.append((ny, nx))
                visited.add((ny, nx))
    answer = max(answer, len(visited))

print(answer)
