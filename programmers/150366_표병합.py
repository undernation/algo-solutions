"""
PGS 150366  표 병합
https://school.programmers.co.kr/learn/courses/30/lessons/150366

풀이일 : 2026-10-24   결과: 못품 (1회차, AI 설명 참고 / 마지막 본인 코드 보존)
제약   : 50 x 50 표, 명령 최대 1,000개
검증·반례·AI 참고 코드 : notes/programmers/150366.md
첨부 대화 원문 : notes/programmers/150366-conversation.txt
메모   : 전체 값 UPDATE 미구현, PRINT에서 find 대신 직계 부모를 조회함.
"""

from collections import defaultdict


parent = dict()
value = dict()

def find(pos):
    global parent
    while parent[pos] != pos:
        parent[pos] = parent[parent[pos]]
        pos = parent[pos]

    return pos


def solution(commands):
    global parent, value
    answer = []

    for i in range(1, 51):
        for j in range(1, 51):
            parent[(i, j)] = (i, j)
            value[(i, j)] = None



    for command in commands:
        command = command.split()

        if command[0] == "UPDATE":

            if len(command) == 4:
                r = int(command[1])
                c = int(command[2])
                cur_value = command[3]

                root = find((r, c))
                value[root] = cur_value


            elif len(command) == 3:
                value1 = command[1]

                value2 = command[2]





        elif command[0] == "MERGE":
            r1 = int(command[1])
            c1 = int(command[2])

            r2 = int(command[3])
            c2 = int(command[4])

            root1 = find((r1, c1))

            root2 = find((r2, c2))
            if root1 == root2:
                continue
            value1 = value[root1]

            value2 = value[root2]



            if value1 is not None:
                merged_value = value1
            else:
                merged_value = value2

            parent[root2] = root1

            value[root1] = merged_value
            value[root2] = None





        elif command[0] == "UNMERGE":
            r = int(command[1])
            c = int(command[2])

            target = (r, c)

            root = find(target)

            saved_value = value[root]

            members = []

            for pos in parent:
                if find(pos) == root:
                    members.append(pos)


            for pos in members:
                parent[pos] = pos
                value[pos] = None

            value[target] = saved_value




        else:
            r = int(command[1])
            c = int(command[2])
            root = parent[(r, c)]

            if value[root] is None:
                answer.append("EMPTY")
            else:
                answer.append(value[root])

    return answer
