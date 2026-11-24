"""a-7 테스트: CSV import(검증·건너뛰기·BOM·따옴표), export(기간 조건·정렬·덮어쓰기 보호), 왕복."""

import csv
from pathlib import Path

from tests.test_add_category import CliTestCase

GOOD_AND_BAD = (
    "date,type,category,amount,memo,tags\n"
    '2024-01-15,expense,food,"15,000",점심,"meal,lunch"\n'
    "2024-01-14,income,salary,3000000,,\n"
    "2024-13-40,expense,food,100,,\n"  # 4행: 날짜
    "2024-01-16,expense,hobby,100,,\n"  # 5행: 카테고리
    "2024-01-17,refund,food,100,,\n"  # 6행: 타입
    "2024-01-18,expense,food,0,,\n"  # 7행: 금액
    '2024-01-19,expense,transport,1200,"버스, 지하철",\n'
)


class ImportExportTest(CliTestCase):
    def write_csv(self, name: str, text: str, encoding: str = "utf-8") -> str:
        path = Path(self.tmp.name) / name
        path.write_text(text, encoding=encoding)
        return str(path)

    def read_csv(self, path: str) -> list[dict]:
        with open(path, encoding="utf-8", newline="") as file:
            return list(csv.DictReader(file))

    def test_import_skips_bad_rows_with_reasons(self):
        code, out, _ = self.run_cli("import", "--from", self.write_csv("in.csv", GOOD_AND_BAD))
        self.assertEqual(code, 0)
        self.assertIn("[완료] imported=3, skipped=4", out)
        for line in ["4행: 날짜 형식", "5행: 등록되지 않은 카테고리입니다: hobby", "6행: 타입은", "7행: 금액은 0보다"]:
            self.assertIn(line, out)
        saved = self.transactions()
        self.assertEqual([t["id"] for t in saved], ["TX-000001", "TX-000002", "TX-000003"])
        self.assertEqual(saved[0]["amount"], 15000)
        self.assertEqual(saved[0]["tags"], ["meal", "lunch"])
        self.assertEqual(saved[2]["memo"], "버스, 지하철")

    def test_import_continues_ids_and_handles_bom(self):
        self.add()
        path = self.write_csv("bom.csv", "date,type,category,amount\n2024-02-01,expense,rent,500000\n", encoding="utf-8-sig")
        code, out, _ = self.run_cli("import", "--from", path)
        self.assertEqual(code, 0, out)
        self.assertEqual(self.transactions()[-1]["id"], "TX-000002")

    def test_import_file_errors(self):
        cases = {
            self.write_csv("missing.csv", "date,amount\n2024-01-01,1\n"): "필수 열이 없습니다: type, category",
            str(Path(self.tmp.name) / "none.csv"): "CSV 파일이 없습니다",
        }
        for path, message in cases.items():
            with self.subTest(path=path):
                code, _, err = self.run_cli("import", "--from", path)
                self.assertEqual(code, 1)
                self.assertIn(message, err)
        self.assertEqual(self.transactions(), [])

    def test_import_non_utf8(self):
        path = Path(self.tmp.name) / "cp949.csv"
        path.write_bytes("date,type,category,amount,memo\n2024-01-01,expense,food,1,점심\n".encode("cp949"))
        code, _, err = self.run_cli("import", "--from", str(path))
        self.assertEqual(code, 1)
        self.assertIn("UTF-8", err)

    def test_export_month_sorted_by_date(self):
        self.run_cli("import", "--from", self.write_csv("in.csv", GOOD_AND_BAD))
        self.add(date="2024-02-01", category="rent", amount="500000")
        out_path = str(Path(self.tmp.name) / "out.csv")
        code, out, _ = self.run_cli("export", "--out", out_path, "--month", "2024-01")
        self.assertEqual(code, 0)
        self.assertIn("(3 records)", out)
        rows = self.read_csv(out_path)
        self.assertEqual(list(rows[0].keys()), ["date", "type", "category", "amount", "memo", "tags"])
        self.assertEqual([r["date"] for r in rows], ["2024-01-14", "2024-01-15", "2024-01-19"])
        self.assertEqual(rows[1]["tags"], "meal,lunch")

    def test_export_range_and_guards(self):
        self.run_cli("import", "--from", self.write_csv("in.csv", GOOD_AND_BAD))
        out_path = str(Path(self.tmp.name) / "out.csv")
        self.assertEqual(self.run_cli("export", "--out", out_path, "--from", "2024-01-15", "--to", "2024-01-31")[0], 0)
        self.assertEqual(len(self.read_csv(out_path)), 2)
        code, _, err = self.run_cli("export", "--out", out_path, "--month", "2024-01")
        self.assertEqual(code, 1)
        self.assertIn("--force", err)
        self.assertEqual(self.run_cli("export", "--out", out_path, "--month", "2024-01", "--force")[0], 0)
        self.assertEqual(len(self.read_csv(out_path)), 3)
        for argv, message in {
            (): "내보낼 기간이 없습니다",
            ("--month", "2024-01", "--from", "2024-01-01"): "함께 쓸 수 없습니다",
            ("--from", "2024-02-01", "--to", "2024-01-01"): "늦습니다",
        }.items():
            with self.subTest(argv=argv):
                code, _, err = self.run_cli("export", "--out", str(Path(self.tmp.name) / "x.csv"), *argv)
                self.assertEqual(code, 1)
                self.assertIn(message, err)

    def test_round_trip(self):
        self.run_cli("import", "--from", self.write_csv("in.csv", GOOD_AND_BAD))
        out_path = str(Path(self.tmp.name) / "out.csv")
        self.run_cli("export", "--out", out_path, "--month", "2024-01")
        first = self.read_csv(out_path)
        self.data = Path(self.tmp.name) / "data2"  # 빈 데이터 폴더에 다시 가져오기
        self.assertIn("imported=3, skipped=0", self.run_cli("import", "--from", out_path)[1])
        again = str(Path(self.tmp.name) / "again.csv")
        self.run_cli("export", "--out", again, "--month", "2024-01")
        self.assertEqual(self.read_csv(again), first)
