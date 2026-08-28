# `#221`-mono-specimen — the mono gallery default CANDIDATE, drawn for Dave's eye, nothing ruled

session: `#221` · 2026-08-27
window: mono-specimen lane — Dave's conditional sentence over the mono gallery default, s220-D2 (3)
EXPRESSLY OPEN and left that way
sub index: `mono-specimen`
tokens: `UNMEASURED` — a sub cannot read its own `message.usage`; the conductor's panel is the only
place this spend is real. Effort band: **M**.

## VERDICT

**DONE — BOTH PREMISES HOLD AT HEAD, and the page is a decision surface only.**
`reviews/MONO-GALLERY-DEFAULT-2026-08-27-v1.html` shows, light AND dark: **console's RULED default**
(rounded 20px image + transparent caption) beside the **MONO CANDIDATE** (square image — mono's own
radius token — + transparent caption, same colours) beside **MONO TODAY** (square + grey block).
Dave's sentence is quoted verbatim with both premise receipts beside it, each carrying a
**VERIFIED AT HEAD** chip that the build computes, never types. **No ruling, no default, no token,
no canon file, no `_rulings.json` was touched.**

Dave's sentence, verbatim, as briefed: *"there are no rounded corners in mono but I think they
share the same neutral ramp so the colours can be the same if this is true"* — conditional, and
the condition is met:

```
PREMISE A — shared neutral ramp        VERIFIED AT HEAD
  --color-neutral-5    light/dark   mono #313131 = console #313131   (supercharge #312C26 — the warm swap; mono is NOT on it)
  --background-default light/dark   mono #FFFFFF/#1A1A1A = console   (the token a transparent caption actually sits on)
  --text-secondary     light/dark   mono #1A1A1A/#FFFFFF = console   (the ink a transparent caption actually uses)
  CAPTION_GROUND_MINTS (mono,dark,darkgrey) and (console,dark,darkgrey) BOTH point at
  primitive color/neutral/5 / --color-neutral-5  (gen_bento_matrix_217.py:687–740)

PREMISE B — no rounded corners in mono  VERIFIED AT HEAD
  canon.css:20035  "Mono is the base (no block)"        — mono has NO theme override block at all
  canon.css:542    --border-radius-default: 0;           (the base every theme inherits)
  canon.css:546    --border-radius-container: var(--border-radius-default);
  canon.css:22162  --border-radius-container: 20px;      (inside [data-apollo-theme="console"] — the #199 override)
  resolved via matrix.theme_tokens():  mono 0 / 0  ·  console 20px / 20px  (both modes)
```

Measured **in the browser** on the finished page (probe banked, VERDICT GREEN):

```
con-light   imgR 20px · cap rgba(0,0,0,0) · ink rgb(26,26,26)     17.40:1
cand-light  imgR 0px  · cap rgba(0,0,0,0) · ink rgb(26,26,26)     17.40:1   ← identical colours, square corner
today-light imgR 0px  · cap rgb(240,240,240) · ink rgb(26,26,26)  15.27:1
con-dark    imgR 20px · cap rgba(0,0,0,0) · ink rgb(255,255,255)  17.40:1
cand-dark   imgR 0px  · cap rgba(0,0,0,0) · ink rgb(255,255,255)  17.40:1   ← identical colours, square corner
today-dark  imgR 0px  · cap rgb(31,31,31) · ink rgb(255,255,255)  16.48:1
```

The candidate's ink is asserted **equal to console's ink** in both modes (premise A on the pixels),
and its image radius **0px** (premise B on the pixels).

## COUNTS

new in-repo files `2` (generator + page) · build refusal guards in the generator `14` SystemExit
clauses · premise receipts rendered `6 token rows all SAME + 4 canon.css byte-receipts all PRESENT`
· browser-probe cards driven `6 trio + 8 strip = 14`, probe fails `0`, VERDICT `GREEN` · render
rounds `3`, each re-probed GREEN · widths rendered and SEEN `1180 + 480` · font probe `target 347 =
both aliases ≠ control 375 ≠ noface 301` · findings `7` · ruling-shaped `2` · UNPROVEN `3` ·
`.uuid` strays after render `0` · specimen files used `5`, all pinned s217-D1 names

## HOW THE PAGE IS BUILT (the method, briefly)

- **COPIED, not re-drawn.** Specimen markup + specimen CSS lifted from
  `showroom/_foundations/bento-rails.html` via the #220 banked source
  `notes/_subreports/assets/2026-08-27-220-default-switch/build.py.txt`, `.cdl-` chrome names
  carried with the copy. No git checkout anywhere.
- **No dial typed.** Console card reads `GALLERY_SETTINGS['console']`; mono TODAY reads
  `GALLERY_SETTINGS['mono']` (build refuses if it differs from `RECEIPT_ROLE_DEFAULTS` — expressly
  open means it must not have moved); the CANDIDATE is derived: mono today + exactly the ruled
  console dial pair. Build refuses if the candidate is more than one dial (`capBg`) from today.
- **Premises resolved, not quoted.** Both premise verdicts are computed through
  `gen_bento_matrix_217.resolve_token` / `theme_tokens` at build time; a failed premise renders a
  FALSE AT HEAD chip and the true numbers — the page cannot silently claim the condition.
- **Stale-artefact guards kept from the precedent:** console's enacted rules asserted byte-present
  in `showroom/_foundations/photography.html`; the s220-D1 caption mint asserted byte-present in
  `bento-rails.html`; two-red hexes refused in the output.
- **Photographs pinned by name** from `gen_bento_roles_217.read_photos()` (the ratified s217-D1
  set): `eyeem-100014108-…` for the trios; `gettyimages-1336692652`, `gettyimages-2190197969`,
  `gettyimages-1498039805`, `stocksy-6629948` for the four-more strip. Build refuses a name not in
  the pinned set. Alt text + licence come from the manifest rows, never typed.

## FINDINGS

1. **Premise A holds, and more strongly than stated:** not just the ramp — every token the
   transparent-caption treatment consumes (`--background-default`, `--text-secondary`) resolves
   **byte-identically** in mono and console, both modes. "The colours can be the same" is not an
   approximation; they are the same values.
2. **Premise B holds by construction:** mono is the base theme (no override block), so
   `--border-radius-container → --border-radius-default → 0`. The corner squares itself **through
   the very rule that rounds console's** — the candidate needs **no per-theme carve-out** and no
   new CSS.
3. **The candidate is ONE dial from today** (`capBg: grey → transparent`); `rounding` is already
   `corners` in mono. And it is **exactly console's ruled dial pair** — three themes would agree on
   the pair (legacy/supercharge already carry corners+transparent), with mono's token squaring it.
4. **The NOT-RULED status is machine-readable.** `chord_refusals('rounded','mono','gallery',…)`
   returns the X6 scope refusal — *"…it is not refused on taste, it is simply not ruled yet"* —
   **identically for mono's SHIPPED today-state and for the candidate**. So the chord layer is a
   console-scoped named bundle, not a state-legality law (the dial state itself passes P2/P3 and
   `transparent` is in mono gallery's reachable set `['grey','white','transparent']`). The page
   quotes the refusal verbatim as its own status; the build refuses if the symmetry ever breaks.
5. ⚠ **INHERITED CHROME DEFECT in the #220 banked source, repaired here, still live there:**
   `t-ed-heading-5` **does not exist in type.css** (headings run 1–4) and the source's table
   `<th>`/plain `<td>` carry no composite — with no base font-family on the page chrome, all of
   them fall to the browser serif. Seen in this page's own first render; repaired here
   (`t-ed-heading-4`, composites on cells). **`reviews/DEFAULT-SWITCH-2026-08-27-v1.html` shares
   the grammar and almost certainly renders its column heads and tables in the fallback serif** —
   out of this lane's region, NOT touched, conductor's call.
6. **`repeat(auto-fit, minmax(300px,420px))` counts repetitions by the definite MAX track size**
   (css-grid 7.2.3.2): at 1180 the copied pair grammar fits TWO tracks, so a trio wrapped 2+1 under
   itself. Seen in this page's first render; the trio now caps tracks at 348px (three fit; the
   wall stays under canon's 520px container band, ds-054 discipline preserved).
7. **Unclamped card labels break row scanning** — the strip's 2–4-line descriptions pushed cards to
   four different origins (the #220 ladder defect one level up). Clamped to 3 lines with a matching
   floor; panel origins now agree within 2px per row.

## RULING-SHAPED QUESTIONS

1. **The one word (Dave's, by design):** mono gallery default — the CANDIDATE (square image +
   transparent caption, console's colours) or TODAY (square + grey block), or neither? The page
   puts the three side by side in both modes; nothing was enacted.
2. **If the word is the candidate:** does the X6 rounded-chord scope extend to mono/gallery as part
   of the same word, and is the enactment the `role_defaults_219.py` supersession-layer shape (as
   console's was — receipt never edited)?

## REPLAY-THESE (conductor)

- The **premise-receipt block** in VERDICT above — it is the answer to "if this is true".
- Finding 4 (X6 fires identically for today and candidate) before wording any enactment.
- Finding 5 (the DEFAULT-SWITCH serif defect) — whether to regenerate that page is a conductor
  decision, not this lane's.

## UNPROVEN / CLAIMED (ADR-0016)

- **The DEFAULT-SWITCH page's serif rendering is INFERRED, not screenshot-proven on that page:**
  mechanism observed live on this page's copy of the same grammar + grep receipts
  (`t-ed-heading-5` absent from type.css; bare `<th>` in that page's HTML). That page was not
  re-rendered by this lane.
- **Strip row alignment is within 2px, not 0px** (2-line vs 3-line clamped labels round
  differently). Beneath the 1px keyline weight; not driven to zero.
- **Sandbox chromium only** — the page has not been seen in Dave's real browser; the
  Claude-in-Chrome fallback loop was not exercised.

## Fences honoured

No canon/token/generator-of-record edits · no defaults changed anywhere · `knowledge/_rulings.json`
untouched · no commits, no checkout, no push · region kept to `reviews/` + one new generator under
`knowledge/_render/` + this report + one banked probe asset. Render PNGs went to `outputs/`
(gitignored); TTF dir clean after render (`.uuid` count 0); `PYTHONDONTWRITEBYTECODE=1` kept
`__pycache__` out of the tree.

## Evidence

- **The page:** `reviews/MONO-GALLERY-DEFAULT-2026-08-27-v1.html` (53,460 bytes)
- **The generator (canonical home):** `knowledge/_render/gen_mono_gallery_221.py`
- **Browser probe (banked):**
  `notes/_subreports/assets/2026-08-27-221-mono-specimen/probe.py.txt` — run with
  `PYTHONPATH=/var/tmp/pylibs`, `LD_LIBRARY_PATH=/var/tmp/chromelibs-220/root/usr/lib/aarch64-linux-gnu`,
  `FONTCONFIG_FILE=/var/tmp/fonts-221m.conf` (the #138 symlink farm), shell
  `/var/tmp/pw-browsers-220/…/headless_shell`. ⚠ Environment note for the runbook's next reader:
  **`/var/tmp/chromelibs-s213e2` is HOLLOW in this sandbox too** (the #219 fifth-stratum shape);
  `/var/tmp/chromelibs-220` is intact and `ldd` reports 0 not-found with it.
- **Renders (outputs/, gitignored):** `mono221-1180.png`, `mono221-480.png`, crops
  `mono221-c0…c5`, `mono221-n2-trio.png` — all SEEN.
- **Premise sources:** `gen_bento_matrix_217.py:687` (`CAPTION_GROUND_MINTS`), `:628–682` (the
  neutral/5 calibration commentary and per-theme table), `canon.css:542/546/20035/22162`.

## USAGE

Effort band **M** (job-window tokens; sub spend excluded per s168-D2/D3). Three build+render+probe
rounds; two viewport widths; six crops read. `subs 0 tokens (n=0)` — this lane spawned no subs.
