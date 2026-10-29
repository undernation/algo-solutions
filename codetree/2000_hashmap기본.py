"""
CT 2000  hashmap 기본
https://www.codetree.ai/ko/trails/complete/curated-cards/intro-hashmap-basic/description

풀이일 : 2026-10-29   결과: 품
한도   : time Python3 1초 · C++17 1초 / memory 80 MB / time_sec 1
난이도 : Easy  |  정답률 91.6%
제약   : - $1 \le N \le 100\,000$
제약   : - $1 \le \texttt{주어지는 수} \le 10^9$

[채점] accepted  1/1  (0.232s)

[문제]
$N$개의 명령이 주어졌을 때, 각 명령을 수행하는 프로그램을 작성해보세요. 명령의 종류는 크게 $3$가지 입니다.

- `add k v` : $(k, v)$ 쌍을 hashmap에 추가합니다. key가 $k$, value가 $v$라는 뜻입니다. 이때 만약 동일한 $k$가 이미 존재한다면, $v$로 덮어씁니다.
- `remove k` : key가 $k$인 쌍을 찾아 hashmap에서 제거합니다. 잘못된 입력은 주어지지 않습니다.
- `find k` : key가 $k$인 쌍이 hashmap에 있는지를 판단합니다. 있다면 해당하는 value를 출력하고, 없다면 `None`을 출력합니다.

[예제 1]
입력:
11
add 3 5
add 10000 1
find 3
find 5
find 10000
add 3 10
find 3
add 7 15
remove 3
remove 7
find 7

출력:
5
None
1
10
None

"""

N = int(input())
commands = []
for _ in range(N):
    line = input().split()
    cmd = line[0]
    k = int(line[1])
    if cmd == "add":
        v = int(line[2])
        commands.append((cmd, k, v))
    else:
        commands.append((cmd, k))

# Please write your code here.
new_dict = dict()
for n in range(N):
    cur_command = commands[n]

    if cur_command[0] == "add":
        k = cur_command[1]
        v = cur_command[2]
        new_dict[k] = v

    elif cur_command[0] == "remove":
        k = cur_command[1]
        del new_dict[k]
    elif cur_command[0] == "find":
        k = cur_command[1]
        if k in new_dict:
            print(new_dict[k])
        else:
            print("None")
