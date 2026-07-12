# 9. Implementation notes

**Hunts:** unknowns discovered mid-flight. No plan survives contact with the codebase — log what changed and why, without stopping the work.

**Use when:** starting any long build session (hours, many files), especially for features touching legacy data, permissions, or infrastructure assumptions. Without a log, every deviation dies in scrollback and gets re-discovered next time.

**Prompt shape:** *"While you implement, keep a dated log file. Record every point where reality differed from the plan, what you chose, and why. Categorize entries; flag anything that needs my judgment instead of silently deciding."*

## Handoff from planning session

Implementation notes usually start in a **new session** after plan approval (recommended default; same-session continuation is allowed if the user asks). The first turn should confirm the handoff bundle (see [SKILL.md](../SKILL.md)):

- Approved plan / decisions table attached
- Goal restated in one paragraph
- Log path agreed (`implementation-notes.md` at project root or scratch)
- Instruction to append on every deviation, not batch at the end

If the user continues in the same session without handoff, still create the log file before the first source edit.

## Mechanics

- Create `implementation-notes.md` at the project root (or the user's preferred path). Append dated sections for new tasks rather than overwriting.
- The file is scaffolding, not deliverable: don't commit it unless asked; in a git repo add it to `.git/info/exclude`. **The chat digest at session end is the durable handoff.**
- Update incrementally — one to three lines per entry, logged the moment the surprise happens. Stop work only when a deviation would invalidate the goal itself.

## Entry categories

- **Plan-confirmed** — the plan's assumption checked out (brief; still worth recording as verified territory).
- **Discovery** — the code already contains something better than the plan (e.g. a production-tested `zipStream.ts` utility, an existing `useProgressChannel()` hook), eliminating planned work or dependencies.
- **Deviation** — reality contradicts the plan, forcing a choice on the spot (see conservative-choice rule).
- **Needs human judgment** — a decision with product implications the agent must not make alone (guest access policy, retention windows, anything user-visible or security-relevant). Log it, take the conservative interim path, and surface it prominently.

## Entry format

- Timestamp.
- **What the plan said** vs **what the code revealed** — explicit contrast.
- **The conservative choice taken**, with reasoning. The conservative-choice rule: when surprised, pick the option that loses no data and widens no access. Examples of the pattern: ~12% of annotations predate a migration and lack frame timestamps → exclude from video burn-in but include in CSV with a flag, nothing silently dropped; the queue serializes `Date` to ISO strings through JSON breaking staleness checks → define typed wire-format payloads and parse at the worker boundary; guest reviewers with download restrictions could exfiltrate via the new export path → return 403 for all formats, mirroring existing asset checks.
- **Revisit** notes — what to reconsider later if assumptions change.

## Log footer (maintained continuously, finalized at session end)

- **Todo for human** — the collected needs-judgment items.
- **Summary bullets** — deviations and discoveries distilled into inputs for the next planning cycle; brief the user on these in chat at session end.

Optionally render an HTML timeline view at session end when the log will be reviewed by stakeholders — entries on a time axis, color-coded by category, needs-judgment items pinned to the top.

## Rules

- **Never silently deviate** from the agreed plan — every departure gets an entry.
- Don't duplicate what version control already captures: log the *reasoning* and the surprise, not facts a diff shows.
- The test of a good log: could the *next* attempt at a similar feature be prompted better because of it? Progress narration ("implemented the endpoint") doesn't qualify — only contact-with-territory events do.
