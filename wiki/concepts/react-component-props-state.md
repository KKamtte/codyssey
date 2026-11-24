---
title: React 컴포넌트, props와 state, 상태 → 렌더링
updated: 2026-11-24
sources: []
---

[[b1-2]]에서 배운 것. 과제 목표 "컴포넌트를 왜·어떤 기준으로 쪼갰나", "props와 state의 차이와 상태 위치", "라우팅 → 컴포넌트 → 상태 → 이벤트 → 렌더링". B1-1의 순수 JS 버전은 [[dom-event-state-render]]. 문답은 [[b1-2-review-qa]] Q1·Q2·Q5.

## 컴포넌트를 나눈 기준
- **같은 생김새·동작이 두 곳 이상에서 쓰이면** 하나로 뺀다. 등록·수정 페이지가 `CardForm` 하나를 같이 쓴다.
- **다른 부분만 props로 넘긴다.** 상속이 아니라 조립(composition)이다.
  ```jsx
  <CardForm submitLabel="등록" onSubmit={handleCreate} />                       // initialValues 없음 → 기본값 EMPTY_CARD
  <CardForm initialValues={{ question, answer, topic, level }} submitLabel="저장" onSubmit={handleUpdate} />
  ```
- 폴더로도 나눴다: `components/ui/`(어느 화면에나 쓰는 Button·Input·Loading 등), `components/cards/`(카드 전용), `pages/`(라우트 하나 = 페이지 하나).

## props와 state
| | props | state |
|---|---|---|
| 누가 정하나 | 부모가 넘겨줌 | 컴포넌트가 직접 가짐(`useState`) |
| 바꿀 수 있나 | 받은 쪽은 못 바꿈 | `set...`으로 바꿈 → 다시 렌더링 |

- 같은 값이 어떤 컴포넌트에겐 state, 그 자식에겐 props다. `filters`는 `CardListPage`의 state이고 `CardFilters`의 props.

## 상태를 어디에 두나: 끌어올리기
- 그 값을 **알아야 하는 컴포넌트들의 공통 부모**에 둔다. 필터 입력은 `CardFilters`에 있지만, 걸러진 목록(`CardList`)과 "전체 n장 중 m장"도 필터 값을 알아야 하므로 `CardListPage`가 가진다.
- **데이터는 아래로, 이벤트는 위로.** 부모가 `filters`를 props로 내려주고, 자식은 `onChange={setFilters}`로 받은 함수를 불러 "바꿔 달라"고 올려 보낸다.

## 기능 하나의 흐름: "답 보기" 버튼
1. **라우팅**: `/cards/:id` → `CardDetailPage`
2. **컴포넌트**: 질문, 배지, 답 영역, "답 보기" 버튼을 그린다
3. **상태**: `const [showAnswer, setShowAnswer] = useState(false)`
4. **이벤트**: 클릭 → `setShowAnswer((shown) => !shown)`
5. **렌더링**: React가 다시 렌더링 → 버튼 글자(`답 보기`↔`답 가리기`)와 답 영역(안내 문구↔마크다운 답)이 바뀐다

B1-1은 상태를 바꾼 뒤 `textContent`·`classList`로 **DOM을 직접** 고쳤다. React는 **state만 바꾸면 React가 DOM을 맞춘다.**

## 메모이제이션 (보너스)
- `useMemo`: `cards`나 `filters`가 바뀔 때만 필터 결과를 다시 계산한다. 다른 이유로 다시 그려질 때는 이전 결과를 쓴다.
- `React.memo`(목록 항목), `useCallback`(`reload` 함수)도 같은 목적: 바뀌지 않은 것은 다시 만들거나 그리지 않는다.
