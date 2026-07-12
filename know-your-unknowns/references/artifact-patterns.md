# HTML Artifact Patterns

Shared construction rules for the interactive artifacts every technique in this skill produces. Start new artifacts from `assets/artifact-skeleton.html`, which implements the base styling and the reply-builder mechanics.

## Why HTML instead of markdown

Spatial information — side-by-side comparisons, timelines, design directions, annotated code pairs — flattens badly into linear text, and long markdown gets skimmed. A self-contained interactive page trades a document the user would skim for one they will actually read, and lets the user *react* (click, select, copy) instead of composing a reply from scratch.

Use plain chat/markdown instead when the content is short, purely linear, or the user just needs an answer — an artifact for three bullet points is overhead, not clarity.

## Hard rules

1. **One self-contained `.html` file.** Inline all CSS and JS. No CDN links, no external fonts, no build step, no network requests. It must render identically from `file://`.
2. **Fake data must be plausible and clearly disposable** (mocks, design directions); **factual artifacts must cite the real territory** (file paths, PR numbers, flag names) — never invent citations.
3. **Every artifact that asks for decisions ends with a reply builder** (see below). An artifact that leaves the user to type a freeform response has failed at its job.
4. **State the artifact's contract at the top:** one line saying what this is and what the user should do ("Click through the three placements, answer the four questions, then copy the reply at the bottom").
5. **If the artifact is meant to be reused or regenerated, put the generating prompt at the top** (collapsed `<details>` is fine) so anyone can rerun or adapt it later.

## The reply builder

The signature pattern: interactive selections accumulate into a structured, copyable reply the user pastes back into chat.

- A sticky footer (or end-of-page section) holds a live-updating `<textarea readonly>` plus a **Copy reply** button.
- Every selection control on the page (chips, checkboxes, radios) writes into it on change.
- The assembled reply is written in first person from the user's voice, structured for the agent to parse: e.g.
  `Direction: 2 (airy editorial). Steal: serif numerals (D2), age timeline (D3). Skip: status column (D1). Q2: collapse behind popover.`
- Include unanswered questions in the reply as `Q3: (unanswered)` so gaps stay visible.

## Selection controls by use case

- **Steal/skip chips** (design directions): each notable element gets a chip that cycles neutral → steal → skip. Green/red visual states.
- **"This resonates" checkboxes** (brainstorms): one per option card; checked titles accumulate into the reply.
- **A/B question blocks** (mocks, plans): radio chips per question, question text restated in the reply.
- **Approve/change chips** (tweakable plans): per decision; "change" opens a one-line text input for the correction.
- **Copyable prompt blocks** (blindspot cards, improved prompts): `<pre>` with a per-block copy button.
- **Quiz gate** (merge quiz): multiple-choice (A–D) with instant feedback; wrong answers link (`href="#section"`) to the report section that teaches the point; the final checklist section stays `hidden` until the in-page score is perfect (all questions answered correctly). The **copyable reply** must list `Q1: B` / `Q2: (unanswered)` lines — **not** `Quiz score:`. The agent re-scores in chat; unlock only when **every** artifact question has a correct letter — any `(unanswered)` blocks unlock. A forged score never unlocks.
- **Sign-off gate** (semantics map): each map row has a stable **row id**; closing instruction asks for whitelist lines — `semantics confirmed` and/or `Correction: <row-id> -> <text>`, optional `Session: continue here`.

## Layout patterns

- **Card grid** for independent items (blindspots, interventions): category badge + title + body + citation line + action control.
- **Full-width stacked sections** for design directions: each direction rendered at realistic fidelity with its philosophy statement as a kicker line.
- **Side-by-side panes** for code pairs (reference ports): source left, target right, load-bearing lines highlighted with an annotation callout underneath.
- **Vertical timeline** for cost/effort axes (brainstorms) and dated logs (implementation notes): items pinned to the axis with scope/category badges.
- **Collapsed `<details>`** for mechanical/low-interest content (Section C of plans): honest summary text ("14 refactoring tasks, no judgment calls").
- **Tables** for decisions, edge cases, preserve/change/drop classifications — with a status column using colored dots or badges.

## Visual defaults

- System font stack; monospace only for code. Generous line-height; readable measure (~70ch max for prose).
- Neutral background, one accent color, semantic green/amber/red for statuses. Respect `prefers-color-scheme` if trivial; otherwise pick one scheme and keep contrast high.
- Category badges: small uppercase labels (LANDMINE, HISTORY, DISCOVERY, NEEDS JUDGMENT) — instantly scannable.
- No animation except purposeful ones (a demo walkthrough, a state transition). Never decorate for decoration's sake.

## Delivery and hygiene

- Save artifacts to a scratch location — a dedicated directory at project root (e.g. `./design-directions/`, `./artifacts/`) or a single file like `change-report.html` — never inside the app's source tree.
- **Artifacts are scaffolding, not deliverables:** don't commit them unless the user asks. In a git repo, add them to `.git/info/exclude` (not `.gitignore`, which would itself show up in the diff).
- Tell the user the file path, what to do with it, and the expected reply format. When the reply comes back, act on it — the artifact is a means, the folded-in decisions are the product.
