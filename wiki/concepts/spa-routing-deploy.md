---
title: SPA 라우팅, 보호 라우트, 정적 배포(Vercel)와 권한
updated: 2026-11-24
sources: []
---

[[b1-2]]에서 배운 것. React Router로 화면을 나누고, 로그인한 사람만 들어가게 막고, Vercel에 정적 사이트로 올리면서 생긴 문제와 이유. 문답은 [[b1-2-review-qa]] Q6·Q7·Q8.

## 클릭 이동과 새로고침의 차이
- **클릭**: React Router가 주소창만 바꾸고(History API) 맞는 페이지 컴포넌트를 그린다. 서버에 요청하지 않는다. 그래서 Single Page.
- **새로고침·주소 직접 입력**: 브라우저가 서버에 `/cards/3`을 직접 요청한다. 빌드 결과(`dist`)에는 `index.html`과 `assets/`뿐이라 404가 난다.
- 해결: `vercel.json` rewrite로 어떤 주소든 `index.html`을 돌려준다. React가 뜬 뒤 `BrowserRouter`가 주소를 읽어 그 화면을 그린다.
  ```json
  { "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }] }
  ```

## 보호 라우트
- 등록·수정 라우트를 `ProtectedRoute`로 감싼다. 로그인 안 했으면 `<Navigate to="/login" state={{ from: location }} />`로 보내고, 로그인 후 원래 주소로 돌아온다.
- 세션 확인 중(`loading`)에는 판단하지 않고 기다린다. "모름"과 "없음"을 구분하는 것은 [[react-useeffect-data-fetching]]의 상태 구분과 같은 생각이다.

## 환경변수는 빌드할 때 들어간다 (Vite)
- `VITE_`로 시작하는 값만 클라이언트 코드에 노출되고, `import.meta.env.VITE_...`는 **빌드할 때 실제 값으로 바뀌어** JS 파일에 박힌다.
- `.env.local`은 git에 올리지 않으므로, 빌드하는 Vercel 대시보드에 같은 값을 등록하고 **그다음에** 빌드해야 한다.
- 번들에 들어간 값은 누구나 개발자 도구로 볼 수 있다. 비밀 키는 넣지 않는다. Supabase anon(publishable) key는 원래 공개용이다.

## 버튼 숨기기는 UX, 보호는 RLS
- 남의 카드에 수정·삭제 버튼을 숨기는 건 화면 편의다. anon key와 API 주소는 공개돼 있으니 누구든 직접 요청을 보낼 수 있다.
- 실제로 막는 건 DB의 RLS 정책이다. 조회는 누구나, 등록은 로그인 사용자, 수정·삭제는 `user_id = auth.uid()`인 작성자만.

## Vercel에서 겪은 것
- 레포 하나에 과제가 여러 개라 **Root Directory**를 과제 폴더로 지정한다.
- 첫 Import는 기본 브랜치(`main`)만 읽는다. 폴더가 아직 미션 브랜치에만 있으면 프로젝트를 먼저 만들고 설정에서 Root Directory를 지정한 뒤, 미션 브랜치는 **Preview**(Vercel 로그인한 본인만 열림), `main` merge 후 **Production**(공개)으로 확인했다.
- GitHub 앱은 계정·조직마다 따로 설치된다. 레포가 목록에 없으면 그 계정에 앱이 설치됐는지 본다.
