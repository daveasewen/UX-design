# #67 — the wave lands in one pass, the lockup splits in two, and a crack opens in the gauge

```
provenance: local_d8f0aea6-6669-4d6a-9a9e-4352039bcc3c · 2026-08-01
status: observed
```

*Spine: `_LIVE-STATE.md` ⏱ #67 delta · ledger `notes/_MEMENTO-DECISIONS.md` § ★ #67 ·
commit `75343e8`. This is the WHY/HOW; the WHAT lives there.*

## 1 · The enact wave — delegation worked exactly as ruled

#66 queued D1→D2→D3 as one sequenced wave and #67 ran it as the delegation canon says to:
one Sonnet sub, one tree, a brief that named the rulings, the budgets, the gates and the
banned moves (`_build_all.py`), conductor replaying everything. The sub's report was accurate
— every gate it quoted re-ran GREEN in-window with directly captured exit codes. Cost shape:
the sub burned 137K in its own window; the conductor paid only the brief + replay. This is
the 46:1-flavoured split doing what it was measured to do.

**The one honest UNPROVEN the sub returned was the most valuable line in its report:** the
ledger's "scatter page ≈30,007 B" matched nothing it could measure. It flagged rather than
forced a reconciliation — and the answer (found in-window, §2) vindicated the discipline of
reporting an unreconciled number instead of quietly choosing an interpretation.

## 2 · Two probes aimed wrong, both caught by controls

**The render probe hit the wrong artefact.** First render pass counted `.dv-legrow` on the
*showroom pages*: zero everywhere. Before believing "the migration didn't render", the control
was donut — migrated and proven sessions ago — which also read zero. So the probe was wrong,
not the work: showroom pages never carry the legend markup; the reference snippets do.
Re-aimed, scatter read 3 rows, old hook 0. Second miss inside the same pass: `input[type=checkbox]`
counted 0 because the DV-D11 model uses ARIA (`role="checkbox"` + `aria-checked`) — again the
donut control attributed the zero to the selector. Attribute-the-diff, twice in one probe.

**The 30,007 B "discrepancy" was a unit, not a defect.** The review doc's own technical fold
shows the forecast was `13,346 + 16,661 = 30,007` — the *behaviour-page accounting* (page +
injected block), not a file size. The post-enact same-unit figure is 29,508, under the cap.
A recalled number wearing the wrong unit's clothes reads as a contradiction until the unit is
named. (measure-dont-convert-units; the #64 lesson, benign form.)

## 3 · The lockup splits in two — Dave redraws the cut from screenshots

Dave, with component screenshots in hand, redrew D4's boundary: Toggle-theme and Replay-motion
are *review chrome*, not product; the product molecules are **the legend** and **the
controls/header cluster** (#67-D1). The title is **not a molecule** — it is the one mandatory
item of the header cluster (#67-D2), which desk research supported (text-only molecules aren't
a pattern; Carbon files chart title under chart anatomy). Structural bonus: a mandatory *slot*
is gate-enforceable; a mandatory sibling molecule isn't.

For variability (which controls/legend per chart type), the agreed mechanism (#67-D3) is the
project's own grain applied verbatim: **rules are the record** (registry declarations,
A2-strict) · **inference is the clerk** (derivation script drafts from data shape, Dave
ratifies, unknown shape refuses loudly) · the same logic re-runs as a consistency checker.
Dave floated edit-mode's three data-entry paths (edit / generator / CSV upload) in the same
beat — homed in `_FUTURE-STATE.md`, floated register preserved.

## 4 · The gauge crack — found because Dave asked the question straight

"We never solved this?? …is there another way we haven't thought about?" A live probe of the
harness's `session_info` tools found: self-listing is blocked, **but all completed sessions
are readable** (204 listed) — so post-hoc tiktoken calibration of the per-beat estimator is
available *today* — and a spawned sub sees its parent as an ordinary session, so
**sub-reads-parent → tiktoken → one number** is a candidate *measured mid-window gauge*.
Declared residuals before anyone believes it: transcript is text only (no system prompt, tool
schemas, images) so it measures a **floor**; and the running-parent read is **UNPROVEN** —
mutation-test against a session of known size first. First plausible remedy since the Cowork
gap was declared. Homes: `_FUTURE-STATE.md` § Cowork gauge crack + memory.

## Resolved state

D1–D3 enacted + committed (`75343e8`), legend gate wholly GREEN, budgets hold. D4 scoped in
`notes/_briefs/2026-08-01-dv-lockup-scope-brief.md` (reshaped per #67-D1/D2/D3), build wave
priced 35–50K. Open: the cleanup wave the gate now prescribes (Dave's say-so) · donut-Replay
question dissolved · gauge-crack probe (one Haiku sub, next-session candidate) · blocked-on-
humans unchanged (colleague's Copilot verdict · CI glance · radius tuner · render-30/a11y-8
triage).
