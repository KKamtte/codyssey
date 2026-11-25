---
title: 데코레이터로 공통 관심사 분리 (예외 처리, 로그, 종료 코드)
updated: 2026-11-25
sources: []
---

[[b2-1]]에서 배운 것. 과제 목표 "데코레이터로 공통 관심사(로그/예외/시간 측정)를 분리한 구조와 이유". 문답은 [[b2-1-review-qa]] Q4·Q8.

## 데코레이터
- 함수를 받아 "앞뒤에 일을 덧붙인 새 함수"를 돌려주는 함수. `@deco`는 `func = deco(func)`와 같다.
- `functools.wraps`를 붙여야 감싼 함수의 이름·설명이 원래 것으로 남는다.

```python
def handle_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AppError as e:            # 앱이 던진 오류: 원인 + 힌트 + 종료 코드
            print_error(e.message, e.hint); return e.exit_code
        except Exception as e:           # 예상 못 한 오류: 화면엔 스택트레이스 없이, 로그에만 남김
            ...; return 1
    return wrapper
```

## 왜 쓰나
- 명령이 12개다. 데코레이터가 없으면 명령마다 try/except 와 시간 재기·로그 코드를 반복해야 하고, 하나라도 빠뜨리면 그 명령만 스택트레이스를 뿜는다.
- 데코레이터로 빼면 명령 함수에는 "그 명령이 할 일"만 남는다.

## 순서가 결과를 바꾼다
```python
@log_execution   # 바깥: 정수(종료 코드)를 돌려받아 app.log 에 "명령 exit=N 시간"
@handle_errors   # 안쪽: 예외를 종료 코드(정수)로 바꿈
def cmd_delete(args): ...
```
- 순서를 바꾸면 예외가 `log_execution`을 그냥 지나가 **로그 한 줄만 조용히 사라진다**(화면 출력·종료 코드는 그대로라 알아채기 어렵다). 그래서 "오류로 끝나도 로그에 exit=1 이 남는지"를 테스트로 고정했다.

## 오류 종류와 종료 코드
| 종류 | 예 | 종료 코드 |
|---|---|---|
| 입력·검증 오류, 없는 데이터 | 날짜 형식, 없는 id | 1 |
| 사용법 오류 | 없는 명령 (argparse) | 2 |
| 파일 오류 | 깨진 줄(몇 번째 줄), 권한 | 3 |
| 사용자 중단 | Ctrl+C | 130 |

- 같은 "날짜 형식 오류"라도 **원인이 있는 곳**에 맞춘다. 입력이면 다시 묻거나 1, 파일에 저장된 줄이면 줄 번호와 함께 3. 그래서 파일을 읽을 때 난 검증 오류는 `ValueError`로 바꿔 저장소가 파일 오류로 감싸게 했다.
- 셸에서는 `$?`로 종료 코드를 보고, 0 이 아니면 다음 명령을 멈추는 식으로 스크립트가 판단한다.

## 관련
- 데코레이터가 감싸는 명령 함수들이 어느 계층에 있는지: [[python-layered-cli]]
