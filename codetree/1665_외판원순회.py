"""
CT 1665  외판원 순회
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-traveling-salesman-problem/description

풀이일 : 2026-10-04   결과: 틀림
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 43.2%
제약   : - $2 \le N \le 10$
제약   : - $1 \le i, j \le N$
제약   : - $0 \le \texttt{주어지는 정수} \le 10\,000$
제약   : - $A_{ii} = 0$
제약   : - 불가능한 입력은 주어지지 않는다고 가정해도 좋습니다.

[문제]
$1$번 지점에서 출발하여 모든 지점을 정확히 딱 한 번씩만 방문하고 다시 $1$번 지점으로 돌아오려고 합니다. $i$번 지점에서 $j$번 지점으로 이동하는데 드는 비용 정보 $A_{ij}$가 주어졌을 때 모든 정점을 겹치지 않게 방문하고 되돌아오는데 필요한 최소 비용의 합을 구하는 프로그램을 작성해보세요.

[예제 1]
입력:
4
0 2 5 9
3 0 8 11
7 3 0 10
9 5 7 0

출력:
22

"""

N = int(input())
A = [list(map(int, input().split())) for _ in range(N)]

# Please write your code here.

MAX = (1 << N) - 1
answer = 10 ** 18

def dfs(last_node, cost, mask):
    global answer
    if mask == MAX:
        if A[last_node][0] == 0:
            return
        answer = min(answer, cost + A[last_node][0])
        return

    for node in range(N):
        if mask & (1 << node):
            continue
        if A[last_node][node] == 0:
            continue
        dfs(node, cost + A[last_node][node], mask | (1 << node))

dfs(0, 0, 1)
print(answer)
