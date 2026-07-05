# know-your-unknowns

*A Claude Code skill for discovering what you don't know — before it gets expensive to fix.*

[中文文档 / Chinese README](README.zh.md)

Based on Thariq Shihipar's **"Know Your Unknowns"** field guide and its [companion HTML demos](https://thariqs.github.io/html-effectiveness/unknowns/). The premise: **the map is not the territory.** The "map" is everything you hand an AI agent before it starts — the prompt, the plan, the assumptions. The "territory" is the actual codebase, its history, its undocumented constraints, and the real intent behind the request. The gap between them is your unknowns, and every technique in this skill exists to close that gap deliberately instead of discovering it through rework.

## What you get

**11 techniques** covering the full development lifecycle, delivered as **self-contained interactive HTML artifacts** — not walls of markdown — plus a cross-cutting policy layer that applies even when no specific technique is triggered.

### The four kinds of unknowns

|  | You know it | You don't know it |
|---|---|---|
| **Aware** | Known knowns — already in the prompt | **Known unknowns** — open questions you know you haven't resolved |
| **Unaware** | **Unknown knowns** — taste you can't verbalize but recognize on sight | **Unknown unknowns** — what you didn't know to ask |

### The 11 techniques

| # | Phase | Technique | Hunts | Trigger examples |
|---|-------|-----------|-------|------------------|
| 1 | Pre | **Blindspot pass** — scan unfamiliar code + git history, report landmines as cards with copyable prompt fixes | Unknown unknowns | "blindspot pass", "盲区扫描" |
| 2 | Pre | **Teach me my unknowns** — interactive explainer with vocabulary ladder and live controls | Missing vocabulary | "teach me my unknowns", "教我" |
| 3 | Pre | **Four design directions** — same data, 3–5 incompatible design philosophies, steal/skip chips | Unknown knowns (taste) | "design directions", "出几个设计方向" |
| 4 | Pre | **Mock before you wire** — throwaway clickable mock with fake data and A/B questions | Unknown knowns (interaction) | "mock it first", "做个原型看看" |
| 5 | Pre | **Brainstorm the intervention** — ~10 codebase-grounded options, cheapest to most ambitious | The option space | "brainstorm interventions" |
| 6 | Pre | **The interview** — one question at a time, ordered by architectural blast radius | Known unknowns | "interview me", "访谈我" |
| 7 | Pre | **Point at a reference** — semantics map proving comprehension, sign-off gate before porting | Recognizable-but-indescribable behavior | "semantics map", "照着这个实现" |
| 8 | Pre | **The tweakable plan** — sorted by likelihood-of-tweaking, mechanical work collapsed, explicit go/no-go | The decisions most likely to change | "implementation plan", "实现计划" |
| 9 | During | **Implementation notes** — dated log of every plan deviation and conservative choice | Unknowns discovered mid-flight | "keep implementation notes", "记录实现笔记" |
| 10 | Post | **The buy-in doc** — demo first, objections pre-answered with linked evidence, named sign-offs | The reviewers' unknowns | "pitch doc", "提案文档" |
| 11 | Post | **Quiz me before I merge** — merge-readiness report gated by a six-question comprehension quiz | Your own unknowns about the change | "quiz me", "考考我" |

### The cross-cutting layer

Even when no technique is triggered, the skill provides defaults for any non-trivial task ([references/scan-and-policies.md](know-your-unknowns/references/scan-and-policies.md)):

- **The unknowns scan** — a 7-line pre-flight classification of what's known, unknown, and suspected, ending in a recommended next move.
- **Ask-vs-decide policy** — pause for architecture/data/permissions/rollout decisions; decide-and-log (with an assumption record) for local, reversible, conventional ones.
- **Territory inspection checklist** — flags, migrations, legacy data, reverted PRs, env splits, existing utilities, reviewer expectations.
- **14 failure modes to avoid** — e.g. copying the most-similar file without checking it's an exception; treating dev/staging behavior as production truth; treating a passing unit test as proof of permission safety.

### The signature interaction: the reply builder

Every decision-seeking artifact ends with a **reply builder**: steal/skip chips, "this resonates" checkboxes, and A/B choices accumulate into a structured, copyable reply the user pastes back into chat. *Reacting is easier than imagining* — the user clicks instead of composing, and the agent receives structured input instead of prose. A working skeleton implementing these mechanics ships in [assets/artifact-skeleton.html](know-your-unknowns/assets/artifact-skeleton.html).

## Installation

### Claude Code (personal skill)

```bash
git clone https://github.com/dudaxing/know-your-unknowns-skill.git
cp -r know-your-unknowns-skill/know-your-unknowns ~/.claude/skills/
```

On Windows (PowerShell):

```powershell
git clone https://github.com/dudaxing/know-your-unknowns-skill.git
Copy-Item -Recurse know-your-unknowns-skill/know-your-unknowns "$env:USERPROFILE\.claude\skills\"
```

New sessions pick it up automatically. Verify by asking Claude Code: *"Do a blindspot pass on the auth module."*

### Packaged `.skill` file

[dist/know-your-unknowns.skill](dist/know-your-unknowns.skill) is the validated, packaged distribution (a zip with a `.skill` extension) for platforms that accept skill uploads.

## Usage examples

```text
I've never touched this codebase's payment module. Do a blindspot pass before I prompt you to add a refund flow.
```

```text
Interview me one question at a time about the export feature. Prioritize questions where my answer would change the architecture.
```

```text
This Rust crate has exactly the backoff behavior we need. Build a semantics map first — I'll reply "semantics confirmed" before you port anything.
```

```text
出几个设计方向让我挑，同一份数据，风格差异要大，带 steal/skip 选项。
```

```text
Create a merge-readiness report for this diff with a quiz I must pass before merging.
```

Techniques chain naturally — a typical full-feature flow: blindspot pass → interview → tweakable plan → implementation notes → buy-in doc → merge quiz. But this is **a toolbox, not a pipeline**: the skill picks only what the dominant unknowns justify.

## Repository structure

```
know-your-unknowns/            The skill (copy this directory to ~/.claude/skills/)
├── SKILL.md                   Core: principles, technique selection table, workflow (~120 lines)
├── references/                Loaded on demand, one file per technique
│   ├── scan-and-policies.md   Cross-cutting: unknowns scan, ask-vs-decide, failure modes
│   ├── artifact-patterns.md   HTML artifact construction rules + reply-builder spec
│   ├── blindspot-pass.md      … through …
│   └── merge-quiz.md          (11 technique files total)
└── assets/
    └── artifact-skeleton.html Reusable single-file skeleton: chips, checkboxes, reply builder
dist/
└── know-your-unknowns.skill   Packaged distribution
```

The layout follows **progressive disclosure**: only the ~100-word description sits in context permanently; the SKILL.md body loads when the skill triggers; each technique's reference file loads only when that technique runs. Using one technique never pays the context cost of the other ten.

## Design lineage

This skill synthesizes three sources, keeping the best of each:

1. **[Thariq's companion demos](https://thariqs.github.io/html-effectiveness/unknowns/)** (primary) — all 11 techniques with their full interactive depth: the seven blindspot categories, the semantics map's "load-bearing detail" annotations, the reply-builder mechanics.
2. **[GreatMark/fable-field-guide-skills](https://github.com/GreatMark/fable-field-guide-skills)** — behavioral rules (anchor on the user's starting point first; recommend an option in every interview question; push one design direction beyond stated taste) and artifact hygiene (scratch directories, `.git/info/exclude`, never committing scaffolding).
3. **An `unknowns-driven-development` variant** — the cross-cutting policy layer: the default unknowns scan, the ask-vs-decide policy, and the failure-modes list.

## Credits

Methodology by [Thariq Shihipar](https://thariqs.github.io/) (Anthropic), from the "Know Your Unknowns" field guide and the HTML-effectiveness companion demos. This repository is an independent skill implementation for AI coding agents.
