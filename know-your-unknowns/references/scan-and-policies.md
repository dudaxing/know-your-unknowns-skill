# Cross-Cutting: The Unknowns Scan and Operating Policies

These apply across all techniques — and they are the *default* behavior when no specific technique is triggered.

## The unknowns scan (default for any non-trivial task)

When a task is non-trivial but no full technique is warranted, run a compact scan before planning or coding. Chat/markdown, not an artifact:

```markdown
## Unknowns scan
- Goal (restated in implementation terms):
- Known knowns:
- Known unknowns:
- Likely unknown knowns:
- Likely unknown unknowns:
- Evidence inspected so far:
- Recommended next move: (implement / prototype / interview / blindspot pass / investigate)
- Suggested trigger phrase: (one copy-paste sentence to run the recommended technique — English; add 中文 when helpful. If next move is **implement**, write `n/a — proceed after logging assumptions` instead of a fake trigger.)
```

Example trigger phrases by recommended move:

| Recommended next move | Suggested trigger phrase (EN) | 中文示例 |
|----------------------|-------------------------------|----------|
| blindspot pass | `Do a blindspot pass on [module] before we implement [task].` | `在实现 [任务] 之前，对 [模块] 做一次盲区扫描。` |
| interview | `Interview me one question at a time about [feature]; prioritize architecture-changing answers.` | `就 [功能] 访谈我，一次一题，优先问会改变架构的问题。` |
| prototype / design directions | `Make an HTML page with 4 wildly different design directions for [screen] so I can react.` | `给 [界面] 出 4 个差异很大的设计方向 HTML，让我反应式选择。` |
| tweakable plan | `Write a tweakable implementation plan in HTML — decisions I'm likely to change first.` | `写一份可调实现计划 HTML，把最可能改的决策放在前面。` |
| investigate | `Investigate [area] in the territory and report findings before we decide the next technique.` | `先调查疆域里的 [区域] 并汇报，再决定下一招。` |
| implement | `n/a — proceed after logging assumptions` | `无需触发句 — 记录假设后直接实现` |

For tiny safe edits, skip even this: log any assumption and proceed.

Watch for **over-specific prompts** ("just copy this file", "just add a field", "just wire this endpoint") — they can encode a wrong assumption. Verify the premise against the territory before executing it literally.

## Territory inspection checklist

When scanning a codebase, check:

- Entry points, call paths, shared utilities, and existing patterns.
- Tests, fixtures, contract suites, and generated clients.
- Schemas, migrations, data backfills, legacy/null data, compatibility constraints.
- Feature flags, environment differences (dev/staging/prod splits), rollout state.
- Auth, permissions, audit logging, rate limits, privacy, billing, abuse boundaries.
- Prior PRs, reverts, TODOs/FIXMEs, changelog entries, incident reports, stale docs.
- Queues, background jobs, caches, locks, lifecycle rules, telemetry, failure handling.
- Existing utilities that avoid new dependencies.
- Reviewer/stakeholder expectations and likely objections.

## Ask-vs-decide policy

This is the single rule for "do I stop and ask, or decide and keep going?" — before implementation and in the middle of it alike. [implementation-notes.md](implementation-notes.md) applies it to mid-build surprises; it does not define a competing rule.

**The test is whether a conservative option exists.** Apply it in two steps — the first step is what stops "do nothing" from winning every time.

**Step 1 — which options even count.** A candidate must *meet the stated goal* and *preserve existing contracts* (public API shape, data formats, documented behaviour, availability for users who already had it). Abandoning the feature, or breaking today's callers, is not a conservative option; it is a different decision, and it belongs to the user.

**Step 2 — is any candidate conservative?** A conservative candidate has all three properties:

> It **loses no data**, **widens no access**, and **causes no irreversible external effect** — no money moved, no message or notification sent, no third party told something that cannot be untold.

- **One or more candidates qualify** → take the most conservative; if several tie, take the one with the smallest blast radius, and if they still tie, the one easiest to reverse. Record it (template below), flag it prominently, keep going. Interrupting for every question that touches permissions or data would make the agent unusable; those questions arise constantly in real work.
- **No candidate qualifies** → **stop and ask.** Every path forward costs something the user has not agreed to, and choosing which cost to pay is theirs.

Worked examples:

| Mid-build situation | Conservative candidate? | Action |
|---|---|---|
| Guests could download files they should not, via the new export path | Return 403 for guests on the new path: loses no data, widens no access, reverses trivially | Take it, log it, flag it, continue |
| Guests already export elsewhere in the product, and the only fix that closes the hole also removes that | Fails step 1: it withdraws access users already had, so it is not a candidate at all | Stop and ask |
| Retry logic might double-charge a card | Making the charge idempotent qualifies; if the payment API cannot express that, no candidate does | Idempotency if available, else stop |
| The fix would 403 *everyone*, not just guests | Fails step 1 — it breaks availability for users who already had access | Not a candidate; stop and ask |
| The safe path costs an unbounded amount of compute per request | Fails step 1 if it breaks a stated latency or cost contract | Stop and ask |

If two candidates still tie after blast radius and reversibility, take either and say in the log that the tie was arbitrary — a coin-flip you disclose beats a decision you pretend was forced.

The categories below are **examples of where the test usually lands**, not a separate rule. When a category and the test disagree, **the test wins** — including when the test clears something the categories list as usually-stop. A schema change that meets the goal, preserves every existing contract, loses no data, widens no access, and is reversible really is safe to make and log; the category is there for the far more common schema change that fails one of those.

*Usually no conservative option (expect to stop):* architecture and execution model; scope and object model; schema, migration, retention, or API contract changes; anything widening auth, permissions, privacy, billing, or data export; irreversible user-facing behaviour or product policy; rollout and rollback commitments.

*Usually conservative and reversible (expect to decide and log):* naming, formatting, scaffolding, fixtures, obvious tests, small refactors, anything local and easy to change later, and anything the repository's existing patterns already imply.

When deciding without asking, record:

```markdown
Assumption: [decision]
Reason: [why conservative / repository precedent]
Reversible: yes/no
Revisit when: [condition]
```

## Failure modes to avoid

- Implementing the user's first wording without checking the territory.
- Treating the 11 techniques as a mandatory pipeline instead of a toolbox.
- Asking many low-impact questions instead of one high-blast-radius question.
- Producing options that are cosmetic variations rather than distinct strategies.
- Hiding high-blast-radius decisions inside a mechanical execution sequence.
- Copying the newest or most similar file without checking whether it is an exception, bypass, or half-migration.
- Adding a dependency when an existing utility already covers it.
- Treating dev/staging behavior as production truth without checking flags and config.
- Dropping legacy or null data because the fixtures are clean.
- Treating a passing unit test as proof of permissions, rollout, or observability safety.
- Letting mid-build deviations disappear into chat scrollback.
- Copying external reference code verbatim instead of porting semantics.
- Shipping a change the approver could not explain during an incident.
- Producing decorative HTML that reveals nothing prose wouldn't.
