# #261 — component lane brief (shared, read before you build)

Five parallel Opus lanes. One component family each: **kpi-tile** · **grid header** (`data-grid`/`table`) ·
**filter-toolbar-bar** · **nav family** (`sidebar-nav`/`navigations`/`tab-bar`) · **footer**.
⚠ `knowledge/components/footer.meta.json`, `knowledge/snippets/Footer.reference.html` and
`showroom/footer.html` ALREADY EXIST — the footer lane is a REDESIGN, not a new component. Say so before you build.

## 1. Anatomy of a shipped component

| Layer | Path | Owner |
|---|---|---|
| Meta (source of truth) | `knowledge/components/<slug>.meta.json` | hand-authored |
| Reference snippet | `knowledge/snippets/<Capitalised-slug>.reference.html` (single self-contained HTML) | hand-authored |
| Showroom page | `showroom/<slug>.html` + `showroom/_thumbs/<slug>.png` | GENERATED — `python3 knowledge/gen_showroom.py` |
| Library index | `showroom/index.html` + `index.json` | GENERATED — `knowledge/_render/gen_library_214.py` (s215-D5: NOT gen_showroom) |
| Role registry | `knowledge/roles.json` (12 roles, s252-D1) — a component either `provides` a role or is listed under `$not-a-provider` | hand-authored |
| Partial/behaviour registry | `knowledge/component-types.json` → `component-type/<group>/$members` + `$partials` + `$behaviour` — ONLY if it consumes an injected partial or JS (groups today: `button-family`, `dataviz`, `segmented`) | hand-authored |
| Type binding | append your selector to the `.t-cm-*`/`.t-ed-*` list in `knowledge/canon/type.css`, then record blast radius in `knowledge/canon/_type-bindings.json` | hand-authored |

**Meta key list, verbatim from `knowledge/components/kpi-tile.meta.json`:**
`name, category, $status, $floated, purpose, provides, answers, shape, span, priority, when, with, not-with,
$differsFromStatCard, props, variants, slots, tokens, $finding-two-seats, relationships, accessibility,
antiPatterns, tokenValidation, provenance, interactive, stateModel, responsive, dimensions, edges`

**Snippet template — first 20 lines of `knowledge/snippets/Kpi-tile.reference.html`:** `<!DOCTYPE html>` ·
`<html lang="en">` · `<head>` · charset · viewport · `<title>KPI tile — reference implementation (PROPOSED #203)</title>`
· then an HTML comment block that states STATUS (`PROPOSED`/gated), the session, and the ruling that governs it,
quoting Dave verbatim. Copy that shape: **title line names the component and its status; the first comment is provenance.**
The document then carries its own `[data-theme]` toggle, CSS vars = resolved token values, a live variant/state
spread, and the embedded `#token-manifest` JSON (`vars` / `contrastPairs` / `requiredAria`) — that manifest IS the
proof-of-done. Full procedure: `knowledge/_RUNBOOK-gated-component.md` (read it; do not re-derive).

⛔ `_validate_coverage.py` fails if a meta has no snippet whose manifest `component` matches its `name`, or a
snippet names a component with no meta. Meta and snippet ship together or not at all.

## 2. How a NEW component is registered end-to-end — what #260 did (`git show --stat 9a702b5`)

`#260 I: eight fast-follower chart types on the engine (s259-D1)` — 38 files, +8173/−476. File types touched:

1. **registry** — `knowledge/component-types.json` (+104) — the `$members`/`$partials`/`$behaviour` rows.
2. **partials / engine JS** — `knowledge/canon/dv-render-<type>.js` ×6 (new files).
3. **metas** — `knowledge/components/Chart-<type>.meta.json` ×8 (+ `chart-pie`).
4. **snippets** — `knowledge/snippets/Chart-<type>.reference.html` ×8.
5. **test pages** — `knowledge/_tests/chart-engine/<type>.html` ×7 (the driven-receipt surfaces).
6. **the gate itself** — `knowledge/_validate_dataviz.py` (+136) when new types need new checks.
7. **gate reports (regenerated, always dirty)** — `_A11Y-GATE.md`, `_BEHAVIOUR-GATE.md`, `_DATAVIZ-GATE.md`.
8. **lane subreports** — `notes/_subreports/2026-09-08-260-F<n>-*.md` ×4.

Showroom pages were NOT in the commit: they are generated. Run `python3 knowledge/gen_showroom.py` and commit the
generated `showroom/<slug>.html` with your files; `--check` is the build gate. Prior-art lane pack:
`notes/_lanes/260/_LANE-BRIEF-fast-follower.md`, `notes/_lanes/260/<type>.registry.json`.

## 3. Gates — commands, and what runs in this sandbox

RUNS HERE (verified today, all green on `master`):

```
python3 knowledge/_validate_snippets.py        # 136 snippets, 0 failures — token fidelity, ARIA,
                                               # contrast, no ALL-CAPS, :focus-visible, no italics/
                                               # text-shadow/raw brand-red text, copy-lint
python3 knowledge/_validate_behaviour.py       # ADR-0015: MAX_BYTES 16,384 per source,
                                               # PAGE_BYTES 34,816 per page (s250-D1, CODE-ONLY
                                               # bytes); bans setInterval, fetch/XHR/WS, JS scale-
                                               # physics; EXACTLY ONE rAF-debounced resize listener;
                                               # no external <script src> in a snippet
python3 knowledge/_validate_dataviz.py         # charts only — figure.dv contract, dv-table spine,
                                               # dv-legend, zero baseline, dv-004 separation
python3 knowledge/_validate_screen.py [--render] [path…]   # composed screens (*.canon.html):
                                               # receipt → compose → composition → icon-source → a11y
```

⛔ DO NOT run `knowledge/_build_all.py` (session standing instruction).

NEEDS CHROMIUM (Playwright): `_validate_hit_area.py`, `_validate_state_contrast.py`, `_validate_screen.py --render`,
`_validate_fit_physics.py`, `_validate_descender_computed.py`, `_validate_wiring.py`, `_drive_chart_engine.py`.
Exit code **77 = COULD-NOT-ASK** (harness unavailable) — that is a REFUSAL, never a pass. Never `set_content()`;
`goto file://…` only (`knowledge/_RUNBOOK-render-verify.md`).

**Chromium install recipe (lane D3 used it today; docstring of `knowledge/_drive_chart_engine.py`, confirmed at
`notes/_subreports/2026-09-08-261-D3-driver-scope.md:102-106`):**
```
pip install playwright --break-system-packages
playwright install chromium
apt-get download libxdamage1 …        # then: dpkg-deb -x <deb> <prefix>
export APOLLO_PW_LD_LIBRARY_PATH=<prefix>/usr/lib/x86_64-linux-gnu   # the script adds it to LD_LIBRARY_PATH
```
**Touch targets** — `_validate_hit_area.py`: controls 44px (HSBC default / WCAG 2.5.5 AAA), **dial-down floor 24px,
never below**; data marks held to 24×24 (s116-D1). Below 24 = `BREACH-FLOOR`.

**FOUR THEMES × TWO MODES — test every one.** Themes are the `[data-apollo-theme]` slots in
`knowledge/canon/canon.css`: `legacy` (aliased `common`), `console`, `supercharge`, and **mono** (the base — no
`data-apollo-theme` attribute / empty override set). Modes are `[data-theme="light"|"dark"]`. Drive them by setting
`html[data-apollo-theme]` + `body[data-theme]` — exactly what the showroom harness and `_drive_chart_engine.py` do
(`per page × 4 themes (mono, legacy, console, supercharge) × 2 modes`). Link your snippet to the cascade with
`data-apollo-theme` on the root and re-project your manifest vars via `gen_theme_cascade.snippet_theme_css()`.

**TWO-RED LAW (s151-D1 / s134-D5):** minus/red is `#DA1A00` on light grounds (4.503 on #F1F1F1) and `#F6604C`
everywhere else (4.763 on #272727). Plus/green pairs with it: `#137F3C` light / `#66CC8D` dark. Plus/minus numerals
are the ONLY coloured text Apollo uses. On a rag-tinted ground the ruled treatment is `#1A1A1A` glyph ink, not the
coloured rung (s134-D4). RAG FILLS are mode-invariant (dark = light).

## 4. Design rules

- **Type**: `knowledge/canon/type.css` — hand-authored. Editorial `.t-ed-display-1/2`, `.t-ed-heading-1..4`,
  `.t-ed-body` (16/24), `.t-ed-body-small` (14/20), `.t-ed-caption` (12/16); Component `.t-cm-*` keep TYPE and BOX
  separate (T-D12). Bind by APPENDING your selector to the composite's selector list — no generator, no markup
  change. **Load order is load-bearing: type.css BEFORE component CSS.** Gated by `_validate_type_composites.py`.
  No light/ultra weights on body sizes (font-5/6/7 min 400). `--uf` is the family var.
- **Tokens**: `knowledge/canon/canon.css` + `knowledge/tokens/semantic-colour.json`. Resolved SEMANTIC tokens only,
  never invented hexes; prefer semantic over primitive; `_validate_no_hardcode.py` / `_validate_palette_tier.py` bite.
- **Spacing/grid**: leading-trim is ON, so **every vertical stack needs an explicit tokenised gap**
  (`gap/fixed/content` = 2/4/8/12px) — never rely on line-height. Body copy keeps `text-box-trim:normal`;
  truncating labels use `text-box-edge:text text`. Square corners except Badge + Avatar.
- **Rulings that govern `knowledge/components/**` (grep `governs` in `knowledge/_rulings.json`):**
  1. `s234-D4` — grouping lives once in the KG; a typed `groupsWith` edge in the meta schema is its home.
  2. `s234-D5` — the behaviour address is BOTH, one generated: the meta owns the declaration.
  3. `s245-D1` — `behaviour.script` grammar is (a) PATH + FRAGMENT, with the foreign refusal.
  4. `s245-D2` — `behaviour.partial` is `string | string[] | null`, widened by addition.
  5. `s245-D3` — a PROSE `behaviour` value BLOCKS the gate.
  6. `s245-D4` — `behaviour.events` is optional and GENERATED from the snippet, never authored.
  7. `s245-D5` — `behaviour.fallback` is settled by a JS-off render, not by a reading.
  8. `s245-D7` — the composition edge takes all L3 recommendations; C9 span legality BLOCKS, C1/C7/C8/C4 advisory.
  9. `s248-D3` — an edit mode is coming: every component placed in a bento tile MUST be responsive.
  10. `s251-D4` — an interchangeability grade is the four-word ladder: drop-in / same-shape / same-answer / similar.
  11. `s251-D5` — an edge's `when` is a C9-readable PREDICATE over shape, prominence and span, not prose.
  12. `s251-D6` — reciprocal edges are DERIVED; author one direction only.
  (KPI lane also: `s246-D5` DP-06 four-compact-tile row is the shipped default, 2×2 removed; `s247-D3`; and
  `s182-D2`, which FLOATS the kpi-tile component itself — ⛔ never launder it into a ruling.)
- **`knowledge/_COMPONENT-GAPS.md` open rows (all 6, none closed):** Modals — true modals + lightboxes, desktop and
  mobile · Confirmation/success — desktop variant · Links — external/new-window variant (aca-006, ruled IN the
  Links ★ pass) · Inverse/hero surface — no light-mode dark-band role · Data-viz palette (largely closed by
  #259/#260) · Register/craft tokens — no global elevation/gradient ramp.

## 5. Git hygiene TODAY

- `.git` forbids `unlink`. If `index.lock` / `HEAD.lock` / `refs/heads/master.lock` appear stale,
  **`mv` them into `.git/orphan-locks-261D3/` — never `rm`.** First commit of the session, call
  `mcp__cowork__allow_cowork_file_delete`; if granted the dance is unnecessary (`knowledge/_RUNBOOK-git-commit.md` step 0).
- Commit via `bash knowledge/_git_commit.sh --reconciled <msgfile>` and READ THE MESSAGE BACK.
- ⛔ never `git stash` · ⛔ never `git checkout` another lane's files (two lanes wiped each other this way at #253)
  · commit ONLY your own files · subject prefix `#261 <lane>:` · **do not push.**
- Gate reports (`_A11Y-GATE.md`, `_BEHAVIOUR-GATE.md`, `_DATAVIZ-GATE.md`) are rewritten by every gate run and will
  be dirty outside your fence — absorb, do not go red on them.
- Lane fragments → `notes/_lanes/` ONLY, never `knowledge/_tmp/`. Report to
  `notes/_subreports/2026-09-08-261-<lane>-<topic>.md`, ≤60 lines.

## 6. Wiring — cross-component JS is now ALLOWED

`s258-D1`, ruled verbatim: *"Rule 2a of ADS-generate-from-canon ('Copy the script address with the markup; author
no JS') is REMOVED. The author MAY write JavaScript - cross-component wiring (filter->grid/KPI/chart, nav
state->storage) and beyond; Dave wants the creativity, not only the wiring."*

`s258-D2`, ruled verbatim: *"Builds are AMBITIOUS BY DEFAULT: every interactive element on a generated page is
assumed to work; generated mock data is rich and deep (entities, currencies, time series, relationships) so that
behaviours and interactions have something to act on. Writing code is an avenue to innovation - the interface is
tied down, the code is not."*

So: wire filter-toolbar-bar → grid/KPI/chart, and nav state → storage. Stay inside the behaviour gate —
16 KB code-only per source, 34,816 bytes per page, no `setInterval`, no network, one rAF-debounced resize listener,
and no external `<script src>` in a snippet.
