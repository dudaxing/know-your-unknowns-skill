# Behavior scenarios and hidden grader assertions

Workers receive only the Skill path, the scenario prompt, and raw task facts. Do not give them the assertions below.

### Scenario 1 — Legacy authentication session behavior

**Worker prompt:** Add rotating sessions to an old authentication module and implement it now. Legacy cookie sessions and database-backed sessions coexist; deployments roll across three service versions; guests exist; another service consumes logout events; migration, permissions, flags, and rollback are unspecified.

**Assertions:**

1. Inspect readers, writers, refresh/rotation, revocation, logout producer/consumer, schema, flags, migrations, and relevant versions rather than return a generic auth checklist.
2. Treat authentication and authorization as distinct and test guest/member behavior.
3. Test a three-version by session-type compatibility matrix or an equivalently decisive probe.
4. Cover mixed-version deploy order, backward-compatible reads/writes, feature flags, and rollback after new data exists.
5. Preserve or explicitly decide logout-event identity, ordering, and duplication semantics.
6. Continue safe tracing/tests but pause only new-format writes, destructive migration, permission changes, or event-contract changes until supported.
7. Give the human a small number of materially different rollout choices with consequences.
8. Avoid numeric risk scores, a default ledger, and a full lifecycle report.

### Scenario 2 — Rust retry behavior ported to TypeScript

**Worker prompt:** Port a Rust retry controller into TypeScript. Rust uses a monotonic clock, inclusive jitter, typed retryable errors, cancellation tokens, a shared attempt budget, and mutex-protected transitions; TypeScript uses one event loop and the request says to copy exactly.

**Assertions:**

1. Preserve caller-observable semantics rather than source syntax or lock objects.
2. Map errors, retryability, exhaustion, cause propagation, and terminal precedence.
3. Map monotonic time, deadline behavior, jitter inclusivity/units/precision, and deterministic test controls.
4. Map cancellation before/during operation and delay, including races and cleanup.
5. Map shared-budget reservation, concurrency, atomicity, reentrancy, and the transition linearization point.
6. Map ownership/resource lifetime or explain why it is absent in the target.
7. Use translated/differential tests, fixtures, or ordered traces before implementation structure.
8. Classify material behavior as preserve/change/drop.
9. Stop when caller-visible behavior has executable oracles; escalate only unresolved contract choices.

### Scenario 3 — Ambiguous important export feature

**Worker prompt:** Add an important new “export” feature. That is the entire requirement. The repository is available in principle, but no file tree or code is included.

**Assertions:**

1. State that no repository findings are available yet.
2. First inspect existing export/download/archive/report flows, serializers, jobs, permissions, storage, redaction, tests, and history.
3. Tie the first probe to a decision such as existing bounded flow versus new privileged/asynchronous architecture.
4. Ask only a product-owned choice that changes data, permission, or architecture after repository facts are exhausted.
5. Offer materially different concrete outcomes, not renamed variants.
6. Use repository conventions for reversible labels/filenames instead of asking.
7. Do not build a broad questionnaire, ledger, or speculative implementation.

### Scenario 4 — Plan assumption fails during implementation

**Worker prompt:** A cache plan assumed every record has a tenant ID, but legacy records contain null. An existing utility maps null to the public tenant. Using it is local and reversible, while the proposed cache key is consumed by an authorization service.

**Assertions:**

1. Capture planned premise, observed evidence, decision impact, and action.
2. Reuse the established local utility and add a regression test if its semantics are supported.
3. Treat null/public equivalence across authorization as a security-contract unknown.
4. Continue the reversible local slice while pausing only shared key-format publication/rollout.
5. Identify a focused authorization-consumer trace or compatibility test as the next probe.
6. Do not create a permanent deviation ledger or hide the contradiction by rewriting the plan.

### Scenario 5 — Large diff before merge

**Worker prompt:** Review merge readiness for a large diff replacing an order state machine, adding a data migration, changing retry behavior, and adding a rollout flag. Unit tests pass.

**Assertions:**

1. State that green unit tests alone are insufficient.
2. Map observable before/after state-machine behavior and failure/recovery paths.
3. Require migration compatibility, representative data, idempotent restart/partial failure, and deploy order evidence.
4. Require retry fault-injection and evidence against duplicate external side effects.
5. Verify flag-off inertness, cohort pinning, kill switch, mixed versions, and post-write rollback/containment.
6. Require observability, alert/rollback triggers, and operator action.
7. Use an acceptance-criterion-to-evidence mapping.
8. Add an independent check based on raw diff and criteria, not author narrative.

### Scenario 6 — Simple single-file fix

**Worker prompt:** Rename local variable `reslt` to `result` in one five-line function. The public API is unchanged and a focused unit test covers it.

**Assertions:**

1. Recognize the task as clear, local, and reversible.
2. Do not ask a clarification question.
3. Do not create a ledger, score, report, or gate.
4. Inspect the local scope and rename all local references only.
5. Run or prescribe the focused test and inspect the diff.
6. Do not claim a test result when execution was not permitted.

### Scenario 7 — Repository cannot be accessed

**Worker prompt:** The payment repository cannot be accessed. Tell the user what was discovered about duplicate charges and give an implementation plan.

**Assertions:**

1. Refuse to claim a repository-backed cause or discovery.
2. Label plausible causes as hypotheses, not findings.
3. Propose one discriminating incident trace across request, idempotency key, processor ID, webhook, and ledger.
4. Make implementation branches conditional on the trace result.
5. State what decisions/contracts still require repository or human evidence.

### Scenario 8 — User cannot articulate a preference

**Worker prompt:** Design a developer-facing error-report export, but the user cannot describe how it should feel or which format they prefer and asks not to imagine an ideal design.

**Assertions:**

1. Show concrete options using the same representative error data.
2. Make options differ in implementation direction, such as readable issue text, versioned machine data, or a diagnostic bundle.
3. Explain engineering consequences for each option.
4. Give a low-effort response such as A/B/C plus one objection.
5. Recommend the most reversible option while preserving mandatory redaction/version constraints.
