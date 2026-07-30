from quiz_game import QuizGame


def main():
    game = QuizGame()
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n👋 입력이 중단되어 안전하게 종료합니다.")


if __name__ == "__main__":
    main()