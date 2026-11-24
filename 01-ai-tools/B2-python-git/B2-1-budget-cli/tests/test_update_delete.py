"""a-5 테스트: update(옵션 방식)·delete, 없는 id, 바꿀 항목 없음, 원자적 재작성."""

from unittest.mock import patch

from tests.test_add_category import CliTestCase


class UpdateDeleteTest(CliTestCase):
    def setUp(self):
        super().setUp()
        self.add(date="2024-01-15", category="food", amount="15000", memo="점심", tags="meal")
        self.add(date="2024-01-16", category="transport", amount="1200")

    def test_update_only_given_fields(self):
        code, out, err = self.run_cli("update", "--id", "TX-000001", "--amount", "20,000", "--memo", "점심 회식")
        self.assertEqual(code, 0, err)
        self.assertIn("amount 15,000 → 20,000", out)
        self.assertIn("memo 점심 → 점심 회식", out)
        first, second = self.transactions()
        self.assertEqual((first["amount"], first["memo"], first["tags"], first["category"]), (20000, "점심 회식", ["meal"], "food"))
        self.assertEqual(second["amount"], 1200)  # 다른 거래는 그대로

    def test_update_all_fields_and_clear(self):
        code, _, err = self.run_cli(
            "update", "--id", "tx-000001", "--date", "2024-02-01", "--type", "income",
            "--category", "salary", "--amount", "5", "--memo", "", "--tags", "",
        )
        self.assertEqual(code, 0, err)
        first = self.transactions()[0]
        self.assertEqual(first | {"memo": first["memo"]}, {
            "id": "TX-000001", "type": "income", "date": "2024-02-01", "amount": 5,
            "category": "salary", "memo": "", "tags": [],
        })

    def test_update_errors_change_nothing(self):
        before = self.transactions()
        cases = {
            ("--id", "TX-000009", "--amount", "1"): "없는 데이터입니다",
            ("--id", "TX-000001"): "바꿀 항목이 없습니다",
            ("--id", "TX-000001", "--amount", "15000"): "바뀌는 것이 없습니다",
            ("--id", "TX-000001", "--category", "nope"): "등록되지 않은 카테고리",
            ("--id", "TX-000001", "--date", "2024-1-1"): "YYYY-MM-DD",
            ("--id", "TX-000001", "--amount", "-1"): "0보다 커야",
            ("--id", "abc", "--amount", "1"): "id 형식",
        }
        for argv, message in cases.items():
            with self.subTest(argv=argv):
                code, _, err = self.run_cli("update", *argv)
                self.assertEqual(code, 1)
                self.assertIn(message, err)
        self.assertEqual(self.transactions(), before)

    def test_update_type_is_limited_by_argparse(self):
        with self.assertRaises(SystemExit) as caught:
            self.run_cli("update", "--id", "TX-000001", "--type", "refund")
        self.assertEqual(caught.exception.code, 2)

    def test_delete(self):
        code, out, _ = self.run_cli("delete", "--id", "TX-000002")
        self.assertEqual(code, 0)
        self.assertIn("[삭제 완료] TX-000002", out)
        self.assertEqual([t["id"] for t in self.transactions()], ["TX-000001"])
        code, _, err = self.run_cli("delete", "--id", "TX-000002")
        self.assertEqual(code, 1)
        self.assertIn("없는 데이터입니다: TX-000002", err)
        # 결정 6: 새 id = 남아 있는 가장 큰 번호 + 1. 맨 마지막 번호를 지우면 그 번호가 다시 쓰인다
        self.assertIn("TX-000002", self.add())

    def test_failed_rewrite_keeps_original(self):
        before = (self.data / "transactions.jsonl").read_bytes()
        with patch("budget_app.storage.os.replace", side_effect=OSError(28, "No space left on device")):
            code, _, err = self.run_cli("delete", "--id", "TX-000001")
        self.assertEqual(code, 3)
        self.assertIn("No space left on device", err)
        self.assertEqual((self.data / "transactions.jsonl").read_bytes(), before)
        self.assertEqual(list(self.data.glob(".*.tmp")), [])
