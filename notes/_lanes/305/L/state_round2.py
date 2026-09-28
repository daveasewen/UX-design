# #305 lane L round two - W-305w note by addition (D64 answers its fifth question only), and W-305wr minted for the wrap redesign.
import sys, os; sys.path.insert(0, 'knowledge')
import _state as st
doc = st.load()
w = [i for i in doc['items'] if i['id'] == 'W-305w'][0]
before = w['body']
w['body'] = before + (" · #305 post-wrap (by addition, lane L round two, 2026-09-28): the LAST of the five questions in closes_when - whether --wrap is the wrap path "
    "again - is ANSWERED by s305-D64 (Dave, 12:21 BST, \"yes both\": the boot ceiling is 135,000; the wrap gate's boot-ceiling arm reads 0 fails against the gauge log). "
    "The row is NOT closed: the other four (the 102, s212-D1/s256-D1, the ring and the threads, the s279-D1/W-305n6 collision) are still his, unruled and uncarried by him.")
assert w['body'].startswith(before) and w['state'] == 'open'
row = dict(id='W-305wr', home='notes/_lanes/293/IDEA-wrap-is-slow-five-levers.md', owner='claude', condition='stated',
  links=['notes/_lanes/305/L/DAVE-WORDS-2026-09-28-1141.md', '_HANDOFF-156-he-took-the-sitting-v1014-was-cut-and-ci-went-green.md',
         'knowledge/_RUNBOOK-capture-ritual.md', 'W-305n3'],
  title="#306's second job, after the 102 ticks - the wrap redesign: one story written once as the handoff with the banner, delta, dossier, wrap report and memory hook generated from it (lever 1), three seats in parallel (lever 5); scheduled by Dave's \"yes both\"",
  body=("Scheduling, not a ruling. His 11:41 BST words, verbatim: \"can we parallelise the wrap at all to make it quicker, don't we have a plan to make the wrap better too, we had duplicate- -writes all over the place.\" "
        "At 12:21 BST, asked \"yes to both, the boot ceiling at 135,000 and the wrap redesign as #306's second job, after your 102 ticks?\", he answered \"yes both\". "
        "The plan is notes/_lanes/293/IDEA-wrap-is-slow-five-levers.md: lever 1 one story, the other views generated; lever 5 three seats (story / mechanics / commit-push-CI); "
        "lever 3 mostly done (the boot-ceiling fail ended with s305-D64). _HANDOFF-156 OWED item 2."),
  closes_when=("a wrap has run on the redesign - the handoff written once with the banner, delta, dossier, wrap report and memory hook generated from it, and the story, mechanics and "
               "commit-push-CI seats run in parallel - with its receipt filed; or Dave re-schedules or parks it with a tripwire"))
if 'W-305wr' not in {i['id'] for i in doc['items']}:
    assert st.ID_RE.match(row['id'])
    st.add(doc, project='apollo', opened=305, state='open', **row); print('added W-305wr')
ok, fails, _ = st.check(doc); print('check ok', ok); assert ok, fails[:5]
st.save(doc); print('items', len(doc['items']))
