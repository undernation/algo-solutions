"""
CT 2599  동일하게 분할
https://www.codetree.ai/ko/trails/complete/curated-cards/test-equal-partition/description

풀이일 : 2026-10-14   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 192 MB / time_sec 1
난이도 : Easy  |  정답률 55.4%
제약   : - $2 \le N \le 100$
제약   : - $1 \le \texttt{주어지는 정수} \le 1\,000$

[채점] accepted  2/2  (0.511s)

[문제]
$N$개의 정수가 주어졌을 때 이를 정확히 $2$개의 그룹 $A$, $B$로 나누어 $A$에 들어있는 수들의 합과 $B$에 들어있는 수들의 합이 일치하도록 하는 프로그램을 작성해보세요. 단, 주어진 $N$개의 수는 각각 $A$ 또는 $B$ 중 정확히 한 곳에만 속해야 하며, 각 그룹은 최소 $1$개 이상의 수를 포함하고 있어야 함에 유의합니다.

[예제 1]
입력:
4
2 2 1 5

출력:
Yes


[예제 2]
입력:
5
4 7 8 9 5

출력:
No

"""

N = int(input())
arr = list(map(int, input().split()))

# Please write your code here.

dp = set()
total = sum(arr)

dp.add(0)

for num in arr:
    nxt_dp = dp.copy()

    for nxt in dp:
        nxt_dp.add(nxt + num)

    dp = nxt_dp

# print(dp)

if total / 2 in dp:
    print("Yes")
else:
    print("No")
