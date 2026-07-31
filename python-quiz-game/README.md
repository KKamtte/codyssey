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
- **속성**: `quizzes`(`Quiz` 목록), `best_score`(최고 점수, 아직 한 번도 안 풀었으면 `None`)
- **메서드**: `show_menu`/`get_menu_choice`(메뉴 출력·입력), `play_quiz`/`add_quiz`/`list_quizzes`/`show_score`(각 기능), `save`/`load`(state.json 입출력), `run`(메인 루프)
- **`_read_choice(self, prompt, min_value, max_value)`**: 숫자 입력 공통 검증 로직(공백 제거, 숫자 변환 실패, 범위 밖, 빈 입력 처리 후 재입력)을 담당하는 내부 헬퍼. `get_menu_choice`(메뉴 선택)와 `play_quiz`(정답 입력)가 이 메서드를 공유해서 사용한다.
- **`_read_text(self, prompt)`**: 텍스트 입력 공통 검증 로직(빈 입력 시 재입력)을 담당하는 내부 헬퍼. `add_quiz`에서 문제/선택지 입력을 받을 때 사용한다.
- **`add_quiz(self)`**: 문제, 선택지 4개, 정답 번호(1~4)를 순서대로 입력받아 `Quiz`를 생성하고 `self.quizzes`에 추가한 뒤 `self.save()`를 호출해 파일에 반영한다.
- **`best_score`가 `0`이 아닌 `None`으로 초기화되는 이유**: 문제를 다 틀려서 받은 "0점"과 "아직 한 번도 안 풀어본 상태"를 구분하기 위함이다. `play_quiz`는 `self.best_score is None or score > self.best_score` 조건으로 최고 점수 갱신 여부를 판단하고, `show_score`는 `best_score is None`이면 "아직 퀴즈를 푼 기록이 없습니다"를 출력한다.
- **`save(self)` / `load(self)`**: `state.json` 저장·불러오기를 담당한다. 자세한 내용은 아래 [데이터 파일 설명](#데이터-파일-설명-statejson) 참고.

## 데이터 파일 설명 (state.json)
- **경로**: 프로젝트 루트의 `state.json` (`quiz_game.py` 파일 위치 기준 `Path(__file__).resolve().parent`로 계산해서, 어느 위치에서 `python main.py`를 실행해도 항상 프로젝트 루트에 저장/조회한다.)
- **역할**: 등록된 퀴즈 목록과 최고 점수를 저장해, 프로그램을 종료했다가 다시 실행해도 데이터가 유지되게 한다.
- **필드 구조**:
  ```json
  {
    "quizzes": [
      { "question": "문제", "choices": ["선택지1", "선택지2", "선택지3", "선택지4"], "answer": 1 }
    ],
    "best_score": 80
  }
  ```
  `best_score`는 아직 한 번도 퀴즈를 풀지 않았다면 `null`이다.
- **저장 시점**: 퀴즈 추가(`add_quiz`), 새 최고 점수 달성(`play_quiz`), `Ctrl+C`/`Ctrl+D` 등으로 중단될 때(`main.py`) — 상태가 바뀔 때마다 저장한다.
- **불러오기**: `main.py`가 시작할 때 `game.load()`를 호출한다. 파일이 없으면 `QuizGame.__init__`에서 이미 설정한 기본 퀴즈 데이터를 그대로 사용한다. 파일 내용이 JSON으로 파싱되지 않거나 필요한 키가 없는 등 손상된 경우에는 안내 메시지를 출력하고 기본 퀴즈 데이터로 초기화한다.
- **인코딩**: UTF-8 (`open(..., encoding="utf-8")`), 한글 문제/선택지도 깨지지 않고 그대로 저장된다.

## 실행 화면 스크린샷
- docs/screenshots/menu.png
- docs/screenshots/play.png
- docs/screenshots/add_quiz.png
- docs/screenshots/score.png