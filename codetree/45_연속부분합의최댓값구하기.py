"""
CT 45  연속 부분 합의 최댓값 구하기
https://www.codetree.ai/ko/trails/complete/curated-cards/intro-max-of-partial-sum/description

풀이일 : 2026-10-14   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Easy  |  정답률 62.9%
제약   : - $1 \le N \le 100\,000$
제약   : - $-1\,000 \le \texttt{정수} \le 1\,000$

[채점] accepted  2/2  (0.577s)

[문제]
$N$개의 정수가 입력으로 주어지고, 이 중 연속한 부분 수열에 속한 원소들의 합이 최대가 될 때의 값을 출력하는 코드를 작성해보세요. (단, 부분 수열은 최소 한 개 이상의 원소를 포함합니다.)

[예제 1]
입력:
7
4 -1 2 -19 3 6 9

출력:
18


[예제 2]
입력:
2
-2 -1

출력:
-1

"""

N = int(input())
arr = list(map(int, input().split()))

# Please write your code here.

MIN_INF = -float('inf')

dp = [MIN_INF] * N

dp[0] = arr[0]

for i in range(1, N):
    dp[i] = max(arr[i], dp[i - 1] + arr[i])

print(max(dp))
