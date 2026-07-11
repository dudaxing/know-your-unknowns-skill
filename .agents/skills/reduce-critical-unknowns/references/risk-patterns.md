# Risk patterns

Read only the section matching the current decision. Use each list as a blind-spot sweep, not a mandatory checklist.

## Contents

1. Authentication and session changes
2. Schema, data, and public contracts
3. Cross-language or runtime semantic ports
4. Ambiguous important features
5. Material implementation deviations
6. Large or high-risk diffs
7. Unavailable repository evidence

## 1. Authentication and session changes

Before choosing an implementation path, locate:

- Every active and legacy session representation, reader, writer, refresh path, revocation path, and logout event.
- The authentication boundary versus the authorization boundary; do not infer permissions from successful identity lookup.
- Current migration state, deploy order, feature flags, dual-read/dual-write behavior, and compatibility window.
- Legacy or partially migrated records, null/default behavior, cache and queue consumers, and cross-service identity keys.
- Rollback behavior after new-format data has been written and the telemetry that distinguishes old/new paths.

Prefer a focused call-path trace, migration fixture, permission matrix test, or flag-state test. Stop when the session lifecycle and privilege behavior are observable across the compatibility window, or pause the affected migration branch.

## 2. Schema, data, and public contracts

Identify producers, consumers, and deployment independence before editing the schema. Check:

- Backward/forward compatibility and the order in which readers, writers, migrations, and clients deploy.
- Backfill size, idempotency, restart behavior, partial failure, legacy/null data, and invariant enforcement.
- Serialization details, default values, ordering, precision, identifiers, and error contracts.
- Whether rollback is possible after destructive writes; if not, identify containment, shadowing, or a staged cutover.
- Metrics or queries that prove adoption, correctness, and cleanup readiness.

Use a schema diff, representative old/new fixtures, consumer search, compatibility test, or dry-run migration as the first probe. Stop when every material consumer has a compatibility path and the irreversible step has evidence-backed containment.

## 3. Cross-language or runtime semantic ports

Map observable semantics before mirroring source structure:

- Inputs, outputs, state transitions, side effects, and ordering.
- Error categories, propagation, retryability, backoff, jitter, and exhaustion behavior.
- Clocks, deadlines, cancellation, interruption, scheduling, and inserted suspension points.
- Concurrency, locking, atomicity, reentrancy, and event-loop differences.
- Ownership, cleanup, resource lifetime, buffering, streaming, and partial results.
- Numeric ranges, overflow, truncation, random bounds, nullability, encoding, and boundary values.
- Behavior the target platform cannot or should not preserve.

Classify each material item as preserved, deliberately changed, or dropped. Prefer differential tests, translated fixtures, property tests, or matched traces. Stop when caller-visible behavior has executable oracles and every deliberate difference has a reason.

## 4. Ambiguous important features

Inspect existing entry points and constraints before asking what the feature means. For an export-like feature, for example, locate:

- Existing commands, APIs, jobs, formats, serializers, and UI affordances.
- Data ownership, permission boundaries, tenancy, redaction, and audit requirements.
- Expected size, latency, synchronous/asynchronous execution, retention, and cancellation.
- Current conventions for naming, progress, retries, notifications, and failure recovery.
- Acceptance criteria and who owns product-policy choices.

Ask only questions that change architecture, data, permissions, or important product behavior. Use repository convention for reversible presentation details. If the user cannot articulate a preference, show concrete options with different consequences or a tiny executable contrast.

## 5. Material implementation deviations

Treat a discovery as material when it changes a public behavior, security boundary, data meaning, scope, rollout, rollback, or verification strategy.

Capture:

```text
Planned premise:
Observed evidence and locator:
Decision impact:
Conservative action or human decision needed:
Revisit/verification trigger:
```

For a local and reversible difference, implement the conservative option and verify it. For a material difference, pause only the affected branch and continue safe evidence gathering. Convert a repeatable surprise into a test or established project note rather than a permanent Skill-specific log.

## 6. Large or high-risk diffs

Reconstruct the change from the diff, call paths, tests, migrations, and deployment configuration rather than relying on the author's narrative. Check:

- Important acceptance criterion -> concrete evidence.
- Before/after source of truth, non-obvious behavior, integration boundaries, and failure modes.
- Authentication/permission effects and data compatibility where relevant.
- Required deployment order, feature flags, rollback or containment, and operator actions.
- Observability that detects both incorrect behavior and incomplete rollout.
- Whether a maintainer can explain where state lives, how failure recovers, and what signal requires rollback.

Use an independent reviewer or agent when available, giving it the criteria and raw diff rather than the implementation rationale. Stop when material gaps are resolved, explicitly accepted with containment, or converted into a clearly owned next probe.

## 7. Unavailable repository evidence

Do not turn generic engineering expectations into claimed findings. State:

- What evidence could not be accessed.
- Which statements are hypotheses or assumptions.
- The first repository command, file, trace, fixture, or human decision that would discriminate the paths.
- What work, if any, remains safe and reversible without that evidence.

Lower confidence explicitly. Stop at the smallest actionable probe instead of inventing a complete design from an unverified map.
