#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    branch = subprocess.check_output(
        ["git", "branch", "--show-current"], cwd=ROOT, text=True
    ).strip()
    if branch != "cursor":
        print(f"refusing: on {branch!r}, expected cursor", file=sys.stderr)
        return 2
    print("+ git push -u origin HEAD", flush=True)
    subprocess.check_call(["git", "push", "-u", "origin", "HEAD"], cwd=ROOT)
    subprocess.check_call(["git", "status", "-sb"], cwd=ROOT)
    subprocess.check_call(["git", "log", "-2", "--oneline"], cwd=ROOT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
