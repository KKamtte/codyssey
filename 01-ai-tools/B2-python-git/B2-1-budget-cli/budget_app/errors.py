"""앱에서 쓰는 예외와 종료 코드.

사용자에게 보여 줄 오류는 모두 AppError 계열로 던지고, 맨 바깥의 @handle_errors 가
"[오류] 원인" + "[힌트] 해결 방법"으로 출력한 뒤 exit_code 로 종료한다 (스택트레이스 없음).
"""

EXIT_OK = 0
EXIT_INPUT = 1  # 입력·검증 오류, 없는 데이터
EXIT_USAGE = 2  # 사용법 오류 (argparse 가 쓰는 값과 같다)
EXIT_STORAGE = 3  # 파일·저장 오류


class AppError(Exception):
    """사용자에게 원인과 힌트를 보여 주고 종료하는 오류."""

    exit_code = EXIT_INPUT

    def __init__(self, message: str, hint: str = "") -> None:
        super().__init__(message)
        self.message = message
        self.hint = hint


class ValidationError(AppError):
    """입력 값이 규칙에 맞지 않음 (날짜 형식, 금액, type, 카테고리 등)."""


class NotFoundError(AppError):
    """찾는 데이터(id, 카테고리 등)가 없음."""


class StorageError(AppError):
    """데이터 파일을 읽거나 쓰지 못함."""

    exit_code = EXIT_STORAGE
