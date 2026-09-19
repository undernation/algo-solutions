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

from solution import init, addBlock, isSameRegion, top10


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
