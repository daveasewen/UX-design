# PREMISE PROBE — DP-08 A+B under `s251-D1` (#251, 2026-09-06)

> MODEL-ROUTING rule 7 (i). Opus 5, cold. Rules nothing, builds nothing in canon, writes ONE report.
> Template: `notes/_briefs/_TEMPLATE-premise-probe.md`. Report: `notes/_subreports/2026-09-06-251-PROBE-dp08.md`.

## The ruling this serves (read it first, verbatim, from the store)

`knowledge/_rulings.json` § `s251-D1` — DP-08 resolved as A+B: the header status STRIP is the orientation layer, the Needs-attention card is the detail; strip items point at their detail (a chip may anchor-link to the card); one shared count and label; Undrawn facilities is strip-only (a state, not an action).
Also in scope: `s247-D3` (status tiles not inside KPI cards), `s247-D4` (headline = a ROW), `s248-D1` (1100 band re-flows, rail may sit two-up), `s249-D2` (row count is data-dictated; 12-col desirable only), `s249-D5` ("No ragged layouts"), `s250-D1` (byte gate: code-only, `consumes`-aware, caps 16,384 / 34,816 UNMOVED).

Prior work to build on, not redo: `notes/_subreports/2026-09-06-249-DP08-status-surface-analysis.md` and `outputs/w2-debt/dp08/` (options A, B, B2 as byte-clean copies of `outputs/w2-rhythm/arm-B-sighted/dashboard.html`, probe JSONs, `_render.py`, `_build.py`). Only 1440 light was rendered there.

## Three premises

### P1 — the four-tile row survives the bands
1. **PREMISE** — Option A's `.tpl-group-lead > .c-bento__grid{--bento-cols-now:4}` renders four equal, un-ragged tiles at 1440, 1100 and 820, with a 4/2/1 (or 4/4/2, state which) band line that does not orphan a cell.
2. **CONSEQUENCE IF FALSE** — the build lane ships a row that breaks `s249-D5` at 1100 (four does not divide three), discovered only at the cold test of the release.
3. **PROOF** — render `dp08-A.html` at 1440 / 1100 / 820 (light; dark once at 1440), paste tile x/w for all four per width; report any tile whose width differs from its siblings by >1px, any wrap, any void > one gutter.
4. **MUTATION** — set `--bento-cols-now:3` at 1100 and confirm the probe reports the ragged fourth tile; if it can't see it, the probe isn't a proof.
5. **RULINGS** — `s247-D4`, `s249-D2`, `s249-D5`, `s248-D1`.

### P2 — B2's rail order is legal and keeps the card above the fold at every band
1. **PREMISE** — Needs-attention above Balances puts the card top ≤ 900px at 1440 AND does not break `s248-D1`'s two-up rail at 1100 (both cards fill their row, no orphan, no ragged seam).
2. **CONSEQUENCE IF FALSE** — the anchor link from the strip lands on a card the user still can't see, or the 1100 layout regresses to lane D's 358.7px orphan.
3. **PROOF** — render `dp08-B2.html` at 1440 / 1100 / 820; paste Needs-attention `{x,y,w,h}` and Balances `{x,y,w,h}` per width; at 1100 paste both rail card heights side by side.
4. **MUTATION** — swap the order back (B, not B2) and confirm the probe reports y > 900 at 1440.
5. **RULINGS** — `s248-D1`, `s249-D5`, DP-10 (`reviews/DASHBOARD-PRINCIPLES-2026-09-05-v1.html` L462).

### P3 — the chip-to-card anchor is one behaviour that fits the page byte cap
1. **PREMISE** — a status-strip chip with `href="#<needs-attention id>"` plus a small arrive-and-highlight behaviour (focus the card, transient outline, respect `prefers-reduced-motion`) can be a behaviour partial that, added to the dashboard page's `consumes` sum, keeps the page under `PAGE_BYTES` 34,816 code-only and the partial under `MAX_BYTES` 16,384 — AND the anchor target is inside the same tab panel (`#p1`) as the chip, so no tab switch is needed.
2. **CONSEQUENCE IF FALSE** — the build lane writes the behaviour, the gate goes red, and the byte fork re-opens one session after `s250-D1` closed it.
3. **PROOF** — (a) write a THROWAWAY prototype of the behaviour in `outputs/w2-debt/dp08/` (NOT in `knowledge/`), measure its code-only bytes with the scanner in `knowledge/_validate_behaviour.py` (import it; do not edit it); (b) run `_validate_behaviour.py` as-is and paste the current dashboard page sum, then the sum with the prototype added; (c) grep `dp08-A.html` and `dp08-B2.html` for the chip's current `href` (`#p2`) and the card's id, paste both and state whether they are in the same `role="tabpanel"`.
4. **MUTATION** — pad the prototype with code (not comments — `CODE_PAD()` style) until the page sum crosses 34,816 and confirm the gate names it.
5. **RULINGS** — `s250-D1`, `s234-D5` (behaviour address), ADR-0015 A3.

## Also probe (cheap, no premise line): does A+B double-report?
Count DP-20 signal carriers above the fold in A+B2 (A's strip + B2's card) vs A alone vs B2 alone. Paste the counts. State the strongest case that the strip chip and the card row are REDUNDANT, then the strongest case they are INDEX and BODY. Recommend nothing.

## Rules
- Every number pasted from a command run in this window. No figure from #249's report is re-quoted without re-running it.
- Playwright may be absent; #249 bootstrapped it without root (libXdamage from a .deb) — do the same, note the cost, or say why not.
- Never `_build_all.py`. Never edit `knowledge/`. Edit, never Write, on existing files. Batch independent reads.
- Report per `notes/_subreports/_TEMPLATE.md`: `COUNTS:` exact shape, `CITES:` beside it listing the ruling ids above, `REPLAY-THESE:` with the commands. Recommend nothing; price each premise TRUE/FALSE/UNPROVEN with the pasted evidence.
- Report your token use from `message.usage` if reachable; else write `UNMEASURED` and why.
