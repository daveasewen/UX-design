# #292 lane H — the design-system map, in Apollo's Swiss idiom

Dave's ask, verbatim: *"I'd like to see a version of this diagram in our swiss style, anything that
we dont have currently we can fade and badge with 'coming soon'"*.

## WHAT LANDED

`notes/_lanes/292/H/design-system-map.html` — the reference poster's structure (twelve around one,
a ring of six words, a footer line) re-composed in the repo's own idiom. What changed, and why:

- **The ring became a rigid 4×4 grid.** The twelve tiles are the *perimeter* of that grid; the
  centre 2×2 is the hub. Twelve is exactly the perimeter count of a 4×4 with a 2×2 core, so the
  "twelve around one" reading survives with nothing placed by eye — every tile has a `grid-area`,
  numbered clockwise from top-left in the reference's own sequence.
- **The spokes became the grid's own gaps.** 1px gap on a rule-coloured background, cells opaque:
  the hairline structure *is* the drawing, not a layer on top of it.
- **The arrows became one 26px hairline tick** on each tile's inward edge — a stem, no arrowhead.
  Each tick is given its own inward margin (`padding: var(--s5)` on the facing side) so structure
  never sits on a line of type.
- **The icons are gone.** Index numeral + title carry the tile, per the skill's "typography carries
  the layout". No pastel fills; the only surface tint is `--color-grey-100` behind a faded tile.
- **The six ring words became a rule-separated mono strip** under the lockup — not text on a circle.
- **The hub is the masterbrand lockup** inlined from `knowledge/assets/logos/masterbrand-light-colour.svg`,
  with the wordmark re-bound to a `.wordmark` class so one lockup serves both themes (the dark master
  differs only in that fill). The hexagon's own red is brand, not accent.
- **Accent discipline:** the skill's ceiling is 2–3. Used twice — the eyebrow dash/label at the head,
  and the 2px rule under the lockup. Everything else is black and the neutral ramp.
- **Descriptions are Apollo's own words**, one line each, no marketing. The reference's copy was not
  carried across.
- **Every "have" tile cites one repo path in mono.** The citation is the claim and it can be opened —
  which is the point of the map: it is a *measurement* of the repo, not a wish list.

Renders: `notes/_lanes/292/H/design-system-map.png` (light, required) and
`-dark.png` (dark, cheap — one `data-theme` flip). Driver: `notes/_lanes/292/H/shoot.py`.
Probe: `notes/_lanes/292/H/measured.json`.

## MEASURED

### The have / coming-soon table

| # | Tile | State | Cited path | What was measured |
|---|---|---|---|---|
| 01 | Brand Standards | **HAVE** | `knowledge/guidelines/brand-principles.md` | plus `guidelines/logos.md`, `brand-refresh-assets.md`, and 8 lockup masters + 20 sized masters in `knowledge/assets/logos/` |
| 02 | User Research & Insights | **COMING SOON** | — | no research-practice file anywhere. `grep -ril "user research\|usability test\|participant"` over `knowledge/guidelines/` returns only `accessibility.md`, `accessibility-qa-cx-testing.md`, `neurodiversity.md` — i.e. testing *mentioned inside* a11y docs, never a research discipline of its own. No studies, no participants, no findings store. |
| 03 | Design Patterns | **HAVE** | `knowledge/components/template-report.meta.json` | 12 `template-*.meta.json` (auth, confirmation, create-edit, dashboard, dashboard-bento, detail, empty, error, list-index, report, settings, wizard); pattern vocabulary in `knowledge/components/_nodes-pattern.json`; bento generator `knowledge/canon/gen_canon_bento.py` |
| 04 | Tone of Voice | **HAVE** | `knowledge/guidelines/tone-of-voice.md` | the file exists and is in `guidelines/_rules-index.json` scope |
| 05 | Accessibility Standards | **HAVE** | `knowledge/_A11Y-GATE.md` | 9 `accessibility-*.md` guidelines + `digital-accessibility-standards.md`, `focus-indicators.md`, `neurodiversity.md`; gates `_validate_a11y.py`, `_validate_hit_area.py`, `_validate_state_contrast.py`; audits `_TEXT-CONTRAST-AUDIT.md`, `_SURFACE-CONTRAST-AUDIT.md`, `_ICON-CONTRAST-DELTA.md`, `_INDICATOR-CONTRAST-AUDIT.md` |
| 06 | Governance & Operations | **HAVE** | `knowledge/_rulings.json` | **622 rulings**, each with `id / ruled / date / by / says / governs / evidence / status / watch`; plus `_standing.md`, `_ENACTMENT-REGISTER.md`, `guidelines/digital-governance.md`, `guidelines/design-system-processes.md`, ~50 `_validate_*.py` gates |
| 07 | Data & Insights | **HAVE** | `knowledge/_INSTRUMENT-FIT.md` | `_context_gauge.py`, `_gauge_tokens.py`, `_KNOWLEDGE-USAGE-TRACE.{md,json,html}`, `_GRAPH-REPORT.md`, `_INTEGRITY-REPORT.md` — the system measuring itself. (Distinct from dataviz *rendering*, which sits under Components.) |
| 08 | Design Tokens | **HAVE** | `knowledge/canon/canon.css` | **12,061** custom-property declarations at `:root` depth; `knowledge/tokens/` with `_manifests`, `_raw`, `_proposals`, `_blast-radius.json`; gates `_validate_dtcg.py`, `_validate_token_tiers.py`, `_validate_token_forks.py` |
| 09 | Content Guidelines | **HAVE** | `knowledge/guidelines/copywriting.md` | plus `naming.md`, `calls-to-action.md`, `contextual-help.md`, `cookie-notifications.md`, `accessibility-content-authoring.md` |
| 10 | UX Principles | **HAVE** | `knowledge/_ux_principle_nodes.json` | **145 `ux:` nodes**, 53 `evidence:` nodes (crossref DOIs), 32 `family:`, 30 `polarity:`; `"ratified": "s281-D1"` |
| 11 | CX Principles | **COMING SOON** | — | absent from `guidelines/`. The only `cx` hit is `accessibility-qa-cx-testing.md` (a11y QA, not principles). `knowledge/_parked.json` carries a parked item whose due condition is literally *"Due when the CX principles arrive (guidelines/ moves)"* — so the repo already knows this is a gap, and it is parked, not declared out of scope. |
| 12 | UX Components | **HAVE** | `knowledge/components/` | **138 `*.meta.json`** component metas (142 files in dir, 4 non-meta), **139** `*.reference.html` builds in `knowledge/snippets/`, `_ACCESSIBILITY-CONFORMANCE.md`, `_STATES-COMPLETENESS.md` |

**Split: 10 have · 2 coming soon.** Coming soon: **User Research & Insights**, **CX Principles**.

### The render

Both renders clean, at 1440 @2x, full page, height 1680 CSS px:

| | light | dark |
|---|---|---|
| body background | `rgb(255,255,255)` | `rgb(16,16,16)` (`--color-grey-dark-mode-700`) |
| tiles measured | 12 (10 `have`, 2 `soon`) | same |
| clipped content, all tiles + hub | **0 px** | **0 px** |
| page errors | **none** | **none** |
| ring words | 6, one line, no wrap | same |

Typeface resolved to the real face: `"Univers Next HSBC", HSBC_MtUnivers_Latin, …`, fontconfig
reporting **10 HSBC faces / 404 total** (include live — the #138 shape checked, not assumed).

### Render-environment finding (worth carrying)

`knowledge/_render/seat_env.sh` **fails at this seat**, twice over, in the exact shapes its own
header documents:

1. `outputs/_render-env-229` — **absent**. `SEAT_ENV: FAIL envdir absent`.
2. `outputs/_render-env-231` (and `-230`) — `chromelibs/usr/lib/aarch64-linux-gnu` **hollow**.
   `SEAT_ENV: FAIL lib dir hollow or absent (fifth-stratum shape)`.
3. Their font farms are the **#238 third cause verbatim**: `outputs/_render-env-231/fonts/` holds
   10 symlinks, **0/10 resolve** here — every target is `/sessions/gifted-kind-allen/mnt/…`.

The lane rendered anyway because **the real faces are live in the repo** at
`knowledge/assets/fonts/_desktop/TTF/*.ttf` (10 files, `HSBC_MtUnivers_Latin-*`), and
`outputs/syslibs/usr/lib/aarch64-linux-gnu/libXdamage.so.1` supplies the one missing shared library
(`ldd … | grep -c "not found"` → **0** once it is on `LD_LIBRARY_PATH`). The farm was **copied, not
symlinked**, into `$TMPDIR/render-<seat>/fonts` — copies cannot dangle across seats, which is the
whole failure class. This is the seat-free half done from repo bytes rather than from a stored env
dir, and it worked first time.

## RULING-SHAPED QUESTIONS

Only Dave decides these. Nothing below was decided in-lane.

1. **Are the two faded tiles *planned*, or *out of scope*?** The map currently badges both
   "COMING SOON", which asserts intent. For **CX Principles** there is at least a parked item in
   `knowledge/_parked.json` pointing at it, so "coming" has some footing. For **User Research &
   Insights** there is nothing in the repo at all — it may be a genuine gap, or it may be something
   Apollo deliberately does not own (research being a practice, not an artefact store). If it is the
   latter, the badge should read differently, or the tile should not be on the map.
2. **Should a badged tile carry a date or an owner?** A badge with no date is a promise with no
   receipt, which is the shape `_standing.md` exists to prevent. Options: leave it bare, add
   "parked — `_parked.json`" for CX, or leave User Research unbadged-but-faded.
3. **Is "Data & Insights" the right reading?** The lane read it as *the system measuring itself*
   (`_INSTRUMENT-FIT.md`, the context gauge, the usage trace). The reference poster may have meant
   *product analytics about users* — which Apollo does **not** have, and which would move this tile
   to COMING SOON and change the split to 9/3. This is a definitional call, not a measurement.
4. **Does the hub title stay "Intelligent Design System"?** It is the reference's phrase, kept so
   the two posters can be read side by side. The strap beneath it is Apollo's own words.
5. **Do the twelve names stay the reference's?** "Tone of Voice" was shortened from "Tone of Voice
   Guidelines" to sit on one line; the other eleven are verbatim. If Apollo should name these in its
   own vocabulary (e.g. "Rulings" rather than "Governance & Operations"), that is a rename ruling.

## COUNTS:

- Tiles: **12** — **10 have**, **2 coming soon**
- Repo paths cited on the face of the poster: **10**, one per "have"
- Rulings measured: **622** (`knowledge/_rulings.json`)
- Token declarations measured: **12,061** (`knowledge/canon/canon.css`)
- Component metas measured: **138**; reference builds: **139**; page templates: **12**
- UX principle nodes measured: **145** (ratified `s281-D1`), evidence nodes **53**
- Guideline files measured: **63** in `knowledge/guidelines/`; accessibility guidelines among them: **10**
- Renders: **2** (light + dark), **0** clipped px, **0** page errors, **10/404** HSBC faces live
- Accent appearances on the page: **2** (label, hub rule) — skill ceiling is 2–3
- Files written by this lane: **5** (html, shoot.py, 2 png, measured.json) + this report
- Git: **untouched**, as instructed

## REPLAY-THESE:

The render env at this seat, in **one** bash call (seat-bound half regenerated, never reused):

```bash
cd /sessions/<seat>/mnt/UX-design
export TMPDIR=/dev/shm
SD=$TMPDIR/render-$(basename $(dirname $(dirname $PWD)))
rm -rf "$SD"; mkdir -p "$SD/fonts" "$SD/fccache"
cp knowledge/assets/fonts/_desktop/TTF/*.ttf "$SD/fonts/"      # COPY, never symlink
cat > "$SD/fonts.conf" <<EOF
<?xml version="1.0"?><fontconfig>
<cachedir>$SD/fccache</cachedir><dir>$SD/fonts</dir>
<include ignore_missing="yes">/etc/fonts/fonts.conf</include>
<alias><family>Univers Next HSBC</family><prefer><family>HSBC_MtUnivers_Latin</family></prefer></alias>
<alias><family>Helvetica Neue</family><prefer><family>HSBC_MtUnivers_Latin</family></prefer></alias>
</fontconfig>
EOF
export FONTCONFIG_FILE="$SD/fonts.conf"; fc-cache -f "$SD/fonts" >/dev/null 2>&1
fc-list | grep -c HSBC_MtUnivers_Latin      # ASSERT 10, and `fc-list | wc -l` must exceed it
export LD_LIBRARY_PATH="$PWD/outputs/syslibs/usr/lib/aarch64-linux-gnu:$LD_LIBRARY_PATH"
python3 notes/_lanes/292/H/shoot.py         # SAME call
```

Then:

- **Replay the measure** — every "have" in the table above is one `ls` / `grep -c` / `json.load` away.
  If a cited path has moved, the tile is lying and must be re-cited or re-badged.
- **Replay the split** — `python3 -c "import json;d=json.load(open('notes/_lanes/292/H/measured.json'));
  m=d['measured']['light'];print(m['have'],m['soon'])"` → `10 2`.
- **Re-render after any answer to the ruling questions** — a change to the split changes the masthead
  count (`IN REPO 10 / 12`) and the key block, both of which are hand-set in the HTML and will go
  stale silently. They are the one un-gated number on the page.
- **Carry the seat_env finding** into `knowledge/_RUNBOOK-render-verify.md` as a ninth stratum if the
  conductor agrees: *the stored env dirs are now 0/3 usable at a fresh seat, and the repo's own
  `knowledge/assets/fonts/_desktop/TTF` + `outputs/syslibs` are sufficient without them.* Not done
  in-lane — that file is a governing record and the edit is the conductor's call.
