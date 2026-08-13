"""
SWEA 2105  [모의 SW 역량테스트] 디저트 카페
https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AV5VwAr6APYDFAWu

풀이일 : 2026-08-13   결과: 품
한도   : time 50개 테스트케이스를 합쳐서 C의 경우 3초 / C++의 경우 3초 / Java의 경우 3초 / Python의 경우 15초 / memory 힙, 정적 메모리 합쳐서 256MB 이내, 스택 메모리 1MB 이내 / time_sec 15
난이도 : Master  |  정답률 67.12%
제약   : 1. 시간제한 : 최대 50개 테스트 케이스를 모두 통과하는 데 C/C++/Java 모두 3초
제약   : 2. 디저트 카페가 모여있는 지역의 한 변의 길이 N은 4 이상 20 이하의 정수이다. (4 ≤ N ≤ 20)
제약   : 3. 디저트 종류를 나타나는 수는 1 이상 100 이하의 정수이다.

[채점] accepted  1/1  (0.505s)

[문제]
※ SW Expert 아카데미의 문제를 무단 복제하는 것을 금지합니다.

친구들과 디저트 카페 투어를 할 계획이다.

[Fig. 1]과 같이 한 변의 길이가 N인 정사각형 모양을 가진 지역에 디저트 카페가 모여 있다.

 

[[IMG:1]]

원 안의 숫자는 해당 디저트 카페에서 팔고 있는 디저트의 종류를 의미하고

카페들 사이에는 대각선 방향으로 움직일 수 있는 길들이 있다.

디저트 카페 투어는 어느 한 카페에서 출발하여

[Fig. 2]와 같이 대각선 방향으로 움직이고 사각형 모양을 그리며 출발한 카페로 돌아와야 한다.

 

 

[[IMG:2]]

디저트 카페 투어를 하는 도중 해당 지역을 벗어나면 안 된다.

또한, 친구들은 같은 종류의 디저트를 다시 먹는 것을 싫어한다.

즉, [Fig. 3]과 같이 카페 투어 중에 같은 숫자의 디저트를 팔고 있는 카페가 있으면 안 된다.

 

 

[[IMG:3]]

[Fig. 4]와 같이 하나의 카페에서 디저트를 먹는 것도 안 된다.

 

[[IMG:4]]

[Fig. 5]와 같이 왔던 길을 다시 돌아가는 것도 안 된다.

 

[[IMG:5]]

 

친구들과 디저트를 되도록 많이 먹으려고 한다.

디저트 가게가 모여있는 지역의 한 변의 길이 N과 디저트 카페의 디저트 종류가 입력으로 주어질 때,

임의의 한 카페에서 출발하여 대각선 방향으로 움직이고

서로 다른 디저트를 먹으면서 사각형 모양을 그리며 다시 출발점으로 돌아오는 경우,

디저트를 가장 많이 먹을 수 있는 경로를 찾고, 그 때의 디저트 수를 정답으로 출력하는 프로그램을 작성하라.

만약, 디저트를 먹을 수 없는 경우 -1을 출력한다.

[예시]

한 변의 길이 N이 4인 지역에 디저트 카페가 [Fig. 6]과 같이 있다고 생각하자.

 

[[IMG:6]]

디저트 카페 투어가 가능한 경우는 [Fig. 7]과 같이 5가지로 나눌 수 있다.

(출발한 곳과 도는 방향은 다를 수 있지만, 디저트 카페 투어의 경로가 그리는 사각형 모양은 5가지 중 하나이다.)

 

[[IMG:7]]

[Fig. 7]

 

이 중에 디저트를 가장 많이 먹을 수 있는 경우는 ⑤인 경우로 디저트의 종류는 6개이다.

따라서, 정답은 6이 된다.

[예제 1]
입력:
10
4
9 8 9 8
4 6 9 4
8 7 7 8
4 5 3 5
5
8 2 9 6 6
1 9 3 3 4
8 2 3 3 6
4 3 4 4 9
7 4 6 3 5
6
1 8 9 6 3 9
5 3 1 9 8 2
6 9 3 4 1 2
7 1 1 5 1 9
1 9 6 8 7 3
7 6 4 5 5 5
7
7 4 1 5 1 7 9
9 4 6 1 4 6 8
9 6 4 8 4 7 4
3 2 6 2 4 2 8
4 9 4 6 2 4 7
1 7 6 8 9 5 8
1 9 4 7 2 9 7
8
18 18 7 16 15 3 5 6
3 6 8 3 15 13 15 2
4 1 11 17 3 4 3 17
16 2 18 10 2 3 11 12
11 17 16 2 9 16 5 4
17 7 6 16 16 11 15 8
2 1 7 18 12 11 6 2
13 12 12 15 9 11 12 18
9
12 3 10 8 11 12 5 3 11
8 6 4 9 8 2 4 7 6
6 10 12 8 3 8 11 3 3
6 10 5 5 5 11 8 10 2
5 13 3 7 5 6 5 12 6
6 1 5 4 4 13 8 7 2
12 7 13 3 5 1 11 7 3
13 12 7 5 6 12 12 9 6
1 12 13 13 11 3 4 10 9
10
18 8 21 24 8 4 20 15 14 23
17 22 3 14 3 19 19 7 6 13
2 26 10 10 10 7 18 14 15 17
13 25 7 20 18 21 8 2 4 24
4 3 1 5 15 3 15 12 22 23
19 22 9 17 6 9 22 26 2 5
12 13 19 13 6 2 12 19 24 8
21 21 24 15 4 1 20 13 14 5
6 10 17 13 7 4 22 16 9 7
17 8 12 11 20 13 5 24 11 3
11
19 1 20 18 8 11 21 11 4 19 14
14 17 6 10 19 3 5 9 18 20 7
4 8 9 3 3 1 3 17 3 19 21
20 19 13 21 20 17 5 21 15 3 10
18 1 7 16 19 21 15 8 7 17 5
21 1 3 11 14 4 15 10 14 15 17
5 15 5 12 16 5 15 14 8 11 5
14 18 2 19 19 8 5 7 11 11 1
20 9 13 8 16 4 21 20 12 16 1
9 11 7 18 5 19 5 18 13 18 20
5 16 1 12 6 15 8 15 3 18 7
14
11 31 22 3 36 20 10 23 6 5 22 22 19 29
9 7 13 9 31 15 7 1 13 33 11 24 7 36
21 22 6 19 23 4 6 21 14 36 9 4 30 21
17 2 30 13 26 36 2 13 32 27 36 5 28 16
8 20 12 16 31 10 32 15 19 24 34 20 1 16
17 18 22 3 10 2 30 26 27 29 10 16 24 12
25 32 31 20 10 29 19 11 32 23 28 20 33 24
9 13 19 4 6 27 24 5 16 2 8 34 2 7
21 5 5 26 2 35 7 36 21 22 23 33 2 6
16 21 15 21 12 11 13 28 3 3 14 23 16 4
1 31 35 33 23 29 12 18 24 25 19 33 17 13
29 6 30 19 33 14 35 14 6 23 27 16 12 24
26 31 30 10 16 21 7 4 16 25 31 19 21 8
12 5 2 4 4 27 29 2 18 20 19 26 32 31
20
11 34 7 49 59 88 79 12 63 38 13 27 9 70 97 92 86 95 84 18
11 84 39 44 86 86 59 52 61 97 81 94 92 78 32 7 5 62 41 75
15 61 71 27 3 4 79 51 95 99 73 27 75 31 4 7 15 51 50 16
6 81 32 61 75 24 36 26 57 55 52 15 35 44 30 25 2 54 12 25
42 4 66 1 23 44 1 7 63 27 82 70 40 45 4 3 12 35 11 85
97 55 69 49 34 79 37 69 89 66 85 22 23 88 24 79 1 48 85 72
4 67 23 3 27 18 37 61 7 68 88 80 35 21 42 88 38 10 81 84
78 86 21 50 46 13 50 9 54 3 1 94 85 75 80 45 31 100 29 70
9 59 7 48 81 82 43 68 90 37 26 41 84 31 58 42 4 96 86 20
22 4 49 94 74 42 6 38 84 90 29 95 84 36 18 4 10 34 71 26
46 43 7 88 18 21 96 57 3 72 52 83 50 53 56 51 19 50 57 6
15 30 88 26 49 10 6 12 98 81 47 88 82 2 68 85 62 12 92 88
100 31 5 15 76 84 39 10 52 61 28 12 50 22 35 85 1 83 2 76
17 27 83 45 18 4 95 37 23 96 58 49 36 47 13 10 41 38 37 6
22 92 59 68 51 15 65 88 18 69 40 49 7 11 78 14 95 94 45 27
13 36 33 22 29 49 11 10 50 91 15 71 87 83 63 26 76 89 28 9
98 9 96 58 72 79 28 9 63 67 85 16 40 66 46 47 17 85 16 99
42 87 28 97 60 89 92 90 51 60 96 22 51 95 55 44 16 9 51 69
27 45 53 43 45 52 12 90 86 91 47 39 84 9 21 77 69 56 5 69
99 47 66 91 71 2 9 26 43 54 52 30 4 94 97 92 2 67 12 85
출력:
#1 6
#2 -1
#3 4
#4 4
#5 8
#6 6
#7 14
#8 12
#9 18
#10 30
"""

T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    N = int(input())

    board = [list(map(int, input().split())) for _ in range(N)]
    answer = -1

    # 특정 위치에서 출발,
    # 방향은 어차피 상관없음
    # 직사각형임.

    def check_length(sy, sx):
        # 오른쪽 아래로 얼마나 갈수있는지 체크
        dy = 1
        dx = 1
        right_cnt = 0
        cy = sy
        cx = sx

        while True:
            ny = cy + dy
            nx = cx + dx
            if not (0 <= ny < N and 0 <= nx < N):
                break
            right_cnt += 1
            cy = ny
            cx = nx

        left_cnt = 0
        dy = 1
        dx = -1
        cy = sy
        cx = sx
        while True:
            ny = cy + dy
            nx = cx + dx
            if not (0 <= ny < N and 0 <= nx < N):
                break
            left_cnt += 1
            cy = ny
            cx = nx

        return right_cnt, left_cnt

    def check_ok(sy, sx, right_cnt, left_cnt):
        dy = 1
        dx = 1
        ny = sy + dy * right_cnt
        nx = sx + dx * right_cnt
        if not (0 <= ny < N and 0 <= nx < N):
            return False
        dy = 1
        dx = -1
        ny = sy + dy * left_cnt
        nx = sx + dx * left_cnt
        if not (0 <= ny < N and 0 <= nx < N):
            return False
        dy = 1
        dx = 1
        dy2 = 1
        dx2 = -1
        ny = sy + dy * right_cnt + dy2 * left_cnt
        nx = sx + dx * right_cnt + dx2 * left_cnt
        if not (0 <= ny < N and 0 <= nx < N):
            return False
        return True

    def check(sy, sx, right_cnt, left_cnt):
        cnt = 1

        desserts = {}
        desserts[board[sy][sx]] = 1
        dy = 1
        dx = 1
        cy = sy
        cx = sx
        temp_right_cnt = right_cnt
        while temp_right_cnt > 0:
            ny = cy + dy
            nx = cx + dx
            # print("debug N ny, nx first right",N, ny, nx, temp_right_cnt)
            key = board[ny][nx]
            if desserts.get(key, -1) == 1:
                return False
            else:
                desserts[key] = 1
            cy = ny
            cx = nx
            temp_right_cnt -= 1
            cnt += 1
        # 첫번 째 턴
        dy = 1
        dx = -1
        temp_left_cnt = left_cnt
        while temp_left_cnt > 0:
            ny = cy + dy
            nx = cx + dx
            # print("debug N ny, nx first left",N, ny, nx, temp_left_cnt)
            key = board[ny][nx]
            if desserts.get(key, -1) == 1:
                return False
            else:
                desserts[key] = 1
            cy = ny
            cx = nx
            temp_left_cnt -= 1
            cnt += 1
        dy = -1
        dx = -1
        temp_right_cnt = right_cnt
        while temp_right_cnt > 0:
            ny = cy + dy
            nx = cx + dx
            key = board[ny][nx]
            if desserts.get(key, -1) == 1:
                return False
            else:
                desserts[key] = 1
            cy = ny
            cx = nx
            temp_right_cnt -= 1
            cnt += 1
        # 첫번 째 턴
        dy = -1
        dx = 1
        temp_left_cnt = left_cnt - 1
        while temp_left_cnt > 0:
            ny = cy + dy
            nx = cx + dx
            key = board[ny][nx]
            if desserts.get(key, -1) == 1:
                return False
            else:
                desserts[key] = 1
            cy = ny
            cx = nx
            temp_left_cnt -= 1
            cnt += 1
        return cnt

    for i in range(N):
        for j in range(N):
            right_cnt, left_cnt = check_length(i, j)
            if right_cnt == 0 or left_cnt == 0:
                continue
            else:
                for right in range(1, right_cnt + 1):
                    for left in range(1, left_cnt + 1):
                        if check_ok(i, j, right, left):
                            # print("debug i, j", i, j)
                            ret = check(i, j, right, left)
                            if ret == False:
                                pass
                            else:
                                if ret > answer:
                                    # if test_case == 1:
                                    # print("debug", i, j)
                                    answer = max(answer, ret)


    print(f"#{test_case} {answer}")
