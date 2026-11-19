#!/usr/bin/env python3
"""Deterministic checks for prompt-coach-v2 output.

Usage:
  python3 check_output.py <response.md> --eval-id N [--evals evals.json] [--catalog ../reference/products.md] [--out grading.json]

Writes a grading.json ({expectations:[{text,passed,evidence}], summary:{...}}) that
skill-creator's aggregate_benchmark.py and eval viewer can read. Only checks rules that
can be verified mechanically. Prompt quality still needs a human look.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
HEADER = ["#", "Use Case", "Product", "What to do", "Notes"]
PREFIX_RE = re.compile(
    r"^`?\s*(Admin-enabled|Plan-dependent|Install required)(\s*\+\s*(Admin-enabled|Plan-dependent|Install required))*\s*:"
)
RESEARCH_PARTS = ["Context", "Objective", "Scope", "Requirements", "Deliverables", "Constraints"]
CLOSING = "If something above isn't visible to you"


def load_catalog(path):
    """Return (all product names, gated product names) from products.md tables."""
    text = Path(path).read_text()
    all_names, gated = set(), set()
    section = None
    for line in text.splitlines():
        if line.startswith("## "):
            section = line
        m = re.match(r"^\|\s*([^|]+?)\s*\|", line)
        if not m or line.startswith("|---") or m.group(1) in ("Product",):
            continue
        name = m.group(1)
        all_names.add(name)
        if section and "Gated" in section:
            gated.add(name)
    return all_names, gated


def split_row(line):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return cells


def find_tables(md):
    """Return list of (heading, header_cells, rows) for every markdown table."""
    lines = md.splitlines()
    tables, heading, i = [], "", 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
        if line.strip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            header = split_row(line)
            rows, j = [], i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.append(split_row(lines[j]))
                j += 1
            tables.append((heading, header, rows))
            i = j
            continue
        i += 1
    return tables


def code_blocks(md):
    """Map label -> block text for fenced blocks whose first non-empty line is a label like G1/F2."""
    blocks = {}
    for m in re.finditer(r"(`{3,})[^\n]*\n(.*?)\n\1", md, re.S):
        body = m.group(2)
        first = body.strip().splitlines()[0].strip() if body.strip() else ""
        lm = re.match(r"^\**([GF]\d+)\b", first)
        if lm:
            blocks[lm.group(1)] = body
    # Also accept a heading/label line right before the fence, e.g. "**F1**" or "### F1"
    for m in re.finditer(r"(?m)^[#*\s]*([GF]\d+)\b[^\n]*\n+(`{3,})[^\n]*\n(.*?)\n\2", md, re.S):
        blocks.setdefault(m.group(1), m.group(3))
    return blocks


def section(md, title):
    m = re.search(rf"(?ms)^#+\s*{re.escape(title)}\s*$(.*?)(?=^#+\s|\Z)", md)
    return m.group(1) if m else None


def check(md, cfg, catalog_names, gated_names):
    results = []

    def add(text, passed, evidence):
        results.append({"text": text, "passed": bool(passed), "evidence": evidence})

    tables = find_tables(md)
    sheet_tables = [t for t in tables if [h.strip("* ") for h in t[1]] == HEADER]

    if not cfg.get("expect_sheet", True):
        add("Asks a clarifying question", "?" in md, f"{md.count('?')} question marks")
        add("Does not produce enablement tables yet", not tables, f"{len(tables)} tables found")
        low = md.lower()
        add("Asks for company and role/responsibilities", "company" in low and any(w in low for w in ("role", "responsib", "work on", "projects")), "keyword scan")
        add("Asks about tools (Microsoft 365 / Google Workspace / Slack)", any(w in low for w in ("microsoft", "m365", "google", "slack")), "keyword scan")
        add("Asks in one short message (under 1200 chars)", len(md) < 1200, f"{len(md)} chars")
        return results

    t1 = next((t for t in sheet_tables if "Get Started" in t[0]), None)
    t2 = next((t for t in sheet_tables if "Go Further" in t[0]), None)
    has_sheet = bool(t1 and t2)
    NO_SHEET = "no sheet tables with the required header"
    add("Has 'Get Started' and 'Go Further' tables with exact headers `# | Use Case | Product | What to do | Notes`",
        has_sheet, f"{len(sheet_tables)} tables with exact header; headings: {[t[0] for t in sheet_tables]}")

    # Every check below runs even without the sheet format, so configs are graded on the same
    # assertion list. Table-only checks fail with NO_SHEET; content checks fall back to text scans.
    rows = ([(r, 1) for r in t1[2]] + [(r, 2) for r in t2[2]]) if has_sheet else []
    add("Table 1 has 5-7 rows", has_sheet and 5 <= len(t1[2]) <= 7, f"{len(t1[2])} rows" if has_sheet else NO_SHEET)
    add("Table 2 has 3-6 rows", has_sheet and 3 <= len(t2[2]) <= 6, f"{len(t2[2])} rows" if has_sheet else NO_SHEET)

    bad_notes = [r[0] for r, _ in rows if len(r) < 5 or not r[4].strip()]
    add("Every row has Notes", has_sheet and not bad_notes,
        NO_SHEET if not has_sheet else (f"rows missing notes: {bad_notes}" if bad_notes else "all rows have notes"))

    bad_labels = [r[0] for r, n in rows if not re.fullmatch(rf"\**{'G' if n == 1 else 'F'}\d+\**", r[0])]
    add("Prompt column holds labels (G#/F#), not full prompts", has_sheet and not bad_labels,
        NO_SHEET if not has_sheet else (f"bad labels: {bad_labels}" if bad_labels else "ok"))

    blocks = code_blocks(md)
    labels = [r[0].strip("*") for r, _ in rows]
    missing = [l for l in labels if l not in blocks]
    add("Every table label has a matching fenced prompt block", has_sheet and not missing,
        NO_SHEET if not has_sheet else (f"missing blocks: {missing}" if missing else f"{len(labels)} labels matched"))

    if has_sheet:
        products = [r[2].strip("*` ") for r, _ in rows if len(r) > 2]
    else:  # text fallback: any catalog product named anywhere in the reply
        products = [p for p in catalog_names if re.search(rf"\b{re.escape(p)}\b", md)]
    unknown = sorted({p for p in products if p not in catalog_names})
    add("Product names match the catalog exactly", has_sheet and not unknown,
        NO_SHEET if not has_sheet else (f"not in catalog: {unknown}" if unknown else "ok"))

    gated_rows = [(r[0], r[2].strip("*` "), r[4]) for r, _ in rows if len(r) > 4 and r[2].strip("*` ") in gated_names]
    unflagged = [lab for lab, _, notes in gated_rows if not PREFIX_RE.match(notes.strip())]
    if has_sheet:
        add("Every gated product row starts Notes with an access prefix", not unflagged,
            f"unflagged: {unflagged}" if unflagged else f"{len(gated_rows)} gated rows flagged")
    else:
        hits = len(PREFIX_RE.findall(md)) + len(re.findall(r"(?m)^\W*(Admin-enabled|Plan-dependent|Install required)\s*:", md))
        add("Every gated product row starts Notes with an access prefix", False, f"{NO_SHEET}; {hits} prefix-style flags in text")

    admin = section(md, "Ask your admin")
    gated_used = sorted({p for _, p, _ in gated_rows}) if has_sheet else sorted(p for p in products if p in gated_names)
    if admin is None:
        add("'Ask your admin' lists exactly the gated products used", False, "no 'Ask your admin' section")
        add("'Ask your admin' ends with the forward-to-admin line", False, "no 'Ask your admin' section")
    else:
        listed = sorted({p for p in gated_names if re.search(rf"\b{re.escape(p)}\b", admin)})
        # A product name that is a prefix of another (e.g. Claude Code vs nothing) is fine; compare sets.
        miss, extra = sorted(set(gated_used) - set(listed)), sorted(set(listed) - set(gated_used))
        add("'Ask your admin' lists exactly the gated products used", not miss and not extra,
            f"missing: {miss}; extra: {extra}" if (miss or extra) else f"matches {gated_used}")
        add("'Ask your admin' ends with the forward-to-admin line", CLOSING in admin, "found" if CLOSING in admin else "closing line missing")

    research = [r[0].strip("*") for r, _ in rows if r[2].strip("*` ") == "Research"]
    if cfg.get("require_research_row"):
        add("Includes a Research row", bool(research), f"research rows: {research}" if has_sheet else NO_SHEET)
        # One fixed assertion (not one per row) so every config is graded on the same list.
        if research:
            bad = {}
            for lab in research:
                miss = [p for p in RESEARCH_PARTS if not re.search(rf"(?mi)^\W*{p}\b", blocks.get(lab, ""))]
                if miss:
                    bad[lab] = miss
            add("Research prompts have all six labelled parts", not bad, f"missing: {bad}" if bad else f"{research} complete")
        else:
            miss = [p for p in RESEARCH_PARTS if not re.search(rf"(?mi)^\W*{p}\b", md)]
            add("Research prompts have all six labelled parts", False, f"no Research row; six-part labels missing from text: {miss}")

    add("Never suggests npm install for Claude Code", "npm install" not in md, "found 'npm install'" if "npm install" in md else "ok")
    toggle = re.search(r"(?i)(turn on|enable|toggle)\s+artifacts|press \+", md)
    add("Never tells the user to turn Artifacts on", not toggle, toggle.group(0) if toggle else "ok")

    for p in cfg.get("required_products", []):
        add(f"Recommends {p}", p in products, f"products: {sorted(set(products))}")
    for p in cfg.get("forbidden_products", []):
        add(f"Does not recommend {p}", p not in products, f"products: {sorted(set(products))}")

    if cfg.get("chrome_must_mention_hipaa"):
        if "Claude in Chrome" not in products:
            add("If Chrome is recommended, it notes HIPAA orgs have it off by default", True, "Chrome not recommended")
        else:
            notes = " ".join(r[4] for r, _ in rows if r[2].strip("*` ") == "Claude in Chrome") + (admin or "") if has_sheet else md
            ok = "HIPAA" in notes and re.search(r"(?i)off by default|disabled by default|stays off|until an? (org )?owner", notes)
            add("If Chrome is recommended, it notes HIPAA orgs have it off by default", bool(ok), "found" if ok else "no HIPAA default-off note")

    if cfg.get("require_native_installer_if_cli"):
        ok = "install.sh" in md or "Code tab" in md or "desktop app" in md.lower()
        add("Claude Code setup uses native installer or desktop Code tab", ok, "found" if ok else "no install path given")

    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("response")
    ap.add_argument("--eval-id", type=int, required=True)
    ap.add_argument("--evals", default=str(HERE / "evals.json"))
    ap.add_argument("--catalog", default=str(HERE.parent / "reference" / "products.md"))
    ap.add_argument("--out")
    a = ap.parse_args()

    evals = {e["id"]: e for e in json.load(open(a.evals))["evals"]}
    cfg = evals[a.eval_id].get("checks", {})
    names, gated = load_catalog(a.catalog)
    md = Path(a.response).read_text()
    res = check(md, cfg, names, gated)
    passed = sum(r["passed"] for r in res)
    out = {"expectations": res,
           "summary": {"passed": passed, "failed": len(res) - passed, "total": len(res),
                       "pass_rate": round(passed / len(res), 2) if res else 0.0}}
    s = json.dumps(out, indent=2)
    if a.out:
        Path(a.out).write_text(s)
    print(s if not a.out else f"{passed}/{len(res)} passed -> {a.out}")


if __name__ == "__main__":
    sys.exit(main())
