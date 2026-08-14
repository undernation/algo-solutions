"""
SWEA 27172  태양광 발전 단지 관제 시스템 D6
https://swexpertacademy.com/main/code/userProblem/userProblemDetail.do?fromProbList=N&deleteYn=N&contestProbId=AZ-HaGAam0_HBITH&topPath=code&lastPath=problemDetail&secondPath=problem&menuBreakDown=swea.code.menu&menuBreakDown=swea.code.problem.menu&menuDesc=swea.code.desc&menuDesc=swea.code.problem.desc&contextPath=%2Fmain&locale=ko-kr%2Cko%3Bq%3D0.9%2Cen-us%3Bq%3D0.8%2Cen%3Bq%3D0.7&serverName=localhost&localeLanguage=ko_KR&localeLanguage2=Ko_KR&remoteAddr=175.213.163.17&scripts=%2Fjs%2Finit%2Fjquery-debug.js&scripts=%2Fjs%2Finit%2Fjquery-ui.js&scripts=%2Fjs%2Finit%2Fjquery.validate.js&scripts=%2Fjs%2Fcommon.js&NOTICE_NEW_COUNT=0&ssoLogin=false&hasSDPAdminLinkAuth=false&systemAdmin=false&backendAdmin=false&isTechBlogManager=false&CURRENT_MENU_AUTHORIZATION=READ&CURRENT_MENU_AUTHORIZATION=UPDATE&CURRENT_MENU_AUTHORIZATION=EXECUTE&CURRENT_MENU_AUTHORIZATION=DOWNLOAD&logoMainfileName=logo_company.png

풀이일 : 2026-08-14   결과: 시간초과
한도   : time 12개 테스트케이스를 합쳐서 C/C++의 경우 2초 / Java의 경우 6초 / memory 힙, 정적 메모리 합쳐서 256MB 이내, 스택 메모리 1MB 이내 / time_sec 2
난이도 : ?  |  정답률 25.00%

[문제]
한 태양광 발전 단지는 N×N개의 정사각형 지점(cell) 격자로 이루어져 있으며, 각 지점에는 태양광 패널이 하나씩 설치되어 그 현재 발전량이 값으로 기록되어 있다.

관제 센터는 관리 편의를 위해 전체 단지를 한 변의 길이가 K인 정사각형 구역(sector)들로 분할하여 운영한다. N은 항상 K로 나누어떨어짐이 보장되므로, 전체 단지는 정확히 (N/K)×(N/K)개의 구역으로 나뉜다.

당신은 관제 시스템에 들어오는 4종류의 명령을 순서대로 처리하는 프로그램을 작성해야 한다.

[좌표계]

지점은 두 정수 x, y로 표현한다. x는 열(column) 번호, y는 행(row) 번호이며, 좌측 상단 지점이 (x=0, y=0)이다. x는 오른쪽으로, y는 아래쪽으로 증가한다. (0 ≤ x, y < N)

초기 값 배열에서 i번째 줄의 j번째 값은 y=i(행), x=j(열) 지점의 초기 발전량이다.

[범위(직사각형)의 표현]

두 지점 A(x1, y1)(좌측 상단), B(x2, y2)(우측 하단)가 주어지면, 범위는 x1 ≤ x ≤ x2, y1 ≤ y ≤ y2를 만족하는 모든 지점의 집합이다.

구역 정렬 보장 — 범위를 사용하는 명령(3, 4)에 주어지는 범위는 항상 구역 단위이다. 즉 x1, y1은 K로 나누어떨어지고, x2, y2는 K로 나눈 나머지가 K−1이 됨이 보장된다. 따라서 범위에 일부만 걸치는 구역은 존재하지 않으며, 범위에 속한 구역의 모든 지점은 범위에 포함된다.

[상위 발전량의 우선순위 기준]

명령 4(query)에서 지점들은 다음 기준으로 정렬되며, 앞에 있을수록 우선순위가 높다.

  1) 지점의 발전량이 큰 순서 (내림차순)
  2) 발전량이 같다면 x좌표가 작은 순서 (오름차순)
  3) x좌표도 같다면 y좌표가 작은 순서 (오름차순)

[처리해야 할 명령]

각 테스트 케이스는 초기 격자와 M개의 명령으로 구성된다. 명령은 다음 4종류이다.

명령형식동작출력
1 (set)1 x y value지점 (x, y)의 값을 value로 설정(덮어쓰기)없음
2 (get)2 x y지점 (x, y)의 현재 값을 조회값을 한 줄에 출력
3 (update)3 x1 y1 x2 y2 num범위의 모든 지점의 값을 num만큼 증가없음
4 (query)4 x1 y1 x2 y2 count범위에서 우선순위가 높은 순서대로 상위 count개 지점의 좌표를 찾아 출력x y x y … (2×count개 정수)를 한 줄에 출력

[예시] N=6, K=2이고 초기 값이 1~36인 경우를 보자. 전체 단지는 3×3 = 9개의 구역으로 나뉜다(색은 구역 구분용, 굵은 선은 구역 경계).

[[IMG:1]]

① 명령 1 0 0 19 — 지점 (0, 0)의 값을 19로 설정한다.

[[IMG:2]]

② 명령 2 0 0 — 지점 (0, 0)의 현재 값 19를 한 줄에 출력한다.

③ 명령 3 0 0 1 3 5 — x∈[0, 1], y∈[0, 3] 범위(좌측의 세로로 이어진 두 구역)의 모든 지점이 5씩 증가한다.

[[IMG:3]]

④ 명령 4 0 0 1 3 2 — 같은 범위에서 상위 2개 지점을 찾는다. 범위 내 최댓값 25는 (x=1, y=3)에 있으므로 1순위. 다음 값 24는 (0, 0)과 (0, 3) 두 곳에 있는데, 값과 x좌표(0)가 같으므로 y좌표가 작은 (0, 0)이 2순위이다. 따라서 1 3 0 0을 한 줄에 출력한다.

[[IMG:4]]

[제공되는 뼈대 코드 — 커맨드 패턴]

아래에 언어별 뼈대 코드가 제공된다. main 함수는 입력 파싱과 명령 분기(커맨드 패턴), 출력을 모두 처리하며, 당신은 5개 함수 — init, set, get, update, query — 만 구현하면 된다. 필요한 전역 변수, 보조 함수, 클래스는 자유롭게 추가해도 된다. (Python 뼈대는 내장 함수와의 이름 충돌을 피하기 위해 set_value / get_value 이름을 사용한다)

뼈대 전체를 복사해 함수 구현을 채워 제출하라. 함수의 원형(시그니처)은 변경하지 말고, main과 입출력 부분은 수정하지 않는 것을 권장한다. main을 수정하더라도 입출력 형식만 일치하면 정답으로 처리되지만, 최종 출력 형식은 반드시 유지해야 한다.

[C]

#include <stdio.h>

#define MAX_N 500

typedef struct {
    int x, y;   /* x: 열(column), y: 행(row) */
} Point;

/*=========================================================
  여기서부터 5개 함수만 구현하시오.
  main 및 입출력 부분은 수정하지 않는 것을 권장한다.
=========================================================*/

void init(int N, int K, int graph[][MAX_N])
{
    /* TODO: 각 테스트 케이스 시작 시 1회 호출된다.
       전역 자료 구조를 반드시 초기화할 것. */
}

void set(Point p, int value)
{
    /* TODO: 지점 p의 값을 value로 설정(덮어쓰기) */
}

int get(Point p)
{
    /* TODO: 지점 p의 현재 값을 반환 */
    return 0;
}

void update(Point A, Point B, int num)
{
    /* TODO: [A, B] 범위(구역 정렬 보장)의 모든 지점에 num을 더함 */
}

void query(Point A, Point B, int count, Point result[])
{
    /* TODO: 우선순위 상위 count개 지점의 좌표를
       result[0..count-1]에 순서대로 채움 */
}

/*========= 이하 수정 비권장 (출력 형식 유지) =========*/
static int in_graph[MAX_N][MAX_N];
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
        int N, K, M, i, j;
        N = read_int(); K = read_int(); M = read_int();
        for (i = 0; i < N; i++)
            for (j = 0; j < N; j++)
                in_graph[i][j] = read_int();
        init(N, K, in_graph);
        printf("#%d\n", tc);
        while (M--) {
            int op = read_int();
            if (op == 1) {
                Point p; int v;
                p.x = read_int(); p.y = read_int(); v = read_int();
                set(p, v);
            } else if (op == 2) {
                Point p;
                p.x = read_int(); p.y = read_int();
                printf("%d\n", get(p));
            } else if (op == 3) {
                Point a, b; int w;
                a.x = read_int(); a.y = read_int();
                b.x = read_int(); b.y = read_int(); w = read_int();
                update(a, b, w);
            } else {
                Point a, b, res[5] = {{0,0},{0,0},{0,0},{0,0},{0,0}};
                int c;
                a.x = read_int(); a.y = read_int();
                b.x = read_int(); b.y = read_int(); c = read_int();
                query(a, b, c, res);
                for (i = 0; i < c; i++)
                    printf(i ? " %d %d" : "%d %d", res[i].x, res[i].y);
                printf("\n");
            }
        }
    }
    return 0;
}

[C++]

#include <cstdio>
/* 필요한 STL 헤더는 자유롭게 추가해도 된다.
   단, 아래 전역 함수 set과 std::set의 이름 충돌을 피하기 위해
   using namespace std; 는 쓰지 말고 std:: 접두사를 사용할 것. */

#define MAX_N 500

struct Point {
    int x, y;   // x: 열(column), y: 행(row)
};

/*=========================================================
  여기서부터 5개 함수만 구현하시오.
  main 및 입출력 부분은 수정하지 않는 것을 권장한다.
=========================================================*/

void init(int N, int K, int graph[][MAX_N])
{
    // TODO: 각 테스트 케이스 시작 시 1회 호출된다.
    //       전역 자료 구조를 반드시 초기화할 것.
}

void set(Point p, int value)
{
    // TODO: 지점 p의 값을 value로 설정(덮어쓰기)
}

int get(Point p)
{
    // TODO: 지점 p의 현재 값을 반환
    return 0;
}

void update(Point A, Point B, int num)
{
    // TODO: [A, B] 범위(구역 정렬 보장)의 모든 지점에 num을 더함
}

void query(Point A, Point B, int count, Point result[])
{
    // TODO: 우선순위 상위 count개 지점의 좌표를
    //       result[0..count-1]에 순서대로 채움
}

/*========= 이하 수정 비권장 (출력 형식 유지) =========*/
static int in_graph[MAX_N][MAX_N];
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
        int N, K, M, i, j;
        N = read_int(); K = read_int(); M = read_int();
        for (i = 0; i < N; i++)
            for (j = 0; j < N; j++)
                in_graph[i][j] = read_int();
        init(N, K, in_graph);
        printf("#%d\n", tc);
        while (M--) {
            int op = read_int();
            if (op == 1) {
                Point p; int v;
                p.x = read_int(); p.y = read_int(); v = read_int();
                set(p, v);
            } else if (op == 2) {
                Point p;
                p.x = read_int(); p.y = read_int();
                printf("%d\n", get(p));
            } else if (op == 3) {
                Point a, b; int w;
                a.x = read_int(); a.y = read_int();
                b.x = read_int(); b.y = read_int(); w = read_int();
                update(a, b, w);
            } else {
                Point a, b, res[5] = {{0,0},{0,0},{0,0},{0,0},{0,0}};
                int c;
                a.x = read_int(); a.y = read_int();
                b.x = read_int(); b.y = read_int(); c = read_int();
                query(a, b, c, res);
                for (i = 0; i < c; i++)
                    printf(i ? " %d %d" : "%d %d", res[i].x, res[i].y);
                printf("\n");
            }
        }
    }
    return 0;
}

[Java]

import java.io.*;

public class Solution {

    static class Point {
        int x, y;                     // x: 열(column), y: 행(row)
        Point() {}
        Point(int x, int y) { this.x = x; this.y = y; }
    }

    /*=========================================================
      여기서부터 5개 메서드만 구현하시오.
      main 및 입출력 부분은 수정하지 않는 것을 권장한다.
    =========================================================*/

    static void init(int N, int K, int[][] graph) {
        // TODO: 각 테스트 케이스 시작 시 1회 호출된다.
        //       전역 자료 구조를 반드시 초기화할 것.
    }

    static void set(Point p, int value) {
        // TODO: 지점 p의 값을 value로 설정(덮어쓰기)
    }

    static int get(Point p) {
        // TODO: 지점 p의 현재 값을 반환
        return 0;
    }

    static void update(Point A, Point B, int num) {
        // TODO: [A, B] 범위(구역 정렬 보장)의 모든 지점에 num을 더함
    }

    static void query(Point A, Point B, int count, Point[] result) {
        // TODO: 우선순위 상위 count개 지점의 좌표를
        //       result[0..count-1]에 순서대로 채움 (각 원소를 덮어쓸 것)
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
            in.nextToken(); int K = (int) in.nval;
            in.nextToken(); int M = (int) in.nval;
            int[][] graph = new int[N][N];
            for (int i = 0; i < N; i++)
                for (int j = 0; j < N; j++) {
                    in.nextToken();
                    graph[i][j] = (int) in.nval;
                }
            init(N, K, graph);
            sb.append('#').append(tc).append('\n');
            for (int q = 0; q < M; q++) {
                in.nextToken(); int op = (int) in.nval;
                if (op == 1) {
                    in.nextToken(); int x = (int) in.nval;
                    in.nextToken(); int y = (int) in.nval;
                    in.nextToken(); int v = (int) in.nval;
                    set(new Point(x, y), v);
                } else if (op == 2) {
                    in.nextToken(); int x = (int) in.nval;
                    in.nextToken(); int y = (int) in.nval;
                    sb.append(get(new Point(x, y))).append('\n');
                } else if (op == 3) {
                    in.nextToken(); int x1 = (int) in.nval;
                    in.nextToken(); int y1 = (int) in.nval;
                    in.nextToken(); int x2 = (int) in.nval;
                    in.nextToken(); int y2 = (int) in.nval;
                    in.nextToken(); int w = (int) in.nval;
                    update(new Point(x1, y1), new Point(x2, y2), w);
                } else {
                    in.nextToken(); int x1 = (int) in.nval;
                    in.nextToken(); int y1 = (int) in.nval;
                    in.nextToken(); int x2 = (int) in.nval;
                    in.nextToken(); int y2 = (int) in.nval;
                    in.nextToken(); int c = (int) in.nval;
                    Point[] res = new Point[5];
                    for (int i = 0; i < 5; i++) res[i] = new Point(0, 0);
                    query(new Point(x1, y1), new Point(x2, y2), c, res);
                    for (int i = 0; i < c; i++) {
                        if (i > 0) sb.append(' ');
                        sb.append(res[i].x).append(' ').append(res[i].y);
                    }
                    sb.append('\n');
                }
            }
        }
        System.out.print(sb);
    }
}

[Python]

import sys

class Point:
    __slots__ = ('x', 'y')          # x: 열(column), y: 행(row)

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

# =========================================================
#  여기서부터 5개 함수만 구현하시오.
#  (내장 함수 set과의 충돌을 피하기 위해 Python 뼈대에서는
#   set_value / get_value 라는 이름을 사용한다)
#  main 및 입출력 부분은 수정하지 않는 것을 권장한다.
# =========================================================

def init(N, K, graph):
    # TODO: 각 테스트 케이스 시작 시 1회 호출된다.
    #       전역 자료 구조를 반드시 초기화할 것.
    pass

def set_value(p, value):
    # TODO: 지점 p의 값을 value로 설정(덮어쓰기)
    pass

def get_value(p):
    # TODO: 지점 p의 현재 값을 반환
    return 0

def update(A, B, num):
    # TODO: [A, B] 범위(구역 정렬 보장)의 모든 지점에 num을 더함
    pass

def query(A, B, count, result):
    # TODO: 우선순위 상위 count개 지점의 좌표를
    #       result[0..count-1]에 채움 (result[i]의 x, y를 덮어쓸 것)
    pass

# ========= 이하 수정 비권장 (출력 형식 유지) =========
def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    out = []
    T = int(next(it))
    for tc in range(1, T + 1):
        N = int(next(it)); K = int(next(it)); M = int(next(it))
        graph = [[int(next(it)) for _ in range(N)] for _ in range(N)]
        init(N, K, graph)
        out.append('#%d' % tc)
        for _ in range(M):
            op = int(next(it))
            if op == 1:
                x = int(next(it)); y = int(next(it)); v = int(next(it))
                set_value(Point(x, y), v)
            elif op == 2:
                x = int(next(it)); y = int(next(it))
                out.append(str(get_value(Point(x, y))))
            elif op == 3:
                x1 = int(next(it)); y1 = int(next(it))
                x2 = int(next(it)); y2 = int(next(it)); w = int(next(it))
                update(Point(x1, y1), Point(x2, y2), w)
            else:
                x1 = int(next(it)); y1 = int(next(it))
                x2 = int(next(it)); y2 = int(next(it)); c = int(next(it))
                res = [Point() for _ in range(c)]
                query(Point(x1, y1), Point(x2, y2), c, res)
                out.append(' '.join('%d %d' % (p.x, p.y) for p in res))
    sys.stdout.write('\n'.join(out) + '\n')

main()

[제약 사항]

항목범위 / 조건
테스트 케이스 수 T1 ≤ T ≤ 12, 이 중 N > 100인 테스트 케이스는 최대 5개
단지의 크기 N2 ≤ N ≤ 500, N은 K의 배수
구역의 한 변 K2 ≤ K ≤ 50, N/K ≤ 20 (구역은 최대 20×20 = 400개)
지점의 초기 값 / set의 value1 ≤ 값 ≤ 100,000
update의 num1 ≤ num ≤ 1,000
query의 count1 ≤ count ≤ 5, 범위 내 지점 수 ≥ count 보장
값의 범위모든 시점에서 모든 지점의 값은 항상 1억 이하이다 (int 범위 내 보장)
좌표 유효성모든 좌표는 0 ≤ x, y < N. 명령 3, 4의 범위는 구역 경계에 정렬됨 (x1, y1 ≡ 0, x2, y2 ≡ K−1 (mod K)), x1 ≤ x2, y1 ≤ y2
명령 수 (테스트 케이스당)M ≤ 30,000 — set ≤ 5,000 / get ≤ 5,000 / update ≤ 20,000 / query ≤ 3,000
명령 수 (입력 파일 전체 합)set ≤ 15,000 / get ≤ 15,000 / update ≤ 80,000 / query ≤ 17,000

[유의 사항]

· 제한 시간은 입력 파일 전체(모든 테스트 케이스)를 처리하는 기준이다.
· 시간 복잡도에 주의. 매 query마다 범위 내 모든 지점(최대 250,000개)을 순회하거나, 매 update마다 범위 내 모든 지점을 하나씩 갱신하는 단순한 방법으로는 통과할 수 없도록 채점 데이터가 구성되어 있다. 구역(최대 400개) 단위의 자료 구조 설계가 필요하다.
· 각 테스트 케이스는 독립적이다. 이전 테스트 케이스의 상태가 남지 않도록 init에서 모든 전역 자료 구조를 초기화하라.
· 표준 라이브러리(STL, java.util 등)는 사용할 수 있다.
· C/C++ 뼈대는 입력 전체를 한 번에 읽으므로, 로컬에서 테스트할 때는 키보드 입력 대신 파일 리다이렉션(예: prog.exe < input.txt)을 사용하라.
· 주어진 예시를 통과하더라도 채점에는 공개되지 않은 테스트 케이스가 포함되므로, 제약 최대 규모에서 시간 내에 동작하는지 반드시 확인하라.

[예제 1]
입력:
2
6 2 4
1 2 3 4 5 6
7 8 9 10 11 12
13 14 15 16 17 18
19 20 21 22 23 24
25 26 27 28 29 30
31 32 33 34 35 36
1 0 0 19
2 0 0
3 0 0 1 3 5
4 0 0 1 3 2
4 2 7
5 5 3 1
5 5 1 2
2 2 9 9
2 2 9 9
4 0 0 3 3 5
3 2 0 3 3 4
2 3 1
4 0 0 3 3 3
1 3 1 6
2 3 1
2 0 0
출력:
#1
19
1 3 0 0
#2
2 2 2 3 3 2 3 3 0 0
6
2 2 2 3 3 2
6
5
"""

import heapq


class Point:
    __slots__ = ('x', 'y')          # x: 열(column), y: 행(row)

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


# =========================================================
#  여기서부터 5개 함수만 구현하시오.
#  (내장 함수 set과의 충돌을 피하기 위해 Python 뼈대에서는
#   set_value / get_value 라는 이름을 사용한다)
#  main 및 입출력 부분은 수정하지 않는 것을 권장한다.
# =========================================================


def init(N, K, graph):
    # TODO: 각 테스트 케이스 시작 시 1회 호출된다.
    #       전역 자료 구조를 반드시 초기화할 것.
    global board, g_N, hqs, lazy, ver, area, g_K

    board = [row[:] for row in graph]
    g_N = N
    g_K = K
    area = N // K
    lazy = [[0] * area for _ in range(area)]
    hqs = [[] for _ in range(area * area)]
    ver = [[0] * N for _ in range(N)]

    def check_area(i, j):
        row = i // g_K
        col = j // g_K

        return row * area + col

    for i in range(N):
        for j in range(N):
            cur_area = check_area(i, j)
            cur_val = board[i][j]
            heapq.heappush(hqs[cur_area], [-cur_val, j, i, 0])


def set_value(p, value):
    # TODO: 지점 p의 값을 value로 설정(덮어쓰기)
    # 업데이트,
    cy = p.y
    cx = p.x
    board[cy][cx] = value - lazy[cy // g_K][cx // g_K]

    def check_area(i, j):
        row = i // g_K
        col = j // g_K

        return row * area + col

    cur_area = check_area(cy, cx)
    cur_ver = ver[cy][cx]
    heapq.heappush(hqs[cur_area], [-value, cx, cy, cur_ver + 1])
    ver[cy][cx] += 1

    pass

def get_value(p):
    # TODO: 지점 p의 현재 값을 반환
    cy = p.y
    cx = p.x
    # print()
    # for i in board:
    #     print(i)
    # print("lazy")
    # for i in lazy:
    #     print(i)
    return board[cy][cx] + lazy[cy // g_K][cx // g_K]

def update(A, B, num):
    # TODO: [A, B] 범위(구역 정렬 보장)의 모든 지점에 num을 더함
    x1 = A.x
    y1 = A.y
    # A 가 속한 구역의 시작지점 체크해야함.
    x2 = B.x
    y2 = B.y
    
    # x1 부터 x2 까지 area 만큼 옮겨가면서 넣기
    #
    for x in range(x1, x2, g_K):
        for y in range(y1, y2, g_K):
            lazy[y // g_K][x // g_K] += num
    #         print("x, y", x, y)
    # for i in lazy:
    #     print(i)


def query(A, B, count, result):
    # TODO: 우선순위 상위 count개 지점의 좌표를
    #       result[0..count-1]에 채움 (result[i]의 x, y를 덮어쓸 것)
    x1 = A.x
    y1 = A.y

    x2 = B.x
    y2 = B.y
    hq = []
    def check_area(i, j):
        row = i // g_K
        col = j // g_K

        return row * area + col
    cand = []
    cand2 = []
    for x in range(x1, x2, g_K):
        for y in range(y1, y2, g_K):
            cand.append([y, x])
            cand2.append(check_area(y, x))
    cnt = 0
    pop_list = []
    for c in cand2:
        while hqs[c]:
            value, cx, cy, version = heapq.heappop(hqs[c])
            if ver[cy][cx] == version:
                break
        
        pop_list.append([value, cy, cx, version, c])
        heapq.heappush(hq, [value - lazy[cy // g_K][cx // g_K], cx, cy, c])

    while cnt < count:
        
        value, cx, cy, c = heapq.heappop(hq)
        # print("cnt value, cx, cy, c", cnt, value, cx, cy, c)
        while hqs[c]:
            value, nx, ny, version = heapq.heappop(hqs[c])
            if ver[ny][nx] == version:
                heapq.heappush(hq, [value - lazy[ny // g_K][nx // g_K], nx, ny, c])
                pop_list.append([value, ny, nx, version, c])
                break
        # print(value)
        result[cnt].x = cx
        result[cnt].y = cy

        cnt += 1

    for value, cy, cx, version, c in pop_list:
        heapq.heappush(hqs[c], [value, cx, cy, version])



# ========= 이하 수정 비권장 (출력 형식 유지) =========

def main():
    out = []

    T = int(input())
    for tc in range(1, T + 1):
        N, K, M = map(int, input().split())
        graph = [list(map(int, input().split())) for _ in range(N)]

        init(N, K, graph)
        out.append('#%d' % tc)

        for _ in range(M):
            cmd = list(map(int, input().split()))
            op = cmd[0]

            if op == 1:
                _, x, y, v = cmd
                set_value(Point(x, y), v)

            elif op == 2:
                _, x, y = cmd
                out.append(str(get_value(Point(x, y))))

            elif op == 3:
                _, x1, y1, x2, y2, w = cmd
                update(Point(x1, y1), Point(x2, y2), w)

            else:
                _, x1, y1, x2, y2, c = cmd
                res = [Point() for _ in range(c)]
                query(Point(x1, y1), Point(x2, y2), c, res)
                out.append(' '.join('%d %d' % (p.x, p.y) for p in res))

    print('\n'.join(out))


main()
