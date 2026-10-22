---
title: 시맨틱 HTML과 구조 설계 기준
updated: 2026-10-22
sources: []
---

[[b1-1]]에서 배운 것. 과제 목표 "시맨틱 태그를 왜 쓰고, 어떤 기준으로 구조를 설계했는지".

## 왜 쓰나
- `div`만 쓰면 사람 눈에는 같아 보여도 브라우저·화면 낭독기·검색 엔진은 어디가 메뉴고 본문인지 모른다.
- `header`/`nav`/`main`/`section`/`article`/`footer`는 "이 영역이 무슨 역할인지"를 태그 자체로 알려 준다. 화면 낭독기는 이걸로 영역 사이를 건너뛴다.

## 내가 쓴 기준
- 페이지에 한 번: `header > nav`, `main`, `footer`.
- 메뉴에서 이동하는 단위는 `section` + `id`(About, Experience, Skills, Projects, Contact). 각 section은 `aria-labelledby`로 자기 `h2`를 이름으로 쓴다.
- 혼자 떼어 내도 뜻이 통하는 덩어리는 `article`(경력 한 건, 프로젝트 카드 한 장).
- 순서가 의미 있으면 `ol`(경력 타임라인), 아니면 `ul`(기술 칩, 성과 수치).
- 제목은 `h1` 하나(Hero), 섹션은 `h2`, 그 안은 `h3`. 글자 크기 때문에 제목 단계를 건너뛰지 않는다(크기는 CSS로).

## 접근성으로 같이 챙긴 것
- 버튼 상태: 햄버거 `aria-expanded`, 테마·필터 버튼 `aria-pressed`.
- 폼: `label for`, 에러 문구를 `aria-describedby`로 연결, 틀린 칸에 `aria-invalid`.
- 바뀌는 문구(로딩·에러·성공)는 `aria-live="polite"`.
- 장식용 효과(타이핑)는 `aria-hidden`, 대신 `.sr-only`로 전체 문장을 둔다.
