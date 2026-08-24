"""
BOJ 11651  좌표 정렬하기 2
https://cosal.aviss.kr/problems/detail/11651

풀이일 : 2026-08-24   결과: 품
한도   : time 1 초 / memory 256 MB

[채점] accepted  15/15  (17.009s)

[문제]
2차원 평면 위의 점 N개가 주어진다. 좌표를 y좌표가 증가하는 순으로, y좌표가 같으면 x좌표가 증가하는 순서로 정렬한 다음 출력하는 프로그램을 작성하시오.

[예제 1]
입력:
5
0 4
1 2
1 -1
2 2
3 3
출력:
1 -1
1 2
2 2
3 3
0 4
"""

import sys

input = sys.stdin.readline

N = int(input())

pos = []
for _ in range(N):
    pos.append(list(map(int, input().split())))
pos.sort(key= lambda x: (x[1], x[0]))
for i in pos:
    print(*i)
