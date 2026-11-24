"""CLI 계층: 명령어와 옵션을 해석하고 알맞은 명령 함수를 부른다.

여기는 "무엇을 입력받아 무엇을 출력하나"만 다룬다. 계산·검증·저장은 서비스와 저장소 계층이 맡는다.
"""

import argparse
from pathlib import Path
from typing import Sequence

from .decorators import handle_errors, log_execution
from .errors import EXIT_OK, AppError
from .models import parse_amount, parse_category_name, parse_date, parse_month, parse_tags, parse_type, today
from .prompts import ask
from .formatting import format_amount, transactions_table
from .services import BudgetService, Page, SearchCriteria
from .storage import Storage

DEFAULT_DATA_DIR = "data"
DEFAULT_LIMIT = 20
DEFAULT_TOP = 3


def open_service(args: argparse.Namespace) -> BudgetService:
    """데이터 폴더를 준비하고(처음이면 파일·기본 카테고리 생성) 서비스를 만든다."""
    storage = Storage(args.data_dir)
    for notice in storage.initialize():
        print(notice)
    return BudgetService(storage)


# ---- 명령 ---------------------------------------------------------------

@log_execution
@handle_errors
def cmd_add(args: argparse.Namespace) -> int:
    service = open_service(args)
    service.storage.transactions.next_id()  # 입력을 다 받은 뒤 파일 오류로 버려지지 않게, 먼저 파일을 한 번 읽어 확인
    categories = service.category_names()
    date = ask(f"날짜(YYYY-MM-DD, 엔터=오늘 {today()})", parse_date, default=today())
    tx_type = ask("타입(income/expense)", parse_type)
    category = ask(f"카테고리({', '.join(categories)})", lambda text: service.require_category(parse_category_name(text)))
    amount = ask("금액(양수)", parse_amount)
    memo = ask("메모(선택)", str.strip, default="")
    tags = ask("태그(쉼표로 구분, 없으면 엔터)", parse_tags, default="")
    tx = service.add_transaction(type=tx_type, date=date, amount=amount, category=category, memo=memo, tags=tags)
    print(f"[저장 완료] id={tx.id}")
    return EXIT_OK


def print_page(page: Page, empty_message: str) -> None:
    if not page.items:
        print(empty_message)
        return
    print(transactions_table(page.items))
    print(f"({page.total}건 중 최신 {len(page.items)}건)")


@log_execution
@handle_errors
def cmd_list(args: argparse.Namespace) -> int:
    service = open_service(args)
    print_page(service.list_latest(args.limit), "거래가 없습니다. add 로 첫 거래를 추가하세요.")
    return EXIT_OK


@log_execution
@handle_errors
def cmd_search(args: argparse.Namespace) -> int:
    service = open_service(args)
    criteria = SearchCriteria(
        date_from=parse_date(args.date_from) if args.date_from else None,
        date_to=parse_date(args.date_to) if args.date_to else None,
        category=args.category,
        type=args.type,
        q=args.q,
        tag=args.tag,
    )
    print_page(service.search(criteria, args.limit), "조건에 맞는 거래가 없습니다.")
    return EXIT_OK


UPDATE_FIELDS = {  # 옵션 이름 → 검증 함수. None 이 아닌(준) 옵션만 바꾼다
    "date": parse_date,
    "type": parse_type,
    "category": parse_category_name,
    "amount": parse_amount,
    "memo": str.strip,  # 빈 문자열("")을 주면 메모를 지운다
    "tags": parse_tags,  # 빈 문자열("")을 주면 태그를 지운다
}


def describe(value: object) -> str:
    if isinstance(value, tuple):
        return ",".join(value) or "(없음)"
    if isinstance(value, int):
        return format_amount(value)
    return str(value) if value != "" else "(없음)"


@log_execution
@handle_errors
def cmd_update(args: argparse.Namespace) -> int:
    service = open_service(args)
    changes = {name: parse(getattr(args, name)) for name, parse in UPDATE_FIELDS.items() if getattr(args, name) is not None}
    old, new = service.update_transaction(args.id, changes)
    diffs = [f"{name} {describe(getattr(old, name))} → {describe(getattr(new, name))}" for name in UPDATE_FIELDS if getattr(old, name) != getattr(new, name)]
    print(f"[수정 완료] {new.id}: {', '.join(diffs)}")
    return EXIT_OK


@log_execution
@handle_errors
def cmd_delete(args: argparse.Namespace) -> int:
    service = open_service(args)
    tx = service.delete_transaction(args.id)
    print(f"[삭제 완료] {tx.id} ({tx.date} {tx.type} {tx.category} {format_amount(tx.amount)}원)")
    return EXIT_OK


@log_execution
@handle_errors
def cmd_summary(args: argparse.Namespace) -> int:
    service = open_service(args)
    month = parse_month(args.month)
    s = service.summary(month, args.top)
    print(f"[{month} 요약]")
    if s.count == 0:
        print("데이터 없음 (이 달에 기록된 거래가 없습니다)")
        if s.budget:
            print(f"예산: {format_amount(s.budget.amount)}원 (사용 0원)")
        return EXIT_OK
    print(f"총 수입: {format_amount(s.income)}원")
    print(f"총 지출: {format_amount(s.expense)}원")
    print(f"잔액: {format_amount(s.balance)}원")
    if s.budget:
        print(f"예산: {format_amount(s.budget.amount)}원 (사용률 {s.budget_rate:.1f}%)")
        if s.over_budget:
            print(f"[경고] 예산을 {format_amount(s.over_budget)}원 초과했습니다.")
    else:
        print(f"예산: 없음 (budget set --month {month} --amount <금액> 으로 설정)")
    if s.top_expenses:
        print(f"\n지출 TOP {args.top}")
        for rank, (category, amount) in enumerate(s.top_expenses, start=1):
            print(f"{rank}) {category} {format_amount(amount)}원")
    return EXIT_OK


@log_execution
@handle_errors
def cmd_budget_set(args: argparse.Namespace) -> int:
    service = open_service(args)
    month, amount = parse_month(args.month), parse_amount(args.amount)
    previous = service.set_budget(month, amount)
    changed = f" (이전 {format_amount(previous.amount)}원)" if previous else ""
    print(f"[저장 완료] {month} 예산 {format_amount(amount)}원{changed}")
    return EXIT_OK


@log_execution
@handle_errors
def cmd_budget_show(args: argparse.Namespace) -> int:
    service = open_service(args)
    month = parse_month(args.month) if args.month else None
    budgets = service.budgets(month)
    if not budgets:
        print(f"{month} 예산이 없습니다." if month else "설정한 예산이 없습니다.")
        return EXIT_OK
    for budget in budgets:
        print(f"{budget.month}  {format_amount(budget.amount)}원")
    return EXIT_OK


MAX_SKIP_LINES = 20  # 건너뛴 행이 많으면 앞의 몇 개만 보여 준다


@log_execution
@handle_errors
def cmd_import(args: argparse.Namespace) -> int:
    service = open_service(args)
    result = service.import_csv(args.source)
    for line_no, reason in result.skipped[:MAX_SKIP_LINES]:
        print(f"[건너뜀] {line_no}행: {reason}")
    if len(result.skipped) > MAX_SKIP_LINES:
        print(f"[건너뜀] … 외 {len(result.skipped) - MAX_SKIP_LINES}행")
    print(f"[완료] imported={result.imported}, skipped={len(result.skipped)}")
    return EXIT_OK


@log_execution
@handle_errors
def cmd_export(args: argparse.Namespace) -> int:
    service = open_service(args)
    if Path(args.out).exists() and not args.force:
        raise AppError(f"이미 있는 파일입니다: {args.out}", "다른 이름을 주거나, 덮어쓰려면 --force 를 붙이세요.")
    count = service.export_csv(
        args.out,
        month=parse_month(args.month) if args.month else None,
        date_from=parse_date(args.date_from) if args.date_from else None,
        date_to=parse_date(args.date_to) if args.date_to else None,
    )
    print(f"[완료] {args.out} ({count} records)")
    return EXIT_OK


@log_execution
@handle_errors
def cmd_category_add(args: argparse.Namespace) -> int:
    service = open_service(args)
    # 인자로 주면 틀렸을 때 오류로 끝내고, 대화형이면 형식·중복이 맞을 때까지 다시 묻는다
    name = service.add_category(args.name if args.name is not None else ask("카테고리명", service.check_new_category))
    print(f"[저장 완료] category={name}")
    return EXIT_OK


@log_execution
@handle_errors
def cmd_category_list(args: argparse.Namespace) -> int:
    service = open_service(args)
    for name in service.category_names():
        print(f"- {name}")
    return EXIT_OK


@log_execution
@handle_errors
def cmd_category_remove(args: argparse.Namespace) -> int:
    service = open_service(args)
    moved = service.remove_category(args.name, args.replace_with)
    suffix = f" (거래 {moved}건을 {args.replace_with}(으)로 옮김)" if moved else ""
    print(f"[삭제 완료] category={args.name}{suffix}")
    return EXIT_OK


def _not_ready(step: str):
    """아직 만들지 않은 명령. 해당 단계에서 진짜 함수로 바꾼다."""

    @log_execution
    @handle_errors
    def command(args: argparse.Namespace) -> int:
        raise AppError(f"'{args.command_name}' 명령은 아직 구현하지 않았습니다.", f"작업 계획 {step} 단계에서 구현합니다.")

    return command


# ---- 파서 ---------------------------------------------------------------

def _common_options() -> argparse.ArgumentParser:
    """모든 명령에 붙는 공통 옵션. 명령 앞이든 뒤든 쓸 수 있게 하위 명령에도 붙인다."""
    common = argparse.ArgumentParser(add_help=False)
    # 하위 명령에서 주지 않으면 값을 넣지 않아(SUPPRESS) 맨 앞에서 준 값이나 기본값이 남는다
    common.add_argument("--data-dir", default=argparse.SUPPRESS, help=f"데이터 폴더 (기본: ./{DEFAULT_DATA_DIR})")
    return common


def _add_command(subparsers, name: str, help_text: str, func, common, **kwargs) -> argparse.ArgumentParser:
    parser = subparsers.add_parser(name, help=help_text, description=help_text, parents=[common], **kwargs)
    parser.set_defaults(func=func, command_name=name)
    return parser


def build_parser() -> argparse.ArgumentParser:
    common = _common_options()
    parser = argparse.ArgumentParser(
        prog="python -m budget_app",
        description="용돈 기입장: 수입·지출을 파일에 저장하고 검색·요약하는 콘솔 가계부",
    )
    parser.add_argument("--data-dir", default=DEFAULT_DATA_DIR, help=f"데이터 폴더 (기본: ./{DEFAULT_DATA_DIR})")
    sub = parser.add_subparsers(title="명령", metavar="<command>", required=True)

    _add_command(sub, "add", "거래 추가 (날짜·타입·카테고리·금액·메모·태그를 차례로 입력)", cmd_add, common)

    p = _add_command(sub, "list", "거래 목록 (최신순)", cmd_list, common)
    p.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help=f"보여 줄 개수 (기본: {DEFAULT_LIMIT})")

    p = _add_command(sub, "search", "조건으로 거래 검색 (최신순)", cmd_search, common)
    p.add_argument("--from", dest="date_from", metavar="YYYY-MM-DD", help="이 날짜부터")
    p.add_argument("--to", dest="date_to", metavar="YYYY-MM-DD", help="이 날짜까지")
    p.add_argument("--category", help="카테고리")
    p.add_argument("--type", choices=["income", "expense"], help="income 또는 expense")
    p.add_argument("--q", metavar="키워드", help="메모에 들어 있는 글자")
    p.add_argument("--tag", help="태그")
    p.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help=f"보여 줄 개수 (기본: {DEFAULT_LIMIT})")

    p = _add_command(sub, "update", "거래 수정 (바꿀 항목만 옵션으로)", cmd_update, common)
    p.add_argument("--id", required=True, help="수정할 거래 id (예: TX-000003)")
    p.add_argument("--date", metavar="YYYY-MM-DD")
    p.add_argument("--type", choices=["income", "expense"])
    p.add_argument("--category")
    p.add_argument("--amount", metavar="금액", help="양의 정수")
    p.add_argument("--memo")
    p.add_argument("--tags", metavar="태그,태그", help="쉼표로 구분 (빈 값이면 태그 지우기)")

    p = _add_command(sub, "delete", "거래 삭제", cmd_delete, common)
    p.add_argument("--id", required=True, help="삭제할 거래 id")

    p = _add_command(sub, "summary", "월별 요약 (수입·지출·잔액, 지출 TOP N, 예산 사용률)", cmd_summary, common)
    p.add_argument("--month", required=True, metavar="YYYY-MM")
    p.add_argument("--top", type=int, default=DEFAULT_TOP, help=f"카테고리별 지출 상위 N개 (기본: {DEFAULT_TOP})")

    budget = _add_command(sub, "budget", "월 예산 설정·조회", None, common)
    budget_sub = budget.add_subparsers(title="budget 명령", metavar="<set|show>", required=True)
    p = _add_command(budget_sub, "set", "월 예산 저장", cmd_budget_set, common)
    p.set_defaults(command_name="budget set")
    p.add_argument("--month", required=True, metavar="YYYY-MM")
    p.add_argument("--amount", required=True, metavar="금액", help="양의 정수")
    p = _add_command(budget_sub, "show", "월 예산 조회", cmd_budget_show, common)
    p.set_defaults(command_name="budget show")
    p.add_argument("--month", metavar="YYYY-MM", help="없으면 전체")

    category = _add_command(sub, "category", "카테고리 관리", None, common)
    category_sub = category.add_subparsers(title="category 명령", metavar="<add|list|remove>", required=True)
    p = _add_command(category_sub, "add", "카테고리 추가 (이름을 입력)", cmd_category_add, common)
    p.set_defaults(command_name="category add")
    p.add_argument("name", nargs="?", help="카테고리 이름 (없으면 물어봄)")
    p = _add_command(category_sub, "list", "카테고리 목록", cmd_category_list, common)
    p.set_defaults(command_name="category list")
    p = _add_command(category_sub, "remove", "카테고리 삭제 (사용 중이면 막음)", cmd_category_remove, common)
    p.set_defaults(command_name="category remove")
    p.add_argument("name", help="삭제할 카테고리")
    p.add_argument("--replace-with", metavar="카테고리", help="사용 중인 거래를 이 카테고리로 옮긴 뒤 삭제")

    p = _add_command(sub, "import", "CSV 파일에서 거래 가져오기", cmd_import, common)
    p.add_argument("--from", dest="source", required=True, metavar="CSV", help="가져올 CSV 파일")

    p = _add_command(sub, "export", "조건에 맞는 거래를 CSV로 내보내기 (--month 또는 --from/--to 필수)", cmd_export, common)
    p.add_argument("--out", required=True, metavar="CSV", help="만들 CSV 파일")
    p.add_argument("--month", metavar="YYYY-MM")
    p.add_argument("--from", dest="date_from", metavar="YYYY-MM-DD")
    p.add_argument("--to", dest="date_to", metavar="YYYY-MM-DD")
    p.add_argument("--force", action="store_true", help="이미 있는 파일을 덮어쓰기")

    _add_command(sub, "backup", "데이터 파일 백업 (data/backups/시각/)", _not_ready("a-8"), common)

    recurring = _add_command(sub, "recurring", "반복 내역 (월급·월세 등)", None, common)
    recurring_sub = recurring.add_subparsers(title="recurring 명령", metavar="<add|list|remove|apply>", required=True)
    p = _add_command(recurring_sub, "add", "반복 규칙 추가 (대화형)", _not_ready("a-8"), common)
    p.set_defaults(command_name="recurring add")
    p = _add_command(recurring_sub, "list", "반복 규칙 목록", _not_ready("a-8"), common)
    p.set_defaults(command_name="recurring list")
    p = _add_command(recurring_sub, "remove", "반복 규칙 삭제", _not_ready("a-8"), common)
    p.set_defaults(command_name="recurring remove")
    p.add_argument("--id", required=True, help="삭제할 규칙 id")
    p = _add_command(recurring_sub, "apply", "그 달의 반복 거래 만들기 (이미 만든 건 건너뜀)", _not_ready("a-8"), common)
    p.set_defaults(command_name="recurring apply")
    p.add_argument("--month", required=True, metavar="YYYY-MM")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args) if args.func else EXIT_OK
