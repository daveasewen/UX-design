# Brief — s176 enact-queue: stale prose fix + Legacy selftest mirror (2026-08-14, v1)

Conductor: #176. You are ONE Opus build sub. Two small jobs, both queued at the #175 wrap. Budget: small; if anything surprises you, STOP and report rather than improvise.

## Job A — the ~15 lines of now-FALSE prose (queued #175 ⑪)

`s175-D1` made `progress/complete` resolve to ink in ALL four themes and moved the red overrides to the minted `step/complete`. The Progress-bar contrast failure (Legacy dark 1.75, Supercharge dark 2.38) is FIXED for the bar (now 9.15 / 10.46) — but three places still describe the OLD state as current:

1. `knowledge/snippets/Progress-bar.reference.html` `knownFindings` (~line 151): the CONTRAST FINDING entry still reports Legacy 1.75 / SC 2.38 FAIL for the bar. Rewrite it to the post-s175-D1 truth: fill-on-track now Mono 15.27/9.15, Console 15.27/9.15, Legacy ~/9.15, Supercharge ~/10.46 — MEASURE the light-mode Legacy/SC figures yourself against canon.css at HEAD, do not guess them; state that the failure REMAINS on the step components (Progress-tracker/Stepper, which bind step/complete) and is queued, Dave's.
2. `knowledge/components/progress-bar.meta.json:22` (`tokens.fill`): still says "Legacy #DB0011 both modes, Supercharge #B92F1E | #CC4333". Now: ink in all four themes (Mono/Console #1A1A1A|#FFFFFF, Legacy #1A1A1A|#FFFFFF, SC #13110E|#F7F6F4 — VERIFY by resolving against canon.css, don't trust this brief). Line ~75 `$finding`: same correction as (1).
3. `knowledge/canon/canon.css:~8029`: the mirrored Finding lines. ⛔ NEVER hand-edit canon.css — it must change ONLY via its generator. Find which generator mirrors knownFindings into canon.css (likely gen_canon_components.py), fix the SOURCE (the snippet), regenerate, and attribute every hunk.

Preserve provenance: where the old figures were true, the rewrite should say "was X before s175-D1" rather than deleting history — append/amend, don't erase measured receipts.

## Job B — Legacy mirror of the selftest clause (queued #175 ⑮, ~3 lines)

`knowledge/canon/gen_theme_cascade.py` selftest (~lines 541–557) asserts the SC leg of s175-D1 (`step/complete` light == #B92F1E; `progress/complete` resolves to theme ink). Add the LEGACY mirror: `step/complete` == #DB0011 (both modes, per the moved override) and legacy `progress/complete` resolves to the Legacy ink pair. ⚠ Assert VALUES, never absences — `load_themes()` returns ALIAS-EXPANDED overrides, so "no declared override" is indistinguishable from "expanded override" in that dict. Mutation-test the new clauses: temporarily break each asserted value, confirm the selftest goes red, restore, confirm green. Report the mutation receipts.

## Generator ownership / blast radius (#174 class)

Name which regions of canon.css your regeneration touches BEFORE running it; attribute every hunk afterwards. Expected: ONLY the Progress-bar comment block. Any hunk outside it = STOP and report.

## Gates — run BEFORE and AFTER, rc captured DIRECTLY (no pipes)

snippet · a11y · radius --strict · coverage · icon · --check on showroom / snippet-tokens / canon-components / component-partials / theme-cascade · theme-cascade --selftest. Type-composite ratchet baseline is 1101 red — it may only shrink, not grow. ⚠ If you run state-contrast FILTERED, it rewrites the whole tracked `knowledge/_STATE-CONTRAST-AUDIT.md` — restore it byte-identical afterwards (this bit us at #175).

## ⛔ DO NOT

- Run `knowledge/_build_all.py` (ANY partial run strands the tree; composite verdict is CI's).
- Rule anything. DO-NOT-RULE: the three undecided step-colour themes (Mono/Console/SC) · `step/incomplete` (asymmetry left alone deliberately) · the step-component contrast failure (Dave's) · s151-D1 · s149-D1 · any colour VALUE · the `#166` labels in `_build_all.py` (JOIN KEYS) · anything not named in Jobs A/B. If Job A's rewrite seems to need a design decision, write the sentence that reports the open question instead of answering it.
- Touch `_rulings.json`, `_state.json`, MEMORY, or any wrap machinery.
- Reformat any file you edit — minimal textual diffs; round-trip JSON byte-identical outside your edit.

## Pitfalls replayed (Dave's standing rule)

- A token NAME is not an ADDRESS — resolve through the alias chain when you verify hexes.
- rc through a pipe reports the pipe's rc — capture `$?` immediately.
- A green that cannot fail is an assertion — hence the mutation tests in Job B.
- Sandbox call boundary ~45s wall — chunk long runs.
- `pip install tiktoken --break-system-packages` first if any gauge/instrument refuses.

## Report back

Per job: files touched, hunk attribution, gate rc table before/after, mutation receipts, measured figures with the command that produced them, friction log (anything that fought you), and an explicit "NOT DONE / NOT RULED" list.

Repo (bash): /sessions/upbeat-nifty-mayer/mnt/UX-design
