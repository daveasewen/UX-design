"""#307 lane B — build the 78 ruling entries (entries/s307-D<n>.json), the store spec (rows.json) and the park list
(parks.json) from Dave's export (cards.json, parsed verbatim) and lane B's bucket table (decisions.py).  No write to the tree."""
import json, os, sys
sys.path.insert(0, 'notes/_lanes/307/B'); from decisions import D
B = 'notes/_lanes/307/B'
EXP = 'notes/_lanes/307/DAVE-RULINGS-2026-09-28-reopened-78.md'
PAGE = 'notes/_SITTING-307-reopened-78-2026-09-28-v1.html'
REP_A = 'notes/_subreports/2026-09-28-307-A-sitting-78.md'
exp = open(EXP, encoding='utf-8').read()
cards = json.load(open(f'{B}/cards.json', encoding='utf-8'))
st = {i['id']: i for i in json.load(open('knowledge/_state.json', encoding='utf-8'))['items']}
cardfile = {}
for k in (1, 2, 3):
    for blk in open(f'notes/_lanes/307/A/cards-{k}.txt', encoding='utf-8').read().split('\n@ ')[1:]:
        cardfile[blk.split('\n')[0].strip()] = f'notes/_lanes/307/A/cards-{k}.txt'
IDS = [f'W-307q{c}' for c in '123456789abcdefghijklmnopqrstuvwxyz'] + [f'W-307y{c}' for c in '123456789abcdefghijklmnopqrstuvwxyz']
PARK = {'W-99zm': 'P-307-1', 'W-99zn': 'P-307-2', 'W-51': 'P-307-3'}
os.makedirs(f'{B}/entries', exist_ok=True)
ops, notes_ops, mints, parks, table = [], [], [], [], []
nid = 0
for c in cards:
    n, wid, kind = c['n'], c['wid'], D[c['wid']][0]
    means, rows = D[wid][1], D[wid][2]
    rid = f's307-D{n}'
    hhmm = c['at'].split()[1]
    anchor = c['wline'].strip('`')
    assert exp.count(anchor) == 1, anchor
    dot = '' if c['q'][-1] in '.?!' else '.'
    rec = 'the recommendation' if c['rec'] == 'the recommendation' else 'NOT the recommendation'
    new = []
    for (title, cw, group, owner) in rows:
        new.append((IDS[nid], title, cw, group, owner)); nid += 1
    if kind == 'close':
        eff = f"RECORD: {wid} is closed by addition in knowledge/_state.json, `closed_by` naming this ruling. No work row: the answer closes it."
    elif kind == 'park':
        eff = (f"RECORD: parked with a tripwire as {PARK[wid]} in knowledge/_parked.json (the s305-D38/D39 register), and {wid} is closed by addition "
               f"with `closed_by` naming this ruling and {PARK[wid]}.")
        if new: eff += f" The candidature-record line is owed as live row {new[0][0]} (owner claude)."
    elif kind == 'live':
        eff = f"RECORD: {wid} STAYS LIVE (state open) and gains a dated note carrying his note verbatim; the visual check is owed to him on that row."
    else:
        eff = (f"RECORD: the question row {wid} is closed by addition as answered, `closed_by` naming this ruling; the doing is minted as live row(s) "
               + ', '.join(f"{i} ({'a review owed to Dave' if g == 'review' else 'work'}, owner {o})" for i, _, _, g, o in new) + ".")
    note = ''
    if c['note']:
        note = f" His note on the card, verbatim: \"I want to check this visually\"."
        assert 'I want to check this visually' in c['note']
    ruled = (f"THE REOPENED QUESTION {wid} IS ANSWERED BY CLICK: {c['label'].upper()}. {means} "
             f"Dave's answer, by click, verbatim: '{c['label']}' ({rec}), to the card's question, verbatim: '{c['q']}'{dot}{note} "
             f"The #307 sitting page, theme {c['section']} ('{c['theme']}'); lane S's verdict at #306: {c['verdict']}. {eff}")
    says = (f"chat #307, Mon 2026-09-28 21:18 BST, from the sitting page export ({PAGE}, exported 2026-09-28 21:18, received in chat as {EXP}; "
            f"78 of 78 answered, all by hand click, 0 by take-all) · section {c['section']} '{c['theme']}' · card, verbatim: '{c['q']}' — "
            f"his answer, by click at {hhmm} BST, verbatim: '{c['label']}' ({rec})" + (" · his note, verbatim: \"I want to check this visually\"" if c['note'] else ''))
    gov = [wid, 'knowledge/_state.json'] + (['knowledge/_parked.json'] if kind == 'park' else [])
    ev = [f"chat #307 2026-09-28 (live) - the 21:18 BST export; his click on this card is in it, quoted verbatim in `says`",
          f"{EXP}#{anchor}", PAGE, REP_A, cardfile[wid]]
    entry = {"id": rid, "date": "2026-09-28", "by": "Dave", "status": "ruled", "ruled": ruled, "says": says, "governs": gov, "evidence": ev}
    json.dump(entry, open(f'{B}/entries/{rid}.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    click = f"{rid} (#307, Dave by click 2026-09-28 {hhmm} BST, verbatim: '{c['label']}')"
    if kind == 'close':
        ops.append({"op": "close", "id": wid, "closed_by": f"{click}: {means}"})
    elif kind == 'park':
        ops.append({"op": "close", "id": wid, "closed_by": f"{click}: {means} Parked with a tripwire as {PARK[wid]} in knowledge/_parked.json; the park register now carries the question" + (f"; the candidature-record line is live row {new[0][0]}." if new else ".")})
    elif kind == 'live':
        notes_ops.append({"op": "note", "id": wid, "para": f"{rid} (Dave, by click at {hhmm} BST on the #307 sitting page, export 21:18 BST {EXP}): he answered 'Keep it open' — not the recommendation ('Fold the third red into the one error red; Claude checks the forks'). His note, verbatim: \"I want to check this visually\". The row STAYS LIVE; a visual check is owed to him: the third red #a8000b beside the one error red, and the four ink forks declared at #305 (s305-D41) against what was left of the 29. `closes_when` above is unchanged."})
    else:
        ops.append({"op": "close", "id": wid, "closed_by": f"{click}: answered. {means} The doing is live row(s) {', '.join(x[0] for x in new)}."})
    oldhome = (st[wid].get('home') or '').split('#')[0]
    for (i, title, cw, group, owner) in new:
        links = [wid, PAGE] + ([oldhome] if oldhome and os.path.exists(oldhome) else [])
        what = 'A REVIEW OWED TO DAVE (he asked to see it). ' if group == 'review' else ''
        left = ' / '.join(c['card'].get('O') or c['card'].get('C') or [])
        body = (f"Minted #307 lane B under {rid} — Dave, by click at {hhmm} BST on 2026-09-28, verbatim: '{c['label']}' ({rec}), answering the reopened "
                f"question {wid}, verbatim: '{c['q']}'{dot} {what}{means} What the card said was still open (lane A's reading, {cardfile[wid]}): {left} "
                f"The question row {wid} is closed as answered; this row is the doing. Export: {EXP}; page: {PAGE}.")
        mints.append({"op": "mint", "id": i, "live": True, "owner": owner, "title": f"#307 {wid} answered - {title}",
                      "home": f"{EXP}#{anchor}", "links": links, "closes_when": cw, "body": body})
    if kind == 'park':
        parks.append({"pid": PARK[wid], "wid": wid, "rid": rid, "label": c['label'], "hhmm": hhmm, "q": c['q'], "means": means})
    table.append({"n": n, "rid": rid, "wid": wid, "kind": kind, "label": c['label'], "rec": rec, "new": [(i, t, g, o) for i, t, _, g, o in new]})
spec = {"session": 307, "by": "#307 B (2026-09-28)", "ops": ops + notes_ops + mints}
json.dump(spec, open(f'{B}/rows.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
json.dump(parks, open(f'{B}/parks.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
json.dump(table, open(f'{B}/table.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('entries 78; ops', len(ops), 'notes', len(notes_ops), 'mints', len(mints), 'parks', len(parks), 'ids used', nid)
