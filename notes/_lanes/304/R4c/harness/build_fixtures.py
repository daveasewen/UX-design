#!/usr/bin/env python3
"""build_fixtures.py — the harness's test pages, rebuilt deterministically from pinned sources.

  good-composed.html        KNOWN GOOD (by construction, on the measured axes only): the #292 lane D
                            cold one-shot (composed with the template CLOSED — its header says so),
                            put on Common, plus a fixture layer that makes views, a theme switch, a
                            filter, search and sort WORK and PERSIST (localStorage). Taste is not claimed.
  bad-traced.html           PLANTED BAD: the pack's own Template-dashboard-bento.reference.html
                            (= a 100% trace), on the WRONG theme (supercharge), with its chart tile
                            CLIPPED by a planted max-height/overflow rule.
  good--wrong-theme.html    mutant: good with data-apollo-theme="supercharge" and nothing else.
  good--clipped-chart.html  mutant: good with the first chart's tile clipped and nothing else.
  good--no-persist.html     mutant: good with its storage writes turned into no-ops and nothing else.

Every fixture links the pack as ../pack/knowledge/… — the harness stages it with --copy-out, so the
fixture renders against whichever pack is under test (the same staging path a cold run's output takes).
"""
import hashlib, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
FIX = os.path.join(HERE, "fixtures")
GOOD_SRC = os.path.join(REPO, "notes/_lanes/292/D/overview-dashboard-oneshot-v1.html")

LAYER_TOP = """
<!-- R4C FIXTURE LAYER (harness test page, not a design) — views, theme switch, filter, search, sort, all persisted -->
<nav aria-label="Views" id="r4c-views">
  <button type="button" data-view="overview" aria-current="page">Overview</button>
  <button type="button" data-view="payments">Payments and approvals</button>
  <button type="button" data-view="settings">Settings</button>
  <button type="button" id="r4c-theme">Dark mode</button>
  <label>Entity <select id="r4c-entity" aria-label="Entity filter"><option value="all">All entities</option><option value="uk">HSBC UK</option><option value="hk">HSBC HK</option></select></label>
  <label>Search programmes <input type="search" id="r4c-search" placeholder="Search programmes"></label>
</nav>
<section data-view-panel="payments" hidden aria-label="Payments and approvals"><h2>Payments and approvals</h2>
  <table id="r4c-payments"><thead><tr><th scope="col" aria-sort="none"><button type="button" id="r4c-sort">Payee</button></th><th scope="col">Amount (GBP)</th><th scope="col">Entity</th></tr></thead><tbody>%ROWS%</tbody></table></section>
<section data-view-panel="settings" hidden aria-label="Settings"><h2>Settings</h2><p>Reporting currency GBP. Illustrative FX rates.</p></section>
"""
LAYER_SCRIPT = """
<script>/* R4C FIXTURE LAYER */
(function(){
  var S = { get: function(k){ try { return localStorage.getItem(k); } catch(e) { return null; } },
            set: function(k,v){ try { localStorage.setItem(k,v); } catch(e) {} } };
  var root = document.documentElement;
  var overview = [].slice.call(document.querySelectorAll('body > section:not([data-view-panel]), body > header, body > div'));
  function view(v){ S.set('r4c-view', v);
    [].forEach.call(document.querySelectorAll('[data-view]'), function(b){ if (b.getAttribute('data-view') === v) b.setAttribute('aria-current','page'); else b.removeAttribute('aria-current'); });
    [].forEach.call(document.querySelectorAll('[data-view-panel]'), function(p){ p.hidden = p.getAttribute('data-view-panel') !== v; });
    overview.forEach(function(e){ if (!e.contains(document.getElementById('r4c-views'))) e.hidden = v !== 'overview'; }); }
  function theme(t){ S.set('r4c-theme', t); root.setAttribute('data-theme', t); document.getElementById('r4c-theme').textContent = t === 'dark' ? 'Light mode' : 'Dark mode'; }
  function entity(v){ S.set('r4c-entity', v); document.getElementById('r4c-entity').value = v;
    [].forEach.call(document.querySelectorAll('#r4c-payments tbody tr'), function(r){ r.hidden = v !== 'all' && r.getAttribute('data-entity') !== v; }); }
  function search(q){ S.set('r4c-search', q); document.getElementById('r4c-search').value = q; q = q.toLowerCase();
    [].forEach.call(document.querySelectorAll('table tbody tr'), function(r){ if (r.closest('#r4c-payments') || r.closest('figure')) return; r.hidden = q && r.textContent.toLowerCase().indexOf(q) < 0; }); }
  function sort(dir){ S.set('r4c-sort', dir); var th = document.getElementById('r4c-sort').parentNode; th.setAttribute('aria-sort', dir);
    var tb = document.querySelector('#r4c-payments tbody'); var rows = [].slice.call(tb.rows);
    rows.sort(function(a,b){ var x = a.cells[0].textContent, y = b.cells[0].textContent; return dir === 'ascending' ? x.localeCompare(y) : y.localeCompare(x); });
    rows.forEach(function(r){ tb.appendChild(r); }); }
  [].forEach.call(document.querySelectorAll('[data-view]'), function(b){ b.addEventListener('click', function(){ view(b.getAttribute('data-view')); }); });
  document.getElementById('r4c-theme').addEventListener('click', function(){ theme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'); });
  document.getElementById('r4c-entity').addEventListener('change', function(e){ entity(e.target.value); });
  document.getElementById('r4c-search').addEventListener('input', function(e){ search(e.target.value); });
  document.getElementById('r4c-sort').addEventListener('click', function(){ sort(document.getElementById('r4c-sort').parentNode.getAttribute('aria-sort') === 'ascending' ? 'descending' : 'ascending'); });
  view(S.get('r4c-view') || 'overview'); theme(S.get('r4c-theme') || root.getAttribute('data-theme') || 'light');
  entity(S.get('r4c-entity') || 'all'); search(S.get('r4c-search') || ''); if (S.get('r4c-sort')) sort(S.get('r4c-sort'));
})();
</script>
"""
PAYEES = ["Acme Freight", "Blue Harbour", "Cedar Metals", "Delta Agri", "Eastline Power", "Fjord Shipping", "Granite Retail", "Harbor Foods",
          "Ionic Pharma", "Jade Textiles", "Kestrel Air", "Lumen Tech", "Meridian Oil", "Northgate Steel", "Orchid Hotels", "Pioneer Rail",
          "Quartz Chips", "Redwood Paper", "Summit Glass", "Tidal Energy", "Umber Mining", "Vale Logistics", "Willow Health", "Xenon Labs",
          "Yarrow Farms", "Zenith Motors", "Atlas Cement", "Beacon Media", "Crest Bank", "Dune Solar"]

def rows():
    out = []
    for i, p in enumerate(PAYEES):
        amt = "{:,}".format(12000 + (i * 7919) % 480000)
        ent = "uk" if i % 2 == 0 else "hk"
        out.append('<tr data-entity="%s"><td>%s</td><td>%s</td><td>%s</td></tr>' % (ent, p, amt, "HSBC UK" if ent == "uk" else "HSBC HK"))
    return "".join(out)

def good():
    s = open(GOOD_SRC, encoding="utf-8").read()
    s = s.replace("../../../../knowledge/", "../pack/knowledge/")
    s = s.replace('<html lang="en" class="canon" data-theme="light">', '<html lang="en" class="canon" data-apollo-theme="common" data-theme="light">', 1)
    assert 'data-apollo-theme="common"' in s
    s = s.replace("<body>", "<body>" + LAYER_TOP.replace("%ROWS%", rows()), 1)
    i = s.rindex("</body>")
    return s[:i] + LAYER_SCRIPT + s[i:]

def bad(pack_root):
    src = os.path.join(pack_root, "knowledge", "snippets", "Template-dashboard-bento.reference.html")
    s = open(src, encoding="utf-8").read()
    s = re.sub(r'(src|href)="\.\./', r'\1="../pack/knowledge/', s)
    s = s.replace('<html lang="en">', '<html lang="en" class="canon" data-apollo-theme="supercharge">', 1)
    assert 'data-apollo-theme="supercharge"' in s
    s = s.replace("</head>", '<style id="planted-clip">/* PLANTED DEFECT: the chart tile is cut off */ .c-bento__tile:has(figure.dv){max-height:150px;overflow:hidden}</style>\n</head>', 1)
    return s, src

def main():
    pack_root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.environ["HOME"], "r4c", "packs", "Apollo-Spider-v1.0.13", "Apollo-Spider-v1.0.13")
    os.makedirs(FIX, exist_ok=True)
    g = good()
    b, bsrc = bad(pack_root)
    files = {
        "good-composed.html": g,
        "bad-traced.html": b,
        "good--wrong-theme.html": g.replace('data-apollo-theme="common"', 'data-apollo-theme="supercharge"', 1),
        "good--clipped-chart.html": g.replace("</head>", '<style id="planted-clip">/* PLANTED DEFECT */ .c-bento__tile:has(#fig-spend){max-height:150px;overflow:hidden}</style>\n</head>', 1),
        "good--no-persist.html": g.replace("set: function(k,v){ try { localStorage.setItem(k,v); } catch(e) {} }", "set: function(k,v){ /* PLANTED: persistence removed */ }", 1),
    }
    for n, t in files.items():
        open(os.path.join(FIX, n), "w", encoding="utf-8").write(t)
    for n in ("good--wrong-theme.html", "good--clipped-chart.html", "good--no-persist.html"):
        assert files[n] != g, n + " mutant did not change anything"
    src = {"good_source": os.path.relpath(GOOD_SRC, REPO), "good_source_sha256": hashlib.sha256(open(GOOD_SRC, "rb").read()).hexdigest(),
           "bad_source": "pack:" + os.path.relpath(bsrc, pack_root), "bad_source_sha256": hashlib.sha256(open(bsrc, "rb").read()).hexdigest(),
           "fixtures": {n: hashlib.sha256(t.encode()).hexdigest() for n, t in files.items()}}
    json.dump(src, open(os.path.join(FIX, "SOURCES.json"), "w"), indent=1, sort_keys=True)
    print("FIXTURES", ", ".join(sorted(files)))

if __name__ == "__main__":
    main()
