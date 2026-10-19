"""
CT 4093  신전 탐험하기 2
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-explore-temple-2/description

풀이일 : 2026-10-19   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 58.5%
제약   : - $2 \le N \le 1\,000$
제약   : - $1 \le l,\ m,\ r \le 1\,000$

[채점] accepted  1/1  (0.296s)

[문제]
신전은 $N$층으로 이루어져 있습니다. 각 층에는 왼쪽, 가운데, 오른쪽 세 개의 방이 있으며 이 중 하나의 방만을 들어가 그 방 안에 있는 보물을 가져갈 수 있습니다.

신전에는 특이한 장치가 있어서, 바로 직전 층에서 들어갔던 방향의 방을 한번 더 들어가면, 예를 들어 $3$층에서 오른쪽 방을 들어갔는데 $4$층에서도 오른쪽 방을 들어갈 경우 위험 장치가 발동해 쫓겨납니다.

또한 꼭대기 층인 $N$층에서는 한 가지의 장치가 더 있으며, $N$층에서 들어갔던 방의 방향과 $1$층에서 들어갔던 방의 방향이 같을 경우에도 위험 장치가 발동해 쫓겨납니다.

남우는 $1$층부터 시작해서 $N$층까지 차례대로 올라가면서 방을 들어가되, 쫓겨나지 않고 최대한 많은 보물을 가져가고자 합니다. 남우가 가져갈 수 있는 보물의 최대 개수를 구하는 프로그램을 작성하세요.

[예제 1]
입력:
2
10 9 8
10 7 6

출력:
19

"""

N = int(input())
l, m, r = [], [], []
num_list = []
for _ in range(N):
    left, mid, right = map(int, input().split())
    l.append(left)
    m.append(mid)
    r.append(right)
    num_list.append([left, mid, right])

# Please write your code here.

dp = [list([-1] * 3 for _ in range(3)) for _ in range(N)]

for i in range(3):
    dp[0][i][i] = num_list[0][i]


for n in range(1, N):

    for first in range(3):

        for last in range(3):

            if dp[n - 1][last][first] == -1:
                continue

            for nxt in range(3):

                if nxt == last:
                    continue

                if n == N - 1 and nxt == first:
                    continue

                dp[n][nxt][first] = max(dp[n][nxt][first], dp[n - 1][last][first] + num_list[n][nxt])
answer = 0

for i in range(3):
    answer = max(answer, max(dp[N - 1][i]))
print(answer)
