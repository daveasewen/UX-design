# Receipt — #204 Wave, Lane P · Fintech visuals (Payment-card visual · Coverage/runway bar)

*Worker receipt per the parallel-conductor checklist, written 2026-08-19, `s203-D2` PM-topology trial.*
*⛔ Nothing here is a ruling. No git command of any kind was run — no commit, no push, no `checkout/restore/stash`.*
*⛔ No generator was run, not one, not even `--check`. `_build_all.py` NOT run.*
*⛔ No existing file was edited. `knowledge/_rulings.json`, `component-types.json`, all `tokens/*.json`, `canon.css`, `_DS-IMPROVEMENTS.md`, `_REVIEW-SIGNOFF.md`, `_validate_radius.py`, `gen_showroom.py`, `knowledge/_state.py` — untouched. Proposals for the BUILD-PM are at the end, as exact text.*

**Context gauge at close — `knowledge/_checkin.py`, run live:** BUDGET **FILL 120,690 real** · boot 56,589 · peak 120,690 over 28 turns · room to the advisory stop line (150,929) **30,239** · throughput 136,525 real (`gauge.count`, one call — not comparable to FILL).
⚠ **Declared, not glossed:** `_checkin.py` reads the *session* transcript, which this wave shares with sibling lanes. That figure is **session-wide, not this lane's isolated spend** — a sub's own window is not separately instrumented, and I am not converting it into a per-lane number (`measure-dont-convert-units`).

---

## Headline for the BUILD-PM, before anything else

### 1 · Row 94's provenance: **this row originates in a TEST FIXTURE, not a product need. PROVEN, not assumed.**

The itinerary's own note said "fitness tests invented this". I chased it to ground and the chain is complete:

- `grep -rn "runway" knowledge/_COMPONENT-GAPS.md` → line 18, under the heading **"Token / system gaps (SME-Payments fitness tests, 2026-06-30) — Exposed by the portfolio run: the canon was silent in exactly the places it had to invent"**, records verbatim: *"Data-viz palette + chart primitives | no chart components, no named data series — **the waterfall / runway / proportional bars were invented** | … | 2026-06-30"*.
- `grep -rn "runway" knowledge/_fitness-test/*.html` → **four synthetic pages** (`sme-payments-portfolio`, `-balanced`, `-final`, `cold-A-inference`) each hand-rolling a `.runway` section in raw hex and raw `font:` shorthands. `cold-A-inference.html:217` even labels its own block *"coverage rail (right 4 cols) — the runway readout"*. Probe artefacts.
- `grep -rn "runway" knowledge/_COMPONENT-LIBRARY-TARGET.md` → **line 104**, the *Fintech-specific* table: *"Payment-card visual · Coverage/runway bar · Standing-order / mandate row · Limits meter | **GAP · P2–P3**"*.
- `grep -inE "runway|coverage|burn rate|fintech|plastic|contactless" knowledge/_rulings.json` → **ZERO hits naming this component.** ("coverage" appears only as *gate* coverage; sample lines quoted in the premise table.)
- `python3 knowledge/_memento_search.py "runway bar"` — run, and **disregarded as evidence**: the retrieval index is STALE this session. The ruling claim rests on the **direct grep of `_rulings.json`, the store itself** (`retrieval-default-hides-the-ruling`: store > chain).

**Verdict, stated plainly and put on the review page as its first note:** a fitness test invented a runway section because the canon had nothing to offer it → the invention was logged as a *token/system gap* → the gap was promoted into the Layer-1 target table → the target table became the itinerary row. There *is* a real user question underneath — *"does my money cover what is already scheduled, and until when?"* — and the fitness test answered it with drawn evidence. **But nobody has ruled that it should be a component. Declining it is a completely legitimate answer, and it is Dave's first decision.** It is built PROPOSED so he can answer by eye.

### 2 · The Chart-bullet overlap: **the brief named the wrong neighbour. It is not a Chart-bullet; it is a Progress-bar.**

The `ITINERARY-STATUS` JSON's `related` field said *"Chart-bullet is a measure-vs-target gauge — the nearest gated grammar"*. I read `Chart-bullet.meta.json` and `progress-bar.meta.json` in full and the evidence points the other way:

| | Chart-bullet (gated) | Runway bar | Progress-bar (gated) |
|---|---|---|---|
| purpose, verbatim | *"a measure bar against a **comparative target marker** and **qualitative performance ranges**"* | no target, no bands | *"a **determinate** completion display … as a proportion of a **known total**"* |
| intent | `comparison` | composition of one balance | proportion |
| form | SVG figure, fixed 580px, real `<table class="dv-table">` (dv-005), `data/series/1` fill, ink target tick | two CSS rules and text | `.pb-track` / `.pb-fill`, 4px + 8px |
| non-% domains | via chart axis | yes | **yes — specimen 3, "Savings goal · 1,450 of 2,000", `aria-valuetext` carries the units** |
| its own `commonPatterns` | revenue/satisfaction/retention vs target | — | **"savings goal / limits meter"** ← already names this shape |

★ **The tell: a Chart-bullet needs a TARGET; a runway bar has no target, it has a HORIZON.** Nothing is measured against a goal; the question is how far the money reaches.
⇒ **So the bar is a Progress-bar and is copied byte-for-byte. This lane drew no new bar.** What is actually absent is not a bar but a **readout**: the verdict-with-a-date, the balance−committed arithmetic, and the two-key legend. A molecule around a gated atom.
★ **A runway bar without the verdict and the arithmetic IS a Progress bar and should be one. A runway bar with a target IS a Chart-bullet and should be one.** Both are antiPatterns in the meta.

### 3 · Row 93: the brand surfaces are **empty on purpose**, and that is the deliverable's headline

Every brand surface on the card face is a **declared, empty, PROPOSED placeholder slot** — issuer mark, network mark, EMV chip. Probe, quoted: `ls knowledge/assets/icons/*/ | grep -iE "chip|visa|mastercard|amex|network"` → **empty**. No such glyph exists. `_validate_icons.py` exists precisely to stop invented icons, and inventing a *brand* mark is worse. `#86-D2` fences our own marks too (Dave, verbatim: *"the crescent is only a mark for apollo, we use it when we need designs to be anonymous / use the hsbc mark normally"*).
**The one glyph on the card is real and byte-matched:** `assets/icons/media/contactless.svg` — a functional indicator, not a brand mark.

### 4 · The green/red that is not there

⛔ A cash-runway meter is exactly where a healthy/critical binding gets invented. **I invented none.** The bar is **ink on track in every state including "Short"**, inherited from the gated Progress-bar, whose meta gives the reason in Dave's own words: *"Progress is STRUCTURE, not status (Dave 2026-07-21) — hence the ink pair rather than a RAG colour."* Coverage is a **quantity**. The verdict is a separate object: a Status-indicator chip carrying **a word and a date**, copied verbatim from Account-card. Which verdict maps to which tone is a **semantic** binding and is Dave's.
⛔ The live Stat-card / Kpi-tile FILL-vs-INK two-red seam (#203) is on this lane's DO-NOT-RULE list. **Neither component touches it** — no arrows, no deltas, no series anywhere. The chip *dot* does sit on the same fill seat; **inherited and flagged exactly as Account-card already declares it**, never resolved, never load-bearing.

---

## Step 0 — the premise table. One row per claim, probe quoted, verdict.

⚠ **HEAD sha not quoted: the lane brief forbids git commands outright.** Declared gap, not a silent one.

| # | Claim | Probe run, quoted | Verdict |
|---|---|---|---|
| 1 | Row 93 `payment-card-visual` is absent — no snippet | `ls knowledge/snippets/ \| grep -i <t>` for **card · payment · credit · debit · plastic · face** → `card` matches only `Account-card`, `Cards`, `Stat-card`; **all five others EMPTY** | ✅ **CONFIRMED** |
| 2 | …and no meta | same greps over `ls knowledge/components/` → `account-card.meta.json`, `cards.meta.json`, `stat-card.meta.json` only | ✅ **CONFIRMED** |
| 3 | Row 94 `runway-bar` is absent — no snippet | `ls knowledge/snippets/ \| grep -i <t>` for **runway · coverage · meter · gauge · burn · cash** → **all six EMPTY**; `bullet` → `Chart-bullet`, `progress` → `Progress-bar`/`Progress-tracker` | ✅ **CONFIRMED** |
| 4 | …and no meta | same greps over `ls knowledge/components/` → **all six EMPTY** | ✅ **CONFIRMED** |
| 5 | Content-level check, not just filenames | `grep -rinE "runway\|payment[ -]card\|card[ -]face\|burn[ -]?rate\|contactless\|embossed\|cardholder\|card number\|CVV\|magstripe\|coverage bar" knowledge/snippets/ knowledge/components/` → **5 hits, none a component**: `Cards.reference.html:193` (*"a contactless debit card"*, prose inside a radio option), `_nodes-pattern.json:417` + `banner.meta.json` ×2 (`pattern:expiry-warnings`, unrelated) | ✅ **CONFIRMED absent** |
| 6 | No ruling names either component | **direct grep of the store**: `grep -inE "runway\|payment[ -]card\|card face\|coverage\|burn rate\|fintech\|plastic\|contactless" knowledge/_rulings.json` → 6 hits, **every one about something else**: line 1145 *"the digest's own card face"* (the #124 graph-mark ruling, a metaphor), 1865 / 2478 / 2485 / 2853 / 2920 all *gate* or *links* **coverage**. **ZERO name a fintech visual.** | ✅ **CONFIRMED — no ruling** |
| 7 | ⚠ the retrieval index is STALE, so the search tool cannot carry claim 6 | `_capture_gate.py --selftest` reports the structural retrieval index STALE this session (carried forward from the #203 laneK receipt and re-declared here). `_memento_search.py` was run and its result **not used as evidence**. | ✅ handled — claim 6 rests on the store, not the index |
| 8 | Row 94's note "fitness tests invented this" is literally true | `grep -rilE "runway" --include=*.md --include=*.html --include=*.py .` → `knowledge/_COMPONENT-GAPS.md`, `knowledge/_COMPONENT-LIBRARY-TARGET.md`, `knowledge/gen_itinerary_status.py:200-202`, and **four `knowledge/_fitness-test/*.html` pages**. Full quotations in the headline above. | ✅ **CONFIRMED — and it is the headline** |
| 9 | Chart-bullet is "the nearest gated grammar" for row 94 | Read `Chart-bullet.meta.json` (141 lines) **in full**. Purpose: *"a measure bar against a comparative target marker and qualitative performance ranges"*; `intent: "comparison"`; SVG at fixed 580px; real `dv-table`; `data/series/1` measure fill; ink target tick | ❌ **FALSE as stated — Chart-bullet is NOT the nearest.** Pivoted to measurement rather than building on it (see claim 10) |
| 10 | The nearest gated grammar is Progress-bar | Read `progress-bar.meta.json` (147 lines) + `Progress-bar.reference.html` (164 lines) **in full**. `commonPatterns` **already contains "savings goal / limits meter"**; specimen 3 is a non-% determinate bar (`Savings goal · 1,450 of 2,000`) with `aria-valuetext` carrying units; `$note` states *"Progress is STRUCTURE, not status (Dave 2026-07-21)"* | ✅ **CONFIRMED — this is the parent, and the bar is copied from it byte-for-byte** |
| 11 | No chip / network / issuer glyph exists to copy | `ls knowledge/assets/icons/*/ \| grep -icE "visa\|mastercard\|amex\|emv"` → **0**; `\| grep -iE "^chip\|network"` → **rc=1, no matches**. `_validate_icons.py` docstring confirms it byte-matches every inline `<svg>` path against the library and fails UNKNOWN | ✅ **CONFIRMED — slots stay empty** |
| 12 | A real contactless glyph DOES exist | `find knowledge/assets/icons -name contactless.svg` → `./media/contactless.svg`; path data copied byte-for-byte into a `<symbol>` | ✅ **CONFIRMED** |
| 13 | No reveal/eye glyph exists | `find knowledge/assets/icons -iname "*eye*" -o -iname "*show*" -o -iname "*hide*"` → only `miscellaneous/masthead-{show,hide}.svg`, which are **download-arrow + rules** marks — wrong meaning | ✅ **CONFIRMED — the reveal control is a TEXT button, not an icon** |
| 14 | A dark "premium" card face needs a token that does not exist | `knowledge/_COMPONENT-GAPS.md` line 16, verbatim: *"**Inverse / hero surface** — no light-mode dark-band role — the portfolio invented charcoals (`#0E1014`…) when canon dark values already exist"* | ✅ **CONFIRMED — no dark card face was built; this is a FINDING** |
| 15 | `role="meter"` is unruled | `grep -rn 'role="meter"' knowledge/snippets/` → **2 hits, both of them my own new file's prose**, i.e. **ZERO in the 87 pre-existing snippets**; `grep -icE "\bmeter\b" knowledge/_rulings.json` → **0** | ✅ open, and surfaced with its failed search (`s202-D3`) |

★ Claim 9 is the one that came back FALSE. Per the brief I **stopped and pivoted to measurement** on that component before drawing anything, and the adjudication in the headline is the result.

---

## Deliverables — 5 new files, nothing overwritten, nothing edited

| File | State |
|---|---|
| `knowledge/snippets/Payment-card-visual.reference.html` | **NEW** — PROPOSED specimen, `#token-manifest` present |
| `knowledge/snippets/Runway-bar.reference.html` | **NEW** — PROPOSED specimen, `#token-manifest` present |
| `knowledge/components/payment-card-visual.meta.json` | **NEW** — includes `antiPatterns`, `$differsFrom`, `$decisionsForDave` |
| `knowledge/components/runway-bar.meta.json` | **NEW** — same, with the provenance verdict inside `provenance.source` |
| `reviews/REVIEW-204-payment-card-visual-four-themes-v1.html` | **NEW** — 8 panes, 1400 + 480 |
| `reviews/REVIEW-204-runway-bar-four-themes-v1.html` | **NEW** — 8 panes, 1400 + 480 |
| `notes/_receipts/2026-08-19-204-wave-laneP-fintech-visuals.md` | **NEW** — this file |

**Specimens COPY the approved artefact, never re-draw** (`specimen-starts-from-reference`). Sources copied verbatim and left untouched:

| Copied atom | From |
|---|---|
| Card shell (surface / 1px border / `border-radius-surface` / 16px padding), `···` masked-number idiom, `.tag` atom, `.chip` RAG-tint atom with dot + word, the `role="group" + aria-labelledby` unit | `Account-card.reference.html` (which itself carries Tags + Status-indicator) |
| `.pb-track` / `.pb-fill`, 4px + 8px heights, `progress/complete` on `progress/incomplete`, `role="progressbar"` + `aria-valuenow/min/max/valuetext`, the reduced-motion clause, and the **zero-raw-type-declaration pattern** | `Progress-bar.reference.html` |
| `.amount` money-format primitive (symbol before with no space, tabular lining, `-.01em` at display size, U+2212 minus, monochrome) | `Amount-display.reference.html` |
| Tertiary button (44px `--h`, outlined, `button/tertiary/*`, focus 2px offset 2) | `Button.reference.html` |
| Review-page shell (`.pane` grid, `data-apollo-theme` sections, `.cn-` hand-mirror convention) | `reviews/REVIEW-203-kpi-tile-four-themes-v1.html` |
| PROPOSED-header convention, `$status` field in the manifest | `Kpi-tile.reference.html` (`s182-D2` precedent) |

**No new token was minted or wanted.** Every value both components use already exists and is already bound by a gated component.

---

## Gates — every rc captured directly, verbatim

| Gate | Result | Verdict |
|---|---|---|
| `python3 knowledge/_validate_snippets.py` | **rc=0** — `snippet gate: 91 snippet(s), 0 failure(s)` | ✅ |
| `python3 knowledge/_validate_a11y.py` | **rc=0** — `a11y gate: 91 snippet(s), 0 failure(s), 186 warning(s), 218 note(s) · 566 controls + 203 marks measured · 107 mark(s) below 24` | ✅ |
| `python3 knowledge/_validate_type_composites.py <my 2 files>` | **rc=0** — `TYPE GATE PASS — all component text bound to canon composites (2 file(s)).` + `advisory — 0 raw font decl(s) in demo-chrome scope` | ✅ |
| `python3 knowledge/_validate_type_composites.py` (repo-wide) | **rc=1** — `TYPE GATE FAIL — 1097 violation(s) across 90/106 file(s). TYPE-001 ×31 · TYPE-002 ×1050 · TYPE-003 ×16` | ✅ **RATCHET HELD — I added ZERO.** 1,097 is the measured baseline (#203). Both files declare **no raw font at all** — no `body{font-family}`, no `font-size` anywhere, following Progress-bar's zero-raw-type pattern |
| `_validate_dataviz.py` | **NOT RUN — declared, and the reason is load-bearing** | Neither file carries dataviz geometry: no SVG chart canvas, no `data/series/*`, no `dv-*` class. That absence is itself part of the Chart-bullet adjudication. The `#184` dangling-dataviz-var silent-black class **cannot apply** to files with no dataviz vars |
| `_validate_state_contrast.py` | **NOT RUN — declared owed** | A filtered run overwrites the tracked `_STATE-CONTRAST-AUDIT.md`. With sibling lanes live and no shared-file edits permitted, restoring it by hand was not a risk worth taking. **Owed to the BUILD-PM or CI** |
| `_validate_radius.py`, `_validate_icons.py`, `_validate_coverage.py`, `_build_integrity.py`, every generator `--check` | **NOT RUN — the BUILD-PM's serially** | Declared by name. A declared gap passes; this is the declaration |

⚠ **The filtered runs of `_validate_snippets.py` and `_validate_a11y.py` are not actually filtered** — they ignore the path argument and sweep the whole directory (the known defect the brief names). I therefore attributed my contribution **by diffing the failure list**, not by trusting the filter. Both were rc=0 with **0 failures** at 91 snippets, so my two files contribute zero failures by construction.

⚠ **Snippet count moved 90 → 91 mid-lane** as sibling lanes wrote. Every count here is timestamped by the probe that produced it.

### Two gate failures I caused and fixed, recorded because they are cheap intelligence

1. **`_validate_snippets.py` rc=1 ×2** — `ALL-CAPS text run "INK ON TRACK"` and `"NO RED WAS INVENTED"` in my *visible* specimen captions. The **type26-019 sentence-case rule is gated and it bites on rendered text, not on comments.** Fixed by sentence-casing the captions; the emphasis survives in the file comments where the gate correctly does not look. Useful signal: the gate distinguishes prose-in-comments from prose-on-screen.
2. No other gate ever went red.

---

## Render proof — driven, not asserted

`goto("file://…")` throughout; **`set_content()` never used.** `_RUNBOOK-render-verify.md` read **before** touching anything. Environment, all four env vars set on every call (each bash call is independent):
`PYTHONPATH=/var/tmp/pylibs-s203e` · `PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-s197` · `FONTCONFIG_FILE=/var/tmp/fonts-s204p.conf` · `TMPDIR=/var/tmp` · `LD_LIBRARY_PATH=/var/tmp/chromelibs/root/usr/lib/aarch64-linux-gnu`.
Fontconfig **symlink farm** at `/var/tmp/fonts-s204p` (10 links) with the `<include>` present and `<cachedir>` outside the repo, so markers land in the farm. **No browser download was needed** — the `#138`/`#161` guidance to reuse foreign `/var/tmp` farms read-only worked first time; **no launch failure occurred**, so the `libXdamage` pothole did not arise.

**Font asserted by CANVAS MEASUREMENT against two controls, never `fonts.check()`** (40px `Handgloves 12345`), identical at 1400 **and** 480:

| probe | measured |
|---|---|
| `HSBC_MtUnivers_Latin` | **347** |
| `"Univers Next for HSBC"` (snippet alias) | **347** |
| `"Univers Next HSBC"` (type.css alias) | **347** |
| `DejaVu Sans` — control | 375 |
| nonexistent face — control | 301 |

Both aliases land on the target and **not** on the nonexistent-face number ⇒ the real HSBC cut, and the probe demonstrably discriminates.

**Result: 8/8 panes on both pages, at 1400px and 480px, 0 page errors, no document overflow.** All four themes fork correctly and were read **off the DOM**:

| theme · mode | runway `--fill` (progress/complete) | runway `--track` | track radius | card `--surface` | card radius | card box |
|---|---|---|---|---|---|---|
| mono light | `rgb(26,26,26)` | `rgb(240,240,240)` | 0px | `rgb(255,255,255)` | 0px | 340×214, ratio **1.586** |
| mono dark | `rgb(255,255,255)` | `rgb(72,72,72)` | 0px | `rgb(31,31,31)` | 0px | 340×214, 1.586 |
| legacy light | **`rgb(51,51,51)`** ← Legacy's own ink `#333333`, not the Mono black | `rgb(240,240,240)` | 0px | `rgb(255,255,255)` | 0px | 340×214, 1.586 |
| legacy dark | `rgb(255,255,255)` | `rgb(72,72,72)` | 0px | `rgb(31,31,31)` | 0px | 340×214, 1.586 |
| console light | `rgb(26,26,26)` | `rgb(240,240,240)` | **4px** | `rgb(255,255,255)` | **20px** | 340×214, 1.586 |
| console dark | `rgb(255,255,255)` | `rgb(72,72,72)` | **4px** | `rgb(31,31,31)` | **20px** | 340×214, 1.586 |
| supercharge light | **`rgb(19,17,14)`** ← the warm DNA tier `#13110E` | **`rgb(223,222,220)`** `#DFDEDC` | 0px | `rgb(247,246,244)` | 0px | 340×214, 1.586 |
| supercharge dark | `rgb(247,246,244)` | `rgb(65,57,52)` `#413934` | 0px | **`rgb(42,38,33)`** `#2A2621` | 0px | 340×214, 1.586 |

Every one of those is the value the theme is *supposed* to produce, including Supercharge reaching `progress/incomplete` through the `color/neutral → color/warm` DNA rebind rather than an explicit override (the `#108` "a token NAME is not an ADDRESS" case, observed working).

**44px minimum hit area — enforced BY HAND and PROVEN, since no gate reads the token from a snippet.**
`button.pcv-reveal` measured in **all four themes × both modes × both widths**: **16 targets, zero under 44** (each 190×44 / 176×44 depending on label). The runway bar is **passive throughout — 0 interactive targets**, stated so the absence is declared rather than assumed.

Renders viewed by eye at `outputs/s204p-renders/` — **(NON-REPO: session outputs folder)**, `s191-D2` marker. They are my verification, not review artefacts; HTML is what Dave reviews.
Repo-pollution assert after the fact: `ls -a knowledge/assets/fonts/_desktop/TTF/ | grep -c '^\.uuid'` → **0**; `find . \( -name '.uuid*' -o -name '*.LCK' \) -not -path './_to_delete/*'` → **empty**.

### ★ Four defects the gates could not see, caught only by looking at the render

All four were invisible to every green gate (`green-tests-cannot-see-scope`), and **three of them were in my own review-page builder, not in the components** — the #203 laneK lesson repeating in a new shape: *a page-builder is an artefact that needs its own verification, not a transparent pipe.*

1. **⛔ A SELF-REFERENTIAL VAR MAPPING SILENTLY KILLED CONSOLE'S RADIUS — and this is the finding worth carrying.** My `.cn-` mirror emitted, from the manifest, `--border-radius-surface: var(--border-radius-surface);`. That is a **cycle**, CSS resolves a cyclic custom property to its *initial* value, and the card rendered **0px in Console where it should be 20px** — measured, then fixed, then re-measured at 20px. It is silent: no error, no warning, no gate, and the value that appears is a *plausible* one (square corners are the house rule), so it reads as correct. The same trap exists for `--border-radius-indicator` (Console 4px) and `--alpha-48`. **Generalised: wherever a snippet's local var name is identical to the semantic token name, a mechanical `local: var(semantic)` emitter produces a cycle.** The fix is to emit nothing and let the cascade supply it. `gen_canon_components.py` avoids this today by emitting explicit per-theme forks instead — worth checking that it always does. **This is the same species as `#184`'s dangling dataviz var: a var that resolves to a plausible wrong value rather than failing loudly.**
2. **`box-sizing:border-box` was dropped by the mirror**, because the extractor skips the snippet's `*{}` rule. The card face rendered **374×248 (ratio 1.506)** instead of 340×214 (1.586) — padding and border added outside the declared width. The snippet itself was always correct; **only the review surface was wrong**, exactly the case a snippet-scoped gate cannot reach. Fixed by scoping `box-sizing` into the mirror; re-measured 340×214 / 1.586 in all 8 panes at both widths.
3. **The specimen rack stretched component atoms to the card's width.** `.unit{display:flex; flex-direction:column}` defaults to `align-items:stretch`, so a 24px status chip and the reveal button rendered ~340px wide. Cosmetically wrong in a way that misrepresents the atoms. Fixed in the snippet with `align-items:flex-start` (demo chrome, not component CSS).
4. **A `⛔` in visible caption text rendered as TOFU (▯)** — the HSBC cut has no U+26D4. Removed from rendered text; the symbol survives in comments and in this receipt. **Generalisable: the emphasis symbols this project uses in prose are not in the brand font and must never reach a rendered specimen.**

Also caught by eye and fixed: the compact card's placeholder labels ("issuer mark", "network mark") **wrapped inside their boxes**, and the compact card's descriptive line wrapped onto two lines — a `.t-cm-*` composite is single-line by rule (the N1 caveat), so multi-line component text is an off-grid defect, not a cosmetic one. Fixed by shortening the slot labels to one word with `white-space:nowrap`, and by moving to Account-card's own `···4821` masking idiom with a `.sr-only` accessible name carrying the readable sentence.

The extractor/page-builder is a **throwaway at `/var/tmp/s204p/`, outside the repo** (the #174 / Lane E precedent). It is **not** an instrument the repo carries. `machinery: 0 instrument / ~110 feature`.

---

## The components

### Row 93 — Payment card visual. How it differs from its nearest gated neighbours

- **vs `Account-card` (the real neighbour).** Account-card's subject is **money**: label + masked number + **balance** + status. This component's subject is the **physical instrument**, and it carries **no balance at all**. Account-card answers *"how much is in it?"*; this answers *"which piece of plastic is this, and is it usable right now?"*. **A payment-card visual showing a balance is an Account-card wearing a card shape and should be an Account-card** (antiPattern).
- **vs `Cards`.** Cards is the generic content-surface family — a rectangle you put arbitrary things in, with **no anatomy**. This is a representation of a specific real-world object with a **fixed ID-1 geometry and a fixed anatomy**. Cards has no anatomy; this is nothing but anatomy.
- **vs `Chart-bullet`.** No relationship whatsoever. Named in the meta only because rows 93 and 94 are adjacent and a reader may carry row 94's chart neighbourhood across.

Anatomy: issuer-mark slot · product tag · chip slot + contactless indicator · masked number · cardholder + expiry · network-mark slot · status chip. Variants: default (340px) · compact (240px) · revealed · unusable (frozen / expired).
Geometry is quoted as an **external physical standard**: `aspect-ratio: 1.586` = ID-1, ISO/IEC 7810 (85.60 × 53.98 mm) — so it cannot be mistaken for taste.
Colour never alone: every status carries its **word**, and the unusable states additionally drop to `alpha/48` — a **second non-colour channel**.

### Row 94 — Coverage / runway bar

Adjudication is in the headline. Anatomy: label + **verdict chip carrying a word and a date** · buffer figure in the Amount-display display size · the Progress-bar rule · a two-key legend naming both segments in money · the `balance − committed = buffer` arithmetic as a real `<dl>`. Four specimens: covered · tight · **short** · emphasis (8px).

Colour never alone is enforced **three ways** on every specimen: the verdict word and date, the full arithmetic in text (17.4:1), and `aria-valuetext` on the bar. **Strip every colour from this component and it still says everything it means.**

---

## Findings

### ⛔ Finding 1 — a self-referential custom-property mapping resolves to a plausible WRONG value, silently

Full detail in render-proof defect 1. It cost Console's 20px surface radius and 4px indicator radius across 8 panes, produced no error anywhere, and the wrong value it produced (`0px`) is *the house default*, so it reads as correct. **A gate candidate:** flag any generated or hand-written `--x: var(--x)`. Proposed for `_DS-IMPROVEMENTS.md` below. Same species as `#184`'s dangling dataviz var — the failure mode is *plausible wrongness*, not visible breakage, and that is the class of defect this system is least able to see.

### ⚠ Finding 2 — the ITINERARY-STATUS `related` field can name the wrong neighbour, and it is authoritative-looking

Row 94's `related` field says *"Chart-bullet is a measure-vs-target gauge — the nearest gated grammar"*, generated by `gen_itinerary_status.py:200-202`. Reading both metas in full says the nearest gated grammar is **Progress-bar** — whose own `commonPatterns` **already names this shape** (*"savings goal / limits meter"*). The `related` hints are a *derived* editorial judgment sitting inside a file whose `$status` correctly says *"a MEASUREMENT of the store, not a ruling"*, but a worker reading only the JSON would have built a bullet chart. **Signal for the BUILD-PM and for Lane H's successor: the `related` hints are a hypothesis to be tested against the metas, not a finding.** (`premise-ages-faster-than-rule`.) Row 96 `limits-meter` carries the **same** Chart-bullet hint and is very likely the same misdirection — a Progress-bar with a limit, not a bullet.

### ⚠ Finding 3 — `_validate_hit_area.py` EXISTS, and the standing "no gate reads 44px" claim needs qualifying

`ls knowledge/` shows **`_validate_hit_area.py`**, plus `_HIT-AREA-ADVISORY.md` and `_HIT-AREA-ADVISORY.json`. The brief's instruction ("no gate reads this token, enforce by hand") is what I followed and I measured by hand regardless — but the honest statement is **"no *blocking* gate reads it from a snippet"**, not "no gate exists". I did **not** run it (it is not on this lane's list and the 44-enforcement record split is on the DO-NOT-RULE list), so I make **no claim about what it does or whether it would pass**. Flagged so the BUILD-PM can decide whether the standing phrasing needs correcting. `unmatched-grep-is-not-an-absence` applies in reverse: I found the file, which does not tell me it is wired.

### ⚠ Finding 4 — the "short" and "tight" verdicts land on the same chip tone, which is a design question the drawing exposes

Both take the warning tint, so a reader cannot tell "nearly out" from "already short" by the chip alone — they can only tell by the **word and the date**, which is exactly the design intent but which also means the chip tone is carrying no information in that pair. Whether "short" should move to the **error** seat is a two-red question and therefore **Dave's**; I deliberately did not take it. Shown, not described: the two states sit adjacent in every pane.

### ⚠ Finding 5 — `_COMPONENT-GAPS.md`'s inverse-surface gap blocks a whole family, not one component

The absent `inverse/hero surface` role is why there is no dark card face here. The same absence will block any "premium card", any dark hero band, and any inverted summary panel. It is logged as a *token/system gap* from 2026-06-30 and is still open. **It is the single token most likely to be invented ad hoc by the next lane that needs a dark band** — the fitness-test portfolio already did it once (`#0E1014`).

---

## Decisions needed — Dave's, every one PROPOSED #204

**Row 94, before anything else**
1. ★ **Should the runway bar exist at all?** It originates in a fitness-test fixture. Nothing in the store asked for it. **Declining it and closing the itinerary row as "not a component" is a completely legitimate answer.**
2. If it exists: is the shape right — verdict + buffer figure + bar + legend + arithmetic? Or is the arithmetic a `Summary` and this component just the verdict and the bar?
3. ★ **The verdict vocabulary and its chip binding.** "Covered through 31 May" → success tint; "Covered to 24 May" → warning; "Short from 12 May" → warning. Should **short** be the *error* seat? That touches the two-red law and I did not take it (finding 4).
4. `role="progressbar"` vs `role="meter"` — nothing in the store rules it (searches quoted, `s202-D3`).
5. The **short** state pins the bar at 100% and clamps `aria-valuenow`, because a progressbar cannot express overflow. Should there be a dedicated overflow treatment, and if so, what is it **that is not a red bar**?
6. Should the 8px emphasis variant live here at all, or should a consumer compose Progress-bar's own emphasis size?

**Row 93**
7. Should this component exist in this form? Fintech semantics are yours.
8. **The three brand placeholder slots** — right shape, right positions, right count? And is a dashed labelled placeholder the right way to say *"a licensed asset belongs here"*?
9. ★ **Corners.** The card follows the angular rule (square in Mono/Legacy, 20px in Console). **Real cards are rounded.** Should a payment-card visual be a documented **exemption**, like Avatar and Badge?
10. ★ **The dark / premium card face.** It needs the `inverse/hero surface` role that `_COMPONENT-GAPS.md` records as missing (finding 5). Mint the role, or accept a light-only card face?
11. The status vocabulary and its chip binding: active → success, frozen → warning, **expired → warning**. Should expired be the error seat? Same two-red caution as item 3.
12. The reveal control is a **text button**, not an icon, because no eye/reveal glyph exists in the library. Correct call, or is a new glyph owed to `_ICON-GAPS.md`?
13. Should the **revealed-PAN state ship at all**, or should the component stop at masked?

**Both**
14. Neither component is registered anywhere (`component-types.json`, `MIGRATED_SNIPPETS`, `CATEGORIES` / showroom, `canon.css`). **Registration is promotion and therefore yours** — and none of it should happen before items 1 and 7.

None of the above was resolved here. **Nothing a sub writes is a ruling.**

---

## Proposals for the BUILD-PM to merge — exact text, I edited no shared file

**`_DS-IMPROVEMENTS.md`, add:**
> *"A SELF-REFERENTIAL CUSTOM-PROPERTY MAPPING (`--x: var(--x)`) IS A CYCLE, AND CSS RESOLVES A CYCLE TO THE INITIAL VALUE — SILENTLY, AND OFTEN TO A PLAUSIBLE VALUE. Proven at #204 Lane P: a `.cn-` scope generated mechanically from a snippet's `#token-manifest` emitted `--border-radius-surface: var(--border-radius-surface)`, which killed Console's 20px surface radius and the 4px indicator radius across 8 panes. No error, no warning, no gate, and the wrong value produced (`0px`) is the house default so it reads as correct. This arises for EVERY manifest var whose local name equals its semantic token name (`--border-radius-*`, `--alpha-*`). Candidate gate: scan `canon.css` and any generated scope for `--([a-z0-9-]+):\s*var\(--\1\)` and fail. Same species as #184's dangling dataviz var: plausible wrongness, not visible breakage."*

**`_DS-IMPROVEMENTS.md`, add:**
> *"A `.cn-` scope that drops the snippet's `*{box-sizing:border-box}` rule changes component GEOMETRY, not just chrome. Proven at #204: a card declared `width:340px; aspect-ratio:1.586` rendered 374×248 (ratio 1.506) in the review mirror while the snippet itself was correct. Any hand-mirrored or generated scope must carry `<scope>, <scope> *, <scope> *::before, <scope> *::after{box-sizing:border-box}`."*

**`_DS-IMPROVEMENTS.md`, add:**
> *"The project's emphasis symbols (⛔ U+26D4, ★, ⚠) ARE NOT IN THE BRAND FONT and render as tofu in a specimen. Proven at #204 by render. They belong in comments, receipts and review-page prose (which is not brand-typeset), never in rendered component text. type26-019 already gates ALL-CAPS in rendered text; this is the adjacent case and is currently ungated."*

**`_DS-IMPROVEMENTS.md`, reinforcing the standing item:**
> *"`_validate_hit_area.py`, `_HIT-AREA-ADVISORY.md` and `_HIT-AREA-ADVISORY.json` EXIST in `knowledge/`. Lane briefs continue to state 'no gate reads the 44px token'. The accurate statement is 'no BLOCKING gate reads it from a snippet'. #204 Lane P enforced 44px by hand across 16 measured targets without running the advisory, because the 44-enforcement record split is on a DO-NOT-RULE list. The phrasing and the wiring should be reconciled by whoever owns that record."*

**`gen_itinerary_status.py` / Lane H's successor — a signal, not an edit:**
> *"Row 94's `related` hint names Chart-bullet as 'the nearest gated grammar'. Reading both metas in full at #204 says the nearest is Progress-bar, whose own `commonPatterns` already contains 'savings goal / limits meter'. The `related` hints are a derived editorial hypothesis, correctly marked PROPOSED at the file level, but a worker reading only the JSON would have built a bullet chart. **Row 96 `limits-meter` carries the same Chart-bullet hint and is very likely the same misdirection.** Consider marking `related` explicitly as a hypothesis to be tested against the meta."*

**`component-types.json`** — neither component is registered. Payment-card-visual needs no dataviz partial (no chart geometry); runway-bar needs none either (no SVG at all). **Registration is a promotion decision and therefore Dave's, not a merge chore** — flagged, not requested, and it should not happen before decisions 1 and 7.

**`gen_canon_components.py` / `canon.css`** — no `.cn-payment-card-visual` or `.cn-runway-bar` scope exists. The review pages hand-mirror them, **deriving every binding from each snippet's own `#token-manifest`**. When the BUILD-PM regenerates, the authoritative scopes should replace the mirrors — **and finding 1 should be checked against the generator's own output first**.

**`_validate_radius.py` `MIGRATED_SNIPPETS`** — two new snippets are absent from the radius ratchet (⛔ shared file). Console's 20px surface and 4px indicator radii were verified present in the render.

**`CATEGORIES` / `gen_showroom.py`** — two new slugs (`payment-card-visual`, `runway-bar`) have no showroom entry. ⛔ shared file, and neither should be added before Dave rules.

**Itinerary rows 93 and 94** — both were genuinely `Gap`; the Status column is **correct** for both. Row 94's *note* is also correct and unusually valuable — *"fitness tests invented this"* was the single most useful sentence in the brief.

**No new token is wanted.** One token is *proposed* and is Dave's: the `inverse/hero surface` role (finding 5), which is already logged in `_COMPONENT-GAPS.md` and is not mine to mint.

---

## Friction log

- **The brief's hazard 2 was right to make me read both metas in full, and it changed the build.** Had I taken the itinerary's `related` hint at face value I would have drawn a bullet chart with a target that does not exist. The Progress-bar meta's own `commonPatterns` line — *"savings goal / limits meter"* — is what settled it, and it was one line deep in a file I was told to read in full. **Reading the whole meta was the load-bearing instruction.**
- **The provenance hunt cost two calls and was worth all of them.** The chain `_fitness-test/*.html` → `_COMPONENT-GAPS.md` → `_COMPONENT-LIBRARY-TARGET.md` line 104 → itinerary row is now on the record, so the next lane that meets rows 95/96 (Standing-order row, Limits meter — the *same table row* in `_COMPONENT-LIBRARY-TARGET.md`) inherits it rather than re-deriving it. **All four fintech P2–P3 rows come from that one table line.**
- **The store grep, not the search index, is what carried every ruling claim.** `_memento_search.py` was run and its answer deliberately not used, because the index is STALE this session.
- **I wrote a claim I had not probed, and the probe disproved it.** My first draft of the runway snippet asserted `role="meter"` had *0 hits across snippets*. Running it returned **2** — both my own file's prose. The honest form ("zero in the 87 pre-existing snippets; the only 2 hits are this file's own words") is now what the file, the meta and the review page all say. Cheap here; the same shape unchecked is how a false inscription happens.
- **I also quoted a contrast figure from memory (2.11:1) and measured it at 2.18:1.** Corrected in both snippets before the gates ran, using the repo's own `_contrast_utils.contrast_ratio`. **A remembered number is not a measurement.**
- **Three of my four eye-caught defects were in my own page-builder, not the components.** Exactly the #203 laneK lesson, in a new shape. The builder is a throwaway and was still the least trustworthy thing in the lane.
- **`type26-019` bit twice on my visible captions** and was correct both times. The gate distinguishes rendered prose from comment prose, which is the right line.
- **Concurrency is visible**: the snippet count moved 90 → 91 during the lane, and sibling lanes' `REVIEW-204-*` files appeared alongside mine in the same directory listing.

---

## Residuals — declared, not glossed

- **`_validate_state_contrast.py` NOT run.** A filtered run overwrites the tracked `_STATE-CONTRAST-AUDIT.md`; with sibling lanes live and no shared-file edits permitted, restoring it by hand was not a risk worth taking. **Owed — BUILD-PM or CI.**
- **HEAD sha not captured** — the lane's ⛔ on git commands overrides the base brief's §3. Declared.
- **Both components are absent from `canon.css`, the radius ratchet, the showroom and `component-types.json`.** All four are shared surfaces. The review pages' `.cn-` scopes are hand-mirrors, faithful to each manifest but **not generator output** — that is the fence working, and it is declared, not silent.
- **`_validate_dataviz.py` not run, and the reason is affirmative, not evasive:** neither file contains dataviz geometry, an SVG chart canvas, a `data/series/*` token or a `dv-*` class. I state that as a property I checked, not as an assumption.
- **`_validate_icons.py` not run** (BUILD-PM's). The one inline glyph was byte-copied from `assets/icons/media/contactless.svg` and should classify as `library`, but **I did not drive the gate and therefore do not claim it passes.**
- **`_validate_hit_area.py` not run** (finding 3). 44px was enforced and measured by hand instead.
- **Narrow-viewport reflow below 480px is unexamined** and is not claimed. Verified at 1400 and 480 only.
- **The reveal toggle is drawn as two static specimens, not scripted** — no `AUTO-BEHAVIOUR` partial is injected because the component is not registered. Declared.
- **The runway bar's `role="progressbar"` is inherited, not adjudicated.** `role="meter"` may be more correct and nothing in the store settles it.
- `outputs/s204p-renders/` holds 8 PNGs — **(NON-REPO: session outputs folder)**, `s191-D2`.
- Throwaway extractor/page-builder at `/var/tmp/s204p/` — outside the repo, not carried, not an instrument.

---

## ⚠ CONSEQUENCES / PITFALLS — what I did NOT run, what a green gate cannot see, what to attack first

**What I did not run:** `_build_all.py` and every generator (fenced) · `_validate_state_contrast.py` (would overwrite a tracked file) · `_validate_radius.py`, `_validate_icons.py`, `_validate_coverage.py`, `_validate_dtcg.py`, `_build_integrity.py`, `_validate_hit_area.py` · every generator `--check` · any git command. **A declared gap passes; this is the declaration.**

**What a green gate cannot see here:**
- **Whether either component should exist.** `_validate_snippets.py` rc=0 says the tokens resolve. It says nothing about whether a fitness-test fixture deserved to become a component. **Row 94 could be fully green and still be the wrong thing to have built.**
- **The four-theme legs.** The snippet gate resolves against `tokens/semantic-colour.json`, the **mono base only**. Every Legacy / Console / Supercharge figure in this receipt was read **off the DOM in a browser**, outside the gate. If the render is wrong, no gate would tell you.
- **A self-referential var** (finding 1). Nothing failed. The radius was simply wrong, and wrong in the direction that looks right.
- **Undeclared vars.** The #203 laneK finding stands: `_validate_snippets.py` compares *declared* vars against the store, so a var omitted from the manifest is invisible to the drift gate. I declared every var I use, including `--alpha-48`, but no gate checked that I did.
- **Semantic correctness of the RAG bindings.** "expired → warning tint" and "short → warning tint" are propositions about *meaning*. Every gate is green either way.
- **Whether the placeholder slots are the right answer.** A gate cannot tell an honest empty slot from a missing feature.

**What a verifier should attack first, in order:**
1. **Row 94's right to exist.** Re-run my provenance greps against `_COMPONENT-GAPS.md`, `_fitness-test/` and `_rulings.json`. If you reach a different conclusion, the whole component is void, not just its details.
2. **The self-referential-var finding, against `gen_canon_components.py`'s real output** — not against my mirror. If the generator has the same shape anywhere, the bug is in canon, not in a throwaway. Mutation-test it: change one theme's radius and confirm the change appears.
3. **The Chart-bullet-vs-Progress-bar adjudication**, by reading both metas yourself. My whole build rests on it. Then check **row 96 `limits-meter`**, which carries the identical hint.
4. **Re-measure the four-theme table off the DOM**, independently. Every figure in it came from one probe script I wrote; a second pair of eyes on `progress/complete` in Legacy (`#333333`, not the Mono black) and Supercharge (`#13110E` via the warm DNA tier) is the cheapest way to catch a probe that lied.
5. **Drive `_validate_icons.py`** on `Payment-card-visual.reference.html`. I byte-copied the contactless path but never ran the gate that would prove it.
6. **Check the `.t-cm-*` single-line rule against the compact card at every width you care about.** I fixed one wrap I could see at 480px; a narrower viewport or a longer product name will wrap again, and no gate reads the N1 caveat.
