#!/usr/bin/env python3
"""#305 H1 — calls 13, 31, 32, 33, 34, 35, 37 applied to knowledge/_state.json through the store's own API
(_state.load -> mutate -> _state.check -> _state.save), BY ADDITION: closes carry `closed_by`, parks append a
dated paragraph to `body`; no closes_when is rewritten except the 14 legacy rows' null -> a stated close (call 35).
  python3 notes/_lanes/305/H1/store_batch.py --dry-run | --write     (idempotent: rows no longer open are skipped)"""
import json, sys, os, subprocess, datetime, collections
sys.path.insert(0, 'knowledge'); sys.path.insert(0, 'notes/_lanes/305/B4')
import _state, rows as B4
WRITE = '--write' in sys.argv
LANE = 'notes/_lanes/305/H1'
D = json.load(open('notes/_lanes/304/A2/decision_unblocks.json'))
V = {x['id']: x for x in json.load(open('notes/_lanes/304/A2/verify.json'))}
L = {k.split()[0]: v for k, v in D.items()}
doc = _state.load(); by = {i['id']: i for i in doc['items']}
before = _state.counts(doc)
live = lambda i: by[i]['state'] == 'open'
S31, S32, S33, S34, S37 = (L['D1'], [i for i in L['D2'] if live(i)], [i for i in L['D3'] if live(i)], L['D7'],
                           L['D6'] + L['D8'])
assert (len(S31), len(S32), len(S33), len(L['D7']), len(L['D6']), len(L['D8'])) == (95, 102, 22, 17, 12, 20), 'set sizes moved'
def sha_ok(s):
    return subprocess.run(['git', '--no-optional-locks', 'cat-file', '-e', s + '^{commit}'], capture_output=True).returncode == 0
HEAD = "#305 H1 (2026-09-27)"
FRI = ("RECEIPT: Friday 2026-09-25 happened — his note `notes/_lanes/305/FRIDAY-2026-09-25-what-came-back.md`, verbatim: "
       "\"nothing of substance came out of it aopart from people wanting to know more. The CEO prompt ran well\"")
C31 = ("`s305-D31` (Dave, sitting call 31, 14:26 BST, \"yes\" to 'Close the 95 deck, drawing and presentation rows whose close "
       "is \"Friday's deck is final\"?')")
C34 = "`s305-D34` (Dave, sitting call 34, 14:27 BST, \"yes\" to 'Close your 17 rows whose closing event has already happened?')"
C33 = "`s305-D33` (Dave, sitting call 33, 14:27 BST, \"yes\" to 'Close the 22 release rows for v1.0.1 to v1.0.12 as superseded by v1.0.13?')"
C32 = ("`s305-D32` — Dave, sitting call 32 (14:27 BST), verbatim: \"park but surface for me so I can have a scan of it\"")
C37 = ("`s305-D37` — Dave, sitting call 37 (14:28 BST), \"yes\" to 'Park the 12 component-wave rows and the 20 decision pages "
       "whose export never came back?', tripwire \"reopen when the catalogue lists the component\"")
C35 = "`s305-D35` (Dave, sitting call 35, 14:27 BST, \"yes\" to 'The 14 oldest rows with no close condition: take the disposition proposed for each?')"
def d7_receipt(i):
    r = V[i]['receipts']; shas = [w.rstrip(')') for x in r for w in x.split() if len(w.rstrip(')')) >= 7 and all(c in '0123456789abcdef' for c in w.rstrip(')'))]
    bad = [s for s in shas if not sha_ok(s)]
    assert V[i]['verdict'] in ('EVENT-PASSED', 'FILED') and not bad, (i, bad)
    return f"A2 verify ({V[i]['verdict']}): {'; '.join(r)} — commit(s) resolved at HEAD by `git cat-file`"
ops = []   # (id, kind, detail)
def close(i, text, state='done'):
    it = by[i]
    if it['state'] != 'open': ops.append((i, 'SKIP-not-open', it['state'])); return
    it['state'] = state; it['closed_by'] = text; ops.append((i, state, text[:90]))
def park(i, para):
    it = by[i]
    if it['state'] != 'open': ops.append((i, 'SKIP-not-open', it['state'])); return
    it['state'] = 'parked'; it['body'] = ((it.get('body') or '').rstrip() + '\n\n' + para).lstrip()
    ops.append((i, 'parked', para[:90]))
# ---- call 31 (+34 overlap)
for i in S31:
    t = f"{HEAD} — CLOSED BY ADDITION under {C31}. {FRI}. Every file this row points at stays. Set: A2 D1, `notes/_lanes/304/A2/decision_unblocks.json`."
    if i in L['D7']:
        t += f" ALSO in call 34's set, {C34}: {d7_receipt(i)}."
    if i in L['D8']:
        t += " ALSO in call 37's export-page set (A2 D8); call 31's close is applied, so it is not parked."
    close(i, t)
# ---- call 34 (rest)
for i in L['D7']:
    if i in S31: continue
    close(i, f"{HEAD} — CLOSED BY ADDITION under {C34}: its closing event has happened. RECEIPT, {d7_receipt(i)}. Set: A2 D7, `notes/_lanes/304/A2/decision_unblocks.json`.")
# ---- call 32 (+37 overlap)
SCAN = 'notes/_SCAN-305-parked-questions-2026-09-27-v1.html'
for i in S32:
    q, trip = B4.ROWS[i]
    p = (f"⏸ PARKED #305 2026-09-27 under {C32}. SURFACED on the scan page `{SCAN}` (lane B4) as: \"{q}\" "
         f"TRIPWIRE: reopens when {trip}. Any row he ticks \"Keep open\" on that page is reopened (state → open) by addition. "
         f"`closes_when` above is unchanged.")
    if i in L['D6']:
        p += f" ALSO under {C37}."
    if i in L['D3']:
        p += (" ALSO in call 33's release set (A2 D3); parked, not closed, because it is on the scan page he asked to see "
              "(call 33's close would take it off his scan).")
    park(i, p)
# ---- call 37
for i in L['D6'] + L['D8']:
    if i in S32 or i in S31: continue
    extra = (" The housekeeping page's words for this set: \"Each reopens if its export turns up.\"" if i in L['D8'] else '')
    park(i, f"⏸ PARKED #305 2026-09-27 under {C37}. TRIPWIRE: reopen when the catalogue lists the component.{extra} "
            f"Every page stays. `closes_when` above is unchanged. Set: A2 {'D8' if i in L['D8'] else 'D6'}.")
# ---- call 33
V13 = ("SUPERSEDED BY v1.0.13: ratified `s268-D3` (Dave \"okay do 13\", 2026-09-11) on the cut at 08e315dca376 "
       "(`knowledge/_release/_gen_pack_manifest.py` RATIFY_IDS \"v1.0.13\"), and since overtaken again by v1.0.14, released at "
       "0ef30746 under `s305-D2` (#305). The row's own close condition is NOT claimed met; it is closed as overtaken, on his word. "
       "Every file stays. Set: A2 D3, `notes/_lanes/304/A2/decision_unblocks.json`.")
assert sha_ok('0ef30746') and sha_ok('08e315dca376')
for i in S33:
    if i in S32: continue
    close(i, f"{HEAD} — CLOSED BY ADDITION under {C33}. {V13}")
# ---- call 13
t13 = (f"{HEAD} — CLOSED BY ADDITION under `s305-D14` (Dave, sitting call 13, 14:17 BST, verbatim \"accept\": 'The console radius set "
       "is built: does the console read right at control 6, surface 8, container 12?'). Each limb of closes_when, receipted: "
       "(1) wave two committed as 4be130e5 with the stamps at aaf3bb7e, pushed, CI run 36275037261 read back by name "
       "(`notes/_subreports/2026-09-27-304-C2-commit-seat-wave-two.md` lines 10-12; 4be130e5 is on origin/master); "
       "(2) `s245-D10` status reads enacted with commit 4be130e5 in its evidence, and `s277-D12` reads enacted; "
       "(3) his eye: \"accept\" (the sitting page says \"Your eye closes the row\"); "
       "(4) gen_kg_tokens.py --check and --selftest are in `knowledge/_build_all.py` STEPS (lines 367-368).")
assert sha_ok('4be130e5') and sha_ok('aaf3bb7e')
close('W-304r3', t13)
# ---- call 35 — the fourteen legacy rows (A2 §7 / housekeeping page table), each by its own proposed disposition
def restate(i, cw, note, state=None):
    it = by[i]
    if it['condition'] != 'UNCONDITIONED': ops.append((i, 'SKIP-already-conditioned', '')); return
    it['condition'] = 'stated'; it['closes_when'] = cw
    it['body'] = ((it.get('body') or '').rstrip() + '\n\n' + f"✎ #305 2026-09-27 — close condition STATED under {C35}: {note} "
                  f"Before this, `closes_when` was null (UNCONDITIONED, legacy DOFIRST).").lstrip()
    if state: it['state'] = state
    ops.append((i, 'restated' + (f'+{state}' if state else ''), cw[:90]))
def legacy_close(i, text, state='done'):
    it = by[i]
    if it['condition'] != 'UNCONDITIONED': ops.append((i, 'SKIP-already-conditioned', '')); return
    close(i, f"{HEAD} — CLOSED BY ADDITION under {C35}. {text}", state)
restate('W-0b', "finding 1 of notes/_briefs/2026-07-28-chart-encoding-gaps-carry-forward.md has its remedy ruled, or is ruled superseded by the #259/#260 chart engine",
        "the page's disposition, \"Close when its first finding is ruled, or rule it overtaken by the chart engine of 8 and 9 September (estimate).\"")
restate('W-01', "FOLDED into W-99 (the s212-D1 disabled-grey enactment, #9D9D9D light / #808080 dark): this row closes when W-99 closes",
        "the page's disposition, \"Fold into the disabled-grey build row and close with it.\"")
restate('W-02', "the page-budget rulings (s250-D1, s260-D1 'core priced once per page') are confirmed to replace the dv-legend/dv-behaviour size ceiling",
        "the page's disposition, \"Close when the page-budget rulings are confirmed to replace it (estimate).\"")
restate('W-03', "Chart-bar renders the real HSBC labels unclipped at the narrow floor, render-proved, and Dave's eye passes the floor",
        "the page's disposition, \"Close when the bar chart renders real HSBC labels unclipped at the narrow floor and your eye passes it.\"")
restate('W-04', "FOLDED into W-175 (DV-D16 wording 2, on 2 of 3 stacked surfaces): this row closes when the third stacked surface carries it",
        "the page's disposition, \"Fold into the stacked-surfaces row; close when the third surface carries it.\"")
restate('W-06', "FOLDED into the citation gate s114-D2 (ds-016 remedy (a)), parked under s305-D39 in knowledge/_parked.json: this row closes when s114-D2 is built",
        "the page's disposition, \"Fold into the citation gate, which the stamps page recommends parking.\" The citation gate is parked (call 39), so this row is parked with it.", state='parked')
restate('W-11', "W-17's 'rolls retired' lands (the 2c/2d/2f rolls stop), or Dave rules the deadlock overtaken",
        "the page's disposition, \"Close when the rolls are retired, or rule it overtaken now.\" His yes did not pick the second branch, so the checkable first branch is the close.")
restate('W-13', "no runbook under knowledge/ instructs a write to /tmp, and a grep arm in a gate proves it",
        "the page's disposition, \"Close when no runbook does, with a gate that proves it.\"")
NEW = [
 dict(id='W-305h1', title="W-05 part (4): the consult enforcement column — fix it (your lean), yes or no?", project='apollo', state='open', opened=305, owner='dave',
      closes_when="Dave answers the one question — fix the consult enforcement column, or leave it — in chat or on a sitting page", condition='stated',
      home='GOOD-MORNING.md#> **5.', links=['W-05'],
      body=f"Split from W-05 under {C35}: \"turn part 4 into one question\". GOOD-MORNING DOFIRST 5 (4), verbatim: \"consult enforcement column: Dave leans fix but wants the DISCUSSION — have it before touching\"."),
 dict(id='W-305h2', title="W-08 (i): the showroom type sweep folded into the register as a P2 proof, not re-run one-off", project='apollo', state='open', opened=305, owner='claude',
      closes_when="knowledge/_type-sweep-2026-07-27.json is folded into the register as a P2 proof (run with --allow-file-access-from-files), or Dave drops it", condition='stated',
      home='GOOD-MORNING.md#> **8.', links=['W-08'],
      body=f"Split from W-08 under {C35} (\"Split any live one into its own row, close the bundle.\"). DOFIRST 8 (i), verbatim: \"showroom type sweep → fold into the register as a P2 proof, don't re-run one-off (knowledge/_type-sweep-2026-07-27.json; ⚠ needs --allow-file-access-from-files or it reads a cheerful zero)\". No other store row carries it (grep of titles/bodies for 'type sweep', #305 H1)."),
 dict(id='W-305h3', title="W-08 (ii): the GOOD-MORNING §C·2 ruling batch (15 + 17-22), unmoved since July", project='apollo', state='open', opened=305, owner='dave',
      closes_when="Dave rules, parks or strikes the GOOD-MORNING §2 ruling batch items 15 and 17-22", condition='stated',
      home='GOOD-MORNING.md#> **8.', links=['W-08'],
      body=f"Split from W-08 under {C35}. DOFIRST 8 (ii), verbatim: \"§C·2 RULING BATCH 15 + 17–22 — unmoved for days, gates §C·1(c); Fable is the model\". GOOD-MORNING still carries '## 2. ★ DAVE: THE RULING BATCH — 15 REMAIN of 16'; no store row carries it (#305 H1 grep)."),
 dict(id='W-305h4', title="W-08 (v): showroom/chart-bar.html cb5 rendered and unseen by Dave (series-3 at 4.61:1)", project='apollo', state='open', opened=305, owner='dave',
      closes_when="Dave has looked at showroom/chart-bar.html cb5 and passed it or named a change, or it is superseded by a later chart-bar review", condition='stated',
      home='GOOD-MORNING.md#> **8.', links=['W-08'],
      body=f"Split from W-08 under {C35}. DOFIRST 8 (v), verbatim: \"showroom/chart-bar.html cb5 rendered, UNSEEN by Dave — ⚠ series-3 at 4.61:1 (0.11 over AA) constrains any re-tune of that hue\". No store row names cb5 (#305 H1 grep)."),
]
legacy_close('W-05', "The page's disposition, \"Park part 2 with a tripwire, turn part 4 into one question, close the row.\" Part (5) is DONE #66 "
             "(the row's own GOOD-MORNING DOFIRST 5 text: \"`CTRL` vocabulary sweep: ✅ DONE #66\"). Part (2), the adoption-time citation half, IS "
             "`s114-D2` (its own `says`: \"This IS DO-FIRST item 5(2)'s adoption-time half\"), parked with a tripwire under `s305-D39` in "
             "`knowledge/_parked.json` (P-305-2). Part (4) is now one question, W-305h1.")
legacy_close('W-07', "The page's disposition, \"A floated item that would overrule a standing instruction. Rule it overtaken by the work store and "
             "strike-by-addition (estimate).\" — his yes rules it OVERTAKEN by the task store `knowledge/_state.json` (#88) and the strike-by-addition regime (`s183-D1`, `s188-D2`).")
legacy_close('W-08', "The page's disposition, \"Six sub-items still owed from late July. Split any live one into its own row, close the bundle.\" "
             "(i) → W-305h2 · (ii) → W-305h3 · (iii) hit-area rule + gate → already carried by W-99n (s114-D5/s114-D6) · (iv) the radius/corner "
             "tuner → already carried by W-407/W-411 (built #244, s244-D2) · (v) → W-305h4 · (vi) ds-014(d) donut cluster → already carried by W-99q "
             "(\"ds-014(d) donut cluster … rule it live\"). Nothing in the bundle is dropped.")
legacy_close('W-09', "The page's disposition, \"How work is delegated between seats. Close as answered by the team shape you adopted on 19 August.\" — "
             "answered by `s204-D1`, the PM topology \"ADOPTED WITH FOUR AMENDMENTS\".")
legacy_close('W-10', "The page's disposition, \"The per-gate test plan. Close: its own text says closed, all five ratified.\" — its body, verbatim: "
             "\"CLOSED #64: 5/5 DRAFTED AND 5/5 RATIFIED (9bc34af\".")
legacy_close('W-12', "DROPPED on the page's disposition, \"A July dossier still marked owed. Drop.\" The only #57-era dossier on disk is #58's "
             "(`_DECISION-HISTORY/2026-07-30-the-ritual-and-the-two-stale-clauses.md`).", state='dropped')
assert sha_ok('9bc34af')
for n in NEW:
    if n['id'] in by: ops.append((n['id'], 'SKIP-exists', '')); continue
    doc['items'].append(n); by[n['id']] = n; ops.append((n['id'], 'added', n['title'][:80]))
ok, fails, notes = _state.check(doc)
after = _state.counts(doc)
kinds = collections.Counter(k for _, k, _ in ops)
print(('WRITE' if WRITE else 'DRY-RUN'), dict(kinds), 'check ok', ok, 'fails', len(fails))
for f in fails[:8]: print('  FAIL', f[:300])
print(' before live', before['live'], before['by_state'], before['by_owner'], 'uncond', before['unconditioned'])
print(' after  live', after['live'], after['by_state'], after['by_owner'], 'uncond', after['unconditioned'])
json.dump({'ops': ops, 'before': before, 'after': after, 'check_ok': ok}, open(f'{LANE}/store_batch.{"write" if WRITE else "dry"}.json', 'w'), indent=1, ensure_ascii=False)
if WRITE and ok:
    st = os.stat('knowledge/_state.json').st_mtime
    _state.save(doc); print(' saved')
