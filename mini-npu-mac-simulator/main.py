"""Mini NPU MAC Simulator

MAC(Multiply-Accumulate) 연산으로 N×N 패턴이 Cross인지 X인지 판별하는 콘솔 프로그램.
외부 라이브러리 없이 표준 라이브러리(json, time)만 사용한다.
"""

import json
import math
import time
import unicodedata
from typing import Any, Dict, List, Optional, Tuple

Matrix = List[List[float]]


# ---------------------------------------------------------------
# [1] 상수
# ---------------------------------------------------------------

# 두 점수의 차이가 이 값보다 작으면 동점으로 본다 (부동소수점 오차 흡수)
EPSILON = 1e-9

# 프로그램 내부에서 사용하는 표준 라벨. 입력단에서 정규화한 뒤에는 이 값만 쓴다.
LABEL_CROSS = 'Cross'
LABEL_X = 'X'
LABEL_UNDECIDED = 'UNDECIDED'

# 모드 1은 사용자가 넣은 필터 두 개를 비교하므로 Cross/X가 아니라 A/B로 부른다.
LABEL_A = 'A'
LABEL_B = 'B'

# 모드 1이 다루는 행렬 크기 (과제 지정: 3×3 고정)
MODE1_SIZE = 3

# 메뉴 선택지
MENU_INPUT = '1'
MENU_JSON = '2'
MENU_QUIT = 'q'

# 성능 측정 반복 횟수 (과제 최소 기준: 10회 반복 후 평균)
REPEAT = 10

# 분석 대상 데이터 파일 (프로젝트 루트 기준)
DATA_FILE = 'data.json'

# 성능 분석에서 측정할 패턴 크기
PERF_SIZES = [3, 5, 13, 25]


# ---------------------------------------------------------------
# [2] 라벨 정규화
# ---------------------------------------------------------------

# 원본 표기 → 표준 라벨 대응표.
# 같은 'Cross'라도 expected는 '+'로, 필터 키는 'cross'로 적혀 있어 표를 따로 둔다.
EXPECTED_LABELS = {'+': LABEL_CROSS, 'x': LABEL_X}
FILTER_KEY_LABELS = {'cross': LABEL_CROSS, 'x': LABEL_X}


def _lookup_label(raw: Any, table: Dict[str, str]) -> Optional[str]:
    """대응표에서 표준 라벨을 찾는다. 문자열이 아니거나 표에 없으면 None을 반환"""
    if not isinstance(raw, str):
        return None
    return table.get(raw.strip().lower())


def normalize_expected(raw: Any) -> Optional[str]:
    """data.json의 expected 값을 표준 라벨로 변환 ('+' → Cross, 'x' → X)"""
    return _lookup_label(raw, EXPECTED_LABELS)


def normalize_filter_key(raw: Any) -> Optional[str]:
    """data.json의 필터 키를 표준 라벨로 변환 ('cross' → Cross, 'x' → X)"""
    return _lookup_label(raw, FILTER_KEY_LABELS)


# ---------------------------------------------------------------
# [3] MAC 연산
# ---------------------------------------------------------------

def mac(pattern: Matrix, filter_matrix: Matrix) -> float:
    """패턴과 필터의 MAC(Multiply-Accumulate) 점수를 반환"""
    total = 0.0
    n = len(pattern)
    for row in range(n):
        for col in range(n):
            product = pattern[row][col] * filter_matrix[row][col]  # Multiply
            total = total + product  # Accumulate
    return total


def measure_mac_ms(pattern: Matrix, filter_matrix: Matrix, repeat: int = REPEAT) -> float:
    """MAC 연산을 repeat회 반복한 뒤 1회당 평균 소요 시간을 ms 단위로 반환

    측정 구간에는 mac() 호출만 들어간다. 출력·입력·파일 읽기는 물론 행렬 생성도
    포함하지 않는다. 인자로 받은 행렬은 호출 전에 이미 준비되어 있어야 한다.
    반복 루프를 함수 안에 둔 것도 호출부가 측정 구간에 다른 일을 섞지 못하게 하기 위함이다.
    """
    start = time.perf_counter()
    for _ in range(repeat):
        mac(pattern, filter_matrix)
    elapsed = time.perf_counter() - start
    return (elapsed / repeat) * 1000.0


# ---------------------------------------------------------------
# [4] 점수 비교 및 판정
# ---------------------------------------------------------------

def is_tie(score_a: float, score_b: float) -> bool:
    """두 점수를 동점으로 볼지 판단하여, 차이가 EPSILON보다 작으면 같은 값으로 판단"""
    return abs(score_a - score_b) < EPSILON


def compare_scores(score_first: float, score_second: float,
                   label_first: str, label_second: str) -> str:
    """점수가 높은 쪽의 라벨을 반환한다. 동점이면 LABEL_UNDECIDED"""
    if is_tie(score_first, score_second):
        return LABEL_UNDECIDED
    if score_first > score_second:
        return label_first
    return label_second


def decide(score_cross: float, score_x: float) -> str:
    """모드 2용 판정. 두 점수를 비교해 표준 라벨(Cross/X/UNDECIDED)로 반환"""
    return compare_scores(score_cross, score_x, LABEL_CROSS, LABEL_X)


def is_correct(predicted: str, expected: Optional[str]) -> bool:
    """판정한 라벨이 기대 라벨과 일치하면 True(PASS), 아니면 False(FAIL)를 반환"""
    if predicted == LABEL_UNDECIDED:  # 판정 자체를 못 했으므로 정답일 수 없음
        return False
    if expected is None:  # 기대 라벨 정규화에 실패한 경우 비교 대상이 없음
        return False
    return predicted == expected


# ---------------------------------------------------------------
# [5] 패턴 생성기
# ---------------------------------------------------------------

def _empty_matrix(n: int) -> Matrix:
    """모든 값이 0.0인 n×n 행렬을 반환"""
    matrix = []
    for _ in range(n):
        # 행마다 새 리스트를 만든다. [[0.0] * n] * n 으로 쓰면 같은 행 객체를 n번
        # 참조하게 되어, 한 칸만 바꿔도 모든 행이 함께 바뀐다.
        matrix.append([0.0] * n)
    return matrix


def generate_cross(n: int) -> Matrix:
    """n×n 십자가(Cross) 패턴을 생성한다. 가운데 행과 가운데 열이 1.0"""
    matrix = _empty_matrix(n)
    center = n // 2
    for i in range(n):
        matrix[center][i] = 1.0  # 가운데 행
        matrix[i][center] = 1.0  # 가운데 열
    return matrix


def generate_x(n: int) -> Matrix:
    """n×n X 패턴을 생성한다. 두 대각선이 1.0"""
    matrix = _empty_matrix(n)
    for i in range(n):
        matrix[i][i] = 1.0  # 왼쪽 위 → 오른쪽 아래 대각선
        matrix[i][n - 1 - i] = 1.0  # 오른쪽 위 → 왼쪽 아래 대각선
    return matrix


# ---------------------------------------------------------------
# [6] 입력 검증 및 행렬 입력
# ---------------------------------------------------------------

def parse_row(line: str, n: int) -> Tuple[Optional[List[float]], str]:
    """줄단위 검증. 한 줄을 숫자 n개로 변환한다. 실패하면 (None, 사유)를 반환"""
    tokens = line.split()
    if len(tokens) != n:
        return None, '입력 형식 오류: 각 줄에 %d개의 숫자를 공백으로 구분해 입력하세요.' % n

    values = []
    for token in tokens:
        try:
            value = float(token)
        except ValueError:
            return None, "입력 형식 오류: '%s'은(는) 숫자가 아닙니다." % token
        # float()은 'nan'과 'inf'도 받아준다. 이 값들이 들어오면 점수 비교가
        # 조용히 무너지므로(nan은 어떤 비교에도 False) 여기서 막는다.
        if not math.isfinite(value):
            return None, "입력 형식 오류: '%s'은(는) 사용할 수 없는 값입니다." % token
        values.append(value)
    return values, ''


def validate_matrix(matrix: Any, n: int) -> Tuple[bool, str]:
    """행렬 검증. n×n 숫자 행렬인지 검사한다. 아니면 (False, 사유)를 반환"""
    if not isinstance(matrix, list):
        return False, '2차원 배열이 아닙니다.'
    if len(matrix) != n:
        return False, '행 수가 %d이어야 하는데 %d입니다.' % (n, len(matrix))

    for index, row in enumerate(matrix):
        position = index + 1
        if not isinstance(row, list):
            return False, '%d번째 행이 배열이 아닙니다.' % position
        if len(row) != n:
            return False, '%d번째 행의 열 수가 %d이어야 하는데 %d입니다.' % (position, n, len(row))
        for value in row:
            # bool은 int의 하위 타입이라 isinstance(True, int)가 참이다.
            # True/False가 1.0/0.0으로 조용히 계산되는 것을 막으려고 따로 걸러낸다.
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return False, '%d번째 행에 숫자가 아닌 값이 있습니다.' % position
            if not math.isfinite(value):
                return False, '%d번째 행에 사용할 수 없는 값(nan/inf)이 있습니다.' % position
    return True, ''


def _prompt(message: str) -> str:
    """input() 래퍼. Ctrl+C / Ctrl+D를 안내 문구와 함께 정상 종료"""
    try:
        return input(message)
    except (KeyboardInterrupt, EOFError):
        print('\n입력이 중단되었습니다. 프로그램을 종료합니다.')
        raise SystemExit(0)


def read_matrix(title: str, n: int) -> Matrix:
    """n×n 행렬을 한 줄씩 입력받는다. 올바른 줄만 쌓이므로 틀린 줄만 다시 묻는다"""
    print(title)
    matrix: Matrix = []
    while len(matrix) < n:
        line = _prompt('')
        values, reason = parse_row(line, n)
        if values is None:
            print('  ' + reason)
            continue  # 실패한 줄은 쌓지 않으므로 같은 번호를 다시 묻게 된다
        matrix.append(values)
    return matrix


# ---------------------------------------------------------------
# [7] 모드 실행
# ---------------------------------------------------------------

def run_mode_input() -> None:
    """모드 1. 3×3 필터 두 개와 패턴을 입력받아 MAC 점수로 판정한다"""
    size = MODE1_SIZE

    print_section(1, '필터 입력')
    filter_a = read_matrix('필터 A (%d줄 입력, 공백 구분)' % size, size)
    filter_b = read_matrix('필터 B (%d줄 입력, 공백 구분)' % size, size)

    print_section(2, '패턴 입력')
    pattern = read_matrix('패턴 (%d줄 입력, 공백 구분)' % size, size)

    # 입력이 모두 끝난 뒤에 계산한다. 측정 구간에 입력 대기 시간이 섞이면 안 된다.
    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)
    verdict = compare_scores(score_a, score_b, LABEL_A, LABEL_B)
    average_ms = measure_mac_ms(pattern, filter_a)

    print_section(3, 'MAC 결과')
    print('A 점수: %s' % score_a)
    print('B 점수: %s' % score_b)
    print('연산 시간(평균/%d회): %.3f ms' % (REPEAT, average_ms))
    if verdict == LABEL_UNDECIDED:
        print('판정: 판정 불가 (|A-B| < %g)' % EPSILON)
    else:
        print('판정: %s' % verdict)

    print_section(4, '성능 분석 (평균/%d회)' % REPEAT)
    print_perf_table([(size, average_ms)])


def run_mode_json() -> None:
    """모드 2. data.json 일괄 분석 (7~9단계에서 구현)"""
    print('data.json 분석 기능은 아직 구현 중입니다.')


# ---------------------------------------------------------------
# [8] 출력 및 진입점
# ---------------------------------------------------------------

# 성능 표 컬럼 제목과 각 칸의 너비(터미널 출력 기준)
PERF_HEADERS = ('크기(N×N)', '평균 시간(ms)', '연산 횟수(N²)')
PERF_WIDTHS = (14, 16, 14)


def _display_width(text: str) -> int:
    """터미널에서 차지하는 칸 수를 센다"""
    width = 0
    for char in text:
        if unicodedata.east_asian_width(char) in ('W', 'F'):
            width += 2
        else:
            width += 1
    return width


def _pad(text: str, width: int, align_right: bool = False) -> str:
    """표시 너비 기준으로 문자열을 width 칸에 맞춰 채운다"""
    padding = ' ' * max(0, width - _display_width(text))
    if align_right:
        return padding + text
    return text + padding


def print_perf_table(rows: List[Tuple[int, float]]) -> None:
    """크기별 평균 시간 표를 출력한다. rows는 (N, 평균 시간 ms) 목록"""
    header = ''
    for title, width in zip(PERF_HEADERS, PERF_WIDTHS):
        header += _pad(title, width)
    print(header)
    print('-' * _display_width(header))

    for n, avg_ms in rows:
        line = _pad('%d×%d' % (n, n), PERF_WIDTHS[0])
        line += _pad('%.3f' % avg_ms, PERF_WIDTHS[1] - 2, align_right=True) + '  '
        line += _pad('%d' % (n * n), PERF_WIDTHS[2] - 2, align_right=True)
        print(line)


def print_section(number: int, title: str) -> None:
    """구획 머리말을 출력한다"""
    line = '#' + '-' * 40
    print('\n' + line)
    print('# [%d] %s' % (number, title))
    print(line)


def print_menu() -> None:
    print('\n[모드 선택]')
    print('%s. 사용자 입력 (%dx%d)' % (MENU_INPUT, MODE1_SIZE, MODE1_SIZE))
    print('%s. %s 분석' % (MENU_JSON, DATA_FILE))
    print('%s. 종료' % MENU_QUIT)


def main() -> None:
    print('=== Mini NPU Simulator ===')
    while True:
        print_menu()
        choice = _prompt('선택: ').strip().lower()
        if choice == MENU_INPUT:
            run_mode_input()
        elif choice == MENU_JSON:
            run_mode_json()
        elif choice == MENU_QUIT:
            print('프로그램을 종료합니다.')
            return
        else:
            # 잘못 골랐다고 프로그램을 끝내지 않는다. 안내만 하고 다시 묻는다.
            print("'%s'은(는) 없는 선택지입니다. %s, %s, %s 중에서 고르세요."
                  % (choice, MENU_INPUT, MENU_JSON, MENU_QUIT))


if __name__ == '__main__':
    main()
