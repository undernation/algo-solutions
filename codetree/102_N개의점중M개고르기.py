"""
CT 102  N개의 점 중 M개 고르기
https://www.codetree.ai/ko/trails/complete/curated-cards/test-choose-m-out-of-n-points/description

풀이일 : 2026-10-04   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 49.0%
제약   : - $2 \le M \le N \le 20$
제약   : - $1 \le x_i,\ y_i \le 100$ $(1 \le i \le N)$
제약   : - 주어지는 모든 점의 위치는 서로 다릅니다.

[채점] accepted  2/2  (0.523s)

[문제]
좌표 평면 위에 점 $N$개의 좌표가 주어졌을 때, 점 $M$개를 적절히 선택하여 선택한 점들 중 거리가 가장 먼 두 점 사이의 거리값이 최소가 되도록 하는 프로그램을 작성해주세요.  
단 여기서의 거리란 유클리디안 거리를 뜻합니다. 두 점 $(x_1,\ y_1), (x_2,\ y_2)$ 사이의 유클리디안 거리 $dist$는 다음과 같이 정의됩니다.  

$dist = \sqrt{(x_1-x_2)^2 + (y_1 - y_2)^2}$

[예제 1]
입력:
2 2
1 1
1 3

출력:
4


[예제 2]
입력:
3 2
1 1
4 4
3 5

출력:
2

"""

N, M = map(int, input().split())
points = [tuple(map(int, input().split())) for _ in range(N)]

# Please write your code here.

def calc_dist(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    ret = pow(x1 - x2, 2) + pow(y1 - y2, 2)

    return ret

def calc_min_val(num_list):
    # print("debug", num_list)
    max_dist = 0

    for i in range(M):
        for j in range(i + 1, M):
            cur_dist = calc_dist(num_list[i], num_list[j])
            max_dist = max(max_dist, cur_dist)

    return max_dist

pos_list = []
answer = 10 ** 18
def dfs(idx, cnt):
    global answer, pos_list
    if cnt == M:
        ret = calc_min_val(pos_list)
        # print("ret", ret)
        answer = min(answer, ret)
        return

    if idx == N:
        return

    pos_list.append(points[idx])
    dfs(idx + 1, cnt + 1)
    pos_list.pop()

    dfs(idx + 1, cnt)

dfs(0, 0)
print(answer)
