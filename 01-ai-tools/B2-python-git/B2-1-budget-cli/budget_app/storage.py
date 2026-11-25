"""저장소 계층: JSONL 파일 읽기·쓰기만 맡는다 (검증·계산은 하지 않는다).

JSONL = 한 줄에 JSON 하나. 파일을 한 줄씩 읽으면 거래가 몇만 건이어도 메모리에는 한 건씩만 올라간다.

- 읽기: stream() 은 제너레이터다. yield 로 한 건씩 넘겨주고, 다음 값을 달라고 할 때까지 멈춰 있다.
- 추가: append() 는 파일 끝에 한 줄만 덧붙인다 (기존 내용을 다시 쓰지 않음).
- 수정·삭제: rewrite() 는 "바뀐 전체"를 임시 파일에 다 쓴 뒤 os.replace 로 한 번에 바꿔 끼운다.
  중간에 프로그램이 죽어도 원본은 그대로이거나 새 파일로 완전히 바뀐 상태 둘 중 하나다 (원자적 교체).
"""

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator, TypeVar

from .errors import StorageError
from .models import Budget, RecurringRule, Transaction

Record = dict[str, Any]
T = TypeVar("T")

TRANSACTIONS_FILE = "transactions.jsonl"
CATEGORIES_FILE = "categories.jsonl"
BUDGETS_FILE = "budgets.jsonl"
RECURRING_FILE = "recurring.jsonl"
DATA_FILES = (TRANSACTIONS_FILE, CATEGORIES_FILE, BUDGETS_FILE, RECURRING_FILE)
DEFAULT_CATEGORIES = ("food", "transport", "rent", "salary", "etc")  # 결정 5


class JsonlFile:
    """JSONL 파일 하나를 다루는 가장 아래 층."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def _broken(self, line_no: int | None, what: str) -> StorageError:
        where = f"{self.path.name} {line_no}번째 줄" if line_no else self.path.name
        return StorageError(
            f"{where}{what}",
            f"{self.path.parent / 'backups'} 의 백업으로 되돌리거나 그 줄을 고친 뒤 다시 실행하세요.",
        )

    def stream(self, convert: Callable[[Record], T] = lambda record: record) -> Iterator[T]:
        """한 줄씩 읽어 convert 로 바꿔 넘긴다. 파일 전체를 리스트로 만들지 않는다.

        JSON 문법이 깨졌거나, dict 가 아니거나, convert 가 실패하면(필드 빠짐·형식 오류)
        "몇 번째 줄"을 알려 주는 StorageError 로 바꾼다 (결정 11: 파일 오류 = 종료 코드 3).
        """
        try:
            with open(self.path, encoding="utf-8") as file:
                for line_no, line in enumerate(file, start=1):
                    if not line.strip():
                        continue
                    try:
                        record = json.loads(line)
                    except json.JSONDecodeError:
                        raise self._broken(line_no, "이 깨져 있습니다 (JSON 형식 아님).") from None
                    if not isinstance(record, dict):
                        raise self._broken(line_no, "이 올바른 기록이 아닙니다 (JSON 객체가 아님).")
                    try:
                        value = convert(record)
                    except (KeyError, TypeError, ValueError) as error:
                        raise self._broken(line_no, f"의 내용이 올바르지 않습니다 ({type(error).__name__}: {error}).") from None
                    yield value
        except FileNotFoundError:
            return  # 파일이 없으면 빈 데이터로 본다
        except UnicodeDecodeError:
            raise self._broken(None, " 이 UTF-8 텍스트가 아닙니다.") from None

    def append(self, record: Record) -> None:
        """파일 끝에 한 줄 덧붙인다."""
        self.append_many([record])

    def append_many(self, records: Iterable[Record]) -> None:
        """파일 끝에 여러 줄을 덧붙인다. 마지막 줄에 줄바꿈이 빠져 있으면 먼저 채운다.

        (편집기로 고치거나 이전 쓰기가 끊기면 줄바꿈 없이 끝날 수 있다. 그대로 붙이면 두 거래가 한 줄로 합쳐져 깨진다)
        records 가 제너레이터여도 한 건씩 받아 바로 쓴다.
        """
        with open(self.path, "a+b") as file:
            file.seek(0, os.SEEK_END)
            if file.tell() > 0:
                file.seek(-1, os.SEEK_END)
                if file.read(1) != b"\n":
                    file.write(b"\n")
            for record in records:
                file.write((json.dumps(record, ensure_ascii=False) + "\n").encode("utf-8"))

    def rewrite(self, records: Iterable[Record], keep: Callable[[], bool] = lambda: True) -> bool:
        """records 를 임시 파일에 모두 쓴 뒤 원본과 바꿔 끼운다 (원자적 교체).

        다 쓴 뒤 keep() 이 False 면 교체하지 않고 임시 파일을 버린다 (바뀐 게 없을 때). 교체했으면 True.
        """
        fd, tmp_name = tempfile.mkstemp(prefix=f".{self.path.name}.", suffix=".tmp", dir=self.path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as tmp:
                for record in records:
                    tmp.write(json.dumps(record, ensure_ascii=False) + "\n")
                tmp.flush()
                os.fsync(tmp.fileno())  # 디스크에 실제로 쓰였는지까지 기다린다
            if not keep():
                Path(tmp_name).unlink()
                return False
            if self.path.exists():  # mkstemp 는 0600 으로 만든다. 원래 파일 권한을 그대로 옮긴다
                os.chmod(tmp_name, self.path.stat().st_mode & 0o777)
            os.replace(tmp_name, self.path)  # 같은 폴더 안의 rename 이라 한 번에 바뀐다
            return True
        except BaseException:
            Path(tmp_name).unlink(missing_ok=True)  # 실패하면 임시 파일만 지우고 원본은 그대로
            raise


class TransactionRepository:
    """거래 파일. 읽기는 모두 제너레이터, 바꾸기는 모두 rewrite 로."""

    ID_PREFIX = "TX-"

    def __init__(self, file: JsonlFile) -> None:
        self.file = file

    def stream(self) -> Iterator[Transaction]:
        return self.file.stream(Transaction.from_dict)

    def add(self, tx: Transaction) -> None:
        self.file.append(tx.to_dict())

    def next_id(self) -> str:
        """남아 있는 거래 중 가장 큰 번호 + 1 (결정 6). 중간 번호를 지워도 그 번호는 다시 쓰지 않지만, 맨 마지막 번호를 지우면 다시 쓰인다."""
        largest = max((tx.number for tx in self.stream()), default=0)
        return f"{self.ID_PREFIX}{largest + 1:06d}"

    def find(self, tx_id: str) -> Transaction | None:
        return next((tx for tx in self.stream() if tx.id == tx_id), None)

    def update_where(self, change: Callable[[Transaction], Transaction | None]) -> int:
        """모든 거래에 change 를 적용해 다시 쓴다. change 가 None 을 돌려주면 그 거래는 지운다.

        파일을 한 번만 훑으며 임시 파일에 쓰고, 바뀌거나 지워진 게 0건이면 교체하지 않는다.
        바뀌거나 지워진 건수를 돌려준다.
        """
        changed = 0

        def updated() -> Iterator[Record]:
            nonlocal changed
            for tx in self.stream():
                new = change(tx)
                if new != tx:
                    changed += 1
                if new is not None:
                    yield new.to_dict()

        self.file.rewrite(updated(), keep=lambda: changed > 0)
        return changed


class CategoryStore:
    def __init__(self, file: JsonlFile) -> None:
        self.file = file

    def stream(self) -> Iterator[str]:
        return self.file.stream(lambda record: str(record["name"]))

    def names(self) -> list[str]:
        return list(self.stream())

    def exists(self, name: str) -> bool:
        return any(existing == name for existing in self.stream())

    def add(self, name: str) -> None:
        self.file.append({"name": name})

    def remove(self, name: str) -> None:
        self.file.rewrite({"name": existing} for existing in self.stream() if existing != name)


class BudgetStore:
    def __init__(self, file: JsonlFile) -> None:
        self.file = file

    def stream(self) -> Iterator[Budget]:
        return self.file.stream(lambda record: Budget(month=str(record["month"]), amount=int(record["amount"])))

    def get(self, month: str) -> Budget | None:
        return next((budget for budget in self.stream() if budget.month == month), None)

    def set(self, budget: Budget) -> None:
        """같은 달 예산이 있으면 바꾸고, 없으면 추가한다."""
        others = (b for b in self.stream() if b.month != budget.month)
        self.file.rewrite([*({"month": b.month, "amount": b.amount} for b in others), {"month": budget.month, "amount": budget.amount}])


class RecurringStore:
    ID_PREFIX = "RC-"

    def __init__(self, file: JsonlFile) -> None:
        self.file = file

    def stream(self) -> Iterator[RecurringRule]:
        return self.file.stream(RecurringRule.from_dict)

    def next_id(self) -> str:
        largest = max((rule.number for rule in self.stream()), default=0)
        return f"{self.ID_PREFIX}{largest + 1:06d}"

    def add(self, rule: RecurringRule) -> None:
        self.file.append(rule.to_dict())

    def update_where(self, change: Callable[[RecurringRule], RecurringRule | None]) -> int:
        """TransactionRepository.update_where 와 같다: 바꾸거나(None 이면 지우고) 바뀐 건수를 돌려준다."""
        changed = 0

        def updated() -> Iterator[Record]:
            nonlocal changed
            for rule in self.stream():
                new = change(rule)
                if new != rule:
                    changed += 1
                if new is not None:
                    yield new.to_dict()

        self.file.rewrite(updated(), keep=lambda: changed > 0)
        return changed


class Storage:
    """데이터 폴더 하나에 있는 파일들을 묶는다."""

    def __init__(self, data_dir: str | Path) -> None:
        self.data_dir = Path(data_dir)
        self.transactions = TransactionRepository(JsonlFile(self.data_dir / TRANSACTIONS_FILE))
        self.categories = CategoryStore(JsonlFile(self.data_dir / CATEGORIES_FILE))
        self.budgets = BudgetStore(JsonlFile(self.data_dir / BUDGETS_FILE))
        self.recurring = RecurringStore(JsonlFile(self.data_dir / RECURRING_FILE))

    def initialize(self) -> list[str]:
        """폴더·파일이 없으면 만들고, 사용자에게 보여 줄 안내 문구를 돌려준다."""
        notices: list[str] = []
        try:
            self.data_dir.mkdir(parents=True, exist_ok=True)
            created = [name for name in DATA_FILES if not (self.data_dir / name).exists()]
            for name in created:
                (self.data_dir / name).touch()
        except OSError as error:
            raise StorageError(f"데이터 폴더를 만들지 못했습니다: {self.data_dir} ({error.strerror})", "--data-dir 로 쓸 수 있는 폴더를 지정하세요.") from None
        if created:
            notices.append(f"[안내] 데이터 파일을 만들었습니다: {self.data_dir}/ ({', '.join(created)})")
        if not self.categories.names():
            for name in DEFAULT_CATEGORIES:
                self.categories.add(name)
            notices.append(f"[안내] 기본 카테고리를 만들었습니다: {', '.join(DEFAULT_CATEGORIES)} (category add 로 추가)")
        return notices
