# 1. Blindspot pass

**Hunts:** unknown unknowns — the questions the user didn't know to ask.

**Use when:** about to implement in a module the user (or the agent) hasn't worked in before, especially when the task *sounds* straightforward. The output is "sentences you couldn't have written this morning — each one bought with someone else's half-day."

## Workflow

**Step 0 — Anchor on the user's starting point.** One short message, at most three sub-questions: experience with this codebase/area, decisions already made, what they plan to do next. This calibrates which findings are blindspots *for them* rather than generic facts.

**Step 1 — Explore the territory.** Scan the module's code, git log/blame, reverted PRs and their discussion threads, feature-flag configs per environment, event-bus topics, registration/wiring conventions, TODO/FIXME comments — focusing on what the user's task description *omitted*.

Blindspot categories to hunt for (each maps to a card):

- **Landmine — in-flight migration:** two implementations coexist (e.g. sessions double-written to Postgres and Redis, reads still on the old store). The newer-looking code path works in dev and fails silently in prod. Fix: name the single safe entry point (e.g. "route through `SessionBridge` only").
- **Landmine — the bad template:** the most copy-pasteable existing example is the wrong one (e.g. a SAML provider that bypasses the auth middleware pipeline due to an old CSRF workaround). Fix: name the *right* template and the invariant to verify ("confirm new routes mount inside `authPipeline`").
- **History — the reverted attempt:** someone already tried this and reverted (find the PR, read the revert thread). The agreed-upon correct approach may be documented but never implemented. Fix: link the thread; implement the agreed solution.
- **Missing concept — domain distinction:** a conceptual split the newcomer won't expect (e.g. `users` = accounts vs `identities` = linked auth methods, with linking keyed on verified email → account-takeover risk). Fix: point at the file that encodes the concept; state the safe default.
- **Landmine — environment flag discrepancy:** behavior gated by a flag that is on in dev/staging but off in prod (e.g. refresh-token rotation). Code tests fine, fails in prod. Fix: implement against production reality; document what changes if the flag ships.
- **Convention — multi-step registration:** adding a thing requires N separate steps (code registry + DB migration + contract-test fixture); skipping one leaves it silently invisible. Fix: list all steps; require the contract tests passing as evidence.
- **Architecture — it's an event, not a function call:** a side effect flows through an event bus (e.g. logout publishes `auth.session.revoked`; another service listens to release grants). Missing the event = delayed security incident. Fix: publish from every code path; test the downstream effect.

Also report, when relevant: **what "good" looks like** (quality standards, the best reference implementation in the repo, prior art) and **3–5 key domain concepts** if the domain is new to the user — key ones only, not a comprehensive glossary.

**Step 2 — Report as artifact.**

## Artifact structure

- Header stating the task and the module scanned.
- One card per blindspot with five fields: category badge (landmine / history / missing concept / convention / architecture), **evidence** (file/PR citations with line numbers), **why it bites** (the trap and its concrete consequence), **conservative default** (the safe choice if the user decides nothing), and a **copyable prompt fix** — one or two sentences to paste into the implementation prompt — plus, where applicable, the **test or verification** that proves the blindspot was avoided.
- **"How to prompt me better" section:** 3–6 concrete suggestions for future requests in this area, derived from the blindspots found (e.g. "always name the target environment — behavior differs by flag here").
- Footer: **the improved implementation prompt** — the user's original request rewritten to incorporate every constraint, ordered by execution sequence, with a review checkpoint before coding begins. One copy button for the whole thing.

## Rules

- This is a read-only pass — no code changes.
- Prioritize blindspots that would change the user's approach; drop trivia.
- Every card must cite a real file, commit, PR, or config so claims are checkable.
- If the area turns out to be straightforward with few blindspots, say exactly that — never pad with generic best practices to fill the format.
