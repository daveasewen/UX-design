# #230 POST-WRAP — Dave's v1.0.2 test: charts INTERPRETED, not retrieved

provenance: 230 · 2026-08-31, after wrap commit 92b3b13
status: observed

**Dave's words, verbatim, in chat tonight:**

> "Ive just done some testing with 1.02 and it seems to have trouble with component
> retrieval, it did and okay job but the chart retrieval was a bit shoddy it seems to
> interpreted rather than get the component, it was really close but I could tell it was
> built locally rather than retrieved... bit odd"

**Reading (conductor's, declared):** consistent with the #230 rehearsal's F1 — in v1.0.2 the
design contract ("copy the markup — component HTML comes from knowledge/snippets/, never
from memory") reaches NO auto-loaded file, so a cold builder has never seen the rule and
paraphrases the component from its own understanding. Charts are the worst case: the largest
snippets, so the strongest pull toward interpretation. v1.0.5-PROPOSED places the contract
in all three auto-load hosts (W-323, cold beats 1/5 → 4/5).

**The NEW finding his eye adds, beyond F1:** "really close but built locally" is a failure
mode NO SHIPPED GATE CAN SEE. The pack's screen gate checks compose/icon-source/a11y — it
does not verify that built markup was SPLICED FROM a snippet rather than reconstructed.
A close paraphrase passes every check and drifts silently. Same family as the raw-hex
side-finding (demo-repairs report RSQ). ⬛ Candidate instrument for #231+: a
retrieval-vs-interpretation detector (structural fingerprint of snippet markup present in
output; red on paraphrase) — priced and ruled by Dave, not built here.

**For tonight:** the discriminating test is v1.0.5-PROPOSED (sha 5c9b6247…). If charts are
STILL interpreted there — with the contract auto-loaded and grill-me fired — that is a real
class finding for #231's opener, not noise. If they splice, F1 was the whole story.

⛔ Nothing ruled here. No store row (receipts are outside the doc-row population; #231's
opener may mint one). Post-wrap capture per the #223 precedent — one commit, this file only.
