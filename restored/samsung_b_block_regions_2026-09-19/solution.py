"""블록 구역 관리 문제의 구현용 틀.

일부 함수 이름과 Result 필드 이름은 복원용으로 정한 API다.
원문에서 확인된 시그니처가 아니며, README.md의 확정 내용/가정을 참고한다.
정답 구현이나 알고리즘 힌트는 포함하지 않는다.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Result:
    # 실제 반환한 구역 수: 0 이상 10 이하.
    count: int = 0
    # 순위순 구역 ID. 실제 반환할 count개만 넣는다.
    ids: List[int] = field(default_factory=list)


def init(N: int) -> None:
    """테스트 케이스 시작 시 호출된다. 이전 테스트의 모든 상태를 초기화한다."""
    raise NotImplementedError("init 함수를 구현하세요.")


def addBlock(blockId: int, x1: int, y1: int, x2: int, y2: int) -> int:
    """새 블록을 추가하고, 추가 후 그 블록이 속한 구역의 전체 면적을 반환한다."""
    raise NotImplementedError("addBlock 함수를 구현하세요.")


def isSameRegion(blockId1: int, blockId2: int) -> int:
    """두 블록이 같은 구역에 속하면 1, 아니면 0을 반환한다."""
    raise NotImplementedError("isSameRegion 함수를 구현하세요.")


def top10() -> Result:
    """면적 내림차순, 블록 수 오름차순, 구역 ID 오름차순으로 최대 10개 반환.

    세 번째 정렬 기준은 아직 확실하지 않은 기억을 복원본에 반영한 것이다.
    Result.count == len(Result.ids)이며, 구역이 없으면 Result()를 반환한다.
    """
    raise NotImplementedError("top10 함수를 구현하세요.")
