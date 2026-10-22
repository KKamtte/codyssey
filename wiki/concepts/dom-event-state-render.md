---
title: DOM 선택, 이벤트, 상태 → 렌더링 흐름
updated: 2026-10-22
sources: []
---

[[b1-1]]에서 배운 것. 과제 목표 "querySelector·addEventListener 흐름"과 "이벤트 → 상태 변경 → DOM 업데이트 연결(React 상태-렌더링의 기초)".

## 기본 흐름
1. `document.querySelector('.theme-toggle')`로 요소를 한 번 찾아 상수에 둔다.
2. `addEventListener('click', handler)`로 동작을 붙인다. HTML의 `onclick`은 쓰지 않는다(구조와 동작 분리, 여러 개 붙이기 가능).
3. 스크립트는 `defer`로 부른다. 없으면 head에서 실행될 때 body가 아직 없어 `querySelector`가 `null` → `null.textContent`에서 TypeError가 나고 그 아래 코드가 전부 멈춘다.
   - 예외: `theme-init.js`는 화면을 그리기 **전에** 테마를 적용해야 깜빡이지 않으므로 일부러 defer 없이 head에서 실행한다.

## 상태 → 렌더링
- 화면을 직접 여기저기 고치지 않고, **상태 객체 하나**를 바꾼 뒤 **그 상태를 읽어 다시 그리는 함수**를 부른다.
  ```js
  setProjectsState({ activeLanguage: 'Java' });   // 바뀌는 것: 상태 값
  // → renderProjects()                           // 하는 일: 상태를 읽어 그리기
  ```
- 문답에서 헷갈린 점: "바뀌는 상태 값"(`activeLanguage`: `'All'` → `'Java'`)과 "그 값을 읽어 그리는 함수"(`renderProjects`)는 다른 것이다 ([[b1-1-review-qa]] Q4).
- 이 페이지의 흐름 예시
  - 필터: 클릭 → `activeLanguage` 변경 → 버튼 `aria-pressed`·카드 목록 다시 그림 (API 재호출 없음)
  - 다크 모드: 클릭 → `data-theme` + localStorage → CSS 변수가 바뀌어 전체 색 변경
  - 햄버거: 클릭 → `.active` + `aria-expanded` → CSS가 메뉴 표시
  - 폼: 제출 → 칸별 검사 결과 → 에러 문구·`aria-invalid` 표시
- React의 `useState` + 렌더링이 이 패턴을 자동으로 해 주는 것이다.

## 이벤트 위임
- 필터 버튼은 `renderFilters()`가 그릴 때마다 `innerHTML`로 지우고 새로 만든다. 버튼마다 리스너를 달면 다시 그릴 때 리스너도 같이 사라진다.
- 그래서 그대로 남는 부모 `.projects__filters`에 한 번만 달고, `event.target.closest('.filter-btn')`으로 눌린 버튼을 찾는다.

## innerHTML과 XSS
- 외부 데이터(GitHub 저장소 설명 등)를 `innerHTML`에 그대로 넣으면 `<img src=x onerror="...">` 같은 이벤트 속성이 실행된다. `<script>` 태그만 막는다고 안전하지 않다.
- `escapeHtml`로 `& < > " '`를 바꿔 넣는다. 따옴표도 바꾸므로 속성 값 밖으로 빠져나가는 것도 막는다.
