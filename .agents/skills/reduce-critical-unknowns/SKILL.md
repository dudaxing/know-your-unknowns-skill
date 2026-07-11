---
name: reduce-critical-unknowns
description: Find and cheaply test decision-changing unknowns in risky software work before they cause rework; do not expand clear, local, reversible fixes into a full uncertainty workflow. Use for ambiguous or unfamiliar important features, authentication or permission changes, schema and contract migrations, cross-language semantic ports, material implementation deviations, rollout or rollback decisions, and pre-merge verification of large or high-blast-radius diffs; also use when the user asks for blind spots, an assumption audit, a focused requirements interview, a design spike, semantic mapping, deviation triage, or independent evidence. If explicitly invoked for a small task, keep it to at most one material assumption and proceed. 用户提到关键未知量、盲点、迁移风险、语义移植、实现偏差或高风险合并验证时使用。
---

# Reduce Critical Unknowns

Reduce uncertainty only until the next design, implementation, or verification decision is safe enough to make. Treat plans and requests as provisional; let repository and runtime evidence correct them.

## Scale the work

For a clear, local, reversible change:

1. Inspect the relevant code and tests.
2. Note at most one material assumption when one actually exists.
3. Implement and verify normally.

Do not create a scan report, score, ledger, gate, or separate decision document for that path.

For work with meaningful blast radius or weak evidence, follow the workflow below. If the user asks to implement immediately, keep moving after the smallest premise check; pause only the branch whose unresolved premise could cause high-impact, hard-to-reverse harm.

Honor an explicitly requested probe, but scale it to the task. Do not replace a focused request with a larger lifecycle process.

## Core workflow

### 1. Name the next decision

State internally what must be decided next: an interface, behavior, migration path, implementation slice, verification oracle, rollout, or rollback. Ignore uncertainties that would not change that decision.

### 2. Inspect the strongest available evidence

Answer repository-answerable questions before asking the user. Prefer, in order as relevant:

1. Executable tests, schemas, traces, and observed runtime behavior.
2. Current code, call paths, configuration, feature flags, and integration boundaries.
3. Version-control history, reverted attempts, migrations, incident notes, and review context.
4. Specifications and documentation.
5. Human decisions and preferences.

Attach a locator to material evidence: a path and line, symbol, commit, command and result, trace, schema field, or named decision. Never claim to have inspected evidence that was unavailable. Without repository access, present hypotheses and a next probe, not repository findings.

Distinguish these only where confusion would change the decision:

- **Observed evidence**: directly read or run.
- **Inference**: derived from evidence but not directly observed.
- **Assumption**: temporarily adopted and still falsifiable.
- **Human decision**: a choice with an owner, not a fact to discover.

### 3. Isolate and route decision-changing unknowns

Use three qualitative questions; do not calculate a risk score:

- What changes or fails if this is wrong?
- How large is the evidence gap?
- How difficult is containment or rollback?

Route each material unknown:

- **Default and continue** when it is local, reversible, observable, and implied by repository convention.
- **Probe now** when a cheap evidence-producing action could change the next decision.
- **Ask or pause the affected branch** when the answer belongs to a human and the wrong path is high-impact, weakly evidenced, and hard to reverse.

Escalation commonly matters for architecture, public or data contracts, authentication, authorization, privacy, destructive migration, important product behavior, rollout, rollback, and the test oracle. These topics are signals, not automatic global gates.

### 4. Run one probe

Choose the cheapest credible action most likely to change the next decision. Before acting, be able to fill this compact contract:

```text
Decision: what result could change
Probe: smallest action that discriminates the paths
Evidence: result that supports or rejects each path
Stop: point at which more exploration will not change this decision
```

Run one primary probe at a time. A focused test, trace, history lookup, schema comparison, fixture, pseudocode contrast, or small executable spike usually outranks a broad report.

Read [references/probe-playbook.md](references/probe-playbook.md) when selecting a probe family, honoring a named technique, or shaping a low-friction response.

### 5. Fold the result forward

Use the result immediately:

- Continue with the supported implementation slice.
- Reject an option and record the evidence briefly.
- Turn an assumption into a test or observable acceptance criterion.
- Ask for the human-owned choice with concrete consequences.
- Pause only the affected high-risk branch and identify the next probe.

For a human choice, show the evidence already gathered, the decision it affects, and two or three materially different options. Put the recommended option first and explain consequences. Ask one question when its answer changes later questions; batch a few independent choices when that is cheaper for the user.

When implementation contradicts the plan, capture only a material deviation:

```text
Planned premise -> observed evidence -> decision impact -> conservative action or escalation
```

Continue autonomously for reversible local deviations. Pause the related branch when the deviation changes security, permissions, data meaning, a public contract, important product behavior, rollout, rollback, or the verification oracle.

### 6. Verify and stop

Map important acceptance criteria to concrete evidence. For high-risk work, also inspect failure paths, rollback or containment, observability, and the maintainer's before/after mental model. Prefer an independent check that starts from the criteria and diff rather than the implementer's explanation.

Stop exploring and continue work when all are true:

- The next bounded action has an evidence-supported path.
- Remaining uncertainty is low-impact, reversible, observable, explicitly accepted, or outside the current decision.
- High-impact failure has adequate containment, rollback, or a clearly paused branch.
- Another probe is unlikely to change the next decision.

If evidence cannot lower the risk enough, stop the affected branch with the smallest next probe or human decision required. Do not keep exploring merely to exhaust a taxonomy.

## Persist and report proportionally

Default to chat, patches, tests, traces, commands, Markdown, or a small machine-readable handoff. Do not create a durable state file solely because this Skill ran.

Persist a minimal decision/unknown handoff only when the work genuinely spans sessions, agents, or owners and no existing issue, plan, or project mechanism already carries it. Reuse the project's established location and format.

At a coordination boundary, use only the fields that help the next actor:

```text
Decision:
Evidence:
Assumption or residual risk:
Next action:
```

Omit this block when the patch and verification already communicate the result.

Read only the relevant section of [references/risk-patterns.md](references/risk-patterns.md) for authentication/session work, schema or public contracts, semantic ports, ambiguous important features, implementation deviations, risky diffs, or unavailable repository evidence.

## Guardrails

- Do not invent findings to fill a format.
- Do not run every probe or checklist.
- Do not treat agent agreement as evidence.
- Do not use a comprehension check as a correctness test.
- Do not ask the user for facts that code, tests, history, configuration, or a cheap run can answer.
- Do not silently choose a low-confidence, high-impact, hard-to-reverse path.
- End with an executable next step, implementation, or verification result rather than an uncertainty report alone.
