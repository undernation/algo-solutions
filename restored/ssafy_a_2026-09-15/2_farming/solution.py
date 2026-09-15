"""SSAFY A형 2번 복원: 농지 이동과 수확.

원본의 이동 순서와 day + 4 + k 성숙일을 그대로 재현한다.
공식 정답/시험 통과를 뜻하지 않는다. 원본은 original/에 보관한다.
"""

import sys


# 동, 남, 서, 북 (시계 방향)
DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0))


def simulate(grid, days, row, col, facing):
    n = len(grid)
    ready = [[-1 if cell else 0 for cell in line] for line in grid]
    plant_count = [[0] * n for _ in range(n)]
    harvested = 0

    for day in range(1, days + 1):
        next_move = None
        # 오전 작업 전 농장 상태로 오른쪽, 앞, 왼쪽, 뒤를 검사한다.
        for direction in ((facing + 1) % 4, facing, (facing - 1) % 4,
                          (facing + 2) % 4):
            dr, dc = DIRECTIONS[direction]
            nr, nc = row + dr, col + dc
            if 0 <= nr < n and 0 <= nc < n and 0 <= ready[nr][nc] <= day:
                next_move = nr, nc, direction
                break

        if ready[row][col] == 0:
            if next_move is not None:
                plant_count[row][col] += 1
                ready[row][col] = day + 4 + plant_count[row][col]
        elif ready[row][col] <= day:
            harvested += 1
            ready[row][col] = 0

        if next_move is not None:
            row, col, facing = next_move

    return harvested


def solve(grid, days):
    best = 0
    for row, line in enumerate(grid):
        for col, cell in enumerate(line):
            if cell == 0:
                for facing in range(4):
                    best = max(best, simulate(grid, days, row, col, facing))
    return best


def main():
    values = iter(map(int, sys.stdin.buffer.read().split()))
    t = next(values)
    output = []
    for case in range(1, t + 1):
        n, days = next(values), next(values)
        grid = [[next(values) for _ in range(n)] for _ in range(n)]
        output.append(f"#{case} {solve(grid, days)}")
    print("\n".join(output))


if __name__ == "__main__":
    main()
