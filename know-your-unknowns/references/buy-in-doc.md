# 10. The buy-in doc

**Hunts:** the reviewers' unknowns. Reviewers start with the same unknowns the author started with; experts want to see that the failure points they'd probe were accounted for. Build the document that closes both gaps.

**Use when:** development is complete and the change needs sign-off from people across engineering, security, design, or product — especially people who weren't in the loop.

## Workflow

1. **Collect the artifacts:** spec, prototype, implementation notes, the diff, demo media (GIF/screenshots). If a key artifact is missing, ask once, then work with what exists.
2. **Build one self-contained document** — single HTML file preferred (inline CSS, no network), droppable into Slack or an issue, readable on a phone, skimmable in 90 seconds with links for depth.

## Artifact structure — five sections, in this order

1. **Watch it work.** Lead with the demo: an embedded recording, GIF, or animated walkthrough of the feature running, annotated with real usage context. Architecture comes after belief — never open with it.
2. **The pitch.** Problem tied to measurable business impact (e.g. "41% of departed teams cited this gap in churn interviews"), the solution in two sentences, and why now.
3. **What reviewers will ask.** The 4–6 objections each stakeholder role would raise, each pre-answered with *linked, verifiable evidence* — not reassurance. Pull from the implementation notes' deviations and needs-judgment items if they exist. Evidence types by objection:
   - Data-leak risk → permission-matrix tests, visibility-resolver spec.
   - Performance at scale → load-test numbers (e.g. "12,400 annotations: 3.1s; p95 340ms").
   - "Why not build X instead?" → usage/ticket analysis showing the chosen scope covers the demand (e.g. "83% of requests satisfied by these formats").
   - Infrastructure burden → architecture section proving zero new services.
   - Compliance/audit → audit-logging spec, metadata stamping, expiring URLs.
4. **Spec at a glance.** One reference table: formats, entry points, permissions, limits, telemetry, rollout plan. Links into the full spec for deep-divers.
5. **Risk, rollback, limitations, and what I need from you.** Failure modes and containment; rollback emphasized as trivially reversible ("one toggle") to lower the psychological cost of approving; **what this deliberately does not do** — limitations and open questions stated up front; then *named* stakeholders with the specific sign-off requested from each ("✓ on your piece") and a concrete date ("target: ramp starts Monday").

## Rules

- Write for the reviewer's unknowns, not the author's pride — the goal is that their first question is already answered in the doc.
- **Do not oversell.** Limitations stated up front build more trust than completeness claimed and disproven.
- Every answer must link to its evidence (spec section, test file, dashboard); an unlinked claim is an invitation to relitigate.
- Specific asks with names and dates create accountability that "PTAL" never does.
