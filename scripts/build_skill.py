#!/usr/bin/env python3
"""Validate and package the know-your-unknowns skill.

The packaged .skill file is a build artifact and is deliberately NOT tracked in
git: a committed binary drifts from source the moment someone edits a reference
file without rebuilding. Build it when you need it; CI builds it for releases.

    python scripts/build_skill.py --check     validate only (what CI runs on push)
    python scripts/build_skill.py             validate, then write dist/<name>.skill

Standard library only, so it runs anywhere Python 3.8+ does. All file I/O is
explicitly UTF-8: the default codepage on a Chinese Windows install is GBK and
silently fails to decode these files. Output is ASCII for the same reason -- a
GBK console raises UnicodeEncodeError on emoji.
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO / "know-your-unknowns"
DIST = REPO / "dist"

DESCRIPTION_LIMIT = 1024

# Machine- and tool-specific patterns that must never reach the distributed skill.
# Each entry is (compiled pattern, human explanation).
POLLUTION = [
    (re.compile(r"[A-Za-z]:[\\/]Users[\\/]", re.I),
     "absolute Windows user path -- use a host-relative path or an example placeholder"),
    (re.compile(r"/home/[a-z][a-z0-9_-]*", re.I),
     "absolute Linux home path -- use a host-relative path or an example placeholder"),
    (re.compile(r"\$HOME/"),
     "hardcoded $HOME path -- the skill must not assume where a host installs things"),
    (re.compile(r"skills/[A-Za-z0-9_-]+/(scripts|hooks)/"),
     "reaches into another skill's install path -- let the host route instead"),
]

# README files legitimately document install paths, so they are checked only for
# a literal user directory (install docs should use ~ or $env:USERPROFILE).
README_POLLUTION = [POLLUTION[0], POLLUTION[1]]

LINK_RE = re.compile(r"\]\((?!https?://|#)([^)]+\.(?:md|html))(?:#[^)]*)?\)")


def fail(problems: list[str]) -> None:
    print("FAILED: %d problem(s)" % len(problems))
    for p in problems:
        print("  - " + p)
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    fields: dict[str, str] = {}
    for line in text[3:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t", "#")):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


def validate() -> list[str]:
    problems: list[str] = []

    if not SKILL_DIR.is_dir():
        return ["skill directory not found: %s" % rel(SKILL_DIR)]

    skill_md = SKILL_DIR / "SKILL.md"
    if not skill_md.is_file():
        return ["missing %s" % rel(skill_md)]

    # --- frontmatter ---
    fm = parse_frontmatter(read(skill_md))
    if not fm:
        problems.append("%s: no YAML frontmatter" % rel(skill_md))
    else:
        name = fm.get("name", "")
        if not name:
            problems.append("%s: frontmatter has no 'name'" % rel(skill_md))
        elif name != SKILL_DIR.name:
            problems.append(
                "%s: name '%s' does not match directory '%s'"
                % (rel(skill_md), name, SKILL_DIR.name))
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name or ""):
            problems.append("%s: name '%s' is not lowercase-kebab-case" % (rel(skill_md), name))

        desc = fm.get("description", "")
        if not desc:
            problems.append("%s: frontmatter has no 'description'" % rel(skill_md))
        elif len(desc) > DESCRIPTION_LIMIT:
            problems.append(
                "%s: description is %d characters, limit is %d"
                % (rel(skill_md), len(desc), DESCRIPTION_LIMIT))

        extra = set(fm) - {"name", "description"}
        if extra:
            problems.append(
                "%s: unexpected frontmatter fields: %s"
                % (rel(skill_md), ", ".join(sorted(extra))))

    # --- internal links resolve ---
    for md in sorted(SKILL_DIR.rglob("*.md")):
        for target in LINK_RE.findall(read(md)):
            if not (md.parent / target).exists():
                problems.append("%s: broken link -> %s" % (rel(md), target))

    for readme in sorted(REPO.glob("README*.md")):
        for target in LINK_RE.findall(read(readme)):
            if not (readme.parent / target).exists():
                problems.append("%s: broken link -> %s" % (rel(readme), target))

    # --- no machine- or tool-specific content ---
    def scan(paths, rules):
        for path in paths:
            for lineno, line in enumerate(read(path).splitlines(), 1):
                for pattern, why in rules:
                    if pattern.search(line):
                        problems.append(
                            "%s:%d: %s\n      %s" % (rel(path), lineno, why, line.strip()[:100]))

    scan(sorted(p for p in SKILL_DIR.rglob("*") if p.suffix in {".md", ".html"}), POLLUTION)
    scan(sorted(REPO.glob("README*.md")), README_POLLUTION)

    # --- nothing unexpected inside the skill directory ---
    allowed_suffixes = {".md", ".html"}
    for path in sorted(SKILL_DIR.rglob("*")):
        if path.is_file() and path.suffix not in allowed_suffixes:
            problems.append("%s: unexpected file type in the skill payload" % rel(path))

    return problems


def build() -> Path:
    """Write a byte-reproducible .skill archive. Same source -> same bytes."""
    DIST.mkdir(exist_ok=True)
    out = DIST / (SKILL_DIR.name + ".skill")
    files = sorted(
        (p for p in SKILL_DIR.rglob("*") if p.is_file()),
        key=lambda p: p.relative_to(SKILL_DIR).as_posix(),
    )
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            arcname = "%s/%s" % (SKILL_DIR.name, path.relative_to(SKILL_DIR).as_posix())
            # Fixed timestamp and mode: rebuilding unchanged source must not
            # produce a different file, or "is it stale?" becomes unanswerable.
            info = zipfile.ZipInfo(arcname, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, path.read_bytes())
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true",
                        help="validate only; do not write the archive")
    args = parser.parse_args()

    problems = validate()
    if problems:
        fail(problems)

    count = sum(1 for p in SKILL_DIR.rglob("*") if p.is_file())
    print("OK: %s validated (%d files)" % (SKILL_DIR.name, count))

    if args.check:
        return

    out = build()
    print("Built %s (%d bytes)" % (rel(out), out.stat().st_size))


if __name__ == "__main__":
    main()
