# Receipt — #203 Wave 3b, Lane H · the itinerary class-fix

*Worker receipt against `_BRIEF-wave3b-verified-work-2026-08-19-v1.md` (extending
`_BRIEF-wave3-foundations-2026-08-19-v1.md`). Opus work sub.*
*⛔ **Nothing here is a ruling.** No commit, no push, no `git checkout/restore/stash`. No git command
of any kind was run (the lane binding forbade them, so the usual `git log --oneline -1` HEAD stamp is
DECLARED ABSENT, not silently skipped). `knowledge/_rulings.json`, `knowledge/tokens/*`, `MEMORY.md`,
`_DS-IMPROVEMENTS.md`, `_validate_radius.py`, `gen_showroom.py` all untouched. `_build_all.py` NOT run.
No other generator run, not even `--check` (Lane G owns that surface this wave).*

**Context gauge at close** — `knowledge/_checkin.py --no-rehearse --no-block`, run first-hand:
FILL **145,808 real** · boot **56,488** (inside the ruled band) · peak 145,808 over 30 turns ·
room to the advisory stop line 150,929 = **5,121**. ⚠ Declared, as sibling lanes declared: `_checkin.py`
reads the newest mounted transcript and I cannot prove from inside a sub that it found mine rather than
the conductor's. Treat as ORDER-OF-MAGNITUDE. `--no-rehearse` used deliberately: the default path
appends to the shared rolling `notes/_REHEARSAL-LOG.jsonl` and five sibling lanes are live in this
same tree — an unattributable append to a shared rolling file is exactly what the fence forbids.

---

## 0 · The headline

The itinerary's `Status` column is now **derived, not typed**. `knowledge/gen_itinerary_status.py`
measures all 124 rows against the store and emits Dave's surface plus a machine-readable sidecar.

Measured at close of lane: **86 rows agree · 35 rows STALE (itinerary understates the store) ·
3 rows OVERSTATED · 0 UNRESOLVED**. The TRUE-gap list is **23 Layer-1 rows** (below), plus Layer 2
as **one** structural gap rather than 28 component gaps.

And the second, sharper finding: **the wave-3a "18/18" number was itself produced by slug matching,
and the two lanes that swept widest disagreed with each other.** Lane F's sweep called rows
13/53/63/86 "genuinely absent" and flagged 17/19/52/89 as a declared miss; Lane A called 19 of 20 P1
rows present. Both were reading the same disk. Rows 13/17/19/52/63/89 live under names the row text
does not produce (`Form-layout`, `Amount-input`, `Secure-entry`, `Stat-card`, `Modals` +
`Modal-lightbox`, `Amount-display`). **A slug mismatch is indistinguishable from an absence**
[[unmatched-grep-is-not-an-absence]] — so the class-fix is not "re-status the column", it is
"make the name→artefact link carry its evidence, and refuse to guess when it doesn't".

## 1 · Step 0 — the premise, verified first-hand

| Claim inherited | Verified? | Probe (named, quoted) |
|---|---|---|
| HEAD sha | **NOT ESTABLISHED — declared** | lane binding: ⛔ no git commands. Every finding below is measured against the WORKING TREE, which is the honest unit here anyway. |
| The itinerary carries 124 rows | ✅ TRUE | parsed `xl/worksheets/sheet1.xml` from the .xlsx with stdlib `zipfile` — 124 data rows, sheet `Summary` says "Total items in itinerary 124" |
| Its `Status` column is hand-maintained and stale | ✅ TRUE, **and measured**: 38 of 124 rows disagree with the store | `gen_itinerary_status.py` drift table |
| Wave 3a's "18/18 already existed" | ✅ TRUE **as a count**, ⚠ but **arrived at by a method that also produced four false absences** | lane A/B/D/E/F receipts vs. lane F's own declared miss on rows 17/19/52/89 |
| Row 86 brand mark is the one TRUE P1 gap | ⚠ **REFINED, not confirmed** | `ls knowledge/snippets/ \| grep -iE 'brand\|logo\|mark'` → ∅; `ls knowledge/components/ \| grep -iE …` → ∅; `ls showroom/ \| grep -iE …` → ∅; **but** `knowledge/assets/logos/` holds **12 official SVGs** (masterbrand, hexagon, identifier × light/dark × colour/mono). Verdict: **ASSET-ONLY** — the raw assets exist, the component does not. Whoever builds it starts from those files, not from scratch. |
| "most P2/P3 are true gaps" | ⚠ **FALSE as of this run** — five sibling lanes are landing P2 rows right now | rows 21/22/23/35/36/37/55/56 all moved from GAP to PARTIAL/BUILT **between two runs of the generator, minutes apart** |
| The 2026-07-14 files are frozen | ✅ HONOURED | neither the `.xlsx` nor the `.html` was opened for writing; the generator has no write path to either |

**Searched twice before calling any of this new** [[unrun-search-indistinguishable-from-absent-record]] —
declared limitation: `_memento_search.py` was NOT run this lane (it is a shared instrument and my
binding forbade running other generators; the store-search evidence I rely on is the one quoted in
Lane A's receipt, which searched `"itinerary stale P1 gaps already built"` and a direct regex over
`_rulings.json` for `itinerar|P1 gap|foundations wave` → 1 hit, `s174-D1`, not on point). **This is a
borrowed search, not mine.** If the conductor wants it first-hand, it costs one call.

## 2 · Deliverables — 5 NEW files, all uniquely named

| File | State |
|---|---|
| `knowledge/gen_itinerary_status.py` | **NEW** — the generator, 959 lines incl. a 5-arm selftest |
| `reviews/ITINERARY-STATUS-2026-08-19-v1.html` | **NEW** — Dave's surface, 86,504 B, 6 sections |
| `reviews/ITINERARY-STATUS-2026-08-19-v1.json` | **NEW** — machine-readable sidecar, 166,456 B, 124 rows |
| `reviews/ITINERARY-STATUS-2026-08-19-v1-1180.png` | **NEW** — render proof, desktop |
| `reviews/ITINERARY-STATUS-2026-08-19-v1-480.png` | **NEW** — render proof, mobile |
| `notes/_receipts/2026-08-19-203-wave3b-laneH-itinerary-status.md` | **NEW** — this receipt |

## 3 · How it derives — the ladder, and why every rung is declared

**Four ROUTE signals per resolved slug**, each an independent probe printed in the output:
`knowledge/snippets/<Name>.reference.html` · `knowledge/components/<slug>.meta.json` ·
`showroom/<slug>.html` · count of `.cn-<slug>` rules in `knowledge/canon/canon.css`.

**The radius ratchet (`MIGRATED_SNIPPETS`) is deliberately NOT in the ladder.** My first cut put it
in and produced **21 "OVERSTATED" rows** — components the itinerary calls Gated that are simply not
yet radius-migrated. That is a migration state, not a gating state, and folding it in would have made
the instrument lie in a new direction [[gate-glob-scope-rule]]. It is reported as a named ADVISORY
(28 snippets). After the fix, OVERSTATED fell 21 → **3**, and all three are honest.

**Resolution ladder — four rungs, `basis` recorded per row:**
1. `map` — `ROW_MAP`, the alternate-slug map. **Every entry carries a `why` with its probe.** 26 entries.
2. `mechanical` — slugified row name that HITS the store.
3. `notes` — a known slug named verbatim in the itinerary's own Notes cell (`"dropdown, gated."`).
4. `absent` — nothing hits, and the fuzzy scan finds nothing plausible.

⚠ **Rung 4's fuzzy scan NEVER decides.** If it finds a plausible alias it raises **UNRESOLVED** and
the run exits 1. That refusal is the whole point.

**Ordering defect I hit and fixed, worth the conductor knowing:** I originally ran `notes` before
`mechanical`. Row 5 (Icon button) has a Notes cell mentioning `button`, so it resolved to row 1's
artefact and `icon-button` fell out as an ORPHAN. A prose MENTION is not a binding
[[unmatched-grep-is-not-an-absence]] — matched is not presence either. Mechanical now outranks notes.

## 4 · Driven on real data — and it caught a live one

The brief's acceptance bar is that an instrument is only real once it has run on real data and caught
the known failures. It did better than that: **it caught an unknown one, live.**

Mid-lane, `python3 knowledge/gen_itinerary_status.py` exited **1** with:

> `UNRESOLVED row 37 'Anchor / scrollspy' — row name did not resolve, but the store holds plausible
> aliases anchor-nav(0.50). A slug mismatch is indistinguishable from an absence — add a ROW_MAP entry
> with its evidence, or confirm the gap. NOT GUESSING.`

Lane I had landed `Anchor-nav.reference.html` **between two runs of my generator**. A naive derivation
would have printed "Gap" for row 37 and re-created the exact #203 defect on a component that had
existed for ninety seconds. Same for `Sidebar-nav`, `Combobox`, `Multi-select`, `Command-palette`,
`Kpi-tile`, `Tags-input`, `Timeline` — all appeared under my feet during the lane.

**Selftest, 5 arms, all green** (`python3 knowledge/gen_itinerary_status.py --selftest` → rc 0):
- **arm 1, pass**: rows 13/17/19/52/63/89 — wave-3a's four false absences plus row 63 — must all measure GATED/BUILT.
- **arm 2, fail**: row 86 must measure ASSET-ONLY, and rows 6/7/25/26/61/93 must measure GAP. A derivation that cannot report a gap is always-true and worthless. ⚠ My first fixture set used rows 21/22/35 — **wrong**, because Lanes I/J/K were building them in this same tree. The test moved under me. Fixtures are now chosen only from rows no #203 lane owns.
- **arm 3, mutation on the STORE**: hide `Amount-input` from the index and drop its map entry — row 17 must go UNRESOLVED.
- **arm 4, mutation on the CLAUSE** [[mutation-tests-the-clause-not-the-feature]]: remove row 17's map entry while the artefact stays ON DISK. If the derivation reports GAP, that is **the #203 defect reproduced**, and the arm fails. It reports UNRESOLVED.
- **arm 5, fail-loud, DRIVEN**: builds three real malformed `.xlsx` fixtures (non-integer `#`, blank Component, wrong header) and runs `read_itinerary` on each, asserting the named `SystemExit`. An unrun gate cannot fail [[instrument-without-a-consumer]] — so this arm actually crosses the fence.

**Render proof, SEEN** (not claimed): `_RUNBOOK-render-verify.md` recipe, `goto("file://…")`, never
`set_content`. Pothole hit and cleared per the runbook: `libXdamage.so.1` missing →
`LD_LIBRARY_PATH=/var/tmp/chromelibs/root/usr/lib/aarch64-linux-gnu` (foreign-session libs, runbook
line 44). Measured at 1180 and 480: `documentElement.scrollWidth > clientWidth` was **TRUE at 480**
(a 9-column table pushing the page sideways) — fixed with a `≤720px` scroll rule, re-measured **False**
at both widths. 203 table rows, 24 gap blocks, title correct. I looked at the 1180 PNG.

**Parse gate, first** [[no-gate-parses-the-artefact]]: the HTML is parsed in the consumer's grammar
(`html.parser`) — 0 unclosed tags, 0 mismatches. The JSON is re-read and asserted: 124 rows, every
row carries probes or a declared class reason, every TRUE-gap row carries its probes.

## 5 · The TRUE-gap list — 23 Layer-1 rows, probe-backed

*(Next wave's brief input. Verdicts as measured at close of this lane; the live-tree caveat below is
part of the finding, not a hedge. Full probes per row are in §2 of the HTML and in the JSON.)*

**P1 — 1 row.** `86` Brand mark / logo → **ASSET-ONLY**. 12 official SVGs in `knowledge/assets/logos/`,
no component. *This is the only P1 row still open, and it is a wrapping job, not a design job.*

**P2 — 8 rows.** `75` Popconfirm · `81` Footer · `82` Grid / stack utilities · `87` Image / media block
(related: `cards` "Media card"; `hero` `textOverMedia`) · `91` Transaction / ledger row (⚠ the store
records its own gap: `amount-display.meta.json` says *"Transaction / ledger row (gap)"*; related:
`list-items` covers "Account, Badge, Item, Review, Review Detail, **Transaction**") · `92` Statement /
document row (related: `list-items`) · `93` Payment-card visual · `94` Coverage / runway bar
(related: `chart-bullet`, "a measure bar against a comparative target marker").

**P3 — 14 rows.** `6` Split button · `7` FAB · `24` Range slider · `25` Rating · `26` Cascader /
tree-select · `27` Transfer (dual list) · `38` Back-to-top · `58` Tree · `59` Calendar (the itinerary's
OWN note says "distinct from date picker", so Date-picker does not satisfy it) · `60` Carousel ·
`61` QR code · `83` Splitter / resizable · `95` Standing-order row · `96` Limits meter (related:
`chart-bullet`).

**Layer 2 (rows 97–124) — ONE structural gap, not 28.** No shell/template/lock-up artefact class
exists in the store at all (`find . -maxdepth 3 -iname '*shell*'` → nothing in-repo;
`-iname '*template*'` → one unrelated `review-skills/review-dossier/dossier-template.html`). Absence
of a Layer-1 snippet carries no information about them [[measure-dont-convert-units]].

⚠ **Rows 21/22/23/35/36/37/55/56 are NOT on this list** — they were GAP at lane open and were built
by Lanes I/J/K while I ran. They read PARTIAL/BUILT because their showroom pages and canon `.cn-`
scopes are GENERATED surfaces that Lane G has not regenerated yet. **Re-run this generator after
Lane G's pass before briefing anything off it.**

## 6 · Decisions needed — Dave's, all PROPOSED #203

1. **Does the derived surface replace the spreadsheet's `Status` column, or sit beside it?** I did not
   touch the frozen files (ADR-0017), so today there are two answers on disk. PROPOSED: the derived
   page is the live answer and the .xlsx is history. **Dave's.**
2. **Should `gen_itinerary_status.py --check` be wired into `_build_all.py`?** ⛔ Not wired by me —
   `_build_all.py` is out of fence, and an instrument without a consumer cannot fail
   [[instrument-without-a-consumer]], so this is a real open cost, not a formality. Note it will fail
   legitimately every time a component lands until the generator pass runs; that is the surface
   working, but it is a build-gate design question. **Conductor prices, Dave rules.**
3. **The GATED ladder's definition.** I ruled nothing: I chose snippet+meta+showroom+canon and made
   the radius ratchet advisory, because the alternative produced 21 false OVERSTATED rows. If "gated"
   in this repo means something narrower (e.g. a `_REVIEW-SIGNOFF.md` entry), the ladder should read
   that instead — one constant to change. **Dave's, and it moves 20+ rows.**
4. **Row 86 is a wrapping job.** Twelve official SVGs already exist. PROPOSED: next wave builds
   `Brand-mark.reference.html` from `knowledge/assets/logos/` rather than treating it as a design gap.
5. **Rows 91/92 vs List-items.** The store contradicts itself: `list-items.meta.json` claims a
   Transaction row variant while `amount-display.meta.json` names "Transaction / ledger row (gap)".
   Surfaced, not resolved — component promotion is on the DO-NOT-RULE list.
6. **The 28-snippet radius-ratchet advisory** is a real backlog nobody owns. Surfaced, not touched.

## 7 · Residuals, declared

- ⚠ **`notes/_receipts/_tmp203h/` — a stray directory I created and could NOT remove.** I copied the
  render PNGs there to view them, then found `mv` and `rm` both blocked (`Operation not permitted`;
  no delete grant, and a sub should not take one). The PNGs now also live at their proper
  `reviews/ITINERARY-STATUS-…png` names. **The conductor should delete `notes/_receipts/_tmp203h/`.**
  My mistake, undone as far as the fence allows, declared rather than left silent.
- **No HEAD sha in this receipt** — the lane binding forbade git. Declared, not skipped.
- **`_memento_search.py` not run first-hand** (see §1). Borrowed evidence, marked as borrowed.
- **Gates left to the conductor, by name:** `_validate_snippets.py` (I created no snippet),
  `_validate_a11y.py`, `_validate_state_contrast`, `_validate_type_composites.py` (its population is
  `knowledge/snippets/*.html` + `knowledge/_proforma/*.html`, line 245–246 — `reviews/*.html` is not
  scanned, so my HTML contributes **0** to the 1,101/1,097 debt by construction, not by luck),
  `_validate_radius.py`, and every `--check` generator (Lane G's surface this wave).
- **The output is a snapshot of a live tree.** `--check` was rc 0 at close and will go rc 1 the moment
  a sibling lane lands another file. That is correct behaviour for a generated surface; it is stated
  in §6 of the HTML and in `$caveat` in the JSON so no future reader mistakes it for rot.
- **Quality is out of scope.** GATED here means four artefacts exist — not that a component meets
  #203's rule set. Wave 3a's four-theme reviews found real defects in components this page calls
  GATED [[green-tests-cannot-see-scope]].

## 8 · Friction log

- The tree moved under me three times. Every re-run changed the counts. The generator's refusal to
  guess is what made that survivable rather than corrupting.
- The fuzzy rung flagged five rows as UNRESOLVED on first full run (6, 26, 27, 36, 82) — all name
  prefixes: "Split **button**", "Cascader / tree-**select**", "Transfer (dual **list**)",
  "**Grid** / stack utilities". Each got an explicit map entry stating the distinction. That is the
  designed remedy, and the reason the map has a `why` column at all.
- Chromium was already downloaded at `/var/tmp/pw-browsers-s197` from a foreign session; only the
  Python package and `LD_LIBRARY_PATH` were needed. ~2 min, not the 340 MB the runbook warns about.
