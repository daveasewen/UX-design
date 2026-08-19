# Post-wrap receipt — #202 — specimen v3 REJECTED by Dave

provenance: local_4859d145 #202 · 2026-08-18
status: observed

After the #202 wrap commit (`ec2336d`), Dave reviewed `reviews/SEGMENTED-SCALE-SPECIMEN-2026-08-18-v3.html`
and rejected it: **"all of these are wrong"** — all four scales, screenshot supplied in chat.

Observed in the screenshot: the white thumb seated on the LAST segment ("Month") overflows the
track's RIGHT edge at every scale — no trailing inset visible; the track's right rounded corner is
hidden behind the thumb. Same seating-defect class the #202 compare pages hit on other sides
(border-blind height calc; viewport-scaled offsets). The thumb RADII themselves are not re-opened —
`s202-D2` stands; this is the specimen's rendering, not the tokens.

Disposition: FIRST ITEM at #203. The fix starts from the canonical seating in
`knowledge/snippets/Segmented-control.reference.html` (`.ind` + `moveInd()`), per
the #202 lesson: specimens copy the reference, never re-draw. The `_REVIEW-SIGNOFF.md`
row is updated to REJECTED in this same post-wrap pass. Label-binding decision unaffected, still Dave's.

## Second finding, same post-wrap pass — T3 mid-session refusal loop (possible gate defect)

Attempting to commit this receipt + the signoff row mid-session (SESSION_N=202,
`--reconciled`, fresh printf msgfile per invocation) refused every time on the #170
reused-msgfile gate — INCLUDING on a byte-fresh msgfile written seconds earlier in the same
call. Observed mechanism: T3 prepends its `after #N <date> — ` prefix to the msgfile in place,
then the reuse check reads the file and sees the prefix T3 itself just wrote — a gate that
cannot pass in this invocation path [[gate-cannot-pass-in-one-environment]] class. Four fresh
msgfiles, four identical refusals; nothing staged each time (refusal honest, file untouched
except the prefix). NOT diagnosed further at 48K-to-wall. These two files are handed up
UNCOMMITTED for #203's opening commit; the T3 loop is a queued diagnosis item.
