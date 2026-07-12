# Windows-safe Claude project hooks via .cmd wrappers (cmd-safe paths)

## Human decision
Chose **B**: keep Claude Code project-level gates; do not empty `.claude/settings.json` hooks.

## Prior FAIL addressed
P0: `.cursor/hooks/...` forward-slash relative paths fail under `cmd.exe` (`.cursor` not recognized).
Fix: use cmd-safe `.\.cursor\hooks\...` backslash form in `.claude/settings.json`.

## Goal
Stop Cursor Hooks panel white-X for Claude Project config on Windows, keep Cursor Python gates + Claude bash gates.

## Changes

### 1. Exact file: `.cursor/hooks/claude_plan_gate.cmd`

```bat
@echo off
setlocal EnableExtensions
set "SCRIPT=%USERPROFILE%\.claude\skills\codex-verify\hooks\plan-gate.sh"
set "GIT_BASH=%CLAUDE_CODE_GIT_BASH_PATH%"
if not defined GIT_BASH set "GIT_BASH=D:\Program Files\Git\bin\bash.exe"
if not exist "%GIT_BASH%" (
  echo [plan-gate wrapper] Git Bash not found: "%GIT_BASH%" 1>&2
  exit /b 2
)
if not exist "%SCRIPT%" (
  echo [plan-gate wrapper] missing script: "%SCRIPT%" 1>&2
  exit /b 2
)
"%GIT_BASH%" "%SCRIPT%"
exit /b %ERRORLEVEL%
```

### 2. Exact file: `.cursor/hooks/claude_bash_gate.cmd`

```bat
@echo off
setlocal EnableExtensions
set "SCRIPT=%USERPROFILE%\.claude\skills\codex-verify\hooks\bash-gate.sh"
set "GIT_BASH=%CLAUDE_CODE_GIT_BASH_PATH%"
if not defined GIT_BASH set "GIT_BASH=D:\Program Files\Git\bin\bash.exe"
if not exist "%GIT_BASH%" (
  echo [bash-gate wrapper] Git Bash not found: "%GIT_BASH%" 1>&2
  exit /b 2
)
if not exist "%SCRIPT%" (
  echo [bash-gate wrapper] missing script: "%SCRIPT%" 1>&2
  exit /b 2
)
"%GIT_BASH%" "%SCRIPT%"
exit /b %ERRORLEVEL%
```

Wrappers inherit stdin; quote spaced Git Bash path; forward deny exit 2 via `exit /b %ERRORLEVEL%`.

### 3. Exact file: `.claude/settings.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit|NotebookEdit",
        "hooks": [
          { "type": "command", "command": ".\\.cursor\\hooks\\claude_plan_gate.cmd" }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": ".\\.cursor\\hooks\\claude_bash_gate.cmd" }
        ]
      }
    ]
  }
}
```

## Allowed paths
- `.claude/settings.json`
- `.cursor/hooks/claude_plan_gate.cmd`
- `.cursor/hooks/claude_bash_gate.cmd`

## Keep as-is
- `.cursor/hooks.json` + Python gates
- Skill `.sh` scripts
- No commit unless asked

## Smoke (local, before asking user to Reload Hooks panel)
From project root via `cmd.exe`:
1. `cmd /d /s /c ".\\.cursor\\hooks\\claude_plan_gate.cmd"` with Write-like JSON on stdin → exit 2
2. Same for bash wrapper with write-like Bash JSON → exit 2
3. Then user Reloads Hooks panel; Claude Project config should show the `.cmd` commands without white X

## Notes
- bash-gate denies write-like commands without marker; pure read may exit 0
- Cursor process PATH may differ from interactive shell; wrappers force Git Bash path explicitly
