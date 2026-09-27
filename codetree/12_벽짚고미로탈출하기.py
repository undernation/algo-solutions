"""
CT 12  벽 짚고 미로 탈출하기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-escape-maze-with-wall-following/description

풀이일 : 2026-09-27   결과: 틀림
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 30.7%
제약   : - $1 \le x < N$
제약   : - $1 \le y \le N$
제약   : - $2 \le N \le 100$

[문제]
$N \times N$ 크기의 격자 안에서 주어진 위치에서 우측 방향을 바라보고 시작하여 오른쪽 벽을 짚고 쭉 따라가는 방식으로 미로를 탈출하는 프로그램을 작성해보세요. 규칙에 맞게 이동하다 격자 밖을 벗어났을 때 미로를 탈출 한 것으로 봅니다.

벽을 짚고 탈출하는 방식은 다음과 같습니다.

- Step 1 : 바라보고 있는 방향으로 이동하는 것이 가능하지 않은 경우

  - 반 시계 방향으로 $90^{\circ}$ 만큼 방향을 바꿉니다.

![](https://contents.codetree.ai/problems/12/images/problems-54ccc6f5-373f-4dce-838b-ddf577d1e480.png)

- Step 2 : 바라보고 있는 방향으로 이동하는 것이 가능한 경우

  - Case 1 : 바로 앞이 격자 밖이라면 이동하여 탈출합니다.

![](https://contents.codetree.ai/problems/12/images/problems-425727dd-469b-4b65-bf76-4319077633f5.png)

  - Case 2 :  만약 그 방향으로 이동했다 가정했을 때 해당 방향을 기준으로 오른쪽에 짚을 벽이 있다면 그 방향으로 한 칸 이동합니다.

![](https://contents.codetree.ai/problems/12/images/problems-db7c3d60-bb29-427f-aee7-cc8640fc35bd.png)

  - Case 3 : 만약 그 방향으로 이동했다 가정했을 때 해당 방향을 기준으로 오른쪽에 벽이 존재하지 않는다면, 현재 방향으로 한 칸 이동 후 방향을 시계 방향으로 $90^{\circ}$ 만큼 방향을 틀어 한 칸 더 전진하여 오른쪽에 벽이 있게끔 합니다.

![](https://contents.codetree.ai/problems/12/images/problems-4e35f504-8dd5-419e-af85-2e23eb8a14a1.png)

이러한 과정을 반복하게 됩니다.

다음은 탈출을 하게 되는 예시 중 하나 입니다.
![](https://contents.codetree.ai/problems/12/images/problems-865a09e2-a25c-4aff-9932-ca1105ac983d.png)
![](https://contents.codetree.ai/problems/12/images/problems-86e5f933-998f-4ce2-86a1-68db0c7cb67b.png)
![](https://contents.codetree.ai/problems/12/images/problems-e1bc5aff-0907-4273-a223-955ea72b687c.png)
![](https://contents.codetree.ai/problems/12/images/problems-cae6bce8-aa24-4f3b-9a01-afe7cb209fff.png)
![](https://contents.codetree.ai/problems/12/images/problems-c1c3ce59-77c9-40bc-90f1-a45615170d3d.png)
![](https://contents.codetree.ai/problems/12/images/problems-2c72a2c9-0655-4e3e-b1f4-4b1fd9a69c76.png)
![](https://contents.codetree.ai/problems/12/images/problems-8a992b34-7805-4ae7-a2ac-b335979a7a26.png)
![](https://contents.codetree.ai/problems/12/images/problems-2b9fd1c8-5682-47a3-9b3c-3b5606487478.png)
![](https://contents.codetree.ai/problems/12/images/problems-3e9ce97f-24d5-4010-8aa4-d173dfd0fb0a.png)
![](https://contents.codetree.ai/problems/12/images/problems-880aa737-a77f-450a-bf37-dcd63de7a2e5.png)

.

[예제 1]
입력:
3
1 1
.#.
#..
...

출력:
1


[예제 2]
입력:
3
1 1
...
##.
...

출력:
7


[예제 3]
입력:
3
1 1
...
#..
...

출력:
5


[예제 4]
입력:
3
1 2
...
.#.
...

출력:
-1

"""

N = int(input())
x, y = map(int, input().split())

grid = [["."] * N for _ in range(N)]
for i in range(N):
    row = input()
    for j in range(N):
        grid[i][j] = row[j]

# Please write your code here.

x -= 1
y -= 1
visited = set()
DIR = [[1, 0], [-1, 0], [0, 1], [0, -1]]
visited.add((y, x, 2))

DIR_DICT2 = {
    0: 2,
    1: 3,
    2: 1,
    3: 0
}

DIR_DICT = {
    0: 3,
    1: 2,
    2: 0,
    3: 1
}


# 현재 방향으로 이동 가능한지 확인
def check(cy, cx, cur_direction):
    dy, dx = DIR[cur_direction]
    ny = cy + dy
    nx = cx + dx

    if not (0 <= ny < N and 0 <= nx < N):
        return "escaped"
    elif grid[ny][nx] == "#":
        return "no"
    elif grid[ny][nx] == ".":
        return "yes"


time = 0


# 이동 후에 오른쪽에 벽 있는지 확인, 벽없으면 90도 틀어서 한칸 전진
def after_moved(cy, cx, cur_direction):
    global time
    right_dir = DIR_DICT[cur_direction]
    dy, dx = DIR[right_dir]

    ny = cy + dy
    nx = cx + dx
    if grid[ny][nx] == "#":
        return cy, cx, cur_direction
    else:
        time += 1
        return ny, nx, right_dir


cy, cx = y, x
cd = 2
# print("start", cy, cx)
while True:
    # print("debug", cy, cx)
    ret = check(cy, cx, cd)
    if ret == "escaped":
        time += 1
        break
    elif ret == "yes":
        dy, dx = DIR[cd]
        cy = cy + dy
        cx = cx + dx
        if (cy, cx, cd) in visited:
            time = -1
            break
        time += 1
        visited.add((cy, cx, cd))
    elif ret == "no":
        cd = DIR_DICT2[cd]
        if (cy, cx, cd) in visited:
            time = -1
            break
        visited.add((cy, cx, cd))
        continue

    if ret == "yes":
        # print("yes", cy, cx)
        ny, nx, nd = after_moved(cy, cx, cd)
        if (cy, cx, cd) != (ny, nx, nd):
            if (ny, nx, nd) in visited:
                time = -1
                break

        if not (0 <= ny < N and 0 <= nx < N):
            break

        cy, cx, cd = ny, nx, nd

        visited.add((cy, cx, cd))

print(time)
