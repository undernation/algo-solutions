"""단일코어 Python 성능 벤치 — 채점 환경 비교용."""
import time, sys, platform


def bench(name, fn, *a):
    t0 = time.perf_counter()
    r = fn(*a)
    el = time.perf_counter() - t0
    print("  %-22s %7.3f초   %s" % (name, el, r))
    return el


def sieve(n):
    s = bytearray([1]) * (n + 1)
    s[0] = s[1] = 0
    i = 2
    while i * i <= n:
        if s[i]:
            s[i*i::i] = bytearray(len(s[i*i::i]))
        i += 1
    return sum(s)


def loop_add(n):
    t = 0
    for i in range(n):
        t += i
    return t


def dp2d(n):
    dp = [[0] * n for _ in range(n)]
    for i in range(1, n):
        for j in range(1, n):
            dp[i][j] = (dp[i-1][j] + dp[i][j-1] + 1) % 1000000007
    return dp[n-1][n-1]


def strops(n):
    parts = []
    for i in range(n):
        parts.append(str(i))
    return len("".join(parts))


print("=" * 58)
print(" CPU : %s" % platform.processor()[:52])
print(" Py  : %s (%s)" % (sys.version.split()[0], platform.machine()))
print("=" * 58)
tot = 0
tot += bench("에라토스테네스 4e6", sieve, 4_000_000)
tot += bench("단순 루프 1e7", loop_add, 10_000_000)
tot += bench("2D DP 1500x1500", dp2d, 1500)
tot += bench("문자열 100만", strops, 1_000_000)
print("-" * 58)
print("  %-22s %7.3f초" % ("합계", tot))
print("=" * 58)
