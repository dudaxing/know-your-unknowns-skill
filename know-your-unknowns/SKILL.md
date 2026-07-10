---
name: know-your-unknowns
description: Toolkit of 11 techniques for surfacing unknowns before, during, and after software implementation, delivered as self-contained interactive HTML artifacts (based on Thariq Shihipar's "Know Your Unknowns" field guide). Use when starting work in an unfamiliar module or codebase, learning an unfamiliar domain, choosing between UI/design directions, brainstorming solutions to a product problem, clarifying ambiguous requirements, porting code from a reference implementation, writing an implementation plan, running a long build session, pitching a finished change for approval, or verifying understanding before merging a large diff. Triggers include - blindspot pass, unknown unknowns, teach me, design directions, mock it first, brainstorm interventions, interview me, semantics map, reference port, tweakable plan, implementation notes, buy-in doc, pitch doc, merge quiz, quiz me, 盲区扫描, 未知项, 教我, 需求澄清, 访谈我, 问我问题, 出几个设计方向, 做个原型看看, 照着这个实现, 实现计划, 写个实现方案, 记录实现笔记, 提案文档, 打包给评审, 合并前检查, 考考我.
---

# Know Your Unknowns

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

4. **Reacting is easier than imagining.** Users often cannot articulate what they want, but they recognize it instantly when shown. Generate concrete options and let the user react. Every artifact must end with a low-effort response mechanism — steal/skip chips, "this resonates" checkboxes, A/B choices, a copyable assembled reply — so reactions come back as a structured message with minimal typing.

5. **Gate irreversible steps on confirmed understanding.** Require explicit sign-off on a semantics map before porting code; require a passed quiz before merging a risky diff. Understanding must be demonstrated, not assumed.

6. **Ground everything in the actual territory.** Blindspots come from reading the real code and git history, not from generic best practices. Brainstormed interventions cite real files, dormant flags, and unwired backend data. When the territory turns out to be simple and there is little to report, say so — never fabricate findings to fill a format.

7. **Discovery artifacts are scaffolding — keep them out of the changeset.** Mocks, design directions, reports, and note files live in a scratch directory, never inside the app's source tree, and are not committed unless the user asks. In a git repo, add them to `.git/info/exclude` (not `.gitignore`, which would itself dirty the diff).

8. **Host note (Cursor / Claude Code).** Install once under `~/.claude/skills/know-your-unknowns/` — Cursor loads user skills from there; do not duplicate into `~/.cursor/skills`. HTML artifacts open via `file://` or the system browser; scratch paths and `.git/info/exclude` hygiene apply the same in both hosts.

## Choosing a technique

Selection rules:

- **Honor an explicit trigger.** If the user says "interview me," run the interview — never silently substitute a different technique.
- **No default technique triggered?** For non-trivial tasks, run the compact unknowns scan and apply the ask-vs-decide policy from [scan-and-policies.md](references/scan-and-policies.md) — that file also lists the territory-inspection checklist and the failure modes to avoid. End every scan with a **Suggested trigger phrase** (English + Chinese when helpful): one copy-paste sentence the user can send to run the recommended next technique.
- **User asks to implement immediately?** Don't force a pre-implementation ritual: compact scan, ask-or-decide, then implement (with implementation notes if non-trivial).
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
4. **Build the artifact** as one self-contained `.html` file per [artifact-patterns.md](references/artifact-patterns.md), starting from [assets/artifact-skeleton.html](assets/artifact-skeleton.html).
5. **Deliver and collect.** Tell the user the file path, what to do, and what reply to send back. The reply is structured input for the next step.
6. **Fold the answers forward** per the protocol below. Techniques chain — a typical full-feature flow: blindspot pass → interview → tweakable plan → implementation notes → buy-in doc → merge quiz. These are tools, not a mandatory pipeline; run only what the dominant unknowns justify, and when the user has already made a decision an artifact would re-litigate, skip it and proceed.

## Fold-forward protocol

When the user pastes a reply from an artifact's reply builder (or sends an equivalent structured message), treat it as **binding input**, not background prose.

1. **Parse explicitly.** Extract labeled fields: direction choices, steal/skip lists, resonate selections, A/B answers, approve/change per decision, go/no-go, `semantics confirmed`, quiz score, deferred items marked `(unanswered)`.
2. **Apply before acting.** Update the plan, decisions table, or implementation prompt to reflect every parsed choice. Unanswered items stay visible as open assumptions — do not silently fill them in.
3. **Do not ignore and implement.** Never start coding, porting, or merging in the same turn if the pasted reply changes scope, architecture, or gates — acknowledge what changed, then proceed only along the updated path.
4. **Gate phrases are hard stops until satisfied:**
   - Reference port: no code until the user replies **`semantics confirmed`** (or sends corrections to the map).
   - Tweakable plan: no implementation until explicit **go** (or listed tweaks are folded in first).
   - Merge quiz: no merge checklist until **perfect score** on the quiz section.
5. **Chain forward.** After folding, state the next artifact or phase (e.g. "plan updated — open the handoff bundle when you start a fresh implementation session").

## Implementation session handoff

After pre-implementation artifacts are approved (especially a tweakable plan), **start implementation in a fresh session** with a clean context window — per the field guide, planning context is compiled into files, not chat scrollback.

**Bring into the new session (attach or @-mention paths):**

- Approved plan artifact (`.html` or exported decisions)
- Improved implementation prompt / decisions table from interview or blindspot pass
- Approved mock or design-direction artifact if UX was settled there
- Reference semantics map if porting
- `implementation-notes.md` path (create empty or continue existing)

**Leave behind:** exploratory chat, rejected design directions, intermediate brainstorm cards the user did not select.

**First message in the new session** should restate goal + folded decisions + "keep implementation notes per [implementation-notes.md](references/implementation-notes.md)." See that reference for log format and session-end digest.
