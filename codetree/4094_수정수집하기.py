"""
CT 4094  수정 수집하기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-collect-crystals/description

풀이일 : 2026-10-20   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 52.4%
제약   : - $1 \le N \le 1\,000$
제약   : - $1 \le K \le 20$
제약   : - $|S| = N$
제약   : - $S_i \in \{\texttt{L}, \texttt{R}\}$ $(1 \le i \le N)$

[채점] accepted  1/1  (0.296s)

[문제]
고대의 숲에는 두 개의 마법 샘터가 있으며, 특별한 수정이 존재합니다. 이 수정들은 샘터에서 생성되어 공중에 머물다가 땅에 떨어지면 소멸합니다. 숲의 수호자인 엘라는 이 수정들을 수집하여 숲에 그 힘을 전달해야 합니다. 수정을 수집하기 위해 엘라는 수정이 소멸하기 전에 공중에서 잡아야 하며, 두 샘터 사이를 빠르게 이동할 수 있지만, 자주 움직이면 힘이 소진되기에 최대 $K$번만 이동하고자 합니다.

각 시간마다 수정 하나가 두 샘터 중 한 곳에서 떨어지며, 엘라는 그 시점에 해당 샘터 앞에 있을 때에만 그 수정을 수집할 수 있습니다. 각 수정이 떨어지기 직전(첫 번째 수정 직전 포함)에 엘라는 현재 위치에 머무르거나 반대편 샘터로 이동할 수 있으며, 이동 횟수의 총합은 $K$ 이하여야 합니다.

엘라가 초기에 왼쪽 샘터 앞에 서있고, 최대 $K$번만 이동했을 때, 수집할 수 있는 최대 수정의 개수를 구하는 프로그램을 작성하세요.

[예제 1]
입력:
5 1
LLRLL

출력:
4

"""

N, K = map(int, input().split())
str = input()

# Please write your code here.

# dp[i][k] k 는 마지막 위치 0 은 l 1 은 r

dp = [[-1] * (K + 1) for _ in range(N + 1)]

if str[0] == "L":
    dp[0][0] = 1
    dp[0][1] = 0
else:
    dp[0][0] = 0
    dp[0][1] = 1

for i in range(1, N):

    cur = str[i]

    if cur == "L":
        cur_num = 0
    else:
        cur_num = 1

    for k in range(1, K + 1):
        # 이동하는 경우의 수
        last_num = dp[i - 1][k - 1]

        cur_pos = k % 2

        if cur_num == cur_pos:
            dp[i][k] = max(dp[i][k], last_num + 1)
        else:
            dp[i][k] = max(dp[i][k], last_num)

    # 이동 안하는 경우의 수

    for k in range(K + 1):
        last_num = dp[i - 1][k]


        cur_pos = k % 2

        if cur_num == cur_pos:
            dp[i][k] = max(dp[i][k], last_num + 1)
        else:
            dp[i][k] = max(dp[i][k], last_num)

print(max(dp[N - 1]))
