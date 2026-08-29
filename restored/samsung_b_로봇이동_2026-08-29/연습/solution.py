# 로봇 이동 — User Code
#
# 아래 세 함수를 구현한다. 입출력은 main.py 가 처리하므로 여기서는 다루지 않는다.
#
#   python main.py < tc_valid.txt      → #1 100 ... #5 100 이 나오면 정답
#
# init(N)
#     각 테스트 케이스 시작에 한 번 호출. N x N 빈 도시를 초기화한다.
#
# build(mID, mX, mY, mW, mH, mDoorX, mDoorY)
#     건물 추가. 건물 영역은 x = mX ~ mX+mW-1, y = mY ~ mY+mH-1 이고
#     그 바깥 한 칸이 도로가 된다.
#     출입구 실제 좌표는 (mX + mDoorX, mY + mDoorY).
#
# move(mStart, mEnd, M, mID)
#     mStart 출입구에서 출발해 mID[0:M] 의 모든 출입구를 방문한 뒤
#     mEnd 출입구까지 가는 최소 이동 거리를 반환한다. (M <= 5)


def init(N):
    pass


def build(mID, mX, mY, mW, mH, mDoorX, mDoorY):
    pass


def move(mStart, mEnd, M, mID):
    return 0
