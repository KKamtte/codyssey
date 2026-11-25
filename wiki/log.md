# log

학습·미션 타임라인. 규칙은 [[AGENTS]]의 "log.md 규칙".

## [2026-10-14] setup | 학습 위키 구축
- Karpathy LLM Wiki 패턴으로 codyssey/wiki 구성. 운영 방식과 결정 이유는 [[llm-wiki]], 규칙은 AGENTS.md. 남은 할 일은 [[review-quiz]].

## [2026-10-14] ingest | Karpathy - LLM Wiki, 코디세이 과정/학칙
- [[karpathy-llm-wiki]] 요약, [[codyssey]]에 과정 단계·레포 구조·학칙 요점 정리. 학칙 원문은 공개 레포라 넣지 않음.

## [2026-10-14] mission | B1-1 시작
- 원문 받아 `01-ai-tools/B1-web-frontend/B1-1-self-intro-page/`에 README(요약·요구사항 체크리스트) 작성. 순수 HTML/CSS/JS 포트폴리오 + GitHub API + GitHub Pages 배포.

## [2026-10-22] quiz | B1-1 - 미디어 쿼리에서 덮어쓰는 규칙, 필터의 바뀌는 상태 값
- 768px 이상에서 `.nav__toggle`/`.nav__menu`를 무엇으로 덮어쓰는지 설명 못 함. 필터 클릭 시 바뀌는 값(`activeLanguage`)과 렌더 함수를 섞어 답함. 자세한 내용은 [[b1-1-review-qa]].

## [2026-10-22] mission | B1-1 완료
- GitHub Pages 배포(https://kkamtte.github.io/codyssey/01-ai-tools/B1-web-frontend/B1-1-self-intro-page/), README 회고·스크린샷. 배운 개념 [[semantic-html]], [[flexbox-vs-grid]], [[dom-event-state-render]], [[es6-syntax]], [[fetch-async-ui-state]]. 계획 [[b1-1]] done. 코디세이 제출은 사용자가 직접.

## [2026-10-27] mission | B1-2 시작
- 원문 받아 `01-ai-tools/B1-web-frontend/B1-2-react-spa/`에 README(요약·요구사항 체크리스트) 작성. React SPA(라우트 5개+, 재사용 컴포넌트 8개+) + Supabase/Firebase CRUD + Vercel/Netlify 배포. 계획 [[b1-2]].

## [2026-11-17] mission | B1-2 주제 변경과 결정 사항 확정
- 주제를 학습 위키 뷰어/에디터에서 **문답 카드**로 바꿈: 레포 `wiki/`와 앱의 Supabase 사본이 서로 반영되지 않아 원천이 두 개가 되는 문제. 스타일(CSS Modules), 보너스 전부(Auth·Context·메모이제이션), Vercel, 라우트·권한까지 구현 전에 모두 정함. [[b1-2]]

## [2026-11-17] mission | B1-2 구현 a-1 ~ a-9
- Vite + React 프로젝트, 레이아웃·라우트 7개, 공통 UI 컴포넌트 11개, Supabase 연결(`cards` 테이블·RLS·시드), 목록·상세 조회(`useCards`·`useCard`), 로그인·보호 라우트(`AuthContext`), 등록·수정 폼, 삭제, 토스트(`ToastContext`)·메모이제이션까지 구현. [[b1-2]]

## [2026-11-23] mission | B1-2 - Vercel 배포 막힘과 해결
- Import 목록에 개인 레포가 안 보임: Vercel GitHub 앱이 다른 조직에만 설치돼 있었음 → 개인 계정에 `codyssey` 레포 하나만 허용해 설치.
- 첫 Import는 `main`만 읽는데 `main`에는 아직 B1-2 폴더가 없어 Root Directory를 고를 수 없음 → 프로젝트를 먼저 만들고 설정에서 Root Directory·Vite를 지정. mission 브랜치는 Preview 배포로 확인하고, 공개 Production URL은 a-11 `main` merge 후. [[b1-2]]

## [2026-11-24] quiz | B1-2 - useEffect 첫 마운트 실행, 빈 상태 버튼 이유
- push 전 문답 8문항 중 6개 통과, 2개 부분. useEffect가 처음 마운트될 때도 실행된다는 점을 빠뜨림. 필터 때문에 0장인 빈 상태에 "필터 초기화"가 필요한 이유를 놓침. [[b1-2-review-qa]]

## [2026-11-24] mission | B1-2 완료
- 문답 8문항([[b1-2-review-qa]]) 후 `main` merge, Vercel Production 배포 https://b1-2-qa-cards.vercel.app (로그인 없이 열림 확인). 회고 작성, 개념 [[react-component-props-state]] · [[react-useeffect-data-fetching]] · [[spa-routing-deploy]] 정리. [[b1-2]]

## [2026-11-24] mission | B2-1 시작
- 원문 받아 `01-ai-tools/B2-python-git/B2-1-budget-cli/`에 README(요약·요구사항) 작성. 표준 라이브러리만으로 콘솔 가계부, JSONL 저장, 제너레이터 스트리밍·데코레이터·타입 힌트. 결정 사항 15개 확정(포맷·update 방식·카테고리 삭제·보너스 전부는 직접 결정). 계획 [[b2-1]].

## [2026-11-24] mission | B2-1 - 코드 리뷰로 찾은 저장 버그
- a-4 진행 중 옆 칸(herdr)의 다른 Claude 세션에 a-1~a-3 읽기 전용 리뷰를 맡김. 줄바꿈 없는 마지막 줄에 append 하면 두 거래가 한 줄로 붙는 문제, 필드 빠진 줄이 "예상 못 한 오류"로 나가는 문제, 원자적 교체 뒤 권한 0600 등을 찾아 고치고 회귀 테스트 15개 추가. [[atomic-file-write]]

## [2026-11-25] mission | B2-1 완료
- 문답 8문항 모두 통과([[b2-1-review-qa]]) 후 `main` merge. 명령 12개(보너스 backup·반복 내역 포함), 테스트 90개. 회고 작성, 개념 [[python-layered-cli]] · [[python-generator-streaming]] · [[atomic-file-write]] · [[python-decorator-cross-cutting]] 정리. [[b2-1]]
