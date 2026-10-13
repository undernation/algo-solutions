"""
CT 2492  수들 중 최솟값 최대화하기
https://www.codetree.ai/ko/trails/complete/curated-cards/test-maximin-of-numbers/description

풀이일 : 2026-10-13   결과: 품
한도   : time Python3 4초 · C++17 1초 / memory 128 MB / time_sec 4
난이도 : Medium  |  정답률 77.1%
제약   : - $1 \le N \le 10$
제약   : - $1 \le \texttt{주어지는 정수} \le 10\,000$

[채점] accepted  1/1  (0.281s)

[문제]
크기가 $N \times N$인 이차원 격자 내 각 칸에 정수값이 적혀 있습니다.

이때 정확히 $N$개의 칸에 색칠을 하여 각 행과 열에 정확히 $1$개의 색칠된 칸만 오도록 하려고 합니다. 이러한 조건 하에서 색칠된 칸에 적힌 수들 중 최솟값이 최대가 되도록 하는 프로그램을 작성해보세요.

[예제 1]
입력:
3
3 5 3
5 8 4
2 7 1

출력:
3

"""

N = int(input())
grid = [list(map(int, input().split())) for _ in range(N)]

# Please write your code here.

visited = [False] * N

answer = 0
def dfs(idx, cur_min):
    global answer
    if idx == N:
        answer = max(answer, cur_min)
        return

    for col in range(N):
        if visited[col]:
            continue

        cur_num = grid[idx][col]
        visited[col] = True
        dfs(idx + 1, min(cur_min, cur_num))
        visited[col] = False

INF = 10 ** 18

dfs(0, INF)

print(answer)
