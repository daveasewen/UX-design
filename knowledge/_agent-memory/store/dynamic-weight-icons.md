---
name: dynamic-weight-icons
description: New outline icon set with variable line-weight that matches label font-weight; why + where + Figma route
metadata: 
  node_type: memory
  type: project
  originSessionId: bc6a6b73-6478-4f90-b02a-6bd0e429d7ae
---

Built 2026-06-23: a NEW outline/stroke icon set whose line thickness, colour and scale are each one CSS variable, so stroke-width can snap to the adjacent label's font-weight ("dynamic width to match text weight"). Needed because the HSBC catalogue is FILLED (605 `fill="currentColor"`, zero strokes) and can't be re-weighted — that's why HSBC ships separate `-thick` assets. See [[token-collection-architecture]].

Location: `knowledge/assets/icons/dynamic-weight/` — `playground.html` (CALIBRATION tool: Tune/Matrix/Decisions tabs; per weight×size thickness, lock + apply-px/apply-ratio, editable size set, export JSON/CSS/JS, autosave), `dynamic-icons.js` (68 path defs + baked `ICON_STROKE` table + `strokeFor()` + auto `<dyn-icon name weight size color>` component), `icon-weight-decisions.json` (locked calibration = source of truth), `README.md`. Icons (68): core 8 + essential actions + nav&arrows + status&alerts (check-circle/x-circle/alert-triangle/alert-circle/help-circle/bell/eye/eye-off/lock/unlock/shield-check/ban) + people&comms (user/users/mail/phone/message/calendar/clock/star/heart/bookmark) + media&common (play/pause/stop/volume/mute/image/file/folder/link/tag/map-pin/globe/camera/send/minus/minus-circle). NOTE: "convert"=redraw to outline variable-icons, NOT Figma port (Figma deferred). HSBC full 658-glyph catalogue not 1:1 yet — common product-UI set covered; more group-by-group on request.

LOCKED calibration 2026-06-23 (Dave) — stroke px per weight×size, key insight = thickness must scale with SIZE not just weight (fixed px reads heavier next to small text):
- 300: 14→.6 16→.7 20→.85 24→1 32→1.35
- 400: 14→1.2 16→1.4 20→1.7 24→2.05 32→2.75
- 500: 14→1.65 16→1.9 20→2.35 24→2.8 32→3.75
- 700: 14→2.1 16→2.4 20→3 24→3.6 32→4.8
STATES (2026-06-23): `<dyn-icon>` supports `state=default|active` + `badge` toggle. ACTIVE is NOT a blanket fill (Dave: must keep BOTH fill AND lines, interior reversed out — see trash example). 4 strategies via `activeMode(name)`: **knockout** (solid + authored interior reversed via SVG mask: ACTIVE_KNOCKOUT map outer/sym/symFill — info, mail, camera, trash…), **bold** (line-only icons, no fill area → heavier stroke ×1.6: ACTIVE_BOLD set — close, menu, chevrons, arrows…), **fill** (clean silhouettes → plain solid: PLAIN_FILL set — star, play, phone, bell, edit, volume + ACTIVE_PATHS overrides like gear-with-hole), **fill-detail** (general fallback: fill silhouette + reverse icon's own lines via mask — lock, user, folder, globe…). Canonical renderer = `buildIconSVG(name,{state,strokePx,badge})`, shared by component AND playground (playground `paintIcon` routes through it). THIN single shapes must be PLAIN_FILL not fill-detail (reversing own outline hollows them). Playground shows states: State seg + badge toggle + All-states strip. 77 icons.

CATALOGUE CONVERSION (group by group, started 2026-06-23): runbook = `RUNBOOK-icon-conversion.md` (method + coverage tracker). Rules: `-thick`→drop (weight axis); `*Active`→state; `*Badge`→badge toggle; `-low`/`-narrow`→skip; Social(7)=brand logos SKIP; Status(20)=keep colour-fixed. HSBC "Arrow"=solid caret (not line arrow). DONE: Arrows&chevrons (12). NEXT GROUP: Global controls (121, 46 active states). Then Touch, Volume, Media, Informative, Misc, Products&services.

Prior concept work: `knowledge/_fitness-test/icon-weight-system.html` + `icon-fake-weight.html`. Figma port still deferred (one component/icon, Weight variant property, colour→`icon/*` tokens, size→icon-scale.json).
