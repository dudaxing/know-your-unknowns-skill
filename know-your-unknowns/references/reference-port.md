# 7. Point at a reference

**Hunts:** unknown knowns — behavior the user can point at but not describe. The best reference is source code.

**Use when:** porting or reimplementing existing behavior (another language, another framework, a module seen elsewhere). Make the agent **prove it understood the reference — as a reviewable artifact — before a single line gets ported.** Subtle semantics (truncation, atomicity, monotonic clocks) are exactly what a plausible-looking port silently breaks.

## Workflow

**Step 0 — Get a pointer.** If the user named a reference (a vendored crate, a folder, a library, a component on a website), start there. If they can only say "like this" or can't name one, **propose 2–3 candidate references** — from the codebase, vendored dependencies, or well-known open-source implementations — and let them pick. One short message, not an interview.

**Step 1 — Read the real implementation.** The source code, not the README, docs, or a screenshot. A different language than the target is fine; semantics transfer, syntax does not.

**Step 2 — Build the semantics map** (below) and present it for sign-off.

**Step 3 — Only after the gate clears, implement** — reimplement into the target stack's idioms and the project's existing conventions; never transplant code verbatim.

## Artifact: the semantics map — five sections

1. **Behavior inventory** — what the reference actually does, as testable statements ("token bucket refills at 8 tokens/sec, bursts to 40; refill is lazy and integer-truncated; decorrelated jitter backoff in `[base, min(prev×3, cap)]`; retry budget deposits 1 per success, withdraws 10 per retry").
2. **Side-by-side code pairs** — 2–4 annotated source/target excerpts for the trickiest translations, with **load-bearing details flagged by name**: e.g. Rust integer division → JS `Math.floor`, where the `newTokens > 0` guard is "the load-bearing guard — drop it and the bucket stops refilling under frequent polling"; Rust inclusive range `lo..=hi` → `lo + Math.floor(random() * (span + 1))` where the `+1` is "a one-character bug magnet"; Rust `Mutex` → event-loop synchronous contract where "an `await` inserted between check and debit lets two retries both pass."
3. **Preserve / change / drop table** — every design choice classified: preserved exactly (formulas, economics, guards); deliberately changed with justification (`Instant` → `performance.now()`, both monotonic; `u64` nanos → `number` ms with floor to preserve truncation; injectable RNG); dropped as inapplicable (overflow guards unreachable in the target, thread-safety primitives, foreign instrumentation).
4. **Edge-case table** — rows of edge case → reference behavior → target equivalent → status (`identical` / `equivalent*`), with asterisks explaining every deliberate difference (e.g. bare `false` becomes a typed `RetryBudgetExhausted` error for the UI). Cover: clock skew, burst at t=0, exhaustion under sustained failure, sub-unit accumulation, behavior at caps.
5. **Sign-off gate** — give every preserve/change/drop and edge-case row a stable **row id** (`^[a-z][a-z0-9_-]{0,63}$`, unique, case-sensitive). End with: reply using whitelist lines only — exact **`semantics confirmed`**, and/or **`Correction: <row-id> -> <replacement text>`** (one per corrected row). Optionally add **`Session: continue here`** to implement in this session after confirm. Do not start porting until a valid confirm clears the gate.

## Reply / fold-forward

- Reply builder emits full lines: `Correction: row_id -> …` and/or `semantics confirmed`, optional `Session: continue here`.
- Free-text corrections are not binding — only structured `Correction:` lines. Unknown id, empty replacement, missing ` -> `, or conflicting duplicate ids in one paste → reject that Correction batch and void any prior confirm.
- A valid `semantics confirmed` freezes the map until a new accepted Correction batch (which voids confirm until re-confirmed).
- After confirm: recommend a fresh implementation session by default; if the user also sends `Session: continue here` (same paste or a later sole continue message), implement in-session per [SKILL.md](../SKILL.md) option-2 handoff.

## Rules

- Never copy code verbatim from an external reference — port semantics, respect licenses, match the project's style.
- If the reference's behavior conflicts with something the user stated, surface the conflict in the map instead of silently picking one.
- If the reference turns out to be a poor fit, say so and propose another — a bad reference is worse than none.
- Cite reference file paths throughout so every claim is checkable.

**Why it works:** it moves code review before the code exists, catching conceptual misunderstandings while they're still cheap to fix.
