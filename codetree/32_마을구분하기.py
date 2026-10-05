"""
CT 32  마을 구분하기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-seperate-village/description

풀이일 : 2026-10-05   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 192 MB / time_sec 1
난이도 : Medium  |  정답률 78.6%
제약   : - $5 \le N \le 25$
제약   : - 격자의 각 칸 값은 $0$ 또는 $1$입니다. $(1 \le i,\ j \le N)$

[채점] accepted  2/2  (0.509s)

[문제]
$N \times N$크기의 이차원 영역에 사람 혹은 벽이 놓여 있습니다. 이때 상하좌우의 인접한 영역에 있는 사람들은 같은 마을에 있는 것으로 간주한다고 합니다. 예를 들어 그림과 같이 사람과 벽이 배치되어 있는 경우, 그림 안의 점선과 같이 마을을 나눌 수 있습니다. 이때 총 마을의 개수와 같은 마을에 있는 사람의 수를 오름차순으로 정렬하여 출력하는 코드를 작성합니다.

![](https://contents.codetree.ai/problems/32/images/problems-9bdd3983-b029-4be7-b2cc-2ad504f27272.png)

[예제 1]
입력:
5
1 0 1 1 1
1 0 0 0 0
0 0 0 1 1
1 1 0 1 1
1 1 0 1 1

출력:
4
2
3
4
6


[예제 2]
입력:
5
0 1 0 0 1
0 1 0 1 1
0 1 0 0 1
0 1 1 1 1
1 0 0 0 0

출력:
2
1
11

"""

N = int(input())
grid = [list(map(int, input().split())) for _ in range(N)]

# Please write your code here.
visited = [[False] * N for _ in range(N)]
people_list = []

def dfs(cy, cx):
    global cnt, visited
    for dy, dx in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
        ny = cy + dy
        nx = cx + dx

        if not (0 <= ny < N and 0 <= nx < N):
            continue

        if grid[ny][nx] == 0:
            continue

        if visited[ny][nx]:
            continue

        visited[ny][nx] = True
        cnt += 1
        dfs(ny, nx)


for i in range(N):
    for j in range(N):
        if not visited[i][j] and grid[i][j] == 1:
            cnt = 1
            visited[i][j] = True
            dfs(i, j)

            people_list.append(cnt)

print(len(people_list))
people_list.sort()
for i in people_list:
    print(i)
