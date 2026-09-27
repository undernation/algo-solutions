"""
CT 93  대폭발
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-big-explosion/description

풀이일 : 2026-09-27   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Hard  |  정답률 67.7%
제약   : -  $1 \le N \le 100$
제약   : - $1 \le M \le 8$
제약   : - $1 \le r, c \le N$

[문제]
$N \times N$ 크기의 격자판 위의 한 지점에 폭탄이 놓여 있습니다. 아래 그림은 시작 시점($0$초)의 모습입니다.

![](https://contents.codetree.ai/problems/93/images/problems-e6d9fc84-b9c1-48c4-8c73-683d0026bd36.png)

폭탄은 시간이 흐름에 따라 $4$방향으로 폭발합니다. $1$초에 한 번씩 폭발하며, $t$초가 되면 $t-1$초에 폭탄이 있던 위치에서 상하좌우 $4$방향으로 거리 $2^{t - 1}$ 만큼 떨어진 지점에 새로운 폭탄이 생기게 됩니다. 이때 기존 위치에 있던 폭탄은 그대로 남아있으며 여전히 계속 터짐을 반복하게 됩니다.



예를 들어 위의 경우에서 시작하여 $1$초가 되면 다음과 같이 거리를 $1$만큼 두고 $4$방향으로 폭탄이 새롭게 생겨나게 됩니다.


![](https://contents.codetree.ai/problems/93/images/problems-33cfea41-2137-45aa-b941-1b46a307e673.png)

다시 $1$초가 지나 $2$초가 되면 다음과 같이 거리를 $2$만큼 두고 폭탄이 새롭게 생겨나게 됩니다. 이때 $1$초 전에 새로 생겨난 폭탄들도 $0$초부터 있었던 원시폭탄과 마찬가지로 거리를 $2$만큼 두고 새로운 폭탄을 생성하게 됩니다. 격자를 벗어나는 곳에는 폭탄이 새로 생기지 않게 되고, 이미 폭탄이 있는 경우 역시 새롭게 폭탄이 생겨나지 않습니다.

![](https://contents.codetree.ai/problems/93/images/problems-fc438281-cdb1-4bf3-b28d-e7ed13c6132d.png)

격자판의 크기와 처음 폭탄의 위치가 주어졌을 때, $M$초가 되었을 때 격자판에 놓여있는 폭탄의 개수를 구하는 프로그램을 작성해보세요.

[예제 1]
입력:
5 1 3 4

출력:
5


[예제 2]
입력:
5 2 3 4

출력:
15

"""

N, M, R, C = map(int, input().split())

# Please write your code here.
R -= 1
C -= 1

bombs = set()
bombs.add((R, C))



for time in range(1, M + 1):
    new_bombs = set()
    for cy, cx in bombs:
        new_bombs.add((cy, cx))
        for dy, dx in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            ny = cy + dy * pow(2, time - 1)
            nx = cx + dx * pow(2, time - 1)

            if not (0 <= ny < N and 0 <= nx < N):
                continue

            new_bombs.add((ny, nx))
    bombs = new_bombs
print(len(bombs))
