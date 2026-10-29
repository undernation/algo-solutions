"""
CT 4097  신전 탐험하기 3
https://www.codetree.ai/ko/trails/complete/curated-cards/test-explore-temple-3/description

풀이일 : 2026-10-29   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Easy  |  정답률 83.7%
제약   : - $2 \le N \le 1\,000$
제약   : - $2 \le M \le 100$
제약   : - $1 \le a_{i,j} \le 1\,000$ $(1 \le i \le N,\ 1 \le j \le M)$

[채점] accepted  1/1  (0.248s)

[문제]
신전은 $N$층으로 이루어져 있습니다. 각 층에는 왼쪽부터 시작해 $1$, $2$, $3$, $\cdots$, $M$번까지 총 $M$개의 방이 있으며 이 중 하나의 방만을 들어가 그 방 안에 있는 보물을 가져갈 수 있습니다.

신전에는 특이한 장치가 있어서, 바로 직전 층에서 들어갔던 번호의 방을 한번 더 들어가면, 예를 들어 $3$층에서 $2$번 방을 들어갔는데 $4$층에서도 $2$번 방을 들어갈 경우 위험 장치가 발동해 쫓겨납니다.

남우는 $1$층부터 시작해서 $N$층까지 차례대로 올라가면서 방을 들어가되, 쫓겨나지 않고 최대한 많은 보물을 가져가고자 합니다. 남우가 가져갈 수 있는 보물의 최대 개수를 구하는 프로그램을 작성하세요.

[예제 1]
입력:
2 3
10 9 8
10 7 6

출력:
19

"""


N, M = map(int, input().split())

board = [list(map(int, input().split())) for _ in range(N)]

# print(board)
INF = 10 ** 18
dp = [[0] * M for _ in range(N)]

for i in range(M):
    dp[0][i] = board[0][i]

for idx in range(1, N):

    for i in range(M):
        for j in range(M):
            if i == j:
                continue

            dp[idx][j] = max(dp[idx][j], dp[idx- 1][i] + board[idx][j])

print(max(dp[N - 1]))
