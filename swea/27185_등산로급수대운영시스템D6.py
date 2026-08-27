"""
SWEA 27185  등산로 급수대 운영 시스템 D6
https://swexpertacademy.com/main/code/userProblem/userProblemDetail.do?fromProbList=N&deleteYn=N&contestProbId=AZ-JQYsqpU_HBITH&topPath=code&lastPath=problemDetail&secondPath=problem&menuBreakDown=swea.code.menu&menuBreakDown=swea.code.problem.menu&menuDesc=swea.code.desc&menuDesc=swea.code.problem.desc&contextPath=%2Fmain&locale=ko-kr%2Cko%3Bq%3D0.9%2Cen-us%3Bq%3D0.8%2Cen%3Bq%3D0.7&serverName=localhost&localeLanguage=ko_KR&localeLanguage2=Ko_KR&remoteAddr=175.213.163.17&scripts=%2Fjs%2Finit%2Fjquery-debug.js&scripts=%2Fjs%2Finit%2Fjquery-ui.js&scripts=%2Fjs%2Finit%2Fjquery.validate.js&scripts=%2Fjs%2Fcommon.js&NOTICE_NEW_COUNT=0&ssoLogin=false&hasSDPAdminLinkAuth=false&systemAdmin=false&backendAdmin=false&isTechBlogManager=false&CURRENT_MENU_AUTHORIZATION=READ&CURRENT_MENU_AUTHORIZATION=UPDATE&CURRENT_MENU_AUTHORIZATION=EXECUTE&CURRENT_MENU_AUTHORIZATION=DOWNLOAD&logoMainfileName=logo_company.png

풀이일 : 2026-08-27   결과: 품
한도   : time 12개 테스트케이스를 합쳐서 C/C++의 경우 1초 / Java의 경우 6초 / memory 힙, 정적 메모리 합쳐서 256MB 이내, 스택 메모리 1MB 이내 / time_sec 1
난이도 : ?  |  정답률 33.33%

[채점] accepted  1/1  (0.313s)

[문제]
국립공원 관리공단은 등산로 입구부터 정상까지 이어지는 탐방로를 따라 늘어선 쉼터에 급수대를 설치·운영하는 관제 시스템을 구축한다. 쉼터는 수시로 신설되거나 폐쇄되며, 예산상 급수대는 일부 쉼터에만 설치할 수 있다.

시스템은 매 시점 두 가지 배치 지표를 즉시 계산해야 한다. 하나는 탐방객 분산을 위해 급수대 사이가 최대한 벌어지도록 k곳을 고르는 배치이고(인접 간격의 최소값을 최대화), 다른 하나는 순찰 보급을 위해 양끝 쉼터를 반드시 포함해 k곳을 골라 가장 긴 무급수 구간을 줄이는 배치이다(인접 간격의 최대값을 최소화). 한편 순찰 드론은 경로 점검을 위해 임의 지점에서 “그 지점 이상에서 가장 가까운 쉼터”를 연쇄적으로 대량 조회하는데, 직전 조회 결과가 다음 조회 지점을 결정한다.

당신은 관제 시스템에 들어오는 5종류의 명령을 순서대로 처리하는 프로그램을 작성해야 한다.

[위치와 쉼터]

탐방로는 하나의 수직선이며, 각 쉼터는 입구로부터의 거리를 나타내는 하나의 정수 위치 p로 식별된다(1 ≤ p ≤ 10^9, 단위 m). 어느 시점에도 서로 다른 두 쉼터가 같은 위치에 있지 않다.

여러 쉼터를 위치 오름차순으로 늘어놓았을 때 이웃한 두 쉼터를 인접하다고 하며, 인접한 두 쉼터의 간격은 그 위치의 차이다.

[급수대 배치 지표]

· 명령 3은 현재 존재하는 쉼터 중 정확히 k곳을 골라 급수대를 설치할 때, 선택한 k곳을 위치 순으로 늘어놓은 인접 간격의 최솟값을 최대로 만드는 배치의 그 값을 구한다.

· 명령 4는 위치가 가장 작은 쉼터와 가장 큰 쉼터를 반드시 포함해 정확히 k곳을 골라 보급 거점을 설치할 때, 선택한 k곳의 인접 간격의 최댓값을 최소로 만드는 배치의 그 값을 구한다.

두 명령 모두 입력에서 k ≥ 2가 보장되며, k가 현재 쉼터 수보다 크면 배치가 불가능하므로 −1을 출력한다. 특별한 경우로, k가 현재 쉼터 수와 같으면 명령 3의 답은 최소 인접 간격, 명령 4의 답은 최대 인접 간격이 되고, k = 2이면 두 명령 모두 답이 (최대 위치 − 최소 위치)가 된다.

[순찰 드론 조회 — 명령 5]

명령 5 s c는 순찰 드론 경로를 점검한다. 시작 지점 x_1 = s에서 출발하여, i = 1, 2, …, c에 대해 다음을 반복한다.

  · y_i = 현재 존재하는 쉼터 중 위치가 x_i 이상인 최소 위치 (그런 쉼터가 없으면 0)
  · 다음 조회 지점 x_(i+1) = (x_i + y_i) mod 1,000,000,000 + 1

직전 조회 결과가 다음 조회 지점을 결정하므로 c개의 조회는 순차적으로 의존한다. 출력은 Σ y_i (i = 1..c)이다. 이 합은 최대 3×10^11에 이르러 32비트 정수를 초과하므로 64비트 정수로 다루어야 하는데, 체인 반복과 합산·출력은 뼈대 main이 모두 처리하고 당신은 위치 조회 한 번을 담당하는 next_site 함수만 구현한다.

[처리해야 할 명령]

각 테스트 케이스는 초기 쉼터 목록과 M개의 명령으로 구성된다. 명령은 다음 5종류이다.

명령형식동작출력
1 (신설)1 p위치 p에 쉼터를 신설한다. 현재 쉼터가 없는 위치만 주어짐이 보장된다.없음
2 (폐쇄)2 p위치 p의 쉼터를 폐쇄한다. 현재 쉼터가 있는 위치만 주어짐이 보장된다.없음
3 (질의)3 k현재 쉼터 중 정확히 k곳 선택 시 인접 간격의 최솟값을 최대화한 값그 값(정수)을 한 줄에 출력. k > 현재 쉼터 수이면 −1
4 (질의)4 k양끝(최소·최대 위치) 쉼터를 포함해 정확히 k곳 선택 시 인접 간격의 최댓값을 최소화한 값그 값(정수)을 한 줄에 출력. k > 현재 쉼터 수이면 −1
5 (조회)5 s cx_1 = s에서 시작하는 c회의 순찰 드론 successor 조회 체인Σ y_i (64비트 정수)를 한 줄에 출력

[예시] 초기 쉼터가 6 1 10 3의 순서(입력 순서 = 등록 순서일 뿐, 위치 오름차순이 아님)로 주어진 경우를 보자. 위치 오름차순으로 나타내면 {1, 3, 6, 10}이다.

[[IMG:1]]

① 명령 3 3 — 쉼터 {1, 3, 6, 10} 중 3곳을 골라 인접 간격의 최솟값을 최대화한다. 인접 간격이 모두 4 이상이 되도록 1, 6, 10을 고르면 3곳을 배치할 수 있지만, 모두 5 이상이 되도록 3곳을 배치하는 것은 불가능하다. 따라서 답은 4이다.

[[IMG:2]]

② 명령 1 8 — 위치 8에 쉼터를 신설한다. 8은 6과 10 사이이므로 쉼터는 {1, 3, 6, 8, 10}이 된다.

[[IMG:3]]

③ 명령 4 3 — 쉼터 {1, 3, 6, 8, 10}에서 양끝 1과 10을 반드시 포함해 3곳을 골라 인접 간격의 최댓값을 최소화한다. 인접 간격이 모두 5 이하가 되도록 1, 6, 10에 3거점을 두면 조건을 만족하지만, 모두 4 이하로 하려면 1, 3, 6, 10으로 4거점이 필요해 3곳으로는 불가능하다. 따라서 답은 5이다.

[[IMG:4]]

④ 명령 2 6 — 위치 6의 쉼터를 폐쇄하면 쉼터는 {1, 3, 8, 10}이 된다. ⑤ 이어서 명령 4 3을 처리하면 양끝 1, 10 고정에 중간 한 곳(3 또는 8)을 더해 인접 간격의 최댓값이 7이 되어 답은 7이다.

⑥ 명령 5 2 3 — 순찰 드론 조회를 3회 반복한다. x_1 = 2에서 y_1 = next_site(2) = 3(2 이상 최소 위치), x_2 = (2 + 3) mod 10^9 + 1 = 6에서 y_2 = next_site(6) = 8, x_3 = (6 + 8) mod 10^9 + 1 = 15에서 15 이상 쉼터가 없어 y_3 = 0이다. 합은 3 + 8 + 0 = 11을 출력한다.

⑦ 명령 3 5 — 현재 쉼터가 4개뿐이라 5곳을 선택할 수 없으므로 −1을 출력한다.

이 테스트 케이스의 출력은 순서대로 4, 5, 7, 11, −1의 5줄이다(명령 1, 2는 출력이 없다).

[제공되는 뼈대 코드 — 커맨드 패턴]

아래에 언어별 뼈대 코드가 제공된다. main 함수는 입력 파싱과 명령 분기(커맨드 패턴), 명령 5의 체인 반복·64비트 합산·출력을 모두 처리하며, 당신은 6개 함수 — init, add_site, close_site, next_site, max_min_distance, min_max_distance — 만 구현하면 된다. 필요한 전역 변수, 보조 함수, 클래스는 자유롭게 추가해도 된다. 명령 5에서 당신이 맡는 부분은 next_site(x) 한 번의 위치 조회뿐이며, 체인 루프와 합산·출력은 main이 담당한다.

뼈대 전체를 복사해 함수 구현을 채워 제출하라. 함수의 원형(시그니처)은 변경하지 말고, main과 입출력 부분은 수정하지 않는 것을 권장한다. main을 수정하더라도 입출력 형식만 일치하면 정답으로 처리되지만, 최종 출력 형식은 반드시 유지해야 한다.

[C]

#include <stdio.h>

/*=========================================================
  여기서부터 6개 함수만 구현하시오.
  main 및 입출력 부분은 수정하지 않는 것을 권장한다.

  init      : 각 테스트 케이스 시작 시 1회 호출 (전역 초기화 필수)
  add_site  : 명령 1 — 위치 p에 쉼터 신설 (현재 없는 위치만 주어짐)
  close_site: 명령 2 — 위치 p의 쉼터 폐쇄 (현재 있는 위치만 주어짐)
  next_site : 명령 5의 단위 조회 — x 이상인 최소 쉼터 위치, 없으면 0
              (체인 반복·64비트 합산·출력은 아래 main이 수행한다)
  max_min_distance: 명령 3 — 답 반환, k가 현재 쉼터 수보다 크면 -1
  min_max_distance: 명령 4 — 답 반환, k가 현재 쉼터 수보다 크면 -1
=========================================================*/

void init(int n, const int sites[])
{
    /* TODO: 초기 쉼터 n개(정렬 비보장·셔플 순서)를 등록하고
       전역 자료 구조를 반드시 초기화할 것. n = 0이면 빈 배열. */
}

void add_site(int p)
{
    /* TODO: 위치 p에 쉼터 신설 */
}

void close_site(int p)
{
    /* TODO: 위치 p의 쉼터 폐쇄 */
}

int next_site(int x)
{
    /* TODO: x 이상인 최소 쉼터 위치를 반환, 없으면 0 */
    return 0;
}

int max_min_distance(int k)
{
    /* TODO: 정확히 k곳 선택 시 인접 간격의 최솟값을 최대화한 값.
       k가 현재 쉼터 수보다 크면 -1 */
    return -1;
}

int min_max_distance(int k)
{
    /* TODO: 최소·최대 위치를 반드시 포함해 정확히 k곳 선택 시
       인접 간격의 최댓값을 최소화한 값. k가 현재 쉼터 수보다 크면 -1 */
    return -1;
}

/*========= 이하 수정 비권장 (출력 형식 유지) =========*/
#define MAX_INIT 10005

static int in_sites[MAX_INIT];
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
        int n, M, i;
        n = read_int(); M = read_int();
        for (i = 0; i < n; i++)
            in_sites[i] = read_int();
        init(n, in_sites);
        printf("#%d\n", tc);
        while (M--) {
            int op = read_int();
            if (op == 1) {
                int p = read_int();
                add_site(p);
            } else if (op == 2) {
                int p = read_int();
                close_site(p);
            } else if (op == 3) {
                int k = read_int();
                printf("%d\n", max_min_distance(k));
            } else if (op == 4) {
                int k = read_int();
                printf("%d\n", min_max_distance(k));
            } else {
                int s = read_int(), c = read_int(), j;
                long long total = 0;
                int x = s;
                for (j = 0; j < c; j++) {
                    int y = next_site(x);
                    total += y;
                    x = (int)(((long long)x + y) % 1000000000 + 1);
                }
                printf("%lld\n", total);
            }
        }
    }
    return 0;
}

[C++]

#include <cstdio>
/* 필요한 STL 헤더는 자유롭게 추가해도 된다.
   단, next_site 등 전역 함수명과 std 심볼의 충돌을 피하기 위해
   using namespace std; 는 쓰지 말고 std:: 접두사를 사용할 것. */

/*=========================================================
  여기서부터 6개 함수만 구현하시오.
  main 및 입출력 부분은 수정하지 않는 것을 권장한다.

  init      : 각 테스트 케이스 시작 시 1회 호출 (전역 초기화 필수)
  add_site  : 명령 1 — 위치 p에 쉼터 신설 (현재 없는 위치만 주어짐)
  close_site: 명령 2 — 위치 p의 쉼터 폐쇄 (현재 있는 위치만 주어짐)
  next_site : 명령 5의 단위 조회 — x 이상인 최소 쉼터 위치, 없으면 0
              (체인 반복·64비트 합산·출력은 아래 main이 수행한다)
  max_min_distance: 명령 3 — 답 반환, k가 현재 쉼터 수보다 크면 -1
  min_max_distance: 명령 4 — 답 반환, k가 현재 쉼터 수보다 크면 -1
=========================================================*/

void init(int n, const int sites[])
{
    // TODO: 초기 쉼터 n개(정렬 비보장·셔플 순서)를 등록하고
    //       전역 자료 구조를 반드시 초기화할 것. n = 0이면 빈 배열.
}

void add_site(int p)
{
    // TODO: 위치 p에 쉼터 신설
}

void close_site(int p)
{
    // TODO: 위치 p의 쉼터 폐쇄
}

int next_site(int x)
{
    // TODO: x 이상인 최소 쉼터 위치를 반환, 없으면 0
    return 0;
}

int max_min_distance(int k)
{
    // TODO: 정확히 k곳 선택 시 인접 간격의 최솟값을 최대화한 값.
    //       k가 현재 쉼터 수보다 크면 -1
    return -1;
}

int min_max_distance(int k)
{
    // TODO: 최소·최대 위치를 반드시 포함해 정확히 k곳 선택 시
    //       인접 간격의 최댓값을 최소화한 값. k가 현재 쉼터 수보다 크면 -1
    return -1;
}

/*========= 이하 수정 비권장 (출력 형식 유지) =========*/
#define MAX_INIT 10005

static int in_sites[MAX_INIT];
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
        int n, M, i;
        n = read_int(); M = read_int();
        for (i = 0; i < n; i++)
            in_sites[i] = read_int();
        init(n, in_sites);
        printf("#%d\n", tc);
        while (M--) {
            int op = read_int();
            if (op == 1) {
                int p = read_int();
                add_site(p);
            } else if (op == 2) {
                int p = read_int();
                close_site(p);
            } else if (op == 3) {
                int k = read_int();
                printf("%d\n", max_min_distance(k));
            } else if (op == 4) {
                int k = read_int();
                printf("%d\n", min_max_distance(k));
            } else {
                int s = read_int(), c = read_int(), j;
                long long total = 0;
                int x = s;
                for (j = 0; j < c; j++) {
                    int y = next_site(x);
                    total += y;
                    x = (int)(((long long)x + y) % 1000000000 + 1);
                }
                printf("%lld\n", total);
            }
        }
    }
    return 0;
}

[Java]

import java.io.*;

public class Solution {

    /*=========================================================
      여기서부터 6개 메서드만 구현하시오.
      main 및 입출력 부분은 수정하지 않는 것을 권장한다.

      init         : 각 테스트 케이스 시작 시 1회 호출 (전역 초기화 필수)
      addSite      : 명령 1 — 위치 p에 쉼터 신설 (현재 없는 위치만 주어짐)
      closeSite    : 명령 2 — 위치 p의 쉼터 폐쇄 (현재 있는 위치만 주어짐)
      nextSite     : 명령 5의 단위 조회 — x 이상인 최소 쉼터 위치, 없으면 0
                     (체인 반복·64비트 합산·출력은 아래 main이 수행한다)
      maxMinDistance: 명령 3 — 답 반환, k가 현재 쉼터 수보다 크면 -1
      minMaxDistance: 명령 4 — 답 반환, k가 현재 쉼터 수보다 크면 -1
    =========================================================*/

    static void init(int n, int[] sites) {
        // TODO: 초기 쉼터 n개(정렬 비보장·셔플 순서)를 등록하고
        //       전역 자료 구조를 반드시 초기화할 것. n == 0이면 빈 배열.
    }

    static void addSite(int p) {
        // TODO: 위치 p에 쉼터 신설
    }

    static void closeSite(int p) {
        // TODO: 위치 p의 쉼터 폐쇄
    }

    static int nextSite(int x) {
        // TODO: x 이상인 최소 쉼터 위치를 반환, 없으면 0
        return 0;
    }

    static int maxMinDistance(int k) {
        // TODO: 정확히 k곳 선택 시 인접 간격의 최솟값을 최대화한 값.
        //       k가 현재 쉼터 수보다 크면 -1
        return -1;
    }

    static int minMaxDistance(int k) {
        // TODO: 최소·최대 위치를 반드시 포함해 정확히 k곳 선택 시
        //       인접 간격의 최댓값을 최소화한 값. k가 현재 쉼터 수보다 크면 -1
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
            in.nextToken(); int n = (int) in.nval;
            in.nextToken(); int M = (int) in.nval;
            int[] sites = new int[n];
            for (int i = 0; i < n; i++) {
                in.nextToken();
                sites[i] = (int) in.nval;
            }
            init(n, sites);
            sb.append('#').append(tc).append('\n');
            for (int q = 0; q < M; q++) {
                in.nextToken(); int op = (int) in.nval;
                if (op == 1) {
                    in.nextToken(); int p = (int) in.nval;
                    addSite(p);
                } else if (op == 2) {
                    in.nextToken(); int p = (int) in.nval;
                    closeSite(p);
                } else if (op == 3) {
                    in.nextToken(); int k = (int) in.nval;
                    sb.append(maxMinDistance(k)).append('\n');
                } else if (op == 4) {
                    in.nextToken(); int k = (int) in.nval;
                    sb.append(minMaxDistance(k)).append('\n');
                } else {
                    in.nextToken(); int s = (int) in.nval;
                    in.nextToken(); int c = (int) in.nval;
                    long total = 0;
                    int x = s;
                    for (int j = 0; j < c; j++) {
                        int y = nextSite(x);
                        total += y;
                        x = (int) (((long) x + y) % 1000000000 + 1);
                    }
                    sb.append(total).append('\n');
                }
            }
        }
        System.out.print(sb);
    }
}

[Python]

import sys

# =========================================================
#  여기서부터 6개 함수만 구현하시오.
#  main 및 입출력 부분은 수정하지 않는 것을 권장한다.
#
#  init             : 각 테스트 케이스 시작 시 1회 호출 (전역 초기화 필수)
#  add_site         : 명령 1 — 위치 p에 쉼터 신설 (현재 없는 위치만 주어짐)
#  close_site       : 명령 2 — 위치 p의 쉼터 폐쇄 (현재 있는 위치만 주어짐)
#  next_site        : 명령 5의 단위 조회 — x 이상인 최소 쉼터 위치, 없으면 0
#                     (체인 반복·64비트 합산·출력은 아래 main이 수행한다)
#  max_min_distance : 명령 3 — 답 반환, k가 현재 쉼터 수보다 크면 -1
#  min_max_distance : 명령 4 — 답 반환, k가 현재 쉼터 수보다 크면 -1
# =========================================================

def init(n, sites):
    # TODO: 초기 쉼터 n개(정렬 비보장·셔플 순서)를 등록하고
    #       전역 자료 구조를 반드시 초기화할 것. n == 0이면 빈 배열.
    pass

def add_site(p):
    # TODO: 위치 p에 쉼터 신설
    pass

def close_site(p):
    # TODO: 위치 p의 쉼터 폐쇄
    pass

def next_site(x):
    # TODO: x 이상인 최소 쉼터 위치를 반환, 없으면 0
    return 0

def max_min_distance(k):
    # TODO: 정확히 k곳 선택 시 인접 간격의 최솟값을 최대화한 값.
    #       k가 현재 쉼터 수보다 크면 -1
    return -1

def min_max_distance(k):
    # TODO: 최소·최대 위치를 반드시 포함해 정확히 k곳 선택 시
    #       인접 간격의 최댓값을 최소화한 값. k가 현재 쉼터 수보다 크면 -1
    return -1

# ========= 이하 수정 비권장 (출력 형식 유지) =========
def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    out = []
    T = int(next(it))
    for tc in range(1, T + 1):
        n = int(next(it)); M = int(next(it))
        sites = [int(next(it)) for _ in range(n)]
        init(n, sites)
        out.append('#%d' % tc)
        for _ in range(M):
            op = int(next(it))
            if op == 1:
                p = int(next(it)); add_site(p)
            elif op == 2:
                p = int(next(it)); close_site(p)
            elif op == 3:
                k = int(next(it)); out.append(str(max_min_distance(k)))
            elif op == 4:
                k = int(next(it)); out.append(str(min_max_distance(k)))
            else:
                s = int(next(it)); c = int(next(it))
                x = s
                total = 0
                for _ in range(c):
                    y = next_site(x)
                    total += y
                    x = (x + y) % 1000000000 + 1
                out.append(str(total))
    sys.stdout.write('\n'.join(out) + '\n')

main()

[제약 사항]

항목범위 / 조건
테스트 케이스 수 T1 ≤ T ≤ 12
위치 p, 조회 시드 s1 ≤ p, s ≤ 1,000,000,000 (정수, 단위 m). 어느 시점에도 쉼터 위치 중복 없음
초기 쉼터 수 N0 ≤ N ≤ 7,000 (init 배열은 정렬 비보장 셔플 순서)
동시 존재 쉼터 수모든 시점에 10,000 이하
명령 수 (테스트 케이스당)M ≤ 15,000 — 신설(1) ≤ 8,000 / 폐쇄(2) ≤ 5,000 / 질의(3) ≤ 15 / 질의(4) ≤ 15 / 조회(5) ≤ 2,500
명령 5 반복 c1 ≤ c ≤ 300, 테스트 케이스당 Σc ≤ 300,000
질의 k2 ≤ k ≤ 10,000 (명령 3, 4 공통)
명령 수 (입력 파일 전체 합)ΣN ≤ 40,000 / 신설 ≤ 40,000 / 폐쇄 ≤ 20,000 / 질의(3) ≤ 70 / 질의(4) ≤ 70 / 조회(5) Σc ≤ 1,300,000
대형 테스트 케이스최대 동시 쉼터 수가 2,000을 초과하는 테스트 케이스는 5개 이하
명령 5 출력값3×10^11 이하 (64비트 정수 필요 — 뼈대가 처리)

[유의 사항]

· 제한 시간은 입력 파일 전체(모든 테스트 케이스)를 처리하는 기준이다.
· 시간 복잡도에 주의. 매 질의마다 모든 위치 쌍을 후보로 나열·정렬하거나, 명령 5의 조회마다 쉼터 전체를 선형으로 훑거나, 조회 때마다 전체를 다시 정렬하는 단순한 방법으로는 통과할 수 없도록 채점 데이터가 구성되어 있다. 효율적인 자료 구조와 탐색 설계가 필요하다.
· 각 테스트 케이스는 독립적이다. 이전 테스트 케이스의 상태가 남지 않도록 init에서 모든 전역 자료 구조를 초기화하라.
· 명령 5의 합은 64비트 정수 범위이며, 뼈대 main이 이를 처리한다. 당신은 next_site(x) 한 번의 조회만 정확히 구현하면 된다.
· 표준 라이브러리(STL, java.util 등)는 사용할 수 있다.
· C/C++ 뼈대는 입력 전체를 한 번에 읽으므로, 로컬에서 테스트할 때는 키보드 입력 대신 파일 리다이렉션(예: prog.exe < input.txt)을 사용하라.
· 주어진 예시를 통과하더라도 채점에는 공개되지 않은 테스트 케이스가 포함되므로, 제약 최대 규모에서 시간 내에 동작하는지 반드시 확인하라.

[예제 1]
입력:
2
4 7
6 1 10 3
3 3
1 8
4 3
2 6
4 3
5 2 3
3 5
4 29
10 2 5 8
3 4
4 4
3 5
4 5
3 2
4 2
2 2
4 3
2 10
4 2
1 2
1 3
3 4
2 5
2 8
2 3
3 2
2 2
3 2
5 100 3
1 1
1 250000000
1 500000000
1 750000000
1 1000000000
5 1 300
5 1000000000 2
2 1000000000
5 1000000000 1
출력:
#1
4
5
7
11
-1
#2
2
3
-1
-1
8
8
3
3
1
-1
-1
0
297750000001
1000000001
0
"""

import sys
from bisect import bisect_left, bisect_right

# =========================================================
#  여기서부터 6개 함수만 구현하시오.
#  main 및 입출력 부분은 수정하지 않는 것을 권장한다.
#
#  init             : 각 테스트 케이스 시작 시 1회 호출 (전역 초기화 필수)
#  add_site         : 명령 1 — 위치 p에 쉼터 신설 (현재 없는 위치만 주어짐)
#  close_site       : 명령 2 — 위치 p의 쉼터 폐쇄 (현재 있는 위치만 주어짐)
#  next_site        : 명령 5의 단위 조회 — x 이상인 최소 쉼터 위치, 없으면 0
#                     (체인 반복·64비트 합산·출력은 아래 main이 수행한다)
#  max_min_distance : 명령 3 — 답 반환, k가 현재 쉼터 수보다 크면 -1
#  min_max_distance : 명령 4 — 답 반환, k가 현재 쉼터 수보다 크면 -1
# =========================================================

def init(n, sites):
    # TODO: 초기 쉼터 n개(정렬 비보장·셔플 순서)를 등록하고
    #       전역 자료 구조를 반드시 초기화할 것. n == 0이면 빈 배열.
    global g_N, g_sites

    g_N = n
    g_sites = sites
    g_sites.sort()

    pass


def add_site(p):
    global g_N
    # TODO: 위치 p에 쉼터 신설
    cur_idx = bisect_left(g_sites, p)
    g_sites.insert(cur_idx, p)
    g_N += 1
    pass


def close_site(p):
    global g_N
    # TODO: 위치 p의 쉼터 폐쇄
    g_sites.remove(p)
    g_N -= 1
    pass



def next_site(x):
    # TODO: x 이상인 최소 쉼터 위치를 반환, 없으면 0
    cur_idx = bisect_left(g_sites, x)
    if cur_idx == g_N:
        return 0
    else:
        return g_sites[cur_idx]


def can_do1(area, k):
    # 간격 area 이상으로 k 곳 배치 가능?
    cur_idx = 0
    cur_pos = g_sites[cur_idx]

    nxt_idx = 1
    nxt_pos = g_sites[nxt_idx]

    cnt = 1

    while cnt < k:
        # area 보다 작은 공간에 있는거면 다음거보기.
        while nxt_pos - cur_pos < area:
            nxt_idx += 1
            # 아직 cnt 가 k 보다 작은데 g_N에 도달했으면 불가처리.
            # 다음 급수대를 찾지 못함.
            if nxt_idx >= g_N:
                return False
            nxt_pos = g_sites[nxt_idx]

        # nxt pos 가 cur pos 에서 area 이상 떨어짐.
        cnt += 1
        cur_idx = nxt_idx
        cur_pos = nxt_pos

    return True


def max_min_distance(k):
    # TODO: 정확히 k곳 선택 시 인접 간격의 최솟값을 최대화한 값.
    #       k가 현재 쉼터 수보다 크면 -1
    if g_N < k:
        return -1

    # area 설정.
    left = 1
    right = g_sites[-1] - g_sites[0]
    answer = -1
    while left <= right:
        center = (left + right) // 2

        if can_do1(center, k):
            answer = center
            # 더큰거 가능한지 확인
            left = center + 1
        else:
            right = center - 1

    return answer



def can_do2(area, k):
    # 그리디 방식
    cur_idx = 0
    cur_pos = g_sites[cur_idx]

    cnt = 1

    while cnt < k:
        nxt_point = cur_pos + area

        nxt_idx = bisect_right(g_sites, nxt_point) - 1
        if nxt_idx >= g_N - 1:
            return True

        cur_idx = nxt_idx
        cur_pos = g_sites[cur_idx]
        cnt += 1

    if cur_idx < g_N - 1:
        return False
    else:
        return True


def min_max_distance(k):
    # TODO: 최소·최대 위치를 반드시 포함해 정확히 k곳 선택 시
    #       인접 간격의 최댓값을 최소화한 값. k가 현재 쉼터 수보다 크면 -1
    if k > g_N:
        return -1

    left = 1
    right = g_sites[-1] - g_sites[0]
    answer = -1
    while left <= right:
        center = (left + right) // 2

        if can_do2(center, k):
            answer = center
            right = center - 1
        else:
            left = center + 1
    return answer

# ========= 이하 수정 비권장 (출력 형식 유지) =========
def main():
    out = []

    T = int(input())

    for tc in range(1, T + 1):
        n, M = map(int, input().split())
        sites = list(map(int, input().split()))

        init(n, sites)

        out.append('#%d' % tc)

        for _ in range(M):
            cmd = list(map(int, input().split()))
            op = cmd[0]

            if op == 1:
                p = cmd[1]
                add_site(p)

            elif op == 2:
                p = cmd[1]
                close_site(p)

            elif op == 3:
                k = cmd[1]
                out.append(str(max_min_distance(k)))

            elif op == 4:
                k = cmd[1]
                out.append(str(min_max_distance(k)))

            else:
                s = cmd[1]
                c = cmd[2]

                x = s
                total = 0

                for _ in range(c):
                    y = next_site(x)
                    total += y
                    x = (x + y) % 1000000000 + 1

                out.append(str(total))

    print('\n'.join(out))


main()
