# #218 — the seven phantom surfaces (s218-D4), built · drawn · and one NOT built

Brief: `notes/_briefs/2026-08-25-218-phantom-surfaces-brief.md`. Dave ruled the CLASS at s218-D4
("build them"); **every DESIGN below is PROPOSED and carries that label in its own file header.**
Nothing here is a ruling, no ruling was inscribed, no token/canon/registry/store file was touched.

## The headline, before the detail

**Six surfaces exist that did not exist this morning. The seventh was a false phantom and the
honest deliverable there was NOT to build it** — Confirmation's "Replay button" is real and lives
where Dave put it in 2026-08-05. Details in surface 6; it is the one item on this page that needs
his eye before anything else.

## Premise check, first — the brief said to, and it paid

Every phantom was verified in its own file before a line was written. **Six of seven premises held
exactly.** The seventh did not:

| # | file | premise from the W3 receipt | verdict |
|---|---|---|---|
| 1 | Headers | "More options" opens nothing | ✅ held — one `<button aria-label="More options">`, no menu anywhere |
| 2 | Navigations | Search + Account inert | ✅ held — and the file's own script said so in prose ("NOT WIRED, deliberately") |
| 3 | Avatar-group | "+N" and the group target open nothing | ✅ held — two triggers, no surface |
| 4 | Standing-order row | "Manage" opens nothing | ✅ held — 8 manage controls (1 legitimately disabled), no surface |
| 5 | Kpi-tile | table CTA opens nothing, header forbids inventing the panel | ✅ held, prohibition quoted below |
| 6 | Confirmation | "the documented Replay button is missing from markup" | ⛔ **AGED — see surface 6** |
| 7 | Timeline | "Load older activity" has nothing to load | ✅ held — and its aria-current/progressbar prohibitions are real |

---

## 1 · Headers — "More options" → an APG menu button

**Built.** `aria-haspopup="menu"` + `aria-expanded` + `aria-controls` on the existing trigger; a
`role="menu"` panel of three `role="menuitem"` buttons. The panel's visual CSS is **Dropdown's
`.menu`/`.opt`/`.sep` shell copied via Card-header-lockup (#210)**, which had already made and
DECLARED the same ARIA deviation (a listbox's floating-panel skin worn by an actions panel) —
nothing was re-drawn. Keyboard: open on Enter/Space/ArrowDown (ArrowUp opens at the last item),
Arrow walk, Home/End, Escape closes and returns focus, Tab-out and outside-click dismiss.

**⬛ For Dave**
- **The three item labels are invented copy** for a Statements screen: "Download statements" ·
  "Filter by date" · (rule) · "Statement preferences". What a real product menu says is his.
- **One structural change, declared:** this file now links `canon/type.css` so the items carry a
  `.t-cm-label` composite instead of a raw `font:` (which would have GROWN the shrink-only 1,097
  TYPE-002 debt). type.css binds no bare selector this file uses — read, not assumed; nothing
  already drawn moved. Side effect: the file cleared a TYPE-001 violation, so the debt **shrank**.
- Inherited a11y warning, not new: the trigger is the header's existing 40×40 button, under the
  44 default. It was 40×40 before #218; it is not this lane's to resize.

## 2 · Navigations — Search → a disclosure, Account → a menu

**Built, by EXTENSION.** The W3 destination-selection script was left intact and two IIFEs were
added beside it; the "NOT WIRED, deliberately" note was replaced by a note saying who superseded it
and why. A regression check drives the W3 behaviour and would go red if the extension had eaten it.

- **Search** reveals a full-width bar beneath the masthead carrying **Search-field's UNDERLINE form,
  copied** (mag glyph, `input[type=search]`, and the clear × that exists only while the field holds
  a value). Focus lands in the field; Escape closes and returns focus to the trigger. Enter is
  stopped and declared — a submitted search has no destination in a reference artefact.
- **Account** is the same menu pattern as Headers: "Your profile" · "Settings" · (rule) · "Sign out".
- **⚠ The #218 W3 F1 lesson is applied, not re-learned:** the revealed bar carries an explicit
  `[hidden]{display:none}` rule, because an author `display:` beats the UA `[hidden]` sheet.

**⬛ For Dave**
- **Reveal vs replace.** The proposed reading opens a bar UNDER the masthead. The alternative is a
  field that replaces the nav row in place — cheaper to draw, worse to operate on a narrow masthead.
- **Item copy is invented**, and "Sign out" in a menu is a product question, not a component one.
- Inherited warning: the clear × is 24×24 — **Search-field's own** size, copied with the rest of it.

## 3 · Avatar-group — "+N" and the group target → the overflow list

**Built as a DISCLOSURE, not a menu** — the panel holds NAMES, which are content; `role="menu"`
would misdescribe what it is. The `+3` trigger lists exactly the three members the stack hid; the
group-as-one-target lists all six, because its own accessible name says "all 6". Opening one closes
the other; Escape closes and returns focus; focus deliberately STAYS on the trigger (there is
nothing focusable inside, and moving focus into static text strands a keyboard user).

**⬛ For Dave**
- **The names link nowhere, on purpose.** A row of "open profile" links would promise six further
  surfaces — re-opening the very class this ruling closes. If members should be reachable, that is a
  decision to make once, for the component.
- **Two triggers, two different truthful contents** (hidden-only vs whole-set). Whether the product
  wants both forms at all is his.
- Rendered console-dark and read: the panel overlaps the demo note beneath it, as any floating panel
  does. Not a defect; named so nobody re-reports it.

## 4 · Standing-order / mandate row — "Manage" → an inline action surface

**Built as the CHEAPER honest reading, and the expensive one is priced rather than built.**

- **What is drawn:** an INLINE DISCLOSURE inside the row carrying the three actions this file's own
  header already names at line 22 — Pause/Resume · Amend · Cancel mandate. Wired on all seven
  manageable rows (the cancelled row's control stays natively disabled).
- **Why not the floating menu** that Headers and Navigations take: `ul.mdlist` carries
  `overflow:hidden` (inherited from Document-row and flagged there), so a panel anchored inside a
  row is **clipped by the list shell**. The menu reading therefore needs `position:fixed` plus
  placement maths to escape its own container — Popover's machinery, inside a row. The inline
  reading needs none of it and reflows for free at 340px. **Structural, not stylistic.**
- **The demo enactments are declared, not disguised:** Pause/Resume moves the row's own status chip;
  **Cancel puts the row into the CANCELLED state this file already draws** (chip word + disabled
  control + `aria-disabled`), so the documented end state is reachable by hand rather than only
  described. A polite live region announces each change, and focus is RESCUED onto the payee link
  when Cancel disables the control that was holding it.

**⬛ For Dave**
- **Inline panel or floating menu?** Priced above. If he wants the menu, the honest cost is a
  fixed-position placement helper in this file (~25 lines) or a change to the list shell's overflow.
- **Cancel with no confirmation step.** A real product must confirm a destructive action first
  (Popconfirm / Modals). That step is deliberately NOT invented here, and whether a destructive
  action belongs in this surface at all is his call. This is the one place a reviewer might read the
  specimen as endorsing a pattern; it is declared in the file, not just here.
- **P10** was added to the file's own PROPOSED list so the question travels with the artefact.

## 5 · Kpi-tile — the table CTA: the panel is DRAWN, and nothing is wired

The file's own header forbids inventing the panel, verbatim: *"The PANEL it would open is NOT built:
s116-D2's table molecule is a composition-level artefact and inventing one here would be canon by
improvisation."* **That prohibition stands.** Per the brief, s218-D4 is enacted here as a DRAWING:

- a marked SPECIMEN beside the tile ("SPECIMEN — not wired, not a panel, not ruled"), the
  prohibition quoted on the page, and **Table.reference.html's passive markup and four cell seats
  copied** (caption · `th scope` · focusable `role="region"` · no sort);
- twelve rows — the series the sparkline already draws, consistent with the tile's own +£2,450.00
  and +12.4% vs February;
- **the CTA is still inert**: no `aria-controls`, no `aria-expanded`, and this file still contains
  **no behaviour script at all**. A harness CONTROL asserts that inertness in both arms, so if a
  later hand wires it, the instrument says so by name.

**⬛ For Dave — three questions the drawing exists to answer**
1. Does the panel belong to the TILE, or to a composition above it (s116-D2's table molecule)?
2. Does it open in place, in a Drawer, or in a Modal?
3. Does the CTA survive at all? s182-D2 kept it optional, and his own words there were *"a sparkline
   shows a trend beside a headline figure, it is not an analysis tool."*

## 6 · Confirmation — ⛔ NOTHING WAS BUILT, AND THAT IS THE FINDING

**The brief's premise aged, and building to it would have contradicted a ruling.** The brief said
"the documented Replay button is missing from markup: add it and its behaviour". Driven to the
source instead of taken on trust:

- **The Replay button EXISTS.** It lives in the showroom's ONE BAR (`showroom/confirmation.html`,
  generated by `knowledge/gen_showroom.py`) — **ruled #98-D1**, when Dave purged demo controls out of
  all 75 snippet sources so the components would be *"pure canonical"* and Replay was **kept but
  moved into the bar**.
- **This component is named in the generator's own comment** as the second recognised motion idiom —
  **ds-029, ruled #103: "Replay = second detection idiom, snippet untouched"** — and **#104** fixed
  that bar control to restart this file's `svg.success` correctly (`getBoundingClientRect`, because
  `offsetWidth` is HTMLElement-only).
- So an in-file Replay would have **re-introduced the exact demo-control class #98-D1 removed** and
  **duplicated a ruled control**, visible as two Replay buttons in the review surface.

**What was done instead:** I built it first, found the ruling, and **reverted the build** (`git
checkout` on the file, then a fresh minimal edit). The repair went to the **PROSE**: the header now
says where the button is and cites #98-D1 / ds-029 / #103 / #104, so the file no longer describes a
control it does not own. The verify script proves the premise mechanically — a harness control
drives `showroom/confirmation.html` and asserts its `#replay` is present and **enabled** for this
component, and a second control asserts the component still owns **no** replay affordance.

**⬛ For Dave — the one item that most needs your eye**
- Accept the prose repair (shipped), **or** overrule #98-D1 for this component and let it own a
  replay affordance of its own. The second reading is NOT built and would need your word, because it
  reverses a ruling. Cost if you want it: ~30 lines, one afternoon, and the same duplication risk.

## 7 · Timeline — "Load older activity" → a real load

**Built.** Two further date groups arrive from a **declared demo dataset carried in the file as a
readable JSON island** (`#tl-older-demo`) — the Video-player precedent for a declared demo clock. A
reference artefact may not fetch, and a faked network call would be a worse invention than declared
copy. Each load is announced through `role="status"`. When the record is exhausted the button is
**replaced by an end note rather than disabled** (a disabled control still asserts something is
there), and the focus the vanishing button held is moved onto that note.

**⛔ The header's prohibitions were honoured and are asserted, not just promised:** no `aria-current`,
no `role="progressbar"`, no focusable entries. A harness control drives two loads and then checks
all three absences — green in both arms, so it is an invariant, not a behaviour claim.

**⬛ For Dave**
- **Pagination by DATE GROUP (drawn) or by a fixed entry count?** A product rule, not a component one.
- The invented older-activity copy is his to replace with something the product would really show.

---

## Verification — driven both ways, tails verbatim

`knowledge/_render/verify_phantom_surfaces_218.py` (NEW, untracked). 11 harness controls + 27
surface checks. **Every check drives a real click or key press and reads state off the live DOM** —
a load assertion is banned, because "the panel is in the markup" was true of nothing that worked.

```
=== verify_phantom_surfaces_218 — REAL FILES
controls green 11/11 · surfaces green 27/27
GREEN
```
```
=== verify_phantom_surfaces_218 — BREAK ARM (s218-D4 work removed)
controls green 11/11 · surfaces red 27/27
BREAK ARM OK — every surface assertion is load-bearing.
```

**The break arm mutates per file, because the work differs per file:** behaviour `<script>` stripped
(Headers · Navigations · Avatar-group · mandate row · Timeline) · the `S218-D4-KPI-SPECIMEN` block
stripped (Kpi-tile — there is no script to strip, by its own prohibition) · the s218-D4 prose
correction stripped (Confirmation). JSON islands (token-manifest, Timeline's demo dataset) are never
touched: they are not behaviour.

**⚠ THE BREAK ARM EARNED ITS KEEP ON THE FIRST RUN — 8 of 27 checks passed WITHOUT the work.**
Every "Escape closes / clicking away closes / only one opens at a time" check was one-sided: its
"after" state equalled the authored state (closed, focus on the trigger, because clicking a button
focuses it). All eight were rewritten as two-sided transitions that assert the OPEN leg first, and
now go red by name. *This is the second consecutive wave where the arm caught exactly this class —
worth a standing note for whoever writes the next one.*

**The W3 inline-script contract, MEASURED rather than asserted** (≤16KB · no polling · no network ·
no external source · `node --check` clean) — five scripts, extracted and checked one by one:

```
Headers                    3,040 bytes   polling/network hits: []   node --check OK
Navigations                6,384 bytes   polling/network hits: []   node --check OK
Avatar-group               1,990 bytes   polling/network hits: []   node --check OK
Standing-order-mandate-row 4,646 bytes   polling/network hits: []   node --check OK
Timeline                   3,523 bytes   polling/network hits: []   node --check OK
Kpi-tile        — NO behaviour script, by its own prohibition
Confirmation    — NO behaviour script, by #98-D1
```

**Gates, before → after (whole tree; other lanes are live in it):**

| gate | before | after |
|---|---|---|
| `_validate_snippets.py` | 135 snippet(s), 0 failure(s) | **135 snippet(s), 0 failure(s)** |
| `_validate_a11y.py` | 0 fail, 285 warn | **0 fail, 286 warn** (the two inherited hit-area warnings above) |
| `_validate_grid.py` | PASS 151 file(s) | **PASS 151 file(s)** |
| `_validate_descender_clip.py` | PASS 151 file(s) | **PASS 151 file(s)** |
| `_validate_type_composites.py` | 1097 | **1095** — the ratchet SHRANK; my seven files contribute **zero** new raw font declarations (checked by name in the gate's own listing, twice: two `font-weight:500` rules I first wrote into the Kpi specimen were caught and removed in favour of a `.t-cm-ctl-14` composite) |

**Render env (per the photography brief's pitfalls, session-suffixed `-s218ph`):**
`TMPDIR=/var/tmp` · `PYTHONPATH=/var/tmp/pylibs` · `PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-215`
· `FONTCONFIG_FILE=/var/tmp/fonts-s218ph.conf` (fresh symlink farm + `/var/tmp/fccache-s218ph`) ·
`LD_LIBRARY_PATH=/var/tmp/chromelibs/...:/var/tmp/chromelibs-s213e2/...` (both paths load-bearing).
Font probe with controls, not a boolean: `HSBC_MtUnivers_Latin` **347** · `"Univers Next for HSBC"`
**347** · `DejaVu Sans` 375 · nonexistent face 301 — both aliases land on the target and not on the
fallback number.

**Seen, not just asserted — six renders READ by eye, one per theme where it matters:**
Headers menu open **supercharge dark** · Navigations search + account open **legacy light** ·
mandate row panel open **mono light** · Timeline after one load **console dark** · Kpi specimen
**legacy light** · Avatar overflow **console dark**. PNGs are NON-REPO: `outputs/s218ph-shots/`
(session outputs folder, not the repo tree).

**The four-theme axis was checked mechanically, not assumed.** Every new var is DECLARED in its
file's token-manifest, so the showroom's per-theme projection reaches it —
`cascade.component_overrides` re-binds e.g. Headers 8/11 vars under supercharge including
`--menu-surface` and `--menu-border`; per file (legacy/mono/console/supercharge): Headers 1/0/0/8 ·
Navigations 1/0/0/10 · Avatar-group 3/0/1/10 · mandate row 9/0/8/15 · Kpi-tile 5/0/3/11 · Timeline
10/0/10/16 · Confirmation 6/0/2/7. An UNDECLARED var would have rendered mono in three themes and
nobody would have seen it — that is why the new vars are in the manifests.

## Tree state left for the conductor (reconcile every path)

**Modified (7):** `knowledge/snippets/` — `Headers` · `Navigations` · `Avatar-group` ·
`Standing-order-mandate-row` · `Kpi-tile` · `Confirmation` · `Timeline` `.reference.html`
(+849 / −51).
**New (untracked, 1):** `knowledge/_render/verify_phantom_surfaces_218.py`.
**Also this file:** `notes/_receipts/2026-08-25-phantom-surfaces.md`.

⚠ **`knowledge/_A11Y-GATE.md` is REGENERATED as a side effect of running `_validate_a11y.py`** — it
is a gate output, not a hand edit, and my runs rewrote it. Declared rather than reverted.
⚠ **No store rows exist** for the new verify script or this receipt (forgotten-document class,
#185) — **rows owed at the conductor's wrap**; workers do not write the store.
⚠ **SEAM:** other lanes were live in the shared tree during this work (`.github/workflows/gates.yml`,
`knowledge/_rulings.json`, `knowledge/_ICON-SOURCE-AUDIT.md`, several `_render/gen_*.py` and
`verify_*.py`, and at least one snippet — `Alert.reference.html` — moved under me and are **not
mine**). The whole-tree TYPE-002 number therefore moves with their work as well as mine; my seven
files' contribution was measured by name.

## Residuals, priced

1. **Showroom pages are STALE for all seven components** — `gen_showroom.py` was NOT run: it writes
   `showroom/*.html` including `chart-bar`, which is another lane's region, and the fence named the
   seven component files only. Cost to clear: one `gen_showroom.py` run by the conductor once the
   lanes converge (~1 min), then `--check` goes green again. **Until then `gen_showroom --check`
   will read all seven as out of sync — expected and declared, not a defect.**
2. **Component metas untouched** — the seven `knowledge/components/*.meta.json` files still describe
   components with no surfaces. Fenced (not named in the brief). Cost: seven small `$note` edits,
   ~20 min, conductor's or a follow-up lane's.
3. **No gate polices these inline behaviour scripts** — #218 W3's finding F2 stands unchanged: the
   ≤16KB / no-polling / no-network contract is honoured by hand here (all five scripts are well
   under, none polls, none fetches) and enforced by nothing. Gate-shaped candidate, still unbuilt.
4. **The verify harness is a fourth near-copy** of the `verify_behaviour_218w3_*` structure (~130
   shared lines) — W3's finding F6, now n=4. A shared test harness is a real candidate; still a
   test-architecture question, not a snippet one.
5. **Two inherited a11y warnings** are now attributed to named elements rather than anonymous ones
   (Headers' 40×40 header button; Search-field's 24×24 clear ×). Neither is new; both are the parent
   artefacts'. Fixing either changes a gated component.
6. **Confirmation surface 6 is UNRESOLVED until Dave rules** — the prose repair is shipped, the
   alternative (component owns its own replay) is not built and needs his word because it reverses
   #98-D1.

## Fence

No rulings inscribed · no tokens/canon touched · no registry/serial/`component-types.json` ·
no store/lane/GM/LS/memory edits · **no commit, no push** · Command-palette, Chart-bar and every
wave-3 lane component untouched · `/var/tmp` session-suffixed `-s218ph` throughout.
