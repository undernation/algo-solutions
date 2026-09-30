"""
CT 104  강력한 폭발
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-strong-explosion/description

풀이일 : 2026-09-30   결과: 품
한도   : time Python3 3.5초 · C++17 1초 / memory 128 MB / time_sec 3.5
난이도 : Medium  |  정답률 67.8%
제약   : - $1 \le N \le 20$
제약   : - 격자에 놓인 폭탄의 수 $M$은 $1$ 이상 $10$ 이하입니다.

[채점] accepted  2/2  (0.583s)

[문제]
$0$, $1$로 구성된 $N \times N$ 크기의 격자판이 주어집니다.

$1$은 해당 위치가 폭탄이 놓인 칸임을 의미합니다.

폭탄이 놓인 각 칸마다 다음 $3$가지 중 정확히 하나의 폭탄을 선택하여, 초토화되는 칸들의 합집합의 크기를 최대화하려고 합니다. 여러 폭탄에 의해 동시에 초토화된 칸은 한 번만 셉니다.

각 폭탄은 폭탄 위치를 포함하여 파란색으로 표시된 영역을 초토화시키게 됩니다. 세 폭탄의 모양은 다음과 같습니다.

- 세로 폭탄: 폭탄 위치와 그 위·아래 방향으로 각각 $2$칸씩, 세로로 연속된 $5$칸을 초토화합니다.
- 십자 폭탄: 폭탄 위치와 상·하·좌·우로 인접한 $4$칸, 총 $5$칸을 초토화합니다.
- X자 폭탄: 폭탄 위치와 네 대각선 방향으로 인접한 $4$칸, 총 $5$칸을 초토화합니다.

초토화 범위가 격자 밖으로 나가는 경우 그 부분은 무시하며, 격자 안에 걸치는 칸만 초토화됩니다.

![](https://contents.codetree.ai/problems/104/images/problems-fe15f418-5aac-4ede-b5b1-a7f681eecb41.png)

다음과 같이 폭탄을 놓아야 하는 위치가 $2$곳인 경우를 생각해봅시다.

![](https://contents.codetree.ai/problems/104/images/problems-e9db3ae6-53a1-4d21-931b-5a6ad566e01c.png)

만약 다음과 같이 폭탄을 놓게 되면 총 $7$곳이 초토화됩니다.

![](https://contents.codetree.ai/problems/104/images/problems-99f28aa2-45ff-41ce-bfcb-af1dfb6bab2e.png)

하지만 다음과 같이 폭탄을 놓게 되면, 총 $9$곳이 초토화됩니다.

![](https://contents.codetree.ai/problems/104/images/problems-b36e36d1-448c-44f0-8de8-1d35ea795355.png)

초기 격자판의 상태와 폭탄이 놓인 칸들이 주어졌을 때, 초토화되는 칸들의 합집합 크기의 최댓값을 구하는 프로그램을 작성해보세요.

[예제 1]
입력:
4
0 0 0 0
0 0 1 0
0 1 0 0
0 0 0 0

출력:
9


[예제 2]
입력:
4
0 1 0 0
0 1 0 0
0 1 0 0
0 1 0 0

출력:
12

"""

N = int(input())
grid = [list(map(int, input().split())) for _ in range(N)]


bombs = {
    1: ((-2, 0), (-1, 0), (1, 0), (2, 0), (0, 0)),
    2: ((1, 0), (0, 1), (-1, 0), (0, -1), (0, 0)),
    3: ((-1, -1), (-1, 1), (1, 1), (1, -1), (0, 0))
}

answer = 0

cands = []
cands_cnt = 0
for i in range(N):
    for j in range(N):
        if grid[i][j] == 1:
            cands.append((i, j))
            cands_cnt += 1



def dfs(idx, cur_set):
    global answer
    if idx == cands_cnt:
        answer = max(answer, len(cur_set))
        return

    for bomb in range(1, 4):
        new_set = cur_set.copy()
        cy, cx = cands[idx]

        for dy, dx in bombs[bomb]:
            ny = cy + dy
            nx = cx + dx
            if not (0 <= ny < N and 0 <= nx < N):
                continue
            new_set.add((ny, nx))

        dfs(idx + 1, new_set)

dfs(0, set())
print(answer)
