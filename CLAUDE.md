# CLAUDE.md — 이 repo 작업 지침

> **이 파일을 읽는 AI 에이전트에게:** 아래는 이 저장소의 운영 규칙이다.
> 사용자가 "문제 풀었어 + 코드"를 주면 **이 순서 그대로** 처리한다.
> 이전 대화 맥락이 없어도 이 문서만으로 동일하게 동작해야 한다.

---

## 0. 이 repo는 무엇인가

**코딩테스트 풀이 아카이브** (BOJ / SWEA / 코드트리). 사용자가 푼 코드를 문제 단위로 보관한다.

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

> 🔓 **코드트리(CT)도 공개 저장 — 소유자 결정 (2026-09-23).**
> 코드트리 트레일은 **유료 콘텐츠**다(계정 결제됨). 에이전트가 "public repo 에 올리면 재배포가 되어
> DMCA 로 repo·Pages 전체가 내려가거나 계정이 정지될 수 있다"고 알렸고, 소유자가 **위험을 감수하고**
> BOJ/SWEA 처럼 지문·예제를 그대로 저장하기로 했다. **에이전트는 다시 묻지 않는다.**
>
> | 코드트리 | 저장 |
> |---|---|
> | 번호·제목·URL·트레일/챕터/레슨·기출 출처·난이도·한도 | ✅ `problems/codetree/`, `_meta/codetree_list.json` |
> | 지문·입출력 설명·제약·힌트·예제 | ✅ `problems/codetree/<no>.json` (+ 보관소 `_meta/tc_store/codetree/` 에도 사본) |
> | 기출의 **유형 태그·선수 레슨**, 내 코드트리 진행상태 | ❌ 어디에도 저장 안 함 (**유형 스포 금지** — 공개 여부와 무관) |
>
> - **스위치 한 곳: `_meta/judge_config.json` 의 `"privateSites"`** (지금 `[]`).
>   `["CT"]` 로 바꾸면 지문을 repo 에서 빼고 허브 보관소(`/prob`, 토큰 필요)에서만 내준다.
>   서버·크롤러·selfcheck·pre-commit 훅이 모두 이 값을 읽고, **못 읽으면 안전하게 `["CT"]`** 로 동작한다.
> - 비공개로 되돌려도 **이미 push 된 지문은 히스토리에 남는다**(위 ⚠️ 와 같다).
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
| `#run` | **연습장** — 코드+입력 넣고 실행해 출력만 보기 (토큰 있을 때만 메뉴 노출) |

#### 🎨 테마 (2026-08-26)

헤더 오른쪽 버튼이 **자동 → 라이트 → 다크 → 자동** 으로 돈다. 기본은 `자동`(운영체제
설정을 따름)이라 예전과 똑같이 동작하고, 고른 값만 그 브라우저 `localStorage.theme`
에 남는다(repo 에는 아무것도 안 들어간다).

> 🚩 **색을 고칠 때는 `_dashboard_tpl.py` 의 `_DARK` 한 곳만 고친다.**
> 다크 값은 거기 한 벌만 적어 두고 빌드할 때 `__DARKVARS__` 두 자리
> (`@media(prefers-color-scheme:dark)` 안 / `:root[data-theme="dark"]`)에 같이 박힌다.
> 예전처럼 규칙마다 `@media(prefers-color-scheme:dark)` 를 새로 달면 **버튼으로 고른
> 테마에는 반영되지 않는다** — 색은 `:root` 변수로 추가할 것.
> 첫 그림이 번쩍이지 않게 `<head>` 맨 위 스크립트가 `data-theme` 를 미리 붙인다.

#### 🔤 문제 지문 가독성 규칙 (2026-09-23)

코드트리·코딩살구 실측(둘 다 Pretendard 16px)에 맞춰 **문제 페이지 지문 영역만** 통일했다(홈·트리·현황 글꼴은 그대로).

| | 규칙 |
|---|---|
| 글자 | Pretendard 16px(웹폰트는 문제 페이지에서만 jsdelivr 동적 서브셋, 막히면 기존 글꼴), 줄간격 1.7, **글 칸 최대 800px** |
| 코드·예제·히든 TC 패널 | 14px |
| CT 그림 | `width` 적힌 HTML 그림은 그 폭 / 폭 없는 그림은 **원본폭÷3.75 를 240~520px** 로(코드트리가 보여 주는 크기와 거의 같다) |
| BOJ 그림 | `image_widths`(코딩살구가 보여 주는 폭, `_meta/crawl_img_widths.py`) → 없으면 640px 상한 |
| SWEA 그림 | 원본 크기, 640px 상한 |

- 어떤 그림도 원본보다 크게 늘리지 않는다. 클릭 확대는 그대로.
- 예전엔 마크다운 그림이 칸 폭(1,080px)까지 커져 "그림이 너무 크다"는 지적을 받았다(1800px 원본이 1,080px로 떴다).

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

#### 🔒 공개 범위 — "읽기는 공개, 쓰기는 나만" (2026-08-14 점검·강화)

터널 주소는 `_meta/endpoint.json` 이 public repo 에 커밋되므로 **누구나 안다.**
그 전제에서 실제로 외부인이 무엇을 할 수 있는지 찔러보고 정리했다.

| | 누가 | 근거 |
|---|---|---|
| 잔디·문제·제출현황 **보기** | 누구나 | Pages 정적 파일 + `GET /`·`/status` |
| **채점·저장·삭제·메모·크롤링·연습장** | 토큰 보유자(=나)만 | 모든 POST 가 `_auth_ok()` 통과 후에만 본문을 읽는다 |

- 무토큰·틀린토큰 POST 를 **50회** 시도해 통과 0회 확인. `/judge` 는 VM 에서
  코드를 실행하므로 **토큰이 곧 RCE 권한**이다. 그래서 아래를 같이 걸었다:
  - `?token=` **쿼리 인증 제거** — URL 은 프록시 로그·브라우저 히스토리·Referer 에
    남아 토큰이 새는 통로였다. 이제 헤더로만 받는다.
  - 인증 실패 **누적 시 지수 백오프**(4회째부터, 최대 15초) — 대입 시도 무력화.
  - `GET /problems` 를 토큰 뒤로. 지문 공개가 아까워서가 아니라(이미 Pages 에 공개)
    **한 번에 574개 파일을 읽어 18MB 를 만드는 부하** 때문. 대시보드는 이걸 안 쓴다.
  - 바인딩 기본값 `0.0.0.0` → **`127.0.0.1`** (`--bind` 로 변경). 사내망·공용
    와이파이 노출 방지. VM 은 iptables 로도 12014 를 막고 있지만 이중으로 둔다.
- 🚩 **401 을 던지기 전에 요청 본문을 반드시 비운다**(`_drain()`). 본문을 소켓에
  남긴 채 응답하면 keep-alive 가 어긋나 **다음 요청이 400 으로 깨진다.** 실제로
  무토큰 25회 중 13회가 400 이라 "인증이 뚫린 것처럼" 보여 한참 헤맸다.

#### 📦 도구 배포 `#tools` — `POST /toolinfo` · `POST /tool` (2026-08-28)

**다른 PC 에서 대시보드만 열면 개인 도구(zip)를 바로 받아 쓰기 위한 것.**

- 대시보드 상단 **도구** 메뉴. 연습장과 같이 `TOK` 가 있을 때만 뜨고, 서버도 토큰을 요구한다.
- 파일은 **VM 의 `~/algo-tools/`** — `ALGO_TOOLS_DIR` 로 바꿀 수 있다.
- 올리기: `sh judge/push_tool.sh` (릴리스에서 받아 올림) 또는 `sh judge/push_tool.sh ./x.zip`.
  이름을 안 주면 서버가 **디렉토리에서 가장 최근 zip** 을 고른다.

> 🚩 **배포 파일을 repo 안에 두지 말 것.** 이 저장소는 public 이라 `problems/` 옆에
> 두는 순간 Pages 로 그대로 공개된다. 배포 zip 에는 설정·자격증명이 함께 들어가는
> 일이 많아 이 구분이 곧 보안선이다. VM 에서도 `chmod 600` 으로 둔다.

흔적을 줄이려고 걸어 둔 것들 — 하나라도 빠지면 파일이 어딘가에 남는다:

| 어디서 샐 수 있나 | 막은 방법 |
|---|---|
| URL(프록시 로그·히스토리·Referer) | 토큰은 **헤더로만**. `GET ?token=` 은 애초에 없다 |
| 브라우저 디스크 캐시·중간 프록시 | 응답에 `Cache-Control: no-store` + `Pragma`/`Expires` |
| 저장 후 남는 blob 주소 | 저장 직후 `URL.revokeObjectURL()` — 탭에서 다시 못 연다 |
| 파일명으로 다른 파일 읽기 | `os.path.basename()` 으로 경로 조작 차단 |
| 토큰 대입 | 기존 `_reject()` 지수 백오프 그대로 탄다 |

- 서버 로그는 **디버깅용으로 남긴다**: 언제·어느 IP 가·어떤 파일을 받았는지까지.
  토큰과 파일 내용은 남기지 않는다.

#### ▶ 연습장 `#run` — `POST /exec`

문제와 무관하게 **코드 + 입력을 넣고 출력만 본다**(정답 대조 없음, print 디버깅용).

- 대시보드 상단 **연습장** 메뉴. `TOK` 가 있을 때만 뜨고, 서버도 토큰을 요구한다.
- Ctrl+Enter 실행 · Tab/Shift+Tab 들여쓰기 · 코드/입력은 `localStorage` 에만 남는다(커밋 안 됨).
- 제한 0.5~30초. stdout 은 20,000자에서 자른다(무한 출력이 브라우저를 죽이지 않게).
- 상태: `ok` / `runtime_error`(stderr 표시) / `time_limit_exceeded` / `compile_error`.
- 🚩 **두 허브의 토큰은 반드시 같은 값이어야 한다.** 대시보드는 토큰을 하나만 저장하므로
  값이 다르면 한쪽(주로 크롤링용 로컬 허브)이 **401** 을 뱉는다. 새 PC 세팅 시:
  ```bash
  ssh -i ~/.ssh/oracle_judge ubuntu@134.185.106.155 'cat ~/.algo-hub-token' > ~/.algo-hub-token
  ```
- 서버 로그: `ssh ubuntu@134.185.106.155 'journalctl -u algo-hub -n 50'`
- SSH 키: `~/.ssh/oracle_judge` (= Downloads 의 `quality-search.key`)

### 💾 테스트케이스는 두 곳에 나뉘어 있다 (중요)

코딩살구의 히든 TC 는 실제 채점용이라 매우 크다. **BOJ 2493 탑은 한 케이스가 4.4MB**
(N ≤ 500,000, 높이 8자리) 이고 문제 전체로 28MB 다. 전부 repo 에 넣었더니
`problems/` 가 **565MB** 가 되어 **GitHub Pages 빌드가 실패**했고, 브라우저는 문제 하나
보려고 28MB 를 받아야 했다.

| 어디 | 무엇 | 용량 |
|---|---|---|
| **repo** `problems/` | 문제당 **200KB 로 줄인 보기용** (커밋됨) | 20MB |
| **채점 서버** `~/algo-tc/` | **전체 테스트케이스** (git 밖) | 564MB |
| 로컬 `_meta/tc_store/` | 서버로 올릴 원본 (**gitignore**) | 564MB |

- 케이스를 자르지 않는다(자르면 채점에 못 쓴다). 통째로 들어가는 것까지만 담고
  나머지는 `private_tc_omitted` 에 개수만 남긴다. 상한은 `fetch_problem.py` 의 `PRIV_CAP`.
- **채점은 전체본으로 한다.** 대시보드가 `useStoredTC: true` 만 보내면 서버가
  `~/algo-tc/<sub>/<no>.json` 을 읽어 채점한다. 브라우저는 케이스를 올리지 않는다.
- 서버로 올리기:
  ```bash
  python _meta/sync_tc.py            # 없는 것만
  python _meta/sync_tc.py --force    # 전부 다시
  ```
- 관련 엔드포인트: `POST /tc` (정보·미리보기), `POST /tcupload` (업로드)

> ⚠️ **`_meta/tc_store/` 를 커밋하지 말 것.** .gitignore 에 있다. 실수로 넣으면
> repo 가 다시 500MB 를 넘고 Pages 가 죽는다.

### 🧹 히스토리 재작성 (2026-08-12, 1회 발생)

TC 를 200KB 로 줄이기 **전에** 올렸던 거대 blob(2493 26.8MB, 12015 19.7MB 등)이
히스토리에 남아 **clone 이 206MB** 였다. `git filter-repo --strip-blobs-bigger-than 1M`
으로 제거하고 force push 했다.

- 결과: clone **206MB → 48MB**, `.git` 208MB → 17MB. 커밋 75개·파일 969개·트리 해시 **모두 동일**(내용 변화 0).
- 커밋 SHA 는 전부 바뀌었다. **재작성 이전 클론은 pull 이 안 되므로** `git reset --hard origin/master` 또는 재clone.
- GitHub 잔디·작성자 연결은 유지됨(재계산 후 확인).
- ⚠️ 다시 할 일이 없도록 **큰 파일을 애초에 커밋하지 말 것**. 위 tc_store 경고가 그래서 있다.

### 📦 문제 자료 파이프라인

```
_meta/crawl_cosal_list.py   코딩살구 전체 목록  → _meta/cosal_list.json   (513문제, 주차·개념 섹션)
_meta/crawl_all.py          지문·예제 일괄 수집 → problems/<site>/<no>.json
_meta/build_probindex.py    색인 생성          → problems/index.json
_meta/build_heatmap.py      잔디 + 대시보드    → index.html
```

> Pages 는 디렉터리 목록을 안 주므로 **`problems/index.json` 색인이 반드시 있어야** 트리가 뜬다.
> 새로 크롤링했으면 `build_probindex.py` → `build_heatmap.py` 순서로 돌린다.

**선행조건**: 디버그 크롬 + 각 사이트 로그인
```bash
python _meta/debug_chrome.py         # 로그인용 크롬(9222). --check 로 확인만
#   → 뜨는 창에서 코딩살구 / SWEA 로그인 (프로필에 남아 다음에도 유지)
python _meta/crawl_cosal_list.py     # 코딩살구 전체 목록 (2~3분)
python _meta/crawl_all.py            # 지문·예제·이미지 (문제당 ~5초)
python _meta/crawl_all.py --htc      # 히든 테스트케이스
python _meta/sync_tc.py              # 전체 TC 를 채점 서버로
python _meta/build_probindex.py && python _meta/build_heatmap.py
python _meta/selfcheck.py            # 이상 없나 확인
```

### ⚠️ SWEA 는 번호로 역검색이 안 된다

표시번호(2382) ≠ `contestProbId`(AWXR…). 목록 페이지도 JS 렌더라 자동 매핑 실패.
→ `_meta/swea_ids.json` 에 `{"2382": "AWXRQm6q…"}` 를 채워야 자동 크롤링 대상이 된다.
→ 없으면 대시보드에서 **문제 다시 가져오기** 클릭 시 URL 을 물어본다.

### 🌳 코드트리 (CT) — 2026-09-23 추가

**대상**: 트레일 6개(Novice Low ~ Intermediate High, 1,334카드) + 기출 3종(삼성 SW 역량테스트 78 · 현대 HSAT 22 · ACPC 17) = **1,451문제**.

| | |
|---|---|
| 번호 | 코드트리 `problem_id`. **트레일은 숫자(`196`), 기출은 `f` + 번호(`f386`)** |
| 왜 f 인가 | 트레일과 기출은 번호 체계가 달라 106개가 겹친다(386 = 트레일 "문자열 돌리기" = 기출 "AI 로봇청소기"). 합치면 기출이 엉뚱한 문제 밑으로 사라진다 |
| 목록 | `_meta/codetree_list.json` (트레일 → 챕터 → 레슨 / 기출 → 회차). 대시보드가 필요할 때만 받는다(index.html 에 안 박음) |
| 문제 자료 | `problems/codetree/<no>.json` (지문·예제 포함 — 위 소유자 결정) + 사본 `_meta/tc_store/codetree/<no>.json` |
| 풀이 파일 | `codetree/<no>_<제목>.py` (예: `codetree/f386_AI로봇청소기.py`) |
| URL | 트레일 `…/trails/complete/curated-cards/<card>/description` · 기출 `…/frequent-problems/<source>/problems/<alias>/description` |

**크롤링** — 디버그 크롬(9222)에서 코드트리 **로그인** 필요(세션은 프로필에 남는다):
```bash
python _meta/crawl_codetree.py list [--refresh]        # 목록(트레일 6 + 기출 3)
python _meta/crawl_codetree.py fetch [--group samsung-sw] [--no 196 --no f386] [--force] [--retry-locked]
python _meta/crawl_codetree.py all                     # list + fetch
python _meta/crawl_codetree.py rebuild-public [--no f386]   # 보관소로 공개 JSON 다시 만들기(브라우저 불필요)
python _meta/fetch_problem.py <코드트리 URL | ct:196 | ct:f386> --print [--save]   # 단건(대시보드 '새 문제')
```
- 코드트리 API(`api-prod.codetree.ai/api/v2/`)를 **브라우저 페이지 안에서** 부른다. JWT(`localStorage.CODETREE_GLOBAL_TOKEN`)는 페이지 밖으로 꺼내지 않는다.
- 계정 보호: 동시 3·초당 4건 이하. 429/403 이 연달아 나오면 받은 데까지 저장하고 멈춘다(exit 3, 다시 돌리면 이어 받음).
- 토큰 수명이 15분이라 긴 크롤링 중 401 이 나면 탭을 새로고침해 사이트가 스스로 갱신하게 한다.
- 그림은 받지 않는다(`contents.codetree.ai` 공개 CDN URL 그대로). 옛 기출 88문제는 마크다운이 아니라 `<p align>`/`<img>`/`<br>` **HTML** 로 그림을 넣는다 — 대시보드는 이 네 태그만 허용 목록으로 되살린다.
- 퀴즈형 283문제(`ptype`: Single/Multiple/Sequential choice)는 예제·한도가 없고 보기가 지문 끝에 붙는다. 대시보드는 채점 대신 "코드트리에서 풀기"만 띄운다.
- 🚩 **유형 스포 금지**: 기출의 `tags`·`prerequisite_lessons`, 내 `progress_status` 는 어디에도 저장하지 않는다(selfcheck 가 막는다).

**옛 기록 연결** — 실수노트에 번호 없이 적힌 코드트리 기록(`## 코드트리 나무박멸 (틀림)`, `## 여왕개미` …)을
`build_heatmap.py` 가 카탈로그 제목으로 찾아 `CT/<no>` 로 잇는다(2026-09-23 기준 29제목 · 48건).
제목에 `코드트리`가 있으면 전체에서, 없으면 **기출에서만**, **정확히 하나**와 맞을 때만 잇고 원래 제목은 `title_raw` 에 남긴다.
프로그래머스·SWEA 제목은 건드리지 않는다.

**생성 테스트케이스(삼성 기출)** — 코드트리는 히든 TC 를 주지 않는다(예제만 준다):
```bash
python _meta/ct_tcgen.py prep --group samsung-sw      # 작업 폴더(지문·예제·그림 PNG)
python _meta/ct_tcgen.py cross f386                    # 독립 풀이 A/B 를 랜덤 입력에서 교차검증
python _meta/ct_tcgen.py emit f386                     # 일치하면 30케이스를 보관소 private 로
python _meta/ct_tcgen.py status --group samsung-sw
python _meta/crawl_codetree.py rebuild-public          # 보관소 → 공개 JSON(private_testcases 200KB 상한)
python _meta/sync_tc.py --site CT                      # VM 보관소로(큰 케이스 채점용)
```
- 문제마다 **서로 모르는 두 풀이**(A: 생성기+풀이 / B: 입력 검증기+풀이)가 공식 예제를 통과하고,
  랜덤 입력 수백 개에서 끝까지 같은 답을 낼 때만 케이스로 남긴다. 입력은 검증기가 통과시킨 것만 쓴다.
- 기준 풀이는 **스포일러라 repo 밖** `~/_스포주의_CT기출_참고풀이/<no>/` 에 둔다(`_스포주의_B형_참고풀이` 와 같은 관례).
- 대시보드는 `tc_generated` 인 문제에 **"생성 TC (공식 아님)"** 을 붙인다. 여기서 맞아도 코드트리 채점 통과와 같지 않다.
- ❌ 다른 사용자 제출 결과에서 히든 케이스를 긁어모으는 방법은 쓰지 않는다(목록의 실패 케이스는 127자에서 잘려 있기도 하다).

**공개/비공개 스위치** (`_meta/judge_config.json` 의 `privateSites`) — 비공개로 돌리려면:
1. `"privateSites": ["CT"]` 로 바꾸고
2. `python _meta/crawl_codetree.py rebuild-public` (공개 JSON 에서 지문 제거)
3. `python _meta/sync_tc.py --site CT` (공개 모드에선 크롤링 뒤 VM 동기화를 안 하므로 **꼭** 올릴 것)
4. 허브 재시작(로컬·VM). 대시보드는 `/prob` 로 허브 보관소에서 지문을 받는다.

### 🧰 스크립트 한눈에 (전부 repo 안에 있다)

| 파일 | 하는 일 |
|---|---|
| `_meta/debug_chrome.py` | 크롤링용 **디버그 크롬(9222)** 실행. 평소 크롬과 프로필 분리 |
| `_meta/crawl_cosal_list.py` | 코딩살구 전체 문제 **목록** → `cosal_list.json` |
| `_meta/crawl_all.py` | 지문·예제·이미지·히든TC **수집** (`--htc --empty --bad --force --site --limit`) |
| `_meta/fetch_problem.py` | URL/번호 하나로 **단건 크롤링** (4개 사이트 — 코드트리는 crawl_codetree 로 넘긴다) |
| `_meta/crawl_codetree.py` | 코드트리 **목록·지문·예제** (트레일 6 + 기출 3, `list/fetch/all/rebuild-public`) |
| `_meta/ct_tcgen.py` | 코드트리 기출 **생성 테스트케이스** (`prep/check/cross/emit/status`) |
| `_meta/crawl_img_widths.py` | 코딩살구가 **그림을 보여 주는 폭**을 모아 `problems/boj/<no>.json` 의 `image_widths` 로 (그림 순서 = `[[IMG:n]]`). 새로 받는 문제는 `fetch_problem.py` 가 알아서 넣는다 |
| `_meta/map_swea_ids.py` | SWEA 번호 → `contestProbId` 매핑 |
| `_meta/sync_tc.py` | 전체 테스트케이스를 **채점 서버로 업로드** |
| `_meta/build_probindex.py` | 문제 **색인** → `problems/index.json` |
| `_meta/build_heatmap.py` | 잔디 + **대시보드**(`index.html`) 생성 |
| `_meta/build_index.py` | README 현황표 |
| `_meta/install_hooks.py` | pre-commit 훅 + 커밋 이메일 + merge 드라이버 (**새 PC 1회**) |
| `_meta/publish_endpoint.py` | 터널 URL 을 `endpoint.json` 에 publish (서버에서 timer 로) |
| `_meta/selfcheck.py` | **저장소 자체 점검** — 조용히 망가지는 것 탐지. `--leak-only [--staged]` 는 공개 금지 검사(훅이 쓴다) |
| `judge/server.py` | 허브 서버(채점·저장·크롤링·메모·삭제·TC·`/prob`) — **CPython 으로만** 띄울 것(아래 5장) |
| `judge/_bench.py` | 기기 속도 벤치(시간 보정에 사용) |

> 📌 `C:/Users/solom/crawler.py` 는 **SSAFY 강의자료 전용**이고 이 repo 와 무관하다.
> (파일 자체에 "외부 공유 금지" 고지가 있어 public repo 에 넣지 않았다.)
> 이 repo 에 필요한 디버그 크롬 기능만 `_meta/debug_chrome.py` 로 따로 두었다.
> `C:/Users/solom/review_queue.py` 도 옵시디언 볼트 전용이라 repo 밖이다.

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
python _meta/debug_chrome.py        # 디버그 크롬(9222) — 각 사이트 로그인
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

> 🚩 **rebase 뒤에는 반드시 다시 빌드하고 커밋한다.**
> ```bash
> python _meta/build_heatmap.py && git add -A && git commit -m "빌드 산출물 갱신"
> ```
> `.gitattributes` 의 `merge=ours` 는 **rebase 에서 방향이 뒤집힌다** —
> rebase 중에는 upstream 이 "ours" 라서, 내가 방금 만든 `index.html` 이
> 원격의 옛 것으로 조용히 되돌아간다. 소스는 `_meta/_dashboard_tpl.py` 이므로
> 다시 빌드하면 복구되지만, **모르고 push 하면 사이트에 변경이 안 나타난다.**
> (2026-08-14 실제로 겪음 — 코드 페이지 기능이 배포에서 통째로 빠졌다.)

---

## 2. 파일 규약

```
boj/<번호>.py                  예: boj/2293.py
swea/<번호>_<제목>.py           예: swea/2382_미생물격리.py
codetree/<번호>_<제목>.py       예: codetree/f386_AI로봇청소기.py · codetree/196_한줄출력.py
                               (번호 = 코드트리 problem_id — 트레일은 숫자, 기출은 f+숫자)
```

> 코드트리 풀이 헤더도 BOJ/SWEA 처럼 `[문제]`·`[예제]` 가 들어간다(공개 모드). 단 힌트는 넣지 않고,
> 제약은 마크다운 문자열이라 앞 6줄만 적는다. 비공개 모드(`privateSites: ["CT"]`)면 한 줄 안내로 바뀐다.

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
python _meta/debug_chrome.py     # 디버그 크롬 (9222) — SWEA 로그인 필요
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
| `git pull` 이 `unrelated histories` / 계속 충돌 | **2026-08-12 히스토리 재작성** 이전의 낡은 클론이다 → `git reset --hard origin/master` 하거나 다시 clone |
| `git push` 시 `Permission denied (publickey)` | SSH 키 없음 → `gh auth setup-git` 후 remote를 **HTTPS**로 |
| `ECONNREFUSED 127.0.0.1:9222` | 디버그 크롬 꺼짐 → `python _meta/debug_chrome.py` |
| SWEA가 로그인 페이지로 튐 | 세션 만료 → 사용자에게 로그인 요청 (자주 끊김) |
| 한글 깨짐 / `UnicodeEncodeError` | 앞에 `PYTHONIOENCODING=utf-8` |
| `review_queue.py`가 이상하게 동작 | **반드시 `C:/Users/solom` 에서 실행** (한글 경로 인코딩) |
| 저장 직후 **새로고침하면 방금 낸 기록이 없음** | 정상 동작으로 고쳐졌다. 데이터가 `index.html` 에 박혀 있어 **Pages 재빌드(실측 ~46초, 캐시 10분)** 전에는 옛 빌드가 온다. 이제 `localStorage.pendingSubs` 에 들고 있다가 얹어 주고 **"반영 대기" 배지**를 단다. 배지가 안 사라지면 push 실패를 의심 |
| 지운 기록이 새로고침하면 되살아남 | 대기분(`pendingSubs`)이 안 지워진 경우. 삭제 시 `pendDrop` 이 같이 지운다. 수동 해제는 devtools 에서 `localStorage.removeItem("pendingSubs")` |
| **커밋했는데 고친 내용이 안 들어감** | 🚩 `build_heatmap.py` 는 돌릴 때마다 `built.json` 타임스탬프가 바뀌어 워킹트리가 절대 깨끗해지지 않는다. 그 잡음을 지우려고 **`git checkout -- .` 을 돌리면 커밋 안 된 `_dashboard_tpl.py` 수정까지 같이 날아간다** (2026-08-17 실제로 겪음 — 메시지만 있고 소스가 빠진 커밋이 push 됐다). **소스를 먼저 커밋하고 나서** pull/rebase/빌드할 것 |
| 대시보드가 "허브 꺼짐" | 클라우드는 `curl https://<터널>/` 로 확인. 로컬은 `python judge/server.py` |
| 허브 호출이 **401** | 토큰 불일치 → 우측 상단 허브 버튼에서 재입력 (`~/.algo-hub-token`) |
| 401 이 **몇 초씩 늦게** 온다 | 정상. 인증 실패가 누적되면 백오프가 걸린다. 올바른 토큰으로 한 번 성공하면 초기화 |
| POST 가 **400** (`bad request` HTML) | 인증 실패 응답이 본문을 안 비워 keep-alive 가 깨진 경우. `_drain()` 이 고쳤다. 재발하면 401 자리부터 의심 |
| 연습장 메뉴가 **안 보임** | 토큰 미설정 → 우측 상단 허브 버튼에서 입력하면 바로 뜬다 |
| 다른 PC 로컬 허브에 **LAN 에서 못 붙음** | 의도된 것(127.0.0.1 바인딩). 필요하면 `python judge/server.py --bind 0.0.0.0` |
| 터널 URL 이 바뀜 | 정상(quick tunnel). `algo-endpoint.timer` 가 5분 내 `_meta/endpoint.json` 갱신 |
| `/fetch` 가 `needsLocal` | 클라우드엔 브라우저·세션 없음 → **내 PC 로컬 허브**에서 실행 |
| 문제 클릭 시 "자료 없음" | 아직 안 받은 문제 → `python _meta/crawl_all.py` 후 `build_probindex.py`+`build_heatmap.py` |
| 지문이 **문장 중간에서 잘림** | 섹션 경계를 `"입력"` 처럼 맨글자로 자르면 본문의 "…을 **입력**받아" 에서 끊긴다. 경계는 반드시 `"\n입력\n"`. 복구는 `crawl_all.py --empty` (30자 미만도 대상) |
| 트리가 비어 있음 | `problems/index.json` 또는 `_meta/cosal_list.json` 누락 → 위 파이프라인 재실행 |
| SWEA 를 번호로 가져오기 실패 | 정상. `contestProbId` 필요 → URL 을 직접 입력하거나 `_meta/swea_ids.json` 채우기 |
| 옵시디언에 오늘 기록이 없음 | **싱크 지연** — 파일 mtime 확인하고, 없으면 사용자에게 알림 |
| 코드트리 크롤링이 `로그인 필요` 로 멈춤 | 디버그 크롬에서 코드트리 로그인이 풀렸다 → 그 창에서 로그인(비밀번호는 에이전트가 넣지 않는다) 후 다시 실행(이어 받음) |
| 코드트리 크롤링이 exit 3 으로 멈춤 | 429/403 연속 — 계정 보호용 자동 정지. 시간을 두고 다시 돌리면 이어 받는다 |
| CT 문제가 트리에 안 보임 | `_meta/codetree_list.json` 누락/깨짐 → `python _meta/crawl_codetree.py list` |
| CT 기록이 "번호 없는 BOJ" 로 보임 | 실수노트 제목이 카탈로그 제목과 정확히 안 맞는다(예: "퇴근 버스"). 실수노트 헤딩을 코드트리 제목으로 고치면 다음 빌드에서 이어진다 |
| 채점 결과가 `no_testcases` | 채점할 케이스가 0개(보관본 없음). 예전엔 이때 **accepted 0/0(가짜 정답)** 이 나갔다 |
| 커밋이 "공개 금지 검사" 로 막힘 | `privateSites` 에 든 사이트의 지문이 공개 파일에 들어갔거나, 유형 태그·진행상태 키가 들어갔다. `python _meta/selfcheck.py --leak-only` 로 원인 확인. 허브 응답의 `commitError` 에 이유가 실린다 |
| VM 허브가 배포 뒤 안 뜸 | VM 은 **Python 3.8** 이다. `server.py`·`build_*.py`·`sync_tc.py` 에 3.9+ 문법(`removeprefix`, `dict \| dict`, `list[str]` …)을 쓰면 죽는다 — `ast.parse(..., feature_version=(3,8))` 로 확인 |
| 허브를 PyPy 로 띄웠더니 보관소 파일이 0바이트 | `server.py` 는 파일을 닫지 않고 쓰는 곳이 있어 PyPy 에서는 바로 안 써진다. **서버는 CPython 으로만** (채점 러너만 PyPy) |

---

## 6. 현황 · 잔디 — **자동화되어 있음**

수동으로 돌릴 일은 거의 없다. **2중 자동화**가 걸려 있다:

| | 어디서 | 언제 | 데이터 |
|---|---|---|---|
| **pre-commit 훅** | 로컬 PC | **커밋할 때마다** | `history.json` + **실수노트** + repo 파일 (완전) |
| **GitHub Actions** | GitHub 서버 | 매일 **KST 01:00** + `boj/`·`swea/`·`codetree/`·`problems/`·`_meta/codetree_list.json`·`history.json` push + 수동 | `history.json` + repo 파일 (실수노트 접근 불가) |

- 훅 설치: `python _meta/install_hooks.py` (**PC마다 1회**. `.git/hooks`는 push 안 됨. 워크트리끼리는 공유)
- Actions 수동 실행: `gh workflow run heatmap.yml`
- 빌드 단계는 실패해도 **커밋을 막지 않는다** (`exit 0`). **단 하나 — 공개 금지 검사(`selfcheck.py --leak-only --staged`)만은 막는다**
  (`privateSites` 사이트의 지문 누출, 유형 태그·진행상태 키, `_meta/tc_store/` 추적). 2026-09-23 추가.

### 🚩 채점 비교 규칙 (2026-09-23 수정)
`judge/server.py same()` 은 **정답 토큰이 실수(소수점·지수)일 때만** 1e-6 오차를 준다. 정답이 정수면 글자가 같아야 한다.
예전엔 정수에도 상대오차를 줘서 **답이 100만 이상이면 ±1 오답이 '맞았습니다'** 였다(1000001 vs 1000000 통과).
코드트리 생성 TC 도구를 시험하다 일부러 틀린 풀이가 통과해서 드러났다. 그 전 채점 기록 중 큰 정수 답 문제는 봐준 판정이 섞여 있을 수 있다.

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

### 제출 이력은 회차마다 남는다 (2026-08-14 수정)

같은 날 같은 문제를 다시 내면 **예전엔 이전 기록을 지우고 새로 넣어** 
"틀렸다가 다시 풀어 맞힘" 의 앞부분이 사라졌다. 지금은 이렇게 나뉜다.

| | 단위 | 어디 |
|---|---|---|
| 잔디 `count` | **그날 시도한 문제 수** | `items` 는 문제당 하나로 유지 |
| 제출 이력 | **제출 1회 = 1줄** | 각 item 안의 `attempts[]` |

- `build_rows()` 가 `attempts` 를 회차별로 펼쳐 대시보드 `rows` 를 만든다(`2/3회` 배지).
- 통계 카드·잔디 툴팁은 **문제 단위로 묶어** 센다. 안 그러면 한 문제가 품과 못품 양쪽에 잡힌다.
- `_fill()` 은 `attempts` 를 **합집합**으로 합친다. 빈칸 채우기 규칙에 맡기면
  한쪽에 이미 있다는 이유로 다른 쪽 회차가 통째로 버려진다.
- ⚠️ `save_solution()` 안에서 attempts 리스트에 `hist` 라는 이름을 쓰지 말 것 —
  바깥의 history 딕셔너리를 가려 **`history.json` 을 배열로 덮어쓴다**(실제로 겪음).

- **회차별 코드 "보기" (2026-09-10)**: 풀이 파일은 문제당 하나라 재제출하면 덮어써진다.
  그래서 옛 회차 "보기"가 전부 최신 코드를 보여줬다(27183 에서 발견). 지금은
  `build_heatmap.annotate_commits()` 가 회차마다 그 시각의 커밋 해시를 붙이고(`row.commit`),
  대시보드가 `#c/<file>@<sha>` 로 raw.githubusercontent 에서 그 커밋의 파일을 연다.
  최신 회차는 그대로 로컬 파일. 전제: **git 이력이 있어야 한다** — Actions 는 `fetch-depth: 0`,
  허브는 full clone. 히스토리를 재작성하면 그 이전 회차 링크는 최신 코드로 되돌아간다.

> 🔑 **`history.json`이 핵심이다.** 볼트가 없는 PC에서도 잔디가 유지되도록 **repo에 커밋된 누적본**이다.
> 볼트가 있는 PC에서 돌리면 실수노트 전체 이력이 자동으로 합쳐진다. **절대 삭제하지 말 것.**

- 카운트 정의 = **그날 시도한 문제 수** (데일리 노트의 `solved`와 같은 의미. 못품·틀림 포함)
- 검증됨: 데일리 `solved` 값과 최근 8일 전부 일치
- 다크모드는 SVG 내부 `prefers-color-scheme`으로 자동 전환
- 셀에 마우스 올리면 `날짜 — N문제` 툴팁

### 실수노트에서 상태(품/못품/틀림)를 읽는 규칙 — 순서를 지킬 것

실수노트는 형식이 한 가지가 아니다. 아래 **우선순위**대로 읽는다 (`build_heatmap.py`).

| 순위 | 근거 | 예 |
|---|---|---|
| 1 | 날짜 줄의 괄호 | `#### 2026-07-08 (맞음)` · `2026-04-06 (틀림)` |
| 2 | 헤딩의 괄호 | `## 1463 (1로 만들기) (틀림)` — 괄호가 여럿이면 **마지막 상태어** |
| 3 | 날짜 다음 줄의 자유 문장 | `#### 2026-04-06` + `쉽게 풀었음 (못푼문제에서 삭제)` |

- **3번은 1·2번이 전혀 없을 때만 쓴다.** 본문은 결과가 아니라 *과정*을 적은 서술문이라,
  먼저 적용하면 크게 틀린다. 실제로 우선순위 없이 돌렸다가 16건이 잘못 뒤집혔다:
  `1450 "일반 냅색으로 **풀었**는데 메모리 초과"` → 품(실제 틀림),
  `15972 "답을 봐도 어떻게 **풀었**는지 이해가 안 간다"` → 품(실제 못품),
  `1463 "dp 개념이 박히지 **못했다**"` → 못품(실제 틀림).
- 자유 문장 판정 순서: `답보고`→못품 → `못품/못했`→못품 → **`삭제`→품** → `틀림` → `시간초과` → `풀었`.
  `못푼문제에서 삭제` = 졸업 = **품** (소유자 판단, 4659 는 "시간초과…필요성을 못느껴 삭제"라 품).
- 괄호는 `(시간 초과)` 처럼 띄어쓴 것도 받되, `(푸는시간 초과)`(= 본인이 푸는 데 걸린 시간)
  처럼 **한글 뒤에 이어붙은 것은 상태어가 아니다**.
- 같은 날짜가 두 번 적힌 경우(1486 은 `#### 06-09 (못품)` 과 맨 날짜줄이 둘 다 있음)
  **근거가 약한 쪽이 덮어쓰지 않게** 등급으로 막는다.
- 🚩 **`history.json` 캐시보다 실수노트가 우선이다** (`merge(..., status_first=True)`).
  예전엔 동점이면 캐시가 이겨서, 실수노트에 `(맞음)` 인 15926 이 계속 `못품` 으로 남았다.
  단 통째로 갈아끼우지 말 것 — 허브가 저장한 `file`·`passed`·`elapsed` 가 날아간다. **필드 단위로 채운다.**

> ⚠️ 옵시디언의 `코테 잔디.md`는 **dataviewjs + 히트맵 플러그인** 기반이라 GitHub에서 안 돌아간다.
> 그래서 별도 SVG 생성 방식을 쓴다. **둘은 같은 데이터(실수노트)를 보므로 수치가 일치해야 정상이다.**
