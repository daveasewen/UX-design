# #305 lane A — mint the six new open threads from Dave's 2026-09-27 sitting through the sanctioned
# _state writer (_state.add refuses a row with no close condition; _state.save is the store's own writer).
import sys, os, json
sys.path.insert(0, 'knowledge')
import _state as st
EX = 'notes/_lanes/305/DAVE-RULINGS-2026-09-27-sitting.md'
FRI = 'notes/_lanes/305/FRIDAY-2026-09-25-what-came-back.md'
SIT = 'notes/_SITTING-304-tuesday-2026-09-29-v1.html'
MAP = 'notes/_lanes/305/A/CALL-MAP.json'
rows = [
 dict(id='W-305n1', owner='dave', home=EX + '#06 · Thinning the category', links=[SIT, MAP],
  title="#305 sitting call 6, his comment - labelling rules for complex charts (5 columns, 3 labels, two keys)",
  body="Opened from Dave's comment on sitting call 6 (ruled s305-D7, thinning ratified), verbatim: \"The second chart is confusing, there are 5 columns and three labels, typically iI'd recommend an alpha-numerical and a key but this is extra complex as you would need 2 keys, we need to think more about the labeling rules for these complex charts\". Not decided by s305-D7.",
  closes_when="Dave has ruled a labelling rule for complex charts whose categories outnumber their labels (his case: 5 columns, 3 labels, two keys) at a sitting, or parked it with a tripwire"),
 dict(id='W-305n2', owner='dave', home=EX + '#08 · A ring', links=[SIT, MAP, 'knowledge/components/chart-donut.meta.json'],
  title="#305 sitting call 8, his comment - the donut is not responsive but not fixed: 4px-grid size bands computed at build time, editable in edit mode",
  body="Opened from Dave's comment on sitting call 8 (ruled s305-D9: the ring's tile hugs, half-width column), verbatim: \"Note that we have decided that the donut should not be responsive, however this does not mean that it will be fixed. We need to think about this, the simplest way might be something similar to the edit-mode example we have where we had a count-down that could scale to the 4px grid and had upper and lower bands. would could calculate the best solution at build time and allow changes in edit mode.\" Not decided by s305-D9; ds-030 not edited.",
  closes_when="Dave has ruled how a donut or pie takes its size (his sketch: a 4px-grid scale with upper and lower bands, the best size computed at build time, changeable in edit mode) at a sitting, or parked it with a tripwire"),
 dict(id='W-305n3', owner='dave', home=EX + '#29 · The boot ceiling', links=[SIT, MAP, 'notes/_lanes/293/IDEA-wrap-is-slow-five-levers.md', 'knowledge/_gauge_tokens.py'],
  title="#305 sitting call 29, his comment - make the boot more efficient, and return to improving the wrap",
  body="Opened from Dave's comment on sitting call 29 (ruled s305-D29: boot ceiling 130,000 until the Mac seat), verbatim: \"I really find this frustrating, we need to make this more efficient somehow, and I want to return to impoving the wrap too at some point\". The Mac-seat re-measure under s305-D29 does not by itself close this row.",
  closes_when="Dave has ruled a plan for boot efficiency and a lane for improving the wrap (the five levers of notes/_lanes/293/IDEA-wrap-is-slow-five-levers.md or their successor) at a sitting, or parked either with a tripwire"),
 dict(id='W-305n4', owner='claude', home=EX + '#27 · Two things the skill lane widened', links=[SIT, MAP],
  title="#305 sitting call 27 NOT RULED - visuals owed so Dave can rule it (the page never sizes a part, width included; the reader is the skill's first step)",
  body="Dave's only answer on call 27 was a comment, verbatim: \"I need to visuals for this\". Nothing was inscribed for call 27. The conductor owes a visuals page showing both widened points before and after.",
  closes_when="a visuals page for sitting call 27 showing both points (width ban, reader-first routing) is filed under notes/ and Dave has ruled call 27 from it, or parked it"),
 dict(id='W-305n5', owner='claude', home=EX + '#32 · Park 102 ruling-shaped questions', links=[SIT, MAP, 'notes/_DECIDE-304-housekeeping-and-lines-2026-09-26-v1.html'],
  title="#305 sitting call 32 - surface the 102 parked ruling-shaped questions for Dave to scan",
  body="s305-D32 parks the 102 ruling-shaped questions two weeks old or more, each with a tripwire, on Dave's condition, verbatim: \"park but surface for me so I can have a scan of it\". The surfacing is the conductor's.",
  closes_when="a scan page listing all 102 questions parked under s305-D32, each with its tripwire, is filed and put to Dave, and every one he names in one line is reopened"),
 dict(id='W-305n6', owner='dave', home=FRI, links=[EX, SIT, MAP, 'notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html'],
  title="#305 Friday note - the Launchpad proof of concept is a surprise: nothing about it on shared material",
  body="From Dave's Friday answer, verbatim in the home file: \"Nothing promised, one of the audience asked if Apollo could be used for Gen-UI, I answered yes. I want to do the POC as a sort of surprise.\" Applies to s305-D45..D54 (route, scope, Jev switch, the name Launchpad, timing, delivery shape).",
  closes_when="Dave has shown the proof of concept, or says in his own words that it may be named on shared material"),
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
