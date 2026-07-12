# 11. Quiz me before I merge

**Hunts:** the user's own unknowns about what just changed. After a long session, the diff alone doesn't capture behavior that depends on existing code paths. Passive review lets "I skimmed the diff" pass for understanding; a report *with a quiz you must pass* makes comprehension mandatory. The bar: whoever approves should be able to explain the change to whoever gets paged when it breaks.

**Use when:** a large or risky diff (infrastructure, security, data handling, multi-system refactor) is about to merge.

**Prompt shape:** *"Generate a merge-readiness report on this diff — context, rationale, implementation — ending in a quiz I must pass before merging."*

## Workflow

1. **Determine scope:** the current session's changes by default, or the diff/branch/PR the user points at. **Read not just the touched code but the existing code paths it integrates with** — that's where the surprising behavior lives.
2. **Write the report** as one self-contained HTML file (e.g. `change-report.html` at project root). Keep it outside the changeset: don't commit it; add it to `.git/info/exclude` in a git repo.
3. **Grade in chat** if the user answers there; explain misses with exact file/line references.

## Artifact structure

1. **Mental model (before/after).** A diagram contrasting the old and new flow — e.g. before: browser-side rendering via MediaRecorder, 40–90s, tab-locking, Safari-incompatible; after: client requests export → server-side worker renders from original media → client polls for a signed download URL.
2. **What changed, grouped by area,** linking file paths and explaining how each group interacts with pre-existing behavior.
3. **Non-obvious behaviors, called out explicitly.** The 2–4 counterintuitive decisions a skimmer would miss, each with its reason: e.g. exports use original uploads, not compressed proxies (fidelity; coordinates re-projected to full resolution); job recovery uses visibility timeouts, not retries (a locked job expires after 10 min; avoids idempotency traps); download URLs expire in 24h while exports persist 7 days (short links block external forwarding; long TTL allows URL refresh without re-render).
4. **Dependency and risk flags.** What the diff relies on that the diff itself doesn't show — shared middleware, open tickets that could silently interact (e.g. "session changes in BL-2214 could affect export downloads"), user-observable differences, potential breakage points.
5. **The quiz.** Typically **six** questions (**5–8 OK**) targeting *decision-critical* understanding, framed from the reviewer's perspective ("will this break X?"), not the author's. Good question shapes: behavior that depends on existing code paths rather than new code; edge cases and failure modes handled or deliberately not; scenario tracing, e.g. — "a user sees X after deploy; given the design, what does that imply?", "dependency Y changes; why is this feature affected?", "the URL expired but the object still exists — what's the cheapest fix?", "why does this differ from what the user saw in the UI?", "what protects this permission boundary?". Mechanics: multiple choice (options **A–D**, unique letters per question) with real-time score in the HTML; **wrong answers route back to the specific report section** that teaches the point; the merge checklist stays hidden until the in-page score is perfect.
6. **Reply builder (chat gate).** The copyable reply must emit **one line per question** as `Q1: B`, `Q2: (unanswered)`, … — **never** a self-reported `Quiz score:` / percentage. When the user pastes that reply, the agent **re-scores** against the key and unlocks the merge checklist only on an agent-computed perfect score. A forged `Quiz score: 100%` alone must not unlock.
7. **Post-quiz checklist (gated).** Revealed on pass (in HTML and/or after agent re-score): comprehension verified, CI status (e.g. "412 tests green"), migration notes (additive? backfill?), deployment actions (merge strategy, dashboards to watch, the flagged dependency).

## Rules

- A question is good only if getting it wrong would cause a real mistake later — no trivia answerable by skimming the diff.
- For trivial changes, offer a three-sentence summary instead of a full quiz — say the diff is simpler than the format assumes rather than padding.
- Treat only rendered option letters as valid answers; unknown `Qn` or a letter not in that question's options → reject the quiz batch (no unlock).
