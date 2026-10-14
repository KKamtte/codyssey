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

(구현하면서 채운다: 실행 방법, 폴더 구조, 기준값(스크롤 300/60px, threshold), 주요 결정과 이유, 배포 URL)

## 회고

(막혔던 것, 배운 것)
