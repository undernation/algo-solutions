"""
BOJ 14891  톱니바퀴
https://cosal.aviss.kr/problems/detail/14891

풀이일 : 2026-08-08   결과: 품
한도   : time 2 초 / memory 512 MB

[채점] accepted  18/18  (5.897s)

[문제]
총 8개의 톱니를 가지고 있는 톱니바퀴 4개가 아래 그림과 같이 일렬로 놓여져 있다. 또, 톱니는 N극 또는 S극 중 하나를 나타내고 있다. 톱니바퀴에는 번호가 매겨져 있는데, 가장 왼쪽 톱니바퀴가 1번, 그 오른쪽은 2번, 그 오른쪽은 3번, 가장 오른쪽 톱니바퀴는 4번이다.

[[IMG:1]]

이때, 톱니바퀴를 총 K번 회전시키려고 한다. 톱니바퀴의 회전은 한 칸을 기준으로 한다. 회전은 시계 방향과 반시계 방향이 있고, 아래 그림과 같이 회전한다.

[[IMG:2]]

[[IMG:3]]

톱니바퀴를 회전시키려면, 회전시킬 톱니바퀴와 회전시킬 방향을 결정해야 한다. 톱니바퀴가 회전할 때, 서로 맞닿은 극에 따라서 옆에 있는 톱니바퀴를 회전시킬 수도 있고, 회전시키지 않을 수도 있다. 톱니바퀴 A를 회전할 때, 그 옆에 있는 톱니바퀴 B와 서로 맞닿은 톱니의 극이 다르다면, B는 A가 회전한 방향과 반대방향으로 회전하게 된다. 예를 들어, 아래와 같은 경우를 살펴보자.

[[IMG:4]]

두 톱니바퀴의 맞닿은 부분은 초록색 점선으로 묶여있는 부분이다. 여기서, 3번 톱니바퀴를 반시계 방향으로 회전했다면, 4번 톱니바퀴는 시계 방향으로 회전하게 된다. 2번 톱니바퀴는 맞닿은 부분이 S극으로 서로 같기 때문에, 회전하지 않게 되고, 1번 톱니바퀴는 2번이 회전하지 않았기 때문에, 회전하지 않게 된다. 따라서, 아래 그림과 같은 모양을 만들게 된다.

[[IMG:5]]

위와 같은 상태에서 1번 톱니바퀴를 시계 방향으로 회전시키면, 2번 톱니바퀴가 반시계 방향으로 회전하게 되고, 2번이 회전하기 때문에, 3번도 동시에 시계 방향으로 회전하게 된다. 4번은 3번이 회전하지만, 맞닿은 극이 같기 때문에 회전하지 않는다. 따라서, 아래와 같은 상태가 된다.

[[IMG:6]]

톱니바퀴의 초기 상태와 톱니바퀴를 회전시킨 방법이 주어졌을 때, 최종 톱니바퀴의 상태를 구하는 프로그램을 작성하시오.

[예제 1]
입력:
10101111
01111101
11001110
00000010
2
3 -1
1 1
출력:
7

[예제 2]
입력:
11111111
11111111
11111111
11111111
3
1 1
2 1
3 1
출력:
15

[예제 3]
입력:
10001011
10000011
01011011
00111101
5
1 1
2 1
3 1
4 1
1 -1
출력:
6

[예제 4]
입력:
10010011
01010011
11100011
01010101
8
1 1
2 1
3 1
4 1
1 -1
2 -1
3 -1
4 -1
출력:
5
"""

from collections import deque


mag1 = deque(map(int, input().strip()))
mag2 = deque(map(int, input().strip()))
mag3 = deque(map(int, input().strip()))
mag4 = deque(map(int, input().strip()))

magnets = [0, mag1, mag2, mag3, mag4]

K = int(input())

commands = []

for _ in range(K):
    a, b = map(int, input().split())
    commands.append([a, b])


def forward_check(cur_mag, nxt_mag):
    if magnets[cur_mag][2] != magnets[nxt_mag][6]:
        return True

    return False


def back_check(cur_mag, nxt_mag):
    if magnets[cur_mag][6] != magnets[nxt_mag][2]:
        return True

    return False


def toggle(cur_dir):
    if cur_dir == 1:
        return -1
    else:
        return 1


def check_dir(cur_mag, direction):

    turn_dir = [0] * 5
    turn_dir[cur_mag] = direction

    nxt_mag = cur_mag + 1
    temp_dir = direction

    while nxt_mag < 5:
        if forward_check(nxt_mag - 1, nxt_mag):
            temp_dir = toggle(temp_dir)
            turn_dir[nxt_mag] = temp_dir
        else:
            break

        nxt_mag += 1

    nxt_mag = cur_mag - 1
    temp_dir = direction

    while nxt_mag > 0:
        if back_check(nxt_mag + 1, nxt_mag):
            temp_dir = toggle(temp_dir)
            turn_dir[nxt_mag] = temp_dir
        else:
            break

        nxt_mag -= 1

    return turn_dir


def real_rotate(mag_num, direction):
    if direction == 1:
        # 시계 방향 회전
        magnets[mag_num].appendleft(magnets[mag_num].pop())

    elif direction == -1:
        # 반시계 방향 회전
        magnets[mag_num].append(magnets[mag_num].popleft())


def rotate(mag_num, direction):
    turn_dir = check_dir(mag_num, direction)

    for i in range(1, 5):
        if turn_dir[i] != 0:
            cur_dir = turn_dir[i]
            real_rotate(i, cur_dir)


for a, b in commands:
    rotate(a, b)


answer = 0

for i in range(1, 5):
    if magnets[i][0] == 1:
        answer += 2 ** (i - 1)


print(answer)
