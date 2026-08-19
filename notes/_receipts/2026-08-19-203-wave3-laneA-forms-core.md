# Receipt — #203 Wave 3, Lane A · forms core (Form layout + validation · Textarea · Alert)

*Worker receipt per the parallel-conductor checklist, against `_BRIEF-wave3-foundations-2026-08-19-v1.md`.*
*⛔ Nothing here is a ruling. No commit, no push. No git checkout/restore/stash of any kind was run.*
*Author's context gauge at authoring: `_checkin.py` — FILL **108,667 real**, boot 56,488, peak 108,667
over 18 turns, room to advisory stop line (150,929) **42,262**. ⚠ Declared: `_checkin.py` reads the live
transcript and I cannot prove from inside the sub that the transcript it found is mine rather than the
conductor's; treat the figure as ORDER-OF-MAGNITUDE for this sub, not as an audited sub reading.*

---

## ⛔ HEADLINE — THE BRIEF'S PREMISE IS FALSE, AND NOT ONLY FOR THIS LANE

**All three Lane A components already exist, gated, four-theme-cascaded, and ruled.** They were not
built here because they did not need building, and the fence forbids overwriting them.

Widening the probe because the failure looked structural: **19 of the 20 P1 "Gap" rows in the
itinerary already have gated reference snippets.** Only row 86, *Brand mark / logo*, is genuinely
absent. The itinerary is dated **2026-07-14**; the forms and feedback components landed **2026-07-22**
in "Phase-2 wave 1: 14 components land" (`60e4dc1`). The document has simply never been re-statused.

This is not a Lane A problem. Every lane in Wave 3 was briefed to build components that already exist.

## Step 0 — the premise, verified first-hand before anything else

| Claim inherited from the brief | Verified? | Evidence (probe named) |
|---|---|---|
| HEAD is unstated; establish it | HEAD = **`ec2336d`** (#202 wrap) | `git log --oneline -1` |
| The itinerary carries 20 P1 gaps | ✅ TRUE as a *row count* | parsed `xl/worksheets/sheet1.xml` from the .xlsx; 20 rows with `Status=Gap, Priority=P1` |
| My three components are absent | **FALSE — all three present** | `ls knowledge/snippets/` → `Alert.reference.html`, `Textarea.reference.html`, `Form-layout.reference.html`; metas present too |
| …and they are merely stubs | **FALSE — fully gated** | each carries a `#token-manifest`; each has a `.cn-<slug>` scope in `canon/canon.css`; each has **3 override blocks in each of legacy/console/supercharge** (grep on `[data-apollo-theme="<t>"] .cn-<c>`) |
| The other 17 P1 gaps are real | **FALSE for 16 of them** | mapped each Gap row to its expected snippet filename: 19 EXISTS / 1 ABSENT (`Brand mark / logo`) |
| "Alert and Form interlock — use Alert in Form" | **FALSE** | `grep -cE 'class="alert\|\.alert' Form-layout.reference.html` → **0**. Form-layout implements its own `.fl-summary` + `.fl-msg`. See Decisions needed #1. |
| Type-composite debt is 1,101 | **STALE — it is 1,097** | `_validate_type_composites.py --ratchet` → `declared debt holds at 1097`. A carried COUNT is the same defect class as a carried claim [[premise-ages-faster-than-rule]] #194. |

**Searched twice before calling any of this new** [[unrun-search-indistinguishable-from-absent-record]]:
`_memento_search.py "itinerary stale P1 gaps already built"` → no record of the staleness (returns the
charts lane + three GOOD-MORNING sections, none on point); and a direct regex over `_rulings.json` for
`itinerar|P1 gap|foundations wave` → **1 hit, `s174-D1`**, which is about the scaffold brief's six
gates, not about itinerary status. No prior record. The finding is genuinely new.

## What I built instead — and why it is the right thing inside the fence

The three components had **never been seen outside Apollo Mono**. Progress-bar got a four-theme review
surface at #174; these did not. The brief's own MAY-create list includes exactly this file, so the
honest Lane A deliverable was to put the existing, approved artefacts in front of Dave across the full
spread for the first time.

| File | State |
|---|---|
| `reviews/REVIEW-203-alert-four-themes-v1.html` | NEW — 8 panes, 4 themes x light/dark, live |
| `reviews/REVIEW-203-textarea-four-themes-v1.html` | NEW — 8 panes, live counter per pane |
| `reviews/REVIEW-203-form-layout-four-themes-v1.html` | NEW — 8 panes, live validation per pane |
| `notes/_receipts/2026-08-19-203-wave3-laneA-forms-core.md` | NEW — this receipt |

**Nothing else in the repo was created, edited, deleted or regenerated.** No snippet, no meta, no
token, no generator output, no shared file.

Method, per [[specimen-starts-from-reference]]: each pane is the snippet's own `<body>` inner HTML
**byte-for-byte**, with one purely mechanical transform — a per-pane id suffix. Eight copies on one
page would otherwise collide on `id=`, silently breaking every `label/for` and `aria-describedby` for
AT. The `<symbol>` sprite is emitted once and its ids are excluded from the rename set. Colour and
type come from the generated `canon.css` via `[data-apollo-theme] x [data-theme]` — the #174 grammar,
not a re-specification. Generator lived at `/var/tmp/s203/mkreview.py`, outside the repo; it is not an
instrument the repo carries.

⚠ **A defect I introduced and then caught.** The first build copied each snippet's behaviour script
once per pane. Alert's script is **class**-scoped (`querySelectorAll('.alert .x')`), so eight copies
bound eight handlers to every dismiss button. Fixed by detecting whether a script names any suffixed
id: id-scoped scripts are emitted per pane (Textarea, Form-layout), class-scoped ones once (Alert).
The build now prints which mode it chose, so the choice is visible rather than assumed.

## Gates — every rc measured directly, never after a pipe

*(The #174 receipt's warning applies: `rc=$?` after a pipe reads `tail`'s status. Captured directly.)*

| Gate | Baseline (HEAD `ec2336d`, before I wrote anything) | After | Verdict |
|---|---|---|---|
| `_validate_snippets.py` | **rc=1** — 76 snippets, **18 failures** | rc=1, 76, 18 failures | ⚠ **RED AT HEAD, NOT MINE** — unchanged, see below |
| `_validate_a11y.py` | rc=0 — 76, 0 failures, 179 warnings | rc=0, identical | ✅ unchanged |
| `_validate_type_composites.py --ratchet` | rc=0 — debt **1097** | rc=0 — debt **1097 (0 new)** | ✅ ratchet held |
| `_validate_type_composites.py` on my 3 NEW files | — | **rc=0, PASS on all three** | ✅ my files contribute **0** |
| `gen_showroom.py --check` (read-only) | — | rc=0, "76 page(s) + index in sync" | ✅ |

**Gates left to the conductor, by name** (declared gap passes, silent gap fails):
`_validate_state_contrast.py` (exceeds the sandbox call cap over 76 snippets, and it *writes*
`_STATE-CONTRAST-AUDIT.md`, which is a shared output — deliberately not run), `_validate_radius.py`,
`_validate_coverage.py`, `_validate_icons.py`, `_validate_partials.py`, `_build_all.py`, and all
`gen_*` regenerations. My three files are NEW `reviews/` pages, so I expect several of these to report
them as absent from generated outputs — that is the fence working, not a defect.

### ⛔ The snippet gate is RED at HEAD, and it is a wave-wide blocker

18 failures, all one cause: `--pri-hover` is `#626262` light / `#B7B7B7` dark in the snippet, but the
store says `#636363` / `#B2B2B2`. **Nine snippets carry the stale pair** — Action-bar, Button,
Confirmation, Drawer, Empty-state, **Form-layout**, Icon-button, Modals, Stepper. This is drift left
behind when `--pri-hover` was re-minted at #198/#199. Proved pre-existing on a true control: the
failures were read *before* this sub created any file, and `git status` showed no snippet modified.
Form-layout (Lane A) and Drawer (Lane D), Empty-state (Lane E) and Stepper (Lane F) are all inside
Wave 3 lanes, so this will surface in several lanes at once. **Not fixed here** — it edits nine
existing shared artefacts and belongs to one hand, the conductor's.

## ⚠ A fence residual I created and repaired

`_validate_snippets.py` **writes** `knowledge/_SNIPPET-AUDIT.md` (line 354) as a side effect. The
brief instructs running that gate, so the write happened before I knew to expect it — same trap #174
hit with `_STATE-CONTRAST-AUDIT.md`. **Repaired by re-writing the file from `git show HEAD:<path>`,
which is a re-edit, not a `checkout`** — the banned verb was not used. `git diff --stat` on that path
is now empty, twice verified (it was re-dirtied by the second gate run and restored again).

⬛ **Proposal for the conductor:** the brief tells six parallel lanes to run a gate that writes a
shared tracked file. Six lanes doing so concurrently is a clobber race. Either the brief should name
the write, or the gate should grow a `--no-write` flag. Filed as a `_DS-IMPROVEMENTS.md` candidate
below rather than fixed, since that file is fenced.

**A second instrument writes too, and this one I deliberately did NOT repair.**
`knowledge/_memento_search.py` — which §6 of the brief *requires* be run before framing any question as
open — appends to the tracked `knowledge/_graph-mark-observations.jsonl`. It grew by **72 lines** during
this lane, of which **16 are mine** (query `itinerary stale P1 gaps already built`). The other 56 belong
to lanes running concurrently, including 21 on `date picker calendar grid` (Lane B), 18 on
`C1 strands chart expansion wave 3`, and — corroborating this receipt from another desk entirely —
**15 on `itinerary status stale components already built`**, i.e. at least one other lane reached the
same premise finding independently.

Restoring that file from HEAD would have destroyed five other lanes' appends. **The right move for an
append-only log written by six concurrent lanes is to declare it and leave it**, which is the opposite
of the right move for `_SNIPPET-AUDIT.md`, which is rewritten wholesale. Two shared files, two opposite
remedies, and the difference is *append vs overwrite* — worth a line in the worker checklist, because
applying #174's restore reflex to this one would have been quietly destructive.

Final tree state under `knowledge/`: **2 modified files, neither of them mine to repair** —
`_REVIEW-SIGNOFF.md` (untouched by me; mtime 2026-08-18, predates this session) and
`_graph-mark-observations.jsonl` (shared append log, as above).

## Render proof — `goto("file://…")`, never `set_content()`

Chromium + Playwright per `_RUNBOOK-render-verify.md`. First launch died on
`libXdamage.so.1: cannot open shared object file` — **a crash is not a fail**; the runbook's own step 4
names the remedy (`LD_LIBRARY_PATH` at a `chromelibs` farm) and it worked first try with
`/var/tmp/chromelibs-s201`. Font farm was a `/var/tmp` symlink farm per the #138 stratum; **`ls -a` on
the repo TTF dir shows 0 `.uuid` strays** — the symlink farm did what it was built to do, and no render
artefact reached the tree.

**Font asserted with controls, not `fonts.check()`** — identical numbers on all three pages:

| probe | measured | reading |
|---|---|---|
| `HSBC_MtUnivers_Latin` | **347** | the real cut |
| `"Univers Next HSBC"` (type.css alias) | **347** | resolves |
| `"Univers Next for HSBC"` (snippet alias) | **347** | resolves |
| `DejaVu Sans` — control | 375 | genuinely different face |
| nonexistent face — control | 301 | default fallback |

Both aliases land on the target and on neither control. These are the same five numbers #174 recorded.

**Structural assertions, all three pages:** 8 panes each · **0 duplicate ids** (21 / 89 / 251 unique) ·
**0 console errors**.

**Driven, not merely rendered** [[mutation-tests-the-clause-not-the-feature]]. Submitting the empty
form in the **Legacy dark** pane only:

```
mono/light        invalid 1->1  msgs 2->2  summary False->False
legacy/dark       invalid 1->5  msgs 2->6  summary False->True     <- the only pane that moved
supercharge/dark  invalid 1->1  msgs 2->2  summary False->False
```
ISOLATION **PASS** — exactly the driven pane changed.

⚠ My first isolation check reported **FAIL**, and the checker was wrong, not the page: every pane
carries a static `aria-invalid` specimen in its states gallery, so `invalid > 0` was already true
everywhere at baseline. Re-asserted on the **delta** before/after. Recording this because a green that
could not fail, and a red that could not succeed, are the same defect seen from opposite sides.

**Measured geometry and colour across all 8 Alert panes** (a check no gate performs — the snippet gate
reads the Mono base only):

| theme/mode | shell radius | tint | ink | glyph | dismiss hit | visual |
|---|---|---|---|---|---|---|
| mono light / dark | 0 / 0 | #FDD9D4 / #60302A | #1A1A1A / #FFFFFF | #F6604C | **44x44** | 24x24 |
| legacy light / dark | 0 / 0 | #F9F2F3 / #260005 | #333333 / #FFFFFF | #A8000B | **44x44** | 24x24 |
| console light / dark | **20 / 20** | #EECDC9 / #60231C | #1A1A1A / #FFFFFF | #B92F1E | **44x44** | 24x24 |
| supercharge light / dark | 0 / 0 | #F1E0DC / #2C120D | #13110E / #F7F6F4 | #B92F1E | **44x44** | 24x24 |

- **44px min-hit-area holds in all eight panes**, enforced by the `::before` expander and now MEASURED
  rather than asserted — the brief notes no gate enforces it.
- **Square corners hold** everywhere except Console's 20px, which is the ruled `s199-D3` console radii
  enactment, not drift. *(I first read Supercharge as rounded by eye; the measurement corrected me.
  Recording it because the eye was wrong and the probe was right.)*
- **Two-red law consistent**: Mono's error glyph is `#F6604C` sitting on a tint, not on white, so it is
  the correct leg of `s151-D1`. Legacy/Console/Supercharge carry their own reds, which the law does not
  reach (MONO ONLY).
- **Mono error ink camp consistent**: message ink `#1A1A1A`, and the glyph's internal mark is `#1A1A1A`
  on the `#F6604C` shape — `s149-D1`, with `s194-D1`'s white-on-error nowhere present.

**Contrast of the DRIVEN error state, all four themes x light/dark** (24 legs, computed from real DOM
colours after driving every form):

| | mono L/D | legacy L/D | console L/D | supercharge L/D |
|---|---|---|---|---|
| summary link on summary bg | 13.30 / 10.75 | 11.45 / 19.36 | 11.78 / 11.97 | 14.75 / 16.21 |
| summary title on summary bg | 13.30 / 10.75 | 11.45 / 19.36 | 11.78 / 11.97 | 14.75 / 16.21 |
| inline message on page | 17.40 / 17.40 | 12.63 / 17.40 | 17.40 / 17.40 | 17.45 / 17.45 |

**Nothing below 4.5:1 anywhere.** The "error text stays ink, never red" decision is doing exactly the
work it was made to do, and it holds in the three themes no gate had ever checked it in.

## Decisions needed — Dave's, all PROPOSED #203, nothing resolved

1. **The inline-callout grammar exists twice.** Alert renders status messaging as a tinted shell with
   icon + title + dismiss. Form-layout renders its own, independently: `.fl-summary` for the
   form-level error box and `.fl-msg` per field, **sharing no markup and no CSS with Alert** (verified:
   zero `.alert` references in the Form-layout snippet). The brief assumed Form *uses* Alert; it does
   not. Whether the form error summary should become an Alert, or whether the two are legitimately
   different objects worth writing down as distinct, is a design call. Surfaced on both review pages.
2. **Textarea declares no hit-target rule at all.** Alert and Form-layout both carry explicit 44px
   rules; Textarea carries none. Today the requirement is met by geometry — a `rows="3"` textarea is
   far taller than 44px — but a future one-row variant would drop under the floor silently. A rule is
   worth having; adding one is a decision, not a fix.
3. **The itinerary needs re-statusing, and that is not a sub's call.** 19 of 20 P1 "Gap" rows are
   built. Someone must decide whether the itinerary is corrected, superseded, or retired — and what
   Wave 3's six lanes should do instead. Component promotion of any kind is on the DO-NOT-RULE list,
   so this receipt states the fact and stops.
4. **Type-composite debt in the three Lane A snippets: Alert 4, Textarea 7, Form-layout 9 = 20 of
   1,097.** The ratchet is shrink-only so these are safe to pay down, but each fix edits an existing
   shared artefact and belongs to one hand.

## Proposals for the conductor to merge

- **`_DS-IMPROVEMENTS.md`**: `_validate_snippets.py` writes `_SNIPPET-AUDIT.md` as a side effect of
  *reading*. Under a six-lane parallel brief that is a clobber race. Candidate: a `--no-write` flag,
  or split the audit emission into its own generator.
- **`_DS-IMPROVEMENTS.md`**: `--pri-hover` drift across 9 snippets (18 gate failures) since the
  #198/#199 re-mint. Single-cause, mechanical, and currently the reason the tree is red.
- **Brief template**: a lane brief that asserts "component X is absent" should carry the probe that
  established the absence and the date it was run. Every claim in §9 of this brief was eight days
  stale and no field required it to be re-derived.
- **Carried counts**: the brief's "1,101 debt" measures 1,097. Same class as #194's "standing 44".
- **No CATEGORIES entry is owed** — I added no component, so `gen_showroom.py`'s `CATEGORIES` is
  untouched and correctly so.

## Friction log

1. **The premise collapsed at step 0**, which is the step designed to catch exactly that — but only
   because I widened the probe from "are *my* three absent?" to "are *any* of the 20 absent?". The
   narrow probe would have returned a true answer and a false picture.
2. `libXdamage.so.1` blocked the first Chromium launch; the runbook's step 4 already had the remedy.
   Cost ~1 tool call because I opened the runbook instead of concluding "rendering is blocked".
3. `rc=$?` after a pipe reads `tail`'s status — the #174 warning is real and I hit it once, reading
   `rc=0` off three gates that were all `rc=1`. Re-measured directly.
4. `2>&1` into a JSON parser corrupts the JSON with Playwright's banner. Wrote results to files.
5. My own isolation assertion produced a false FAIL (see render proof). The artefact was fine.
6. Other lanes were live in the same sandbox throughout: `/var/tmp/pylibs-s203e` appeared, and
   `knowledge/_graph-mark-observations.jsonl` grew by 72 lines during my run. My first reading of that
   file attributed **all** 72 to other lanes — wrong: **16 are mine**, from the store search §6
   requires. I only caught it because I verified a "0 modifications" claim I had already written into
   this receipt, and it measured 2. **The claim was written before it was measured; that is the defect,
   and the measurement is what caught it** [[enactment-register-adr-0016]]. Both the count and the
   attribution are corrected above.

## Commit state

**Nothing committed. Nothing pushed. No git write command of any kind was run** — not `checkout`, not
`restore`, not `stash`, not `add`, not `commit`. `git show`, `git log`, `git status` and `git diff`
(all read-only) only. Four new files handed up, listed above.
