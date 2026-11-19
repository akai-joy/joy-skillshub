# joy-skillshub

A collection of Claude skills, packaged as a Claude Code plugin marketplace.

## Plugins

| Plugin | Skills | What it does |
|---|---|---|
| [`prompt-coach`](plugins/prompt-coach/) | `prompt-coach-v2` | Builds a role-specific Claude enablement sheet. It recommends newer Claude products (Claude for Excel / Microsoft 365, Claude Tag, Claude in Chrome, Cowork, Claude Code, Claude Docs, connectors and skills), flags each one that needs an admin, a particular plan, or an install, and ends with an "Ask your admin" checklist. |
| [`2ndcouncil`](plugins/2ndcouncil/) | `2ndcouncil` | Pressure-tests a hard, expensive-to-reverse decision with a council of five Claude subagents (Contrarian, First-Principles, Expansionist, Outsider, Executor). The members answer independently, review each other anonymously, and an Opus head gives a GO / NO-GO / RECONSIDER verdict. It relies on subagents, so it's designed for Claude Code. |
| [`pre-mortem`](plugins/pre-mortem/) | `pre-mortem` | Assumes a plan, launch or migration has already failed and works backwards from there. It writes specific failure stories, ranks them by likelihood × impact, names the early warning signs, and sorts actions into fix now / watch / accept. |

## Install in Claude Code

One step (Claude Code 2.1.275 or later):

```
/plugin install prompt-coach --marketplace akai-joy/joy-skillshub
/plugin install 2ndcouncil --marketplace akai-joy/joy-skillshub
/plugin install pre-mortem --marketplace akai-joy/joy-skillshub
```

Or add the marketplace once, then install what you want:

```
/plugin marketplace add akai-joy/joy-skillshub
/plugin install prompt-coach@joy-skillshub
/plugin install 2ndcouncil@joy-skillshub
/plugin install pre-mortem@joy-skillshub
```

To get updates, run `/plugin marketplace update joy-skillshub`, then `/reload-plugins`. You can also turn on auto-update for this marketplace under `/plugin` → **Marketplaces**.

## Install in the Claude app (chat / Cowork)

Zip a skill folder, for example `plugins/prompt-coach/skills/prompt-coach-v2/`, and upload it in your skills settings. On Team and Enterprise plans, your org admin has to allow custom skills.

## Note

Product availability and admin settings change often. `prompt-coach-v2/reference/products.md` has a last-verified date, so check it against https://support.claude.com before relying on it.
