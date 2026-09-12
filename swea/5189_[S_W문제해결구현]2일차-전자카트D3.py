"""
SWEA 5189  [S/W 문제해결 구현] 2일차 - 전자카트 D3
https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AWTtmmdKeD8DFAVT

풀이일 : 2026-09-12   결과: 품
한도   : time 10개 테스트케이스를 합쳐서 Python의 경우 2초 / memory 힙, 정적 메모리 합쳐서 256MB 이내, 스택 메모리 1MB 이내 / time_sec 2
난이도 : Master  |  정답률 75.37%

[채점] accepted  1/1  (0.241s)

[문제]
골프장 관리를 위해 전기 카트로 사무실에서 출발해 각 관리구역을 돌고 다시 사무실로 돌아와야 한다.

사무실에서 출발해 각 구역을 한 번씩만 방문하고 사무실로 돌아올 때의 최소 배터리 사용량을 구하시오.

각 구역을 이동할 때의 배터리 사용량은 표로 제공되며, 1번은 사무실을, 2번부터 N번은 관리구역 번호이다.

두 구역 사이도 갈 때와 올 때의 경사나 통행로가 다를 수 있으므로 배터리 소비량은 다를 수 있다.

N이 3인 경우 가능한 경로는 1-2-3-1, 1-3-2-1이며 각각의 배터리 소비량은 다음과 같이 계산할 수 있다.

e[1][2]+e[2][3]+e[3][1] = 18+55+18 = 91

e[1][3]+e[3][2]+e[2][1] = 34+7+48 = 89

 

e

	

1

	

2

	

3

	

도착

1

	

0

	

18

	

34

	

 

2

	

48

	

0

	

55

	

 

3

	

18

	

7

	

0

	

 

출발

	

 

	

 

	

 

	

 

이 경우 최소 소비량은 89가 된다.

[예제 1]
입력:
3
3
0 18 34
48 0 55
18 7 0
4
0 83 65 97
82 0 78 6
19 19 0 82
6 34 94 0
5
0 9 26 85 42
14 0 84 31 27
58 88 0 16 46
83 61 94 0 17
40 71 24 38 0
출력:
#1 89
#2 96
#3 139
"""

T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    N = int(input())
    board = [list(map(int, input().split())) for _ in range(N)]
    memo = {}
    MAX = (1 << N) - 1
    INF = 10 ** 18


    def dfs(mask, last):
        if mask == MAX:
            return board[last][0]

        ret = INF
        if (mask, last) in memo:
            return memo[(mask, last)]
        for nxt in range(N):
            if mask & (1 << nxt):
                continue
            ret = min(ret, board[last][nxt] + dfs(mask | (1 << nxt), nxt))

        memo[(mask, last)] = ret
        # print(ret)
        return ret
    answer = dfs(1, 0)
    print(f"#{test_case} {answer}")
