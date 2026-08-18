# PROPOSAL — master size ramp + per-theme size modes (FLOATED, Dave's, #200)

> **REGISTER: FLOATED.** Dave, #200, verbatim: *"this might get complicated but I think this should be
> a mode for each theme, but I don't want to go down a rabbit hole for now"* · *"I'm working in
> instinct, lets record these shapes tho"*. ⛔ **Nothing here is ruled. Nothing mints. The console
> xs/s/m/l dimension-first work (tuner v3, `reviews/RADIUS-CORNER-TUNER-2026-08-18-v3.html`) stands
> untouched by this document.**

## The shape, as Dave gave it

**Master size ramp — FIVE steps, all on the 4px grid** (Dave corrected his first spread 24-32-38-44-50
to on-grid when the 4px rule was surfaced):

```
24 · 32 · 40 · 44 · 48
```

**Four named size classes, each an OVERLAPPING PAIR off the ramp** (each class shares a boundary
height with its neighbour):

| class    | heights   |
|----------|-----------|
| x-small  | 24 + 32   |
| small    | 32 + 40   |
| med      | 40 + 44   |
| large    | 44 + 48   |

**Sizing becomes a MODE per theme** — each theme exposes sizes as modes over the shared ramp
(the semantic-scale mode grammar, `layout.json`), rather than each theme minting its own heights.
Earlier wording, same turn-family: *"each mode gets two sizes each"*.

## What is deliberately OPEN (asked, Dave: "not sure right now, I'm working in instinct")

**The semantics of the two heights within a class.** Candidate readings offered, none picked:
(a) a theme picks ONE of the two when it adopts the class (density pick);
(b) both are available within the class as a compact/comfortable variant pair;
(c) they are min/max bounds.

Also open: which classes/modes each theme gets, and how this composes with the s200-D1 mint-time
derivation (padding + thumb would derive off ramp heights at mint, per that mechanism — implied,
not ruled).

## Provenance

- Chat #200, 2026-08-18, live — this document is the record Dave asked for ("lets record these shapes tho").
- Context rulings (inscribed, `knowledge/_rulings.json`): `s200-D1` mint-time derivation + 2px padding
  step · `s200-D2`/`s200-D3` console-only mint · labels xs/s/m/l ruled in-chat on tuner v3.
- Intended beneficiary named by Dave: the future **theme generator** side project.
