# #304 W5b — the sitting page for Tuesday 29 September: 53 calls in six groups, the one decision named, rendered and looked at

provenance: 304 · Sunday 2026-09-27 · seat W5b (Fable 5.1, judgment) · mount HEAD `3100da99` · read-only on the mount except the page, `notes/_lanes/304/W5b/` and this report · no `git status`, no git writes, no commit, no Project memory, no store write, nothing inscribed
status: observed for every count (each is quoted from a report named on the page); the recommendations are this seat's readings
window: UNMEASURED (a seat cannot read its own usage)
COUNTS: calls 53 in 6 groups (release 4 · looks 9 · brain 14 · lines and housekeeping 14 · Apollo-MCP 10 · Jev 2) · decision boxes 55 (53 + Friday context + whole page) · renders 2 (1440, 390): scrollWidth = viewport both, 0 elements past the right edge, 0 clipped overflow boxes, 0 broken images, 0 page errors · page height 36,771 px at 1440 and 60,887 at 390 (full-page shot skipped above 14,000; 37 + 61 viewport slices in `shots/`) · embedded renders 24, all copied from V3, W4a, R3, R6a, R6b, R4s and R4s2, none redrawn
CITES: the plan (`notes/_PLAN-304-roadmap-and-weekend-runs-2026-09-26-v1.html`) · the six `_DECIDE-304-*` pages · `_REVIEW-304-v1013-vs-candidate-…` · `_REVIEW-304-candidate-2-…` · `_PROPOSAL-apollo-mcp-2026-09-26-v2.html` · reports A1–A4, F, M, R1–R6b, V1–V4, C1–C4, W3a–W3c, W4a–W4b, R4s, R4s2, J · s261-D4 · s234-D5 · s294-D10 · s295-D3 · s245-D10 · s277-D12

## THE ANSWER FIRST

**The page:** `notes/_SITTING-304-tuesday-2026-09-29-v1.html`. One page for a one-hour sitting: the answer first (what the weekend nailed, with the CI read-backs by run id; what it did not; the one decision that matters most), then 53 calls merged and de-duplicated across the plan's ten decisions, the six decision pages' forty calls, the proposal's six and the weekend's fifteen new items, in six groups ordered by how much work a yes unblocks, then what runs next on each answer and what stays parked, a context box for what came back from Friday, and a Technical footer with ids, shas, CI run ids and paths.

**The one decision:** cut v1.0.14 from candidate 2 on Tuesday (call 1). R4s and R4s2 disagree on the condition; the page shows both side by side and takes R4s2 (the three unmet R4s conditions are calls 4, 5 and 11, each waits on Dave and each is in v1.0.13 already).

**One yes takes forty:** groups 3 to 6 (calls 14–53) carry a recommendation each and can be taken on one "yes to the recommendations" in the whole-page box. Groups 1 and 2 (calls 1–13) want his eye; each has the picture where there is one (KPI crop three ways, thinning before/after, markers today/option, ring fill/narrow, ground light and dark, badge 7/8, console before/after, v1.0.13 against candidate 2).

## THE CALLS, BY GROUP

1. **The release (1–4):** cut from candidate 2 · ship the two gates and name the roster 60 · keep them advisory through the cut · the chart receipt names the meta's script (dv-render.js; this seat's reading, flagged).
2. **How things look (5–13):** KPI label — the clip-visible form (V3's alternative; keeps the s261-D4 lock-up, costs one descender-gate leg) · ratify label thinning (shipped unruled at `3100da99`: hidden at all, 8px, last-category anchor) · markers off above 12 with end marker and one letter per band · ring tile hugs and a narrow-column when-rule · ground light (his sentence) and dark (section one step below the tiles, minted) · solid inks for the two 3.7:1 labels · full-height app-shell form · badge 8px · console radius set accepted with the derived card padding.
3. **What the brain says (14–27):** the six schema calls (R6a) · the six when-rule calls (R6a) · step 5's four edge types yes, lifecycle as a field, content standard parked · the notification border as one number token · the skill lane's two widenings (width ban; reader first) ratified.
4. **Lines and housekeeping (28–41):** window lines and stop/tolerance · boot ceiling 130,000 until the Mac seat (his word over his word twice; the 19:47 correction from R6b carried) · credential helper before the push · the eleven housekeeping calls (R6b) · the ten uncertain-stamp calls (R6b) folded to three · the three remaining CI calls (declare, port now, retire; the three-chart-one-table correction carried).
5. **Apollo-MCP (42–51):** the proposal's six (route B, PoC as scoped, Jev ranker behind a switch, Apollo Live, data-only for money, when to start) · the delivery-shape three · the probe's motion-check question. On "when to start" the page takes the plan (October, after the schema calls) over the proposal's "now", and says so.
6. **Jev (52–53):** hand-run suggester on four edge types with the two-band rule, never a gate · the 1,135 code-only node titles fixed mechanically.

Where a verifier and a lane disagree the page says so and recommends: R4s v R4s2 (call 1), W3a v V3 (call 5), proposal v plan (call 47), W4a's thinning shipped on V4's recommendation (call 6).

## THE W5A SLOT

`notes/_subreports/2026-09-27-304-W5a-gate-bugs-and-trim.md` was not on disk at build time (`notes/_lanes/304/W5a/` held `test_icons_markup.py`, `gates/`, `probe/`). The page carries a clearly marked slot after call 41 ("numbered 41a onward") and names W5a's two gate-code fixes as what runs before the cut. If W5a raises a call, the conductor adds it to the slot in `page.src.html` and re-runs `render.py`.

## BUILD AND RENDER

- `notes/_lanes/304/W5b/page.src.html` → `build.py`: copies both house style blocks and the decisions overlay from `notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html` (asserting each anchor occurs exactly once); overlay changes and only these: page id/title/path; `skip` keeps a section box only on `#friday`; that box's kind reads "Context" instead of "Section"; decision boxes keyed on `.decide > li` with the `b` title as in the proposal. Adds one CSS block (`.rec`, `.why`, `.more`, `.specs`, `.clash`, `.crop`, `.one`, `.slot`, phone rules).
- `render.py` builds then renders with Playwright at the seat (`executable_path=$RENDER_SHELL`, `file://` goto), 1440 and 390, forces lazy images eager, scrolls to the foot, checks scroll width, off-edge boxes, clipped overflow boxes, broken images, page errors, box and call counts; writes `shots/sitting-w{1440,390}-partNN.png` and `render_report.json`. One call: `cd "$HOME/mnt/Projects--UX-design" && export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh; python3 notes/_lanes/304/W5b/render.py`.
- Looked at by eye: 1440 parts 00, 01, 03, 05, 06, 09, 33; 390 parts 00, 06. Fixed on sight: the house `.beats b{display:block}` rule was breaking the recommendation line after its bold lead (one CSS line); the three 4x descender crops were unreadable three-up and now stack full width.
- Page text uses the house Helvetica stack as the proposal page does; every embedded render carries the real face from its own lane.

## NOT DONE, BY FENCE

No git write, no `git status`, no commit, no Project memory, no store write, nothing inscribed. No new render was made of any Apollo artefact: every picture is a copy of a lane's or verifier's file. The mapping of the plan's ten decisions onto the calls is in the page's Technical footer and is this seat's; the count 53 is measured by the render (`calls: 53`).

## FILES

- `notes/_SITTING-304-tuesday-2026-09-29-v1.html`
- `notes/_lanes/304/W5b/`: `page.src.html`, `build.py`, `render.py`, `shots/` (render_report.json + slices)
- this report

## `_state` doc row (spec)

```json
{"id":"W-304fb","title":"#304 W5b filed report - the sitting page for Tuesday 29 September: 53 calls in six groups ordered by work unblocked, the v1.0.14 cut named as the one decision, 24 renders copied not redrawn, rendered at 1440 and 390 with no overflow","home":"notes/_subreports/2026-09-27-304-W5b-tuesday-sitting.md","links":["notes/_SITTING-304-tuesday-2026-09-29-v1.html","notes/_lanes/304/W5b/page.src.html","notes/_lanes/304/W5b/build.py","notes/_lanes/304/W5b/render.py","notes/_lanes/304/W5b/shots/render_report.json"],"project":"apollo","opened":304,"state":"open","owner":"dave","condition":"stated","body":"s218-D7 filed report, #304 seat W5b (Fable judgment). Merges the plan's ten decisions, the six decision pages' forty calls, the Apollo-MCP proposal's six and fifteen weekend items into 53 calls in six groups (release 4, looks 9, brain 14, lines and housekeeping 14, Apollo-MCP 10, Jev 2); groups 3-6 take one 'yes to the recommendations'. Disagreements shown and recommended: R4s v R4s2 (cut), W3a v V3 (Kpi-tile form), proposal v plan (when to start MCP), W4a thinning shipped unruled. W5a slot left after call 41.","closes_when":"Dave has sat with the page and exported his rulings (DAVE-RULINGS-*-sitting-304-tuesday-v1.md dropped in notes/_lanes/304/), and the conductor has inscribed or parked each of the 53 by his words"}
```
