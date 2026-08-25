# #218 build brief — the decision-batch enactment (s218-D4/D5/D6, small edits, all ruled)

Every item here is RULED (store ids named) — this brief only enacts. Re-drive the named verify
after each edit; regenerate through the ONE writer wherever a page is generated.

1. **Chart-bar** (`knowledge/snippets/Chart-bar.reference.html`, s218-D5): growth easing → the
   file's house `cubic-bezier(.22,.61,.36,1)` family (two tokens); stacked letter keys' `dvFade`
   delayed by `var(--grow-dur)` so keys appear only on settled segments. Re-drive
   `knowledge/_render/verify_dv_d16_render.py` (update its easing/key expectations — the ruling
   changed them; keep all 9 mutation arms red) + `_verify_dv_stacked_enactment.py`. Regenerate
   `showroom/chart-bar.html` via `gen_showroom.py`.
2. **Command-palette** (s218-D4/D5): land the one-line hidden fix in the snippet's own `<style>`
   (`.cp[hidden],.cp-opt[hidden],.cp-empty[hidden],.cp-group[hidden]{display:none}`); the chord
   is CLAIMED — update the header/manifest wording from PROPOSED to the documented ⌘K/Ctrl+K
   pair (wording only; wiring already correct). Re-drive `verify_behaviour_218w3_overlay.py`
   green + break arm. Regenerate its showroom page.
3. **12-col grid page** (s218-D6): the column overlay paints BEHIND the demo content — in
   `knowledge/_render/gen_grids_218.py`, regenerate, re-drive `verify_grids_218.py --page 12col`.
4. **Photography gallery wall SQUARED** (s218-D6): the page's wall runs the squaring pass —
   `edge:square` enacted in `gen_foundations_217.py`'s photography body (scope: THIS page; the
   gallery ROLE's exemption elsewhere untouched — canon and the roles pages do not change).
   Regenerate; re-drive `verify_photography_218.py` (its hole-tolerance expectation flips to
   zero-holes for this wall; keep the settings mutation arm red).
5. **CI sweep → BLOCKING** (s218-D4): in `.github/workflows/gates.yml`, remove
   `continue-on-error` from the full contrast sweep job/step (the one labelled ADVISORY pending
   Banner 8). Update its label comment to name s218-D4. Do not touch other advisory jobs.

Fence: no rulings, no tokens/canon, no registry/serial, no store/lane/GM/LS/memory edits, no
commit/push. /var/tmp session-suffixed. Return: per-item receipt + verify tails, residuals priced.
