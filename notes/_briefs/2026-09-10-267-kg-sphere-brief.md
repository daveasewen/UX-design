# #267 lane K brief — KG EXPLORER v1.9: the dig is a SPHERE again, not a disc

**Model: Opus. Conductor: Fable (#267). Dave's word, on his own screenshot of a 3D dig on Pagination: "very simple, click a node and it renders this" · "you can spin it but its just on a flat plane, it wast before". His screenshot is at the conductor's seat; what it shows is described below.**

## WHAT HAPPENED

v1.7/1.8 (`6d3b61e`) replaced the 3D halo sphere with a **ring in the camera plane** (`placeHalo()` + `basis()` in `knowledge/_kg_explorer.template.html:283-287`) so neighbours in line with the camera stopped hiding behind the focus. Side effect: the dig is now a flat disc that always faces the camera — spin gives no parallax. Dave reads that as broken. He is right: the fix removed the third dimension from the one view that exists to show it.

Second thing in his screenshot: the sector labels (`FAMILY · 2`, `HASPART · 4` …) sat nowhere near their nodes and the "ring" was a lopsided fan. Cause, read from the source: `mousemove` during a rotate-drag (`:381`) sets `rot` and calls `draw()` directly — `placeHalo()` only runs inside `tick()` — so during a drag the halo nodes stay in the OLD camera plane while the labels (`:279-280`, computed per draw with the current `basis()`) move to the new one. Verify this by driving it, not by reading it.

## THE JOB

1. **Read** `git show 9ee4fb7:knowledge/_kg_explorer.template.html` (v1.6, the last sphere) and HEAD's template. Name the exact lines that changed the geometry.
2. **v1.9 = sphere back, draw-order fix kept.** Halo neighbours are placed on a **world-space sphere** around the focus (v1.6's geometry — sectors as bands/patches on the sphere, so the sector labels still mean something; keep whatever v1.6 did for depth-2), and the v1.8 draw-order rule (halo dots above label plates) STAYS. Sector labels are placed on the same sphere, same frame, as their nodes. Depth-of-field and Macro cycle unchanged.
3. **The occlusion v1.8 was solving:** with a sphere, a neighbour directly behind the focus on the view axis is hidden. Mitigate WITHOUT flattening: e.g. draw the focus node with a lower alpha halo when a neighbour's projected position is inside it, or nudge (per frame, in screen space, ≤ 12px) a halo dot that projects inside the focus disc. Pick one, state it, measure it. Do NOT re-introduce the camera-plane ring.
4. **Drag staleness:** rotate-drag must re-place the halo (call `placeHalo()` before `draw()` in the mousemove path, or equivalent). With a world-space sphere this may be moot — prove it either way with a driven drag.
5. **Regenerate** with `python3 knowledge/_build_kg_explorer.py` → `notes/_KG-EXPLORER.html`. Never hand-edit the output.
6. **Sweep, don't eyeball** — the #266 method: playwright, 24 angles × 3 digs (Pagination, Button, and one SC), count wrong-colour centres and report against v1.8's **25/672, 2/192, 6/360**. A worse number is REPORTED, not hidden — the sphere will cost some occlusion and Dave has chosen that. Also: drive a rotate-drag mid-dig and assert every sector label is within N px of the centroid of its own sector's nodes (state N). Also: reproduce the v1.4 stall guard — a node behind the camera must not throw (`arc()` radius ≥ 0).
7. **Screenshots** of the Pagination dig at 3 angles (light + dark) to `notes/_kg-sweeps/267-v19/` for Dave's eye.
8. **Commit** template + built page (one commit, `during #267 2026-09-10 — KG explorer v1.9: …`, message names the geometry change and the sweep numbers). No push.
9. `notes/_lanes/2026-09-10-267-K-sphere.md` — done / NOT done / numbers / tokens (declare ESTIMATED).

## RULES
- ⛔ Do NOT read _CHAIN.md, GOOD-MORNING.md, _LIVE-STATE.md, _CARRIES.md. No `_build_all.py`, no `gen_kg_edges.py`, no `git stash`, never delete `.git/index.lock`. No edits outside the template, the built page, the sweep dir and the lane file.
- ⛔ Playwright: `pip install tiktoken --break-system-packages` if a gauge refuses; chromium recipe — if `libXdamage.so.1` is missing, `apt-get download libxdamage1 && dpkg -x` into a local dir and set `LD_LIBRARY_PATH`. Use `page.goto("file://…")`, never `set_content`.
- Every claim carries a probeable token (line numbers, counts, screenshot paths).
- Return under 300 words: commit sha · what changed (lines) · the occlusion mitigation chosen · sweep numbers vs v1.8 · label-distance assertion result · drag test result · screenshot paths · tokens · anything RED / NOT DONE.
