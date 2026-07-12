#!/usr/bin/env python3
"""Repackage skill + commit Bug1 quiz perfect-score clarification on cursor."""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FILES = [
    "know-your-unknowns/SKILL.md",
    "know-your-unknowns/evals/smoke-triggers.md",
    "know-your-unknowns/references/artifact-patterns.md",
    "know-your-unknowns/references/merge-quiz.md",
    "dist/know-your-unknowns.skill",
]
MSG = (
    "Clarify merge-quiz perfect score requires all questions answered.\n"
)


def run(args: list[str], **kwargs) -> None:
    print("+", " ".join(args), flush=True)
    subprocess.check_call(args, cwd=ROOT, **kwargs)


def package() -> None:
    pack = Path.home() / ".claude/skills/skill-creator/scripts/package_skill.py"
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    run(
        [sys.executable, str(pack), "know-your-unknowns", "dist"],
        env=env,
    )
    skill = ROOT / "know-your-unknowns"
    zpath = ROOT / "dist" / "know-your-unknowns.skill"
    files = [p for p in skill.rglob("*") if p.is_file()]
    with zipfile.ZipFile(zpath) as z:
        names = z.namelist()
        exp = {"know-your-unknowns/" + p.relative_to(skill).as_posix() for p in files}
        assert set(names) == exp and len(names) == len(set(names))
        for p in files:
            n = "know-your-unknowns/" + p.relative_to(skill).as_posix()
            data = z.read(n)
            assert (zipfile.crc32(data) & 0xFFFFFFFF) == z.getinfo(n).CRC
            assert hashlib.sha256(data).digest() == hashlib.sha256(p.read_bytes()).digest()
    print("pack ok", len(files))


def main() -> int:
    branch = subprocess.check_output(
        ["git", "branch", "--show-current"], cwd=ROOT, text=True
    ).strip()
    if branch != "cursor":
        print(f"refusing: on {branch!r}, expected cursor", file=sys.stderr)
        return 2
    package()
    run(["git", "add", "--"] + FILES)
    run(["git", "commit", "-m", MSG])
    run(["git", "status", "-sb"])
    run(["git", "log", "-2", "--oneline"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
