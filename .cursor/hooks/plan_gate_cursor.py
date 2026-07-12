#!/usr/bin/env python3
"""Native Cursor preToolUse plan gate for codex-verify."""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    allowed_roots,
    canonical_path,
    has_parent_traversal,
    is_governance_path,
    is_protocol_path,
    is_within,
    log_bypass,
    marker_path,
    marker_schema,
    project_root,
    protocol_root_symlink,
    read_stdin_json,
    respond,
)

_PATH_KEYS = ("file_path", "path", "notebook_path", "target_notebook")
_PATCH_PATH_RE = re.compile(r"^\*\*\* (?:Add|Update|Delete) File:\s*(.+?)\s*$", re.M)


def extract_file_paths(payload: dict) -> list[str]:
    tool_input = payload.get("tool_input") or {}
    raw_text = ""
    if isinstance(tool_input, str):
        raw_text = tool_input
        try:
            parsed = json.loads(tool_input)
            tool_input = parsed if isinstance(parsed, dict) else {}
        except json.JSONDecodeError:
            tool_input = {}
    if not isinstance(tool_input, dict):
        tool_input = {}

    paths: list[str] = []
    for source in (tool_input, payload):
        for key in _PATH_KEYS:
            value = source.get(key)
            if isinstance(value, str) and value.strip():
                paths.append(value.strip())
        values = source.get("file_paths")
        if isinstance(values, list):
            paths.extend(str(value).strip() for value in values if str(value).strip())

    patch = tool_input.get("patch") or payload.get("patch") or raw_text
    if isinstance(patch, str):
        paths.extend(match.strip() for match in _PATCH_PATH_RE.findall(patch))

    return list(dict.fromkeys(paths))


def deny(message: str) -> int:
    respond("deny", f"[计划闸门] {message}")
    return 0


def main() -> int:
    payload, _ = read_stdin_json()
    # Infrastructure/encoding failures fail open to avoid another permanent
    # workspace lockout. Valid policy violations still deny deterministically.
    if payload is None:
        respond("allow")
        return 0

    project = project_root(payload)
    raw_paths = extract_file_paths(payload)
    if not raw_paths:
        return deny("无法识别写入目标路径；为避免绕过项目边界，已拒绝本次写操作。")

    source_targets: list[Path] = []
    protocol_symlink = protocol_root_symlink(project)

    for raw in raw_paths:
        if has_parent_traversal(raw):
            return deny(f"目标路径包含 ..，拒绝解析歧义路径：{raw}")
        target = canonical_path(raw, project)

        raw_lower = raw.replace("\\", "/").lower()
        if (
            "plan-approved" in raw_lower
            or "ledger.jsonl" in raw_lower
            or is_governance_path(target, project)
        ):
            return deny(f"禁止直接写治理工件：{raw}。这些文件仅由校验 harness 维护。")

        if is_protocol_path(target, project):
            if protocol_symlink:
                return deny(
                    f"协议目录 {protocol_symlink} 是 symlink，拒绝通过协议目录写入。"
                )
            continue
        source_targets.append(target)

    # All targets are legitimate protocol files (plans/sessions/artifacts).
    if not source_targets:
        respond("allow")
        return 0

    if os.environ.get("PLAN_GATE", "on").lower() == "off":
        if not marker_path(project).is_file():
            log_bypass(project, "plan-gate")
        respond("allow")
        return 0

    marker = marker_path(project)
    valid, fields, reason = marker_schema(marker)
    if not valid:
        return deny(
            f"拒绝文件修改：{reason}（{marker}）。"
            "请先形成计划并运行 verify.sh plan；总评 PASS 后自动放行。"
        )

    roots = allowed_roots(fields, project)
    for target in source_targets:
        if not is_within(target, project):
            return deny(f"目标位于项目根之外：{target}")
        if roots is not None and not any(is_within(target, root) for root in roots):
            return deny(f"目标不在过审计划声明的 allowed 路径内：{target}")

    respond("allow")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
