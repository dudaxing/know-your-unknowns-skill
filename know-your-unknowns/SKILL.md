---
name: know-your-unknowns
description: An explicitly-invoked toolbox of 11 techniques for surfacing unknowns before, during and after implementation, delivered as interactive HTML artifacts or plain chat — whichever reduces unknowns fastest. Use when the user names a technique below, or asks what they do not yet know: entering unfamiliar code, learning an unfamiliar domain, reacting to design directions, brainstorming interventions, clarifying vague requirements, porting from a reference, planning, logging a long build, pitching finished work, or checking their own understanding before merging. Do NOT take over general docs, specs or RFCs; UI design and building; or code-correctness review — yield to the skill that owns those. Triggers - blindspot pass, unknown unknowns, teach me my unknowns, design directions, mock it first, brainstorm interventions, interview me, semantics map, reference port, tweakable plan, implementation notes, buy-in doc, merge quiz, quiz me, 盲区扫描, 未知项, 教我我的未知, 访谈我, 出几个设计方向, 做个原型看看, 照着这个实现, 可调计划, 记录实现笔记, 打包给评审, 合并前检查, 考考我.
---

# Know Your Unknowns

Based on Thariq Shihipar's "Know Your Unknowns" field guide and its companion HTML demos.

The map is not the territory. The "map" is everything handed to an agent before it starts working — the prompt, the plan, the assumptions. The "territory" is the actual codebase, its history, its undocumented constraints, and the real intent behind the request. The gap between map and territory is the unknowns. Every explainer, brainstorm, interview, prototype, and reference is a cheap way to find out what you didn't know — before it gets expensive to fix.

## The four kinds of unknowns

|  | The user knows it | The user doesn't know it |
|---|---|---|
| **Aware** | Known knowns — already in the prompt | **Known unknowns** — open questions they know they haven't resolved |
| **Unaware** | **Unknown knowns** — taste and knowledge they can't verbalize but recognize on sight | **Unknown unknowns** — what they didn't know to ask |

Diagnose which kind dominates, then pick the technique that hunts it (table below).

## Core principles

1. **Spend tokens on discovery before spending them on implementation.** A blindspot found in five minutes of scanning costs nothing; the same blindspot found in production costs someone's half-day. Front-load the questions whose answers change the architecture.

2. **Anchor on the user's starting point first.** When a technique depends on the user's knowledge state (blindspot pass, teach-me, interview), open with one short message — at most three sub-questions — establishing their experience level, prior familiarity, and decisions already made. Then investigate. Never interrogate at length before delivering value.

3. **Pick the medium that reduces unknowns fastest.** Markdown/chat for short scans, simple plans, and direct answers; a self-contained interactive HTML artifact when layout, comparison, interaction, or quizzes reveal unknowns better than prose — spatial information flattens badly into linear text, and interactivity trades a document the user would skim for one they will actually read. Never produce decorative HTML that reveals nothing prose wouldn't. See [references/artifact-patterns.md](references/artifact-patterns.md) before building any artifact.

4. **Reacting is easier than imagining.** Users often cannot articulate what they want, but they recognize it instantly when shown. Generate concrete options and let the user react. Every artifact **that asks the user to decide something** must end with a low-effort response mechanism — steal/skip chips, "this resonates" checkboxes, A/B choices, a copyable assembled reply — so reactions come back as a structured message with minimal typing. Purely explanatory output (e.g. the teach-me explainer) needs no reply builder.

5. **Hold checkpoints before irreversible steps.** Ask for sign-off on a semantics map before porting code; ask for a passed quiz before merging a risky diff. Understanding should be demonstrated, not assumed. Be honest about what these are: **checkpoints this skill holds, not enforcement.** A skill is text a host loads when it judges the skill relevant — someone who opens a fresh chat and says "merge it" may never load this file at all, in which case no checkpoint exists to bypass. Real enforcement lives outside the model, in host hooks or a restricted permission mode. Never describe a checkpoint in language that implies it physically blocks anything.

6. **Ground everything in the actual territory.** Blindspots come from reading the real code and git history, not from generic best practices. Brainstormed interventions cite real files, dormant flags, and unwired backend data. When the territory turns out to be simple and there is little to report, say so — never fabricate findings to fill a format.

7. **Discovery artifacts are scaffolding — keep them out of the changeset.** Mocks, design directions, and reports live in a scratch directory, never inside the app's source tree. The implementation-notes log is the one exception: it sits at the project root by convention (see [implementation-notes.md](references/implementation-notes.md)) but is still scaffolding. Neither is committed unless the user asks. In a git repo, exclude them via the repo's info/exclude file — resolve its real path with `git rev-parse --git-path info/exclude` rather than hardcoding `.git/info/exclude`, which is wrong in worktrees and submodules where `.git` is a file. Do not use `.gitignore`, which would itself dirty the diff. If the path can't be resolved or the environment is read-only, say so and fall back to chat output rather than writing files.

8. **Host note.** Pick **one** install location per host — do not maintain divergent copies. Each host's native skill roots:

   | Host | Native roots (user / project) |
   |---|---|
   | Claude Code | `~/.claude/skills/` · `.claude/skills/` |
   | Cursor | `~/.cursor/skills/` · `.cursor/skills/` |
   | Codex | `~/.agents/skills/` · `.agents/skills/` |

   These are native paths for their own host, not compatibility shims. A host may additionally load another host's root depending on version and settings — treat that as a bonus, never as the documented install path. After installing or updating, starting a **new chat** is the safe default; Claude Code picks up edits inside an already-known skills directory in-session, but a skills root that did not exist when the session started needs a restart. HTML artifacts open via `file://` or the system browser; scratch-path and info/exclude hygiene (principle 7) applies across hosts.

## Positioning: an invoked toolbox, not a default orchestrator

This skill runs when the user asks for one of its techniques. It does **not** insert itself into ordinary work. Someone who says "add CSV import" gets CSV import, not a discovery ritual.

The single exception is the **compact unknowns scan** in [scan-and-policies.md](references/scan-and-policies.md): a few lines classifying what is known and unknown, ending in a recommended next move. It produces no artifact and interrupts nothing, so it is cheap enough to run by default on non-trivial work. Everything else — including the implementation-notes log — waits to be asked for; recommend, then stop.

**Two paths lead here, and they are not equal.** A host may load this skill *implicitly*, having matched the description against an ordinary request. On that path, run the scan, recommend a technique, and go no further: the user did not ask for a technique, so starting one would be the orchestrator behaviour this positioning rejects. The eleven techniques run on the *explicit* path only — the user named one, or accepted a recommendation. When you cannot tell which path you are on, you are on the implicit one.

### Yielding to neighbour skills

Several installed skills claim adjacent territory. Overlap is resolved by **handing off**, not by competing: produce the structured input this skill is good at, then say which skill should take the deliverable. Never invoke another skill's scripts or reach into its install path — the host does the routing.

| The user wants | This skill's part | Then hand off to |
|---|---|---|
| A proposal, spec, RFC, or decision doc | The interview's decisions table, or a blindspot pass, as input | The documentation/co-authoring skill |
| A dashboard or screen designed and built | Design directions to pick a philosophy; a throwaway mock to settle interaction | The frontend/UI design skill |
| A prototype needing routing, state, or a component library | The interaction contract and the questions the prototype must answer | The web-artifacts/app-building skill |
| A diff checked before merging | The merge quiz — whether *the user* understands the change | The code-review skill, which checks whether *the code* is correct |

That last row is a distinction, not a division of labour: code correctness and reviewer comprehension are separate checks, and **neither one passing means the merge is cleared**.

When a request is ambiguous between this skill and a neighbour, say which reading you took and offer the other in one line.

## Choosing a technique

Selection rules:

- **Honor an explicit trigger.** If the user says "interview me," run the interview — never silently substitute a different technique.
- **No technique named?** For non-trivial tasks, run the compact unknowns scan and apply the ask-vs-decide policy from [scan-and-policies.md](references/scan-and-policies.md) — that file also lists the territory-inspection checklist and the failure modes to avoid. End every scan with a **Suggested trigger phrase** (English + Chinese when helpful): one copy-paste sentence the user can send to run the recommended next technique. Recommend; do not start the technique unasked.
- **User asks to implement immediately?** Don't force a pre-implementation ritual: compact scan, ask-or-decide, then implement. For a long or surprise-prone build, *offer* the implementation-notes log in one line — do not start keeping one unasked, since that is a technique like any other.
- **Over-specific prompts** ("just copy this file", "just add a field") can encode a wrong assumption — verify the premise against the territory before executing literally.

Read the linked reference file for the full workflow before executing.

| # | Situation | Unknowns hunted | Technique | Reference |
|---|-----------|-----------------|-----------|-----------|
| 1 | About to work in unfamiliar code; task sounds simpler than the codebase is | Unknown unknowns | **Blindspot pass** | [blindspot-pass.md](references/blindspot-pass.md) |
| 2 | User lacks the domain vocabulary to prompt precisely | Unknown unknowns (vocabulary) | **Teach me my unknowns** | [teach-me.md](references/teach-me.md) |
| 3 | Visual/UX preferences exist but can't be articulated | Unknown knowns (taste) | **Four design directions** | [design-directions.md](references/design-directions.md) |
| 4 | UI details (placement, density, flow) undecided | Unknown knowns (taste) | **Mock before you wire** | [mock-first.md](references/mock-first.md) |
| 5 | Problem is clear, solution is not | Known unknowns (option space) | **Brainstorm the intervention** | [brainstorm-interventions.md](references/brainstorm-interventions.md) |
| 6 | Requirements are vague or conflicting | Known unknowns (decisions) | **The interview** | [interview.md](references/interview.md) |
| 7 | Porting/reimplementing from a reference | Unknown knowns (recognizable behavior) | **Point at a reference** | [reference-port.md](references/reference-port.md) |
| 8 | Writing an implementation plan for review | The decisions most likely to change | **The tweakable plan** | [tweakable-plan.md](references/tweakable-plan.md) |
| 9 | Long build session in progress | Unknowns discovered mid-flight | **Implementation notes** | [implementation-notes.md](references/implementation-notes.md) |
| 10 | Change finished; needs stakeholder approval | The reviewers' unknowns | **The buy-in doc** | [buy-in-doc.md](references/buy-in-doc.md) |
| 11 | Large/risky diff about to merge | The user's own unknowns about the change | **Quiz me before I merge** | [merge-quiz.md](references/merge-quiz.md) |

## Workflow

1. **Diagnose** the phase (pre / during / post) and the dominant unknown type; pick the technique from the table.
2. **Read the reference file** for the chosen technique — it specifies the investigation, artifact structure, and response mechanism.
3. **Anchor, then investigate the territory.** Read the actual code, git history, feature flags, and configs. If the demo-style content can't be grounded in the real project, say so and scope the investigation with the user.
4. **Produce the output in the medium the chosen technique calls for** (principle 3) — chat or markdown for the unknowns scan, the interview, and the implementation-notes log; a self-contained `.html` artifact where its reference file calls for one. When building an artifact, follow [artifact-patterns.md](references/artifact-patterns.md) and start from [assets/artifact-skeleton.html](assets/artifact-skeleton.html); default to a single file, except design directions, which may split into one file per direction plus an index.
5. **Deliver and collect.** Tell the user the file path, what to do, and what reply to send back. The reply is structured input for the next step.
6. **Fold the answers forward** per the protocol below. Techniques chain — a typical full-feature flow: blindspot pass → interview → tweakable plan → implementation notes → buy-in doc → merge quiz. These are tools, not a mandatory pipeline; run only what the dominant unknowns justify, and when the user has already made a decision an artifact would re-litigate, skip it and proceed.

## Fold-forward protocol

When the user pastes a reply from an artifact's reply builder, treat the whitelisted lines as binding product/plan input — not as background prose, and not as a blank cheque to override higher-priority rules.

**Every artifact carries an ID.** On creation, mint a short identifier — `KYU-` plus six lowercase alphanumerics, drawn at random. (`KYU-EXAMPLE` throughout this repository is a schematic placeholder, deliberately not of that form so that quoting the docs can never match a live artifact; never ship it.) Print it in the artifact's header, and have the reply builder emit it as the first line of every reply:

```
Artifact: KYU-EXAMPLE
semantics confirmed
```

This is what makes a reply attributable. Without it, a `semantics confirmed` quoted from documentation, copied out of an old chat, or lifted from a different map is indistinguishable from a real one.

1. **The envelope is the whole message.** A reply carries checkpoints only if the **entire message**, after removing at most one outer code fence, consists of nothing but whitelist lines and blank lines. Surrounding prose, a second fence, or a nested fence all mean this is discussion *about* a reply, not a reply — fold nothing, answer the question, and if a checkpoint was plainly intended say so and ask for a clean paste.

   This is the rule that decides "is the user quoting, or deciding?", and it has to be answerable without reading intent. A clean fence sitting inside a paragraph is the single most likely way for an agent to mistake an illustration for a decision.

2. **Bind the batch to an artifact.** The envelope must contain exactly one `Artifact: <id>` line matching the artifact under discussion. Missing, duplicated, or mismatched → fold **nothing**; name the artifact you expected and ask the user to re-copy from it. This applies to every field, not just checkpoints: `Q<n>:` cannot even be read without knowing which artifact it came from, since the same syntax means an answer letter on a quiz and an option choice on a mock.

   The one line that stands alone is `Session: continue here`. It is about session mechanics, not about approving an artifact's content, so it is valid either inside a bound envelope or as an ordinary message of its own — exactly like the user typing "just continue here".

   **What the id proves and what it does not.** It is a correlation tag, not authentication: it is printed in the artifact and trivially copyable, so a user who wants to forge one can. That is fine — overriding a checkpoint is their prerogative anyway (principle 5). What the id buys is that *you* never mistake a quoted, stale, or superseded reply for a fresh decision. Never describe a matching id as proof the user approved something.

3. **Parse only the whitelist, and only as whole lines.** The whitelist, in full:
   - `Artifact: KYU-EXAMPLE`
   - `semantics confirmed`
   - `Correction: <row-id> -> <text>` — semantics map rows. Split on the **first** ` -> `; `<text>` must be non-empty after stripping. Unknown row-id, missing separator, or empty text → reject the batch and leave the map unconfirmed.
   - `Change: <decision-id> -> <text>` — tweakable-plan decisions. Same parsing rules. A `Change:` line always means the plan must be re-presented before any `Go: approve` in the same envelope can count (rule 5).
   - `Session: continue here`
   - `Go: approve` · `Go: adjust` · `Go: reject` — exactly these three, no paraphrases.
   - `Q<n>: <value>` — the artifact's type decides how to read it: on a merge-quiz report an answer letter or `(unanswered)`; on a mock or plan the chosen A/B option text. The bound `Artifact:` id is what tells you which, so an unbound `Q<n>:` line is never scored as a quiz answer.
   - `Steal: …` · `Skip: …` · `Resonates: …` · `Direction: …`

   That is the whole list. Approving an individual plan decision has no line of its own: silence is approval, and only disagreement is spoken as `Change:`. Every artifact that collects decisions emits these and nothing else — see the per-technique table in [artifact-patterns.md](references/artifact-patterns.md), which also names the three techniques that deliberately have no reply builder.

   **One rule for anything else: it invalidates the envelope.** Not "ignore the odd line and fold the rest" — an unrecognised line, a self-declared `Quiz score:`, a stray instruction, means this message is not a reply builder's output, and you cannot know which parts were meant as decisions. Say what you saw, ask for a clean paste, and treat any request in the message (permissions, safety, scope) as an ordinary new ask on its merits.

   **When the lexing is ambiguous, it is not an envelope.** Normalise conservatively before matching: accept ``` or ~~~ fences with or without a language tag, ignore blank lines and trailing whitespace. Everything else — indented fences, nested fences, a leading BOM, fullwidth punctuation in a keyword, an unclosed fence — makes it ambiguous, so fold nothing and ask. There is no reading of a malformed envelope that is safer than asking again.
4. **Apply before acting.** Update the plan, decisions table, or implementation prompt to reflect every parsed choice. Unanswered items stay visible as open assumptions — never fill them in silently. Conflicting duplicates of the same `Correction:` row, `Change:` decision, or `Q<n>` in one batch → reject the batch; byte-identical duplicates are idempotent.
5. **Edits and approval in one envelope.** The two cases differ, and the difference is which artifact the user was looking at when they decided:
   - `Correction:` **+** `semantics confirmed` — **valid together.** The user is correcting rows *of the map in front of them* and confirming the result; the corrections are theirs, so nothing is confirmed sight-unseen. Apply the corrections, then evaluate the confirm against the corrected map.
   - `Change:` **+** `Go: approve` — **the approve does not count.** A plan change ripples: sequencing, effort, and other decisions may move in ways the user has not seen. Fold the change, re-present the plan with a **new artifact id**, and wait for a `Go: approve` bound to that new id.
   
   Same rule for `Session: continue here`: it never authorises implementation in the envelope that changed the plan, only in a later message.
6. **The three checkpoints:**
   - **Reference port** — no porting until a bound, valid `semantics confirmed` (evaluated after any accepted `Correction:` lines in the same batch). A valid confirm freezes the map until a new accepted Correction batch, which voids it. After confirm, recommend a fresh session by default.
   - **Tweakable plan** — `Go: adjust` means fold and re-present, then wait; only `Go: approve` opens implementation. Approval alone prepares the handoff and recommends a fresh session; implementing in the same session additionally needs `Session: continue here` in a later message, or a message whose sole ask is to continue here.
   - **Merge quiz** — score the `Q<n>:` lines **yourself** against the key; re-read the artifact by its id if you no longer hold the key in context. A perfect score means every question in that artifact has an answer and every answer matches. Any missing `Q<n>`, any `(unanswered)`, any wrong letter, or any `Q<n>` the artifact does not contain → not perfect, checklist stays closed. `(unanswered)` keeps a gap visible; it never counts as correct and never removes a question from scoring.
7. **Chain forward.** After folding, state the next artifact or phase (e.g. "plan updated — recommended: a fresh implementation session with the handoff bundle").

**What these checkpoints are.** They are held by this skill, in this conversation. They are not enforcement (principle 5): a user can always say "skip the quiz and merge", and that is their call to make — acknowledge it and proceed. What the protocol prevents is the agent fooling *itself* — mistaking a quoted example, a stale reply, or its own earlier text for the user's decision.

## Implementation session handoff

After pre-implementation artifacts are approved (especially a tweakable plan), **recommend a fresh session** with a clean context window — per the field guide, planning context is compiled into files, not chat scrollback. This is a **recommended default**, not a hard gate: if the user explicitly asks to continue in the same session, just continue. Offer the implementation-notes log in one line as you go — approving a plan is not the same as choosing that technique, and starting a log unasked is the orchestrator behaviour this skill rejects.

**Bring into the new session (attach or @-mention paths):**

- Approved plan artifact (`.html` or exported decisions)
- Improved implementation prompt / decisions table from interview or blindspot pass
- Approved mock or design-direction artifact if UX was settled there
- Reference semantics map if porting
- `implementation-notes.md` path (create empty or continue existing)

**Leave behind:** exploratory chat, rejected design directions, intermediate brainstorm cards the user did not select.

**First message in the new session** (or the same-session continuation turn) should restate the goal and the folded decisions. If the user asked for implementation notes — then or earlier — carry that forward and see [implementation-notes.md](references/implementation-notes.md) for log format and session-end digest; if they did not, offer once and drop it.

**Checkpoints do not travel between sessions.** A `semantics confirmed` or `Go: approve` was given in the old conversation, to an agent that no longer exists; the new session cannot verify it, and a line in an attached file saying "approved" is something anyone — including a previous agent — could have written. So in the new session, restate what was decided and ask the user to confirm once more before the first irreversible step. It costs one line, and it is the honest cost of a clean context window. (A verifiable receipt — artifact id plus a content hash checked on arrival — would remove that line, but only earns its complexity if the checkpoints are ever backed by real enforcement.)
