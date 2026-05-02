#!/bin/bash
# Auto-push: commit and push any untracked/modified files in IST repo
# Usage: ./auto_push.sh [optional commit message]

cd /home/selab/research/IST

MSG="${1:-Auto-push: update research artifacts $(date '+%Y-%m-%d %H:%M')}"

git add -A
if git diff --cached --quiet; then
    echo "[auto_push] nothing to commit"
    exit 0
fi

git commit -m "$MSG

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
git push
echo "[auto_push] done: $(git log --oneline -1)"
