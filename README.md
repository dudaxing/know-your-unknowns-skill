# Reduce Critical Unknowns for OpenAI Codex

[![Validate Skill](https://github.com/dudaxing/know-your-unknowns-skill/actions/workflows/validate-skill.yml/badge.svg)](https://github.com/dudaxing/know-your-unknowns-skill/actions/workflows/validate-skill.yml)

An evidence-first, risk-proportional Agent Skill for finding and cheaply testing the unknowns that could change a software design, implementation, rollout, or verification strategy.

[中文说明](README.zh.md)

> The repository name is retained for continuity. The primary Skill is now named `reduce-critical-unknowns` and targets OpenAI Codex.

The layout follows OpenAI's current [Build skills](https://learn.chatgpt.com/docs/build-skills) guidance: repository discovery under `.agents/skills`, two-field Skill frontmatter, progressive disclosure, and `agents/openai.yaml` UI metadata.

## What it changes

The original repository organized eleven techniques around interactive page artifacts. This version keeps the useful engineering behavior and removes the fixed medium and ceremony:

- inspect code, tests, history, configuration, schemas, and runtime behavior before asking broad questions;
- find only unknowns that could change the next decision;
- run one cheapest credible probe with an explicit evidence target and stop condition;
- use conservative defaults for local, reversible choices;
- pause only the affected branch when a high-impact, weakly evidenced choice is hard to reverse;
- fold probe results into implementation, tests, rollout, or a compact human decision;
- stop when the next bounded action is safe enough, not when every uncertainty is exhausted.

The runtime Skill does not require page artifacts, a canonical unknowns ledger, numeric risk multiplication, fixed phase gates, or a packaged `.skill` archive.

## Use it for

- unfamiliar authentication, permission, session, or migration work;
- schema and public-contract changes across independently deployed consumers;
- cross-language or cross-runtime semantic ports;
- ambiguous important features whose meaning changes architecture or data boundaries;
- implementation discoveries that invalidate a plan premise;
- rollout, rollback, or observability decisions;
- independent merge-readiness checks for large or high-risk diffs;
- explicit requests for a blind-spot scan, assumption audit, focused interview, design spike, semantics map, deviation triage, or evidence review.

Do not expand typos, formatting, local renames, or well-specified reversible fixes into a full workflow. Even when explicitly invoked, the Skill should keep those tasks to at most one material assumption and proceed.

## Install

### Use directly in this repository

Clone the repository and open Codex from any directory at or below its root. Codex discovers the Skill at `.agents/skills/reduce-critical-unknowns`.

```bash
git clone https://github.com/dudaxing/know-your-unknowns-skill.git
cd know-your-unknowns-skill
```

### Copy into another repository

Copy the Skill folder into that repository's `.agents/skills/` directory:

```powershell
$source = ".agents\skills\reduce-critical-unknowns"
$target = "C:\path\to\your-repo\.agents\skills\reduce-critical-unknowns"
New-Item -ItemType Directory -Force -Path (Split-Path $target) | Out-Null
Copy-Item -Recurse -Force $source $target
```

```bash
mkdir -p /path/to/your-repo/.agents/skills
cp -R .agents/skills/reduce-critical-unknowns /path/to/your-repo/.agents/skills/
```

### Install for the current user

Copy the same folder to `$HOME/.agents/skills/reduce-critical-unknowns`.

## Invoke

Explicit examples:

```text
$reduce-critical-unknowns Add rotating sessions to this legacy auth module. Test the migration and rollback assumptions before enabling writes.
```

```text
$reduce-critical-unknowns Port this Rust retry controller to TypeScript while preserving caller-visible timing, error, retry, and cancellation semantics.
```

```text
$reduce-critical-unknowns Check this large diff's merge readiness by mapping acceptance criteria, rollback, observability, and failure paths to evidence.
```

Codex may also invoke the Skill implicitly when the task matches its frontmatter description.

## Operating model

| Situation | Expected behavior |
|---|---|
| Clear, local, reversible fix | Inspect locally, note at most one material assumption, implement, and run the focused verification. |
| Important but repository-answerable unknown | Inspect the strongest evidence and run one focused probe before asking the user. |
| Human-owned, high-impact, hard-to-reverse choice | Present evidence and a few materially different options; pause only the affected branch. |
| Plan contradicted during implementation | Record premise → evidence → impact → conservative action or escalation. |
| Large or risky diff | Map acceptance criteria to evidence and inspect failure paths, rollback, observability, and the maintainer mental model. |
| Repository unavailable | State the evidence gap, keep claims as hypotheses, and return the first discriminating probe. |

Detailed probe selection and domain-specific risk sweeps load only when needed from the two references.

## Repository structure

```text
.agents/skills/reduce-critical-unknowns/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── probe-playbook.md
    └── risk-patterns.md

evals/reduce-critical-unknowns/
├── trigger-cases.json
├── behavior-scenarios.md
├── forward-test-results.md
├── results.md
└── run_static_checks.py
```

The runtime Skill has four files. Evals, validation records, and repository documentation remain outside the Skill to preserve progressive disclosure.

## Validate

```bash
python -m pip install PyYAML==6.0.3
python -m py_compile evals/reduce-critical-unknowns/run_static_checks.py
python evals/reduce-critical-unknowns/run_static_checks.py
```

Also run the `quick_validate.py` bundled with your current Codex `$skill-creator` against `.agents/skills/reduce-critical-unknowns`.

Current baseline:

- 25 labeled trigger prompts: positive, explicit, immediate, near-negative, and negative;
- 8 behavior scenarios with 54 observable assertions;
- 54/54 assertions passed in explicit independent forward-tests;
- real implicit trigger rate remains unmeasured because the test surface did not expose Skill-load traces.

See [validation results](evals/reduce-critical-unknowns/results.md) and [forward-test results](evals/reduce-critical-unknowns/forward-test-results.md).

## Migrating from the previous Skill

- The invocation name changes from `$know-your-unknowns` to `$reduce-critical-unknowns`.
- Remove an installed copy of the old Skill before installing this one; keeping both may create overlapping triggers.
- The old `dist/know-your-unknowns.skill` archive is removed. The repository-native `.agents/skills/` folder is the source of truth.
- Historical technique names still map to the smallest matching probe, but they no longer force the old output medium, item count, or gate.

## Design lineage

The methodology is informed by Thariq Shihipar's [Know Your Unknowns field guide and companion demonstrations](https://thariqs.github.io/html-effectiveness/unknowns/) and by the previous implementation in this repository. This rewrite re-synthesizes the engineering behavior for OpenAI Codex instead of copying the previous artifact layer.
