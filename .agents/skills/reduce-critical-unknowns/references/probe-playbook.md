# Probe playbook

Use this playbook to choose one probe family. Do not run the families as a sequence or produce every listed field.

## Contents

1. Territory scan
2. Contract and semantics map
3. Contrast or executable probe
4. Human decision probe
5. Deviation probe
6. Readiness evidence probe
7. Explicit-request mapping
8. Low-friction handoffs

## 1. Territory scan

Use this to decide whether the request's apparent path matches the actual system.

- **Minimum action:** Trace the target entry point through tests, configuration, flags, schema/migrations, integrations, and relevant history. Narrow the scan around the current decision.
- **Evidence:** Concrete locators, executed behavior, a reverted attempt, an environment difference, or a missing registration/cleanup path.
- **Handoff:** Convert each material finding into a constraint, rejected premise, test, or implementation-order change.
- **Stop:** The candidate path is supported or falsified, and another scan area is unlikely to change the next decision.

Do not report generic best practices as repository blind spots. If the area is simple, say so and proceed.

## 2. Contract and semantics map

Use this to decide what behavior must be preserved, deliberately changed, or dropped across a boundary or reference implementation.

- **Minimum action:** Compare only caller-observable behavior and load-bearing edge cases. Translate existing tests or fixtures before translating implementation structure when possible.
- **Evidence:** Source and target tests, schemas, traces, error behavior, timing, retries, cancellation, concurrency, resource lifetime, boundary values, side effects, and compatibility constraints.
- **Handoff:** Record `preserve / change / drop`, the reason, and the executable oracle for each material difference.
- **Stop:** Every material observable behavior has a disposition, and unresolved differences are explicit enough to test or escalate.

Do not require human sign-off when executable evidence resolves a low-risk equivalence. Do pause when a public contract or destructive interpretation remains a human-owned decision.

## 3. Contrast or executable probe

Use this to decide among tacit preferences, competing architectures, or uncertain feasibility.

- **Minimum action:** Show two or three materially different directions using the same inputs, or build the smallest disposable spike that discriminates them.
- **Possible forms:** Markdown comparison, API/schema examples, pseudocode, request/response traces, test fixtures, CLI simulation, benchmark slice, or bounded code spike.
- **Evidence:** A user reaction tied to consequences, a compile/run result, a test oracle, measured behavior, or a repository constraint.
- **Handoff:** Select a direction, combine explicitly compatible attributes, or reject all directions with the next probe.
- **Stop:** The result selects or eliminates a path. Do not generate extra variants after the decision has converged.

Keep options genuinely different in behavior, cost, failure mode, or reversibility. Renaming the same idea is not a contrast.

## 4. Human decision probe

Use this only when the remaining answer belongs to a person rather than the repository.

- **Minimum action:** Present the decision, evidence already checked, and two or three concrete options with consequences. Recommend the safest evidence-supported option first.
- **Evidence:** The named owner's selection or explicit risk acceptance.
- **Handoff:** A short constraint that downstream implementation can apply without reinterpreting the conversation.
- **Stop:** The high-impact choice is made, safely defaulted, or isolated from the current work.

Ask one question at a time when an answer changes later questions. Batch a few independent choices when that reduces round trips. Do not interview for polish that a reversible repository convention can settle.

## 5. Deviation probe

Use this when implementation evidence contradicts a plan or accepted premise.

- **Minimum action:** Capture the planned premise, observed evidence, effect on behavior or verification, and the smallest safe response.
- **Evidence:** The exact code, fixture, trace, integration behavior, or migration state that contradicted the plan.
- **Handoff:** Continue with a conservative local choice, revise the plan, add a regression test, or pause the affected branch for a decision.
- **Stop:** The current branch is safe to continue or clearly isolated; future work will not have to rediscover the same material fact.

Do not log mechanical differences already obvious from the diff. Do not rewrite the old plan to make the deviation disappear.

## 6. Readiness evidence probe

Use this to decide whether a large or high-risk change is ready to merge, deploy, or hand off.

- **Minimum action:** Map each important acceptance criterion to evidence, then sample the highest-consequence failure path.
- **Evidence:** Targeted tests, integration or migration results, rollback/containment, observability, permission checks, and an independently reconstructed before/after mental model.
- **Handoff:** `criterion -> evidence -> gap/owner`, plus the concrete merge, deploy, or next-probe decision.
- **Stop:** Material criteria have credible evidence and residual risk has an owner or containment path.

A quiz can reveal misunderstanding when explicitly requested, but it does not prove correctness and must not replace tests or independent verification.

## 7. Explicit-request mapping

Respect the user's named intent while keeping the action proportional:

| User intent | Smallest matching family |
|---|---|
| Find blind spots or audit assumptions | Territory scan |
| Teach the missing vocabulary | Contrast/executable probe focused on terms and oracle |
| Show directions, mock, or prototype first | Contrast or executable probe |
| Interview me or clarify the high-impact requirement | Human decision probe |
| Map or port reference behavior | Contract and semantics map |
| Review or make a plan tweakable | Human decision probe on judgment calls |
| Record implementation surprises | Deviation probe |
| Prepare approval evidence or test merge understanding | Readiness evidence probe |

Do not force the historical technique's original output medium, item count, or gate.

## 8. Low-friction handoffs

Use a plain response when possible. At a boundary, choose one compact shape.

Decision snapshot:

```text
Decision: ...
Evidence: ...
Residual risk: ...
Next: ...
```

Concrete choice:

```text
A (recommended): behavior and consequence
B: different behavior and consequence
Reply with A/B, or state the constraint that changes the choice.
```

Machine-readable handoff when another tool or agent needs it:

```json
{
  "decision": "...",
  "evidence": ["locator: result"],
  "assumption": "...",
  "next": "..."
}
```

Do not create a new file for these shapes unless persistence is genuinely required.
