---
title: push 전 문답(퀴즈) 방식 - 계획
updated: 2026-10-14
sources: []
status: open
---

과제 변경을 push하기 전에 Claude가 변경 코드를 보고 질문을 내고, 내가 답하는 방식. 동료 평가 예행연습 겸 학습 기록.
PR을 쓰지 않으므로 "PR 전"이 아니라 "push 전"에 한다 (Git 운영은 [[AGENTS]]).

## 검토한 선택지

| 방식 | 내용 | 비용 | 판단 |
|---|---|---|---|
| A. GitHub Actions 질문 봇 | `anthropics/claude-code-action`이 PR에 질문 코멘트 | Actions는 공개 레포 무료. Claude 호출은 API 키(종량 과금) 또는 구독 토큰(구독 한도 사용) | 보류. PR을 안 쓰기로 해서 우선순위 낮음. 회사 구독 토큰을 개인 레포에 넣으면 안 됨 |
| B. push 전 세션 문답 | Claude Code 세션에서 `/quiz` 같은 스킬로 출제 → 답변 → 꼬리 질문 | 추가 비용 없음 | **우선 후보** |

## 원칙

- 문답 중에는 정답을 바로 주지 않고 질문으로 이끈다. 코드는 Claude가 써도 되지만, 이 단계의 목적은 내가 설명할 수 있는지 확인하는 것이다 ([[codyssey]] 학습 철학).
- 버그로 보이는 곳은 위치만 짚는다.

## 집에서 개인 계정으로 확인할 것

- [ ] 개인 Claude 계정(구독 여부, 한도)으로 Claude Code CLI 로그인 확인
- [ ] 집 PC에 클론: `git clone git@github.com:KKamtte/codyssey.git` 후 Claude Code에서 규칙(`AGENTS.md`)을 읽는지 확인
- [ ] 모바일 앱 Claude Code에서 `KKamtte/codyssey` 레포 연결, `AGENTS.md` Git 규칙대로 동작하는지 확인 (모바일은 자체 브랜치를 만들 수 있음)
- [ ] 방식 B: `/quiz` 스킬을 레포 안(`.claude/skills/`)에 둘지, 개인 전역(`~/.claude/skills/`)에 둘지 결정. 레포 안이면 모바일에서도 같이 쓰임. 단 지금 `.gitignore`가 `.claude`를 통째로 제외하므로 `!.claude/skills/` 예외 추가 필요
- [ ] 문답 기록 위치 결정: 과제 폴더 `review-qa.md` / `wiki/analyses/` / 둘 다
- [ ] (선택) 방식 A가 필요하면 개인 계정 기준 비용 확인 후 결정

## 이어서 할 일

- [x] codyssey B1-1 과제 시작 (2026-10-14) → [[b1-1]]
- [ ] 「동료 평가 규칙」 문서 읽고 [[codyssey]]에 요약
