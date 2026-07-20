#!/usr/bin/env python3
"""Generate the style-consolidation review screens from _style-clusters.json.

Encodes Dave's rulings (2026-07-20) as an explicit, reproducible verdict map rather
than hand-editing HTML. Two rounds of rulings are baked in:
  - ROUND 1 (per-cluster policy): RULINGS below.
  - ROUND 2 (per-item, from the v3 review markup — 27 comments): OVERRIDES below.

Emits:
  - reviews/STYLE-CONSOLIDATION-REVIEW-2026-07-20-v4.html   (round-2 "nearly there" screen)
  - reviews/_style-consolidation-decisions-2026-07-20.json  (cumulative durable record)
Then run _make_review.py on the html for the overlay copy.

VERDICTS
  keep           canon Mono-clean, keep as-is                       (green)
  align          keep but re-home drift onto Apollo Mono values     (amber)
  archive        superseded — kept not deleted; collapsed tray      (grey)
  experiment     valuable experiment — keep, NOT canon              (violet)
  keep-legacy    keep for legacy reference only                     (slate)
  hidden         review DUPLICATE (-REVIEW/.REVIEW) — not displayed
  undecided      no ruling yet — replayed into the next review

RECATEGORISATION (Dave: "look at the title of the files to categorise")
  cards-selectable.html -> Cards ; table-responsive.html + Table.reference.html -> Table
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC  = os.path.join(HERE, "_style-clusters.json")
OUT_HTML = os.path.join(HERE, "STYLE-CONSOLIDATION-REVIEW-2026-07-20-v5.html")
OUT_DEC  = os.path.join(HERE, "_style-consolidation-decisions-2026-07-20.json")

# ---- ROUND 1 — per-cluster policy -------------------------------------------
RULINGS = {
    "Button":             "keep mono-clean; archive everything else",
    "Tags":               "keep mono-clean; archive everything else",
    "Cards":              "keep mono-clean; align MONO+drift; archive LEGACY/old",
    "Dropdown":           "align MONO+drift; archive both LEGACY/old",
    "Links":              "align MONO+drift; archive everything else",
    "Pro-forma tranches": "keep all; align to Mono",
}
DECIDED_ORDER = ["Button", "Tags", "Cards", "Dropdown", "Links", "Pro-forma tranches"]

# ---- ROUND 2 — per-item rulings from the v3 review markup (27 comments) ------
# key = (cluster_after_recat, base) -> (verdict, note)
OVERRIDES = {
    ("Amount display", "Amount-display.reference.html"):        ("keep",        "check it's correctly tokenised"),
    ("Badge", "badge-AB-showcase.html"):                        ("archive",     ""),
    ("Badge", "Badge.reference.html"):                          ("align",       ""),
    ("DataViz", "DataViz-interactive.html"):                    ("align",       "awesome — may need some alignment"),
    ("Icon / weight", "icon-fake-weight.html"):                 ("experiment",  "valuable experiment — keep, not canon"),
    ("Icon / weight", "icon-weight-system.html"):               ("experiment",  "valuable experiment — keep, not canon"),
    ("Tooltip", "tooltip-AB-showcase.html"):                    ("archive",     ""),
    ("Tooltip", "Tooltip.reference.html"):                      ("keep",        "align if needed"),
    ("Tabs", "Reconciled-tab-and-stepper-2026-07-17.html"):     ("align",       "keep + align — this is the tab (+stepper) canon"),
    ("Tabs", "tabs-responsive.html"):                           ("archive",     ""),
    ("Tabs", "Tab-bar.reference.html"):                         ("archive",     "retired in favour of the reconciled model"),
    ("Tabs", "Tabs.reference.html"):                            ("archive",     "retired in favour of the reconciled model"),
    ("Table", "table-responsive.html"):                         ("archive",     ""),
    ("Table", "Table.reference.html"):                          ("keep",        "align if needed"),
    ("Status indicator", "status-indicator.html"):             ("archive",     ""),
    ("Status indicator", "Status-indicator.reference.html"):    ("align",       ""),
    ("Selection controls", "selection-controls-AB-showcase.html"): ("archive",  ""),
    ("Selection controls", "selection-controls-family.html"):   ("archive",     ""),
    ("Selection controls", "Selection-controls.reference.html"):("align",       ""),
    ("Progress / stepper", "Progress-tracker.reference.html"):  ("archive",     "stepper now lives in the reconciled tab+stepper model"),
    ("Progress / stepper", "progress-tracker-segmented.html"):  ("archive",     ""),
    ("Notifications", "notifications-responsive.html"):         ("archive",     ""),
    ("Notifications", "Notifications.reference.html"):          ("keep-legacy", "keep for legacy reference only"),
    ("Modals", "modal-motion-3up.html"):                        ("archive",     ""),
    ("Modals", "modals-dialog.html"):                           ("archive",     ""),
    ("Modals", "Modals.reference.html"):                        ("align",       ""),
    ("Masthead", "Masthead-interactive.html"):                  ("align",       "beautiful — keep + align"),
    # ROUND 3 — Input fields + List items (from the v4 replay markup)
    ("List items", "List-items.reference.html"):                ("align",       ""),
    ("List items", "list-items-transaction.html"):              ("archive",     ""),
    ("Input fields", "Input-fields.reference.html"):            ("align",       ""),
    ("Input fields", "input-fields.html"):                      ("archive",     ""),
    ("Input fields", "input-fields-AB-showcase.html"):          ("archive",     ""),
}

# ROUND 3 — singletons (keyed by base; cluster is null). "keep align" -> align.
SINGLETON_RULINGS = {
    "Video-player.reference.html":      "align",
    "View-options.reference.html":      "align",
    "Summary.reference.html":           "align",
    "Slider.reference.html":            "align",
    "Search-field.reference.html":      "align",
    "Reorder.reference.html":           "align",
    "Quick-actions.reference.html":     "align",
    "Pagination.reference.html":        "align",
    "Navigations.reference.html":       "archive",
    "Loading-indicator.reference.html": "align",
    "Hero.reference.html":              "archive",
    "Headers.reference.html":           "align",
    "Eyebrow.reference.html":           "align",
    "Divider.reference.html":           "align",
    "Countdown-timer.reference.html":   "align",
    "Confirmation.reference.html":      "align",
    "Breadcrumbs.reference.html":       "align",
    "Avatar.reference.html":            "align",
    "Action-bar.reference.html":        "align",
    "Accordion.reference.html":         "align",
}

# clusters whose ruling retires canon / needs a caught-eye flag
FLAGS = {
    "Tabs": "Tab-bar + Tabs snippets retired; the reconciled tab+stepper is the tab canon.",
    "Progress / stepper": "Whole cluster archived — stepper now lives in the reconciled tab+stepper model.",
    "Notifications": "Kept only as legacy reference — no active Mono notification canon remains.",
}

VERDICT_ORDER = ["keep", "align", "experiment", "keep-legacy", "archive", "undecided", "hidden"]
VLAB = {"keep":"keep","align":"align → Mono","archive":"archive","experiment":"keep · not canon",
        "keep-legacy":"keep · legacy ref","undecided":"to rule","hidden":"hidden",
        "preserve":"preserve","ignore":"ignore"}

def is_review_dupe(base):
    b = base.lower()
    return b.endswith("-review.html") or b.endswith(".review.html")

def verdict_for(item, cluster):
    base, era = item["base"], item["era"]
    if is_review_dupe(base):
        return "hidden", ""
    if (cluster, base) in OVERRIDES:
        return OVERRIDES[(cluster, base)]
    if cluster in ("Button", "Tags"):
        return ("keep", "") if era == "MONO-clean" else ("archive", "")
    if cluster == "Cards":
        if era == "MONO-clean": return "keep", ""
        if era == "MONO+drift": return "align", ""
        return "archive", ""
    if cluster in ("Dropdown", "Links"):
        return ("align", "") if era == "MONO+drift" else ("archive", "")
    if cluster == "Pro-forma tranches":
        return "align", ""
    return "undecided", ""

def propose(item):
    """A suggested verdict for still-undecided items so Dave can just confirm."""
    era = item["era"]
    if era == "MONO-clean": return "keep"
    if era == "MONO+drift": return "align"
    if era == "LEGACY/old": return "archive"
    return "keep"

def recategorise(clusters):
    moves = []
    tabs = clusters.get("Tabs", [])
    keep_tabs, table = [], []
    for it in tabs:
        b = it["base"].lower()
        if b.startswith("cards-"):
            it = dict(it, cluster="Cards"); clusters.setdefault("Cards", []).append(it)
            moves.append((it["base"], "Tabs", "Cards"))
        elif b.startswith("table"):
            it = dict(it, cluster="Table"); table.append(it)
            moves.append((it["base"], "Tabs", "Table"))
        else:
            keep_tabs.append(it)
    clusters["Tabs"] = keep_tabs
    if table:
        clusters["Table"] = table
    return clusters, moves

def annotate(clusters):
    out = {}
    for name, items in clusters.items():
        rows = []
        for it in items:
            v, note = verdict_for(it, name)
            row = dict(it, verdict=v)
            if note: row["note"] = note
            if v == "undecided": row["proposed"] = propose(it)
            rows.append(row)
        out[name] = rows
    return out

def cluster_summary(items):
    """e.g. 'keep 1 · align 1 · archive 2'  (excludes hidden)."""
    from collections import Counter
    c = Counter(it["verdict"] for it in items if it["verdict"] != "hidden")
    parts = []
    for v in VERDICT_ORDER:
        if c.get(v): parts.append(f"{VLAB[v]} {c[v]}")
    hid = sum(1 for it in items if it["verdict"] == "hidden")
    s = " · ".join(parts)
    if hid: s += f"  ({hid} dupe{'s' if hid>1 else ''} hidden)"
    return s

def main():
    data = load()
    clusters = {k: list(v) for k, v in data["clusters"].items()}
    clusters, moves = recategorise(clusters)
    annotated = annotate(clusters)

    # decided = has a policy or every non-hidden item carries a verdict != undecided
    decided_names, torule_names = [], []
    for name, items in annotated.items():
        live = [it for it in items if it["verdict"] != "hidden"]
        undecided = [it for it in live if it["verdict"] == "undecided"]
        (torule_names if undecided else decided_names).append(name)
    # stable order: round-1 first, then the rest alpha
    decided_names.sort(key=lambda n: (DECIDED_ORDER.index(n) if n in DECIDED_ORDER else 99, n))
    torule_names.sort()

    research   = data.get("research", [])
    journeys   = data.get("journeys", [])
    singletons = [s for s in data.get("singletons", []) if s["base"] != "_review-overlay.html"]
    for s in singletons:
        v = SINGLETON_RULINGS.get(s["base"])
        if v:
            s["verdict"] = v
        else:
            s["verdict"] = "undecided"; s["proposed"] = propose(s)
    singletons_ruled = all(s["verdict"] != "undecided" for s in singletons)

    # ---- cumulative decision record -----------------------------------------
    from collections import Counter
    counts = Counter()
    for items in annotated.values():
        for it in items: counts[it["verdict"]] += 1
    for s in singletons: counts[s["verdict"]] += 1  # fold singleton verdicts into the tally
    decisions = {
        "date": "2026-07-20", "session": "Style consolidation — rounds 1 & 2",
        "rulings_round1": RULINGS,
        "rulings_round2_count": len(OVERRIDES),
        "recategorised": [{"file": m[0], "from": m[1], "to": m[2]} for m in moves],
        "flags": FLAGS,
        "counts": dict(counts),
        "decided_clusters": decided_names,
        "still_to_rule": torule_names + ([] if singletons_ruled else ["Singletons"]),
        "clusters": {name: [{"base": it["base"], "dir": it["dir"], "era": it["era"],
                             "verdict": it["verdict"], **({"note": it["note"]} if it.get("note") else {})}
                            for it in items] for name, items in annotated.items()},
    }
    with open(OUT_DEC, "w") as f:
        json.dump(decisions, f, indent=1)

    # ---- payload for the v4 screen ------------------------------------------
    decided_blocks = [{
        "name": name, "summary": cluster_summary(annotated[name]),
        "flag": FLAGS.get(name, ""), "items": annotated[name],
    } for name in decided_names]
    if singletons_ruled:
        decided_blocks.append({"name": "Singletons (one variant each)",
                               "summary": cluster_summary(singletons), "flag": "",
                               "items": singletons})

    torule_blocks = [{"name": name, "items": annotated[name]} for name in torule_names]
    if not singletons_ruled:
        torule_blocks.append({"name": "Singletons (one variant each)", "items": singletons})

    settled = [
        {"name": "Research / inference", "verb": "preserved", "n": len(research)},
        {"name": "SME journeys", "verb": "ignored (test pages)", "n": len(journeys)},
    ]

    n_tot = len(decided_names) + len(torule_names) + 1  # +1 singletons group
    n_dec = len(decided_names) + (1 if singletons_ruled else 0)
    html = render_v4(decided_blocks, torule_blocks, settled, dict(counts), moves, n_dec, n_tot)
    with open(OUT_HTML, "w") as f:
        f.write(html)

    print("counts:", dict(counts))
    print(f"decided clusters: {n_dec}/{n_tot}")
    print("still to rule:", decisions["still_to_rule"] or "none")
    print("wrote:", os.path.relpath(OUT_HTML, ROOT))
    print("wrote:", os.path.relpath(OUT_DEC, ROOT))

def load():
    with open(SRC) as f:
        return json.load(f)

def render_v4(decided, torule, settled, counts, moves, n_dec, n_tot):
    P = {"decided": decided, "torule": torule, "settled": settled,
         "counts": counts, "moves": [{"file":m[0],"from":m[1],"to":m[2]} for m in moves],
         "nDec": n_dec, "nTot": n_tot,
         "vlab": VLAB}
    return TEMPLATE.replace("/*__P__*/", json.dumps(P))

TEMPLATE = r"""<!doctype html><html><head><meta charset=utf8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Apollo · style consolidation — round 2 · nearly there</title><style>
:root{--bg:#f4f4f2;--ink:#1a1a1a;--card:#fff;--line:#ddd;--frameH:52vh;--cols:3}
*{box-sizing:border-box}
body{margin:0;font:14px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--ink)}
header{background:#1a1a1a;color:#fff;padding:16px 22px 14px;position:sticky;top:0;z-index:20}
.h1{font-size:16px;font-weight:600;margin:0 0 10px}.h1 small{color:#aaa;font-weight:400;margin-left:8px}
.prog{display:flex;align-items:center;gap:12px;margin:0 0 10px}
.bar{flex:1;height:10px;background:#333;border-radius:6px;overflow:hidden;max-width:420px}
.bar i{display:block;height:100%;background:#2FA35B}
.prog b{font-size:15px}.prog span{color:#bbb;font-size:12px}
.tally{display:flex;gap:14px;flex-wrap:wrap;font-size:12px;color:#ddd}
.tally .dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px;vertical-align:middle}
main{padding:18px 22px 80px;max-width:1500px}
.sec{font-size:13px;text-transform:uppercase;letter-spacing:.08em;color:#666;margin:22px 0 10px;border-bottom:1px solid #ddd;padding-bottom:5px}
/* decided checklist */
.check{list-style:none;margin:0;padding:0}
.row{background:#fff;border:1px solid #e6e6e3;border-radius:7px;margin-bottom:7px;overflow:hidden}
.rowhd{display:flex;align-items:center;gap:10px;padding:9px 12px;cursor:pointer}
.rowhd .tk{color:#2FA35B;font-weight:700;font-size:15px}
.rowhd .nm{font-weight:600;min-width:150px}
.rowhd .sm{color:#666;font-size:12px;flex:1}
.rowhd .fl{color:#B45309;font-size:11px}
.rowhd .cv{color:#aaa;font-size:11px}
.row .body{display:none;padding:0 12px 12px;border-top:1px dashed #eee}
.row.open .body{display:block}
.row.open .rowhd .cv::after{content:" ▾"}
.rowhd .cv::after{content:" ▸"}
.mini{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.chip{font-size:11px;padding:3px 8px;border-radius:4px;border:1px solid #e0e0dd;display:flex;gap:6px;align-items:center;background:#fafafa}
.chip a{color:#1a1a1a;text-decoration:none;border-bottom:1px dotted #bbb}
.vb{color:#fff;padding:1px 6px;border-radius:3px;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.03em;white-space:nowrap}
.vb.keep{background:#2FA35B}.vb.align{background:#E0912F}.vb.archive{background:#8a8a8a}
.vb.experiment{background:#7A5CC0}.vb.keep-legacy{background:#4a7a8c}.vb.undecided{background:#5b6b8c}
.note{color:#8a6d3b;font-size:11px;font-style:italic;margin-left:4px}
/* to-rule live cards */
.torulehd{font-weight:600;font-size:14px;margin:16px 0 4px}
.torulehd .pn{color:#888;font-weight:400;font-size:12px;margin-left:6px}
.hint{font-size:12px;color:#666;margin:0 0 10px}
.grid{display:grid;grid-template-columns:repeat(var(--cols),minmax(0,1fr));gap:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;overflow:hidden;display:flex;flex-direction:column}
.card:fullscreen{width:100vw;height:100vh}.card:fullscreen iframe{height:calc(100vh - 46px)}
.cap{display:flex;align-items:center;gap:7px;padding:7px 9px;border-bottom:1px solid #eee;background:#fafafa;font-size:11px}
.cap .path{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.pvb{border:1.5px dashed;background:#fff;padding:1px 6px;border-radius:3px;font-size:10px;font-weight:700;text-transform:uppercase;white-space:nowrap}
.pvb.keep{color:#2FA35B;border-color:#2FA35B}.pvb.align{color:#C57A1E;border-color:#E0912F}.pvb.archive{color:#777;border-color:#8a8a8a}
.era{color:#fff;padding:1px 6px;border-radius:3px;font-size:10px;font-weight:600}
.btn{border:1px solid #ccc;background:#fff;border-radius:5px;padding:2px 7px;cursor:pointer;font-size:11px;text-decoration:none;color:#1a1a1a;white-space:nowrap}
.btn:hover{background:#f0f0f0}
iframe{width:100%;height:var(--frameH);border:0;display:block;background:var(--fbg,#fff)}
.toolbar{display:flex;gap:16px;align-items:center;padding:8px 22px;background:#efefec;border-bottom:1px solid #e2e2df;position:sticky;top:120px;z-index:19;font-size:12px;flex-wrap:wrap}
.toolbar label{display:flex;gap:6px;align-items:center}.toolbar input[type=range]{width:100px}
.legend{color:#888;font-size:11px}
.movenote{font-size:11px;color:#888;margin:8px 0 0}
</style></head><body>
<header>
  <div class="h1">Apollo · style consolidation <small id=subtitle>2026-07-20</small></div>
  <div class="prog"><b id=pct></b><div class="bar"><i id=barfill></i></div><span id=progtxt></span></div>
  <div class="tally" id=tally></div>
</header>
<div class="toolbar">
  <label>Columns <input type=range id=cols min=1 max=4 value=3></label>
  <label>Height <input type=range id=hgt min=30 max=90 value=52> <span id=hv>52</span>vh</label>
  <label>Frame bg <select id=fbg><option value=#fff>white</option><option value=#1a1a1a>dark</option><option value=#f4f4f2>grey</option></select></label>
  <span class="legend">To-rule cards show a <b>dashed proposed verdict</b> — confirm or override in the overlay.</span>
</div>
<main>
  <div class="sec">✓ Ruled — <span id=decn></span> clusters</div>
  <ul class="check" id=check></ul>
  <div class="sec" id=torulesec>○ Still to rule</div>
  <p class="hint" id=torulehint></p>
  <div id=torule></div>
  <div class="sec">Settled</div>
  <ul class="check" id=settled></ul>
  <div class="movenote" id=movenote></div>
</main>
<script>
const P=/*__P__*/;
const ERAC={"MONO-clean":"#1a1a1a","MONO+drift":"#B45309","LEGACY/old":"#B92F1E","neutral":"#666"};
const VLAB=P.vlab;
function esc(s){return (s||'').replace(/[&<>"]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m]));}
// progress
const pct=Math.round(P.nDec/P.nTot*100);
document.getElementById('pct').textContent=pct+'%';
document.getElementById('barfill').style.width=pct+'%';
document.getElementById('progtxt').textContent=P.nDec+' of '+P.nTot+' clusters ruled';
document.getElementById('decn').textContent=P.nDec;
const c=P.counts;
document.getElementById('tally').innerHTML=
 `<span><span class=dot style="background:#2FA35B"></span>keep <b>${c.keep||0}</b></span>`+
 `<span><span class=dot style="background:#E0912F"></span>align <b>${c.align||0}</b></span>`+
 `<span><span class=dot style="background:#7A5CC0"></span>experiment <b>${c.experiment||0}</b></span>`+
 `<span><span class=dot style="background:#4a7a8c"></span>legacy-ref <b>${c['keep-legacy']||0}</b></span>`+
 `<span><span class=dot style="background:#8a8a8a"></span>archive <b>${c.archive||0}</b></span>`+
 `<span><span class=dot style="background:#5b6b8c"></span>to rule <b>${c.undecided||0}</b></span>`+
 `<span style="color:#888">${c.hidden||0} dupes hidden</span>`;
// decided checklist
const check=document.getElementById('check');
P.decided.forEach(cl=>{
  const li=document.createElement('li');li.className='row';
  const mini=cl.items.filter(x=>x.verdict!=='hidden').map(x=>
    `<span class=chip><span class="vb ${x.verdict}">${VLAB[x.verdict]||x.verdict}</span>`+
    `<a href="${x.rel}" target=_blank rel=noopener>${esc(x.base)}</a>`+
    (x.note?`<span class=note>${esc(x.note)}</span>`:'')+`</span>`).join('');
  li.innerHTML=`<div class=rowhd><span class=tk>✓</span><span class=nm>${esc(cl.name)}</span>`+
    `<span class=sm>${esc(cl.summary)}</span>`+
    (cl.flag?`<span class=fl>⚑ ${esc(cl.flag)}</span>`:'')+`<span class=cv></span></div>`+
    `<div class=body><div class=mini>${mini}</div></div>`;
  li.querySelector('.rowhd').onclick=()=>li.classList.toggle('open');
  check.appendChild(li);
});
// to-rule live
const torule=document.getElementById('torule');
let torn=0;P.torule.forEach(b=>torn+=b.items.filter(x=>x.verdict!=='hidden').length);
document.getElementById('subtitle').textContent='2026-07-20 · '+(pct>=100?'every cluster ruled ✓':'nearly there');
if(torn===0){
  document.getElementById('torulesec').innerHTML='✓ Nothing left to rule';
  document.getElementById('torulehint').innerHTML='<b>Consolidation ruled — every cluster and singleton has a verdict.</b> Next: run the Mono alignment sweep on the <b>'+(c.align||0)+' align</b> items, then flip the theme-provenance gate to blocking. (Some kept components may still be duplicates — flagged for a later pass.)';
} else {
  document.getElementById('torulehint').innerHTML=
    `<b>${torn} items</b> across ${P.torule.length} groups — each shows a dashed <b>proposed</b> verdict (Mono-clean → keep, drift → align, legacy → archive). Rule or override, and I'll bank them.`;
}
function fscard(b){b.querySelectorAll('[data-fs]').forEach(x=>x.onclick=()=>{const cd=x.closest('.card');cd.requestFullscreen&&cd.requestFullscreen();});}
P.torule.forEach(bl=>{
  const shown=bl.items.filter(x=>x.verdict!=='hidden');
  const hd=document.createElement('div');hd.className='torulehd';
  hd.innerHTML=esc(bl.name)+' <span class=pn>'+shown.length+' to rule</span>';torule.appendChild(hd);
  const g=document.createElement('div');g.className='grid';
  g.innerHTML=shown.map(x=>{
    const col=ERAC[x.era]||'#666';const pv=x.proposed||'keep';
    return `<div class=card><div class=cap>
      <span class="pvb ${pv}">proposed: ${pv}</span>
      <span class=era style="background:${col}">${x.era}</span>
      <span class=path>${esc(x.base)}</span>
      <a class=btn href="${x.rel}" target=_blank rel=noopener>↗</a>
      <button class=btn data-fs>⤢</button></div>
      <div class=frameWrap><iframe loading=lazy src="${x.rel}"></iframe></div></div>`;
  }).join('');
  torule.appendChild(g);fscard(g);
});
// settled
const settled=document.getElementById('settled');
P.settled.forEach(s=>{const li=document.createElement('li');li.className='row';
  li.innerHTML=`<div class=rowhd style="cursor:default"><span class=tk>✓</span><span class=nm>${esc(s.name)}</span><span class=sm>${esc(s.verb)} — ${s.n} files</span></div>`;
  settled.appendChild(li);});
// moves
if(P.moves.length)document.getElementById('movenote').innerHTML=
  '↳ recategorised by filename: '+P.moves.map(m=>esc(m.file)+' ('+m.from+'→'+m.to+')').join(' · ');
// controls
document.getElementById('cols').oninput=e=>document.documentElement.style.setProperty('--cols',e.target.value);
const hv=document.getElementById('hv');
document.getElementById('hgt').oninput=e=>{hv.textContent=e.target.value;document.documentElement.style.setProperty('--frameH',e.target.value+'vh');};
document.getElementById('fbg').onchange=e=>document.documentElement.style.setProperty('--fbg',e.target.value);
</script></body></html>
"""

if __name__ == "__main__":
    sys.exit(main())
