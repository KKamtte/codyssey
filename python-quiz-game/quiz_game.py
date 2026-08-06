import json
import random
from pathlib import Path

from quiz import Quiz

STATE_FILE = Path(__file__).resolve().parent / "state.json"

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
        hint="따옴표로 감싸지 않고, 소수점도 없는 숫자를 찾아보세요.",
    ),
    Quiz(
        "다음 중 문자열(str) 타입인 것은?",
        ["10", "3.14", "'Hello'", "True"],
        3,
        hint="따옴표(' 또는 \")로 감싸진 값을 찾아보세요.",
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
        hint="리스트를 하나씩 순회할 때 어떤 반복문을 주로 쓰는지 떠올려보세요.",
    ),
    Quiz(
        "파이썬에서 함수를 정의할 때 사용하는 키워드는?",
        ["func", "def", "function", "define"],
        2,
        hint="'define'의 줄임말입니다.",
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
        hint="객체를 생성(instantiate)할 때 자동으로 호출되는 메서드입니다.",
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
        hint="dict는 {key: value} 형태로 값을 저장합니다.",
    ),
]


class QuizGame:
    def __init__(self, quizzes=None, best_score=None, best_correct_count=None, best_total=None):
        self.quizzes = quizzes if quizzes is not None else list(DEFAULT_QUIZZES)
        self.best_score = best_score
        self.best_correct_count = best_correct_count
        self.best_total = best_total

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

    def _read_answer_choice(self, prompt, quiz):
        max_value = len(quiz.choices)
        hint_used = False
        while True:
            raw = input(prompt).strip()

            if raw.lower() == "h":
                if quiz.hint:
                    print(f"💡 힌트: {quiz.hint}")
                    hint_used = True
                else:
                    print("💡 이 문제는 등록된 힌트가 없습니다.")
                continue

            if raw == "":
                print(f"⚠️ 빈 입력입니다. 1-{max_value} 사이의 숫자를 입력하세요.")
                continue

            if not raw.isdigit():
                print(f"⚠️ 잘못된 입력입니다. 1-{max_value} 사이의 숫자를 입력하세요.")
                continue

            choice = int(raw)
            if choice < 1 or choice > max_value:
                print(f"⚠️ 잘못된 입력입니다. 1-{max_value} 사이의 숫자를 입력하세요.")
                continue

            return choice, hint_used

    def play_quiz(self):
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
            return

        available = len(self.quizzes)
        if available == 1:
            question_count = 1
        else:
            question_count = self._read_choice(
                f"몇 문제를 푸시겠습니까? (1-{available}): ", 1, available
            )

        quizzes_to_play = list(self.quizzes)
        random.shuffle(quizzes_to_play)
        quizzes_to_play = quizzes_to_play[:question_count]

        total = len(quizzes_to_play)
        print(f"📝 퀴즈를 시작합니다! (총 {total}문제)")

        correct_count = 0
        hint_used_count = 0
        points = 0.0
        for index, quiz in enumerate(quizzes_to_play, start=1):
            print("-" * 40)
            quiz.display(index)
            print()
            selected, hint_used = self._read_answer_choice(
                "정답 입력 (힌트를 보려면 h): ", quiz
            )
            if hint_used:
                hint_used_count += 1

            if quiz.check_answer(selected):
                correct_count += 1
                if hint_used:
                    points += 0.5
                    print("✅ 정답입니다! (힌트 사용으로 0.5점 처리)")
                else:
                    points += 1
                    print("✅ 정답입니다!")
            else:
                print(f"❌ 오답입니다. (정답: {quiz.answer}번)")

        score = round(points / total * 100)
        print("=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")
        if hint_used_count:
            print(f"💡 힌트를 사용한 문제: {hint_used_count}개")

        is_new_best = self.best_score is None or score > self.best_score or (
            score == self.best_score and self.best_total is not None and total > self.best_total
        )
        if is_new_best:
            self.best_score = score
            self.best_correct_count = correct_count
            self.best_total = total
            self.save()
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
        hint = input("힌트 (선택 사항, 없으면 Enter): ").strip()

        self.quizzes.append(Quiz(question, choices, answer, hint))
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
        if self.best_score is None:
            print("📭 아직 퀴즈를 푼 기록이 없습니다.")
            return

        if self.best_total is None or self.best_correct_count is None:
            print(f"🏆 최고 점수: {self.best_score}점")
        else:
            print(f"🏆 최고 점수: {self.best_score}점 ({self.best_total}문제 중 {self.best_correct_count}문제 정답)")

    def save(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_correct_count": self.best_correct_count,
            "best_total": self.best_total,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print(f"⚠️ 데이터 저장에 실패했습니다: {e}")

    def load(self):
        if not STATE_FILE.exists():
            return

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            self.best_score = data.get("best_score")
            self.best_correct_count = data.get("best_correct_count")
            self.best_total = data.get("best_total")
        except (json.JSONDecodeError, KeyError, TypeError, OSError):
            print("⚠️ 저장된 데이터가 손상되어 기본 데이터로 초기화합니다.")
            self.quizzes = list(DEFAULT_QUIZZES)
            self.best_score = None
            self.best_correct_count = None
            self.best_total = None
            return

        if self.best_score is None:
            score_display = "없음"
        elif self.best_total is None or self.best_correct_count is None:
            score_display = f"{self.best_score}점"
        else:
            score_display = f"{self.best_score}점 ({self.best_total}문제 중 {self.best_correct_count}문제 정답)"
        print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {score_display})")

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