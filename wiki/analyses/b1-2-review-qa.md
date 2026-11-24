---
title: B1-2 push 전 문답 기록
updated: 2026-11-24
sources: []
---

[[b1-2]] 미션을 `main`에 merge하기 전 문답. 방식은 [[review-quiz]]. Q1~Q5는 미션 "과제 목표" 5개, Q6~Q8은 보호 라우트·배포·권한.
결과: 8문항 중 6개 통과(Q1, Q2, Q5, Q6, Q7, Q8, 꼬리 질문 포함), 2개 부분(Q3, Q4).

## Q1. 컴포넌트 분리 기준: `CardForm` 공유 (통과)
- 질문: 등록·수정 페이지가 `CardForm` 하나를 같이 쓰는 이유, 두 페이지의 차이를 어떻게 넘기나.
- 내 답: 공통 영역이 있어서. 차이는 상속으로 처리하나? (수정 기능이 있는지 몰랐음)
- 꼬리 Q1-1 답: `submitLabel`·`onSubmit`·`initialValues`는 props. 버튼 글자, 저장 함수, 초기값이 다르다. (정답)
- 보충: React는 상속 대신 props로 조립한다. `initialValues`가 없으면 기본값 `EMPTY_CARD`(빈 칸, B1-2, 모름). 수정은 내 카드 상세의 "수정" 버튼 → `/cards/:id/edit`.

## Q2. props와 state, 상태 위치: `filters` (통과)
- 내 답: `filters`는 `CardListPage`에선 state, `CardFilters`에선 props. 목록도 필터 값을 알아야 해서 부모에 둠. (정답, 상태 끌어올리기)
- 꼬리 Q2-1 답: `onChange`로 부모의 `setFilters`를 호출. 데이터는 아래로, 이벤트는 위로. (정답)

## Q3. useEffect 실행 시점: `useCard` (부분)
- 내 답: `id`나 `reloadCount`가 바뀔 때 실행. `id`를 빼면 다른 카드로 가도 안 바뀜.
- 빠진 것: **처음 마운트될 때도** 한 번 실행된다. `/cards/1` → `/cards/2`는 같은 `CardDetailPage`를 재사용(재마운트 없음)하므로 `id`가 의존성에 있어야 한다.
- 꼬리 Q3-1 답: `ignore`가 없으면 늦게 온 1번 응답이 2번 카드를 덮어씀, `ignore`로 무시. (정답)
- 보충: effect 실행마다 자기 `ignore`가 생기고(클로저), 다시 실행되기 직전 정리 함수가 **이전 실행의** `ignore`만 `true`로 바꾼다.

## Q4. 로딩·성공·실패·빈 상태 (부분)
- 내 답: `/cards/999`는 `notFound`, 와이파이 끊김은 `error`. `error`는 결과를 모르니 재시도로 받아옴. (정답. `notFound`는 서버가 "없다"고 확정해 다시 해도 같음 → "목록으로")
- 빈 상태: ① "아직 카드가 없습니다"는 `cards` 0장. (정답)
- 꼬리 Q4-1: 카드 8장, 필터 B1-2 → `cards` 8 / `visibleCards` 0, ② 화면. (정답) 필요한 버튼은 "첫 카드 만들기"라고 답함. (틀림)
- 보충: 카드는 있고 **조건 때문에** 안 보이는 것이라 "필터 초기화"가 맞다. 빈 상태는 "왜 비었는지"로 나눈다: 데이터가 없으면 만들기, 조건 때문이면 조건 풀기.

## Q5. 기능 하나의 흐름: "답 보기" (통과)
- 내 답: `/cards/:id` → `CardDetailPage`, `useState`로 토글.
- 꼬리 Q5-1 답: `setShowAnswer` 후 리렌더링, 버튼 글자와 답 영역이 바뀜, B1-1에선 DOM을 직접 수정. (정답)
- 한 줄: 라우트가 페이지를 고르고, `showAnswer` state가 기억하고, 클릭 이벤트가 state를 바꾸면, React가 다시 렌더링한다. state만 바꾸면 React가 DOM을 맞춘다.

## Q6. 보호 라우트의 loading 확인 (통과)
- 내 답: 새로고침 직후 `user`는 `null`, loading 확인을 지우면 로그인 화면으로 튕김. (정답)
- 보충: "모름(loading)"과 "없음(null)"을 구분. `state.from`으로 로그인 후 원래 주소로 돌아감.

## Q7. 배포: `vercel.json` rewrite (통과)
- 내 답: 없으면 새로고침 시 404, 서버에 `cards/3` 파일이 없어서. 클릭 이동은 서버에 요청하지 않고 React Router가 주소를 바꾸고 화면을 그림. (정답)

## Q8. 권한: 버튼 숨기기와 RLS (통과)
- 내 답: API로 직접 요청하면 버튼 숨기기로는 못 막아서 RLS가 필요, 버튼 숨기기는 UX용. (정답)
- 보충: anon key는 번들에 그대로 들어가 누구나 볼 수 있으므로, 실제 보호는 DB의 RLS(`user_id = auth.uid()`)가 맡는다.

## 다시 볼 것
- useEffect 실행 시점은 "처음 마운트 + 의존성이 바뀔 때"로 빠짐없이 말하기.
- 빈 상태는 "왜 비었는지"(데이터 없음 vs 조건 때문)로 나누고 그에 맞는 다음 행동을 안내한다.
