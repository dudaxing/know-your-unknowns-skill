# Explicit forward-test results

Run date: 2026-07-12. Eight independent worker turns received only the Skill path and one raw scenario. They were told to return actions without modifying files. Assertions were not included in worker prompts. The main thread graded outputs afterward.

These runs validate behavior after explicit invocation. They do **not** prove implicit triggering.

| Scenario | Worker | Result | Assertion result | Concrete evidence from output |
|---|---|---|---:|---|
| 1. Legacy auth sessions | `forward_auth` | PASS | 8/8 | Traced create/read/refresh/revoke/logout, separated authorization, proposed a 3-version compatibility matrix, staged flag rollout and rollback, and paused only new writes/destructive branches. |
| 2. Rust→TypeScript retry | `forward_port` | PASS | 9/9 | Mapped monotonic time, inclusive jitter, runtime error discrimination, cancellation races, shared budget and atomic transition; proposed differential ordered traces and preserve/change/drop. |
| 3. Ambiguous export | `forward_export` | PASS | 7/7 | Refused repository claims, proposed a focused existing-flow scan, then offered self-service/archive, compliance, and report outcomes with different permission/architecture costs. |
| 4. Implementation deviation | `forward_deviation` | PASS | 6/6 | Reused the local null-mapping utility with a regression test, documented premise/evidence/impact/action, and held only the authorization-facing key contract. |
| 5. Large risky diff | `forward_diff` | PASS | 8/8 | Rejected unit tests as sufficient; required behavior map, migration restart, retry fault injection, flag-off/rollback evidence, observability, and independent reconstruction. |
| 6. Simple rename | `forward_simple` | PASS | 6/6 | Explicitly classified the change as local/reversible and used only inspect→rename→diff→focused-test, with no questions or process artifacts. |
| 7. No repository access | `forward_no_repo` | PASS after retry | 5/5 | Said no cause was discovered, separated four hypotheses, proposed one end-to-end incident trace, and made each implementation branch conditional. |
| 8. Unarticulated preference | `forward_preference` | PASS | 5/5 | Showed the same fictional error as readable Markdown, versioned JSON, or a diagnostic bundle, with implementation consequences and one-letter reply. |

Total: **54/54 observable assertions passed** on the successful outputs.

Infrastructure note: the first Scenario 7 worker attempt failed before producing output because its response stream disconnected. The same prompt was retried successfully. This was recorded as an execution-infrastructure failure, not silently counted as a behavioral failure or pass.

Observed improvement opportunity: Scenario 3 appropriately delayed implementation because neither repository evidence nor a product contract was present, but its answer was longer than needed. No high-priority behavior defect was found; future real usage should watch whether ambiguous-feature probes remain concise after repository evidence is available.

## Implicit-like samples

Two additional fresh workers received tasks without the Skill name or path:

- High-risk schema migration: the response used an expand–migrate–contract path, prioritized a consumer compatibility probe, allowed discovery/observability/dry-run work, and paused backfill/source-of-truth switch/deletion. Behavior matched the positive expectation.
- Authentication-guide typo: the response stayed to the exact spelling replacement and did not start an uncertainty workflow. Behavior matched the near-negative expectation.

These samples show that fresh-agent behavior was compatible with the intended routing. The collaboration surface did not expose whether either worker actually loaded `SKILL.md`, so they are **not counted as real implicit-trigger passes**.
