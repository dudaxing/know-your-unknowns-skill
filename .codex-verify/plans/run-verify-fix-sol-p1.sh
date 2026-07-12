#!/usr/bin/env bash
set -euo pipefail
cd /d/Coding/know-your-unkowns
export VERIFY_HOST=cursor
export CODEX_MODEL=gpt-5.6-sol
export VERIFY_BACKEND=codex
export VERIFY_TASK_ID=know-your-unknowns-fix-sol-p1-r11
export VERIFY_ALLOWED_PATHS="know-your-unknowns/,README.md,README.zh.md,dist/,.cursor/skills/know-your-unknowns/"
exec bash "$HOME/.claude/skills/codex-verify/scripts/verify.sh" plan < .codex-verify/plans/fix-sol-p1-p2.md
