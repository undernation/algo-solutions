"""
CT 22  XOR 결과 최대 만들기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-max-of-xor/description

풀이일 : 2026-10-03   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Easy  |  정답률 53.6%
제약   : - $1 \le M \le N \le 20$
제약   : - $0 \le \texttt{정수} \le 1\,000\,000$

[채점] accepted  1/1  (0.231s)

[문제]
$N$개의 음이 아닌 정수가 입력으로 주어졌을 때, 그 중 $M$개의 정수를 뽑아 모두 XOR한 결과의 최댓값을 출력하는 코드를 작성해보세요.

[예제 1]
입력:
5 3
1 2 3 4 5

출력:
7

"""

N, M = map(int, input().split())
A = list(map(int, input().split()))

# Please write your code here.

answer = 0


def dfs(idx, cnt, result):
    global answer
    if cnt == M:
        answer = max(answer, result)
        return

    if idx == N:
        return 

    # 현재꺼 뽑기
    cur_num = A[idx]

    dfs(idx + 1, cnt + 1, result ^ cur_num)

    dfs(idx + 1, cnt, result)

dfs(0, 0, 0)

print(answer)
