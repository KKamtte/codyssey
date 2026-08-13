"""Mini NPU MAC Simulator

MAC(Multiply-Accumulate) 연산으로 N×N 패턴이 Cross인지 X인지 판별하는 콘솔 프로그램.
외부 라이브러리 없이 표준 라이브러리(json, time)만 사용한다.
"""

import json
import time
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

def main() -> None:
    print('=== Mini NPU Simulator ===')


if __name__ == '__main__':
    main()
