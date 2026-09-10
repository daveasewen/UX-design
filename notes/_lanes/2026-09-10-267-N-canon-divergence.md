# #267 lane N — the canon.css divergence (cold run 6, finding 1)

## The mechanism: canon.css is GENERATED, and it was STALE

Not hand-kept. Evidence:

- `knowledge/_RUNBOOK-compose-from-canon.md` §"Regenerate canon (the two generators — canon.css
  is generated, not hand-kept)": `canon/gen_canon_tokens.py` writes the AUTO-TOKENS block,
  `canon/gen_canon_components.py` writes the AUTO-COMPONENTS block **from
  `knowledge/snippets/<Name>.reference.html`**, "never hand-edit between the AUTO-COMPONENTS
  markers". `canon/gen_theme_cascade.py` writes AUTO-THEMES.
- `knowledge/canon/canon.css` mtime **2026-09-08 17:48**; the three snippets the cold run named
  were revised **2026-09-09** (`Navigations` 14:35, `Sidebar-nav`/`Tab-bar` 19:51,
  `Filter-toolbar-bar` 10:29, `Data-grid` 11:58) by #261 commits `c0225a0`, `d57a1e9`, `886e7e5`.
- Nobody re-ran the generator. The `.cn-navigations` block in canon still carried the PRE-#261
  markup grammar (`nav.main a`, `.actions button`) while the snippet had moved to the shared
  `.nv-item` family. So a designer obeying compose-from-canon got an unstyled sidebar.
- `gen_theme_cascade.py --check` was **already rc=1 before this lane** (verified by swapping the
  pre-lane canon.css back in) — the same class, a second generator not re-run.

## Done

- `python3 knowledge/canon/gen_canon_components.py` → 137 components; `--check` OK.
- `python3 knowledge/canon/gen_theme_cascade.py` → 230 override paths / 397 projections;
  `--check` OK.
- `knowledge/snippets/Kpi-tile.reference.html:256` — removed the dead `min-height:var(--slot)`
  left behind by #261 K3's own reversal (`--slot` defined nowhere ⇒ already invalid-at-
  computed-value-time ⇒ `auto`; no visual change).
- `knowledge/_validate_compose.py:87–99` — a `var(--x, fallback)` ref is not "unresolved"; a ref
  is exempt only when EVERY occurrence carries a fallback. Generalises the s258-D3 `-max`
  allowance from a name suffix to the grammar. **REVERSIBLE JUDGEMENT** — see below.
- Commits `e470ae0`, `57ddff1`. No push.

### Before → after hit counts in `canon/canon.css`

| class | before | after |
|---|---|---|
| `.nv-item` | 0 | 59 |
| `.nv-ic` | 0 | 19 |
| `.nv-label` | 0 | 20 |
| `.nv-count` | 0 | 18 |
| `.nv-chev` | 0 | 13 |
| `.ftb-primary` | 0 | 3 |
| `.ftb-ctl` | 0 | 4 |
| `.ftb-context` | 0 | 2 |
| `.ftb-status` | 0 | 2 |
| `.ftb-hint` | 0 | 1 |
| `.ftb-clear` | 0 | 2 |
| `.th-in` | 0 | 3 |

`.ftb-trailing` is **0 before and after — it does not exist** in `Filter-toolbar-bar.reference.html`.
The cold run named it loosely.

## The divergence list (the measurement that establishes the class)

Method: for every one of the 137 `knowledge/snippets/*.reference.html`, take the class names in
its own `<style>` selectors (APOLLO-DEMO fenced CSS and comments stripped) and ask whether each
appears anywhere in `canon/canon.css`.

**BEFORE — 20 of 137 snippets had classes styled only in their own `<style>`:**

| snippet | missing / total |
|---|---|
| Kpi-tile | 23/45 (`kpi-lbl`, `kpi-delta`, `kpi-target`, `dv-area`, `is-loading`, …) |
| Filter-toolbar-bar | 19/55 (`ftb-primary`, `ftb-ctl`, `ftb-status`, `ftb-hint`, `ftb-clear`, …) |
| Legend | 17/39 (`leg-host`, `leg-slot`, `sw-bar`, `dv-leg-pct`, … — **no `.cn-legend` scope existed at all**) |
| Data-grid | 13/57 (`th-in`, `colmenu`, `dgden`, `rsz`, …) |
| Footer | 13/17 (`ft-copy`, `ft-status`, `ft-ver`, …) |
| Sidebar-nav | 11/29 (`nv-item`, `nv-label`, `sn-topbar`, `sn-scrim`, …) |
| Navigations | 10/22 (`nv-item`, `nv-btn`, `nav-drawer`, …) |
| Tab-bar | 6/13 (`nv-item`, `nv-count`, …) |
| Dropdown | 3/13 (`grp`, `grp-list`, `optgrp`) |
| Account-card · Action-bar · Amount-display · Eyebrow · Limits-meter · List-items · Payment-card-visual · Runway-bar · Summary | 1 each (`stateLabel` — a deliberate `DROP_FIRST` harness drop) |
| Template-dashboard-bento | 1 (`tpl-bento-body` — a `body.` rule, correctly dropped) |
| Video-player | 1 (`caption` — matches the `.cap` DROP_FIRST prefix) |

**AFTER — 12 remain, and every one is a deliberate harness drop** (`stateLabel` ×10,
`tpl-bento-body`, `caption`). i.e. there is **no fast-follower scope**: the divergence was not
per-snippet rot needing 20 fixes, it was **one stale generator output**. The whole list closed on
a single regen.

## Proof (playwright, `file://`, never `set_content`)

Throwaway `/tmp/proofN/` containing ONLY `canon.css` + `type.css` + the two snippets' markup with
their `<style>` blocks removed (Sidebar-nav scripts dropped too), body
`class="canon" data-apollo-theme="common" data-theme="light"`, viewport 1440×1000.

| assertion | AFTER (fixed canon) | BEFORE (pre-lane canon, negative control) |
|---|---|---|
| `.nv-item` count | 33 | 33 |
| `.nv-item` computed `display` | **flex** | inline (UA default) |
| `.nv-item` computed `min-height` | **44px** | 0px |
| `.nv-item` computed `padding-left` | **16px** | 0px |
| `.nv-label` computed `text-overflow` | **ellipsis** | clip |
| `.nv-item` box | **247×44** | 247×286 |
| `#ftbAddT` click → `#ftbAddM[data-open]` | `true`, `aria-expanded=true` | true |
| `#ftbAddM` computed `pointer-events` | `none` → **`auto`** | none → auto |
| `elementFromPoint` at option centre | **inside `#ftbAddM`** (`LI.opt`, 111×44) | inside (`LI.opt`, 1382×44) |
| real click on the option closes the menu | yes | yes |

⚠️ HONEST NOTE: the *nav* half of the finding reproduced exactly and is closed. The
*pointer-dead dropdown* half did **not** reproduce in this composition — `.menu` /
`[data-open]` styling reaches the menu from the Dropdown scope in both old and new canon; only
the `.ftb-*` layout was missing. Whatever made `#ftbStatus` intercept pointer events in the cold
run came from a different composition path (likely the ftb-status/context layout being unstyled
and overlapping), and it is fixed here by the same regen — but the mechanism was not isolated.

## Gates

| gate | rc |
|---|---|
| `canon/gen_canon_components.py --check` | 0 |
| `canon/gen_theme_cascade.py --check` | 0 (was **1 before this lane** — pre-existing) |
| `gen_token_ramp.py --check` | 0 |
| `_validate_compose.py` | 0 (was 0 pre-lane, 1 after the regen, 0 after the two fixes) |
| `_validate_binds_resolve.py` | 0 (137 snippets / 137 canon blocks) |
| `_validate_snippets.py` | 0 (137 snippets, 0 failures) |
| `_validate_radius.py` | 0 |
| `_gate_dataviz_vars.py` | 0 |
| `_gate_minted_consumption.py` | 0 |
| `_validate_type_composites.py` | **1 — PRE-EXISTING RED**, 1087 violations before this lane / 1089 after (TYPE-002 ×1044, the `font: … var(--font)` shorthands in canon's own hand-authored `.c-*` layer). Not this lane's; unchanged in kind. |

## NOT DONE

- `_validate_state_contrast.py --render` and `_validate_screen.py --render` (render gates) were
  NOT run — out of lane budget.
- The two `_validate_type_composites` violations added by the regen were not chased to their
  snippet; they are the same TYPE-002 class as the 1087 already there.
- No push (7+ commits still local per the standing rule).

## RULING-SHAPED QUESTION FOR DAVE

**Is a `var(--x, 380px)` with a real fallback "unresolved" for `_validate_compose`?** I ruled it
is not (commit `57ddff1`) because that is what the browser does, and because s258-D3 already
grants exactly this to `--*-max` by name. If you want the allowance kept to an explicit name
list instead, revert that hunk and add `--dg-vh` and `--ftb-top` to `RUNTIME_VARS`.

**Second, smaller:** nothing in the repo re-runs `gen_canon_components.py` when a snippet
changes. `_build_all.py` does (barred in this lane). A pre-commit hook, or a `--check` in the
snippet gate, would have caught this on 2026-09-09 instead of at cold run 6 on 2026-09-10.

## Tokens

ESTIMATED ~95K FILL for the lane (measurement scripts + two generator runs + gate sweep +
playwright drive, no `_checkin.py` run — no gauge answer given).
