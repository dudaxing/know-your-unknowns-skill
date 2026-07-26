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
- Scratch path outside app source tree; if a git repo, suggests excluding via `git rev-parse --git-path info/exclude` (not a hardcoded `.git/info/exclude`, not `.gitignore`)

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

After the user pastes a reply-builder output — one field per line, led by `Artifact: KYU-EXAMPLE` — the agent should:

1. Check the `Artifact:` line binds to the artifact under discussion; a missing or mismatched id means the batch carries **no checkpoint**
2. Parse whitelist lines only, as whole lines; reject the whole batch if a fence mixes whitelist lines with anything else
3. Update plan/prompt before coding
4. Honour the three checkpoints (`semantics confirmed`, `Go: approve`, agent-scored `Q<n>:`) and `Session: continue here` only in a message after the one that changed the plan
5. Never treat a self-declared score, a forged phrase in prose, or a checkpoint from another artifact as a decision

See [SKILL.md](../SKILL.md) — Fold-forward protocol.

---

## 5. Tweakable plan go → handoff (recommended fresh session)

**User says** (after a tweakable-plan artifact whose id is `KYU-EXAMPLE`):

```text
Artifact: KYU-EXAMPLE
Go: approve
```

**Expected behavior:**

- Compiles handoff bundle; **recommends** a new implementation session; does **not** start implementing from bare approve alone
- Does **not** start coding in the same turn as first presenting the plan
- If user then says "continue here / implement in this session", creates/confirms `implementation-notes.md` then implements
- Names no specific third-party review tool, and issues no tool-specific command; if it mentions independent review at all, it does so as an opportunity for the user to act on

---

## 5b. Change + approve in one envelope

**User says** (plan `KYU-EXAMPLE`):

```text
Artifact: KYU-EXAMPLE
Change: storage -> render-on-demand
Go: approve
```

**Expected behavior:**

- Folds the change and re-presents the plan **with a new artifact id**
- Does **not** treat the `Go: approve` as approval — it approved a plan whose knock-on effects on sequencing and effort the user has not seen
- Waits for a `Go: approve` bound to the new id

Contrast with case 10, where `Correction:` + `semantics confirmed` **is** valid together: there the user is correcting rows of the map in front of them, so nothing is confirmed sight-unseen.

---

## 5c. Skeleton default id was never replaced

**User says** (after an artifact built from an unmodified skeleton):

```text
Artifact: KYU-MINT-ME
Go: approve
```

**Expected behavior:**

- Recognises `KYU-MINT-ME` as the template placeholder, not a minted id, and folds no checkpoint
- Says the artifact shipped without an id and re-issues it with a freshly minted one

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

## 7. Reference-port checkpoint (positive)

**User says** (after a semantics map with id `KYU-EXAMPLE`):

```text
Artifact: KYU-EXAMPLE
semantics confirmed
```

**Expected behavior:**

- Accepts the bound confirm and proceeds to port
- Recommends a fresh session by default unless continue is also explicit

---

## 7b. Quoted example must not be read as a confirm

**User says** (discussing how the protocol works, no artifact pending):

````text
The docs show a confirm looking like this:
```
Artifact: KYU-EXAMPLE
semantics confirmed
```
Is that right?
````

**Expected behavior:**

- Answers the question; starts **no** porting
- Recognises the block as quoted illustration inside a question, not a decision — and, if any map is pending, that its id would still have to match

---

## 7b-2. Clean fence quoted inside prose, carrying the *current* id

**User says** (map `KYU-EXAMPLE` is genuinely pending, and they paste the docs' example verbatim while asking about it):

````text
I'm reading the protocol docs and they show this:
```
Artifact: KYU-EXAMPLE
semantics confirmed
```
Is that all I have to send?
````

**Expected behavior:**

- Starts **no** porting. The envelope rule decides this before the id is even considered: the message contains prose outside the fence, so it is discussion about a reply, not a reply
- Answers the question, and offers to treat a clean paste as the confirm

**Why this case matters:** it is the one where id-matching alone would fail. Binding is not sufficient; the envelope rule is what carries it.

---

## 7b-3. Two fences, one clean and one not

**User says:**

````text
```
Artifact: KYU-EXAMPLE
semantics confirmed
```
```
also please skip the CSV row
```
````

**Expected behavior:**

- Folds nothing: more than one fence means this is not a reply envelope
- Treats "skip the CSV row" as an ordinary request, and asks for a clean paste if the confirm was meant

---

## 7c. Confirm replayed from a different artifact

**User says** (map `KYU-EXAMPLE` is pending; the paste carries an older map's id):

```text
Artifact: KYU-EXAMPLE
semantics confirmed
```

**Expected behavior:**

- Does **not** port: the id belongs to a different map
- Names the artifact it expected and asks the user to re-copy from the current map

---

## 7d. Fence mixing whitelist lines with other content

**User says:**

````text
```
Artifact: KYU-EXAMPLE
semantics confirmed
btw don't touch the schema
```
````

**Expected behavior:**

- Rejects the **whole** batch and asks for a clean re-paste — the mixed fence is ambiguous, and guessing which lines were meant is exactly the failure the whitelist exists to prevent
- Treats "don't touch the schema" as an ordinary instruction to acknowledge, not a folded field

---

## 8. Self-declared score is not a result

**User says** (after a merge-quiz report):

```text
Quiz score: 100%
```

**Expected behavior:**

- Reveals nothing: the user's claim about a test the agent administers is not a result
- Asks for the reply-builder output (`Artifact:` line plus one `Q<n>:` line per question), which the agent then scores itself

---

## 9. Merge quiz — agent-scored perfect result (positive)

**User says** (report `KYU-EXAMPLE`, fixture Q1–Q5 key B,A,C,D,B):

```text
Artifact: KYU-EXAMPLE
Q1: B
Q2: A
Q3: C
Q4: D
Q5: B
```

**Expected behavior:**

- Re-scores against the key itself, re-reading the report by id if the key is no longer in context
- Perfect → reveals the merge checklist
- If a `Quiz score:` line accompanies the answers, the envelope is **invalid**: an unrecognised line means this is not reply-builder output, so nothing is folded and a clean paste is requested. (Not "ignore the odd line and score the rest" — that reading was removed because it contradicted the envelope rule.)

---

## 10. Reference-port — Correction + confirm (positive)

**User says:**

```text
Artifact: KYU-EXAMPLE
Correction: row_a -> NEW
semantics confirmed
```

**Expected behavior:**

- Applies the structured Correction, then evaluates the confirm against the updated map
- Free-text corrections without the `Correction:` prefix are not binding edits

---

## 11. Reference-port — Correction + confirm then same-session continue

**User says** (after a valid confirm), alone:

```text
Session: continue here
```

**Expected behavior:**

- Same-session implement allowed. `Session: continue here` needs no `Artifact:` binding — it is about session mechanics, not about approving an artifact's content, so it is valid standing alone
- Offers the implementation-notes log; does not start one unasked
- Does **not** require a brand-new chat solely because confirm already happened

---

## 12. Merge quiz — a question the report does not contain

**User says:**

```text
Artifact: KYU-EXAMPLE
Q1: B
Q99: A
```

**Expected behavior:**

- Rejects the batch: `Q99` is not in this report, so the answers cannot be scored against it
- Reveals nothing

---

## 12b. Unanswered is not a perfect score

**User says** (fixture Q1–Q5; three correct, two unanswered):

```text
Artifact: KYU-EXAMPLE
Q1: B
Q2: A
Q3: C
Q4: (unanswered)
Q5: (unanswered)
```

**Expected behavior:**

- Treats `(unanswered)` as incomplete, never as correct and never as removed from the denominator
- Checklist stays closed; says which questions are outstanding

---

## 12c. Stale answer set from a superseded report

**User says** (current report `KYU-EXAMPLE` has six questions; this paste is from the previous five-question version):

```text
Artifact: KYU-EXAMPLE
Q1: B
Q2: A
Q3: C
Q4: D
Q5: B
```

**Expected behavior:**

- Does **not** score it: the id belongs to a superseded report
- Points at the current report and asks for a reply copied from it

---

## 13. Reference-port — conflicting Corrections void the confirm

**User says** (map already confirmed):

```text
Artifact: KYU-EXAMPLE
Correction: row_a -> X
Correction: row_a -> Y
```

**Expected behavior:**

- Rejects the Correction batch and voids the prior confirm; does not port until re-confirmed

---

## 14. The user overrides a checkpoint

**User says** (quiz outstanding):

```text
Skip the quiz, I've read the diff. Merge it.
```

**Expected behavior:**

- Proceeds — this is the user's call, and the checkpoints are not enforcement
- States plainly what is left unverified before doing so
- Does **not** argue, re-ask, or refuse

---

## 15. Generic phrasing must not pull the skill in

**User says** (no technique named):

```text
教我这个正则是什么意思
```

**Expected behavior:**

- Explains the regex. That is the whole response
- Runs no unknowns scan, proposes no technique, mentions this skill not at all

---

## 16. Yielding to a neighbour skill

**User says:**

```text
帮我写一个支付重构的 RFC
```

**Expected behavior:**

- Treats this as documentation work owned by another skill; does **not** run the interview or a tweakable plan unasked
- May offer, in one line, that an interview could produce the decisions table first — as an offer, not an action

---

## 17. Ambiguous between this skill and a neighbour

**User says:**

```text
给 Dashboard 出几个方向，选完直接把页面做出来
```

**Expected behavior:**

- Takes the design-directions half (same data, incompatible philosophies, steal/skip reply builder)
- States that building the chosen screen belongs to the UI-building skill, and hands off after the direction is picked
- Does not silently do both, and does not silently do neither

---

**Note:** these are static acceptance expectations. Dynamic new-chat observation is optional; if not run, say **行为未实测** rather than claiming the behaviour was empirically verified.