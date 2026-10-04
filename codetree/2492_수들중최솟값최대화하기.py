"""
CT 2492  수들 중 최솟값 최대화하기
https://www.codetree.ai/ko/trails/complete/curated-cards/test-maximin-of-numbers/description

풀이일 : 2026-10-04   결과: 시간초과
한도   : time Python3 4초 · C++17 1초 / memory 128 MB / time_sec 4
난이도 : Medium  |  정답률 77.1%
제약   : - $1 \le N \le 10$
제약   : - $1 \le \texttt{주어지는 정수} \le 10\,000$

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

def get_min_val(num_list):
    return min(num_list)
answer = 0
visited = set()
col_list = []
def dfs(row_idx, total):
    global answer
    if row_idx == N:

        answer = max(answer, min(total))
        return

    for col in range(N):
        if col in col_list:
            continue
        col_list.append(col)
        total.append(grid[row_idx][col])
        dfs(row_idx + 1, total)
        total.remove(grid[row_idx][col])
        col_list.pop()

dfs(0, [])
print(answer)
