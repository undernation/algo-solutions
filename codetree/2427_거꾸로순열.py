"""
CT 2427  거꾸로 순열
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-backward-permutation/description

풀이일 : 2026-10-04   결과: 품
한도   : time Python3 1초 · C++17 1초 / memory 128 MB / time_sec 1
난이도 : Easy  |  정답률 94.1%
제약   : - $1 \le N \le 8$

[채점] accepted  1/1  (0.28s)

[문제]
$1$부터 $N$까지의 수를 정확히 한 번씩만 사용하여 만들 수 있는 가능한 모든 수열을 구해주는 프로그램을 작성해보세요. 단, 사전순으로 가장 뒤에 있는 수열부터 먼저 출력하도록 합니다.

[예제 1]
입력:
3

출력:
3 2 1
3 1 2
2 3 1
2 1 3
1 3 2
1 2 3

"""

N = int(input())

# Please write your code here.

num_list = []

def dfs(idx):
    if idx == N:
        print(*num_list)
        return

    for num in range(N, 0, -1):
        if num in num_list:
            continue

        num_list.append(num)
        dfs(idx + 1)
        num_list.pop()

dfs(0)
