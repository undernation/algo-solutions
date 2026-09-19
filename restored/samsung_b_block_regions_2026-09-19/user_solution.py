class Result:
    def __init__(self, count=0, ids=None):
        # 실제 반환한 구역 수: 0 이상 10 이하.
        self.count = count
        # 순위순 구역 ID. 실제 반환할 count개만 넣는다.
        self.ids = [] if ids is None else ids


import heapq

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

    parent = []
    uf_size = []

    region_area = []
    region_count = []
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
