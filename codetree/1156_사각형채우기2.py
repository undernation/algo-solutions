"""
CT 1156  사각형 채우기 2
https://www.codetree.ai/ko/trails/complete/curated-cards/test-rectangle-fill-2/description

풀이일 : 2026-10-09   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 64 MB / time_sec 1
난이도 : Medium  |  정답률 63.9%
제약   : - $1 \le N \le 1\,000$

[채점] accepted  2/2  (0.568s)

[문제]
$2 \times N$ 크기의 사각형을 $1 \times 2$, $2 \times 1$, $2\times 2$ 크기의 사각형들로 채우는 방법의 수를 구하는 프로그램을 작성하세요.

예로 $N = 2$일 때는 다음과 같이 3가지 방법이 가능합니다.

![](https://contents.codetree.ai/problems/1156/images/problems-34cbae9e-ade0-4668-9ef7-ed786ff8ad57.svg)

[예제 1]
입력:
2

출력:
3


[예제 2]
입력:
8

출력:
171

"""

N = int(input())

# Please write your code here.

dp = [0] * (N + 2)

dp[1] = 1
dp[2] = 3

for i in range(3, N + 1):

    dp[i] = (dp[i - 2] * 2 + dp[i - 1]) % 10007

print(dp[N])
