#!/usr/bin/env python3
"""Run deterministic structural checks for the repository's Codex Skill."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment failure path
    print("ERROR: PyYAML is required to validate YAML files.", file=sys.stderr)
    raise SystemExit(2) from exc


EXPECTED_FILES = {
    "SKILL.md",
    "agents/openai.yaml",
    "references/probe-playbook.md",
    "references/risk-patterns.md",
}
FRONTMATTER_KEYS = {"name", "description"}
PLACEHOLDER_PATTERNS = (
    r"\bTODO\b",
    r"\bTBD\b",
    r"ARTIFACT TITLE",
    r"\[TODO",
    r"placeholder",
)
PLATFORM_PATTERNS = (
    r"CLAUDE_SKILL_DIR",
    r"\.claude[/\\]skills",
    r"~/\.claude",
    r"/unknowns-first-code-design",
)
REMOVED_MECHANISMS = (
    r"impact\s*[×x*]\s*uncertainty\s*[×x*]\s*irreversibility",
    r"\.agent[/\\]unknowns",
    r"ledger\.json",
)
TRIGGER_CATEGORY_COUNTS = {
    "positive": 8,
    "explicit": 4,
    "immediate": 2,
    "near_negative": 6,
    "negative": 5,
}
TRIGGER_SPLIT_COUNTS = {"train": 15, "validation": 10}
TRIGGER_INTENSITIES = {
    "full",
    "bounded",
    "lightweight",
    "premise-check-then-implement",
    "none",
}
BEHAVIOR_ASSERTION_COUNTS = [8, 9, 7, 6, 8, 6, 5, 5]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the repository's reduce-critical-unknowns Skill and eval corpus."
    )
    parser.add_argument(
        "--skill",
        type=Path,
        default=Path(".agents/skills/reduce-critical-unknowns"),
        help="Path to the Skill directory.",
    )
    parser.add_argument(
        "--eval-dir",
        type=Path,
        default=Path("evals/reduce-critical-unknowns"),
        help="Path to evaluation materials.",
    )
    return parser.parse_args()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_frontmatter(path: Path, errors: list[str]) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
    if not match:
        fail(errors, "SKILL.md must begin with YAML frontmatter.")
        return {}, text
    try:
        metadata = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        fail(errors, f"SKILL.md frontmatter is invalid YAML: {exc}")
        return {}, text
    if not isinstance(metadata, dict):
        fail(errors, "SKILL.md frontmatter must be a mapping.")
        return {}, text
    return metadata, text


def check_links(skill: Path, errors: list[str]) -> None:
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    skill_links: set[str] = set()
    for markdown in skill.rglob("*.md"):
        text = markdown.read_text(encoding="utf-8")
        for target in link_re.findall(text):
            if re.match(r"^[a-z]+://", target) or target.startswith("#"):
                continue
            clean = target.split("#", 1)[0]
            resolved = (markdown.parent / clean).resolve()
            try:
                resolved.relative_to(skill.resolve())
            except ValueError:
                fail(errors, f"Link escapes Skill directory: {markdown}: {target}")
                continue
            if not resolved.exists():
                fail(errors, f"Broken relative link: {markdown}: {target}")
            if markdown == skill / "SKILL.md":
                skill_links.add(clean.replace("\\", "/"))
    expected_refs = {
        "references/probe-playbook.md",
        "references/risk-patterns.md",
    }
    if not expected_refs.issubset(skill_links):
        fail(errors, "Every reference must be linked directly from SKILL.md.")


def check_duplicate_paragraphs(skill: Path, errors: list[str]) -> None:
    seen: dict[str, list[str]] = {}
    for markdown in skill.rglob("*.md"):
        text = markdown.read_text(encoding="utf-8")
        for paragraph in re.split(r"\n\s*\n", text):
            normalized = re.sub(r"\s+", " ", paragraph.strip()).casefold()
            if len(normalized) < 120 or normalized.startswith("```"):
                continue
            seen.setdefault(normalized, []).append(str(markdown.relative_to(skill)))
    for paragraph, locations in seen.items():
        if len(locations) > 1:
            fail(errors, f"Duplicated long paragraph in {locations}: {paragraph[:80]}...")


def check_repository_boundaries(repo_root: Path, skill: Path, errors: list[str]) -> None:
    skills_root = repo_root / ".agents" / "skills"
    skill_dirs = sorted(path.name for path in skills_root.iterdir() if path.is_dir())
    if skill_dirs != [skill.name]:
        fail(errors, f"Repository must expose only the primary Skill; found {skill_dirs}.")

    forbidden_files: list[str] = []
    platform_paths: list[str] = []
    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(repo_root)
        if ".git" in relative.parts:
            continue
        if path.suffix.casefold() in {".html", ".skill"}:
            forbidden_files.append(str(relative))
        if any(part.casefold() == ".claude" for part in relative.parts):
            platform_paths.append(str(relative))
    if forbidden_files:
        fail(errors, f"Forbidden legacy artifact files outside the Skill: {forbidden_files}")
    if platform_paths:
        fail(errors, f"Claude-specific repository paths are not allowed: {platform_paths}")

    legacy_root = repo_root / "know-your-unknowns"
    legacy_files = [path for path in legacy_root.rglob("*") if path.is_file()] if legacy_root.exists() else []
    if legacy_files:
        fail(errors, "Legacy know-your-unknowns runtime directory must not coexist with the new Skill.")


def check_trigger_cases(eval_dir: Path, errors: list[str]) -> tuple[int, Counter]:
    path = eval_dir / "trigger-cases.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(errors, f"Cannot parse trigger cases: {exc}")
        return 0, Counter()
    if data.get("schema_version") != 1:
        fail(errors, "trigger-cases.json schema_version must be 1.")
    if data.get("skill") != "reduce-critical-unknowns":
        fail(errors, "trigger-cases.json must target reduce-critical-unknowns.")
    cases = data.get("cases")
    if not isinstance(cases, list):
        fail(errors, "trigger-cases.json must contain a cases list.")
        return 0, Counter()
    required = {
        "id",
        "split",
        "category",
        "prompt",
        "expected_activation",
        "expected_intensity",
        "required_signals",
        "rationale",
    }
    ids: list[str] = []
    categories: Counter = Counter()
    splits: Counter = Counter()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            fail(errors, f"Trigger case {index} must be an object.")
            continue
        case_keys = set(case)
        missing = required - case_keys
        extra = case_keys - required
        if missing:
            fail(errors, f"Trigger case {index} missing fields: {sorted(missing)}")
        if extra:
            fail(errors, f"Trigger case {index} has unexpected fields: {sorted(extra)}")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id.strip():
            fail(errors, f"Trigger case {index} id must be a non-empty string.")
        else:
            ids.append(case_id)
        category = case.get("category")
        split = case.get("split")
        categories[str(category)] += 1
        splits[str(split)] += 1
        if category not in TRIGGER_CATEGORY_COUNTS:
            fail(errors, f"Trigger case {case_id} has invalid category {category!r}.")
        if split not in TRIGGER_SPLIT_COUNTS:
            fail(errors, f"Trigger case {case_id} has invalid split {split!r}.")
        activation = case.get("expected_activation")
        intensity = case.get("expected_intensity")
        if not isinstance(activation, bool):
            fail(errors, f"Trigger case {case_id} activation must be boolean.")
        if intensity not in TRIGGER_INTENSITIES:
            fail(errors, f"Trigger case {case_id} has invalid intensity {intensity!r}.")
        if activation is False and intensity != "none":
            fail(errors, f"Inactive trigger case {case_id} must use intensity 'none'.")
        if activation is True and intensity == "none":
            fail(errors, f"Active trigger case {case_id} cannot use intensity 'none'.")
        for field in ("prompt", "rationale"):
            if not isinstance(case.get(field), str) or not case[field].strip():
                fail(errors, f"Trigger case {case_id} field {field} must be non-empty text.")
        signals = case.get("required_signals")
        if not isinstance(signals, list) or not signals or not all(
            isinstance(signal, str) and signal.strip() for signal in signals
        ):
            fail(errors, f"Trigger case {case_id} required_signals must be a non-empty string list.")
    duplicate_ids = [item for item, count in Counter(ids).items() if count > 1]
    if duplicate_ids:
        fail(errors, f"Duplicate trigger case IDs: {duplicate_ids}")
    if categories != Counter(TRIGGER_CATEGORY_COUNTS):
        fail(errors, f"Trigger category counts changed: {dict(categories)}")
    if splits != Counter(TRIGGER_SPLIT_COUNTS):
        fail(errors, f"Trigger split counts changed: {dict(splits)}")
    return len(cases), categories


def check_behavior_results(eval_dir: Path, errors: list[str]) -> tuple[int, int]:
    try:
        behavior = (eval_dir / "behavior-scenarios.md").read_text(encoding="utf-8")
        forward = (eval_dir / "forward-test-results.md").read_text(encoding="utf-8")
    except OSError as exc:
        fail(errors, f"Cannot read behavior evaluation files: {exc}")
        return 0, 0

    blocks = re.split(r"^### Scenario \d+[^\n]*$", behavior, flags=re.MULTILINE)[1:]
    assertion_counts = [
        len(re.findall(r"^\d+\. ", block, flags=re.MULTILINE)) for block in blocks
    ]
    if assertion_counts != BEHAVIOR_ASSERTION_COUNTS:
        fail(errors, f"Behavior assertion counts changed: {assertion_counts}")

    result_rows = re.findall(r"^\| [1-8]\.[^\n]+$", forward, flags=re.MULTILINE)
    if len(result_rows) != 8 or any("PASS" not in row for row in result_rows):
        fail(errors, "forward-test-results.md must retain eight passing scenario rows.")
    if "Total: **54/54 observable assertions passed**" not in forward:
        fail(errors, "forward-test-results.md must record the 54/54 assertion baseline.")
    if "do **not** prove implicit triggering" not in forward:
        fail(errors, "Forward-test results must retain the implicit-trigger limitation.")
    return len(blocks), sum(assertion_counts)


def main() -> int:
    args = parse_args()
    skill = args.skill.resolve()
    eval_dir = args.eval_dir.resolve()
    errors: list[str] = []

    if not skill.is_dir():
        print(f"ERROR: Skill directory does not exist: {skill}", file=sys.stderr)
        return 2
    if not eval_dir.is_dir():
        print(f"ERROR: Eval directory does not exist: {eval_dir}", file=sys.stderr)
        return 2
    repo_root = skill.parent.parent.parent
    try:
        eval_dir.relative_to(repo_root)
    except ValueError:
        fail(errors, "Eval directory must stay inside the repository root.")

    check_repository_boundaries(repo_root, skill, errors)
    actual_files = {
        str(path.relative_to(skill)).replace("\\", "/")
        for path in skill.rglob("*")
        if path.is_file()
    }
    unexpected = actual_files - EXPECTED_FILES
    missing = EXPECTED_FILES - actual_files
    if unexpected:
        fail(errors, f"Unexpected runtime files: {sorted(unexpected)}")
    if missing:
        fail(errors, f"Missing runtime files: {sorted(missing)}")
    html_files = [path for path in skill.rglob("*") if path.is_file() and path.suffix.lower() == ".html"]
    if html_files:
        fail(errors, f"Forbidden page files: {html_files}")

    skill_md = skill / "SKILL.md"
    metadata, skill_text = load_frontmatter(skill_md, errors)
    if set(metadata) != FRONTMATTER_KEYS:
        fail(errors, f"Frontmatter keys must be exactly {sorted(FRONTMATTER_KEYS)}; got {sorted(metadata)}")
    name = metadata.get("name")
    description = metadata.get("description")
    if name != skill.name:
        fail(errors, f"Skill name {name!r} must equal folder name {skill.name!r}.")
    if not isinstance(description, str) or not description.strip():
        fail(errors, "Description must be a non-empty string.")
        description = ""
    if len(description) > 1024:
        fail(errors, f"Description exceeds 1024 characters: {len(description)}")
    first_sentence = description.split(".", 1)[0].casefold()
    if "risky software" not in first_sentence or "clear, local, reversible" not in first_sentence:
        fail(errors, "Description must front-load both the risky-work use case and low-risk boundary.")
    if len(skill_text.splitlines()) >= 500:
        fail(errors, "SKILL.md must stay below 500 lines.")
    if len(re.findall(r"\S+", skill_text)) >= 5000:
        fail(errors, "SKILL.md must stay below 5,000 whitespace tokens.")

    combined_text = "\n".join(
        path.read_text(encoding="utf-8") for path in skill.rglob("*") if path.is_file()
    )
    if re.search(r"\bhtml\b", combined_text, flags=re.IGNORECASE):
        fail(errors, "Runtime Skill must not contain page-generation instructions or media references.")
    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(pattern, combined_text, flags=re.IGNORECASE):
            fail(errors, f"Placeholder pattern found: {pattern}")
    for pattern in PLATFORM_PATTERNS:
        if re.search(pattern, combined_text, flags=re.IGNORECASE):
            fail(errors, f"Platform-specific legacy found: {pattern}")
    for pattern in REMOVED_MECHANISMS:
        if re.search(pattern, combined_text, flags=re.IGNORECASE):
            fail(errors, f"Deleted mechanism leaked into runtime Skill: {pattern}")

    openai_path = skill / "agents/openai.yaml"
    try:
        openai = yaml.safe_load(openai_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        fail(errors, f"agents/openai.yaml is invalid: {exc}")
        openai = {}
    interface = openai.get("interface", {}) if isinstance(openai, dict) else {}
    expected_interface = {"display_name", "short_description", "default_prompt"}
    if set(interface) != expected_interface:
        fail(errors, f"openai.yaml interface keys must be {sorted(expected_interface)}")
    short_description = interface.get("short_description", "")
    if not 25 <= len(short_description) <= 64:
        fail(errors, "openai.yaml short_description must be 25-64 characters.")
    if f"${name}" not in interface.get("default_prompt", ""):
        fail(errors, "openai.yaml default_prompt must mention the Skill explicitly.")
    for line in openai_path.read_text(encoding="utf-8").splitlines():
        if ":" in line and line.strip() and not line.endswith(":"):
            _, value = line.split(":", 1)
            if value.strip() and not re.fullmatch(r'".*"', value.strip()):
                fail(errors, f"openai.yaml string value must be quoted: {line}")

    check_links(skill, errors)
    check_duplicate_paragraphs(skill, errors)
    trigger_count, categories = check_trigger_cases(eval_dir, errors)
    scenario_count, assertion_count = check_behavior_results(eval_dir, errors)

    if errors:
        print(f"FAIL: {len(errors)} issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS: repository Skill static checks")
    print(f"- runtime files: {len(actual_files)}")
    print(f"- SKILL.md lines: {len(skill_text.splitlines())}")
    print(f"- description characters: {len(description)}")
    print(f"- trigger cases: {trigger_count} {dict(categories)}")
    print(f"- behavior scenarios: {scenario_count}")
    print(f"- behavior assertions: {assertion_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
