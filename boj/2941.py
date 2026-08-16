"""
BOJ 2941  크로아티아 알파벳
https://cosal.aviss.kr/problems/detail/2941

풀이일 : 2026-08-16   결과: 품
한도   : time 1 초 / memory 128 MB

[채점] accepted  19/19  (4.61s)

[문제]
예전에는 운영체제에서 크로아티아 알파벳을 입력할 수가 없었다. 따라서, 다음과 같이 크로아티아 알파벳을 변경해서 입력했다.

크로아티아 알파벳	변경
č	c=
ć	c-
dž	dz=
đ	d-
lj	lj
nj	nj
š	s=
ž	z=

예를 들어, ljes=njak은 크로아티아 알파벳 6개(lj, e, š, nj, a, k)로 이루어져 있다. 단어가 주어졌을 때, 몇 개의 크로아티아 알파벳으로 이루어져 있는지 출력한다.

dž는 무조건 하나의 알파벳으로 쓰이고, d와 ž가 분리된 것으로 보지 않는다. lj와 nj도 마찬가지이다. 위 목록에 없는 알파벳은 한 글자씩 센다.

[예제 1]
입력:
ljes=njak
출력:
6

[예제 2]
입력:
ddz=z=
출력:
3

[예제 3]
입력:
nljj
출력:
3

[예제 4]
입력:
c=c=
출력:
2

[예제 5]
입력:
dz=ak
출력:
3
"""

import sys
input = sys.stdin.readline

N = input().strip()

alphas = ["c=", "c-", "dz=", "d-", "lj", "nj", "s=", "z="]

idx = 0
cnt = 0
# print(len(N))
while idx < len(N):
    # print(idx)
    if N[idx:idx + 2] in alphas:
        idx += 2
        cnt += 1
    elif N[idx:idx + 3] in alphas:
        idx += 3
        cnt += 1
    else:
        idx += 1
        cnt += 1
print(cnt)
