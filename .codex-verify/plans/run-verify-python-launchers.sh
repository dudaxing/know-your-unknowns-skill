#!/usr/bin/env bash
set -euo pipefail
cd /d/Coding/know-your-unkowns
exec bash "$HOME/.claude/skills/codex-verify/scripts/verify.sh" plan "$(cat .codex-verify/plans/claude-hooks-python-launchers.md)"
