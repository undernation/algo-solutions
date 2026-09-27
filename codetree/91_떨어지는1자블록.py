"""
CT 91  떨어지는 1자 블록
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-falling-horizontal-block/description

풀이일 : 2026-09-27   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 192 MB / time_sec 1
난이도 : Easy  |  정답률 43.6%
제약   : - $1 \le N \le 100$
제약   : - $1 \le M \le N$
제약   : - $1 \le K \le N - M + 1$

[채점] accepted  2/2  (0.502s)

[문제]
$0$과 $1$로만 채워져 있는 $N \times N$ 크기의 격자판 정보가 주어집니다. $0$은 빈 칸을, $1$은 해당 칸에 블럭이 채워져 있음을 뜻합니다. 

이때 $1 \times  M$ 크기의 블럭이 격자판 위에서 떨어집니다. 이 블럭은 $K$번째 열 부터 $K + M - 1$번째 열까지의 공간을 차지하며, 가장 위에서부터 밑으로 떨어집니다. 만약 이 블럭이 떨어지는 도중 단 한곳에라도 이미 격자판 위에 놓여있던 블럭과 맞닿게 된다거나, 혹은 바닥에 닿게 된다면 떨어지는 것을 멈추게 됩니다.

예를 들어, 다음과 같이 블럭이 채워져 있던 경우를 생각해봅시다.

![](https://contents.codetree.ai/problems/91/images/problems-8903676d-b4a5-47a8-9128-de482c5162f9.png)

이때 만약 $1 \times 3$ 크기의 블럭을 첫 번째 열부터 $3$번째 열까지의 공간을 차지하게 떨어뜨리게 되면 다음과 같이 블럭이 격자판 위에 안착하게 됩니다.

![](https://contents.codetree.ai/problems/91/images/problems-9cefe554-a23b-4841-8ccc-54da7ed7468a.png)

격자판의 정보와 떨어질 블럭의 정보가 주어졌을 때, 블럭이 떨어진 이후의 상태를 출력하는 프로그램을 작성해보세요.

[예제 1]
입력:
4 3 1
0 0 0 0
0 0 0 1
1 0 0 1
1 1 1 1

출력:
0 0 0 0
1 1 1 1
1 0 0 1
1 1 1 1


[예제 2]
입력:
4 2 2
0 0 0 0
0 0 0 1
1 0 0 1
1 1 1 1

출력:
0 0 0 0
0 0 0 1
1 1 1 1
1 1 1 1

"""

N, M, K = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(N)]

# Please write your code here.


start = K - 1
end = start + M - 1

min_val = 0
is_found = False
ret = -1
for i in range(N):
    for j in range(start, end + 1):
        if grid[i][j] == 1:
            is_found = True
            ret = i
            break
    if is_found:
        break
if ret == -1:
    i = N - 1

else:
    i = ret - 1

for j in range(start, end + 1):
    grid[i][j] = 1

for i in grid:
    print(*i)
