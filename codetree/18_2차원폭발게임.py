"""
CT 18  2차원 폭발 게임
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-The-2D-bomb-game/description

풀이일 : 2026-09-26   결과: 품
한도   : time Python3 3초 · C++17 1초 / memory 128 MB / time_sec 3
난이도 : Hard  |  정답률 29.9%
제약   : - $1 \le N \le 100$
제약   : - $1 \le M \le 100$
제약   : - $1 \le K \le 1\,000$
제약   : - $1 \le \texttt{폭탄에 적힌 정수} \le 100$

[채점] accepted  4/4  (1.074s)

[문제]
$1$이상 $100$이하의 숫자가 적혀있는 폭탄이 $N \times N$ 크기의 상자에 들어있습니다.

![](https://contents.codetree.ai/problems/18/images/problems-e6539b9e-a937-4203-99ad-642cd6b24890.png)

이때 각각의 열에 대하여 행 기준으로 봤을 때 연속으로 $M$개 이상의 같은 숫자가 적혀있는 폭탄들은 터지게 되고, 중력에 의해 위에 있던 폭탄들은 밑으로 떨어지게 됩니다. $M$개 이상 연속한 폭탄은 부분만 터져서는 안되고 전부 다 터져야 하며, $M$개 이상인 폭탄들의 쌍이 여러 개라면 동시에 터지게 됩니다. 만약 터진 이후에도 같은 열에 행 기준으로 봤을 때 연속으로 $M$개 이상의 같은 숫자가 있는 경우가 존재한다면, 터져야 할 폭탄이 없을 때까지 조건에 맞는 폭탄들을 터뜨리는 것을 반복합니다.

$M = 2$인 경우 위의 예에서 폭탄들은 다음과 같이 터지게 됩니다.

![](https://contents.codetree.ai/problems/18/images/problems-d741f670-2d6c-44f4-aa38-ce094492c8b3.png)

폭탄이 터진 후, 다음과 같이 떨어지게 됩니다.

![](https://contents.codetree.ai/problems/18/images/problems-18fb7a18-e17e-441c-b6fe-f777af670d21.png)

터지는 과정을 한번 반복한 이후에는 상자를 시계방향으로 $90^{\circ}$ 회전시킵니다. 회전할 때 폭탄들이 옆으로 빠져나가는 경우는 없고, 회전 이후 중력에 의해 밑에 여유 공간이 있을 경우 밑으로 떨어지게 됩니다.

![](https://contents.codetree.ai/problems/18/images/problems-117a7715-3265-40e3-a98d-6402d22ef407.png)

폭탄들이 움직이지 않게 되면 다시 각각의 열마다 행을 기준으로 연속으로 $M$개 이상의 같은 숫자가 적혀있는 폭탄들은 터지게 되고 다시 중력에 의해 밑으로 떨어지게 됩니다.

위의 예에서 $M=2$인 경우 과정을 더 진행하면 다음과 같이 상태가 변하게 됩니다.

![](https://contents.codetree.ai/problems/18/images/problems-cc5453fe-bc68-48a2-b3f1-832dfae46a81.png)

![](https://contents.codetree.ai/problems/18/images/problems-7d66469c-dfbd-4d28-865a-36af078dc57e.png)

그리고 또 다시 시계방향으로 $90^{\circ}$ 회전하게 됩니다.

![](https://contents.codetree.ai/problems/18/images/problems-760de65f-a55e-421a-b2de-4b0e23ec6af2.png)

이와 같이 터지고 회전하는 과정을 총 $K$번 반복한다고 했을 때, 최종적으로 상자에 남아있는 폭탄의 수를 출력하는 프로그램을 작성해주세요. 만약 $K$번째 회전을 진행한 이후에도 터질 폭탄이 상자에 남아있다면, 조건에 맞는 폭탄들을 전부 터뜨리는 것을 반복한 이후에 최종적으로 상자에 남아 있는 폭탄의 수를 구해야 합니다.

[예제 1]
입력:
3 2 2
1 3 1
2 1 2
3 1 1

출력:
1


[예제 2]
입력:
6 2 5
3 3 2 2 3 3
3 3 3 3 4 4
3 2 2 2 4 1
1 3 3 3 4 1
3 4 3 3 4 1
2 4 3 3 1 2

출력:
5


[예제 3]
입력:
4 2 7
4 4 4 1
4 4 4 1
2 1 4 1
1 4 3 1

출력:
5


[예제 4]
입력:
4 2 8
4 4 4 1
4 4 4 1
2 1 4 1
1 4 3 1

출력:
3

"""

N, M, K = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(N)]

# Please write your code here.

def explode():
    is_explode = False
    for j in range(N):
        cur_num = grid[0][j]
        cnt = 1
        temp_list = []
        explode_targets = set()
        for i in range(1, N):
            # 같은 경우
            if cur_num == grid[i][j]:
                cnt += 1

            # 다른 경우
            else:
                # if cnt >= M:
                #     explode_targets.add(cur_num)
                temp_list.append([cur_num, cnt])
                cur_num = grid[i][j]
                cnt = 1
        # if cnt >= M:
        #     explode_targets.add(cur_num)
        temp_list.append([cur_num, cnt])

        ret = []

        for num, cnt in temp_list:
            if num == 0:
                continue
            if num in explode_targets:
                continue
            if cnt >= M:
                is_explode = True
                continue
            for _ in range(cnt):
                ret.append(num)
        len_ret = len(ret)
        new_list = [0] * N

        for i in range(N - 1, -1, -1):
            if len_ret <= 0:
                break
            new_list[i] = ret[len_ret - 1]
            len_ret -= 1


        for i in range(N):
            grid[i][j] = new_list[i]
    return is_explode
# explode()

def rotate():
    global grid

    new_grid = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            new_grid[j][N - 1 - i] = grid[i][j]

    grid = new_grid

    # print("debug rotated")
    # for i in grid:
    #     print(*i)

    # 내려주기
    for j in range(N):
        ret = []

        for i in range(N):
            if grid[i][j] != 0:
                ret.append(grid[i][j])
        len_ret = len(ret)
        new_list = [0] * N
        # print("wow", ret)
        for i in range(N - 1, -1, -1):
            if len_ret <= 0:
                break
            # print(i, len_ret - 1)
            new_list[i] = ret[len_ret - 1]
            len_ret -= 1


        for i in range(N):
            grid[i][j] = new_list[i]

#
# rotate()
#
# print("debug")
# for i in grid:
#     print(*i)

for k in range(K):
    while explode():
        pass
    rotate()
    # print("debug")
    # for i in grid:
    #     print(*i)
    while explode():
        pass


answer = 0
for i in range(N):
    for j in range(N):
        if grid[i][j] != 0:
            answer += 1
print(answer)
