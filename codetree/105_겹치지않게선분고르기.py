"""
CT 105  겹치지 않게 선분 고르기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-select-segments-without-overlap/description

풀이일 : 2026-10-11   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 45.6%
제약   : - $1 \le N \le 15$
제약   : - $1 \le l_i < r_i \le 1\,000$ ($1 \le i \le N$)

[채점] accepted  2/2  (0.589s)

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
lines = []

for _ in range(N):
    a, b = map(int, input().split())
    lines.append((a, b))

# Please write your code here.
lines.sort()
answer = 0
last_point = 0

def dfs(cnt, last_point, idx):
    global answer
    if idx == N:
        answer = max(answer, cnt)
        return

    # 현재꺼 고를 수 있는지 확인

    c1, c2 = lines[idx]
    
    # 못고름
    if c1 <= last_point:
        dfs(cnt, last_point, idx + 1)
    # 고를 수 있는 경우
    else:
        # 안고르는 경우

        dfs(cnt, last_point, idx + 1)

        # 고르는 경우
        dfs(cnt + 1, max(last_point, c2), idx + 1)
        
dfs(0, last_point, 0)

print(answer)
