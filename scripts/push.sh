#!/bin/bash
# Auto-push changes to GitHub
cd /home/openclaw/.openclaw/workspace

CHANGES=$(git status --porcelain)
if [ -z "$CHANGES" ]; then
    exit 0
fi

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S %Z')
git add -A
git commit -m "Auto-update $TIMESTAMP"
git push origin main 2>&1
