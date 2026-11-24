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
from typing import Any, Callable, Iterable, Iterator

from .errors import StorageError
from .models import Budget, Transaction

Record = dict[str, Any]

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

    def stream(self) -> Iterator[Record]:
        """한 줄씩 읽어 dict 로 넘긴다. 파일 전체를 리스트로 만들지 않는다."""
        try:
            with open(self.path, encoding="utf-8") as file:
                for line_no, line in enumerate(file, start=1):
                    if not line.strip():
                        continue
                    try:
                        yield json.loads(line)
                    except json.JSONDecodeError:
                        raise StorageError(
                            f"{self.path.name} {line_no}번째 줄이 깨져 있습니다.",
                            "data/backups/ 의 백업으로 되돌리거나 그 줄을 고친 뒤 다시 실행하세요.",
                        ) from None
        except FileNotFoundError:
            return  # 파일이 없으면 빈 데이터로 본다

    def append(self, record: Record) -> None:
        with open(self.path, "a", encoding="utf-8") as file:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")

    def rewrite(self, records: Iterable[Record]) -> None:
        """records 를 임시 파일에 모두 쓴 뒤 원본과 바꿔 끼운다 (원자적 교체)."""
        fd, tmp_name = tempfile.mkstemp(prefix=f".{self.path.name}.", suffix=".tmp", dir=self.path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as tmp:
                for record in records:
                    tmp.write(json.dumps(record, ensure_ascii=False) + "\n")
                tmp.flush()
                os.fsync(tmp.fileno())  # 디스크에 실제로 쓰였는지까지 기다린다
            os.replace(tmp_name, self.path)  # 같은 폴더 안의 rename 이라 한 번에 바뀐다
        except BaseException:
            Path(tmp_name).unlink(missing_ok=True)  # 실패하면 임시 파일만 지우고 원본은 그대로
            raise


class TransactionRepository:
    """거래 파일. 읽기는 모두 제너레이터, 바꾸기는 모두 rewrite 로."""

    ID_PREFIX = "TX-"

    def __init__(self, file: JsonlFile) -> None:
        self.file = file

    def stream(self) -> Iterator[Transaction]:
        for record in self.file.stream():
            yield Transaction.from_dict(record)

    def add(self, tx: Transaction) -> None:
        self.file.append(tx.to_dict())

    def next_id(self) -> str:
        """지금까지 쓴 가장 큰 번호 + 1 (결정 6). 지운 번호는 다시 쓰지 않는다."""
        largest = max((int(tx.id.removeprefix(self.ID_PREFIX)) for tx in self.stream()), default=0)
        return f"{self.ID_PREFIX}{largest + 1:06d}"

    def find(self, tx_id: str) -> Transaction | None:
        return next((tx for tx in self.stream() if tx.id == tx_id), None)

    def update_where(self, change: Callable[[Transaction], Transaction | None]) -> int:
        """모든 거래에 change 를 적용해 다시 쓴다. change 가 None 을 돌려주면 그 거래는 지운다.

        바뀌거나 지워진 건수를 돌려준다. 0건이면 파일을 다시 쓰지 않는다.
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

        # 먼저 바뀔 게 있는지만 훑어보고, 있을 때만 다시 쓴다
        if not any(change(tx) != tx for tx in self.stream()):
            return 0
        self.file.rewrite(updated())
        return changed


class CategoryStore:
    def __init__(self, file: JsonlFile) -> None:
        self.file = file

    def names(self) -> list[str]:
        return [record["name"] for record in self.file.stream()]

    def exists(self, name: str) -> bool:
        return any(record["name"] == name for record in self.file.stream())

    def add(self, name: str) -> None:
        self.file.append({"name": name})

    def remove(self, name: str) -> None:
        self.file.rewrite(record for record in self.file.stream() if record["name"] != name)


class BudgetStore:
    def __init__(self, file: JsonlFile) -> None:
        self.file = file

    def stream(self) -> Iterator[Budget]:
        for record in self.file.stream():
            yield Budget(month=record["month"], amount=int(record["amount"]))

    def get(self, month: str) -> Budget | None:
        return next((budget for budget in self.stream() if budget.month == month), None)

    def set(self, budget: Budget) -> None:
        """같은 달 예산이 있으면 바꾸고, 없으면 추가한다."""
        others = (b for b in self.stream() if b.month != budget.month)
        self.file.rewrite([*({"month": b.month, "amount": b.amount} for b in others), {"month": budget.month, "amount": budget.amount}])


class Storage:
    """데이터 폴더 하나에 있는 파일들을 묶는다."""

    def __init__(self, data_dir: str | Path) -> None:
        self.data_dir = Path(data_dir)
        self.transactions = TransactionRepository(JsonlFile(self.data_dir / TRANSACTIONS_FILE))
        self.categories = CategoryStore(JsonlFile(self.data_dir / CATEGORIES_FILE))
        self.budgets = BudgetStore(JsonlFile(self.data_dir / BUDGETS_FILE))
        self.recurring_file = JsonlFile(self.data_dir / RECURRING_FILE)

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
