"""
CT 31  두 방향 탈출 가능 여부 판별하기
https://www.codetree.ai/ko/trails/complete/curated-cards/intro-determine-escapableness-with-2-ways/description

풀이일 : 2026-10-05   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 192 MB / time_sec 1
난이도 : Easy  |  정답률 47.8%
제약   : - $2 \le N, M \le 100$
제약   : - 격자의 각 칸의 값은 뱀이 없는 경우 $1$, 뱀이 있는 경우 $0$입니다.
제약   : - 시작 칸과 끝 칸에는 뱀이 주어지지 않는다고 가정해도 좋습니다.

[채점] accepted  2/2  (0.517s)

[문제]
$N \times M$ 크기의 이차원 영역의 좌측 상단에서 출발하여 우측 하단까지 뱀에게 물리지 않고 탈출하려고 합니다. 이동을 할 때에는 반드시 아래와 오른쪽 두 방향 중 인접한 칸으로만 이동할 수 있으며, 뱀이 있는 칸으로는 이동을 할 수 없습니다. 예를 들어 <그림 1>과 같이 뱀이 배치되어 있는 경우 실선과 같은 경로로 탈출을 할 수 있습니다. 이 때 뱀에게 물리지 않고 탈출 가능한 경로가 있는지 여부를 판별하는 코드를 작성해보세요.

![](https://contents.codetree.ai/problems/31/images/problems-fd5f8453-7d51-4973-8202-2eb4f14c070d.png)

[예제 1]
입력:
5 5
1 0 1 1 1
1 0 1 0 1
1 0 1 1 1
1 0 1 0 1
1 1 1 0 1

출력:
0


[예제 2]
입력:
5 5
1 0 1 1 1
1 0 1 0 1
1 1 1 0 1
1 0 1 1 1
0 1 1 0 1

출력:
1

"""

N, M = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(N)]

# Please write your code here.

visited = [[False] * M for _ in range(N)]
is_exist = False


def dfs(cy, cx):
    global is_exist, visited

    for dy, dx in [[1, 0], [0, 1]]:
        ny = cy + dy
        nx = cx + dx

        if not (0 <= ny < N and 0 <= nx < M):
            continue
        if grid[ny][nx] == 0:
            continue
        if visited[ny][nx]:
            continue

        if ny == N - 1 and nx == M - 1:
            is_exist = True
            return

        visited[ny][nx] = True

        dfs(ny, nx)


visited[0][0] = True
dfs(0, 0)

if is_exist:
    print(1)
else:
    print(0)
