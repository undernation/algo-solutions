"""
SWEA 99997  [SSAFY A형 1번 복원] 충전소 설치 (2026-09-15)

풀이일 : 2026-09-15   결과: 품
한도   : time 50개 테스트케이스 합산 약 10초 (응시자 기억) / time_sec 10 / memory 미확인 (원문 미제공) / time_source participant_recollection / time_is_approximate True / time_scope all_testcases / remembered_testcase_count 50
제약   : 시간 제한: 50개 테스트케이스 합산 약 10초 (응시자 기억).
제약   : 정확한 시간 및 언어별 차등 여부, 메모리 제한과 전체 입력 제한은 미확인이다.
제약   : 다음 입력 범위는 제공 테스트케이스에서 관찰한 값이며, 원문의 최대 제한을 뜻하지 않는다.
제약   : 코드에 명시된 충전소 설치 좌표: -15 ≤ x, y ≤ 15인 정수 좌표.
제약   : 제공 입력: T=5, N은 2~10, 허용 거리 d는 1~11.
제약   : T·N·d의 원문 상한은 확인되지 않았다.

[채점] accepted  1/1  (3.392s)

[문제]
※ 2026-09-15 SSAFY A형 1번의 제공 코드와 입력으로 복원한 연습 문제입니다.
제목은 복원용이며, 내부 식별자는 SWEA/99997입니다. 공식 SWEA 번호가 아닙니다.
원문과 공식 출력은 제공되지 않았습니다. 원본 output.txt가 비어 있어 아래 예제 출력은 원본 풀이와 독립 구현을 대조해 계산했습니다.

정수 좌표로 나타내는 마을에 N개의 집이 있다. i번째 집의 좌표는 (x_i, y_i)이고, 이 집에서 이용할 수 있는 충전소까지의 최대 거리는 d_i이다.

충전소를 설치할 수 있는 위치는 x좌표와 y좌표가 각각 -15 이상 15 이하인 정수 좌표이다. 집이 있는 위치에는 충전소를 설치할 수 없다. 충전소를 두 개 설치할 때는 서로 다른 위치에 설치해야 한다.

집 (x, y)와 충전소 (a, b) 사이의 거리는 맨해튼 거리 |x-a| + |y-b|이다. 각 집은 설치된 충전소 중 가장 가까운 곳을 이용한다. 모든 집이 충전소를 이용하려면 각 집에서 가장 가까운 충전소까지의 거리가 그 집의 d_i 이하여야 한다. 한 충전소를 이용하는 집의 수에는 제한이 없다.

다음 우선순위에 따라 충전소를 최대 두 개 설치하려고 한다.

1. 충전소 하나로 모든 집의 거리 조건을 만족시킬 수 있다면 반드시 하나만 설치한다.
2. 하나로 불가능할 때만 두 개를 설치한다.
3. 위에서 결정한 설치 개수 안에서, 각 집과 가장 가까운 충전소 사이의 거리 합이 최소가 되도록 한다.

구해야 하는 값은 이때의 최소 거리 합이다. 충전소 두 개로도 모든 집의 거리 조건을 만족시킬 수 없다면 -1을 출력한다.

설치 개수를 줄이는 것이 거리 합을 줄이는 것보다 우선한다. 따라서 두 개를 설치하면 더 짧은 거리 합을 얻을 수 있더라도, 하나로 가능하다면 하나를 설치한 결과를 출력한다.

[예제 1]
입력:
5
2
-2 0 1
1 3 2
2
-1 -1 1
1 0 2
10
3 5 4
2 6 8
7 4 10
6 6 11
3 3 3
5 2 8
0 5 10
4 7 9
6 2 5
1 1 10
5
-1 -2 1
4 -2 1
7 9 2
10 10 3
0 3 1
8
1 1 8
-3 1 8
-4 0 4
3 3 6
-1 1 6
-4 4 7
-3 5 4
-1 -2 4

출력:
#1 2
#2 3
#3 36
#4 -1
#5 21

"""


from itertools import combinations


'''
  여러 개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
'''

T = int(input())
for test_case in range(1, T + 1):
    INF = 10 ** 18
    N = int(input())
    houses_set = set()
    house_info = dict()

    for n in range(N):
        x, y, d = map(int, input().split())
        houses_set.add((x, y))
        house_info[(x, y)] = d


    def calc_dist(sx, sy, ex, ey):
        return abs(sx - ex) + abs(sy - ey)


    charger_pos = []

    for x in range(-15, 16):
        for y in range(-15, 16):
            charger_pos.append([x, y])

    answer = INF

    # 완탐
    # 충전기 1개
    for x, y in charger_pos:
        if (x, y) in houses_set:
            continue
        temp = 0

        is_provide = True
        # 충전소 완탐
        for house_pos, house_dist in house_info.items():
            cur_house_x = house_pos[0]
            cur_house_y = house_pos[1]
            cur_dist = house_dist
            calced_dist = calc_dist(cur_house_x, cur_house_y, x, y)
            if calced_dist > cur_dist:
                is_provide = False
                break
            temp += calced_dist


        if is_provide:
            answer = min(answer, temp)

    if answer == INF:
        # 충전기 2개 처리 필요.

        for combi in combinations(charger_pos, 2):
            charger1 = combi[0]
            charger2 = combi[1]
            charger1_x, charger1_y = charger1
            charger2_x, charger2_y = charger2

            if ((charger1_x, charger1_y) in houses_set) or ((charger2_x, charger2_y) in houses_set):
                continue

            temp = 0
            is_provide = True
            for house_pos, house_dist in house_info.items():
                cur_house_x = house_pos[0]
                cur_house_y = house_pos[1]
                cur_dist = house_dist

                # 둘중에 가까운거 확인, 가까운게 cur_dist 보다 크면 break

                first_dist = calc_dist(cur_house_x, cur_house_y, charger1_x, charger1_y)
                second_dist = calc_dist(cur_house_x, cur_house_y, charger2_x, charger2_y)

                min_val = min(first_dist, second_dist)

                if min_val > cur_dist:
                    is_provide = False
                    break

                temp += min_val

            if is_provide:
                answer = min(answer, temp)

    if answer == INF:
        answer = -1

    # 표준출력(화면)으로 답안을 출력합니다.
    print(f"#{test_case} {answer}")
