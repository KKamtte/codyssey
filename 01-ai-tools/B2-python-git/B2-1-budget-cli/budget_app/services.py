"""서비스 계층: 가계부의 규칙(비즈니스 로직)을 맡는다.

- CLI 는 "입력을 받아 서비스에 넘기고 결과를 출력"만 한다.
- 저장소는 "파일 읽기·쓰기"만 한다.
- 그 사이의 규칙(등록된 카테고리만 허용, 사용 중인 카테고리는 지우지 않음, id 발급 등)은 여기 있다.
그래서 같은 규칙을 대화형 add 와 CSV import 가 함께 쓸 수 있다.
"""

import heapq
import shutil
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, replace
from typing import Iterable, Iterator

from .errors import NotFoundError, ValidationError
from .csv_io import read_rows, write_transactions
from .models import Budget, RecurringRule, Transaction, TxType, parse_amount, parse_category_name, parse_date, parse_rule_id, parse_tags, parse_tx_id, parse_type
from .storage import DATA_FILES, Storage


@dataclass(frozen=True)
class SearchCriteria:
    """search 조건. 비어 있는(None) 조건은 검사하지 않는다."""

    date_from: str | None = None
    date_to: str | None = None
    category: str | None = None
    type: TxType | None = None
    q: str | None = None  # 메모에 들어 있는 글자 (대소문자 무시)
    tag: str | None = None

    def matches(self, tx: Transaction) -> bool:
        if self.date_from and tx.date < self.date_from:  # YYYY-MM-DD 문자열 비교 = 날짜 비교
            return False
        if self.date_to and tx.date > self.date_to:
            return False
        if self.category and tx.category != self.category:
            return False
        if self.type and tx.type != self.type:
            return False
        if self.q and self.q.lower() not in tx.memo.lower():
            return False
        if self.tag and self.tag not in tx.tags:
            return False
        return True


@dataclass(frozen=True)
class Page:
    """최신순 상위 N개와, 조건에 맞은 전체 건수."""

    items: list[Transaction]
    total: int


@dataclass(frozen=True)
class ApplyResult:
    created: list[Transaction]
    skipped: list[tuple[RecurringRule, str]]


@dataclass(frozen=True)
class ImportResult:
    imported: int
    skipped: list[tuple[int, str]]  # (CSV 행 번호, 건너뛴 이유)


@dataclass(frozen=True)
class MonthSummary:
    month: str
    count: int
    income: int
    expense: int
    top_expenses: list[tuple[str, int]]  # (카테고리, 지출 합계) 큰 순서
    budget: Budget | None

    @property
    def balance(self) -> int:
        return self.income - self.expense

    @property
    def budget_rate(self) -> float | None:
        """예산 대비 지출 비율(%). 예산이 없으면 None."""
        return self.expense / self.budget.amount * 100 if self.budget else None

    @property
    def over_budget(self) -> int:
        """예산을 넘은 금액. 넘지 않았거나 예산이 없으면 0."""
        return max(self.expense - self.budget.amount, 0) if self.budget else 0


def summarize(transactions: Iterable[Transaction], month: str, top: int, budget: Budget | None) -> MonthSummary:
    """한 달 요약을 파일을 한 번 훑으며 계산한다.

    거래를 모아 두지 않고 합계만 더한다. 메모리에 남는 건 카테고리별 합계(카테고리 수만큼)뿐이다.
    """
    if top < 1:
        raise ValidationError(f"--top 은 1 이상이어야 합니다: {top}", "예: --top 3")
    count = income = expense = 0
    by_category: dict[str, int] = {}
    for tx in transactions:
        if tx.month != month:
            continue
        count += 1
        if tx.type == "income":
            income += tx.amount
        else:
            expense += tx.amount
            by_category[tx.category] = by_category.get(tx.category, 0) + tx.amount
    # 금액이 큰 순서, 같으면 이름 순서로 상위 top 개
    top_expenses = sorted(by_category.items(), key=lambda item: (-item[1], item[0]))[:top]
    return MonthSummary(month, count, income, expense, top_expenses, budget)


def latest(transactions: Iterable[Transaction], limit: int) -> Page:
    """스트리밍으로 들어오는 거래 중 최신 limit 개만 고른다 (결정 7).

    heapq.nlargest 는 크기 limit 인 힙만 유지하며 한 건씩 비교한다.
    그래서 거래가 N건이어도 메모리에는 limit 개만 남는다 (전체를 리스트로 만들어 정렬하지 않음).
    """
    if limit < 1:
        raise ValidationError(f"--limit 는 1 이상이어야 합니다: {limit}", "예: --limit 10")
    total = 0

    def counted() -> Iterator[Transaction]:
        nonlocal total
        for tx in transactions:
            total += 1
            yield tx

    items = heapq.nlargest(limit, counted(), key=lambda tx: tx.sort_key)
    return Page(items=items, total=total)


class BudgetService:
    def __init__(self, storage: Storage) -> None:
        self.storage = storage

    # ---- 카테고리 ----------------------------------------------------------

    def category_names(self) -> list[str]:
        return self.storage.categories.names()

    def require_category(self, name: str) -> str:
        """등록된 카테고리인지 확인한다. 아니면 목록을 힌트로 보여 준다."""
        if not self.storage.categories.exists(name):
            raise ValidationError(
                f"등록되지 않은 카테고리입니다: {name}",
                f"등록된 카테고리: {', '.join(self.category_names())} (새로 만들려면 category add {name})",
            )
        return name

    def check_new_category(self, raw_name: str) -> str:
        """새 카테고리로 쓸 수 있는 이름인지(형식, 중복) 확인한다. 대화형 입력의 검증 함수로도 쓴다."""
        name = parse_category_name(raw_name)
        if self.storage.categories.exists(name):
            raise ValidationError(f"이미 있는 카테고리입니다: {name}", "category list 로 목록을 확인하세요.")
        return name

    def add_category(self, raw_name: str) -> str:
        name = self.check_new_category(raw_name)
        self.storage.categories.add(name)
        return name

    def count_in_category(self, name: str) -> int:
        """이 카테고리를 쓰는 거래 + 반복 규칙 수."""
        in_transactions = sum(1 for tx in self.storage.transactions.stream() if tx.category == name)
        in_rules = sum(1 for rule in self.storage.recurring.stream() if rule.category == name)
        return in_transactions + in_rules

    def remove_category(self, name: str, replace_with: str | None = None) -> int:
        """카테고리를 지운다. 사용 중이면 막고, replace_with 를 주면 거래·반복 규칙을 옮긴 뒤 지운다 (결정 3).

        옮긴 거래·규칙 수를 돌려준다.
        """
        if not self.storage.categories.exists(name):
            raise NotFoundError(f"없는 카테고리입니다: {name}", f"등록된 카테고리: {', '.join(self.category_names())}")

        # 대체 카테고리를 줬다면, 쓰는 거래가 있든 없든 먼저 확인한다 (오타를 조용히 넘기지 않음)
        if replace_with is not None:
            if replace_with == name:
                raise ValidationError("같은 카테고리로는 옮길 수 없습니다.", "다른 카테고리 이름을 주세요.")
            self.require_category(replace_with)

        in_use = self.count_in_category(name)
        moved = 0
        if in_use:
            if replace_with is None:
                raise ValidationError(
                    f"'{name}' 카테고리를 쓰는 거래·반복 규칙이 {in_use}건 있어 삭제할 수 없습니다.",
                    f"다른 카테고리로 옮기며 삭제: category remove {name} --replace-with <카테고리>",
                )
            # 거래·규칙을 먼저 옮기고(원자적 재작성) 그다음 카테고리를 지운다.
            # 중간에 멈춰도 "카테고리는 남아 있고 일부는 옮겨진" 상태라 없는 카테고리를 가리키는 데이터가 생기지 않는다.
            moved = self.storage.transactions.update_where(
                lambda tx: replace(tx, category=replace_with) if tx.category == name else tx
            )
            moved += self.storage.recurring.update_where(
                lambda rule: replace(rule, category=replace_with) if rule.category == name else rule
            )
        self.storage.categories.remove(name)
        return moved

    # ---- 반복 내역 (보너스) ----------------------------------------------------

    def add_rule(self, *, day: int, type: TxType, category: str, amount: int, memo: str = "") -> RecurringRule:
        self.require_category(category)
        rule = RecurringRule(self.storage.recurring.next_id(), day, type, category, amount, memo.strip())
        self.storage.recurring.add(rule)
        return rule

    def rules(self) -> list[RecurringRule]:
        return sorted(self.storage.recurring.stream(), key=lambda rule: (rule.day, rule.number))

    def remove_rule(self, raw_id: str) -> RecurringRule:
        rule_id = parse_rule_id(raw_id)
        found = next((rule for rule in self.storage.recurring.stream() if rule.id == rule_id), None)
        if found is None:
            raise NotFoundError(f"없는 반복 규칙입니다: {rule_id}", "recurring list 로 id 를 확인하세요.")
        self.storage.recurring.update_where(lambda rule: None if rule.id == rule_id else rule)
        return found

    def apply_rules(self, month: str) -> ApplyResult:
        """month 에 반복 규칙의 거래를 만든다. 이미 그 달에 만든 규칙은 건너뛴다 (두 번 실행해도 안전).

        "이미 만들었나"는 거래의 recurring_id 로 판단한다. 파일을 한 번 훑어 그 달에 만든 규칙 id 만 모은다.
        """
        done = {tx.recurring_id for tx in self.storage.transactions.stream() if tx.recurring_id and tx.month == month}
        categories = set(self.category_names())
        created: list[Transaction] = []
        skipped: list[tuple[RecurringRule, str]] = []
        for rule in self.rules():
            if rule.id in done:
                skipped.append((rule, "이 달에 이미 만들었습니다"))
            elif rule.category not in categories:
                skipped.append((rule, f"카테고리 '{rule.category}'가 없습니다"))
            else:
                created.append(self.add_transaction(
                    type=rule.type, date=rule.date_in(month), amount=rule.amount,
                    category=rule.category, memo=rule.memo, recurring_id=rule.id,
                ))
        return ApplyResult(created, skipped)

    # ---- 백업 (보너스) ---------------------------------------------------------

    def backup(self, now: datetime | None = None) -> Path:
        """데이터 파일을 backups/YYYYMMDD-HHMMSS/ 에 복사한다 (결정 13). 만든 폴더를 돌려준다.

        같은 초에 두 번 실행하면 -2, -3 을 붙여 이전 백업을 덮어쓰지 않는다.
        """
        stamp = (now or datetime.now()).strftime("%Y%m%d-%H%M%S")
        root = self.storage.data_dir / "backups"
        target, n = root / stamp, 2
        while target.exists():
            target, n = root / f"{stamp}-{n}", n + 1
        target.mkdir(parents=True)
        for name in DATA_FILES:
            source = self.storage.data_dir / name
            if source.exists():
                shutil.copy2(source, target / name)  # copy2: 수정 시각 같은 정보도 같이 복사
        return target

    # ---- 거래 --------------------------------------------------------------

    def get_transaction(self, raw_id: str) -> Transaction:
        tx_id = parse_tx_id(raw_id)
        tx = self.storage.transactions.find(tx_id)
        if tx is None:
            raise NotFoundError(f"없는 데이터입니다: {tx_id}", "list 나 search 로 id 를 확인하세요.")
        return tx

    def update_transaction(self, raw_id: str, changes: dict[str, object]) -> tuple[Transaction, Transaction]:
        """옵션으로 받은 필드만 바꾼다 (결정 2). (바꾸기 전, 바꾼 뒤)를 돌려준다.

        changes 는 이미 검증한 값만 담는다. 예: {"amount": 20000, "memo": "저녁"}
        """
        if not changes:
            raise ValidationError(
                "바꿀 항목이 없습니다.",
                "예: update --id TX-000003 --amount 20000 (--date --type --category --amount --memo --tags)",
            )
        old = self.get_transaction(raw_id)
        if "category" in changes:
            self.require_category(str(changes["category"]))
        new = replace(old, **changes)
        if new == old:
            raise ValidationError("지금 값과 같아서 바뀌는 것이 없습니다.", "다른 값을 주세요.")
        # 해당 거래만 새 것으로 바꿔 전체를 원자적으로 다시 쓴다
        self.storage.transactions.update_where(lambda tx: new if tx.id == old.id else tx)
        return old, new

    def delete_transaction(self, raw_id: str) -> Transaction:
        old = self.get_transaction(raw_id)
        self.storage.transactions.update_where(lambda tx: None if tx.id == old.id else tx)
        return old

    # ---- CSV 가져오기·내보내기 ------------------------------------------------

    def import_csv(self, path: str) -> ImportResult:
        """CSV 를 한 행씩 읽어 검증하고, 통과한 행만 거래로 추가한다.

        틀린 행은 건너뛰고 (행 번호, 사유)를 모은다. id 는 처음에 한 번만 구해 1씩 올린다
        (행마다 next_id() 를 부르면 그때마다 파일 전체를 다시 읽게 된다).
        """
        categories = set(self.category_names())
        number = int(self.storage.transactions.next_id()[3:])
        skipped: list[tuple[int, str]] = []
        imported = 0

        def valid_records() -> Iterator[dict]:
            nonlocal number, imported
            for line_no, row in read_rows(path):
                try:
                    category = parse_category_name(row.get("category", ""))
                    if category not in categories:
                        raise ValidationError(f"등록되지 않은 카테고리입니다: {category}")
                    tx = Transaction(
                        id=f"TX-{number:06d}",
                        type=parse_type(row.get("type", "")),
                        date=parse_date(row.get("date", "")),
                        amount=parse_amount(row.get("amount", "")),
                        category=category,
                        memo=row.get("memo", "").strip(),
                        tags=parse_tags(row.get("tags", "")),
                    )
                except ValidationError as error:
                    skipped.append((line_no, error.message))
                    continue
                number += 1
                imported += 1
                yield tx.to_dict()

        self.storage.transactions.file.append_many(valid_records())
        return ImportResult(imported, skipped)

    def export_csv(self, path: str, month: str | None, date_from: str | None, date_to: str | None) -> int:
        """조건에 맞는 거래를 날짜 순서로 CSV 에 쓴다. 쓴 건수를 돌려준다."""
        if month is None and date_from is None and date_to is None:
            raise ValidationError("내보낼 기간이 없습니다.", "--month YYYY-MM 또는 --from YYYY-MM-DD --to YYYY-MM-DD 를 주세요.")
        if month and (date_from or date_to):
            raise ValidationError("--month 와 --from/--to 는 함께 쓸 수 없습니다.", "둘 중 하나만 주세요.")
        if date_from and date_to and date_from > date_to:
            raise ValidationError(f"--from({date_from})이 --to({date_to})보다 늦습니다.", "기간의 앞뒤를 바꿔 주세요.")
        if month:
            date_from, date_to = f"{month}-01", f"{month}-31"  # YYYY-MM-DD 문자열 비교라 31일로 둬도 그 달만 걸린다
        criteria = SearchCriteria(date_from=date_from, date_to=date_to)
        # 조건에 맞는 것만 모아 날짜순으로 정렬한다 (내보내는 기간만큼만 메모리에 둔다)
        matching = sorted((tx for tx in self.storage.transactions.stream() if criteria.matches(tx)), key=lambda tx: tx.sort_key)
        return write_transactions(path, matching)

    # ---- 예산·요약 ----------------------------------------------------------

    def set_budget(self, month: str, amount: int) -> Budget | None:
        """월 예산을 저장한다 (같은 달이 있으면 바꿈). 바꾸기 전 예산을 돌려준다."""
        previous = self.storage.budgets.get(month)
        self.storage.budgets.set(Budget(month, amount))
        return previous

    def budgets(self, month: str | None = None) -> list[Budget]:
        found = [b for b in self.storage.budgets.stream() if month is None or b.month == month]
        return sorted(found, key=lambda b: b.month)

    def summary(self, month: str, top: int) -> MonthSummary:
        return summarize(self.storage.transactions.stream(), month, top, self.storage.budgets.get(month))

    def list_latest(self, limit: int) -> Page:
        return latest(self.storage.transactions.stream(), limit)

    def search(self, criteria: SearchCriteria, limit: int) -> Page:
        if criteria.date_from and criteria.date_to and criteria.date_from > criteria.date_to:
            raise ValidationError(f"--from({criteria.date_from})이 --to({criteria.date_to})보다 늦습니다.", "기간의 앞뒤를 바꿔 주세요.")
        matching = (tx for tx in self.storage.transactions.stream() if criteria.matches(tx))
        return latest(matching, limit)

    def add_transaction(
        self,
        *,
        type: TxType,
        date: str,
        amount: int,
        category: str,
        memo: str = "",
        tags: tuple[str, ...] = (),
        recurring_id: str | None = None,
    ) -> Transaction:
        """검증이 끝난 값으로 거래를 만들어 저장한다. 카테고리 확인과 id 발급은 여기서 한다."""
        self.require_category(category)
        tx = Transaction(
            id=self.storage.transactions.next_id(),
            type=type,
            date=date,
            amount=amount,
            category=category,
            memo=memo.strip(),
            tags=tags,
            recurring_id=recurring_id,
        )
        self.storage.transactions.add(tx)
        return tx
