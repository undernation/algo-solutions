"""
SWEA 1247  [S/W 문제해결 응용] 3일차 - 최적 경로 D5
https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AV15OZ4qAPICFAYD

풀이일 : 2026-08-14   결과: 품
한도   : time 10개 테스트케이스를 합쳐서 C++의 경우 10초 / Java의 경우 20초 / Python의 경우 30초 / memory 힙, 정적 메모리 합쳐서 256MB 이내, 스택 메모리 1MB 이내 / time_sec 30
난이도 : Master  |  정답률 84.71%
제약   : 고객의 수 N은 2≤N≤10 이다.
제약   : 그리고 회사의 좌표, 집의 좌표를 포함한 모든 N+2개의 좌표는 서로 다른 위치에 있으며 좌표의 값은 0이상 100 이하의 정수로 이루어진다.

[채점] accepted  1/1  (0.604s)

[문제]
삼성전자의 서비스 기사인 김대리는 회사에서 출발하여 냉장고 배달을 위해 N명의 고객을 방문하고 자신의 집에 돌아가려한다.

회사와 집의 위치, 그리고 각 고객의 위치는 이차원 정수 좌표 (x, y)로 주어지고 (0 ≤ x ≤ 100, 0 ≤ y ≤ 100)

두 위치 (x1, y1)와 (x2, y2) 사이의 거리는 |x1-x2| + |y1-y2|으로 계산된다.

여기서 |x|는 x의 절대값을 의미하며 |3| = |-3| = 3이다. 회사의 좌표, 집의 좌표, 고객들의 좌표는 모두 다르다.

회사에서 출발하여 N명의 고객을 모두 방문하고 집으로 돌아오는 경로 중 가장 짧은 것을 찾으려 한다.

회사와 집의 좌표가 주어지고, 2명에서 10명 사이의 고객 좌표가 주어질 때,

회사에서 출발해서 이들을 모두 방문하고 집에 돌아가는 경로 중 총 이동거리가 가장 짧은 경로를 찾는 프로그램을 작성하라.

여러분의 프로그램은 가장 짧은 경로의 이동거리만 밝히면 된다.

이 문제는 가장 짧은 경로를 ‘효율적으로’ 찾는 것이 목적이 아니다.

여러분은 모든 가능한 경로를 살펴서 해를 찾아도 좋다.

모든 경우를 체계적으로 따질 수 있으면 정답을 맞출 수 있다.

[예제 1]
입력:
10
5
0 0 100 100 70 40 30 10 10 5 90 70 50 20
6
88 81 85 80 19 22 31 15 27 29 30 10 20 26 5 14
7
22 47 72 42 61 93 8 31 72 54 0 64 26 71 93 87 84 83
8
30 20 43 14 58 5 91 51 55 87 40 91 14 55 28 80 75 24 74 63
9
3 9 100 100 16 52 18 19 35 67 42 29 47 68 59 38 68 81 80 37 94 92
10
39 9 97 61 35 93 62 64 96 39 36 36 9 59 59 96 61 7 64 43 43 58 1 36
10
26 100 72 2 71 100 29 48 74 51 27 0 58 0 35 2 43 47 50 49 44 100 66 96
10
46 25 16 6 48 82 80 21 49 34 60 25 93 90 26 96 12 100 44 69 28 15 57 63
10
94 83 72 42 43 36 59 44 52 57 34 49 65 79 14 20 41 9 0 39 100 94 53 3
10
32 79 0 0 69 58 100 31 67 67 58 66 83 22 44 24 68 3 76 85 63 87 7 86
출력:
#1 200
#2 304
#3 265
#4 307
#5 306
#6 366
#7 256
#8 399
#9 343
#10 391
"""

T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    N = int(input())
    num_list = list(map(int, input().split()))
    company = [num_list[0], num_list[1]]
    home = [num_list[2], num_list[3]]
    visits = []
    rest = num_list[4:]
    for idx in range(len(rest) // 2):
        visits.append([rest[idx * 2], rest[idx * 2 + 1]])

    

    visits = [company] + visits
    # 비트마스킹 dfs
    # print(visits)
    INF = 10 ** 18

    memo = {}
    def dfs(last, mask):
        global visits
        if str(bin(mask)).count("1") == N + 1:
            # 집으로 돌아가는 거리 리턴하기
            cy, cx = visits[last]
            hy, hx = home
            return abs(cy - hy) + abs(cx - hx)

        key = (last, mask)
        if key in memo:
            return memo[key]
        ret = INF

        for i in range(N + 1):
            if mask & (1 << i):
                continue
            cy, cx = visits[last]
            ny, nx = visits[i]
            # print(dfs(i, mask | (1 << i)))
            ret = min(ret, dfs(i, mask | (1 << i)) + abs(cy - ny) + abs(cx - nx))

        memo[key] = ret
        return ret

    answer = dfs(0, 1)
    print(f"#{test_case} {answer}")
