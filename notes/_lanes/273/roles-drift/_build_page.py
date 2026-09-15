#!/usr/bin/env python3
"""#273 lane RD — build the ROLES DRIFT decision page from DRIFT.json.

EVERY figure on the page is READ from DRIFT.json (or DERIVED from it by a
formula recorded in DERIVED.json). No number is typed by hand.

  python3 notes/_lanes/273/roles-drift/_build_page.py
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
SRC = os.path.join(HERE, "DRIFT.json")
DERIVED_OUT = os.path.join(HERE, "DERIVED.json")
OUT = os.path.join(REPO, "notes", "_REVIEW-roles-drift-2026-09-15-v1.html")

D = json.load(open(SRC))
E = html.escape

# ---------------------------------------------------------------- derivation
# Every number on the page that is not a literal value in DRIFT.json is
# computed HERE and registered with its formula, so _numbers_check.py can
# prove it and a reader can audit it.
DERIVED = {}


def derive(name, value, formula):
    DERIVED[name] = {"value": value, "formula": formula}
    return value


PER = {r["role"]: r for r in D["per_role"]}
ZERO = list(D["roles_zero_in_metas"])
HELD = ["record-list", "input"]
PASS2 = [r for r in D["per_role"] if r["role"] not in HELD and r["meta_silent"] > 0]

n_zero = derive("zero_roles", len(ZERO), "len(roles_zero_in_metas)")
n_legal = derive("legal_field_count", len(D["legal_when_fields"]),
                 "len(legal_when_fields)")
illegal = D["metas_with_illegal_when_fields"]
n_illegal_entries = derive(
    "illegal_field_entries", sum(len(v) for v in illegal.values()),
    "sum(len(v) for v in metas_with_illegal_when_fields.values())")
n_illegal_names = derive(
    "illegal_field_names_distinct",
    len({f for v in illegal.values() for f in v}),
    "len(set of distinct field names across metas_with_illegal_when_fields)")
n_illegal_metas = derive("illegal_field_metas", len(illegal),
                         "len(metas_with_illegal_when_fields)")
n_pass2 = derive(
    "pass2_silent", sum(r["meta_silent"] for r in PASS2),
    "sum(per_role[r].meta_silent) for roles not in {record-list, input}")
n_pass2_roles = derive("pass2_roles", len(PASS2),
                       "count of roles not in {record-list, input} with meta_silent > 0")
n_rl_silent = derive("record_list_silent", PER["record-list"]["meta_silent"],
                     "per_role[record-list].meta_silent")
n_in_silent = derive("input_silent", PER["input"]["meta_silent"],
                     "per_role[input].meta_silent")
n_fb_silent = derive("feedback_silent", PER["feedback"]["meta_silent"],
                     "per_role[feedback].meta_silent")
n_ov_silent = derive("overlay_silent", PER["overlay"]["meta_silent"],
                     "per_role[overlay].meta_silent")
n_fb_ov = derive("feedback_plus_overlay", n_fb_silent + n_ov_silent,
                 "per_role[feedback].meta_silent + per_role[overlay].meta_silent")
pct_silent = derive(
    "pct_silent", round(D["memberships_meta_silent"] * 100
                        / D["memberships_json"]),
    "round(memberships_meta_silent * 100 / memberships_json)")
n_contra = derive("contradictions", len(D["contradictions"]), "len(contradictions)")
n_dangling = derive("dangling", len(D["dangling_slugs"]), "len(dangling_slugs)")
n_invent = derive("invented_roles",
                  len(D["meta_provides_not_in_json"]) + len(D["meta_provides_unknown_role"]),
                  "len(meta_provides_not_in_json) + len(meta_provides_unknown_role)")
n_nap = derive("not_a_provider_with_provides", len(D["not_a_provider_with_provides"]),
               "len(not_a_provider_with_provides)")

SILENT_ROWS = []
for r in D["per_role"]:
    for p in r["providers"]:
        if p["state"] != "agrees":
            SILENT_ROWS.append((r["role"], p))
n_silent_rows = derive("silent_rows", len(SILENT_ROWS),
                       "count of per_role[*].providers[*] with state != 'agrees'")

open(DERIVED_OUT, "w").write(json.dumps(DERIVED, indent=1, sort_keys=True) + "\n")


# ------------------------------------------------------------------ helpers
def n(value):
    """A figure that came from the data. Wrapped so it is auditable."""
    return '<span class="n">%s</span>' % E(str(value))


DECISIONS = [
    {
        "id": "RD-1",
        "title": "THE ADDRESS",
        "lead": (
            "Write <code>provides: &lt;role&gt;</code> onto the " + n(D["memberships_meta_silent"])
            + " silent metas, copied from <code>roles.json</code>, by TEXTUAL SPAN "
            "(never <code>json.dump</code> a meta — the #179 reformat class). The graph "
            "goes " + n(D["memberships_meta_agree"]) + " &rarr; " + n(D["memberships_json"])
            + " <code>providesRole</code> edges."),
        "options": [
            ("a", True, "All " + n(D["memberships_meta_silent"]) + " now, <code>input</code>'s "
             + n(n_in_silent) + " included. An address is legal without a gate: "
             "<code>_validate_roles_resolve.py</code> check six forbids priority-without-provides, "
             "not the reverse."),
            ("b", False, "Only the " + n(D["silent_with_json_when"]) + " that carry a "
             "<code>roles.json</code> <code>when</code>; <code>input</code> waits."),
            ("c", False, "Leave it at " + n(D["memberships_meta_agree"])
             + " — <code>roles.json</code> stays a roadmap."),
        ],
        "why": (
            "Why (a): the membership is already ruled (s252-D1, &ldquo;with the membership&rdquo;), "
            "so this ENACTS, it does not rule. A resolver that can name substitutes without "
            "ordering them beats one that cannot see " + n(pct_silent) + "% of them."),
    },
    {
        "id": "RD-2",
        "title": "THE GATES",
        "lead": (
            "<code>when</code> + <code>priority</code> + <code>shape</code> + <code>answers</code> "
            "— the DESK address, AUTHORED not copied: <code>roles.json</code>'s <code>when</code> "
            "strings are prose like &ldquo;default, read-mostly&rdquo; and do not parse under the "
            "closed field grammar. This decision sets the SCOPE of authoring pass two."),
        "options": [
            ("a", True, "The " + n(n_pass2) + " silent providers of the " + n(n_pass2_roles)
             + " roles that are neither <code>record-list</code> nor <code>input</code>. One lane "
             "per role, verifier in the same wave, <code>when</code> in the closed grammar, "
             "<code>priority</code> unique per role."),
            ("b", False, "The two zero roles not held elsewhere — <code>feedback</code> "
             + n(n_fb_silent) + " + <code>overlay</code> " + n(n_ov_silent) + " = "
             + n(n_fb_ov) + " metas. The rest later."),
            ("c", False, "Wait."),
        ],
        "why": (
            "<code>record-list</code> (" + n(n_rl_silent) + ") is HELD behind P-272-1: "
            "list-vs-card — <code>list-items</code> and its neighbours cannot be gated until the "
            "definition exists (see RD-4). <code>input</code> (" + n(n_in_silent) + ", every "
            "<code>roles.json</code> <code>when</code> null) is HELD behind the input sub-roles "
            "that <code>roles.json</code>'s <code>$extension</code> expects (s251-D7, "
            "&ldquo;not now&rdquo;)."),
    },
    {
        "id": "RD-3",
        "title": "THE ILLEGAL FIELD NAMES",
        "lead": (
            "<code>_validate_roles_resolve.py</code> gained reds at <code>b46ea90</code> "
            "(#272's inscribed <code>when</code>s): " + n(n_illegal_metas) + " metas use "
            + n(n_illegal_entries) + " left-hand field-name entries (" + n(n_illegal_names)
            + " distinct) that are not in <code>when-fields.json</code>, whose legal set is "
            + n(n_legal) + " names. The older reds are <code>data-grid</code> <code>with</code> "
            "entries without a <code>slug</code> (#261, unrelated). This was NOT declared at the "
            "#272 seam."),
        "options": [
            ("a", True, "Extend <code>when-fields.json</code> with the names by ruling. s254-D2 "
             "closed the list so that a LANE cannot add a name; Dave adding one is exactly what "
             "the <code>$extension</code> clause anticipates, and the gates came from thirteen "
             "systems' unanimous vocabulary."),
            ("b", False, "Rewrite the " + n(n_illegal_metas) + " gates in the existing "
             + n(n_legal) + " names."),
            ("c", False, "Mixed — mark per name in the table below, then one note here."),
        ],
        "why": ("The table in section five shows every name with its meta and its clause, so (c) "
                "is a click, not a re-read."),
    },
    {
        "id": "RD-4",
        "title": "LIST-vs-CARD NOW?",
        "lead": (
            "P-272-1 blocks the <code>record-list</code> gates in RD-2 and nothing else on this "
            "page."),
        "options": [
            ("a", True, "Spin the P-272-1 research lane today, in parallel with RD-1. Definitions "
             "from the harvested systems: simple-list &middot; column-list &middot; list-card "
             "(rows B-09, B-10, B-20, N-account-card)."),
            ("b", False, "Wait for the tripwire to fire."),
        ],
        "why": "",
    },
]

# ------------------------------------------------------------------- markup
CSS = """
:root{
 --accent:#DA1A00; --ink:#000; --paper:#fff;
 --g1:#F3F3F3; --g2:#EDEDED; --g3:#D7D8D6; --g6:#767676; --g7:#545454; --g8:#333;
 --rule:#EDEDED; --soft:#F3F3F3; --muted:#545454;
 --max:1200px;
 --s1:.5rem; --s2:1rem; --s3:1.5rem; --s4:2rem; --s5:3rem; --s6:4rem; --s7:6rem;
 --font:"Univers Next for HSBC","Univers Next","Helvetica Neue",Helvetica,Arial,sans-serif;
 color-scheme:light;
}
@media (prefers-color-scheme:dark){
 :root:not([data-theme="light"]){
  --accent:#F6604C; --ink:#F2F2F2; --paper:#111;
  --g1:#1A1A1A; --g2:#2A2A2A; --g3:#3A3A3A; --g6:#9B9B9B; --g7:#B7B7B7; --g8:#D7D8D6;
  --rule:#2A2A2A; --soft:#1A1A1A; --muted:#B7B7B7; color-scheme:dark;
 }
}
:root[data-theme="dark"]{
 --accent:#F6604C; --ink:#F2F2F2; --paper:#111;
 --g1:#1A1A1A; --g2:#2A2A2A; --g3:#3A3A3A; --g6:#9B9B9B; --g7:#B7B7B7; --g8:#D7D8D6;
 --rule:#2A2A2A; --soft:#1A1A1A; --muted:#B7B7B7; color-scheme:dark;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--font);
 font-size:1rem;line-height:1.7;-webkit-font-smoothing:antialiased}
.wrap{max-width:var(--max);margin:0 auto;padding-left:var(--s4);padding-right:var(--s4)}
@media (max-width:520px){.wrap{padding-left:var(--s2);padding-right:var(--s2)}}
section{padding-block:var(--s6);border-top:1px solid var(--rule)}
section:first-of-type{border-top:0}
.label{font-size:.75rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;
 color:var(--accent);display:flex;align-items:center;gap:var(--s1);margin:0 0 var(--s3)}
.label::before{content:"";display:inline-block;width:20px;height:1px;background:var(--accent);flex:0 0 20px}
h1{font-size:3.5625rem;line-height:1.04;font-weight:400;letter-spacing:0;margin:0 0 var(--s4);max-width:22ch}
h2{font-size:2.125rem;line-height:1.15;font-weight:400;margin:0 0 var(--s3)}
h3{font-size:1.1875rem;line-height:1.2;font-weight:500;margin:0 0 var(--s2)}
p{margin:0 0 var(--s2);max-width:78ch}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.86em;
 background:var(--soft);padding:.08em .3em;border-radius:2px}
a{color:var(--accent)}
.n{font-variant-numeric:tabular-nums;font-weight:500}
@media (max-width:760px){h1{font-size:2.125rem}h2{font-size:1.6rem}}

.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--g2);
 border:1px solid var(--g2);margin:var(--s5) 0 var(--s4)}
.stat{background:var(--paper);padding:var(--s3)}
.stat b{display:block;font-size:2.6875rem;font-weight:200;line-height:1;
 font-variant-numeric:tabular-nums;margin-bottom:var(--s1)}
.stat span{display:block;font-size:.75rem;letter-spacing:.1em;text-transform:uppercase;color:var(--g6)}
@media (max-width:760px){.stats{grid-template-columns:repeat(2,1fr)}}

.zeros{display:grid;grid-template-columns:repeat(4,1fr);gap:var(--s3);margin-top:var(--s4)}
.zeros div{border-top:1px solid var(--g3);padding-top:var(--s1);font-size:.875rem;color:var(--muted)}
.zeros b{color:var(--ink);font-weight:500}
@media (max-width:900px){.zeros{grid-template-columns:repeat(2,1fr)}}
@media (max-width:480px){.zeros{grid-template-columns:1fr}}

.split{display:grid;grid-template-columns:1fr 2fr;gap:var(--s6);align-items:start}
@media (max-width:900px){.split{grid-template-columns:1fr;gap:var(--s3)}}

.dec{border-top:1px solid var(--g3);padding-top:var(--s3);margin-top:var(--s5)}
.dec:first-of-type{margin-top:var(--s3)}
.dechead{display:flex;flex-wrap:wrap;align-items:baseline;gap:var(--s2);margin-bottom:var(--s2)}
.decid{font-size:.75rem;letter-spacing:.14em;font-weight:500;color:var(--accent)}
.opts{list-style:none;margin:var(--s3) 0 0;padding:0}
.opts li{border-top:1px solid var(--rule);padding:var(--s2) 0}
.opt{display:grid;grid-template-columns:auto 1fr;gap:var(--s2);align-items:start}
.opt input{margin-top:.45rem;accent-color:var(--accent);width:16px;height:16px;flex:0 0 16px}
.opt label{cursor:pointer;max-width:78ch}
.okey{font-weight:500;text-transform:uppercase;letter-spacing:.08em;font-size:.75rem;
 color:var(--g6);margin-right:var(--s1)}
.rec{display:inline-block;font-size:.6875rem;letter-spacing:.12em;text-transform:uppercase;
 font-weight:500;color:var(--accent);border:1px solid var(--accent);padding:.05rem .35rem;
 border-radius:2px;margin-right:var(--s1);white-space:nowrap}
.why{border-top:1px solid var(--rule);margin-top:var(--s2);padding-top:var(--s2);
 font-size:.875rem;color:var(--muted)}
textarea{width:100%;max-width:100%;font:inherit;font-size:.875rem;margin-top:var(--s2);
 padding:var(--s1) var(--s2);border:1px solid var(--g3);background:var(--paper);
 color:var(--ink);border-radius:2px;resize:vertical;min-height:2.6rem}
textarea:focus,button:focus-visible,input:focus-visible{outline:2px solid var(--accent);outline-offset:2px}

.bar{display:flex;flex-wrap:wrap;gap:var(--s2);align-items:center;margin-top:var(--s5);
 border-top:1px solid var(--g3);padding-top:var(--s3)}
button{font:inherit;font-size:.875rem;letter-spacing:.04em;padding:.5rem 1rem;cursor:pointer;
 background:var(--paper);color:var(--ink);border:1px solid var(--ink);border-radius:2px}
button:hover{background:var(--ink);color:var(--paper)}
button.ghost{border-color:var(--g3);color:var(--muted)}
.said{font-size:.8125rem;color:var(--g6)}
pre.exp{white-space:pre-wrap;word-break:break-word;background:var(--soft);border:1px solid var(--g2);
 padding:var(--s2);font-size:.8125rem;max-height:20rem;overflow:auto;margin-top:var(--s2)}

.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;margin-top:var(--s3);
 border-top:1px solid var(--g3)}
table{border-collapse:collapse;width:100%;font-size:.875rem;min-width:640px}
th,td{text-align:left;padding:.5rem .75rem;border-bottom:1px solid var(--rule);vertical-align:top}
th{font-size:.6875rem;letter-spacing:.1em;text-transform:uppercase;color:var(--g6);font-weight:500;
 white-space:nowrap}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
#perrole table{min-width:1120px}
tr.zero td{background:var(--soft)}
.zmark{color:var(--accent);font-weight:500}
.defn{font-size:.8125rem;color:var(--muted);max-width:52ch}
.sub td{font-size:.8125rem;color:var(--muted);background:var(--soft)}
.slug{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.82rem;white-space:nowrap}
.rolecell{font-weight:500;white-space:nowrap}
footer{border-top:1px solid var(--g3);padding-block:var(--s5);font-size:.8125rem;color:var(--muted)}
.recs{font-size:.875rem}
.recs dt{font-weight:500;margin-top:var(--s2)}
.recs dd{margin:0;color:var(--muted);word-break:break-word}
"""

parts = []
A = parts.append

A('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">')
A("<title>Roles drift — #273 decision page</title>")
A("<style>%s</style>" % CSS)
A('<script type="application/json" id="drift">%s</script>'
  % json.dumps(D).replace("<", "\\u003c"))

# ---- 1. headline
A('<section id="headline"><div class="wrap">')
A('<p class="label">#273 &middot; lane RD &middot; decision page</p>')
A("<h1>The canon is thin, not wrong.</h1>")
A("<p>The ruled membership in <code>roles.json</code> (s252-D1) names " + n(D["memberships_json"])
  + " memberships across " + n(D["roles"]) + " roles. The metas' <code>provides</code> — the "
  "first authoring pass, s251-D12 — carries " + n(D["memberships_meta_agree"]) + " of them. "
  "Only a meta's <code>provides</code> generates a <code>providesRole</code> edge (s270-D2), so "
  "the graph carries " + n(D["memberships_meta_agree"]) + " edges where the ruling names "
  + n(D["memberships_json"]) + ".</p>")
A("<p>The drift is ONE-DIRECTIONAL. Nothing in the metas contradicts the ruling; the metas are "
  "simply silent. Closing it is an enactment by addition, not a re-judgement.</p>")
A('<div class="stats">')
for v, lab in ((D["memberships_json"], "memberships ruled"),
               (D["memberships_meta_agree"], "carried by metas"),
               (D["memberships_meta_silent"], "metas silent"),
               (n_zero, "roles at zero")):
    A("<div class=\"stat\"><b>%s</b><span>%s</span></div>" % (E(str(v)), E(lab)))
A("</div>")
A('<div class="zeros">')
for v, lab in ((n_contra, "contradictions"), (n_dangling, "dangling slugs"),
               (n_invent, "metas inventing a role"),
               (n_nap, "not-a-provider carrying provides")):
    A("<div><b>%s</b> %s</div>" % (E(str(v)), E(lab)))
A("</div>")
A("<p class=\"why\">Corpus: " + n(D["corpus_metas"]) + " metas, of which " + n(D["metas_with_provides"])
  + " carry <code>provides</code> and " + n(D["metas_with_when"]) + " carry a <code>when</code>. "
  "<code>roles.json</code> supplies an illustrative <code>when</code> for " + n(D["json_when_present"])
  + " of its " + n(D["memberships_json"]) + " memberships; " + n(D["silent_with_json_when"])
  + " of the silent metas have one waiting.</p>")
A("</div></section>")

# ---- 2. decisions
A('<section id="decisions"><div class="wrap">')
A('<p class="label">Decisions</p>')
A("<h2>Four decisions. The recommendation is first in each.</h2>")
A("<p>Nothing here is ruled. Every option stays open; the marked option is the lane's "
  "recommendation and carries no weight beyond that.</p>")
for d in DECISIONS:
    A('<div class="dec" data-id="%s">' % E(d["id"]))
    A('<div class="dechead"><span class="decid">%s</span><h3>%s</h3></div>'
      % (E(d["id"]), E(d["title"])))
    A("<p>%s</p>" % d["lead"])
    A('<ul class="opts">')
    for key, is_rec, text in d["options"]:
        oid = "%s-%s" % (d["id"], key)
        A('<li><div class="opt">'
          '<input type="radio" name="%s" id="%s" value="%s">'
          '<label for="%s"><span class="okey">(%s)</span>%s%s</label>'
          "</div></li>"
          % (E(d["id"]), E(oid), E(key), E(oid), E(key),
             '<span class="rec">Recommended</span>' if is_rec else "", text))
    A('<li><div class="opt">'
      '<input type="radio" name="%s" id="%s-none" value="">'
      '<label for="%s-none"><span class="okey">(&mdash;)</span>No choice yet — clear this decision.'
      "</label></div></li>" % (E(d["id"]), E(d["id"]), E(d["id"])))
    A("</ul>")
    if d["why"]:
        A('<p class="why">%s</p>' % d["why"])
    A('<textarea class="note" data-id="%s" aria-label="Notes for %s" '
      'placeholder="Notes for %s — your words"></textarea>'
      % (E(d["id"]), E(d["id"]), E(d["id"])))
    A("</div>")
A('<div class="bar">'
  '<button type="button" id="btnExport">Export JSON</button>'
  '<button type="button" id="btnCopy">Copy to clipboard</button>'
  '<button type="button" class="ghost" id="btnClear">Clear</button>'
  '<span class="said" id="said">not saved yet</span>'
  "</div>")
A('<pre class="exp" id="exp" hidden></pre>')
A("</div></section>")

# ---- 3. per-role table
A('<section id="perrole"><div class="wrap">')
A('<p class="label">Per role</p>')
A("<h2>Where the drift sits</h2>")
A("<p><b>json</b> = memberships ruled in <code>roles.json</code>. <b>agree</b> = metas that carry "
  "the address today. <b>silent</b> = metas RD-1 would write. <b>j-when</b> = memberships with an "
  "illustrative <code>when</code> in <code>roles.json</code>.</p>")
A('<div class="tw"><table><thead><tr>'
  '<th class="num">#</th><th>Role</th><th class="num">json</th><th class="num">agree</th>'
  '<th class="num">silent</th><th class="num">j-when</th><th>Zero</th><th>Definition</th>'
  "</tr></thead><tbody>")
for r in D["per_role"]:
    A('<tr class="%s">' % ("zero" if r["zero_in_metas"] else ""))
    A('<td class="num">%s</td>' % E(str(r["index"])))
    A('<td class="rolecell">%s</td>' % E(r["role"]))
    for k in ("json", "meta_agrees", "meta_silent", "json_when_present"):
        A('<td class="num">%s</td>' % E(str(r[k])))
    A('<td>%s</td>' % ('<span class="zmark">ZERO</span>' if r["zero_in_metas"] else "&mdash;"))
    A('<td class="defn">%s</td>' % E(r["definition"]))
    A("</tr>")
    if r["zero_in_metas"]:
        items = " &middot; ".join(
            "<span class='slug'>%s</span> <span style='color:var(--g6)'>%s</span>"
            % (E(p["slug"]), E(p["json_when"] or "—"))
            for p in r["providers"])
        A('<tr class="sub"><td></td><td colspan="7">Providers: %s</td></tr>' % items)
A("</tbody></table></div>")
A("</div></section>")

# ---- 4. the silent metas
A('<section id="silent"><div class="wrap">')
A('<p class="label">What RD-1 writes</p>')
A("<h2>The " + str(D["memberships_meta_silent"]) + " silent metas</h2>")
A("<p>Grouped by role, in <code>roles.json</code> order. The <code>when</code> column is "
  "<code>roles.json</code>'s illustrative one-liner — RD-1 does not copy it onto the meta "
  "(RD-2 authors the gate instead).</p>")
A('<div class="tw"><table><thead><tr><th>Role</th><th>Slug</th>'
  "<th>roles.json <code>when</code></th></tr></thead><tbody>")
for role, p in SILENT_ROWS:
    A('<tr><td class="rolecell">%s</td><td class="slug">%s</td><td class="defn">%s</td></tr>'
      % (E(role), E(p["slug"]), E(p["json_when"] or "—")))
A("</tbody></table></div>")
A("</div></section>")

# ---- 5. the illegal field names
A('<section id="fields"><div class="wrap">')
A('<p class="label">RD-3 detail</p>')
A("<h2>The field names outside the closed list</h2>")
A("<p>The legal set in <code>when-fields.json</code>: "
  + " &middot; ".join("<code>%s</code>" % E(f) for f in D["legal_when_fields"]) + ".</p>")
A('<div class="tw"><table><thead><tr><th>Meta</th><th>Field</th><th>Clause</th>'
  "</tr></thead><tbody>")
for row in sorted(D["illegal_when_clauses"],
                  key=lambda r: (r["meta"].lower(), r["field"].lower())):
    A('<tr><td class="slug">%s</td><td class="slug">%s</td><td class="defn">%s</td></tr>'
      % (E(row["meta"]), E(row["field"]), E(row["clause"])))
A("</tbody></table></div>")
A("</div></section>")

# ---- 6. receipts
A('<section id="receipts"><div class="wrap">')
A('<p class="label">Receipts</p>')
A("<h2>Where every figure came from</h2>")
A('<div class="split"><div>')
A('<dl class="recs">')
for k, v in (("Commit", D["measured_at"]),
             ("Script", "knowledge/_roles_drift.py"),
             ("Corpus", "knowledge/components/*.meta.json &middot; knowledge/roles.json "
                        "&middot; knowledge/when-fields.json"),
             ("Data", "notes/_lanes/273/roles-drift/DRIFT.json"),
             ("Builder", "notes/_lanes/273/roles-drift/_build_page.py"),
             ("Command", "<code>python3 knowledge/_roles_drift.py --json &gt; "
                         "notes/_lanes/273/roles-drift/DRIFT.json</code>")):
    A("<dt>%s</dt><dd>%s</dd>" % (E(k), v))
A("</dl>")
A("</div><div>")
A("<p>Every figure on this page is read from <code>DRIFT.json</code> at build time, or derived "
  "from it by a formula recorded in <code>DERIVED.json</code> beside it. No number was typed by "
  "hand. <code>_numbers_check.py</code> re-extracts the integers from the rendered page and "
  "proves each one against those two files.</p>")
A("<p>The #270 measurement (<code>notes/_lanes/270/roles-desk/ROLES-DRIFT.md</code>) is STALE — "
  "these numbers supersede it.</p>")
A("</div></div>")
A("</div></section>")

A('<footer><div class="wrap">Nothing on this page is a ruling. Dave rules; the lane enacts by '
  "addition.</div></footer>")

JS = """
(function(){
 var KEY="apollo-roles-drift-273-v1";
 var IDS=%s;
 var state={};
 var lastSaved=null;
 function el(id){return document.getElementById(id);}
 function load(){
  try{var raw=localStorage.getItem(KEY);
   if(raw){var o=JSON.parse(raw);
    if(o&&typeof o==="object"){state=o.decisions||{};lastSaved=o.at||null;}}}
  catch(e){state={};}
  if(!state||typeof state!=="object")state={};
 }
 function save(){
  lastSaved=new Date().toISOString();
  try{localStorage.setItem(KEY,JSON.stringify({decisions:state,at:lastSaved}));}catch(e){}
  paint();
 }
 function two(v){return (v<10?"0":"")+v;}
 function paint(){
  var done=0;
  IDS.forEach(function(id){var r=state[id];if(r&&r.choice)done++;});
  var t="\\u2014";
  if(lastSaved){try{var d=new Date(lastSaved);t=two(d.getHours())+":"+two(d.getMinutes());}catch(e){}}
  el("said").textContent=done+" of "+IDS.length+" decided \\u00b7 saved "+t;
 }
 function put(id,k,v){
  var r=state[id]||{};r[k]=v;r.at=new Date().toISOString();
  if(!r.choice&&!r.note){delete state[id];}else{state[id]=r;}
 }
 function restore(){
  IDS.forEach(function(id){
   var r=state[id]||{};
   if(r.choice){
    var b=document.querySelector('input[name="'+id+'"][value="'+r.choice+'"]');
    if(b)b.checked=true;
   }
   var ta=document.querySelector('textarea.note[data-id="'+id+'"]');
   if(ta&&r.note)ta.value=r.note;
  });
 }
 function exportObj(){
  return {page:"_REVIEW-roles-drift-2026-09-15-v1.html",
          at:new Date().toISOString(),
          decisions:IDS.map(function(id){
            var r=state[id]||{};
            return {id:id,choice:r.choice||null,note:r.note||""};
          })};
 }
 function show(){
  var j=JSON.stringify(exportObj(),null,2);
  var p=el("exp");p.hidden=false;p.textContent=j;return j;
 }
 document.addEventListener("change",function(e){
  if(e.target.type==="radio"&&IDS.indexOf(e.target.name)>-1){
   put(e.target.name,"choice",e.target.value||null);save();
  }
 });
 var timer=null;
 document.addEventListener("input",function(e){
  if(e.target.classList&&e.target.classList.contains("note")){
   put(e.target.dataset.id,"note",e.target.value);
   clearTimeout(timer);timer=setTimeout(save,400);
  }
 });
 /* #272 by addition: a note typed <400ms before a reload/close was lost. Flush on blur and unload. */
 document.addEventListener("focusout",function(e){
  if(e.target.classList&&e.target.classList.contains("note")){clearTimeout(timer);save();}
 });
 window.addEventListener("beforeunload",function(){clearTimeout(timer);save();});
 el("btnExport").addEventListener("click",function(){
  var j=show();
  try{
   var a=document.createElement("a");
   a.href=URL.createObjectURL(new Blob([j],{type:"application/json"}));
   a.download="roles-drift-decisions-2026-09-15.json";
   document.body.appendChild(a);a.click();
   setTimeout(function(){URL.revokeObjectURL(a.href);a.remove();},1500);
  }catch(e){}
  el("exp").scrollIntoView({behavior:"smooth",block:"nearest"});
 });
 el("btnCopy").addEventListener("click",function(){
  var j=show();var b=el("btnCopy");
  function ok(){b.textContent="Copied";setTimeout(function(){b.textContent="Copy to clipboard";},1600);}
  try{
   if(navigator.clipboard&&navigator.clipboard.writeText){
    navigator.clipboard.writeText(j).then(ok,function(){ok();});return;
   }
  }catch(e){}
  try{var t=el("exp");var r=document.createRange();r.selectNodeContents(t);
   var s=getSelection();s.removeAllRanges();s.addRange(r);document.execCommand("copy");ok();}catch(e){}
 });
 el("btnClear").addEventListener("click",function(){
  if(!confirm("Clear every choice and note on this page?"))return;
  state={};try{localStorage.removeItem(KEY);}catch(e){}
  document.querySelectorAll('input[type="radio"]').forEach(function(i){i.checked=false;});
  document.querySelectorAll("textarea.note").forEach(function(t){t.value="";});
  el("exp").hidden=true;save();
 });
 load();restore();paint();
})();
""" % json.dumps([d["id"] for d in DECISIONS])
A("<script>%s</script>" % JS)

open(OUT, "w").write("\n".join(parts) + "\n")
print("wrote", OUT, os.path.getsize(OUT), "bytes")
print("wrote", DERIVED_OUT, len(DERIVED), "derived figures")
