---
title: fetch + async/await와 로딩·성공·에러·빈 상태
updated: 2026-10-22
sources: []
---

[[b1-1]]에서 배운 것. 과제 목표 "비동기로 데이터를 가져오고, 상태를 UI로 어떻게 표현했는지". 흐름은 [[dom-event-state-render]].

## async/await
- `fetch`는 Promise를 돌려준다. `await`로 결과를 기다리면 위에서 아래로 읽히는 코드가 된다. `try/catch`로 실패를 잡는다.
- 응답 본문도 `await response.json()`으로 한 번 더 기다린다.

## fetch가 실패로 치는 것
- **네트워크가 끊겼을 때만** reject된다(`TypeError`). 404·403·500 같은 HTTP 에러는 정상 응답으로 온다.
- 그래서 직접 확인해야 한다.
  ```js
  if (response.status === 403) throw new Error('GitHub API 요청 한도를 넘었습니다. ...');
  if (!response.ok) throw new Error(`GitHub API 응답 오류 (${response.status})`);
  ```
- 403이 오면: `throw` → `catch (error)` → `error instanceof TypeError`는 false(네트워크 문제가 아님) → `setProjectsState({ status: 'error', errorMessage })` → `renderProjects()`가 에러 문구와 "다시 시도" 버튼을 그린다.
- 인증 없는 GitHub API는 시간당 60회 제한. 넘으면 403.

## 상태 4가지와 화면
| status | 화면 |
|---|---|
| `loading` | 스피너 + "로딩 중..." |
| `success` | 카드 목록 (선택한 언어로 거른 것) |
| `empty` | "표시할 프로젝트가 없습니다." |
| `error` | 에러 문구 + 원인별 설명 + "다시 시도" 버튼 (`loadProjects` 다시 호출) |

- 상태 문구 영역은 `aria-live="polite"`라 화면 낭독기도 바뀐 걸 읽는다.
- 확인할 때는 `window.fetch`를 잠깐 가짜로 바꿔 403·네트워크 실패·500·빈 목록·느린 응답을 하나씩 재현했다.
