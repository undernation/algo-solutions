"""
SWEA 99996  [삼성 B형 복원] 블록 구역 관리

풀이일 : 2026-09-22   결과: 못품
한도   : time 50개 테스트 케이스 합산 Python 6초 (응시자 기억) / time_sec 6 / memory 미확인 / time_source participant_recollection / time_is_approximate True / time_scope all_testcases / remembered_testcase_count 50 / runtime Python
난이도 : B형 (복원)  |  정답률 ?%
제약   : N 최댓값: 45,000 (기억). 복원본에서는 1 ≤ N ≤ 45,000.
제약   : addBlock: 테스트 케이스당 최대 15,000회로 기억.
제약   : 블록의 내부는 겹치지 않으며 삭제 함수는 없다.
제약   : 블록 ID는 순차적으로 입력된다는 보장이 없다.
제약   : 변의 일부를 공유해도 같은 구역이며, 꼭짓점만 공유하면 그 접촉만으로 연결되지 않는다.
제약   : 블록은 랜덤하게 생성된다 (사용자 재확인). 구체적 분포와 크기 상한 식은 미확인.

[채점] accepted  1/1  (1.295s)

[문제]
※ 삼성 B형 시험의 기억을 바탕으로 작성한 검토용 복원본입니다. 제목과 내부 식별자 SWEA/99996은 아카이브 등록을 위해 정했으며 공식 문제 번호가 아닙니다. 2026-09-19는 복원일입니다. 원문과 공식 예제는 확보하지 못했습니다.

한 변의 길이가 N인 정사각형 보드에 직사각형 블록을 하나씩 추가한다. 처음 보드는 비어 있다. 각 블록에는 고유한 ID가 있으며, 블록을 추가하면서 연결된 구역과 그 순위를 관리해야 한다.

■ 블록의 좌표와 면적

블록은 blockId, x1, y1, x2, y2로 주어진다. (x1, y1), (x2, y2)는 좌표축에 평행한 직사각형의 두 꼭짓점이다. 모든 좌표는 정수이다.

    0 ≤ x1 < x2 ≤ N
    0 ≤ y1 < y2 ≤ N
    면적 = (x2 - x1) × (y2 - y1)

예를 들어 (1, 1)부터 (2, 2)까지의 블록은 면적이 1이다. 두 좌표를 양끝 칸 번호로 세지 않는다.

서로 다른 블록의 내부는 절대로 겹치지 않는다. 블록은 랜덤하게 생성된다. 이 생성 조건은 사용자가 재확인했으며, 구체적인 확률 분포와 블록 크기 상한 식은 미확인이다.

블록 ID는 추가 순서와 무관하다. 예를 들어 20, 7, 15, 3 순서로 들어올 수 있으며, 1부터 차례대로 주어진다는 보장은 없다.

■ 같은 구역이 되는 조건

두 블록이 경계에서 길이가 양수인 선분을 공유하면 같은 구역에 속한다. 변 전체가 일치할 필요 없이 일부만 맞닿아도 된다. 꼭짓점 하나만 닿는 경우에는 그 접촉만으로 같은 구역이 되지 않는다.

블록 A와 B가 연결되고 B와 C가 연결되면, A와 C가 직접 닿지 않아도 세 블록 모두 같은 구역이다. 다른 블록과 닿지 않는 블록도 혼자 하나의 구역을 이룬다.

새 블록이 서로 다른 여러 구역과 맞닿으면, 새 블록과 그 구역들이 하나의 구역으로 합쳐진다. 블록을 삭제하거나 이동하는 함수는 없다.

■ 구역의 정보

구역 ID: 그 구역에 속한 블록 ID 중 최솟값.
구역 면적: 그 구역에 속한 모든 블록의 면적 합계. 블록 사이의 빈 공간은 포함하지 않는다.
블록 수: 그 구역에 속한 블록의 개수.

구역 ID는 구역이 합쳐질 때 바뀔 수 있지만, 각 블록의 고유한 ID는 바뀌지 않는다. 예를 들어 블록 20, 7, 15가 같은 구역이면 구역 ID는 7이다. 이 구역이 블록 3을 포함한 구역과 합쳐지면 새 구역 ID는 3이 된다. 이후에도 블록 20, 7, 15는 각각의 원래 ID로 조회한다.

■ 구현할 함수

init(N)
빈 N × N 보드로 초기화한다. 테스트 케이스가 시작될 때 한 번 호출되며, 이전 테스트의 모든 상태를 초기화한다. 반환값은 없다.

addBlock(blockId, x1, y1, x2, y2) → int
새 블록을 추가하고, 추가가 끝난 뒤 그 블록이 속한 구역의 전체 면적을 반환한다. blockId는 해당 테스트에서 처음 사용하는 양의 정수이다. 새 블록 한 개의 면적이나 구역 ID를 반환하는 것이 아니다.

isSameRegion(blockId1, blockId2) → int
두 인자는 이미 추가된 각 블록의 고유한 ID다. 그 블록들이 조회 시점에 속한 구역을 비교하여, 같은 구역이면 1, 아니면 0을 반환한다. 같은 ID가 두 번 주어지면 1이다.

top10() → Result
현재 존재하는 구역을 아래 순서로 정렬하여 최대 10개의 구역 ID를 반환한다.

    1. 구역 면적 내림차순
    2. 면적이 같으면 블록 수 오름차순
    3. 면적과 블록 수가 모두 같으면 구역 ID 오름차순 (복원본에서 채택한 기준, 원문 미확인)

한 구역은 한 번만 반환한다. 구역이 10개 미만이면 그 개수만, 구역이 없으면 빈 결과를 반환한다. 조회로 블록이나 구역의 상태가 바뀌지 않는다.

이 복원본의 Result에는 다음 필드를 사용한다.

    count: 반환한 구역 수 (0~10)
    ids: 순위대로 정렬된 구역 ID 목록. 길이는 정확히 count.

구역이 있으면 ids[0]은 1위 구역의 현재 ID이며, 각 구역은 목록에 한 번만 포함한다.

예를 들어 반환할 구역이 순서대로 7, 12, 40이라면 Result(count=3, ids=[7, 12, 40])이다. 빈 결과는 Result(count=0, ids=[])이다. 남는 칸을 0으로 채우지 않는다.

■ 확인이 필요한 복원 부분

좌표 범위 0~N, 세 번째 정렬 기준인 구역 ID 오름차순, Result에 개수 필드와 ID 배열이 모두 있었다는 점은 확실하지 않은 기억을 채택했다.

init/isSameRegion/top10의 정확한 원래 함수명, Result의 원래 필드명, 명령 번호는 미확인이다. 이 복원본에서 표시한 이름과 명령 번호를 사용한다.

N의 최솟값 1, 블록 ID가 중복되지 않는 양의 정수라는 보장, 유효한 블록 ID만 조회한다는 보장, 케이스당 한 번의 초기화는 연습본의 약속이다.

블록 하나의 가로·세로 길이에 N에 따른 별도 상한이 있었는지는 아직 미확인이다. 랜덤 생성 조건 자체는 사용자가 재확인했으며, 구체적인 분포와 생성 방식은 아직 복원되지 않았다. 예제는 규칙 확인을 위해 직접 구성했다.

아래 User Code에는 직접 구현할 함수 틀이 제공된다. Result는 일반 클래스로 정의되어 있다.

[예제 1]
입력:
4 100
19
100 20
400 0
200 20 0 0 2 2 4
200 7 4 0 6 2 4
400 2 7 20
300 20 7 0
200 15 2 0 4 1 10
300 20 7 1
400 1 7
200 3 6 2 8 4 4
300 7 3 0
400 2 7 3
200 9 6 0 8 2 18
300 20 3 1
400 1 3
200 1 10 10 11 11 1
300 1 1 1
400 2 3 1
400 2 3 1
17
100 50
200 50 0 0 2 3 6
200 5 2 0 4 3 12
200 40 10 0 14 3 12
200 8 20 0 24 3 12
200 99 30 0 35 3 15
400 4 99 8 40 5
300 50 5 1
300 5 8 0
200 3 0 3 1 4 13
400 4 99 3 8 40
200 2 1 3 2 4 14
400 4 99 2 8 40
200 1 2 3 3 4 15
400 4 99 1 8 40
300 50 1 1
400 4 99 1 8 40
22
100 100
200 120 0 0 1 1 1
200 110 3 0 4 1 1
200 100 6 0 7 1 1
200 90 9 0 10 1 1
200 80 12 0 13 1 1
200 70 15 0 16 1 1
200 60 18 0 19 1 1
200 50 21 0 22 1 1
200 40 24 0 25 1 1
200 30 27 0 28 1 1
200 20 30 0 31 1 1
200 10 33 0 34 1 1
400 10 10 20 30 40 50 60 70 80 90 100
400 10 10 20 30 40 50 60 70 80 90 100
200 5 0 1 1 2 2
400 10 5 10 20 30 40 50 60 70 80 90
300 5 120 1
300 5 110 0
200 1 1 0 3 1 5
400 10 1 10 20 30 40 50 60 70 80 90
300 5 110 1
9
100 45000
400 0
200 7 44996 44996 45000 45000 16
200 20 44995 44996 44996 45000 20
300 7 20 1
400 1 7
200 1 0 0 1 1 1
400 2 7 1
300 1 7 0

출력:
#1 100
#2 100
#3 100
#4 100

"""

# ── User Code ──
class Result:
    def __init__(self, count=0, ids=None):
        # 실제 반환한 구역 수: 0 이상 10 이하.
        self.count = count
        # 순위순 구역 ID. 실제 반환할 count개만 넣는다.
        self.ids = [] if ids is None else ids


import heapq


# 유니온 파인드 구현

# 특정 노드의 부모를 찾는 함수
def find(node):
    while parent[node] != node:
        node = parent[node]

    return node


# a 노드와 b 노드를 이어붙임. 단 여기서 노드의 갯수가 적은걸 많은거 아래에 이어붙임
def union(a, b):
    pass

g_N = 0

block_to_idx = {}
parent = []
uf_size = []

region_area = []
region_count = []
region_id = []

version = []
rank_heap = []

x_edges = []
y_edges = []

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]

    return x

def union(a, b):
    ra = find(a)
    rb = find(b)

    if ra == rb:
        return ra

    if uf_size[ra] < uf_size[rb]:
        ra, rb = rb, ra

    parent[rb] = ra

    uf_size[ra] += uf_size[rb]

    region_area[ra] += region_area[rb]
    region_count[ra] += region_count[rb]

    region_id[ra] = min(
        region_id[ra],
        region_id[rb]
    )

    version[ra] += 1

    return ra

def init(N: int) -> None:
    """테스트 케이스 시작 시 호출된다. 이전 테스트의 모든 상태를 초기화한다."""
    global g_N, block_to_idx, parent, uf_size, region_area
    global region_count, region_id, version, rank_heap, x_edges, y_edges
    g_N = N
    block_to_idx = {}

    # 부모 모음?
    parent = []
    # 유니온 파인드 사이즈?
    uf_size = []


    # 구역 면적
    region_area = []
    # 구역 칸 세기
    region_count = []
    # 구역 id 모음?
    region_id = []

    version = []
    rank_heap = []

    x_edges = [[] for _ in range(N + 1)]
    y_edges = [[] for _ in range(N + 1)]


def addBlock(blockId: int, x1: int, y1: int, x2: int, y2: int) -> int:
    """새 블록을 추가하고, 추가 후 그 블록이 속한 구역의 전체 면적을 반환한다."""
    idx = len(parent)
    block_to_idx[blockId] = idx

    area = (x2 - x1) * (y2 - y1)

    parent.append(idx)
    uf_size.append(1)

    region_area.append(area)
    region_count.append(1)
    region_id.append(blockId)

    version.append(0)

    neighbors = set()

    for oy1, oy2, other_idx in x_edges[x1]:
        if y1 < oy2 and oy1 < y2:
            neighbors.add(other_idx)

    for oy1, oy2, other_idx in x_edges[x2]:
        if y1 < oy2 and oy1 < y2:
            neighbors.add(other_idx)

    for ox1, ox2, other_idx in y_edges[y1]:
        if x1 < ox2 and ox1 < x2:
            neighbors.add(other_idx)

    for ox1, ox2, other_idx in y_edges[y2]:
        if x1 < ox2 and ox1 < x2:
            neighbors.add(other_idx)

    root = idx

    for other_idx in neighbors:
        root = union(root, other_idx)

    root = find(root)

    heapq.heappush(
        rank_heap,
        (
            -region_area[root],
            region_count[root],
            region_id[root],
            root,
            version[root]
        )
    )

    x_edges[x1].append(
        (y1, y2, idx)
    )

    x_edges[x2].append(
        (y1, y2, idx)
    )

    y_edges[y1].append(
        (x1, x2, idx)
    )

    y_edges[y2].append(
        (x1, x2, idx)
    )

    return region_area[root]


def isSameRegion(blockId1: int, blockId2: int) -> int:
    """두 블록이 같은 구역에 속하면 1, 아니면 0을 반환한다."""
    idx1 = block_to_idx[blockId1]
    idx2 = block_to_idx[blockId2]

    return 1 if find(idx1) == find(idx2) else 0

def top10() -> Result:
    """면적 내림차순, 블록 수 오름차순, 구역 ID 오름차순으로 최대 10개 반환.

    세 번째 정렬 기준은 아직 확실하지 않은 기억을 복원본에 반영한 것이다.
    Result.count == len(Result.ids)이며, 구역이 없으면 Result()를 반환한다.
    """
    selected = []

    while rank_heap and len(selected) < 10:
        entry = heapq.heappop(rank_heap)

        neg_area, cnt, rid, root, ver = entry

        if parent[root] != root:
            continue
        if version[root] != ver:
            continue

        selected.append(entry)

    for entry in selected:
        heapq.heappush(rank_heap, entry)

    ids = [
        entry[2]
        for entry in selected
    ]

    return Result(
        len(ids),
        ids
    )


# ── Main (수정 불가) ──
"""복원한 함수형 문제를 채점하는 연습용 드라이버.

실행: python main.py sample_input.txt --debug
표준 입력: python main.py < sample_input.txt  (이 리다이렉션은 cmd/bash용)
문제 규칙과 복원용 명령 형식은 README.md에 설명한다.
"""

import argparse
from contextlib import nullcontext
from pathlib import Path
import sys
from typing import List, Optional, TextIO
# (합쳐서 실행하므로 import 제거)


CMD_INIT = 100
CMD_ADD = 200
CMD_SAME = 300
CMD_TOP10 = 400


class InputFormatError(ValueError):
    pass


def read_row(stream: TextIO, description: str) -> List[int]:
    """빈 줄을 건너뛰고 명령 한 줄을 읽는다."""
    while True:
        line = stream.readline()
        if not line:
            raise InputFormatError(f"{description}: 입력이 중간에 끝났습니다.")
        if line.strip():
            try:
                return [int(token) for token in line.split()]
            except ValueError as exc:
                raise InputFormatError(f"{description}: 정수만 입력할 수 있습니다.") from exc


def read_case(stream: TextIO, case_number: int) -> List[List[int]]:
    header = read_row(stream, f"#{case_number} 명령 수")
    if len(header) != 1 or header[0] < 1:
        raise InputFormatError("명령 수 Q는 1 이상의 정수 하나여야 합니다.")

    commands = []
    for index in range(header[0]):
        row = read_row(stream, f"#{case_number} 명령 {index + 1}")
        command = row[0]
        if command == CMD_INIT:
            valid = len(row) == 2 and 1 <= row[1] <= 45_000 and index == 0
        elif command == CMD_ADD:
            valid = len(row) == 7 and row[6] > 0
        elif command == CMD_SAME:
            valid = len(row) == 4 and row[3] in (0, 1)
        elif command == CMD_TOP10:
            valid = len(row) >= 2 and 0 <= row[1] <= 10 and len(row) == row[1] + 2
        else:
            valid = False

        if index == 0 and command != CMD_INIT:
            valid = False
        if not valid:
            raise InputFormatError(f"#{case_number} 명령 {index + 1}: 잘못된 형식 {row}")
        commands.append(row)

    return commands


def judge_case(commands: List[List[int]], case_number: int, debug: bool = False) -> bool:
    """정답을 solution 함수에 넘기지 않고, 반환값을 채점기 안에서 비교한다."""
    correct = True
    first_failure = None

    for index, row in enumerate(commands, start=1):
        command = row[0]
        failure = None
        try:
            if command == CMD_INIT:
                init(row[1])
            elif command == CMD_ADD:
                actual = addBlock(*row[1:6])
                if actual != row[6]:
                    failure = f"addBlock({', '.join(map(str, row[1:6]))}): 기대 {row[6]}, 실제 {actual!r}"
            elif command == CMD_SAME:
                actual = isSameRegion(row[1], row[2])
                if actual != row[3]:
                    failure = f"isSameRegion({row[1]}, {row[2]}): 기대 {row[3]}, 실제 {actual!r}"
            elif command == CMD_TOP10:
                actual = top10()
                expected_count, expected_ids = row[1], row[2:]
                if actual.count != expected_count or actual.ids != expected_ids:
                    failure = (
                        f"top10(): 기대 count={expected_count}, ids={expected_ids}; "
                        f"실제 count={actual.count!r}, ids={actual.ids!r}"
                    )
        except Exception as exc:
            # 해당 케이스의 명령은 이미 읽었으므로, 예외가 나도 다음 케이스를 채점할 수 있다.
            correct = False
            if first_failure is None:
                first_failure = f"명령 {index}: {type(exc).__name__}: {exc}"
            break

        if failure is not None:
            correct = False
            if first_failure is None:
                first_failure = f"명령 {index}: {failure}"

    if debug and first_failure is not None:
        print(f"[#{case_number}] {first_failure}", file=sys.stderr)
    return correct


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path, help="생략하면 표준 입력을 읽습니다.")
    parser.add_argument("--debug", action="store_true", help="케이스별 첫 실패 이유를 stderr에 표시합니다.")
    args = parser.parse_args(argv)

    try:
        source = args.input.open("r", encoding="utf-8-sig") if args.input else nullcontext(sys.stdin)
        with source as stream:
            header = read_row(stream, "테스트 수와 배점")
            if len(header) != 2 or header[0] < 1 or header[1] < 1:
                raise InputFormatError("첫 줄에는 양수 T와 MARK를 입력해야 합니다.")
            case_count, mark = header
            for case_number in range(1, case_count + 1):
                commands = read_case(stream, case_number)
                passed = judge_case(commands, case_number, args.debug)
                print(f"#{case_number} {mark if passed else 0}")
            if stream.read().strip():
                raise InputFormatError("마지막 테스트 케이스 뒤에 불필요한 입력이 있습니다.")
    except (OSError, InputFormatError) as exc:
        print(f"입력 오류: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
