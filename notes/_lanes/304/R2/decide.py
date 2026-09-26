#!/usr/bin/env python3
"""#304 Run 2a — turn audit_proposals.json into VERDICTS (decisions.json). READ-ONLY on the stores.

Standard for an ENACTED verdict (the only verdict that is stamped):
  S-A  a commit dated on/after the ruling names the id in a clause with a completed-enactment verb, no
       negation, touching a non-record file the ruling governs; hand-read (auto list below, minus EXCLUDE);
  S-B  a non-record file the ruling governs carries the id at HEAD 571d458c, in a line that states or
       implements the ruling, INTRODUCED by a commit dated on/after the ruling whose message names the id
       (range forms like s223-D1..D5 count); hand-read;
  MANUAL  a hand-read receipt of either kind, or a later ruling plus the sha that carried it (listed with
       its reason in MANUAL_ENACTED).
Everything else is UNCERTAIN (a receipt exists that does not meet the standard, or reports conflict) or
NOT-FOUND (no enactment receipt; where a seat PROBED the tree and found it absent, `probe` says so).
"""
import json, re, sys, collections
sys.path.insert(0, 'notes/_lanes/304/R2')
from audit import expand

A = json.load(open('notes/_lanes/304/R2/audit_proposals.json'))
C = {c['sha']: c for c in json.load(open('/tmp/r2/commits.json'))}
C12 = {k[:12]: v for k, v in C.items()}
cache = json.load(open('notes/_lanes/304/R2/intro_cache.json'))
NEGLINE = re.compile(r'\b(NOT (YET )?(ENACTED|BUILT|DONE)|not (yet )?(enacted|built)|owed|OWED|PLACEHOLDER|placeholder|still awaits|pending|TODO|-> ?"fail" enacts)\b')

def names(sha, rid):
    c = C.get(sha) or C12.get(sha[:12])
    return bool(c) and rid in {i for i, _, _ in expand(c['subject'] + '\n' + c['body'])}

# ---- T1 (S-A) hand-read exclusions: the positive clause is NOT this ruling's enactment -------------
EXCLUDE = {
 's186-D2': "clause is about W-25 being moot ('the s186-D2 promotion carried a stale premise'), not an enactment",
 's214-D1': "commit 9c64ac88 says the band was RULED; the enactment verb ('built') belongs to the recall probe (s214-D3)",
 's214-D2': "a no-change ruling (256K stays the wall); 9c64ac88's verb belongs to the probe",
 's244-D1': "the same commit 33062c1b says 's244-D1 … deliberately NOT built here'; no later build receipt found",
 's244-D2': "a sequencing order (#245 runs the reds first); nothing to stamp as enacted in code",
 's224-D2': "a DEFERRAL ruling; 333deee7's 'enacted' refers to the tier-1 port-back (s224-D1)",
}
# ---- MANUAL ENACTED: (sha, receipt sentence) --------------------------------------------------------
MANUAL_ENACTED = {
 's149-D1': ('2bc83b44', "commit 2bc83b44 (#158): 's149-D1 ENACTED AT THE SOURCE: Banner.reference.html mono error ink on-light …'; 0c511016 was the partial first pass; knowledge/_TEXT-CONTRAST-AUDIT.json:278 'ENACTED #158, APPROVED #159'"),
 's165-D4': ('3bde9c08', "commit 3bde9c08: 's170-D1/D2/D3 enacted: six links ratified (s165-D4 closed 37/37)'; later ruling s170-D1 status: 's165-D4's open ratification is CLOSED 37/37'"),
 's190-D1': ('fc3015a7', "commit fc3015a7 '#190 fix 2 — STEP_STATES widened per s190-D1'; knowledge/_gen_lanes.py:43 `superseded` RULED s190-D1"),
 's214-D4': ('540f2cd8', "knowledge/_RUNBOOK-context-gauge.md:368 'THE s214-D4 CONDITIONAL ADVISORY … (ARMED #217, by ADDITION)', introduced by 540f2cd8 which names s214-D4; s260-D2 later puts the band into force"),
 's228-D1': ('ddc7821d', "knowledge/_release/_gen_pack_manifest.py:969 RATIFY_IDS moved 's224-D1 by s228-D1', introduced by ddc7821d 'the v1.0.4 enact set — the ratifying key moves'"),
 's260-D3': ('223310b9', "commit 223310b9 '#260 A: driven receipts become the gate for engine-drawn charts (s260-D3)'; knowledge/_tests/chart-engine/_receipts.json:2 consumer line"),
 's267-D3': ('b5c54d22', "commit b5c54d22 '#267 G: explorer generator reads the authored store' + f5448cb8 's267-D3 enacted, 48 authored edges'; knowledge/_build_kg_explorer.py:102 'The AUTHORED ruling->ruling edges ratified by s267-D3'"),
 's269-D2': ('eb47a582', "later ruling s275-D1 'ux:<id> (… prefix per s269-D2 …)' landed by commit eb47a582 's275-D1..D6 ENACTED (lane RL2)'"),
 's270-D2': ('23f7d166', "commit 23f7d166 's270-D2 RATIFIED (Dave: \"1. ratify\"): the four ROLE/DESK edge types land — gen_kg_roles_desk …'; knowledge/_validate_kg.py:113"),
 's271-D3': ('cf008720', "commit cf008720 's271-D3 enacted (dream-12 P3, expiry-stamp form): run-of-show header carries the dates AS AT 2026-09-14' (the ruling governs that notes page)"),
 's273-D3': ('783a8d9a', "commit 783a8d9a 's273-D3 enacted: LIST vs CARD research (lane LC, Opus)' — the ruling pulled the research forward; it ran"),
 's277-D4': ('f6412422', "commit f6412422 '#279 lane IL: icons landed — s277-D4..D7 … 688 nodes / 1,299 edges'; knowledge/_icon_nodes.json:2 'RATIFIED _icon_nodes.json under s277-D4'"),
 's277-D5': ('f6412422', "commit f6412422 '#279 lane IL: icons landed — s277-D4..D7'"),
 's277-D6': ('f6412422', "commit f6412422 '#279 lane IL: icons landed — s277-D4..D7'; body: 's277-D6's clause is enacted as \"no edge sourced at a base, no defaultActive\"'"),
 's277-D7': ('f6412422', "commit f6412422 '#279 lane IL: icons landed — s277-D4..D7' (the 12 logos entered; s282-D4 later scrapped the identifier lockup, a later ruling, not a non-enactment)"),
 's277-D8': ('2c6b640d', "commit 2c6b640d '#279 lane EX: explorer 1.15 — three views by force'; knowledge/_build_kg_explorer.py:604/617 cite s277-D8"),
 's277-D11': ('eb2ff7c0', "commit eb2ff7c0 '#279 lane VB: the twelve verbs — _kg_verbs.json reading map'; knowledge/_build_kg_explorer.py:992 'THE TWELVE VERBS (s277-D11)'"),
 's277-D13': ('d6bd57ba', "commit d6bd57ba '#279 lane RD: the reader — _compose_slice.py is step 1, thin-slice contract + ASK door'; knowledge/_compose_slice.py:4/8"),
 's278-D1': ('d6bd57ba', "commit d6bd57ba (names s278-D1); knowledge/_compose_slice.py:9 's278-D1 fixed the relationship: the slice is a SEED …'"),
 's282-D3': ('ade8a403', "commit ade8a403 's282-D3 enacted: 8 lockups ×…'; 9a97e006 '\"the sheet is good BTW\" - so s282-D3 is ENACTED'"),
 's283-D1': ('85aee083', "commit 85aee083 '#283 conductor: s283-D1 enacted in the hygiene gate'; knowledge/_RUNBOOK-context-gauge.md:881"),
 's223-D7': ('14af4d76', "knowledge/_release/_gen_pack_manifest.py:962 RATIFY_IDS '\"v1.0.2\": \"s223-D7\"' introduced by 14af4d76 (the v1.0.2 pre-bake fix commit)"),
 's227-D5': ('cec5997d', "commit cec5997d 'cold-start contract: … the B2 merge'; apollo-spider/cold-start/gen_projections.py:77 '(Ruled #227, s227-D5 / red-team B2.)'"),
 's234-D6': ('be52c30f', "knowledge/_validate_screen.py:10/37 carry s234-D6's parse-first clause, introduced by be52c30f (#235, the L1 gate)"),
 's268-D4': ('a4f78ee8', "knowledge/_received.json:3 'THE RECEIVED REGISTER — s268-D4 …' introduced by a4f78ee8 'unreceived releases may be re-cut at version'"),
 's276-D5': ('bedf3838', "s276-D5 ordered the three chart extras authored IN THE NEXT LANE; commit bedf3838 's277-D1..D3 ENACTED (lane LL): the 87 authored edges.obeys land on the four chart metas'"),
 's280-D1': ('b5df9c96', "knowledge/_build_kg_explorer.py:688 '#280 s280-D1: the LAYOUT MATRIX' introduced by b5df9c96 '#280 lane LM'; W-280lm closed 'the six cells are shipped'"),
 's281-D3': ('7f714f0f', "commit 7f714f0f '#281 lane RL: rests on, landed'; knowledge/_build_kg_explorer.py:453 'restsOn (#281, s281-D3 authorised / s281-D6 landed)'"),
 's144-D1': ('a1995c0c', "its own status, amended by addition at #145: 'NAME RULED s145-D1 (Dave) and the rung MINTED in knowledge/tokens/semantic-colour.json'; commit a1995c0c 's145-D1 RULED AND ENACTED IN-WINDOW: THE RUNG IS rag/<se…'"),
 's234-D5': ('5ae4d32c', "knowledge/components/meta.schema.json:277 's234-D5 + s245-D1 … `behaviour` promoted … to a TYPED OBJECT' introduced by 5ae4d32c 'v1.0.6 content: L2/L3/L4 enacted'"),
}
# ---- MANUAL UNCERTAIN (a receipt exists; it does not meet the standard, or reports conflict) --------
MANUAL_UNCERTAIN = {
 's130-D4': "enacted AS AMENDED for mono by s149-D1 (canon.css:6681/6711, commit 0c511016); non-mono themes not proven. RECOMMEND: enacted-as-amended; do NOT re-enact in Run 3 (A1 §2b)",
 's130-D5': "A1 §2b: carried by s149-D1 ('TOUCHES s130-D5 … labels stay ink'); selection-controls.meta.json:143 cites it; no single enacting sha. RECOMMEND: enacted; do NOT re-enact in Run 3",
 's130-D6': "A1 §2b: in effect SUPERSEDED by s151-D2 ('chip pressed = no reversal'); the store has no superseded_by. RECOMMEND: stamp `superseded` (Dave's word) ; do NOT re-enact in Run 3",
 's151-D1': "A1 §2b: enacted through s158-D1..D4 / s160-D2 (ee091eff cites 's151-D1 clause 4'); gate vocabulary landed at f0917690; no single enacting sha. RECOMMEND: enacted; do NOT re-enact in Run 3",
 's151-D2': "A1 §2b: pressed reversal removal + 16-pair migration carried by s158/s160-D2 (ee091eff '(s151-D2 motion)'); no single enacting sha. RECOMMEND: enacted; do NOT re-enact in Run 3",
 's155-D1': "CONFLICT: A1 says enacted via s158-D1..D4; A2 says the two green VALUES are still Dave's; 2022b96d says 'needed no build: values minted #145'. RECOMMEND: Dave's word",
 's131-D2': "its own status and 5b590996 record the MECHANICAL half enacted ('typed edges + parse-gate + index 642->1077'); the Dave's-eye half (s133-D1) is his — part-enacted",
 's135-D2': "A1: the verdicts were applied via s135-D4 (b22e16b9 's135-D4 ENACTED — 82/82 KG VERDICTS'); s135-D2's exceptions ledger 'returns to Dave' not proven. RECOMMEND: enacted via s135-D4",
 's136-D1': "precondition enacted (8b548b87, 0cff8055); the four enact lanes only PARTLY found (A1: 'PARTLY'). RECOMMEND: part-enacted",
 's143-D1': "its own status already reads PART-ENACTED (B) — left as is",
 's172-D1': "multi-part (B1/B2/B3); project field built (gen_dashboard.py:91, e5ab8eed) but B3 'after one dream-pass cycle' not proven",
 's173-D1': "completed by s210-D1 ('one Meter (completes s173-D1)', f75d8f55) and extended by s174-D1; the ruling itself is a scaffold-route gate. RECOMMEND: enacted",
 's174-D1': "own status: 'GATE 2 ENACTED THE SAME SESSION … GATE 5 NOT YET RUN' — part-enacted by its own record",
 's177-D1': "own status: P2/P3/P4a/P4b enacted, P1 DEFERRED — part-enacted",
 's212-D1': "f104cba0 records an EVIDENCE amend only; A2 lists W-99 (ds-018 disabled grey #9D9D9D) as ruled-not-built",
 's216-D1': "A1 probe: no per-theme CSS artefact on disk; only the inscription commit 175246f8 names it",
 's219-D6': "SUPERSEDED by s219-D7 then s219-D8 (_gen_pack_manifest.py:100). RECOMMEND: stamp `superseded`",
 's219-D7': "SUPERSEDED by s219-D8 (_gen_pack_manifest.py:100, :2607). RECOMMEND: stamp `superseded`",
 's219-D9': "the 55-gate figure was superseded by s223-D6's 58 (_gen_pack_manifest.py:451). RECOMMEND: stamp `superseded`",
 's234-D4': "CONFLICT: A2 says the composition edge is 'ruled and unbuilt'; meta.schema.json:811 cites it under s245-D7 (5ae4d32c). RECOMMEND: check groupsWith in metas",
 's251-D7': "schema description cites s251-D3…D8 generically; the 1100-band ownership is a template rule not located",
 's251-D8': "a scheduling intent ('targeted at the SH meeting'); nothing to enact in code",
 's251-D15': "a working-shape ruling for a two-week window (expired 2026-09-21); nothing to enact in code",
 's254-D1': "ratify-as-authored ('all 18 calls KEPT'); nothing moved to enact",
 's256-D1': "44c80619's 'ENACTED' is dream pass 11 (s256-D2); the three stores shipping in the pack not traced to a sha",
 's262-D5': "680823f2 is a lane REPORT commit (1 file) saying 'enacted and inscribed'; the pack-source edit sha not located",
 's265-D1': "an instrument-posture ruling; 27888f1e says the bite-test 'was built, driven and ruled' — posture, not a build",
 's265-D2': "a grading-posture ruling (RUBRIC-ONLY); nothing to enact in code",
 's273-D2': "AUTHORING PASS TWO: 3b9d89be says 's273-D2 pass …' partial; not proven complete",
 's229-D2': "only the inscription commit names it; the four .seg snippets' fix not traced",
 's229-D3': "only the inscription commit names it; the generated-source fix not traced",
 's231-D2': "the bento snippet exists (Template-dashboard-bento.reference.html) but its build commit is not traced to the id",
 's190-D2': "'s190-D2 recorded (150,929 advisory …)' — recorded, not enacted; later superseded by the stop-line rulings",
}
# ---- probe-verified absences (A1 §2a) -----------------------------------------------------------------
PROBED_ABSENT = {
 's114-D6': "A1 probe: knowledge/_validate_a11y.py:64 CONTROL_TIER_44 = \"warn\"",
 's116-D1': "A1 probe: knowledge/_validate_a11y.py:65 MARK_TIER = \"warn\" (its own status already says BLOCKING HALF NOT ENACTED)",
 's114-D2': "A1 probe: status NOT BUILT; no gate file found by name (hedged)",
 's135-D1': "A1 probe: canon.css:2046 one border rule for all themes",
 's135-D3': "A1 probe: mechanism NOT designed; no file cites it",
 's245-D10': "A1 probe: canon console block radius 8/20/20 vs ruled 6/8/12",
 's246-D3': "A1 probe: zero commits name it; absent from _bento_edit_rails.json (hedged)",
 's269-D1': "A1 probe: step-5 edge types appear only in _rulings.json and _memento-index.json (steps 1-4 landed: s270-D2, s274-D8, s275-D2, s277-D4)",
 's269-D6': "A1 probe: no generator or node file carries either kind",
 's277-D12': "A1 probe: 'was never started'; no generator emits bindsToken",
}

out = []
for o in A:
    rid = o['id']; d = {'id': rid, 'population': o['population'], 'date': o['date'], 'status_before': o['status'],
                        'ruled': o['ruled'][:200]}
    if rid in MANUAL_ENACTED:
        sha, why = MANUAL_ENACTED[rid]; d.update(verdict='ENACTED', sha=sha, basis='MANUAL', receipt=why)
    elif rid in PROBED_ABSENT:
        d.update(verdict='NOT-FOUND', probe=PROBED_ABSENT[rid], receipt=PROBED_ABSENT[rid])
    elif rid in MANUAL_UNCERTAIN:
        d.update(verdict='UNCERTAIN', receipt=MANUAL_UNCERTAIN[rid])
    elif o['proposed'] == 'ENACTED' and rid not in EXCLUDE:
        s = o['strong'][0]
        d.update(verdict='ENACTED', sha=s['sha'][:8], basis='S-A',
                 receipt=f"commit {s['sha'][:8]} ({s['date']}) touching {', '.join(s['governs_touched'][:2])}: '{s['clause'][:220]}'")
    else:
        # S-B: governed file carries the id, introduced by a commit on/after the ruling that names it
        sb = None
        for f, ln, txt in o['tree_governs'][:2]:
            ic = cache.get(rid + '|' + f, {}).get('intro')
            if not ic or NEGLINE.search(txt): continue
            if ic[1] >= o['date'] and names(ic[0], rid):
                sb = (ic, f, ln, txt); break
        if sb and rid not in EXCLUDE and not rid.startswith('s272-D') or (sb and rid == 's272-D93'):
            ic, f, ln, txt = sb
            d.update(verdict='ENACTED', sha=ic[0][:8], basis='S-B',
                     receipt=f"{f}:{ln} (HEAD 571d458c) '{txt[:160]}' — introduced by {ic[0][:8]} ({ic[1]}) '{ic[2][:110]}', which names {rid}")
        elif rid.startswith('s272-D') and rid != 's272-D93':
            d.update(verdict='NOT-FOUND', probe="measured #304: the ruled `when`/answer text is carried by NO component meta (substring probe over knowledge/components/*.meta.json); no commit claims enactment; adeef056's 'DISCHARGED by s272-D1..D92' strikes the harvest CARRY, it is not an enactment",
                     receipt="none — ratified wording awaiting the when-rules route (Run 4d) / the MCP catalogue")
        elif rid in EXCLUDE:
            d.update(verdict='UNCERTAIN', receipt=EXCLUDE[rid])
        else:
            rc = []
            if o['pos_other']: rc.append(f"commit {o['pos_other'][0]['sha'][:8]}: '{o['pos_other'][0]['clause'][:160]}'")
            for f, ln, txt in o['tree_governs'][:1]:
                ic = cache.get(rid + '|' + f, {}).get('intro')
                rc.append(f"{f}:{ln} '{txt[:120]}'" + (f" introduced by {ic[0][:8]} ({ic[1]}{'' if names(ic[0], rid) else ', does NOT name the id'})" if ic else ''))
            if not rc and o['tree']: rc.append(f"{o['tree'][0][0]}:{o['tree'][0][1]} '{o['tree'][0][2][:120]}' (not a governed file)")
            if not rc and o['later_rulings']: rc.append(f"later ruling {o['later_rulings'][0][0]}: '{o['later_rulings'][0][1][:140]}'")
            d.update(verdict='UNCERTAIN' if rc else 'NOT-FOUND', receipt=' | '.join(rc) if rc else 'no commit, tree or later-ruling receipt found')
    out.append(d)
json.dump(out, open('notes/_lanes/304/R2/decisions.json', 'w'), ensure_ascii=False, indent=1)
cnt = collections.Counter((d['population'], d['verdict']) for d in out)
print(len(out)); [print(' ', k, v) for k, v in sorted(cnt.items())]
print('ENACTED by basis', collections.Counter(d.get('basis') for d in out if d['verdict'] == 'ENACTED'))
