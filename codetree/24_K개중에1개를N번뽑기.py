"""
CT 24  K개 중에 1개를 N번 뽑기
https://www.codetree.ai/ko/trails/complete/curated-cards/intro-n-permutations-of-k-with-repetition/description

풀이일 : 2026-09-30   결과: 품
한도   : time Python3 1초 · C++17 1초 / memory 128 MB / time_sec 1
난이도 : Easy  |  정답률 80.2%
제약   : - $1 \le K \le 4$
제약   : - $1 \le N \le 8$

[채점] accepted  2/2  (0.567s)

[문제]
$1$이상 $K$이하의 정수를 하나 고르는 행위를 $N$번 반복하여 나올 수 있는 모든 서로 다른 수열을 구해주는 프로그램을 작성해보세요.

예를 들어 $K$가 $3$, $N$이 $2$인 경우 다음과 같이 $9$개의 수열이 가능합니다.

- $1\ 1$

- $1\ 2$

- $1\ 3$

- $2\ 1$

- $2\ 2$

- $2\ 3$

- $3\ 1$

- $3\ 2$

- $3\ 3$

[예제 1]
입력:
2 2

출력:
1 1
1 2
2 1
2 2


[예제 2]
입력:
3 2

출력:
1 1
1 2
1 3
2 1
2 2
2 3
3 1
3 2
3 3

"""



K, N = map(int, input().split())

# Please write your code here.
answer = []
def dfs(idx):
    if idx == N:
        print(*answer)
        return

    for num in range(1, K + 1):
        answer.append(num)
        dfs(idx + 1)
        answer.pop()
        
dfs(0)
