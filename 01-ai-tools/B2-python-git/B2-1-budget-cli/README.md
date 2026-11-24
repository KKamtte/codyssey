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
- [ ] `python -m budget_app <command> [options]`로 실행
- [ ] 모든 명령에 `--help`
- [ ] `add`는 대화형 입력(`input()`), 나머지(`list`·`search`·`summary`·`export`·`import`·`delete`)는 옵션 방식 허용
- [ ] `update`는 옵션 방식과 대화형 중 하나로 고정하고 문서에 적기
- [ ] 옵션 표기는 `--`로 통일

### 데이터 모델
- [ ] 거래(Transaction): `id`(유일), `type`(income/expense), `date`(YYYY-MM-DD), `amount`(양수), `category`, `memo`(선택), `tags`(선택)
- [ ] `dataclass` 또는 그에 준하는 구조, 클래스 2개 이상
- [ ] 입력 검증: 날짜 형식, 음수·0 금액, 잘못된 type, 없는 category는 재입력 또는 오류 메시지

### 저장
- [ ] JSONL 또는 CSV 중 하나, 파일 3개 이상(`transactions`·`categories`·`budgets`)
- [ ] 기본 폴더 `./data`, 옵션으로 변경(`--data-dir`)
- [ ] 파일이 없을 때 자동 생성 또는 안내, 카테고리가 비었을 때 동작을 정해 두기
- [ ] `update`·`delete`는 전체 재작성·임시 파일·원자적 교체 등 안정성 고려

### 명령
- [ ] `add`: 대화형으로 입력해 저장, 등록된 카테고리만, 저장 후 `id` 출력
- [ ] `list`: 최신순, `--limit N`(기본값 있음), 제너레이터 스트리밍
- [ ] `update`·`delete --id`: 없는 id는 "없는 데이터" 메시지
- [ ] `search`: `--from`·`--to`·`--category`·`--type`·`--q`(메모)·`--tag`, 최신순, 스트리밍 유지
- [ ] `summary --month YYYY-MM`: 총수입·총지출·잔액, 카테고리별 지출 TOP N(`--top`), 데이터 없는 달은 "데이터 없음"
- [ ] `budget set --month --amount`: 영구 저장, `summary`에 사용률(%)과 초과 경고
- [ ] `category add/list/remove`: 사용 중인 카테고리 삭제는 막거나 대체 카테고리 요구
- [ ] `import --from <csv>`, `export --out <csv>`(`--month` 또는 `--from`/`--to` 필수), CSV 스키마 고정(아래)

### 구조와 오류 처리
- [ ] 데코레이터 1개 이상(예외 처리·로그·시간 측정 등)을 실제로 적용
- [ ] 스택트레이스 대신 원인 + 해결 힌트, 정상 종료 0 / 오류 종료 0이 아님
- [ ] 모듈 3개 이상(권장: CLI / 서비스 / 저장소 / 모델)

### 보너스 (선택, 전부 하기로 함)
- [ ] `backup`: 타임스탬프가 붙은 백업 파일 생성
- [ ] 반복 내역: 월급·월세 같은 반복 규칙을 등록하고 특정 월에 자동 생성
- [ ] 출력 테이블 정렬: 외부 라이브러리 없이 문자열 정렬
- [ ] 저장 원자성: 임시 파일에 쓰고 rename으로 교체

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
- (구현하면서 채운다: 실행 방법, 저장 파일 위치·형식, 명령 예시, 구조, 주요 결정과 이유)

## 회고
- (완료 후 작성)
