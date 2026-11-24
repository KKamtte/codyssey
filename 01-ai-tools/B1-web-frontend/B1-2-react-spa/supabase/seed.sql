-- 시드 카드: B1-1 push 전 문답(wiki/analyses/b1-1-review-qa.md)과 B1-2에서 설명해야 할 질문
-- schema.sql 다음에 SQL Editor 에서 한 번 실행한다.
-- SQL Editor 는 관리자 권한이라 RLS 를 거치지 않고, auth.uid() 가 없으므로 user_id 는 비어 있다(작성자 없음 → 앱에서는 아무도 수정·삭제 못 함).
-- 마크다운 본문은 따옴표 처리가 필요 없도록 $md$ ... $md$ 로 감쌌다.

insert into public.cards (question, answer, topic, level) values
(
  'theme-init.js 는 defer 없이, main.js 는 defer 로 불러오는 이유는?',
  $md$- `theme-init.js`: 화면을 그리기 **전에** 테마를 붙여야 흰 화면 깜빡임(FOUC)이 없다. defer 없이 `<head>`에서 바로 실행.
- `main.js`: DOM 이 다 만들어진 **뒤** 실행해야 `querySelector` 가 요소를 찾는다.
- defer 를 빼면 `<body>` 가 아직 없어 `null.textContent` 에서 TypeError → 그 아래 코드가 전부 멈춘다.

defer 는 "실행할지"가 아니라 "**언제** 실행할지"를 정한다.$md$,
  'B1-1', 'known'
),
(
  '768px 이상에서 햄버거가 사라지고 메뉴가 가로로 펼쳐지는 CSS 구조는?',
  $md$모바일 기본 스타일 위에 `@media (min-width: 768px)` 가 같은 선택자로 덮어쓴다 (우선순위가 같으면 뒤에 쓴 규칙이 이김).

- `.nav__toggle { display: none; }` → 햄버거 숨김
- `.nav__menu { display: flex; flex-direction: row; order: 0; flex-basis: auto; }` → 항상 보이게, 가로로, 로고와 같은 줄에
- `.nav { flex-wrap: nowrap; }` → 한 줄 유지

min-width 를 쓰는 이유: 작은 화면이 기본이고 "이 폭 이상이면" 덮어쓰는 방향이라서.$md$,
  'B1-1', 'unsure'
),
(
  'try/catch 가 있는데 response.ok 를 따로 확인하는 이유는? 403 이면 어떤 순서로 실행되나?',
  $md$`fetch` 는 HTTP 에러(403, 404, 500)로는 reject 되지 않고 **네트워크 실패만** reject 된다. 그래서 상태 코드를 직접 보고 throw 한다.

403 순서: `throw new Error('요청 한도…')` → `catch` 로 이동 → `instanceof TypeError` 는 false → `setProjectsState({ status: 'error' })` → `renderProjects()` 가 에러 문구와 "다시 시도" 버튼을 그린다.$md$,
  'B1-1', 'unsure'
),
(
  '"Java" 필터를 누르면 어떤 상태가 바뀌고, 이벤트를 부모에 한 번만 다는 이유는?',
  $md$- 바뀌는 값: `projectsState.activeLanguage` 가 `'All'` → `'Java'`. `renderProjects()` 는 그 값을 **읽어 그리는 함수**지 바뀌는 값이 아니다.
- 이벤트 위임: `renderFilters()` 가 그릴 때마다 `innerHTML` 로 버튼을 새로 만든다. 버튼마다 리스너를 달면 버튼과 함께 사라진다. 부모는 그대로라 한 번만 달고 `event.target.closest('.filter-btn')` 으로 버튼을 찾는다.$md$,
  'B1-1', 'unsure'
),
(
  '제출할 때 every 만 쓰지 않고 map(validateField) 로 먼저 모든 칸을 검사한 이유는? preventDefault 가 없으면?',
  $md$- `validateField` 는 에러 문구와 `aria-invalid` 를 다는 **부수 효과**가 있다. `every` 는 첫 false 에서 멈춰 나머지 칸 에러가 안 보인다. `map` 으로 모두 검사한 뒤 `every(Boolean)` 으로 판단.
- `preventDefault` 가 없으면 기본 GET 제출 → 새로고침되고 주소에 `?name=…&email=…` 가 붙는다. `novalidate` 라 막을 장치도 없다.$md$,
  'B1-1', 'known'
),
(
  '저장소 설명을 innerHTML 에 넣기 전에 escapeHtml() 을 거치지 않으면?',
  $md$XSS. 설명에 `<img src=x onerror="…">` 가 있으면 스크립트가 이 페이지 권한으로 실행된다.

`innerHTML` 로 넣은 `<script>` 는 실행되지 않지만 이벤트 속성은 실행되므로 "script 태그만 막으면 된다"는 틀린 생각. 근본 대안은 `textContent` 나 요소를 직접 만드는 방식.$md$,
  'B1-1', 'known'
),
(
  'props 와 state 의 차이는? 이 앱에서 상태를 어디에 두었나?',
  $md$(B1-2 진행하면서 채운다)$md$,
  'B1-2', 'unknown'
),
(
  'useEffect 는 언제 실행되고, 의존성 배열은 데이터 요청과 어떤 관계인가?',
  $md$(B1-2 진행하면서 채운다)$md$,
  'B1-2', 'unknown'
);
