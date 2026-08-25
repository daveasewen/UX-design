# #218 build brief — filed sub-reports machinery (s218-D7) + the frozen-column fix

## Half 1 — enact s218-D7 (read the ruling in knowledge/_rulings.json first; it is the spec)

1. **The fenced directory**: `notes/_subreports/` with a `_TEMPLATE.md` skeleton — header
   (session · window · sub index · brief pointer · token spend), VERDICT, COUNTS line
   (findings · ruling-shaped · UNPROVEN — parsed, not prose), body sections incl. a mandatory
   **RULING-SHAPED QUESTIONS** section and a priced **REPLAY-THESE** line, ADR-0016 vocabulary
   (CLAIMED/UNPROVEN) named in the skeleton. Evidence files sit BESIDE the report
   (`notes/_subreports/assets/<report-stem>/`), never in session scratch.
2. **Gate extension A**: widen the doc-row gate's glob to `notes/_subreports/*.md` (template
   exempt by name) — a filed report with no store row fails exactly like a brief does.
3. **Gate extension B**: a new wrap check — a file under `notes/_subreports/` newer than the
   last wrap that is NOT cited by path in the session's receipt/banner REFUSES the wrap
   (the unread-pointer pitfall). ADVISORY at birth (promotion is Dave's), red-arm driven on a
   planted uncited report.
4. **Runbook**: ADDITION to `knowledge/_RUNBOOK-capture-ritual.md` — the sub-brief section
   gains the filed-report contract (subs write the file, return the stub; conductor cites by
   path at reconcile). Reference s218-D7, never restate its body.

## Half 2 — the frozen itinerary column (premise class, 5th surface, gate-don't-patch)

The generator behind `reviews/ITINERARY-STATUS-*.json` still emits the 2026-07-14 spreadsheet
cell as `itinerary_status` — read as live twice now (#203, #218). Fix at the generator: the
field becomes `itinerary_status_1907_FROZEN` (the date in the name is the fence), `$caveat`
names the class, and the MEASURED `derived` column keeps its name. Emit a fresh dated snapshot
(v4) alongside v3 (dated artefacts are history — v3 stays untouched); check every consumer of
the old field name (grep, fix the readers, list them in the report). Selftest bite: the frozen
name present, the bare name ABSENT from new emissions.

## Discipline (both halves)

You are the FIRST consumer of half 1: file your full report at
`notes/_subreports/2026-08-25-218-cA-filed-reports.md` per your own template and return ONLY
the stub to chat. Fence: no rulings, no constants/bands, no promotion of gate B past advisory,
no store/lane/GM/LS/memory edits, no commit/push. Every new check red-arm driven before it
counts. /var/tmp session-suffixed (-s218fr).
