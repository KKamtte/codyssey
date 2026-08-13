"""Mini NPU MAC Simulator

MAC(Multiply-Accumulate) 연산으로 N×N 패턴이 Cross인지 X인지 판별하는 콘솔 프로그램.
외부 라이브러리 없이 표준 라이브러리(json, time)만 사용한다.
"""

import json
import time
from typing import List, Optional, Tuple

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
# [5] 입력 검증 및 행렬 입력
# ---------------------------------------------------------------


# ---------------------------------------------------------------
# [6] 모드 실행
# ---------------------------------------------------------------


# ---------------------------------------------------------------
# [7] 출력 및 진입점
# ---------------------------------------------------------------

def main() -> None:
    print('=== Mini NPU Simulator ===')


if __name__ == '__main__':
    main()
