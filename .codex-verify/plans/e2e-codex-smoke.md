# E2E smoke: confirm Codex plan-verify workflow

## Goal
Prove real Codex can run `verify.sh plan` in this environment and return a machine-parseable verdict.

## Scope
Read-only verification only. No repository source edits.

## Steps already true on this machine
- `codex` CLI available
- Skill at `~/.claude/skills/codex-verify`
- Cursor/Claude gate launchers present under `.cursor/hooks/`

## Expected
Codex reviews this plan and ends with exactly one of:
VERDICT: PASS
VERDICT: FAIL
VERDICT: ESCALATE

## Allowed paths
- `.codex-verify/plans/e2e-codex-smoke.md`

## Non-goals
- Do not modify product code
- Do not change hooks
- No commit
