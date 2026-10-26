"""
PGS 154538  숫자 변환하기
https://school.programmers.co.kr/learn/courses/30/lessons/154538

풀이일 : 2026-10-26   결과: 품
제약   : 1 ≤ x ≤ y ≤ 1,000,000
제약   : 1 ≤ n < y

[채점] wrong_answer  0/3  (0.814s)

[문제]
자연수 `x`를 `y`로 변환하려고 합니다. 사용할 수 있는 연산은 다음과 같습니다.

- `x`에 `n`을 더합니다

- `x`에 2를 곱합니다.

- `x`에 3을 곱합니다.

자연수 `x`, `y`, `n`이 매개변수로 주어질 때, `x`를 `y`로 변환하기 위해 필요한 최소 연산 횟수를 return하도록 solution 함수를 완성해주세요. 이때 `x`를 `y`로 만들 수 없다면 -1을 return 해주세요.

---

제한사항

- 1 ≤ `x` ≤ `y` ≤ 1,000,000

- 1 ≤ `n` < `y`

---

입출력 예

| x | y | n | result |
| --- | --- | --- | --- |
| 10 | 40 | 5 | 2 |
| 10 | 40 | 30 | 1 |
| 2 | 5 | 4 | -1 |

---

입출력 예 설명

입출력 예 #1

`x`에 2를 2번 곱하면 40이 되고 이때가 최소 횟수입니다.

입출력 예 #2

`x`에 `n`인 30을 1번 더하면 40이 되고 이때가 최소 횟수입니다.

입출력 예 #3

`x`를 `y`로 변환할 수 없기 때문에 -1을 return합니다.

[예제 1]
입력:
10 40 5
출력:
2

[예제 2]
입력:
10 40 30
출력:
1

[예제 3]
입력:
2 5 4
출력:
-1
"""

def solution(x, y, n):
    answer = 0
    
    INF = 10 ** 18
    dp = [INF] * (y + 1)
    dp[x] = 0
    for i in range(x, y + 1):
        cur_num = dp[i]
        if cur_num == INF:
            continue
            
        nxt_num = i + n
        if nxt_num <= y:
            dp[nxt_num] = min(dp[nxt_num], cur_num + 1)
            
        nxt_num = i * 2
        if nxt_num <= y:
            dp[nxt_num] = min(dp[nxt_num], cur_num + 1)
            
        nxt_num = i * 3
        if nxt_num <= y:
            dp[nxt_num] = min(dp[nxt_num], cur_num + 1)
            
            
    if dp[y] == INF:
        return -1
    else:
        return dp[y]
