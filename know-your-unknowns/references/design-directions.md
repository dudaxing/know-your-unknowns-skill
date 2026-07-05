# 3. Four design directions

**Hunts:** unknown knowns — taste the user can only articulate on sight. Reacting is easier than imagining.

**Use when:** stakeholders can't articulate visual preferences. Render the *same real data* through several incompatible design philosophies and let the user react instead of writing a brief.

## Workflow

**Step 0 — Confirm scope in one message:** what surface, what data it shows. No lengthy interview.

**Step 1 — Produce 3–5 genuinely incompatible directions (default 4)** — different philosophies, not palette swaps. Vary layout philosophy, density, hierarchy, and interaction model. **Push at least one direction beyond the user's stated taste** — the point is to discover what they didn't know they wanted. Reference philosophies (adapt to the actual product):

1. **Dense ops console** — "show everything, waste nothing, let the anomalies pop": metric strips, status indicators, maximal table.
2. **Airy editorial cards** — "one number that matters, then the queue as a reading list": breathing room, serif numerals, human status language.
3. **Kanban/timeline hybrid** — "a review is a thing that moves": pipeline columns plus age visualization.
4. **Brutalist mono terminal** — "no decoration, no chrome; read it top to bottom and get out": monospace, keyboard-first.

Others when they fit: guided wizard (one decision per screen), analytics dashboard (charts first, records second).

**Step 2 — Deliver as artifact and collect reactions.**

## Artifact structure

Default: one comparison file — each direction a fully rendered section (same underlying data in all of them) with a memorable name and a one-line philosophy statement. Under each direction, **steal/skip chips** for its distinctive elements ("steal: serif numerals", "skip: status column"). A sticky footer assembles all chip selections plus a "which direction's overall attitude wins?" choice into a structured reply with a copy button.

When directions are heavy full-page experiences that cramp side-by-side, split into one file per direction under `./design-directions/` with memorable filenames, and keep the steal/skip reply builder in a small index file.

## Rules

- Fake data must be realistic — never lorem ipsum; taste reactions depend on plausible content.
- Prototypes live in a scratch directory (e.g. `./design-directions/`), never inside the app's source tree. Do not modify application code, add dependencies, or wire up backends.
- Do not commit prototypes; in a git repo, add the directory to `.git/info/exclude`.

## Follow-up

When the reply comes back, fold the stolen elements into the winning direction and produce the refined single design. Iterate on reactions, not briefs.
