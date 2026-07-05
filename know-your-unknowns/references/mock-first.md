# 4. Mock before you wire

**Hunts:** unknown knowns — interaction preferences that only surface on click. "You'll find out what you actually want the moment you can click it, not three PRs later."

**Use when:** UI decisions (placement, density, interaction flow) are undecided and the design direction is already roughly settled (otherwise start with [design-directions.md](design-directions.md)).

## Rules

- One throwaway HTML file, fake-but-realistic data, zero backend, zero integration with the real app.
- Build the 2–3 competing variants *in the same file* so they can be toggled and compared.
- Note in the artifact where the real implementation will live (e.g. `apps/player/src/annotate/Toolbar.tsx` behind a feature flag) so the mock is explicitly disposable.
- The mock lives in a scratch directory, is never committed, and goes in `.git/info/exclude` in a git repo.

## Artifact structure

- Working clickable mock of each layout variant (e.g. toolbar as floating pill bottom-center that hides during playback, vs docked left rail always visible, vs strip under the seekbar costing ~56px of height).
- **A/B question blocks** for every open decision, as radio/chip choices, e.g.: Q1 which placement ships? Q2 controls always visible in the bar or collapsed behind a popover? Q3 does the drawer overlay the content or push it aside? Q4 include feature X in v1 (with its cost named) or defer to v1.1?
- Sticky reply builder assembling all answers into a copyable structured reply.

## Quality bar

Interactions must actually work (click to place an annotation, open the drawer). A static screenshot grid defeats the purpose.
