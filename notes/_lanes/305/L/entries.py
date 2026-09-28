# #305 lane L - the two ruling entries (s305-D62, s305-D63), written as JSON for _inscribe_ruling.py
import json
W = 'notes/_lanes/305/L/DAVE-WORDS-2026-09-28-1141.md'
WIN = "Lets make the window 320 including a wrap, 320 is a bright amber and 350 as the limit."
SUM = "lt's turn the summary into shorter bullets just outlining decisions, outputs and problems, less verbose."
d62 = {
 "id": "s305-D62",
 "ruled": ("THE WORKING WINDOW IS 320,000 AND INCLUDES THE WRAP; 320,000 IS THE BRIGHT-AMBER LINE; THE HARD LIMIT IS 350,000. "
           "Dave's words, verbatim: \"" + WIN + "\" "
           "THE CONDUCTOR'S READING, stated as the reading: the working window (`BUDGET_WORKING`) is 320,000 and INCLUDES the wrap (was 256,000); "
           "320,000 is the bright-amber line, so the tolerance line (`TOLERATED_TK`) becomes that amber line, 320,000 (was 276,000); "
           "the hard limit (`BUDGET_HARD`) is 350,000 (was 300,000); the stop line (`STOP_LINE_TK`), where the wrap starts, moves to 300,000 (was 236,000) "
           "so that a wrap lands inside 320,000. Stop and tolerance stay ADVISORY; the blocking tier is still the hard line. "
           "`BUDGET_AMBER` (160,000, where a job stops taking on more) is not named by his words and does not move. "
           "⚠ SUPERSEDES `s305-D28` (working 256,000, hard 300,000, stop 236,000, tolerance 276,000); `s305-D28` is not edited - this ruling crosses its numbers out. "
           "`knowledge/_standing.md` line 19 (\"180,000 FILL is the QUALITY line and stands; working 256,000 and hard 300,000 ...\") is Dave's ratified text (`s287-D1`) and is NOT edited here; it is his to amend."),
 "date": "2026-09-28",
 "by": "Dave",
 "says": ("chat #305, Mon 2026-09-28 11:41 BST, after the #305 wrap was committed (eb2630bb) and pushed; the second of three lines he sent together, verbatim: \"" + WIN + "\""),
 "governs": ["knowledge/_gauge_tokens.py", "knowledge/_capture_gate.py", "knowledge/_checkin.py", "knowledge/_seam.py", "knowledge/_RUNBOOK-context-gauge.md"],
 "evidence": [
   "chat #305 2026-09-28 (live) - 11:41 BST, his window line, quoted verbatim in `says`; the conductor's reading of it is in `ruled`",
   W + "#The window",
 ],
 "status": "ruled",
}
d63 = {
 "id": "s305-D63",
 "ruled": ("THE WRAP SUMMARY FOR DAVE IS SHORT BULLETS UNDER THREE HEADINGS - DECISIONS, OUTPUTS, PROBLEMS - AND LESS VERBOSE. "
           "Dave's words, verbatim: \"" + SUM + "\" "
           "It REPLACES the #250 practice: a plain-prose narrative of the session, five to seven paragraphs, given to him after every wrap (his ask at #250, 2026-09-06). "
           "The form: the three headings in that order, one short line per bullet, about 20 bullets in all at most, no narrative paragraphs; each bullet names a decision (with its ruling id where one exists), an output (with its path or sha), or a problem (with what is open and whose it is). "
           "The #250 practice was never written into `knowledge/_RUNBOOK-capture-ritual.md`; this ruling is homed there by addition as step 5c, with the old practice struck through beside it. Nothing is erased."),
 "date": "2026-09-28",
 "by": "Dave",
 "says": ("chat #305, Mon 2026-09-28 11:41 BST, after the #305 wrap was committed (eb2630bb) and pushed, answering the wrap's plain-prose narrative; the first of three lines he sent together, verbatim: \"" + SUM + "\""),
 "governs": ["knowledge/_RUNBOOK-capture-ritual.md"],
 "evidence": [
   "chat #305 2026-09-28 (live) - 11:41 BST, his summary line, quoted verbatim in `says`",
   W + "#The summary",
   "notes/_lanes/305/W/NARRATIVE.md",
 ],
 "status": "ruled",
}
for e in (d62, d63):
    json.dump(e, open(f"notes/_lanes/305/L/entry-{e['id']}.json", "w"), ensure_ascii=False, indent=1)
print("ok")
