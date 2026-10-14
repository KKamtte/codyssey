---
title: 한 Mac에서 개인/회사 GitHub 계정 나눠 쓰기
updated: 2026-10-14
sources: []
---

회사 Mac에서 개인 계정(KKamtte) 레포를 다룰 때 쓴 방식. 키 값은 여기 두지 않는다.

1. 개인용 SSH 키를 따로 만들고 개인 계정 GitHub → Settings → SSH keys에 등록.
2. `~/.ssh/config`에 별칭 추가:
   ```
   Host github-kkamtte
     HostName github.com
     User git
     IdentityFile ~/.ssh/id_ed25519_kkamtte
     IdentitiesOnly yes
   ```
3. 클론/원격 주소에 별칭 사용: `git@github-kkamtte:KKamtte/<repo>.git`
4. `~/.gitconfig`에 폴더 단위로 작성자 정보 분리:
   ```
   [includeIf "gitdir:~/personal/"]
       path = ~/.gitconfig-personal
   ```
5. 확인: `ssh -T github-kkamtte` → `Hi KKamtte!`

브라우저도 분리: Chrome은 회사, Edge는 개인 GitHub 로그인. Claude in Chrome 확장은 시크릿 창을 다루지 못했다.

집 PC처럼 개인 계정만 쓰는 곳에서는 이 설정이 필요 없다.
