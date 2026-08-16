"""
SWEA 27181  공항 활주로 관제 시스템 D6
https://swexpertacademy.com/main/code/userProblem/userProblemDetail.do?fromProbList=N&deleteYn=N&contestProbId=AZ-JQTG6pUPHBITH&topPath=code&lastPath=problemDetail&secondPath=problem&menuBreakDown=swea.code.menu&menuBreakDown=swea.code.problem.menu&menuDesc=swea.code.desc&menuDesc=swea.code.problem.desc&contextPath=%2Fmain&locale=ko-kr%2Cko%3Bq%3D0.9%2Cen-us%3Bq%3D0.8%2Cen%3Bq%3D0.7&serverName=localhost&localeLanguage=ko_KR&localeLanguage2=Ko_KR&remoteAddr=175.213.163.17&scripts=%2Fjs%2Finit%2Fjquery-debug.js&scripts=%2Fjs%2Finit%2Fjquery-ui.js&scripts=%2Fjs%2Finit%2Fjquery.validate.js&scripts=%2Fjs%2Fcommon.js&NOTICE_NEW_COUNT=0&ssoLogin=false&hasSDPAdminLinkAuth=false&systemAdmin=false&backendAdmin=false&isTechBlogManager=false&CURRENT_MENU_AUTHORIZATION=READ&CURRENT_MENU_AUTHORIZATION=UPDATE&CURRENT_MENU_AUTHORIZATION=EXECUTE&CURRENT_MENU_AUTHORIZATION=DOWNLOAD&logoMainfileName=logo_company.png

풀이일 : 2026-08-16   결과: 품
한도   : time 12개 테스트케이스를 합쳐서 C/C++의 경우 2초 / Java의 경우 6초 / memory 힙, 정적 메모리 합쳐서 256MB 이내, 스택 메모리 1MB 이내 / time_sec 2
난이도 : ?  |  정답률 50.00%

[채점] accepted  1/1  (0.298s)

[문제]
혼잡한 국제공항의 접근 관제소는 착륙을 기다리는 모든 항공편을 전산으로 관제한다. 항공편은 접근 공역에 진입할 때 긴급도를 부여받아 착륙 대기열에 오르고, 연료 잔량이나 기상 변화에 따라 긴급도가 재산정되며, 목적지를 변경해 스스로 착륙 요청을 철회하기도 한다.

활주로에 자리가 나면 관제소는 가장 긴급한 항공편에 착륙 허가를 내리고, 공역이 포화되면 가장 여유로운 항공편을 인근 공항으로 회항시킨다.

당신은 이 관제 시스템에 들어오는 5종류의 명령을 순서대로 처리하는 프로그램을 작성해야 한다.

[식별자와 긴급도]

각 항공편은 서로 다른 정수 식별자 fid로 구분되며, 대기열에 오를 때 정수 긴급도 u를 부여받는다. 같은 순간 대기 중인 항공편의 fid는 서로 다르지만, 착륙·회항·철회되어 대기열을 떠난 fid는 나중에 다시 요청될 수 있다.

[요청 순번]

동점(긴급도가 같은 상황)의 우선순위를 정하기 위해, 대기열에 오른 각 항공편에는 요청 순번이 부여된다. 요청 순번은 전역 카운터로 매겨진다.

  · 각 테스트 케이스의 초기 대기 명단 P편은 입력에 주어진 순서대로 요청 순번 1, 2, …, P를 받는다.
  · 이후 명령 1(요청)로 새로 대기열에 오르는 항공편은 P+1, P+2, …로 이어지는 새 요청 순번을 받는다.
  · 명령 2(재산정)로 긴급도만 바뀌는 경우 요청 순번은 그대로 유지된다.
  · 대기열을 떠났던 항공편이 명령 1로 다시 요청될 때는 그 시점의 새 요청 순번을 받는다.

[우선순위 기준]

명령 4(착륙 허가)와 명령 5(회항)는 대기 중인 항공편들을 다음 기준으로 비교해 각각 우선순위가 가장 높은 항공편 하나를 선택한다.

· 착륙 허가(명령 4) — 가장 긴급한 항공편을 고른다.
  1) 긴급도가 큰 순서 (내림차순)
  2) 긴급도가 같다면 요청 순번이 작은(먼저 요청한) 순서

· 회항(명령 5) — 가장 여유로운 항공편을 고른다.
  1) 긴급도가 작은 순서 (오름차순)
  2) 긴급도가 같다면 요청 순번이 큰(나중에 요청한) 순서

[처리해야 할 명령]

각 테스트 케이스는 초기 대기 명단과 M개의 명령으로 구성된다. 명령은 다음 5종류이다.

명령형식동작출력
1 (요청)1 fid u대기 중이 아닌 항공편 fid를 긴급도 u로 착륙 대기열에 등록한다. 새 요청 순번을 부여한다(재요청 가능).없음
2 (재산정)2 fid u대기 중인 항공편 fid의 긴급도를 u로 변경한다. 요청 순번은 유지된다(현재와 같은 u가 주어질 수 있다).없음
3 (철회)3 fid대기 중인 항공편 fid가 대기열에서 이탈한다.없음
4 (착륙 허가)4대기 중 우선순위가 가장 높은(가장 긴급한) 항공편을 대기열에서 제거한다.제거된 항공편의 fid를 한 줄에 출력. 대기열이 비어 있으면 -1
5 (회항)5대기 중 우선순위가 가장 높은(가장 여유로운) 항공편을 대기열에서 제거한다.제거된 항공편의 fid를 한 줄에 출력. 대기열이 비어 있으면 -1

[예시] 초기 대기 명단이 P=4편이고 명령이 M=8개인 경우를 보자. 초기 명단은 입력 순서대로 요청 순번 1~4를 받는다: (fid=101, 긴급도=5, 순번=1), (202, 3, 2), (303, 5, 3), (404, 2, 4).

[[IMG:1]]

① 명령 4 (착륙 허가) — 긴급도가 5로 가장 큰 항공편은 101(순번 1)과 303(순번 3) 두 편이다. 동점이므로 요청 순번이 작은 101을 착륙 허가하고 fid 101을 출력한다.

[[IMG:2]]

② 명령 1 505 7 (요청) — 항공편 505를 긴급도 7로 등록한다. 다음 요청 순번 5를 받는다.

③ 명령 2 202 9 (재산정) — 항공편 202의 긴급도를 3에서 9로 바꾼다. 요청 순번 2는 그대로 유지된다. 현재 유효한 대기열은 (202, 9, 2), (303, 5, 3), (404, 2, 4), (505, 7, 5)이다.

[[IMG:3]]

④ 명령 4 (착륙 허가) — 이제 긴급도가 9로 가장 큰 202가 착륙 허가되어 fid 202를 출력한다. 재산정된 값이 정확히 반영되어야 한다.

[[IMG:4]]

⑤ 명령 5 (회항) — 잔여 대기열 (303, 5, 3), (404, 2, 4), (505, 7, 5) 중 긴급도가 2로 가장 작은 404를 회항하고 fid 404를 출력한다.

⑥ 명령 3 303 (철회) — 항공편 303이 대기열에서 이탈한다.

⑦ 명령 4 (착륙 허가) — 잔여 대기열은 (505, 7, 5)뿐이므로 505가 착륙 허가되어 fid 505를 출력한다.

⑧ 명령 5 (회항) — 대기열이 비어 있으므로 -1을 출력한다.

따라서 이 테스트 케이스의 출력은 #1에 이어 101, 202, 404, 505, -1이 각각 한 줄씩이다.

[제공되는 뼈대 코드 — 커맨드 패턴]

아래에 언어별 뼈대 코드가 제공된다. main 함수는 입력 파싱과 명령 분기(커맨드 패턴), 출력을 모두 처리하며, 당신은 6개 함수 — init, request, renew, cancel, clear_landing, divert — 만 구현하면 된다. 필요한 전역 변수, 보조 함수, 클래스는 자유롭게 추가해도 된다. (Java는 관례상 명령 4 함수명으로 camelCase clearLanding을 사용하며, Python 뼈대는 내장 함수 id와의 혼동을 피해 식별자를 fid로 명명한다.)

뼈대 전체를 복사해 함수 구현을 채워 제출하라. 함수의 원형(시그니처)은 변경하지 말고, main과 입출력 부분은 수정하지 않는 것을 권장한다. main을 수정하더라도 입출력 형식만 일치하면 정답으로 처리되지만, 최종 출력 형식은 반드시 유지해야 한다.

[C]

#include <stdio.h>

/*=========================================================
  공항 활주로 관제 시스템
  여기서부터 6개 함수만 구현하시오.
  main 및 입출력 부분은 수정하지 않는 것을 권장한다.

  init      : 각 테스트 케이스 시작 시 1회 호출. 전역 자료 구조 초기화.
  request   : 명령 1 — 비대기 fid 를 긴급도 u 로 착륙 대기열 등록(새 요청 순번).
  renew     : 명령 2 — 대기 중 fid 의 긴급도를 u 로 변경(요청 순번 유지).
  cancel    : 명령 3 — 대기 중 fid 가 대기열에서 이탈.
  clear_landing : 명령 4 — 우선순위 1위(긴급도 큰 순 → 순번 작은 순) 제거·반환.
  divert        : 명령 5 — 우선순위 최하위(긴급도 작은 순 → 순번 큰 순) 제거·반환.
                  빈 대기열이면 -1 반환.
=========================================================*/

void init(int P, const int fids[], const int urg[])
{
    /* TODO: 초기 대기 항공편 P편. fids[i], urg[i] (0-indexed)가
       요청 순번 i+1 의 초기 대기 항공편. 전역 자료 구조를 반드시 초기화할 것. */
}

void request(int fid, int u)
{
    /* TODO: 명령 1 — 비대기 fid 를 긴급도 u 로 등록(새 요청 순번 부여). */
}

void renew(int fid, int u)
{
    /* TODO: 명령 2 — 대기 중 fid 의 긴급도를 u 로 변경(요청 순번 유지). */
}

void cancel(int fid)
{
    /* TODO: 명령 3 — 대기 중 fid 가 대기열에서 이탈. */
}

int clear_landing(void)
{
    /* TODO: 명령 4 — 최긴급 착륙 허가. 제거한 fid 반환. 빈 대기열이면 -1. */
    return -1;
}

int divert(void)
{
    /* TODO: 명령 5 — 최저긴급 회항. 제거한 fid 반환. 빈 대기열이면 -1. */
    return -1;
}

/*========= 이하 수정 비권장 (출력 형식 유지) =========*/
#define MAX_P 60000
static int in_fids[MAX_P];
static int in_urg[MAX_P];
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
        int P, M, i;
        P = read_int(); M = read_int();
        for (i = 0; i < P; i++) {
            in_fids[i] = read_int();
            in_urg[i] = read_int();
        }
        init(P, in_fids, in_urg);
        printf("#%d\n", tc);
        while (M--) {
            int op = read_int();
            if (op == 1) {
                int fid = read_int(), u = read_int();
                request(fid, u);
            } else if (op == 2) {
                int fid = read_int(), u = read_int();
                renew(fid, u);
            } else if (op == 3) {
                int fid = read_int();
                cancel(fid);
            } else if (op == 4) {
                printf("%d\n", clear_landing());
            } else {
                printf("%d\n", divert());
            }
        }
    }
    return 0;
}

[C++]

#include <cstdio>
/* 필요한 STL 헤더는 자유롭게 추가해도 된다.
   단, 아래 전역 함수 이름(예: clear_landing, divert)과 std 의 이름 충돌을
   피하기 위해 using namespace std; 는 쓰지 말고 std:: 접두사를 사용할 것. */

/*=========================================================
  공항 활주로 관제 시스템
  여기서부터 6개 함수만 구현하시오.
  main 및 입출력 부분은 수정하지 않는 것을 권장한다.

  init      : 각 테스트 케이스 시작 시 1회 호출. 전역 자료 구조 초기화.
  request   : 명령 1 — 비대기 fid 를 긴급도 u 로 착륙 대기열 등록(새 요청 순번).
  renew     : 명령 2 — 대기 중 fid 의 긴급도를 u 로 변경(요청 순번 유지).
  cancel    : 명령 3 — 대기 중 fid 가 대기열에서 이탈.
  clear_landing : 명령 4 — 우선순위 1위(긴급도 큰 순 → 순번 작은 순) 제거·반환.
  divert        : 명령 5 — 우선순위 최하위(긴급도 작은 순 → 순번 큰 순) 제거·반환.
                  빈 대기열이면 -1 반환.
=========================================================*/

void init(int P, const int fids[], const int urg[])
{
    // TODO: 초기 대기 항공편 P편. fids[i], urg[i] (0-indexed)가
    //       요청 순번 i+1 의 초기 대기 항공편. 전역 자료 구조를 반드시 초기화할 것.
}

void request(int fid, int u)
{
    // TODO: 명령 1 — 비대기 fid 를 긴급도 u 로 등록(새 요청 순번 부여).
}

void renew(int fid, int u)
{
    // TODO: 명령 2 — 대기 중 fid 의 긴급도를 u 로 변경(요청 순번 유지).
}

void cancel(int fid)
{
    // TODO: 명령 3 — 대기 중 fid 가 대기열에서 이탈.
}

int clear_landing()
{
    // TODO: 명령 4 — 최긴급 착륙 허가. 제거한 fid 반환. 빈 대기열이면 -1.
    return -1;
}

int divert()
{
    // TODO: 명령 5 — 최저긴급 회항. 제거한 fid 반환. 빈 대기열이면 -1.
    return -1;
}

/*========= 이하 수정 비권장 (출력 형식 유지) =========*/
#define MAX_P 60000
static int in_fids[MAX_P];
static int in_urg[MAX_P];
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
        int P, M, i;
        P = read_int(); M = read_int();
        for (i = 0; i < P; i++) {
            in_fids[i] = read_int();
            in_urg[i] = read_int();
        }
        init(P, in_fids, in_urg);
        printf("#%d\n", tc);
        while (M--) {
            int op = read_int();
            if (op == 1) {
                int fid = read_int(), u = read_int();
                request(fid, u);
            } else if (op == 2) {
                int fid = read_int(), u = read_int();
                renew(fid, u);
            } else if (op == 3) {
                int fid = read_int();
                cancel(fid);
            } else if (op == 4) {
                printf("%d\n", clear_landing());
            } else {
                printf("%d\n", divert());
            }
        }
    }
    return 0;
}

[Java]

import java.io.*;

public class Solution {

    /*=========================================================
      공항 활주로 관제 시스템
      여기서부터 6개 메서드만 구현하시오.
      main 및 입출력 부분은 수정하지 않는 것을 권장한다.

      init      : 각 테스트 케이스 시작 시 1회 호출. 전역 자료 구조 초기화.
      request   : 명령 1 — 비대기 fid 를 긴급도 u 로 착륙 대기열 등록(새 요청 순번).
      renew     : 명령 2 — 대기 중 fid 의 긴급도를 u 로 변경(요청 순번 유지).
      cancel    : 명령 3 — 대기 중 fid 가 대기열에서 이탈.
      clearLanding : 명령 4 — 우선순위 1위(긴급도 큰 순 → 순번 작은 순) 제거·반환.
      divert       : 명령 5 — 우선순위 최하위(긴급도 작은 순 → 순번 큰 순) 제거·반환.
                     빈 대기열이면 -1 반환.
      (Java 관례상 명령 4 함수명은 camelCase clearLanding 을 사용한다.)
    =========================================================*/

    static void init(int P, int[] fids, int[] urg) {
        // TODO: 초기 대기 항공편 P편. fids[i], urg[i] (0-indexed)가
        //       요청 순번 i+1 의 초기 대기 항공편. 전역 자료 구조를 반드시 초기화할 것.
    }

    static void request(int fid, int u) {
        // TODO: 명령 1 — 비대기 fid 를 긴급도 u 로 등록(새 요청 순번 부여).
    }

    static void renew(int fid, int u) {
        // TODO: 명령 2 — 대기 중 fid 의 긴급도를 u 로 변경(요청 순번 유지).
    }

    static void cancel(int fid) {
        // TODO: 명령 3 — 대기 중 fid 가 대기열에서 이탈.
    }

    static int clearLanding() {
        // TODO: 명령 4 — 최긴급 착륙 허가. 제거한 fid 반환. 빈 대기열이면 -1.
        return -1;
    }

    static int divert() {
        // TODO: 명령 5 — 최저긴급 회항. 제거한 fid 반환. 빈 대기열이면 -1.
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
            in.nextToken(); int P = (int) in.nval;
            in.nextToken(); int M = (int) in.nval;
            int[] fids = new int[P];
            int[] urg = new int[P];
            for (int i = 0; i < P; i++) {
                in.nextToken(); fids[i] = (int) in.nval;
                in.nextToken(); urg[i] = (int) in.nval;
            }
            init(P, fids, urg);
            sb.append('#').append(tc).append('\n');
            for (int q = 0; q < M; q++) {
                in.nextToken(); int op = (int) in.nval;
                if (op == 1) {
                    in.nextToken(); int fid = (int) in.nval;
                    in.nextToken(); int u = (int) in.nval;
                    request(fid, u);
                } else if (op == 2) {
                    in.nextToken(); int fid = (int) in.nval;
                    in.nextToken(); int u = (int) in.nval;
                    renew(fid, u);
                } else if (op == 3) {
                    in.nextToken(); int fid = (int) in.nval;
                    cancel(fid);
                } else if (op == 4) {
                    sb.append(clearLanding()).append('\n');
                } else {
                    sb.append(divert()).append('\n');
                }
            }
        }
        System.out.print(sb);
    }
}

[Python]

import sys

# =========================================================
#  공항 활주로 관제 시스템
#  여기서부터 6개 함수만 구현하시오.
#  (파이썬 내장 id 와의 혼동을 피하기 위해 항공편 식별자는 fid,
#   긴급도는 u 라는 이름을 사용한다.)
#  main 및 입출력 부분은 수정하지 않는 것을 권장한다.
#
#  init      : 각 테스트 케이스 시작 시 1회 호출. 전역 자료 구조 초기화.
#  request   : 명령 1 — 비대기 fid 를 긴급도 u 로 착륙 대기열 등록(새 요청 순번).
#  renew     : 명령 2 — 대기 중 fid 의 긴급도를 u 로 변경(요청 순번 유지).
#  cancel    : 명령 3 — 대기 중 fid 가 대기열에서 이탈.
#  clear_landing : 명령 4 — 우선순위 1위(긴급도 큰 순 → 순번 작은 순) 제거·반환.
#  divert        : 명령 5 — 우선순위 최하위(긴급도 작은 순 → 순번 큰 순) 제거·반환.
#                  빈 대기열이면 -1 반환.
# =========================================================

def init(P, fids, urg):
    # TODO: 초기 대기 항공편 P편. fids[i], urg[i] (0-indexed)가
    #       요청 순번 i+1 의 초기 대기 항공편. 전역 자료 구조를 반드시 초기화할 것.
    pass

def request(fid, u):
    # TODO: 명령 1 — 비대기 fid 를 긴급도 u 로 등록(새 요청 순번 부여).
    pass

def renew(fid, u):
    # TODO: 명령 2 — 대기 중 fid 의 긴급도를 u 로 변경(요청 순번 유지).
    pass

def cancel(fid):
    # TODO: 명령 3 — 대기 중 fid 가 대기열에서 이탈.
    pass

def clear_landing():
    # TODO: 명령 4 — 최긴급 착륙 허가. 제거한 fid 반환. 빈 대기열이면 -1.
    return -1

def divert():
    # TODO: 명령 5 — 최저긴급 회항. 제거한 fid 반환. 빈 대기열이면 -1.
    return -1

# ========= 이하 수정 비권장 (출력 형식 유지) =========
def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    out = []
    T = int(next(it))
    for tc in range(1, T + 1):
        P = int(next(it)); M = int(next(it))
        fids = [0] * P
        urg = [0] * P
        for i in range(P):
            fids[i] = int(next(it))
            urg[i] = int(next(it))
        init(P, fids, urg)
        out.append('#%d' % tc)
        for _ in range(M):
            op = int(next(it))
            if op == 1:
                fid = int(next(it)); u = int(next(it))
                request(fid, u)
            elif op == 2:
                fid = int(next(it)); u = int(next(it))
                renew(fid, u)
            elif op == 3:
                fid = int(next(it))
                cancel(fid)
            elif op == 4:
                out.append(str(clear_landing()))
            else:
                out.append(str(divert()))
    sys.stdout.write('\n'.join(out) + '\n')

main()

[제약 사항]

항목범위 / 조건
테스트 케이스 수 T1 ≤ T ≤ 12, 이 중 P > 10,000인 대형 테스트 케이스는 최대 3개
항공편 식별자 fid1 ≤ fid ≤ 100,000. 같은 순간 대기 중인 항공편의 fid는 서로 다르며, 착륙·회항·철회된 fid는 재요청될 수 있음
긴급도 u1 ≤ u ≤ 100,000 (초기 명단·명령 1·명령 2 공통)
초기 대기 편수 P0 ≤ P ≤ 60,000. 초기 명단은 P개 줄, 각 줄에 "fid u". 입력 순서가 곧 요청 순번 1..P
명령 유효성명령 2, 3은 대기 중인 fid에만, 명령 1은 대기 중이 아닌 fid에만 주어짐 (별도 오류 처리 불필요)
명령 수 (테스트 케이스당)M ≤ 150,000 — 요청(1) ≤ 50,000 / 재산정(2) ≤ 40,000 / 철회(3) ≤ 20,000 / 착륙 허가(4) ≤ 45,000 / 회항(5) ≤ 45,000
명령 수 (입력 파일 전체 합)P의 합 ≤ 210,000, 요청 ≤ 170,000, 재산정 ≤ 80,000, 철회 ≤ 40,000, 착륙 허가 ≤ 160,000, 회항 ≤ 160,000

[유의 사항]

· 제한 시간은 입력 파일 전체(모든 테스트 케이스)를 처리하는 기준이다.
· 시간 복잡도에 주의. 매 착륙 허가·회항마다 대기 중인 모든 항공편을 선형으로 훑어 가장 긴급한/여유로운 항공편을 찾는 단순한 방법으로는 통과할 수 없도록 채점 데이터가 구성되어 있다. 한쪽 방향만 빠르게 처리하는 절반짜리 구현으로도 부족하다.
· 착륙 허가(최댓값)와 회항(최솟값)이 양방향으로 공존하고, 재산정·철회·재요청으로 대기 중 임의 항공편의 우선순위가 수시로 바뀌거나 무효화된다는 점에 유의하라.
· 각 테스트 케이스는 독립적이다. 이전 테스트 케이스의 상태가 남지 않도록 init에서 요청 순번 카운터를 포함한 모든 전역 자료 구조를 초기화하라.
· 표준 라이브러리(STL, java.util 등)는 사용할 수 있다.
· C/C++ 뼈대는 입력 전체를 한 번에 읽으므로, 로컬에서 테스트할 때는 키보드 입력 대신 파일 리다이렉션(예: prog.exe < input.txt)을 사용하라.
· 주어진 예시를 통과하더라도 채점에는 공개되지 않은 테스트 케이스가 포함되므로, 제약 최대 규모에서 시간 내에 동작하는지 반드시 확인하라.

[예제 1]
입력:
2
4 8
101 5
202 3
303 5
404 2
4
1 505 7
2 202 9
4
5
3 303
4
5
6 30
10 3
20 3
30 7
40 5
50 3
60 1
5
5
2 10 3
4
4
5
4
5
4
5
1 30 4
1 60 4
4
5
4
1 10 3
1 20 3
3 10
1 10 3
5
1 40 8
2 20 8
4
4
1 55 2
1 65 2
1 75 9
4
5
4
출력:
#1
101
202
404
505
-1
#2
60
50
30
40
20
10
-1
-1
-1
30
60
-1
10
20
40
75
65
55
"""

import heapq
import sys
def init(P, fids, urg):
    # TODO: 초기 대기 항공편 P편. fids[i], urg[i] (0-indexed)가
    #       요청 순번 i+1 의 초기 대기 항공편. 전역 자료 구조를 반드시 초기화할 것.
    global version, CNT, landing_q, return_q, g_cnt
    
    CNT = 1
    # 버전
    version = {}
    # 긴급도 큰순서, 같으면 순번 작은 순서., fid, 버전.
    landing_q = []
    # 긴급도 작은순서, 요청순번이 큰순서, fid, 버전.
    return_q = []
    # 요청 순번
    g_cnt = {}

    for p in range(P):
        cur_fid = fids[p]
        cur_urg = urg[p]
        cur_ver = 0
        cur_cnt = CNT
        g_cnt[cur_fid] = cur_cnt
        version[cur_fid] = cur_ver
        heapq.heappush(landing_q, [-cur_urg, cur_cnt, cur_fid, cur_ver])
        heapq.heappush(return_q, [cur_urg, -cur_cnt, cur_fid, cur_ver])
        CNT += 1
    # print(landing_q)

def request(fid, u):
    # TODO: 명령 1 — 비대기 fid 를 긴급도 u 로 등록(새 요청 순번 부여).
    global CNT
    cur_fid = fid
    cur_urg = u
    cur_ver = version.get(fid, 0)
    if cur_ver != 0:
        cur_ver += 1
    cur_cnt = CNT
    version[cur_fid] = cur_ver
    g_cnt[fid] = CNT
    heapq.heappush(landing_q, [-cur_urg, cur_cnt, cur_fid, cur_ver])
    heapq.heappush(return_q, [cur_urg, -cur_cnt, cur_fid, cur_ver])
    CNT += 1

def renew(fid, u):
    # TODO: 명령 2 — 대기 중 fid 의 긴급도를 u 로 변경(요청 순번 유지).
    cur_fid = fid
    new_urg = u
    new_ver = version[fid] + 1
    cur_cnt = g_cnt[fid]
    version[fid] = new_ver
    heapq.heappush(landing_q, [-new_urg, cur_cnt, cur_fid, new_ver])
    heapq.heappush(return_q, [new_urg, -cur_cnt, cur_fid, new_ver])

def cancel(fid):
    # TODO: 명령 3 — 대기 중 fid 가 대기열에서 이탈.
    version[fid] += 1

def clear_landing():
    # TODO: 명령 4 — 최긴급 착륙 허가. 제거한 fid 반환. 빈 대기열이면 -1.
    while landing_q:
        cur_urg, cur_cnt, cur_fid, cur_ver = heapq.heappop(landing_q)
        # 이미 삭제된 버전이면 continue
        if cur_ver != version[cur_fid]:
            continue

        # print(landing_q)
        version[cur_fid] += 1
        return cur_fid
    
    return -1


def divert():
    # TODO: 명령 5 — 최저긴급 회항. 제거한 fid 반환. 빈 대기열이면 -1.
    while return_q:
        cur_urg, cur_cnt, cur_fid, cur_ver = heapq.heappop(return_q)
        # 이미 삭제된 버전이면 continue
        if cur_ver != version[cur_fid]:
            continue
        version[cur_fid] += 1
        return cur_fid
    return -1


# ========= 이하 수정 비권장 (출력 형식 유지) =========
def main():
    out = []

    T = int(input())

    for tc in range(1, T + 1):
        P, M = map(int, input().split())

        fids = [0] * P
        urg = [0] * P

        for i in range(P):
            fids[i], urg[i] = map(int, input().split())

        init(P, fids, urg)

        out.append(f'#{tc}')

        for _ in range(M):
            cmd = list(map(int, input().split()))
            op = cmd[0]

            if op == 1:
                request(cmd[1], cmd[2])

            elif op == 2:
                renew(cmd[1], cmd[2])

            elif op == 3:
                cancel(cmd[1])

            elif op == 4:
                out.append(str(clear_landing()))

            else:
                out.append(str(divert()))

    print('\n'.join(out))


main()
