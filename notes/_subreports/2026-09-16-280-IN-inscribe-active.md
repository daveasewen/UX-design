# LANE IN — REPORT — Dave's 15-base active review, inscribed: 9 twins landed, 6 rows asked back

#280 · 2026-09-16 · enacting the #279 wrap's standing instruction under `s277-D6` · opus seat.
Everything below was RUN, not recalled. His export is read WHOLE and quoted verbatim where it is quoted.

---

## For Dave — in plain words

**Nine of your fifteen rows are now in the library, and six are back with you.**

You went through the fifteen icons that came back with two or three drawings all called "… Active" and
named a twin on every one. On nine of them the drawing you ticked, the drawing your note names and the
twin you chose all said the same thing — so those nine twins are now the default in the icon store, and
the nine drawings you called wrongly labelled are written down as icons of their own that need an
inactive version drawn. Nothing was guessed on the other six: they are byte-untouched, and each one is a
single question on a page for your eye — **`notes/_lanes/280/inscribe-active/ASK-2026-09-16.html`**, the
same shape as the sheet you filled in, with the drawings side by side and your own words quoted back.

**Inscribed (9):** alert · contact-chat-ai · dentist · e-coupon · laboratory · renew · user-staff ·
voice · withdraw-overpayment.

**Asked (6) — one question each:**

1. **electricity** — You named `electricity-active` as the twin and then ticked that same drawing as one
   that is its own icon, while your note names `electricity-active-2` as the mislabelled one; which did
   you mean?
2. **employee-banking-solution** — You named `employee-banking-solution-active-2` as the twin and wrote
   that `employee-banking-solution-active` is mislabelled but did not tick it; should it be written down
   as its own icon that needs an inactive version drawn, or is it just the right picture under a wrong
   name?
3. **financial-health-check** — Same shape: you named `financial-health-check-active-2` as the twin and
   wrote that `financial-health-check-active` is mislabelled without ticking it; does it go on the list?
4. **reward** — Same shape: you named `reward-active-2` as the twin and wrote that `reward-active` is
   mislabelled without ticking it; does it go on the list?
5. **jade-lifestyle** — You named `jade-lifestyle-active` as the twin but wrote that you were not certain
   and that both the base drawing and `jade-lifestyle-active` are mislabelled; does that twin stand, or
   is this row still open?
6. **traditional-chinese-medicine** — You ticked `traditional-chinese-medicine-active-2` as a drawing
   that is its own icon, but your note says that one is correctly labelled and that the base drawing and
   `traditional-chinese-medicine-active` — the twin you named — are the wrong ones; which reading is
   right?

The sixth was not on the list the wrap named. It came out of reading every note: on
`traditional-chinese-medicine` your tick and your note point at opposite drawings, so it was left alone
like the others rather than read one way and inscribed.

**One thing worth your word later, not now.** The generator that writes the icon store still treats
"which drawing is the twin" as an open question, so if anyone regenerates that file your nine answers
are wiped. The file now says so in its own header, and the repair — teaching the generator to read your
export — is a small lane, not a decision.

---

## 1. What was read, and how the fifteen rows were split

`notes/_lanes/279/active-review/DAVE-EXPORT-active-2026-09-16.json` (15:55:41.531Z), whole: 15 answers,
every one `choice: "twin"` (7 bare `-active`, 8 `-active-2`), 12 of them carrying a flag or a note.

The split is DERIVED in `_inscribe.py`, not typed: each note line is read for the drawings it names and
for whether it calls them wrongly labelled, correctly labelled, or uncertain, and a row is ASKED when

* his note names drawings his ticks do not (or the other way round),
* his note calls the twin he named — or the base itself — wrongly labelled,
* his note calls a drawing correctly labelled that his tick calls its own icon, or
* his note says he is not certain.

The five rows the #279 wrap already named are an **assertion** over that derivation (`WRAP_NAMED_ASK`),
never its input: if any of them came out INSCRIBE the script refuses to run. They all come out ASK, and
one more with them.

| | rows |
|---|---|
| INSCRIBE (9) | alert · contact-chat-ai · dentist · e-coupon · laboratory · renew · user-staff · voice · withdraw-overpayment |
| ASK (6) | electricity · employee-banking-solution · financial-health-check · jade-lifestyle · reward · **traditional-chinese-medicine** |

**The sixth, found by reading.** `traditional-chinese-medicine`: flag `…-active-2`, twin `…-active`,
note *"traditional-chinese-medicine-active-2 is correctly labeled / traditional-chinese-medicine,
traditional-chinese-medicine-active - mislabeled"*. The tick says `-active-2` is its own icon; the note
says `-active-2` is the correct one and the twin he named is not. Flag and note disagree, so the note is
his sentence and the row is asked — the wrap's instruction applied to a row the wrap had not seen.

**One near-miss, said out loud.** A first pass read *"incorrectly labeled"* as *"correctly labeled"* and
put `alert` and `contact-chat-ai` in the ASK pile. Caught by reading the printed reasons against his
words; the regex now refuses `in`-prefixed matches and the two rows come out INSCRIBE, which is what his
note says.

## 2. The edits to `knowledge/_icon_nodes.json` — textual spans, insertions and replacements

No regenerate; `gen_kg_icons.py` was not run against the tree. Four kinds of edit, each on an exact span:

1. **Nine `defaultActive` edges** — `"t": null` becomes `"t": "icon:<his twin>"`, the `$note` (the
   candidate list) is kept unchanged, and a `$ruled` sentence is added naming him, the twin, the export
   and its timestamp, and the fact that a regenerate would drop it.
2. **Nine rows leave `unresolved`** — they are not declared nulls any more. They move into a new
   `ruled` ledger beside it, carrying `t`, the candidate list, **his note verbatim** (`his_note`), the
   drawings he ticked (`his_flags`) and the export path + timestamp. `unresolved` 19 → 10, `ruled` 0 → 9;
   nothing is dropped and the selftest asserts the two ledgers still sum to 19.
3. **`edge_types.defaultActive`** said *"DECLARED-NULL ONLY — never drawn, never resolved"*. That stopped
   being true, so it now says drawn only where his own review names the twin, 9 of 15, the other 6 still
   null, never inferred.
4. **`$description`** said *"never hand-edit"*. It now says it, and then says the exception and the
   consequence: the generator still declares `defaultActive` a null, so regenerating this file drops his
   answers until it learns to read his export.

`git diff --numstat`:

```
20	0	knowledge/_ICON-GAPS.md
136	62	knowledge/_icon_nodes.json
```

(The other two dirty files under `knowledge/` — `_build_kg_explorer.py`, `_kg_explorer.template.html` —
are lane LY's, untouched here.)

The six asked rows are byte-identical: `t: null`, no `$ruled`, still in `unresolved`, and the selftest
asserts exactly that.

## 3. The exporter-defect list — where it went, and why there

**There was no such list.** `grep` over the tree for "exporter-defect" returns only the wrap's own
instruction to make one. The durable log of this exact defect class already exists —
`knowledge/_ICON-GAPS.md` § *Mislabeled assets (verified by render, 2026-07-17 · T8 footer social strip)*,
where the social-glyph mislabels and the inverted `payment` pair live — so the new list is a section in
that file, immediately before the `-active` convention section, inserted and nothing else changed.

Nine drawings across eight bases, each with **his words verbatim** and the twin he named beside it:
`alert-active-2`, `contact-chat-ai-active`, `dentist-active`, `dentist-active-3`, `laboratory-active-2`,
`renew-active`, `user-staff-active`, `voice-active-2`, `withdraw-overpayment-active`. The section ends by
naming the six asked rows and saying their drawings join the table when he answers. `e-coupon` is the one
inscribed row that flags nothing, so it contributes none.

The same nine, machine-readable, are in the node file's `ruled` ledger (`his_flags`) — the list and the
store say the same thing from the same input.

## 4. Gates — every line run at this seat

```
$ python3 notes/_lanes/280/inscribe-active/_inscribe.py --selftest
  ok     the classification is his: 15 rows read, 9 inscribed, 6 asked, and every row the #279 wrap named as disagreeing is among the asked
  ok     alert: the default is his twin alert-active, the variant edge stands, the null is retired, and his own words are kept
  ok     contact-chat-ai: … contact-chat-ai-active-2 …
  ok     dentist: … dentist-active-2 …
  ok     e-coupon: … e-coupon-active …
  ok     laboratory: … laboratory-active …
  ok     renew: … renew-active-2 …
  ok     user-staff: … user-staff-active-2 …
  ok     voice: … voice-active …
  ok     withdraw-overpayment: … withdraw-overpayment-active-2 …
  ok     the 6 asked rows are untouched: no default drawn, still declared nulls, nothing in the ruled ledger
  ok     the file still parses, the population is unchanged (676 nodes / 1294 edges / 15 defaults) and no edge type appeared
  ok     nothing is dropped: every null that left `unresolved` is in `ruled`, and the ledgers together still carry all 19 rows the file owned
SELFTEST PASS   rc=0
```

One bite per inscribed base, as the brief asks, and each bite is four assertions at once: the default is
his twin, the `activeVariantOf` edge from that twin to the base stands (and from every other candidate —
no repair was needed, all 31 were already drawn), the declared null is retired, and his own words survive
in the ledger.

```
$ python3 notes/_lanes/277/icons-propose/gen_kg_icons.py --selftest        → 19 ok, SELFTEST PASS, rc 0
$ python3 notes/_lanes/277/icons-propose/_mutate.py /tmp/s280/mut          → BASELINE PASS, ALL MUTANTS CAUGHT (26, 0 survivors), rc 0
$ python3 knowledge/_validate_kg.py                                        → OK, rc 0 (139 metas; every ref parses+resolves)
$ python3 notes/_lanes/280/inscribe-active/_drive_ask.py                   → 29 checks, 0 failures
```

The generator's own selftest and mutants run on its mini corpus, so they are green **because** the
inscription is a hand edit on the landed file and not a generator change — that is the finding in §6, not
a gate that was dodged. `_validate_kg.py` is the gate that reads the LIVE file, and it resolves the nine
new edge targets.

## 5. The ASK page

`notes/_lanes/280/inscribe-active/ASK-2026-09-16.html` — 106,652 B, single file, inline CSS/JS/SVG,
swiss idiom, built by `_build_ask.py` from the node file's remaining declared nulls, his export and the
SVGs. Six rows. Each row: the base and its 2 drawings at 48px and 16px on a white chrome and a `#111`
chrome side by side; a quoted block — **you named** / **you ticked** / **you wrote** — with his note
verbatim; then ONE question in plain prose and 3–4 radio answers, each answer naming the drawings it
would write down, plus a free note. Progress in the sticky nav, localStorage, **Export** writing
`DAVE-EXPORT-ask-active-2026-09-16.json` in the #279 envelope exactly (`{page, at, exportedAt,
answers:{<base>:{choice, twin, flags[], note}}}`), Copy JSON and Clear all beside it.

Plain prose only: the builder refuses if a ruling id appears above the footer, and the driver re-checks
it in the rendered DOM.

**Driver, 29 checks 0 failures** (`_drive_ask.py`, Chromium through `knowledge/_render/seat_env.sh` —
the seat's own headless shell, nothing downloaded): 6 sections, 18 glyphs × 4 renders = 72 `<svg>`, no
duplicate DOM ids, virgin first load, no ruling id in the body, **his note quoted verbatim on every
row**, progress 0 → 2 of 6, chosen card marked, download filename, envelope keys, per-answer shape, each
answer exporting exactly the twin and flags its option names, a note with no answer still exporting,
unanswered rows null, localStorage round-trip across a reload, no page errors, no horizontal overflow at
1280 and 390 in both themes.

**Screenshots, looked at** — `shots/ask-{1280,390}-{light,dark}-{top,row01}.png`, 8 files, 664 KB, each
from a fresh never-driven context asserted virgin before the PNG. Full-page PNGs were not taken: the disk
is at 99% (156 MB free). What the first row shows is worth saying: `electricity-active-2` is a **smiley
face**. His note is plainly right, and the page shows him why the question is being asked.

## 6. Findings — for the conductor, none of them re-opening the inscription

**F1 — a regenerate wipes his answers.** `gen_kg_icons.py` declares `defaultActive` a null-only type
(`NULL_ONLY_TYPES`), and bite 3 of its selftest asserts no `defaultActive` edge ever carries a target. So
the generator and the landed file now disagree on purpose, and `--land` would silently drop nine of
Dave's decisions. Mitigated by saying so in the file's own `$description` and here; the fix is a lane that
teaches the generator to read `DAVE-EXPORT-active-*.json` (and the ASK export after it) and to keep bite 3
for the rows he has not answered. Small, and it should happen before anything regenerates the assets.

**F2 — `_validate_icons.py`'s twin arm is still the known-unsafe assumption.** `s277-D6` recorded that
its `active_names` arm assumes the bare `-active` is the twin. On the nine inscribed bases we now know
better, and on **5 of the 9** the bare form is NOT the twin (contact-chat-ai, dentist, renew, user-staff,
withdraw-overpayment). Repairing, scoping or removing that arm is downstream of the review and is not
touched here.

**F3 — the explorer draws six asset edge types and `defaultActive` is not one of them**
(`ASSET_DRAWN` in `_build_kg_explorer.py`). So the nine inscribed defaults are in the store and invisible
on the graph. That is the state as landed under `s277-D4`, not a regression from this lane; whether a
resolved `defaultActive` should draw is a question for the lane that owns the explorer.

**F4 — the #279 sheet's builder derives its 15 rows from `unresolved`.** Re-running
`notes/_lanes/279/active-review/_build_review.py` now asserts `n_bases == 15` and would REFUSE, because
six nulls remain. That is the instrument telling the truth about a finished review, not a break; it was
not re-run, and the ASK page is its successor.

## 7. What was not done, with size

* No full-page screenshots of the ASK page (disk at 99%); the first viewport and the first row are shipped
  in both themes at both widths. Small.
* The four `-active` drawings named in the asked rows are NOT on the defect list, by design — they join it
  when he answers. Zero.
* `_LIVE-STATE.md` / `_CHAIN.md` still carry the "unread by the record" banner; updating the live state is
  the wrap's, not a build lane's. Small.

## 8. Files

| path | what |
|---|---|
| `knowledge/_icon_nodes.json` | 9 defaults inscribed, 9 nulls retired into a `ruled` ledger, two header sentences repaired (+136 −62) |
| `knowledge/_ICON-GAPS.md` | the exporter-defect list, his words verbatim (+20) |
| `notes/_lanes/280/inscribe-active/_inscribe.py` | the classifier, the span edits, the defect-list writer, the selftest (one bite per inscribed base) |
| `notes/_lanes/280/inscribe-active/_build_ask.py` | builds the ASK page; refuses on a leaked ruling id or a missing glyph |
| `notes/_lanes/280/inscribe-active/_drive_ask.py` | 29 checks + the never-driven screenshots |
| `notes/_lanes/280/inscribe-active/ASK-2026-09-16.html` | the six questions for Dave |
| `notes/_lanes/280/inscribe-active/_driver-export.json` | a sample export from the driven pass |
| `notes/_lanes/280/inscribe-active/shots/` | 8 PNGs, 664 KB |
