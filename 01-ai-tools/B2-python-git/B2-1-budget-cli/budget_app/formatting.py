"""출력 포맷 계층: 거래 목록을 열 너비가 맞는 표로 만든다 (외부 라이브러리 없이).

터미널에서 한글·한자 같은 "넓은 글자"는 영문 두 칸을 차지한다. len() 은 글자 수만 세므로
그대로 맞추면 한글이 들어간 줄만 밀린다. 그래서 unicodedata.east_asian_width 로 칸 수를 센다.
"""

import unicodedata
from typing import Iterable, Sequence

from .models import Transaction

COLUMNS = ("ID", "날짜", "타입", "카테고리", "금액", "메모", "태그")
MAX_MEMO_WIDTH = 24


def display_width(text: str) -> int:
    """터미널에서 차지하는 칸 수. 넓은 글자(W, F)는 2칸, 나머지는 1칸."""
    return sum(2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1 for ch in text)


def truncate(text: str, max_width: int) -> str:
    """max_width 칸을 넘으면 잘라서 끝에 '…'를 붙인다."""
    if display_width(text) <= max_width:
        return text
    result, width = "", 0
    for ch in text:
        w = display_width(ch)
        if width + w > max_width - 1:
            break
        result, width = result + ch, width + w
    return result + "…"


def pad(text: str, width: int, align: str = "left") -> str:
    gap = " " * max(width - display_width(text), 0)
    return gap + text if align == "right" else text + gap


def format_amount(amount: int) -> str:
    return f"{amount:,}"


def transaction_row(tx: Transaction) -> tuple[str, ...]:
    return (
        tx.id,
        tx.date,
        tx.type,
        tx.category,
        format_amount(tx.amount),
        truncate(tx.memo, MAX_MEMO_WIDTH),
        ",".join(tx.tags),
    )


def table(headers: Sequence[str], rows: Iterable[Sequence[str]], right_align: Iterable[int] = ()) -> str:
    """머리글과 행으로 열 너비를 맞춘 표 문자열을 만든다."""
    rows = [list(row) for row in rows]
    right = set(right_align)
    widths = [max([display_width(h)] + [display_width(row[i]) for row in rows]) for i, h in enumerate(headers)]

    def line(cells: Sequence[str]) -> str:
        return " | ".join(pad(cell, widths[i], "right" if i in right else "left") for i, cell in enumerate(cells)).rstrip()

    separator = "-+-".join("-" * w for w in widths)
    return "\n".join([line(headers), separator, *(line(row) for row in rows)])


def transactions_table(transactions: Iterable[Transaction]) -> str:
    return table(COLUMNS, (transaction_row(tx) for tx in transactions), right_align=[COLUMNS.index("금액")])
