"""
CT 106  알파벳과 사칙연산
https://www.codetree.ai/ko/trails/complete/curated-cards/test-calculations-with-alphabet/description

풀이일 : 2026-10-01   결과: 틀림
한도   : time Python3 1초 · C++17 0.5초 / memory 128 MB / time_sec 1
난이도 : Medium  |  정답률 44.6%
제약   : - $1 \le N \le 200$
제약   : - 계산 도중 값이 항상 $-2^{31}$이상 $2^{31} - 1$이하를 벗어나지 않음을 가정해도 좋습니다.
제약   : - 식은 `a`에서 `f`까지의 소문자 알파벳과 $+$, $-$, $*$ 기호만으로 이루어져 있습니다. 알파벳이나 연산자가 연속하여 $2$번 이상 나타나는 경우 없이 항상 번갈아가며 주어지며, 식의 시작과 마지막에는 반드시 알파벳이 입력된다고 가정해도 좋습니다.

[채점] accepted  3/3  (1.081s)

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
        return int(num1) + int(num2)
    elif method == "-":
        return int(num1) - int(num2)
    elif method == "*":
        return int(num1) * int(num2)


def decode(alpha):
    return ord(alpha) - ord("a")


def calc_total(exp):
    global numbers
    if len(exp) == 1:
        return numbers[decode(exp[0])]
    first_ret = calc(numbers[decode(exp[0])], exp[1], numbers[decode(exp[2])])

    for idx in range(2, len(exp) - 2, 2):
        ret = calc(first_ret, exp[idx + 1], numbers[decode(exp[idx + 2])])
        first_ret = ret

    return first_ret


answer = -10 ** 18
numbers = []



def dfs(idx):
    global answer, numbers
    if idx == 6:
        # 알파벳 계산 연산
        answer = max(answer, calc_total(expression))
        return

    for i in range(1, 5):
        numbers.append(i)

        dfs(idx + 1)

        numbers.pop()


dfs(0)

print(answer)
