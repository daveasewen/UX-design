# Receipt — #203 Wave 3, Lane D · overlays (Toast · Drawer · Popover)

*Worker receipt per the parallel-conductor checklist, against the brief
`_BRIEF-wave3-foundations-2026-08-19-v1.md` (v1, FABLE conductor, 2026-08-19).*
*⛔ Nothing here is a ruling. No commit, no push, no git mutation of any kind. `knowledge/_rulings.json` untouched.*

**Gauge at close** — `_checkin.py`, real Claude tokens: FILL **108,667 real** · boot **56,488**
(inside the ruled band) · peak 108,667 over 18 turns · room to the advisory stop line (150,929)
**42,262**. Throughput 122,840 (`gauge.count`, one call — a different object, never summed with FILL).

---

## 1 · The headline, before anything else

**The brief's premise did not hold, and it does not hold for any of the six lanes.**

Wave 3 was briefed off `reviews/ITINERARY-2026-07-14-apollo-component-library.xlsx`, which marks
rows 69/70/71 — Toast, Drawer, Popover — as **`Gap` / `P1` / `1 Foundations`**. They are not gaps.
All three were built, gated, metaed, showroomed and migrated on **2026-07-22**, eight days after
that spreadsheet was written. I did not re-build them. Re-building them would have produced three
duplicate components and clobbered a month of ruled work.

I checked the other five lanes' rows with the same probe, because a premise that stale is rarely
stale in one place:

| Lane | Rows | Itinerary says | On disk |
|---|---|---|---|
| A | 13 · 20 · 68 | Gap | `Form-layout` · `Textarea` · `Alert` — **all present** |
| B | 14 · 15 · 16 | Gap | `Date-picker` · `Date-range-picker` · `Time-picker` — **all present** |
| C | 17 · 89 · 19 | Gap | `Amount-input` · `Amount-display` · `Secure-entry` — **all present** |
| **D** | **69 · 70 · 71** | **Gap** | **`Toast` · `Drawer` · `Popover` — all present** |
| E | 54 · 52 · 51 | Gap | `Empty-state` · `Stat-card` · `Data-grid` — **all present** |
| F | 72 · 18 · 34 | Gap | `Skeleton-loader` · `File-upload` · `Stepper` — **all present** |

**18 of 18.** They landed in three commits: `397e3e4` (2026-07-19), `60e4dc1` "Phase-2 wave 1:
14 components land" (2026-07-22), `16c8b84` "Phase-2 wave 2: 10 components land" (2026-07-22).
The itinerary snapshot predates all three. Corroboration, not just my reading: at the time of
writing, lanes A, B, C and E have each landed a receipt and review pages and **not one of them has
created a snippet or a meta** — `git status --untracked-files=all` shows `knowledge/` carrying only
the two files that were already dirty at session open.

⇒ **[[premise-ages-faster-than-rule]], at the scale of a whole wave.** The brief's §3 instruction
to verify the premise first-hand is what caught it. The itinerary is a **derived snapshot**, and it
was treated as live state. **PROPOSED for the conductor:** the itinerary needs a freshness stamp or
a generator that recomputes `Status` from `ls knowledge/snippets/`, or the next wave briefed from it
will make the same mistake. Not fixed here — it is a shared file and a scope question.

## 2 · The re-scope — PROPOSED #203, Dave's eye owed

Given the above, "build three components" was not available. What I did instead, and why I judge it
the honest reading of the brief's own words (*"a real, reviewable component for Dave's eye, not
scaffolding"*):

> **Audit the three existing overlays against the current ruled bar, and give Dave the four-theme
> live review surface the brief's fence already provides for.**

The review page is in the fence verbatim (`reviews/REVIEW-203-<slug>-four-themes-v1.html`) and is
the one thing these components have never had: they are Apollo-Mono-only snippets, and until now
nobody had put them through the real generated `canon.css` in all four themes and looked.

**⛔ I did not touch the snippets, the metas, or any shared file.** Every defect below is a proposal.

## 3 · Step 0 — the premise, verified first-hand

| Claim inherited from the brief | Verified? | Evidence (probe named) |
|---|---|---|
| HEAD is at #202 | ✅ TRUE — `ec2336d` | `git log --oneline -1` |
| Toast/Drawer/Popover are P1 **gaps** | ❌ **FALSE** — all three gated since 2026-07-22 | `ls knowledge/snippets/`; `git log --diff-filter=A` per file |
| The other 15 rows are gaps | ❌ **FALSE** — 18/18 present | itinerary parsed with `openpyxl` + `ls` cross-check |
| Type-composite debt is **1,101** | ⚠ **STALE** — measured **1,097** today | `_validate_type_composites.py`, rc=1 |
| Gates are green at HEAD | ❌ **FALSE** — `_validate_snippets` rc=1, 18 failures | run at HEAD before any change |
| Snippets carry four themes | ❌ **FALSE, and correctly so** — all snippets are mono light/dark; four themes live in `canon.css` and are exercised at the review layer. Progress-bar (the #174 exemplar) is the same. Declared as canon grammar, not a defect. | `grep data-theme` across 6 snippets; `REVIEW-174` |
| Notifications/Tooltip must be read first | ✅ done — §5 | both read in full |

## 4 · Deliverables

| File | State |
|---|---|
| `reviews/REVIEW-203-toast-four-themes-v1.html` | NEW — 4 themes × light/dark + Toast-vs-Notifications side-by-side |
| `reviews/REVIEW-203-drawer-four-themes-v1.html` | NEW — 4 themes × light/dark |
| `reviews/REVIEW-203-popover-four-themes-v1.html` | NEW — 4 themes × light/dark |
| `notes/_receipts/2026-08-19-203-wave3-laneD-overlays.md` | NEW — this file |

**Nothing else in the repo was written or modified by this lane.** No snippet, no meta, no token, no
generator output, no shared document.

Every pane is the **real gated markup**, extracted from the approved artefact by line-slice with a
content assertion (`must_contain`, fails loud if the line numbers move), rendered through the real
generated `canon.css` — never re-drawn ([[specimen-starts-from-reference]]; #202's three hand-rolled
pages and three invented defects are the reason). The builder lives at `/var/tmp/s203/build.py`,
outside the repo, per the #174 precedent — it is not an instrument the repo carries.

⚠ **Declared: the three `-v1` files were regenerated in-lane, twice.** The render caught two wrong
claims (§7·3, §7·5) and a missing tail, and I rewrote the same `-v1` rather than leaving three stale
files for the conductor to merge. No `-v1` was ever presented, committed or seen. Nothing Dave has
reviewed was replaced. If the conductor reads "version, don't overwrite" more strictly than that,
say so and I will re-emit as `-v2`.

## 5 · How mine differ from the gated Notifications and Tooltip — the brief's explicit ask

Both were read in full before building. The distinctions are also stated on each review page.

**Popover vs Tooltip — clean, and enforced by the markup.** Tooltip opens on hover/focus, is
`role="tooltip"` (measured: 3 occurrences), binds to its trigger with `aria-describedby`
(5 occurrences), holds plain text, and nothing inside it is focusable. Popover opens on click, is
`role="dialog"` + `aria-labelledby`, its trigger carries `aria-expanded`/`aria-controls`/
`aria-haspopup="dialog"`, and it holds focusable content. Shared: only the placement mechanics.
No overlap. The Popover snippet's own header already states this and the meta already carries it.

**Drawer vs Modals — clean.** Same mechanics (scrim, `aria-modal="true"`, focus trap, `inert` page,
Esc, focus return), different anchoring: edge-docked instead of centred, so the page stays
glanceable. Verified in the source, not assumed.

**Toast vs Notifications — ⚠ NOT clean. This is a real finding.**
`Notifications.reference.html:190–193` already ships a **Snackbar** placement: `role="status"`,
transient, warning/success/information, **error deliberately omitted** — identical brief to Toast,
identical ARIA, identical status set. The difference is purely chrome:

- **Notifications · Snackbar** — *tinted* ground plus elevation shadow, coloured 1px border.
- **Toast** — *elevated neutral raised surface*, no tint, the status glyph sitting on it.

Rendered side by side (third strip of every Toast pane) they read as two different components doing
one job. **PROPOSED #203, Dave's eye owed:** either Toast supersedes the Notifications Snackbar
placement and that placement retires, or the two are given a stated reason to differ. I have not
resolved it — it is a duplicate-surface question *and* a component-promotion question, and
**component promotion of any kind is on the brief's DO-NOT-RULE list.** Surfaced, never swapped
([[feedback-visual-compare-duplicates]], [[feedback-grey-tint-check]]).

## 6 · Gates — every rc reported, every gap declared

Baseline measured at HEAD **before** anything was written, so failures are attributable.
⚠ Exit codes captured directly, never through a pipe (#174's void first reading).

| Gate | Baseline at HEAD | After | Verdict |
|---|---|---|---|
| `_validate_snippets.py` | **rc=1** · 76 snippets, **18 failures** | rc=1 · 76, 18 | ⚠ **red at HEAD, unchanged** — see below |
| `_validate_a11y.py` | rc=0 · 76, 0 fail, 179 warn | rc=0 · 76, 0 fail, 179 warn | ✅ unchanged |
| `_validate_type_composites.py` | **rc=1** · **1,097** across 90/91 files | rc=1 · 1,097 | ✅ ratchet held (see scope note) |
| `gen_showroom.py --check` (read-only) | — | **rc=0** · 76 pages + index in sync | ✅ I disturbed nothing |
| `_validate_state_contrast.py` | — | **NOT RUN** | ⛔ declared, see below |

**Scope, stated precisely — a green here would be a green that cannot fail.** All three validators
glob `knowledge/snippets/*.reference.html` (plus `knowledge/_proforma/` for the type gate);
`reviews/` is **not scanned by any of them**. My three files therefore contribute **0** to the 1,097
debt **by scope, not by merit**. I authored them with composites only and no raw font declarations
anyway, but I am not claiming a gate proved that. [[gate-glob-scope-rule]], [[unrun-search-is-not-an-absence]].

**`_validate_state_contrast.py` — NOT RUN, and I tried to cross the fence before declaring it.**
I grepped it for a `--check` / no-write / filter flag before concluding: line **1317** is an
unconditional `open(os.path.join(HERE,"_STATE-CONTRAST-AUDIT.md"),"w")` with no suppression option.
Running it — even filtered to my components, as #174 did — **rewrites a shared tracked artefact**,
which the fence forbids under any framing. Owed to the conductor or CI.
[[instrument-without-a-consumer]] — I did not inscribe a fence I had not tried to cross.

### ⚠ `_validate_snippets` is RED AT HEAD, and it is not this lane's

18 failures, **all one class**: `DRIFT --pri-hover`, across **nine** snippets —
`Action-bar` · `Button` · `Confirmation` · **`Drawer`** · `Empty-state` · `Form-layout` ·
`Icon-button` · `Modals` · `Stepper`.

The snippets still carry the pre-`s198-D1` ramp-snapped literals `#626262` light / `#B7B7B7` dark;
the token store now says `#636363` / `#B2B2B2` — minted at `s198-D2`, renamed `hover-light` /
`hover-dark` at `s199-D2`. The snippets were never re-synced after the mint.
**`canon.css` is correct** — it resolves `var(--primary-background-hover)` — so the review panes
show the *right* hover and only the snippet files are stale.

**Four of the six Wave 3 lanes touch an affected file** (A: Form-layout · D: Drawer · E: Empty-state ·
F: Stepper). **PROPOSED for the conductor:** one re-sync pass over the nine snippets at reconcile,
not six lanes each patching shared state. I have not touched it. This is exactly the
[[chart-expansion-programme]] warning — *an alias-repoint can strip a theme's override silently* —
arriving from the other direction: the repoint landed and the consumers were left behind.

## 7 · The audit — what the four themes actually showed

Render proof: `goto("file://…")`, **never `set_content()`**. Font asserted with a canvas measurement
against **two controls**, not `fonts.check()` — target `HSBC_MtUnivers_Latin` **347**, both aliases
`"Univers Next HSBC"` / `"Univers Next for HSBC"` **347**, `DejaVu Sans` **375**, a nonexistent face
**301** ⇒ the real HSBC cut, both aliases landing on it, neither falling back. Symlink farm per #138;
tree asserted clean afterwards — `0` `.uuid` strays, `git status --untracked-files=all -- knowledge/`
shows only the two files already dirty at session open. Rendered at **1180 and 480**. PNGs were
**read**, not merely produced.

**1 · Toast and Notifications-Snackbar are two answers to one question.** §5. The strongest item here.

**2 · The Toast dark roundel has been waiting since 2026-07-22.** The snippet's own manifest note
says the dark coloured roundel on the elevated neutral ground was *"flagged in the worker receipt for
confirmation"* — the tint-surface white-shape ruling targets *tinted* grounds, not elevated neutral
ones. It was flagged and then nothing happened for a month. Now visible in four dark panes.
**PROPOSED, Dave's eye owed.**

**3 · CORRECTION, caught by the render — Console's 20px radius is RULED, not a drift.** My first pass
wrote that square corners hold in every theme. The render measured `border-radius: 20px` on all
three overlay surfaces in Console, light and dark. Before calling it a defect I searched the store:
**`s199-D3`** (Dave, #198→#199, off the radius tuner) — *console control 4→8, **surface 12→20***.
It is Dave's own rounding arriving correctly. The claim was corrected on the page.
⇒ [[retrieval-default-hides-the-ruling]] — the store refused a "new" defect. Had I not checked I
would have handed Dave a fabricated bug against his own ruling, in a lane briefed to find bugs.

**4 · Measured: in Supercharge dark, the only thing holding these overlays off the page is a hairline
at 1.96:1.** The elevation recipe is shadow-in-light, 1px-border-in-dark. In light the panel is
*exactly* the page colour in all four themes (1.00:1) and the shadow does the work — canon, reads
fine. In dark the border takes over, and it is not equal across themes:

| theme, dark | hairline | on | ratio |
|---|---|---|---|
| mono / legacy / console | `#808080` | `#1A1A1A` | **4.41:1** ✅ |
| supercharge | `#524842` | `#1A1A1A` | **1.96:1** ❌ under the 3:1 non-text floor |

Pre-existing and theme-level, not these components' — but they are what shows it. Not declared as a
gated `contrastPair`: it would be a green that cannot fail in the theme where it is false (the #174
precedent for exactly this shape). **PROPOSED, Dave's eye owed.** ⚠ Belongs in
`knowledge/_DS-IMPROVEMENTS.md`; that file is on the fence's do-not-touch list, so it is queued here
for the conductor to merge, not written.

**5 · CORRECTION, also caught by the render — one of these is not like the others, and it is Popover.**
`Popover` binds `--surface` → `background/default`, the **page** token. `Toast` and `Drawer` both bind
→ `tertiary/background/default`, the **raised-surface** token. Measured consequence in dark:

| | mono dark | supercharge dark |
|---|---|---|
| Toast / Drawer surface vs page | 1.06:1 | 1.16:1 |
| **Popover** surface vs page | **1.00:1** | **1.00:1** |

The Popover is painted precisely the colour of the page it floats above, in all four themes, both
modes; everything separating it is the hairline — and in Supercharge dark that is the 1.96:1 hairline
above. Deliberate, or an inconsistent binding across three siblings sharing one elevation recipe?
Never ruled. **PROPOSED, Dave's eye owed.**
⚠ *My own instrument nearly lied here first:* my pane rule, inherited from `REVIEW-174`, painted dark
panes with `--surface-digital-black`, a **different token** from the page background, which made the
Supercharge numbers look like a canon defect. I suspected the measurement before the artefact
([[a-crash-is-not-a-fail]] discipline) and re-pointed the pane to `--background-default`. The finding
survived the correction in a cleaner form; the fabricated version did not.

**6 · Popover cannot be seen standing still.** Toast ships `.spec` and Drawer ships `.specimen`
precisely so the component can be shown in-flow, at rest. **Popover ships neither.** `.pop` is
`position:fixed` with `opacity:0`, revealed only by its placement JS — so it is invisible in any
still: a review page, a showroom thumbnail, a screenshot, a paste into Figma. The panes exist only
because the page carries a **declared** local override, marked `REVIEW-SURFACE OVERRIDE` in the
`<style>` block. Its tail is likewise absent without `pos-above`/`pos-below`, so the specimen carries
`pos-below` — the class the snippet's own `place()` adds when the trigger sits above it. Verified
after the fix: the `::after` tail computes 10×10 in all 8 panes with the correct per-theme surface
and border. **PROPOSED: give Popover a static-specimen affordance matching Drawer's `.specimen`.**

**7 · Popover's trigger is unstyled demo chrome.** `.pop-trigger` has **no canon rule at all**, so it
renders as a raw browser button — grey, round-cornered, in every theme, and conspicuously wrong on
the dark panes (seen in the PNG, not inferred). Not part of the component, but it is the first thing
anyone opening the snippet or the showroom page sees, and it borrows the browser's corners in a
square-corner system.

**8 · 44px min-hit-area — enforced by hand, passes on all three.** No gate enforces it (§5 of the
brief says so); I measured it in the sources rather than assuming. Toast: action is a real 44px-tall
button, dismiss × is a 24px visual with a 44×44 `::before`. Drawer: footer buttons 44px, close × a
36px visual with a 44×44 `::before`. Popover: close × 24px visual with a 44×44 `::before`. ✅
⚠ Worth the conductor's attention: `Drawer.reference.html:118–120` records that the **wave-1 receipt
claimed 44 and the file measured 36**, and the conductor corrected the receipt to the file. That
class of error has happened in this exact component before.

**9 · Colour is never the only carrier.** Every status toast carries `data-carries="symbol label"`, a
glyph and a sentence. Correct for the problem hues [[colour-stability-red-yellow-problem]].

**10 · Type-composite debt, attributed.** Toast 3 · Drawer 3 · Popover 2 = **8 of the 1,097**. Seven
are demo chrome (`body` font-family, the demo `h2`'s `font-size:14px` / `font-weight:500`). **One is
in a component**: `Popover`'s `.pop a { font-weight:500 }` — an inline link's weight set raw instead
of by a composite. The gate already keeps a demo-chrome advisory bucket; these are not in it.

## 8 · Decisions needed — Dave's, none of them mine

1. **Toast vs the Notifications Snackbar placement.** Two chromes, one job. Retire one, or state why
   both. *(Touches component promotion — DO-NOT-RULE, so genuinely untouched.)*
2. **The Toast dark roundel** on the elevated neutral ground — confirm or change. Open since 07-22.
3. **Supercharge dark's 1.96:1 elevation hairline** — accept, or lift the token.
4. **Popover's surface binding** — page token or raised-surface token? Currently the odd one of three.
5. **A static-specimen affordance for Popover** — add, or accept it cannot appear in stills.
6. **`.pop-trigger`** — style it in canon, or mark it explicitly out of scope.
7. **Toast stack placement** — bottom-left (current, MD3) or top-right (Ant). Never ruled.
8. **Drawer `side`** — the enum has only `"right"`. Deliberate scope box, or a gap?
9. **`.pop a { font-weight:500 }`** — the one real type violation of the eight.
10. **The re-scope itself** (§2) — was auditing the right call over rebuilding? If you want three
    genuinely new overlay components, the itinerary rows are the wrong place to find them.

## 9 · Proposals for the conductor to merge

- **The `--pri-hover` re-sync** across nine snippets (§6). One pass, not six.
- **`_DS-IMPROVEMENTS.md`**: the Supercharge-dark 1.96:1 elevation hairline (§7·4); the Popover
  surface-binding inconsistency (§7·5). Queued here, not written — the file is fenced.
- **The itinerary's `Status` column is a stale derived snapshot** (§1). Freshness stamp, or generate
  it. This is the whole wave's root cause and it will recur.
- **Carried-figure correction**: type-composite debt is **1,097**, not the 1,101 in the standing
  memory hook. The ratchet is shrink-only, so 1,097 is the new floor. Same class as #194's
  "standing 44" measuring 4 [[premise-ages-faster-than-rule]].
- **No `CATEGORIES` entry is needed** — `toast`, `drawer`, `popover` are already listed at
  `gen_showroom.py:142–143`. No token proposals: I minted nothing and wished for nothing.

## 10 · Residuals and friction — declared, not glossed

- **Two of my own claims were wrong and the render caught both** (§7·3 console radius, §7·5 pane
  token). Both were corrected before delivery. Neither would have been caught by a gate; both would
  have been caught by Dave, expensively. The render is the fourth check and it earned its place.
- **`_validate_state_contrast.py` unrun** (§6) — owed to the conductor or CI.
- **`_validate_snippets` red at HEAD** — pre-existing, proven at HEAD before I wrote anything.
- **Write tool cannot reach `/var/tmp`** in this session; the builder had to be written by bash
  heredoc in two chunks. Minor, but it means the `/var/tmp` scripts are not readable by file tools.
- **`/var/tmp` farms were re-used, not rebuilt** — `pw-browsers-s197`, `pylibs-s203e` (another #203
  lane's), `chromelibs-s201`. Read-only re-use per the #161 pothole; no download was needed. Disk
  healthy (`/` 70%, `/sessions` 16%) — no ENOSPC this session, n=0.
- **Nothing was deleted, moved, or git-touched.** No `checkout`, `restore`, `stash`, `add` or
  `commit` was issued at any point. The only git commands run were read-only: `log`, `ls-tree`,
  `status`.

**Machinery price** — `0 instrument / ~470 feature`. No gate, checker or harness was built. The three
throwaway scripts (`/var/tmp/s203/{build,shoot,crop,tail}.py`) live outside the repo and are not
instruments the repo carries.
