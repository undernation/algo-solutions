"""
CT 103  아름다운 수
https://www.codetree.ai/ko/trails/complete/curated-cards/challenge-beautiful-number/description

풀이일 : 2026-09-30   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Easy  |  정답률 67.7%
제약   : - $1 \le N \le 10$

[채점] accepted  2/2  (0.51s)

[문제]
$1$이상 $4$이하의 정수로만 이루어져 있으면서, 정확히 해당 숫자만큼 연달아 같은 숫자가 나오는 수를 아름다운 수라고 부릅니다.

예를 들어 $1333221$는 $1$이 $1$번, $3$이 $3$번, $2$가 $2$번 그리고 $1$이 $1$번 연속하여 나오므로 아름다운 수입니다.

이때 동일한 숫자에 대해 연달아 같은 숫자의 묶음이 나오는 것 또한 아름다운 수입니다.

예를 들어 $111$, $22222222$와 같은 수 역시 $1$이 $1$번 나온 것이 $3$번 반복되었고, $2$가 $2$번 나온 것이 $4$번 반복되었다고 할 수 있기 때문에 아름다운 수라고 할 수 있습니다.
다만, $222$의 경우에는 $2$가 $2$번 나온 뒤, 다시 $2$가 $1$번 나왔으므로 아름다운 수가 아닙니다.

$N$자리 아름다운 수가 몇 개 있는지를 구하는 프로그램을 작성해보세요.

[예제 1]
입력:
1

출력:
1


[예제 2]
입력:
3

출력:
4

"""

N = int(input())

# Please write your code here.

answer = []


def check(num_list):
    cur_N = len(num_list)
    cur_num = num_list[0]
    cnt = 1
    ret = []
    for idx in range(1, cur_N):
        if cur_num != num_list[idx]:
            ret.append((cur_num, cnt))
            cur_num = num_list[idx]
            cnt = 1
        else:
            cnt += 1
    ret.append((cur_num, cnt))

    for a, b in ret:
        if b % a != 0:
            return False
    return True

cnt = 0

def dfs(idx):
    global cnt
    if idx == N:
        if check(answer):
            cnt += 1
        return

    for num in range(1, 5):
        answer.append(num)
        dfs(idx + 1)
        answer.pop()

dfs(0)
print(cnt)
