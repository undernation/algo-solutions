"""
CT 2030  자주 등장한 top K 숫자
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-top-k-frequent-elements/description

풀이일 : 2026-10-31   결과: 품
한도   : time Python3 1초 · C++17 1초 / memory 80 MB / time_sec 1
난이도 : Medium  |  정답률 60.5%
제약   : - $1 \le K \le N \le 100\,000$
제약   : - $1 \le \texttt{주어지는 원소 값} \le 10^9$

[채점] accepted  1/1  (0.369s)

[문제]
$N$개의 숫자가 주어졌을 때, 자주 등장한 순으로 $K$개의 숫자를 출력하는 프로그램을 작성해보세요.

[예제 1]
입력:
5 2
1 1 3 2 3

출력:
3 1

"""

from collections import defaultdict

N, K = map(int, input().split())
arr = list(map(int, input().split()))

# Please write your code here.
temp = defaultdict(int)
for num in arr:
    temp[num] += 1
num_list = []
for key, value in temp.items():
    num_list.append((-value, -key))

num_list.sort()

for i in range(K):
    print(-num_list[i][1], end= " ")
