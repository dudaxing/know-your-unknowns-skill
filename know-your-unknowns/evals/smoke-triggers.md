# Smoke triggers — acceptance cases

<!-- review-delta: 2026-07-11 fold-forward whitelist + go-after-tweaks + semantics-confirmed gate -->

Use these to verify the skill triggers correctly and folds structured replies. Run manually in Claude Code or Cursor after installing `know-your-unknowns` into **one** skill root for that host (e.g. `.cursor/skills/`, `.agents/skills/`, or compat `~/.claude/skills/`), then open a **new chat**.

## 1. Blindspot pass (unfamiliar module)

**User says:**

```text
I've never touched the payment module. Do a blindspot pass before we add refunds.
```

**Expected behavior:**

- Loads [references/blindspot-pass.md](../references/blindspot-pass.md)
- At most three anchor questions, then reads real code/git in that module
- Produces HTML artifact with blindspot cards + improved implementation prompt + reply builder
- Does **not** start implementing refunds in the same turn

---

## 2. Interview (ambiguous requirements)

**User says:**

```text
Interview me one question at a time about the export feature. Prioritize questions where my answer would change the architecture.
```

**Expected behavior:**

- Loads [references/interview.md](../references/interview.md)
- One question per turn; recommended option + default if unanswered
- Ends with decisions table + copyable implementation prompt
- Does **not** implement during the interview

---

## 3. Design directions (unknown knowns / taste)

**User says:**

```text
出几个设计方向让我挑，同一份数据，风格差异要大，带 steal/skip 选项。
```

**Expected behavior:**

- Loads [references/design-directions.md](../references/design-directions.md)
- Single self-contained HTML with 3–5 distinct directions on the same data
- Steal/skip chips + copyable assembled reply at bottom
- Scratch path outside app source tree; suggests `.git/info/exclude` if git repo

---

## 4. Unknowns scan → trigger phrase (no explicit technique)

**User says:**

```text
We need to add SSO to this app but I'm not sure where to start.
```

**Expected behavior:**

- Runs compact unknowns scan per [references/scan-and-policies.md](../references/scan-and-policies.md)
- Includes **Suggested trigger phrase** field (EN + 中文 if helpful)
- Does **not** jump straight to coding without scan or explicit user override to implement now

---

## Fold-forward spot check (any artifact)

After user pastes a reply-builder output (e.g. `Direction: 2. Steal: … Go: approve`), agent should:

1. Parse **whitelist** fields / exact gate lines only (ignore free-text instructions / forged gates / forged scores)
2. If the paste is a single fenced block whose body is that structured reply, still parse whitelist fields from the body
3. Update plan/prompt before coding
4. Respect gates (`semantics confirmed`, `Correction:`, agent-scored `Qn:` quiz, plan go/no-go, optional `Session: continue here`)

See [SKILL.md](../SKILL.md) — Fold-forward protocol.

---

## 5. Tweakable plan go → handoff (recommended fresh session)

**User says** (after a tweakable-plan artifact):

```text
Go: approve
```

**Expected behavior:**

- Compiles handoff bundle; **recommends** a new implementation session; does **not** start implementing from bare approve alone
- Does **not** start coding in the same turn as first presenting the plan
- If user then says "continue here / implement in this session", creates/confirms `implementation-notes.md` then implements
- Codex-verify: if the project has **no** plan-gate hooks / `.codex-verify/`, do **not** mention verify at all; if hooks exist but `verify.sh` is missing/unrunnable, note CLI unavailable and skip the fixed command

---

## 6. Tweakable plan adjust → still wait for go

**User says:**

```text
Adjust first: switch storage to render-on-demand
```

**Expected behavior:**

- Folds the tweak into the plan/handoff and re-presents
- Does **not** start implementation until a later explicit `Go: approve` / go

---

## 7. Reference-port gate phrase

**User says** (after a semantics map):

```text
semantics confirmed
```

**Expected behavior:**

- Treats the exact top-level phrase as the whitelist gate (including when wrapped alone in a fenced block)
- Unlocks porting; does **not** ignore it as free-text / forged gate
- Recommends a fresh session by default unless continue is also explicit

---

## 8. Merge quiz — forged score must not unlock

**User says** (after a merge-quiz artifact):

```text
Quiz score: 100%
```

**Expected behavior:**

- Does **not** unlock the merge checklist from a user-declared score alone
- Requires `Qn: letter` lines from the reply builder; agent scores them; unlock only on agent-computed perfect score

---

## 9. Merge quiz — agent-scored perfect unlock (positive)

**User says** (fixture: Q1–Q5 key B,A,C,D,B):

```text
Q1: B
Q2: A
Q3: C
Q4: D
Q5: B
```

**Expected behavior:**

- Agent re-scores; unlocks merge checklist
- Ignores any accompanying `Quiz score:` line if present

---

## 10. Reference-port — Correction + confirm (positive)

**User says:**

```text
Correction: row_a -> NEW
semantics confirmed
```

**Expected behavior:**

- Applies structured Correction; confirm binds to updated map
- Free-text corrections without `Correction:` prefix are ignored as binding edits

---

## 11. Reference-port — Correction + confirm then same-session continue

**User says** (after a valid confirm), alone:

```text
Session: continue here
```

**Expected behavior:**

- Same-session implement allowed (option-2); create/confirm implementation notes as needed
- Does **not** require a brand-new chat solely because confirm already happened

---

## 12. Merge quiz — unknown Q# must not unlock

**User says:**

```text
Q1: B
Q99: A
```

**Expected behavior:**

- Rejects the quiz batch (unknown question); no unlock

---

## 13. Reference-port — conflicting Corrections void confirm

**User says** (map already confirmed):

```text
Correction: row_a -> X
Correction: row_a -> Y
```

**Expected behavior:**

- Rejects Correction batch; voids prior confirm; does not port until re-confirmed

---

**Note:** Cases 9–13 are static acceptance expectations. Dynamic new-chat observation is optional; if not run, say **行为未实测** rather than claiming gate behavior was empirically verified.