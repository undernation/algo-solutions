"""
CT 17  1차원 폭발 게임
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-The-1D-bomb-game/description

풀이일 : 2026-09-25   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 64 MB / time_sec 1
난이도 : Medium  |  정답률 44.0%
제약   : - $1 \le N \le 100$
제약   : - $1 \le M \le 100$
제약   : - $1 \le A_i \le 100$ $(1 \le i \le N)$

[문제]
$1$이상 $100$이하의 정수가 적혀있는 $N$개의 폭탄이 쌓여있습니다.

![](https://contents.codetree.ai/problems/17/images/problems-499267d1-9e07-4934-9dc3-c7486956454e.png)

이때 $M$개 이상 연속으로 같은 정수가 적혀있는 폭탄들은 터지게 되고, 중력에 의해 위에 있던 폭탄들은 밑으로 떨어지게 됩니다. $M$개 이상 연속한 폭탄은 부분만 터져서는 안되고 전부 다 터져야 합니다.

예를 들어 다음과 같은 예시에서 $M$이 $2$인 경우 $3$이라는 정수가 연속하여 $M$번 이상 나오므로 그 폭탄들이 터지게 됩니다.

![](https://contents.codetree.ai/problems/17/images/problems-52a8c6a3-ebe8-4da5-a68d-01796fd71ee8.png)

만약 $M$개 이상인 폭탄들의 쌍이 여러 개라면 동시에 터지게 됩니다.

![](https://contents.codetree.ai/problems/17/images/problems-cffa3b0a-4b34-4d6b-bc91-d3cfa1f33bba.png)

이 과정을 $M$개 이상 연속한 정수를 갖는 폭탄들이 존재하지 않을때까지 계속 반복했을 때, 최종 결과를 출력하는 프로그램을 작성해주세요.

위의 예에서 $M=2$인 경우 진행 과정은 다음과 같습니다.

![](https://contents.codetree.ai/problems/17/images/problems-7f69f140-c41e-4b24-84b3-f6c7e9e775c4.png)

[예제 1]
입력:
4 2
1
2
2
1

출력:
0


[예제 2]
입력:
4 2
1
2
2
3

출력:
2
1
3


[예제 3]
입력:
8 2
1
3
3
3
2
1
1
2

출력:
1
1

"""

N, M = map(int, input().split())
numbers = [int(input()) for _ in range(N)]

# Please write your code here.

def explode(num_list):
    if len(num_list) == 0:
        return [], False

    temp_list = []
    cnt = 1
    cur_num = num_list[0]
    cur_N = len(num_list)
    for idx in range(1, cur_N):
        if num_list[idx] != cur_num:
            temp_list.append([cur_num, cnt])
            cnt = 1
            cur_num = num_list[idx]
        else:
            cnt += 1

    temp_list.append([cur_num, cnt])
    # print(temp_list)
    ret = []
    is_explode = False

    for num, cnt in temp_list:
        if cnt >= M:
            is_explode = True
            continue
        else:
            for _ in range(cnt):
                ret.append(num)

    return ret, is_explode

while True:
    ret, is_explode = explode(numbers)
    if not is_explode:
        break
    numbers = ret
print(len(ret))
for i in ret:
    print(i)
