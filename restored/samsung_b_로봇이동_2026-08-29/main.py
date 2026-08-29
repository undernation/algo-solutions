import os
import sys

from solution import init, build, move

# 입력 파일. 인자로 주면 그 파일을, 아니면 같은 폴더의 sample_input.txt 를 읽는다.
# (실제 SWEA Main 의 `sys.stdin = open('sample_input.txt', 'r')` 과 같은 역할)
#   python main.py                     -> sample_input.txt
#   python main.py 다른입력.txt          -> 그 파일
#   python main.py < 다른입력.txt        -> 리다이렉트도 그대로 동작
_HERE = os.path.dirname(os.path.abspath(__file__))
_SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "sample_input.txt")
if os.path.exists(_SRC):
    sys.stdin = open(_SRC, "r")

input = sys.stdin.readline

CMD_INIT = 100
CMD_BUILD = 200
CMD_MOVE = 300

DEBUG = True   # move 실제 반환값 출력


def run():
    Q = int(input())
    okay = True
    for _ in range(Q):
        command = list(map(int, input().split()))
        cmd = command[0]

        if cmd == CMD_INIT:
            N = command[1]
            init(N)

        elif cmd == CMD_BUILD:
            (_, mID, mX, mY, mW, mH, mDoorX, mDoorY) = command
            build(mID, mX, mY, mW, mH, mDoorX, mDoorY)

        elif cmd == CMD_MOVE:
            mStart = command[1]
            mEnd = command[2]
            M = command[3]
            mID = command[4:4 + M]
            expected = command[4 + M]
            ret = move(mStart, mEnd, M, mID)
            if DEBUG:
                mark = "OK" if ret == expected else "MISMATCH"
                sys.stderr.write(
                    "move(start=%d end=%d via=%s) -> got=%s expected=%s  %s\n"
                    % (mStart, mEnd, mID, ret, expected, mark))
            if ret != expected:
                okay = False
    return okay


if __name__ == "__main__":
    T, MARK = map(int, input().split())
    for tc in range(1, T + 1):
        score = MARK if run() else 0
        print("#%d %d" % (tc, score))
