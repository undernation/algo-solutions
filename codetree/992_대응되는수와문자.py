"""
CT 992  대응되는 수와 문자
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-corresponding-numbers-and-characters/description

풀이일 : 2026-10-30   결과: 품
한도   : time Python3 1초 · C++17 1초 / memory 80 MB / time_sec 1
난이도 : Easy  |  정답률 77.2%
제약   : - $1 \le N, M \le 100\,000$
제약   : - $1 \le \texttt{문자열의 길이} \le 20$
제약   : - $1 \le \texttt{조사할 정수} \le N$

[채점] accepted  2/2  (1.215s)

[문제]
$N$개의 문자열이 주어집니다. 각 문자열은 $1$부터 $N$까지 주어진 순서대로 각각 하나의 정수와 대응됩니다.   
이 후, 조사할 $M$개의 정수 혹은 문자열이 주어졌을 때, 정수에 대해서는 대응되는 문자열을, 문자열에 대해서는 대응되는 정수를 출력하는 프로그램을 작성해보세요.

[예제 1]
입력:
5 2
a
b
c
d
e
3
c

출력:
c
3


[예제 2]
입력:
5 3
qw
er
ty
ui
op
2
ty
op

출력:
er
3
5

"""

from curses.ascii import isdigit

N, M = map(int, input().split())

# Note: Using 1-based indexing for words as per C++ code
words = [""] + [input() for _ in range(N)]
queries = [input() for _ in range(M)]

temp_dict = dict()

# Please write your code here.
for idx, word in enumerate(words):
    temp_dict[word] = idx

for word in queries:
    if isdigit(word[0]):
        print(words[int(word)])

    else:
        print(temp_dict[word])
