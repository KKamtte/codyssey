"""a-6 테스트: summary(합계·잔액·TOP N·데이터 없음), budget set/show, 사용률·초과 경고."""

import unittest

from budget_app.errors import ValidationError
from budget_app.models import Budget, Transaction
from budget_app.services import summarize
from tests.test_add_category import CliTestCase


def tx(n, date, type_, category, amount):
    return Transaction(f"TX-{n:06d}", type_, date, amount, category)


class SummarizeTest(unittest.TestCase):
    DATA = [
        tx(1, "2024-01-14", "income", "salary", 3_000_000),
        tx(2, "2024-01-05", "expense", "rent", 150_000),
        tx(3, "2024-01-15", "expense", "food", 15_000),
        tx(4, "2024-01-20", "expense", "food", 30_000),
        tx(5, "2024-01-12", "expense", "transport", 20_000),
        tx(6, "2024-02-01", "expense", "rent", 150_000),  # 다른 달
    ]

    def test_original_example_numbers(self):
        s = summarize(iter(self.DATA), "2024-01", 3, Budget("2024-01", 500_000))
        self.assertEqual((s.count, s.income, s.expense, s.balance), (5, 3_000_000, 215_000, 2_785_000))
        self.assertEqual(s.top_expenses, [("rent", 150_000), ("food", 45_000), ("transport", 20_000)])
        self.assertAlmostEqual(s.budget_rate, 43.0)
        self.assertEqual(s.over_budget, 0)

    def test_top_n_and_ties(self):
        data = [tx(1, "2024-01-01", "expense", "b", 10), tx(2, "2024-01-01", "expense", "a", 10), tx(3, "2024-01-01", "expense", "c", 5)]
        self.assertEqual(summarize(iter(data), "2024-01", 2, None).top_expenses, [("a", 10), ("b", 10)])
        with self.assertRaises(ValidationError):
            summarize(iter(data), "2024-01", 0, None)

    def test_over_budget_and_no_budget(self):
        s = summarize(iter(self.DATA), "2024-02", 3, Budget("2024-02", 100_000))
        self.assertAlmostEqual(s.budget_rate, 150.0)
        self.assertEqual(s.over_budget, 50_000)
        s = summarize(iter(self.DATA), "2024-02", 3, None)
        self.assertIsNone(s.budget_rate)
        self.assertEqual(s.over_budget, 0)

    def test_empty_month(self):
        s = summarize(iter(self.DATA), "2024-03", 3, None)
        self.assertEqual((s.count, s.income, s.expense, s.top_expenses), (0, 0, 0, []))


class SummaryBudgetCliTest(CliTestCase):
    def seed(self):
        self.add(date="2024-01-14", type_="income", category="salary", amount="3000000")
        self.add(date="2024-01-05", category="rent", amount="150000")
        self.add(date="2024-01-15", category="food", amount="45000")

    def test_summary_with_budget(self):
        self.seed()
        self.assertEqual(self.run_cli("budget", "set", "--month", "2024-01", "--amount", "500000")[0], 0)
        code, out, _ = self.run_cli("summary", "--month", "2024-01", "--top", "1")
        self.assertEqual(code, 0)
        for line in ["총 수입: 3,000,000원", "총 지출: 195,000원", "잔액: 2,805,000원", "예산: 500,000원 (사용률 39.0%)", "지출 TOP 1", "1) rent 150,000원"]:
            self.assertIn(line, out)
        self.assertNotIn("food", out)
        self.assertNotIn("[경고]", out)

    def test_summary_over_budget_warning(self):
        self.seed()
        self.run_cli("budget", "set", "--month", "2024-01", "--amount", "100000")
        _, out, _ = self.run_cli("summary", "--month", "2024-01")
        self.assertIn("사용률 195.0%", out)
        self.assertIn("[경고] 예산을 95,000원 초과했습니다.", out)

    def test_summary_no_budget_and_no_data(self):
        self.seed()
        _, out, _ = self.run_cli("summary", "--month", "2024-01")
        self.assertIn("예산: 없음", out)
        _, out, _ = self.run_cli("summary", "--month", "2024-03")
        self.assertIn("데이터 없음", out)
        self.assertNotIn("총 수입", out)

    def test_budget_set_overwrites_and_show(self):
        self.run_cli("budget", "set", "--month", "2024-02", "--amount", "300000")
        self.run_cli("budget", "set", "--month", "2024-01", "--amount", "500000")
        _, out, _ = self.run_cli("budget", "set", "--month", "2024-01", "--amount", "450,000")
        self.assertIn("2024-01 예산 450,000원 (이전 500,000원)", out)
        _, out, _ = self.run_cli("budget", "show")
        self.assertEqual(out.strip().splitlines(), ["2024-01  450,000원", "2024-02  300,000원"])
        _, out, _ = self.run_cli("budget", "show", "--month", "2024-05")
        self.assertIn("2024-05 예산이 없습니다", out)

    def test_bad_inputs(self):
        for argv, message in {
            ("summary", "--month", "2024-1"): "YYYY-MM",
            ("summary", "--month", "2024-01", "--top", "0"): "--top",
            ("budget", "set", "--month", "2024-01", "--amount", "0"): "0보다 커야",
            ("budget", "set", "--month", "24-01", "--amount", "100"): "YYYY-MM",
        }.items():
            with self.subTest(argv=argv):
                code, _, err = self.run_cli(*argv)
                self.assertEqual(code, 1)
                self.assertIn(message, err)


if __name__ == "__main__":
    unittest.main()
