# Icon catalogue (HSBC Common Toolkit)

SVG icons exported from the Figma "Export board" (node `13244:4171`, "Gaps and edits" branch), organised by export group, for use in knowledge-base prototype builds.

## Status (2026-06-17)
- **Pilot done:** `status/` holds a validated sample (error, success, warning, yes) — cleaned, transparent background.
- **Full export pending** a Figma personal access token (see below).

## Running the full export
1. In Figma → Settings → Security → Personal access tokens → generate a token with **File content: Read-only** (`file_content:read`).
2. From this folder:
   ```bash
   export FIGMA_TOKEN=figd_your_token_here
   python3 _export-icons.py
   ```
   (Keep the token out of any committed file — it's read from the environment only.)
3. Output: `<group>/<icon>.svg` + `icons.manifest.json`.

## Conventions
- **Cleaning:** Figma's raw export wraps each icon in artboard artefacts (an `#E5E5E5` rect + a giant "Export board" path). The script strips these and unwraps the `Export board` / `Export Group` `<g>` layers.
- **Theming (`currentColor`):** icons with a *single neutral fill* (greys/black from `colour.json`) are rewritten to `fill="currentColor"` so they inherit `icon/*` colour tokens. Coloured/status icons keep their baked fills — these intentionally match brand/RAG tokens (e.g. error `#A8000B` = `rag/red`, success `#00847F` = `rag/green`).
- **Manifest:** each entry has `name`, `slug`, `file`, `active` (state variant), `fillMode` (`currentColor`|`baked`), and `fills`.

## Groups
Miscellaneous · Social · Touch · Informative · Volume and audio · Media · Arrows and chevrons · Products and services · Global controls · Status Icons
