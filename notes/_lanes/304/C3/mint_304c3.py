# #304 C3 commit seat - mint the store rows for the wave-three filed reports (doc-row gate, s218-D7),
# and close W-304c2 (its final copy rides this commit, as its own row says). Modelled on C2's mint_304c2.py.
# ID_RE allows at most two suffix characters: W3a's own spec id W-304w3a is illegal, so W-304wa.
import sys, os
sys.path.insert(0, 'knowledge')
import _state as st
S = 'notes/_subreports/'
W3A = S + '2026-09-27-304-W3a-plain-defects.md'
W3B = S + '2026-09-27-304-W3b-why-quality-is-flat.md'
W3C = S + '2026-09-27-304-W3c-ci-121-and-13.md'
V3 = S + '2026-09-27-304-V3-verifier-wave-three.md'
C3 = S + '2026-09-27-304-C3-commit-seat-wave-three.md'
rows = [
 dict(id='W-304wa', home=W3A, owner='dave',
      links=['knowledge/canon/gen_bento_role_vars.py', 'knowledge/canon/dv-render-donut.js', 'knowledge/canon/dv-legend.js',
             'knowledge/canon/canon.css', 'notes/_lanes/304/W3a/NOTES.md', 'notes/_lanes/304/W3a/held-back/README.txt',
             'notes/_lanes/304/V3/kpi-lockup-measure.json'],
      title="#304 W3a filed report - three plain defects fixed at their generators: Common's bento gutter alias and the donut/legend float centre SHIPPED; the Kpi-tile label crop fix HELD BACK for Dave",
      body="s218-D7 filed report, #304 wave three seat W3a (its spec id W-304w3a is illegal under ID_RE, so W-304wa; minted by the C3 commit seat). R4s defects (a), (f) and (g). SHIPPED in the wave-three commit: gen_bento_role_vars reads the registry's attrAliases so Common gets legacy's 24/4 (s227-D8 (1), s219-D1 (5)); the donut and legend centre use the engine's raw-branch rounding (DV-D13 holds). HELD BACK on V3's verdict: the Kpi-tile .kpi-lbl text-box-trim:trim-both fix clears every descender (G8 12 -> 0) but moves the value 4px down (offsetTop 22 -> 26, tile 155.14 -> 159.14) against s261-D4's 'as tight as the original'; W3a's bytes are kept at notes/_lanes/304/W3a/held-back/, V3's renders of before/after/ALT (overflow-x:clip; overflow-y:visible, which keeps the lock-up but fails _validate_descender_clip until the gate learns overflow-y:visible, S) are in notes/_lanes/304/V3/. Declared by W3a: gen_bento_role_vars --check is unwired; the descender gate cannot see an edge without a trim; a compact-format legend re-parse is suspected. V3 nits: selftest bite 7c vacuous, 7b assumes one alias per theme.",
      closes_when="Dave has ruled the Kpi-tile label pair (the trim form, the clip-visible form, or leave it) from V3's renders and that ruling is landed or declined, and a verifier that did not build it has run probe_legend.py on a cold-run page (no float centre) at the seat and filed under notes/_subreports/ citing this report by path"),
 dict(id='W-304wb', home=W3B, owner='dave',
      links=['notes/_lanes/304/W3b/probe_dead.py', 'notes/_lanes/304/W3b/geo-v1013-r2.json', 'notes/_subreports/2026-09-27-304-R4s-cold-run-scores.md'],
      title="#304 W3b - why quality is flat between v1.0.13 and the v1.0.14 candidate: the ceiling is canon and the chart engine, and the rubric scores what the prompt already forces",
      body="s218-D7 filed report, #304 wave three seat W3b (Fable, read-only judgment); row minted by the C3 commit seat. Five changes would visibly move Tuesday's pages, four without a ruling (ring in a tall tile and the axis gutter in the engine, letters and markers off dense series, the donut total, Common's gutter key); one needs Dave's word: whether a chart tile hugs its content or fills the row. Rubric: stop scoring the saturated four, score dead ink, cut ink, collisions, size drift, ground and gutter per view.",
      closes_when="Dave has ruled whether a chart tile hugs its content or fills the row, and whether the rubric changes as the report proposes"),
 dict(id='W-304wc', home=W3C, owner='claude',
      links=['knowledge/_gen_chain.py', 'notes/_lanes/304/W3c/patch_gen_chain.py', 'notes/_lanes/304/W3c/r13_results.txt'],
      title="#304 W3c - CI's [121] fixed at the sentence (the verdict's total is the AST's, a different-sized run is declared), and [13] was [121] nested, not a flake",
      body="s218-D7 filed report, wave-three seat W3c (#304). _gen_chain's verdict line printed the run's step count as the AST's; [13] fails through _capture_gate's call to _gen_chain.selftest; the flake was the survey's own ledger append. Fix + like-with-like bite + mutations; no survey import (a record is always one sha behind).",
      closes_when="the fix is committed with _CHAIN.md regenerated and CI's gates job step 5 reads [121] green and [13] not FAIL, by name"),
 dict(id='W-304v3', home=V3, owner='claude',
      links=[W3A, W3C, 'notes/_lanes/304/V3/kpi-lockup-measure.json'],
      title="#304 V3 - verifier, wave three: W3c PASS, W3a PASS WITH FIXES (the Kpi-tile trio held back - it moves a lock-up Dave ruled at #261)",
      body="s218-D7 filed report, Fable verifier seat, wave three (#304); row minted by the C3 commit seat, which applied its fixes: Kpi-tile snippet, showroom page and canon hunk restored to aaf3bb7e (W3a's bytes kept in notes/_lanes/304/W3a/held-back/), bento block regenerated, 13 chart test pages re-driven 27/27 FRESH with measurements identical, the pre-W3a rollback copies left unstaged.",
      closes_when="the wave-three commit carries its fixes and CI's gates job reads back with no red outside the named set"),
 dict(id='W-304c3', home=C3, owner='claude', links=['knowledge/_git_commit.sh'],
      title="#304 C3 - the commit seat, wave three: W3a (minus the Kpi-tile trio), W3c, the W3b and V3 reports and C2's final copy in one commit, pushed, CI read back",
      body="s218-D7 filed report, commit seat, wave three (#304). The interim copy rides the wave-three commit; the final copy with the sha, push range and CI read-back rides the next commit.",
      closes_when="the final copy of this report, carrying the sha, the push range and CI verdict by job, is committed"),
]
doc = st.load()
have = {i['id']: i for i in doc['items']}
for r in rows:
    assert os.path.exists(r['home']), r['home']
    for l in r['links']:
        assert l.startswith('W-') or os.path.exists(l), l
    assert st.ID_RE.match(r['id']), r['id']
    if r['id'] in have:
        print('exists', r['id']); continue
    st.add(doc, project='apollo', opened=304, state='open', **r)
    print('added', r['id'])
c2 = have['W-304c2']
if c2['state'] != 'done':
    c2['state'] = 'done'
    c2['closed_by'] = ("#304 C3 commit seat: the FINAL copy of notes/_subreports/2026-09-27-304-C2-commit-seat-wave-two.md "
                       "(both shas 4be130e5 and aaf3bb7e, push 6af293df..aaf3bb7e, CI run 36275037261 by job) and its "
                       "transcripts in notes/_lanes/304/C2/ ride the wave-three commit, as the row's close condition says")
    print('closed W-304c2')
ok, fails, _ = st.check(doc)
print('check ok', ok, [f for f in fails if '304' in f][:5])
assert ok, fails[:5]
st.save(doc)
print('saved items', len(doc['items']))
