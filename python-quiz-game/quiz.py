class Quiz:
    def __init__(self, question, choices, answer, hint=""):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

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
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["question"],
            data["choices"],
            data["answer"],
            data.get("hint", ""),
        )