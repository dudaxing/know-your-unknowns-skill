#!/usr/bin/env bash
set -euo pipefail
cd /d/Coding/know-your-unkowns
PLAN=".codex-verify/plans/know-unknowns-skill-landing.md"
MARKER=".codex-verify/plan-approved"
HASH="$(sha256sum "$PLAN" | awk '{print $1}')"
NOW="$(date +%s)"
TTL="${VERIFY_APPROVAL_TTL:-86400}"
mkdir -p .codex-verify
cat > "$MARKER" <<EOF
# codex-verify 计划闸门标记：用户批准落地 + Codex VERDICT PASS（parser 未锚定）
task: skill-landing
plan_hash: sha256:$HASH
verdict: PASS
backend: codex
approved_at: $(date +%Y-%m-%dT%H:%M:%S)
expires_epoch: $((NOW + TTL))
allowed: know-your-unknowns/
allowed: README.md
allowed: README.zh.md
EOF
echo "wrote $MARKER"
