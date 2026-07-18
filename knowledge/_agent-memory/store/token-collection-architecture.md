---
name: token-collection-architecture
description: "The real Figma variable collection structure (brand / semantic-color / semantic-scale) and modes, from the native variable export"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 92c69cca-fca7-4999-a3d7-517fe5550c6c
---

Authoritative structure of the HSBC Common Toolkit variables, from Figma's native **"Export modes"** (right-click a collection in the Local variables panel → Export modes → DTCG `.tokens.json` per mode). Export landed 2026-06-17 in `knowledge/tokens/_raw/` (subfolders `brand/`, `semantic-color/`, `semantic-scale/`). This SUPERSEDES the earlier OCR-sourced token files. See [[sutherland-figma-mapping]] for the Sutherland modes.

**Three collections:**
1. **brand** (133 primitives, modes: `hsbc`, `Sutherland-core`). Naming: `color/primary` (#DB0011, the HSBC red — NOT "core/hsbc-red"), `color/black`, `color/white`, `color/complimentary/red-1..3` ("complimentary" misspelled in-variable), `color/grey/100..800` + `grey/white|black|transparent/*`. No depricate. NOTE: variable names differ from the doc swatch names I OCR'd (e.g. doc `neutral-grey-8` = variable `color/grey/800`).
2. **semantic-color** (258 leaves/mode, modes: `light`, `dark`, `Sutherland-light`). Intent groups: background, border, divider, form, icon, primary, progress, rag, scrollbar, secondary, table, tabs, tertiary, text, timer, tooltip, data-vis, blur — PLUS `non-interactive (depricate)` and `interactive (depricate)` groups. **147 of 258 are deprecated** (name contains "depricate"); only **111 are live/canon**. Each token resolves to a concrete `hex` per mode AND keeps `com.figma.aliasData` pointing at its brand primitive (e.g. `text/default` → `color/grey/800` = #333333 in light). light vs dark differ in 141 tokens.
3. **semantic-scale** (127 leaves/mode, modes: `scale-1`, `scale-2`, `scale-3`, `scale-1-200`). Groups: layout, gap, padding, border-radius, border-width, typography, icon, elevation. This is the responsive scale layer — overlaps/supersedes the OCR'd `layout.json`, `typography.json`, `spacing.json`. `scale-1-200` looks like a 200% density/zoom variant of scale-1.

**Token value format:** Figma verbose color object `{"colorSpace":"srgb","components":[...],"alpha":1,"hex":"#RRGGBB"}`; `$extensions["com.figma.variableId"]` + `com.figma.aliasData` carry the variable id and alias target. Use the `hex` field for the resolved value and `aliasData.targetVariableName` for the primitive reference.

**Canon rule:** HSBC modes are canon; exclude all 147 `depricate` tokens from canon (keep a manifest for Dave's bulk-delete). Sutherland modes = mapping layer, not canon.

**UPDATE 2026-07-17 — non-destructive divergence via SIBLING token files.** When Apollo SDS diverges from the HSBC-general incumbent (e.g. 4px-normalised type + spacing vs the raw Figma export), the pattern Dave ruled ("preserve the old as legacy… the old ones are used by HSBC in general… Apollo will hopefully be adopted for HSBC") is: **park the incumbent as an underscore-prefixed sibling file** — `tokens/_typography-hsbc-general.json`, `_spacing-hsbc-general.json`, `_icon-scale-hsbc-general.json`. The `_` prefix keeps it OUT of Apollo generation automatically: `gen_canon_tokens.py` uses an explicit file list, and `_build_blast_radius.py` globs `tokens/*.json` non-recursively AND skips `startswith("_")`. So the incumbent stays on disk + resolvable for HSBC-general/legacy consumers, governed as a sibling MODE for a mode-by-mode migration, while Apollo's canon file carries the diverged values. Both are HSBC — incumbent vs proposed-standard, not fork. Also this session: legacy/unused tokens (the fixed-px `padding/arrow` + `icon/arrow/font-N` chevron) get retired into these siblings rather than deleted. See [[multi-mode-product-vision]], [[fixed-flex-charter]]; full rulings in `knowledge/_proforma/_TYPE-DECISIONS.md`.
