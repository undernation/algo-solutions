# 로봇 이동 — 연습용

정답이 없는 빈 세트다. 여기서 직접 풀어라.

## 파일

| 파일 | 내용 |
|---|---|
| `로봇이동_문제지.pdf` | 문제지 (풀이 힌트 없음) |
| `solution.py` | **여기를 채운다** — `init` / `build` / `move` |
| `main.py` | 채점기. **수정하지 않는다** |
| `sample_input.txt` | 입력 (테스트 케이스 5개) |
| `sample_output.txt` | 다 맞았을 때의 출력 |

## 푸는 법

1. `로봇이동_문제지.pdf` 를 읽는다
2. `solution.py` 의 세 함수를 구현한다
3. 채점한다

```
python main.py
```

`sample_input.txt` 를 자동으로 읽는다. 다른 입력을 쓰려면:

```
python main.py 다른입력.txt
python main.py < 다른입력.txt      (리다이렉트도 됨)
```

## 출력 보는 법

다 맞으면 각 테스트 케이스가 배점(100)을 받는다.

```
#1 100
#2 100
#3 100
#4 100
#5 100
```

그 테스트 케이스의 `move` 중 **하나라도 틀리면 그 케이스는 0점**이다.

```
#1 100
#2 0        <- 2번 케이스 안에서 틀린 move 가 있다
#3 100
```

지금은 `solution.py` 가 빈 함수라 전부 0 이 나온다.

## 어디서 틀렸는지 보기

`main.py` 가 stderr 로 move 별 결과를 찍는다.

```
python main.py 2> err.txt
```

`err.txt` 에 이렇게 남는다.

```
move(start=3 end=2 via=[]) -> got=27 expected=27  OK
move(start=1 end=4 via=[2]) -> got=51 expected=44  MISMATCH
```

## 입력 형식

```
T MARK              테스트 케이스 수, 배점
Q                   그 케이스의 명령 수 (25개)
100 N                             init(N)
200 mID mX mY mW mH mDoorX mDoorY build(...)
300 mStart mEnd M (mID x M) 정답  move(...) 결과가 '정답' 과 같아야 한다
```

## 막히면

상위 폴더(`..`)의 `solution.py` 가 정답이다. **충분히 시도한 뒤에 보라.**
