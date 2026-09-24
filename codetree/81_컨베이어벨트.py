"""
CT 81  컨베이어 벨트
https://www.codetree.ai/ko/trails/complete/curated-cards/intro-conveyor-belt/description

풀이일 : 2026-09-24   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 64 MB / time_sec 1
난이도 : Easy  |  정답률 75.5%
제약   : - $1 \le N \le 200$
제약   : - $1 \le T \le 1\,000$
제약   : - 주어지는 정수는 $1$ 이상 $9$ 이하입니다.

[채점] accepted  2/2  (0.532s)

[문제]
시계 방향으로 한 칸씩 회전하는 컨베이어 벨트가 있습니다. 컨베이어 벨트 위아래로 $N$개씩 총 $2 \times N$ 개의 정수가 두 줄로 적혀 있고, $1$초에 한 칸씩 움직입니다.

![](https://contents.codetree.ai/problems/81/images/problems-986cf4a0-f378-461d-adc0-864c76b062ae.png)

위의 그림에서 $1$초가 흐른 뒤에는 다음과 같이 그림이 바뀌게 됩니다.

![](https://contents.codetree.ai/problems/81/images/problems-35c6083f-59d7-49c8-8387-917ca7324154.png)

$T$초의 시간이 흐른 뒤 컨베이어 벨트에 놓여있는 정수들의 상태를 출력하는 프로그램을 작성해보세요.

[예제 1]
입력:
3 1
1 2 3
6 5 1

출력:
1 1 2
3 6 5


[예제 2]
입력:
3 3
1 2 3
6 5 1

출력:
6 5 1
1 2 3

"""

N, T = map(int, input().split())
u_list = list(map(int, input().split()))
d_list = list(map(int, input().split()))

# Please write your code here.

for t in range(T):
    temp1 = u_list[N - 1]

    temp2 = d_list[N - 1]

    for n in range(N-1, 0, -1):
        u_list[n] = u_list[n - 1]

    for n in range(N-1, 0, -1):
        d_list[n] = d_list[n - 1]

    u_list[0] = temp2
    d_list[0] = temp1
    # print(*u_list)
    # print(*d_list)

print(*u_list)
print(*d_list)
