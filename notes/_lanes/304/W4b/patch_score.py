"""W4b: patch the harness score.py — views phase, floor, ink, judgment rows, runs dir by env."""
P = "notes/_lanes/304/R4c/harness/score.py"
s = open(P).read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, (c, old[:100])
    s = s.replace(old, new)

rep('''  ext      4b's geometry and own-size gates, if found (see EXT_GATES below). exit 77 = absent.
  card     scorecard.json + scorecard.html from whatever phases exist (missing = 'not run').
  all      stage→card, skipping phases already on disk unless --force.''',
'''  views    (W4b) EVERY view the run built — linked files, ?view= and #/ routes, script-swapped views —
           found by clicking the nav in fresh contexts and measured where the click left it: the five
           INK classes (dead ink, cut ink, collisions, size drift, markers) from the geometry and
           own-size gates' own code, rendered text (script-written included), charts, and the theme
           switch in BOTH directions. See views.py. Resumable.
  ext      4b's geometry and own-size gates, if found (see EXT_GATES below). exit 77 = absent.
  card     scorecard.json + scorecard.html from whatever phases exist (missing = 'not run').
  all      stage→card, skipping phases already on disk unless --force.
  selftest-views  (W4b) ink planted vs clean, three routing shapes, script text, theme both ways + a
           one-way mutant, determinism. Needs no stage.

THE SCORE (W4b, restructured on W3b #304 §4). The four rubric parts are a FLOOR, not a sum: each must
be 2 or more, and the card says PASS or names the parts that fail; they saturate on the CEO prompt, so
summing them cannot rank runs. The COMPARABLE score is INK: affected tiles per class across every
view, and "ink defects per 10 tiles" (lower is better), each with its worst case. Two JUDGMENT ROWS
are printed with their evidence and left blank for Dave's eye, never filled by the harness: does the
overview answer the three questions as three visible groups; is any ring chart in a tile wider than
half the wall. The /12 sum is still computed (`total`, for continuity) and labelled legacy.''')
rep('''RUNS = os.path.join(LANE, "runs")''', '''RUNS = os.path.abspath(os.environ.get("R4C_RUNS") or os.path.join(LANE, "runs"))   # W4b: a re-score writes elsewhere''')
rep('''HARNESS_VERSION = "r4c-1.0"''', '''HARNESS_VERSION = "w4b-2.0"   # r4c-1.0 + the views phase, floor/ink score (#304 W4b)
INK_CLASSES = [("dead", "dead ink", "G6 empty band ≥48px in a tile, or G12 a chart covering <35% of its box"),
               ("cut", "cut ink", "G8 glyphs cut by an overflow box or past a scroll box's start edge"),
               ("collision", "collisions", "G7 text ink on text ink"),
               ("size", "size drift", "own-size S1/S2/S3: a cn- part off its reference size"),
               ("markers", "markers", "G11 a mark on every point of a series longer than 12")]
JUDGMENT_ROWS = [
    ("three_questions", "Does the overview answer the three CEO questions as three visible groups (resilience · exposure · decisions)?",
     "the overview's headings, in order"),
    ("ring_in_wide_tile", "Is any ring chart (donut or pie) sitting in a tile wider than half the wall?",
     "every ring chart on every view, with its tile's share of the content width"),
]''')

# score(): views integration
rep('''    ent = (rn or {}).get("entry", {})
    light = ent.get("light") or {}
    subs = (rn or {}).get("subpages", [])''', '''    ent = (rn or {}).get("entry", {})
    light = ent.get("light") or {}
    subs = (rn or {}).get("subpages", [])
    vw = jload(os.path.join(rd, "views.json"), None) or {}
    kept = [v for v in vw.get("views", []) if v.get("kept")]
    if not kept: S["missing_phases"].append("views")''')
rep('''    rendered = [c for c in charts if c.get("marks", 0) > 0 and c.get("w", 0) > 20 and c.get("h", 0) > 20]
    clipped = [c for c in charts if c.get("clipped")]''', '''    rendered = [c for c in charts if c.get("marks", 0) > 0 and c.get("w", 0) > 20 and c.get("h", 0) > 20]
    clipped = [c for c in charts if c.get("clipped")]
    if kept:
        # W4b: every VIEW, not the entry page + linked files; a chart is clipped only when something CUTS
        # it (overflow hidden/clip, or a scroll box's start edge) — below a shell's fold is reachable
        vch = [dict(c, page=v.get("head") or v.get("nav_text")) for v in kept for c in v["page"]["charts"]]
        rendered = [c for c in vch if c.get("marks", 0) > 0 and c.get("w", 0) > 20 and c.get("h", 0) > 20]
        clipped = [dict(c, clipped=True, clip_by=c["clip"]["by"], clip_px=c["clip"]["px"]) for c in vch if c.get("clip")]''')
rep('''    templates_seen = sorted(c for c in comp_set if c.startswith("template-"))''', '''    comp_set |= {c for v in kept for c in v["page"].get("components", []) if c in slugs_known}
    templates_seen = sorted(c for c in comp_set if c.startswith("template-"))''')
rep('''        kp = (st.get("keywords") or {}).get("kpis", {})
        qs = (st.get("keywords") or {}).get("questions", {})
        rows = max([light.get("max_table_rows", 0)] + [sp.get("max_table_rows", 0) for sp in subs])''', '''        kp = (st.get("keywords") or {}).get("kpis", {})
        qs = (st.get("keywords") or {}).get("questions", {})
        rows = max([light.get("max_table_rows", 0)] + [sp.get("max_table_rows", 0) for sp in subs])
        if kept:
            # W4b: RENDERED text of every view (script-written text included), not the page source
            kp = {k: any(v["page"]["kpi_words"].get(k) for v in kept) for k in prof.get("kpis", {})}
            qs = {k: any(v["page"]["question_words"].get(k) for v in kept) for k in prof.get("questions", {})}
            rows = max([rows] + [v["page"].get("rows", 0) for v in kept])
            views_live = max(views_live, len(kept))''')
rep('''        if prof["theme"].get("switch_required") and dr:
            sw = th.get("switch") or {}
            checks.append(("light/dark switch flips the theme, on <html>", bool(sw.get("flips")) and bool(sw.get("on_html"))))''',
'''        if prof["theme"].get("switch_required") and vw.get("theme_switch"):
            ts = vw["theme_switch"]; th["switch_both_ways"] = ts
            checks.append(("the run's own switch goes to dark and BACK to light, on <html> (%s, then %s)" % (
                (ts.get("to_dark_control") or {}).get("found"), (ts.get("to_light_control") or {}).get("found")), ts.get("verdict") == "PASS"))
        elif prof["theme"].get("switch_required") and dr:
            sw = th.get("switch") or {}
            checks.append(("light/dark switch flips the theme, on <html>", bool(sw.get("flips")) and bool(sw.get("on_html"))))''')
rep('''    S["judgment"] = JUDGMENT
    S["meta"] = m''', '''    S["total_is_legacy"] = True
    # ---------- W4b: the FLOOR (four parts, pass/fail each at >= 2), the INK score, the two judgment rows
    fl = {k: (dims[k]["score"] if k in dims else None) for k in ("visually_rich", "full", "persistent", "interactive")}
    fails = [k for k, v in fl.items() if v is None or v < 2]
    S["floor"] = {"parts": fl, "min": 2, "verdict": "PASS" if not fails else ("INCOMPLETE" if any(fl[k] is None for k in fails) else "FAIL"),
                  "failing": fails, "rule": "each rubric part must reach 2; the parts are never summed"}
    if kept:
        tiles = sum(v["ink"]["tiles"] for v in kept)
        aff = {k: sum(v["ink"]["affected"][k] for v in kept) for k, _, _ in INK_CLASSES}
        inst = {k: sum(v["ink"]["instances"][k] for v in kept) for k, _, _ in INK_CLASSES}
        W = [v["ink"]["worst"] for v in kept]
        worst = {"dead": max(w["dead"] for w in W), "dead_ring_cover_pct": min(w.get("dead_ring_cover_pct", 100) for w in W),
                 "cut": max(w["cut"] for w in W), "collision": max(w["collision"] for w in W),
                 "size": min(w["size"] for w in W), "markers": max(w["markers"] for w in W)}
        S["ink"] = {"views": len(kept), "tiles": tiles, "affected": aff, "instances": inst, "worst": worst,
                    "per10": round(10.0 * sum(aff.values()) / max(tiles, 1), 2),
                    "per10_by_class": {k: round(10.0 * aff[k] / max(tiles, 1), 2) for k in aff},
                    "clean_views": sum(1 for v in kept if not any(v["ink"]["affected"].values())),
                    "font_ok": all(v.get("font_ok") for v in kept),
                    "per_view": [{"view": v.get("head") or v.get("nav_text"), "url": v.get("url"), "tiles": v["ink"]["tiles"],
                                  "affected": v["ink"]["affected"], "worst": v["ink"]["worst"], "shot": v.get("shot"),
                                  "sample": v["ink"].get("sample")} for v in kept],
                    "rule": "affected = distinct tiles (or parts, for size) carrying the class; per10 = 10 x all affected / all tiles, every view; lower is better",
                    "gates": vw.get("gates")}
        ov = kept[0]["page"]
        rings = [{"view": v.get("head") or v.get("nav_text"), "type": c["type"], "tile_share_of_content_width": c.get("tile_frac"), "w": c["w"], "h": c["h"]}
                 for v in kept for c in v["page"]["charts"] if c.get("type") in ("donut", "pie")]
        S["judgment_rows"] = [{"id": "three_questions", "row": JUDGMENT_ROWS[0][1], "evidence_label": JUDGMENT_ROWS[0][2],
                               "evidence": ov.get("headings", []), "answer": None},
                              {"id": "ring_in_wide_tile", "row": JUDGMENT_ROWS[1][1], "evidence_label": JUDGMENT_ROWS[1][2],
                               "evidence": rings, "answer": None}]
    else:
        S["ink"] = None
        S["judgment_rows"] = [{"id": i, "row": r, "evidence_label": e, "evidence": None, "answer": None} for i, r, e in JUDGMENT_ROWS]
    S["judgment"] = JUDGMENT
    S["meta"] = m''')
rep('''    S["reproduce"] = ["python3 notes/_lanes/304/R4c/harness/score.py %s --run-id %s" % (p, rid) for p in ("static", "gates", "render", "drive", "ext", "card")]''',
    '''    S["reproduce"] = ["python3 notes/_lanes/304/R4c/harness/score.py %s --run-id %s" % (p, rid) for p in ("static", "gates", "render", "drive", "views", "ext", "card")]''')

# card
rep('''    tot = S.get("total")
    out.append("<p><span class='tag'>mechanical total %s / 12</span> <span class='tag'>geometry (4b) %s / 3</span> %s</p>" % (esc(tot if tot is not None else "incomplete"), esc(S.get("geometry_score") if S.get("geometry_score") is not None else "not scored"),
               ("<span class='warn'>phases missing: %s</span>" % esc(", ".join(S["missing_phases"]))) if S["missing_phases"] else ""))
    out.append("<h2>The four-part rubric, measured</h2><div class='grid4'>")''', '''    tot = S.get("total")
    fl = S.get("floor") or {}
    ink = S.get("ink")
    out.append("<p><span class='tag %s'>floor %s%s</span> <span class='tag'>ink %s defects per 10 tiles · %s views · %s clean</span> <span class='tag'>geometry (4b) %s / 3</span> %s</p>" % (
        okcls(fl.get("verdict") == "PASS"), esc(fl.get("verdict")), (" — below 2: " + esc(", ".join(fl.get("failing", [])))) if fl.get("failing") else "",
        esc(ink["per10"]) if ink else "–", esc(ink["views"]) if ink else "–", esc(ink["clean_views"]) if ink else "–",
        esc(S.get("geometry_score") if S.get("geometry_score") is not None else "not scored"),
        ("<span class='warn'>phases missing: %s</span>" % esc(", ".join(S["missing_phases"]))) if S["missing_phases"] else ""))
    if ink:
        out.append("<h2>Ink — the comparable score, every view</h2><p class='fact'>%s</p><table><tr><th>class</th><th>affected</th><th>per 10 tiles</th><th>instances</th><th>worst</th><th>what counts</th></tr>" % esc(ink["rule"]))
        wl = {"dead": "%spx band · ring covers %s%%" % (ink["worst"]["dead"], ink["worst"]["dead_ring_cover_pct"]), "cut": "%spx cut" % ink["worst"]["cut"],
              "collision": "%spx overlap" % ink["worst"]["collision"], "size": "%s of its own size" % ink["worst"]["size"], "markers": "%s marks on one series" % ink["worst"]["markers"]}
        for k, lab, what in INK_CLASSES:
            out.append("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td class='fact'>%s</td></tr>" % (esc(lab), esc(ink["affected"][k]), esc(ink["per10_by_class"][k]), esc(ink["instances"][k]), esc(wl[k]), esc(what)))
        out.append("</table><table><tr><th>view</th><th>tiles</th><th>dead</th><th>cut</th><th>collisions</th><th>size</th><th>markers</th></tr>")
        for pv in ink["per_view"]:
            a_ = pv["affected"]
            out.append("<tr><td>%s <span class='fact'>%s</span></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                esc(pv["view"]), esc(pv["url"]), esc(pv["tiles"]), esc(a_["dead"]), esc(a_["cut"]), esc(a_["collision"]), esc(a_["size"]), esc(a_["markers"])))
        out.append("</table>")
    out.append("<h2>Two rows for Dave's eye — evidence shown, never answered by the harness</h2><table>")
    for jr in S.get("judgment_rows") or []:
        out.append("<tr><td>%s<div class='fact'>%s: %s</div></td><td style='min-width:120px'>Dave: ______</td></tr>" % (
            esc(jr["row"]), esc(jr["evidence_label"]), esc(json.dumps(jr["evidence"], ensure_ascii=False)[:700])))
    out.append("</table>")
    out.append("<h2>The floor — the four-part rubric, pass at 2 each, never summed (legacy sum %s / 12)</h2><div class='grid4'>" % esc(tot if tot is not None else "incomplete"))''')
rep('''    print("CARD %s  rich=%s full=%s persistent=%s interactive=%s total=%s geo=%s  trace=%s theme=%s clipped=%s" % (
        a.run_id, *(d.get(k, {}).get("score", "-") for k in ("visually_rich", "full", "persistent", "interactive")), S["total"], S["geometry_score"],''',
'''    ink = S.get("ink") or {}
    print("CARD %s  floor=%s ink=%s/10tiles %s views=%s  rich=%s full=%s persistent=%s interactive=%s legacy=%s geo=%s  trace=%s theme=%s clipped=%s" % (
        a.run_id, S["floor"]["verdict"], ink.get("per10"), ink.get("affected"), ink.get("views"),
        *(d.get(k, {}).get("score", "-") for k in ("visually_rich", "full", "persistent", "interactive")), S["total"], S["geometry_score"],''')
# compare
rep('''            ("mechanical total /12", lambda c: c.get("total")),''', '''            ("FLOOR (each part >= 2)", lambda c: (c.get("floor") or {}).get("verdict", "–") + ((" — " + ", ".join(c["floor"]["failing"])) if (c.get("floor") or {}).get("failing") else "")),
            ("INK defects per 10 tiles (lower is better)", lambda c: (c.get("ink") or {}).get("per10", "–")),
            ("views measured / clean", lambda c: "%s / %s" % ((c.get("ink") or {}).get("views", "–"), (c.get("ink") or {}).get("clean_views", "–"))),
            ("tiles measured", lambda c: (c.get("ink") or {}).get("tiles", "–")),
            ("dead ink — tiles (worst band px)", lambda c: "%s (%s)" % (c["ink"]["affected"]["dead"], c["ink"]["worst"]["dead"])),
            ("cut ink — tiles (worst px)", lambda c: "%s (%s)" % (c["ink"]["affected"]["cut"], c["ink"]["worst"]["cut"])),
            ("collisions — tiles (worst overlap px)", lambda c: "%s (%s)" % (c["ink"]["affected"]["collision"], c["ink"]["worst"]["collision"])),
            ("size drift — parts (worst ratio)", lambda c: "%s (%s)" % (c["ink"]["affected"]["size"], c["ink"]["worst"]["size"])),
            ("markers — tiles (most marks on a series)", lambda c: "%s (%s)" % (c["ink"]["affected"]["markers"], c["ink"]["worst"]["markers"])),
            ("legacy sum /12 (not a score)", lambda c: c.get("total")),''')
rep('''    jdump({i: {"total": c.get("total"), "dims": {k: v["score"] for k, v in c["dimensions"].items()}} for i, c in cards}, os.path.splitext(outp)[0] + ".json")''',
    '''    jdump({i: {"total_legacy": c.get("total"), "dims": {k: v["score"] for k, v in c["dimensions"].items()}, "floor": c.get("floor"),
              "ink": {k: (c.get("ink") or {}).get(k) for k in ("views", "tiles", "affected", "instances", "worst", "per10", "per10_by_class", "clean_views")},
              "theme": c["sections"]["theme"]["verdict"]} for i, c in cards}, os.path.splitext(outp)[0] + ".json")''')
# main
rep('''    ap.add_argument("phase", choices=["stage", "static", "gates", "render", "drive", "ext", "card", "all", "compare", "selftest"])''',
    '''    ap.add_argument("phase", choices=["stage", "static", "gates", "render", "drive", "views", "ext", "card", "all", "compare", "selftest", "selftest-views"])''')
rep('''    if a.phase in ("render", "drive"):''', '''    if a.phase == "views":
        sys.path.insert(0, HERE); import views
        return views.run(a.run_id, a.budget)
    if a.phase == "selftest-views":
        sys.path.insert(0, HERE); import views
        return sys.exit(views.selftest())
    if a.phase in ("render", "drive"):''')
rep('''        if os.path.exists(os.path.join(rd, "drive.json")) and not os.path.exists(os.path.join(rd, "ext.json")) and time.time() - t0 < 120:
            cmd_ext(a)''', '''        vj = jload(os.path.join(rd, "views.json"), {}) or {}
        if os.path.exists(os.path.join(rd, "drive.json")) and (a.force or not vj.get("views") or vj.get("truncated")):
            left = 170 - (time.time() - t0)
            if left < 45:
                print("ALL: stopping before views (%.0fs left in this call) — run it in the next call" % left)
            else:
                import views
                views.run(a.run_id, min(a.budget, left - 20))
        if os.path.exists(os.path.join(rd, "drive.json")) and not os.path.exists(os.path.join(rd, "ext.json")) and time.time() - t0 < 120:
            cmd_ext(a)''')
open(P, "w").write(s); print("score patched")
