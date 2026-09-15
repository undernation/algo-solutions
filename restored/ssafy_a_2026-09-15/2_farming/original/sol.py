import sys
sys.stdin = open('input.txt', 'r')

dx = [0, -1, 0, 1]  # 우, 상, 좌, 하
dy = [1, 0, -1, 0]

def can_move(x, y, d, data, day):
    N = len(data)
    directions = {
        0: [3, 0, 1, 2],  # 우 -> 하 우 상 좌
        1: [0, 1, 2, 3],  # 상 -> 우 상 좌 하
        2: [1, 2, 3, 0],  # 좌 -> 상 좌 하 우
        3: [2, 3, 0, 1]   # 하 -> 좌 하 우 상
    }

    for nd in directions[d]:
        nx = x + dx[nd]
        ny = y + dy[nd]
        if not (0 <= nx < N and 0 <= ny < N):
            continue

        harvest_day, cnt = data[nx][ny]

        # 산
        if harvest_day == -1:
            continue
        # 빈 농지
        if harvest_day == 0:
            return nd
        # 곡식이 열린 농지
        if harvest_day <= day:
            return nd
    return -1


def search(x, y, d, data, M):
    result = 0

    for day in range(1, M + 1):
        # 오전 작업 전에 오후에 이동 가능한 곳 확인
        nd = can_move(x, y, d, data, day)
        harvest_day, cnt = data[x][y]

        # 빈 농지
        if harvest_day == 0:
            # 이동할 수 있는 경우 씨 심기
            if nd != -1:
                k = cnt + 1
                # 씨 심기
                # 다음날 싹 + (3 + k)일
                data[x][y] = [day + 4 + k, k]

        # 곡식이 열린 농지
        elif harvest_day <= day:
            result += 1
            # 빈 농지로 변경
            # 지금까지 싹이 난 횟수는 유지
            data[x][y] = [0, cnt]

        # 오후 이동
        if nd != -1:
            x += dx[nd]
            y += dy[nd]
            d = nd

    return result


T = int(input())

for tc in range(1, T + 1):
    N, M = map(int, input().split())
    raw_data = [list(map(int, input().split())) for _ in range(N)]
    # 수확일 계산하기 쉽게 전처리
    data = []

    for x in range(N):
        row = []
        for y in range(N):
            if raw_data[x][y] == 1:
                # 산
                row.append([-1, -1])
            else:
                # [수확 가능 날짜, 해당 농지에서 싹이 난 횟수]
                row.append([0, 0])
        data.append(row)
    result = 0

    for x in range(N):
        for y in range(N):
            # 농지가 아니면 시작 불가
            if data[x][y][0] == -1:
                continue
            for d in range(4):
                # 각각 독립적인 농장 상태에서 시작
                copied_data = [[cell[:] for cell in row] for row in data]
                result = max(result, search(x, y, d, copied_data, M))

    print(f'#{tc} {result}')