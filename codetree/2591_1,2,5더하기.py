"""
CT 2591  1, 2, 5 더하기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-1-2-5-plus/description

풀이일 : 2026-10-12   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 64 MB / time_sec 1
난이도 : Easy  |  정답률 62.4%
제약   : - $1 \le N \le 1\,000$

[채점] accepted  2/2  (0.573s)

[문제]
정수 $N$을 $1$, $2$, $5$의 합으로 나타내는 방법의 수를 구하는 프로그램을 작성해보세요. 단, 더해지는 순서가 다르면 다른 조합이라 생각합니다.

예를 들어 $5$는 다음과 같이 $9$가지 방법으로 나타낼 수 있습니다.

```
1 + 1 + 1 + 1 + 1
1 + 1 + 1 + 2
1 + 1 + 2 + 1
1 + 2 + 1 + 1
1 + 2 + 2
2 + 1 + 1 + 1
2 + 1 + 2
2 + 2 + 1
5
```

단, 합을 나타낼 때는 수를 $1$개 이상 사용해야 합니다.

[예제 1]
입력:
5

출력:
9


[예제 2]
입력:
6

출력:
15

"""

N = int(input())

# Please write your code here.

dp = [0] * (N + 1)
dp[0] = 1

num_list = [1, 2, 5]

for i in range(1, N + 1):

    for num in num_list:

        if i - num >= 0:
            dp[i] += dp[i - num]
            dp[i] %= 10007

print(dp[N])
