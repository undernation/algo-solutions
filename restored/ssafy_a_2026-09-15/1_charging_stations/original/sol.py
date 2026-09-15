import sys
sys.stdin = open('input.txt', 'r')


def solve():
    # N = 3 = 0b111 
    full_mask = (1 << N) - 1
    candidates = []

    # 집이 있는 좌표
    house_positions = {(x, y) for x, y, d in data}

    # 마을 전체 좌표는 -15 ~ 15
    for station_x in range(-15, 16):
        for station_y in range(-15, 16):
            # 집이 있는 위치에는 충전소 설치 불가
            if (station_x, station_y) in house_positions:
                continue
            dist = []
            mask = 0
            for idx, (x, y, d) in enumerate(data):
                # 맨해튼 거리
                distance = abs(station_x - x) + abs(station_y - y)
                dist.append(distance)
                # 해당 집의 허용 거리 이내
                if distance <= d:
                    # 현재 집이 2번 인덱스라면 
                        # idx = 2 = 0b100
                        # mask = 0b100 
                    # 그 다음 집이 3번 인덱스면
                        # idx = 3 = 0b1000
                        # mask = 0b1100 (이전 집들을 커버한 비트들도 그대로 유지됨)
                    mask |= 1 << idx
            candidates.append((dist, mask))


    # 1. 충전소 1개로 모든 집을 커버할 수 있는지 검사
    min_v = float('inf')
    for dist, mask in candidates:
        if mask == full_mask:
            result = sum(dist)
            min_v = min(min_v, result)

    # 하나라도 가능하면 반드시 충전소 1개만 설치
    if min_v != float('inf'):
        return min_v

    # 2. 1개로 불가능한 경우에만 충전소 2개 검사
    min_v = float('inf')
    for first_idx in range(len(candidates) - 1):
        fd, fm = candidates[first_idx]
        for second_idx in range(first_idx + 1, len(candidates)):
            sd, sm = candidates[second_idx]
            # 두 충전소를 합쳐도 모든 집을 커버하지 못함
            if (fm | sm) != full_mask:
                continue
            result = 0
            for idx in range(N):
                # 두 충전소 중 가까운 곳과의 거리
                result += min(fd[idx], sd[idx])
                # 가지치기
                if result >= min_v:
                    break
            else:
                min_v = result

    # 2개로도 모든 집을 커버할 수 없음
    if min_v == float('inf'):
        return -1

    return min_v


T = int(input())

for tc in range(1, T + 1):
    N = int(input())
    data = [list(map(int, input().split())) for _ in range(N)]

    result = solve()
    print(f'#{tc} {result}')