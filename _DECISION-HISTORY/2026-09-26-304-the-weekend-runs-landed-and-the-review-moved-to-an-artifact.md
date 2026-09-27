# #304 — the weekend runs landed, and the review moved to an artifact

provenance: 304 · 2026-09-26
status: observed

*The WHY and HOW of session #304 — a DATE SPLIT: Saturday 2026-09-26 from 14:40 BST, the delegated runs through the night, and Sunday 2026-09-27 from 11:44 to 12:16 BST. Written at the delegated wrap seat (Opus 5.5) on 2026-09-27 for a conductor on Opus 5.5 in the CLOUD, linked to his computer. His words are verbatim in `notes/_lanes/304/WRAP-BRIEF.md`; the figures here are the lanes' reports and this seat's own reads. Nothing was inscribed: `knowledge/_rulings.json` reads 638.*

## 1. The proposal page, and the Jev correction

`_HANDOFF-154` made the Apollo-MCP proposal page the first beat, and the conductor sent it to a helper at once, so the chat stayed clear. Lane M built v1 from G1's archaeology, G2's forty dated sources and the June note, in the house style with a decisions overlay. While it ran he sent two short messages. The first asked whether the page defined a proof of concept or the final architecture, and it carried a correction: *"the reason we've rejected jev at build time is because it makes Apollo less transferable at the moment, its not rulled out completly for a GenUI project."* The second said the entitlements could be a best guess for the PoC.

The correction mattered because #303's record had carried G1's caution as if it were a rule: Jev is dev-time only, so run-time judgement must be mechanical. His words narrow that. The dev-time ruling (#294) is about portability at build time; it is not a bar on a GenUI project. v2 therefore sets rules and rules-plus-Jev side by side (rules pick the shortlist, Jev may rank within it) and names the cost. It also puts the PoC first, June's contextual dashboard on mock data, and labels the four mock roles "Best guess for the PoC, not HSBC's entitlement model". Run 5 later probed the premise: every one of the 137 metas yields a valid A2UI entry, but only 17 are ready to be picked at run time, and 14 of those are charts. What stops the rest is mostly missing data shapes and when-rules, which is Apollo's own backlog, not the protocol's.

## 2. "Lets get ripping": the plan, and why it was six runs

At 15:33 he pasted his usage panel (5% of the session, 3% of the week, Fable untouched) and asked for three things: an analysis of all the proposed development and the future state, a roadmap, and big pushes over the weekend that he could leave running, with models, effort and sub structure recommended, *"watch the externalities, dependancies and test it hard"*. The conductor split the analysis four ways (A1 the proposals, A2 the open work, A3 the future state, A4 health and dependencies) and gave the synthesis to a Fable seat, F, because the synthesis was judgement and the four inputs disagreed with each other in seven places.

F's recommendation was a milestone, not a list: Spider v1.0.14, "the pack the deck describes", built as a CANDIDATE on a build that runs to the end, with the MCP probe beside it. Six runs followed from that. Three needed no ruling and started at once (CI sees to the end; the store tells the truth; the MCP probe). Two needed no ruling to BUILD but left the cut to him (the rulings already made, now built; the candidate). The sixth wrote the decision pages for Tuesday. The order put the instruments first: nothing about the candidate could be judged while CI stopped at step 8 and the rulings store said "ruled" for things that had been built weeks ago.

## 3. What the runs found, and the four waves after them

Every wave had the same shape: builders in their own windows, a Fable verifier that built none of it, then an Opus commit seat that ran the regen serial, committed through the door on the declared not-a-wrap path, pushed, and read CI back to the end. Six waves ran that way, and every CI read matched its prediction by name except two, each traced the same night.

- **CI saw the whole build again** for the first time since 2026-09-09 (Run 1). Two of the plan's premises were wrong and the lane followed the code, not the brief; in `[38]`'s case the snippet blocks were the newer truth, not the metas.
- **The store told the truth** (Run 2): 184 rulings stamped `enacted`, each with its enacting sha and quoted receipt; 109 left UNCERTAIN for him; 53 of 93 candidate work rows closed on receipts, none of his. V1 caught twelve ratification rulings the stamp had wrongly moved, and C1 restored them before the commit.
- **Two rulings were built** (Run 3): `s245-D10`'s console radii and `s277-D12`'s tokens in the graph. Three stopped at their own words, because each says the next step is his.
- **The candidate composed rather than traced** (Run 4), but R4s scored it level on quality with v1.0.13, which is why the next waves existed. W3b named why quality was flat; W3a and W4a fixed the engine and canon defects that needed no ruling; W4b taught the instruments to see ink. Candidate 2 then read better and cleaner (R4s2), and most of the gain was the chart engine, which lifts old pages equally.
- **Jev on the graph's edges** (lane J, his 16:19 question): a good suggester at the extremes, noisy in the middle, useless where the truth lives in text it was not shown. A tool he ratifies, never a gate.

Three behaviours shipped on a verifier's reading without a ruling, each declared in its commit message: tick-label thinning, the right-gutter fit, console card padding 20 to 8. Two were held back because they touch what he has ruled on before: the Kpi-tile descender (`s261-D4`) and a root trim default that reached 26 components. The Tuesday sitting page (W5b, Fable) gathers all of it into 53 calls, most-unblocking first, with one decision named: cut v1.0.14 from candidate 2.

## 4. The externality he asked us to watch

The scheduled dream pass fired at 07:12 BST on Sunday, in the middle of the runs. It committed its proposals, ran `git status` on the mount (the one command the house forbids, because it strands the index lock), and, as its runbook tells it to, wrote its status row into `_LIVE-STATE.md` after its own commit and left it uncommitted. Wave five's memento index was built over that file, so CI's index determinism check went red once. W6 traced it to the dream pass's row, not to anything the wave did; C6 carried the two lines on the precedent of passes 12 and 13, and CI went green. It is the plainest case yet of a scheduled seat acting on a tree a live session is using. What to change is his.

## 5. The links, and the artifact

On Sunday morning he said that no link worked, with a screenshot: *"Files saved in this location can't be previewed."* Every link the session had given him was a `computer://` link into his repo folder, which the Claude app will not preview. The fix was to stop linking to files: one sub seat published all eleven review pages, the render-pairs page and their 147 images as one private artifact, "Apollo 304 review", with a hub that starts at the sitting page and explains that his answers save in that browser and come back by "Copy as text". At 12:11 he said he had lost the index and there was no back button; the conductor republished to the same URL with a fixed "← All review pages" button on every published page. The repo's pages are unchanged, so the button lives only in the artifact. This seat read the published file list and found that the hub's links name the pages without the `notes/` folder they were published under; whether they open is unproven, and the repair is one republish.

## 6. What the record does not know

Friday 2026-09-25 happened; its outcome is still not in the record. Whether the Common demo prompt ran, which Spider pack his work machine has, and the other `_HANDOFF-154` questions stand. The conductor's window crossed his 300K hard line at 22:08 on Saturday while the runs were delegated, and closed at 453,905; the growth was read-backs and dispatches, not work done in the seat.

## Resolved, and still open

Resolved by acts: the Apollo-MCP page exists in two versions; CI asks every step; the store's statuses match the tree for 184 more rulings; the console radii and token nodes are built; the review surface is an artifact. Still open, and his: the 53 calls, starting with the cut; the three unruled behaviours; the two held-back fixes; the proposal's seven decisions; Jev as a suggester; the dream pass's runbook; and everything carried in `_CARRIES.md` § `residual → #305`.

Links: `_LIVE-STATE.md` ⏱ LATEST DELTA (#304) · `_HANDOFF-155-the-weekend-runs-landed-and-the-review-moved-to-an-artifact.md` · `notes/_lanes/304/WRAP-BRIEF.md` · `notes/_subreports/2026-09-27-304-W-wrap.md`.
