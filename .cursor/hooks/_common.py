"""Shared native-Python helpers for Cursor codex-verify gates."""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

DEBUG_LOG = (
    Path(os.environ.get("TEMP", os.environ.get("TMP", ".")))
    / "codex-verify-cursor-hook-debug.txt"
)

_TASK_RE = re.compile(r"^[A-Za-z0-9._-]+$")
_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_PROTECTED_MIXED = {
    "00-index.md",
    "20-reviewer-prompt.md",
    "30-review-report.md",
    "40-human-notes.md",
    "80-human-decision.md",
}


def read_stdin_json() -> tuple[dict | None, str]:
    """Decode Cursor stdin across Windows encodings without false lockouts."""
    raw = sys.stdin.buffer.read()
    if not raw:
        return {}, ""

    errors: list[str] = []
    # PowerShell 5 may pipe UTF-16-LE without a BOM. A UTF-8 decode can still
    # "succeed" because NUL is valid UTF-8, so parse each decoded candidate.
    for encoding in ("utf-8-sig", "utf-16", "utf-16-le", "utf-16-be", "mbcs"):
        try:
            text = raw.decode(encoding).strip().lstrip("\ufeff")
        except (UnicodeDecodeError, LookupError) as exc:
            errors.append(f"{encoding}: {exc}")
            continue
        if not text:
            return {}, ""
        payload = _parse_json_object(text)
        if payload is not None:
            return payload, ""
        errors.append(f"{encoding}: not a JSON object")

    detail = "; ".join(errors)
    _write_debug(raw, detail)
    return None, detail


def _parse_json_object(text: str) -> dict | None:
    candidates = [text]
    start, end = text.find("{"), text.rfind("}")
    if start >= 0 and end > start and (start != 0 or end != len(text) - 1):
        candidates.append(text[start : end + 1])
    for candidate in candidates:
        try:
            value = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    return None


def _write_debug(raw: bytes, detail: str) -> None:
    try:
        DEBUG_LOG.write_text(
            f"detail={detail}\nlen={len(raw)}\nhex_head={raw[:96].hex()}\n",
            encoding="utf-8",
        )
    except OSError:
        pass


def respond(permission: str, message: str = "") -> None:
    result: dict[str, str] = {"permission": permission}
    if message:
        result["user_message"] = message
        result["agent_message"] = message
    # ASCII-only stdout avoids Windows console-codepage corruption.
    print(json.dumps(result, ensure_ascii=True), flush=True)


def project_root(payload: dict) -> Path:
    cwd = payload.get("cwd")
    if isinstance(cwd, str) and cwd.strip():
        return Path(cwd).resolve(strict=False)
    return Path.cwd().resolve(strict=False)


def canonical_path(raw: str, project: Path) -> Path:
    path = Path(raw.replace("/", os.sep).replace("\\", os.sep))
    if not path.is_absolute():
        path = project / path
    return path.resolve(strict=False)


def is_within(path: Path, root: Path) -> bool:
    try:
        return os.path.commonpath(
            [os.path.normcase(str(path)), os.path.normcase(str(root))]
        ) == os.path.normcase(str(root))
    except ValueError:
        return False


def has_parent_traversal(raw: str) -> bool:
    return ".." in re.split(r"[/\\]+", raw)


def state_dir() -> Path:
    configured = os.environ.get("VERIFY_STATE_DIR")
    if configured:
        return Path(configured).expanduser().resolve(strict=False)
    xdg = os.environ.get("XDG_STATE_HOME")
    root = Path(xdg).expanduser() if xdg else Path.home() / ".local" / "state"
    return (root / "codex-verify").resolve(strict=False)


def ledger_path() -> Path:
    configured = os.environ.get("VERIFY_LEDGER")
    if configured:
        return Path(configured).expanduser().resolve(strict=False)
    return state_dir() / "ledger.jsonl"


def marker_path(project: Path) -> Path:
    configured = os.environ.get("PLAN_GATE_FILE", ".codex-verify/plan-approved")
    return canonical_path(configured, project)


def is_governance_path(path: Path, project: Path) -> bool:
    if path == marker_path(project) or path == ledger_path() or is_within(path, state_dir()):
        return True
    codex_root = project / ".codex-verify"
    if path.parent == codex_root and path.suffix == ".state":
        return True
    try:
        relative = path.relative_to(codex_root / "sessions")
    except ValueError:
        return False
    parts = relative.parts
    return (
        path.name in _PROTECTED_MIXED
        or "_templates" in parts
    )


def protocol_root_symlink(project: Path) -> str | None:
    for relative in (
        ".codex-verify",
        ".codex-verify/plans",
        ".codex-verify/sessions",
        ".codex-verify/artifacts",
    ):
        candidate = project / relative
        if candidate.is_symlink():
            return relative
    return None


def is_protocol_path(path: Path, project: Path) -> bool:
    return any(
        is_within(path, project / ".codex-verify" / directory)
        for directory in ("plans", "sessions", "artifacts")
    )


def marker_schema(marker: Path) -> tuple[bool, dict[str, list[str]], str]:
    if not marker.is_file():
        return False, {}, "未找到过审标记"
    try:
        lines = marker.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        return False, {}, f"无法读取过审标记：{exc}"

    fields: dict[str, list[str]] = {}
    for line in lines:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields.setdefault(key.strip(), []).append(value.strip())

    def one(key: str) -> str:
        values = fields.get(key, [])
        return values[0] if values else ""

    if not _TASK_RE.fullmatch(one("task")):
        return False, fields, "task 缺失或格式非法"
    if not _HASH_RE.fullmatch(one("plan_hash")):
        return False, fields, "plan_hash 缺失或格式非法"
    if one("verdict") != "PASS":
        return False, fields, "verdict 不是 PASS"
    if one("backend") not in {"codex", "glm"}:
        return False, fields, "backend 必须是 codex 或 glm"
    if not one("approved_at") or not one("approved_at")[0].isdigit():
        return False, fields, "approved_at 缺失或格式非法"
    try:
        expires = int(one("expires_epoch"))
    except ValueError:
        return False, fields, "expires_epoch 缺失或格式非法"
    if int(time.time()) > expires:
        return False, fields, "过审标记已过期"
    return True, fields, ""


def allowed_roots(fields: dict[str, list[str]], project: Path) -> list[Path] | None:
    values = fields.get("allowed")
    if values is None:
        return None
    roots: list[Path] = []
    for raw in values:
        if not raw or has_parent_traversal(raw) or Path(raw).is_absolute():
            continue
        root = canonical_path(raw, project)
        if is_within(root, project):
            roots.append(root)
    return roots


def log_bypass(project: Path, task: str) -> None:
    ledger = ledger_path()
    try:
        ledger.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "event": "gate_bypass",
            "mode": "cursor-hook",
            "task": task,
            "cwd": str(project),
            "backend": "none",
            "degraded": False,
            "degrade_reason": "",
            "round": 0,
            "verdict": "",
            "overrides": "plan_gate_off",
            "note": "operation allowed without approved plan",
        }
        with ledger.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError:
        pass
