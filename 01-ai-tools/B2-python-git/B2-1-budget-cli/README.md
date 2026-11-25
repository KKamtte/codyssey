# B2-1 나만의 용돈 기입장 프로그램 만들기

> 분야: Python과 Git 심화 · 기간: 60시간(필수, 개인 미션) · 상태: 진행중
> 원문: https://usr.codyssey.kr/learning/learningMap?projectNo=136003 → B2-1 (원문 사본: 비공개 `codyssey-mission/B2-1-budget-cli.md`)
> 작업 계획·결정 사항: [wiki/plans/b2-1.md](../../../wiki/plans/b2-1.md)

## 과제 요약

Python 표준 라이브러리만으로 터미널에서 쓰는 가계부 프로그램(`python -m budget_app <명령>`)을 만든다.
수입·지출 거래를 추가·조회·검색·수정·삭제하고, 월별 요약과 예산 초과 경고, 카테고리 관리, CSV 가져오기·내보내기까지 하는 "작은 서비스"다.
데이터는 파일 3개 이상에 영구 저장하고, 파일을 한 번에 읽지 않는 **제너레이터 스트리밍**, 공통 기능을 떼어 낸 **데코레이터**, **타입 힌트**, 모델·저장소·서비스·CLI로 나눈 **모듈 구조**가 평가의 중심이다.

## 요구사항

### 실행과 입력
- [x] `python -m budget_app <command> [options]`로 실행
- [x] 모든 명령에 `--help`
- [x] `add`는 대화형 입력(`input()`), 나머지(`list`·`search`·`summary`·`export`·`import`·`delete`)는 옵션 방식 허용
- [x] `update`는 옵션 방식과 대화형 중 하나로 고정하고 문서에 적기
- [x] 옵션 표기는 `--`로 통일

### 데이터 모델
- [x] 거래(Transaction): `id`(유일), `type`(income/expense), `date`(YYYY-MM-DD), `amount`(양수), `category`, `memo`(선택), `tags`(선택)
- [x] `dataclass` 또는 그에 준하는 구조, 클래스 2개 이상
- [x] 입력 검증: 날짜 형식, 음수·0 금액, 잘못된 type, 없는 category는 재입력 또는 오류 메시지

### 저장
- [x] JSONL 또는 CSV 중 하나, 파일 3개 이상(`transactions`·`categories`·`budgets`)
- [x] 기본 폴더 `./data`, 옵션으로 변경(`--data-dir`)
- [x] 파일이 없을 때 자동 생성 또는 안내, 카테고리가 비었을 때 동작을 정해 두기
- [x] `update`·`delete`는 전체 재작성·임시 파일·원자적 교체 등 안정성 고려

### 명령
- [x] `add`: 대화형으로 입력해 저장, 등록된 카테고리만, 저장 후 `id` 출력
- [x] `list`: 최신순, `--limit N`(기본값 있음), 제너레이터 스트리밍
- [x] `update`·`delete --id`: 없는 id는 "없는 데이터" 메시지
- [x] `search`: `--from`·`--to`·`--category`·`--type`·`--q`(메모)·`--tag`, 최신순, 스트리밍 유지
- [x] `summary --month YYYY-MM`: 총수입·총지출·잔액, 카테고리별 지출 TOP N(`--top`), 데이터 없는 달은 "데이터 없음"
- [x] `budget set --month --amount`: 영구 저장, `summary`에 사용률(%)과 초과 경고
- [x] `category add/list/remove`: 사용 중인 카테고리 삭제는 막거나 대체 카테고리 요구
- [x] `import --from <csv>`, `export --out <csv>`(`--month` 또는 `--from`/`--to` 필수), CSV 스키마 고정(아래)

### 구조와 오류 처리
- [x] 데코레이터 1개 이상(예외 처리·로그·시간 측정 등)을 실제로 적용
- [x] 스택트레이스 대신 원인 + 해결 힌트, 정상 종료 0 / 오류 종료 0이 아님
- [x] 모듈 3개 이상(권장: CLI / 서비스 / 저장소 / 모델)

### 보너스 (선택, 전부 하기로 함)
- [x] `backup`: 타임스탬프가 붙은 백업 파일 생성
- [x] 반복 내역: 월급·월세 같은 반복 규칙을 등록하고 특정 월에 자동 생성
- [x] 출력 테이블 정렬: 외부 라이브러리 없이 문자열 정렬
- [x] 저장 원자성: 임시 파일에 쓰고 rename으로 교체

## 제약 / 평가 기준
- Python 3.10 이상, **표준 라이브러리만**(`pip install` 금지)
- 저장은 JSONL 또는 CSV 하나, 파일 3개 이상
- 스택트레이스 출력 금지, 오류 종료 코드는 0이 아님
- README에 실행 방법, 저장 파일 위치·형식, 주요 명령 예시, import/export CSV 스키마
- 평가 때 설명할 것: 파일 기반 CRUD·검색·요약·입출력, 계층(모델/저장소/서비스/CLI)의 책임, `yield` 스트리밍의 이유와 동작, 데코레이터로 분리한 공통 관심사, 타입 힌트의 이점

### import/export CSV 스키마 (원문 고정)
| column | required | 설명 |
|---|---|---|
| date | Y | YYYY-MM-DD |
| type | Y | income / expense |
| category | Y | 등록된 카테고리 |
| amount | Y | 양수 정수 |
| memo | N | 문자열 |
| tags | N | 쉼표(,) 구분 문자열 |

공통: UTF-8, 헤더 포함.

## 구현

### 실행 방법
설치할 것이 없다 (Python 3.10 이상, 표준 라이브러리만). 이 폴더에서 실행한다.

```bash
cd 01-ai-tools/B2-python-git/B2-1-budget-cli
python3 -m budget_app --help              # 명령 목록
python3 -m budget_app <command> --help    # 명령별 사용법 (모든 명령에 있음)
python3 -m unittest                       # 테스트 90개
```

- 데이터 폴더는 기본 `./data`. 다른 곳을 쓰려면 `--data-dir 경로` (명령 앞·뒤 어디든)
- 처음 실행하면 데이터 파일을 만들고 기본 카테고리(food, transport, rent, salary, etc)를 넣는다. 카테고리를 모두 지워도 다음 실행 때 다시 만든다 (원문 안 A: "카테고리 파일이 비어있으면 기본 카테고리 생성")

### 명령
| 명령 | 입력 방식 | 하는 일 |
|---|---|---|
| `add` | 대화형 | 날짜(엔터=오늘)·타입·카테고리·금액·메모·태그를 차례로 묻는다. 틀리면 이유를 보여 주고 다시 묻는다 |
| `list [--limit N]` | 옵션 | 최신순 N건 (기본 20) |
| `search [--from] [--to] [--category] [--type] [--q] [--tag] [--limit]` | 옵션 | 조건 검색, 최신순. `--q`는 메모 키워드(대소문자 무시), `--tag`는 정확히 일치 |
| `update --id ID [--date] [--type] [--category] [--amount] [--memo] [--tags]` | **옵션으로 고정** | 준 항목만 바꾼다. `--memo ""`·`--tags ""`는 지우기 |
| `delete --id ID` | 옵션 | 삭제 |
| `summary --month YYYY-MM [--top N]` | 옵션 | 총수입·총지출·잔액, 지출 TOP N, 예산 사용률·초과 경고, 거래 없는 달은 "데이터 없음" |
| `budget set --month --amount` / `budget show [--month]` | 옵션 | 월 예산 저장(같은 달은 덮어씀)·조회 |
| `category add [이름]` / `list` / `remove 이름 [--replace-with 다른것]` | 이름 없으면 대화형 | 사용 중인(거래·반복 규칙) 카테고리는 막고, `--replace-with`면 옮긴 뒤 삭제 |
| `import --from CSV` | 옵션 | 틀린 행은 건너뛰고 행 번호·이유 출력 |
| `export --out CSV (--month \| --from/--to) [--force]` | 옵션 | 날짜순 CSV. 이미 있는 파일은 `--force`일 때만 덮어씀 |
| `backup` | - | `data/backups/YYYYMMDD-HHMMSS/`에 데이터 파일 복사 (보너스) |
| `recurring add` / `list` / `remove --id` / `apply --month` | add 는 대화형 | 반복 내역 (보너스). `apply`는 같은 달에 두 번 만들지 않고, 31일 규칙은 짧은 달의 마지막 날로 |

### 주요 명령 예시
```
$ python3 -m budget_app add
날짜(YYYY-MM-DD, 엔터=오늘 2026-11-25): 2024-13-40
[오류] 날짜 형식이 올바르지 않습니다 (YYYY-MM-DD).
[힌트] 예: 2024-01-15
날짜(YYYY-MM-DD, 엔터=오늘 2026-11-25): 2024-01-15
타입(income/expense): expense
카테고리(food, transport, rent, salary, etc): food
금액(양수): 15000
메모(선택): 점심
태그(쉼표로 구분, 없으면 엔터): meal
[저장 완료] id=TX-000001

$ python3 -m budget_app list --limit 3
ID        | 날짜       | 타입    | 카테고리 |      금액 | 메모 | 태그
----------+------------+---------+----------+-----------+------+-----
TX-000005 | 2024-01-20 | expense | food     |    30,000 |      |
TX-000001 | 2024-01-15 | expense | food     |    15,000 | 점심 | meal
TX-000002 | 2024-01-14 | income  | salary   | 3,000,000 |      |
(5건 중 최신 3건)

$ python3 -m budget_app budget set --month 2024-01 --amount 500000
[저장 완료] 2024-01 예산 500,000원

$ python3 -m budget_app summary --month 2024-01 --top 3
[2024-01 요약]
총 수입: 3,000,000원
총 지출: 215,000원
잔액: 2,785,000원
예산: 500,000원 (사용률 43.0%)

지출 TOP 3
1) rent 150,000원
2) food 45,000원
3) transport 20,000원

$ python3 -m budget_app update --id TX-000001 --amount 20000 --memo "점심 회식"
[수정 완료] TX-000001: amount 15,000 → 20,000, memo 점심 → 점심 회식

$ python3 -m budget_app export --out export.csv --month 2024-01
[완료] export.csv (5 records)

$ python3 -m budget_app import --from import.csv      # 7행 중 4행이 틀린 CSV
[건너뜀] 4행: 날짜 형식이 올바르지 않습니다 (YYYY-MM-DD).
[건너뜀] 5행: 등록되지 않은 카테고리입니다: hobby
[건너뜀] 6행: 타입은 income 또는 expense 여야 합니다: refund
[건너뜀] 7행: 금액은 0보다 커야 합니다.
[완료] imported=3, skipped=4

$ python3 -m budget_app delete --id TX-000099
[오류] 없는 데이터입니다: TX-000099
[힌트] list 나 search 로 id 를 확인하세요.
```

### 저장 파일 위치·형식
모두 `./data/`(또는 `--data-dir`) 아래, **JSONL**(한 줄 = JSON 하나, UTF-8). `data/`는 내 실제 기록이라 git 에 올리지 않는다.

| 파일 | 한 줄 예시 |
|---|---|
| `transactions.jsonl` | `{"id": "TX-000001", "type": "expense", "date": "2024-01-15", "amount": 15000, "category": "food", "memo": "점심", "tags": ["meal"]}` (반복 규칙으로 만든 거래는 `"recurring_id": "RC-000001"`이 더 붙는다) |
| `categories.jsonl` | `{"name": "food"}` |
| `budgets.jsonl` | `{"month": "2024-01", "amount": 500000}` |
| `recurring.jsonl` | `{"id": "RC-000001", "day": 25, "type": "income", "category": "salary", "amount": 3000000, "memo": "월급"}` |
| `app.log` | `2026-11-25T13:40:28	add	exit=0	1.7ms` (명령마다 한 줄. 예상 못 한 오류의 스택트레이스도 여기에만) |
| `backups/YYYYMMDD-HHMMSS/` | `backup` 때 위 JSONL 4개를 복사 |

- import/export CSV 스키마는 위 "제약 / 평가 기준"의 표 그대로 (`date,type,category,amount,memo,tags`, UTF-8, 헤더 포함, tags 는 한 칸에 쉼표로). 엑셀 CSV 의 BOM 도 읽는다.

### 구조
```
budget_app/
├── __main__.py    # python -m budget_app 진입점
├── cli.py         # CLI 계층: argparse 명령·옵션, 입력을 서비스에 넘기고 결과 출력
├── prompts.py     #   대화형 입력: 검증 통과할 때까지 다시 묻기
├── formatting.py  #   표 출력 (한글 2칸 계산, 금액 오른쪽 정렬)
├── decorators.py  # 공통 관심사: @handle_errors, @log_execution
├── errors.py      # AppError 계열과 종료 코드
├── services.py    # 서비스 계층: 규칙(카테고리 확인, id 발급, 사용 중 막기, 요약 계산, import 검증, 반복 내역, 백업)
├── models.py      # 모델: Transaction·Budget·RecurringRule (frozen dataclass), 검증 함수 parse_*
├── storage.py     # 저장소 계층: JSONL 읽기(제너레이터)·추가·원자적 교체
└── csv_io.py      #   CSV 읽기·쓰기 (import/export 의 파일 부분)
tests/             # unittest 90개 (임시 폴더를 --data-dir 로 써서 실제 데이터와 분리)
```

호출은 위에서 아래로만 간다: **CLI → (데코레이터) → 서비스 → 저장소 → 파일**. 모델은 모든 계층이 같이 쓴다.
- CLI 는 계산하지 않는다 (서비스가 돌려준 값을 출력만)
- 서비스는 파일을 직접 열지 않는다 (저장소에 맡김)
- 저장소는 규칙을 모른다 (카테고리가 등록됐는지 같은 건 서비스가 판단)

그래서 같은 규칙을 대화형 `add`, CSV `import`, `recurring apply`가 함께 쓴다 (셋 다 `parse_*` 검증 + `BudgetService.add_transaction` 또는 같은 검증을 거친다).

### 과제 목표별 설명
**1) 파일 기반 저장과 CRUD** — 추가는 파일 끝에 한 줄 `append`. 수정·삭제는 JSONL 중간 한 줄만 고칠 수 없으므로(줄 길이가 다름) 전체를 다시 쓴다. 그 과정이 안전하도록:
- `rewrite()`: 임시 파일에 다 쓰고 → `fsync` → `os.replace`로 바꿔 끼운다. 같은 폴더 안의 rename 은 한 번에 일어나므로, 중간에 죽어도 원본 그대로이거나 완전히 새 파일 둘 중 하나다 (보너스 "저장 원자성"). 실패하면 임시 파일만 지운다
- 바뀐 게 0건이면 교체하지 않고, 원래 파일 권한도 유지한다
- 마지막 줄에 줄바꿈이 빠진 파일에 `append`하면 두 거래가 한 줄로 붙어 깨지므로 먼저 줄바꿈을 채운다
- 파일 내용이 깨졌으면 "transactions.jsonl 3번째 줄"처럼 위치를 알려 주고 종료 코드 3

**2) 제너레이터 스트리밍** — `JsonlFile.stream()`은 `yield`로 한 줄씩 넘긴다. 다음 값을 달라고 할 때까지 멈춰 있으므로 메모리에는 한 건만 있다.
- `list`/`search`의 "최신순"은 원래 전체를 정렬해야 하지만, `heapq.nlargest(N, 제너레이터, key=(날짜, id 번호))`로 **크기 N 인 힙만 유지**하며 한 번 훑는다 → 거래가 몇만 건이어도 메모리에는 N건
- `summary`는 거래를 모으지 않고 합계만 더한다 (메모리에는 카테고리별 합계만)
- 예외: `export`는 날짜순으로 쓰려고 **내보내는 기간의 거래만** 모아 정렬한다

**3) 데코레이터** — 모든 명령 함수에 두 개를 붙였다. 명령 함수 안에는 try/except 도, 로그 코드도 없다.
```python
@log_execution    # 바깥: 명령 이름·종료 코드·걸린 시간을 app.log 에 (오류로 끝나도 종료 코드가 남음)
@handle_errors    # 안쪽: AppError → "[오류] 원인" + "[힌트] 해결 방법" + 종료 코드. 예상 못 한 오류도 스택트레이스 없이
def cmd_add(args): ...
```
종료 코드: 0 정상, 1 입력·검증 오류와 없는 데이터, 2 사용법 오류(argparse), 3 파일 오류, 130 Ctrl+C

**4) 타입 힌트** — 함수가 무엇을 받고 무엇을 돌려주는지 계약이 보인다. 예:
```python
def parse_amount(text: str | int) -> int: ...                   # 문자열을 받아 "검증된 양의 정수"를 돌려준다 (아니면 ValidationError)
def stream(self) -> Iterator[Transaction]: ...                    # 리스트가 아니라 "하나씩 나오는" 것임을 타입이 말해 준다
def update_where(self, change: Callable[[Transaction], Transaction | None]) -> int: ...  # None 을 돌려주면 삭제라는 약속
TxType = Literal["income", "expense"]                             # 두 값 말고는 들어올 수 없다
```

**5) 클래스와 모듈** — 모델 3개(`Transaction`·`Budget`·`RecurringRule`, frozen dataclass: 만든 뒤 바꿀 수 없고 수정은 `replace`로 새 객체), 저장소 클래스(`JsonlFile`·`TransactionRepository`·`CategoryStore`·`BudgetStore`·`RecurringStore`·`Storage`), 서비스 `BudgetService`, 모듈 11개.

### 주요 결정과 이유
| 결정 | 이유 |
|---|---|
| 저장 포맷 JSONL | 한 줄씩 읽는 제너레이터와 맞고, 숫자·태그 목록 타입이 그대로 남는다. CSV 는 import/export 에만 |
| `update`는 옵션 방식으로 고정 | 한 줄로 끝나 테스트·자동화가 쉽고 delete·search 와 사용법이 같다 |
| 사용 중인 카테고리는 삭제를 막고 `--replace-with` 제공 | 거래가 없는 카테고리를 가리키지 않게. 옮길 때는 거래·규칙을 먼저 옮기고 카테고리를 마지막에 지워, 중간에 멈춰도 어긋나지 않음 |
| 처음 실행 때 기본 카테고리 생성 (원문 안 A) | 처음 쓰는 사람이 `add`부터 막히지 않게. 그래서 원문 예시와 달리 `category add food`는 "이미 있는 카테고리"가 된다 |
| id `TX-000001` = 남은 최대 번호 + 1 | 별도 파일 없이 스트리밍으로 구한다. 맨 마지막 거래를 지우면 그 번호가 다시 쓰일 수 있다 (id 를 참조하는 데이터가 없어 문제없음) |
| 금액은 양의 정수, `15,000` 쉼표 허용 | CSV 스키마 "양수 정수"와 맞춤. `1_000`·전각 숫자처럼 `int()`가 받아 주는 이상한 입력은 막는다 |
| 카테고리 이름은 한글·영문·숫자·`_`·`-`만 | `\|`는 표 출력, 앞의 `-`는 명령 옵션, 쉼표는 태그·CSV 와 섞인다 |
| import 는 틀린 행만 건너뜀, 중복 검사 없음 | 원문 출력 `imported=5, skipped=0` 형식대로. 같은 CSV 를 두 번 넣으면 두 번 들어간다 |
| export 는 이미 있는 파일을 `--force` 없이는 덮어쓰지 않음 | 실수로 다른 파일을 지우지 않게 |
| 반복 거래에 `recurring_id` 기록 | `apply`를 몇 번 실행해도 같은 달에 두 번 만들지 않는 근거 |

작업 단계와 결정 전체(19개)는 [wiki/plans/b2-1.md](../../../wiki/plans/b2-1.md).

## 회고
- (완료 후 작성)
