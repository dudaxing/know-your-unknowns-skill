#!/usr/bin/env bash
# Reset + re-review know-your-unknowns with Codex GPT-5.6 Sol
set -euo pipefail
cd /d/Coding/know-your-unkowns
export VERIFY_HOST=cursor
export VERIFY_REVIEW_BASE=main
export VERIFY_TASK_ID=know-your-unknowns-skill-review
export CODEX_MODEL=gpt-5.6-sol
bash "$HOME/.claude/skills/codex-verify/scripts/verify.sh" reset "$VERIFY_TASK_ID"
exec bash "$HOME/.claude/skills/codex-verify/scripts/verify.sh" review know-your-unknowns
