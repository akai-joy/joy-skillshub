# joy-skillshub

A collection of Claude skills. Each top-level folder holds one skill.

## Skills

| Skill | What it does |
|---|---|
| [`prompt-coach-v2`](prompt-coach-v2/) | Builds a role-specific Claude enablement sheet. It recommends newer Claude products (Claude for Excel / Microsoft 365, Claude Tag, Claude in Chrome, Cowork, Claude Code, Claude Docs, connectors and skills), flags each one that needs an admin, a particular plan, or an install, and ends with an "Ask your admin" checklist. |

## Install a skill

**Claude Code:** copy the skill's folder (for example `prompt-coach-v2/`) into `~/.claude/skills/`.

**Claude app:** zip the skill's folder and upload it in your skills settings. On Team and Enterprise plans, your org admin has to allow custom skills.

## Note

Product availability and admin settings change often. `prompt-coach-v2/reference/products.md` has a last-verified date, so check it against https://support.claude.com before relying on it.
