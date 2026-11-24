"""서비스 계층: 가계부의 규칙(비즈니스 로직)을 맡는다.

- CLI 는 "입력을 받아 서비스에 넘기고 결과를 출력"만 한다.
- 저장소는 "파일 읽기·쓰기"만 한다.
- 그 사이의 규칙(등록된 카테고리만 허용, 사용 중인 카테고리는 지우지 않음, id 발급 등)은 여기 있다.
그래서 같은 규칙을 대화형 add 와 CSV import 가 함께 쓸 수 있다.
"""

import heapq
from dataclasses import dataclass, replace
from typing import Iterable, Iterator

from .errors import NotFoundError, ValidationError
from .models import Transaction, TxType, parse_category_name
from .storage import Storage


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
        return sum(1 for tx in self.storage.transactions.stream() if tx.category == name)

    def remove_category(self, name: str, replace_with: str | None = None) -> int:
        """카테고리를 지운다. 사용 중이면 막고, replace_with 를 주면 거래를 옮긴 뒤 지운다 (결정 3).

        옮긴 거래 수를 돌려준다.
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
                    f"'{name}' 카테고리를 쓰는 거래가 {in_use}건 있어 삭제할 수 없습니다.",
                    f"다른 카테고리로 옮기며 삭제: category remove {name} --replace-with <카테고리>",
                )
            # 거래를 먼저 옮기고(원자적 재작성) 그다음 카테고리를 지운다.
            # 중간에 멈춰도 "카테고리는 남아 있고 거래는 옮겨진" 상태라 데이터가 어긋나지 않는다.
            moved = self.storage.transactions.update_where(
                lambda tx: replace(tx, category=replace_with) if tx.category == name else tx
            )
        self.storage.categories.remove(name)
        return moved

    # ---- 거래 --------------------------------------------------------------

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
