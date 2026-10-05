"""
CT 53  그래프 탐색
https://www.codetree.ai/ko/trails/complete/curated-cards/intro-graph-traversal/description

풀이일 : 2026-10-05   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Easy  |  정답률 65.7%
제약   : - $1 \le N \le 1\,000$
제약   : - $0 \le M \le \min(10\,000, \frac{N (N-1)}{2})$
제약   : - $1 \le x_i, y_i \le N$ $(1 \le i \le M)$
제약   : - $x_i \ne y_i$ $(1 \le i \le M)$
제약   : - $(x_i,\ y_i)$ 쌍이 동일한 연결관계가 두 번 이상 주어지는 경우는 없습니다.

[채점] accepted  2/2  (0.524s)

[문제]
$N$개의 정점과 $M$개의 간선으로 이루어진 양방향 그래프가 주어졌을 때, $1$번 정점에서 시작하여 주어진 간선을 따라 이동했을 때 도달할 수 있는 서로 다른 정점의 개수를 구하는 프로그램을 작성해보세요. (여기서 $1$번 정점 자기 자신에 도달하는 경우는 개수에서 제외합니다.)

다음 예시에서 $1$번 정점은 $2, 3$번 정점과 이어져 있기 때문에 답은 $2$가 됩니다.

![](https://contents.codetree.ai/problems/53/images/problems-7fb3914d-b4b0-4cc7-9852-62d59e560d9e.png)

[예제 1]
입력:
5 4
1 2
1 3
2 3
4 5

출력:
2


[예제 2]
입력:
5 4
1 2
4 2
5 3
3 4

출력:
4

"""

N, M = map(int, input().split())
edges = [tuple(map(int, input().split())) for _ in range(M)]

# Please write your code here.

lines = [[] for _ in range(N + 1)]

for a, b in edges:
    lines[a].append(b)
    lines[b].append(a)

visited = set()
visited.add(1)


def dfs(cur):
    for nxt in lines[cur]:
        if nxt in visited:
            continue
        visited.add(nxt)

        dfs(nxt)


dfs(1)

print(len(visited) - 1)
