# B1-2 버튼 누르면 화면이 스르륵 바뀌는 요즘 웹사이트 만들기

> 분야: 웹 기초와 프론트엔드 · 기간: 80시간(선택, 개인 미션) · 상태: 진행중
> 원문: https://usr.codyssey.kr/learning/learningMap?projectNo=136003 → B1-2 (원문 사본: 비공개 `codyssey-mission/B1-2-react-spa.md`)
> 작업 계획·결정 사항: [wiki/plans/b1-2.md](../../../wiki/plans/b1-2.md)

## 만드는 것: 문답 카드

동료 평가를 대비해 "설명할 수 있어야 하는 질문"과 내 답을 카드로 모아 복습하는 SPA.
핵심 데이터는 **문답 카드** 한 종류(질문, 답(마크다운), 분야(과제 코드), 숙련도 모름/애매/앎)이고, Supabase에 저장해 CRUD한다.
누구나 카드를 볼 수 있고, 로그인하면 카드를 등록하고 내가 쓴 카드만 고치거나 지울 수 있다.

## 과제 요약

React로 라우팅이 있는 SPA 하나를 만들고, 핵심 데이터 한 종류를 Supabase 또는 Firebase에 두고 등록/조회/수정/삭제(CRUD)한다.
화면 품질보다 **"사용자 이벤트 → 상태 변화 → 렌더링 변화"** 흐름과 컴포넌트·상태 설계가 평가의 중심이다.
로딩/에러/빈 상태를 재사용 컴포넌트로 통일하고, 외부에서 접속 가능한 URL(Vercel/Netlify 등)로 배포한다.

## 요구사항

### 프로젝트 구성
- [ ] React 18 이상 프로젝트
- [ ] 폴더 역할 분리: `pages`(라우트 화면) / `components`(재사용 UI) / `hooks` 또는 `lib`(커스텀 훅·유틸)
- [ ] 공통 레이아웃(헤더/네비게이션)을 주요 페이지에 적용
- [ ] 서비스 주제는 직접 정하되 핵심 데이터 한 종류의 CRUD 수준

### 라우팅
- [ ] 라우트 5개 이상 (목록 `/items`, 상세 `/items/:id` 포함)
- [ ] 잘못된 주소는 Not Found 페이지
- [ ] 네비게이션 링크로 주요 라우트 이동

### 컴포넌트
- [ ] 재사용 컴포넌트 8개 이상 (prop에 따라 동작·표시가 달라지는 것)
- [ ] 페이지 컴포넌트와 UI 컴포넌트 분리
- [ ] 로딩/에러/빈 상태 UI를 공통 컴포넌트로 통일

### 상태 관리
- [ ] 폼 입력은 controlled input
- [ ] 목록/상세 데이터 상태, 로딩/에러 상태를 React state로 관리
- [ ] 조회/갱신 흐름 중 1개 이상을 커스텀 훅으로 분리 (예: `useItems()`, `useItemDetail(id)`)

### CRUD (Supabase 또는 Firebase 원격 데이터)
- [ ] 목록 조회 → 리스트 렌더링
- [ ] 상세 조회 → 라우트 파라미터로 불러와 렌더링
- [ ] 등록/수정 → 폼 제출 → 성공 시 이동·갱신
- [ ] 삭제 → 목록 갱신 또는 이동

### 폼 UX
- [ ] 필수값 검증 (비어 있으면 제출 불가)
- [ ] 에러 메시지를 필드 근처 또는 상단에 표시
- [ ] 제출 중 버튼 비활성화 또는 스피너
- [ ] 요청 실패(네트워크/권한 등)를 화면에 표시

### 이벤트와 렌더링
- [ ] 상태 변경 → 렌더링 변화 지점 3곳 이상 (예: 필터 → 목록, 입력 → 미리보기, 저장 성공 → 알림)

### 배포
- [ ] 외부 접속 URL(Vercel/Netlify 등)에서 목록/상세/등록/수정/삭제 모두 동작
- [ ] 배포 환경변수 누락 없음
- [ ] 이 README에 실행 방법과 기술 스택 명시

### 보너스 (선택)
- [ ] 전역 상태(Context 등): 로그인 사용자 / 테마 / 알림 중 하나
- [ ] 메모이제이션(`useMemo`/`useCallback`/`React.memo`) 1개 이상
- [ ] Supabase/Firebase Auth 로그인 + 보호 라우트

## 제약 / 평가 기준

- React 기반. 백엔드는 Supabase 또는 Firebase, 서버를 직접 만들지 않는다. RLS/Rules 같은 고급 기능은 필수 아님.
- TypeScript, 스타일링 방식(CSS·Tailwind·CSS-in-JS·UI 라이브러리), 반응형은 자유.
- API Key는 `.env`에 두고 `.gitignore`로 제외. 키가 들어간 코드를 push하지 않는다. 배포 플랫폼 대시보드에 환경변수를 따로 등록한다.
- 제출: 배포 URL + GitHub 레포 URL.
- 평가 때 설명할 것: 컴포넌트를 나눈 기준, props와 state 차이와 상태 위치, `useEffect` 실행 시점과 의존성, 비동기 상태를 UI로 표현한 방법, 라우팅 → 컴포넌트 → 상태 → 이벤트 → 렌더링 연결.

## 구현

### 실행 방법

```bash
cd 01-ai-tools/B1-web-frontend/B1-2-react-spa
npm install
cp .env.example .env.local   # Supabase URL/Key 채우기
npm run dev                  # http://localhost:5173
npm run build                # dist/ 에 빌드
```

### 기술 스택

| 영역 | 선택 | 이유 |
|---|---|---|
| UI | React 19 (JavaScript) | 과제 기준 React 18 이상. TypeScript는 가산점이 없어 설명할 범위를 React에 집중 |
| 빌드 | Vite 8 | 개발 서버가 빠르고 설정이 `vite.config.js` 한 파일 |
| 라우팅 | React Router 7 | `BrowserRouter`로 URL과 화면을 연결 |
| 백엔드 | Supabase (DB + Auth) | 테이블 하나로 CRUD, SQL로 구조가 보임, 로그인 연결이 쉬움 |
| 스타일 | CSS Modules + CSS 변수 | 컴포넌트마다 스타일 파일을 둬 컴포넌트 단위로 관리, 클래스 이름 충돌 없음, Vite 기본 지원 |
| 마크다운 | react-markdown | 답 미리보기·상세 표시. HTML 문자열을 직접 넣지 않아 XSS 걱정이 없음 |
| 배포 | Vercel | GitHub 연결, 대시보드에서 환경변수 등록 |

### 구조

```
index.html          # <div id="root"> 하나뿐인 SPA 진입 HTML
vite.config.js
src/
  main.jsx          # React 시작점: <BrowserRouter>로 감싸 <App> 렌더링
  App.jsx           # 라우트 정의 (a-2)
  pages/            # 라우트 단위 화면
  components/       # 재사용 UI 컴포넌트
  hooks/            # 커스텀 훅 (데이터 조회·갱신)
  lib/              # Supabase 클라이언트, 유틸
```

### 주요 결정
- `create-vite` 템플릿 대신 같은 구성을 직접 만들었다 (도구 버전 문제). 그래서 파일마다 역할을 설명할 수 있다.
- API 키는 `.env.local`에만 둔다. `.gitignore`가 `.env*`를 막고 예시 파일 `.env.example`만 커밋한다.
- 루트 `.gitignore`(Python 템플릿)가 `lib/`를 무시해서, 이 폴더 `.gitignore`에 `!src/lib/`로 예외를 뒀다.

## 회고

(완료 후 작성)
