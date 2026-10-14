---
title: Karpathy - LLM Wiki
updated: 2026-10-14
sources: []
---

원본: `wiki/raw/karpathy-llm-wiki.md` (https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

## 요약

- RAG는 질문할 때마다 원문에서 지식을 다시 찾는다. LLM Wiki는 LLM이 위키를 **계속 고쳐 가며 지식을 누적**한다.
- 3계층: raw sources(수정 금지) / wiki(LLM이 전부 작성) / schema(CLAUDE.md, AGENTS.md).
- 작업 3가지: Ingest(자료 하나가 10~15페이지를 고칠 수 있음), Query(좋은 답은 위키에 다시 저장), Lint(모순, 낡은 내용, 고아 페이지 점검).
- `index.md`는 내용 중심 목차, `log.md`는 시간순 기록. `## [날짜] 종류 | 제목` 형식이면 grep으로 뽑을 수 있다.
- 도구: Obsidian(사람이 보는 화면, 그래프 보기), Web Clipper, Dataview(frontmatter 질의), qmd(markdown 검색).
- 사람은 자료를 고르고 질문한다. 정리와 기록은 LLM이 한다.

## 이 위키에 적용한 방식

[[llm-wiki]] 참고.
