# 로봇 이동 — 연습용

정답이 없는 빈 세트다. 여기서 직접 풀어라.

## 푸는 법

1. `로봇이동_문제지.pdf` 를 읽는다 (풀이 힌트 없음)
2. `solution.py` 의 세 함수를 채운다 — `init` / `build` / `move`
3. 채점:

   ```
   python main.py < tc_valid.txt
   ```

   `#1 100 ... #5 100` 이 전부 100 이면 정답.
   지금은 빈 함수라 `#1 0 ... #5 0` 이 나온다.

## 참고

- `main.py` 는 채점기다. **수정하지 않는다.**
- 각 테스트 케이스는 명령 25개(init 1 + build/move)로 구성된다.
- 어느 move 가 틀렸는지 보려면 실행 시 stderr 에 상세가 찍힌다:

  ```
  python main.py < tc_valid.txt 2> err.txt
  ```

- 막히면 상위 폴더의 `solution.py` 가 정답이다. **먼저 충분히 시도한 뒤에 보라.**
