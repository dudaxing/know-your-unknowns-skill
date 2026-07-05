# 6. The interview

**Hunts:** known unknowns — ambiguities the user knows they haven't resolved.

**Use when:** requirements are vague, conflicting, or have multiple valid architectures. Canonical prompt shape: *"Interview me one question at a time about anything still ambiguous in [feature]. Prioritize questions where my answer would change the architecture."*

## Method

- **Silently build the question list first** from the conversation and the code; don't think aloud through candidate questions at the user.
- **Blast-radius ordering:** architecture and data model > scope and behavior > UX details > cosmetics. Ask first the questions whose answers change system boundaries.
- **One question per turn** — batching produces shallow answers.
- Each question carries: the question, why it matters (what changes downstream depending on the answer), 2–4 concrete options with trade-offs, **a recommended option listed first and marked as recommended**, and **a "default if unanswered"** — the conservative choice that applies if the user skips it. Options let the user react rather than compose; a recommendation gives them something to veto.
- **Never pad with questions the code can answer — go read the code instead.** Skip anything a reasonable default settles.
- If the user answers "I don't know": offer to prototype the alternatives (see [mock-first.md](mock-first.md)) or adopt the recommended default and record it as an assumption — **do not re-ask**.
- If the user asks to proceed without finishing: apply conservative reversible defaults for low-risk items and mark high-risk assumptions prominently in the resulting plan.
- **Stop when remaining ambiguity no longer changes the architecture** — typically 3–8 questions.
- **Never start implementing during the interview.**

## Deliverables

Artifact preferred when there are more than ~4 decisions; otherwise chat is fine.

1. **Decisions table:** question → decision → rationale → what it ruled out. Plus a **deferred-assumptions table**: assumption → why acceptable for now → revisit when.
2. **Implementation-ready prompt:** the original request rewritten with every decision folded in, copyable, ready to start the build.

The interview can run *as* an interactive artifact (questions as sequential cards, options as radio chips, decisions table and final prompt assembled live) or as a chat exchange followed by a summary artifact.
