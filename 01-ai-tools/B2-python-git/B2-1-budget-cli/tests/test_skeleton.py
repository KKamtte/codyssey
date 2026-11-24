"""a-1 뼈대 테스트: 모든 명령의 --help, 사용법 오류, 공통 옵션, 데코레이터."""

import argparse
import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from budget_app.cli import build_parser, main
from budget_app.decorators import handle_errors, log_execution
from budget_app.errors import EXIT_INPUT, EXIT_STORAGE, EXIT_USAGE, AppError, NotFoundError, StorageError

ALL_COMMANDS = [
    ["add"], ["list"], ["search"], ["update"], ["delete"], ["summary"],
    ["budget"], ["budget", "set"], ["budget", "show"],
    ["category"], ["category", "add"], ["category", "list"], ["category", "remove"],
    ["import"], ["export"], ["backup"],
    ["recurring"], ["recurring", "add"], ["recurring", "list"], ["recurring", "remove"], ["recurring", "apply"],
]


def run_quiet(func, *args):
    """stdout/stderr 를 잡아서 (결과, 출력, 에러 출력)을 돌려준다."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        result = func(*args)
    return result, out.getvalue(), err.getvalue()


class HelpTest(unittest.TestCase):
    def test_every_command_has_help(self):
        for command in [[]] + ALL_COMMANDS:
            with self.subTest(command=command):
                with self.assertRaises(SystemExit) as caught:
                    run_quiet(main, command + ["--help"])
                self.assertEqual(caught.exception.code, 0)

    def test_unknown_command_is_usage_error(self):
        with self.assertRaises(SystemExit) as caught:
            run_quiet(main, ["nosuch"])
        self.assertEqual(caught.exception.code, EXIT_USAGE)


class DataDirOptionTest(unittest.TestCase):
    def test_default(self):
        self.assertEqual(build_parser().parse_args(["list"]).data_dir, "data")

    def test_before_and_after_command(self):
        parser = build_parser()
        self.assertEqual(parser.parse_args(["--data-dir", "a", "list"]).data_dir, "a")
        self.assertEqual(parser.parse_args(["list", "--data-dir", "b"]).data_dir, "b")
        self.assertEqual(parser.parse_args(["category", "list", "--data-dir", "c"]).data_dir, "c")


class HandleErrorsTest(unittest.TestCase):
    def call(self, error):
        @handle_errors
        def command(args):
            raise error

        return run_quiet(command, None)

    def test_app_error_prints_cause_and_hint(self):
        code, out, err = self.call(NotFoundError("없는 거래입니다: TX-000009", "list 로 id 를 확인하세요."))
        self.assertEqual(code, EXIT_INPUT)
        self.assertIn("[오류] 없는 거래입니다: TX-000009", err)
        self.assertIn("[힌트] list 로 id 를 확인하세요.", err)

    def test_exit_codes(self):
        self.assertEqual(self.call(AppError("x"))[0], EXIT_INPUT)
        self.assertEqual(self.call(StorageError("x"))[0], EXIT_STORAGE)
        self.assertEqual(self.call(PermissionError(13, "Permission denied"))[0], EXIT_STORAGE)

    def test_unexpected_error_has_no_traceback(self):
        code, out, err = self.call(ZeroDivisionError("division by zero"))
        self.assertEqual(code, EXIT_INPUT)
        self.assertIn("[오류]", err)
        self.assertNotIn("Traceback", err)

    def test_success_passes_through(self):
        @handle_errors
        def command(args):
            return 0

        self.assertEqual(run_quiet(command, None)[0], 0)


class LogExecutionTest(unittest.TestCase):
    def test_writes_command_exit_code_and_time(self):
        with tempfile.TemporaryDirectory() as tmp:
            @log_execution
            def command(args):
                return 0

            command(argparse.Namespace(data_dir=tmp, command_name="list"))
            line = (Path(tmp) / "app.log").read_text(encoding="utf-8").strip()
            self.assertRegex(line, r"\tlist\texit=0\t\d+\.\dms$")


if __name__ == "__main__":
    unittest.main()
