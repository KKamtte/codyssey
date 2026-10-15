# B1-1 나를 소개하는 웹페이지 처음부터 만들기

> 분야: 웹 기초와 프론트엔드 · 기간: 80시간(필수, 개인 미션) · 상태: 진행중
> 원문: https://usr.codyssey.kr/learning/learningMap?projectNo=136003 → B1-1 (로컬 `MISSION.md`)
> 작업 계획·결정 사항: [wiki/plans/b1-1.md](../../../wiki/plans/b1-1.md)

## 과제 요약

외부 라이브러리 없이 순수 HTML/CSS/JavaScript로 반응형 포트폴리오 사이트를 만들고 GitHub Pages로 배포한다.
화면을 예쁘게 만드는 것보다 **"사용자 이벤트 → 상태 변경 → 화면 업데이트"** 흐름을 이해하는 것이 목적이다.
GitHub API로 내 저장소 목록을 불러와 로딩/성공/에러/빈 상태를 처리한다. 다음 미션(React)의 기초가 된다.

## 요구사항

### 구성
- [x] 폴더 분리: `index.html`, `css/`, `js/`, `images/`
- [x] 외부 CSS(`css/style.css`), JS 연결 (JS는 `defer`)
- [ ] VS Code + Live Server 개발 환경

### HTML
- [x] 시맨틱 태그 사용: `header`, `nav`, `main`, `section`, `article`, `footer`
- [x] 섹션: Hero(인사, CTA) / About(소개, 프로필 사진) / Skills / Projects(GitHub 카드) / Contact(폼) / Footer(저작권, 소셜)
- [x] 네비게이션 앵커 링크로 각 섹션 이동
- [x] 모든 이미지에 의미 있는 `alt`
- [x] 폼 `label`과 입력의 `for`-`id` 연결

### CSS
- [x] `:root` CSS 변수(색상, 폰트, 간격) + 다크 모드 변수 `[data-theme="dark"]`
- [x] 네비게이션은 Flexbox(로고 왼쪽, 메뉴 오른쪽), Projects 카드는 Grid(`auto-fit` + `minmax`)
- [x] 모바일 퍼스트, 브레이크포인트 768px / 1024px
- [x] 모바일에서 메뉴 숨김 + 햄버거 버튼
- [x] 버튼·카드 hover + transition, 카드 box-shadow

### JavaScript 기본
- [x] `const`/`let`만 사용, `onclick` 대신 `addEventListener`
- [x] `querySelector(All)`, `textContent`/`innerHTML`, `classList.add/remove/toggle`
- [x] click, submit, scroll, input 이벤트 처리, `preventDefault()`

### 인터랙션
- [x] 햄버거 메뉴 토글 (`classList.toggle('active')`)
- [x] 부드러운 스크롤
- [x] 스크롤 탑 버튼 (기준 300px, 바꾸면 아래 "구현"에 기록)
- [x] 스크롤 시 네비게이션 배경 변경 (기준 60px, 바꾸면 기록)
- [x] 다크 모드 토글 + localStorage 저장(새로고침 후 유지)
- [x] 스크롤 애니메이션: Intersection Observer (threshold 0.2 이상 권장, 값 기록)
- [x] 문의 폼(이름/이메일/메시지): 필수값 검증, 이메일 형식 검증, 필드 옆 에러 메시지, 제출 시 성공 메시지

### ES6+
- [x] 화살표 함수, 템플릿 리터럴로 HTML 생성, 구조분해 할당
- [x] `map`(데이터 → 카드), `forEach`, `filter`(선택)

### API 연동
- [x] `fetch` + `async/await`로 `https://api.github.com/users/KKamtte/repos` 호출, `try/catch`
- [x] 로딩(스피너/"로딩 중...") / 성공(카드) / 에러("프로젝트를 불러올 수 없습니다" + 재시도 버튼) / 빈 상태("표시할 프로젝트가 없습니다")
- [x] 레이트 리밋(403)일 때도 에러 상태 표시

### 상태 → 렌더링 흐름 (3개 이상)
- [x] 다크 모드 토글 → 테마 상태 → 전체 스타일
- [x] API 호출 → 로딩/성공/에러 상태 → Projects 렌더링
- [x] 폼 입력 → 유효성 상태 → 에러 메시지 표시/숨김
- [x] (선택) 필터 버튼 → 필터 상태 → 목록 변경

### 배포 / 제출
- [ ] GitHub Pages 배포, 배포 URL에서 모든 기능 동작
- [ ] 이 README에 프로젝트 설명, 사용 기술, 배포 URL, 스크린샷(데스크톱/모바일/다크 모드)
- [ ] 제출: 저장소 URL, 배포 URL, 스크린샷

### 보너스 (선택)
- [x] 언어별 프로젝트 필터 (`filter`)
- [x] Hero 타이핑 효과
- [ ] 폼 실제 전송 (Formspree / EmailJS) — 하지 않음 (외부 가입 필요)
- [x] 시스템 다크 모드 감지 (`prefers-color-scheme`)

## 제약 / 평가 기준

- 금지: React, Vue, jQuery, Bootstrap, Tailwind 등 외부 라이브러리, 인라인 스타일(`style="..."`)
- 허용: Font Awesome 아이콘, Google Fonts
- 최신 Chrome에서 정상 동작
- GitHub API는 인증 없이 시간당 60회 제한, 반복 새로고침 주의
- 평가 때 설명할 수 있어야 하는 것:
  - 시맨틱 태그를 쓰는 이유와 내 구조 설계 기준
  - Flexbox와 Grid의 차이, 언제 무엇을 쓰는지
  - `querySelector` → `addEventListener` 흐름
  - 화살표 함수, 구조분해, `map`/`filter`를 쓰는 이유
  - `fetch` + `async/await`, 로딩/성공/실패 UI 처리
  - 이벤트 → 상태 변경 → DOM 업데이트 연결 (React 상태-렌더링의 기초)

## 구현

### 실행 방법

VS Code에서 이 폴더를 열고 Live Server로 `index.html`을 연다.
Live Server가 없으면 이 폴더에서 `python3 -m http.server 5500` 실행 후 http://127.0.0.1:5500 접속.

### 폴더 구조

```
B1-1-self-intro-page/
├── index.html        # 페이지 구조 (시맨틱 태그)
├── css/style.css     # 스타일
├── js/theme-init.js  # 저장된 테마를 화면 그리기 전에 적용 (defer 없이 head 에서)
├── js/main.js        # 동작 (defer 로 불러옴)
└── images/           # 이미지 (avatar.svg: 캐릭터 프로필 이미지)
```

### 주요 결정

- **시맨틱 구조**: `header > nav`, `main > section` 6개(Hero/About/Experience/Skills/Projects/Contact), `footer`.
  Experience는 필수 섹션 외에 추가했다. 백엔드 경력이 핵심이라 About에 섞기보다 따로 두는 편이 읽기 쉽다.
  섹션마다 `aria-labelledby`로 제목과 연결해 화면 낭독기에서도 구역 이름이 읽힌다.
- **`defer`로 JS 연결**: HTML을 다 읽은 뒤 실행되므로 `DOMContentLoaded`를 기다리지 않아도 `querySelector`로 요소를 찾을 수 있다.
- **폼 `novalidate`**: 브라우저 기본 검증 대신 JS로 검증하고, 에러 메시지를 각 필드 아래 `.form__error`에 표시한다 (a-6).
- **Projects 영역 분리**: 상태 메시지(`.projects__status`)와 카드 목록(`.projects__grid`)을 나눠 로딩/에러/빈 상태를 따로 렌더링한다 (a-5).

- **디자인 방향**: 흰 바탕과 넓은 여백(미니멀)에 성과 수치를 큰 숫자 카드로 보여준다(대시보드형).
  포인트 색은 딥그린 하나, 본문 폰트는 IBM Plex Sans KR, 수치·코드는 JetBrains Mono(Google Fonts).
- **CSS 변수(`:root`)**: 색·폰트·간격·그림자를 변수로 모았다. 다크 모드(a-4)는 변수 값만 바꾸면 된다.
- **모바일 퍼스트**: 기본 스타일을 좁은 화면 기준으로 쓰고 `min-width: 768px`, `min-width: 1024px`에서 덮어쓴다.
  모바일에서는 메뉴를 접고 햄버거를 보이며, 768px 이상에서 햄버거를 숨기고 메뉴를 가로로 편다.
- **Flexbox와 Grid 구분**: 한 줄로 늘어놓는 것(네비, 버튼 묶음, 기술 칩)은 Flexbox,
  카드 목록(성과 카드, 기술 분류, 프로젝트)은 Grid `repeat(auto-fill/auto-fit, minmax(...))`로 화면 폭에 따라 열 수가 바뀐다.
  성과 카드는 `auto-fill`로 두어 카드가 하나뿐일 때 한 줄을 다 차지하지 않게 했다.
- **Hero 높이**: 화면 전체(100vh)를 채우지 않고 내용 높이만 쓴다. 첫 화면에서 About이 바로 이어 보여 아래에 내용이 더 있다는 것이 드러난다.
  CTA 버튼(View Projects / Contact)은 과제 필수 요소라 유지한다.
- **고정 헤더와 앵커**: 헤더를 `position: fixed`로 두고 `scroll-padding-top`으로 앵커 이동 시 제목이 가려지지 않게 했다.
- **상태 클래스**: 메뉴 펼침(`.active`), 네비 배경(`.is-scrolled`), 맨 위로 버튼(`.is-visible`), 나타나기(`.reveal`)는
  CSS에 모양을 정의하고 JS는 `classList`로 클래스만 붙이고 뗀다. 모양과 동작을 나눠 두면 디자인을 바꿀 때 JS를 건드리지 않는다.
- **햄버거 메뉴**: `classList.toggle('active')`로 열고 닫고, `aria-expanded`도 같이 바꿔 화면 낭독기에 열림 상태를 알린다.
  메뉴 항목을 누르면 이동과 함께 메뉴를 닫는다.
- **부드러운 스크롤**: CSS `scroll-behavior` 대신 JS에서 `event.preventDefault()`로 앵커 점프를 막고 `scrollIntoView({ behavior: 'smooth' })`로 이동한다.
  주소창 해시는 `history.pushState`로 맞춘다. 운영체제의 "동작 줄이기"를 켠 사용자에게는 애니메이션 없이 바로 이동한다.
- **스크롤 애니메이션**: Intersection Observer로 섹션이 보이면 한 번만 나타나게 하고 관찰을 끊는다(`unobserve`).
  숨김 클래스(`.reveal`)를 JS가 붙이므로 JS가 실패해도 내용은 보인다.

- **다크 모드**: `<html data-theme="dark">`일 때 `[data-theme="dark"]` 규칙이 색 변수만 덮어쓴다. 컴포넌트 CSS는 변수만 쓰므로 고칠 필요가 없다.
  토글하면 `localStorage`의 `theme`에 `dark`/`light`를 저장한다. 저장소 접근이 막힌 환경에서도 오류 없이 전환만 되도록 `try...catch`로 감쌌다.
  다크 배경에서는 진한 초록이 잘 안 보여 포인트 색을 밝은 초록으로 바꾸고, 버튼 글자색(`--color-on-accent`)도 함께 바꾼다.
- **테마 깜빡임 방지**: `main.js`는 `defer`라 화면을 그린 뒤 실행된다. 저장된 테마를 여기서 적용하면 다크 모드 사용자에게 흰 화면이 잠깐 보이므로,
  저장값을 읽어 적용하는 작은 `theme-init.js`만 `<head>`에서 `defer` 없이 먼저 실행한다.
- **토글 버튼 접근성**: 아이콘(🌙/☀️)만 있는 버튼이라 `aria-label`로 "다크 모드로 전환" 등 동작을 알리고, `aria-pressed`로 켜짐 상태를 알린다.

- **Projects 상태 관리**: `projectsState`(`status`, `repos`, `errorMessage`)를 `setProjectsState()`로만 바꾸고, 바꿀 때마다 `renderProjects()`가 상태에 맞는 화면을 그린다.
  상태는 `loading`(스피너 + "로딩 중...") → `success`(카드) / `empty`("표시할 프로젝트가 없습니다") / `error`("프로젝트를 불러올 수 없습니다" + 다시 시도) 네 가지다.
- **API 호출**: `fetch` + `async/await`, `try...catch`로 실패를 잡는다. `response.ok`가 아니면 직접 `throw`해 같은 에러 처리로 보낸다.
  인증 없는 호출은 시간당 60회 제한이 있어 넘으면 403이 오므로 따로 안내 문구를 보여 준다. 네트워크가 끊기면 `fetch`가 `TypeError`로 실패하는 것을 구분했다.
- **보여줄 저장소**: 전체 공개 저장소 중 결과물로 볼 수 있는 3개(`library-search`, `spring-playground`, `nest_study`)만 `filter`로 고르고 최근 push 순으로 `sort`한다.
- **카드 생성**: 구조분해 할당으로 필요한 값만 꺼내 템플릿 리터럴로 카드 HTML을 만들고 `map` + `join`으로 붙인다.
  저장소 설명 같은 외부 데이터는 `innerHTML`에 넣기 전에 `escapeHtml()`로 `<`, `>` 등을 바꿔 HTML로 해석되지 않게 했다.

- **Contact 폼 검증**: 칸마다 검증 함수(`validators`)가 에러 메시지를 돌려주고(통과면 빈 문자열), 그 결과로 칸 아래 `.form__error`를 채우거나 비운다.
  - 제출(`submit`) 때 `event.preventDefault()`로 새로고침을 막고 모든 칸을 검사한다. `every`는 첫 실패에서 멈추므로 `map`으로 전부 검사해 에러를 한 번에 보여 주고, 첫 에러 칸으로 포커스를 옮긴다.
  - 한 번 에러가 난 칸은 입력(`input`)할 때마다 다시 검사해, 고치는 즉시 메시지가 사라진다. 처음부터 입력마다 검사하면 쓰기도 전에 에러가 떠서 이렇게 나눴다.
  - 공백만 넣은 값은 `trim()`으로 빈 값으로 본다. 이메일은 `이름@도메인.최상위` 모양인지 정규식으로 확인한다.
  - 에러 칸에는 `aria-invalid="true"`를 붙여 테두리를 빨갛게 하고, `aria-describedby`로 에러 문장과 연결해 화면 낭독기가 함께 읽게 했다.
  - 실제 전송 기능은 없어서, 성공 메시지에 데모 폼이라 전송되지 않는다는 점을 알리고 이메일 연락을 안내한다.

- **내용**: 이력서를 바탕으로 쓰되 공개 페이지라 연락처는 이메일과 GitHub만 둔다(전화번호 제외).
  경력은 회사별 기간·역할과 대표 성과 수치 몇 개만 넣어 과하지 않게 했다.
- **프로필 이미지**: 실제 사진 대신 증명사진을 참고해 SVG로 직접 그린 캐릭터를 쓴다. 실제 얼굴 사진은 공개 후 회수하기 어렵고,
  SVG는 코드라서 크기와 상관없이 선명하고 파일이 작다.

### 보너스

- **언어별 필터**: 불러온 저장소의 언어를 `new Set`으로 중복 없이 모아 버튼(All / Java / TypeScript)을 만든다.
  버튼 클릭 → `activeLanguage` 상태 변경 → `filter`로 고른 카드만 다시 그린다. 버튼마다 이벤트를 달지 않고 부모 하나에서 받는다(이벤트 위임).
  누른 버튼은 `aria-pressed="true"`로 표시하고 CSS가 그 속성으로 색을 바꾼다.
- **타이핑 효과**: Hero 소개 문장을 `setTimeout`으로 60ms마다 한 글자씩 늘려 보여 주고, 끝나면 깜빡이는 커서를 멈춘다.
  화면 낭독기가 글자 조각을 읽지 않도록 움직이는 글은 `aria-hidden`, 전체 문장은 화면에 안 보이는 `.sr-only`로 따로 둔다.
  JS가 안 돌아도 문장이 그대로 보이고, 동작 줄이기 설정이면 바로 전체를 보여 준다.
- **시스템 다크 모드 감지**: 토글로 직접 고른 적이 없으면 `prefers-color-scheme`(운영체제 설정)을 따른다. 우선순위는 직접 고른 값 > 운영체제 설정.
  운영체제 설정이 바뀌면(`change` 이벤트) 고른 적 없는 사용자에게만 바로 반영한다.
- **폼 실제 전송 (Formspree)은 하지 않았다**: 외부 서비스 가입이 필요해 이번에는 제외했다. 성공 메시지에 데모 폼이라 실제로 전송되지 않는다고 알린다.

### 기준값

| 항목 | 값 | 위치 |
|---|---|---|
| 맨 위로 버튼 표시 | 스크롤 300px 이상 | `js/main.js` `SCROLL_TOP_OFFSET` |
| 네비게이션 배경 변경 | 스크롤 60px 이상 | `js/main.js` `HEADER_SCROLL_OFFSET` |
| 타이핑 효과 글자 간격 | 60ms | `js/main.js` `TYPING_DELAY` |
| 스크롤 애니메이션 threshold | 0.2 (섹션 20%가 보이면) | `js/main.js` `REVEAL_THRESHOLD` |
| 브레이크포인트 | 768px, 1024px | `css/style.css` |

(배포 URL은 이후 단계에서 채운다)

## 회고

(막혔던 것, 배운 것)
