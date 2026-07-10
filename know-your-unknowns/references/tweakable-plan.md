# 8. The tweakable plan

**Hunts:** the decisions most likely to change — surfacing them before they're expensive to reverse.

**Use when:** presenting an implementation plan for human review. Default plans are sorted by execution order, which buries the interesting decisions in the middle. Instead **sort by how likely the reviewer is to change each part** — judgment calls surface first, trusted mechanical work sinks and collapses. High-revision-risk items lead: data model and schema changes, new type interfaces and API shapes, anything user-facing (UX flows, copy, layout).

## Artifact structure

Open with **summary chips** — one glanceable line: effort, files touched, migrations, feature flags, risk level, rollback story. Then three sections:

- **Section A — Decisions (expanded, first).** Each flagged judgment call shows: the chosen option, 1–2 concrete alternatives considered, rationale, costs of each side, the condition under which the alternative wins, and where applicable a scope-cut note ("if nobody asked for this, cutting it removes ~½ day"). Typical flag-worthy decisions: data model (snapshot/denormalize for audit-safety vs live-join for freshness), storage lifecycle (render-once-and-store vs render-on-demand), UX flow (fire-and-forget notification vs wait-then-notify hybrid). Each decision gets an approve/change chip feeding the reply builder.
- **Section B — Sequencing.** The actual build order, with the constraint that everything lands green on CI before user-facing rollout. **Mark improvisation zones:** steps where implementation is likely to reveal unknowns, each with its fallback posture ("if the queue can't guarantee ordering, fall back to client-side sort and log it").
- **Section C — Mechanical work (collapsed by default).** Refactors, plumbing, test scaffolding — labeled "no judgment calls here." The reviewer expands only if they distrust something.

## Response mechanism

Per-decision approve/change chips assembling into a copyable reply, ending in an **explicit go/no-go choice**: approve and start, adjust first, or reject. Also include **"tweak these first"** — the 2–4 one-line overrides the user is most likely to send ("switch storage to render-on-demand", "cut the CSV format"), each copyable as-is. Do not begin implementation in the same turn as presenting the plan — the pause is the point.

## Handoff bundle (after go)

When the user approves, compile a **handoff bundle** for a fresh implementation session (see [SKILL.md](../SKILL.md) — Implementation session handoff):

- Path to this plan artifact
- Folded decisions from the reply builder (restated in chat or as a short `decisions.md` in scratch)
- Any linked mock, semantics map, or improved prompt from earlier techniques
- Empty or continued `implementation-notes.md` path

Tell the user to start a **new session** and attach these files rather than continuing the planning thread.

## Optional: plan gate verification

If the project uses **codex-verify** plan gates (`.codex-verify/plan-approved`, Cursor/Claude hooks), suggest running plan review **before** source edits:

```bash
bash ~/.claude/skills/codex-verify/scripts/verify.sh plan "$(cat path/to/plan-export.md)"
```

Export the approved plan sections (decisions + sequencing + allowed paths) to a markdown file under `.codex-verify/plans/` first. PASS writes the marker and unlocks gated edits; this skill does not require codex-verify — mention it only when hooks or `.codex-verify/` already exist in the repo.

## Rules

- The plan enables review, not enforcement — it should make the likely error points visible, not prescribe every keystroke.
- Cut sections that state the obvious; a padded plan hides the decisions it exists to surface.
- The reviewer's uncertainty differs from the executor's: spend the reviewer's attention only where their preference actually matters.
