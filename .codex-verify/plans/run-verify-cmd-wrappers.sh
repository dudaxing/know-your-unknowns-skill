#!/usr/bin/env bash
set -euo pipefail
cd /d/Coding/know-your-unkowns
bash "$HOME/.claude/skills/codex-verify/scripts/verify.sh" reset plan-efa97a501918
exec bash "$HOME/.claude/skills/codex-verify/scripts/verify.sh" plan "$(cat .codex-verify/plans/claude-hooks-cmd-wrappers.md)"
