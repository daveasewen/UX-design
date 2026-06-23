# Dynamic-weight icons

Outline icon set whose **line thickness, colour and scale are each a single variable** — so an
icon can be tuned freely or snapped to match the font weight of the label beside it.

## Why this exists
The HSBC catalogue (`../`) is built from **filled** paths (605 `fill="currentColor"`, zero strokes),
so its icons can't be re-weighted — that's why the library ships separate hand-drawn `-thick`
variants. To get *dynamic* width you need **outline/stroke** icons, where one `stroke-width` drives
everything. These 8 are drawn that way, using the HSBC set as visual reference.
See `../../guidelines/icons.md`.

## Files
- **`playground.html`** — interactive tuner: thickness slider + Light/Regular/Medium/Bold presets,
  colour swatches (icon tokens) + picker, scale slider, light/dark theme, live label match, copyable CSS.
- **`dynamic-icons.js`** — the source the builder uses: 8 path definitions + a `<dyn-icon>` web component.
- **`README.md`** — this file.

## Core 8
`close · plus · check · chevron · search · arrow · info · menu` (24×24 grid, round caps/joins).

## Usage
```html
<script src="dynamic-icons.js"></script>
<span class="icon"><!-- DYN_ICONS["search"] --></span>
<!-- or --> <dyn-icon name="search"></dyn-icon>
```
```css
.icon, dyn-icon{
  --icon-stroke:1.7;        /* 1.3 Light · 1.7 Regular · 2.1 Medium · 2.7 Bold */
  --icon-color:#333333;     /* icon/default token, or currentColor */
  --icon-size:24px;
  display:inline-flex; width:var(--icon-size); height:var(--icon-size); color:var(--icon-color);
}
.icon svg, dyn-icon svg{ fill:none; stroke:currentColor; stroke-linecap:round; stroke-linejoin:round; }
.icon svg *, dyn-icon svg *{ stroke-width:var(--icon-stroke); vector-effect:non-scaling-stroke; }
```

To **match a label**, set `--icon-stroke` from the label's weight:
`300→1.3 · 400→1.7 · 500→2.1 · 700→2.7` (starting map — tune to taste).

`vector-effect:non-scaling-stroke` keeps the line a constant px at any size (system-consistent).
Drop it to let the line scale with the icon instead.

## Route to Figma (later)
Each icon becomes one component with a **Weight** variant property (Light/Regular/Medium/Bold) mapping
to the stroke values above — or a single component bound to a stroke-weight variable once the team is on
variable-driven strokes. Colour binds to the existing `icon/*` tokens; size to `icon-scale.json`
(xsmall 12 / small 18 / medium 24 / large 36). Can be pushed via the Figma MCP when ready.
