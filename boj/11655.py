"""
BOJ 11655  ROT13
https://cosal.aviss.kr/problems/detail/11655

풀이일 : 2026-08-12   결과: 품
한도   : time 1 초 / memory 256 MB

[채점] accepted  28/28  (6.899s)

[문제]
ROT13은 카이사르 암호의 일종으로 영어 알파벳을 13글자씩 밀어서 만든다.

예를 들어, "Baekjoon Online Judge"를 ROT13으로 암호화하면 "Onrxwbba Bayvar Whqtr"가 된다. ROT13으로 암호화한 내용을 원래 내용으로 바꾸려면 암호화한 문자열을 다시 ROT13하면 된다. 앞에서 암호화한 문자열 "Onrxwbba Bayvar Whqtr"에 다시 ROT13을 적용하면 "Baekjoon Online Judge"가 된다.

ROT13은 알파벳 대문자와 소문자에만 적용할 수 있다. 알파벳이 아닌 글자는 원래 글자 그대로 남아 있어야 한다. 예를 들어, "One is 1"을 ROT13으로 암호화하면 "Bar vf 1"이 된다.

문자열이 주어졌을 때, "ROT13"으로 암호화한 다음 출력하는 프로그램을 작성하시오.

[예제 1]
입력:
Baekjoon Online Judge
출력:
Onrxwbba Bayvar Whqtr

[예제 2]
입력:
One is 1
출력:
Bar vf 1
"""

def solution(S):
    answer = ""

    # 여기에 풀이 작성
    for s in S:
        if ("a" <= s <= "z"):
            answer += chr((ord(s) - ord("a") + 13) % 26 + ord("a"))
        elif ("A" <= s <= "Z"):
            answer += chr((ord(s) - ord("A") + 13) % 26 + ord("A"))
        else:
            answer += s

    return answer


if __name__ == "__main__":
    S = input().rstrip("\n")

    print(solution(S))
