# #311 — the night ran slow, and Apollo was ruled for other libraries

provenance: 311 · 2026-09-30
status: observed

*Session #311, opened Wednesday 2026-09-30 19:23 BST, ran overnight, wrapped Thursday 2026-10-01 on his 11:22 "wrap as soon as your done" (date split, `s294-D11`'s shape). Written at the wrap by the delegated Opus 5.5 wrap seat. The WHAT is in the ledger (`knowledge/_rulings.json`, `s311-D1`..`D9`) and the ⏱ LATEST delta of `_LIVE-STATE.md`; this file holds the why and the how. Handoff: `_HANDOFF-162-the-night-ran-slow-and-apollo-was-ruled-for-other-libraries.md`. Row: W-311dh.*

## 1. Why the soft white stood, and why the icons followed

At #310 he ruled the dark text down from #FFFFFF to #E1E1E1 and the tab strip onto its container's colour, with the note *"i need to see this"*. So #311 built first and asked second. Lane A moved the source tokens, not canon.css, and let the generators carry it: 137 snippets re-projected, 137 swept for state contrast with 0 text failures. Two choices were readings, declared rather than hidden: Common's secondary text kept its own #9B9B9B (softening it to #E1E1E1 would have brightened it), and Supercharge stayed on its warm #F7F6F4 because its own step 12 is a grey, not a white.

Looking at the picture, he let both stand and saw the next thing at once: *"the icons should follow the ink colour"*. A pure-white glass next to #E1E1E1 text reads brighter than the words it sits with, which undoes the halation argument that chose #E1E1E1 in the first place. That became `s311-D1`. His call 3 settled the question #310 left with lane A's finding: Supercharge's dark page read #1A1A1A because the cascade generator locked `background/default` after its light half. Lane B fixed the generator, not the symptom, so the page and section now resolve to warm/4 #25211C, one step above the tile. He has not yet looked at that page, so both stay ruled.

## 2. Why the night ran slow

His 21:30 ask was fuel: chunky multi-agent jobs, Fable as much as needed. Lane P's plan answered with eight jobs in three waves. The plan relied on chain conductors, each launching its own lanes. That failed at once, and the cause is structural, not a bug: a sub-agent has no Agent tool, so only the top-level conductor can launch lanes. The conductor fell back to twelve flat lanes, but sent one first and the other eleven about an hour later, and it did all of it from a chat already at about 250,000.

The lanes then crawled. His morning words were *"we need to understand what went wrong this will be a constant issue otherwise"*, so lane X measured instead of guessing. Across 2,182 seat calls the pattern was exact: every cut call had a wall time of 180 s, whatever its run time. The seat runs one command at a time, and the clock starts when a call joins the queue, so with twelve lanes most of each call's budget was spent waiting. With three lanes or fewer, the median call took 0.7 s. The second fault was older: the mount refuses `unlink`, and git releases an unused lock by unlinking it, so every git command that writes nothing strands a lock. 948 stranded locks were on record since #263. Twelve lanes did not create the fault, they made the collisions fatal. The fix lane X recommends is a rule, not a tool: two seat lanes at most, one of them the only committer, and text lanes in the cloud.

The one CI red had the same shape as earlier reds. The clone survey ran with `--include-mutating`, so step 118 rebuilt the memento index before step 119 checked it, and the survey passed a tree that CI then failed. The lesson is now written for every lane: survey the committed tree first, without the mutating half.

## 3. How the snippet became a fixture

His 08:09 question looked small: does the compiler rely on the snippet for structure? The answer was yes, and at 08:54 he challenged that: *"my instinct is that we shouldn't rely on the snippets, they are for the user to view the components"*, and asked for a plan to make Apollo work with other HTML, React or Angular libraries, *"solid, but flexible, using standards and best practice"*.

Lanes M1 to M3 split the question: research on how other systems do it, a measurement of what the compiler actually depends on, and a proposal. The proposal agreed with his instinct and went further. If the snippet is the source, every other output has to reverse-engineer HTML. If the meta carries the spec (anatomy, states, emits, bindings), then the HTML snippet becomes one emitter's output, checked by a round-trip gate, and a Lit custom element or a React wrapper is another emitter. Light DOM was chosen over Shadow DOM because about 35 gates measure rendered geometry and contrast through canon.css, and Shadow DOM would hide the elements from them. For a client's own library, Apollo should govern and theirs should render, through an adapter manifest per library. Tokens move to the W3C DTCG format now, because every later step reads them.

He took all seven recommendations by click, with the note *"This cool, lets get it done"*, and asked how it fits the other plans. Lane R's answer: three new jobs today (DTCG tokens, the spec fields in the metas with a first cohort for his eye, the adapter schema), one job dropped because the renderer it was going to spike is now the first emitter, and fourteen lanes moved to Friday.

## 4. Resolved, and still open

Resolved: the soft white and the tab strip (enacted), the generator lock behind Supercharge's dark page, the reason the night was slow (proven, not yet acted on), the direction for other libraries (`s311-D3`..`D9`).

Open, his: the look page for the icons and Supercharge's page; lane X's four calls; the revised plan's calls; cohort one's trees when they come; the inactive tab's 70% → 67%.

Open, mine: wave 2 under the two-seat-lane rule before the 23:00 reset; the lock leaks inside `_git_commit.sh`.
