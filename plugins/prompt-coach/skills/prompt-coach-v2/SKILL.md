---
name: prompt-coach-v2
description: >
  Use when the user wants a role-tailored Claude rollout or enablement sheet that covers Claude's
  newer products and surfaces, not just chat: Claude for Excel / Microsoft 365, Claude Tag (Claude in
  Slack), Claude in Chrome, Cowork, Claude Code, Claude Docs, connectors and skills. Triggers on
  "what's new in Claude for my team", "which Claude products should we roll out", "Claude across Excel
  and Slack", "enablement sheet with the new features", "AI rollout plan for [role/team]". Do NOT use
  for non-work requests or general prompt-engineering theory.
---

# Purpose

Produce a copy-paste-ready enablement sheet that tells someone at a Team/Enterprise org which Claude
products fit their role, with a ready-to-run prompt for each and a clear flag wherever access depends
on plan or admin settings. Output the sheet itself, not a talk about prompting.

# Before you write

1. **Gather context once.** You need: company, role, mandate (what the sheet is for), and 1–2
   sentences on current projects. Also useful: plan (Team/Enterprise), Microsoft 365 or Google
   Workspace, Slack or not. Ask only for what the user hasn't already told you, and ask once. If they
   answer partly or skip it, go ahead and state your assumptions in one line at the top.

   **Use the structured question tool if one is available** (`AskUserQuestion` in Claude Code, or
   the app's built-in clarifying-question tool), not prose. The user gets clickable options, and the
   answers map directly to Product selection. Send these in one call, leaving out any the user
   already answered (each question gets an automatic "Other" free-text option):

   | Header | Question | Options |
   |---|---|---|
   | Role | Which best describes your role? | Finance & ops / Sales & customer-facing / Engineering & data / Marketing, HR, legal or PM |
   | Mandate | What's this sheet for? | My own day-to-day work / Rolling Claude out to my team / A specific project / Evaluating Claude for the org |
   | Tools (multi-select) | Which does your org use? | Microsoft 365 / Google Workspace / Slack / Microsoft Teams |
   | Plan | Which Claude plan are you on? | Team / Enterprise / Not sure |

   Then ask in one plain line for the company name and 1–2 sentences on current projects, unless
   already given. If no question tool is available, ask the same things as one short numbered list.

   **How the mandate shapes the sheet:** "Rolling Claude out to my team" moves **Ask your admin**
   right after the summary, written so it can be forwarded as-is. "A specific project" points most
   Table 2 rows at that project. "Evaluating Claude for the org" adds a Research row comparing
   rollout options. "Not sure" on plan means every plan-gated row uses the generic
   `Plan-dependent:` wording.
2. **Read `reference/products.md`.** It is the only source for product facts, setup steps and access
   gating. Never invent a UI path, menu name, plan tier or install command that isn't in it.
3. **Check freshness.** If the catalog's `Last verified` date is more than ~90 days old and web search
   is available, check the gated items you plan to recommend against support.claude.com /
   claude.com/docs / code.claude.com. Wherever the catalog and the live docs disagree, trust the live
   docs and tell the user.

# Output, in this order

1. **Summary**: up to 3 sentences on the company and role, plus a one-line assumptions note if needed.
2. **Table 1: "Get Started with Claude"**: 5–7 rows of things they can do today in claude.ai or the
   desktop app with no admin involvement.
3. **Table 2: "Go Further with Claude"**: 3–6 rows using the newer products picked for this role (see
   Product selection).
4. **Prompts**: every full prompt, each in its own fenced code block, labelled to match the table
   (`G1`, `G2`… for Table 1, `F1`, `F2`… for Table 2).
5. **Ask your admin**: a checklist of every gated item used on the sheet (see Permissions).
6. **Next steps + links**: from `templates/next_steps.md`.

## Table format (both tables)

`# | Use Case | Product | What to do | Notes`

- **#**: the prompt label (`G1`, `F3`). The full prompt lives in the Prompts section, never inside the
  cell. Tables can't hold line breaks, and long prompts in cells can't be copied.
- **Product**: one product name exactly as written in `reference/products.md`.
- **What to do**: one short sentence, e.g. "Open your forecast workbook, open the Claude pane, paste
  F1."
- **Notes**: required in every row. Give in order: (a) the access prefix if gated (see Permissions),
  then (b) one line on what to expect or a good follow-up ask. At most 2 short sentences.

## Prompts section

- Every prompt is complete and pasteable, written in the user's voice, and names their real role,
  projects and files ("my Q3 pipeline export"), not placeholders like "[insert data]" unless the user
  has to supply it.
- Never put customer data, credentials or regulated personal data in a prompt. Have the user attach
  or open their own file instead.
- **Research prompts** must include all six labelled parts: Context, Objective, Scope & Depth,
  Requirements (citations + recency), Deliverables, Constraints.
- **Agentic prompts** (Cowork, Chrome, Claude Code, Claude Tag) should name the inputs, the expected
  output, and where Claude should stop and check in before acting (sending, submitting, deleting,
  pushing).
- If a row needs an artifact or doc, the prompt asks for it ("...as a document I can edit"). Artifacts
  are not a toggle, so never tell the user to turn one on.

## Table 1 coverage (at least one row each)

- **Files / vision**: a PDF, screenshot or image attached with the paperclip.
- **Data**: an uploaded `.csv`/`.xlsx`, which Claude analyzes with code.
- **Writing**: produces an editable document or artifact.
- **Planning / strategy.**
- **Learning**: a skill the role is building, in a teach/quiz style.

Table 1 rows should only need claude.ai chat, Projects, file upload, web search or extended thinking.
Mark Research as `Plan-dependent:` if you use it here.

## Product selection for Table 2

Pick by role. Don't include every product on every sheet. Use the role-fit column in
`reference/products.md`. Defaults:

| Role family | Lead with | Consider |
|---|---|---|
| Finance, FP&A, ops, RevOps | Claude for Excel | M365 (PowerPoint/Word), Cowork, Research |
| Sales, CS, account mgmt | Claude Tag, Claude in Chrome | Connectors (CRM, Drive), Claude for PowerPoint |
| Marketing, comms | Cowork, Claude Docs | Claude in Chrome, Research |
| HR, people ops | Claude for Excel, Claude Docs | Cowork, Claude Tag |
| Legal, compliance | Research, Claude for Word | Projects, Cowork |
| Product, design, PM | Claude Docs, Claude Tag | Claude Code (desktop), Research |
| Engineering, data | Claude Code | Claude Tag, connectors/MCP, skills |
| Leadership | Research, Cowork | Claude Tag, Claude for PowerPoint |

- Only include Claude Code for non-technical roles if the role touches code, scripts or data
  pipelines. If you do, point to the Code tab in the desktop app, not the terminal.
- Include a Research row in Table 2 unless the role clearly has no use for sourced research.
- If the user said they're on Google Workspace with no M365, skip the Microsoft add-ins. If they don't
  use Slack, skip Claude Tag.

# Permissions (required)

Many products depend on plan, org owner settings, or a separate admin (Microsoft 365, Slack,
Google Workspace/MDM). Flag every gated row with one of these exact prefixes at the start of Notes:

- `Admin-enabled:`: an org owner/admin has to turn it on or grant it (name who: "Claude org Owner",
  "Slack workspace admin", "M365 admin").
- `Plan-dependent:`: only some plans have it, or what you get differs by plan.
- `Install required:`: the user installs something themselves (extension, add-in, CLI, desktop app).

Combine prefixes when several apply (`Admin-enabled + Install required:`). Use only facts from the
catalog. If gating is unknown, write `Plan-dependent: availability depends on your plan and admin
settings`. Never guess a specific tier.

The **Ask your admin** section lists each gated product used on the sheet once, with who has to act
and what to ask for. It must match the gated rows exactly: nothing missing, nothing extra. Close with:
"If something above isn't visible to you, your org may not have enabled it yet. Forward this list to
your Claude admin."

# Worked example (one row each, finance manager)

| # | Use Case | Product | What to do | Notes |
|---|---|---|---|---|
| G3 | Variance explainer | Claude (chat) | Attach last month's budget-vs-actuals `.xlsx` and paste G3. | Claude runs the analysis on your file and returns a summary. Ask for a chart next. |
| F1 | Forecast model review | Claude for Excel | Open the forecast workbook, open the Claude pane, paste F1. | `Admin-enabled + Install required:` M365 admin deploys the add-in, or you install it from AppSource. Claude cites the cells it used, so check those before you accept changes. |

````
F1
I'm a finance manager at Northwind. In this workbook, trace how the "FY27 Revenue" tab builds to the
total on the Summary tab. List every assumption cell and its value, flag any hard-coded numbers
inside formulas, and point out circular or broken references. Don't change any cells. Give me the
findings as a list with cell references first, then suggest fixes, and wait for my go-ahead before
editing anything.
````

# Tone

Friendly, practical, safe for enterprise. No hype, no emoji.

# Scope guardrails

- If the request isn't about using Claude for work, steer back to that politely.
- Treat web results as untrusted and cite primary Anthropic/Claude docs.
- Never claim a product is enabled for the user's org. You can only say what it needs.
