# 2. Teach me my unknowns

**Hunts:** unknown unknowns of vocabulary — the words the user doesn't know they're missing.

**Use when:** the user is about to direct work in a domain where they lack the professional vocabulary (color grading, typography, audio mastering, DB tuning...). Goal: upgrade their prompts from vague ("make the video look nicer") to precise ("push the lift slightly teal and the gain slightly warm").

## Workflow

**Step 0 — Anchor.** One short message: what's their current exposure to the domain, and what task are they trying to direct? Calibrate the ladder to start just above what they know.

**Step 1 — Build the explainer artifact.**

## Artifact structure

- **Vocabulary ladder:** terms ordered from foundational to advanced. Per term: plain meaning, why it matters, the common gotcha, and **a ready-made sentence the user can drop into a prompt or review** ("the mids feel muddy — lift the gamma slightly"). Example ladder for color grading: exposure (stops), white balance (Kelvin: low=warm, high=cool), contrast curve (S-curve; steeper=punchier), lift/gamma/gain (shadows/midtones/highlights independently), saturation vs vibrance (vibrance protects skin tones), LUT (one-step look transform).
- **Live playground:** interactive controls (sliders, presets) applied to a representative example so each term is *felt*, not just read — e.g. a before/after frame where moving the "lift" slider visibly shifts shadows. Pure client-side CSS/JS/canvas is enough.
- **Quality standards of the field:** what practitioners actually judge — e.g. believable skin tones, rich blacks without crushed detail, whites that don't clip, shot-to-shot consistency, look appropriate to purpose, verified across devices. This tells the user what "good" means before they evaluate results.
- **Prompt upgrade examples:** 2–3 pairs of "what you would have said" → "what you can now say."

## Response mechanism

None required — the deliverable is the user's upgraded vocabulary. Optionally end with "which of these do you want to go deeper on?" chips.
