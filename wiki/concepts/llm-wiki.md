---
title: LLM Wiki (이 위키의 운영 방식)
updated: 2026-10-14
sources: [[[karpathy-llm-wiki]]]
---

[[karpathy-llm-wiki]] 패턴을 기본으로 하고, 다음을 바꾸거나 더했다.

| 항목 | 결정 | 이유 |
|---|---|---|
| 규칙 파일 | `AGENTS.md` 본문 + `CLAUDE.md`는 `@AGENTS.md` 한 줄 | Claude Code가 주 도구지만 ChatGPT/Codex도 쓸 수 있게 |
| 링크 | Obsidian `[[링크]]` | 나중에 Obsidian으로 열어 그래프 보기 |
| 위치 | 과제 레포 안 `codyssey/wiki/` (규칙 파일은 레포 루트) | 이 학습용으로만 쓰므로 한 레포로. 클론·연결도 한 번 |
| 반영 | PR 없음. 미션은 작업 브랜치 → `main`에 `--no-ff` merge, 그 외는 `main`에 커밋 하나 | 작업을 Claude에 맡기므로 PR은 필요 없음. 미션은 작은 커밋을 남기고, 위키·규칙 작업은 단순하게 |
| 도구 | Claude Code CLI + 모바일 앱 Claude Code | 집, 외부 어디서든 이어서 |
| 공개 | 공개 레포 | 학칙상 금지 조항 없음 ([[codyssey]]) |
| 인수인계 | 별도 `now.md` 없이 `log.md` 최근 기록 + `wiki/plans/` | 원문 구조 유지 |
| plans/ | 원문에 없는 추가 폴더 | 미결정 사항, 집에서 확인할 일 |

## 원문과 다른 점

- 원문에는 "어디서든 이어서"라는 요구가 없다. 그래서 GitHub 레포를 기준 저장소로 두고 시작/끝 git 규칙을 추가했다.
- frontmatter 필드(`title`, `updated`, `sources`)는 Lint에서 낡은 페이지와 근거 없는 내용을 찾으려고 정했다.
