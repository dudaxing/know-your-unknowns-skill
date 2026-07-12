#!/usr/bin/env python3
"""Native Cursor beforeShellExecution gate for codex-verify."""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    canonical_path,
    is_governance_path,
    log_bypass,
    marker_path,
    marker_schema,
    project_root,
    read_stdin_json,
    respond,
)

_DANGEROUS_ENV_RE = re.compile(
    r"(?<![A-Za-z0-9_./-])"
    r"(?:GIT_[A-Z0-9_]*|PAGER|MANPAGER|BROWSER|SSH_ASKPASS|"
    r"LESS|LESSOPEN|LESSCLOSE|LD_PRELOAD|LD_LIBRARY_PATH|LD_AUDIT|BASH_ENV)=",
    re.I,
)
_GENERAL_WRITE_RE = re.compile(
    r"""
    >>|(?<![>&])>(?!&)
    |(?<![A-Za-z0-9_.-])(?:tee|cp|mv|rm|dd|truncate|touch|mkdir|rmdir|ln|
      chmod|chown|install|patch|scp|sftp)(?![A-Za-z0-9_.-])
    |\bsed\s+[^|;&]*\s-i(?:\s|$)
    |\b(?:perl|ruby)\s+[^|;&]*-[A-Za-z]*i
    |\bnpm\s+(?:install|ci|update)\b
    |\b(?:yarn|pnpm)\s+(?:add|install)\b
    |\bpip(?:3)?\s+install\b
    |\btar\s+[^|;&]*[cxurA]
    |\b(?:curl|wget)\s+[^|;&]*(?:-o|-O|--output|--remote-name|--output-document)
    |(?<![A-Za-z0-9_.-])rsync(?![A-Za-z0-9_.-])
    |\b(?:open|write_text|write_bytes|writeFile)\s*\(
    |\.write\s*\(
    |\bshutil\.(?:copy|copyfile|copy2|move)\s*\(
    |\bos\.(?:rename|replace|remove|unlink|symlink)\s*\(
    |\bPath\s*\([^)]*\)\.(?:mkdir|touch|unlink|rename|write_text|write_bytes)\s*\(
    |\b(?:Set|Add|Clear)-Content\b
    |\bOut-File\b
    |\b(?:New|Remove|Move|Copy|Rename|Set)-Item\b
    |\[(?:System\.)?IO\.File\]::(?:WriteAllText|WriteAllBytes|AppendAllText)\b
    """,
    re.I | re.X,
)
_ARTIFACT_WRITE_RE = re.compile(
    r">>|(?<![>&])>(?!&)|\b(?:tee|rm|mv|cp|ln|truncate|dd|touch)\b|"
    r"\b(?:Set|Add|Clear)-Content\b|\bOut-File\b|"
    r"\b(?:Remove|Move|Copy|Rename|Set|New)-Item\b|"
    r"\b(?:write_text|write_bytes|writeFile|open)\s*\(",
    re.I,
)
_GIT_TOKEN_RE = re.compile(r"(?<![A-Za-z0-9_.-])git(?:\.exe)?(?=\s|$)", re.I)
_GIT_DANGEROUS_OPTION_RE = re.compile(
    r"(?:^|\s)(?:--output|--ext-diff|--external-diff|--textconv|--exec-path|"
    r"--open-files-in-pager|--git-dir|--work-tree|--namespace)(?:[=\s]|$)"
    r"|(?:^|\s)-O"
    r"|(?:^|\s)-C(?:\s|$)"
    r"|(?:^|\s)-c\s+[A-Za-z0-9_.-]+=",
    re.I,
)
_PATCH_FLAG_RE = re.compile(
    r"(?:^|\s)(?:-p|-u|--patch|--patch-with-stat|--cc|--unified|-U\d+)(?:\s|$)",
    re.I,
)
_SUMMARY_FLAG_RE = re.compile(
    r"(?:^|\s)(?:--stat|--numstat|--shortstat|--name-only|--name-status|"
    r"--dirstat|--summary|--compact-summary|--check|--raw)(?:\s|$)",
    re.I,
)
_SIMPLE_READ_GIT = {
    "status",
    "diff",
    "log",
    "show",
    "rev-parse",
    "ls-files",
    "ls-tree",
    "ls-remote",
    "cat-file",
    "describe",
    "blame",
    "shortlog",
    "for-each-ref",
    "name-rev",
    "merge-base",
    "rev-list",
    "show-ref",
    "var",
    "grep",
    "whatchanged",
    "check-ignore",
    "check-attr",
    "version",
    "help",
}
_PROTECTED_MIXED_RE = re.compile(
    r"(?:00-index|20-reviewer-prompt|30-review-report|40-human-notes|"
    r"80-human-decision)\.md|[/\\]_templates[/\\]",
    re.I,
)


def extract_command(payload: dict) -> str:
    command = payload.get("command")
    if isinstance(command, str) and command.strip():
        return command
    tool_input = payload.get("tool_input") or {}
    if isinstance(tool_input, str):
        try:
            parsed = json.loads(tool_input)
            tool_input = parsed if isinstance(parsed, dict) else {}
        except json.JSONDecodeError:
            tool_input = {}
    if isinstance(tool_input, dict):
        command = tool_input.get("command")
        if isinstance(command, str):
            return command.strip()
    return ""


def strip_benign_redirects(command: str) -> str:
    command = re.sub(r"\d*>\s*&\s*\d+", "", command)
    command = re.sub(r"\d*>{1,2}\s*(?:/dev/null|\$null|NUL)\b", "", command, flags=re.I)
    return command


def strong_normalize(command: str) -> str:
    return re.sub(r"""[\\$'"]""", "", command)


def git_is_mutating(command: str) -> bool:
    normalized = strong_normalize(command)
    if not _GIT_TOKEN_RE.search(normalized):
        return False
    if _GIT_DANGEROUS_OPTION_RE.search(normalized):
        return True

    for segment in re.split(r"(?:&&|\|\||[;&|\n])", normalized):
        matches = list(_GIT_TOKEN_RE.finditer(segment))
        for match in matches:
            tail = segment[match.end() :].strip()
            tokens = tail.split()
            if not tokens:
                return True
            while tokens and tokens[0].startswith("-"):
                tokens.pop(0)
            if not tokens:
                return True
            subcommand = tokens[0].lower()
            arguments = [token.lower() for token in tokens[1:]]

            if subcommand in {"diff", "show", "whatchanged"}:
                summary_only = bool(_SUMMARY_FLAG_RE.search(tail)) and not _PATCH_FLAG_RE.search(tail)
                if not summary_only and not (
                    "--no-ext-diff" in arguments and "--no-textconv" in arguments
                ):
                    return True
            if subcommand in {"log", "rev-list"} and _PATCH_FLAG_RE.search(tail):
                if not (
                    "--no-ext-diff" in arguments and "--no-textconv" in arguments
                ):
                    return True

            if subcommand in _SIMPLE_READ_GIT:
                continue
            if subcommand == "remote" and arguments and arguments[0] in {
                "-v",
                "show",
                "get-url",
            }:
                continue
            if subcommand == "branch" and arguments and arguments[0] in {
                "--show-current",
                "-v",
                "--list",
                "-a",
                "-r",
                "--contains",
            }:
                continue
            if subcommand == "config" and arguments and arguments[0] in {
                "--get",
                "--list",
                "-l",
            }:
                continue
            return True
    return False


def has_write(command: str) -> bool:
    if "$'" in command or '$"' in command:
        return True
    normalized = strong_normalize(command)
    if "=" in command and _DANGEROUS_ENV_RE.search(normalized):
        return True
    return bool(_GENERAL_WRITE_RE.search(command)) or git_is_mutating(command)


def explicit_governance_write(command: str, project: Path) -> bool:
    if not _ARTIFACT_WRITE_RE.search(command):
        return False
    lowered = command.replace("\\", "/").lower()
    if (
        "plan-approved" in lowered
        or "ledger.jsonl" in lowered
        or ".codex-verify/" in lowered and ".state" in lowered
        or _PROTECTED_MIXED_RE.search(command)
    ):
        return True

    # Resolve straightforward redirection and PowerShell -Path targets, including
    # symlink aliases. Dynamic string construction remains an acknowledged limit.
    target_patterns = (
        r">>{0,1}\s*['\"]?([^'\"\s<>|;&]+)",
        r"\b(?:tee|Set-Content|Add-Content|Out-File)\b(?:\s+-\w+)*\s+['\"]?([^'\"\s<>|;&]+)",
    )
    for pattern in target_patterns:
        for raw in re.findall(pattern, command, flags=re.I):
            if is_governance_path(canonical_path(raw, project), project):
                return True
    return False


def deny(message: str) -> int:
    respond("deny", f"[Shell 闸门] {message}")
    return 0


def main() -> int:
    payload, _ = read_stdin_json()
    if payload is None:
        # Avoid infrastructure-caused workspace lockout.
        respond("allow")
        return 0

    command = extract_command(payload)
    if not command:
        respond("allow")
        return 0
    project = project_root(payload)
    stripped = strip_benign_redirects(command)

    normalized = strong_normalize(command)
    if re.search(r"\bmixed\.sh\b", normalized, re.I) and re.search(
        r"\b(?:review|next|decide|import-review|import-decision)\b", normalized, re.I
    ):
        return deny("mixed.sh 的 review/decide/next/import-* 是人类或审查者专属命令。")
    if re.search(r"\b(?:import-review|import-decision|decide)\b", normalized, re.I):
        return deny("检测到 mixed-review 人类/审查者专属命令。")
    if re.search(
        r"CODEX_SANDBOX=\S*(?:workspace-write|danger|full-access|write)",
        normalized,
        re.I,
    ):
        return deny("CODEX_SANDBOX 非只读会破坏审查者只读保证。")
    if explicit_governance_write(stripped, project):
        return deny("命令试图写入闸门标记、ledger、状态或 mixed-review 受保护文件。")

    if os.environ.get("PLAN_GATE", "on").lower() == "off":
        if not marker_path(project).is_file():
            log_bypass(project, "shell-gate")
        respond("allow")
        return 0

    if has_write(stripped):
        marker_valid, _, _ = marker_schema(marker_path(project))
        if marker_valid:
            return deny(
                "计划已过审，但文件写入仍须使用 Write/编辑工具，由计划闸门校验目标路径；"
                "Shell 仅用于读取、测试和构建。"
            )
        return deny(
            "计划未过审，检测到疑似写操作。请先完成计划校验；"
            "计划草稿可用 Write 写入 .codex-verify/plans/。"
        )

    respond("allow")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
