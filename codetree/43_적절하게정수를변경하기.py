"""
CT 43  적절하게 정수를 변경하기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-change-number-properly/description

풀이일 : 2026-10-20   결과: 못품
한도   : time Python3 3초 · C++17 0.5초 / memory 128 MB / time_sec 3
난이도 : Medium  |  정답률 59.8%
제약   : - $1 \le N \le 500$
제약   : - $0 \le M \le 100$
제약   : - $1 \le A_i \le 4$ $(1 \le i \le N)$

[채점] accepted  2/2  (0.595s)

[문제]
$1$이상 $4$이하의 정수로만 이루어진 길이가 $N$인 수열이 하나 있습니다.

이 수열과 같은 길이를 가지며, 마찬가지로 $1$이상 $4$이하의 정수로만 이루어진 비슷한 수열을 만들고 싶습니다.
- 비슷한 수열의 조건 : 수열을 순서대로 읽었을 때, 인접한 두 원소가 다른 횟수가 $M$번 이하입니다.

예를 들어, $1$, $2$, $1$, $3$, $3$은 인접한 두 원소가 다른 횟수가 $3$회 입니다.

또한, 두 수열의 유사도는 같은 위치에 같은 원소가 있는 횟수로 정의됩니다.

예를 들어, $1$, $2$, $1$, $3$, $3$과 $1$, $1$, $1$, $3$, $3$의 유사도는 $4$ 입니다.

만들 수 있는 비슷한 수열 중, 주어진 수열과의 유사도가 가장 큰 값을 출력하는 프로그램을 작성해보세요.

예를 들어, $N = 5$, $M = 1$ 이고 입력으로 주어진 수열이 $1$, $2$, $1$, $3$, $3$ 이라면 새로 만든 수열 $1$, $1$, $1$, $3$, $3$ 은
- 인접한 두 원소가 다른 횟수가 $1$회($M$이하)이므로 비슷한 수열이고,
- 유사도가 $4$이므로 (두 번째 원소를 제외하고 모두 같음)

유사도가 가장 큰 비슷한 수열의 예시입니다.

![](https://contents.codetree.ai/problems/43/images/problems-649efb7a-6310-4477-8c36-fe86062865d3.png)

[예제 1]
입력:
5 1
1 2 1 3 3

출력:
4


[예제 2]
입력:
5 3
1 2 1 3 3

출력:
5

"""

N, M = map(int, input().split())
a = [0] + list(map(int, input().split()))

# dp[n][k][last]
dp = [[[-1] * 5 for _ in range(M + 1)] for _ in range(N + 1)]

# 초기화
for num in range(1, 5):
    dp[1][0][num] = int(a[1] == num)

for n in range(2, N + 1):

    cur_a = a[n]

    for k in range(M + 1):

        for last in range(1, 5):

            if dp[n - 1][k][last] == -1:
                continue

            for cur_num in range(1, 5):

                # 인접한 숫자가 다르면 변경 횟수 증가
                next_k = k

                if last != cur_num:
                    next_k += 1

                if next_k > M:
                    continue

                # 유사도 계산
                score = 1 if cur_a == cur_num else 0

                dp[n][next_k][cur_num] = max(
                    dp[n][next_k][cur_num],
                    dp[n - 1][k][last] + score
                )

answer = 0

for k in range(M + 1):
    for last in range(1, 5):
        answer = max(answer, dp[N][k][last])

print(answer)
