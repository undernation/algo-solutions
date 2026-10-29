"""
CT 2031  수 등장 횟수
https://www.codetree.ai/ko/trails/complete/curated-cards/intro-number-frequency/description

풀이일 : 2026-10-29   결과: 품
한도   : time Python3 1초 · C++17 1초 / memory 80 MB / time_sec 1
난이도 : Easy  |  정답률 77.8%
제약   : - $1 \le M \le N \le 100\,000$
제약   : - $1 \le \texttt{주어지는 원소, 수 값} \le 10^9$

[채점] accepted  1/1  (0.397s)

[문제]
$N$개의 수로 이루어진 수열 정보가 하나 주어졌을 때, $M$번에 걸쳐 특정 수가 주어지면 해당 수가 수열에 몇 개 있는지를 출력하는 프로그램을 작성해보세요.

[예제 1]
입력:
5 2
1 1 3 2 3
1 4

출력:
2 0

"""

N, M = map(int, input().split())
arr = list(map(int, input().split()))
nums = list(map(int, input().split()))

# Please write your code here.
from collections import defaultdict
ddict = defaultdict(int)
for i in arr:
    ddict[i] += 1

for num in nums:
    print(ddict[num], end = " ")
