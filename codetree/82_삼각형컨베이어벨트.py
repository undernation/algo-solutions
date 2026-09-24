"""
CT 82  삼각형 컨베이어 벨트
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-conveyor-belt-triangle/description

풀이일 : 2026-09-24   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Easy  |  정답률 72.5%
제약   : - $1 \le N \le 200$
제약   : - $1 \le T \le 1\,000$
제약   : - $1 \le \texttt{주어지는 수} \le 9$

[채점] accepted  2/2  (0.592s)

[문제]
시계 방향으로 한 칸씩 회전하는 삼각형 모양의 컨베이어 벨트가 있습니다. 각 변에 $N$개씩 총 $3N$개의 정수가 적혀 있고, $1$초에 한 칸씩 움직입니다.

![Image](https://contents.codetree.ai/problem_factory/images/2d70d8a6-803f-4aee-85ed-8193a665e52b.webp)



위의 그림에서 $1$초가 흐른 뒤에는 다음과 같이 그림이 바뀌게 됩니다.


![Image](https://contents.codetree.ai/problem_factory/images/1f17e9bf-c4eb-463f-88e0-fe2e105cdfef.webp)



$T$초의 시간이 흐른 뒤 컨베이어 벨트에 놓여있는 정수들의 상태를 출력하는 프로그램을 작성해보세요.

[예제 1]
입력:
3 1
1 2 4
5 9 3
6 5 1

출력:
1 1 2
4 5 9
3 6 5


[예제 2]
입력:
3 3
1 2 4
5 9 3
6 5 1

출력:
6 5 1
1 2 4
5 9 3

"""

N, T = map(int, input().split())

l_list = list(map(int, input().split()))
r_list = list(map(int, input().split()))
d_list = list(map(int, input().split()))

# Please write your code here.
for t in range(T):
    temp1 = l_list[N - 1]
    temp2 = r_list[N - 1]
    temp3 = d_list[N - 1]

    for n in range(N-1, 0, -1):
        l_list[n] = l_list[n - 1]

    for n in range(N-1, 0, -1):
        r_list[n] = r_list[n - 1]

    for n in range(N-1, 0, -1):
        d_list[n] = d_list[n - 1]

    r_list[0] = temp1
    d_list[0] = temp2
    l_list[0] = temp3

print(*l_list)
print(*r_list)
print(*d_list)
