"""
BOJ 25757  임스와 함께하는 미니게임
https://cosal.aviss.kr/problems/detail/25757

풀이일 : 2026-08-23   결과: 품
한도   : time 1 초 / memory 512 MB

[채점] accepted  17/17  (4.405s)

[문제]
임스가 미니게임을 같이할 사람을 찾고 있습니다.

플레이할 미니게임으로는 윷놀이 Y, 같은 그림 찾기 F, 원카드 O가 있습니다. 각각 2, 3, 4 명이서 플레이하는 게임이며 인원수가 부족하면 게임을 시작할 수 없습니다.

사람들이 임스와 같이 플레이하기를 신청한 횟수 N과 임스가 플레이할 게임의 종류가 주어질 때, 최대 몇 번이나 임스와 함께 게임을 플레이할 수 있는지 구하시오.

임스와 여러 번 미니게임을 플레이하고자 하는 사람이 있으나, 임스는 한 번 같이 플레이한 사람과는 다시 플레이하지 않습니다.

임스와 함께 플레이하고자 하는 사람 중 동명이인은 존재하지 않습니다. 임스와 lms0806은 서로 다른 인물입니다.

[예제 1]
입력:
7 Y
lms0806
lms0806
exponentiale
lms0806
jthis
lms0806
leo020630
출력:
4

[예제 2]
입력:
12 F
lms0806
powergee
skeep194
lms0806
tony9402
lms0806
wider93
lms0806
mageek2guanaah
lms0806
jthis
lms0806
출력:
3

[예제 3]
입력:
12 O
lms0806
mageek2guanaah
jthis
lms0806
exponentiale
lms0806
leo020630
lms0806
powergee
lms0806
skeep194
lms0806
출력:
2
"""

import sys
input = sys.stdin.readline
N, game = input().split()
members = set()
for _ in range(int(N)):
    members.add(input().strip())

if game == "Y":
    player = 1
elif game == "F":
    player = 2
else:
    player = 3
print(len(members) // player)
