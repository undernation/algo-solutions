"""
BOJ 22251  빌런 호석
https://cosal.aviss.kr/problems/detail/22251

풀이일 : 2026-10-28   결과: 못품
한도   : time 1 초 / memory 512 MB

[채점] accepted  16/16  (15.712s)

[문제]
치르보기 빌딩은 1층부터 N층까지 이용이 가능한 엘리베이터가 있다. 엘리베이터의 층수를 보여주는 디스플레이에는 최대 K 자리의 수가 보인다. 수는 0으로 시작할 수도 있다. 0부터 9까지의 각 숫자가 디스플레이에 보이는 방식은 아래와 같다. 각 숫자는 7개의 표시등 중의 일부에 불이 들어오면서 표현된다.

[[IMG:1]]

예를 들어 K=4인 경우에 1680층과 501층은 아래와 같이 보인다.

[[IMG:2]]

[[IMG:3]]

빌런 호석은 치르보기 빌딩의 엘리베이터 디스플레이의 LED 중에서 최소 1개, 최대 P개를 반전시킬 계획을 세우고 있다. 반전이란 켜진 부분은 끄고, 꺼진 부분은 켜는 것을 의미한다. 예를 들어 숫자 1을 2로 바꾸려면 총 5개의 LED를 반전시켜야 한다. 또한 반전 이후에 디스플레이에 올바른 수가 보여지면서 1 이상 N 이하가 되도록 바꿔서 사람들을 헷갈리게 할 예정이다. 치르보기를 사랑하는 모임의 회원인 당신은 호석 빌런의 행동을 미리 파악해서 혼쭐을 내주고자 한다. 현재 엘리베이터가 실제로는 X층에 멈춰있을 때, 호석이가 반전시킬 LED를 고를 수 있는 경우의 수를 계산해보자.

[예제 1]
입력:
9 1 2 5
출력:
4

[예제 2]
입력:
48 2 5 35
출력:
30
"""

from itertools import combinations

N, K, P, X = map(int, input().split())

zero = 0

zero = (1, 2, 3, 4, 5, 6)

num_dict = {
    0:(1, 2, 3, 4, 5, 6),
    1:(3, 4),
    2:(0, 2, 3, 5, 6),
    3:(0, 2, 3, 4, 5),
    4:(0, 1, 3, 4),
    5:(0, 1, 2, 4, 5),
    6:(0, 1, 2, 4, 5, 6),
    7:(2, 3, 4),
    8:(0, 1, 2, 3, 4, 5, 6),
    9:(0, 1, 2, 3, 4, 5)
}


num_list = [0] * 10

for key, value in num_dict.items():

    temp = 0
    for num in value:
        temp |= (1 << num)

    num_list[key] = temp

origin = str(X).zfill(K)

answer = 0

for floor in range(1, N + 1):

    if floor == X:
        continue

    target = str(floor).zfill(K)

    count = 0

    for a, b in zip(origin, target):
        count += bin(num_list[int(a)] ^ num_list[int(b)]).count('1')

    if count <= P:
        answer += 1

print(answer)
