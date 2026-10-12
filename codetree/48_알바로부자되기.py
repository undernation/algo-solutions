"""
CT 48  알바로 부자 되기
https://www.codetree.ai/ko/trails/complete/curated-cards/test-being-rich-by-working-part-time/description

풀이일 : 2026-10-12   결과: 못품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Easy  |  정답률 43.6%
제약   : - $1 \le N \le 1\,000$
제약   : - $1 \le s_i \le e_i \le 10^9$ $(1 \le i \le N)$
제약   : - $1 \le p_i \le 1\,000$ $(1 \le i \le N)$
제약   : - 알바가 시작되는 날짜가 증가하는 순으로 데이터가 주어진다고 가정해도 좋습니다.

[문제]
총 $N$개의 알바 정보가 주어졌을 때, 적절하게 알바를 선택하여 일하는 기간이 겹치지 않게 하면서 얻을 수 있는 돈이 최대가 되도록 하는 프로그램을 작성해보세요. 동시에 $2$개 이상의 알바를 하는 것은 불가능하며, 각각의 알바는 일해야 하는 기간을 모두 채워야 돈을 얻을 수 있습니다. 단, 한 알바를 끝낸 날과 다른 알바를 시작하는 날이 일치하는 경우에도 일하는 기간이 겹치는 것으로 간주합니다.

예를 들어 $N = 3$ 이고 알바 정보가 다음과 같이 주어진 경우를 생각해봅시다.

![](https://contents.codetree.ai/problems/48/images/problems-844ae536-c9fb-462a-b7f9-3e94efcd2692.png)

$1$, $2$번 알바를 같이 하게 된다면 일해야 하는 기간이 겹치게 되어 불가능합니다.

$1$, $3$번 알바를 같이 하게 된다면 겹치지 않게 일을 할 수 있고, 총 $25$ 만큼의 돈을 얻게 됩니다.

$2$번 알바만 하게 된다면 $26$ 만큼의 돈을 얻게 됩니다.

[예제 1]
입력:
2
1 5 10
5 10 6

출력:
10


[예제 2]
입력:
3
1 2 10
2 3 26
3 3 15

출력:
26

"""

N = int(input())
jobs = [tuple(map(int, input().split())) for _ in range(N)]
s = [job[0] for job in jobs]
e = [job[1] for job in jobs]
p = [job[2] for job in jobs]

# Please write your code here.

answer = 0
dp = [0] * N
jobs.sort()

for i in range(N):
    dp[i] = jobs[i][2]


for i in range(N):
    cs, ce, cp = jobs[i]
    for j in range(i):
        ps, pe, pp = jobs[j]
        # 겹치는 경우
        if pe < cs:
            dp[i] = max(dp[i], dp[j] + cp)
        # 안겹치는 경우

# print(dp)
print(max(dp))
