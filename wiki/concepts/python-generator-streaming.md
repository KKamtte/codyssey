---
title: 제너레이터(yield) 스트리밍과 heapq.nlargest
updated: 2026-11-25
sources: []
---

[[b2-1]]에서 배운 것. 과제 목표 "`yield` 기반 제너레이터로 대용량 파일도 스트리밍 처리하는 이유와 동작 방식". 문답은 [[b2-1-review-qa]] Q2.

## yield 가 하는 일
```python
def stream(self):
    with open(self.path, encoding="utf-8") as file:
        for line in file:
            yield json.loads(line)   # 한 건 넘기고 여기서 멈춤. 다음 값을 달라고 하면 이어서 실행
```
- `return [...]`(리스트)는 파일 전체를 메모리에 올린 뒤 돌려준다. 100만 건이면 100만 건이 메모리에.
- `yield`는 값을 **하나 넘기고 멈춘다.** `for`·`next()`·`max()`·`heapq` 같은 쪽이 다음 값을 요구할 때만 한 줄 더 읽는다. 메모리에는 지금 처리 중인 한 건만 있다.
- 제너레이터는 **한 번 훑으면 끝**이다. 다시 읽으려면 `stream()`을 다시 불러 파일을 처음부터 연다.
- 제너레이터끼리 이어 붙일 수 있다: `(tx for tx in stream() if criteria.matches(tx))`도 제너레이터라, 거르는 동안에도 전부 모으지 않는다.

## "최신순"과 스트리밍을 함께: heapq.nlargest
```python
heapq.nlargest(3, stream(), key=lambda tx: tx.sort_key)   # sort_key = (날짜, id 번호)
```
- 최신순은 원래 전체 정렬이 필요하다. `nlargest(N, …)`는 **크기 N 인 최소 힙**만 유지한다.
- 힙의 루트 = 지금까지 고른 N개 중 가장 오래된 것. 새 거래는 루트와만 비교해, 더 최신이면 루트를 빼고 넣고 아니면 버린다.
- 그래서 몇 건을 훑든 메모리에는 N건만 남는다. 전체 건수도 세고 싶으면 넘기는 제너레이터 안에서 세면 된다(`counted()`).

## 모으지 않고 합계만: summary
- 월별 요약은 거래를 리스트로 모으지 않고 훑으면서 수입·지출 합계와 카테고리별 합계 dict 만 더한다. 메모리에는 카테고리 수만큼의 숫자만.

## 일부러 모으는 경우
- `export`는 날짜순으로 써야 해서 **내보내는 기간의 거래만** 모아 정렬한다. "전부 모으지 않는다"가 원칙이고, 모아야 할 때는 범위를 줄인다.

## 관련
- 같은 원칙(한 번 훑으며 새 파일에 쓰기)으로 수정·삭제를 안전하게 하는 법: [[atomic-file-write]]
