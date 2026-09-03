"""
SWEA 4831  [S/W 문제해결 기본] 1일차 - 전기버스 D3
https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AWTLS24ao9ADFAVT

풀이일 : 2026-09-03   결과: 품
한도   : time 10개 테스트케이스를 합쳐서 Python의 경우 2초 / memory 힙, 정적 메모리 합쳐서 256MB 이내, 스택 메모리 1MB 이내 / time_sec 2
난이도 : Master  |  정답률 50.22%

[채점] accepted  1/1  (0.219s)

[문제]
※ SW Expert 아카데미의 문제를 무단 복제하는 것을 금지합니다.

A도시는 전기버스를 운행하려고 한다. 전기버스는 한번 충전으로 이동할 수 있는 정류장 수가 정해져 있어서, 중간에 충전기가 설치된 정류장을 만들기로 했다.

버스는 0번에서 출발해 종점인 N번 정류장까지 이동하고, 한번 충전으로 최대한 이동할 수 있는 정류장 수 K가 정해져 있다.

충전기가 설치된 M개의 정류장 번호가 주어질 때, 최소한 몇 번의 충전을 해야 종점에 도착할 수 있는지 출력하는 프로그램을 만드시오.

만약 충전기 설치가 잘못되어 종점에 도착할 수 없는 경우는 0을 출력한다. 출발지에는 항상 충전기가 설치되어 있지만 충전횟수에는 포함하지 않는다.

 

[예시]

[[IMG:1]]

다음은 K = 3, N = 10, M = 5, 충전기가 설치된 정류장이 1, 3, 5, 7, 9인 경우의 예이다.

[예제 1]
입력:
3
3 10 5
1 3 5 7 9
3 10 5
1 3 7 8 9
5 20 5
4 7 9 14 17
출력:
#1 3
#2 0
#3 4
"""

import sys
from bisect import bisect_right

T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    K, N, M = map(int, input().split())
    num_list = list(map(int, input().split()))
    idx = 0
    cnt = 0
    while idx < N:
        # 현재 충전량으로 갈수 있는 최대한 먼 거리
        # print("debug idx", idx)
        nxt_pos = idx + K

        if nxt_pos >= N:
            break
        else:
            nxt_idx = bisect_right(num_list, nxt_pos) - 1
            # print("nxt_idx", nxt_idx)
            cnt += 1
            if num_list[nxt_idx] == idx:
                cnt = 0
                break
            else:
                idx = num_list[nxt_idx]

    print(f"#{test_case} {cnt}")
