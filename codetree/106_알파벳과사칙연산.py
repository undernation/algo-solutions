"""
CT 106  알파벳과 사칙연산
https://www.codetree.ai/ko/trails/complete/curated-cards/test-calculations-with-alphabet/description

풀이일 : 2026-10-04   결과: 품
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 44.6%
제약   : - $1 \le N \le 200$
제약   : - 계산 도중 값이 항상 $-2^{31}$이상 $2^{31} - 1$이하를 벗어나지 않음을 가정해도 좋습니다.
제약   : - 식은 `a`에서 `f`까지의 소문자 알파벳과 $+$, $-$, $*$ 기호만으로 이루어져 있습니다. 알파벳이나 연산자가 연속하여 $2$번 이상 나타나는 경우 없이 항상 번갈아가며 주어지며, 식의 시작과 마지막에는 반드시 알파벳이 입력된다고 가정해도 좋습니다.

[채점] accepted  3/3  (1.083s)

[문제]
`a`에서 `f`까지의 소문자 알파벳과 $+$, $-$, $*$ 기호만으로 이루어져 있는 길이가 $N$인 식이 하나 주어집니다. 

이때, 각 소문자 알파벳에 $1$ 이상 $4$ 이하의 정수 중 적절한 수를 집어넣어 식의 결과를 최대로 하는 프로그램을 작성해보세요. 

단, 일반 사칙연산처럼 $*$가 우선순위가 더 높은 것이 아닌, 모든 연산의 우선순위가 전부 같다고 가정하고 계산해야 합니다. 예를 들어 $3 - 2 * 3$ 은 $-3$이 아닌 $3$으로 계산합니다.

[예제 1]
입력:
c-a*b

출력:
12


[예제 2]
입력:
b-a*b-c+b

출력:
15


[예제 3]
입력:
a+e

출력:
8

"""

expression = input()

# Please write your code here.

def calc(num1, method, num2):
    if method == "+":
        return num1 + num2
    elif method == "-":
        return num1 - num2
    else:
        return num1 * num2

def decoder(ch):
    return ord(ch) - ord("a")

def calc_total(exp, num_list):
    if len(exp) == 1:
        return num_list[decoder(exp)]

    first_val = calc(num_list[decoder(exp[0])], exp[1], num_list[decoder(exp[2])])
    for idx in range(2, len(exp) - 1, 2):
        first_val = calc(first_val, exp[idx + 1], num_list[decoder(exp[idx + 2])])
    return first_val


answer = -10 ** 18

num_list = []

def dfs(idx):
    global answer
    if idx == 6:
        answer = max(answer, calc_total(expression, num_list))
        # print("wow")
        return

    for num in range(1, 5):
        num_list.append(num)
        dfs(idx + 1)
        num_list.pop()
dfs(0)
print(answer)
