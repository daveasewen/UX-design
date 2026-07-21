# Dynamic-weight icons

Outline icon set whose **line thickness, colour and scale are each a single variable** — so an
icon can be tuned freely or snapped to match the font weight of the label beside it.

## Why this exists
The HSBC catalogue (`../`) is built from **filled** paths (605 `fill="currentColor"`, zero strokes),
so its icons can't be re-weighted — that's why the library ships separate hand-drawn `-thick`
variants. To get *dynamic* width you need **outline/stroke** icons, where one `stroke-width` drives
everything. These are drawn that way, using the HSBC set as visual reference.
See `../../guidelines/icons.md`.

**Thickness is now calibrated.** `icon-weight-decisions.json` holds the locked stroke for each
weight × size; `dynamic-icons.js` bakes it in as `ICON_STROKE[weight][size]` and the `<dyn-icon>`
component applies it automatically.

## Files
- **`playground.html`** — calibration tool (3 tabs):
  - **Tune** — pick a weight + text size, set the icon thickness against a real text sample, then
    *Lock this cell*, *Apply px to whole weight*, or *Apply ratio across sizes*.
  - **Matrix** — every weight × size combo rendered side by side for comparison; green = locked, grey = auto.
  - **Decisions** — the locked table + export to JSON / CSS vars / JS map; import and clear.
  - Setup panel: pick icon, sample text, colour (icon tokens + picker), editable list of text sizes,
    icon-size ratio, and a **State** control (Default / Active) + **Show badge** toggle. Decisions
    **autosave** (and export to a file you keep).
  - Tune shows an **All states** strip (default · active · default+badge · active+badge); carets
    render solid automatically; the Matrix reflects the chosen state.
- **`dynamic-icons.js`** — the source the builder uses: 77 path definitions, the calibrated
  `ICON_STROKE` table + `strokeFor()`, `SOLID`/`ACTIVE_PATHS`, and an auto `<dyn-icon>` web component
  with `state` + `badge` support.
- **`icon-weight-decisions.json`** — the locked weight×size→stroke calibration (source of truth).
- **`RUNBOOK-icon-conversion.md`** — the method + coverage tracker for porting the HSBC catalogue group by group.
- **`README.md`** — this file.

## Icons (77)
**Core 8:** close · plus · check · chevron · search · arrow · info · menu
**Essential actions:** settings · filter · edit · trash · download · upload · share · copy · refresh · more · external-link · plus-circle
**Navigation & arrows:** chevron-up · chevron-down · chevron-left · arrow-up · arrow-down · arrow-left · home · expand · collapse · back
**Status & alerts:** check-circle · x-circle · alert-triangle · alert-circle · help-circle · bell · eye · eye-off · lock · unlock · shield-check · ban
**People & comms:** user · users · mail · phone · message · calendar · clock · star · heart · bookmark
**Media & common:** play · pause · stop · volume · mute · image · file · folder · link · tag · map-pin · globe · camera · send · minus · minus-circle
**Arrows & chevrons (HSBC group):** chevron-right · chevron-double-up · chevron-double-down · chevron-double-left · chevron-double-right · caret-up · caret-down · caret-left · caret-right
All on a 24×24 grid, round caps/joins. Carets are always solid; chevrons collapse the HSBC `-thick`
variants into the weight axis. Catalogue conversion runs group by group — see the **runbook**.

## States
```html
<dyn-icon name="trash" weight="400" size="24"></dyn-icon>             <!-- default: outline -->
<dyn-icon name="trash" state="active" size="24"></dyn-icon>           <!-- active -->
<dyn-icon name="bell"  weight="400" size="24" badge></dyn-icon>       <!-- notification dot -->
```
`badge` adds a dot (recolour via `--dyn-badge`). The **active** state keeps *both* the fill and the
lines — it never collapses to a featureless blob. Each icon resolves to one of four strategies
(see `activeMode(name)`):

- **knockout** — solid shape with authored interior reversed out (info, alert, mail, camera, **trash**…).
- **bold** — line-only icons with nothing to fill (close, menu, chevrons, arrows) → heavier stroke.
- **fill** — clean single silhouettes (star, play, phone, bell…) → plain solid.
- **fill-detail** — solid silhouette with the icon's own lines reversed out (lock, user, folder, globe…).

Tune which icon uses which via the `ACTIVE_KNOCKOUT`, `ACTIVE_BOLD`, `PLAIN_FILL` sets in `dynamic-icons.js`.

## How thickness, size and "scaling" relate
With `non-scaling-stroke`, a 1.7px line is 1.7px at *any* icon size — so next to 16px text it looks
heavier than next to 32px text. To truly match the label you set the thickness **per size**. That's the
calibration the Matrix is for. *Apply ratio across sizes* keeps a constant stroke-to-text proportion for a
weight (the usual best match); *Apply px to whole weight* forces one fixed px line everywhere.

## Output
Export gives you `icon-weight-decisions.json` plus copy-to-clipboard for:
- **CSS vars** — `--icon-stroke-400-16: 1.50px;` (one per weight×size)
- **JS map** — `iconStroke[400][16] = 1.5`
Hand the JSON back here to commit it next to these files, or wire the map into the component.

## Usage
**Easiest — auto component** (pulls the calibrated thickness for you):
```html
<script src="dynamic-icons.js"></script>
<dyn-icon name="search" weight="400" size="16"></dyn-icon>
<dyn-icon name="settings" weight="700" size="32" color="#DB0011"></dyn-icon>
```

**Manual — raw markup + CSS** (when you want to drive the variables yourself):
```css
.icon{
  --icon-stroke:1.4;        /* e.g. ICON_STROKE[400][16] */
  --icon-color:#333333;     /* icon/default token, or currentColor */
  --icon-size:16px;
  display:inline-flex; width:var(--icon-size); height:var(--icon-size); color:var(--icon-color);
}
.icon svg{ fill:none; stroke:currentColor; stroke-linecap:round; stroke-linejoin:round; }
.icon svg *{ stroke-width:var(--icon-stroke); vector-effect:non-scaling-stroke; }
```

`strokeFor(weight, size)` returns the calibrated px (nearest weight, interpolated across size), so
you can match any label without memorising the table.

## Route to Figma (later)
Each icon becomes one component with a **Weight** variant property (Light/Regular/Medium/Bold) mapping
to the stroke values above — or a single component bound to a stroke-weight variable once the team is on
variable-driven strokes. Colour binds to the existing `icon/*` tokens; size to `icon-scale.json`
(xsmall 12 / small 18 / medium 24 / large 36). Can be pushed via the Figma MCP when ready.
