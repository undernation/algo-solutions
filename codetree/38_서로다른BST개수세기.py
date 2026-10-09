"""
CT 38  서로 다른 BST 개수 세기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-number-of-unique-bst/description

풀이일 : 2026-10-09   결과: 못품
한도   : time Python3 1초 · C++17 0.5초 / memory 64 MB / time_sec 1
난이도 : Hard  |  정답률 57.7%
제약   : - $1 \le N \le 19$

[문제]
BST란 자식을 $2$개 이하로 갖는 이진 탐색 트리입니다. 각 노드마다 왼쪽에 있는 모든 노드들의 값이 해당 노드의 값보다 작아야 하고, 오른쪽에 있는 모든 노드들의 값이 해당 노드의 값보다 커야 합니다.

$1$부터 $N$까지의 정수들을 단 한 번씩만 써서 만들 수 있는 노드의 개수가 $N$인 서로 다른 이진 탐색 트리 개수를 세는 프로그램을 작성해보세요. 

예를 들어 $N = 4$일 때,

다음은 모든 정점이 연결되어 있지 않기 때문에 트리가 아닙니다.

![](https://contents.codetree.ai/problems/38/images/problems-36697944-a1c7-4d97-bee7-46f9e9f01831.svg)

이 그림은 사이클이 존재하므로 트리가 아닙니다.

![](https://contents.codetree.ai/problems/38/images/problems-ad899f5d-480a-4a0a-bac0-49aa63949428.svg)

이 그림은 트리이긴 하지만, 자식을 $2$개보다 많이 갖고 있는 노드가 있으므로 이진 탐색 트리가 아닙니다. 
![](https://contents.codetree.ai/problems/38/images/problems-61db2283-858c-4ff8-b366-e14d17b83f8a.svg)

다음은 노드 $2$를 기준으로 왼쪽 자식에 자신보다 값이 큰 노드 $4$가 있기 때문에 이진 탐색 트리가 아닙니다.

![](https://contents.codetree.ai/problems/38/images/problems-a58fba11-7842-424b-b5aa-fe1db5365a1f.svg)

다음은 올바른 이진 탐색 트리입니다.

![](https://contents.codetree.ai/problems/38/images/problems-c48e2b29-6be7-440e-8295-09ef280ca0d5.svg)

$N = 3$일 때 가능한 BST는 총 $5$개입니다.

![](https://contents.codetree.ai/problems/38/images/problems-46a56519-31ad-44cf-87a2-59df2d4e8d26.svg)

[예제 1]
입력:
2

출력:
2


[예제 2]
입력:
3

출력:
5

"""

N = int(input())

# Please write your code here.

print(pow(2, 19))
dp = [0] * (N * 4)
MAX = (1 << N) - 1
answer = 0

def dfs(mask, cur_idx):
    global answer

    if mask == MAX:
        answer += 1
        return
