---
name: pre-mortem
description: >-
  Run a structured pre-mortem before committing to a plan, launch, migration,
  feature, refactor, or any high-stakes decision. A pre-mortem imagines the plan
  has already failed and works backwards to surface failure modes, rank them by
  likelihood and impact, identify early-warning signs, and propose concrete
  mitigations — so risks get caught while they're still cheap to fix. Use this
  skill whenever the user is about to ship/launch/migrate/cut over, asks "what
  could go wrong", "what are we missing", "is this ready", "what are the risks",
  "stress-test this plan", "poke holes in this", or wants a go/no-go gut-check —
  even if they don't say the words "pre-mortem". Prefer this over an ad-hoc list
  of risks: the failure-first framing surfaces things a normal review misses.
---

# Pre-Mortem

## What this is and why it works

A pre-mortem is the opposite of a post-mortem. A post-mortem asks "why did this
fail?" after the fact. A pre-mortem asks the same question *before* you commit —
by **assuming the plan has already failed** and working backwards to explain how.

The framing is the whole trick. Asking "what are the risks?" produces a bland,
hedged list because the mind is still defending the plan. Asking "it's six
months from now and this was a disaster — what happened?" flips the brain into
*prospective hindsight*: you're no longer predicting whether it fails, you're
explaining a failure that (in the exercise) already happened. Klein's research
found this framing raises the number and specificity of causes people identify
by ~30%. It also makes it socially safe to name doubts, because you're describing
a hypothetical past, not attacking the plan.

So the job of this skill is not to produce a generic risk register. It's to tell
**specific, plausible failure stories**, then turn the most dangerous ones into
things the user can act on today.

## Before you start: ground the analysis

A pre-mortem is only as good as its grounding. Generic risks ("there might be
bugs", "scope could creep") are worthless — the user already knows those. The
value is in failure modes specific to *this* plan, *this* codebase, *this*
timeline.

So first, gather what you can:
- **Read the actual artifacts.** If there's a plan doc, a PR, a spec, code, a
  CLAUDE.md, deployment config — read them. Concrete failure modes come from
  concrete details (an undeployed rule, an unbounded query, a hard external
  deadline, a single owner for a critical step).
- **Pull in what you already know** from the conversation. If you've been working
  with the user, you likely already know where the bodies are buried. Use it.

Then nail down three things. Ask the user only for what you genuinely can't infer
— don't interrogate; propose sensible defaults and let them correct you:

1. **The subject** — what exactly is being committed to? State it in one sentence.
2. **The horizon** — by when do we judge success/failure? ("the closed beta",
   "30 days after cutover", "end of the quarter"). Failure modes are different at
   1 week vs 1 year.
3. **What "failure" means here** — concrete and severe. Not "it's not perfect"
   but "we had to roll back", "testers churned and gave no usable feedback",
   "we corrupted production data", "we blew the budget", "we missed the deadline
   and shipped broken". Pick the failure(s) that would actually hurt.

## Step 1 — Imagine total failure, then diverge

State the premise out loud, dated to the horizon: *"It's [horizon]. [Subject] has
failed — [definition of failure]. Here's how it happened."*

Now **generate failure modes widely before judging any of them.** Diverge first;
you'll prioritize later. The most dangerous risk is often not the first one you
think of, and early convergence kills the exercise. Aim for breadth across these
lenses (not every category applies to every plan — skip the irrelevant ones, and
add ones specific to the domain):

- **Technical / correctness** — bugs, edge cases, data loss, race conditions,
  performance under real load, rollback that doesn't actually work.
- **Integration / dependencies** — third-party APIs, services, libraries, other
  teams. What breaks if a dependency is flaky, rate-limited, down, or changes?
- **Deployment / operational** — config that was never applied, environment
  drift, secrets/permissions, missing monitoring, no rollback path, the deploy
  itself.
- **Product / adoption** — users don't understand it, don't want it, can't find
  the value, hit friction and bounce. The thing works but no one cares.
- **Data / correctness of content** — stale, wrong, empty, or embarrassing
  output (especially for AI-generated content).
- **Cost / scale** — unbounded spend, costs that look fine in testing and
  explode at scale, quota exhaustion.
- **Legal / compliance / trust** — privacy, consent, platform review gates
  (App Store, etc.), user-generated or AI content liability, security exposure.
- **People / process** — single point of failure (one person knows the thing),
  unclear ownership, no feedback channel, communication gaps, key person
  unavailable.
- **External / timing** — competitors, market timing, seasonality, hard external
  deadlines you don't control.

For each failure mode, write it as a **short causal story**, not a label.
"Performance" is a label. "At 200 concurrent users the feed query does a full
collection scan because there's no composite index, response times hit 8s,
testers think the app is broken and stop opening it" is a failure mode you can do
something about. Specificity is the entire value.

## Step 2 — Assess each failure mode

For each mode, judge four things. Keep it lightweight — rough bands, not false
precision:

- **Likelihood** — High / Medium / Low. How plausible is this story, honestly?
- **Impact** — High / Medium / Low. If it happens, how bad? (A High/High is a
  "this could sink it"; a Low/Low is noise — don't spend words on it.)
- **Early warning sign** — what would you *observe* first if this were starting
  to happen? This is what turns a risk into something monitorable. ("Error rate
  on uploads climbs", "first three testers all ask the same confused question",
  "daily TTS cost ticks past $X".) A failure mode with no detectable signal is
  more dangerous and deserves a stronger upfront mitigation.
- **Controllable?** — can you reduce this, or only watch for it? Distinguish
  risks you own from risks you can only hedge against. Don't waste mitigation
  effort trying to control the uncontrollable; for those, plan the response.

Rank by likelihood × impact. The top few are where all the value is.

## Step 3 — Turn the top risks into action

For each of the top risks (usually 3–6), give a **concrete mitigation** and
classify it:

- **Fix now** — cheap or critical enough that it should happen before committing.
  Be specific about the action ("deploy the storage rules", "add the composite
  index", "write the privacy-policy page"), and note the rough cost/effort.
- **Watch** — not worth pre-empting, but set up the early-warning sign so you
  catch it if it starts. Name the signal and the threshold.
- **Accept** — acknowledge it, decide it's a tolerable risk, and move on. Saying
  "we accept this" explicitly is a real outcome — it stops the same worry
  resurfacing later.

A good pre-mortem usually *shrinks* the action list rather than growing it: it
separates the two or three things that genuinely must happen first from the long
tail of worries that can be watched or accepted.

## Output format

Produce a report in this structure. Keep it tight — this is a decision aid, not a
document to file away.

```
# Pre-Mortem: [Subject]

**Premise:** It's [horizon]. [Subject] failed — [definition of failure].
**Grounding:** [one line on what this is based on — files read, context known]

## Top failure stories
[The 2–4 most dangerous modes, each as a short narrative paragraph. Lead with
these — they're the point. Make them concrete enough to feel real.]

## Risk table
| Failure mode | Likelihood | Impact | Early warning sign | Verdict |
|---|---|---|---|---|
| [short causal description] | H/M/L | H/M/L | [observable signal] | Fix now / Watch / Accept |
[ordered by likelihood × impact, highest first]

## Fix now (before committing)
[Numbered, concrete, ordered by priority. Each: the action + rough effort.
If something is actively broken today, say so plainly and put it first.]

## Watch
[Risks to monitor, each with the signal + threshold that should trigger a response.]

## Accept
[Risks consciously tolerated, one line each.]

## Bottom line
[2–3 sentences: is the biggest threat what the user expected, or something else?
What's the single most important thing to do before proceeding?]
```

## Principles that keep a pre-mortem honest

- **Be specific or be silent.** A vague risk is worse than no risk — it adds
  noise and false comfort. If you can't tell a concrete story about how something
  fails, either dig until you can or drop it.
- **Look where the user isn't looking.** The user has already thought about the
  obvious risks in their domain. Earn your keep on the non-obvious: the
  operational gap behind the shiny feature, the dependency everyone assumes is
  fine, the thing that's *already* broken but hasn't surfaced yet.
- **Separate "scary" from "likely."** Dramatic failure modes crowd out boring
  probable ones. The thing that actually sinks projects is usually mundane (a
  config never applied, a missing index, no feedback channel) — not the
  exotic disaster. Rank by likelihood × impact, not by drama.
- **Don't sandbag and don't catastrophize.** The goal is calibrated honesty. If
  the plan is mostly sound, say so and keep the list short. Inventing risks to
  look thorough wastes the user's attention; a pre-mortem with 15 "High" risks is
  useless because nothing stands out.
- **End with a decision, not a worry list.** The deliverable is "here are the two
  things to fix first, here's what to watch, the rest is acceptable" — something
  the user can act on, not a cloud of anxiety.
