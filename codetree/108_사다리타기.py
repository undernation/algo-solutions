"""
CT 108  사다리 타기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-ladder-game/description

풀이일 : 2026-10-01   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Hard  |  정답률 55.1%
제약   : - $2 \le N \le 11$
제약   : - $1 \le M \le 15$
제약   : - $1 \le a_i \lt N$ $(1 \le i \le M)$
제약   : - $1 \le b_i \le 15$ $(1 \le i \le M)$
제약   : - 서로 겹치거나 맞닿아 있는 가로줄은 주어지지 않습니다.

[채점] accepted  2/2  (0.537s)

[문제]
사다리 타기 게임은 사람 수 $N$만큼 세로줄을 긋고 위쪽 편에는 $1$부터 $N$까지의 숫자를 순서대로 적은 다음, 몇몇 인접한 세로줄 사이에 가로줄 $M$개를 서로 겹치지 않게 긋습니다.

이후 위쪽에 있는 각 숫자에서부터 시작하여 내려가다가 교점을 만날 때마다 $90$도로 방향을 꺾다 끝에 도착하게 되면 해당 숫자를 적는 게임입니다.

예를 들어 $N$이 $4$, $M$이 $6$이고 다음과 같이 가로줄이 주어졌을 때의 결과는 $3$, $4$, $1$, $2$가 됩니다.

![](https://contents.codetree.ai/problems/108/images/problems-72462dfd-437c-46c1-ad10-e88905b8959a.png)

하지만 주어진 가로줄 중 다음과 같이 $4$개의 가로줄만 갖고 사다리 게임을 진행해도 처음 주어진 사다리와 동일한 결과를 얻을 수 있습니다.

![](https://contents.codetree.ai/problems/108/images/problems-5c66b307-fcd0-4a37-ba18-2e5b08b968c6.png)

세로줄의 수 $N$과 $M$개의 가로줄의 상태가 주어졌을 때, 사용한 가로줄을 적절하게 선택해 모든 가로줄을 이용했을 때의 결과와 동일하게 되도록 하는 최소 가로줄의 수를 구하는 프로그램을 작성해보세요.

[예제 1]
입력:
4 6
1 1
1 3
2 2
2 4
3 3
3 5

출력:
4


[예제 2]
입력:
4 6
1 1
2 2
3 3
3 4
2 5
1 6

출력:
0

"""

N, M = map(int, input().split())
edges = [tuple(map(int, input().split())) for _ in range(M)]

# Please write your code here.

board = [[0] * N for _ in range(15)]

for a, b in edges:
    new_a = a - 1
    new_b = b - 1
    board[new_b][new_a] = 1
    board[new_b][new_a + 1] = -1


def check(start_line):
    cx = start_line

    for i in range(15):
        # print(cx)
        if board[i][cx] == 0:
            continue
        elif board[i][cx] == 1:
            cx += 1

        else:
            cx -= 1

    return cx

temp_result = []

for start_line in range(N):
    ret = check(start_line)

    temp_result.append(ret)

answer = 10 ** 18

board = [[0] * N for _ in range(15)]

def dfs(mask, cnt, idx):
    global answer
    if idx == M:
        is_ok = True
        for start_line in range(N):
            ret = check(start_line)
            if temp_result[start_line] != ret:
                is_ok = False
                break

        if is_ok:
            answer = min(answer, cnt)
        return
    a, b = edges[idx]
    new_a = a - 1
    new_b = b - 1
    board[new_b][new_a] = 1
    board[new_b][new_a + 1] = -1
    # 선택 하는 경우의 수
    dfs(mask | (1 << idx), cnt + 1, idx + 1)
    board[new_b][new_a] = 0
    board[new_b][new_a + 1] = 0

    # 선택 안하는 경우의 수
    dfs(mask | (1 << idx), cnt, idx + 1)

dfs(0, 0, 0)
print(answer)
