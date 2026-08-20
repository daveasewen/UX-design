# Receipt — #209 Wave 3 · Lane A · the fintech-row family

**Lane:** A (Opus) · **Session:** #209 · **Date:** 2026-08-20
**Brief:** `notes/_briefs/2026-08-20-209-wave3-fanout-brief-v1.md` (THE JOB, LANE A)
**Members:** transaction-row (row 91, P2) · standing-order-mandate-row (row 95, P3) · limits-meter (row 96, P3)

> ⛔ **NOTHING IN THIS RECEIPT IS A RULING.** Every fintech semantic below is PROPOSED and is
> Dave's (the Kpi-tile precedent, `s182-D2`). No registry, `MIGRATED_SNIPPETS`, `CATEGORIES`,
> spine, canon.css, `_rulings.json` or git operation was touched — the serial set is the
> conductor's, and this lane created NEW FILES ONLY.

---

## 0 · THE HEADLINE: ROW 91 CARRIES A PRIOR ADJUDICATION AND THIS LANE DID NOT OVERRULE IT

**#204 Lane N stopped on row 91 and built nothing.** Its receipt
(`notes/_receipts/2026-08-19-204-wave-laneN-fintech-rows.md`) says, verbatim:

> "Row 91 'Transaction / ledger row' **IS A DUPLICATE**. It is not a gap … I built no
> transaction row."

I re-probed its evidence rather than trusting its summary, and **the evidence is correct**:

| probe | result, verbatim |
|---|---|
| `list-items.meta.json` `build.$status` | *"PROMOTED 2026-06-22 (Dave) — TRANSACTION row brought to the Tabs-bar standard … Build green."* |
| `list-items.meta.json` `build.scope` | *"Transaction row only (the ★ payments-journey row)."* |
| `list-items.meta.json` `build.prototypeGrade` | *"9.0/9 (2026-06-22)"* |
| `List-items.reference.html` `<title>` | *"List items — Transaction row (reference implementation, gated)"* |

**The #209 brief nevertheless re-lists row 91 as a build**, because the itinerary re-probe reads
BY SLUG — which is the exact mechanism defect Lane N named ("Any derived-status instrument that
probes by slug cannot see a component that lives as a VARIANT of another"). The brief's own
survey line ("6 of its 22 GAPs were already built at #204") cannot have caught row 91, because
#204 produced no artefact for it.

**What I did with that contradiction — stated so it can be refused:**
I did not build what Lane N stopped, and I did not silently drop a briefed P2. I built **only
the form Lane N's adjudication does not cover** — the **LEDGER**: an ordered statement with a
**running balance**, column heads and a closing total. The tappable transaction row is **not
re-drawn anywhere**.

★ **The structural tell:** a running balance is not a property of a transaction, it is a
property of a transaction's **position in a sequence**. That relation is what a `<table>`
encodes and what a `<ul>` of independent `<button>` rows cannot — and List-items' row **is** a
`<button>`. It also turns a 400-line statement into 400 tab stops.

⬛ **AND THE LIVE OUTCOME, NOT A HEDGE:** if Dave rules the product's statement is a LIST and not
a LEDGER, **`transaction-row` should not exist** and row 91 collapses into List-items exactly as
Lane N said. Deleting the pair costs nothing — nothing registers them.

---

## 1 · FILE LIST — six new files, plus this receipt

| # | path | bytes |
|---|---|---|
| 1 | `knowledge/snippets/Transaction-row.reference.html` | 33,183 |
| 2 | `knowledge/components/transaction-row.meta.json` | 15,166 |
| 3 | `knowledge/snippets/Standing-order-mandate-row.reference.html` | 38,401 |
| 4 | `knowledge/components/standing-order-mandate-row.meta.json` | 15,684 |
| 5 | `knowledge/snippets/Limits-meter.reference.html` | 33,495 |
| 6 | `knowledge/components/limits-meter.meta.json` | 15,508 |
| 7 | `notes/_receipts/2026-08-20-209-wave3-laneA-fintech-rows.md` | this file |

**No existing file was edited.** No `intent` field was authored on any of the three (W-58 is
parked; none of these is a chart). Renders used during the build live OUTSIDE the repo
(`NON-REPO: the session outputs folder, laneA-renders/*.png` — six PNGs, light + dark per
member) per `s191-D2` home-or-declare; they are working artefacts, not deliverables.

---

## 2 · CLAIM TABLE — every claim carries a probeable token (`s182-D1`)

| # | claim | probe — re-runnable, exactly as written | verdict |
|---|---|---|---|
| 1 | Row 91's tappable form is gated and promoted, and is NOT re-drawn by this lane | `grep -c '<button type=' knowledge/snippets/Transaction-row.reference.html` → **0** (the ledger contains no control of any kind). ⚠ Note the probe form: a bare `grep -c '<button'` returns **4** and is a FALSE probe — all four hits are PROSE explaining why List-items' button row cannot be used. The probe must match the markup, not the argument. | ✅ |
| 2 | The ledger is a real table with the relations a list cannot carry | `grep -c 'scope="rowgroup"\|scope="col"\|<tfoot' knowledge/snippets/Transaction-row.reference.html` → non-zero for each | ✅ |
| 3 | NO money colour is invented in any of the three | `grep -nE 'rag[./](success\|error)-ink' knowledge/snippets/{Transaction-row,Standing-order-mandate-row,Limits-meter}.reference.html` → **only prose mentions explaining the deliberate non-binding; zero CSS declarations** | ✅ |
| 4 | The leading-trim block is the CURRENT one, byte-identical to Command-palette line 36 | `python3 -c "cp=open('knowledge/snippets/Command-palette.reference.html').read().split(chr(10))[35]; import glob; print(all(cp in open(f).read() for f in ['knowledge/snippets/Transaction-row.reference.html','knowledge/snippets/Standing-order-mandate-row.reference.html','knowledge/snippets/Limits-meter.reference.html']))"` → **True** (run at build: IDENTICAL, 328 chars) | ✅ |
| 5 | Every manifest var resolves against the token store | `python3 knowledge/_validate_binds_resolve.py` → **1,313 vars, 0 var failures**; the only failures are check-D canon blocks (claim 12) | ✅ |
| 6 | 4px-grid gate clean on all three | `python3 knowledge/_validate_grid.py` → **4 off-grid values, all in `Range-slider` / `Rating` / `Transfer-list` (Lanes B/C). Zero in Lane A files** | ✅ |
| 7 | a11y gate: zero failures with the three present | `python3 knowledge/_validate_a11y.py` → *"a11y gate: 100 snippet(s), 0 failure(s)"* | ✅ |
| 8 | Snippet/token gate clean on all three | `python3 knowledge/_validate_snippets.py 2>&1 \| grep -cE "Transaction-row\|Standing-order-mandate\|Limits-meter"` → **0** | ✅ |
| 9 | Type-composite debt UNCHANGED — these three add zero | `python3 knowledge/_validate_type_composites.py` → *"1097 violation(s)"*, the #203 measured baseline, and no Lane A file is named | ✅ |
| 10 | The metas are schema-valid | `python3 knowledge/_probe_registry/probe_meta_schema.py --check` → *"101 meta(s) checked · 0 finding(s)"* | ✅ |
| 11 | Descender-clip gate passes on the truncating labels | `python3 knowledge/_validate_descender_clip.py` → *"PASS — every truncating label is descender-safe (116 file(s))"* | ✅ |
| 12 | ⛔ binds-resolve check D FAILS for all three — DECLARED, not hidden | `python3 knowledge/_validate_binds_resolve.py` → *"91/100 canon blocks · 9 failure(s)"*, naming `Transaction-row`, `Standing-order-mandate-row`, `Limits-meter` (+ 6 Lane B/C files) | ⛔ **CONDUCTOR'S** |
| 13 | ⛔ `_validate_kg.py` FAILS — the new metas name contexts the node registry has never seen | `python3 knowledge/_validate_kg.py` → *"_nodes-pattern.json DRIFTED … _nodes-context.json DRIFTED"*; and `python3 -c "import json;s=json.dumps(json.load(open('knowledge/components/_nodes-context.json')));print('statement-views' in s,'payment-limits' in s)"` → **False False** | ⛔ **CONDUCTOR'S** |
| 14 | Both glyphs in the mandate row are byte-matched from the real library, not drawn | `diff <(grep -o 'd="M12.9891[^"]*"' knowledge/snippets/Standing-order-mandate-row.reference.html \| head -1) <(grep -o 'd="M12.9891[^"]*"' knowledge/assets/icons/media/document.svg)` → identical; same for `menu-more-horizontal.svg` | ✅ |
| 15 | The two-target row shape WORKS — not asserted, driven | headless Chromium: `document.elementFromPoint` at each row centre → the stretched `<a class="mr-payee">`; at each button centre → the button's own content; **every manage button measures 44×44**; Tab order alternates link → button; **14 focusables across 8 drawn rows** | ✅ **DRIVEN** |
| 16 | The meter bar geometry matches the authored values in a real browser | headless Chromium computed fill widths: **64.00 · 96.40 · 100 · 0 · 64.00 · 83.56 · 31.00 %**, fill `#FFFFFF` on track `#484848` in dark (ink on track, no RAG) | ✅ **DRIVEN** |
| 17 | `role="meter"` is still unused and still unruled — the search RE-RUN, not cited | `grep -rln 'role="meter"' knowledge/snippets/` → **2 files (Limits-meter, Runway-bar), every hit PROSE not markup, i.e. 0 of 91 pre-existing snippets**; `grep -icE '\bmeter\b' knowledge/_rulings.json` → **0** | ✅ **OPEN** |
| 18 | Progress-bar already claims the limits-meter pattern by name | `python3 -c "import json;print(json.load(open('knowledge/components/progress-bar.meta.json'))['relationships']['commonPatterns'])"` → includes **`'savings goal / limits meter'`** | ✅ **and it argues against the component** |

---

## 3 · WHAT WAS DRIVEN — a real browser, light AND dark, all three

Headless Chromium (`chromium_headless_shell`, `--no-sandbox --disable-dev-shm-usage
--disable-gpu`), each file loaded from disk, `data-theme` toggled live, full-page screenshots
taken in **both modes for all three members** (6 PNGs) and **looked at**, plus scripted
measurement of computed styles, hit boxes, hit-testing and tab order.

**Three defects were found BY LOOKING, and every gate was green over all three.** This is the
#204 lesson repeating, and it is the most useful thing in this receipt:

1. **⛔ THE LEDGER'S MONEY COLUMNS WERE INVISIBLE.** The first draft carried both money forms in
   ONE table and switched with `display:none` inside a container query. In a
   `table-layout:fixed` table a `display:none` cell still reserved its column slot, so the
   visible columns stopped ~130px short of the table box — and before that, with the browser
   default `auto` layout, the long merchant descriptor stretched the description column past
   the container and the scroll region **clipped every money column and the running balance off
   the right-hand edge. The wide specimen rendered with one visible column, "Description", and
   no figures at all — the entire point of the component.** Grid, a11y, snippets,
   binds-resolve and descender-clip were ALL GREEN over that draft.
   *Repair:* `table-layout:fixed` + declared column widths, and the two money forms became
   **two tables** — which is also the more honest drawing, because P1 asks Dave to CHOOSE one,
   not to watch one become the other at a breakpoint.
2. **⛔ THE CANCELLED MANDATE ROW WAS AN UNREADABLE GHOST.** The draft copied Document-row's
   DISABLED treatment onto it — `text/disabled` on every text element, **#E1E1E1 on #FFFFFF =
   1.42:1** — so the payee, the amount and the reason were all invisible. No gate fires,
   because disabled content is exempt from 1.4.3 (the same class Document-row caught at #204 on
   its GLYPH; here it had swallowed the TEXT).
   *Repair — a CATEGORY correction, not a colour tweak:* **a cancelled mandate is not disabled
   content, it is HISTORY.** You must still be able to read who you were paying and when you
   stopped. The row is now ordinary ink with a "Cancelled" chip; only the CONTROL is disabled.
3. **⛔ THE PAYEE WAS BEING CRUSHED BY ITS OWN CHIPS.** With the title line as a non-wrapping
   flex row, the tag and status chips were `flex:none` and the payee was the only shrinkable
   item — rows carrying both chips rendered "Bristol …" and "Kestrel Ass…". Measured in the
   browser at 560px: payee element widths **66–175px BEFORE, 204–227px AFTER** the fix (the
   line now wraps and the name claims a 160px basis). Same class fixed pre-emptively in the
   ledger's payee cell.

Also driven and passed: the two-target row shape (claim 15), the meter geometry (claim 16),
theme inversion in both modes on all three, and zero horizontal overflow at 1400px.

---

## 4 · EVERY FINTECH / DESIGN QUESTION — NAMED, NOT SETTLED

**All of these are Dave's. None is answered by construction.**

### Q1 — ⛔ Should `transaction-row` exist at all? *(the biggest one)*
#204 ruled row 91 a duplicate. The ledger form is the only part of row 91 List-items does not
hold. If the product's statement is a list, this component should be deleted and row 91 marked
Duplicate. **Live outcome, stated on the file's own face.**

### Q2 — Do ledger CREDITS take the ruled green seat?
The system owns coloured monetary seats — `rag.success-ink` / `rag.error-ink`, MONO ONLY
(`s155-D1` / `s158-D2` / `s158-D3`). **They are deliberately NOT bound.** Every figure in all
three components is monochrome. Binding them on a ledger would have been ruling on Dave's behalf.

### Q3 — Two money columns, or one signed column? *(both drawn)*
Two columns carries the sign STRUCTURALLY — a second, non-colour channel a signed column does
not have. One signed column is what a phone width wants.

### Q4 — Does a pending row show an em dash where the balance will be, nothing, or a projection?
Drawn as an em dash with an aria-label, because the balance does not exist until it settles.

### Q5 — The status vocabularies and their chip bindings
Ledger: Pending / Reversed, settled rows silent. Mandate: Paused / Last payment failed / N
payments left / Cancelled, active rows silent. Meter: within limit / approaching / at limit.
⛔ **"Failed" and "At limit" sit on the WARNING seat, not the error seat. That is declared
RESTRAINT, not a considered ruling** — the error seat touches the two-red law (`s151-D1`) and is
not this lane's to touch.

### Q6 — Standing order vs Direct Debit: one component or two?
They are legally and operationally different objects (customer-controlled fixed instruction vs a
payee pulling a variable amount under the Direct Debit Guarantee). The row says which one **in
text**, in a Tags chip, never by hue. Drawing them in one list does **not** settle it.

### Q7 — For a variable Direct Debit, which figure shows?
Drawn: the LAST taken figure, with "Amount varies" in the rhythm line — rather than presenting a
stale number as if it were the next one.

### Q8 — ⛔ Should `limits-meter` exist at all?
`progress-bar.meta.json` `commonPatterns` **already names 'savings goal / limits meter'**. The
bar is Progress-bar's, copied byte-for-byte. Three live outcomes: keep it, merge it into
Runway-bar as a parameterised "allowance" mode, or delete it and use Progress-bar with a domain
`aria-valuetext`.

### Q9 — Limits meter vs Runway bar: two components or one?
Runway's maximum is **my own balance** and its horizon is a date I DISCOVER. A limit's maximum
is a **cap set by the bank** and its horizon is a repeating RESET known in advance. Runway's
ceiling is a fact about my money; a limit's ceiling is a rule about my permission. **I drew this
one to Runway-bar's own anatomy deliberately, so that if Dave merges them the two files already
rhyme.**

### Q10 — Does the meter fill with what is USED, or empty with what REMAINS?
Drawn as USED (like every progress bar). REMAINING — a fuel gauge — is the other honest reading
of the word "meter", and is what "how much do I have left" actually asks.

### Q11 — The "Per payment" row is a bar that will never fill
It renders as an empty track reading "£0 of £10,000 used" and always will: a per-payment cap is
a ceiling PER EVENT that never accumulates. **Left drawn so Dave can see the oddity rather than
read about it.** Should it be a bar at all, or a plain stated rule?

### Q12 — `role="progressbar"` or `role="meter"`? *(inherited, carried forward unchanged)*
Raised by Runway-bar at #204. The search was **RE-RUN**, not cited (claim 17): zero of the 91
pre-existing snippets use `role="meter"`, and `_rulings.json` says nothing. If Dave rules
"meter", **both components change together.**

### Q13 — Should a CANCELLED mandate be dimmed at all?
It is not dimmed here **because the dimmed version was drawn, rendered, and could not be read**.
If Dave wants dimming, it needs an ink that is legible.

### Q14 — The leading glyph for a mandate
⚠ **No recurring-payment glyph exists in the library.** Probe, run:
`ls knowledge/assets/icons/*/ | grep -iE "recur|repeat|refresh|cycle|rotate|mandate"` →
`refresh.svg`, `refresh-active.svg`, `rotate-left.svg`, `rotate-right.svg` — four RELOAD glyphs,
none of which means "this payment repeats". The generic `media/document.svg` stands in. **An
`_ICON-GAPS.md` entry may be owed — that file is the conductor's, not this lane's.**

### Q15 — Should a ledger line be openable (a receipt view)?
Drawn passive. Making it interactive re-opens the List-items question in Q1.

**⛔ Also NOT settled, by construction:** the two delta conventions question. **None of the three
components paints a delta, an arrow or a series.** There is no trend on any of these pages.

---

## 5 · WHAT STAYS UNPROVEN

1. **The canon-block projection.** `_validate_binds_resolve.py` check D FAILS for all three
   (`.cn-transaction-row`, `.cn-standing-order-mandate-row`, `.cn-limits-meter` do not exist in
   `canon.css`). Six Lane B/C snippets are in the same state — **9 failures in one gate run**.
   Until the conductor projects those blocks, theme cascade projection is silently OFF for these
   files, so **only the light/dark legs authored in each snippet have been seen. Console,
   Legacy and Supercharge are UNPROVEN for all three members.**
2. **`_validate_kg.py` FAILS** — the new metas name contexts and patterns the generated node
   registries have never seen (`statement-views`, `payment-limits`, `payment-management`,
   `reconciliation` all absent from `_nodes-context.json`). `gen_kg_edges.py` must be re-run.
   Shared generated files — **conductor's**.
3. **Four-theme contrast for the meter's fill-on-track is CARRIED, NOT MEASURED.** The figures
   quoted in `Limits-meter.reference.html` (Mono/Console/Legacy 15.27 light / 9.15 dark,
   Supercharge 14.02 / 10.46) come from Runway-bar's own declaration, itself quoting
   Progress-bar's meta. **Nothing was re-measured at #209.** Declared as carried.
4. **`_validate_state_contrast.py` NOT RUN** — a filtered run overwrites the tracked
   `_STATE-CONTRAST-AUDIT.md`, which is outside this lane's fence. Same declaration Lane P made
   at #204. **Owed.**
5. **Hit areas were measured in ONE browser at ONE zoom** (headless Chromium, 1400px viewport,
   plus a 340/400px container). No 480px viewport pass, no second engine, no zoom pass.
6. **The gated `List-items` transaction row still contradicts `copy-025` and still does not
   compose Amount-display** — #204 Lane N's finding 3, unrepaired. This lane **demonstrates** the
   correct composition and **does not repair the parent**: `List-items` is gated, promoted, and
   not a worker lane's to edit. **The repair is still owed there.**
7. **Nothing here has been seen by Dave**, and nothing is registered anywhere. Every one of the
   fifteen questions above is open.
8. **The itinerary's own row-91 status is still `Partial` / derived `GAP` / drift `OVERSTATED`,
   and #204 already measured that as false in the OPPOSITE direction.** Lane N proposed marking
   it **Duplicate** and did not merge it (the itinerary files are fenced). **Still not merged.**

---

## 6 · HANDOFF TO THE CONDUCTOR — the serial set this lane could not touch

1. `.cn-transaction-row`, `.cn-standing-order-mandate-row`, `.cn-limits-meter` blocks in
   `canon/canon.css` (clears 3 of the 9 check-D failures).
2. Re-run `gen_kg_edges.py` (clears `_validate_kg.py`).
3. `component-types.json` · `CATEGORIES` · `gen_showroom.py` · `_validate_radius.MIGRATED_SNIPPETS`
   registrations, if these three are to be kept.
4. **Store rows for the three new components and for this receipt** — the #185 forgotten-document
   class: a document with no store row is invisible.
5. ⚠ **The 4 off-grid failures in `_validate_grid.py` are Lane B/C's** (`Range-slider` 6px gap +
   10px top, `Rating` 10px gap, `Transfer-list` 10px padding), not this lane's. Named here so
   they are not attributed to the wave at large.
6. Consider whether row 91's itinerary status should finally become **Duplicate** pointing at
   `component:list-items` `type: "transaction"` — Lane N asked at #204 and it is still open.
7. ⚠ **RUNNING THE GATES REWROTE TRACKED FILES, AND THAT IS DECLARED, NOT HIDDEN.** A
   filesystem check (`find knowledge notes -newermt "2026-08-20 12:30" -type f`, no git run)
   shows three tracked artefacts modified as a SIDE EFFECT of the gate runs in this receipt —
   `knowledge/_A11Y-GATE.md`, `knowledge/_SNIPPET-AUDIT.md`,
   `knowledge/_graph-mark-observations.jsonl` — plus `notes/_REHEARSAL-LOG.jsonl`. **No lane
   edited them by hand.** They are gate-authored outputs and they are shared with Lanes B and C,
   which ran the same gates, so attribution is the wave's and not any one lane's. This is the
   same class Lane P declared at #204 about `_validate_state_contrast.py` overwriting
   `_STATE-CONTRAST-AUDIT.md`. **The conductor must reconcile these four paths deliberately —
   never `git add -A`.**
