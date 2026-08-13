"""Mini NPU MAC Simulator

MAC(Multiply-Accumulate) 연산으로 N×N 패턴이 Cross인지 X인지 판별하는 콘솔 프로그램.
외부 라이브러리 없이 표준 라이브러리(json, time)만 사용한다.
"""

import json
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


def decide(score_cross: float, score_x: float) -> str:
    """두 점수를 비교해 표준 라벨로 판정"""
    if is_tie(score_cross, score_x):
        return LABEL_UNDECIDED
    if score_cross > score_x:
        return LABEL_CROSS
    return LABEL_X


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


# ---------------------------------------------------------------
# [7] 모드 실행
# ---------------------------------------------------------------


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


def main() -> None:
    print('=== Mini NPU Simulator ===')


if __name__ == '__main__':
    main()
