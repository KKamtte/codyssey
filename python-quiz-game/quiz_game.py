from quiz import Quiz

MENU_PLAY = 1
MENU_ADD = 2
MENU_LIST = 3
MENU_SCORE = 4
MENU_EXIT = 5

DEFAULT_QUIZZES = [
    Quiz(
        "다음 중 정수(int)형 데이터는?",
        ["'10'", "10", "10.0", "True"],
        2,
    ),
    Quiz(
        "다음 중 문자열(str) 타입인 것은?",
        ["10", "3.14", "'Hello'", "True"],
        3,
    ),
    Quiz(
        "for문과 while문에 대한 설명으로 옳은 것은?",
        [
            "for문은 반복 횟수를 알 수 없을 때만 사용한다",
            "while문은 정해진 반복 횟수가 있을 때만 사용한다",
            "for문은 주로 리스트 등 순회 가능한 객체를 반복할 때 사용한다",
            "for문과 while문은 완전히 동일하게 동작한다",
        ],
        3,
    ),
    Quiz(
        "파이썬에서 함수를 정의할 때 사용하는 키워드는?",
        ["func", "def", "function", "define"],
        2,
    ),
    Quiz(
        "클래스의 __init__ 메서드가 하는 역할은?",
        [
            "클래스를 삭제한다",
            "객체가 생성될 때 초기값을 설정한다",
            "클래스의 이름을 반환한다",
            "반복문을 실행한다",
        ],
        2,
    ),
    Quiz(
        "list와 dict의 차이로 옳은 것은?",
        [
            "list는 key-value 쌍으로 이루어져 있다",
            "dict는 순서가 있는 인덱스로만 접근할 수 있다",
            "list는 순서가 있는 값들의 모음이고, dict는 key-value 쌍의 모음이다",
            "list와 dict는 동일한 자료구조이다",
        ],
        3,
    ),
]


class QuizGame:
    def __init__(self, quizzes=None, best_score=0):
        self.quizzes = quizzes if quizzes is not None else list(DEFAULT_QUIZZES)
        self.best_score = best_score

    def show_menu(self):
        print("=" * 40)
        print("        🎯 나만의 퀴즈 게임 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def get_menu_choice(self):
        return self._read_choice("선택: ", MENU_PLAY, MENU_EXIT)

    def _read_choice(self, prompt, min_value, max_value):
        while True:
            raw = input(prompt).strip()

            if raw == "":
                print(f"⚠️ 빈 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            if not raw.isdigit():
                print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            choice = int(raw)
            if choice < min_value or choice > max_value:
                print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            return choice

    def _read_text(self, prompt):
        while True:
            raw = input(prompt).strip()
            if raw == "":
                print("⚠️ 빈 입력입니다. 값을 입력해주세요.")
                continue
            return raw

    def play_quiz(self):
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
            return

        total = len(self.quizzes)
        print(f"📝 퀴즈를 시작합니다! (총 {total}문제)")

        correct_count = 0
        for index, quiz in enumerate(self.quizzes, start=1):
            print("-" * 40)
            quiz.display(index)
            print()
            selected = self._read_choice("정답 입력: ", 1, len(quiz.choices))

            if quiz.check_answer(selected):
                print("✅ 정답입니다!")
                correct_count += 1
            else:
                print(f"❌ 오답입니다. (정답: {quiz.answer}번)")

        score = round(correct_count / total * 100)
        print("=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")
        if score > self.best_score:
            self.best_score = score
            print("🎉 새로운 최고 점수입니다!")
        print("=" * 40)

    def add_quiz(self):
        print("📌 새로운 퀴즈를 추가합니다.")
        print()

        question = self._read_text("문제를 입력하세요: ")
        choices = []
        for i in range(1, 5):
            choices.append(self._read_text(f"선택지 {i}: "))
        answer = self._read_choice("정답 번호 (1-4): ", 1, 4)

        self.quizzes.append(Quiz(question, choices, answer))
        self.save()
        print("✅ 퀴즈가 추가되었습니다!")

    def list_quizzes(self):
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다.")
            return

        print(f"📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print()
        print("-" * 40)
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"[{index}] {quiz.question}")
        print("-" * 40)

    def show_score(self):
        # 8단계에서 구현 예정
        print("🏆 점수 확인 기능은 아직 준비 중입니다.")

    def save(self):
        # 9단계에서 구현 예정 (state.json 저장)
        pass

    def load(self):
        # 9단계에서 구현 예정 (state.json 불러오기)
        pass

    def run(self):
        while True:
            self.show_menu()
            choice = self.get_menu_choice()

            if choice == MENU_PLAY:
                self.play_quiz()
            elif choice == MENU_ADD:
                self.add_quiz()
            elif choice == MENU_LIST:
                self.list_quizzes()
            elif choice == MENU_SCORE:
                self.show_score()
            elif choice == MENU_EXIT:
                print("👋 게임을 종료합니다.")
                break