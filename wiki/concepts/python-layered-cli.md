---
title: 콘솔 프로그램의 계층 구조, dataclass, 타입 힌트
updated: 2026-11-25
sources: []
---

[[b2-1]]에서 배운 것. 과제 목표 "클래스/모듈로 구조화하고 각 계층(모델/저장소/서비스/CLI)의 책임", "타입 힌트로 입출력 계약을 명확히". 문답은 [[b2-1-review-qa]] Q1·Q5·Q6.

## 계층과 책임
호출은 한 방향: **CLI → 서비스 → 저장소 → 파일**. 모델은 모두가 같이 쓴다.

| 계층 | 맡는 것 | 하지 않는 것 |
|---|---|---|
| CLI (`cli.py`) | 명령·옵션 해석, 입력 받기, 결과 출력 | 계산·규칙 판단 |
| 서비스 (`services.py`) | 규칙: 등록된 카테고리만, id 발급, 사용 중 카테고리 막기, 요약 계산 | 파일 직접 열기 |
| 저장소 (`storage.py`) | JSONL 읽기·추가·원자적 교체 | 규칙 |
| 모델 (`models.py`) | 데이터 모양(dataclass), 검증 함수 `parse_*` | 입출력 |

- 규칙을 서비스 **한 곳**에 두면 입구(대화형 add, CSV import, recurring apply)가 몇 개든 같은 규칙을 탄다. CLI 에 두면 입구마다 복사본이 생기고, 하나라도 빠뜨리면 그 입구로 잘못된 데이터가 들어온다 (예: import 로 등록 안 된 카테고리가 저장됨).
- 검증도 마찬가지: `parse_date`·`parse_amount` 하나를 add(대화형), update(옵션), import(CSV)가 같이 쓴다.

## frozen dataclass 와 replace
```python
@dataclass(frozen=True)
class Transaction:
    id: str; type: TxType; date: str; amount: int; category: str
    memo: str = ""; tags: tuple[str, ...] = ()

new = replace(old, amount=20000)   # old 를 고치지 않고 새 객체를 만든다
```
- `frozen=True`면 `old.amount = 1` 같은 대입이 `FrozenInstanceError`. 어디서도 실수로 거래를 바꿀 수 없다.
- 수정은 `replace`로 새 객체를 만들므로 old 가 남아 "amount 15,000 → 20,000"처럼 전·후를 비교할 수 있다.

## 타입 힌트
```python
def parse_amount(text: str | int) -> int                                   # 검증된 양의 정수를 돌려준다
def stream(self) -> Iterator[Transaction]                                  # 리스트가 아니라 하나씩 나온다
def update_where(self, change: Callable[[Transaction], Transaction | None]) -> int   # None 이면 삭제라는 약속
TxType = Literal["income", "expense"]
```
- 함수 한 줄로 "무엇을 넘기고 무엇을 받는지"의 계약이 보인다. 주석과 달리 코드가 바뀌면 같이 바뀐다.
- **실행 때 막아 주지는 않는다.** 에디터나 `mypy` 같은 검사 도구가 실행 전에 잘못된 호출을 알려 주는 것이 이점이다.
- `X | None` 문법은 Python 3.10 부터 실행 시에도 된다 (과제 최소 버전 3.10).

## 관련
- 같은 "역할 나누기"를 React 에서는 컴포넌트·훅으로 했다: [[react-component-props-state]]
- 저장소 계층이 쓰는 기법: [[python-generator-streaming]], [[atomic-file-write]]
- 계층을 가로지르는 공통 처리: [[python-decorator-cross-cutting]]
