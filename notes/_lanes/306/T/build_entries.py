# #306 lane T — the three ruling entries s306-D1..D3 from Dave's check-page export. Every quoted word of his is read
# from the export (the two calls from its markdown, the ticks from its machine copy), never retyped. Writes entry files
# only; the writes go through knowledge/_inscribe_ruling.py. Status `ruled` at inscription; `enacted` is stamped
# after the commit with --set-status and the commit sha (s295-D2), as #305 lane L did.
import json, re, os
EX = 'notes/_lanes/306/DAVE-RULINGS-2026-09-28-parked-check.md'
PAGE = 'notes/_CHECK-306-parked-superseded-2026-09-28-v1.html'
SREP = 'notes/_subreports/2026-09-28-306-S-parked-check.md'
SJS = 'notes/_lanes/306/S/parked-102-check.json'
TREP = 'notes/_subreports/2026-09-28-306-T-parked-enact.md'
OUT = 'notes/_lanes/306/T/entries/'; os.makedirs(OUT, exist_ok=True)
txt = open(EX, encoding='utf-8').read()
A = json.loads(re.search(r'```json\n(.*?)\n```', txt, re.S).group(1))['answers']
CALLS = dict(re.findall(r'^- (.+?) → \*\*(.+?)\*\*$', txt, re.M))
Q1 = 'Close the 24 already-answered questions?'
Q2 = 'Does the call-33 yes settle the two old release rows (W-222, W-272)?'
assert CALLS[Q1] == 'yes' and CALLS[Q2] == 'yes'
KEEP = A['keep']; assert len(KEEP) == 78
C = json.load(open(SJS, encoding='utf-8'))
SUP = [r['id'] for r in C if r['verdict'] == 'SUPERSEDED']; assert len(SUP) == 24
ASK = "can you check these I think some of them have been superseded"
assert ASK in open(SREP, encoding='utf-8').read()
q = lambda s: '"' + s + '"'
SAYS0 = (f"chat #306, Mon 2026-09-28 15:20 BST, from the check page export ({PAGE}, exported 2026-09-28 15:20, "
         f"received in chat as {EX}); the check answered his question at 12:59 BST, verbatim: {q(ASK)}")
first = min(KEEP.values()); last = max(KEEP.values())
E = {
 's306-D1': {
  "id": "s306-D1", "date": "2026-09-28", "by": "Dave", "status": "ruled",
  "ruled": ("THE 24 PARKED QUESTIONS THAT LATER RULINGS ALREADY ANSWER ARE CLOSED AS ANSWERED. Dave's answer, verbatim: "
            f"{q(CALLS[Q1])}, to the check page's call, verbatim: '{Q1}'. The 24 are lane S's SUPERSEDED rows "
            f"({SJS}): {', '.join(SUP)}. Each is closed BY ADDITION in knowledge/_state.json: its body gains the answering "
            "ruling id(s) and the record's words as lane S quoted them, and `closed_by` names this ruling. Nothing already "
            "written is rewritten; `closes_when` stays as history. `s305-D32` (the park) is not edited: this ruling answers "
            "the scan it asked for."),
  "says": f"{SAYS0} · call, verbatim: '{Q1}' — his answer, verbatim: {q(CALLS[Q1])}",
  "governs": ["knowledge/_state.json"],
  "evidence": [f"chat #306 2026-09-28 (live) - 12:59 BST his question and the 15:20 BST export, both quoted verbatim in `says`",
               EX + "#The two calls", PAGE, SREP, SJS]},
 's306-D2': {
  "id": "s306-D2", "date": "2026-09-28", "by": "Dave", "status": "ruled",
  "ruled": ("HIS CALL-33 YES SETTLES THE TWO OLD RELEASE ROWS W-222 AND W-272: THEY CLOSE WITH THE OTHER RELEASE ROWS. "
            f"Dave's answer, verbatim: {q(CALLS[Q2])}, to the check page's call, verbatim: '{Q2}'. At #305 both were in "
            "call 33's release set (`s305-D33`) AND in call 32's park, and lane H1 kept them parked, not closed, so they stayed "
            "on the scan he asked for, with \"Say the word and they close\". This is the word. Both are closed by addition "
            "under this ruling and `s306-D1`. Store row W-305hr gains, by addition, that he has said which way the two go; "
            "its other half (the 28 kind-6 rulings) is still unanswered and it stays open. `s305-D33` is not edited."),
  "says": f"{SAYS0} · call, verbatim: '{Q2}' — his answer, verbatim: {q(CALLS[Q2])}",
  "governs": ["knowledge/_state.json"],
  "evidence": [f"chat #306 2026-09-28 (live) - the 15:20 BST export, quoted verbatim in `says`",
               EX + "#The two calls", PAGE, SREP, "notes/_subreports/2026-09-27-305-H1-records.md"]},
 's306-D3': {
  "id": "s306-D3", "date": "2026-09-28", "by": "Dave", "status": "ruled",
  "ruled": ("THE OTHER 78 PARKED QUESTIONS ARE REOPENED: DAVE TICKED \"KEEP OPEN\" ON EVERY ONE. His answer is 78 ticks, "
            f"saved {first} to {last} BST, listed in the export under \"Keep open (78 of 102)\" — the 34 lane S read as "
            "partly answered, the 10 it was unsure of, and the 34 still live. Per the note #305 lane H1 wrote into each "
            "parked row (\"Any row he ticks \\\"Keep open\\\" on that page is reopened (state → open) by addition\"), each "
            "goes parked → open in knowledge/_state.json with a dated body paragraph; the #305 park paragraph and its "
            "tripwire stay as history, and `closes_when` is unchanged. Five of them (W-510, W-63, W-71, W-72, W-73) were "
            "also parked under `s305-D37`; his tick is the later word and reopens them; `s305-D37` is not edited. No "
            "entry for these rows exists in knowledge/_parked.json (H1 wrote the tripwires into the rows only), so that "
            "register is unchanged."),
  "says": (f"{SAYS0} · section \"Keep open (78 of 102)\": 78 \"Keep open\" ticks, saved {first} to {last} BST, the "
           f"ids and times in the export's machine copy"),
  "governs": ["knowledge/_state.json"],
  "evidence": [f"chat #306 2026-09-28 (live) - the 15:20 BST export; his ticks are listed in it",
               EX + "#Keep open (78 of 102)", PAGE, SREP, SJS]},
}
for k, v in E.items():
    json.dump(v, open(OUT + k + '.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print(k, len(json.dumps(v, ensure_ascii=False)))
