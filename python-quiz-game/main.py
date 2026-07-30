MENU_PLAY = 1
MENU_ADD = 2
MENU_LIST = 3
MENU_SCORE = 4
MENU_EXIT = 5


class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self, index):
        print(f"[문제 {index}]")
        print(self.question)
        print()
        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")

    def check_answer(self, selected):
        return selected == self.answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["question"], data["choices"], data["answer"])


def show_menu():
    print("=" * 40)
    print("        🎯 나만의 퀴즈 게임 🎯")
    print("=" * 40)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("=" * 40)


def get_menu_choice():
    while True:
        raw = input("선택: ").strip()

        if raw == "":
            print("⚠️ 빈 입력입니다. 1-5 사이의 숫자를 입력하세요.")
            continue

        if not raw.isdigit():
            print("⚠️ 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.")
            continue

        choice = int(raw)
        if choice < MENU_PLAY or choice > MENU_EXIT:
            print("⚠️ 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.")
            continue

        return choice


def play_quiz():
    print("📝 퀴즈 풀기 기능은 아직 준비 중입니다.")


def add_quiz():
    print("📌 퀴즈 추가 기능은 아직 준비 중입니다.")


def list_quizzes():
    print("📋 퀴즈 목록 기능은 아직 준비 중입니다.")


def show_score():
    print("🏆 점수 확인 기능은 아직 준비 중입니다.")


def run():
    while True:
        show_menu()
        choice = get_menu_choice()

        if choice == MENU_PLAY:
            play_quiz()
        elif choice == MENU_ADD:
            add_quiz()
        elif choice == MENU_LIST:
            list_quizzes()
        elif choice == MENU_SCORE:
            show_score()
        elif choice == MENU_EXIT:
            print("👋 게임을 종료합니다.")
            break


def main():
    try:
        run()
    except (KeyboardInterrupt, EOFError):
        print("\n👋 입력이 중단되어 안전하게 종료합니다.")


if __name__ == "__main__":
    main()