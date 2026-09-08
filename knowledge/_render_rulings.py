#!/usr/bin/env python3
"""Render knowledge/_rulings.json -> notes/_RULINGS.html (Dave's rulings page).

A GENERATOR, not a one-off page: re-run it at every wrap and the surface stays
current. `--check` compares the source sha256 embedded in the on-disk HTML with
the current sha256 of _rulings.json and prints FRESH or STALE (exit 1 on STALE).
It never builds anything.

Usage:
  python3 knowledge/_render_rulings.py [--out PATH]
  python3 knowledge/_render_rulings.py --check [--out PATH] [--src PATH]
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import argparse
import hashlib
import html
import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(HERE, "_rulings.json")
OUT = os.path.join(ROOT, "notes", "_RULINGS.html")

SHA_RE = re.compile(r"<!-- source-sha256:([0-9a-f]{64}) ")

# Ordered: first keyword found in the status prose wins.
STATUS_ORDER = [
    "SUPERSEDED", "REVERSED", "ABANDONED", "PART-ENACTED",
    "IN PROGRESS", "ENACTED", "BUILT", "STANDING", "OPEN", "RULED",
]


def src_sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def status_key(status):
    u = (status or "").upper()
    for k in STATUS_ORDER:
        if k in u:
            return k
    return "OTHER"


def session_of(rid):
    m = re.match(r"^(s\d+)", rid)
    if m:
        return m.group(1)
    m = re.match(r"^([a-z]+)-", rid)
    return m.group(1) if m else rid


def session_rank(sess):
    m = re.match(r"^s(\d+)$", sess)
    return (1, int(m.group(1))) if m else (0, 0)


E = html.escape


def li(items, cls):
    if not items:
        return ""
    if isinstance(items, str):
        items = [items]
    return ('<ul class="%s">' % cls) + "".join("<li>%s</li>" % E(str(i)) for i in items) + "</ul>"


CSS = """
:root{
  --accent:#DA1A00;            /* TWO-RED LAW: on white */
  --bg:#FFFFFF; --panel:#F3F3F3; --rule:#E2E2E2; --rule-2:#D0D0D0;
  --ink:#000000; --ink-2:#333333; --ink-3:#545454; --ink-4:#767676;
  --quote-bg:#F7F7F5; --pill:#EDEDED;
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,"Liberation Mono",monospace;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI","Helvetica Neue",Helvetica,Arial,sans-serif;
  --s1:.5rem; --s2:1rem; --s3:1.5rem; --s4:2rem; --s5:3rem; --s6:4rem;
  --max:1160px;
}
@media (prefers-color-scheme:dark){
  :root{
    --accent:#F6604C;          /* TWO-RED LAW: on everything else */
    --bg:#0C0C0C; --panel:#161616; --rule:#2A2A2A; --rule-2:#3A3A3A;
    --ink:#F2F2F2; --ink-2:#DCDCDC; --ink-3:#B8B8B8; --ink-4:#8E8E8E;
    --quote-bg:#141414; --pill:#222222;
  }
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:400 16px/1.7 var(--sans);
  overflow-wrap:break-word}
.wrap{max-width:var(--max);margin:0 auto;padding:0 var(--s4)}
a{color:inherit}
.label{font-size:12px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;
  color:var(--accent);display:flex;align-items:center;gap:var(--s1);margin:0 0 var(--s2)}
.label::before{content:"";display:inline-block;width:20px;height:1px;background:var(--accent);flex:none}

/* Masthead */
header.mast{padding:var(--s5) 0 var(--s4);border-bottom:1px solid var(--rule)}
h1{font-size:clamp(2.25rem,7vw,3.5625rem);font-weight:500;line-height:1.05;letter-spacing:0;margin:0 0 var(--s3)}
.standfirst{max-width:46ch;color:var(--ink-2);margin:0 0 var(--s4)}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:var(--s3);
  border-top:1px solid var(--rule);padding-top:var(--s3)}
.stat b{display:block;font-size:clamp(1.75rem,5vw,2.6875rem);font-weight:200;line-height:1.05;letter-spacing:0}
.stat span{display:block;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-4);margin-top:var(--s1)}
.tallies{display:grid;grid-template-columns:1fr 1fr;gap:var(--s3) var(--s5);
  border-top:1px solid var(--rule);margin-top:var(--s3);padding-top:var(--s3)}
.tally h2{font-size:12px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;
  color:var(--ink-4);margin:0 0 var(--s1)}
.tally dl{display:grid;grid-template-columns:1fr auto;gap:2px var(--s2);margin:0;font-size:14px}
.tally dt{color:var(--ink-3)}
.tally dd{margin:0;font-variant-numeric:tabular-nums;font-family:var(--mono);font-size:13px}

/* Filter bar */
.bar{position:sticky;top:0;z-index:10;background:var(--bg);border-bottom:1px solid var(--rule);
  padding:var(--s2) 0}
.bar .wrap{display:flex;flex-wrap:wrap;gap:var(--s1) var(--s2);align-items:center}
.bar input[type=search],.bar select{font:400 14px/1.4 var(--sans);color:var(--ink);
  background:var(--bg);border:1px solid var(--rule-2);border-radius:0;padding:8px 10px}
.bar input[type=search]{flex:1 1 220px;min-width:0;max-width:100%}
.bar select{flex:0 1 auto;min-width:0;max-width:100%}
.bar label.tog{display:flex;align-items:center;gap:6px;font-size:13px;letter-spacing:.04em;
  text-transform:uppercase;color:var(--ink-3);cursor:pointer;white-space:nowrap}
.bar .count{font-family:var(--mono);font-size:13px;color:var(--ink-4);white-space:nowrap}
.bar .count b{color:var(--accent);font-weight:500}

/* Sessions + entries */
main{padding-bottom:var(--s6)}
section.sess{border-top:1px solid var(--rule);padding-top:var(--s3);margin-top:var(--s4)}
section.sess>h2{margin:0 0 var(--s2);font-size:19px;font-weight:500;letter-spacing:.04em;
  display:flex;gap:var(--s2);align-items:baseline;flex-wrap:wrap}
section.sess>h2 .sid{font-family:var(--mono)}
section.sess>h2 .sdate{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-4)}
article.ruling{border-top:1px solid var(--rule);padding:var(--s3) 0;
  display:grid;grid-template-columns:170px 1fr;gap:var(--s3) var(--s4);align-items:start}
article.ruling:first-of-type{border-top:0}
.meta{display:flex;flex-direction:column;gap:6px;font-size:13px;color:var(--ink-4)}
.meta .rid{font-family:var(--mono);font-size:14px;color:var(--ink);text-decoration:none;
  border-bottom:1px solid var(--rule-2);align-self:start}
.meta .rid:hover{border-bottom-color:var(--accent)}
.meta .date{font-variant-numeric:tabular-nums;font-family:var(--mono)}
.pill{align-self:start;font-size:11px;letter-spacing:.12em;text-transform:uppercase;font-weight:500;
  padding:3px 8px;background:var(--pill);color:var(--ink-2);border:1px solid var(--rule-2)}
.pill[data-s="ENACTED"],.pill[data-s="BUILT"]{border-color:var(--ink-3);color:var(--ink)}
.pill[data-s="SUPERSEDED"],.pill[data-s="OPEN"],.pill[data-s="PART-ENACTED"],.pill[data-s="IN PROGRESS"]{
  color:var(--accent);border-color:var(--accent);background:transparent}
.body>*{margin:0 0 var(--s2)}
.body>*:last-child{margin-bottom:0}
.ruled{color:var(--ink)}
blockquote.says{margin:0 0 var(--s2);background:var(--quote-bg);border-left:2px solid var(--accent);
  padding:var(--s2) var(--s3);font-size:17px;line-height:1.65;color:var(--ink)}
blockquote.says::before{content:"\\201C";position:absolute;opacity:0}
.k{font-size:12px;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-4);
  display:block;margin-bottom:4px}
ul.paths,ul.ev{list-style:none;margin:0 0 var(--s2);padding:0;font-size:13px;color:var(--ink-3)}
ul.paths li{font-family:var(--mono);overflow-wrap:anywhere;line-height:1.55}
ul.ev li{overflow-wrap:anywhere;line-height:1.55}
.statusnote{font-size:13px;color:var(--ink-3)}
.det{border-top:1px solid var(--rule);padding-top:var(--s2)}
.det summary{cursor:pointer;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-4)}
.empty{padding:var(--s5) 0;color:var(--ink-4)}
footer{border-top:1px solid var(--rule);padding:var(--s4) 0;font-size:13px;color:var(--ink-4)}

/* Dave's words only */
body.words article.ruling .ruled,body.words article.ruling .extra,
body.words article.ruling .statusnote,body.words article.ruling .pill{display:none}
body.words article.ruling{grid-template-columns:140px 1fr}

/* Narrow */
@media (max-width:760px){
  .wrap{padding:0 var(--s2)}
  .stats{grid-template-columns:repeat(2,1fr)}
  .tallies{grid-template-columns:1fr}
  article.ruling,body.words article.ruling{grid-template-columns:1fr;gap:var(--s2)}
  .meta{flex-direction:row;flex-wrap:wrap;align-items:center;gap:var(--s1) var(--s2)}
  blockquote.says{padding:var(--s2)}
}

@media print{
  .bar,.det{display:none!important}
  body{background:#fff;color:#000;font-size:11pt}
  article.ruling{break-inside:avoid;page-break-inside:avoid;grid-template-columns:150px 1fr}
  blockquote.says{background:transparent;border-left:2px solid #DA1A00}
  a{text-decoration:none}
}
"""

JS = r"""
(function(){
  var arts=[].slice.call(document.querySelectorAll('article.ruling'));
  var sects=[].slice.call(document.querySelectorAll('section.sess'));
  arts.forEach(function(a){ a._s=(a.textContent||'').toLowerCase(); });
  var q=document.getElementById('q'), st=document.getElementById('st'),
      by=document.getElementById('by'), wo=document.getElementById('wo'),
      cnt=document.getElementById('cnt');
  function apply(){
    var t=(q.value||'').trim().toLowerCase(), s=st.value, b=by.value, n=0;
    arts.forEach(function(a){
      var ok=(!s||a.getAttribute('data-status')===s)&&(!b||a.getAttribute('data-by')===b)&&
             (!t||a._s.indexOf(t)>-1);
      a.hidden=!ok; if(ok)n++;
    });
    sects.forEach(function(sec){
      var any=[].slice.call(sec.querySelectorAll('article.ruling')).some(function(a){return !a.hidden;});
      sec.hidden=!any;
    });
    document.body.classList.toggle('words', wo.checked);
    cnt.innerHTML='<b>'+n+'</b> / '+arts.length;
    var e=document.getElementById('empty'); if(e) e.hidden=(n>0);
  }
  [q,st,by].forEach(function(el){el.addEventListener('input',apply);});
  wo.addEventListener('change',apply);
  window.addEventListener('hashchange',function(){
    var el=document.getElementById(location.hash.slice(1));
    if(el&&el.hidden){q.value='';st.value='';by.value='';apply();el.scrollIntoView();}
  });
  apply();
})();
"""


def build(src=SRC, out=OUT):
    with open(src, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    rulings = data["rulings"]
    sha = src_sha(src)

    for r in rulings:
        r["_sess"] = session_of(r["id"])
        r["_sk"] = status_key(r.get("status"))

    dates = sorted(r.get("date", "") for r in rulings if r.get("date"))
    span = "%s - %s" % (dates[0], dates[-1]) if dates else "-"

    by_status, by_who = {}, {}
    for r in rulings:
        by_status[r["_sk"]] = by_status.get(r["_sk"], 0) + 1
        by_who[r.get("by", "?")] = by_who.get(r.get("by", "?"), 0) + 1

    # group by session, newest first
    groups = {}
    for r in rulings:
        groups.setdefault(r["_sess"], []).append(r)

    def gkey(s):
        rs = groups[s]
        return (max(x.get("date", "") for x in rs), session_rank(s), s)

    order = sorted(groups, key=gkey, reverse=True)
    last_id = groups[order[0]][0]["id"] if order else "-"
    for s in order:
        groups[s].sort(key=lambda x: (x.get("date", ""), x["id"]), reverse=True)
    if order:
        g0 = groups[order[0]]
        last_id = g0[0]["id"]

    P = []
    A = P.append
    A("<!-- source-sha256:%s  source:knowledge/_rulings.json -->" % sha)
    A("<!-- generated by knowledge/_render_rulings.py on %s - DO NOT EDIT BY HAND -->" % date.today().isoformat())
    A("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">")
    A("<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">")
    A("<title>His Rulings - %d decisions</title>" % len(rulings))
    A("<style>%s</style></head><body>" % CSS)

    # masthead
    A("<header class=\"mast\"><div class=\"wrap\">")
    A("<p class=\"label\">Apollo / UX-design</p>")
    A("<h1>His rulings</h1>")
    A("<p class=\"standfirst\">Every ruling Dave has made, newest first, in his own words. "
      "Generated from <code>knowledge/_rulings.json</code> - re-run the generator at any wrap "
      "and this page is current again.</p>")
    A("<div class=\"stats\">")
    for b, s in [(str(len(rulings)), "rulings"), (last_id, "last id"),
                 (str(len(order)), "sessions"), (span, "date span")]:
        A("<div class=\"stat\"><b>%s</b><span>%s</span></div>" % (E(b), E(s)))
    A("</div>")
    A("<div class=\"tallies\">")
    A("<div class=\"tally\"><h2>By status</h2><dl>")
    for k in sorted(by_status, key=lambda k: (-by_status[k], k)):
        A("<dt>%s</dt><dd>%d</dd>" % (E(k), by_status[k]))
    A("</dl></div>")
    A("<div class=\"tally\"><h2>By who ruled</h2><dl>")
    for k in sorted(by_who, key=lambda k: (-by_who[k], k)):
        A("<dt>%s</dt><dd>%d</dd>" % (E(k), by_who[k]))
    A("</dl></div>")
    A("</div></div></header>")

    # filter bar
    A("<div class=\"bar\"><div class=\"wrap\">")
    A("<input id=\"q\" type=\"search\" placeholder=\"Search id, ruling, his words, paths\" "
      "aria-label=\"Search rulings\">")
    A("<select id=\"st\" aria-label=\"Filter by status\"><option value=\"\">All statuses</option>")
    for k in sorted(by_status, key=lambda k: (-by_status[k], k)):
        A("<option value=\"%s\">%s (%d)</option>" % (E(k), E(k), by_status[k]))
    A("</select>")
    A("<select id=\"by\" aria-label=\"Filter by who ruled\"><option value=\"\">Anyone</option>")
    for k in sorted(by_who):
        A("<option value=\"%s\">%s (%d)</option>" % (E(k), E(k), by_who[k]))
    A("</select>")
    A("<label class=\"tog\"><input type=\"checkbox\" id=\"wo\"> Dave's words only</label>")
    A("<span class=\"count\" id=\"cnt\" aria-live=\"polite\"></span>")
    A("</div></div>")

    A("<main><div class=\"wrap\">")
    A("<p class=\"empty\" id=\"empty\" hidden>No rulings match those filters.</p>")

    for sess in order:
        rs = groups[sess]
        A("<section class=\"sess\" id=\"sess-%s\">" % E(sess))
        A("<h2><span class=\"sid\">%s</span><span class=\"sdate\">%s &middot; %d ruling%s</span></h2>"
          % (E(sess), E(rs[0].get("date", "")), len(rs), "" if len(rs) == 1 else "s"))
        for r in rs:
            status = r.get("status") or ""
            sk = r["_sk"]
            A("<article class=\"ruling\" id=\"%s\" data-status=\"%s\" data-by=\"%s\">"
              % (E(r["id"]), E(sk), E(r.get("by", ""))))
            A("<div class=\"meta\">")
            A("<a class=\"rid\" href=\"#%s\">%s</a>" % (E(r["id"]), E(r["id"])))
            A("<span class=\"date\">%s</span>" % E(r.get("date", "")))
            A("<span class=\"who\">%s</span>" % E(r.get("by", "")))
            A("<span class=\"pill\" data-s=\"%s\">%s</span>" % (E(sk), E(sk)))
            A("</div>")
            A("<div class=\"body\">")
            A("<p class=\"ruled\">%s</p>" % E(r.get("ruled", "")))
            A("<blockquote class=\"says\">%s</blockquote>" % E(r.get("says", "")))
            A("<div class=\"extra\">")
            if r.get("governs"):
                A("<span class=\"k\">Governs</span>%s" % li(r["governs"], "paths"))
            if r.get("evidence"):
                A("<span class=\"k\">Evidence</span>%s" % li(r["evidence"], "ev"))
            A("</div>")
            if status and status.strip().upper() != sk:
                A("<p class=\"statusnote\"><span class=\"k\">Status</span>%s</p>" % E(status))
            A("</div></article>")
        A("</section>")

    A("</div></main>")
    A("<footer><div class=\"wrap\">%d rulings &middot; source sha256 %s &middot; "
      "regenerate: <code>python3 knowledge/_render_rulings.py</code> &middot; "
      "freshness: <code>python3 knowledge/_render_rulings.py --check</code></div></footer>"
      % (len(rulings), sha[:12]))
    A("<script>%s</script></body></html>" % JS)

    doc = "\n".join(P) + "\n"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(doc)
    return len(rulings), len(order), sha, len(doc.encode("utf-8"))


def check(src=SRC, out=OUT):
    if not os.path.exists(out):
        print("STALE %s missing - never generated" % out)
        return 1
    with open(out, "r", encoding="utf-8") as fh:
        head = fh.read(4096)
    m = SHA_RE.search(head)
    if not m:
        print("STALE %s carries no source-sha256 comment" % out)
        return 1
    cur = src_sha(src)
    if m.group(1) == cur:
        print("FRESH %s matches %s sha256 %s" % (os.path.basename(out), os.path.basename(src), cur))
        return 0
    print("STALE %s embeds %s but %s is now %s" % (os.path.basename(out), m.group(1),
                                                   os.path.basename(src), cur))
    return 1


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--src", default=SRC)
    ap.add_argument("--check", action="store_true",
                    help="report FRESH/STALE only; build nothing (exit 1 if STALE)")
    a = ap.parse_args()
    if a.check:
        sys.exit(check(a.src, a.out))
    n, g, sha, size = build(a.src, a.out)
    print("wrote %s  %d rulings  %d sessions  %d bytes  sha256 %s" % (a.out, n, g, size, sha))


if __name__ == "__main__":
    main()
