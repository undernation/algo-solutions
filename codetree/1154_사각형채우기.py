"""
CT 1154  사각형 채우기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-rectangle-fill/description

풀이일 : 2026-10-08   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 64 MB / time_sec 1
난이도 : Easy  |  정답률 64.6%
제약   : - $1 \le N \le 1\,000$

[채점] accepted  2/2  (0.5s)

[문제]
$2 \times N$ 크기의 사각형을 $1 \times 2$, $2 \times 1$ 크기의 사각형들로 채우는 방법의 수를 구하는 프로그램을 작성하세요.

예로 $N = 3$일 때는 다음과 같이 3가지 방법이 가능합니다.

![](https://contents.codetree.ai/problems/1154/images/problems-e7978035-da53-4bf7-8a96-311cb9997651.svg)

[예제 1]
입력:
3

출력:
3


[예제 2]
입력:
9

출력:
55

"""

N = int(input())

# Please write your code here.

dp = [0] * (N + 2)

dp[1] = 1

dp[2] = 2

for i in range(3, N + 1):
    dp[i] = (dp[i - 2] + dp[i - 1]) % 10007

print(dp[N])
