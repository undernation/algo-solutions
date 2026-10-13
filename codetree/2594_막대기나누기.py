"""
CT 2594  막대기 나누기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-rod-cutting/description

풀이일 : 2026-10-13   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 64 MB / time_sec 1
난이도 : Medium  |  정답률 90.0%
제약   : - $1 \le N \le 100$
제약   : - $1 \le \texttt{주어지는 수익 값} \le 10\,000$

[채점] accepted  2/2  (0.514s)

[문제]
길이가 $N$인 막대기가 하나 주어졌을 때, 막대기를 잘 쪼개어 최대 수익을 얻고자 합니다. $1$부터 $N$까지 각각의 길이에 대해 팔았을 때 얻을 수 있는 수익 정보가 주어졌을 때, 최대 수익을 얻는 프로그램을 작성해보세요.

예를 들어 $N = 4$이며 다음과 같이 표가 주어진 경우에 대해 생각해보겠습니다.

| 길이 | 수익 |
| --- | --- |
|$1$|$2$|
|$2$|$9$|
|$3$|$10$|
|$4$|$11$|

막대기를 자르기 않고 팔면 길이 $4$ 막대기 하나를 팔아 수익 $11$을 얻게 되고, 길이 $1$, 길이 $1$, 길이 $1$, 길이 $1$ 이렇게 $4$개로 나눠서 팔게 되면 수익 $8$을 얻게 됩니다. 길이 $1$, 길이 $3$으로 나눠 팔게 되면 수익 $12$를 얻게 되지만, 길이 $2$, 길이 $2$로 나눠 팔게 되면 수익 $18$을 얻게 되어 최대가 됩니다.

[예제 1]
입력:
4
2 9 10 11

출력:
18


[예제 2]
입력:
4
1 1 1 1

출력:
4

"""

N = int(input())
profit = list(map(int, input().split()))

# Please write your code here.

dp = [0] * (N + 1)
profit = [0] + profit
for length in range(len(profit)):
    cur_profit = profit[length]
    for i in range(N + 1):
        cur = length + i

        if cur <= N:
            dp[cur] = max(dp[cur], dp[i] + cur_profit)


# print(dp)
print(dp[N])
