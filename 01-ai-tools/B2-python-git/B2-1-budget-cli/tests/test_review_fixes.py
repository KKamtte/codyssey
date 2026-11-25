"""a-1~a-3 코드 리뷰에서 찾은 문제의 회귀 테스트 (리뷰 항목 번호를 이름에 붙였다)."""

import json
import os
import stat
import unittest
from unittest.mock import patch

from budget_app.errors import EXIT_STORAGE, ValidationError
from budget_app.models import Transaction, parse_amount, parse_category_name
from budget_app.storage import JsonlFile
from tests.test_add_category import CliTestCase

TX1 = {"id": "TX-000001", "type": "expense", "date": "2024-01-01", "amount": 1, "category": "food"}


class ReviewFixesTest(CliTestCase):
    def write_transactions(self, text: str | bytes):
        self.run_cli("category", "list")  # 폴더·파일 만들기
        path = self.data / "transactions.jsonl"
        path.write_bytes(text if isinstance(text, bytes) else text.encode("utf-8"))
        return path

    def test_01_append_after_line_without_newline(self):
        path = self.write_transactions(json.dumps(TX1))  # 마지막 줄바꿈 없음
        self.add()
        lines = path.read_text(encoding="utf-8").splitlines()
        self.assertEqual([json.loads(line)["id"] for line in lines], ["TX-000001", "TX-000002"])

    def test_02_bad_records_are_storage_errors_with_line(self):
        bad_files = {
            "필드 빠짐": json.dumps(TX1) + "\n" + '{"id": "TX-000002"}\n',
            "객체 아님": "[]\n",
            "id 형식": json.dumps(TX1 | {"id": "X1"}) + "\n",
            "금액 음수": json.dumps(TX1 | {"amount": -3}) + "\n",
            "날짜 형식": json.dumps(TX1 | {"date": "2024-1-1"}) + "\n",
            "UTF-8 아님": b"\xff\xfe\n",
        }
        for name, content in bad_files.items():
            with self.subTest(name):
                self.write_transactions(content)
                code, _, err = self.run_cli("list")
                self.assertEqual(code, EXIT_STORAGE, err)
                self.assertIn("transactions.jsonl", err)
                self.assertNotIn("예상하지 못한", err)
        self.write_transactions(bad_files["필드 빠짐"])
        self.assertIn("2번째 줄", self.run_cli("list")[2])

    def test_02_add_checks_file_before_asking(self):
        self.write_transactions("[]\n")
        code, out, err = self.run_cli("add", inputs=["2024-01-15"])
        self.assertEqual(code, EXIT_STORAGE)
        self.assertNotIn("날짜(", out)  # 하나도 묻기 전에 멈춘다

    def test_03_unexpected_error_logs_traceback(self):
        with patch("budget_app.services.BudgetService.category_names", side_effect=ZeroDivisionError("boom")):
            code, _, err = self.run_cli("category", "list")
        self.assertEqual(code, 1)
        self.assertNotIn("Traceback", err)
        self.assertIn(str(self.data / "app.log"), err)
        log = (self.data / "app.log").read_text(encoding="utf-8")
        self.assertIn("Traceback", log)
        self.assertIn("ZeroDivisionError: boom", log)
        self.assertIn("category list\texit=1", log)  # 데코레이터 조합: 오류 종료 코드도 기록된다

    def test_04_rewrite_keeps_permissions(self):
        self.run_cli("category", "list")
        path = self.data / "categories.jsonl"
        os.chmod(path, 0o644)
        self.run_cli("category", "remove", "rent")
        self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o644)

    def test_05_replace_with_is_checked_even_if_unused(self):
        code, _, err = self.run_cli("category", "remove", "rent", "--replace-with", "nope")
        self.assertEqual(code, 1)
        self.assertIn("등록되지 않은 카테고리", err)
        code, _, err = self.run_cli("category", "remove", "rent", "--replace-with", "rent")
        self.assertEqual(code, 1)
        self.assertIn("같은 카테고리", err)
        self.assertIn("- rent", self.run_cli("category", "list")[1])  # 지워지지 않음

    def test_07_amount_format(self):
        self.assertEqual(parse_amount("15000"), 15000)
        self.assertEqual(parse_amount("1,500,000"), 1500000)
        for bad in ["1_000", "１２３", "1,,0,0", "+5", "15,00", " ", str(10**12 + 1)]:
            with self.subTest(bad=bad), self.assertRaises(ValidationError):
                parse_amount(bad)

    def test_08_interactive_category_add_asks_again_on_duplicate(self):
        code, out, err = self.run_cli("category", "add", inputs=["food", "hobby"])
        self.assertEqual(code, 0)
        self.assertIn("이미 있는 카테고리입니다: food", err)
        self.assertIn("category=hobby", out)

    def test_09_keyboard_interrupt(self):
        with patch("budget_app.services.BudgetService.category_names", side_effect=KeyboardInterrupt):
            code, _, err = self.run_cli("category", "list")
        self.assertEqual(code, 130)
        self.assertIn("[중단]", err)

    def test_10_sort_by_id_number(self):
        a = Transaction("TX-999999", "expense", "2024-01-01", 1, "food")
        b = Transaction("TX-1000000", "expense", "2024-01-01", 1, "food")
        self.assertLess(a.sort_key, b.sort_key)

    def test_11_update_where_reads_once_and_skips_unchanged_write(self):
        self.add()
        repo_file = self.data / "transactions.jsonl"
        before = repo_file.stat().st_mtime_ns
        calls = []
        from budget_app.storage import Storage

        repo = Storage(self.data).transactions
        self.assertEqual(repo.update_where(lambda tx: calls.append(tx.id) or tx), 0)
        self.assertEqual(calls, ["TX-000001"])  # change 는 거래마다 한 번
        self.assertEqual(repo_file.stat().st_mtime_ns, before)  # 바뀐 게 없으면 교체하지 않음
        self.assertEqual(list(self.data.glob(".*.tmp")), [])

    def test_12_category_name_rules(self):
        for good in ["food", "식비", "side_job", "a-b", "2024"]:
            self.assertEqual(parse_category_name(good), good)
        for bad in ["a|b", "-x", "a b", "a,b", "x" * 21]:
            with self.subTest(bad=bad), self.assertRaises(ValidationError):
                parse_category_name(bad)

    def test_13_ask_blank_without_default_asks_again(self):
        code, out, err = self.run_cli("add", inputs=["2024-01-15", "expense", "food", " ", "1000", "  점심  ", ""])
        self.assertEqual(code, 0)
        self.assertIn("금액은 숫자여야 합니다", err)
        self.assertEqual(json.loads((self.data / "transactions.jsonl").read_text(encoding="utf-8"))["memo"], "점심")

    def test_13_next_id_without_file(self):
        from budget_app.storage import Storage

        self.assertEqual(Storage(self.data).transactions.next_id(), "TX-000001")

    def test_13_data_dir_last_one_wins(self):
        from budget_app.cli import build_parser

        self.assertEqual(build_parser().parse_args(["--data-dir", "a", "list", "--data-dir", "b"]).data_dir, "b")
        self.assertEqual(build_parser().parse_args(["category", "--data-dir", "m", "list"]).data_dir, "m")


if __name__ == "__main__":
    unittest.main()
