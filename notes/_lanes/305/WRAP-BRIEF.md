# #305 WRAP BRIEF — his words verbatim, and the facts

provenance: 305 · 2026-09-28 · conductor Opus 5.5 in the CLOUD, linked to Dave's Mac · status: observed

⛔ DATE SPLIT: opened Sun 2026-09-27 13:25 BST; sitting answered Sun; loose ends answered Mon 2026-09-28; ritual Mon 2026-09-28.
Keys/filenames carry the session date 2026-09-27 (s294-D11) except lane reports, which keep the day they were written; rulings s305-D58..D61 carry 2026-09-28 (the day he ruled them).

## His messages, verbatim (BST)

- Sun 13:25 — "Good Morning!"
- Sun 13:52 — "can you surface the link here"
- Sun 13:56 — "whats the difference between 'do it' and 'inscribe'"
- Sun 13:59 — "most of these I want to do both but we might need to test a bit after, I guess we can just have a review on some of these decisions in the future, they are not set in stone they are set in ink and can be crossed out in the future"
- Sun 14:53 — the sitting export: `notes/_lanes/305/DAVE-RULINGS-2026-09-27-sitting.md` (53 calls + Friday), verbatim file
- Sun 16:06 — the call-27 export: `notes/_lanes/305/DAVE-RULINGS-2026-09-27-call-27.md`, verbatim file
- Sun 18:16 — "they don't get the release, only designers, dont fret"
- Sun 19:45 — "okay go for it"  (answer to: push the five commits to the public repo, then read CI back?)
- Sun 20:02 — "what about the rest of these"
- Sun 20:04 — "what about the rest of these" + a screenshot of the review hub's list of pages 1–11
- Sun 21:28 — "please do"  (answer to: shall I build the loose-ends page?)
- Sun 22:32 — "can you surface the file"
- Mon 07:11 — "the images can't be viewed in the review doc"
- Mon 07:15 — "the loose ends page links the screens to an external browser which opens the index page and clicking on the images to view has this error" + screenshot: "claude.ai is blocked · claude.ai refused to connect. · ERR_BLOCKED_BY_RESPONSE"
- Mon 08:05 — the loose-ends export: `notes/_lanes/305/DAVE-RULINGS-2026-09-28-loose-ends.md`, verbatim file
- Mon 10:08 — "wrap"

## What the session did (receipts are the lane reports, notes/_subreports/2026-09-2{7,8}-305-*.md)

- Rulings 638 → 699: s305-D1 (his "set in ink" standing rule: a yes = inscribe AND build) · D2–D57 the sitting + call 27 · D58–D61 the loose ends (2026-09-28).
- Built: B1 look (calls 2–13, 26, 41b; call 10 scoped to Common only after verifier F1), B2 brain (14–25, 41e), W2 (23, 51, 52), B6 (accepted when-rules), H1 records (31–39), H2 code (28, 29, 40, 41 + _git_commit.sh helper), call 30 credential helper (C1).
- v1.0.14 CUT from candidate 2: X 0ef30746 · Y1 02d679b3 (zip sha256 35ae981b…, apollo-spider/dist/) · Y2 d3b809a7 frozen. V2 found the pack ships the whole rulings store incl. the Launchpad rulings; Dave: "they don't get the release, only designers, dont fret".
- The repo daveasewen/UX-design is PUBLIC (checked via API Sun ~17:30); Dave approved the push at 19:45.
- CI: F1 fixed ratification-by-status ("enacted" counts) + a py3.10/3.12 ast.unparse split in the package delta audit; D1 found the CI-only red = git 2.55 prints %cI "+00:00" as "Z" (fix: --date=raw). Runs 36349147952 and 36393419907 ALL GREEN, 154/154 asked.
- Review surface: artifact "Apollo 304 review" (https://claude.ai/artifact/1PpLec2QecFEjdnDAXYCw5), now version 7; new pages: call-27 visuals, 102-parked scan, loose ends. LESSON (his 07:11/07:15): images must be INLINED (data URIs) and must open IN-PAGE (lightbox) — an <a target=_blank> to a file opens an external browser where claude.ai refuses (ERR_BLOCKED_BY_RESPONSE). Fixed on the two 305 pages; the #304 pages were not checked.
- Pushed through cd16f7ec (C4). Uncommitted tail: C4's post-push logs; R1's report notes/_subreports/2026-09-27-305-R1-hub-reconcile.md.
- FILL (hand sum over the cloud transcript /root/.claude/projects/-home-claude/3b9c835a-bbe1-55eb-80be-d4cabf8749b0.jsonl, 87 distinct messages at brief time): boot 131,040 · over 160,000 at 12:26Z Sun · over 200,000 at 13:54Z · over 256,000 at 15:26Z Sun · 447,322 at the message that wrote this brief (Mon 09:08Z). Recompute the 300,000 crossing yourself.

## Open, Dave's (for the handoff, each as a question)
1. The 102 parked questions: his "keep open" ticks on the scan page (never returned).
2. Two old rulings stamped "not built" by the kind-5 "settled" verdict whose records look built: s212-D1, s256-D1 — re-sort?
3. The ring: "set to fill, container constrains" (s305-D59) vs the donut meta's "does not stretch" — on W-305n2.
4. The five new threads W-305e1..e5 (list rule, top-nav/IA rule, page-title lock-up, bento group header, linked subjects as one group).
5. Two new token names (B1: surface/section, notification/contextual/border/alpha) — his to accept or rename (s145-D1).
6. The rails half of call 9 (s305-D10) — held: rails generator drift (theme_tokens() picks the wrong supercharge block since #288) + no bentoBg word binds surface/section.
7. The logos page in the pack shows four missing images (#282 leftover) — rides the next cut.
8. The Launchpad PoC: October, after calls 14–19 build; a surprise (W-305n6); the four setting/slot names (s305-D58) build with the other 23 then.
9. Everything still standing on _HANDOFF-154/155 OWED that this session did not strike.
