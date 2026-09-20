"""
SWEA 5260  [S/W 문제해결 최적화] 3일차 - 부분 집합의 합 D4
https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AWUTWmcqLDcDFAVT

풀이일 : 2026-09-20   결과: 못품
한도   : time 10개 테스트케이스를 합쳐서 Python의 경우 2초 / memory 힙, 정적 메모리 합쳐서 256MB 이내, 스택 메모리 1MB 이내 / time_sec 2
난이도 : Master  |  정답률 42.98%

[채점] accepted  1/1  (0.301s)

[문제]
1부터 N까지 양의 정수를 원소로 갖는 집합이 있다. 이 집합의 모든 부분 집합에 대해 원소의 합이 K인 경우의 수 M을 알아내려고 한다.

부분 집합의 개수는 2N개이기 때문에 모든 부분 집합을 만들어 확인하려면 시간이 오래 걸리지만, 정수 i를 부분 집합에 포함시킬지 고려할 때 이미 부분 집합에 포함시킨 원소의 합 S와 아직 고려하지 않은 숫자들의 합 R을 동시에 활용하면 시간을 단축할 수 있다고 한다.

이를 활용해 M을 출력하는 프로그램을 만드시오.

[예제 1]
입력:
3
10 7
10 53
100 5050
출력:
#1 5
#2 1
#3 1
"""


T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    N, K = map(int, input().split())
    dp = [0] * (K + 1)

    dp[0] = 1

    for num in range(1, N + 1):
        for s in range(K, num - 1, -1):
            dp[s] += dp[s - num]

    answer = dp[K]
    print(f"#{test_case} {answer}")
