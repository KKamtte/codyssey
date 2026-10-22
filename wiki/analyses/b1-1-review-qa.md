---
title: B1-1 push 전 문답 기록
updated: 2026-10-22
sources: []
---

[[b1-1]] 미션을 `main`에 merge하기 전 문답. 방식은 [[review-quiz]].
결과: 6문항 중 3개 통과(Q1, Q5, Q6), 3개는 꼬리 질문까지 진행(Q2, Q3, Q4).

## Q1. 스크립트 로딩 (통과)
- 질문: `theme-init.js`는 defer 없이, `main.js`는 defer로 부르는 이유. `main.js`를 defer 없이 head에서 부르면?
- 내 답: theme-init은 화면 그리기 전에 실행해야 해서 파싱을 멈추고 바로 실행. main.js는 DOM이 다 만들어진 뒤 실행. defer 없이 head면 body가 없어 querySelector가 null.
- 보충: defer는 "실행할지"가 아니라 "언제 실행할지"를 정한다(병렬 다운로드 → 파싱 끝난 뒤 실행). `null.textContent`에서 TypeError가 나면 그 아래 코드가 전부 멈춘다.

## Q2. 768px 이상에서 네비가 바뀌는 이유 (부분)
- 내 답: 모바일 기본 스타일(`.nav__toggle{display:flex}`, `.nav__menu{display:none; flex-direction:column; flex-basis:100%; order:3}`)만 설명.
- 꼬리 Q2-1 답: 기본을 작은 화면 기준으로 쓰고 "이 폭 이상이면" 덮어쓰는 방향이 min-width. max-width면 데스크톱이 기본이고 모바일에서 덮어쓴다. (정답)
- 빠진 것: `@media (min-width: 768px)` 안에서 실제로 덮어쓰는 규칙.
  - `.nav__toggle { display: none; }` → 햄버거 숨김
  - `.nav__menu { display: flex; flex-direction: row; order: 0; flex-basis: auto; }` → 메뉴를 항상 보이게, 가로로, 원래 순서 자리(로고와 테마 버튼 사이)에, 한 줄 전체를 차지하지 않게
  - `.nav { flex-wrap: nowrap; }` → 한 줄 유지

## Q3. 403 응답 처리 (부분 → 꼬리에서 정답)
- 내 답: fetch는 HTTP 에러로는 reject되지 않고 네트워크 실패만 reject. (정답) 이어서 "확인이 없을 때" 벌어질 일을 설명.
- 꼬리 Q3-1 답: `throw new Error('GitHub API 요청 한도를…')` → `catch (error)`로 이동 → `instanceof TypeError`는 false → `setProjectsState({status:'error', errorMessage})` → `renderProjects()`가 에러 문구와 "다시 시도" 버튼을 그린다. (정답)

## Q4. 언어 필터 동작 (부분)
- 내 답: 클릭 감지 → 상태 변경 → 다시 그리기, API는 다시 부르지 않음. (흐름은 정답)
- 꼬리 Q4-1 답: 이벤트 위임 이유 — `renderFilters()`가 렌더링할 때마다 `innerHTML`로 버튼을 지우고 새로 그린다. (정답)
- 빠진 것:
  - 바뀌는 값: `projectsState.activeLanguage`가 `'All'` → `'Java'` (`button.dataset.language`). `renderProjects()`는 바뀐 값을 읽어 그리는 함수지, 바뀌는 값이 아니다.
  - 위임의 결론까지: 버튼마다 리스너를 달면 다시 그릴 때 버튼과 함께 리스너도 사라진다. 부모 `.projects__filters`는 그대로 남으므로 한 번만 달면 되고, `event.target.closest('.filter-btn')`으로 어느 버튼인지 찾는다.

## Q5. 폼 검증 map + every, preventDefault (통과)
- 내 답: validateField는 에러 문구·aria-invalid를 다는 부수 효과가 있어 map으로 모든 칸을 검사해야 한 번에 보인다. every만 쓰면 첫 false에서 멈춘다. preventDefault가 없으면 기본 GET 제출, novalidate라 막을 장치도 없다.
- 보충: 현재 주소에 `?name=…&email=…&message=…`가 붙어 새로고침되고, 입력값이 주소창에 드러난다.

## Q6. escapeHtml이 없으면 (통과)
- 내 답: XSS로 스크립트가 실행될 수 있고, 속성이 섞여 화면도 깨진다.
- 보충: `innerHTML`로 넣은 `<script>`는 실행되지 않지만 `<img src=x onerror="…">` 같은 이벤트 속성은 실행된다. "script 태그만 막으면 된다"는 틀린 생각.

## 다시 볼 것
- 미디어 쿼리 안에서 "무엇을 덮어쓰는지"를 규칙 단위로 말하기.
- 상태 기반 렌더링에서 "바뀌는 상태 값"과 "그 값을 읽어 그리는 함수"를 구분해서 말하기.
