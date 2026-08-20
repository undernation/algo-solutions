# algo-solutions

코딩테스트 풀이 아카이브 — 개인 학습용

# 👉 [**대시보드 열기 — undernation.github.io/algo-solutions**](https://undernation.github.io/algo-solutions/)

> 잔디 · 문제 · 제출 현황 · **문제 보기 / 코드 채점 / 저장** 전부 여기서 된다.
> 문제 제목을 클릭하면 지문·예제·제출 이력이 열리고, 그 자리에서 코드를 채점하고 커밋할 수 있다.

| 어디서 | 주소 |
|---|---|
| 🌐 **대시보드** | **https://undernation.github.io/algo-solutions/** |
| 🖥️ 허브 서버 (클라우드) | 대시보드가 [`_meta/endpoint.json`](_meta/endpoint.json) 을 읽어 **자동 연결** |
| 💻 허브 서버 (로컬) | `python judge/server.py` → `http://localhost:12014` |

**처음 한 번만**: 대시보드 상단 **[설정]** → 인증 토큰 입력 (서버 시작 로그 또는 `~/.algo-hub-token`).
이후 브라우저에 저장되어 자동 연결된다.

---

## 📁 구조

```
boj/  swea/        제출한 풀이 코드      <번호>_<제목>.py
problems/          문제 자료 (지문·예제·이미지·히든TC 일부)
notes/             복기 메모 (마크다운)
judge/server.py    허브 서버 — 채점·저장·크롤링·메모
_meta/             도구 · 색인 · 대시보드 템플릿
```

---

## 🛠 사용법

### 매일 쓰는 것 — 브라우저만 있으면 됨

[대시보드](https://undernation.github.io/algo-solutions/)에서 문제 열고 → 코드 붙여넣고 → **채점** → **저장 & 커밋**.
처음 한 번만 우측 상단 허브 버튼에서 토큰을 넣으면 된다. 채점·저장은 **클라우드 허브**가 하므로 PC를 켜둘 필요가 없다.

### 새 문제를 추가할 때 (내 PC에서)

로그인 세션이 필요해 이때만 로컬에서 돌린다.

```bash
python _meta/debug_chrome.py      # 로그인용 크롬(9222) — 뜨면 코딩살구·SWEA 로그인
python _meta/crawl_all.py         # 지문·예제·이미지
python _meta/crawl_all.py --htc   # 히든 테스트케이스
python _meta/sync_tc.py           # 전체 TC 를 채점 서버로
python _meta/build_probindex.py && python _meta/build_heatmap.py
python _meta/selfcheck.py         # 이상 없나 점검
```

> 대시보드의 **+ 새 문제** 버튼에 URL 만 붙여넣어도 된다 (로컬 허브가 켜져 있을 때).

### 새 PC 세팅

```bash
gh auth login && gh auth setup-git
git clone https://github.com/undernation/algo-solutions.git && cd algo-solutions
python _meta/install_hooks.py     # 훅 + 커밋 이메일 + merge 드라이버
pip install playwright && playwright install chromium   # 크롤링을 할 경우만
```

### 주요 스크립트

| 파일 | 하는 일 |
|---|---|
| `_meta/debug_chrome.py` | 크롤링용 디버그 크롬 실행 (`--check` 로 확인만) |
| `_meta/crawl_all.py` | 문제 수집 `--htc --empty --bad --force --site --limit` |
| `_meta/fetch_problem.py` | URL/번호 하나로 단건 크롤링 |
| `_meta/sync_tc.py` | 전체 테스트케이스를 채점 서버로 업로드 |
| `_meta/build_heatmap.py` | 잔디 + 대시보드 생성 |
| `_meta/selfcheck.py` | 저장소 자체 점검 |
| `judge/server.py` | 허브 서버 (`--runner`, `--no-push`, `--port`) |

> 테스트케이스는 **repo(200KB 보기용)** 와 **채점 서버(전체)** 로 나뉜다.
> 큰 것은 문제 페이지에서 필요할 때만 받아온다. 자세한 건 [CLAUDE.md](CLAUDE.md).

---

## 📄 파일 형식

```python
"""
SWEA 4012  [모의 SW 역량테스트] 요리사
https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=...

풀이일 : 2026-08-09   결과: 품 (자력, 1회차)
난이도 : Master  |  정답률 82.23%  |  Point 200
한도   : Python 10초 (50 TC 합산) / 256MB
제약   : 4 ≤ N ≤ 16 (짝수), 1 ≤ Sij ≤ 20,000

분류   : 조합(N/2 분할) + 완전탐색
관련   : 4013 특이한 자석, 4123 숫자 만들기

[문제]
...

[검증]
독립 브루트포스 N건 0불일치 / 최악 X초

[메모]
실수노트 기록 이식
"""

# 제출 코드
```

---

## 🔗 연동

- **실수노트(SSOT)**: `ObsidianVaults/동기화/_cpp_코테/실수모음 (몰랐으면 답보고 혼자 다시 짜기).md`
- **복기 큐**: `C:/Users/solom/review_queue.py`
- 이 repo는 **코드 저장 전용 (append-only)** — 날짜·상태의 진실 소스는 여전히 실수노트

---

## 🛠️ 사용법

```bash
# 디버그 크롬 (SWEA 로그인 상태)
python C:/Users/solom/crawler.py chrome

# 문제 메타 조회
python _meta/fetch_swea.py <contestProbId>
python _meta/fetch_swea.py <contestProbId> --json
```

---

## 📊 현황

| | |
|---|---|
| 총 풀이 | 34 |
| BOJ | 17 |
| SWEA | 17 |

<!-- INDEX_START -->
| 사이트 | 번호 | 제목 | 결과 | 풀이일 | 분류 |
|---|---|---|---|---|---|
| SWEA | [24995](swea/24995_온라인마트.py) | 온라인마트 | 품 | 2026-08-20 |  |
| SWEA | [24703](swea/24703_어항물채우기정답.py) | 어항물채우기 정답 | 시간초과 | 2026-08-19 |  |
| SWEA | [27185](swea/27185_등산로급수대운영시스템D6.py) | 등산로 급수대 운영 시스템 D6 | 못품 | 2026-08-18 |  |
| BOJ | [17143](boj/17143.py) | 낚시왕 | 품 | 2026-08-18 |  |
| SWEA | [27183](swea/27183_고속선선로피로도관제시스템D6.py) | 고속선 선로 피로도 관제 시스템 D6 | 못품 | 2026-08-17 |  |
| BOJ | [17070](boj/17070.py) | 파이프 옮기기 1 | 못품 | 2026-08-17 |  |
| BOJ | [15662](boj/15662.py) | 톱니바퀴 (2) | 품 | 2026-08-17 |  |
| BOJ | [9086](boj/9086.py) | 풀이일 : 2026-08-16   결과: 품 | 품 | 2026-08-16 |  |
| BOJ | [2941](boj/2941.py) | 크로아티아 알파벳 | 품 | 2026-08-16 |  |
| SWEA | [27181](swea/27181_공항활주로관제시스템D6.py) | 공항 활주로 관제 시스템 D6 | 품 | 2026-08-16 |  |
| BOJ | [2566](boj/2566.py) | 풀이일 : 2026-08-16   결과: 품 | 품 | 2026-08-16 |  |
| BOJ | [2559](boj/2559.py) | 수열 | 틀림 | 2026-08-16 |  |
| BOJ | [1912](boj/1912.py) | 연속합 | 못품 | 2026-08-16 |  |
| BOJ | [17140](boj/17140.py) | 이차원 배열과 연산 | 품 | 2026-08-16 |  |
| BOJ | [20057](boj/20057.py) | 마법사 상어와 토네이도 | 품 | 2026-08-15 |  |
| BOJ | [1100](boj/1100.py) | 하얀 칸 | 품 | 2026-08-15 |  |
| SWEA | [27172](swea/27172_태양광발전단지관제시스템D6.py) | 태양광 발전 단지 관제 시스템 D6 | 시간초과 | 2026-08-14 |  |
| SWEA | [1873](swea/1873_상호의배틀필드D3.py) | 상호의 배틀필드 D3 | 품 | 2026-08-14 |  |
| SWEA | [1248](swea/1248_[S_W문제해결응용]3일차-공통조상D5.py) | [S/W 문제해결 응용] 3일차 - 공통조상 D5 | 품 | 2026-08-14 |  |
| SWEA | [1247](swea/1247_[S_W문제해결응용]3일차-최적경로D5.py) | [S/W 문제해결 응용] 3일차 - 최적 경로 D5 | 품 | 2026-08-14 |  |
| SWEA | [10726](swea/10726_이진수표현D3.py) | 이진수 표현 D3 | 품 | 2026-08-14 |  |
| SWEA | [2105](swea/2105_[모의SW역량테스트]디저트카페.py) | [모의 SW 역량테스트] 디저트 카페 | 품 | 2026-08-13 |  |
| SWEA | [1953](swea/1953_[모의SW역량테스트]탈주범검거.py) | [모의 SW 역량테스트] 탈주범 검거 | 품 | 2026-08-13 |  |
| SWEA | [1952](swea/1952_[모의SW역량테스트]수영장.py) | [모의 SW 역량테스트] 수영장 | 품 | 2026-08-13 |  |
| SWEA | [1949](swea/1949_[모의SW역량테스트]등산로조성.py) | [모의 SW 역량테스트] 등산로 조성 | 품 | 2026-08-13 |  |
| SWEA | [1288](swea/1288_새로운불면증치료법D2.py) | 새로운 불면증 치료법 D2 | 품 | 2026-08-13 |  |
| SWEA | [2115](swea/2115_[모의SW역량테스트]벌꿀채취.py) | [모의 SW 역량테스트] 벌꿀채취 | 품 | 2026-08-12 |  |
| SWEA | [2112](swea/2112_[모의SW역량테스트]보호필름.py) | [모의 SW 역량테스트] 보호 필름 | 품 | 2026-08-12 |  |
| BOJ | [15686](boj/15686.py) | 치킨 배달 | 품 | 2026-08-12 |  |
| BOJ | [11655](boj/11655.py) | ROT13 | 품 | 2026-08-12 |  |
| BOJ | [1159](boj/1159.py) | 농구 경기 | 품 | 2026-08-12 |  |
| BOJ | [10822](boj/10822.py) | 더하기 | 품 | 2026-08-12 |  |
| BOJ | [10809](boj/10809.py) | 알파벳 찾기 | 품 | 2026-08-12 |  |
| BOJ | [14891](boj/14891.py) | 톱니바퀴 | 품 | 2026-08-08 |  |
<!-- INDEX_END -->
