"""
CT 29  가능한 수열 중 최솟값 구하기
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-find-min-of-possible-series/description

풀이일 : 2026-10-05   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 192 MB / time_sec 1
난이도 : Hard  |  정답률 50.7%
제약   : - $1 \le N \le 80$

[채점] accepted  3/3  (0.796s)

[문제]
길이가 $N$인 수열을 세 개의 숫자 $4$, $5$, $6$ 으로만 구성하려고 합니다. 이 때 임의의 길이를 갖는 두 개의 인접한 연속 부분 수열이 동일한 경우, 이는 불가능한 수열로 간주합니다. <그림 $1$>은 불가능한 수열의 예시들 입니다. 아래의 그림과 같이 빨간색으로 밑줄이 쳐진 부분 수열과 파란색으로 밑줄 쳐진 인접한 연속 부분 수열이 동일한 경우, 이는 불가능한 수열입니다. 이 때 길이가 $N$인 가능한 수열 중 앞에서부터 읽었을 때 사전순으로 가장 앞선 수열을 출력하는 코드를 작성해보세요.

![](https://contents.codetree.ai/problems/29/images/problems-35b10d4d-db2e-43b7-8501-6c17703f64e5.png)

[예제 1]
입력:
2

출력:
45


[예제 2]
입력:
3

출력:
454


[예제 3]
입력:
7

출력:
4546454

"""

N = int(input())

# Please write your code here.

def check(num_list):
    cur_N = len(num_list)

    for size in range(1, cur_N // 2 + 1):
        # 뒤엣거 size 만큼
        list1 = num_list[-size:]
        list2 = num_list[-size * 2:-size]

        if list1 == list2:
            return False

    return True
num_list = []

def dfs(idx):
    if idx == N:
        for num in num_list:
            print(num, end="")
        return True


    for num in range(4, 7):

        num_list.append(num)
        if check(num_list):
            if dfs(idx + 1):
                return True
        num_list.pop()

dfs(0)
