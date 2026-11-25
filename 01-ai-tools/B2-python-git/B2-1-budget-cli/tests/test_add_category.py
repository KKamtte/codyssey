"""a-3 테스트: 대화형 add(재입력, 중간 종료), category add/list/remove."""

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from budget_app.cli import main


class CliTestCase(unittest.TestCase):
    """임시 데이터 폴더에서 명령을 실행하는 도우미."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.data = Path(self.tmp.name) / "data"

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *argv, inputs=()):
        out, err = io.StringIO(), io.StringIO()
        answers = iter(inputs)

        def fake_input(prompt=""):
            out.write(prompt)
            try:
                return next(answers)
            except StopIteration:
                raise EOFError from None

        with patch("builtins.input", fake_input), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main([*argv, "--data-dir", str(self.data)])
        return code, out.getvalue(), err.getvalue()

    def transactions(self):
        path = self.data / "transactions.jsonl"
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

    def add(self, date="2024-01-15", type_="expense", category="food", amount="15000", memo="", tags=""):
        code, out, err = self.run_cli("add", inputs=[date, type_, category, amount, memo, tags])
        self.assertEqual(code, 0, err)
        return out


class AddTest(CliTestCase):
    def test_add_saves_and_prints_id(self):
        out = self.add(memo="점심", tags="meal")
        self.assertIn("[저장 완료] id=TX-000001", out)
        self.assertEqual(self.transactions(), [{
            "id": "TX-000001", "type": "expense", "date": "2024-01-15", "amount": 15000,
            "category": "food", "memo": "점심", "tags": ["meal"],
        }])
        self.assertIn("TX-000002", self.add())

    def test_invalid_answers_are_asked_again(self):
        code, out, err = self.run_cli("add", inputs=[
            "2024-13-40", "2024-01-15", "refund", "income", "hobby", "salary", "0", "3,000,000", "", "",
        ])
        self.assertEqual(code, 0)
        self.assertIn("날짜 형식이 올바르지 않습니다", err)
        self.assertIn("타입은 income 또는 expense", err)
        self.assertIn("등록되지 않은 카테고리입니다: hobby", err)
        self.assertIn("금액은 0보다 커야 합니다", err)
        self.assertEqual(self.transactions()[0]["amount"], 3000000)

    def test_empty_date_means_today(self):
        self.add(date="")
        self.assertRegex(self.transactions()[0]["date"], r"^\d{4}-\d{2}-\d{2}$")

    def test_input_ending_early_saves_nothing(self):
        code, out, err = self.run_cli("add", inputs=["2024-01-15", "expense"])
        self.assertEqual(code, 1)
        self.assertIn("입력이 중간에 끝났습니다", err)
        self.assertEqual(self.transactions(), [])

    def test_first_run_notices(self):
        out = self.add()
        self.assertIn("[안내] 기본 카테고리를 만들었습니다", out)
        self.assertNotIn("[안내]", self.add())


class CategoryTest(CliTestCase):
    def test_add_list_and_duplicate(self):
        code, out, _ = self.run_cli("category", "add", inputs=["hobby"])
        self.assertEqual(code, 0)
        self.assertIn("[저장 완료] category=hobby", out)
        _, out, _ = self.run_cli("category", "list")
        self.assertIn("- hobby", out)
        code, _, err = self.run_cli("category", "add", "hobby")
        self.assertEqual(code, 1)
        self.assertIn("이미 있는 카테고리", err)

    def test_remove_unused(self):
        code, out, _ = self.run_cli("category", "remove", "rent")
        self.assertEqual(code, 0)
        _, out, _ = self.run_cli("category", "list")
        self.assertNotIn("- rent", out)

    def test_remove_in_use_is_blocked(self):
        self.add(category="food")
        code, _, err = self.run_cli("category", "remove", "food")
        self.assertEqual(code, 1)
        self.assertIn("1건 있어 삭제할 수 없습니다", err)
        self.assertIn("--replace-with", err)

    def test_remove_with_replacement_moves_transactions(self):
        self.add(category="food")
        self.add(category="transport")
        code, out, _ = self.run_cli("category", "remove", "food", "--replace-with", "etc")
        self.assertEqual(code, 0)
        self.assertIn("거래·반복 규칙 1건을 etc(으)로 옮김", out)
        self.assertEqual([t["category"] for t in self.transactions()], ["etc", "transport"])

    def test_remove_errors(self):
        self.add(category="food")
        self.assertEqual(self.run_cli("category", "remove", "nope")[0], 1)
        code, _, err = self.run_cli("category", "remove", "food", "--replace-with", "nope")
        self.assertEqual(code, 1)
        self.assertIn("등록되지 않은 카테고리", err)
        self.assertEqual(self.transactions()[0]["category"], "food")  # 실패하면 아무것도 바뀌지 않음


if __name__ == "__main__":
    unittest.main()
