# Lane H2 (#311 overnight wave 1, Fable) — Apollo Assembly and Apollo Studio, as a proposal

For lane H3 (the proposal page with his decisions overlay). Nothing here is ruled. The names Assembly, Studio and Launchpad are his (Sun 2026-09-27, 10:54 and 10:58 BST, `notes/_receipts/2026-09-27-304-sq-assembly-studio-modes.md`); everything else is the seat's expansion, and every claim about the tree was measured on 2026-10-01 at the seat and is cited to its file.

Written 2026-10-01, overnight, from the repo at `$HOME/mnt/Projects--UX-design` and three outside sources fetched the same night (§8).

## 0. The verdict in four sentences

The split he named is not a new idea for Apollo; it is the third naming of one the record already made. On 2026-06-19 he decided a two-tier canon model (canon, gated, ships; exploration, not gated, a menu of options) joined by an explicit promotion path, with proposals kept outside the resolving stores until his sign-off moves them in (`knowledge/_PROMOTION-QUEUE.md`). The pack already makes every Copilot declare a lane in its first reply, on-canon or freestyle, and never change lanes silently (`apollo-spider/cold-start/DESIGN-CONTRACT.md` rule 1). What Assembly and Studio would add is the missing half: today's freestyle runs no gates at all, and the pack's runner has no advisory tier, so the modes become real only when the gates keep running in Studio and the runner learns to label instead of block.

## 1. What already exists, measured

Read this section as the ground the proposal stands on. Each line is a fact of the tree on 2026-10-01, with its file.

1. The canon model, decided by Dave 2026-06-19 (`knowledge/_PROMOTION-QUEUE.md`, lines 3–14). Two tiers: canon is the gated `snippets/*.reference.html`, token-faithful, enforced by the build gates, "this is what ships"; exploration is the `_fitness-test/*-AB-showcase.html` files, "the unconstrained quality ceiling", "NOT canon, NOT gated", "a recorded menu of options". Promotion is three steps (tokenise, write into the meta, add to the gated reference) and happens "only when Dave explicitly blesses it". The sentence that matters most for the modes, learned 2026-07-02: "Token proposals live in `tokens/_proposals/` — OUTSIDE the resolving stores — until Dave's sign-off physically moves them in. A `$confidence` tag is not a fence; the store boundary is the fence." Both folders exist today (`knowledge/_fitness-test/`, `knowledge/tokens/_proposals/` with six proposal files).
2. The pack's lane declaration (`apollo-spider/cold-start/DESIGN-CONTRACT.md`, rule 1 and rule 4). "Declare the lane, in your first reply. Before you build, say which one you are in: on-canon — working through the design skills in `skills/` — or freestyle. On-canon is the default. Freestyle happens only when the designer asks for it in words. Never change lanes silently." Rule 4: a non-Apollo skill used for design output is freestyle and must be declared and named, because "an undeclared source is what turns a design problem into an unreadable bug report." This is a lever, declared per reply, with a default; it is not a door.
3. The advisory tier in the engine. `knowledge/_build_all.py` ROUTE_ROWS holds 167 steps: 78 GATE, 67 ABORT, 22 ADVISORY (counted by ast on 2026-10-01). ADR-0005 §5 (2026-07-02): "New checks enter at the advisory tier and earn promotion to blocking by being bite-tested." The rules index carries the same idea for prose rules: 475 rules, 62 BLOCKING, 323 ADVISORY, 34 REVIEW, 56 TASTE (`knowledge/guidelines/_rules-index.json`, counted the same night). So the engine already has two laws for one check; what it lacks is a switch that picks the law by the work's purpose rather than by the check's age.
4. Where the tier lives: inside each script, not in the runner. `_validate_advisory.py` "ALWAYS exits 0 — advisory annotates, never blocks"; `_validate_geometry.py` and `_validate_own_size.py` exit 0 whatever they find "unless `--strict`"; `_validate_theme_provenance.py`, `_validate_hidden_display.py` and `_validate_edge_extremity.py` exit 0 always and have no `--strict` at all (re-read 2026-10-01 22:20 UTC: "always exits 0", "never blocks, never writes", "Exit 0 always (advisory)"). The promotion direction exists as a flag on two of the six (`--strict` makes an advisory gate block); the demotion direction (run a blocking gate as a label) does not exist anywhere.
5. The pack's runner has no tier at all. `apollo-spider/ci-template/run-gates.py` reports three verdicts, pass, FAIL, COULD-NOT-ASK; the shipped manifest's per-gate verdict carries `gate`, `invocation`, `population`, `selftest`, `third_party`, `verdict`, `why` and nothing about tier (`notes/_lanes/305/V2/cold/Apollo-Spider-v1.0.14/_MANIFEST.json`: 57 gates, 43 RUNNABLE, 10 REPO-BOUND, 4 NEEDS-DEP). A gate that is advisory in the repo is advisory in the pack only because its script exits 0; the runner does not know why. `gates.yml` says the rule out loud: "To turn a check off, DELETE ITS STEP. Do not add continue-on-error to hide a red."
6. The pack's six skills (`apollo-spider/skills/*/SKILL.md`): ADS-grill-me (the brief, six questions, skips recorded), ADS-generate-from-canon (compose, never trace; "Only what exists"; a Gaps list when something is missing), ADS-draft-a-new-pattern ("the creative mode"; "a reviewable draft, not adopted canon"; Route C contract turns a sketch into a candidate), ADS-check-with-gates (the mechanical half), ADS-check-against-design-system (the reading half; "Green gates are not a pass"), ADS-usability-review ("a screen can be perfectly conformant and perfectly gated and still be confusing"). Four of his eight sub-modes already have a skill under another name (§3).
7. The record. `knowledge/_rulings.json` holds 851 rulings, status ruled or enacted; `_inscribe_ruling.py` is "THE ONLY SANCTIONED WAY TO APPEND A RULING", with five loud refusals and Dave's words required in `says`. The decision mechanism runs question, options, recommendation, his answer, ruling (#281's recommendation on every set), and the #280 layout matrix is the case where a matrix of rendered cells got a ruling that four sketches had not (`notes/_lanes/280/layout-matrix/REPORT.md`).
8. The provenance receipt (`knowledge/_validate_receipt.py`, s234-D6, s235-D1/D2). A composed page carries `#provenance-receipt` in its head: pack version, and one row per spliced region with the sha256 of the page's own bytes. The gate re-hashes and compares, so "did you invent this?" is a comparison, not a judgement. `data-bespoke="why"` on an svg is the one existing way to mark a deliberate departure so a gate reads it as a decision (`_validate_icons.py`).

## 2. What a mode is, on this reading

A mode is a law setting on one engine. Same canon, same gates, same record; four things change and nothing else:

1. What a gate does with a red. Assembly: a blocking gate blocks, as now. Studio: every gate still runs, and a red becomes a label on the output, in the gate's own words, with the file and line.
2. What the output is called. Assembly: shippable, canon. Studio: a proposal, marked not-canon, in its receipt and on its root.
3. Where the output may live. Assembly: in the resolving stores and the ship set. Studio: outside them, in the places the 2026-06-19 model already named (`_fitness-test/`, `tokens/_proposals/`, the promotion queue), and now the matrix pages.
4. Who moves work across the line. Only promotion, only on his words, only through `_inscribe_ruling.py` and the three-step path already written down. A Studio output never walks into Assembly; what walks is the ruling, and Assembly re-composes from what was promoted.

The test of the reading is that it is what the pack contract already says about lanes, with the gates added to the second lane. Freestyle today is Studio with the gates switched off; the proposal switches them back on and changes what a red does.

## 3. The sub-modes, tested against what the gates do in each

The eight sub-modes were the seat's list on 2026-09-27, not his. Here each is put against the skill that exists today, the law its gates would run under, the kind of output it makes, and what is missing.

Assembly, gates block, one recommended output, shippable:

1. Compose. Skill: ADS-grill-me then ADS-generate-from-canon. Gates: the screen gate (compose, icons, a11y over the file), the receipt gate first, the snippet contract, all blocking. Output: a page whose every region hashes to a canon splice. Missing: nothing; this is the pack as shipped.
2. Adapt. Skill: none. Change an existing output within the rules. Gates: as Compose, plus the receipt re-hash is the whole point (a region that stops hashing is an edit that left canon). The layout dials already have this shape (`_bento_edit_rails.json`; s248's edit mode). Missing: a skill, and it is a small one, because it is Compose starting from a receipt instead of a brief.
3. Check. Skill: ADS-check-with-gates and ADS-check-against-design-system, which already say they are two halves of one act. Gates: all of them, blocking, plus the reading. Output: a verdict with the gate's words. Missing: nothing. "Say why it fails" is already how every gate reports.
4. Hand off. Skill: none as a skill; ADS-generate-from-canon outputs React or HTML, and the pack's frozen-release and ship-list gates govern the pack, not a handoff. Gates: the pack gates on the handed-off files, blocking, and the receipt travels with them. Missing: a skill that names what leaves (code, specs, tokens, the receipt) and what does not. On the seat's 2026-09-27 reading, Launchpad is Hand off at runtime, so its gates are the strictest of the three, not the loosest; that reading is not his and belongs on the page as a call, not a fact.

Studio, gates advise and label, many outputs, proposals marked not-canon:

5. Explore. Skill: none; this is the permutation matrix (lane H1's research, `notes/_receipts/2026-09-27-304-sq-permutation-matrix.md`). Gates: every cell runs the gates and wears its reds as labels, so a cell that would be refused in Assembly is shown with the reason rather than hidden or quietly dropped. The matrix's honesty depends on that: a grid where the refused cells vanish is the dot-to-dot book with extra steps. Output: a pick, with his sentence, recorded as evidence; picks on the same axis across matrices become a candidate ruling by promotion. Missing: the whole thing; the #280 matrix is the hand-built precedent.
6. Sketch. Skill: none; today this is freestyle. Gates: all run, none block; the receipt gate marks every region that does not hash as bespoke, the way `data-bespoke` already marks a custom glyph. Output: a fast, loose page that says on its face which parts are canon and which are not. Missing: a governed freestyle. The change to the five rules is one word: "never invent" becomes "never invent silently".
7. Propose. Skill: ADS-draft-a-new-pattern, which already calls itself "the creative mode" and already produces "a reviewable draft, not adopted canon", and already says that signing the Route C contract "is what turns a sketch into a candidate". Gates: the token-manifest contract, `_validate_snippets.py`, `_validate_coverage.py`, run as the door into the promotion queue. Output: a candidate in `tokens/_proposals/` or the promotion queue, outside the resolving stores. Missing: nothing in the skill; the queue's "review pass is owed" line has stood since 2026-07-02.
8. Review. Skill: ADS-usability-review for the heuristic pass, and the review page with his decisions overlay for his eye (`notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html`'s overlay, which "saves in this browser and exports markdown"). Gates: none; the output is a sentence, and the sentence is what gets inscribed. Missing: nothing.

On the open question whether Check and Review are one thing seen from two sides: the pack's own skills answer no, in their own words. Check is the machine's verdict on construction and it can be green while the thing is wrong ("Green gates are not a pass"); Review is a person's verdict on the thing, and its output is a sentence, not a pass. They sit in different modes because their outputs go to different places: a Check verdict goes back to the page, a Review sentence goes to the record. Recommendation: keep both.

## 4. Door, lever, or both

Three outside precedents, all fetched 2026-10-01 (§8), and all three say both.

1. Claude Code's permission modes are set at launch (`defaultMode` in settings) and changed mid-session; the docs' modes table lists default (Manual), acceptEdits, plan, auto, dontAsk, bypassPermissions. The line that matters here: "Permission rules are enforced by Claude Code, not by the model. Instructions in your prompt or `CLAUDE.md` shape what Claude tries to do, but they don't change what Claude Code allows." A mode written only in SKILL.md prose is a wish; the runner has to hold it.
2. Figma's Dev Mode statuses: "Ready for dev" and "Completed" are set by designers, "while editing designs or in Dev Mode", and a marked design that is then edited gets an automatic "Changed" state that "cannot be set manually". That is a promotion mark with an automatic staleness flag, set from either side of the line. Apollo's receipt already does the staleness half (a receipt is valid against the pack version it was minted from).
3. GitHub's protected branches: required status checks "must have a successful, skipped, or neutral status before collaborators can make changes to a protected branch"; the same checks run elsewhere and merely inform. Same gates, two laws, chosen by where the work is going, not by which check it is. That is the cleanest model of the whole proposal: Assembly is the protected branch, Studio is every other branch, promotion is the merge, and the review is his.

Recommendation: both, with Assembly the default and the lever moving by named triggers, never silently.

1. The door is the brief, not a question. ADS-grill-me already records every skipped question as "a decision left open". A brief with two or more decisions left open (skips, or open discovery items) is the engine's cue to offer Studio's Explore, in the reply, before building. A brief that settles everything starts in Assembly and says so, which is what rule 1 of the contract already requires.
2. The lever from Assembly to Studio has two triggers: a gate refuses (Sketch or Propose, offered in the refusal's own words), or the person asks in words (today's rule for freestyle, kept). The engine names the move in the reply and marks the output.
3. The lever from Studio to Assembly is promotion only. A Studio output is not carried across; a ruling is, and Assembly re-composes. This is the store-boundary fence from 2026-07-02 applied to modes.
4. A front-door choice on its own is the wrong shape for the reason the seat gave on 2026-09-27: it asks the person to know which mode they need before they understand the brief. Kept as a rejected option on the page so he can pick it if he disagrees.

## 5. What it would mean for the pack

Five changes, in the order they should land if he rules for it, smallest fence first.

1. The mark (the fence). The provenance receipt gains one field, `mode`, and its regions gain a kind for the unhashed ones (proposal or bespoke, the existing word). The page root carries the same mark as an attribute beside `data-apollo-theme`. `_validate_receipt.py` in Assembly reds any page marked studio, so a Studio output cannot ship by accident; in Studio it lists the unhashed regions instead of refusing. One gate, both directions, the same check.
2. The law switch in the runner. `run-gates.py --mode assembly|studio` (assembly the default). In studio a FAIL is written as a label into the page's receipt and the runner exits 0 for it, in the gate's own words; COULD-NOT-ASK stays a refusal in both modes, because a gate that could not look is not a label. The tier (blocking or advisory) travels in the manifest's per-gate verdict so the runner reads it instead of inferring it from an exit code. This is the one mechanical change, and it is the demotion direction the engine does not have today.
3. The contract rename. DESIGN-CONTRACT rule 1: on-canon becomes Assembly, freestyle becomes Studio, and the sentence "Freestyle happens only when the designer asks for it in words" gains the two triggers from §4. The five rules stay; "Never invent" reads "Never invent silently" in Studio. `gen_projections.py` regenerates CLAUDE.md, AGENTS.md and the Copilot boot from the one source, as it does now.
4. The skills. Four exist (Compose, Check, Propose, Review, under ADS names); four do not (Adapt, Hand off, Explore, Sketch). Adapt and Sketch are thin; Hand off is a naming of what already leaves; Explore is lane H1's build and the largest by far. None of them is needed for the modes to be real; the mark and the switch are.
5. The brief. ADS-grill-me's skip count becomes the Explore trigger; no new question is added.

For the generate skill specifically: one paragraph at the top, after the two failures it rules out. In Assembly the skill is unchanged. In Studio the Gaps list is not a stop; it is Propose's intake, and every gap becomes a marked region in the receipt. The "Only what exists" rule is not relaxed; what changes is that a gap is shown rather than refused.

## 6. What is a place, not a mode

1. The record: `_rulings.json`, `_state.json`, the knowledge graph and its explorer, the showroom. Both modes read it; only `_inscribe_ruling.py` writes it, on his words; promotion is the only path in. His 2026-09-27 line ("the record is a place, not a mode") is already how the tree is built.
2. The pack is a place: one bake from one commit, byte-identical (`build-designer-pack.sh`); the mode is a setting on how the pack is used, never a second pack.
3. Launchpad, on the seat's reading and not his: a runtime of Assembly's Hand off, running in someone else's product with no designer watching (route B, ruled 2026-09-27 at the sitting, `notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html`). Not a mode; the strictest consumer of one.
4. Simulator: held, per his 11:07 addendum ("we might keep simulator for something else"). The seat's reading that it is a stage every output passes through, from any mode, stays a reading. Not on the page as a call unless he wants it.

## 7. The calls for the page (recommendations, nothing decided)

1. Door, lever, or both. Options: door only; lever only; both. Recommendation: both, Assembly default, the lever moved only by named triggers (open decisions in the brief; a gate refusal; the person's words), and the return by promotion only.
2. The sub-mode lists. Options: the eight as listed; fold Check into Review; fold Adapt into Compose. Recommendation: the eight stand; Check and Review stay apart because their outputs go to different places; Adapt stays because its test (the receipt re-hash) is different from Compose's.
3. The mark on Studio outputs. Options: receipt field plus root attribute, read by the receipt gate; a folder convention only; nothing. Recommendation: receipt plus root, read by the gate, because the store boundary is the fence and a tag on its own is not (his 2026-07-02 lesson).
4. The law switch. Options: a runner flag with the tier in the manifest; a second runner; leave the pack as is and run Studio only in the repo. Recommendation: the flag, with the tier in the manifest; the second runner is a second pack by another name.
5. Launchpad's place. Options: a third mode; a runtime of Hand off. Recommendation: a runtime of Hand off, with the strictest gates. This is the one call where the seat's reading is most likely to be wrong, since the Launchpad strand is his and route B was ruled with other things in mind.
6. Simulator. Options: hold; assign as the stage; assign as a Studio sub-mode. Recommendation: hold, as he said.

Order of build if all six go his way: the mark, the switch, the contract rename, then skills as they are needed; Explore comes from H1's lane, not this one.

Risk named: Studio as the place reds go to hide. Three things hold it: a Studio output cannot ship (the mark and the gate), the promotion queue is a visible list with a review pass owed on it, and ADR-0005 §5 still needs a bite test and his ruling before anything advisory becomes law.

## 8. Sources

Repo, read 2026-10-01 at the seat:
- `notes/_receipts/2026-09-27-304-sq-assembly-studio-modes.md` (his words 10:54, 10:58, 11:07 BST) and `notes/_receipts/2026-09-27-304-sq-permutation-matrix.md` (10:35–10:46 BST).
- `knowledge/_PROMOTION-QUEUE.md` (the model decided 2026-06-19; the store-boundary fence, 2026-07-02).
- `docs/decisions/ADR-0005-ratify-knowledge-engine-pivot.md` (2026-07-02), §5.
- `apollo-spider/cold-start/DESIGN-CONTRACT.md` rules 1, 3, 4; `apollo-spider/skills/{grill-me,generate-from-canon,draft-a-new-pattern,check-with-gates,check-against-design-system,usability-review}/SKILL.md`; `apollo-spider/ci-template/run-gates.py` and `gates.yml`; `apollo-spider/build-designer-pack.sh`.
- `knowledge/_build_all.py` ROUTE_ROWS (167: 78 GATE, 67 ABORT, 22 ADVISORY, by ast); `knowledge/guidelines/_rules-index.json` (475: 62/323/34/56); `knowledge/_validate_{advisory,geometry,own_size,theme_provenance,hidden_display,edge_extremity}.py` headers; `knowledge/_validate_receipt.py`; `knowledge/_validate_icons.py`; `knowledge/_inscribe_ruling.py`; `knowledge/_rulings.json` (851).
- `notes/_lanes/305/V2/cold/Apollo-Spider-v1.0.14/_MANIFEST.json` (57 gate verdicts, no tier field).
- `notes/_lanes/280/layout-matrix/REPORT.md` (the matrix precedent, 2026-09-16); `notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html` (route B; the decisions overlay).

Outside, fetched 2026-10-01:
- Claude Code, "Configure permissions", code.claude.com/docs/en/permissions: the permission modes table; "Permission rules are enforced by Claude Code, not by the model"; `defaultMode`.
- Figma Help, "Dev Mode statuses and notifications", help.figma.com/hc/en-us/articles/26781702258583: Ready for dev, Completed, the automatic Changed state, set "while editing designs or in Dev Mode".
- GitHub Docs, "About protected branches", docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches: required status checks and the successful/skipped/neutral rule.
