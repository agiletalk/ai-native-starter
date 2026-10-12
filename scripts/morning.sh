#!/usr/bin/env bash
# 아침 10분 읽기: 최근 변경된 문서와 커밋을 보여준다.
# 사용법: scripts/morning.sh [일수]   (기본 1일, 월요일엔 3을 권장)
set -euo pipefail

days="${1:-1}"
since="${days} days ago"
cd "$(git rev-parse --show-toplevel)"
git fetch --quiet 2>/dev/null || true

echo "== 최근 ${days}일 사이에 바뀐 문서 =="
docs=$(git log --since="$since" --name-only --pretty=format: -- docs/ | grep -v '^$' | sort -u || true)
if [ -n "$docs" ]; then echo "$docs"; else echo "(없음)"; fi

echo
echo "== 최근 ${days}일 커밋 =="
git log --since="$since" --pretty=format:'%h %an  %s' --all || true
echo
