# Fix Claude Project hooks on Windows (Git Bash path)

## Goal
Make Cursor Settings → Hooks stop failing on Claude Project config entries, without weakening the Cursor native Python gates.

## Problem
- Project config (`.cursor/hooks.json` + Python adapters) works; DENY is expected without `plan-approved`.
- Claude Project config (`.claude/settings.json`) runs `bash ~/.claude/skills/codex-verify/hooks/*.sh`.
- On this machine `bash` resolves to `C:\Windows\System32\bash.exe` (WSL), so those hooks fail with white X (~27s).

## Change (single file)
Update `D:\Coding\know-your-unkowns\.claude\settings.json` so both PreToolUse commands use Git Bash absolute path:

- `"D:/Program Files/Git/bin/bash.exe" "C:/Users/Lenovo/.claude/skills/codex-verify/hooks/plan-gate.sh"`
- `"D:/Program Files/Git/bin/bash.exe" "C:/Users/Lenovo/.claude/skills/codex-verify/hooks/bash-gate.sh"`

## Allowed paths
- `.claude/settings.json`

## Non-goals
- Do not disable Cursor Python gates.
- Do not change gate policy / failClosed.
- Do not commit unless asked.

## Done when
- `.claude/settings.json` uses Git Bash absolute paths.
- Hooks Reload no longer shows white X for Claude Project config (or those hooks succeed).
