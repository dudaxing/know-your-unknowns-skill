# 5. Brainstorm the intervention

**Hunts:** the option space for a known unknown — the problem is clear, the solution is not.

**Use when:** a metric or behavior needs fixing (e.g. "users churn after onboarding") and the team would otherwise jump to the first intuitive fix. Replace intuition with options grounded in what technically exists.

## Investigation

Search the actual codebase for intervention points. The highest-value finds are *almost-finished* things:

- Dead-end empty states missing a CTA that exists elsewhere in the codebase.
- Complete features behind flags set to `false` for months.
- Backend data (pending invites, milestone tracking) that no UI ever queries.
- TODO comments from original authors suggesting the exact fix.
- Admin-only tooling that could be user-facing.
- Deliberately limited features (guest tokens with 24h expiry) that could be expanded into retention loops.

## Structure the ~10 interventions along two axes

- **Vertical timeline (cost):** "ship this afternoon" → "this week" → "this month" → "quarter-long bet."
- **Horizontal scope label:** `wiring` (connect what exists) / `new UI` / `new lifecycle` / `new surface`.

Order from cheapest to most ambitious. For each: title, what exists today (with file/flag citations), what the intervention adds, impact hypothesis (why it plausibly moves the metric), risk, and **what it teaches** — even a cheap intervention that fails tells you something about the problem; name it.

## Artifact structure

Interventions plotted on the timeline with scope badges; each card carries a **"this resonates" checkbox**; checked items accumulate in a sticky footer that builds a copyable reply summarizing which interventions to pursue — turning the brainstorm into a decision record.

## Rules

- "Finish the existing thing" options must outnumber "build a new thing" options unless the codebase genuinely offers nothing.
- Every claim about existing code cites the file; never invent dormant features.
