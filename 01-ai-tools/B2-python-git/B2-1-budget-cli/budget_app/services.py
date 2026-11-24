"""서비스 계층: 가계부의 규칙(비즈니스 로직)을 맡는다.

- CLI 는 "입력을 받아 서비스에 넘기고 결과를 출력"만 한다.
- 저장소는 "파일 읽기·쓰기"만 한다.
- 그 사이의 규칙(등록된 카테고리만 허용, 사용 중인 카테고리는 지우지 않음, id 발급 등)은 여기 있다.
그래서 같은 규칙을 대화형 add 와 CSV import 가 함께 쓸 수 있다.
"""

from dataclasses import replace

from .errors import NotFoundError, ValidationError
from .models import Transaction, TxType, parse_category_name
from .storage import Storage


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

    def add_category(self, raw_name: str) -> str:
        name = parse_category_name(raw_name)
        if self.storage.categories.exists(name):
            raise ValidationError(f"이미 있는 카테고리입니다: {name}", "category list 로 목록을 확인하세요.")
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

        in_use = self.count_in_category(name)
        moved = 0
        if in_use:
            if replace_with is None:
                raise ValidationError(
                    f"'{name}' 카테고리를 쓰는 거래가 {in_use}건 있어 삭제할 수 없습니다.",
                    f"다른 카테고리로 옮기며 삭제: category remove {name} --replace-with <카테고리>",
                )
            if replace_with == name:
                raise ValidationError("같은 카테고리로는 옮길 수 없습니다.", "다른 카테고리 이름을 주세요.")
            self.require_category(replace_with)
            # 거래를 먼저 옮기고(원자적 재작성) 그다음 카테고리를 지운다.
            # 중간에 멈춰도 "카테고리는 남아 있고 거래는 옮겨진" 상태라 데이터가 어긋나지 않는다.
            moved = self.storage.transactions.update_where(
                lambda tx: replace(tx, category=replace_with) if tx.category == name else tx
            )
        self.storage.categories.remove(name)
        return moved

    # ---- 거래 --------------------------------------------------------------

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
