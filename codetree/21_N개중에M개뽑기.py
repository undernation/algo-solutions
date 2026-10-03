"""
CT 21  N개 중에 M개 뽑기
https://www.codetree.ai/ko/trails/complete/curated-cards/intro-n-choose-m/description

풀이일 : 2026-10-03   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Easy  |  정답률 85.3%
제약   : - $1 \le M \le N \le 10$

[채점] accepted  2/2  (0.52s)

[문제]
$1$이상 $N$이하의 정수 중 $M$개의 정수를 골라 만들 수 있는 모든 조합을 구해주는 프로그램을 작성해보세요. 

예를 들어 $N$이 $4$, $M$이 $3$인 경우 다음과 같이 $4$개의 조합이 가능합니다.

- $1\ 2\ 3$
- $1\ 2\ 4$
- $1\ 3\ 4$
- $2\ 3\ 4$

[예제 1]
입력:
3 2

출력:
1 2
1 3
2 3


[예제 2]
입력:
4 3

출력:
1 2 3
1 2 4
1 3 4
2 3 4

"""

N, M = map(int, input().split())

# Please write your code here.
num_list = []
def dfs(idx, last_num):
    if idx == M:
        print(*num_list)
        return



    for num in range(last_num + 1, N + 1):
        if num in num_list:
            continue
        num_list.append(num)
        dfs(idx + 1, num)
        num_list.pop()

dfs(0, 0)
