"""
BOJ 5215  햄버거 다이어트

풀이일 : 2026-09-23   결과: 못품
"""


# Please write your code here.
T = int(input())
for tc in range(1, T + 1):
    N, L = map(int, input().split())

    dp = [0] * (L + 1)

    for _ in range(N):
        taste, calorie = map(int, input().split())

        for c in range(L, calorie - 1, -1):
            dp[c] = max(
                dp[c],
                dp[c - calorie] + taste
            )
    print(f"#{tc} {dp[L]}")
