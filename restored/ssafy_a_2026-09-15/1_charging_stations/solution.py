"""SSAFY A형 1번 복원: 충전소 설치.

GitLab 제공 풀이의 규칙을 따르는 표준 입력용 구현이다.
공식 정답/시험 통과를 뜻하지 않는다. 원본은 original/에 보관한다.
"""

import sys


def solve(houses):
    occupied = {(x, y) for x, y, _ in houses}
    full = (1 << len(houses)) - 1
    candidates = []
    one_station = float("inf")

    for sx in range(-15, 16):
        for sy in range(-15, 16):
            if (sx, sy) in occupied:
                continue
            distances = [abs(sx - x) + abs(sy - y) for x, y, _ in houses]
            mask = 0
            for i, (_, _, limit) in enumerate(houses):
                if distances[i] <= limit:
                    mask |= 1 << i
            if mask == full:
                one_station = min(one_station, sum(distances))
            # 한 집도 맡을 수 없는 후보는 2개로 덮을 때도 필요 없다.
            if mask:
                candidates.append((distances, mask))

    # 거리 합보다 설치 개수 최소화가 우선이다.
    if one_station != float("inf"):
        return one_station

    best = float("inf")
    for a, (da, ma) in enumerate(candidates):
        for b in range(a + 1, len(candidates)):
            db, mb = candidates[b]
            if (ma | mb) != full:
                continue
            total = 0
            for x, y in zip(da, db):
                total += min(x, y)
                if total >= best:
                    break
            else:
                best = total
    return -1 if best == float("inf") else best


def main():
    values = iter(map(int, sys.stdin.buffer.read().split()))
    t = next(values)
    output = []
    for case in range(1, t + 1):
        n = next(values)
        houses = [tuple(next(values) for _ in range(3)) for _ in range(n)]
        output.append(f"#{case} {solve(houses)}")
    print("\n".join(output))


if __name__ == "__main__":
    main()
