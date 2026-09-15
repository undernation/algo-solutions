import sys
sys.stdin = open('input.txt', 'r')


def solve(data):
    n = len(data)
    # 집 좌표
    houses = {(x, y) for x, y, d in data}
    # 집이 없는 위치만 충전소 후보
    stations = [(x, y) for x in range(-15, 16) for y in range(-15, 16) if (x, y) not in houses]

    m = len(stations)

    dist_table = [[0] * n for _ in range(m)]
    can_cover = [[False] * n for _ in range(m)]

    for s_idx, (sx, sy) in enumerate(stations):
        for i, (hx, hy, d) in enumerate(data):
            dist = abs(sx - hx) + abs(sy - hy)
            dist_table[s_idx][i] = dist
            can_cover[s_idx][i] = (dist <= d)

    # 1. 충전소 1개로 가능한지 먼저 검사
    min_v = float('inf')
    for s in range(m):
        possible = True
        result = 0

        for i in range(N):
            if not can_cover[s][i]:
                possible = False
                break
            result += dist_table[s][i]
        if possible:
            min_v = min(min_v, result)

    # 1개로 가능하면 반드시 1개만 설치
    if min_v != float('inf'):
        return min_v

    # 2. 1개로 불가능할 때만 2개 검사
    min_v = float('inf')
    for a in range(m - 1):
        dist_a = dist_table[a]
        cover_a = can_cover[a]

        for b in range(a + 1, m):
            dist_b = dist_table[b]
            cover_b = can_cover[b]

            result = 0
            possible = True

            for i in range(N):
                # 두 충전소 모두 허용 거리 밖
                if not cover_a[i] and not cover_b[i]:
                    possible = False
                    break
                # 가까운 충전소까지의 거리
                result += min(dist_a[i], dist_b[i])

                if result >= min_v:
                    possible = False
                    break

            if possible:
                min_v = result


    if min_v == float('inf'):
        return -1

    return min_v


T = int(input())

for tc in range(1, T + 1):
    N = int(input())
    data = [list(map(int, input().split())) for _ in range(N)]

    result = solve(data)
    print(f'#{tc} {result}')