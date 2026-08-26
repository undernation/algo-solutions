"""
SWEA 27183  고속선 선로 피로도 관제 시스템 D6
https://swexpertacademy.com/main/code/userProblem/userProblemDetail.do?fromProbList=N&deleteYn=N&contestProbId=AZ-JQXMKpUnHBITH&topPath=code&lastPath=problemDetail&secondPath=problem&menuBreakDown=swea.code.menu&menuBreakDown=swea.code.problem.menu&menuDesc=swea.code.desc&menuDesc=swea.code.problem.desc&contextPath=%2Fmain&locale=ko-kr%2Cko%3Bq%3D0.9%2Cen-us%3Bq%3D0.8%2Cen%3Bq%3D0.7&serverName=localhost&localeLanguage=ko_KR&localeLanguage2=Ko_KR&remoteAddr=175.213.163.17&scripts=%2Fjs%2Finit%2Fjquery-debug.js&scripts=%2Fjs%2Finit%2Fjquery-ui.js&scripts=%2Fjs%2Finit%2Fjquery.validate.js&scripts=%2Fjs%2Fcommon.js&NOTICE_NEW_COUNT=0&ssoLogin=false&hasSDPAdminLinkAuth=false&systemAdmin=false&backendAdmin=false&isTechBlogManager=false&CURRENT_MENU_AUTHORIZATION=READ&CURRENT_MENU_AUTHORIZATION=UPDATE&CURRENT_MENU_AUTHORIZATION=EXECUTE&CURRENT_MENU_AUTHORIZATION=DOWNLOAD&logoMainfileName=logo_company.png

풀이일 : 2026-08-26   결과: 못품
한도   : time 12개 테스트케이스를 합쳐서 C/C++의 경우 1초 / Java의 경우 6초 / memory 힙, 정적 메모리 합쳐서 256MB 이내, 스택 메모리 1MB 이내 / time_sec 1
난이도 : ?  |  정답률 25.00%

[문제]
한 고속철도 관제 센터는 일렬로 이어진 N개의 선로 구간(section)의 금속 피로도를 실시간으로 관리한다. 각 구간에는 현재 피로도가 하나의 값으로 기록되어 있다.

열차가 어떤 구간 범위를 통과하면 그 범위의 모든 구간에 피로도가 일정량씩 누적되고, 정비반이 투입되면 정비한 범위의 피로도가 지정된 값으로 재설정된다. 관제사는 수시로 특정 범위의 최대 피로도를 점검하고, 피로도가 경보 임계값 이상인 가장 앞쪽(왼쪽) 구간을 찾아 경보를 발령해야 한다.

당신은 이 관제 시스템에 들어오는 4종류의 명령을 순서대로 처리하는 프로그램을 작성해야 한다.

[구간 번호와 범위]

선로 구간은 왼쪽부터 0번, 1번, …, (N−1)번으로 번호를 매긴다. 한 구간은 하나의 정수 인덱스로 표현한다. (0 ≤ 인덱스 < N)

초기 피로도는 N개의 정수로 한 줄에 주어지며, j번째 값이 j번 구간의 초기 피로도이다. (0 ≤ j < N)

두 정수 l, r (l ≤ r)로 주어지는 범위 [l, r]은 l ≤ 인덱스 ≤ r을 만족하는 모든 구간의 집합이다. l = r이면 단일 구간을, l = 0, r = N−1이면 전체 구간을 가리킨다.

[경보 탐지 기준]

명령 4(경보 탐지)는 범위 [l, r]에서 피로도가 임계값 x 이상인 구간 중 번호가 가장 작은(가장 왼쪽) 구간을 찾는다. 비교는 이상(≥)이므로 피로도가 x와 정확히 같은 구간도 대상이 된다. 범위 안에 피로도가 x 이상인 구간이 하나도 없으면 −1을 출력한다.

[처리해야 할 명령]

각 테스트 케이스는 초기 피로도 배열과 M개의 명령으로 구성된다. 명령은 다음 4종류이다.

명령형식동작출력
1 (열차 통과)1 l r w구간 [l, r]의 모든 구간 피로도를 w만큼 증가없음
2 (정비)2 l r v구간 [l, r]의 모든 구간 피로도를 v로 재설정 (v = 0 가능)없음
3 (점검)3 l r구간 [l, r]의 최대 피로도를 조회최대 피로도를 한 줄에 출력
4 (경보 탐지)4 l r x구간 [l, r]에서 피로도가 x 이상인 가장 왼쪽 구간을 탐색해당 구간 번호를 한 줄에 출력, 없으면 −1

[예시] N=10, 초기 피로도가 [3, 7, 2, 8, 1, 6, 4, 9, 2, 5]인 경우를 보자. 각 칸 아래의 숫자는 구간 번호(인덱스 0~9)이다.

[[IMG:1]]

① 명령 1 2 6 4 — 구간 [2, 6]의 모든 구간 피로도를 4씩 증가시킨다. 2→6, 8→12, 1→5, 6→10, 4→8이 되어 배열은 [3, 7, 6, 12, 5, 10, 8, 9, 2, 5]가 된다. 출력은 없다.

[[IMG:2]]

② 명령 3 1 5 — 구간 [1, 5]의 최대 피로도를 조회한다. 값 7, 6, 12, 5, 10 중 최댓값 12를 한 줄에 출력한다.

③ 명령 2 3 5 2 — 구간 [3, 5]의 모든 구간 피로도를 2로 재설정한다. 배열은 [3, 7, 6, 2, 2, 2, 8, 9, 2, 5]가 된다. 출력은 없다.

[[IMG:3]]

④ 명령 4 0 9 8 — 전체 구간 [0, 9]에서 피로도가 8 이상인 가장 왼쪽 구간을 찾는다. 앞에서부터 값 3, 7, 6, 2, 2, 2는 모두 8 미만이고, 처음으로 8 이상이 되는 곳은 값이 8인 6번 구간이다(‘이상’ 비교이므로 x와 같은 값도 해당). 따라서 6을 출력한다.

⑤ 명령 4 0 5 8 — 구간 [0, 5]에서 피로도가 8 이상인 구간을 찾는다. 이 범위의 최대 피로도는 7로 8 미만이므로 조건을 만족하는 구간이 없다. 따라서 −1을 출력한다.

[[IMG:4]]

[제공되는 뼈대 코드 — 커맨드 패턴]

아래에 언어별 뼈대 코드가 제공된다. main 함수는 입력 파싱과 명령 분기(커맨드 패턴), 출력을 모두 처리하며, 당신은 5개 함수 — init, add_stress, repair, get_peak, find_risk — 만 구현하면 된다. 필요한 전역 변수, 보조 함수, 클래스는 자유롭게 추가해도 된다. (Java 뼈대는 관례상 camelCase — addStress / getPeak / findRisk — 를 사용한다)

뼈대 전체를 복사해 함수 구현을 채워 제출하라. 함수의 원형(시그니처)은 변경하지 말고, main과 입출력 부분은 수정하지 않는 것을 권장한다. main을 수정하더라도 입출력 형식만 일치하면 정답으로 처리되지만, 최종 출력 형식은 반드시 유지해야 한다.

[C]

#include <stdio.h>

#define MAX_N 500000

/*=========================================================
  여기서부터 5개 함수만 구현하시오.
  main 및 입출력 부분은 수정하지 않는 것을 권장한다.

  init      : 각 테스트 케이스 시작 시 1회 호출. 전역 자료 구조 초기화.
  add_stress: 구간 [l,r] 의 모든 구간 피로도를 w 만큼 증가(range add).
  repair    : 구간 [l,r] 을 v 로 재설정(range assign, v=0 가능).
  get_peak  : 구간 [l,r] 의 최대 피로도 반환(range max).
  find_risk : 구간 [l,r] 에서 값 >= x 인 가장 왼쪽 인덱스 반환, 없으면 -1.
=========================================================*/

void init(int N, int fatigue[])
{
    /* TODO: fatigue[0..N-1] = 초기 피로도. 전역 자료 구조를 반드시 초기화할 것. */
}

void add_stress(int l, int r, int w)
{
    /* TODO: 구간 [l,r] 에 피로도 w 누적 */
}

void repair(int l, int r, int v)
{
    /* TODO: 구간 [l,r] 을 v 로 재설정 */
}

int get_peak(int l, int r)
{
    /* TODO: 구간 [l,r] 의 최대 피로도 반환 */
    return -1;
}

int find_risk(int l, int r, int x)
{
    /* TODO: 구간 [l,r] 에서 값 >= x 인 최소 인덱스 반환, 없으면 -1 */
    return -1;
}

/*========= 이하 수정 비권장 (출력 형식 유지) =========*/
static int in_fatigue[MAX_N];
static char in_buf[32 << 20];
static char *in_p;

static int read_int(void)
{
    int v = 0;
    while (*in_p < '0' || *in_p > '9') in_p++;
    while (*in_p >= '0' && *in_p <= '9')
        v = v * 10 + (*in_p++ - '0');
    return v;
}

int main(void)
{
    int T, tc;
    size_t rd = fread(in_buf, 1, sizeof(in_buf) - 1, stdin);
    (void)rd;
    in_p = in_buf;
    T = read_int();
    for (tc = 1; tc <= T; tc++) {
        int N, M, i;
        N = read_int(); M = read_int();
        for (i = 0; i < N; i++)
            in_fatigue[i] = read_int();
        init(N, in_fatigue);
        printf("#%d\n", tc);
        while (M--) {
            int op = read_int();
            if (op == 1) {
                int l = read_int(), r = read_int(), w = read_int();
                add_stress(l, r, w);
            } else if (op == 2) {
                int l = read_int(), r = read_int(), v = read_int();
                repair(l, r, v);
            } else if (op == 3) {
                int l = read_int(), r = read_int();
                printf("%d\n", get_peak(l, r));
            } else {
                int l = read_int(), r = read_int(), x = read_int();
                printf("%d\n", find_risk(l, r, x));
            }
        }
    }
    return 0;
}

[C++]

#include <cstdio>
/* 필요한 STL 헤더는 자유롭게 추가해도 된다.
   단, 아래 전역 함수(repair 등)와 std 심볼의 이름 충돌을 피하기 위해
   using namespace std; 는 쓰지 말고 std:: 접두사를 사용할 것. */

#define MAX_N 500000

/*=========================================================
  여기서부터 5개 함수만 구현하시오.
  main 및 입출력 부분은 수정하지 않는 것을 권장한다.

  init      : 각 테스트 케이스 시작 시 1회 호출. 전역 자료 구조 초기화.
  add_stress: 구간 [l,r] 의 모든 구간 피로도를 w 만큼 증가(range add).
  repair    : 구간 [l,r] 을 v 로 재설정(range assign, v=0 가능).
  get_peak  : 구간 [l,r] 의 최대 피로도 반환(range max).
  find_risk : 구간 [l,r] 에서 값 >= x 인 가장 왼쪽 인덱스 반환, 없으면 -1.
=========================================================*/

void init(int N, int fatigue[])
{
    // TODO: fatigue[0..N-1] = 초기 피로도. 전역 자료 구조를 반드시 초기화할 것.
}

void add_stress(int l, int r, int w)
{
    // TODO: 구간 [l,r] 에 피로도 w 누적
}

void repair(int l, int r, int v)
{
    // TODO: 구간 [l,r] 을 v 로 재설정
}

int get_peak(int l, int r)
{
    // TODO: 구간 [l,r] 의 최대 피로도 반환
    return -1;
}

int find_risk(int l, int r, int x)
{
    // TODO: 구간 [l,r] 에서 값 >= x 인 최소 인덱스 반환, 없으면 -1
    return -1;
}

/*========= 이하 수정 비권장 (출력 형식 유지) =========*/
static int in_fatigue[MAX_N];
static char in_buf[32 << 20];
static char *in_p;

static int read_int()
{
    int v = 0;
    while (*in_p < '0' || *in_p > '9') in_p++;
    while (*in_p >= '0' && *in_p <= '9')
        v = v * 10 + (*in_p++ - '0');
    return v;
}

int main()
{
    int T, tc;
    size_t rd = fread(in_buf, 1, sizeof(in_buf) - 1, stdin);
    (void)rd;
    in_p = in_buf;
    T = read_int();
    for (tc = 1; tc <= T; tc++) {
        int N, M, i;
        N = read_int(); M = read_int();
        for (i = 0; i < N; i++)
            in_fatigue[i] = read_int();
        init(N, in_fatigue);
        printf("#%d\n", tc);
        while (M--) {
            int op = read_int();
            if (op == 1) {
                int l = read_int(), r = read_int(), w = read_int();
                add_stress(l, r, w);
            } else if (op == 2) {
                int l = read_int(), r = read_int(), v = read_int();
                repair(l, r, v);
            } else if (op == 3) {
                int l = read_int(), r = read_int();
                printf("%d\n", get_peak(l, r));
            } else {
                int l = read_int(), r = read_int(), x = read_int();
                printf("%d\n", find_risk(l, r, x));
            }
        }
    }
    return 0;
}

[Java]

import java.io.*;

public class Solution {

    /*=========================================================
      여기서부터 5개 메서드만 구현하시오.
      main 및 입출력 부분은 수정하지 않는 것을 권장한다.

      init      : 각 테스트 케이스 시작 시 1회 호출. 전역 자료 구조 초기화.
      addStress : 구간 [l,r] 의 모든 구간 피로도를 w 만큼 증가(range add).
      repair    : 구간 [l,r] 을 v 로 재설정(range assign, v=0 가능).
      getPeak   : 구간 [l,r] 의 최대 피로도 반환(range max).
      findRisk  : 구간 [l,r] 에서 값 >= x 인 가장 왼쪽 인덱스 반환, 없으면 -1.
    =========================================================*/

    static void init(int N, int[] fatigue) {
        // TODO: fatigue[0..N-1] = 초기 피로도. 전역 자료 구조를 반드시 초기화할 것.
    }

    static void addStress(int l, int r, int w) {
        // TODO: 구간 [l,r] 에 피로도 w 누적
    }

    static void repair(int l, int r, int v) {
        // TODO: 구간 [l,r] 을 v 로 재설정
    }

    static int getPeak(int l, int r) {
        // TODO: 구간 [l,r] 의 최대 피로도 반환
        return -1;
    }

    static int findRisk(int l, int r, int x) {
        // TODO: 구간 [l,r] 에서 값 >= x 인 최소 인덱스 반환, 없으면 -1
        return -1;
    }

    /*========= 이하 수정 비권장 (출력 형식 유지) =========*/
    public static void main(String[] args) throws IOException {
        StreamTokenizer in = new StreamTokenizer(
                new BufferedReader(new InputStreamReader(System.in)));
        StringBuilder sb = new StringBuilder();
        in.nextToken();
        int T = (int) in.nval;
        for (int tc = 1; tc <= T; tc++) {
            in.nextToken(); int N = (int) in.nval;
            in.nextToken(); int M = (int) in.nval;
            int[] fatigue = new int[N];
            for (int i = 0; i < N; i++) {
                in.nextToken();
                fatigue[i] = (int) in.nval;
            }
            init(N, fatigue);
            sb.append('#').append(tc).append('\n');
            for (int q = 0; q < M; q++) {
                in.nextToken(); int op = (int) in.nval;
                if (op == 1) {
                    in.nextToken(); int l = (int) in.nval;
                    in.nextToken(); int r = (int) in.nval;
                    in.nextToken(); int w = (int) in.nval;
                    addStress(l, r, w);
                } else if (op == 2) {
                    in.nextToken(); int l = (int) in.nval;
                    in.nextToken(); int r = (int) in.nval;
                    in.nextToken(); int v = (int) in.nval;
                    repair(l, r, v);
                } else if (op == 3) {
                    in.nextToken(); int l = (int) in.nval;
                    in.nextToken(); int r = (int) in.nval;
                    sb.append(getPeak(l, r)).append('\n');
                } else {
                    in.nextToken(); int l = (int) in.nval;
                    in.nextToken(); int r = (int) in.nval;
                    in.nextToken(); int x = (int) in.nval;
                    sb.append(findRisk(l, r, x)).append('\n');
                }
            }
        }
        System.out.print(sb);
    }
}

[Python]

import sys

# =========================================================
#  여기서부터 5개 함수만 구현하시오.
#  (파이썬 내장과의 충돌을 피하기 위해 함수명은 아래 이름을 그대로 사용한다)
#  main 및 입출력 부분은 수정하지 않는 것을 권장한다.
#
#  init       : 각 테스트 케이스 시작 시 1회 호출. 전역 자료 구조 초기화.
#  add_stress : 구간 [l,r] 의 모든 구간 피로도를 w 만큼 증가(range add).
#  repair     : 구간 [l,r] 을 v 로 재설정(range assign, v=0 가능).
#  get_peak   : 구간 [l,r] 의 최대 피로도 반환(range max).
#  find_risk  : 구간 [l,r] 에서 값 >= x 인 가장 왼쪽 인덱스 반환, 없으면 -1.
# =========================================================

def init(N, fatigue):
    # TODO: fatigue 는 길이 N 리스트(구간 i 의 초기 피로도).
    #       전역 자료 구조를 반드시 초기화할 것.
    pass

def add_stress(l, r, w):
    # TODO: 구간 [l,r] 에 피로도 w 누적
    pass

def repair(l, r, v):
    # TODO: 구간 [l,r] 을 v 로 재설정
    pass

def get_peak(l, r):
    # TODO: 구간 [l,r] 의 최대 피로도 반환
    return -1

def find_risk(l, r, x):
    # TODO: 구간 [l,r] 에서 값 >= x 인 최소 인덱스 반환, 없으면 -1
    return -1

# ========= 이하 수정 비권장 (출력 형식 유지) =========
def main():
    sys.setrecursionlimit(1 << 20)
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    out = []
    T = int(next(it))
    for tc in range(1, T + 1):
        N = int(next(it)); M = int(next(it))
        fatigue = [int(next(it)) for _ in range(N)]
        init(N, fatigue)
        out.append('#%d' % tc)
        for _ in range(M):
            op = int(next(it))
            if op == 1:
                l = int(next(it)); r = int(next(it)); w = int(next(it))
                add_stress(l, r, w)
            elif op == 2:
                l = int(next(it)); r = int(next(it)); v = int(next(it))
                repair(l, r, v)
            elif op == 3:
                l = int(next(it)); r = int(next(it))
                out.append(str(get_peak(l, r)))
            else:
                l = int(next(it)); r = int(next(it)); x = int(next(it))
                out.append(str(find_risk(l, r, x)))
    sys.stdout.write('\n'.join(out) + '\n')

main()

[제약 사항]

항목범위 / 조건
테스트 케이스 수 T1 ≤ T ≤ 12, 이 중 N > 100,000인 테스트 케이스는 최대 4개
선로 구간 수 N5 ≤ N ≤ 500,000 (1차원, 구간 번호 0..N−1)
초기 피로도0 ≤ 값 ≤ 9,999
정비의 값 v0 ≤ v ≤ 100,000
열차 통과의 증가량 w1 ≤ w ≤ 1,000
경보 임계값 x1 ≤ x ≤ 20,000,000 (범위 최대 피로도를 넘는 값이 주어져 −1이 되는 경우도 있다)
값의 범위모든 시점에서 모든 구간의 피로도는 항상 20,000,000 이하이다 (int 범위 내 보장 — long 불필요)
범위 유효성모든 명령에서 0 ≤ l ≤ r ≤ N−1 (l = r 단일 구간, [0, N−1] 전체 범위 모두 등장)
명령 수 (테스트 케이스당)M ≤ 25,000 — 명령 1 ≤ 12,000 / 명령 2 ≤ 5,000 / 명령 3 ≤ 5,000 / 명령 4 ≤ 5,000
명령 수 (입력 파일 전체 합)명령 1 ≤ 45,000 / 명령 2 ≤ 18,000 / 명령 3 ≤ 14,000 / 명령 4 ≤ 13,000 (총 ≤ 90,000)

[유의 사항]

· 제한 시간은 입력 파일 전체(모든 테스트 케이스)를 처리하는 기준이다.
· 시간 복잡도에 주의. 매 명령마다 범위 내 모든 구간(최대 500,000개)을 하나씩 갱신하거나 선형으로 순회하는 단순한 방법으로는 통과할 수 없도록 채점 데이터가 구성되어 있다. 특히 명령 1(범위 증가)과 명령 4(가장 왼쪽 구간 탐색)를 범위 전체에 대해 반복 순회하면 대형 테스트 케이스에서 시간을 초과한다. 범위 단위의 자료 구조 설계가 필요하다.
· 각 테스트 케이스는 독립적이다. 이전 테스트 케이스의 상태가 남지 않도록 init에서 모든 전역 자료 구조를 초기화하라.
· 표준 라이브러리(STL, java.util 등)는 사용할 수 있다.
· C/C++ 뼈대는 입력 전체를 한 번에 읽으므로, 로컬에서 테스트할 때는 키보드 입력 대신 파일 리다이렉션(예: prog.exe < input.txt)을 사용하라.
· 주어진 예시를 통과하더라도 채점에는 공개되지 않은 테스트 케이스가 포함되므로, 제약 최대 규모에서 시간 내에 동작하는지 반드시 확인하라.

[예제 1]
입력:
2
10 5
3 7 2 8 1 6 4 9 2 5
1 2 6 4
3 1 5
2 3 5 2
4 0 9 8
4 0 5 8
10 40
4 4 4 0 0 7 7 7 2 9
3 0 9
4 0 9 9
4 0 9 100
4 3 3 1
4 5 5 7
1 3 3 5
3 3 3
4 0 9 5
2 5 7 0
4 0 9 1
2 0 9 3
1 0 9 2
3 0 9
4 0 9 5
2 2 6 8
1 2 6 3
3 0 9
4 0 9 11
1 0 4 4
4 0 9 15
4 0 1 15
4 7 9 5
2 4 4 15
3 4 4
1 5 8 1000
3 5 9
2 0 9 100000
1 0 9 1000
3 0 9
4 0 9 101000
4 0 9 20000000
2 3 6 50
4 0 9 50
4 4 8 50
3 3 6
1 0 9 500
2 0 9 7
3 0 9
4 0 9 7
4 0 9 8
출력:
#1
12
6
-1
#2
9
9
-1
-1
5
5
3
0
5
0
11
2
2
-1
7
15
1011
101000
0
-1
0
4
50
7
0
-1
"""

.
