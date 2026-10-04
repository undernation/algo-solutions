"""
CT 2491  수들의 합 최대화하기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-max-sum-of-numbers/description

풀이일 : 2026-10-04   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 71.8%
제약   : - $1 \le N \le 9$
제약   : - 주어지는 각 정수는 $1$ 이상 $10\,000$ 이하입니다.

[채점] accepted  1/1  (0.262s)

[문제]
크기가 $N \times N$인 $2$차원 격자 내 각 칸에 정수값이 적혀 있습니다.

이때 정확히 $N$개의 칸에 색칠을 하여 각 행과 열에 정확히 $1$개의 색칠된 칸만 오도록 하려고 합니다. 이러한 조건 하에서 색칠된 칸에 적힌 수들의 합 중 가능한 최댓값을 구하는 프로그램을 작성해보세요.

[예제 1]
입력:
3
3 5 3
5 8 4
2 7 1

출력:
15

"""

N = int(input())
grid = [list(map(int, input().split())) for _ in range(N)]

# Please write your code here.

col_idxes = []
answer = 0

def dfs(row_idx, total):
    global answer
    if row_idx == N:
        answer = max(answer, total)
        return

    for col_idx in range(N):
        if col_idx in col_idxes:
            continue

        col_idxes.append(col_idx)
        dfs(row_idx + 1, total + grid[row_idx][col_idx])
        col_idxes.pop()

dfs(0, 0)
print(answer)
