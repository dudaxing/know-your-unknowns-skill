# 11. Quiz me before I merge

**Hunts:** the user's own unknowns about what just changed. After a long session, the diff alone doesn't capture behavior that depends on existing code paths. Passive review lets "I skimmed the diff" pass for understanding; a report *ending in a quiz* makes comprehension something you demonstrate rather than assume. The bar: whoever approves should be able to explain the change to whoever gets paged when it breaks.

**Use when:** a large or risky diff (infrastructure, security, data handling, multi-system refactor) is about to merge.

**Prompt shape:** *"Generate a merge-readiness report on this diff — context, rationale, implementation — ending in a quiz before I merge."*

## Workflow

1. **Determine scope:** the current session's changes by default, or the diff/branch/PR the user points at. **Read not just the touched code but the existing code paths it integrates with** — that's where the surprising behavior lives.
2. **Write the report** as one self-contained HTML file (e.g. `change-report.html` at project root). Keep it outside the changeset: don't commit it; add it to the file reported by `git rev-parse --git-path info/exclude` in a git repo.
3. **Grade in chat** if the user answers there; explain misses with exact file/line references.

## Artifact structure

1. **Mental model (before/after).** A diagram contrasting the old and new flow — e.g. before: browser-side rendering via MediaRecorder, 40–90s, tab-locking, Safari-incompatible; after: client requests export → server-side worker renders from original media → client polls for a signed download URL.
2. **What changed, grouped by area,** linking file paths and explaining how each group interacts with pre-existing behavior.
3. **Non-obvious behaviors, called out explicitly.** The 2–4 counterintuitive decisions a skimmer would miss, each with its reason: e.g. exports use original uploads, not compressed proxies (fidelity; coordinates re-projected to full resolution); job recovery uses visibility timeouts, not retries (a locked job expires after 10 min; avoids idempotency traps); download URLs expire in 24h while exports persist 7 days (short links block external forwarding; long TTL allows URL refresh without re-render).
4. **Dependency and risk flags.** What the diff relies on that the diff itself doesn't show — shared middleware, open tickets that could silently interact (e.g. "session changes in BL-2214 could affect export downloads"), user-observable differences, potential breakage points.
5. **The quiz.** Typically **six** questions (**5–8 OK**) targeting *decision-critical* understanding, framed from the reviewer's perspective ("will this break X?"), not the author's. Good question shapes: behavior that depends on existing code paths rather than new code; edge cases and failure modes handled or deliberately not; scenario tracing, e.g. — "a user sees X after deploy; given the design, what does that imply?", "dependency Y changes; why is this feature affected?", "the URL expired but the object still exists — what's the cheapest fix?", "why does this differ from what the user saw in the UI?", "what protects this permission boundary?". Mechanics: multiple choice (options **A–D**, unique letters per question) with real-time score in the HTML; **wrong answers route back to the specific report section** that teaches the point; the merge checklist stays hidden until the in-page score is perfect.
6. **Reply builder.** The report prints its **artifact id** (`KYU-EXAMPLE`) in the header, and the copyable reply leads with it, then **one line per question** — **never** a self-reported score:

   ```
   Artifact: KYU-EXAMPLE
   Q1: B
   Q2: D
   Q3: (unanswered)
   ```

   When the user pastes it, **re-score the answers yourself** against the key; if the key is no longer in context, re-read the report by its id rather than trusting recall. The `Artifact:` line binds the answers to *this* report and its question set — that is what catches `Q1`–`Q5` pasted from a previous five-question report when the current one has six. A reply with a missing or mismatched id carries no result: say which report you expected and ask the user to re-copy from it.
7. **Post-quiz checklist — two independent reveals, deliberately.** The page cannot be unlocked from chat, so do not pretend it can:
   - *In the page*: the checklist section is `hidden` until the in-page score is perfect. This is a reading aid for the person filling it in, nothing more — the page grades against a key embedded in its own JavaScript, which the reader could read.
   - *In chat*: after you re-score the pasted reply yourself, deliver the checklist **as a chat message**. That is the one that counts, because it is the only scoring the user did not have the answer key for.
   
   Contents either way: comprehension verified, CI status (e.g. "412 tests green"), migration notes (additive? backfill?), deployment actions (merge strategy, dashboards to watch, the flagged dependency).

## Rules

- A question is good only if getting it wrong would cause a real mistake later — no trivia answerable by skimming the diff.
- For trivial changes, offer a three-sentence summary instead of a full quiz — say the diff is simpler than the format assumes rather than padding.
- Treat only rendered option letters as valid answers; unknown `Qn` or a letter not in that question's options → reject the quiz batch (nothing revealed).
- `Qn: (unanswered)` is a visible gap marker only — score it as incorrect / incomplete; never drop unanswered items from the denominator.
- This is a checkpoint, not a merge lock. If the user decides to merge without a perfect score, that is theirs to decide: say which questions are outstanding and what that leaves unverified, then proceed. The protocol exists so the *agent* never mistakes an unscored or replayed reply for demonstrated understanding.
