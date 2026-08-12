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
boj/     백준
swea/    SW Expert Academy
_meta/   도구
  fetch_swea.py     SWEA 문제 메타 자동 추출
```

**파일명**: `<번호>_<제목>.py` (예: `swea/4012_요리사.py`)

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
| 총 풀이 | 1 |
| BOJ | 1 |
| SWEA | 0 |

<!-- INDEX_START -->
| 사이트 | 번호 | 제목 | 결과 | 풀이일 | 분류 |
|---|---|---|---|---|---|
| BOJ | [1159](boj/1159.py) | 농구 경기 | 품 | 2026-08-12 |  |
<!-- INDEX_END -->
