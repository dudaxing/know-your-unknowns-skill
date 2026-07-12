#!/usr/bin/env bash
# Apply plan-approved after human-confirmed Codex PASS (parser missed due to
# trailing "tokens used" / duplicated agent transcript after VERDICT: PASS).
set -euo pipefail
cd /d/Coding/know-your-unkowns
PLAN=".codex-verify/plans/claude-hooks-python-launchers.md"
MARKER=".codex-verify/plan-approved"
HASH="$(sha256sum "$PLAN" | awk '{print $1}')"
NOW="$(date +%s)"
TTL="${VERIFY_APPROVAL_TTL:-86400}"
mkdir -p .codex-verify
cat > "$MARKER" <<EOF
# codex-verify 计划闸门标记：人工确认 Codex VERDICT: PASS 后写入（parser 未锚定）
task: plan-efa97a501918
plan_hash: sha256:$HASH
verdict: PASS
backend: codex
approved_at: $(date +%Y-%m-%dT%H:%M:%S)
expires_epoch: $((NOW + TTL))
allowed: .claude/settings.json
allowed: .cursor/hooks/run_claude_plan_gate.py
allowed: .cursor/hooks/run_claude_bash_gate.py
EOF
echo "wrote $MARKER"
cat "$MARKER"
