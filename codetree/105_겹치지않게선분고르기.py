"""
CT 105  겹치지 않게 선분 고르기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-select-segments-without-overlap/description

풀이일 : 2026-09-30   결과: 틀림
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 45.6%
제약   : - $1 \le N \le 15$
제약   : - $1 \le l_i < r_i \le 1\,000$ ($1 \le i \le N$)

[문제]
수직선상에 $N$개의 선분이 주어졌을 때, 서로 겹치지 않고 고를 수 있는 가장 많은 선분의 수를 구하는 프로그램을 작성하세요. 

단, 끝점을 공유하는 것 역시 겹친 것으로 생각합니다.

[예제 1]
입력:
3
1 2
3 4
5 6

출력:
3


[예제 2]
입력:
3
1 2
1 4
3 4

출력:
2

"""

N = int(input())
x1, x2 = [], []

for _ in range(N):
    a, b = map(int, input().split())
    x1.append(a)
    x2.append(b)


# Please write your code here.

def check(l1, r1, l2, r2):
    return max(l1, l2) <= min(r1, r2)


answer = 0


def dfs(idx, mask, cnt):
    global answer
    if idx == N:
        is_ok = True
        for i in range(N):
            for j in range(N):
                if i == j:
                    continue
                if not mask & (1 << i):
                    continue
                if not mask & (1 << j):
                    continue

                l1, r1 = x1[i], x2[i]
                l2, r2 = x1[j], x2[j]

                if check(l1, r1, l2, r2):
                    is_ok = False
                    break
            if not is_ok:
                break
        # print("wow")
        if is_ok:
            answer = max(answer, cnt)
        return

    # 선택하는 경우의 수
    dfs(idx + 1, mask | (1 << idx), cnt + 1)
    # 선택안하는 경우의 수
    dfs(idx + 1, mask, cnt)


dfs(0, 0, 0)

print(answer)
