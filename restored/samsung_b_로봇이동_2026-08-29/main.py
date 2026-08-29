import sys
from solution import init, build, move

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
