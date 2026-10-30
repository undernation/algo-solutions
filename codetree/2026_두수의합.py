"""
CT 2026  두 수의 합
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-sum-of-two-num/description

풀이일 : 2026-10-30   결과: 틀림
한도   : time Python3 1초 · C++17 1초 / memory 80 MB / time_sec 1
난이도 : Medium  |  정답률 37.8%
제약   : - $1 \le N \le 100\,000$
제약   : - $-2^{31} \le K \le 2^{31}-1$
제약   : - $-10^9 \le \texttt{정수} \le 10^9$

[문제]
$N$개의 정수가 입력으로 주어지고, 이 중 서로 다른 위치에 있는 두 개의 수를 뽑아 더했을 때 $K$가 되는 가짓수를 구하는 프로그램을 작성해보세요.

[예제 1]
입력:
5 9
4 6 5 3 7

출력:
2

"""

from collections import defaultdict

N, K = map(int, input().split())
arr = list(map(int, input().split()))

# Please write your code here.
ddict = defaultdict(int)
answer = 0

for num in arr:
    ddict[num] += 1

for key, value in ddict.items():
    cur_num = key

    find_num = K - cur_num
    if find_num in ddict:
        # print(cur_num)
        # print(find_num)

        if cur_num == find_num:
            answer += value * (value - 1)
            continue

        answer += value * ddict[find_num]

print(answer// 2)
