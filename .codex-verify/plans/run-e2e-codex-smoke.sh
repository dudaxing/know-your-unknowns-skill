#!/usr/bin/env bash
set -euo pipefail
cd /d/Coding/know-your-unkowns
export VERIFY_TASK_ID="e2e-codex-smoke-$$"
export VERIFY_BACKEND=codex
export VERIFY_ALLOWED_PATHS=".codex-verify/plans/e2e-codex-smoke.md"
bash "$HOME/.claude/skills/codex-verify/scripts/verify.sh" reset "$VERIFY_TASK_ID" 2>/dev/null || true
exec bash "$HOME/.claude/skills/codex-verify/scripts/verify.sh" plan "$(cat .codex-verify/plans/e2e-codex-smoke.md)"
