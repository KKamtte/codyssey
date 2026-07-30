# 나만의 퀴즈 게임 (Python Quiz Game)

## 프로젝트 개요
(작성 예정 — 프로젝트가 무엇을 하는지, 어떤 학습 목적으로 만들었는지 요약)

## 퀴즈 주제 선정 이유
(작성 예정 — 어떤 주제를 선택했고 왜 선택했는지)

## 실행 방법
```bash
python main.py
```

## 기능 목록
- 퀴즈 풀기
- 퀴즈 추가
- 퀴즈 목록 보기
- 점수 확인
- 종료

## 파일 구조
(작성 예정)

## 코드 구조

### Quiz 클래스 (`quiz.py`)
퀴즈 문제 하나를 표현하는 클래스. 문제 하나하나가 이 클래스의 인스턴스(객체)가 된다.

- **속성**: `question`(문제), `choices`(선택지 4개, 리스트), `answer`(정답 번호)
- **`__init__(self, question, choices, answer)`**: 객체 생성 시 호출되는 생성자. 전달받은 값을 `self.question`처럼 객체 속성으로 저장한다.
- **`display(self, index)`**: 문제 번호와 문제 본문, 선택지를 `1. ~`, `2. ~` 형태로 화면에 출력한다.
- **`check_answer(self, selected)`**: 사용자가 입력한 번호(`selected`)와 저장된 정답(`self.answer`)을 비교해 `True`/`False`를 반환한다. 실제 정답 처리와 점수 계산은 이 반환값을 받아 `QuizGame`에서 수행한다.
- **`to_dict(self)`**: `Quiz` 객체를 `{"question": ..., "choices": [...], "answer": ...}` 형태의 딕셔너리로 변환한다. 파이썬 객체는 그대로 JSON에 저장할 수 없기 때문에, `state.json`에 저장하기 전 이 메서드로 변환한다.
- **`from_dict(cls, data)`**: `to_dict()`의 반대 동작. `state.json`에서 읽어온 딕셔너리를 다시 `Quiz` 객체로 복원하는 클래스 메서드(`@classmethod`)다.

### QuizGame 클래스 (`quiz_game.py`)
게임 전체(메뉴 진행, 퀴즈 관리, 점수 관리, 파일 저장/불러오기)를 책임지는 클래스. `main.py`는 이 클래스를 생성해 `run()`을 호출하는 진입점 역할만 한다.
- **속성**: `quizzes`(`Quiz` 목록), `best_score`(최고 점수)
- **메서드**: `show_menu`/`get_menu_choice`(메뉴 출력·입력), `play_quiz`/`add_quiz`/`list_quizzes`/`show_score`(각 기능), `save`/`load`(state.json 입출력), `run`(메인 루프)

## 데이터 파일 설명 (state.json)
(작성 예정 — state.json 경로, 역할, 필드 구조)

## 실행 화면 스크린샷
- docs/screenshots/menu.png
- docs/screenshots/play.png
- docs/screenshots/add_quiz.png
- docs/screenshots/score.png