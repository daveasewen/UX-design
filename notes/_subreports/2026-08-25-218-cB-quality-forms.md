# `#218`-`cB` — quality wave, lane 1: the forms family (and the `{once:true}` class, repo-wide)

session: `#218` · 2026-08-25
window: `#218 crank — quality wave, lane 1`
sub index: `cB`
brief: `notes/_briefs/2026-08-25-218-quality-wave-forms-brief.md`
tokens: `UNMEASURED — a sub cannot read its own message.usage; no instrument in this seat exposes
it to the delegated process.` Bounded ESTIMATE (an estimate, NOT a measurement — see
`planning-estimate-is-not-a-measurement`): **~215,000–235,000** real, of which ~14 Chromium
drive calls and 21 verifier runs dominate. The conductor's own `subs <N> tokens (n=…)` figure
should come from the platform, never from this line.

## VERDICT

**DONE, all six regions of the brief.** The forms family was driven interactively — every
picker opened and closed by pointer, key and synthetic dismissal; every validation flow
entered wrong, corrected and re-entered; files staged and rejected; a real countdown run to
zero — and **eight live defects** came out of it, five of them in the forms family and three
from the repo-wide sweep. Two of the eight are severe: **the Date-range picker could not
complete a range from the keyboard at all**, and **three more components' dismiss controls
removed nothing** (β's R1 class, live in Tags, Notifications and Filter-toolbar-bar — 11→11,
11→11, 3→3 items). All eight are fixed at cause in the snippets, in the file's own idiom, with
Alert's wave-3 repair copied rather than re-invented. One verifier,
`knowledge/_render/verify_quality_forms_218.py`, drives all of it: **56 checks GREEN**, and
**16/16 break arms RED BY NAME with 0 controls red**. Affected gates re-run: snippet 0 fail ·
a11y 0 fail · behaviour PASS · token projection in sync · **type ratchet PASS, debt shrank
1097 → 1093**. `gen_showroom` deliberately NOT run (the conductor's serial). Nothing committed.

COUNTS: findings 11 · ruling-shaped 3 · UNPROVEN 4

## What was done

Region by region, in the brief's order.

**1 · The `{once:true}` guarded-listener class — REPO-WIDE grep first.**
`grep -rn "once: *true" knowledge/snippets/*.html` over all 137 snippets returned five files.
Adjudicated by driving each one, not by reading it:

| file | shape | verdict |
|---|---|---|
| `Alert.reference.html` | 5 hits, ALL inside β's ⛔ documentation notes | already repaired at wave-3 — **not an instance** |
| `Tags.reference.html:127` | guarded on `max-width`, one-shot | **LIVE DEFECT — fixed** |
| `Notifications.reference.html:221` | guarded on `max-height`, one-shot | **LIVE DEFECT — fixed** |
| `Filter-toolbar-bar.reference.html:384` | guarded on `max-width`, one-shot | **LIVE DEFECT — fixed** |
| `Toast.reference.html:217` | `()=>t.remove()` — **UNGUARDED** one-shot | **NOT the class** — see finding 4 |

**2 · Focus stranding on dismiss/disable (WCAG 2.4.3).** Five new instances found and fixed
(findings 2, 3, 5, 6, 7). Driven with a SYNTHETIC `PointerEvent('pointerdown')` where a real
click would have moved focus by itself — so every stranding reading below is the component's
behaviour, not the browser's.

**3 · `[hidden]` vs author-display (W3's F1 class).** No `[hidden]`-defeating rule found in the
eight forms files (`Secure-entry`'s `.se-wait` is the only `hidden` consumer and carries no
author `display`). The class DID surface in a different disguise — Time-picker's closed
listbox, finding 6 — and is fixed there.

**4 · aria-live coverage on validation errors.** Audited across all eight; every error message
container that needed one already carried `aria-live="polite"` (Date-picker `#f-date-msg`,
Time-picker `#f-time-msg`, Amount-input `#a1msg`, Date-range `#dr-announce`, Textarea
`#t1-live`, File-upload `#fu-announce`). **Nothing changed** — no file's documented pattern was
contradicted (the Toast lesson).

**5 · File-upload `aria-invalid` 0 vs siblings 2–7 — α's question.** ANSWERED BY DRIVING, and
it is a **real gap**, not correct-for-a-dropzone. Finding 3.

**6 · γ's two TYPE-002 rows.** Both enacted; ratchet shrank by exactly two. Finding 8.

**Files changed** (all under `/Users/daviewen/Documents/Claude/Projects/UX-design/`):

- `knowledge/snippets/Secure-entry.reference.html` — resend focus + dead countdown
- `knowledge/snippets/File-upload.reference.html` — remove-focus + `aria-invalid` wiring
- `knowledge/snippets/Date-picker.reference.html` — close focus rescue
- `knowledge/snippets/Date-range-picker.reference.html` — close focus rescue + keyboard range
- `knowledge/snippets/Time-picker.reference.html` — closed-listbox visibility + close focus
- `knowledge/snippets/Tags.reference.html` — dismiss repair + container `tabindex="-1"`
- `knowledge/snippets/Notifications.reference.html` — dismiss repair + `#nwrap tabindex="-1"`
- `knowledge/snippets/Filter-toolbar-bar.reference.html` — dismiss repair + `#ftb-chips` id/tabindex
- `knowledge/snippets/Data-grid.reference.html` — TYPE-002 composite
- `knowledge/snippets/Empty-state.reference.html` — TYPE-002 composite
- `knowledge/_render/verify_quality_forms_218.py` — NEW, the verifier
- `knowledge/_type_ratchet.json` — written **by the gate itself** in its ruled shrink-only mode
  (`--ratchet`), 1097 → 1093. Declared here because it is a tracked file this lane's gate run
  mutated; it is the gate's designed behaviour under `s119-D1`, not a hand edit.

⚠ **This report has NO store row and this lane did not add one** — store edits are fenced from
this brief. `knowledge/_gate_doc_rows.py` currently PASSES (`population 64 · unrowed 0`) only
because the file is untracked, i.e. through the #207 single-commit blindspot the doc-row gate
already documents. **The conductor must add the row when staging this report**, or the gate
will bite at the next commit that includes it. Flagged, not enacted.

Four of the 8 forms components were **audited and left alone**: `Form-layout`, `Amount-input`,
`Textarea` measured clean on every promise driven, and their behaviour is pinned by
`control/…` checks in the verifier so a future regression cannot pass silently.

## Findings

**1 · THE DISMISS REMOVED NOTHING, in three more files.** β's R1 class, live.
Probe: `verify_quality_forms_218.py` drives one dismiss per file and counts items.
Measured at HEAD, before any edit:

```
Tags.reference.html                11 -> 11 items (3 dismiss) | focus=BUTTON.x
   max-width events: ['run:...','end:transform', ... ,'end:max-width', ...]
Notifications.reference.html       11 -> 11 items (6 dismiss)
   max-height events: NONE   all=['run:margin-bottom','run:opacity',...,'end:opacity',...]
Filter-toolbar-bar.reference.html   3 -> 3  items (3 dismiss)
   max-width events: ['run:max-width', 'end:max-width']
```

Two distinct halves, and the three files split across them:

- **Tags and Filter-toolbar-bar isolate half (a) perfectly.** `end:max-width` DID arrive — but
  `end:transform` (Tags) and `end:border-bottom-width` (Filter-toolbar) arrived FIRST, failed
  the `propertyName` guard, did nothing, and `{once:true}` had already unsubscribed. The chip
  then stayed **CONNECTED at `max-width:0`** — an invisible ghost still in the tab order and
  the accessibility tree. That is a worse failure than "nothing happened", and the verifier
  pins it separately as `tags/no-ghost-chip-left-behind`.
- **Notifications carries both halves.** `transitionrun` never fired for `max-height` at all
  (the `max-height:0 !important` importance change — Alert's other defect), *and* `end:opacity`
  ate the one-shot. Either fault alone would have stopped the removal.

Fixed by transplanting Alert's repair verbatim in all three: inline→inline collapse, a NAMED
handler that unsubscribes only when its own property arrives, a `setTimeout(finish, 600)`
fallback, a `dataset.going` re-entry guard, and focus rescue.

**2 · Secure-entry — the resend button disabled itself while holding focus.**
Probe: focus `#resend`, programmatic `click()` (which moves no focus of its own), read
`document.activeElement`. `SE focus AFTER resend click: BODY#.` WCAG 2.4.3. Focus now moves to
the first `#otp .se-cell` — the thing the resend exists to serve — BEFORE the control goes away.

**3 · Secure-entry — the countdown never restarted; the resend was disabled FOREVER.**
`const tick = setInterval(...)` was created once and `clearInterval(tick)` at zero killed the
only interval the page ever made. The click handler's `left = 30` then counted down against a
dead timer: button permanently disabled, "in 30s" frozen at 30. Probe (compressed clock, 1000ms
→ 20ms, installed before the page script so the countdown reaches zero honestly):
`secure/resend-restarts-the-countdown` — HEAD frozen, repaired counter runs to 0 and the button
frees itself. **This defect is invisible to any probe that skips the wait** — see finding 10.

**4 · File-upload — removing a staged row stranded focus on BODY.**
`FU focus AFTER remove: BODY#.` with a sibling row still staged, and again
`FU focus after LAST remove: BODY#.`. Alert's idiom applied: next remaining `.fu-remove`, else
`#fu-browse`.

**5 · File-upload `aria-invalid` — α's question, answered: A REAL GAP.**
Driven, at HEAD, with a rejected 11MB file on screen:

```
FU rows after stage: 2 | FU error rows: 1
FU announce: huge.pdf could not be added: over 10MB.
FU aria-invalid after error: 0        <-- across the ENTIRE page
```

So the rejection was painted (`.is-error`), written (the message) and announced (`aria-live`),
and **nothing in the accessibility tree ever said the control was invalid**. It is not a
correct-for-a-dropzone exemption: the dropzone `.fu-zone` is decoration with no widget role,
but `#fu-input` **is** the labelled form control —
`<label class="t-cm-label" for="fu-input">Supporting documents</label>` — and that is exactly
where the other seven components in the family put `aria-invalid`. Wired via a single
`syncInvalid()` writer: set when any staged row is rejected, held while any rejection remains,
lifted when the last one goes. All three transitions are separately pinned.

**6 · Date-picker AND Date-range-picker — closing the panel stranded focus on BODY.**
`.dp-panel` / `.dr-panel` are `display:none` when closed, so an outside dismissal while a day
button held focus destroyed the focused element. Probe used a synthetic `pointerdown` so the
reading is the component's:
`DP after SYNTHETIC outside pointerdown -> focus: BODY#. | panel display: none`.
`close()` now rescues focus to the trigger **only when focus actually lived inside the panel**;
on a real outside click the browser's own focus change lands after this handler and wins, which
is the desired behaviour and is why the fix is not a focus thief.

**7 · Date-range-picker — THE RANGE WAS UNPICKABLE FROM THE KEYBOARD.** The most serious
finding in the lane. `pick()`'s start-date branch calls `render()`, which rebuilds the grid with
`gridEl.innerHTML = ''` — destroying the very button the user just pressed Enter on. Measured:

```
DR pick start -> from: 25/08/2026  announce: Start of range 25 August 2026. Choose an end...
DR pick end   -> to: ''            | focus: BODY#.
```

`document.activeElement` fell to BODY; the grid's `keydown` handler bails unless the active
element is a `.dr-day`, so every subsequent arrow and Enter was ignored and `#f-to` stayed
EMPTY. And because the start pick deliberately leaves the panel OPEN, the blur validator on
`#f-to` is suppressed too — so there was no route to a range by *any* keyboard path. The sibling
Date-picker does not have this bug: every `render()` in its arrow handlers is already followed
by `focusGrid()`. Fixed by doing the same (`focusDay = date.getDate(); render(); focusGrid();`).

**8 · Time-picker — the CLOSED listbox stayed fully in the accessibility tree.**
The closed menu was `opacity:0; pointer-events:none` only — no `visibility`, no `display`:

```
TP closed menu options still in tree: 48 | visibility: visible | display: block
TP closed menu hit-testable: 248   (px tall)
TP after SYNTHETIC close -> focus: LI.tp-opt
```

48 `role="option"` children exposed to assistive tech while `#tp-open` reported
`aria-expanded="false"` — the two statements contradict each other — and focus could be left
sitting on an option inside an invisible listbox. Same species as the `[hidden]`-vs-author-
display class. Fixed with `visibility:hidden` on the closed state plus a `visibility 0s linear
var(--tp-fade)` delay so the fade-out still plays; `--tp-fade` is **declared on the rule
itself** (not a dangling var — the silent-black lesson) and is zeroed under
`prefers-reduced-motion` because the blanket rule kills *duration*, not *delay*. Re-driven: at
90ms after close `opacity 0.224 | visibility visible`, settling to `opacity 0 | visibility
hidden`. The `.tp-menu.is-static` gallery specimen is asserted to stay visible.

**9 · γ's two TYPE-002 rows — enacted, ratchet SHRANK 1095 → 1093.**
(The gate's declared baseline was 1097 and HEAD already measured 1095, so `--ratchet` absorbed
a 2-point shrink that predates this lane as well as the 2 points this lane earned. Ratchet file
now reads `"shrunk": "1097 -> 1093 on 2026-08-25"`. **2 of the 4 points are this lane's.**)

- **Data-grid** `.dgseg button[aria-pressed="true"]{font-weight:500}`. The fix required removing
  `font:inherit` from `.dgseg button` first: `font:inherit` is EXEMPT from the gate but at
  specificity (0,1,1) it out-specifies any composite class (0,1,0), so a composite added
  without removing it would have been **inert decoration in the markup and absent from the
  rendering** — the exact Skeleton-loader trap from wave-3. States now name their own ramp step
  (`.t-cm-ctl-16` at rest, `.t-cm-button` when pressed), toggled by the handler that already
  writes `aria-pressed`, so state has one writer. **Zero visual delta measured**: pressed box
  55×28 before and after, unpressed 85×28 before and after.
- **Empty-state** `.empty a{font-weight:500}` → `class="t-cm-button"` on the anchor.
  **A 5px visual delta, measured and SEEN**: `16px/normal w500 h=21` → `16px/16px w500 h=16`,
  i.e. the link's box tightens onto the 16px slot and the card is 5px shorter. Both crops are
  in the evidence directory and were read; the link itself renders identically. See
  ruling-shaped question 1 — the composite named "button" is the honest ramp match for a
  16/500 *link*, and that is a canon gap, not a decision I took.

**10 · A LANE-LEVEL LESSON: my first verifier cut mis-sorted a "control" as feature-independent
THREE times, and each one was caught only by the break arm.** `control/upload-invalid-survives-
unrelated-remove`, `control/daterange-announces-the-range` and `control/datagrid-composite-
follows-the-press` all depended on the repair being present, so when their mutant ran they went
red as *controls* and the harness correctly reported **"ARM PROVED NOTHING"** rather than a
false pass. All three are now feature assertions in the must-redden lists, each replaced by a
genuinely repair-independent control. **The rule this yields: a control must be true in BOTH
arms by construction, so the test is "would this still hold with the repair deleted?" — asking
"is this about loading?" is not enough.** The three ⚠ notes are inscribed in the verifier beside
the checks they explain. Related: the `se-countdown-dead` arm's FIRST cut came back green
because the harness forced `#resend.disabled = false` to skip the 30s wait — which leaves the
original interval alive, so the mutant kept counting. The harness was wrong, not the check; it
now compresses the clock and lets the countdown reach zero, which is the only state in which
finding 3's defect exists. *(`mutation-tests-the-clause-not-the-feature`, twice in one lane.)*

**11 · A PRE-EXISTING gate refusal, declared, NOT touched.**
`python3 knowledge/canon/gen_canon_components.py` refuses:
`HARVEST NOT CSS — literal '<' outside comments in harvested <style> of Chart-bar.reference.html`
(ds-039). `Chart-bar.reference.html` is not in this lane's changed set and is not modified in
the working tree at all (`git status --short | grep -c Chart-bar` → `0`), so the refusal
predates this lane and blocks the canon-components regeneration step for everyone, not for
these edits. Flagged for the conductor; deliberately not fixed (out of fence, and it is the
known ds-039 class).

## RULING-SHAPED QUESTIONS

1. **Canon has no 16px/500 *link* composite, so `.empty a` now borrows `.t-cm-button`.**
   `.t-cm-link` is the 16/400 step and would have silently LIGHTENED a deliberate 500-weight
   link. Canon's existing home for a 16/500 anchor is the `.t-cm-button` group, whose bind list
   already contains `nav.main a` and `.hero .cta` — so the choice is precedented and measured
   identical (16px/w500). But a text link wearing a class called "button" is a smell, and the
   same shape is waiting in `Notifications.reference.html:83` (`.note a{font-weight:500}`) and
   almost certainly elsewhere.
   *(a)* leave `.t-cm-button` on link-shaped anchors and treat the name as historical;
   *(b)* add a `.t-cm-link` emphasis step (e.g. `.t-cm-link.em` at 500, mirroring the editorial
   tier's existing `.t-ed-body .em` idiom) and repoint;
   *(c)* rename the 16/500 composite to something role-neutral.
   **Recommend (b)** — it uses an idiom canon already has, costs one line in `type.css`, and
   unblocks the remaining link-weight rows in one sweep. **Canon edits are fenced from this
   lane, so nothing was changed; this is a `_DS-IMPROVEMENTS.md` row proposal, below.**

2. **The Empty-state card is 5px shorter (link box 21px → 16px).** This is the Component tier
   doing what it is for — snapping single-line text onto the slot — not a mistake, and Data-grid
   showed zero delta under the same change. But it is a visible change to a page Dave has seen.
   *(a)* accept the tightening as the canon's own consequence wherever a `.t-cm-*` lands on a
   `display:block` element; *(b)* keep the pixels and take the TYPE-002 violation as declared
   debt instead. **Recommend (a)**, with the before/after crops in the evidence directory for
   his eye. *(Per `feedback-mock-the-readings-before-building`: both readings are rendered and
   filed rather than argued.)*

3. **`knowledge/_type_ratchet.json` was written by the gate during this lane** (`--ratchet`,
   1097 → 1093), and 2 of those 4 points were already on disk before this lane started. That is
   the gate's ruled shrink-only behaviour under `s119-D1`, so it is not a fence breach — but it
   means this lane's commit will carry a ratchet movement that is only half its own.
   *(a)* commit it as-is with this report cited for the split; *(b)* revert the file and let
   whichever lane owns the other 2 points ratchet it. **Recommend (a)** — a ratchet that only
   shrinks loses nothing by absorbing an earlier shrink, and (b) risks the number drifting back
   above a real measurement. Conductor's call at reconcile.

## PROPOSED `_DS-IMPROVEMENTS.md` rows (NOT written — proposals only)

1. **A static gate for the `{once:true}` guarded-listener class** (the brief asked for the
   shape, not the build). Cheapest form that would have caught all four instances including
   Alert's: a regex pass over `knowledge/snippets/*.html` for
   `addEventListener\(\s*['"]transition(end|cancel)['"]` whose handler body contains a
   `propertyName`/`ev.target` comparison **and** whose options object contains `once`.
   FAIL on the conjunction. Two properties make it cheap and honest: (i) it needs no browser —
   it is a source-shape gate, so it runs in CI where the render env does not; (ii) it has a
   natural red arm (re-introduce any of the four repaired listeners). Two known false-positive
   shapes to exempt by name: a genuinely single-property transition, and the ⛔ documentation
   notes in `Alert`/`Tags`/`Notifications`/`Filter-toolbar-bar` that QUOTE the broken form —
   which is why the gate must parse the `addEventListener(` call, not grep the file for
   `once:true` (a `grep -c` on this repo returns 12 hits of which **0** are live defects after
   this lane; a naive gate would be all noise). ⚠ Not built: gate machinery is another sub's
   region this window.
2. **A `.t-cm-link` emphasis step at weight 500** — see ruling-shaped question 1. Known
   consumers waiting: `Empty-state .empty a`, `Notifications .note a`.
3. **`.dgseg` is demo-chrome by intent but not by selector name.** `CHROME_SEL` in
   `_validate_type_composites.py` matches `\.demo|\bdemo-|harness|…`; `.dgseg` (whose own JS
   comments call it "demo state switcher") does not match, so a demo control is being graded as
   a shipping component. Either rename the selector or widen `CHROME_SEL` — a decision about
   the GATE, so it is not this lane's and is not enacted.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN: the fixes were driven in ONE theme and ONE mode** (the files' default,
  `data-theme="light"`, at 1180×900, plus a 760px resize inside the picker checks). Every
  defect found and fixed is behavioural or semantic (focus, listeners, `aria-invalid`,
  `visibility`) and none of it is theme-conditional by construction — but that is an argument,
  not a measurement. Price to prove: 4 themes × 2 modes × 11 files through the existing verifier
  ≈ one render matrix, ~12–18k tokens.
- **UNPROVEN: no showroom re-render was seen.** The brief reserves `gen_showroom` for the
  conductor's serial and it was NOT run, so the showroom pages for all 10 changed snippets are
  STALE against the snippets right now. Price: the conductor's existing serial.
- **UNPROVEN: the `{once:true}` sweep covered snippets only** (`knowledge/snippets/*.html`, 137
  files, which is where the brief pointed). `knowledge/_proforma/`, `showroom/`, `dashboard/`
  and `projects/` were NOT swept for the same shape. Price to extend: one grep + one drive per
  hit, ~3–6k tokens.
- **UNPROVEN: `Toast.reference.html:217` is safe.** Its one-shot listener is UNGUARDED
  (`()=>t.remove()`), so it does not meet the class definition and it *does* remove — but it
  removes on the FIRST property to finish, which could be premature, and it has no fallback
  timer. β audited Toast at wave-3 and left it, and contradicting a file's documented canon is
  Dave's call (the Toast lesson), so it was **left untouched and is named here rather than
  fixed**. Price to adjudicate: one drive at 3 motion settings, ~2k tokens.
- **CLAIMED: the a11y and behaviour gate figures are this run's own tails**, re-read from the
  live command output above, not from a banner. The `1097` ratchet baseline is CLAIMED from
  `_type_ratchet.json` as it stood at lane open; the `1095` and `1093` figures are MEASURED
  summary lines from `_validate_type_composites.py` in this seat.

## Evidence

`notes/_subreports/assets/2026-08-25-218-cB-quality-forms/`

- `verify-green.txt` — the full 56-check green tail of `verify_quality_forms_218.py` on the real
  snippets. Proves every repair holds against a live drive.
- `verify-break-arms.txt` — all 16 break arms, each `✓ RED BY NAME`, `0` occurrences of `⛔`.
  Proves the verifier can fail, per mutant, by the check that pins that mutant's defect.
- `218-cB-emptystate-link-head.png` / `218-cB-emptystate-link-fixed.png` — the only visual delta
  in the lane, before and after, both READ (not merely produced): the link renders identically,
  the card is 5px shorter. Feeds ruling-shaped question 2.

Environment for replay (session-suffixed, `-s218qf`):

```bash
export TMPDIR=/var/tmp PYTHONPATH=/var/tmp/pylibs \
       PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-215 \
       FONTCONFIG_FILE=/var/tmp/fonts-s218qf.conf \
       BM_MUTANT_DIR=/var/tmp/218qf-mutants \
       LD_LIBRARY_PATH=/var/tmp/chromelibs/root/usr/lib/aarch64-linux-gnu:/var/tmp/chromelibs-s213e2/root/usr/lib/aarch64-linux-gnu
python3 knowledge/_render/verify_quality_forms_218.py            # 56 green
python3 knowledge/_render/verify_quality_forms_218.py --break all # 16 arms, RED by name
```

⚠ `--break all` exceeds the ~178s call wall in one go — drive it in batches of three mutants,
which is how this lane ran it.

REPLAY-THESE: `knowledge/_render/verify_quality_forms_218.py` docstring + its three ⚠ control-classification notes (~4,500 tk) · this report's finding 7, the Date-range keyboard defect (~700 tk) · finding 10, the control-vs-feature lesson (~600 tk) · the three RULING-SHAPED QUESTIONS (~1,100 tk)
