"""
SWEA 99994  [SSAFY A형] 면접 최소 점수
https://lab.ssafy.com/s16/b06/lectures/-/blob/2fdc0ae590f6731564ff0014568d70833c474f2a/99_exam/A/%EC%B5%9C%EC%86%8C%EC%A0%90%EC%88%98/%EC%B5%9C%EC%86%8C%EC%A0%90%EC%88%98.md

풀이일 : 2026-10-21   결과: 품
한도   : time 원본 MD 미표기 · 아카이브 기본 제한 적용 / memory 원본 MD 미표기
제약   : 3 ≤ N ≤ 500
제약   : 1 ≤ M ≤ N
제약   : 2 ≤ K ≤ N
제약   : 풀이가 불가능한 경우는 주어지지 않는다.
제약   : 정답은 32비트 int 범위를 넘지 않는다.

[채점] wrong_answer  0/2  (8.081s)

[문제]
강의자료의 설명 MD를 옮긴 A형 연습 문제입니다. 99994는 아카이브 내부 번호이며 공식 SWEA 번호가 아닙니다.

원본 입력 파일의 T는 30이지만 실제 입력은 31개입니다. 원본 파일은 그대로 보존하고, 이 화면에는 MD 예제 3개와 나머지 제공 입력 28개를 나누어 등록했습니다. 원본 MD에는 시간·메모리 제한이 없어 채점 시 아카이브 기본 제한이 적용됩니다.

철수는 N개의 문제가 순차적으로 주어지는 면접에서 정확히 M개의 문제를 맞혔다. 어떤 문제를 맞혔는지는 기억나지 않지만, 정확히 M개를 맞혔다는 사실은 확실하다.

이 면접에서는 연속으로 문제를 맞힐 경우 점수를 더 많이 주는 카운터 시스템이 적용된다. 점수 계산 방식은 다음과 같다.

1. 카운터의 초기값은 0이다.
2. 문제를 틀릴 경우 카운터는 0으로 초기화된다.
3. 문제를 맞힐 경우 1점을 획득한 후 카운터가 1 증가한다.
4. 카운터가 주어진 값 K에 도달하면, 카운터는 0으로 초기화되고 현재까지 획득한 총점이 2배가 된다.

철수가 M개의 문제를 맞힐 수 있는 모든 경우 중 최소 총점을 구하라.

[예제 1]
입력:
3
8 7 3
3 3 3
5 2 3

출력:
#1 10
#2 6
#3 2

"""

from collections import deque
import time
start = time.perf_counter()
T = int(input())
for tc in range(1, T + 1):
    N, M, K = map(int, input().split())
    # dp n, M, k
    INF = 10 ** 18
    dp = [list([INF] * (K + 1) for _ in range(M + 1)) for _ in range(N + 1)]
    
    dp[0][0][0] = 0
    
    for n in range(1, N + 1):
    
        for m in range(M + 1):
    
            for k in range(K):
    
                cur_score = dp[n - 1][m][k]
    
                if cur_score == INF:
                    continue
    
    
    
                # 현재 문제를 맞춘 경우
                if m <= M - 1:
                    nxt_score = cur_score + 1
    
                    if k == K - 1:
                        dp[n][m + 1][0] = min(dp[n][m+1][0], nxt_score * 2)
                    else:
                        dp[n][m + 1][k + 1] = min(dp[n][m + 1][k + 1], nxt_score)
    
                # 현재 문제를 틀린 경우 카운터 초기화방식으로
                dp[n][m][0] = min(dp[n][m][0], cur_score)
    # for i in dp:
    #     print(i)
    
    print(f"#{tc} {min(dp[N][M])}")
    end = time.perf_counter()
    print(f"{end - start}")
