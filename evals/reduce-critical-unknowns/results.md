# Validation baseline

Baseline date: 2026-07-12.

## Reproduce

From the repository root:

```bash
python -m pip install PyYAML==6.0.3
python evals/reduce-critical-unknowns/run_static_checks.py
```

Also run the `quick_validate.py` bundled with the current Codex `$skill-creator` against `.agents/skills/reduce-critical-unknowns`.

## Recorded results

| Check | Result |
|---|---|
| Codex `$skill-creator` initializer | PASS; created the Skill, `agents/openai.yaml`, and two references without example placeholders. |
| Codex `$skill-creator` quick validator | PASS in UTF-8 mode: `Skill is valid!`. |
| Repository static checker | PASS; four runtime files, 140-line `SKILL.md`, 773-character description, 25 trigger cases, 8 behavior scenarios, and 54 assertions. |
| CI dependency parity | PASS in a clean temporary venv with PyYAML 6.0.3, the version pinned by the workflow. |
| Checker syntax | PASS via Python `compile(...)`. |
| Checker failure path | PASS; a missing Skill directory produced an actionable error and exit code 2. |
| Legacy-artifact regression guard | PASS; an injected page file was rejected with exit code 1, then removed. |
| Forward-test baseline guard | PASS; a temporary 53/54 result was rejected with exit code 1, then restored. |
| Folder, frontmatter, YAML, links | PASS. |
| Placeholder, platform residue, deleted mechanisms, duplicate paragraphs | PASS. |
| Runtime artifact boundary | PASS; no page file, README, eval, script, asset, or package inside the Skill. |
| Explicit behavior forward-tests | PASS; 54/54 assertions across 8 independent worker scenarios. |

See [forward-test-results.md](forward-test-results.md) for per-scenario evidence.

## Trigger corpus

`trigger-cases.json` contains 25 labeled prompts with a fixed 15/10 train/validation split:

- 8 positive;
- 4 explicit technique requests;
- 2 “implement immediately” cases;
- 6 near negatives sharing risky keywords;
- 5 clear negatives.

The static checker validates corpus structure and expected labels. It does not claim a measured model trigger rate.

## Not yet measured

- Real clean-session implicit trigger rate: the original test surface did not expose a Skill-load trace.
- Real repository with/without-Skill comparison of rework, elapsed time, and token cost.
- Multi-week cross-session persistence behavior.

The absence of those measurements is intentional and should not be presented as a passing result.
