"""
CT 2496  정수 사각형 차이의 최소 2
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-minimum-difference-on-the-integer-grid-2/description

풀이일 : 2026-10-10   결과: 틀림
한도   : time Python3 9초 · C++17 2.5초 / memory 128 MB / time_sec 9
난이도 : Hard  |  정답률 33.7%
제약   : - $1 \le N \le 100$
제약   : - $1 \le \texttt{주어지는 정수} \le 100$

[문제]
$N \times N$ 크기의 격자 정보가 주어졌을 때, $(1,\ 1)$에서 시작하여 오른쪽 혹은 밑으로만 이동하여 $(N,\ N)$으로 간다고 했을 때 거쳐간 위치에 적혀있는 수들 중 최댓값과 최솟값의 차이를 가장 작게 만드는 프로그램을 작성해보세요. 

예로 다음 그림을 살펴봅시다.

![](https://contents.codetree.ai/problems/2496/images/problems-47e2e2c6-c718-436b-a986-868e17c0c8ca.png)

만약 다음 경로로 이동하게 된다면, 경로 상에 있는 수들 중 최솟값은 $1$, 최댓값은 $6$이므로 최대-최소 값이 $5$가 됩니다.

![](https://contents.codetree.ai/problems/2496/images/problems-93c94005-baa0-4b30-b574-28d8dcde9210.png)

하지만 아래와 같은 경로로 이동하게 된다면, 경로 상에 있는 수들 중 최솟값은 $1$, 최댓값은 $4$가 되므로 최대-최소 값이 $3$이 되어 차이가 최소가 됩니다.

![](https://contents.codetree.ai/problems/2496/images/problems-5c1c9ada-9522-49e9-ae13-c3aefe67dbcb.png)

[예제 1]
입력:
3
1 2 3
5 4 6
7 1 2

출력:
3


[예제 2]
입력:
4
20 30 51 30
22 10 12 1
10 25 35 21
34 36 20 20

출력:
21

"""

정수 사각형 차이의 최소 2
