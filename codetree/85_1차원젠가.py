"""
CT 85  1차원 젠가
https://www.codetree.ai/ko/trails/complete/curated-cards/intro-jenga-1d/description

풀이일 : 2026-09-25   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 64 MB / time_sec 1
난이도 : Easy  |  정답률 77.1%
제약   : - $2 \le N \le 100$
제약   : - $1 \le \texttt{블록 값} \le 100$
제약   : - $1 \le s_1 \le e_1 \le N$
제약   : - $1 \le s_2 \le e_2 \le N - (e_1 - s_1 + 1)$
제약   : - 각 제거 작업은 항상 남아 있는 블록 내에서 유효한 구간이 되도록 주어짐이 보장됩니다.

[문제]
$N$개의 층으로 이루어진 1차원 젠가의 상태가 주어집니다. 각 층마다 $1$개의 블록이 놓여져 있고, 각 블록에는 정수가 하나씩 적혀있습니다.

![](https://contents.codetree.ai/problems/85/images/problems-932b33dc-a0b9-4694-a1cc-9a9ebedc422e.png)

이 때 $2$번에 걸쳐 특정 구간의 블록들을 빼는 작업을 진행하려 합니다.

처음에 위에서부터 $2$번째 블록에서 $4$번째 블록까지 블록을 빼게 된다면, 남은 블록은 중력에 의해 떨어지게 되어 다음과 같이 블록이 남게 됩니다.

![](https://contents.codetree.ai/problems/85/images/problems-a6efd6f1-957c-4e4e-af48-c81756ad928e.png)

그 다음에는 $2$번째 블록만 빼게 된다면, 다음과 같이 블록이 남게 됩니다.

![](https://contents.codetree.ai/problems/85/images/problems-fc9856c6-a62c-4773-b259-178844055f5d.png)

특정 구간의 블록을 두 번 빼는 과정을 거친 이후의 결과를 출력하는 프로그램을 작성해보세요.

[예제 1]
입력:
6
1
2
3
1
1
5
2 4
2 2

출력:
2
1
5


[예제 2]
입력:
6
1
2
3
1
1
5
2 4
1 3

출력:
0

"""

n = int(input())
blocks = [int(input()) for _ in range(n)]
s1, e1 = map(int, input().split())
s2, e2 = map(int, input().split())

# Please write your code here.
ret = []
for block in range(n):

    if s1 - 1 <= block <= e1 - 1:
        continue
    ret.append(blocks[block])
# print(ret)
new_ret = []
for new_idx in range(len(ret)):
    if s2 - 1 <= new_idx <= e2 - 1:
        continue
    new_ret.append(ret[new_idx])
print(len(new_ret))
for i in new_ret:
    print(i)
