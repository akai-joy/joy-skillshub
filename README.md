# prompt-coach-v2

A Claude skill that builds a role-specific Claude enablement sheet. It recommends Claude's newer products (Claude for Excel / Microsoft 365, Claude Tag, Claude in Chrome, Cowork, Claude Code, Claude Docs, connectors and skills). Every recommendation that needs admin action, a particular plan, or an install is flagged, and the sheet ends with an "Ask your admin" checklist.

## Contents

- `prompt-coach-v2/SKILL.md`: instructions and output format
- `prompt-coach-v2/reference/products.md`: product catalog with setup steps and who has to enable each product (includes a last-verified date)
- `prompt-coach-v2/templates/next_steps.md`: admin checklist and next steps

## Install

**Claude Code:** copy the `prompt-coach-v2/` folder into `~/.claude/skills/`.

**Claude app:** zip the `prompt-coach-v2/` folder and upload it in your skills settings. On Team and Enterprise plans, your org admin has to allow custom skills.

## Note

Product availability and admin settings change often. Check `reference/products.md` against https://support.claude.com before relying on it.
