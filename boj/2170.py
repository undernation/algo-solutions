"""
BOJ 2170  선 긋기
https://cosal.aviss.kr/problems/detail/2170

풀이일 : 2026-09-23   결과: 못품
한도   : time 1 초 / memory 192 MB

[채점] accepted  17/17  (6.19s)

[문제]
매우 큰 도화지에 자를 대고 선을 그으려고 한다. 선을 그을 때에는 자의 한 점에서 다른 한 점까지 긋게 된다. 선을 그을 때에는 이미 선이 있는 위치에 겹쳐서 그릴 수도 있는데, 여러 번 그은 곳과 한 번 그은 곳의 차이를 구별할 수 없다고 하자.

이와 같은 식으로 선을 그었을 때, 그려진 선(들)의 총 길이를 구하는 프로그램을 작성하시오. 선이 여러 번 그려진 곳은 한 번씩만 계산한다.

[예제 1]
입력:
4
1 3
2 5
3 5
6 7
출력:
5
"""

N = int(input())
answer = 0
lines = [list(map(int, input().split())) for _ in range(N)]
lines.sort()
cur_start, cur_end = lines[0]
for start, end in lines[1:]:
    if start <= cur_end:
        cur_end = max(end, cur_end)

    else:
        answer += cur_end - cur_start
        cur_start, cur_end = start, end

answer += cur_end - cur_start

print(answer)
