"""
CT 116  나이트
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-knight-movements/description

풀이일 : 2026-10-07   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Easy  |  정답률 56.4%
제약   : - $1 \le N \le 100$
제약   : - $1 \le r_1,\ c_1,\ r_2,\ c_2 \le N$

[채점] accepted  2/2  (0.709s)

[문제]
나이트는 다음과 같이 노란색 위치를 기준으로 검은색 $8$곳으로 움직임이 가능합니다. $N \times N$ 격자 위에서 격자를 벗어나지 않고 나이트가 시작점에서 도착점까지 가는 데 걸리는 최소 이동 횟수를 구하는 프로그램을 작성해보세요.

![](https://contents.codetree.ai/problems/116/images/problems-a68e3409-6e4a-44b8-b7bd-b583d6db5aa4.png)

[예제 1]
입력:
5
3 3 3 2

출력:
3


[예제 2]
입력:
3
3 3 1 1

출력:
4

"""

from collections import deque

N = int(input())
r1, c1, r2, c2 = map(int, input().split())

# Please write your code here.

visited = [[-1] * N for _ in range(N)]

r1 -= 1
c1 -= 1
r2 -= 1
c2 -= 1

q = deque()
visited[r1][c1] = 0
q.append((r1, c1))
while q:
    cy, cx = q.popleft()
    for dy, dx in [[-2, -1], [-1, -2], [-2, 1], [-1, 2], [1, -2], [2, -1], [1, 2], [2, 1]]:
        ny = cy + dy
        nx = cx + dx

        if not (0 <= ny < N and 0 <= nx < N):
            continue

        if visited[ny][nx] != -1:
            continue

        visited[ny][nx] = visited[cy][cx] + 1
        q.append((ny, nx))

# for i in visited:
#     print(i)
print(visited[r2][c2])
