# CLAUDE.md — 이 repo 작업 지침

> **이 파일을 읽는 AI 에이전트에게:** 아래는 이 저장소의 운영 규칙이다.
> 사용자가 "문제 풀었어 + 코드"를 주면 **이 순서 그대로** 처리한다.
> 이전 대화 맥락이 없어도 이 문서만으로 동일하게 동작해야 한다.

---

## 0. 이 repo는 무엇인가

**코딩테스트 풀이 아카이브** (BOJ / SWEA). 사용자가 푼 코드를 문제 단위로 보관한다.

| | |
|---|---|
| 소유자 | `undernation` (gmlcjf287@gmail.com) |
| 공개범위 | ⚠️ **현재 PUBLIC** (GitHub Pages 사용 목적) |
| 원격 | `https://github.com/undernation/algo-solutions.git` (**HTTPS** — SSH 키 미설정) |
| Pages | https://undernation.github.io/algo-solutions/ (인터랙티브 잔디) |

## 지문·저작물 취급 규칙

> **소유자 결정 (2026-08-11): public 상태에서도 지문·예제를 그대로 커밋한다.**
> 에이전트는 이에 대해 다시 확인을 요구하거나 지문을 임의로 빼지 않는다.

| 항목 | 저장 |
|---|---|
| 본인이 작성한 **풀이 코드** | ✅ |
| 문제 **번호·제목·URL** | ✅ |
| **제약조건·시간/메모리 한도·정답률** | ✅ |
| **문제 지문 전문 · 예제 입출력** | ✅ (소유자 결정) |
| **비공개 테스트케이스** | ✅ (크롤링되면 그대로) |

- 구현 위치: `judge/server.py` 의 **`PUBLIC_SAFE = False`** (기본값).
  나중에 지문을 빼고 싶으면 **이 값만 `True`** 로 바꾸면 `build_header`와 `problems/*.json` 양쪽에서 자동 제거된다.
- 참고로만 남겨둔 사실: SWEA 문제 페이지에는 *"※ SW Expert 아카데미의 문제를 무단 복제하는 것을 금지합니다."* 고지가 있고,
  SSAFY가 준 허용 조건은 *"private이면 보관 가능"* 이었다. **소유자가 위험을 인지한 상태에서 public 저장을 선택했다.**
- ⚠️ 한 번 public으로 push된 내용은 히스토리·포크·캐시에 남는다. 되돌리려면 히스토리 재작성이 필요하다.
- 비공개로 돌리려면:
  ```bash
  gh repo edit --visibility private --accept-visibility-change-consequences   # ※ 무료 계정은 Pages 중단
  ```

### ⚠️ 이 repo는 "진실의 소스"가 아니다

날짜·상태(품/못품/틀림)의 **단일 진실 소스(SSOT)는 옵시디언 실수노트**다.
이 repo는 **코드 저장 전용 append-only 싱크**다. 여기 있는 날짜와 실수노트가 다르면 **실수노트가 맞다.**

| 정보 | 진실의 소스 |
|---|---|
| 풀이 날짜 · 상태 · 회차 | **실수노트** (아래 경로) |
| 진단·복기 본문 | **실수노트 / 못푼 문제모음** |
| **제출 코드** | **이 repo** ← 여기서만 관리 |

---

## 0-2. 사이트 · 허브 구조 (2026-08-11 구축)

### 🌐 대시보드 — https://undernation.github.io/algo-solutions/

`index.html` (= `assets/heatmap.html`) 하나짜리 SPA. 해시 라우팅 4화면:

| 경로 | 화면 |
|---|---|
| `#home` | 통계 카드 + 잔디(호버 툴팁) + 최근 제출 |
| `#problems` | **폴더 트리** — 코딩살구 커리큘럼(주차별 8 / 개념별 8트랙) |
| `#status` | 제출 현황 표 (검색·필터·정렬) |
| `#p/<site>/<no>` | **문제 페이지** — 백준식 제한표·지문·예제 + 코드 에디터 + 채점/저장 |

### 🖥️ 허브 서버 2개 — 역할이 다르다

| | 어디 | 무엇 | 켜져 있나 |
|---|---|---|---|
| **CLOUD** | Oracle VM `134.185.106.155` | **채점 · 저장/커밋/푸시** | 항상 (systemd) |
| **LOCAL** | 내 PC `localhost:12014` | **문제 크롤링(/fetch)** | 내가 켤 때만 |

> 🔑 **왜 나눴나**: 코딩살구·SWEA·프로그래머스 모두 **로그인 세션**이 있어야 문제를 읽을 수 있다.
> (cosal API 는 비로그인 시 **401**, 페이지는 SPA.) 클라우드엔 브라우저도 세션도 없으므로 **크롤링은 원천적으로 불가**.
> 대신 **미리 크롤링해 `problems/*.json` 으로 커밋**해 두면, 이후엔 클라우드만으로 문제 보기·채점이 된다.

```
Oracle VM
├─ algo-hub.service       채점 + git commit/push       :12014 (localhost only)
├─ algo-tunnel.service    cloudflared quick tunnel     → https://xxx.trycloudflare.com
└─ algo-endpoint.timer    5분마다 터널 URL 을 _meta/endpoint.json 에 커밋
```

- 대시보드는 `_meta/endpoint.json` 을 읽어 **터널 URL 이 바뀌어도 자동 추적**한다.
- VM 은 **deploy key**(`~/.ssh/algo_deploy`, repo에 read-write 등록)로 push 한다.
- **인증**: 모든 POST 에 `X-Auth-Token` 필요. 토큰은 각 허브의 `~/.algo-hub-token`.
  브라우저는 우측 상단 허브 버튼에서 한 번 입력 → `localStorage` 저장.
- 🚩 **두 허브의 토큰은 반드시 같은 값이어야 한다.** 대시보드는 토큰을 하나만 저장하므로
  값이 다르면 한쪽(주로 크롤링용 로컬 허브)이 **401** 을 뱉는다. 새 PC 세팅 시:
  ```bash
  ssh -i ~/.ssh/oracle_judge ubuntu@134.185.106.155 'cat ~/.algo-hub-token' > ~/.algo-hub-token
  ```
- 서버 로그: `ssh ubuntu@134.185.106.155 'journalctl -u algo-hub -n 50'`
- SSH 키: `~/.ssh/oracle_judge` (= Downloads 의 `quality-search.key`)

### 📦 문제 자료 파이프라인

```
_meta/crawl_cosal_list.py   코딩살구 전체 목록  → _meta/cosal_list.json   (513문제, 주차·개념 섹션)
_meta/crawl_all.py          지문·예제 일괄 수집 → problems/<site>/<no>.json
_meta/build_probindex.py    색인 생성          → problems/index.json
_meta/build_heatmap.py      잔디 + 대시보드    → index.html
```

> Pages 는 디렉터리 목록을 안 주므로 **`problems/index.json` 색인이 반드시 있어야** 트리가 뜬다.
> 새로 크롤링했으면 `build_probindex.py` → `build_heatmap.py` 순서로 돌린다.

**선행조건**: 디버그 크롬 + 코딩살구 로그인
```bash
python C:/Users/solom/crawler.py chrome
python _meta/crawl_cosal_list.py     # 목록 (2~3분)
python _meta/crawl_all.py            # 지문 (문제당 ~4.5초)
python _meta/build_probindex.py && python _meta/build_heatmap.py
```

### ⚠️ SWEA 는 번호로 역검색이 안 된다

표시번호(2382) ≠ `contestProbId`(AWXR…). 목록 페이지도 JS 렌더라 자동 매핑 실패.
→ `_meta/swea_ids.json` 에 `{"2382": "AWXRQm6q…"}` 를 채워야 자동 크롤링 대상이 된다.
→ 없으면 대시보드에서 **문제 다시 가져오기** 클릭 시 URL 을 물어본다.

---

## 1. 환경 (PC마다 다를 수 있음)

### 경로 — 먼저 존재 확인부터

```
repo            : <이 파일이 있는 폴더>
옵시디언 볼트    : C:/Users/solom/ObsidianVaults/동기화
실수노트         : <볼트>/_cpp_코테/실수모음 (몰랐으면 답보고 혼자 다시 짜기).md
못푼 문제모음    : <볼트>/_cpp_코테/못푼 문제모음/
졸업 아카이브    : <볼트>/_cpp_코테/못푼 문제모음/_졸업 아카이브/
데일리          : <볼트>/_Daily/YYYY-MM-DD.md
복기 큐 스크립트 : C:/Users/solom/review_queue.py   ← 반드시 C:/Users/solom 에서 실행
```

> 📌 **다른 PC라 경로가 다르면**: 볼트를 못 찾겠다고 말하고 사용자에게 물어라. **추측해서 엉뚱한 곳에 쓰지 말 것.**
> 📌 볼트가 없는 PC라면 **repo 작업만** 수행하고, 실수노트/데일리 동기화는 **건너뛰고 그 사실을 보고**한다.

### 최초 1회 세팅 (새 PC)

```bash
gh auth login                          # 이미 되어 있으면 생략
gh auth setup-git                      # ★ HTTPS 인증 (SSH 키 없음)
gh auth refresh -s workflow -h github.com   # ★ .github/workflows 수정하려면 필수

git clone https://github.com/undernation/algo-solutions.git
cd algo-solutions
git config user.name  "undernation"
git config user.email "solomon2752@naver.com"   # ★ 계정에 연결된 이메일

python _meta/install_hooks.py          # ★ pre-commit 훅 (PC마다 1회)

# 문제 크롤링·로컬 채점을 쓰려면
pip install playwright && playwright install chromium
python C:/Users/solom/crawler.py chrome        # 디버그 크롬(9222) — 각 사이트 로그인
python judge/server.py                         # 로컬 허브 :12014 (시작 로그에 토큰 출력)
```

> 🚩 **커밋 이메일은 반드시 `solomon2752@naver.com`.** 이게 GitHub 계정 `undernation` 에
> 연결된 주소다. 다른 주소(예: gmlcjf287@gmail.com)로 커밋하면 GitHub 가 작성자를 못 알아봐
> **프로필 잔디에 하나도 안 찍힌다.** (2026-08-12 에 실제로 그랬다 — API 로 확인하려면:
> `gh api repos/undernation/algo-solutions/commits --jq '.[0].author.login'` 이 null 이면 미연결)

> 🚩 **SSH로 push하면 실패한다** (`Permission denied`). 반드시 **HTTPS + `gh auth setup-git`**.
> 🚩 **`.github/workflows/` 파일을 push하려면 토큰에 `workflow` 스코프가 필요하다.**
> 없으면 `refusing to allow an OAuth App to create or update workflow ... without workflow scope` 에러.
> `gh auth refresh -s workflow` 는 **브라우저 인증이 필요**하므로 사용자에게 요청해야 한다.
> (백그라운드로 실행해 일회용 코드를 읽어서 전달하면 편하다. 절대 짧은 timeout으로 끊지 말 것 — 코드가 죽는다.)

### 작업 시작 전 항상

```bash
git pull --rebase       # 다른 PC에서 올린 게 있을 수 있음
```

---

## 2. 파일 규약

```
boj/<번호>.py                  예: boj/2293.py
swea/<번호>_<제목>.py           예: swea/2382_미생물격리.py
```

- 제목은 **공백 제거**, 특수문자 `\ / : * ? " < > |` 제거
- 같은 문제를 다시 풀면 **파일을 덮어쓰고**, 헤더의 회차·날짜를 갱신한다 (파일을 새로 만들지 않는다)

### 파일 템플릿

```python
"""
SWEA 4012  [모의 SW 역량테스트] 요리사
https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AWIeUtVakTMDFAVH

풀이일 : 2026-08-09   결과: 품 (자력, 1회차)
난이도 : Master  |  정답률 82.23%  |  Point 200
한도   : Python 10초 (50 TC 합산) / 256MB
제약   : 4 ≤ N ≤ 16 (짝수), 1 ≤ Sij ≤ 20,000

분류   : 조합(N/2 분할) + 완전탐색
관련   : 4013 특이한 자석, 4123 숫자 만들기

[문제]
(SWEA 지문 — fetch_swea.py 의 statement)

[검증]
독립 브루트포스 3,000건 0불일치 / 최악 N=16 → 0.8초

[메모]
실수노트 기록: "..."
"""

# ── 제출 코드 ──
def solution(...):
    ...
```

**BOJ는** 난이도/정답률 항목을 빼고, `https://www.acmicpc.net/problem/<번호>` 링크만 넣는다.
(⚠️ BOJ는 서비스 종료 상태라 자동 조회 불가 — 사용자가 준 정보만 기록)

---

## 3. 사용자가 "N번 풀었어 + 코드"를 주면 — 처리 순서

### ① 검증 (봐주기 금지 — 절대 생략 금지)

**독립 브루트포스를 직접 작성해 실제로 실행**한다. 정적 분석만으로 판정하지 않는다.

- 랜덤 대조 수천 건 + 경계 케이스
- **최악 제약에서 시간 측정**
- `print` 잔존 검색 ← **누적 4회 재발**한 항목 (3197·2293·1285·1561)

> 🚨 **내 기억·레퍼런스부터 의심한다.** 예제 정답이나 기대값을 기억으로 적으면 자주 틀린다
> (실제 오류 사례: 1561 예제 "2"→**4**, 17837 "공식 예제" 4개 중 2개 오기억, 5653 경계 "0"→**4**).
> **교차검증 결과가 근거이고, 내 기억이 틀린 것**으로 간주한다.

### ② SWEA면 메타 조회

```bash
python C:/Users/solom/crawler.py chrome     # 디버그 크롬 (9222) — SWEA 로그인 필요
python _meta/fetch_swea.py <contestProbId> --json
```
- `contestProbId`는 문제 URL의 쿼리파라미터. 사용자가 URL을 안 주면 **물어본다** (번호로 역검색 불가)
- 크롬이 안 떠 있으면 `ECONNREFUSED 9222` → 위 명령으로 띄우고, 로그인 풀렸으면 사용자에게 요청

### ③ 파일 작성 + 커밋 + push

```bash
git add -A
git commit -m "[SWEA 2382] 미생물 격리 — 품 (1회)"
git push
```

**커밋 메시지 형식**
```
[SWEA 2382] 미생물 격리 — 품 (1회)
[BOJ 2293] 동전1 — 품 · 졸업 (5회, 05-28~08-02)
[BOJ 17837] 새로운 게임 2 — 틀림 (2회)
```

> 커밋 본문 끝에 항상:
> ```
> Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
> ```

### ④ 옵시디언 쪽 동기화 (볼트가 있는 PC에서만)

1. **실수노트**는 **사용자가 직접 쓴다** — 대신 쓰지 않는다
2. **못푼 문제모음** 노트에 진단·정답코드·검증결과 추가 (본문은 `<!-- 본문은 본인이 직접: "..." -->` 로 인용)
3. **품/맞음이면** `_졸업 아카이브/`로 이동 + 파일명에 날짜 추가 + ` [졸업]` 접미
4. **데일리**(`_Daily/YYYY-MM-DD.md`) 갱신 — `solved`는 **그날 시도 총수**(못품·틀림 포함)

---

## 4. 사용자 규칙 (반드시 지킬 것)

| 규칙 | 내용 |
|---|---|
| **언어** | 항상 **한국어** |
| **봐주기 금지** | 모든 채점을 **독립 브루트포스로 실제 실행**해 검증. 내 도구·기억·데이터를 **먼저** 의심 |
| **유형 스포 금지** | 복기 문제 **추천 시**에는 문제번호 + 마지막 시도일만. **DP·비트마스크 같은 유형/태그 절대 노출 금지** (유형 판별까지가 훈련) |
| **실수노트 본문** | **사용자가 직접 작성.** AI는 정답 코드·진단·파일 관리만 |
| **졸업 처리** | 삭제 아니라 **아카이브 이동** |
| **검산 리마인드** | "제출 전 `print` 검색 + 예제 대조" |
| **못품 기준** | 답 본 것 = 못품 / **채점 통과만 품** / 힌트 받고 구현 = 못품 |
| **파일명 규칙** | 못푼 문제모음은 `제목 (MM-DD, MM-DD).md` — **이 형식이 아니면 복기 큐에서 통째로 사라진다** (실제 7건 실종 사고) |

---

## 5. 자주 나는 문제

| 증상 | 원인 / 해결 |
|---|---|
| `git push` 시 `Permission denied (publickey)` | SSH 키 없음 → `gh auth setup-git` 후 remote를 **HTTPS**로 |
| `ECONNREFUSED 127.0.0.1:9222` | 디버그 크롬 꺼짐 → `python C:/Users/solom/crawler.py chrome` |
| SWEA가 로그인 페이지로 튐 | 세션 만료 → 사용자에게 로그인 요청 (자주 끊김) |
| 한글 깨짐 / `UnicodeEncodeError` | 앞에 `PYTHONIOENCODING=utf-8` |
| `review_queue.py`가 이상하게 동작 | **반드시 `C:/Users/solom` 에서 실행** (한글 경로 인코딩) |
| 대시보드가 "허브 꺼짐" | 클라우드는 `curl https://<터널>/` 로 확인. 로컬은 `python judge/server.py` |
| 허브 호출이 **401** | 토큰 불일치 → 우측 상단 허브 버튼에서 재입력 (`~/.algo-hub-token`) |
| 터널 URL 이 바뀜 | 정상(quick tunnel). `algo-endpoint.timer` 가 5분 내 `_meta/endpoint.json` 갱신 |
| `/fetch` 가 `needsLocal` | 클라우드엔 브라우저·세션 없음 → **내 PC 로컬 허브**에서 실행 |
| 문제 클릭 시 "자료 없음" | 아직 안 받은 문제 → `python _meta/crawl_all.py` 후 `build_probindex.py`+`build_heatmap.py` |
| 트리가 비어 있음 | `problems/index.json` 또는 `_meta/cosal_list.json` 누락 → 위 파이프라인 재실행 |
| SWEA 를 번호로 가져오기 실패 | 정상. `contestProbId` 필요 → URL 을 직접 입력하거나 `_meta/swea_ids.json` 채우기 |
| 옵시디언에 오늘 기록이 없음 | **싱크 지연** — 파일 mtime 확인하고, 없으면 사용자에게 알림 |

---

## 6. 현황 · 잔디 — **자동화되어 있음**

수동으로 돌릴 일은 거의 없다. **2중 자동화**가 걸려 있다:

| | 어디서 | 언제 | 데이터 |
|---|---|---|---|
| **pre-commit 훅** | 로컬 PC | **커밋할 때마다** | `history.json` + **실수노트** + repo 파일 (완전) |
| **GitHub Actions** | GitHub 서버 | 매일 **KST 01:00** + `boj//swea//history.json` push + 수동 | `history.json` + repo 파일 (실수노트 접근 불가) |

- 훅 설치: `python _meta/install_hooks.py` (**PC마다 1회**. `.git/hooks`는 push 안 됨)
- Actions 수동 실행: `gh workflow run heatmap.yml`
- 훅이 실패해도 **커밋을 막지 않는다** (`exit 0`)

수동 실행이 필요하면:
```bash
python _meta/build_heatmap.py    # 잔디 + 대시보드(index.html)
python _meta/build_index.py      # README 현황표 + 풀이 인덱스
python _meta/build_probindex.py  # 문제 자료 색인(problems/index.json)
```

### 잔디 동작 방식

| | |
|---|---|
| 출력 | `assets/heatmap.svg` → README에서 `![](./assets/heatmap.svg)` 로 표시 |
| 누적 데이터 | **`_meta/history.json`** (date → 그날 시도 문제 수) |
| 데이터 병합 | `history.json` **+** 옵시디언 실수노트(있을 때) **+** repo 풀이파일의 `풀이일` — 셋을 합쳐 큰 값 채택 |

> 🔑 **`history.json`이 핵심이다.** 볼트가 없는 PC에서도 잔디가 유지되도록 **repo에 커밋된 누적본**이다.
> 볼트가 있는 PC에서 돌리면 실수노트 전체 이력이 자동으로 합쳐진다. **절대 삭제하지 말 것.**

- 카운트 정의 = **그날 시도한 문제 수** (데일리 노트의 `solved`와 같은 의미. 못품·틀림 포함)
- 검증됨: 데일리 `solved` 값과 최근 8일 전부 일치
- 다크모드는 SVG 내부 `prefers-color-scheme`으로 자동 전환
- 셀에 마우스 올리면 `날짜 — N문제` 툴팁

> ⚠️ 옵시디언의 `코테 잔디.md`는 **dataviewjs + 히트맵 플러그인** 기반이라 GitHub에서 안 돌아간다.
> 그래서 별도 SVG 생성 방식을 쓴다. **둘은 같은 데이터(실수노트)를 보므로 수치가 일치해야 정상이다.**
