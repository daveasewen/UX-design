# Lane 2 — footers in the three footerless shells, and the bento gate premise

Session #258, 2026-09-08. Dave's words: **"the page shells should include the footer"**.

Two jobs. **JOB A is done.** **JOB B is a premise correction** — the finding the cold run
recorded is real, but its cause is not the bento template, and the fix as specified would
have made a convention change that is Dave's, not a lane's.

---

## JOB A — the footer, in all three

Three files carried no footer; the other five `App-shell-*` did. All three now do.

### What was copied, and from where

`Footer.reference.html`'s **slim** form, taken through `App-shell-top-nav.reference.html`'s
copy of it — the same route `App-shell-split`, `App-shell-nav-rail` and `App-shell-focused`
already took, so the atom arrives with one provenance rather than four. Copied verbatim:
the legal bar, the `a.lnk` link atom (which Footer itself copied from Links), the 44px link
targets, the copyright line, and the `.sh-legal li{display:flex}` **defect repair** that
top-nav found by looking at a render (#204 — an inline-flex child's `min-height` does not
grow its `<li>`'s line box, so without it the two legal links and the copyright render on
top of one another). ⛔ **No parent file was edited.**

Type arrives through `canon/type.css` composites applied in the markup (`.lnk t-ed-body-small`,
`.copy t-cm-legal`) — the T-D14 route. **Ratchet contribution: 0** (`_validate_type_blast_radius`
exit 0). Zero new hex, zero new CSS vars, zero new icons.

### file:line

| file | CSS block | footer markup | meta |
|---|---|---|---|
| `knowledge/snippets/App-shell-side-nav.reference.html` | L231–252 | L482, L592, L675 (3 specimens) | `components/app-shell-side-nav.meta.json` |
| `knowledge/snippets/App-shell-multi-column.reference.html` | L234–254 | L449, L510, L582 (3 specimens) | `components/app-shell-multi-column.meta.json` |
| `knowledge/snippets/Template-dashboard-bento.reference.html` | L742–765 | L1204 (1 page) | `components/template-dashboard-bento.meta.json` |

Also in each snippet: `#token-manifest` gained the contrast pairs the footer band creates
(`text/default` and `text/secondary` on `surface/subtle`, side-nav L750–751 and
multi-column L626–627 — bento already declared `text/default` on
`tertiary/background/default`), and `requiredAria` gained `role="contentinfo"` so the gate
now **holds the footer in place** rather than merely permitting it (side-nav L774,
multi-column L649, bento L1362).

Meta changes: `$copiedFrom` gained the Footer entry, `$consumes` gained `"Footer"`
(bento: `$composes` gained `component:footer`), `slots` gained `endMatter` (bento is a page,
not a slotted shell — it gained `$finding-site-footer` instead), and each carries a placement
finding with the measured numbers. `edges` was regenerated for the two shells through
`gen_kg_edges.py`'s own code path (only those two files written — the corpus was not swept,
because other lanes hold `data-grid` / `filter-toolbar-bar` / `sidebar-nav` metas).
`_validate_kg.py` exit 0, idempotent-clean.

### THE PLACEMENT DECISION, per shell, and why

**`App-shell-side-nav` — the footer spans the CONTENT COLUMN, not the frame.**
It is a child of `.sh-content`, never of `.sh-body`. That is not a preference: it is
`App-shell-nav-rail.reference.html`'s own arrangement, already on disk, and the reason is the
same in both. The nav column is full-bleed chrome that runs floor-to-ceiling; a legal bar
drawn UNDER it would cut the navigation off at the ankles and tell the user the nav had
ended. **Measured at 1440 in a real browser**, light and dark:

- wide specimen — footer `x=273 w=1142`; the shell starts at `x=25` and the nav column is
  248px, so the footer starts exactly where the column ends.
- rail specimen — `x=89 w=1326` (64px rail).
- phone specimen — `x=25 w=390`, full width, because at that width the nav column has
  `display:none` and has left the layout entirely.

⚠ **One declared difference from nav-rail.** `.sh-content` is this shell's scroll container
(`overflow-y:auto`), so the footer travels with the content and lands at the document end
rather than pinned to the frame's floor as nav-rail's is. That is the document-end reading of
a legal bar and it is deliberate. Pinning it would need a second scroll container — a layout
change this lane did not make, and it is named here rather than smuggled.

**`App-shell-multi-column` — the footer spans ALL THREE PANES,** as the last child of `.sh`.
The rail, the list and the detail are **peers**; none of them is "the content column", and a
legal bar under the detail pane alone would read as belonging to the selected account rather
than to the page. Each pane scrolls internally (`.sh-list-body` / `.sh-detail-body` carry the
`overflow-y:auto`), so a footer outside them is pinned to the frame's floor and stays
reachable at every scroll position. This is the top-nav arrangement, not the nav-rail one —
the two differ because top-nav has one content column and nav-rail has a rail to stop at.
**Measured:** `x=25 w=1390` on the three-pane specimen (full shell width), `x=25 w=390` on
both narrow specimens.

**`Template-dashboard-bento` — body-level, after `</main>`,** the mirror of the masthead
before it. This file is a whole page, not a boxed `.sh` frame. It is **not** inside
`.tpl-page`: that element is the bento wall and carries the s219-D1 pageBg, so a legal bar
drawn inside it would sit on the wall ground and read as one more tile.
⚠ **Its token vocabulary differs, deliberately.** The `App-shell-*` files name a `--band`
(surface/subtle); this file has no `--band`, and its page ground already *is* surface/subtle
(`--wall-ground`). So the footer takes `--surface` (tertiary/background/default) — the same
band `.sh-masthead` uses at the other end of the page. The rendered relation (a lighter band
against the grey wall) is the one the shells draw; the var name is this file's own.

### Themes verified

**The snippet convention supports TWO themes, not four, and the probe says so.**
`grep -ho 'data-theme="[a-z0-9-]*"' knowledge/snippets/*.html | sort | uniq -c` returns
**283 `light` + 203 `dark` and nothing else**, across all 136 snippets. The four Apollo
themes (mono · legacy · console · supercharge) live on `data-apollo-theme`, in canon.css's
AUTO-THEMES cascade — which **0 of 137 snippets link** (the TRUE probe
`grep -l 'href="../canon/canon.css"'`). So "each of the four themes the snippets support"
resolves to two, and both were driven, per file, per specimen, at 1440 in headless chromium:

| render | footer bg | link ink | every legal `<li>` |
|---|---|---|---|
| shells, light | `rgb(240,240,240)` = surface/subtle | `rgb(26,26,26)` | 44px |
| shells, dark | `rgb(31,31,31)` | `rgb(255,255,255)` | 44px |
| bento, light | `rgb(255,255,255)` = tertiary/background/default | `rgb(26,26,26)` | 44px |
| bento, dark | `rgb(31,31,31)` | `rgb(255,255,255)` | 44px |

The 44px `<li>` figure is the one that matters: it is the **mutation proof** that the #204
line-box defect the `.sh-legal li{display:flex}` repair exists for did **not** recur in any
of the three files, in either theme, at any specimen width.

**The four-theme question answered a second way, at the token tier.** The footer's semantic
roles are `surface/subtle` · `tertiary/background/default` · `divider/border/section` ·
`text/default` · `text/secondary` · `target/min`. Walking the three override sets:
`apollo-console` and `apollo-supercharge` override **none** of them; `apollo-legacy`
overrides `text/default` and `text/secondary` only. So the footer's band, rule and hit-area
are base in every theme, and its ink follows Legacy's ink exactly as every other borrowed
atom in these shells already does. **No footer-specific theme fork exists.**
`_validate_theme_provenance.py` exit 0, unchanged (49 advisory hexes, same count as before).

### Render diff

Full-page screenshots, before (HEAD) vs after, 1440×1000, light and dark, headless chromium
via the `_ROBUSTNESS-PORTABILITY.md` recipe (`chromium-headless-shell` channel,
`LD_LIBRARY_PATH=~/.local/chromelibs`, `PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=1`).

| file | theme | page height | pixels differing | rows differing |
|---|---|---|---|---|
| Template-dashboard-bento | light | 1133 → **1194** | 5.11% | **1133–1193 ONLY** |
| Template-dashboard-bento | dark | 1133 → **1194** | 5.11% | **1133–1193 ONLY** |
| App-shell-multi-column | light | 2114 → 2114 | 7.57% | 419–2080 |
| App-shell-multi-column | dark | 2114 → 2114 | 4.33% | 419–2080 |
| App-shell-side-nav | light | 2114 → 2114 | 5.88% | 647–2080 |
| App-shell-side-nav | dark | 2114 → 2114 | 5.88% | 647–2080 |

**The bento row is the finding.** The page grew by 61px — *exactly* the footer's own height —
and the diff touches **only** rows 1133–1193, the appended band. Every pixel above it is
byte-identical in both themes. The bento template's visible result is preserved absolutely.

The two shells reflow because `.sh` is a fixed 640px frame: a 61px footer inside it takes its
room from the content region, which is the intended behaviour of a footer in a fixed shell
(and is what the other five shells already do). Page height is unchanged, so nothing on the
page outside the specimens moved.

---

## JOB B — the bento gate finding: the premise is wrong, and the probe is cheap

The brief asked me to make `Template-dashboard-bento.reference.html` pass
`_validate_screen.py` by token-ifying its 146 hexes and removing its `c-bento*` redefinition.
**I did not do that.** Three measurements say the finding does not mean what it looks like.

### (1) The gate reds EVERY shell, not the bento

Run on all eight, unmodified, before any edit of mine:

```
App-shell-top-nav        EXIT=1  compose: ❌ 33 hex colour(s)
App-shell-split          EXIT=1  compose: ❌ 37 hex colour(s)
App-shell-nav-rail       EXIT=1  compose: ❌ 33 hex colour(s)
App-shell-focused        EXIT=1  compose: ❌ 31 hex colour(s)
App-shell-doormat        EXIT=1  compose: ❌ 32 hex colour(s)
App-shell-multi-column   EXIT=1  compose: ❌ 29 hex colour(s)
App-shell-side-nav       EXIT=1  compose: ❌ 31 hex colour(s)
Template-dashboard-bento EXIT=1  compose: ❌ 146 hex colour(s); redefines c-bento*
```

`_validate_screen.py`'s own default argument is
`_fitness-test/*.canon.html`, and `_validate_compose.check_screen` exists to prove that a
screen **composed from canon.css** has not drifted from it. A reference snippet is the other
kind of artefact: self-contained by convention, carrying its own `[data-theme]` block.
Pointing the composed-screen gate at one is [[gate-cannot-pass-in-one-environment]].

**The pack's own snippet gate is green.** `python3 knowledge/_validate_snippets.py` →
`136 snippet(s), 0 failure(s)`, **exit 0**, bento included, before and after this lane.

### (2) 36 of the 146 "hex colours" are not colours

`check_screen` reads the raw bytes of `<style>` and never strips comments — although the same
module already has `strip_css_comments` and already applies it in `check_canon`, for exactly
this reason, recorded there as the #122 / ds-039 finding ("PARSE IN THE CONSUMER'S GRAMMAR:
the browser never sees comment text"). The fix was applied to one half of the file and not
the other.

What the gate is actually counting in bento: `#231`, `#255`, `#248`, `#217`, `#211`, `#210`,
`#230`, `#245`, `#251`, `#184` — **session numbers in prose**.

| file | raw | comments stripped | false |
|---|---|---|---|
| Template-dashboard-bento | 146 | **110** | **36** |
| App-shell-split | 37 | 34 | 3 |
| App-shell-top-nav | 33 | 28 | 5 |
| App-shell-nav-rail | 33 | 32 | 1 |
| App-shell-doormat | 32 | 28 | 4 |
| App-shell-side-nav | 31 | 28 | 3 |
| App-shell-focused | 31 | 28 | 3 |
| App-shell-multi-column | 29 | 26 | 3 |

**MUTATION PROOF, unplanned and free.** My JOB A comments each cite `#258` once. After the
edit the gate reports **147 / 30 / 32** hexes for bento / multi-column / side-nav — one more
each — while the comment-stripped count is **110 / 26 / 28**, *identical to before*. I added
one prose citation per file and zero colours, and the gate counted a colour in each. That is
the clause under test, driven.

⛔ **I did not patch `_validate_compose.py`.** Changing a gate to make a subject pass is the
[[conflated-fix-guarantees-recurrence]] shape even when the gate is wrong, and the one-line
change (call `strip_css_comments` in `check_screen` as `check_canon` already does) still
leaves 110 — it does not make bento pass. It is a real defect, priced at one line, and it is
the build-PM's to take.

### (3) The remaining 110 hexes and the `c-bento*` redefinition are both DECLARED, and undoing them is Dave's call

The 110 are the `[data-theme="light"]` / `[data-theme="dark"]` blocks — spliced
**byte-identical** from `Template-dashboard.reference.html`, and structurally the same
construct all seven other shells carry (26–34 each). Token-ifying bento alone would make it
the only snippet in 136 that cannot render standalone, and would break the byte-identity its
own splice ledger claims.

The `c-bento*` redefinition is not a drift — the file's header already declares it, in these
terms: the AUTO-BENTO block's one home is `canon.css` (ADR-0017 write-once), this file carries
a **declared second home** because the snippet convention is self-contained, and the TRUE
probe `grep -l 'href="../canon/canon.css"' knowledge/snippets/*.reference.html` returns
**0 of 137**. Its own words: *a snippet that uses a canon structural component either links
canon.css — "which no snippet does, and adopting it is a convention change that is Dave's" —
or copies the block.* The brief's instruction ("link/rely on it as the other snippets do")
rests on a premise the repo contradicts: **no other snippet does this.**

So the specified fix *is* the convention change. That is on the DO-NOT-RULE list, and the
file even names the two options it sits between. Left for Dave.

### The "demo chrome" question, answered

Bento's `.demo-bar` is labelled *"demo chrome only — not part of the template"* (L896).
Checked: it is **already fully tokenised** — `var(--header)`, `var(--divider)`, `var(--text)`,
`var(--fborder)`, `var(--focus)`. **Zero hexes.** None of the 146 come from it. There is no
demo-chrome exemption to argue about.

---

## Gate exits, before → after, per file

| gate | side-nav | multi-column | bento |
|---|---|---|---|
| `_validate_snippets.py` (the snippet gate — **the one that owns these files**) | **0 → 0** | **0 → 0** | **0 → 0** |
| `_validate_screen.py` (composed-screen gate, out of scope — see JOB B) | 1 → 1 | 1 → 1 | 1 → 1 |
| ↳ its `compose` step, raw hex | 31 → 32 | 29 → 30 | 146 → 147 |
| ↳ its `compose` step, **comment-stripped hex** | **28 → 28** | **26 → 26** | **110 → 110** |
| ↳ its `a11y` step | ✅ → ✅ | ✅ → ✅ | ✅ → ✅ (2 pre-existing warns) |
| ↳ its `icon-source` step | ✅ → ✅ | ✅ → ✅ | ✅ → ✅ |
| ↳ its `composition` step | n/a → n/a | n/a → n/a | ✅ → ✅ |
| `_validate_receipt.py` standalone | 1 → 1 | 1 → 1 | 1 → 1 |

`_validate_receipt.py` exits 1 on all three, before and after, for one reason:
`UNPROVEN:NO-RECEIPT`. None of the three carries a `#provenance-receipt`, and none did
before this lane. Standalone the gate always reds on that; chained inside `_validate_screen.py`
it downgrades to non-blocking, because every screen in this repo predates the receipt. Minting
receipts was not in scope and is not a lane's call.

Repo-wide, after: `_validate_kg.py` **0** (idempotent-clean) · `_validate_a11y.py` **0**
(136 snippets, 0 failures) · `_validate_icons.py` **0** (0 UNKNOWN) ·
`_validate_no_hardcode.py` **0** · `_validate_type_blast_radius.py` **0** ·
`_validate_theme_provenance.py` **0**.

⚠ Every `_validate_screen.py` run was redirected to `/tmp/l2/screen-gate` with `write_index`
stubbed out. **Nothing was written under `knowledge/_screen-gate/`** and `_SCREEN-GATE.md`
was not touched — the gate keys its record on basename and would have clobbered tracked files
belonging to other subjects.

---

## NOT DONE

1. **`_validate_compose.check_screen` does not strip CSS comments.** Real, one line, proven by
   mutation above. Not patched — a lane does not edit a gate to move its own subject, and the
   fix does not clear the subject anyway.
2. **Bento's 110 real hexes and its `c-bento*` second home stay.** Both declared; removing
   either is the "link canon.css vs. gate the copy" convention change the file itself puts to
   Dave. Left for him.
3. **No provenance receipts minted** for any of the three (all three were NO-RECEIPT before).
4. **The side-nav footer is not pinned** — it scrolls with `.sh-content`. Declared in the
   snippet and in the meta; pinning needs a second scroll container.
5. **Four-theme rendering was not driven**, because it cannot be from a snippet: no snippet
   links canon.css's AUTO-THEMES cascade. Answered at the token tier instead (§Themes
   verified), which is the strongest claim available without a convention change.
6. **Nothing committed, pushed, built or stashed.** `apollo-spider/skills/*`,
   `_validate_receipt.py` and the data-grid / filter-toolbar-bar / sidebar-nav metas were not
   touched — those are other lanes'.
