# Claude product catalog

Last verified: 2026-11-18 (support.claude.com, claude.com/docs, code.claude.com)

This is the only source for setup steps and gating in prompt-coach-v2. If a fact isn't here, use the
generic wording: "availability depends on your plan and admin settings."

## Always available (Team/Enterprise seat, no admin action)

| Product | What it is | Access steps | Role fit |
|---|---|---|---|
| Claude (chat) | claude.ai web, desktop and mobile chat | Open claude.ai or the desktop app | Everyone |
| File upload | PDFs, images, `.csv`/`.xlsx` read and analyzed | Click the **paperclip** and attach. No tool to pick. | Everyone |
| Projects | Saved context (docs, instructions) for repeated work | Create a Project and add files and instructions | Everyone |
| Web search | Live web results in chat | On by default. If it's off, toggle it in the capabilities/settings menu. | Everyone |
| Extended thinking | Deeper reasoning on hard problems | Toggle **Extended thinking** in the model/settings menu | Analysts, strategy, eng |
| Artifacts | Documents, code, visuals Claude renders beside the chat | Not a toggle. Ask for one in the prompt. | Everyone |

## Gated or installed products

| Product | What it is | Access steps | Who has to act | Prefix | Role fit |
|---|---|---|---|---|---|
| Research | Multi-step sourced research with citations | Click **Research** below the message box before sending | Plan/admin | `Plan-dependent:` | Strategy, legal, leadership, PM |
| Claude for Excel | Add-in: reads and edits workbooks, traces formulas, builds models, cites cells | Install from Microsoft AppSource and sign in with Claude, or admin deploys "Claude for Microsoft 365" from the M365 Admin Center | User or M365 admin; admins can manage add-in access | `Install required:` (+ `Admin-enabled:` if IT-managed) | Finance, FP&A, ops, HR, RevOps |
| Claude for PowerPoint | Same M365 add-in family, for decks | Same as Excel ("Claude for Microsoft 365") | Same as Excel | Same as Excel | Sales, leadership, marketing |
| Claude for Word | Same M365 add-in family, for documents and redlines | Same as Excel ("Claude for Microsoft 365") | Same as Excel | Same as Excel | Legal, HR, comms |
| Claude for Outlook | M365 add-in for email | Same family. Status varies (beta / coming soon), so check before recommending. | M365 admin | `Plan-dependent:` | Execs, sales, CS |
| Claude Tag | Claude in Slack: @mention Claude in channels and threads | Claude org **Owner** runs setup at claude.ai/admin-settings/claude-tag. A **Slack workspace admin** installs the app from the Slack Marketplace and pairs it with `@Claude connect`. Enterprise Grid: a Slack Org Owner/Admin installs it org-wide. | Claude Owner + Slack admin (Team/Enterprise) | `Admin-enabled:` | Sales, CS, PM, eng, anyone in Slack |
| Claude in Chrome | Browser extension that acts in the user's own Chrome with their sign-ins (fill forms, navigate, summarize pages) | Install from the Chrome Web Store, or admin deploys it via Google Workspace/MDM. The org toggle is under Organization settings → Claude in Chrome. | Org Owner (on by default for Team, and for Enterprise unless disabled; off by default for HIPAA orgs) | `Admin-enabled + Install required:` | Sales, CS, ops, marketing, recruiting |
| Cowork | Agentic mode in the Claude desktop app: works across local files, apps and the browser on multi-step tasks | Use the Claude desktop app. Owners control it under Organization settings → Cowork. On Enterprise it can be limited to groups/custom roles. Cowork in the cloud is off by default on Enterprise. | Org Owner | `Admin-enabled:` | Marketing, ops, leadership, HR, PM |
| Claude Code | Agentic coding: repos, refactors, tests, migrations, PR review | Desktop app **Code** tab (no install beyond the desktop app), or CLI: `curl -fsSL https://claude.ai/install.sh \| bash` (macOS/Linux/WSL), `irm https://claude.ai/install.ps1 \| iex` (Windows PowerShell). Also web and IDE extensions. | Seat type is plan/admin dependent | `Plan-dependent + Install required:` | Engineering, data, technical PMs |
| Claude Docs | Living documents Claude creates and edits, shareable with teammates | Ask Claude in chat to create a doc | Plan/admin | `Plan-dependent:` | PM, marketing, HR, legal, leadership |
| Connectors | Link Google Drive, CRM, ticketing etc. so Claude can read and act in them | **Settings → Connectors**. Some connectors need an admin to add or approve them first. | User and/or org Owner | `Admin-enabled:` when org-managed | Everyone who lives in a SaaS tool |
| Skills / plugins | Reusable packaged workflows Claude loads for a task | Org- or user-installed. Availability and who can add them are admin-controlled. | Org Owner/admin | `Admin-enabled:` | Teams with repeatable processes |

## Notes and caveats

- The legacy Claude in Slack bot was retired 2026-10-05. Recommend Claude Tag, not the old app.
- Claude for M365 can also run through Bedrock, Vertex AI, Azure AI Foundry or an LLM gateway without
  individual Claude accounts. If the org routes AI that way, it's an IT conversation.
- Government (GCC/GCC High/DoD) tenants can't use the public AppSource listing, so IT deploys the
  manifest.
- Agentic products (Chrome, Cowork, Claude Code, Claude Tag) act on the user's behalf. Prompts should
  always say where Claude stops for confirmation.

## Sources

- https://claude.com/docs/office-agents/excel
- https://support.claude.com/en/articles/13892150-work-across-microsoft-365-apps
- https://claude.com/docs/claude-tag/admins/setup-overview
- https://claude.com/docs/claude-tag/admins/pair-workspace
- https://support.claude.com/en/articles/13065128-claude-in-chrome-admin-controls
- https://support.claude.com/en/articles/13455879-use-claude-cowork-on-team-and-enterprise-plans
- https://code.claude.com/docs/en/setup
