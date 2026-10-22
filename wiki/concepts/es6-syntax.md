---
title: 화살표 함수, 구조분해, map/filter
updated: 2026-10-22
sources: []
---

[[b1-1]]에서 배운 것. 과제 목표 "왜 필요하고 어떻게 쓰는지".

| 문법 | 왜 | 이 페이지에서 |
|---|---|---|
| `const`/`let` | `var`는 함수 단위 범위라 블록 밖으로 새고 재선언된다. 바뀌지 않는 값은 `const`로 실수를 막는다 | 요소·상수는 전부 `const` |
| 화살표 함수 | 콜백을 짧게 쓴다. 자기 `this`가 없어 바깥 `this`를 그대로 쓴다 | `addEventListener('click', () => ...)`, `map((repo) => ...)` |
| 구조분해 | 객체에서 필요한 값만 이름으로 꺼낸다. 어떤 값을 쓰는지 함수 첫 줄에서 보인다 | `createRepoCard({ name, html_url, description, language, ... })` |
| 템플릿 리터럴 | 문자열 + 변수 + 줄바꿈을 한 번에 | 카드 HTML, 성공 문구 `${name}님, 감사합니다!` |
| `filter` | 조건에 맞는 것만 남긴 **새 배열** (원본 그대로) | 선택한 언어의 저장소만, 보여 줄 저장소 3개만 |
| `map` | 각 항목을 바꾼 **새 배열** | 저장소 → 카드 HTML, 폼 칸 → 검사 결과 |
| `sort` | 정렬 (원본을 바꾼다) | `pushed_at` 최신순 |
| `new Set` | 중복 제거 | 저장소 언어 목록 → 필터 버튼 |

## 주의: map vs every
- `formFields.every(validateField)`는 첫 `false`에서 멈춰 나머지 칸에 에러 문구가 안 뜬다.
- `validateField`는 문구를 쓰고 `aria-invalid`를 다는 **부수 효과**가 있으므로, `map`으로 모든 칸을 먼저 검사하고 결과 배열에 `every`를 쓴다.
