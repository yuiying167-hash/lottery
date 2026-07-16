---
date: 2026-07-16
type: docs
status: resolved
---

# GitHub 연결 방식 문서화

## What
lottery-spattra 프로젝트에서 GitHub 푸시가 안 되던 문제 해결 및 연결 방식 문서화

## Why
- SSH 키 미설정으로 `git push` 실패 (403 Permission denied)
- HTTPS URL → SSH로 변경 필요
- yuiying 계정 전용 SSH alias 없음

## Files changed
- `~/.ssh/config` — GitHub alias 추가
- `origin/main` — og-image.png 커밋 푸시

## How
```bash
# 1. SSH config에 lottery 전용 alias 추가 (~/.ssh/config)
cat >> ~/.ssh/config << 'EOF'
Host github-lottery
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_yuiying
EOF

# 2. git remote URL 변경
git remote set-url origin github-lottery:yuiying167-hash/lottery.git

# 3. 푸시 실행
git push origin main
```

## Verification
- `git push origin main` 성공 (커밋 2개 푸시됨)
- SHA: `7982b3a` og-image.png 추가, `c5441aa` handoff 파일 추가

## GitHub 연결 상세 정보

### SSH 키 위치
```
~/.ssh/
├── id_ed25519_farmsolution.pub  # farmSolution 계정
├── id_ed25519_hugh.pub          # hugh 계정 (hugh79757-cmyk)
└── id_ed25519_yuiying.pub      # yuiying 계정 (이 프로젝트 전용)
```

### Remote URLs
```
origin  git@github.com:yuiying167-hash/lottery.git (SSH, 현재)
origin  https://github.com/yuiying167-hash/lottery.git (HTTPS, 이전)
```

### 인증 방법
1. **SSH 방식** (권장): `~/.ssh/config`에 Host alias 설정
2. **HTTPS + 토큰**: `GITHUB_TOKEN` 환경변수 필요
3. **gh CLI**: `gh auth login` 후 `gh repo` 명령어 사용

### 자주 쓰는 명령어
```bash
# 상태 확인
git status --short
git log --oneline -5

# 푸시
git push origin main

# GitHub 확인 (gh CLI)
gh repo view yuiying167-hash/lottery
gh api repos/yuiying167-hash/lottery/contents/og-image.png
```