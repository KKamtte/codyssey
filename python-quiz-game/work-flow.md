# 작업 순서 (Work Flow)

QUIZ.md 과제를 완료하기 위한 단계별 작업 순서. 각 단계는 QUIZ.md의 "Git: ~ 후 커밋한다" 지시를 그대로 커밋 단위로 매핑했다.
최종적으로 최소 10개 이상의 의미 있는 커밋, 브랜치 생성/병합 1회 이상, clone/pull 각 1회 이상, git 기초 명령어 7종(init, add, commit, push, pull, checkout, clone) 사용이 목표다.

## 0단계. 저장소 준비
- [x] `README.md` 초안 생성 (틀만 먼저, 내용은 마지막 단계에서 채움)
- [x] 커밋: `feat: 퀴즈 게임 프로젝트 초기 설정 (.gitignore, README 뼈대)`

## 1단계. 메뉴 기능
- [x] `main.py`에서 메뉴 출력 (`1.퀴즈 풀기 2.퀴즈 추가 3.퀴즈 목록 4.점수 확인 5.종료`)
- [x] 사용자 입력을 받아 분기 처리 (기능은 아직 stub이어도 됨)
- [x] 잘못된 입력 처리(공백 제거, 숫자 변환 실패, 범위 밖, 빈 입력 → 재입력)
- [x] `KeyboardInterrupt`/`EOFError` 처리 (안전 종료)
- [x] 커밋: `feat: 메뉴 및 공통 입력 처리 구현`

## 2단계. Quiz 클래스
- [x] `Quiz` 클래스 정의 (속성: question, choices(4개), answer(1~4))
- [x] 메서드: 퀴즈 출력(`display`), 정답 확인(`check_answer`), 직렬화(`to_dict`/`from_dict`) 등
- [x] 커밋: `feat: Quiz 클래스 작성`
- [x] `quiz.py`로 분리해 `main.py` 가독성 확보
- [x] 커밋: `refactor: Quiz 클래스를 quiz.py로 분리`

## 3단계. 기본 퀴즈 데이터 (주제: 파이썬 기본 문법)
- [x] 본인이 선택한 주제로 퀴즈 5개 이상 작성 (문제/선택지 4개/정답) — 6개 작성
- [x] `Quiz` 인스턴스로 기본 데이터 목록 구성 (`main.py`의 `DEFAULT_QUIZZES`)
- [x] 커밋: `feat: 기본 퀴즈 데이터 추가`

## 4단계. QuizGame 클래스 뼈대
- [x] `QuizGame` 클래스 정의 (속성: 퀴즈 목록, 최고 점수) — `quiz_game.py`
- [x] 메서드 뼈대: `show_menu`, `get_menu_choice`, `play_quiz`, `add_quiz`, `list_quizzes`, `show_score`, `save`, `load`, `run`
- [x] `main.py`는 `QuizGame` 생성 및 실행만 담당하는 진입점으로 정리
- [x] 커밋: `refactor: QuizGame 클래스 구조 정리`

## 5단계. 퀴즈 풀기 기능 (브랜치 활용)
- [x] `git checkout -b feat/play-quiz` 로 새 브랜치 생성
- [x] 퀴즈 출제 → 정답 입력 → 정답/오답 표시 → 전체 결과 표시
- [x] 퀴즈가 없는 경우 처리
- [x] 커밋: `feat: 퀴즈 풀기 기능 구현` (브랜치 내에서)
- [x] `git checkout main` → `git merge feat/play-quiz` 로 병합
- [x] 병합 커밋 push

## 6단계. 퀴즈 추가 기능
- [x] 문제/선택지 4개/정답 번호 입력받기
- [x] 공통 입력 예외 처리 적용 (`_read_text`, `_read_choice` 재사용)
- [x] 추가 후 파일에 저장 (`self.save()` 호출 — 실제 저장 로직은 9단계에서 구현)
- [x] 커밋: `feat: 퀴즈 추가 기능 구현`

## 7단계. 퀴즈 목록 기능
- [x] 등록된 퀴즈 목록 출력
- [x] 퀴즈 없는 경우 처리
- [x] 커밋: `feat: 퀴즈 목록 기능 구현`

## 8단계. 점수 확인 기능
- [x] 최고 점수 표시
- [x] 퀴즈 풀 때마다 최고 점수 비교/갱신 후 저장 (`play_quiz`에서 `self.save()` 호출 — 실제 저장은 9단계)
- [x] 아직 안 푼 경우 처리 (`best_score` 초기값을 `0`이 아닌 `None`으로 변경해 "0점"과 "안 풀었음"을 구분)
- [x] 커밋: `feat: 점수 확인 기능 구현`

## 9단계. 파일 저장/불러오기 (state.json)
- [x] `state.json`에 quizzes, best_score UTF-8로 저장 (`save`, 프로젝트 루트 경로 고정)
- [x] 프로그램 시작 시 불러오기 (`main.py`에서 `game.load()` 호출)
- [x] 파일 없음 → 기본 데이터 사용 (`load`가 조용히 반환, `__init__`의 기본값 유지)
- [x] 파일 손상 → try/except로 안내 후 기본 데이터로 초기화
- [x] `KeyboardInterrupt`/`EOFError` 발생 시에도 `game.save()` 호출해 종료 전 저장
- [x] 커밋: `feat: state.json 저장/불러오기 기능 구현`

## 10단계. 통합 테스트 및 리팩터링
- [x] 전체 시나리오 통합 테스트 수행:
  - 최초 실행(state.json 없음) → 목록(6개) → 추가(7개) → 점수 확인(안 푼 상태) → 플레이(전부 정답, 100점, 최고점수 갱신) → 점수 확인
  - 재실행 → 데이터 유지 확인(퀴즈 7개, 최고점수 100점 그대로 로드)
  - 더 낮은 점수로 재도전 → 최고점수가 덮어써지지 않는지 확인(100점 유지)
  - `main.py` 진입점을 통한 전체 메뉴(1~5) e2e 시나리오, 잘못된 메뉴/정답 입력(공백/문자/범위밖/빈값) 재입력 흐름 확인
  - `python -m py_compile`로 전체 파일 컴파일 확인
- [x] 코드 리뷰 결과: 실제 버그나 리팩터링이 필요한 중복/불일치 코드를 발견하지 못함 (기존 `_read_choice`/`_read_text` 공통화로 이미 정리되어 있었음) — **수정 사항 없음**
- [x] 설계 개선(사용자 지적): 퀴즈 개수가 늘어난 뒤 다시 만점을 받으면 이전 만점 기록과 동점 처리되는 문제를 검토. 점수 비교 자체는 그대로 퍼센트 기준을 유지하되(개수만으로 비교하면 오히려 더 불공평해짐), 최고 기록 갱신 시점의 "맞춘 문제 수/전체 문제 수" 스냅샷을 `best_correct_count`/`best_total`로 별도 저장하도록 변경
  - `QuizGame.__init__`에 `best_correct_count`, `best_total` 속성 추가
  - `play_quiz`에서 최고 점수 갱신 시 두 값도 함께 갱신
  - `show_score`/`load` 출력 문구를 "N문제 중 M문제 정답"까지 보여주도록 수정
  - `save`/`load`가 `state.json`에 두 필드를 함께 저장/복원하도록 수정 (기존 `data.get(...)` 패턴이라 이전 스키마 파일도 안전하게 처리됨)
  - 6문제 만점 → 문제 추가 후 7문제 만점(동점) → 재로드 → 손상 파일 시나리오까지 재테스트, 모두 정상 동작 확인
- [x] 설계 개선(사용자 지적, 2차): 퍼센트가 같을 때 "더 많은 문제 중에서 받은 만점"을 우대하도록 동점자 처리 규칙 추가
  - `play_quiz`의 갱신 조건에 `score == self.best_score and total > self.best_total` 케이스 추가 (`is_new_best` 변수로 가독성 유지)
  - 시나리오: 6/6(100점) → 7/7(100점, total이 더 커서 갱신됨) → 다시 7/7(완전 동일이라 유지됨) 순서로 재테스트, 의도대로 동작 확인
- [x] 커밋: (수정 사항이 없어 테스트 확인만 진행, 별도 fix/refactor 커밋 불필요 — 필요 시 `test:` 또는 메모 성격의 커밋으로 기록 가능)

## 11단계. README 작성
- [ ] 프로젝트 개요
- [ ] 퀴즈 주제 선정 이유
- [ ] 실행 방법 (`python main.py`)
- [ ] 기능 목록
- [ ] 파일 구조
- [ ] 데이터 파일 설명 (state.json 경로/역할/스키마)
- [ ] 스크린샷 경로 안내 (`docs/screenshots/menu.png`, `play.png`, `add_quiz.png`, `score.png`)
- 커밋: `docs: README 작성`
- `git push`로 최종 반영

## 12단계. Git 저장소 복제 실습 (clone & pull)
- [ ] 별도 디렉터리에 `git clone`으로 저장소 복제
- [ ] 복제된 저장소에서 README에 한 줄 추가 → `git add` → `git commit` → `git push`
- [ ] 기존 작업 디렉터리에서 `git pull`로 변경사항 반영 확인

## 13단계. 제출물 준비
- [ ] GitHub 저장소 URL 정리
- [ ] 개발 환경 스크린샷 (VSCode, Python 버전, Git 설정)
- [ ] 프로그램 실행 스크린샷 (추가/목록/플레이/점수)
- [ ] `git log --oneline --graph` 결과 스크린샷
- [ ] (선택) 보너스 과제: 랜덤 출제, 문제 수 선택, 힌트, 퀴즈 삭제, 점수 히스토리
