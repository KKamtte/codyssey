"""대화형 입력 도우미: 질문하고, 검증 함수가 통과할 때까지 다시 묻는다."""

from typing import Callable, TypeVar

from .decorators import print_error
from .errors import ValidationError

T = TypeVar("T")


def ask(label: str, parse: Callable[[str], T], *, default: str | None = None) -> T:
    """label 을 보여 주고 입력을 받는다. parse 가 ValidationError 를 던지면 이유를 보여 주고 다시 묻는다.

    default 가 있으면 빈 입력(엔터)일 때 그 값을 쓴다.
    입력이 끝나면(Ctrl+D, 파이프 끝) 저장하지 않고 ValidationError 로 멈춘다.
    """
    while True:
        try:
            text = input(f"{label}: ")
        except EOFError:
            raise ValidationError("입력이 중간에 끝났습니다. 저장하지 않았습니다.", "모든 항목을 입력한 뒤 엔터를 누르세요.") from None
        if not text.strip() and default is not None:
            text = default
        try:
            return parse(text)
        except ValidationError as error:
            print_error(error.message, error.hint)
