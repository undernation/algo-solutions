"""
CT 4088  게임 스튜디오에서 살아남기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-surviving-in-a-game-studio/description

풀이일 : 2026-10-16   결과: 못품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 67.8%
제약   : - $1 \le N \le 1\,000$

[문제]
남우가 최근 입사한 코디코디 게임 스튜디오는 사람을 해고하는 무서운 규칙이 있습니다.

코디코디 게임 스튜디오는 매일 각 사람의 업무량을 평가합니다. 이는 $'G'$(Good), $'B'$(Bad), $'T'$(Terrible)로 나뉩니다.

이때, $'T'$를 총합 세 번 이상 받았거나, 연속으로 $'B'$를 세 번 받은 사람은 코디코디 게임 스튜디오에서 해고됩니다.

예를 들어, 이 사람의 매일 평가가 $"TGGTT"$라면 해고됩니다. $'T'$를 총합 세 번 받았기 때문입니다. 또한 매일 평가가 $"BBTBBTBB"$라면 해고되지 않습니다. $'T'$를 총합 세 번 받지도, $'B'$를 연속으로 세 번 받지도 않았기 때문입니다.

이렇게 사람의 매일 평가를 문자열로 나타낸 것을 평가 문자열이라고 합니다. 총 $N$일을 살아남기 위해서 만들 수 있는 $N$자리의 평가 문자열의 가짓수를 $10^9 + 7$로 나눈 나머지를 구하세요.

[예제 1]
입력:
2

출력:
9


[예제 2]
입력:
4

출력:
67

"""

N = int(input())

dp = [list([0] * 4 for _ in range(4)) for _ in range(N + 1)]

print(dp)

dp[0][0][0] = 1

for idx in range(1, N + 1):

    # t 인 경우
    for t in range(2):

        # B 인 경우
        # 모르겠다.
