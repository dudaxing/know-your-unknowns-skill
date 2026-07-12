#!/usr/bin/env bash
set -euo pipefail
# Isolated e2e so we do not clobber the project's plan-approved marker.
ROOT="$(mktemp -d "${TMPDIR:-/tmp}/codex-e2e.XXXXXX")"
cleanup() { rm -rf "$ROOT"; }
trap cleanup EXIT
mkdir -p "$ROOT/.codex-verify/plans" "$ROOT/.git"
# minimal git repo so review tooling is happy if touched
git -C "$ROOT" init -q
cat > "$ROOT/.codex-verify/plans/smoke.md" <<'EOF'
# Isolated Codex connectivity smoke

## Goal
Confirm real Codex completes `verify.sh plan` with a machine-parseable verdict.

## Allowed side effects (explicit)
- Writing/updating `.codex-verify/plan-approved` on PASS
- Appending ledger/state under the codex-verify state directory
- Creating task state files for anti-kickball tracking

## Scope
No product/source edits outside this temporary workspace.

## Allowed paths
- `.codex-verify/plans/`
- `.codex-verify/plan-approved`

## Done when
Codex returns a final line that is exactly `VERDICT: PASS` (or FAIL/ESCALATE if it finds a real issue in this smoke plan).
EOF
cd "$ROOT"
export VERIFY_TASK_ID="isolated-e2e-$$"
export VERIFY_BACKEND=codex
export VERIFY_ALLOWED_PATHS=".codex-verify/plans/,.codex-verify/plan-approved"
echo "workdir=$ROOT"
bash "$HOME/.claude/skills/codex-verify/scripts/verify.sh" plan "$(cat .codex-verify/plans/smoke.md)"
echo "verify_exit=$?"
ls -la .codex-verify/ 2>/dev/null || true
if [ -f .codex-verify/plan-approved ]; then
  echo "--- marker ---"
  cat .codex-verify/plan-approved
fi
