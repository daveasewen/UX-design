# #305 lane A2 — mint the five new open threads from Dave's 2026-09-28 loose-ends answers through the sanctioned
# _state writer (_state.add refuses a row with no close condition; _state.save is the store's own writer).
# His words are read from the export's machine copy, never retyped. Usage: python3 mint_threads.py [--write]
import sys, os, json, re
sys.path.insert(0, 'knowledge')
import _state as st
EX = 'notes/_lanes/305/DAVE-RULINGS-2026-09-28-loose-ends.md'
PAGE = 'notes/_DECIDE-305-loose-ends-2026-09-27-v1.html'
MAP = 'notes/_lanes/305/A/CALL-MAP.json'
C = 'knowledge/components/'
t = open(EX, encoding='utf-8').read()
A = json.loads(re.search(r'```json\n(.*?)\n```', t, re.S).group(1))['answers']
dec = lambda k: A[k]['decision'].strip()
q = lambda s: '"' + s + '"'
HDR = "one thing to note, I want to add a header component to bento groups."
assert HDR in dec('g1-ceo-r2') and HDR in dec('g1-ceo-r3')
UXQ = "I wonder if this is a valid variation if two subjects are intimately linked. This is a UX qustion."
assert UXQ in dec('g1-ceo-r3')
rows = [
 dict(id='W-305e1', owner='dave', home=EX + '#4c · 4 · List', links=[PAGE, MAP, C + 'list-items.meta.json', 'notes/_lanes/304/R4a/drafts/when-rules.proposed.json'],
  title="#305 loose ends 4c·4 - the list rule, to be worked on its own (he answered Change)",
  body=("Dave answered \"Change\" on the list's when-rule (the page's sentence: \"A list is for records read across their own row, when "
        "nobody needs to sort, filter, select or edit them. When they do, the data grid takes over.\"), saved " + A['wr-list']['at'] +
        ", with his words, verbatim: " + q(dec('wr-list')) + " The drafted row is NOT accepted and is not in s305-D60; the `records × "
        "fields` data shape the drafting lane proposed beside it was never taken either."),
  closes_when="Dave has ruled a when-rule for the list (list-items), worked on its own as he asked, from a page put to him, or parked it with a tripwire"),
 dict(id='W-305e2', owner='dave', home=EX + '#4c · 6 · Top-nav shell', links=[PAGE, MAP, C + 'app-shell-top-nav.meta.json'],
  title="#305 loose ends 4c·6 - the top-nav shell rule is an IA question, to be explored more rigorously (he answered Change)",
  body=("Dave answered \"Change\" on the top-nav shell's when-rule (the page's sentence: \"Up to 7 destinations and 2 levels; the "
        "default for dashboards. More than that, the side nav. Tight on width, the nav rail. List and detail, the multi-column shell. "
        "No navigation, the focused shell.\"), saved " + A['wr-top-nav']['at'] + ", with his words, verbatim: " + q(dec('wr-top-nav')) +
        " The row is NOT accepted and is not in s305-D60; the meta's current `when` is unchanged by this row."),
  closes_when="Dave has ruled the top-nav shell's when-rule as an IA question (top nav, mega menu for multiple levels, and what hands over to what), explored on its own page, or parked it with a tripwire"),
 dict(id='W-305e3', owner='dave', home=EX + '#4c · 9 · Page title', links=[PAGE, MAP, C + 'headers.meta.json', C + 'page-header-lockup.meta.json'],
  title="#305 loose ends 4c·9 - the page title and page-header lock-up: he accepted the rule, and wants the lock-up worked on",
  body=("Dave accepted the page-title when-rule (\"A page, screen or section title on its own. With actions or tabs beside it, the "
        "page-header lock-up takes over.\"), inscribed in s305-D60, and added, verbatim: " + q(dec('wr-headers')) + " The accept stands; "
        "this row is the lock-up work only."),
  closes_when="Dave has ruled on the page-header lock-up (its design and how it takes over from the page title) from a page or visuals put to him, or parked it with a tripwire"),
 dict(id='W-305e4', owner='dave', home=EX + '#1b · run 2', links=[PAGE, MAP, C + 'template-dashboard-bento.meta.json', 'notes/_REVIEW-304-candidate-2-2026-09-27-v1.html'],
  title="#305 loose ends 1b and 1c - add a header component to bento groups",
  body=("Said twice, at candidate-2 runs 2 and 3 (loose-ends page 1b and 1c, both saved " + A['g1-ceo-r2']['at'] + "), verbatim: " + q(HDR) +
        " Not built; no part named."),
  closes_when="Dave has ruled a header component for bento groups (what it is and where it sits) from a page put to him, or parked it with a tripwire"),
 dict(id='W-305e5', owner='dave', home=EX + '#1c · run 3', links=[PAGE, MAP, C + 'template-dashboard-bento.meta.json', 'notes/_REVIEW-304-candidate-2-2026-09-27-v1.html'],
  title="#305 loose ends 1a-1c - UX question: can two intimately linked subjects form one bento group, as a valid variation?",
  body=("From the candidate-2 overviews (can resilience, exposure and decisions be seen as three groups?). His run-3 words, verbatim "
        "(verdict \"" + A['g1-ceo-r3']['verdict'] + "\", saved " + A['g1-ceo-r3']['at'] + "): " + q(dec('g1-ceo-r3')) +
        " Run 2 (verdict \"" + A['g1-ceo-r2']['verdict'] + "\"), verbatim: " + q(dec('g1-ceo-r2')) +
        " Run 1 (verdict \"" + A['g1-ceo-r1']['verdict'] + "\"), verbatim: " + q(dec('g1-ceo-r1')) +
        " ⬛ NOTE ON THIS THREAD, his run-1 comment, verbatim: " + q(A['g1-ceo-r1']['comment'].strip()) +
        " — kept here as an observation on bento grouping, not its own row. The header component he wants for bento groups is W-305e4."),
  closes_when="Dave has answered, as a UX ruling, whether two intimately linked subjects (his case: exposure and resilience on the CEO overview) may form one bento group as a valid variation, or parked it with a tripwire"),
]
before = os.path.getmtime(st.STORE)
doc = st.load()
n0 = len(doc['items'])
have = {i['id'] for i in doc['items']}
for r in rows:
    assert st.ID_RE.match(r['id']), r['id']
    assert r['id'] not in have, r['id']
    for l in r['links']:
        assert os.path.exists(l), l
    status, detail = st.resolve_home(r['home'])
    assert status == 'anchor-ok', (r['id'], status, detail)
    st.add(doc, project='apollo', opened=305, state='open', **r)
ok, fails, notes = st.check(doc)
assert ok, fails
if '--write' in sys.argv:
    assert os.path.getmtime(st.STORE) == before, 'store changed under us — re-run'
    st.save(doc)
    print('WRITTEN', n0, '->', len(st.load()['items']))
else:
    print('DRY', n0, '->', len(doc['items']), 'check ok')
