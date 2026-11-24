"""명령 함수에 공통으로 붙이는 데코레이터.

명령 함수는 `def cmd_xxx(args) -> int` 모양이다. 각 명령이 직접 try/except 나 로그 코드를
갖지 않도록, 예외 처리와 실행 기록을 여기로 떼어 낸다 (공통 관심사 분리).

    @log_execution      # 바깥: 몇 초 걸렸고 종료 코드가 몇인지 기록
    @handle_errors      # 안쪽: 예외를 "[오류]/[힌트]" 출력 + 종료 코드로 바꿈
    def cmd_add(args): ...
"""

import functools
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Callable

from .errors import EXIT_INPUT, EXIT_STORAGE, AppError

Command = Callable[..., int]

LOG_FILE_NAME = "app.log"
INTERRUPTED = 130  # Ctrl+C 로 멈췄을 때 셸이 쓰는 관례적인 종료 코드


def print_error(message: str, hint: str = "") -> None:
    print(f"[오류] {message}", file=sys.stderr)
    if hint:
        print(f"[힌트] {hint}", file=sys.stderr)


def handle_errors(func: Command) -> Command:
    """예외를 사용자용 메시지와 종료 코드로 바꾼다. 스택트레이스는 보여 주지 않는다."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> int:
        try:
            return func(*args, **kwargs)
        except AppError as error:
            print_error(error.message, error.hint)
            return error.exit_code
        except KeyboardInterrupt:
            print("\n[중단] 입력을 멈췄습니다. 저장하지 않았습니다.", file=sys.stderr)
            return INTERRUPTED
        except OSError as error:
            print_error(f"파일을 읽거나 쓰지 못했습니다: {error.strerror or error}", "데이터 폴더 경로와 권한을 확인하세요 (--data-dir).")
            return EXIT_STORAGE
        except Exception as error:  # 예상하지 못한 오류도 스택트레이스 없이 끝낸다
            print_error(f"예상하지 못한 문제가 생겼습니다: {type(error).__name__}: {error}", "같은 명령을 다시 실행해 보고, 반복되면 data/app.log 를 확인하세요.")
            return EXIT_INPUT

    return wrapper


def log_execution(func: Command) -> Command:
    """명령 이름, 종료 코드, 걸린 시간을 데이터 폴더의 app.log 에 한 줄씩 남긴다."""

    @functools.wraps(func)
    def wrapper(args, *rest, **kwargs) -> int:
        started = time.perf_counter()
        code = func(args, *rest, **kwargs)
        elapsed_ms = (time.perf_counter() - started) * 1000
        _append_log(getattr(args, "data_dir", None), getattr(args, "command_name", func.__name__), code, elapsed_ms)
        return code

    return wrapper


def _append_log(data_dir: str | None, command: str, code: int, elapsed_ms: float) -> None:
    if not data_dir:
        return
    line = f"{datetime.now().isoformat(timespec='seconds')}\t{command}\texit={code}\t{elapsed_ms:.1f}ms\n"
    try:
        path = Path(data_dir)
        path.mkdir(parents=True, exist_ok=True)
        with open(path / LOG_FILE_NAME, "a", encoding="utf-8") as log:
            log.write(line)
    except OSError:
        pass  # 기록 실패가 명령 결과를 바꾸면 안 된다
