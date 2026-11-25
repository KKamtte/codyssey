"""a-8 테스트(보너스): backup, 반복 내역(add/list/remove/apply, 중복 방지, 짧은 달, 카테고리 연동)."""

import json
import unittest
from datetime import datetime

from budget_app.models import RecurringRule
from budget_app.services import BudgetService
from budget_app.storage import Storage
from tests.test_add_category import CliTestCase


class RuleDateTest(unittest.TestCase):
    def test_day_is_clamped_to_month_end(self):
        rule = RecurringRule("RC-000001", 31, "expense", "rent", 1)
        self.assertEqual(rule.date_in("2024-02"), "2024-02-29")  # 윤년
        self.assertEqual(rule.date_in("2023-02"), "2023-02-28")
        self.assertEqual(rule.date_in("2024-04"), "2024-04-30")
        self.assertEqual(rule.date_in("2024-01"), "2024-01-31")
        self.assertEqual(RecurringRule("RC-000002", 5, "income", "salary", 1).date_in("2024-02"), "2024-02-05")


class RecurringCliTest(CliTestCase):
    def add_rule(self, day="25", type_="income", category="salary", amount="3000000", memo="월급"):
        code, out, err = self.run_cli("recurring", "add", inputs=[day, type_, category, amount, memo])
        self.assertEqual(code, 0, err)
        return out

    def test_add_list_remove(self):
        self.assertIn("RC-000001 매월 25일 income salary 3,000,000원 월급", self.add_rule())
        self.add_rule(day="1", type_="expense", category="rent", amount="500000", memo="")
        _, out, _ = self.run_cli("recurring", "list")
        lines = out.strip().splitlines()
        self.assertIn("RC-000002", lines[2])  # 매월 1일이 먼저
        self.assertIn("RC-000001", lines[3])
        code, out, _ = self.run_cli("recurring", "remove", "--id", "rc-000001")
        self.assertEqual(code, 0)
        self.assertNotIn("RC-000001", self.run_cli("recurring", "list")[1])
        self.assertEqual(self.run_cli("recurring", "remove", "--id", "RC-000001")[0], 1)
        self.assertEqual(self.run_cli("recurring", "remove", "--id", "X1")[0], 1)

    def test_add_asks_again_on_bad_day(self):
        code, _, err = self.run_cli("recurring", "add", inputs=["0", "32", "말일", "31", "expense", "rent", "500000", ""])
        self.assertEqual(code, 0)
        self.assertEqual(err.count("1~31"), 3)

    def test_apply_creates_once_per_month(self):
        self.add_rule()
        self.add_rule(day="31", type_="expense", category="rent", amount="500000", memo="월세")
        code, out, _ = self.run_cli("recurring", "apply", "--month", "2024-02")
        self.assertEqual(code, 0)
        self.assertIn("created=2, skipped=0", out)
        saved = self.transactions()
        self.assertEqual([(t["date"], t["recurring_id"]) for t in saved], [("2024-02-25", "RC-000001"), ("2024-02-29", "RC-000002")])
        # 두 번 실행해도 다시 만들지 않는다
        _, out, _ = self.run_cli("recurring", "apply", "--month", "2024-02")
        self.assertIn("created=0, skipped=2", out)
        self.assertIn("이미 만들었습니다", out)
        self.assertEqual(len(self.transactions()), 2)
        # 다른 달은 새로 만든다
        self.assertIn("created=2", self.run_cli("recurring", "apply", "--month", "2024-03")[1])

    def test_apply_with_no_rules_and_bad_month(self):
        self.assertIn("created=0, skipped=0", self.run_cli("recurring", "apply", "--month", "2024-02")[1])
        self.assertEqual(self.run_cli("recurring", "apply", "--month", "2024-2")[0], 1)

    def test_category_in_rule_counts_as_in_use(self):
        self.add_rule(category="rent", type_="expense", amount="500000")
        code, _, err = self.run_cli("category", "remove", "rent")
        self.assertEqual(code, 1)
        self.assertIn("1건 있어 삭제할 수 없습니다", err)
        self.assertEqual(self.run_cli("category", "remove", "rent", "--replace-with", "etc")[0], 0)
        self.assertIn("| etc", self.run_cli("recurring", "list")[1])

    def test_apply_skips_rule_whose_category_is_gone(self):
        self.add_rule()
        rules = self.data / "recurring.jsonl"
        rule = json.loads(rules.read_text(encoding="utf-8")) | {"category": "deleted"}
        rules.write_text(json.dumps(rule) + "\n", encoding="utf-8")  # 파일을 직접 고쳐 없는 카테고리를 만든다
        _, out, _ = self.run_cli("recurring", "apply", "--month", "2024-02")
        self.assertIn("카테고리 'deleted'가 없습니다", out)
        self.assertEqual(self.transactions(), [])


class BackupTest(CliTestCase):
    def test_backup_copies_data_files(self):
        self.add(memo="백업 확인")
        code, out, _ = self.run_cli("backup")
        self.assertEqual(code, 0)
        self.assertIn("[백업 완료]", out)
        backups = list((self.data / "backups").iterdir())
        self.assertEqual(len(backups), 1)
        names = sorted(p.name for p in backups[0].iterdir())
        self.assertEqual(names, ["budgets.jsonl", "categories.jsonl", "recurring.jsonl", "transactions.jsonl"])
        self.assertIn("백업 확인", (backups[0] / "transactions.jsonl").read_text(encoding="utf-8"))

    def test_same_second_does_not_overwrite(self):
        storage = Storage(self.data)
        storage.initialize()
        service = BudgetService(storage)
        moment = datetime(2024, 1, 15, 9, 30, 0)
        first, second = service.backup(moment), service.backup(moment)
        self.assertEqual((first.name, second.name), ("20240115-093000", "20240115-093000-2"))


if __name__ == "__main__":
    unittest.main()
