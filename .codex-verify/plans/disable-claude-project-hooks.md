# Simplify Cursor hooks: disable broken Claude bash gates in this project

## Goal
Stop Cursor Settings → Hooks from running failing Claude Project bash hooks on Windows. Keep the working Cursor native Python gates as the only project gates.

## Why not “point command at Git Bash”
`D:/Program Files/Git/bin/bash.exe` contains spaces. Cursor/Claude hook runners often execute the `command` string via PowerShell/cmd without reliable quoting, so absolute Git Bash paths break (`D:/Program` not found). That approach is not reliable here.

## Change (single file)
Replace `D:\Coding\know-your-unkowns\.claude\settings.json` contents with an empty hooks config so Claude Project config no longer registers PreToolUse gates in this repo:

```json
{
  "hooks": {}
}
```

## Keep as-is (do not change)
- `.cursor/hooks.json` — Python `plan_gate_cursor.py` / `bash_gate_cursor.py` remain the active Cursor gates (`failClosed: true`).
- Skill install at `C:/Users/Lenovo/.claude/skills/codex-verify` — unchanged.
- No commit unless asked.

## Allowed paths
- `.claude/settings.json`

## Trade-off (accepted)
Claude Code in this same project will not get project-level bash gates from `.claude/settings.json` until a space-safe wrapper is added later. Cursor protection remains via `.cursor/hooks.json`.

## Done when
- `.claude/settings.json` has `"hooks": {}`.
- Cursor Hooks panel Claude Project config no longer lists the failing `bash ~/.claude/...` entries (after Reload).
- Project config Python gates still listed and functional.
