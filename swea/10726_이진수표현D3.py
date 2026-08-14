"""
SWEA 10726  이진수 표현 D3
https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AXRSXf_a9qsDFAXS

풀이일 : 2026-08-14   결과: 품
한도   : time 10000개 테스트케이스를 합쳐서 C의 경우 1초 / C++의 경우 1초 / Java의 경우 2초 / Python의 경우 2초 / memory 힙, 정적 메모리 합쳐서 256MB 이내, 스택 메모리 1MB 이내 / time_sec 2
난이도 : Master  |  정답률 59.73%

[문제]
정수 N, M 이 주어질 때, M의 이진수 표현의 마지막 N 비트가 모두 1로 켜져 있는지 아닌지를 판별하여 출력하라.

[예제 1]
입력:
5
4 0
4 30
4 47
5 31
5 62
출력:
#1 OFF
#2 OFF
#3 ON
#4 ON
#5 OFF
"""

T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    N, M = map(int, input().split())
    temp = str(bin(M))
    cur_bit = temp[len(temp) - N:]
    if cur_bit.count("1") == N:
        answer = "ON"
    else:
        answer = "OFF"

    print(f"#{test_case} {answer}")
