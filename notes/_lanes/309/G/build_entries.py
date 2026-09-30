# #309 lane G - the three by-click answers as ruling entries (lane I's shape, #308).
# Labels and questions are quoted from the export and the page; never paraphrased.
import json, pathlib
EXP = "notes/_lanes/309/DAVE-RULINGS-2026-09-30-1104-metric-and-the-arrow.md"
PAGE = "notes/_REVIEW-309-metric-and-the-arrow-2026-09-30-v1.html"
exp = open(EXP).read()
page = open(PAGE).read()
SAYS0 = ("review page export, Wed 2026-09-30 11:04 BST ('Copy as text' pasted into chat #309; " + PAGE +
         ", saved verbatim as " + EXP + "; the page's whole note not answered; items 2 and 7 not answered) · "
         "section '06 · Three smaller calls'")
calls = [
 dict(id="s309-D5", item="6a", q="Should a cost going up show red?", label="Let a metric say up is bad",
      page_label='Let a metric say \\"up is bad\\"', rec=False, rec_label="Keep direction for now",
      rec_line="keep direction only for now, and decide when a real page needs it.",
      head="THE REVIEW PAGE'S CALL ON WHETHER A COST GOING UP SHOWS RED IS ANSWERED BY CLICK: LET A METRIC SAY UP IS BAD.",
      plain=("Metric gains one optional setting that says a rise is bad for this figure: a rise then takes the fall ink "
             "and a fall the rise ink, and the arrow still points the way the number moved. The default stays as it is, "
             "colour by direction (s182-D3, col26-016, dv-017). No live page is switched to it: which metrics are up-is-bad "
             "is Dave's content call, page by page."),
      record="RECORD: carried by #309 lane G (notes/_lanes/309/G/BRIEF.md); the setting is added to Metric's reference file, its meta and canon; no live page uses it.",
      governs=["knowledge/snippets/Metric.reference.html","knowledge/components/metric.meta.json","knowledge/canon/canon.css"],
      extra=["notes/_subreports/2026-09-30-309-D-stat-card-to-metric.md"]),
 dict(id="s309-D6", item="6b", q="The no-change mark: full ink or 60%?", label="Full ink, as ruled",
      page_label=None, rec=True, rec_label=None, rec_line="full ink, as ruled.",
      head="THE REVIEW PAGE'S CALL ON METRIC'S NO-CHANGE MARK IS ANSWERED BY CLICK: FULL INK, AS RULED.",
      plain=("Metric's no-change arrow is drawn at the full standing ink (near-black on light, white on dark, s182-D3), "
             "not at 60% of it. The words 'No change' and the period beside it are untouched."),
      record="RECORD: carried by #309 lane G (notes/_lanes/309/G/BRIEF.md); the 60% is removed from the flat glyph in Metric's reference file and canon.",
      governs=["knowledge/snippets/Metric.reference.html","knowledge/components/metric.meta.json","knowledge/canon/canon.css"],
      extra=["notes/_subreports/2026-09-30-309-D-stat-card-to-metric.md"]),
 dict(id="s309-D7", item="6c", q="Every lane runs the pre-push check before handing back?", label="Yes",
      page_label=None, rec=True, rec_label=None, rec_line="yes.",
      head="THE REVIEW PAGE'S CALL ON A PRE-PUSH CHECK FOR EVERY LANE IS ANSWERED BY CLICK: YES.",
      plain=("Every lane surveys its own commit in a throwaway clone before handing back (lane E's routine: the survey in four "
             "chunks with the writer gates asked, the tests after the build, and the state-contrast sweep when a snippet or "
             "canon.css changed), so a red CI would give is found before the conductor pushes."),
      record="RECORD: carried by #309 lane G (notes/_lanes/309/G/BRIEF.md); the routine is written into the Worker checklist of knowledge/_RUNBOOK-parallel-conductor.md, by addition.",
      governs=["knowledge/_RUNBOOK-parallel-conductor.md"],
      extra=["notes/_subreports/2026-09-30-309-E-checks-at-the-seat.md"]),
]
for c in calls:
    # verify every quoted string against its source, byte for byte
    assert f"{c['item']}. {c['q']}" in exp, c['q']
    tag = "(the recommendation)" if c['rec'] else "(not the recommendation)"
    assert f"Chose: {c['label']} {tag}" in exp, c['label']
    assert c['q'].replace('"','&quot;') in page or c['q'] in page, c['q']
    assert c['rec_line'] in page, c['rec_line']
    if c['rec_label']: assert c['rec_label'] in page
    pl = f" (the page's button reads '{c['page_label'].replace(chr(92),'')}')" if c['page_label'] else ""
    if c['rec']:
        ans = f"Dave's answer, by click, verbatim: '{c['label']}' (the recommendation){pl}"
    else:
        ans = (f"Dave's answer, by click, verbatim: '{c['label']}'{pl} (NOT the recommendation, which was "
               f"'{c['rec_label']}'; the page's recommendation line, verbatim: '{c['rec_line']}')")
    ruled = (f"{c['head']} {c['plain']} {ans}, to the call's question, verbatim: '{c['q']}'. "
             f"No comment on the call. The #309 review page, section '06 · Three smaller calls', call {c['item']}. {c['record']}")
    says = (f"{SAYS0} · call {c['item']}, verbatim: '{c['q']}' — his answer, by click (the export carries no click time), "
            f"verbatim: '{c['label']}' {'(the recommendation)' if c['rec'] else '(NOT the recommendation)'} · comment: none")
    e = {"id": c['id'], "date": "2026-09-30", "by": "Dave", "status": "ruled", "ruled": ruled, "says": says,
         "governs": c['governs'],
         "evidence": ["chat #309 2026-09-30 (live) - his 11:04 BST export of the review page; his click on this call is in it, quoted verbatim in `says`",
                      EXP, PAGE] + c['extra']}
    pathlib.Path(f"notes/_lanes/309/G/entries/{c['id']}.json").write_text(json.dumps(e, ensure_ascii=False, indent=1) + "\n")
    print(c['id'], "ok", len(ruled))
