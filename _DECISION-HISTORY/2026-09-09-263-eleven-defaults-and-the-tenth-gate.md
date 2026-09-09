# #263 — the eleven proposed defaults got a page, a ruling pass, and a tenth release gate

provenance: 263 · 2026-09-09
status: observed

*The WHY and HOW of #263. The WHAT — the thirteen rulings, the commits, the gauge — lives in
`knowledge/_rulings.json` (`s263-D1` … `s263-D13`), `_LIVE-STATE.md` § ⏱ LATEST DELTA #263 and
`GOOD-MORNING.md`'s ★ LATEST banner. Both-way links: `_LIVE-STATE.md` ⏱ delta #263 · the ledger
entries above · `notes/_subreports/2026-09-09-263-W-wrap.md`.*

---

## 1 — The carry that would not die, and the shape that killed it

Eleven lane recommendations had been **defaulted by the #261 conductor** — accepted into the record
without Dave ever seeing them. #262 did not put them to him either; the carry was re-typed and aged
instead. The finding behind the whole session is that **a defaulted recommendation has no natural
moment to come back**: it is not a bug, so no gate reds on it; it is not a question, so no wrap
surfaces it; it is not a build, so no lane picks it up. It just ages.

What broke the loop was giving the eleven a **surface with a decision on every one of them**. Lane P
built `notes/_PROPOSED-263.html`: eleven cards, each carrying the verbatim recommendation, the reason
it was given, **what the code does today**, the alternative, and an Accept / Reject / Later row with a
note field — plus an **export block** that renders one line per ruled item and, crucially, a
`NOT RULED (n): …` line so the wrap can see what is still open. The page rules nothing itself; every
row ships empty and no default is pre-selected.

⛔ **The page was NOT driven in a browser and was NOT published.** Hosted publish was refused (the
approval card could not be answered from the seat), so the file itself was the surface Dave read.
That is a declared limit of this session's method, not a property of the page.

**It worked in one pass.** Dave ruled all eleven through the export block: eight straight ACCEPTs,
and three that came back LATER with notes rather than as decisions.

## 2 — The three LATERs, and why they became rulings anyway

A `LATER` is not a ruling. Each of the three carried a sentence, and the sentences turned out to be
the decision:

- **P-07, the doormat.** His note read *"[p]ark — keep the doormat as a dormant variant of Footer so
  it stays one component"*, then, asked what to call that state, **"dormant variant"**. That is a
  ruling about the shape of the record, not a deferral: `s263-D7`. It also discharges `s261-D3`'s
  hedge (*"App footer for now"*) — the doormat is neither retired nor live; it is dormant.
- **P-08, the legend.** He asked first: *"Is this teh legend for charts? if so leave it at 44 it works
  fine"*, then **"accept"** once it was confirmed as the chart legend. ★ **The question was the
  work** — the recommendation was ambiguous about which legend it meant, and answering the ambiguity
  is what let him rule.
- **P-09, `data-dv-controls`.** *"accept contract-only, it's an interesting idea to wire one legend to
  multiple charts but not required at this stage"* — an acceptance with the scope cut to the contract,
  and the wider idea named and parked in his own words rather than dropped.

★ **The lesson, stated as a method rather than an anecdote: when a LATER arrives with a sentence,
read the sentence before recording the LATER.** Three of eleven would otherwise have aged another
session while their answers sat in the note field.

## 3 — Enacting D7 forced a schema ruling nobody planned

Lane E went to add `status: "dormant"` to `footer.meta.json` and the meta validator went RED:
`meta.schema.json` defines `variants[].items` with `"additionalProperties": false` and
`patternProperties {"^\\$": {}}`, so only `name`, `use` and `$`-prefixed keys are legal. The lane took
the legal route (`$status`) and **declared the deviation rather than hiding it**.

Put to Dave, the answer was *"whatever is the best standard solution"* — `s263-D12` — and the best
standard solution is not an escape-hatch key: `variants[].status` is now a **first-class enum**
`active | dormant | deprecated` in the schema, and the footer's doormat carries `status: "dormant"`.
★ **The `$`-prefix convention exists for one-off annotations; a state three components will want is
not a one-off.** Enacted at `27f0f46`.

## 4 — The gate that was grading nothing, and the report that lied about it

`s263-D11` retired `_validate_snippets.py`'s **source-text** `requiredAria` arm, leaving the
DOM-driven arm in `_validate_dataviz.py` as the single gate for the rule. Lane A deleted the arm, its
bite-test (a bite-test for a retired arm is a guaranteed RED) and corrected four docs that claimed it
existed — and then found the thing that mattered: **every driven receipt in the repo was STALE.**

The chain: `4cc4204` (#261 lane F2, 10:58) changed `knowledge/canon/type.css`; the receipts in
`knowledge/_tests/chart-engine/_receipts.json` had been driven at 09:54 against the old hash
`295b2867…`; `_validate_dataviz.py` therefore read **STALE on all 27 pages**. ⛔ **So the gate
`s263-D11` had just made load-bearing was blocking-on-stale and grading nothing.**

The re-drive needed a browser, and the sandbox had none. Chromium 151 was installed without root —
playwright plus `libXdamage.so.1` extracted from the arm64 deb into `~/.local/lib` under
`LD_LIBRARY_PATH`. 27 pages × 8 theme×mode combos, and the result is the one worth recording:
**0 differing measured fields** against the 09:54 receipts. Marks, rows, contrast, rogue hex,
gradients, curve, aria — all identical. ⇒ **v1.0.9's charts are retroactively clean**, and that is a
measurement, not a reassurance.

★ **AND THE FINDING UNDERNEATH IT.** `knowledge/_DATAVIZ-GATE.md`, committed at `81ce08f` (12:56),
reads **PASS / 0 STALE** — while HEAD's `type.css` already differed from the receipts' hash. The
report was written from a tree that did not match HEAD. This is the #253 two-lanes-wiping pattern in
a new venue: **a lane can commit a green gate report describing a tree that no longer exists**, and
nothing in the repo compares the two. Ruling-shaped, and carried as his.

## 5 — The tenth release gate

The dataviz gate was **not among the nine release gates**, which is why nothing caught the staleness
at the v1.0.9 cut. Asked whether it should join, Dave said **"yes"** (`s263-D13`), and the enactment
is deliberately narrow: `--release` now runs a **`--receipts-fresh` check after `require_clean`**,
**write-nothing** — it refuses over stale driven receipts rather than re-driving them, because a
release that silently re-drives its own evidence is a release grading its own homework. The selftest
drives the mutant RED and the real control GREEN; the frozen, audit and CI gates still PASS. Enacted
at `5050b33`.

★ **The arc of the day in one line: a defaulted recommendation list became eleven rulings, one of
those rulings exposed a gate that was grading nothing, and closing that hole added the tenth gate to
the release line.** Nothing in that chain was planned at the opener.

## 6 — Where it ended

Rulings 423 → **436**. `_render_rulings.py --check` FRESH (and, by `s263-D10`, that check is now a
**BLOCKING wrap gate** at runbook step 4d — the rulings page is the surface Dave consults, and a wrap
that inscribes a ruling without re-rendering leaves it one session behind).

**Still open, and his:** the Stat card arrow seat · `/goal` untested · the sidebar chart glyph · the
false-green gate report above · footer's two pre-existing schema reds · `_validate_icons.py` red on a
pristine repo · `_build_integrity.py`'s 17 errors · and the fact that `_capture_gate.py` has **no
registered bite-test arm** for the D10 check it gained today.
