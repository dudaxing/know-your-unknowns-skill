#!/usr/bin/env python3
"""Launch codex-verify bash-gate.sh with an explicit Git Bash (Claude protocol)."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    bash = (os.environ.get("CLAUDE_CODE_GIT_BASH_PATH") or "").strip().strip('"') or (
        r"D:\Program Files\Git\bin\bash.exe"
    )
    script = Path.home() / ".claude" / "skills" / "codex-verify" / "hooks" / "bash-gate.sh"
    if not Path(bash).is_file():
        print(f"[bash-gate launcher] Git Bash not found: {bash}", file=sys.stderr)
        return 2
    if not script.is_file():
        print(f"[bash-gate launcher] missing script: {script}", file=sys.stderr)
        return 2
    # Inherit stdin JSON from the hook runner; forward exit code (0 allow / 2 deny).
    completed = subprocess.run([bash, str(script)], check=False)
    return int(completed.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
