"""CSV 가져오기·내보내기의 파일 입출력만 맡는다 (검증은 서비스 계층).

스키마는 원문에서 고정: date, type, category, amount, memo, tags (UTF-8, 헤더 포함).
tags 는 한 칸 안에 쉼표로 구분해 넣는다. 예: "meal,lunch" (csv 모듈이 따옴표를 알아서 붙인다)
"""

import csv
import os
import tempfile
from pathlib import Path
from typing import Iterable, Iterator

from .errors import ValidationError
from .models import Transaction

CSV_COLUMNS = ("date", "type", "category", "amount", "memo", "tags")
REQUIRED_COLUMNS = ("date", "type", "category", "amount")

Row = dict[str, str]


def read_rows(path: str | Path) -> Iterator[tuple[int, Row]]:
    """(행 번호, 행)을 한 줄씩 넘긴다. 행 번호는 헤더를 1행으로 센 엑셀식 번호."""
    path = Path(path)
    if not path.is_file():
        raise ValidationError(f"CSV 파일이 없습니다: {path}", "경로를 확인하세요. 예: import --from import.csv")
    # utf-8-sig: 엑셀이 저장한 CSV 맨 앞의 BOM(﻿)을 떼고 읽는다
    # 인코딩 오류는 헤더를 읽을 때도, 중간 행을 읽을 때도 날 수 있어 읽기 전체를 감싼다
    try:
        with open(path, encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            header = [name.strip() for name in (reader.fieldnames or [])]
            missing = [name for name in REQUIRED_COLUMNS if name not in header]
            if missing:
                raise ValidationError(
                    f"CSV 헤더에 필수 열이 없습니다: {', '.join(missing)}",
                    f"첫 줄을 {','.join(CSV_COLUMNS)} 로 맞추세요 (memo, tags 는 선택).",
                )
            reader.fieldnames = header
            for row in reader:
                yield reader.line_num, {key: (value or "") for key, value in row.items() if key is not None}
    except UnicodeDecodeError:
        raise ValidationError(f"CSV 가 UTF-8 이 아닙니다: {path}", "UTF-8 로 다시 저장하세요 (엑셀: CSV UTF-8).") from None


def write_transactions(path: str | Path, transactions: Iterable[Transaction]) -> int:
    """거래를 CSV 로 쓴다. 다 쓴 뒤 바꿔 끼우므로 중간에 실패해도 반쯤 쓴 파일이 남지 않는다. 쓴 행 수를 돌려준다."""
    path = Path(path)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent if str(path.parent) else ".")
    count = 0
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(CSV_COLUMNS)
            for tx in transactions:
                writer.writerow([tx.date, tx.type, tx.category, tx.amount, tx.memo, ",".join(tx.tags)])
                count += 1
        os.chmod(tmp_name, 0o644)
        os.replace(tmp_name, path)
    except BaseException:
        Path(tmp_name).unlink(missing_ok=True)
        raise
    return count
