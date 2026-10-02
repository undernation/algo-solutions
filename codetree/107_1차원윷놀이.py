"""
CT 107  1차원 윷놀이
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-yutnori-1d/description

풀이일 : 2026-10-02   결과: 품
한도   : time Python3 8초 · C++17 1초 / memory 128 MB / time_sec 8
난이도 : Easy  |  정답률 58.5%
제약   : - $1 \le N \le 12$
제약   : - $2 \le M \le 100$
제약   : - $1 \le K \le 4$
제약   : - $1 \le \texttt{주어지는 수} \le 100$

[채점] accepted  2/2  (0.63s)

[문제]
$1$번부터 $M$번까지 번호 순서대로 총 $M$개의 지점이 연결되어 있는 $1$차원 윷놀이 판에서 게임을 진행해보려고 합니다. $M$이 $6$인 경우 윷놀이 판의 모습은 다음과 같습니다.

![](https://contents.codetree.ai/problems/107/images/problems-e7a45079-e3ff-4a34-a98f-02155811c13a.png)

처음에는 $K$개의 말이 $1$번 지점에 놓여있으며, $N$번의 턴에 걸쳐 수가 주어지고 각 턴마다 하나의 말을 선택하여 해당 수만큼 앞으로 나아갈 수 있습니다.

말은 앞으로 나아갈 때 한 칸 단위로 움직이며, 이때 앞으로 나아가던 말이 $M$번에 도달하게 되면 $1$점을 얻게 됩니다.

$M$번에 도달한 말을 또 선택할 수는 있지만 이 경우에는 아무런 변화가 나타나지 않습니다.

위의 그림에서 $K = 3$인 경우를 예로 들어봅시다.

![](https://contents.codetree.ai/problems/107/images/problems-f0556b90-575e-4247-a8ae-1bf2f93106ab.png)

이때, $N = 4$이고 주어진 수들이 순서대로 $2$, $4$, $2$, $4$ 인 경우를 생각해봅시다.

만약 $4$회에 걸쳐 순서대로 $1$번, $2$번, $1$번, $2$번 말을 고른다면 $2$번 말만 점수를 얻게 됩니다.

![](https://contents.codetree.ai/problems/107/images/problems-339062c3-923b-4895-a497-307ef326b88a.png)

하지만 만약 $1$번, $1$번, $2$번, $2$번 순서대로 말을 고르게 되면, 점수를 $2$점 얻게 됩니다.

![](https://contents.codetree.ai/problems/107/images/problems-676b39b3-fcf1-4240-8803-e7e3ea8a9902.png)

$N$번의 턴에 대해 말들을 적당히 움직여 얻을 수 있는 점수 중 최댓값을 구하는 프로그램을 작성해보세요.

[예제 1]
입력:
4 6 3
2 4 2 4

출력:
2


[예제 2]
입력:
6 10 3
5 3 2 2 3 3

출력:
2

"""

N, M, K = map(int, input().split())
nums = list(map(int, input().split()))

# Please write your code here.

horse_list = []


def simulate():
    global horse_list, nums
    horse_scores = [0] * K
    cnt = 0
    for horse in range(N):
        horse_scores[horse_list[horse]] += nums[horse]
    # print("debug", horse_scores)
    for score in horse_scores:
        if score >= M - 1:
            cnt += 1

    return cnt


answer = 0


def dfs(idx):
    global answer
    if idx == N:
        answer = max(answer, simulate())
        return

    for i in range(K):
        horse_list.append(i)
        dfs(idx + 1)
        horse_list.pop()

dfs(0)
print(answer)
