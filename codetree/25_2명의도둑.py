"""
CT 25  2명의 도둑
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-two-thieves/description

풀이일 : 2026-10-01   결과: 품
한도   : time Python3 2초 · C++17 0.5초 / memory 128 MB / time_sec 2
난이도 : Hard  |  정답률 52.2%
제약   : - $3 \le N \le 10$
제약   : - $1 \le M \le 5$
제약   : - $M \le N$
제약   : - $1 \le C \le 30$
제약   : - $1 \le w_{i,j} \le 9$ $(1 \le i,\ j \le N)$, 여기서 $w_{i,j}$는 $i$행 $j$열에 놓인 물건의 무게입니다.

[채점] accepted  2/2  (0.598s)

[문제]
$2$명의 도둑이 $N \times N$ 크기의 방에서 물건을 훔치려 합니다. 두 도둑은 각각 하나의 행을 정해 그 행 내에 연속한 $M$개의 열에 있는 물건들을 훔칠 수 있습니다. 두 도둑이 같은 행을 고를 수는 있지만, 같은 행을 골랐을 때에는 선택한 $M$개의 열이 서로 겹쳐서는 안 됩니다. 즉, 두 도둑이 선택한 크기 $M$의 영역이 서로 겹쳐서는 안 됩니다.

다음은 $M$이 $2$일 때 가능한 두 도둑이 물건을 훔칠 위치의 예시입니다.

![](https://contents.codetree.ai/problems/25/images/problems-5598da3b-f214-45f2-98f8-f44e799c1e74.png)

방 내의 각 위치마다 물건들이 하나씩 있고, 각 물건의 무게가 적혀있습니다. 각 도둑은 자신이 선택한 연속한 $M$개의 열에 있는 물건들 중 임의의 부분집합(하나도 고르지 않는 경우 포함)을 골라 훔칠 수 있습니다. 다만 두 도둑 모두 각각이 들 수 있는 최대 무게가 $C$이기 때문에, 고른 물건들의 무게의 합이 $C$를 넘지 않아야 합니다. 즉, 선택한 연속한 $M$개의 열에 있는 물건들의 무게의 합이 $C$를 넘지 않는다면 해당 물건들을 전부 고를 수 있지만, 만약 무게의 합이 $C$를 넘는다면 그 중에 적절하게 골라서 고른 물건들의 무게의 합이 $C$가 넘지 않도록 가져가야 합니다.

예를 들어 위의 왼쪽 예에서 $C$가 $8$인 경우 $2$번째 행에서 고른 도둑은 물건을 $2$개 다 고를 수 있지만, $4$번째 행에서 고른 도둑의 경우 $8$, $4$를 동시에 고를 수는 없습니다.

![](https://contents.codetree.ai/problems/25/images/problems-8b78b57f-97ed-4f06-afb0-f8c0ac785148.png)

무게가 $W$인 물건으로부터 얻을 수 있는 가치는 $W^2$으로 정해집니다. 이런 상황에서 도둑들이 훔칠 물건들을 잘 골라 주어진 조건을 만족하면서 얻을 수 있는 가치의 총 합 중 최댓값을 구하는 프로그램을 작성해보세요.

예를 들어 다음의 예에서 $M = 2,\ C = 8$일 경우 두 도둑이 얻을 수 있는 가치의 총 합의 최대는 $114$ 입니다. $(8 \times 8 + 7 \times 7 + 1 \times 1 = 114)$

![](https://contents.codetree.ai/problems/25/images/problems-7287f697-c7a6-41af-bb30-b11e8d3a4b23.png)

[예제 1]
입력:
4 3 10
1 8 2 5
2 6 4 7
2 3 4 5
1 2 4 2

출력:
120


[예제 2]
입력:
6 2 8
1 2 1 3 5 7
2 5 3 1 7 4
3 3 2 7 1 5
6 5 5 8 4 4
7 1 6 2 5 2
5 3 4 5 6 7

출력:
114

"""

N, M, C = map(int, input().split())
weight = [list(map(int, input().split())) for _ in range(N)]


# Please write your code here.


def encoder(y, x):
    return y * N + x


def decoder(num):
    mok = num // N
    rest = num % N
    return mok, rest


def check_max(num_list):
    MAX = (1 << M)
    max_val = 0
    for mask in range(MAX):
        total = 0
        total_score = 0
        for idx in range(M):
            if mask & (1 << idx):
                total += num_list[idx]
                total_score += num_list[idx] * num_list[idx]
        if total <= C:
            max_val = max(max_val, total_score)

    return max_val


answer = 0


def check_one_line(start, end):
    start_col = start // N
    end_col = end // N

    return start_col == end_col


def dfs(idx, cnt, total):
    global answer
    if cnt == 2:
        answer = max(answer, total)
        return

    for start in range(idx, N * N - M + 1):
        end = start + M - 1
        if not check_one_line(start, end):
            continue
        decode_start_y, decode_start_x = decoder(start)
        cur_num_list = weight[decode_start_y][decode_start_x: decode_start_x + M]
        dfs(start + M, cnt + 1, total + check_max(cur_num_list))


dfs(0, 0, 0)
print(answer)
