#!/usr/bin/env python3
"""gen_rule_notes.py — #282: the 15 rule notes as a decision page for Dave's export.
Source of every quoted note: notes/_lanes/281/rests-on-land/RULE-NOTES-2026-09-17.md (his words verbatim).
Recommendations are the conductor's; nothing here is inscribed until the export comes back."""
import json, html, datetime, pathlib
OUT = pathlib.Path(__file__).with_name("RULE-NOTES-2026-09-17.html")
PAGE = "RULE-NOTES-2026-09-17"

R = []
def row(id, file, rule, note, change, opts, rec, tier, kind):
    R.append(dict(id=id, file=file, rule=rule, note=note, change=change, opts=opts, rec=rec, tier=tier, kind=kind))

row("aca-003","accessibility-content-authoring.md",
 "CA-3 — unique, concise page/frame/iframe titles (SC 2.4.2 A + 4.1.2 A): first thing a speech-output user hears.",
 "This is interesting, so a designer may argue that an active navigation element might be enough for orientation at the top level of at least, sometimes a salutation might be the first heading and sometimes it might be more marketing lead messging.",
 "A stated exception for top-level pages where an active navigation state already carries the orientation — which weakens a WCAG-A obligation.",
 [("a","Keep the rule as it is; your note stays on the edge as designer knowledge, not as an exception",
   "The floor holds. The title is heard before any navigation is reached, so the nav can’t substitute for it. Your point about salutations and marketing headings is real and is kept — as the reason the H1 and the title are two different things.",
   "The tension you spotted isn’t written into the rule."),
  ("b","Add the exception: top-level pages may rely on an active navigation state",
   "Says what a designer might argue.","A speech-output user hears the title first and the nav later; the exception fails the person the rule exists for, and it is a WCAG A criterion."),
  ("c","Split it: the title stays an obligation; add a heuristic that the first heading need not repeat the title",
   "Captures your actual observation — first heading ≠ title — without touching the floor.","One more guideline line.")],
 "c","floor","rule")

row("aid-009","accessibility-interaction-design.md",
 "ID-26 [introduced 2024] — target size, the formal 2.2 rule: HSBC DEFAULT 44×44, minimum exception 24×24 (SC 2.5.8 + 2.5.5): 24 only with the spacing/equivalent/inline/UA/essential outs; “HSBC already has formal design guidance… 44×44 is therefore considered the default requirement.”",
 "So this is about the actual size of the visible target, we have a 44px invisible hit area to meet the rule, this doesn't take into account context, the clear area around the target spacing can create emphasis also, we also have compact views to think about, but that would be a user choice. I like this principle, but it feels too boolian, maybe we need to discuss.",
 "The rule would have to say whether 44 is measured on the visible target or the hit area, and admit clear space and compact views as context — a rewrite, not a clarification. You said “maybe we need to discuss”.",
 [("a","Split it: the hit area stays boolean (44 default, 24 floor); the visible target, clear space and compact views become a graded heuristic beside it",
   "The a11y floor stays a floor and stays testable. The “too boolean” part — context, emphasis, compact as a user choice — gets a home where taste is allowed.",
   "Two lines where there was one; the heuristic needs a principle to rest on (Fitts already landed)."),
  ("b","Rewrite the one rule to say 44 is the hit area and name clear space and compact views as context",
   "One rule, fuller.","An obligation carrying context clauses is exactly the boolean-with-exceptions shape you don’t like; harder to gate."),
  ("c","Leave it; talk it through in a sitting first",
   "Nothing changes until you’ve discussed it.","It stays boolean meanwhile.")],
 "a","floor","ask")

row("col26-009","colour-standards-2026.md",
 "Don’t use the supporting palette as text.",
 "This is also a brand consistency rule, if designers were allowed to use the supporting palette we would get dramatically varied designs.",
 "The rule states two reasons — a contrast floor and a brand-consistency floor. The edge already carries both; the rule text would be catching up.",
 [("a","Add the second reason to the rule text","The rule says why in your words; the two edges and the text agree.","A guideline edit and a regen."),
  ("b","Leave the text; the two edges carry it","No edit.","A designer reading the guideline sees one reason; the graph knows two.")],
 "a","brand","rule")

row("col26-012","colour-standards-2026.md",
 "Don’t combine HSBC Red with the supporting palette in data visualisations.",
 "I'm actually not sure about this, the rule is partly a brand concern the primary red is only for the logo and for CTAs, tabs and the 'brand-bar' tilting. We allow the use of RAG in charts as long as it's used appropriately.",
 "A flat ban becomes a reservation with a named exception: primary red is reserved for logo, CTAs, tabs and the brand bar; RAG red in charts is allowed when it means status. You said “I’m actually not sure”.",
 [("a","Rewrite as a reservation: primary red reserved for logo · CTAs · tabs · brand bar; RAG red permitted in charts only as status",
   "Matches what you actually allow. A chart lane can gate it: red in a chart must be a RAG token, never the brand token.",
   "It touches the charts guideline as well, so two files move."),
  ("b","Keep the ban as written","No change.","The rule forbids something you say is allowed; the graph records a rule you don’t believe."),
  ("c","Discuss first","Your uncertainty is respected.","Stays wrong meanwhile.")],
 "a","brand","ask")

row("dv-bar-007","data-visualisation-bar-charts.md",
 "Positive + negative values: vertical bars only. Don’t put negative values on a horizontal bar chart.",
 "We do have specific bar charts that show negative values that sink below the zero line. so this rule s for a specific type of bar chart, one that only has a positive scale",
 "Scope narrowing: the rule applies to positive-scale bar charts, and the below-zero vertical form is named as the sanctioned way to show negatives.",
 [("a","Scope it: applies to positive-scale bar charts; negatives use the vertical below-zero form",
   "Says what ships. Removes a false conflict with the diverging bar in the chart engine.","A guideline edit and a regen."),
  ("b","Leave it","No change.","The rule reads as a ban on a chart you already ship.")],
 "a","charts","rule")

row("icon-006","icons.md",
 "Minimum 16px, maximum 48px; scale proportionately in 2px increments.",
 "this is true but it is also in place for consistence and at the ceiling its close illustration dimensions",
 "The rule states that the 16px floor is perceptual and the 48px ceiling exists to keep an icon from reading as an illustration.",
 [("a","Add the two reasons to the rule text: floor = legibility, ceiling = the icon/illustration boundary",
   "A designer learns why, not just what; the pictogram boundary (rows 10–11) gets its mirror.","A guideline edit and a regen."),
  ("b","Leave it","No change.","The ceiling stays an unexplained number.")],
 "a","brand","rule")

row("logo26-001","brand-refresh-assets.md",
 "An HSBC logo appears at least once on every piece of communication or customer journey.",
 "So this is nuanced, the logo will appear on webpages in the nav header anyway but not on native apps, the rational is that the user summoned an HSBC app, they know where the destination is, and the logo will usually appear on a logon or splash screen.",
 "A genuine relaxation: native apps are satisfied by the logon or splash screen, not by every screen.",
 [("a","Add the native-app clause: in a native app the journey’s logon or splash screen satisfies the rule",
   "Describes what ships and why. The logo review you keep asking for can start from a true rule.","A brand obligation gets its first stated exception."),
  ("b","Leave it as “every piece”","No change.","Every native screen is technically in breach.")],
 "a","brand","rule")

row("mot-005","motion-standards.md",
 "Any motion over 5 seconds needs play and pause.",
 "The principle is correct here but is is also a Ally rule we adhere to so the grade is probably wrong",
 "A grade question about the link, not the words: the edge moves from the C-graded control principle to the statutory obligation — or both land, since the link is many-to-many.",
 [("a","Both land: the control principle and the WCAG obligation (SC 2.2.2) as two edges; rule text unchanged",
   "Your “both” shape, already ruled. The statutory edge carries the grade that matters.","None of substance."),
  ("b","Replace the principle with the obligation","Cleaner.","Loses the design reason you said is correct.")],
 "a","floor","link")

row("photo26-002","brand-refresh-assets.md",
 "HARD bans: no Generative AI, mixed media or CGI-rendered elements in imagery; no montages/composites; no staged/posed/clichéd shots; no text as a mask. The gen-AI ban is PIPELINE-CRITICAL.",
 "On the AI part. This will probably change in the future",
 "Nothing today — a forecast, not a correction. The honest action is a review date on the gen-AI clause.",
 [("a","Put a review date on the gen-AI clause — March 2027 — no edit to the ban",
   "The record shows the clause is expected to move and when to look again.","A date is a promise to revisit."),
  ("b","Leave it, no date","No change.","The forecast is lost.")],
 "a","brand","rule")

row("pict-001","pictograms.md",
 "Every pictogram carries a label or copy that underpins its meaning — no exceptions (unlike icons’ universal-meaning carve-out).",
 "the usage rule for pictograms is that they do not signal an action they support a concept",
 "The rule states the boundary in its own words: pictograms support a concept, icons signal an action.",
 [("a","Write the definition into the rule: a pictogram supports a concept; an icon signals an action",
   "The boundary the guideline only implies becomes a sentence a designer and an agent can both quote. Row 15 depends on it.","A guideline edit and a regen."),
  ("b","Leave it implied","No change.","The carve-out keeps doing the defining.")],
 "a","brand","rule")

row("pict-010","pictograms.md",
 "Digital: minimum 60px, maximum 192px, proportional scaling at 2px intervals. Below 60px, use an icon instead.",
 "consistency, and misuse by designers",
 "The rule says the figures are enforcement against misuse, not a perceptual threshold — so the link stays a declared null.",
 [("a","Add the reason line; the null stands","Honest about what the number is for.","A guideline edit and a regen."),
  ("b","Leave it","No change.","A designer may assume the numbers are perceptual.")],
 "a","brand","rule")

row("type26-002","typography-standards-2026.md",
 "Only use brand-approved fonts, weights and colours.",
 "I think 1 is also applicable, think of different H1s on every page",
 "Nothing in the rule changes. Landed both ways under yesterday’s ruling: the declared null (brand and licensing) and “be consistent” beside it. The question is whether you meant the null to stand.",
 [("a","Both stand — the null and the consistency principle","As landed.","—"),
  ("b","The principle only; drop the null","One reason.","Brand and licensing is a real reason with no principle to hang on.")],
 "a","brand","ask")

row("type26-003","typography-standards-2026.md",
 "All text legible and ≥4.5:1 contrast.",
 "linked to 2 as you stated",
 "Not landed. If “linked to 2” means what your thirteen “both” rows mean, readability lands beside the WCAG contrast principle as a second edge.",
 [("a","Yes — land readability as a second edge","Reads as your other thirteen.","—"),
  ("b","No — the contrast principle only","The edge that was proposed stands alone.","—")],
 "a","floor","link")

row("col26-016","colour-standards-2026.md",
 "Don’t use red typography — red text is reserved for call to actions.",
 "This is both 1 and 2, there is one caveat, red text is allowed, but only the RAG red when used for position movement downward, as in a stat card",
 "The most concrete rule change on the list: “reserved for call to actions” becomes “reserved for call to actions and RAG-negative movement, as in a stat card”. Both edges are already landed.",
 [("a","Inscribe the exception: RAG red text is allowed for downward movement, stat-card style",
   "Says what ships. Pairs with row 4 — the same reservation, seen from the typography side.","A guideline edit and a regen; the stat-card component should cite it."),
  ("b","Leave it as a note on the edge","No edit.","The rule bans something the stat card does.")],
 "a","brand","rider")

row("neuro-026","neurodiversity.md",
 "Icons/visuals support text, never replace it — content must remain comprehensible with all images and icons removed.",
 "This 1 and 2. we also allow unpaired icons for the most commonly understood icons",
 "The rule gains the icons’ universal-meaning carve-out — which brings it in line with icons.md and directly against pict-001’s “no exceptions”, so the two must be read together. Both edges are already landed.",
 [("a","Inscribe the carve-out by reference: unpaired icons allowed only for the universal set named in icons.md; pictograms stay no-exception",
   "One list, named once, in one place; neuro and icons agree; pictograms stay strict because a pictogram is a concept, not an action (row 10).","A guideline edit and a regen; the universal set must actually be a list in icons.md."),
  ("b","Leave it as a note","No edit.","Neuro forbids what icons allows.")],
 "a","floor","rider")

assert len(R) == 15
E = html.escape
TIER = {"floor":"Accessibility floor","brand":"Brand","charts":"Charts"}
KIND = {"rule":"Argues with the rule","ask":"Your ASK","link":"About the link","rider":"Rider on a “both”"}

parts = []
for i, r in enumerate(R, 1):
    opts = []
    for v, title, f, a in r["opts"]:
        tag = '<span class="tag">recommended</span>' if v == r["rec"] else ""
        opts.append(f'<label class="opt"><input type="radio" name="{r["id"]}" value="{v}"><div><b>{E(title)}{tag}</b><div class="fa"><div><span>For</span>{E(f)}</div><div><span>Against</span>{E(a)}</div></div></div></label>')
    parts.append(f'''
<section class="dim" id="r{i}"><div class="wrapper"><div class="wrap">
 <div class="aside">
  <div class="idx">{i:02d}</div>
  <p class="tier">{E(TIER[r["tier"]])} · {E(KIND[r["kind"]])}</p>
  <p class="unblocks"><span>Rule</span><code>{E(r["id"])}</code> · {E(r["file"])} · BLOCKING</p>
 </div>
 <div class="main">
  <h3>{E(r["rule"])}</h3>
  <p class="quote">“{E(r["note"])}”</p>
  <p class="plain"><span class="k">If inscribed</span>{E(r["change"])}</p>
  <div class="opts">{"".join(opts)}</div>
  <label class="note"><span>Note</span><input type="text" id="note-{r["id"]}" placeholder="optional — your words, kept verbatim"></label>
 </div>
</div></div></section>''')

ids = json.dumps([r["id"] for r in R])
rec = json.dumps({r["id"]: r["rec"] for r in R})
title = json.dumps({r["id"]: r["rule"] for r in R})
jump = "".join(f'<a href="#r{i}">{i}</a>' for i in range(1, 16))
today = datetime.date.today().isoformat()

doc = f'''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The rule notes — fifteen rows — #282</title>
<style>
:root{{--accent:#DB0011;--black:#000;--white:#fff;--grey-1:#F3F3F3;--grey-2:#EDEDED;--grey-3:#D7D8D6;--grey-5:#9B9B9B;--grey-6:#767676;--grey-7:#545454;--grey-8:#333;--ok:#0B6E3A;
--s1:.5rem;--s2:1rem;--s3:1.5rem;--s4:2rem;--s5:3rem;--s6:4rem;--s7:6rem;--max:1200px;--gutter:2rem}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--white);color:var(--black);font:400 1rem/1.75 "Helvetica Neue",Helvetica,Arial,sans-serif}}
.wrapper{{max-width:var(--max);margin:0 auto;padding:0 var(--gutter)}}
nav{{position:sticky;top:0;z-index:9;background:var(--white);border-bottom:1px solid var(--grey-2)}}
nav .wrapper{{display:flex;align-items:center;justify-content:space-between;height:54px;gap:var(--s3)}}
nav a,nav span{{font-size:.875rem;letter-spacing:.05em;color:var(--grey-6);text-decoration:none}}
nav .now{{color:var(--black);font-weight:500}}
nav .jump{{display:flex;gap:var(--s2)}}
section{{padding:var(--s6) 0;border-bottom:1px solid var(--grey-2)}}
.label{{font-size:.75rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);display:flex;align-items:center;gap:var(--s1);margin:0 0 var(--s3)}}
.label::before{{content:"";display:inline-block;width:20px;height:1px;background:var(--accent);flex:none}}
h1{{font-size:3.5625rem;line-height:1.05;font-weight:400;margin:0 0 var(--s4);max-width:22ch}}
h2{{font-size:2.125rem;line-height:1.15;font-weight:400;margin:0 0 var(--s4)}}
h3{{font-size:1.1875rem;line-height:1.4;font-weight:500;margin:0 0 var(--s3);max-width:60ch}}
p{{margin:0 0 var(--s3);max-width:72ch}}
.lede{{font-size:1.1875rem;line-height:1.7;max-width:60ch}}
.meta{{font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;color:var(--grey-6);margin:0}}
.stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:var(--s4);margin-top:var(--s6)}}
.stats div b{{display:block;font-size:2.6875rem;font-weight:200;line-height:1}}
.stats div span{{display:block;font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;color:var(--grey-6);margin-top:var(--s2)}}
.dim .wrap{{display:grid;grid-template-columns:1fr 2fr;gap:var(--s6);align-items:start}}
.idx{{font-size:5.25rem;font-weight:100;line-height:.9;color:var(--grey-3);margin-bottom:var(--s3)}}
.tier{{font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;color:var(--grey-6);margin:0 0 var(--s3)}}
.unblocks{{font-size:.875rem;color:var(--grey-7);border-top:1px solid var(--grey-2);padding-top:var(--s3);margin:0}}
.unblocks span{{display:block;font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;color:var(--grey-6);margin-bottom:var(--s1)}}
.unblocks code{{font:400 .8125rem/1.6 Menlo,monospace}}
.plain{{font-size:1.0625rem;line-height:1.7}}
.plain .k{{display:block;font-size:.6875rem;letter-spacing:.12em;text-transform:uppercase;color:var(--grey-6)}}
.quote{{font-size:1.1875rem;line-height:1.6;border-left:2px solid var(--accent);padding-left:var(--s3);margin:0 0 var(--s4);max-width:60ch}}
.opts{{margin-top:var(--s3);border-top:1px solid var(--black)}}
.opt{{display:grid;grid-template-columns:auto 1fr;gap:var(--s2) var(--s3);padding:var(--s3) 0;border-bottom:1px solid var(--grey-2);cursor:pointer;align-items:start}}
.opt input{{margin:6px 0 0;flex:none}}
.opt b{{font-weight:500;display:block}}
.opt .tag{{font-size:.6875rem;letter-spacing:.12em;text-transform:uppercase;color:var(--ok);font-weight:500;margin-left:var(--s2)}}
.opt .fa{{display:grid;grid-template-columns:1fr 1fr;gap:var(--s3);margin-top:var(--s1);font-size:.875rem;color:var(--grey-7);line-height:1.6}}
.opt .fa span{{display:block;font-size:.6875rem;letter-spacing:.12em;text-transform:uppercase;color:var(--grey-6)}}
label.note{{display:block;margin-top:var(--s3)}}
label.note span{{display:block;font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;color:var(--grey-6);margin-bottom:var(--s1)}}
label.note input{{width:100%;max-width:46rem;font:400 .9375rem/1.6 inherit;padding:var(--s1) 0;border:none;border-bottom:1px solid var(--grey-3);background:none;color:var(--black)}}
label.note input:focus{{outline:none;border-bottom-color:var(--accent)}}
.grey{{background:var(--grey-1)}}
button{{font:500 .875rem/1 inherit;letter-spacing:.06em;text-transform:uppercase;padding:14px 22px;border:none;background:var(--black);color:var(--white);cursor:pointer}}
button.ghost{{background:none;color:var(--black);border-bottom:1px solid var(--accent);padding:14px 0;margin-left:var(--s4)}}
pre{{background:var(--white);padding:var(--s3);overflow:auto;font:400 .8125rem/1.6 Menlo,monospace;max-height:26rem;border:1px solid var(--grey-2)}}
#msg{{font-size:.875rem;color:var(--grey-7);margin-left:var(--s3)}}
footer{{padding:var(--s6) 0;font-size:.75rem;letter-spacing:.06em;color:var(--grey-6)}}
@media (max-width:900px){{
 :root{{--gutter:1rem}}
 h1{{font-size:2.125rem}} h2{{font-size:1.5rem}}
 section{{padding:var(--s5) 0}}
 nav .jump{{display:none}}
 .stats{{grid-template-columns:repeat(2,1fr);gap:var(--s3)}}
 .dim .wrap{{grid-template-columns:1fr;gap:var(--s3)}}
 .idx{{font-size:2.6875rem;margin-bottom:var(--s2)}}
 .opt .fa{{grid-template-columns:1fr}}
 button.ghost{{margin-left:0;display:block;margin-top:var(--s2)}}
}}
</style></head><body>
<nav><div class="wrapper"><span>#282 · the rule notes</span><span class="now">Fifteen rows</span><span class="jump">{jump}<a href="#export">Export</a></span></div></nav>

<section><div class="wrapper">
 <p class="label">Your notes, back to you</p>
 <h1>Fifteen things you said about a rule. Each becomes a guideline edit, or stays a note.</h1>
 <p class="lede">Yesterday’s 59 cards asked which principle each blocking rule rests on. In 15 of your answers you argued with the rule itself — its scope, its reason, a missing exception. None of that has touched a guideline: a note is not an edit. This page puts each one back as a choice, with a recommendation. Where you said “not sure” or “let’s discuss”, it says so.</p>
 <p class="meta">Every quote is yours, verbatim, from the 14:49Z export · rule text is as stored · the “if inscribed” sentence and the recommendation are mine · nothing lands until the file comes back</p>
 <div class="stats">
  <div><b>15</b><span>rows</span></div>
  <div><b>3</b><span>your ASKs — rows 2, 4, 12</span></div>
  <div><b>5</b><span>touch the accessibility floor</span></div>
  <div><b>11</b><span>would edit a guideline file</span></div>
 </div>
</div></section>
{"".join(parts)}

<section class="grey" id="export"><div class="wrapper">
 <p class="label">Export</p>
 <h2>Send the answers back</h2>
 <p>One choice per row. The export carries your pick and the recommendation side by side, so the record shows where you overruled me. Rows you leave blank stay as notes, exactly as they are today. Anything you pick that edits a guideline goes to one lane: the edit in your words, the rules index regenerated, the graph re-checked.</p>
 <p><button id="takeall" type="button">Take all the recommendations</button><button id="dl" class="ghost" type="button">Download the answers</button><button id="cp" class="ghost" type="button">Copy to clipboard</button><span id="msg"></span></p>
 <pre id="exp" hidden></pre>
</div></section>

<footer><div class="wrapper">#282 · notes/_lanes/282/rule-notes/{PAGE}.html · recommended, not ruled · generated {today}</div></footer>

<script>
var PAGE={json.dumps(PAGE)};
var IDS={ids};
var REC={rec};
var TITLE={title};
function state(id){{var r=document.querySelector('input[name="'+id+'"]:checked');var n=document.getElementById('note-'+id);
 var c=r?r.value:null;return {{rule:TITLE[id],choice:c,note:(n&&n.value)||"",recommended:REC[id],overruled:c!==null&&c!==REC[id]}}}}
function envelope(){{var a={{}};IDS.forEach(function(id){{a[id]=state(id)}});
 return {{exportedAt:new Date().toISOString(),page:PAGE,follows:"RESTS-ON-2026-09-17",source:"notes/_lanes/281/rests-on-land/RULE-NOTES-2026-09-17.md",answers:a}}}}
function show(){{var j=JSON.stringify(envelope(),null,2);var p=document.getElementById('exp');p.hidden=false;p.textContent=j;return j}}
document.getElementById('takeall').onclick=function(){{IDS.forEach(function(id){{var el=document.querySelector('input[name="'+id+'"][value="'+REC[id]+'"]');if(el)el.checked=true}});show();document.getElementById('msg').textContent='all fifteen set to the recommendation — change any before you export'}};
document.getElementById('dl').onclick=function(){{var j=show();var a=document.createElement('a');a.href=URL.createObjectURL(new Blob([j],{{type:'application/json'}}));a.download=PAGE+'-export.json';a.click();document.getElementById('msg').textContent='downloaded'}};
document.getElementById('cp').onclick=function(){{var j=show();try{{if(navigator.clipboard&&navigator.clipboard.writeText){{var w=navigator.clipboard.writeText(j);if(w&&w["catch"])w["catch"](function(){{}})}}}}catch(e){{}}document.getElementById('msg').textContent='copied — the JSON is below too'}};
document.addEventListener('change',function(){{if(!document.getElementById('exp').hidden)show()}});
</script>
</body></html>'''
OUT.write_text(doc, encoding="utf-8")
print(OUT, len(doc), "bytes", len(R), "rows")
