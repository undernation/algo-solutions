"""
BOJ 10822  더하기
https://cosal.aviss.kr/problems/detail/10822

풀이일 : 2026-08-12   결과: 품
한도   : time 1 초 / memory 256 MB

[채점] accepted  1/1  (0.217s)

[문제]
숫자와 콤마로만 이루어진 문자열 S가 주어진다. 이때, S에 포함되어있는 자연수의 합을 구하는 프로그램을 작성하시오.

S의 첫 문자와 마지막 문자는 항상 숫자이고, 콤마는 연속해서 주어지지 않는다. 주어지는 수는 항상 자연수이다.

[예제 1]
입력:
10,20,30,50,100
출력:
210
"""

word = input()
word = word.split(',')
word = sum(map(int, word))
print(word)
