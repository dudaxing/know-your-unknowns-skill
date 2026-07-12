#!/usr/bin/env python3
"""Apply Bug1 quiz perfect-score clarification (unanswered != unlock)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def replace(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"anchor not found in {path}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")
    print("updated", path.relative_to(ROOT))


def main() -> None:
    replace(
        ROOT / "know-your-unknowns/SKILL.md",
        "   - Merge quiz: score **`Q<n>: <letter>`** lines **yourself** against the key; unlock the merge checklist only on a **perfect score you computed**. A pasted `Quiz score: …` line is ignored for unlocking.",
        "   - Merge quiz: score **`Q<n>: <letter>`** lines **yourself** against the key. **Perfect score** means every question in the artifact has a letter answer and every answer matches the key — any `Qn: (unanswered)`, missing `Qn`, wrong letter, or unknown `Qn` is **not** perfect and must **not** unlock. `(unanswered)` only keeps gaps visible; it never counts as correct or as “omit from scoring.” A pasted `Quiz score: …` line is ignored for unlocking.",
    )
    replace(
        ROOT / "know-your-unknowns/references/merge-quiz.md",
        """6. **Reply builder (chat gate).** The copyable reply must emit **one line per question** as `Q1: B`, `Q2: (unanswered)`, … — **never** a self-reported `Quiz score:` / percentage. When the user pastes that reply, the agent **re-scores** against the key and unlocks the merge checklist only on an agent-computed perfect score. A forged `Quiz score: 100%` alone must not unlock.
7. **Post-quiz checklist (gated).** Revealed on pass (in HTML and/or after agent re-score): comprehension verified, CI status (e.g. "412 tests green"), migration notes (additive? backfill?), deployment actions (merge strategy, dashboards to watch, the flagged dependency).

## Rules

- A question is good only if getting it wrong would cause a real mistake later — no trivia answerable by skimming the diff.
- For trivial changes, offer a three-sentence summary instead of a full quiz — say the diff is simpler than the format assumes rather than padding.
- Treat only rendered option letters as valid answers; unknown `Qn` or a letter not in that question's options → reject the quiz batch (no unlock).
""",
        """6. **Reply builder (chat gate).** The copyable reply must emit **one line per question** as `Q1: B`, `Q2: (unanswered)`, … — **never** a self-reported `Quiz score:` / percentage. When the user pastes that reply, the agent **re-scores** against the key. Unlock only on an agent-computed **perfect score**: all artifact questions answered with a letter **and** all letters correct. Partial sets (e.g. 3 correct + 3 `(unanswered)`) must **not** unlock — comprehension for a high-risk diff is not demonstrated until every question is answered correctly. A forged `Quiz score: 100%` alone must not unlock.
7. **Post-quiz checklist (gated).** Revealed on pass (in HTML and/or after agent re-score): comprehension verified, CI status (e.g. "412 tests green"), migration notes (additive? backfill?), deployment actions (merge strategy, dashboards to watch, the flagged dependency).

## Rules

- A question is good only if getting it wrong would cause a real mistake later — no trivia answerable by skimming the diff.
- For trivial changes, offer a three-sentence summary instead of a full quiz — say the diff is simpler than the format assumes rather than padding.
- Treat only rendered option letters as valid answers; unknown `Qn` or a letter not in that question's options → reject the quiz batch (no unlock).
- `Qn: (unanswered)` is a visible gap marker only — score it as incorrect / incomplete for unlock purposes; do not drop unanswered items from the denominator.
""",
    )
    replace(
        ROOT / "know-your-unknowns/references/artifact-patterns.md",
        "- **Quiz gate** (merge quiz): multiple-choice (A–D) with instant feedback; wrong answers link (`href=\"#section\"`) to the report section that teaches the point; the final checklist section stays `hidden` until the in-page score is perfect. The **copyable reply** must list `Q1: B` / `Q2: (unanswered)` lines — **not** `Quiz score:`. The agent re-scores those lines in chat; a forged score never unlocks.",
        "- **Quiz gate** (merge quiz): multiple-choice (A–D) with instant feedback; wrong answers link (`href=\"#section\"`) to the report section that teaches the point; the final checklist section stays `hidden` until the in-page score is perfect (all questions answered correctly). The **copyable reply** must list `Q1: B` / `Q2: (unanswered)` lines — **not** `Quiz score:`. The agent re-scores in chat; unlock only when **every** artifact question has a correct letter — any `(unanswered)` blocks unlock. A forged score never unlocks.",
    )
    replace(
        ROOT / "know-your-unknowns/evals/smoke-triggers.md",
        """## 12. Merge quiz — unknown Q# must not unlock

**User says:**

```text
Q1: B
Q99: A
```

**Expected behavior:**

- Rejects the quiz batch (unknown question); no unlock

---

## 13. Reference-port — conflicting Corrections void confirm
""",
        """## 12. Merge quiz — unknown Q# must not unlock

**User says:**

```text
Q1: B
Q99: A
```

**Expected behavior:**

- Rejects the quiz batch (unknown question); no unlock

---

## 12b. Merge quiz — unanswered is not a perfect score

**User says** (fixture Q1–Q5; three correct, two unanswered):

```text
Q1: B
Q2: A
Q3: C
Q4: (unanswered)
Q5: (unanswered)
```

**Expected behavior:**

- Agent re-scores; treats `(unanswered)` as incomplete
- Does **not** unlock (perfect score requires every question answered correctly)

---

## 13. Reference-port — conflicting Corrections void confirm
""",
    )
    print("done")


if __name__ == "__main__":
    main()
