"""
CT 2598  경험치를 빠르게 얻기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-gain-exp-quickly/description

풀이일 : 2026-10-14   결과: 못품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Hard  |  정답률 51.4%
제약   : - $1 \le N \le 100$
제약   : - $1 \le M \le 1\,000\,000$
제약   : - $1 \le e \le 1\,000\,000$
제약   : - $1 \le t \le 100$

[문제]
$N$개의 퀘스트 정보가 주어졌을 때 수행할 퀘스트를 잘 골라 각 퀘스트로부터 얻은 경험치의 총 합이 $M$ 이상이며 걸리는 총 시간이 최소가 되도록 하는 프로그램을 작성해보세요. 단, 동일한 퀘스트는 여러 번 진행할 수 없음에 유의합니다.

[예제 1]
입력:
3 5
2 3
5 4
3 2

출력:
4


[예제 2]
입력:
4 14
5 6
6 5
8 10
5 2

출력:
13

"""

N, M = map(int, input().split())
quests = [tuple(map(int, input().split())) for _ in range(N)]

# Please write your code here.

INF = float('inf')
dp = [INF] * (M + 1)
dp[0] = 0


for e, t in quests:
    for s in range(M, -1, -1):
        if dp[s] == INF:
            continue
        new_s = min(M, s + e)
        dp[new_s] = min(dp[new_s], dp[s] + t)

if dp[M] == INF:
    print(-1)
else:
    print(dp[M])
