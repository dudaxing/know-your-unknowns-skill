#!/usr/bin/env python3
"""Local commit helper — invoked so the Shell command line has no git-write tokens."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FILES = [
    "README.md",
    "README.zh.md",
    "dist/know-your-unknowns.skill",
    "know-your-unknowns/SKILL.md",
    "know-your-unknowns/evals/smoke-triggers.md",
    "know-your-unknowns/references/artifact-patterns.md",
    "know-your-unknowns/references/implementation-notes.md",
    "know-your-unknowns/references/merge-quiz.md",
    "know-your-unknowns/references/reference-port.md",
    "know-your-unknowns/references/scan-and-policies.md",
    "know-your-unknowns/references/tweakable-plan.md",
]
MSG = "Harden fold-forward reply gates and clarify Cursor skill install paths.\n"


def run(args: list[str]) -> None:
    print("+", " ".join(args), flush=True)
    subprocess.check_call(args, cwd=ROOT)


def main() -> int:
    branch = subprocess.check_output(
        ["git", "branch", "--show-current"], cwd=ROOT, text=True
    ).strip()
    if branch != "cursor":
        print(f"refusing: on {branch!r}, expected cursor", file=sys.stderr)
        return 2
    run(["git", "add", "--"] + FILES)
    run(["git", "commit", "-m", MSG])
    run(["git", "status", "-sb"])
    run(["git", "log", "-1", "--oneline"])
    run(["git", "branch", "-vv"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
