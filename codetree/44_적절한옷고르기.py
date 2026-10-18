"""
CT 44  적절한 옷 고르기
https://www.codetree.ai/ko/trails/complete/curated-cards/intro-select-proper-clothes/description

풀이일 : 2026-10-18   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Easy  |  정답률 74.4%
제약   : - $1 \le N \le 200$
제약   : - $2 \le M \le 200$
제약   : - $1 \le s_i \le e_i \le M$ $(1 \le i \le N)$
제약   : - $1 \le v_i \le 1\,000$ $(1 \le i \le N)$
제약   : - 각 날짜마다 최소 한 개의 옷은 입을 수 있도록 입력이 주어진다고 가정해도 좋습니다.

[채점] accepted  2/2  (0.519s)

[문제]
$N$개의 옷에 대한 정보가 주어졌을 때, $M$일 동안 옷을 적절하게 입어 만족도의 합을 최대화 하려고 합니다. 각각의 옷은 입을 수 있는 기간이 정해져있고, $M$일 안에 같은 옷을 여러 번 입어도 됩니다. 총 만족도는 $M$개의 날 중 각각의 인접한 날짜에 입은 옷의 화려함의 차이의 절댓값의 합으로 정의됩니다. 또한, 하루에 정확히 하나의 옷을 입어야만 합니다.

예를 들어 $N = 3$, $M = 5$ 이고 세 옷의 정보가 다음과 같다고 해봅시다.

![](https://contents.codetree.ai/problems/44/images/problems-75ea9244-5be5-420b-ad40-09fca9feaab9.png)

$1$, $1$, $1$, $1$, $3$ 순서로 옷을 입게 되면, $4$번째 날에는 $1$번 옷을 입을 수 없기 때문에 불가능합니다.

$1$, $1$, $2$, $3$, $3$ 순서로 옷을 입게 되면 각 날의 화려함은 $39$, $39$, $20$, $25$, $25$이기 때문에 만족도의 합은 $|39 - 39| + |39 - 20| + |20 - 25| + |25 - 25| = 24$ 가 됩니다.

$1$, $2$, $1$, $2$, $3$ 순서로 옷을 입게 되면 각 날의 화려함은 $39$, $20$, $39$, $20$, $25$이기 때문에 만족도의 합은 $|39 - 20| + |20 - 39| + |39 - 20| + |20 - 25| = 62$ 가 됩니다.

최대 만족도를 구하는 프로그램을 작성해보세요.

[예제 1]
입력:
2 3
2 3 10
1 2 5

출력:
5


[예제 2]
입력:
3 5
1 3 39
1 4 20
4 5 25

출력:
62

"""

N, M = map(int, input().split())
clothes = [tuple(map(int, input().split())) for _ in range(N)]
s = [x[0] for x in clothes]
e = [x[1] for x in clothes]
v = [x[2] for x in clothes]

NEG = -10 ** 18

dp = [[NEG] * N for _ in range(M)]

# init

for n in range(N):
    cur_s = s[n] - 1
    cur_e = e[n] - 1

    if cur_s <= 0 <= cur_e:
        dp[0][n] = 0

for m in range(1, M):


    for j in range(N):
        for n in range(N):
            if dp[m - 1][j] == NEG:
                continue
            # print(m, j, n)
            cur_s = s[n] - 1
            cur_e = e[n] - 1

            cur_val = v[n]
            last_val = v[j]
            # print("cur vs last", cur_val, last_val)
            if cur_s <= m <= cur_e:
                dp[m][n] = max(dp[m][n], dp[m - 1][j] + abs(last_val - cur_val))

print(max(dp[M - 1]))
