"""
CT 16  2차원 바람
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-The-2D-wind-blows/description

풀이일 : 2026-09-24   결과: 못품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 71.1%
제약   : - $2 \le N \le 100$
제약   : - $2 \le M \le 100$
제약   : - $0 \le Q \le 100$
제약   : - $0 \le A_{i,j} \le 9$ $(1 \le i \le N,\ 1 \le j \le M)$
제약   : - $1 \le r_1 < r_2 \le N$
제약   : - $1 \le c_1 < c_2 \le M$

[문제]
$0$이상 $9$이하의 정수로만 이루어진 $N \times M$ 행렬 모양의 건물에 총 $Q$번의 바람이 붑니다.

이 바람은 굉장히 특이해서 특정 직사각형 영역의 경계에 있는 정수들을 시계 방향으로 한 칸씩 shift 하고 해당 직사각형 내 영역에 있는 값들을 각각 자신의 위치를 기준으로 자신과 인접한 원소들과의 평균 값으로 바꿉니다. (평균 계산시에는 항상 버림하여 정수값이 나오도록 합니다.)

예를 들어 바람이 다음과 같은 영역에 영향을 미치게 되는 경우를 생각해봅시다.

![](https://contents.codetree.ai/problems/16/images/problems-202ecc5d-28c1-41e5-915a-2b0b51011cf8.png)

먼저 직사각형의 경계에 있는 정수들이 시계 방향으로 한 칸씩 회전을 하게 됩니다.

![](https://contents.codetree.ai/problems/16/images/problems-a25992b2-aa19-4d54-b77e-798dff43e66a.png)

그 다음 직사각형 영역 내에 있는 각각의 정수들의 값이 `현재 칸에 적혀있는 정수 + 인접한 곳에 적혀있는 정수들`의 평균 값으로 바뀌게 됩니다. 이 과정은 순차적으로 일어나는 것이 아니라 동시에 일어납니다.

예를 들어 $(2,\ 2)$ 위치에 있던 원소는 인접한 $4$개의 값들과의 평균값을 버림한 값인 $3$으로 바뀌어야 합니다.

![](https://contents.codetree.ai/problems/16/images/problems-85c4e969-381a-43dc-bb48-297dee1f8133.png)

$(4,\ 6)$ 위치에 있던 원소는 인접한 정수가 $2$개밖에 없으므로, 그 정수들과의 평균값을 버림한 값인 $6$으로 바뀌게 됩니다.

![](https://contents.codetree.ai/problems/16/images/problems-284eb239-5099-4f47-9758-0c7ebe210f23.png)

예를 들어 다음 직사각형이 평균값이 변화는 과정을 거치면 다음과 같이 값이 변하게 됩니다.

![](https://contents.codetree.ai/problems/16/images/problems-6103070e-5809-4b6a-bf45-1c5138dbd727.png)

한 바람이 분 이후 모든 값 변경이 완료된 이후에 그 다음 바람이 불어 온다고 할 때, 총 $Q$개의 바람을 거친 이후 건물의 상태를 출력하는 프로그램을 작성해보세요

[예제 1]
입력:
4 6 1
4 5 2 5 6 6
2 1 6 1 0 5
5 2 2 1 6 5
4 5 2 8 8 6
2 2 4 6

출력:
4 5 2 5 6 6 
2 3 2 2 3 3 
5 3 3 4 3 4 
4 4 5 5 6 5 


[예제 2]
입력:
3 3 2
1 2 3
3 2 1
3 3 3
1 1 2 2
2 2 3 3

출력:
2 2 3 
2 2 2 
3 2 1 

"""

N, M, Q = map(int, input().split())

# Create 2D array for building state
arr = [list(map(int, input().split())) for _ in range(N)]

# Process wind queries
winds = [tuple(map(int, input().split())) for _ in range(Q)]

# Please write your code here.

def rotate(y1, x1, y2, x2):
    temp = arr[y1 + 1][x1]
    temp_arr = []
    # 윗변
    i = y1
    for j in range(x1, x2 + 1):
        temp_arr.append((i, j))
    j = x2
    for i in range(y1 + 1, y2 + 1):
        temp_arr.append((i, j))

    # 아랫변
    i = y2
    for j in range(x2 - 1, x1 - 1, -1):
        temp_arr.append((i, j))

    j = x1
    for i in range(y2 - 1, y1, -1):
        temp_arr.append((i, j))

    len_arr = len(temp_arr)
    # 거꾸로
    for i in range(len_arr - 1, 0, -1):
        cy, cx = temp_arr[i]
        ny, nx = temp_arr[i - 1]
        # print(ny, nx)
        arr[cy][cx] = arr[ny][nx]
    arr[y1][x1] = temp

masks = [[-1, 0], [0, -1], [1, 0], [0, 1]]

def change_block(y, x, arr, new_arr):
    cnt = 1
    total = arr[y][x]

    for dy, dx in masks:
        ny = y + dy
        nx = x + dx
        if not (0 <= ny < N and 0 <= nx < M):
            continue
        cnt += 1
        total += arr[ny][nx]
    
    new_arr[y][x] = total // cnt

def change(y1, x1, y2, x2, arr):
    new_arr = [row[:] for row in arr]
    for i in range(y1, y2 + 1):
        for j in range(x1, x2 + 1):
            change_block(i, j, arr, new_arr)

    arr[:] = new_arr


for q in range(Q):
    y1, x1, y2, x2 = winds[q]
    # print("debug",y1, x1, y2, x2, q)
    rotate(y1 - 1, x1 - 1, y2 - 1, x2 - 1)
    change(y1 - 1, x1 - 1, y2 - 1, x2 - 1, arr)

for i in arr:
    print(*i)
