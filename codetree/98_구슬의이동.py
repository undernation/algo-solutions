"""
CT 98  구슬의 이동
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-marble-movement/description

풀이일 : 2026-09-29   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Hard  |  정답률 45.2%
제약   : - $2 \le N \le 50$
제약   : - $1 \le M \le N \times N$
제약   : - $1 \le T \le 100$
제약   : - $1 \le K \le M$
제약   : - $1 \le r \le N$
제약   : - $1 \le c \le N$

[채점] accepted  2/2  (0.682s)

[문제]
$M$개의 구슬이 $N \times N$ 격자 안에 놓여져 있고, 격자는 벽으로 둘러싸여 있습니다. 각 구슬은 일정 속도를 갖고 정해진 방향으로 움직이고 있습니다. 그림에서 나타나는 숫자는 각 구슬마다 $1$초에 몇 칸을 움직이는지를 표시한 것입니다.

![](https://contents.codetree.ai/problems/98/images/problems-b4188cc2-6d8f-4438-b011-e9eeba41ae1a.png)

구슬이 벽에 부딪히면 움직이는 방향이 반대로 뒤집혀 동일한 속도로 움직이는 것을 반복합니다. 이때 방향을 바꾸는 데에는 시간이 전혀 소요되지 않습니다.

![](https://contents.codetree.ai/problems/98/images/problems-1ba076a2-413e-4b70-95a1-0b3ee4bd4414.png)

위의 그림을 예로 1초 뒤의 모습을 그려보면 다음과 같습니다.

![](https://contents.codetree.ai/problems/98/images/problems-a1261a75-32da-4650-923c-2eef356977d0.png)

매 초마다 구슬들은 움직이게 되고, 움직이고 난 후 같은 위치에 여러 구슬이 위치하게 될 수도 있습니다. 만약 동일한 위치에 구슬이 $K$개 이하라면 문제 없이 그 다음 과정을 진행하게 됩니다.  하지만 만약 $K$개가 넘는 구슬이 같은 칸에 위치하게 된다면, 우선순위가 높은 구슬 $K$개만 살아남고 나머지 구슬들은 전부 사라지게 됩니다. 여기서 우선순위가 높다는 말은, 구슬의 속도가 빠른 구슬일수록 우선순위가 높으며 구슬의 속도가 일치할 경우에는 구슬의 번호가 더 큰 구슬이 우선순위가 높습니다.

다음 그림을 예로 들어보겠습니다.
![](https://contents.codetree.ai/problems/98/images/problems-b7b5d8ae-2a30-42d6-b584-63fdfb4be56e.png)

$K=2$라 했을 때 $1$초 뒤에는 세 구슬이 같은 위치에 있게 되고 이때 우선순위가 가장 높은 $2$번 구슬과 그 다음으로 우선순위가 높은 $3$번 구슬만이 살아남게 됩니다.
![](https://contents.codetree.ai/problems/98/images/problems-080f912c-5db8-4410-a0e8-ed510a8f8a88.png)

참고로, 시작시점으로부터 정수시간만큼 지난 경우에만 위 논리대로 구슬의 충돌을 따집니다. 예를 들어, 속도계산에 근거해서 $t=1.5s$ 시점에 부딪히게되는 경우가 있더라도 충돌이 아닌 것으로 간주합니다.

그리고 소멸은 충돌 그 즉시 일어납니다. 즉, 마지막 그림처럼 $t=1s$에 충돌하면, 이 시점에 이미 살아남은 구슬의 수는 두 개가 됩니다

각 구슬의 초기상태가 주어졌을 때, $T$초가 지난 이후에도 여전히 격자 안에 남아있는 구슬의 개수를 출력하는 프로그램을 작성해보세요.

[예제 1]
입력:
4 5 1 1
1 2 L 3
2 3 U 2
3 1 R 4
3 4 D 1
4 2 U 3

출력:
5


[예제 2]
입력:
4 3 1 2
1 4 D 1
2 1 R 3
3 4 U 1

출력:
2

"""

from collections import defaultdict

N, M, T, K = map(int, input().split())

r, c, d, v = [], [], [], []

DIR_DICT = {
    "U":(-1, 0),
    "D":(1, 0),
    "R":(0, 1),
    "L":(0, -1)
}

reversed_dict = {
    "U":"D",
    "D":"U",
    "R":"L",
    "L":"R"
}

for _ in range(M):
    ri, ci, di, vi = input().split()
    r.append(int(ri))
    c.append(int(ci))
    d.append(di)
    v.append(int(vi))

# Please write your code here.
marbles = dict()

for cur_id in range(M):
    cur_y = r[cur_id] - 1
    cur_x = c[cur_id] - 1
    cur_direction = d[cur_id]
    cur_v = v[cur_id]

    marbles[cur_id] = [cur_y, cur_x, cur_direction, cur_v]

def move(cy, cx, cur_direction, cur_v):

    for _ in range(cur_v):
        dy, dx = DIR_DICT[cur_direction]

        ny = cy + dy
        nx = cx + dx
        if not (0 <= ny < N and 0 <= nx < N):
            cur_direction = reversed_dict[cur_direction]
            dy, dx = DIR_DICT[cur_direction]

            ny = cy + dy
            nx = cx + dx

        cy = ny
        cx = nx

    return cy, cx, cur_direction




for time in range(T):
    cnt_board = defaultdict(list)
    new_marbles = dict()
    for marble_id, marble_info in marbles.items():
        cy, cx, cd, cv = marble_info
        ny, nx, new_direction = move(cy, cx, cd, cv)
        cnt_board[(ny, nx)].append([-cv, -marble_id])
        new_marbles[marble_id] = [ny, nx, new_direction, cv]

    for key, value in cnt_board.items():
        if len(value) > K:
            value.sort()
            for i in range(K, len(value)):
                cur = value[i]
                # print(cur)
                del new_marbles[-cur[1]]

    marbles = new_marbles

print(len(marbles))
