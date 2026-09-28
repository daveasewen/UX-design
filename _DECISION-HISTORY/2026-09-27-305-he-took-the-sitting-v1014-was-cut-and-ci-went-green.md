# #305 — he took the sitting, v1.0.14 was cut, and CI went green

provenance: 305 · 2026-09-27
status: observed

*The WHY and HOW of session #305 — a DATE SPLIT: Sunday 2026-09-27 from 13:25 BST (the sitting, the cut, five pushes), and Monday 2026-09-28 from 07:11 to 10:08 BST (the pictures, the loose ends, the wrap). Written at the delegated wrap seat (Opus 5.5) on 2026-09-28 for a conductor on Opus 5.5 in the CLOUD, linked to his computer. His words are verbatim in `notes/_lanes/305/WRAP-BRIEF.md` and his three exports; the lanes' figures are in their 21 reports, `notes/_subreports/2026-09-2{7,8}-305-*.md`. Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA #305. Handoff: `_HANDOFF-156-he-took-the-sitting-v1014-was-cut-and-ci-went-green.md`. Ledger: `knowledge/_rulings.json`, `s305-D1`..`s305-D61`.*

## 1. "Set in ink": why a yes became inscribe and build

`_HANDOFF-155` made the Tuesday sitting the first beat. The conductor opened the artifact for him and asked him to try one link and one back button. He asked instead what the difference was between "do it" and "inscribe". The weekend had shown that the two come apart: three behaviours had shipped with no ruling, and a record can say "ruled" for years about a thing the tree never built. His answer, at 13:59, settled it for the whole sitting: *"most of these I want to do both but we might need to test a bit after, I guess we can just have a review on some of these decisions in the future, they are not set in stone they are set in ink and can be crossed out in the future"*. It is `s305-D1`, the only `standing` ruling of the session. It also let the conductor treat short answers ("as recommended", "b", "yes") as the page's recommendation, which the common brief wrote down call by call so every lane built to the same reading.

## 2. The sitting, and why it went to lanes by kind rather than by call

He returned 53 calls and a Friday box at 14:53, two days before the Tuesday it was set for. Lane A inscribed them one by one through the sanctioned writer, each dry-run first, and minted six new threads where he had written a comment rather than a decision (calls 6, 8, 29 and the call-27 visuals). The builds were split by what they touched, not by call number: B1 took the look (canon, engine, showroom), B2 the brain (schema, metas, when-rules, the graph), H1 the records, H2 the code, W2 the leftovers, K the cut. That split is what made the fence ("careful of externalities") checkable: each lane owned a set of files, and V1, a cold Fable verifier, re-measured every number the lanes claimed. V1 found one overreach worth his eye — call 10 said "Common", and the build changed the muted label ink in every theme — and B1 scoped it back to Common before the commit.

## 3. The cut, and the two things only he could decide

K rebuilt the v1.0.14 pack from wave one and found that the Gumdrop stamp was rewriting three of his rulings inside the pack; it fixed the stamp at the builder, rehearsed the whole release chain in a scratch clone, and then cut for real in the #268 order: X `0ef30746`, Y1 `02d679b3`, Y2 `d3b809a7`. V2, cold, opened the real zip and said DO NOT SHIP to the audience: from v1.0.14 the pack carries the whole ruling store (`s279-D1`), and the store now names Launchpad and says the proof of concept is a surprise. That collision is his; his answer at 18:16 was *"they don't get the release, only designers, dont fret"*. The second decision was the push itself. The conductor found the repo is PUBLIC, so a push would publish the Launchpad rulings; the permission check stopped it, correctly, because "don't fret" was about the release, not the repo. He said *"okay go for it"* at 19:45.

## 4. Why CI took three runs to go green

The first read after the push (P1) was red in the release job at the ship-list audit. F1 found two causes that showed up only in CI: ratification was read from a status line that the session's own "enacted" stamps had changed, and a quote typed by Python 3.10's `ast.unparse` differed from 3.12's. Both were fixed and proved in a clean clone under both Pythons, and C3's run still went red at the same step. D1 then found the real remaining cause by diffing CI's regenerated manifest against the committed one: git 2.55 on the runner prints a zero offset in `%cI` as `Z`, the seat's git prints `+00:00`. Reading `--date=raw` is stable across versions and reproduces every one of 1,650 historic dates byte for byte, so the frozen v1.0.14 manifest did not move. Runs `36349147952` and, after day two, `36393419907` were green on all three jobs, 154 of 154 steps asked.

## 5. The loose ends, and the pictures

At 20:02 and 20:04 he asked about "the rest of these", with a screenshot of the hub's eleven pages. R1 reconciled each page against the sitting; B5 turned what was left into one decision page. On Monday morning he could not see its pictures, and clicking one opened an outside browser that claude.ai refused (`ERR_BLOCKED_BY_RESPONSE`). The cause is the artifact viewer: pictures loaded as separate files did not show, and a `target=_blank` link leaves the app. The fix inlined every picture as a data URI and opened it in a lightbox on the same page; the same fix went onto the call-27 page. He answered the loose ends at 08:05: four rulings (`s305-D58`..`D61`), five new threads where he answered "Change", and what "13" meant. B6 built the accepted when-rules (four new, eleven already in the tree byte for byte) and held the four setting-or-slot names, because no meta yet shows how the other 23 were settled.

## 6. What the record does not know

Which of the 102 parked questions he wants kept open (his ticks did not come back). Whether the #304 pages in the artifact have the same picture problem (not checked). Whether the boot ceiling holds: `s305-D29` raised it to 130,000, but the last two cloud boots were 131,130 and 131,040, and the wrap gate failed on the first of them once it reached the gauge log, so this wrap took the declared not-a-wrap path again.

## Resolved, and still open

Resolved: the sitting (61 rulings, 40 built with receipts), the v1.0.14 cut, CI green, Friday, the Common prompt, the pack on his work machine, the token in the remote URL, the window lines, the hub's links. The boot ceiling was raised and is already breached. Still open, each his: the 102, `s212-D1` and `s256-D1`, the ring's fill against ds-030, five threads, two token names, the rails half of call 9, the logos page in the pack, Launchpad in October, the breached boot ceiling — all in `_HANDOFF-156` § OWED and `_CARRIES.md` § `residual → #306`.
