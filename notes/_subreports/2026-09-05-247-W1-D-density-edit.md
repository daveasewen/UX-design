# `#247`-`W1-D` — DENSITY: the lead group becomes one compact headline row (option 1)

session: `#247` · 2026-09-05
window: `W1 density · lane D (the edit)`
sub index: `W1-D`
brief: `notes/_briefs/2026-09-05-247-W1-density-brief.md` (ONE EDIT + GATES sections only)
tokens: `UNMEASURED — subagent cannot read message.usage; estimate ≈55K real (16 tool calls, one 270-line read, one 16-pane render)`

## VERDICT

DONE. Option 1 built: SIX `kpi-tile` at `data-c="1"`, compact variant (`.t-cm-figure-3`, 24px), in `knowledge/snippets/Template-dashboard-bento.reference.html` GROUP 1. It is square at every band by construction (6 tiles ÷ 6/3/2/1 columns = 1/2/3/6 full rows, remainder 0 at each) and the composition gate's C9 orphan arm confirms it (`_validate_composition.py` GREEN, C9 reds 0, exit 0). Rendered (not computed) at 1440 light: first chart top edge **675.7px → 516.5px** (−159.2px); the lead group **309.7px → 150.5px**. Options 2 and 3 were not needed and not built. `git diff --stat -- knowledge/` shows ONE file. Snippet gate exit 0 (136 snippets, 0 failures). `_validate_screen.py` NOT run; `_SCREEN-GATE.md` diff 0 lines. Row unit 120px kept (floor does not bind: compact tile measures 150.5px). Nothing of Dave's ruled — six-vs-four, order, DP-08 content on two tiles, and the two stale "only 6 and 3" comments are RSQs below.

COUNTS: findings `7` · ruling-shaped `4` · UNPROVEN `2`

## What was done

**The edit** — `knowledge/snippets/Template-dashboard-bento.reference.html`, GROUP 1 only (diff: 54 changed lines, `git diff | grep -c '^[+-]'`; HEAD sha `04099a8`).
- GROUP 1 comment (was L844–845) rewritten: what it now is, why six divides every band, that the 2×2 is the edit-pass option (s246-D5 named), that order is the specimen's not a ruling (DP-07 REVIEW).
- Four existing tiles: `data-c="3"` → `data-c="1"`; `.amt t-cm-figure-4` → `.amt t-cm-figure-3` (the compact variant per `kpi-tile.meta.json` variants[1] and `Kpi-tile.reference.html` L303–307 — a figure-class swap, no new CSS).
- Two tiles ADDED to reach six (DP-07 allows 3–6; option 1 says six): "Money in" (£71,880.00, +6.2% up vs July, up spark — points copied from Kpi-tile.reference.html's compact specimen L312) and "Card spend" (£3,204.80 — the same figure the Balances rail already carries — −1.4% down vs July, down spark). Both use the tile's existing markup verbatim; no new slot, class or CSS.
- Probe: `grep -c 'data-c="1"'` = 8 (6 tiles + 1 comment + 1 CSS rule L341); `grep -c 't-cm-figure-3'` = 7 (6 tiles + 1 comment).
- Nothing else in the file changed. `.c-bento.tpl-group-lead{ --bento-row-unit:120px; }` (L743) untouched.

**Seam check-in** (after edit, before gates): `git status --short knowledge/` = one `M` line for the snippet; the three other `M` files in the tree (`_rulings.json`, `_REHEARSAL-LOG.jsonl`, `_GRADE-DECISIONS.jsonl`) were dirty BEFORE this lane started (first `git status` of the lane) and are not mine.

**Gates**
1. `python3 knowledge/_validate_snippets.py` → `snippet gate: 136 snippet(s), 0 failure(s)`, **exit 0** (that is the whole output; one line).
2. `python3 knowledge/_validate_composition.py knowledge/snippets/Template-dashboard-bento.reference.html` → `GREEN — C9 reds 0 [BLOCKING] · C1 0 · C7 0 · C8 0 · C4 0 · unproven 0`, **exit 0**. C9 line for the group: `grid 'This month' line 854: 6 tile(s) data-c=[1,1,1,1,1,1] -> base [1×6]; <=1100 [1×6]; <=820 [1×6]; <=520 [1×6]`.
3. Render: Playwright installed per `knowledge/_ROBUSTNESS-PORTABILITY.md` recipe in 3 calls (pip 1.61.0; `NODE_EXTRA_CA_CERTS` install of chromium_headless_shell-1228; `apt-get download libxdamage1` → `~/.local/chromelibs`). 16 panes rendered via `goto(file://…)`, 0 page errors in all 16. Screenshots: `outputs/w1-density/template/{before,after}-{1440,1100,820,520}-{light,dark}.png` (before at 1440 only, after at all four bands; the runbook's inverted-compositor check passed — `body` background read off the DOM as rgb(240,240,240) light / rgb(26,26,26) dark, and the after-1440-light PNG was eyeballed: one row of six, chart below).
4. `_validate_screen.py`: NOT run (declared skip — it writes into `knowledge/`; the composition arm it chains was run directly). `git diff HEAD -- knowledge/_SCREEN-GATE.md | wc -l` = 0.
5. `_build_all.py`: NOT run (fenced).

## Findings

1. **First-chart-y at 1440 light, RENDERED: 675.7 → 516.5px** (`.tpl-group-evidence` bounding top; `outputs/w1-density/template/measure.json` keys `before-1440-light` / `after-1440-light`). Dark identical. Lead group height 309.7 → 150.5px. Chart top now sits 383px above a 900px fold.
2. **Square at every band, rendered**: after — 1440: 6 cols × 1 row · 1100: 3 × 2 · 820: 2 × 3 · 520: 1 × 6 (measure.json `cols`/`rows` per pane). Before — 6×2 · 3×4 · 2×4 · 1×4.
3. **Other bands** first-chart-y before → after: 1100: 989.3 → 671 · 820: 1057.3 → 893.5 · 520: 1081.6 → 1368.6. At 520 the row COSTS 287px (six stacked tiles vs four): the density gain is a wide-band gain and a narrow-band loss. Probe: measure.json.
4. **Row unit**: compact tile measures 150.5px (`tile0.h`, all after-panes) against the 120px floor — the floor never paints, so L743 is unchanged. (Before: display tile 156px; the 5.5px difference is the 32→24px figure, minus the line-height rounding.)
5. **DP-08 — what kpi-tile carries**: value (`.amt`), signed delta with arrow glyph + sign + word + NAMED period (`.delta .arrow` / `.t-cm-figure-6 "+4.8% up"` / `.per "vs July"`), and the sparkline in a slot (`.kpi-spark` → meta `slots.spark`, capability `trend-series`). All three DP-08 slots exist; no markup slot was added. No gauge/ring in the group (`grep -c chart-donut` = 0). BUT: two of the six tiles ("Awaiting approval", "Available overdraft" — pre-existing specimen content, untouched) fill the delta slot with a count/status ("6 payments · 2 to approve", "None used · Limit reviewed 4 Aug"), not a signed delta vs a named period — 4/6 tiles meet DP-08 by content, 6/6 by slot. Left as-is: content is the specimen's, not the brief's edit.
6. **DP-09 confirmed, not edited**: rule 7 at L746–751 (`.tpl-group > .c-bento__grid > .kpi-tile … border:0`) — the frame yields to the wall; keylines OFF (header L59). Composition C1 reads the group gap as 4px, the wall as 40px.
7. **Two comments in the file are now stale**: L73–74 ("Every wall here uses ONLY 6 and 3, and every wall holds an even number of 3s") and L837 ("SPANS: only 6 and 3"). The lead group now uses `data-c="1"` ×6, which is square by a different arithmetic (6 % cols = 0). Not edited — the brief says "Nothing else in the file changes". RSQ 3.

## RULING-SHAPED QUESTIONS

1. **Six or four?** Both are square-testable only one way: six is square by construction (built); four at `data-c="1"` orphans at the 3-col band (3+1) and was not built. The brief says if both are square the pick is Dave's — here only six is, so the question is whether six metrics is the RIGHT count for this role, not whether it is legal. (a) six as built · (b) four via option 3 (`--bento-columns:4` override + hand-copied band rules, the header's "third home" objection) · (c) five with a 3-col band rule. Recommend (a) on squareness alone; the count is DP-07's product judgement.
2. **Narrow-band cost** (finding 3): at 520 the first chart drops 287px. (a) accept — phones read the KPI column first anyway · (b) a `data-r`/collapse rule for the lead group under 520 (new band rule, the header forbids hand-copying one) · (c) a "show 3, reveal 3" pattern (new component behaviour, s234-D5 territory). Not recommended either way; it is a trade Dave has not seen.
3. **The two stale "only 6 and 3" comments** (L73–74, L837): (a) lane R or the wrap edits them to "6 and 3 on the wall; 1 ×6 in the lead group" · (b) leave as history until the 4px audit re-puts the file. Recommend (a) — a builder copying this file reads the header first.
4. **DP-08 on the two status tiles** (finding 5): (a) leave — they are "Stat card wearing a spark" specimens · (b) give them a signed delta vs a period · (c) demote them to Stat cards (meta's own anti-pattern: "never ship a KPI tile with an empty spark slot" — they have sparks, but flat/count content). Dave's; the brief forbade changing content beyond the edit.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN:** tile heights under the real HSBC face — the sandbox has no Univers Next, so 150.5/156px are fallback-face readings; the DELTA (row → one row) does not depend on the face, the absolute px do. Price: one render on a host with the font (~3K).
- **UNPROVEN:** whether `knowledge/canon/gen_canon_components.py` would change the `.cn-template-dashboard-bento` block in canon.css (L16684) from this edit. Not run (fenced by _build_all; canon outside the lane fence). The edit is markup-only (attributes, one class swap, two tile clones) so the CSS projection should be byte-stable; the block's "Aria:" line lists landmarks that did not change. Price: `gen_canon_components.py --check` (~2K) at the wrap. `showroom/` carries 0 references to this snippet (`grep -rl`), so no showroom regen is implicated.
- **CLAIMED:** `_validate_snippets.py` is "the" validator for this snippet — it globs every `*.reference.html` (L341) and reported 136; the header's "137 files" count is from #231 and was not re-verified.

## Evidence

`outputs/w1-density/template/` — `before-1440-{light,dark}.png`, `after-{1440,1100,820,520}-{light,dark}.png` (the eight after-panes + two before-panes the brief asked for), `measure.json` (all 16 panes: firstChart y/h, lead h, tile0, tiles, cols, rows, amt font-size, overflow flag, bodyBg, pageErrors), `_render_w1.py` (the script — the probe is re-runnable), `before-HEAD.reference.html` (the `git show HEAD:` copy used as the before arm; moved here from a temp path in `knowledge/snippets/` — the sandbox blocks `rm` on the mount, `mv` was the way out, and `git status` confirms `knowledge/snippets/` holds only the one M).

REPLAY-THESE: `outputs/w1-density/template/after-1440-light.png` (~1.5K tk as an image) · `outputs/w1-density/template/measure.json` (~1.2K tk)
