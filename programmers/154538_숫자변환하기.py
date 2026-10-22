"""
PGS 154538  숫자 변환하기
https://school.programmers.co.kr/learn/courses/30/lessons/154538

풀이일 : 2026-10-22   결과: 틀림 (2회차, 사용자 제출 원본 보존)
사용자는 프로그래머스 통과를 보고했으나 독립 검증에서 반례를 확인했다.
검증   : 공식 예제 3/3 통과; solution(2, 4, 3)은 -1, 정답은 1.
수정본·검증 결과 : notes/programmers/154538.md
"""

def solution(x, y, n):
    answer = 0
    INF = 10 ** 18
    dp = [INF] * (y + 1)

    dp[x] = 0

    for i in range(x, y - n + 1):

        if dp[i] == INF:
            continue

        cur_cnt = dp[i]

        nxt_num = i + n

        if nxt_num <= y:
            dp[nxt_num] = min(dp[nxt_num], cur_cnt + 1)

        nxt_num = i * 2
        if nxt_num <= y:
            dp[nxt_num] = min(dp[nxt_num], cur_cnt + 1)

        nxt_num = i * 3
        if nxt_num <= y:
            dp[nxt_num] = min(dp[nxt_num], cur_cnt + 1)

    if dp[y] == INF:
        return -1
    else:
        return dp[y]
