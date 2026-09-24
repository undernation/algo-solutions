"""
CT 15  1차원 바람
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-The-1D-wind-blows/description

풀이일 : 2026-09-24   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 59.2%
제약   : - $1 \le N \le 100$
제약   : - $1 \le M \le 100$
제약   : - $0 \le Q \le 100$
제약   : - $1 \le r \le N$
제약   : - $0 \le a_{i,j} \le 9$ $(1 \le i \le N, 1 \le j \le M)$
제약   : - $d$는 'L' 또는 'R'입니다.

[문제]
$0$이상 $9$이하의 정수로만 이루어진 $N \times M$ 행렬 모양의 건물에 총 $Q$번의 바람이 붑니다.

바람은 특정 행의 모든 원소들을 왼쪽 혹은 오른쪽으로 전부 한 칸씩 밀어 shift 하는 효과를 가져옵니다.

오른쪽으로 한 칸 shift하는 예시는 다음과 같습니다.

![](https://contents.codetree.ai/problems/15/images/problems-f915fb33-b018-42bc-9f5a-b1aad4c0f539.png)

왼쪽으로 한 칸 shift하는 예시는 다음과 같습니다.

![](https://contents.codetree.ai/problems/15/images/problems-8cd44f57-5718-48da-9b4f-1d1fcfaa5625.png)

이 바람에 영향을 받아 특정 행의 숫자들이 한 칸씩 밀리게 되면, 위 아래로도 영향을 미치기 시작합니다. 밀리기 시작한 행을 기준으로 위 아래 방향으로 순차적으로 전파가 되며 도중에 전파 방향이 바뀌는 경우는 없습니다.

![](https://contents.codetree.ai/problems/15/images/problems-ed2ab251-9d91-41f1-995f-1ceced03153e.png)

전파가 이어질 조건은 현재 행이 shift된 이후, 나아가려는 행과 비교했을 때, 단 하나라도 같은 열에 같은 숫자가 적혀있는 경우라면 전파를 이어나갑니다. 같은 숫자가 하나도 존재하지 않거나 끝에 다다랐다면 전파를 종료합니다. 전파가 진행되는 경우 나아가려는 행의 숫자들을 한 칸씩 밀게되며, 이때 현재 행이 밀렸던 방향과는 반대 방향으로 한 칸씩 밀리게 됩니다.

예를 들어 위의 예에서 우측 방향으로 바람이 불어와 $3$번째 행이 오른쪽으로 한 칸 밀린 이후에는 $2$행, $4$행 방향으로 전파를 시도합니다. $2$번째 행과 $4$번째 행 모두 $3$번째 행과 같은 열에서 일치하는 숫자가 하나 이상 존재하므로 전파를 진행합니다. 이때, $3$행은 우측 방향으로 밀렸던 행이므로 $2$행, $4$행은 전파의 영향을 받아 전부 반대 방향인 좌측 방향으로 한 칸씩 밀리게 됩니다.

![](https://contents.codetree.ai/problems/15/images/problems-44c9ea32-f86d-4c25-9adc-4d96871660d7.png)

전파는 계속 진행됩니다. $2$행과 $4$행은 진행했던 방향으로 그다음 전파를 시도합니다.

$2$행은 $1$행과의 비교에서 같은 열에 일치하는 숫자가 존재하지 않으므로 위로 진행하는 전파를 중단합니다. 하지만 $4$행의 경우 $5$행과 일치하는 숫자가 하나 존재하므로 전파를 진행합니다. 이때, $4$행은 좌측으로 밀렸던 행이므로 $5$행은 전파의 영향을 받아 반대 방향인 우측 방향으로 한 칸씩 밀리게 됩니다.

![](https://contents.codetree.ai/problems/15/images/problems-8a011a7f-7934-433c-ae0d-bcd0eec73a5a.png)

위로 진행하던 전파는 막혔으므로 더 이상 진행되지 않습니다. 아래로는 여전히 전파를 시도하게 되고, $5$행과 $6$행은 일치하는 숫자가 있기 때문에 전파를 진행합니다. 이때 $5$행은 우측으로 밀렸던 행이므로 $6$행은 전파의 영향을 받아 반대 방향인 좌측 방향으로 한 칸씩 밀리게 됩니다.

![](https://contents.codetree.ai/problems/15/images/problems-0bd84bac-8c60-4895-9f58-9c0edcb69bab.png)

이제 아래로 진행하던 전파는 끝에 다다랐기 때문에 진행을 중단합니다.

한 바람이 분 이후 모든 전파가 완료 되었을 때 그 다음 바람이 불어 온다고 할 때, 총 $Q$개의 바람을 거친 이후 건물의 상태를 출력하는 프로그램을 작성해보세요

[예제 1]
입력:
6 5 1
1 5 6 7 3
5 3 2 5 4
6 4 5 2 5
2 6 1 0 5
5 1 2 1 6
4 2 5 2 8
3 L

출력:
1 5 6 7 3
3 2 5 4 5
5 6 4 5 2
6 1 0 5 2
6 5 1 2 1
2 5 2 8 4


[예제 2]
입력:
3 3 2
1 2 3
3 2 1
3 3 3
3 L
1 L

출력:
2 3 1
1 3 2
3 3 3

"""

N, M, Q = map(int, input().split())
building = [list(map(int, input().split())) for _ in range(N)]
winds = [(int(r), d) for r, d in [input().split() for _ in range(Q)]]

# Please write your code here.

def check(col_num1, col_num2):
    for m in range(M):
        if building[col_num1][m] == building[col_num2][m]:
            return True
    return False

def shift_side(col_num, direction):
    cur_list = building[col_num]

    if direction == "L":
        temp = cur_list[M - 1]

        for m in range(M - 1, 0, -1):
            cur_list[m] = cur_list[m - 1]
        cur_list[0] = temp
    else:
        temp = cur_list[0]
        for m in range(M - 1):
            cur_list[m] = cur_list[m + 1]
        cur_list[M - 1] = temp

def toggle(cur_direction):
    if cur_direction == "R":
        return "L"
    else:
        return "R"

def spread(col, direction):
    shift_side(col, direction)

    # 위로 spread
    cur_col = col
    nxt_col = cur_col - 1
    
    cur_dir = direction
    while nxt_col >= 0 and check(nxt_col, cur_col):
        cur_dir = toggle(cur_dir)
        shift_side(nxt_col, cur_dir)
        cur_col = nxt_col
        nxt_col -= 1
    # 아래로 spread

    cur_col = col
    nxt_col = cur_col + 1
    cur_dir = direction

    while nxt_col <= N - 1 and check(nxt_col, cur_col):
        cur_dir = toggle(cur_dir)
        shift_side(nxt_col, cur_dir)
        cur_col = nxt_col
        nxt_col += 1

for q in range(Q):
    row, direction = winds[q]

    spread(row - 1, direction)

for i in building:
    print(*i)
