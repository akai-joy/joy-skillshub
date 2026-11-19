# joy-skillshub

A collection of Claude skills, packaged as a Claude Code plugin marketplace.

## Plugins

| Plugin | Skills | What it does |
|---|---|---|
| [`prompt-coach`](plugins/prompt-coach/) | `prompt-coach-v2` | Builds a role-specific Claude enablement sheet. It recommends newer Claude products (Claude for Excel / Microsoft 365, Claude Tag, Claude in Chrome, Cowork, Claude Code, Claude Docs, connectors and skills), flags each one that needs an admin, a particular plan, or an install, and ends with an "Ask your admin" checklist. |

## Install in Claude Code

One step (Claude Code 2.1.275 or later):

```
/plugin install prompt-coach --marketplace akai-joy/joy-skillshub
```

Or in two steps:

```
/plugin marketplace add akai-joy/joy-skillshub
/plugin install prompt-coach@joy-skillshub
```

To get updates, run `/plugin marketplace update joy-skillshub`, then `/reload-plugins`. You can also turn on auto-update for this marketplace under `/plugin` → **Marketplaces**.

## Install in the Claude app (chat / Cowork)

Zip a skill folder, for example `plugins/prompt-coach/skills/prompt-coach-v2/`, and upload it in your skills settings. On Team and Enterprise plans, your org admin has to allow custom skills.

## Note

Product availability and admin settings change often. `prompt-coach-v2/reference/products.md` has a last-verified date, so check it against https://support.claude.com before relying on it.
