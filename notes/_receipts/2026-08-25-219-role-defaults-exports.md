# #219 — Dave's edit-pass defaults, verbatim tuner exports (2026-08-25)

**Framing, Dave's words (#219, in chat):** "I'll give you the defaults for each, but what I want is
options during the edit pass that Apollo will have in the end. I don't think its as simple as one
decision for each theme, certainly not for the gallery."

⛔ **Status: TRANSCRIPTION IN PROGRESS — Dave said "Please wait for the rest." Nothing here is
enacted or inscribed until the set is complete and read back.** Each export block below is verbatim,
untouched. The ruling shape this feeds is *default + edit-pass option set + locked*, per the #219
framing readback (confirmed by Dave proceeding with defaults).

---

## DASHBOARD

### legacy

```json
{
  "$proposed": true,
  "not_ruled": "Everything beyond s217-D5's own words is PROPOSED, not ruled.",
  "ruling": "s217-D5",
  "type": "dashboard",
  "state": {
    "mainSpacing": "24",
    "subSpacing": "4",
    "keylines": "off",
    "pageBg": "grey",
    "bentoBg": "transparent"
  },
  "resolved": {
    "theme": "legacy",
    "mode": "light",
    "role": "dashboard",
    "gutterPx": 24,
    "containerRadiusPx": 0,
    "tileRadiusPx": 0,
    "tileBorderPx": 0,
    "pageBackground": "rgb(240, 240, 240)",
    "bentoBackground": "rgba(0, 0, 0, 0)",
    "captionBackground": null,
    "captionSpacePx": null
  }
}
```

### mono

```json
{
  "$proposed": true,
  "not_ruled": "Everything beyond s217-D5's own words is PROPOSED, not ruled.",
  "ruling": "s217-D5",
  "type": "dashboard",
  "state": {
    "mainSpacing": "40",
    "subSpacing": "4",
    "keylines": "off",
    "pageBg": "grey",
    "bentoBg": "transparent"
  },
  "resolved": {
    "theme": "mono",
    "mode": "light",
    "role": "dashboard",
    "gutterPx": 40,
    "containerRadiusPx": 0,
    "tileRadiusPx": 0,
    "tileBorderPx": 0,
    "pageBackground": "rgb(240, 240, 240)",
    "bentoBackground": "rgba(0, 0, 0, 0)",
    "captionBackground": null,
    "captionSpacePx": null
  }
}
```

### console

```json
{
  "$proposed": true,
  "not_ruled": "Everything beyond s217-D5's own words is PROPOSED, not ruled.",
  "ruling": "s217-D5",
  "type": "dashboard",
  "state": {
    "mainSpacing": "40",
    "subSpacing": "4",
    "keylines": "off",
    "pageBg": "grey",
    "bentoBg": "transparent"
  },
  "resolved": {
    "theme": "console",
    "mode": "light",
    "role": "dashboard",
    "gutterPx": 40,
    "containerRadiusPx": 20,
    "tileRadiusPx": 20,
    "tileBorderPx": 0,
    "pageBackground": "rgb(240, 240, 240)",
    "bentoBackground": "rgba(0, 0, 0, 0)",
    "captionBackground": null,
    "captionSpacePx": null
  }
}
```

### supercharge

```json
{
  "$proposed": true,
  "not_ruled": "Everything beyond s217-D5's own words is PROPOSED, not ruled.",
  "ruling": "s217-D5",
  "type": "dashboard",
  "state": {
    "mainSpacing": "24",
    "subSpacing": "2",
    "keylines": "off",
    "pageBg": "grey",
    "bentoBg": "transparent"
  },
  "resolved": {
    "theme": "supercharge",
    "mode": "light",
    "role": "dashboard",
    "gutterPx": 24,
    "containerRadiusPx": 0,
    "tileRadiusPx": 0,
    "tileBorderPx": 0,
    "pageBackground": "rgb(223, 222, 220)",
    "bentoBackground": "rgba(0, 0, 0, 0)",
    "captionBackground": null,
    "captionSpacePx": null
  }
}
```

---

## Conductor's parse notes (dashboard set — readings, not rulings)

- **Two spacing dials, new to the dashboard grammar:** `mainSpacing` (legacy 24 · mono 40 · console 40 · supercharge 24) and `subSpacing` (4/4/4/2) — the bento-of-bentos split (s217-D3 dashboard = sectioned app). The #217 matrix's single `spacing` dial does not cover this.
- **`keylines: off` in all four** — read WITH s218-D1 (corner keylines, DASHBOARD-ONLY, option-selected): reading is *keylines stay an edit-pass option for dashboards, default off*. ⚠ Awaiting Dave's confirm at readback.
- **Radii:** console 20/20 (container/tile), all other themes 0 — consistent with the minted console radius grammar; squares stay square.
- **Grey-tint check (standing rule):** supercharge's page grey resolves `rgb(223, 222, 220)` (warm) vs `rgb(240, 240, 240)` in the other three — presumed the theme's own grey token resolving, to be verified at enactment and surfaced, never auto-swapped.
- All four are `mode: light` exports. Dark-mode derivation is NOT in this set.

---

## DISPLAY

### supercharge

```json
{
  "$proposed": true,
  "not_ruled": "Everything beyond s217-D5's own words is PROPOSED, not ruled.",
  "ruling": "s217-D5",
  "type": "display",
  "state": {
    "spacing": "2",
    "keylines": "off",
    "pageBg": "grey",
    "bentoBg": "transparent"
  },
  "resolved": {
    "theme": "supercharge",
    "mode": "light",
    "role": "brochureware",
    "gutterPx": 2,
    "containerRadiusPx": 0,
    "tileRadiusPx": 0,
    "tileBorderPx": 0,
    "pageBackground": "rgb(223, 222, 220)",
    "bentoBackground": "rgba(0, 0, 0, 0)",
    "captionBackground": null,
    "captionSpacePx": null
  }
}
```

### console

```json
{
  "$proposed": true,
  "not_ruled": "Everything beyond s217-D5's own words is PROPOSED, not ruled.",
  "ruling": "s217-D5",
  "type": "display",
  "state": {
    "spacing": "24",
    "keylines": "off",
    "pageBg": "grey",
    "bentoBg": "transparent"
  },
  "resolved": {
    "theme": "console",
    "mode": "light",
    "role": "brochureware",
    "gutterPx": 24,
    "containerRadiusPx": 0,
    "tileRadiusPx": 20,
    "tileBorderPx": 0,
    "pageBackground": "rgb(240, 240, 240)",
    "bentoBackground": "rgba(0, 0, 0, 0)",
    "captionBackground": null,
    "captionSpacePx": null
  }
}
```

### mono

```json
{
  "$proposed": true,
  "not_ruled": "Everything beyond s217-D5's own words is PROPOSED, not ruled.",
  "ruling": "s217-D5",
  "type": "display",
  "state": {
    "spacing": "16",
    "keylines": "off",
    "pageBg": "grey",
    "bentoBg": "transparent"
  },
  "resolved": {
    "theme": "mono",
    "mode": "light",
    "role": "brochureware",
    "gutterPx": 16,
    "containerRadiusPx": 0,
    "tileRadiusPx": 0,
    "tileBorderPx": 0,
    "pageBackground": "rgb(240, 240, 240)",
    "bentoBackground": "rgba(0, 0, 0, 0)",
    "captionBackground": null,
    "captionSpacePx": null
  }
}
```

### legacy

```json
{
  "$proposed": true,
  "not_ruled": "Everything beyond s217-D5's own words is PROPOSED, not ruled.",
  "ruling": "s217-D5",
  "type": "display",
  "state": {
    "spacing": "24",
    "keylines": "on",
    "pageBg": "transparent",
    "bentoBg": "transparent"
  },
  "resolved": {
    "theme": "legacy",
    "mode": "light",
    "role": "brochureware",
    "gutterPx": 24,
    "containerRadiusPx": 0,
    "tileRadiusPx": 0,
    "tileBorderPx": 1,
    "pageBackground": "rgba(0, 0, 0, 0)",
    "bentoBackground": "rgba(0, 0, 0, 0)",
    "captionBackground": null,
    "captionSpacePx": null
  }
}
```

---

## Conductor's parse notes (display set — readings, not rulings)

- **Spacing values leave the s217-D5 trio:** display defaults are 2 / 24 / 16 / 24 (SC/console/mono/legacy). s217-D5's display spacing proposed tight/standard/generous = 1/24/40; supercharge 2 and mono 16 are OUTSIDE that set. Reading: the old three-word option set does not survive as the edit-pass rails — the option space is wider (likely the numeric dial itself, or a wider ruled set). ⚠ For readback.
- **Legacy is the odd one out, twice:** the ONLY display with `keylines: on` (tileBorder 1) and the ONLY one with `pageBg: transparent`. Echoes the s135-D1 pattern (legacy carries borders). Dashboard-legacy had keylines OFF — so keylines split by ROLE within the same theme.
- **Console display: tileRadius 20 with containerRadius 0** — differs from console dashboard (20/20). Radius placement is role-dependent, consistent with s217-D3 (the role decides where radius sits).
- **Stale vocabulary in the tooling, verbatim kept:** every display export resolves `"role": "brochureware"` — s217-D5 renamed that role DISPLAY; the tuner's resolver still emits the old word. Tooling wrinkle to fix at enactment (resolver only, exports stay verbatim history).

---

## GALLERY

### legacy

```json
{
  "$proposed": true,
  "not_ruled": "Everything beyond s217-D5's own words is PROPOSED, not ruled.",
  "ruling": "s217-D5",
  "type": "gallery",
  "state": {
    "spacing": "24",
    "keylines": "on",
    "mode": "bento",
    "edge": "square",
    "rounding": "corners",
    "pageBg": "white",
    "bentoBg": "transparent",
    "capBg": "transparent"
  },
  "resolved": {
    "theme": "legacy",
    "mode": "light",
    "role": "gallery",
    "gutterPx": 24,
    "containerRadiusPx": 0,
    "tileRadiusPx": 0,
    "tileBorderPx": 1,
    "pageBackground": "rgb(255, 255, 255)",
    "bentoBackground": "rgba(0, 0, 0, 0)",
    "captionBackground": "rgba(0, 0, 0, 0)",
    "captionSpacePx": 86
  }
}
```

### mono

```json
{
  "$proposed": true,
  "not_ruled": "Everything beyond s217-D5's own words is PROPOSED, not ruled.",
  "ruling": "s217-D5",
  "type": "gallery",
  "state": {
    "spacing": "40",
    "keylines": "off",
    "mode": "bento",
    "edge": "square",
    "rounding": "corners",
    "pageBg": "transparent",
    "bentoBg": "transparent",
    "capBg": "grey"
  },
  "resolved": {
    "theme": "mono",
    "mode": "light",
    "role": "gallery",
    "gutterPx": 40,
    "containerRadiusPx": 0,
    "tileRadiusPx": 0,
    "tileBorderPx": 0,
    "pageBackground": "rgba(0, 0, 0, 0)",
    "bentoBackground": "rgba(0, 0, 0, 0)",
    "captionBackground": "rgb(240, 240, 240)",
    "captionSpacePx": 86
  }
}
```

### console

```json
{
  "$proposed": true,
  "not_ruled": "Everything beyond s217-D5's own words is PROPOSED, not ruled.",
  "ruling": "s217-D5",
  "type": "gallery",
  "state": {
    "spacing": "40",
    "keylines": "off",
    "mode": "bento",
    "edge": "square",
    "rounding": "capsule",
    "pageBg": "transparent",
    "bentoBg": "transparent",
    "capBg": "grey"
  },
  "resolved": {
    "theme": "console",
    "mode": "light",
    "role": "gallery",
    "gutterPx": 40,
    "containerRadiusPx": 0,
    "tileRadiusPx": 20,
    "tileBorderPx": 0,
    "pageBackground": "rgba(0, 0, 0, 0)",
    "bentoBackground": "rgba(0, 0, 0, 0)",
    "captionBackground": "rgb(240, 240, 240)",
    "captionSpacePx": 86
  }
}
```

### supercharge

```json
{
  "$proposed": true,
  "not_ruled": "Everything beyond s217-D5's own words is PROPOSED, not ruled.",
  "ruling": "s217-D5",
  "type": "gallery",
  "state": {
    "spacing": "1",
    "keylines": "off",
    "mode": "bento",
    "edge": "square",
    "rounding": "corners",
    "pageBg": "transparent",
    "bentoBg": "transparent",
    "capBg": "transparent"
  },
  "resolved": {
    "theme": "supercharge",
    "mode": "light",
    "role": "gallery",
    "gutterPx": 1,
    "containerRadiusPx": 0,
    "tileRadiusPx": 0,
    "tileBorderPx": 0,
    "pageBackground": "rgba(0, 0, 0, 0)",
    "bentoBackground": "rgba(0, 0, 0, 0)",
    "captionBackground": "rgba(0, 0, 0, 0)",
    "captionSpacePx": 86
  }
}
```

---

## Conductor's parse notes (gallery set — readings, not rulings)

- **The gallery grammar is the widest, as Dave said it would be:** 8 dials (spacing, keylines, mode, edge, rounding, pageBg, bentoBg, capBg) vs dashboard's 5 and display's 4.
- **`captionSpacePx: 86` in all four** — confirms the ruled caption space as a gallery-role constant across themes.
- **`edge: "square"` in all four** — ⚠ INTERACTION: s218-D6(4) enacted squaring SCOPED to the photography page's wall, with the gallery role's s217-D3 exemption "expressly untouched." All-four-square defaults read as widening squaring to the gallery role default — WHICH re-livens the flattened-portrait class (sitting Q3) and the W-99zi third bend (orphan/squaring: role property vs parameter). FOR READBACK, not assumed.
- **⚠ CONFLICT TO SURFACE — mono caption ground:** this export resolves mono `capBg` to `rgb(240,240,240)` (light grey). `s218-D6(1)` RATIFIED mono captions on the photography wall at `#1A1A1A` (darkest grey) with white ink, from Dave's own #218 rider. Light-grey default vs ratified dark ground — either a supersession, or photography-wall and gallery-role diverge deliberately. DAVE'S CALL, asked at readback, nothing changed anywhere.
- **`rounding: "capsule"` on console** — resolves s217-D5's open P3 (the capsule's edge) as console-gallery's default, by his hand.
- **Keylines pattern across the full set:** ON only in legacy display + legacy gallery; OFF everywhere else including all dashboards. Legacy is the border-carrying theme (s135-D1 echo); keylines split by role within theme.
- **Full spacing default matrix (main gutter):** dashboard 24/40/40/24 · display 24/16/24/2 · gallery 24/40/40/1 (legacy/mono/console/SC). Values {1,2,4,16,24,40} — six stops, wider than any previously proposed set.

**SET COMPLETE (three types × four themes = 12 exports, matching the s217-D5 matrix).**

---

## PARKED CORRECTION — 2026-08-26, Dave's words, NOT ENACTED

Off the bento-rails page's "Capsule — White" card, Dave: **"almost right, this would never exist.
its ether cohesive capsule or rounded full image if there is no background colour on the caption."**
Reading: the capsule chord's ground ramp EXCLUDES white/no-ground — a ground-less caption belongs
only to the rounded-full-image chord. Confirms lane C's own flagged nit (white member invisible on
white page) from the defect side. ⛔ **PARKED by Dave in the same breath** ("i want to park this for
now though") — the bento lane resumes after the Apollo designer-release task. ⚠ Until enacted, the
bento-rails page carries one card he has said would never exist — known, accepted as parked.

