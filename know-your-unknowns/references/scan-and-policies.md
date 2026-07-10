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
- Suggested trigger phrase: (one copy-paste sentence to run the recommended technique — English; add 中文 when helpful)
```

Example trigger phrases by recommended move:

| Recommended next move | Suggested trigger phrase (EN) | 中文示例 |
|----------------------|-------------------------------|----------|
| blindspot pass | `Do a blindspot pass on [module] before we implement [task].` | `在实现 [任务] 之前，对 [模块] 做一次盲区扫描。` |
| interview | `Interview me one question at a time about [feature]; prioritize architecture-changing answers.` | `就 [功能] 访谈我，一次一题，优先问会改变架构的问题。` |
| prototype / design directions | `Make an HTML page with 4 wildly different design directions for [screen] so I can react.` | `给 [界面] 出 4 个差异很大的设计方向 HTML，让我反应式选择。` |
| tweakable plan | `Write a tweakable implementation plan in HTML — decisions I'm likely to change first.` | `写一份可调实现计划 HTML，把最可能改的决策放在前面。` |
| implement | `(no technique — proceed after logging assumptions)` | `（无需额外技巧 — 记录假设后直接实现）` |

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

**Pause and ask** when the answer could change:

- Architecture, execution model, framework, background-job vs sync/client-side design.
- Scope, object model, or unit of work.
- Data model, schema, migration, storage, serialization, retention, or API contract.
- Auth, permissions, privacy, security, billing, compliance, audit logging, data export.
- User-facing workflow, formats, notifications, irreversible UX, or product policy.
- Rollout, rollback, performance/reliability targets, operational burden.

**Decide and log** when the issue is:

- Local, reversible, conventional, or already implied by repository patterns.
- Naming, formatting, scaffolding, fixtures, obvious tests, small refactors, low-blast-radius details.
- A choice where the conservative option is clearly safer and easy to change later.

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
