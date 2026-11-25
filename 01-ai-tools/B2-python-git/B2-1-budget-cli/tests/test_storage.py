"""a-2 테스트: 검증 함수, JSONL 스트리밍·추가·원자적 교체, 초기화."""

import inspect
import tempfile
import unittest
from pathlib import Path

from budget_app.errors import StorageError, ValidationError
from budget_app.models import Budget, Transaction, parse_amount, parse_category_name, parse_date, parse_month, parse_tags, parse_type
from budget_app.storage import DEFAULT_CATEGORIES, JsonlFile, Storage


def tx(id_no: int, date: str = "2024-01-15", **kwargs) -> Transaction:
    fields = {"type": "expense", "amount": 1000, "category": "food"} | kwargs
    return Transaction(id=f"TX-{id_no:06d}", date=date, **fields)


class ValidationTest(unittest.TestCase):
    def test_date(self):
        self.assertEqual(parse_date(" 2024-01-15 "), "2024-01-15")
        for bad in ["2024-13-40", "2024/01/15", "2024-1-5", "", "abc"]:
            with self.subTest(bad=bad), self.assertRaises(ValidationError):
                parse_date(bad)

    def test_month(self):
        self.assertEqual(parse_month("2024-01"), "2024-01")
        for bad in ["2024-1", "2024-13", "202401"]:
            with self.subTest(bad=bad), self.assertRaises(ValidationError):
                parse_month(bad)

    def test_amount(self):
        self.assertEqual(parse_amount("15,000"), 15000)
        for bad in ["0", "-5", "1.5", "만원", ""]:
            with self.subTest(bad=bad), self.assertRaises(ValidationError):
                parse_amount(bad)

    def test_type_tags_category(self):
        self.assertEqual(parse_type(" Income "), "income")
        with self.assertRaises(ValidationError):
            parse_type("refund")
        self.assertEqual(parse_tags("meal, lunch,,meal"), ("meal", "lunch"))
        self.assertEqual(parse_tags(""), ())
        with self.assertRaises(ValidationError):
            parse_category_name("  ")
        with self.assertRaises(ValidationError):
            parse_category_name("a,b")

    def test_transaction_roundtrip(self):
        original = tx(3, memo="점심", tags=("meal",))
        self.assertEqual(Transaction.from_dict(original.to_dict()), original)
        self.assertNotIn("recurring_id", original.to_dict())


class StorageTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name) / "data"
        self.storage = Storage(self.dir)

    def tearDown(self):
        self.tmp.cleanup()

    def test_initialize_creates_files_and_default_categories(self):
        notices = self.storage.initialize()
        for name in ["transactions.jsonl", "categories.jsonl", "budgets.jsonl", "recurring.jsonl"]:
            self.assertTrue((self.dir / name).exists(), name)
        self.assertEqual(self.storage.categories.names(), list(DEFAULT_CATEGORIES))
        self.assertEqual(len(notices), 2)
        self.assertEqual(self.storage.initialize(), [])  # 두 번째부터는 조용히

    def test_stream_is_a_generator(self):
        self.storage.initialize()
        self.assertTrue(inspect.isgenerator(self.storage.transactions.stream()))

    def test_add_find_next_id(self):
        self.storage.initialize()
        repo = self.storage.transactions
        self.assertEqual(repo.next_id(), "TX-000001")
        repo.add(tx(1))
        repo.add(tx(7))
        self.assertEqual(repo.next_id(), "TX-000008")
        self.assertEqual(repo.find("TX-000007"), tx(7))
        self.assertIsNone(repo.find("TX-000099"))

    def test_update_where_changes_and_deletes(self):
        self.storage.initialize()
        repo = self.storage.transactions
        for n in (1, 2, 3):
            repo.add(tx(n))
        deleted = repo.update_where(lambda t: None if t.id == "TX-000002" else t)
        self.assertEqual(deleted, 1)
        self.assertEqual([t.id for t in repo.stream()], ["TX-000001", "TX-000003"])
        self.assertEqual(repo.update_where(lambda t: t), 0)  # 바뀐 게 없으면 0
        # 가장 큰 번호를 지우면 그 번호가 다시 쓰인다 (결정 6: 남아 있는 최대 + 1)
        repo.update_where(lambda t: None if t.id == "TX-000003" else t)
        self.assertEqual(repo.next_id(), "TX-000002")

    def test_rewrite_failure_keeps_original(self):
        self.storage.initialize()
        repo = self.storage.transactions
        repo.add(tx(1))
        before = (self.dir / "transactions.jsonl").read_text(encoding="utf-8")

        def broken():
            yield tx(1).to_dict()
            raise RuntimeError("쓰는 도중 실패")

        with self.assertRaises(RuntimeError):
            repo.file.rewrite(broken())
        self.assertEqual((self.dir / "transactions.jsonl").read_text(encoding="utf-8"), before)
        self.assertEqual([p.name for p in self.dir.glob("*.tmp")], [])  # 임시 파일도 남지 않음

    def test_broken_line_is_storage_error(self):
        self.storage.initialize()
        (self.dir / "transactions.jsonl").write_text('{"id": "TX-000001"\n', encoding="utf-8")
        with self.assertRaises(StorageError) as caught:
            list(self.storage.transactions.stream())
        self.assertIn("1번째 줄", caught.exception.message)

    def test_missing_file_streams_nothing(self):
        self.assertEqual(list(JsonlFile(self.dir / "none.jsonl").stream()), [])

    def test_categories_and_budgets(self):
        self.storage.initialize()
        self.storage.categories.add("hobby")
        self.assertTrue(self.storage.categories.exists("hobby"))
        self.storage.categories.remove("hobby")
        self.assertFalse(self.storage.categories.exists("hobby"))

        budgets = self.storage.budgets
        budgets.set(Budget("2024-01", 500000))
        budgets.set(Budget("2024-02", 300000))
        budgets.set(Budget("2024-01", 450000))  # 같은 달은 덮어쓴다
        self.assertEqual(budgets.get("2024-01"), Budget("2024-01", 450000))
        self.assertEqual(len(list(budgets.stream())), 2)

    def test_unwritable_data_dir(self):
        blocker = Path(self.tmp.name) / "file"
        blocker.write_text("x")
        with self.assertRaises(StorageError):
            Storage(blocker / "data").initialize()


if __name__ == "__main__":
    unittest.main()
