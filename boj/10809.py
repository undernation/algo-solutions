"""
BOJ 10809  알파벳 찾기
https://cosal.aviss.kr/problems/detail/10809

풀이일 : 2026-08-12   결과: 품
한도   : time 1 초 / memory 256 MB

[채점] accepted  15/15  (3.624s)

[문제]
알파벳 소문자로만 이루어진 단어 S가 주어진다. 각각의 알파벳에 대해서, 단어에 포함되어 있는 경우에는 처음 등장하는 위치를, 포함되어 있지 않은 경우에는 -1을 출력하는 프로그램을 작성하시오.

[예제 1]
입력:
baekjoon
출력:
1 0 -1 -1 2 -1 -1 -1 -1 4 3 -1 -1 7 5 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1
"""

def solution(S):
    answer = []

    # 여기에 풀이 작성
    answer = [-1] * 26

    for i in range(26):
        answer[i] = S.find(chr(i + ord("a")))

    return answer


if __name__ == "__main__":
    S = input().strip()

    result = solution(S)

    print(*result)
