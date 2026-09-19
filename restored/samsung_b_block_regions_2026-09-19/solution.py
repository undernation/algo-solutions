class Result:
    def __init__(self, count=0, ids=None):
        # 실제 반환한 구역 수: 0 이상 10 이하.
        self.count = count
        # 순위순 구역 ID. 실제 반환할 count개만 넣는다.
        self.ids = [] if ids is None else ids


def init(N: int) -> None:
    """테스트 케이스 시작 시 호출된다. 이전 테스트의 모든 상태를 초기화한다."""


def addBlock(blockId: int, x1: int, y1: int, x2: int, y2: int) -> int:
    """새 블록을 추가하고, 추가 후 그 블록이 속한 구역의 전체 면적을 반환한다."""


def isSameRegion(blockId1: int, blockId2: int) -> int:
    """두 블록이 같은 구역에 속하면 1, 아니면 0을 반환한다."""


def top10() -> Result:
    """면적 내림차순, 블록 수 오름차순, 구역 ID 오름차순으로 최대 10개 반환.

    세 번째 정렬 기준은 아직 확실하지 않은 기억을 복원본에 반영한 것이다.
    Result.count == len(Result.ids)이며, 구역이 없으면 Result()를 반환한다.
    """
