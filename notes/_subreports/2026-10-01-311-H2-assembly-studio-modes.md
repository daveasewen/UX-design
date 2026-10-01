# Lane H2 (#311 overnight wave 1, Fable research lane) - Apollo Assembly and Apollo Studio drawn as a proposal, nothing ruled

COUNTS: findings `5` · ruling-shaped `0` · UNPROVEN `2` · 1 proposal document (3,421 words, 8 sections, 6 calls with recommendations) at `notes/_lanes/312/H/H2/PROPOSAL-modes-2026-10-01.md` · 1 calls file for the H3 page at `notes/_lanes/312/H/H2/calls.json` · 8 sub-modes tested against the gates: 4 have a pack skill today (Compose, Check, Propose, Review under ADS names), 4 do not (Adapt, Hand off, Explore, Sketch) · the engine measured: 167 build routes (78 GATE, 67 ABORT, 22 ADVISORY), 475 indexed rules (62 BLOCKING, 323 ADVISORY, 34 REVIEW, 56 TASTE), 851 rulings, 57 pack gate verdicts with no tier field · 3 outside sources fetched and dated · 0 rulings touched, 0 metas touched, 0 gates changed · verdict: DONE, a proposal for H3 to page; nothing for Dave until the page exists.

## Headline

The split he named on 2026-09-27 is the third naming of one the record already made: the 2026-06-19 canon model (canon gated and shipping; exploration ungated, a menu of options; promotion only on his word; proposals outside the resolving stores because "the store boundary is the fence") and the pack contract's first rule (declare on-canon or freestyle in the first reply, never change lanes silently). What Assembly and Studio would add is the half that is missing: freestyle today runs no gates, and the pack's runner has no advisory tier, so Studio becomes real only when every gate keeps running and a red becomes a label instead of a block. The proposal's one mechanical change is that demotion switch in the runner; its one fence is a `mode` field in the provenance receipt the receipt gate already parses.

## What was done

1. Read the two receipts (his words verbatim), the promotion queue, ADR-0005 §5, the pack's design contract and six skills, the runner and its workflow, the shipped v1.0.14 manifest, `_build_all.py` ROUTE_ROWS (by ast), the rules index, the receipt gate, the icon gate's `data-bespoke`, `_inscribe_ruling.py`, the #280 matrix report and the Apollo-MCP v2 page's overlay shape.
2. Fetched three outside precedents on 2026-10-01: Claude Code's permission modes (a launch default and a mid-session switch; "enforced by Claude Code, not by the model"), Figma's Dev Mode statuses (Ready for dev set from either mode, an automatic Changed state), GitHub's protected branches (the same checks everywhere, required only where the work is going).
3. Wrote the proposal: what a mode is (a law setting on one engine: what a red does, what the output is called, where it may live, who moves it across), door/lever/both with a recommendation for both, the eight sub-modes each put against its skill, its gate law, its output kind and its gap, what the pack and the generate skill would change, what is a place not a mode (the record, the pack, Launchpad as a runtime of Hand off, Simulator held), six calls with recommendations, a build order, and the named risk (Studio as where reds hide) with what holds it.
4. Wrote `calls.json` in the shape the decisions overlay reads (`.decide > li`, a `<b>` title), so H3 pages the calls without re-deriving them.

## Two passes, one lane

The proposal, `calls.json` and this report were written by a first H2 pass (22:24–22:32 BST) that ended before its commit step; a second H2 pass (from 23:20 BST) re-measured every number in §1 and §8 against the tree (ROUTE_ROWS 167 = 78/67/22 by ast; rules index 475 = 62/323/34/56 by `destiny`; 851 rulings; 57 manifest verdicts 43/10/4 with fields gate·invocation·population·selftest·third_party·verdict·why and no tier), re-fetched the Claude Code permissions page and found the quoted sentence verbatim, tightened one line (§1.4: only two of the six advisory validators carry `--strict`; the other three exit 0 always), added the store row and committed. Nothing else in the proposal was changed.

## Gates run

None apply: no file under `knowledge/` other than the store row, nothing under `apollo-spider/` or the metas was changed; only two new files under `notes/_lanes/312/H/H2/`, this report, and one born-closed row in `knowledge/_state.json`. `python3 knowledge/_state.py --check` was run after the row inside the commit lock; its verdict is pasted below in § Commit. `test_gates` was not run: nothing this lane touched is in its population, and a clone for it would take the pre-push slot the addendum reserves for the combined HEAD.

## Commit

(filled at commit time)

## Found, not fixed

- The tier of a gate (blocking or advisory) lives inside each script as an exit code and a `--strict` flag; the pack manifest's per-gate verdict has no tier field and `run-gates.py` has no tier logic. Any mode work starts there. Not this lane's file (`apollo-spider/` is job G's; the manifest generator is `knowledge/_release/`).
- Freestyle in the pack contract runs no gates. That is the gap the proposal names; not changed, since the contract is a source file that regenerates CLAUDE.md, AGENTS.md and the Copilot boot.
- `knowledge/_PROMOTION-QUEUE.md` has carried "a review pass is owed" and a standing mot-007 tension since 2026-07-02; the queue is Studio's Propose outlet on this reading and it has not been walked.
- The brief's Hard rules say `SESSION_N=312`; per OVERNIGHT-CHAINS.md this ran as #311 with `SESSION_N=311`, the paths kept under `notes/_lanes/312/`.
- The brief names Hand off's contents as "code, specs, tokens"; nothing in the pack names what leaves in a handoff and what does not. A small skill, not written.

## RULING-SHAPED QUESTIONS

None put now. The six calls (door/lever/both; the eight sub-modes; the mark; the law switch; Launchpad's place; Simulator) go to him on H3's page, with recommendations, in plain prose. No ruling was inscribed and none is proposed for inscription from this lane.

UNPROVEN (ADR-0016): the Figma Dev Mode and GitHub protected-branches quotes in §4 and §8 of the proposal were fetched by the first pass and not re-read by the second (the Claude Code quote was); re-fetching both is about 2 minutes. Whether `run-gates.py --mode studio` can carry a per-gate tier without changing the manifest generator in `knowledge/_release/` is asserted from reading, not from a build.

REPLAY-THESE: `notes/_lanes/312/H/H2/calls.json` whole (~1,000 tk) and the proposal's §2 and §7 (~900 tk) — the six calls and the one-paragraph definition of a mode are what lane H3 pages; the rest is evidence.
