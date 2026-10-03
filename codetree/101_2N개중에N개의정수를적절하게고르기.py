"""
CT 101  2N개 중에 N개의 정수를 적절하게 고르기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-choose-n-out-of-2n-properly/description

풀이일 : 2026-10-03   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 58.0%
제약   : - $1 \le N \le 10$
제약   : - $1 \le a_i \le 1\,000$ ($1 \le i \le 2N$)

[채점] accepted  2/2  (0.525s)

[문제]
$2N$개의 정수로 이루어진 수열 $A$가 주어졌을 때, 주어진 수를 각각 $N$개씩 $2$개의 그룹으로 나눠 각 그룹 원소합의 차가 최소가 되도록 하는 프로그램을 작성해 주세요.

[예제 1]
입력:
2
1 3 5 6

출력:
1


[예제 2]
입력:
3
1 8 9 3 5 15

출력:
1

"""

N = int(input())
num = list(map(int, input().split()))

# Please write your code here.

total_val = sum(num)

num_list = []

answer = 10 ** 18


def dfs(idx, cnt):
    global answer
    if cnt == N:
        if abs((total_val - sum(num_list)) - sum(num_list)) < answer:
            answer = abs((total_val - sum(num_list)) - sum(num_list))

        return

    if idx == len(num):
        return

    num_list.append(num[idx])
    dfs(idx + 1, cnt + 1)
    num_list.pop()

    dfs(idx + 1, cnt)


dfs(0, 0)
print(answer)
