# Plan: Fix Sol P1/P2 (r11 — close r10 P0s)

## Goal
Implement six Sol findings. Handoff option-2. Delivery must say **行为未实测** unless user pastes new-chat transcript.

## r10 P0 → r11

| # | Fix |
|---|-----|
| A | **No `tee`.** Shell only runs read/build/`verify.sh` with **no** `>`/`tee`. Capture = agent Reads terminal output → **Write** `.codex-verify/plans/final-review-capture.txt`. |
| B | Pass iff capture has harness line `总评 PASS` for this task **and** no `总评 FAIL`/`总评 ESCALATE`/`未能从输出解析` for it. **Do not** trust model `VERDICT: PASS` alone (harness may internally reclassify). Optionally confirm last `ledger.jsonl` review event is PASS if present. |
| C | Final adversarial review = `verify.sh custom` with Write-built prompt containing **only** diffs for `know-your-unknowns/**`, `README.md`, `README.zh.md` (and `dist/` note). No `.cursor`/`.claude` hooks. |
| D | README asserts: both READMEs must contain `.cursor/skills`, `.agents/skills`, and compat `.claude/skills` (exact substrings). |
| E | Non-intended skill files: post SHA-256 == pre. Intended files: preserve all lines **added** in pre vs HEAD (difflib insert/replace new sides). |
| F | Smoke = full line messages + preconditions + exact map hashes. |
| G | Any **rejected** Correction batch voids confirm for that artifact. Duplicate meta lines → reject whole batch. |
| H | Strict Go lines + Plan-Version canonical (no self-hash). Strict UUID regex. |

## Marker
```bash
export VERIFY_HOST=cursor VERIFY_BACKEND=codex CODEX_MODEL=gpt-5.6-sol
export VERIFY_TASK_ID=know-your-unknowns-fix-sol-p1-r11
export VERIFY_ALLOWED_PATHS="know-your-unknowns/,README.md,README.zh.md,dist/,.cursor/skills/know-your-unknowns/"
bash "$HOME/.claude/skills/codex-verify/scripts/verify.sh" plan < .codex-verify/plans/fix-sol-p1-p2.md
```

## Persist rule
Read-only Shell → agent **Write/StrReplace** under `.codex-verify/plans/`. Never shell redirect/`tee`/`cp` into the repo.

## Intended edit set (only these may change under allowlist)
```
know-your-unknowns/SKILL.md
know-your-unknowns/references/merge-quiz.md
know-your-unknowns/references/reference-port.md
know-your-unknowns/references/artifact-patterns.md
know-your-unknowns/references/tweakable-plan.md
know-your-unknowns/evals/smoke-triggers.md
README.md
README.zh.md
dist/know-your-unknowns.skill   # via package_skill only
.cursor/skills/know-your-unknowns/**  # optional test install via Write only
```
All other files under `know-your-unknowns/`: **post SHA-256 == pre SHA-256**.

## Findings 1–6 done-when
1. merge-quiz + artifact-patterns + SKILL + smoke: `Artifact-ID` + `Qn: letter`; ignore `Quiz score:`; UUID artifact
2. reference-port + patterns + SKILL + smoke: Correction + Map-Version confirm; void rules
3. tweakable-plan: `VERIFY_ALLOWED_PATHS` + stdin; Edit/Write after PASS only
4. tweakable-plan: Git Bash `plan < file`; PS5.1 bash-internal `<`; Python `shutil.which("bash")` + binary stdin; no WSL; no hardcoded bash path; warn against PS pipe
5. SKILL §8 + both READMEs: native vs compat paths; one install; new chat; substring asserts
6. SKILL hard-stop: reference-port needs confirm; tweakable needs Plan go; continue phrases

## IDs
- UUID (lowercase compare): `^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$`
- `artifact_id` = new UUID each generation; `content_version` = sha256(LF-normalized body with `data-artifact-id` / `Artifact-ID` lines stripped)
- Map canonical = sorted `id\ttext\n` UTF-8 LF; `map_version` = sha256 hex
- Plan canonical payload = plan markdown with LF newlines, strip lines `^Plan-ID:` / `^Plan-Version:` and attributes `data-plan-id` / `data-plan-version`; `Plan-Version: sha256:<hex>` of that payload

## Whitelist (batch = one user message; whitelist-only fences unioned)

Exact line forms:
- `Artifact-ID: <uuid>`
- `Map-Version: sha256:<64 lowercase hex>`
- `Plan-ID: <uuid>`
- `Plan-Version: sha256:<64 lowercase hex>`
- `semantics confirmed`
- `Correction: <rowId> -> <nonempty text>` (first ` -> `)
- `Session: continue here`
- `Q<n>: <A-D>` or `Q<n>: (unanswered)` (`n` = `[1-9][0-9]*`)
- Go (only): `Plan: go` or `Go: approve` (exact)

**Duplicate meta:** >1 of Artifact-ID / Map-Version / Plan-ID / Plan-Version / confirm / Session in one batch → reject entire batch.

**Prefix fail-closed:** `^Q\d`, `^Correction\b`, `^Artifact-ID\b`, `^Map-Version\b`, `^Plan-ID\b`, `^Plan-Version\b`, `^Go\b`, `^Plan:` failing grammar → reject that kind (for `Plan:` only `Plan: go` is valid; other `Plan:` → reject go-kind).

**Sole continue message** (entire trimmed body): `Session: continue here` | `continue here` | `continue in this session`

## Transitions
Order: validate single Artifact-ID/Plan-ID as required → Corrections → confirm → Q → Session/go.

**Correction reject → void confirm** for that map artifact whenever batch is rejected for: conflict, empty text, unknown id, malformed, duplicate meta, wrong Artifact-ID. Accepted map-changing Correction voids old confirm unless same message successfully confirms new Map-Version. Idempotent Correction keeps confirm.

**Quiz:** require Artifact-ID = current quiz UUID. LWW; unanswered clears; bad Q#/letter/malformed → reject all Q lines in message. Unlock on key match. Ignore `Quiz score:`.

**Continue:** reference-port: valid confirm for (artifact_id,map_version) + same-batch Session or later sole-continue. tweakable-plan: valid `Plan: go`/`Go: approve` bound to (Plan-ID,Plan-Version) + Session/sole-continue; no semantics confirm required.

## Smoke (full messages)

Map fixture rows `row_a`/`row_b` texts `TA`/`TB`:
- initial map_version = `fcd27a6531cc6f492e7973c9b5be17e333c2044dea7504e24069917f9c805e5d`
- after `row_a -> NEW` = `e8def2e7ec4dbf52a9a4b6a36bba8d26de2d9cc275b6023b65eff6e4a2bff463`

Quiz UUID `11111111-1111-1111-1111-111111111111`; map UUID `22222222-2222-2222-2222-222222222222`; Q1–Q5 key B,A,C,D,B.

| ID | Prestate | Message lines | Expect |
|----|----------|---------------|--------|
| S1 | empty quiz | Artifact-ID quiz; Q1:B Q2:A Q3:C Q4:D Q5:B | unlock |
| S2 | map TA/TB unconfirmed | Artifact-ID map; Correction: row_a -> NEW; Map-Version: sha256:e8def2e7…f463; semantics confirmed | confirmed at new version |
| S3 | after S2 | sole `continue here` | same-session OK |
| S4 | empty | `Quiz score: 5/5` | no unlock |
| S5 | empty | Artifact-ID quiz; Q99:A | reject Q lines; no unlock |
| S6 | map confirmed at initial version | Artifact-ID map; Correction: row_a -> X; Correction: row_a -> Y | reject Corrections; **confirm void** |
| S7 | map confirmed | Artifact-ID map; `Correction: row_a ->` | reject; **confirm void** |
| S8 | empty | prose containing words semantics confirmed | not confirmed |
| S9 | Q1:A stored | Artifact-ID quiz; Q1:B | stored B |
| S10 | Q1:B stored | Artifact-ID quiz; Q1:(unanswered) | Q1 cleared |
| S11 | confirmed | Artifact-ID map; Correction: row_a -> NEW2 (no confirm) | confirm void |
| S12 | current quiz UUID | Artifact-ID other-uuid; Q1:B | reject batch |
| S13 | answers for old quiz UUID | new quiz UUID minted; old Q lines resent with old id | ignored/reject; no unlock on new |
| S14 | plan v1 | Plan: go without Plan-ID/Version | go invalid |
| S15 | empty | Artifact-ID quiz; `Q1 B` | reject Q lines |

## WIP containment script (Write to `.codex-verify/plans/check-wip-containment.py`)
- Load `sha-pre-p1.txt`; for every `know-your-unknowns/**` file not in intended set, compare SHA-256 of working bytes (open rb) to pre → must match.
- For each intended tracked file: `head=git show HEAD:path` (empty if missing); `pre=snapshot bytes`; `post=current bytes`. Using difflib.SequenceMatcher on splitlines(keepends=False): every line appearing on the **b** side of insert/replace opcodes from head→pre must appear as a line in post (multiset: counts preserved). Fail listing missing lines.
- Snapshots: Read+Write to `plans/snapshots/` before edits; sha-pre via same Read+hash written to `sha-pre-p1.txt`.

## README asserts
After edits, both `README.md` and `README.zh.md` contain all of: `.cursor/skills`, `.agents/skills`, `.claude/skills`.

## Pack
Write `.codex-verify/plans/verify-pack.py` (cwd=repo root):
```python
import hashlib, zipfile, sys
from pathlib import Path
root = Path.cwd()
skill, zpath = root / "know-your-unknowns", root / "dist" / "know-your-unknowns.skill"
def junk(p: Path) -> bool:
    return any(x in {"__pycache__", ".git"} for x in p.parts) or (
        p.is_file() and (p.name in {".DS_Store", "Thumbs.db"} or p.name.endswith("~")
                         or p.suffix in {".pyc", ".pyo", ".swp"}))
if any(junk(p) for p in skill.rglob("*")):
    sys.exit("junk present")
files = [p for p in skill.rglob("*") if p.is_file()]
with zipfile.ZipFile(zpath) as z:
    names = z.namelist()
    assert len(names) == len(set(names))
    exp = {"know-your-unknowns/" + p.relative_to(skill).as_posix() for p in files}
    assert set(names) == exp
    for p in files:
        n = "know-your-unknowns/" + p.relative_to(skill).as_posix()
        data = z.read(n)
        assert (zipfile.crc32(data) & 0xffffffff) == z.getinfo(n).CRC
        assert hashlib.sha256(data).digest() == hashlib.sha256(p.read_bytes()).digest()
print("pack ok", len(files))
```
`PYTHONUTF8=1 python "$HOME/.claude/skills/skill-creator/scripts/package_skill.py" know-your-unknowns dist` then `python .codex-verify/plans/verify-pack.py`.

## Final review (no tee)
1. Preflight in **Git Bash**: `bash -lc 'codex --version'` (not Windows PowerShell shim). Model auth probed by the review itself; unavailable → stop.
2. Read-only: `git diff HEAD -- know-your-unknowns README.md README.zh.md` (+ untracked under those prefixes via `git ls-files -o --exclude-standard` filtered). Agent **Write** `.codex-verify/plans/final-review-prompt.md` wrapping that diff in adversarial review instructions (same spirit as verify review prompt; require `VERDICT:` line).
3. Shell (no redirect):  
   `export VERIFY_TASK_ID=know-your-unknowns-skill-review-after-p1 VERIFY_HOST=cursor VERIFY_BACKEND=codex CODEX_MODEL=gpt-5.6-sol`  
   `bash "$HOME/.claude/skills/codex-verify/scripts/verify.sh" custom < .codex-verify/plans/final-review-prompt.md`
4. Agent Write terminal/stdout text → `plans/final-review-capture.txt`.
5. **Pass only if** capture matches harness success for that task (`总评 PASS`) and lacks harness fail/escalate/unknown-parse for it. Stop otherwise.

## Notes
Out of scope: patching verify.sh; push; WSL; exclude file; global skill overwrite without human OK.
