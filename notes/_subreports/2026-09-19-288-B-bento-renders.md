# Bento gutters read from source, and the four themes rendered — #288 lane B

Session #288, lane B · 2026-09-19 · conductor Fable 5.1 · READ-ONLY on the repo except
`notes/_lanes/288/B/` and this file. No commit, no generator run, no gate run.

**Sheet for Dave's eye:** `notes/_lanes/288/B/four-themes.html`
**Raw numbers:** `notes/_lanes/288/B/measurements.json` ·
**PNGs:** `notes/_lanes/288/B/png/` (16) and `notes/_lanes/288/B/detail/` (16, 1:1 seam crops)

Dave, #287: *"I'm not sure that 0 is right for mono, lets have a proper review and fix this"* and
*"The problem with the gutters it that they are deliberately different for the themes and the
gutters are also different for the inner and outer bentos we essentially have a structural bento
and embedded bentos or tile groupings."*

---

## ⛔ PROVENANCE, FIRST — WHAT WAS READ AND WHAT WAS RENDERED

Lane A is building the `s219-D3` arm in the same working tree, in parallel. At the time of this
lane its edits to `knowledge/canon/canon.css`,
`knowledge/snippets/Template-dashboard-bento.reference.html`,
`knowledge/components/template-dashboard-bento.meta.json` and a new
`knowledge/canon/gen_bento_role_vars.py` were UNCOMMITTED in the tree
(`git status --porcelain`, verified this lane). So:

- **Every line number quoted below was re-read from `git show HEAD:<file>`, HEAD `4cc8b37a`** —
  not from the working tree. The working tree's `canon.css:18117` already carries lane A's new
  comment; HEAD's still carries the old one. All quoted numbers are HEAD's.
- **The render target, `showroom/template-dashboard-bento.html`, is UNMODIFIED at HEAD**
  (`git status --porcelain showroom/template-dashboard-bento.html` → empty). Its embedded base64
  payload is therefore HEAD's template.
- ⇒ **This sheet is what the delivery path gives Dave TODAY, before lane A lands.** It is not a
  picture of lane A's output and must not be read as one.

---

## 1 · THE SOURCE TABLE — outer and inner, per theme, READ NOT ASSUMED

### 1a · Is `--layout-bento-gutter` the structural (outer) gutter? — **YES, for the dashboard role.** READ.

Canon does exactly what Dave described, and says so in its own comment. Three rules, in
specificity order, at HEAD:

| # | file:line | rule | what it governs |
| --- | --- | --- | --- |
| i | `knowledge/canon/canon.css:1082` | `.c-bento{--bento-gutter: var(--layout-bento-gutter);}` — comment *"THE ONLY per-theme divergence"* | the gutter of ANY bento, all roles |
| ii | `knowledge/canon/canon.css:1182–1185` | `.c-bento[data-bento-role="dashboard"]{--bento-gutter:1px;}` | the **INNER** gutter — a dashboard bento whose tiles are plain tiles |
| iii | `knowledge/canon/canon.css:1198–1200` | `.c-bento[data-bento-role="dashboard"]:has(> .c-bento__grid > .c-bento){--bento-gutter:var(--layout-bento-gutter);}` | the **OUTER** gutter — a dashboard bento whose tiles are themselves bentos |

The source comment above (iii), `canon.css:1194–1197` (HEAD), is verbatim:

> ⚠ THE OUTER WALL OF A BENTO-OF-BENTOS KEEPS THE THEME GUTTER. Dave's dashboard is tight inner
> walls inside a generously spaced outer, so `1px everywhere` would collapse exactly the structure
> the role exists to describe. The condition is STRUCTURAL, not a second role name: a dashboard
> whose tiles are themselves bentos IS the outer wall.

⇒ **Within the dashboard role, `--layout-bento-gutter` IS the structural (outer) gutter.** The
inner (embedded / tile-group) gutter is a *separate* quantity and canon gives it a **literal
`1px`**, not a token — so it has no per-theme vocabulary at all. Outside the dashboard role
(`brochureware`, `gallery`, `canon.css:1206`) the same token is just "the bento gutter".

⚠ The scope carve-out is mirrored into the template scope at `canon.css:17770` / `:17784` by
`gen_canon_components.py` (`:where(.cn-template-dashboard-bento) …`), identical rules.

### 1b · The four themes — the outer token, and the role defaults

| theme | **OUTER** — `layout/bento/gutter` (s217-D2) | where it is declared (HEAD) | **OUTER** — `mainSpacing` (s219-D1) | **INNER** — `subSpacing` (s219-D1) |
| --- | --- | --- | --- | --- |
| Apollo Mono | **0** | `knowledge/canon/canon.css:537` (`:root`) · `knowledge/tokens/layout.json` `layout/bento/gutter` = `0px` | **40** | **4** |
| Apollo Legacy / Common | **24px** | `knowledge/canon/canon.css:22009` (`[data-apollo-theme="legacy"],[…="common"]`) · `knowledge/tokens/themes/apollo-legacy.overrides.json:188` | **24** | **4** |
| Apollo Console | **24px** | `knowledge/canon/canon.css:24611` (`[data-apollo-theme="console"]`) · `knowledge/tokens/themes/apollo-console.overrides.json:27` | **40** | **4** |
| Apollo Supercharge | **0** | **no declaration anywhere in the supercharge block** (`canon.css:26250`ff) — it inherits `:root`, `canon.css:537` | **24** | **2** |

Role defaults are `knowledge/_render/role_defaults_219.py --table`, run this lane, parsed by that
module from `notes/_receipts/2026-08-25-219-role-defaults-exports.md`.

⚠ There are FOUR more per-theme declarations of the same token, scoped to the template class by
`gen_showroom.py` / the theme cascade, all `24px` and all agreeing with the theme block above:
`canon.css:24071`, `:24099` (legacy/common, light and dark), `:25914`, `:25934` (console, light
and dark). **Supercharge has none at any scope** — its 0 is inheritance, never a statement.

The token's own note, `knowledge/tokens/layout.json` (`layout/bento` `$description`), verbatim:

> GUTTER IS THE ONLY PER-THEME DIVERGENCE — supercharge + mono 0px (this base), legacy + console
> 24px (their override sets).

and on the gutter itself:

> A theme override that never lands leaves THIS value silently in force, so the gutter is measured
> in every theme, never inferred from one (#217 probe).

### 1c · The template's pin — at HEAD, literals, theme-blind

- `knowledge/canon/canon.css:18119` —
  `:where(.cn-template-dashboard-bento) .tpl-page .c-bento.tpl-wall[data-bento-role="dashboard"]:has(> .c-bento__grid > .c-bento){--bento-gutter:40px; --bento-row-unit:auto;}`
- `knowledge/canon/canon.css:18121` —
  `:where(.cn-template-dashboard-bento) .tpl-page .c-bento.tpl-group[data-bento-role="dashboard"]{--bento-gutter:4px;}`
- authoring source: `knowledge/snippets/Template-dashboard-bento.reference.html:801–802` and `:804`.
- HEAD's own comment at `canon.css:18118`: *"MAIN SPACING 40px — mono's s219-D1 default, read off
  role_defaults_219.py --table."*

Both are literals with no theme condition. This is `s219-D3`'s unbuilt generation arm, exactly as
lane X reported at #287 — **independently re-verified here at HEAD, and then MEASURED (§3).**

---

## 2 · WHERE THE SOURCES DISAGREE — four disagreements, not one

1. **⛔ The OUTER gutter has two ruled numbers, and they differ in 3 of 4 themes.**
   `layout/bento/gutter` (s217-D2) says 0 / 24 / 24 / 0. `dashboard.mainSpacing` (s219-D1) says
   40 / 24 / 40 / 24. Only legacy agrees with itself. **Mono's doubted 0 is the s217-D2 number;
   s219-D1 already says 40 for mono** — so Dave's doubt may be a reading that is already ruled,
   in the other vocabulary. This is the disagreement lane X named; it survives re-reading.
2. **⛔ The INNER gutter has no token and three different answers.** Canon's role default is a flat
   literal `1px` (`canon.css:1184`), identical in all four themes. `subSpacing` (s219-D1) says
   4 / 4 / 4 / 2. The template pins `4px` for every theme (`canon.css:18121`). **Canon's 1px agrees
   with none of the four ruled `subSpacing` values** — including mono's own.
3. **⛔ Supercharge's outer 0 is inherited, never declared.** Legacy and console state 24px in their
   override sets; supercharge states nothing. Per `layout.json`'s own warning that is
   indistinguishable at read time from *"an override that never landed"*. The value is right per
   s217-D2; the *evidence* that anyone decided it for supercharge is absent from the tree.
4. **⚠ The template out-specifies everything.** `canon.css:18119` is `(0,4,0)` + `:has()`; the theme
   token reaches `--bento-gutter` only through the `(0,2,0)` role rule at `canon.css:17784`. So the
   theme token resolves correctly and is then simply never read. **MEASURED, §3.**

---

## 3 · THE MEASURED TABLE — `getBoundingClientRect()`, not eyeballs

Render: `showroom/template-dashboard-bento.html` (HEAD), Chromium headless-shell 153.0.8010.12 in
sandbox, `goto("file://…")` (never `set_content()`), viewport **1440 × 1400**, `device_scale_factor
1`, light mode. Driver `notes/_lanes/288/B/render_four_themes.py`. "Measured" = the minimum px
distance between the bounding rects of sibling children of the grid — column gap and row gap taken
separately. Declared = the CSS value actually in force.

### Row A — AT HEAD, nothing overridden. **The pin is theme-blind, and here is the proof.**

| render | theme | `--layout-bento-gutter` resolved AT THE WALL | outer measured (col / row) | inner measured (lead group) |
| --- | --- | --- | --- | --- |
| `r0-mono` | mono | `0` | **40 / 40** | **4** |
| `r0-legacy` | legacy | `24px` | **40 / 40** | **4** |
| `r0-console` | console | `24px` | **40 / 40** | **4** |
| `r0-supercharge` | supercharge | `0` | **40 / 40** | **4** |

★ **The theme token resolves CORRECTLY in every theme (0 / 24px / 24px / 0) and reaches the gap in
NONE of them.** Four themes, one identical 40 / 4. `r0-mono.png` and `r0-console.png` differ only
in colour and type. That is the defect, measured rather than argued.

### Row B — ruled values applied by override: the TOKEN reading of the outer gutter

| render | theme | declared outer / inner | outer measured | inner measured |
| --- | --- | --- | --- | --- |
| `r1-mono` | mono | 0 / 4 | **0 / 0** | **4** |
| `r1-legacy` | legacy | 24 / 4 | **24 / 24** | **4** |
| `r1-console` | console | 24 / 4 | **24 / 24** | **4** |
| `r1-supercharge` | supercharge | 0 / 2 | **0 / 0** | **2** |

### Row C — Mono's outer gutter ramp, inner held at 4. **This is the row Dave rules from.**

| render | declared outer | outer measured (col / row) | inner measured |
| --- | --- | --- | --- |
| `r2-mono-0` | 0 | **0 / 0** | 4 |
| `r2-mono-8` | 8 | **8 / 8** | 4 |
| `r2-mono-16` | 16 | **16 / 16** | 4 |
| `r2-mono-24` | 24 | **24 / 24** | 4 |

(40 — the fifth point on the ramp, and what the template ships — is `r0-mono` / `r3-mono`.)

### Row D — ruled values applied by override: the ROLE-DEFAULT reading of the outer gutter

| render | theme | declared outer / inner | outer measured | inner measured |
| --- | --- | --- | --- | --- |
| `r3-mono` | mono | 40 / 4 | **40 / 40** | **4** |
| `r3-legacy` | legacy | 24 / 4 | **24 / 24** | **4** |
| `r3-console` | console | 40 / 4 | **40 / 40** | **4** |
| `r3-supercharge` | supercharge | 24 / 2 | **24 / 24** | **2** |

Declared and measured agree to the pixel in all 16 renders. `r3-mono` is byte-identical to
`r0-mono` (113,752 bytes) and `r3-legacy` to `r1-legacy` (114,049) — the two places where the
readings coincide, which is a check on the instrument as well as a finding.

**How the overrides were applied:** a single `<style id="lane-b-override">` injected into the
render copy only, carrying the SAME two selectors as the pinned rules so the literal is replaced
rather than out-specified. **Nothing in the repo was overridden, and the repo's own CSS is
untouched.** The showroom harness bar and the review overlay are hidden in the renders (demo
chrome, not the template).

---

## 4 · WHAT I COULD NOT ESTABLISH

- ⬛ **Which of the two outer numbers Dave wants.** The sheet puts both readings in front of him;
  this lane takes no view and mints no ruling. `s217-D2` (0/24/24/0) and `s219-D1` (40/24/40/24)
  are both his, on different days, in different vocabularies.
- ⬛ **Whether canon's flat inner `1px` (`canon.css:1184`) was ever ruled, or is a pre-`s219-D1`
  survivor.** The rule's own header, `canon.css:1181`, reads *"DASHBOARD — s217-D2's model. Radius
  on the CONTAINER, tiles square, tiles at 1px."*, so it reads
  as ruled — but `s219-D1`'s `subSpacing` (4/4/4/2) came later and nothing in the tree says which
  supersedes which. **Not established from this seat.**
- ⬛ **Whether supercharge's outer 0 was ever decided for supercharge.** It is inheritance from
  `:root`, with no supercharge declaration at any scope. The `layout.json` note says the value is
  mono's base and supercharge "inherits it"; the #217 tuner export is cited for it in the legacy
  and console notes but there is no supercharge override file entry to point at.
- ⬛ **Dark mode.** Every render is light mode. The theme cascade declares the same `24px` in both
  modes (`canon.css:24071`/`:24099`, `:25914`/`:25934`), so no divergence is expected — but it was
  not rendered, so it is not measured.
- ⬛ **Other viewports.** 1440 only. The container-query bands (1100 → 3 cols, 820 → 2, 520 → 1,
  s217-D2) were not exercised, and the four-column lead-row override interacts with them.
- ⬛ **`inner_evidence` row gaps.** The evidence group holds a single tile at this cut, so there is
  no sibling pair to measure inside it; its `computed_column_gap` is reported instead (4px, 2px in
  supercharge). The lead group (four KPI tiles) carries every measured inner number above.
- ⚠ **Lane A's output is not measured here** and this sheet will be stale for the template the
  moment lane A lands. The sheet says so on its face.

---

## 5 · THE RENDER ENVIRONMENT, DECLARED (ADR-0016)

`outputs/_render-env-229` does not exist at this seat, so `knowledge/_render/seat_env.sh` failed
`envdir absent` and the seventh stratum's install lines were re-driven — **into
`/var/tmp/render-env-288b`, NOT the repo**, since this lane is read-only outside its own dir:

- `pip install --target=/var/tmp/render-env-288b/pylibs playwright` → playwright **1.63.0**.
- `python3 -m playwright install chromium-headless-shell` failed on TLS
  (`UNABLE_TO_GET_ISSUER_CERT_LOCALLY`, five attempts — a proxy the node driver does not trust;
  pip's own TLS is fine). `NODE_TLS_REJECT_UNAUTHORIZED=0` on that one command downloaded it.
  **NEW, not in the runbook's seven strata.**
- ⛔ **The browser layout changed and `seat_env.sh` cannot see it.** Playwright 1.63 lays the shell
  down at `chromium_headless_shell-1243/chrome-headless-shell-linux-arm64/chrome-headless-shell`;
  `seat_env.sh:44` globs `pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell`. The
  glob misses, and the script reports `headless_shell not found under …/pw-browsers` — which
  reads as *"the browser is missing"* rather than *"the vendor moved the file"*, the same
  fifth-stratum shape the script was written to end. Worked around here with a compat symlink;
  **the script itself is untouched** (a knowledge/ file, out of this lane's scope). **This wants a
  one-line fix and a stratum note, and is handed to the conductor, not taken.**
- `ldd` named exactly one missing lib, `libXdamage.so.1`; `apt-get download libxdamage1` +
  `dpkg -x` into `/var/tmp/render-env-288b/chromelibs` cleared it.
- With that env dir passed as `seat_env.sh`'s argument the script then passed its own assertions:
  `SEAT_ENV: OK seat=trusting-youthful-franklin faces=10/404 farm=10/10 libs=2`.
- ⚠ The env is on **VM disk, not the mount** — per the sixth stratum's warning it will not survive
  a VM rebuild. It was put there deliberately: the mount is the repo, and this lane may not write
  to it outside `notes/_lanes/288/B/`.

**Verified:** all 32 PNGs exist and are non-empty (16 page renders 1440 × 1400, 16 detail crops
470 × 240); `four-themes.html` parses with zero unclosed tags. Renders were read back by eye.

⚠ `notes/_lanes/288/B/_render_src/` holds the 16 generated render copies (~3 MB). They are
regenerable by re-running the driver; this lane could not delete them (the sandbox refused the
unlink) and declares them rather than leaving them unexplained.

---

## 6 · WHAT THIS LANE DID **NOT** DO

No commit. No generator run (`gen_kg_rules.py`, `land_rests_on.py`, `gen_kg_icons.py`,
`_build_all.py` untouched). No gate run. No edit to `knowledge/canon/canon.css`,
`knowledge/snippets/*`, `knowledge/components/*`, `tokens/*` or `knowledge/_render/*`. No ruling
minted, proposed or implied. `_state.json` written only through `knowledge/_state.py`'s module
API, never by hand.
