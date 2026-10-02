"""
CT 28  특정 조건에 맞게 K개 중에 1개를 N번 뽑기
https://www.codetree.ai/ko/trails/complete/curated-cards/intro-n-permutations-of-k-with-repetition-under-constraint/description

풀이일 : 2026-10-02   결과: 품
한도   : time Python3 1초 · C++17 1초 / memory 128 MB / time_sec 1
난이도 : Easy  |  정답률 62.3%
제약   : - $1 \le K \le 4$
제약   : - $1 \le N \le 8$

[채점] accepted  2/2  (0.599s)

[문제]
$1$이상 $K$이하의 정수를 하나 고르는 행위를 $N$번 반복하여 나올 수 있는 모든 서로 다른 수열을 구해주는 프로그램을 작성해보세요. 단, 연속하여 같은 정수가 $3$번 이상 나오는 경우는 제외합니다.

예를 들어 $K$가 $2$, $N$이 $3$인 경우 다음과 같이 $6$개의 조합이 가능합니다.

- $1\ 1\ 2$

- $1\ 2\ 1$

- $1\ 2\ 2$

- $2\ 1\ 1$

- $2\ 1\ 2$

- $2\ 2\ 1$

[예제 1]
입력:
2 1

출력:
1
2


[예제 2]
입력:
2 3

출력:
1 1 2
1 2 1
1 2 2
2 1 1
2 1 2
2 2 1

"""

K, N = map(int, input().split())

# Please write your code here.


# 연속하여 같은정수 세개면 제외
num_list = []
def dfs(idx):
    if idx == N:
        print(*num_list)
        return

    for num in range(1, K + 1):

        if idx >= 2:
            last_num1 = num_list[-2]
            last_num2 = num_list[-1]
            if last_num1 == last_num2 == num:
                continue

        num_list.append(num)
        dfs(idx + 1)
        num_list.pop()

dfs(0)
