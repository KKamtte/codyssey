"""모델 계층: 데이터 모양(dataclass)과 값 검증.

파일 저장 형식(dict)과 프로그램 안의 객체(Transaction 등)를 오가는 변환도 여기서 한다.
검증 함수는 문자열을 받아 "올바른 값"을 돌려주거나 ValidationError 를 던진다.
대화형 입력(add)·옵션(update)·CSV(import) 어디서 들어온 값이든 같은 함수로 검사한다.
"""

import re
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from typing import Any, Literal

from .errors import ValidationError

TxType = Literal["income", "expense"]
TX_TYPES: tuple[str, ...] = ("income", "expense")
MAX_CATEGORY_LENGTH = 20
TX_ID_PATTERN = re.compile(r"TX-(\d{6,})")
AMOUNT_PATTERN = re.compile(r"\d{1,3}(,\d{3})+|\d+")  # 15000 또는 15,000 (세 자리마다 쉼표)
MAX_AMOUNT = 10**12
CATEGORY_PATTERN = re.compile(r"[0-9A-Za-z가-힣_][0-9A-Za-z가-힣_-]*")  # 결정 17


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
        """파일 한 줄 → 거래. 형식이 틀리면 ValueError (저장소가 "몇 번째 줄" 오류로 바꾼다)."""
        tx = cls(
            id=str(data["id"]),
            type=data["type"],
            date=str(data["date"]),
            amount=data["amount"],
            category=str(data["category"]),
            memo=str(data.get("memo", "")),
            tags=tuple(str(tag) for tag in data.get("tags", ())),
            recurring_id=data.get("recurring_id"),
        )
        if not TX_ID_PATTERN.fullmatch(tx.id):
            raise ValueError(f"id 형식이 TX-000001 이 아닙니다: {tx.id}")
        if tx.type not in TX_TYPES:
            raise ValueError(f"type 이 income/expense 가 아닙니다: {tx.type}")
        if not isinstance(tx.amount, int) or isinstance(tx.amount, bool) or tx.amount <= 0:
            raise ValueError(f"amount 가 양의 정수가 아닙니다: {tx.amount!r}")
        try:
            parse_date(tx.date)
        except ValidationError:  # 입력 오류(AppError)가 아니라 "파일 내용 오류"로 다뤄야 하므로 ValueError 로 바꾼다
            raise ValueError(f"date 형식이 YYYY-MM-DD 가 아닙니다: {tx.date}") from None
        return tx

    @property
    def month(self) -> str:
        return self.date[:7]

    @property
    def number(self) -> int:
        """id 의 숫자 부분 (TX-000012 → 12)."""
        return int(self.id[3:])

    @property
    def sort_key(self) -> tuple[str, int]:
        """최신순 정렬 기준: 날짜, 같은 날이면 id 번호 (결정 7).

        id 를 문자열로 비교하면 TX-1000000 < TX-999999 가 되므로 번호(정수)로 비교한다.
        """
        return (self.date, self.number)


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
    raw = str(text).strip()
    if raw.startswith("-") and AMOUNT_PATTERN.fullmatch(raw[1:]):
        raise ValidationError("금액은 0보다 커야 합니다.", "지출도 양수로 쓰고, 타입(expense)으로 구분합니다.")
    # int() 는 "1_000", 전각 숫자 "１２３" 도 받아 주므로, 먼저 허용 형식(숫자, 세 자리 쉼표)만 통과시킨다
    if not raw.isascii() or not AMOUNT_PATTERN.fullmatch(raw):
        raise ValidationError(f"금액은 숫자여야 합니다: {text}", "원 단위 양의 정수로 입력하세요. 예: 15000 또는 15,000")
    amount = int(raw.replace(",", ""))
    if amount <= 0:
        raise ValidationError("금액은 0보다 커야 합니다.", "지출도 양수로 쓰고, 타입(expense)으로 구분합니다.")
    if amount > MAX_AMOUNT:
        raise ValidationError(f"금액이 너무 큽니다: {amount:,}", f"{MAX_AMOUNT:,}원 이하로 입력하세요.")
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


def parse_tx_id(text: str) -> str:
    value = text.strip().upper()
    if not TX_ID_PATTERN.fullmatch(value):
        raise ValidationError(f"id 형식이 올바르지 않습니다: {text}", "예: TX-000003 (list 로 확인)")
    return value


def parse_category_name(text: str) -> str:
    name = text.strip()
    if not name:
        raise ValidationError("카테고리 이름이 비었습니다.", "예: food")
    if len(name) > MAX_CATEGORY_LENGTH or not CATEGORY_PATTERN.fullmatch(name):
        raise ValidationError(
            f"카테고리 이름으로 쓸 수 없습니다: {name}",
            f"한글·영문·숫자·_·- 만, - 로 시작하지 않게, {MAX_CATEGORY_LENGTH}자 이하. 예: food, 식비, side_job",
        )
    return name


def today() -> str:
    return date.today().isoformat()
