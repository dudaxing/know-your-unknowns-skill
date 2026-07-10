# Smoke triggers — acceptance cases

Use these to verify the skill triggers correctly and folds structured replies. Run manually in Claude Code or Cursor after installing `know-your-unknowns` under `~/.claude/skills/`.

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

1. Parse labeled fields explicitly
2. Update plan/prompt before coding
3. Respect gates (`semantics confirmed`, quiz perfect score, plan go/no-go)

See [SKILL.md](../SKILL.md) — Fold-forward protocol.
