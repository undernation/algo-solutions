"""
BOJ 1991  트리 순회
https://cosal.aviss.kr/problems/detail/1991

풀이일 : 2026-10-27   결과: 품
한도   : time 2 초 / memory 128 MB

[채점] accepted  15/15  (3.716s)

[문제]
이진 트리를 입력받아 전위 순회(preorder traversal), 중위 순회(inorder traversal), 후위 순회(postorder traversal)한 결과를 출력하는 프로그램을 작성하시오.

[[IMG:1]]

예를 들어 위와 같은 이진 트리가 입력되면,
전위 순회한 결과: ABDCEFG // (루트) (왼쪽 자식) (오른쪽 자식) 중위 순회한 결과: DBAECFG // (왼쪽 자식) (루트) (오른쪽 자식) 후위 순회한 결과: DBEGFCA // (왼쪽 자식) (오른쪽 자식) (루트)
가 된다.

[예제 1]
입력:
7
A B C
B D .
C E F
E . .
F . G
D . .
G . .
출력:
ABDCEFG
DBAECFG
DBEGFCA
"""

N = int(input())

graph = dict()

for n in range(N):
    node, left, right = input().split()
    graph[node] = []
    graph[node].append(left)
    graph[node].append(right)

first_ret = ""


def first(start):
    global first_ret
    first_ret += start

    left = graph[start][0]

    if left != ".":
        first(left)

    right = graph[start][1]
    if right != ".":
        first(right)


first("A")
print(first_ret)
mid_ret = ""


def mid(start):
    global mid_ret

    left = graph[start][0]

    if left != ".":
        mid(left)
    mid_ret += start
    # print("wow")
    right = graph[start][1]
    if right != ".":
        mid(right)


mid("A")
print(mid_ret)

last_ret = ""


def last(start):
    global last_ret

    left = graph[start][0]

    if left != ".":
        last(left)

    right = graph[start][1]
    if right != ".":
        last(right)

    last_ret += start


last("A")

print(last_ret)
