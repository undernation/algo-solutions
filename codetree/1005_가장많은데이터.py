"""
CT 1005  가장 많은 데이터
https://www.codetree.ai/ko/trails/complete/curated-cards/intro-most-frequent-data/description

풀이일 : 2026-10-29   결과: 품
한도   : time Python3 1초 · C++17 1초 / memory 80 MB / time_sec 1
난이도 : Easy  |  정답률 83.8%
제약   : - $1 \le N \le 100\,000$
제약   : - $1 \le \texttt{각 문자열의 길이} \le 50$
제약   : - 모든 문자열은 알파벳 대소문자로 이루어져 있습니다.

[채점] accepted  1/1  (0.288s)

[문제]
알파벳 대소문자로 이루어진 문자열들이 중복을 허용하여 입력되었을때, 최대로 등장한 문자열의 등장 횟수를 출력하는 프로그램을 작성하세요.

[예제 1]
입력:
7
red
red
red
blue
blue
blue
green

출력:
3

"""

N = int(input())

cur_dict = dict()
max_val = 0
for n in range(N):
    word = input()

    if word not in cur_dict:
        cur_dict[word] = 0
        cur_dict[word] += 1
        max_val = max(max_val, cur_dict[word])
    else:
        cur_dict[word] += 1
        max_val = max(max_val, cur_dict[word])


print(max_val)
