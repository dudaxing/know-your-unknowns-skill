# Claude project hooks via Python launchers (match working Cursor pattern)

## Human decisions
- Chose **B**: keep Claude Code project-level gates (do not empty hooks).
- Chose **继续**: abandon `.cmd` path forms; use Python launchers identical in shape to the already-working Cursor Project config.

## Why this works
Existing `.cursor/hooks.json` already succeeds with:
`D:/ProgramData/Anaconda3/python.exe .cursor/hooks/plan_gate_cursor.py`
(no spaces in the executable; relative script is an argument, not the command token).

Claude Project config previously used `bash ~/.claude/...`, which fails/hangs under Cursor’s third-party runner. Reuse the same python.exe + relative-script pattern, but launch the skill `.sh` gates via explicit Git Bash so Claude protocol (exit 0/2) is preserved.

## Changes

### 1. `.cursor/hooks/run_claude_plan_gate.py` (exact)

```python
#!/usr/bin/env python3
"""Launch codex-verify plan-gate.sh with an explicit Git Bash (Claude protocol)."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    bash = os.environ.get("CLAUDE_CODE_GIT_BASH_PATH") or r"D:\Program Files\Git\bin\bash.exe"
    script = Path.home() / ".claude" / "skills" / "codex-verify" / "hooks" / "plan-gate.sh"
    if not Path(bash).is_file():
        print(f"[plan-gate launcher] Git Bash not found: {bash}", file=sys.stderr)
        return 2
    if not script.is_file():
        print(f"[plan-gate launcher] missing script: {script}", file=sys.stderr)
        return 2
    # Inherit stdin JSON from the hook runner; forward exit code (0 allow / 2 deny).
    completed = subprocess.run([bash, str(script)], check=False)
    return int(completed.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
```

### 2. `.cursor/hooks/run_claude_bash_gate.py` (exact)

Same as above, but script name `bash-gate.sh` and stderr prefix `[bash-gate launcher]`.

### 3. `.claude/settings.json` (exact)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit|NotebookEdit",
        "hooks": [
          {
            "type": "command",
            "command": "D:/ProgramData/Anaconda3/python.exe .cursor/hooks/run_claude_plan_gate.py"
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "D:/ProgramData/Anaconda3/python.exe .cursor/hooks/run_claude_bash_gate.py"
          }
        ]
      }
    ]
  }
}
```

## Allowed paths
- `.claude/settings.json`
- `.cursor/hooks/run_claude_plan_gate.py`
- `.cursor/hooks/run_claude_bash_gate.py`

## Keep as-is
- `.cursor/hooks.json` and Cursor-native Python gates
- Skill `.sh` gates (read-only)
- No commit unless asked

## Smoke after implement
From project root:
1. Pipe Write-like JSON into `D:/ProgramData/Anaconda3/python.exe .cursor/hooks/run_claude_plan_gate.py` → exit 2 without plan-approved
2. Pipe write-like Bash JSON into bash launcher → exit 2
3. User Reloads Hooks panel; Claude Project config should list the python.exe commands (no white X from missing bash)

## Notes
- bash-gate only denies write-like commands; pure reads may exit 0
- Launchers force Git Bash path so Cursor PATH order (WSL bash first) cannot hijack the skill scripts
