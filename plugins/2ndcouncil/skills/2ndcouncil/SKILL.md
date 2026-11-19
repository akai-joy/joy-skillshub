---
name: 2ndcouncil
description: Convene a 5-persona advisory council of Claude subagents (Contrarian, First-Principles, Expansionist, Outsider, Executor) to pressure-test a decision. Members answer independently, then peer-review each other anonymously, then an Opus council head decides. Use when the user says "2ndcouncil", "convene the second council", "run the 2nd council on...", "pressure-test this with the council", or asks to stress-test a hard, expensive-to-reverse decision with multiple perspectives.
---

# 2nd Council

A 5-member advisory council built from Claude subagents. Unlike `llm-council` (which calls external model APIs), this skill spawns **Claude subagents** as the council members. Members run on **Sonnet**; the council head runs on **Opus**.

## ⛔ READ THIS FIRST — the #1 failure mode

**You MUST spawn all 5 members before forming any opinion. Do NOT answer the question yourself first, and do NOT let your own view leak into the members' prompts or the final verdict.** Your job is to run the council and synthesize *what the council produced* — not to decide and then dress it up. If you find yourself writing the answer before Round 1 has returned, stop and spawn the members.

## When to convene

Only when being wrong is expensive and hard to reverse — architecture bets, strategy, irreversible launches, hard tradeoffs. For quick factual or low-stakes questions, just answer directly; the council is overkill.

## The three rounds

### Round 1 — Independent answers (parallel, Sonnet)

Spawn **all 5 members in parallel in a single message** (5 `Agent` calls in one block). Each member sees **only the framed question** — never each other, never your opinion. Use `subagent_type: "general-purpose"` and `model: "sonnet"`.

Frame the question neutrally first: state the decision plainly, include the minimum context needed (relevant facts from the conversation / repo), and strip any language that signals which way you lean.

Every member prompt MUST contain:
1. Their persona + their **forbidden move** (below).
2. The instruction: *"Reason from your own knowledge ONLY — do NOT use any tools, do NOT read files, do NOT search the web. Just think and answer."*
3. The fixed output schema (below) — this is what makes Rounds 2 and 3 tractable.

**The five members and their forbidden moves:**

| Member | Charter | FORBIDDEN MOVE |
|---|---|---|
| **The Contrarian** | Name exactly what will fail and why. | May not validate, praise, or hedge any part of the proposal. Assume it goes badly and explain how. |
| **The First-Principles Thinker** | Strip the question to fundamentals; ask whether this is even the right problem. | May not accept the user's framing, terminology, or stated goal as given. |
| **The Expansionist** | Find the hidden upside, the 10x version, the adjacent opportunity being undersold. | May not mention risks, costs, or reasons it won't work; may not think incrementally. |
| **The Outsider** | React as an intelligent layperson who knows nothing about this industry; catch curse-of-knowledge, jargon, and unstated assumptions. | May not use domain jargon or assume any insider context; must flag everything that is confusing or taken for granted. |
| **The Executor** | Say only what to actually do tomorrow morning — concrete steps, sequence, owners. | May not discuss theory, vision, or anything beyond the next concrete actions; every line must be doable. |

**Fixed member output schema** (put this verbatim in each Round 1 prompt):
```
POSITION: <one line>
KEY POINTS:
- <3 to 5 bullets>
TAKEAWAY: <one line>
```

### Round 2 — Anonymous peer review (fresh re-spawn, Sonnet)

Do **not** continue the Round 1 agents. **Spawn fresh Sonnet reviewers** so anonymization is clean (a fresh reviewer never saw its own answer and cannot partially de-anonymize). Spawn the review batch in parallel too.

Before sending answers to reviewers:
- **Shuffle** the 5 answers and **strip persona tells** (remove "As the Contrarian…", remove anything that names a role). Label them **Response A / B / C / D / E**.
- Give each reviewer the full anonymized set.
- **Relax the forbidden move for the review only** — e.g. the Expansionist is now allowed to name a blind spot. Tell reviewers to judge on merit, not style.

Reviewer output schema:
```
RANKING: <best to worst, e.g. "C > A > E > B > D">
STRONGEST ANSWER: <letter + one-line why>
BIGGEST BLIND SPOT ACROSS ALL: <one line>
WHAT'S MISSING: <one line>
```
You can run 3–5 reviewers (a reviewer may review the set including a slot that was its own Round-1 answer — that's fine since it's anonymized). Keep it simple: spawn 5 reviewers, one per shuffled set, or 3 reviewers over the same set.

### Round 3 — The council head decides (Opus)

**The head MUST run on Opus.** If the currently active model is Opus, do the synthesis yourself. **If the active model is not Opus, spawn a dedicated `model: "opus"` agent to produce the verdict** — this honors "Opus for the council head" in every session.

The head decides **from the council's output**, not from a fresh independent take. **Forbidden: substituting your own opinion for the council's findings.** Weigh the answers and the peer reviews, then produce:

```
VERDICT: GO | NO-GO | RECONSIDER
STRONGEST CASE: <the most compelling argument the council surfaced>
KEY OBJECTION: <the single most important risk/counterpoint>
MINORITY DISSENT: <name the strongest disagreeing view explicitly — do not average it away>
NEXT-DAY ACTION: <one concrete thing to do tomorrow>
```
Take a position. Do not average into mush.

## Output to the user

1. **Inline:** the Round 3 verdict block, plus 3–6 of the sharpest highlights (best lines from members + the peer-review consensus on strongest answer / biggest blind spot).
2. **Transcript file:** write the full record — framed question, all 5 Round-1 answers, all peer reviews, and the verdict — to `~/.claude/2ndcouncil/council-<YYYYMMDD-HHMMSS>.md`. Create the directory if needed. Tell the user the path so they can open the detail.

## Mechanics notes

- Round 1 = 5 parallel spawns; Round 2 = 3–5 parallel spawns; Round 3 = self (Opus) or 1 spawn. ~9–11 spawns total. This is intentional — only convene for decisions that justify it.
- Members are **stateless charters**: each spawn carries its full persona in the prompt, so fresh re-spawns in Round 2 are correct, not lossy.
- Verified working: Sonnet members reason with `tool_uses: 0` when told "no tools"; fresh-spawn anonymized peer review produces clean rankings. Keep the "no tools" instruction in member prompts — it's what keeps them fast and on-task.
