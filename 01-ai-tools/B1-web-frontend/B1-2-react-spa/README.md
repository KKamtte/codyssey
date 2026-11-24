# B1-2 버튼 누르면 화면이 스르륵 바뀌는 요즘 웹사이트 만들기

> 분야: 웹 기초와 프론트엔드 · 기간: 80시간(선택, 개인 미션) · 상태: 완료
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
cp .env.example .env.local   # Supabase Project URL 과 publishable 키 채우기
npm run dev                  # http://localhost:5173
npm run build                # dist/ 에 빌드
```

Supabase 준비(처음 한 번): 대시보드 SQL Editor 에서 `supabase/schema.sql`(테이블·권한) → `supabase/seed.sql`(예시 카드 8장) 순서로 실행한다.

### 데이터 (`cards` 테이블)

| 컬럼 | 내용 |
|---|---|
| `id` | 자동 증가 번호. 상세 주소 `/cards/:id` |
| `question`, `answer` | 질문과 내 답(마크다운). 빈 값이면 DB가 거부 |
| `topic` | 분야(과제 코드 `B1-1`, `B1-2` …) |
| `level` | 숙련도 `unknown`(모름) / `unsure`(애매) / `known`(앎) |
| `user_id` | 작성자. 로그인 사용자가 등록하면 DB가 `auth.uid()`로 채움 |
| `created_at`, `updated_at` | 생성·수정 시각. 수정 시각은 트리거가 갱신 |

권한은 RLS 정책으로 DB가 직접 검사한다: 조회는 누구나, 등록은 로그인 사용자, 수정·삭제는 작성자 본인만.

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
supabase/
  schema.sql        # 테이블·트리거·권한(RLS) — SQL Editor 에서 실행
  seed.sql          # 예시 카드 8장
src/
  main.jsx          # React 시작점: <BrowserRouter>로 감싸 <App> 렌더링, 전역 CSS 불러오기
  App.jsx           # 라우트 정의: 주소 → 페이지 연결표
  pages/            # 라우트 단위 화면 (Home, CardList, CardDetail, CardNew, CardEdit, Login, NotFound)
  contexts/
    AuthContext.jsx # 로그인 사용자 전역 상태 (AuthProvider)
    ToastContext.jsx # 저장·삭제 알림 전역 상태 (ToastProvider, 알림 목록도 여기서 그림)
  components/       # 재사용 컴포넌트 (Layout: 헤더·네비 + <Outlet />, ProtectedRoute: 로그인 필요 라우트)
    ui/             # 데이터와 상관없는 범용 UI (아래 표)
    cards/          # 카드 데이터를 그리는 컴포넌트 (CardList, CardListItem, CardFilters, LevelBadge, CardForm, DeleteCardButton)
  hooks/            # 커스텀 훅: useCards(목록), useCard(id)(상세), useAuth(로그인 사용자), useToast(알림 띄우기)
  lib/
    supabase.js     # Supabase 클라이언트 하나
    cardsApi.js     # Supabase 요청 모음 (fetchCards, fetchCard, createCard, updateCard, deleteCard)
    authApi.js      # 로그인·가입·로그아웃 요청, 에러를 한국어로
    cardOptions.js  # 숙련도 값 ↔ 이름·색, 분야(과제 코드) 목록
    filterCards.js  # 필터 조건으로 카드 고르기 (순수 함수)
    format.js       # 날짜 표시
  styles/global.css # CSS 변수(색·간격)와 기본 초기화. 컴포넌트 스타일은 각 *.module.css
```

### 재사용 UI 컴포넌트 (`src/components/ui/`)

모두 prop에 따라 모양이나 동작이 달라진다. 스타일은 컴포넌트마다 `*.module.css`.

| 컴포넌트 | 주요 prop | 달라지는 것 |
|---|---|---|
| Button | `variant`, `to`, `loading` | 색(주요/보조/삭제), `to`가 있으면 이동 링크, `loading`이면 스피너 + 비활성(제출 중) |
| Spinner | `size` | 버튼 안(작게) / 화면 가운데(크게) |
| Field | `label`, `error` | 라벨·에러 메시지 틀. Input·TextArea·Select가 함께 씀 |
| Input / TextArea / Select | `label`, `error`, `value`, `onChange`, `options` | controlled 입력. `error`가 있으면 빨간 테두리 + 메시지 + `aria-invalid` |
| Card | `to` | 상자. `to`가 있으면 상자 전체가 링크 |
| Badge | `tone` | 꼬리표 색(분야 / 숙련도 모름·애매·앎) |
| Loading | `message` | 로딩 상태 (`role="status"`) |
| ErrorState | `message`, `onRetry` | 에러 상태 (`role="alert"`). `onRetry`가 있으면 "다시 시도" 버튼 |
| EmptyState | `message`, `children` | 빈 상태. `children`으로 다음 행동 버튼을 넣음 |
| PageHeader | `title`, `children` | 페이지 제목 줄. 오른쪽에 버튼을 넣음 |
| MarkdownView | `children` | 마크다운 글을 그림 (react-markdown, HTML 문자열을 넣지 않아 XSS 없음) |
| ToastList | `toasts`, `onDismiss` | 알림을 화면 아래에 쌓아 그림. `tone`에 따라 초록(성공)/빨강(실패) |

### 데이터 흐름 (조회)

```
페이지 ──부름──▶ 커스텀 훅(useCards / useCard) ──useEffect──▶ cardsApi ──▶ Supabase
   ▲                    │
   └── { status, cards(card), error, reload } ◀── 응답에 따라 state 변경
```

- 훅은 `status`를 `loading` → `success` / `error`(상세는 `notFound`도)로 바꾸고, 페이지는 `status`에 맞춰 `Loading` / `ErrorState` / `EmptyState` / 내용 중 하나를 그린다.
- `useEffect` 의존성: `useCards`는 `[reloadCount]`(처음 한 번 + "다시 시도" 때), `useCard`는 `[id, reloadCount]`(주소의 id가 바뀌면 다시 요청).
- 정리 함수(`ignore = true`)로, 응답이 오기 전에 화면을 떠나거나 다시 요청하면 늦게 온 옛 응답을 버린다.
- 목록 필터는 서버에 다시 묻지 않는다. 받아 온 `cards`는 그대로 두고, 필터 state가 바뀔 때마다 `filterCards()`로 보여줄 카드만 다시 계산한다.

### 상태 → 렌더링 지점

| # | 사용자 이벤트 | 바뀌는 상태 (위치) | 바뀌는 화면 |
|---|---|---|---|
| 1 | 분야·숙련도 선택, 검색어 입력 | `filters` (CardListPage) | 목록이 조건에 맞는 카드만, "전체 N장 중 M장" |
| 2 | 답 입력 | `values.answer` (CardForm) | 옆 미리보기가 같은 내용을 마크다운으로 |
| 3 | "답 보기 / 답 가리기" | `showAnswer` (CardDetailPage) | 답이 나타나거나 가려짐, 버튼 문구 |
| 4 | "삭제" → "삭제 / 취소" | `step` (DeleteCardButton) | 확인 문구와 버튼 둘 → 지우는 중 스피너 |
| 5 | 로그인 / 로그아웃 | `user` (AuthContext) | 헤더(이메일·로그아웃 ↔ 로그인), 내 카드의 수정·삭제 버튼, 보호 라우트 |
| 6 | 등록·수정·삭제·로그인·로그아웃 성공 | `toasts` (ToastContext) | 화면 아래 알림이 3초 동안 떴다 사라짐 |
| 7 | 폼 제출 | `submitting`, `errors`, `formError` (CardForm·LoginPage) | 칸별 에러, 버튼 스피너·비활성, 실패 메시지 |

### 메모이제이션 (보너스)

| 위치 | 방법 | 하는 일 |
|---|---|---|
| CardListPage | `useMemo` | `cards`·`filters`가 바뀔 때만 분야 목록과 보여줄 카드를 다시 계산 |
| CardListItem | `React.memo` | 받은 `card`가 같은 객체면 다시 그리지 않음 |
| MarkdownView | `React.memo` | 글이 같으면 다시 그리지 않음 (폼에서 질문을 칠 때 답 미리보기를 다시 해석하지 않음) |
| ToastContext | `useCallback`, `useMemo` | `showToast`와 Context 값을 같은 것으로 유지해, 알림이 뜨고 사라져도 `showToast`만 쓰는 페이지가 다시 그려지지 않음 |

확인: 목록에서 숙련도 필터를 "전체 → 애매"로 바꾸면 남은 카드 3장의 다시 그리기가 0번이었다. "애매 → 전체"로 바꾸면 새로 나타난 5장만 그려졌다(개발 모드 StrictMode가 두 번씩 그려 10번).

### 라우트

| 주소 | 페이지 | 비고 |
|---|---|---|
| `/` | HomePage | 서비스 소개, 숙련도별 카드 수 (`useCards` 재사용) |
| `/cards` | CardListPage | 목록, 분야·숙련도·검색 필터 |
| `/cards/:id` | CardDetailPage | 상세, `useParams()`로 `id`를 읽음. 답 가리기/보기 |
| `/cards/new` | CardNewPage | 등록 (로그인 필요) |
| `/cards/:id/edit` | CardEditPage | 수정 (로그인 필요) |
| `/login` | LoginPage | 로그인·회원가입. 로그인되면 원래 가려던 주소(없으면 목록)로 이동 |
| `*` | NotFoundPage | 어느 주소에도 맞지 않을 때 |

### 배포 (Vercel)

배포 URL: https://b1-2-qa-cards.vercel.app

| 항목 | 값 |
|---|---|
| 플랜 · 프로젝트 | Vercel Hobby(무료) · `b1-2-qa-cards` |
| 연결 레포 | GitHub `KKamtte/codyssey` (`main`에 push하면 자동 배포) |
| Root Directory | `01-ai-tools/B1-web-frontend/B1-2-react-spa` (레포 하나에 과제가 여러 개라 이 폴더만 빌드) |
| Framework Preset | Vite (빌드 `npm run build`, 결과 폴더 `dist`) |
| 환경변수 | `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY` (Production · Preview) |

- **`vercel.json` rewrite**: 모든 주소(`/(.*)`)를 `/index.html`로 보낸다. 앱 안에서 링크로 `/cards/3`에 가는 건 React Router가 주소만 바꾸는 것이라 괜찮지만, 그 주소에서 **새로고침**하면 브라우저가 서버에 `/cards/3` 파일을 직접 요청한다. 서버에는 `index.html` 하나뿐이라 404가 난다. rewrite로 어떤 주소든 `index.html`을 돌려주면, React가 뜬 뒤 `BrowserRouter`가 주소를 읽어 맞는 페이지를 그린다.
- **환경변수를 대시보드에 등록하는 이유**: `.env.local`은 `.gitignore`로 레포에 올라가지 않아 Vercel이 볼 수 없다. Vite는 `VITE_`로 시작하는 값을 **빌드할 때** 코드에 박아 넣으므로, 빌드하는 Vercel 쪽에 값이 있어야 한다.
- 이 키는 브라우저로 내려가는 공개용 키다. 숨길 수 있는 값이 아니고, 데이터 보호는 DB의 RLS 정책이 맡는다.

### 주요 결정
- `create-vite` 템플릿 대신 같은 구성을 직접 만들었다 (도구 버전 문제). 그래서 파일마다 역할을 설명할 수 있다.
- API 키는 `.env.local`에만 둔다. `.gitignore`가 `.env*`를 막고 예시 파일 `.env.example`만 커밋한다.
- 브라우저에는 공개용 **publishable 키**만 둔다. 서버 전용 secret 키는 RLS를 무시하므로 쓰지 않는다. 대신 "누가 무엇을 할 수 있나"는 DB의 RLS 정책이 막는다(공개 키로는 조회만 되고 등록은 거부, 수정·삭제는 0줄).
- 테이블 구조와 정책을 SQL 파일로 레포에 남겼다. 대시보드에서 클릭으로 만들면 어떻게 만들었는지 남지 않는다.
- 루트 `.gitignore`(Python 템플릿)가 `lib/`를 무시해서, 이 폴더 `.gitignore`에 `!src/lib/`로 예외를 뒀다.
- 모든 라우트를 `<Route element={<Layout />}>` 아래에 중첩했다. 헤더는 한 번만 만들고, 주소가 바뀌면 `<Outlet />` 자리의 페이지만 바뀐다.
- 로딩/에러/빈 상태는 `Loading`·`ErrorState`·`EmptyState` 세 컴포넌트로만 그린다. 페이지마다 따로 만들지 않아 모든 화면에서 모양이 같다.
- 입력 칸 세 종류(Input/TextArea/Select)는 라벨·에러 표시를 `Field` 하나에 맡겼다. 에러 모양을 바꿀 때 한 곳만 고치면 된다.
- 입력 컴포넌트는 값을 스스로 들고 있지 않고 `value`/`onChange`를 부모에게서 받는다(controlled). 폼 상태는 페이지(부모)가 쥐고 검증한다.
- 로그인 사용자는 `AuthContext`(전역 상태)에 둔다. 헤더·보호 라우트·상세 페이지가 모두 필요로 하는데, props로 내려 주면 중간 컴포넌트가 쓰지도 않는 값을 계속 전달해야 한다(props drilling).
- `AuthProvider`는 처음에 저장된 세션을 읽고(`getSession`), 이후 로그인·로그아웃을 `onAuthStateChange`로 구독한다. 로그인 페이지는 성공 후 직접 이동하지 않는다. `user`가 생기면 다시 그려지면서 `<Navigate>`가 이동시킨다.
- 보호 라우트는 세션 확인(`status: 'loading'`)이 끝나기 전에는 판단하지 않는다. 그러지 않으면 로그인한 사람도 새로고침할 때마다 로그인 화면으로 튕긴다.
- 화면에서 버튼을 숨기는 것(내 카드만 "수정")은 편의일 뿐이고, 실제 권한은 DB의 RLS가 막는다.
- 등록과 수정은 같은 `CardForm`을 쓴다. 폼은 입력값·검증 에러·제출 중 상태를 갖고, "어디에 저장할지"는 부모 페이지가 `onSubmit`으로 넘긴다(등록: `createCard`, 수정: `updateCard`). 저장 함수가 throw하면 폼이 실패 메시지를 보여준다.
- 답 입력칸 옆 미리보기는 따로 상태를 두지 않는다. 입력할 때마다 `values.answer`가 바뀌어 다시 렌더링되고, 미리보기는 같은 값을 그린다(상태 → 렌더링 지점).
- 수정·삭제는 RLS 때문에 남의 카드면 에러 없이 0줄이 바뀐다. 그래서 돌려받은 줄이 없으면 실패로 바꿔 알린다.
- 삭제 확인은 브라우저 `confirm()` 창 대신 상태(`idle` → `confirming` → `deleting`)로 버튼 모양을 바꿔 묻는다. 화면 흐름이 React 상태로 보이고, 창이 페이지를 멈추지 않는다.
- 삭제 후에는 `navigate('/cards', { replace: true })`로 목록에 간다. "뒤로 가기"로 지운 카드 주소에 돌아오지 않고, 목록이 새로 나타나며 `useCards`가 다시 불러와 지운 카드가 빠진다.
- 서버에서 온 데이터(`cards`)는 훅이, 화면 조건(필터, 답 보기 여부)은 그 화면을 쓰는 페이지가 state로 가진다. 필터 입력 칸(CardFilters)은 값을 들고 있지 않고 props로 받는다(상태 끌어올리기).
- Supabase 요청은 `lib/cardsApi.js`에만 둔다. supabase-js는 실패해도 throw하지 않고 `{ error }`를 돌려주므로, 여기서 throw로 바꿔 훅이 `.catch` 한 가지 방식으로 실패를 다루게 했다.
- `/cards/abc`처럼 숫자가 아닌 id는 요청하지 않고 바로 "찾을 수 없음"으로 보여준다(DB에 보내면 형식 에러가 난다).
- 네비게이션은 `<a>` 대신 `NavLink`를 쓴다. 페이지를 새로 불러오지 않고 주소만 바꾸며, 현재 주소의 메뉴에 `active` 클래스와 `aria-current="page"`를 붙여 준다. `/`와 `/cards`는 `end`를 줘서 하위 주소(`/cards/new`)에서 함께 켜지지 않게 했다.

## 회고

### 막혔던 것
- **주제를 한 번 바꿈**: 처음엔 레포 `wiki/`를 보여 주고 고치는 앱을 만들려 했다. 그런데 앱은 Supabase에 사본을 두니 레포와 앱이 서로 반영되지 않아 원천이 둘이 되고, 레포에 쓰려면 GitHub 쓰기 토큰이 브라우저에 노출된다. "데이터의 원천이 어디인가"를 먼저 정해야 한다는 걸 배우고, 앱이 원천이 되는 문답 카드로 바꿨다.
- **프로젝트 생성 도구 실패**: `create-vite` 템플릿이 받아지지 않아 같은 구성을 직접 만들었다. 덕분에 파일마다 역할을 설명할 수 있게 됐다.
- **Vercel 배포**:
  - Import 목록에 내 레포가 안 보였다. Vercel GitHub 앱이 다른 조직에만 설치돼 있었다 → 개인 계정에 이 레포 하나만 허용해 설치.
  - 첫 Import는 `main`만 읽는데 `main`에 아직 과제 폴더가 없었다 → 프로젝트를 먼저 만들고 설정에서 Root Directory를 지정, 미션 브랜치는 Preview 배포로 확인한 뒤 `main` merge로 공개 URL을 받았다.
  - 환경변수는 빌드할 때 코드에 들어가므로, Vercel에 값을 넣은 **다음에** 빌드해야 앱이 동작한다.

### 배운 것
- B1-1에서는 상태를 바꾼 뒤 DOM을 직접 고쳤다. React에서는 state만 바꾸면 React가 다시 렌더링해 DOM을 맞춘다. "어디서 화면이 바뀌나"가 state 하나로 모인다.
- 상태는 그 값을 **알아야 하는 컴포넌트들의 공통 부모**에 둔다(필터 → `CardListPage`). 데이터는 props로 내려가고, 바꾸고 싶다는 신호는 함수 props로 올라온다.
- "아직 모름"을 하나의 상태로 따로 둔다: 조회의 `loading`, 보호 라우트의 세션 확인 중. 이걸 빼면 로그인한 사람도 새로고침 때 튕긴다.
- 화면에서 버튼을 숨기는 건 UX이고, 진짜 보호는 DB(RLS)가 한다. 브라우저에 들어가는 키는 누구나 볼 수 있다.
- push 전 문답에서 놓친 것 → 다시 볼 것([wiki/analyses/b1-2-review-qa.md](../../../wiki/analyses/b1-2-review-qa.md)):
  - useEffect는 "처음 마운트될 때 + 의존성이 바뀔 때" 실행된다.
  - 빈 상태는 "왜 비었는지"로 나눈다. 데이터가 없으면 만들기, 조건 때문이면 조건 풀기로 안내한다.

