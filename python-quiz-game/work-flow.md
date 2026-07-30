# 작업 순서 (Work Flow)

QUIZ.md 과제를 완료하기 위한 단계별 작업 순서. 각 단계는 QUIZ.md의 "Git: ~ 후 커밋한다" 지시를 그대로 커밋 단위로 매핑했다.
최종적으로 최소 10개 이상의 의미 있는 커밋, 브랜치 생성/병합 1회 이상, clone/pull 각 1회 이상, git 기초 명령어 7종(init, add, commit, push, pull, checkout, clone) 사용이 목표다.

## 0단계. 저장소 준비
- [ ] `README.md` 초안 생성 (틀만 먼저, 내용은 마지막 단계에서 채움)
- 커밋: `Feat: 프로젝트 초기 설정 (.gitignore, README 뼈대)`
- `git push`로 원격에 첫 push

## 1단계. 메뉴 기능
- [ ] `main.py`에서 메뉴 출력 (`1.퀴즈 풀기 2.퀴즈 추가 3.퀴즈 목록 4.점수 확인 5.종료`)
- [ ] 사용자 입력을 받아 분기 처리 (기능은 아직 stub이어도 됨)
- [ ] 잘못된 입력 처리(공백 제거, 숫자 변환 실패, 범위 밖, 빈 입력 → 재입력)
- [ ] `KeyboardInterrupt`/`EOFError` 처리 (안전 종료)
- 커밋: `Feat: 메뉴 및 공통 입력 처리 구현`

## 2단계. Quiz 클래스
- [ ] `Quiz` 클래스 정의 (속성: question, choices(4개), answer(1~4))
- [ ] 메서드: 퀴즈 출력(`display`), 정답 확인(`check_answer`) 등
- 커밋: `Feat: Quiz 클래스 작성`

## 3단계. 기본 퀴즈 데이터
- [ ] 본인이 선택한 주제로 퀴즈 5개 이상 작성 (문제/선택지 4개/정답)
- [ ] `Quiz` 인스턴스로 기본 데이터 목록 구성
- 커밋: `Feat: 기본 퀴즈 데이터 추가`

## 4단계. QuizGame 클래스 뼈대
- [ ] `QuizGame` 클래스 정의 (속성: 퀴즈 목록, 최고 점수)
- [ ] 메서드 뼈대: `show_menu`, `play_quiz`, `add_quiz`, `list_quizzes`, `show_score`, `save`, `load`
- 커밋: `Refactor: QuizGame 클래스 구조 정리`

## 5단계. 퀴즈 풀기 기능 (브랜치 활용)
- [ ] `git checkout -b feature/play-quiz` 로 새 브랜치 생성
- [ ] 퀴즈 출제 → 정답 입력 → 정답/오답 표시 → 전체 결과 표시
- [ ] 퀴즈가 없는 경우 처리
- 커밋: `Feat: 퀴즈 풀기 기능 구현` (브랜치 내에서)
- `git checkout main` → `git merge feature/play-quiz` 로 병합
- 병합 커밋 push

## 6단계. 퀴즈 추가 기능
- [ ] 문제/선택지 4개/정답 번호 입력받기
- [ ] 공통 입력 예외 처리 적용
- [ ] 추가 후 파일에 저장
- 커밋: `Feat: 퀴즈 추가 기능 구현`

## 7단계. 퀴즈 목록 기능
- [ ] 등록된 퀴즈 목록 출력
- [ ] 퀴즈 없는 경우 처리
- 커밋: `Feat: 퀴즈 목록 기능 구현`

## 8단계. 점수 확인 기능
- [ ] 최고 점수 표시
- [ ] 퀴즈 풀 때마다 최고 점수 비교/갱신 후 저장
- [ ] 아직 안 푼 경우 처리
- 커밋: `Feat: 점수 확인 기능 구현`

## 9단계. 파일 저장/불러오기 (state.json)
- [ ] `state.json`에 quizzes, best_score UTF-8로 저장
- [ ] 프로그램 시작 시 불러오기
- [ ] 파일 없음 → 기본 데이터 사용
- [ ] 파일 손상 → try/except로 안내 후 기본 데이터로 초기화
- 커밋: `Feat: state.json 저장/불러오기 기능 구현`

## 10단계. 통합 테스트 및 리팩터링
- [ ] 전체 시나리오 수동 테스트 (풀기/추가/목록/점수/종료, 잘못된 입력, 재실행 후 유지 확인)
- [ ] 필요 시 책임 분리 리팩터링
- 커밋: `Fix: 예외 처리 보완` / `Refactor: 입력 검증 로직 분리` 등 (필요한 만큼 여러 커밋으로 분리해 10개 이상 채우기)

## 11단계. README 작성
- [ ] 프로젝트 개요
- [ ] 퀴즈 주제 선정 이유
- [ ] 실행 방법 (`python main.py`)
- [ ] 기능 목록
- [ ] 파일 구조
- [ ] 데이터 파일 설명 (state.json 경로/역할/스키마)
- [ ] 스크린샷 경로 안내 (`docs/screenshots/menu.png`, `play.png`, `add_quiz.png`, `score.png`)
- 커밋: `Docs: README 작성`
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

## 체크리스트 (Git 명령어 7종 사용 확인)
- [ ] init
- [ ] add
- [ ] commit
- [ ] push
- [ ] pull
- [ ] checkout
- [ ] clone