"""모델 계층: 데이터 모양(dataclass)과 값 검증.

파일 저장 형식(dict)과 프로그램 안의 객체(Transaction 등)를 오가는 변환도 여기서 한다.
검증 함수는 문자열을 받아 "올바른 값"을 돌려주거나 ValidationError 를 던진다.
대화형 입력(add)·옵션(update)·CSV(import) 어디서 들어온 값이든 같은 함수로 검사한다.
"""

from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from typing import Any, Literal

from .errors import ValidationError

TxType = Literal["income", "expense"]
TX_TYPES: tuple[str, ...] = ("income", "expense")
MAX_CATEGORY_LENGTH = 20


@dataclass(frozen=True)
class Transaction:
    """거래 한 건. frozen: 만든 뒤 바꿀 수 없고, 수정은 replace 로 새 객체를 만든다."""

    id: str
    type: TxType
    date: str  # YYYY-MM-DD. 문자열끼리 비교해도 날짜 순서와 같다
    amount: int  # 양의 정수(원)
    category: str
    memo: str = ""
    tags: tuple[str, ...] = field(default_factory=tuple)
    recurring_id: str | None = None  # 반복 규칙으로 만든 거래면 그 규칙 id

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["tags"] = list(self.tags)
        if self.recurring_id is None:
            del data["recurring_id"]
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Transaction":
        return cls(
            id=str(data["id"]),
            type=data["type"],
            date=str(data["date"]),
            amount=int(data["amount"]),
            category=str(data["category"]),
            memo=str(data.get("memo", "")),
            tags=tuple(data.get("tags", ())),
            recurring_id=data.get("recurring_id"),
        )

    @property
    def month(self) -> str:
        return self.date[:7]

    @property
    def sort_key(self) -> tuple[str, str]:
        """최신순 정렬 기준: 날짜, 같은 날이면 id (결정 7)."""
        return (self.date, self.id)


@dataclass(frozen=True)
class Budget:
    month: str  # YYYY-MM
    amount: int


# ---- 검증 ---------------------------------------------------------------

def parse_date(text: str) -> str:
    value = text.strip()
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise ValidationError("날짜 형식이 올바르지 않습니다 (YYYY-MM-DD).", "예: 2024-01-15") from None
    if parsed.isoformat() != value:  # strptime 은 2024-1-5 도 받아 주므로 자릿수까지 맞는지 본다
        raise ValidationError("날짜는 0을 채운 YYYY-MM-DD 형식이어야 합니다.", f"예: {parsed.isoformat()}")
    return value


def parse_month(text: str) -> str:
    value = text.strip()
    try:
        parsed = datetime.strptime(value, "%Y-%m")
    except ValueError:
        raise ValidationError("월 형식이 올바르지 않습니다 (YYYY-MM).", "예: 2024-01") from None
    if parsed.strftime("%Y-%m") != value:
        raise ValidationError("월은 0을 채운 YYYY-MM 형식이어야 합니다.", f"예: {parsed.strftime('%Y-%m')}")
    return value


def parse_amount(text: str | int) -> int:
    raw = str(text).strip().replace(",", "")
    try:
        amount = int(raw)
    except ValueError:
        raise ValidationError(f"금액은 숫자여야 합니다: {text}", "원 단위 양의 정수로 입력하세요. 예: 15000") from None
    if amount <= 0:
        raise ValidationError("금액은 0보다 커야 합니다.", "지출도 양수로 쓰고, 타입(expense)으로 구분합니다.")
    return amount


def parse_type(text: str) -> TxType:
    value = text.strip().lower()
    if value not in TX_TYPES:
        raise ValidationError(f"타입은 income 또는 expense 여야 합니다: {text}", "수입은 income, 지출은 expense")
    return value  # type: ignore[return-value]


def parse_tags(text: str) -> tuple[str, ...]:
    """'meal, lunch,,meal' → ('meal', 'lunch'): 공백·빈 값·중복을 정리한다."""
    seen: list[str] = []
    for tag in text.split(","):
        tag = tag.strip()
        if tag and tag not in seen:
            seen.append(tag)
    return tuple(seen)


def parse_category_name(text: str) -> str:
    name = text.strip()
    if not name:
        raise ValidationError("카테고리 이름이 비었습니다.", "예: food")
    if len(name) > MAX_CATEGORY_LENGTH or "," in name:
        raise ValidationError(f"카테고리 이름은 쉼표 없이 {MAX_CATEGORY_LENGTH}자 이하여야 합니다: {name}")
    return name


def today() -> str:
    return date.today().isoformat()
