# FILED SUB-REPORT — the `s218-D7` skeleton

⛔ **THIS FILE IS THE TEMPLATE. COPY IT; NEVER WRITE YOUR REPORT INTO IT.** It is exempt by
name from the doc-row gate and from the wrap citation check — every OTHER `.md` in this
directory is a real filed report and is graded as one.

**Filename:** `notes/_subreports/YYYY-MM-DD-<session no>-<sub index>-<slug>.md` — the window and
the sub index are IN the name, so one writer owns one path and two subs can never collide.

**Evidence lives BESIDE the report:** `notes/_subreports/assets/<report-stem>/`. ⛔ Never in
session scratch (`/tmp`, `/var/tmp`, a sandbox home): scratch does not survive the window, and a
report whose evidence has evaporated is a claim, not a receipt.

**Reports are dated HISTORY (ADR-0017 / `s192-D1`).** They are written once and not re-edited by
later sessions. Live facts flow OUT of a report to their one home at the conductor's reconcile —
the report keeps the reading it took on the day it took it.

⛔ **THE FILE IS THE SOLE AUTHORITY.** What goes back to chat is a STUB — verdict + the COUNTS
line + the file pointer + token spend + REPLAY-THESE — and every figure in that stub is COPIED
FROM THIS FILE, never retyped from memory. A stub figure that disagrees with the file is the
defect this whole mechanism exists to stop.

**ADR-0016 vocabulary is MANDATORY.** `CLAIMED` = asserted but not re-read from the artefact.
`UNPROVEN` = honestly not established, with the price of proving it. "Verified" is a property of
a MOMENT and needs its probe named beside it. A declared gap passes; a silent one fails.

---

*(everything below is the skeleton — delete this line and the block above when you copy)*

# `#NNN`-`<sub index>` — `<short subject, one line>`

session: `#NNN` · YYYY-MM-DD
window: `<conductor window or lane name>`
sub index: `<cA | cB | wave3-alpha | wrap | …>`
brief: `notes/_briefs/<brief file>.md`
tokens: `<N>` real (this sub's own spend, `message.usage`; `UNMEASURED — <reason>` if it could
not be read)

## VERDICT

`<One paragraph. What the conductor must know if they read nothing else. Say plainly whether the
brief's regions were DONE, PARTIAL or REFUSED, and why.>`

COUNTS: findings `<N>` · ruling-shaped `<N>` · UNPROVEN `<N>`

*(The COUNTS line is PARSED, not prose — it must match this shape exactly, on its own line, with
` · ` separators and plain integers. Nonzero counts are what force the conductor to open the
file. If a count is genuinely zero, write `0`; never omit the term.)*

## What was done

`<Region by region, in the brief's own order. Name the files touched by absolute-or-repo path.>`

## Findings

`<Numbered. One finding per number. Each carries the probe that produced it — the command, the
file and line, or the quoted string. A finding with no probe is an opinion.>`

## RULING-SHAPED QUESTIONS

⛔ **MANDATORY SECTION — never delete it, even to write "none".** Generated prose reads as
decided; this heading is what stops a sub's recommendation from arriving as a ruling. Anything
that needs Dave's word — a name, a constant, a promotion, a trade-off between two defensible
options — goes HERE, phrased as a question with its options priced, and NOWHERE else.

1. `<question — option (a) …, option (b) …; recommend (x) because …>`

*(or: `**None.** Nothing in this lane needed a decision that was not already ruled.`)*

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN:** `<what was not established>` — price to prove: `<N tokens / one render matrix /
  …>`.
- **CLAIMED:** `<what is asserted from a banner, a docstring or a prior session rather than
  re-read from the artefact>` — re-read costs `<…>`.

## Evidence

`notes/_subreports/assets/<report-stem>/` — `<what is in there and what each file proves>`
*(or: `No evidence files: every claim above quotes its probe inline.`)*

REPLAY-THESE: `<path or item>` (~`<N>` tk) · `<path or item>` (~`<N>` tk)

*(The priced replay line, also PARSED. It names what the conductor must read back IN FULL, each
with its token price, so a deferral is DECLARED rather than silent. If nothing needs replaying,
write exactly: `REPLAY-THESE: none — the stub carries everything.`)*
