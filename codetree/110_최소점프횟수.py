"""
CT 110  최소 점프 횟수
https://www.codetree.ai/ko/trails/complete/curated-cards/test-min-num-of-jumps/description

풀이일 : 2026-10-03   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 64 MB / time_sec 1
난이도 : Medium  |  정답률 60.0%
제약   : - $2 \le N \le 10$
제약   : - $0 \le \texttt{주어지는 수} \le 4$

[채점] accepted  2/2  (0.543s)

[문제]
각 위치로부터의 최대 점프 가능 거리를 의미하는 $N$개의 정수가 첫 번째 위치부터 순서대로 주어졌을 때, 첫 번째 위치로부터 $N$번째 위치에 도달하기 위해 필요한 최소 점프 횟수를 구하는 프로그램을 작성해보세요.

여기서 최대 점프 가능 거리란 현재 위치로부터 추가적으로 나아갈 수 있는 최대 칸의 수를 의미하며, 매 점프마다 $1$칸 이상 최댓값 이하의 거리를 자유롭게 선택할 수 있습니다. 점프는 앞으로만 가능합니다.

예를 들어 다음과 같이 $N$개의 정수가 주어진 경우라면, $2$번 점프하여 $N$번째 위치에 도달할 수 있습니다.



![Image](https://contents.codetree.ai/problem_factory/images/314303a6-f8b5-4f2a-bdd1-5a36150d5f6e.webp)

[예제 1]
입력:
5
2 3 1 1 4

출력:
2


[예제 2]
입력:
5
2 1 1 0 4

출력:
-1

"""

N = int(input())
num = list(map(int, input().split()))

# Please write your code here.
answer = 10 ** 18

def dfs(idx, depth):
    global answer
    if idx == N - 1:
        answer = min(answer, depth)
        # print("wow")
        return
    
    cur_num = num[idx]

    for i in range(1, cur_num + 1):
        # print(i)
        if idx + i > N - 1:
            continue

        dfs(idx + i, depth + 1)
    # print(idx)
    return
#
dfs(0, 0)

if answer == 10 ** 18:
    print(-1)
else:
    print(answer)
