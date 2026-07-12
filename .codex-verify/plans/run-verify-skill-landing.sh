#!/usr/bin/env bash
set -euo pipefail
cd /d/Coding/know-your-unkowns
export VERIFY_TASK_ID="skill-landing-$$"
export VERIFY_ALLOWED_PATHS="know-your-unknowns/,README.md,README.zh.md"
bash "$HOME/.claude/skills/codex-verify/scripts/verify.sh" reset "$VERIFY_TASK_ID" 2>/dev/null || true
exec bash "$HOME/.claude/skills/codex-verify/scripts/verify.sh" plan "$(cat .codex-verify/plans/know-unknowns-skill-landing.md)"
