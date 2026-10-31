"""
CT 2025  순서를 바꾸었을 때 같은 단어 그룹화하기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-group-same-word/description

풀이일 : 2026-10-31   결과: 품
한도   : time Python3 1초 · C++17 1초 / memory 80 MB / time_sec 1
난이도 : Easy  |  정답률 83.2%
제약   : - $1 \le N \le 1\,000$
제약   : - $1 \le \texttt{단어의 길이} \le 1\,000$
제약   : - 알파벳만이 입력으로 주어지며, 대소문자를 구분합니다.

[채점] accepted  2/2  (0.69s)

[문제]
$N$개의 단어가 입력으로 주어질 때, 한 단어에 속한 문자들의 순서를 바꾸어 만들 수 있는 단어들은 같은 그룹에 속한다고 정의된다고 합니다. 이 때 동일한 그룹에 속한 단어가 가장 많은 그룹의 단어 개수를 출력하는 코드를 작성해보세요.

[예제 1]
입력:
4
aba
aab
naa
baa

출력:
3


[예제 2]
입력:
5
aAB
bAB
aBA
BaA
BBA

출력:
3

"""

from collections import defaultdict

N = int(input())
words = [input() for _ in range(N)]

# Please write your code here.

# print(ord("a"))
# print(ord("A"))
# 
# print(ord("z"))
# print(ord("Z"))
#


groups = defaultdict(int)
answer = 0
for word in words:
    num_list = [0] * (122 - 65 + 1)
    for ch in word:
        num_list[ord(ch) - ord("A")] += 1
    key = tuple(num_list)
    groups[key] += 1
    answer = max(answer, groups[key])

print(answer)
