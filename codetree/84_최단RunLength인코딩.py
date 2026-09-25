"""
CT 84  최단 Run Length 인코딩
https://www.codetree.ai/ko/trails/complete/curated-cards/test-shortest-run-length-encoding/description

풀이일 : 2026-09-25   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 64 MB / time_sec 1
난이도 : Medium  |  정답률 50.6%
제약   : - $1 \le |A| \le 10$

[문제]
길이가 $N$인 문자열 $A$가 주어졌을 때, 이 문자열을 오른쪽으로 순환 shift한 뒤 Run-Length Encoding을 적용하여 결과 길이가 최소가 되도록 하려고 합니다.

문자열을 오른쪽으로 $k$번 순환 shift한다는 것은, 마지막 $k$개의 문자를 순서 그대로 문자열 앞에 붙이는 연산을 의미합니다. 이때 $k$는 $0 \le k < |A|$ 범위의 정수 중 자유롭게 선택할 수 있으며, $k = 0$이면 원본 문자열을 그대로 사용합니다.

Run-Length Encoding이란 간단한 비손실 압축 방식으로, 연속해서 나온 문자와 연속해서 나온 개수로 나타내는 방식입니다. 예를 들어, 문자열 $A$가 `aaabbbbcaa`인 경우 순서대로 `a`가 $3$번, `b`가 $4$번, `c`가 $1$번 그리고 `a`가 $2$번 나왔으므로 Run-Length Encoding을 적용하게 되면 `a3b4c1a2`이 되며 길이는 $8$이 됩니다.

만약 문자열 $A$에 해당하는 `aaabbbbcaa`를 오른쪽으로 $2$번 순환 shift 하게 되면 `aaaaabbbbc`가 되며, 이에 Run-Length Encoding을 적용하게 되면 `a5b4c1`이 되므로 길이가 $6$이 되어 최소가 됩니다.

순환 shift를 진행하여 나올 수 있는 Run-Length Encoding 이후의 결과들 중 최소 길이를 구하는 프로그램을 작성해보세요.

[예제 1]
입력:
aaabbbbcaa

출력:
6


[예제 2]
입력:
aaaaaaaaaa

출력:
3

"""

from collections import deque
A = input()

# Please write your code here.
A = list(A)
# print(A)
A = deque(A)
N = len(A)

def encode(str_list):
    ret = ""
    cur_ch = str_list[0]
    cnt = 1
    for idx in range(1, N):
        # 다를 경우
        # print(idx)
        ch = A[idx]
        if cur_ch != ch:
            ret += cur_ch
            ret += str(cnt)
            cur_ch = ch
            cnt = 1
        else:
            cnt += 1

    ret += cur_ch
    ret += str(cnt)
    return len(ret)

def rotate(str_list):
    str_list.appendleft(str_list.pop())

answer = 10 ** 18

for i in range(N):
    answer = min(answer, encode(A))
    rotate(A)

print(answer)
