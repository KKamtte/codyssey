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
- [ ] 폴더 분리: `index.html`, `css/`, `js/`, `images/`
- [ ] 외부 CSS(`css/style.css`), JS 연결 (JS는 `defer`)
- [ ] VS Code + Live Server 개발 환경

### HTML
- [ ] 시맨틱 태그 사용: `header`, `nav`, `main`, `section`, `article`, `footer`
- [ ] 섹션: Hero(인사, CTA) / About(소개, 프로필 사진) / Skills / Projects(GitHub 카드) / Contact(폼) / Footer(저작권, 소셜)
- [ ] 네비게이션 앵커 링크로 각 섹션 이동
- [ ] 모든 이미지에 의미 있는 `alt`
- [ ] 폼 `label`과 입력의 `for`-`id` 연결

### CSS
- [ ] `:root` CSS 변수(색상, 폰트, 간격) + 다크 모드 변수 `[data-theme="dark"]`
- [ ] 네비게이션은 Flexbox(로고 왼쪽, 메뉴 오른쪽), Projects 카드는 Grid(`auto-fit` + `minmax`)
- [ ] 모바일 퍼스트, 브레이크포인트 768px / 1024px
- [ ] 모바일에서 메뉴 숨김 + 햄버거 버튼
- [ ] 버튼·카드 hover + transition, 카드 box-shadow

### JavaScript 기본
- [ ] `const`/`let`만 사용, `onclick` 대신 `addEventListener`
- [ ] `querySelector(All)`, `textContent`/`innerHTML`, `classList.add/remove/toggle`
- [ ] click, submit, scroll, input 이벤트 처리, `preventDefault()`

### 인터랙션
- [ ] 햄버거 메뉴 토글 (`classList.toggle('active')`)
- [ ] 부드러운 스크롤
- [ ] 스크롤 탑 버튼 (기준 300px, 바꾸면 아래 "구현"에 기록)
- [ ] 스크롤 시 네비게이션 배경 변경 (기준 60px, 바꾸면 기록)
- [ ] 다크 모드 토글 + localStorage 저장(새로고침 후 유지)
- [ ] 스크롤 애니메이션: Intersection Observer (threshold 0.2 이상 권장, 값 기록)
- [ ] 문의 폼(이름/이메일/메시지): 필수값 검증, 이메일 형식 검증, 필드 옆 에러 메시지, 제출 시 성공 메시지

### ES6+
- [ ] 화살표 함수, 템플릿 리터럴로 HTML 생성, 구조분해 할당
- [ ] `map`(데이터 → 카드), `forEach`, `filter`(선택)

### API 연동
- [ ] `fetch` + `async/await`로 `https://api.github.com/users/KKamtte/repos` 호출, `try/catch`
- [ ] 로딩(스피너/"로딩 중...") / 성공(카드) / 에러("프로젝트를 불러올 수 없습니다" + 재시도 버튼) / 빈 상태("표시할 프로젝트가 없습니다")
- [ ] 레이트 리밋(403)일 때도 에러 상태 표시

### 상태 → 렌더링 흐름 (3개 이상)
- [ ] 다크 모드 토글 → 테마 상태 → 전체 스타일
- [ ] API 호출 → 로딩/성공/에러 상태 → Projects 렌더링
- [ ] 폼 입력 → 유효성 상태 → 에러 메시지 표시/숨김
- [ ] (선택) 필터 버튼 → 필터 상태 → 목록 변경

### 배포 / 제출
- [ ] GitHub Pages 배포, 배포 URL에서 모든 기능 동작
- [ ] 이 README에 프로젝트 설명, 사용 기술, 배포 URL, 스크린샷(데스크톱/모바일/다크 모드)
- [ ] 제출: 저장소 URL, 배포 URL, 스크린샷

### 보너스 (선택)
- [ ] 언어별 프로젝트 필터 (`filter`)
- [ ] Hero 타이핑 효과
- [ ] 폼 실제 전송 (Formspree / EmailJS)
- [ ] 시스템 다크 모드 감지 (`prefers-color-scheme`)

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
└── images/           # 이미지 (profile.svg: 기본 프로필 이미지)
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

### 기준값

| 항목 | 값 | 위치 |
|---|---|---|
| 맨 위로 버튼 표시 | 스크롤 300px 이상 | `js/main.js` `SCROLL_TOP_OFFSET` |
| 네비게이션 배경 변경 | 스크롤 60px 이상 | `js/main.js` `HEADER_SCROLL_OFFSET` |
| 스크롤 애니메이션 threshold | 0.2 (섹션 20%가 보이면) | `js/main.js` `REVEAL_THRESHOLD` |
| 브레이크포인트 | 768px, 1024px | `css/style.css` |

(배포 URL은 이후 단계에서 채운다)

## 회고

(막혔던 것, 배운 것)
