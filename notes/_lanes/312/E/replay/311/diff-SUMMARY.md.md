## SUMMARY — GREEN

- SIZE: generated 488 · hand 513 · ratio 0.951
- HIS WORDS: 0 quotations in the hand file; missing from the generated view: 0
- HEADINGS: same (3 generated · 3 hand)
- FIGURES numbers: missing 0 · extra 1 · extra unsourced 0
- FIGURES shas: missing 0 · extra 0 · extra unsourced 0
- FIGURES rulings: missing 0 · extra 0 · extra unsourced 0
- FIGURES rows: missing 0 · extra 0 · extra unsourced 0
- FIGURES paths: missing 0 · extra 0 · extra unsourced 0

```diff
--- hand
+++ generated
@@ -6,14 +6,12 @@
 - You haven't seen the icons and Supercharge page yet, so those two stay ruled, not standing.
 
 ## Outputs
-- Built: the soft white and the tab strip, the icons and Supercharge's page, and the twelve overnight lanes' work.
-- Pages: the burn plan, the night diagnosis, the other-libraries proposal and the revised wave-2 plan, all in the review artifact (v21 to v26).
-- The wrap is committed and pushed (`46ff0905`, plus `5dcd4be0` for the wrap seat's files). The full pre-push check ran on the wrap first and came back clean, including the step that went red overnight. CI is green on all three jobs.
-- Next chat: `Apollo - #312: the three pages put to him, then wave 2 on two seat lanes`. It puts the three pages to you, then starts wave 2 before the 23:00 reset.
+- Built: the soft white and the tab strip, the icons and Supercharge's page, the twelve overnight lanes (*"lets get the lanes running over night"*); and four pages (the burn plan, the night diagnosis, the other-libraries proposal, the revised wave-2 plan) in the artifact "Apollo 304 review".
+- The wrap is committed and pushed (`46ff0905`, plus `5dcd4be0` for the wrap seat's files). The full pre-push check ran on the wrap first and came back clean. CI is green on all three jobs.
+- Next chat: `Apollo - #312: the three pages put to him, then wave 2 on two seat lanes`.
 
 ## Problems
 - The overnight run was slow. Your Mac runs one command at a time, and git leaves lock files the folder won't let it delete. Lane X proved both causes. Its fix is two lanes on your Mac at once, with one committer.
 - The chain conductors couldn't start lanes, because a sub-agent can't launch agents. The conductor also launched wave 1 as one lane first and the other eleven an hour later, ran the night from an already-full chat, and gave you the wrong boot figure at the start (the real boot was 133,882).
-- One CI red overnight (`69848bbe`), fixed by `efd0e89f`.
-- The session ended at 341,969, past the 300,000 stop and the 320,000 limit but under the hard line.
+- One CI red overnight (`69848bbe`), fixed by `efd0e89f`. The session ended at 341,969, past the 300,000 stop and the 320,000 limit but under the hard line.
 - Still yours: the icons and Supercharge look page, lane X's four calls, and the revised plan's calls.
```
