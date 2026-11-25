"""a-4 테스트: 최신순 상위 N개(스트리밍), 검색 조건, 표 출력(한글 폭)."""

import unittest

from budget_app.errors import ValidationError
from budget_app.formatting import display_width, table, truncate
from budget_app.models import Transaction
from budget_app.services import SearchCriteria, latest
from tests.test_add_category import CliTestCase


def tx(n: int, date: str, **kwargs) -> Transaction:
    fields = {"type": "expense", "amount": 1000, "category": "food"} | kwargs
    return Transaction(id=f"TX-{n:06d}", date=date, **fields)


class LatestTest(unittest.TestCase):
    def test_orders_by_date_then_id_and_counts_all(self):
        data = [tx(1, "2024-01-12"), tx(2, "2024-01-15"), tx(3, "2024-01-14"), tx(4, "2024-01-15")]
        page = latest(iter(data), 3)
        self.assertEqual([t.id for t in page.items], ["TX-000004", "TX-000002", "TX-000003"])
        self.assertEqual(page.total, 4)

    def test_consumes_a_generator_once(self):
        pulled = []

        def source():
            for n in range(1, 1001):
                pulled.append(n)
                yield tx(n, f"2024-01-{n % 28 + 1:02d}")

        page = latest(source(), 5)
        self.assertEqual(len(page.items), 5)
        self.assertEqual(len(pulled), 1000)  # 한 번만 훑는다 (리스트로 만들어 다시 읽지 않음)
        self.assertEqual(page.total, 1000)

    def test_limit_must_be_positive(self):
        with self.assertRaises(ValidationError):
            latest(iter([]), 0)


class CriteriaTest(unittest.TestCase):
    def test_each_condition(self):
        t = tx(1, "2024-01-15", memo="점심 Kimchi", tags=("meal",))
        self.assertTrue(SearchCriteria().matches(t))
        self.assertTrue(SearchCriteria(date_from="2024-01-15", date_to="2024-01-15").matches(t))
        self.assertFalse(SearchCriteria(date_from="2024-01-16").matches(t))
        self.assertFalse(SearchCriteria(date_to="2024-01-14").matches(t))
        self.assertFalse(SearchCriteria(category="rent").matches(t))
        self.assertFalse(SearchCriteria(type="income").matches(t))
        self.assertTrue(SearchCriteria(q="kimchi").matches(t))  # 대소문자 무시
        self.assertFalse(SearchCriteria(q="저녁").matches(t))
        self.assertTrue(SearchCriteria(tag="meal").matches(t))
        self.assertFalse(SearchCriteria(tag="mea").matches(t))  # 태그는 정확히 일치


class FormattingTest(unittest.TestCase):
    def test_width_counts_korean_as_two(self):
        self.assertEqual(display_width("abc"), 3)
        self.assertEqual(display_width("점심"), 4)
        self.assertEqual(display_width("2월 월세"), 8)

    def test_truncate(self):
        self.assertEqual(truncate("짧음", 10), "짧음")
        cut = truncate("아주아주긴메모입니다", 9)
        self.assertTrue(cut.endswith("…"))
        self.assertLessEqual(display_width(cut), 9)

    def test_table_columns_line_up(self):
        lines = table(["메모", "금액"], [["점심", "15,000"], ["coffee", "8,000"]], right_align=[1]).splitlines()
        self.assertEqual(len({display_width(line) for line in lines}), 1)  # 모든 줄의 칸 수가 같다
        self.assertTrue(lines[3].endswith(" 8,000"))  # 금액은 오른쪽 정렬


class ListSearchCliTest(CliTestCase):
    def seed(self):
        self.add(date="2024-01-12", category="transport", amount="20000")
        self.add(date="2024-01-14", type_="income", category="salary", amount="3000000", memo="1월 월급")
        self.add(date="2024-01-15", category="food", amount="15000", memo="점심 김치찌개", tags="meal,lunch")

    def test_list_latest_first_with_limit(self):
        self.seed()
        code, out, _ = self.run_cli("list", "--limit", "2")
        self.assertEqual(code, 0)
        body = out.splitlines()
        self.assertIn("TX-000003", body[2])
        self.assertIn("TX-000002", body[3])
        self.assertIn("(3건 중 최신 2건)", out)

    def test_list_empty(self):
        _, out, _ = self.run_cli("list")
        self.assertIn("거래가 없습니다", out)

    def test_search_combined_conditions(self):
        self.seed()
        code, out, _ = self.run_cli("search", "--from", "2024-01-13", "--type", "expense", "--tag", "meal")
        self.assertEqual(code, 0)
        self.assertIn("TX-000003", out)
        self.assertNotIn("TX-000001", out)
        _, out, _ = self.run_cli("search", "--q", "월급")
        self.assertIn("TX-000002", out)
        _, out, _ = self.run_cli("search", "--category", "rent")
        self.assertIn("조건에 맞는 거래가 없습니다", out)

    def test_search_bad_dates(self):
        code, _, err = self.run_cli("search", "--from", "2024-1-1")
        self.assertEqual(code, 1)
        self.assertIn("YYYY-MM-DD", err)
        code, _, err = self.run_cli("search", "--from", "2024-02-01", "--to", "2024-01-01")
        self.assertEqual(code, 1)
        self.assertIn("늦습니다", err)


if __name__ == "__main__":
    unittest.main()
