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