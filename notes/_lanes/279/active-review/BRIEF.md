# LANE AR — BRIEF — the manual review sheet for the 15 icon bases with 2–3 "active" drawings (P-277-3)
#279 · 2026-09-16 · instrument for Dave's review under `s277-D6` · written by the conductor (Fable 5.1) · **model: fable** · swiss-design-system idiom (`/sessions/laughing-elegant-feynman/mnt/.claude/skills/swiss-design-system/SKILL.md` — read it)

## Why — `s277-D6`, read WHOLE in `knowledge/_rulings.json`
The `-2/-3` suffix on 31 "active" icons is the exporter's slug-collision counter, so the bare `-active` slug is Figma enumeration order, not the base's twin. Dave reviews the 15 bases MANUALLY; until then no base carries a default and each of the 31 is a declared null. His note named a SECOND defect the review must catch: glyphs under an `-active` slug that are their own icon and "should have an in-active version". Dave said today: *"I need to do the manual review of the 31"*.

## Inputs
- The 15 bases + 31 actives: `knowledge/_icon_nodes.json` (the 15 `defaultActive` declared nulls name every active per base; `activeVariantOf` edges give active→base). SVGs under `knowledge/assets/icons/` per the manifest `file` field.
- The prior sheet on `notes/_lanes/277/icons-propose/REVIEW-icons-2026-09-16-v2.html` (RI-3 card) and its builder `_build_page_v2.py` — the export shape Dave's exports use (`DAVE-EXPORT-2026-09-16.json`) — REUSE the export JSON shape and the page's export button mechanics so the inscribe tooling can read it.

## The page — `notes/_lanes/279/active-review/REVIEW-active-2026-09-16.html`, single file, inline CSS/JS/SVG
- One row per base (15). Left: the base glyph, large (48px) and small (16px), light and dark chrome side by side. Then each active candidate (2 or 3), same two sizes × two themes, labelled with its slug and its Figma name, `fillMode`, and the manifest `group`.
- Per base, ONE choice, radio: (a) `<slug>` is the twin — one radio per candidate · (b) none of these is the twin · (c) FLAG: a candidate is its own icon and needs an inactive version drawn — with checkboxes per candidate so he can flag more than one, plus a free-text note.
- Plain prose only for Dave: no ids like `s277-D6` in the body copy; the ruling id sits once in a small footer line. No integers typed into the HTML that the build can compute — every count is derived at build time from the node file.
- Progress line at the top ("7 of 15 decided"), decisions persist in localStorage, **Export** button writes the same JSON envelope as the v2 page (`{exportedAt, page, answers:{<base>: {choice, twin, flags[], note}}}`) — read `_build_page_v2.py`'s export function and match it.
- Screenshot in a NEVER-DRIVEN fresh context (cleared localStorage) — light + dark, 1280 + 390. Chromium: lane EX's workaround is in `notes/_lanes/279/explorer/REPORT.md` (`/tmp/pw` headless-shell + `/tmp/lib`, `PLAYWRIGHT_BROWSERS_PATH=/tmp/pw LD_LIBRARY_PATH=/tmp/lib`) — it may still be on disk; `/sessions` is at 99%, do NOT download a second browser; if `/tmp/pw` is gone, say so and ship without screenshots rather than fill the disk.
- A driver `_drive_review.py` that opens the page, ticks one of each kind, exports, and asserts the JSON shape — then a fresh context for the screenshots.

## Gates
Builder `_build_review.py` derives everything from `_icon_nodes.json` + the SVGs; asserts 15 bases / 31 candidates; every SVG file exists; `node --check` on the inline script if it is extracted; the export round-trip. No repo file outside `notes/_lanes/279/active-review/` changes.

## Report — `notes/_lanes/279/active-review/REPORT.md` + `notes/_subreports/2026-09-16-279-AR-active-review.md` (+ `_state.json` row W-279ar via `_state.add()`, W-279rd shape, close condition = Dave's export received)
Commit via `SESSION_N=279 SHOWROOM_ACK=1 bash knowledge/_git_commit.sh --reconciled <fresh msgfile> <paths…>`, msgfile `/tmp/_msg-279-AR-$(date +%s).txt`, bare subject `#279 lane AR: the 15-base active review sheet for Dave — P-277-3 instrument`. Regenerate `_CHAIN.md` if the store row trips the chain gate. Locks → `mv` to `.git/_orphan-locks/`. Never `git stash` / `gen_kg_edges.py` / `_build_all.py` / `_build_kg_explorer.main()`. Bash root `/sessions/laughing-elegant-feynman/mnt/UX-design/`.
