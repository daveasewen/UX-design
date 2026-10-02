#!/usr/bin/env python3
"""#315 LA: builds the audit page from audit.json (so the page cannot drift from the data) and writes the
calls and questions back into audit.json. Every quoted sentence is asserted to be a verbatim substring of
its source (the rulings store, or his #314 export) before it is printed. Read-only against the library."""
import json, os, re, html
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../../..'))
A = json.load(open(os.path.join(HERE, 'audit.json')))
RUL = {x['id']: x for x in json.load(open(os.path.join(ROOT, 'knowledge/_rulings.json')))['rulings']}
EXPORT = open(os.path.join(ROOT, 'notes/_lanes/314/DAVE-RULINGS-2026-10-02-1455-borders-switch-templates.md')).read()
OUT = os.path.join(ROOT, 'notes/_AUDIT-315-the-library-against-his-rulings-2026-10-02-v1.html')
PAGE_PATH = os.path.relpath(OUT, ROOT)

def said(src, text, who='his'):
    """who: 'his' = Dave's own words or click, quoted inside the store record; 'store' = the store's wording of the ruling"""
    hay = EXPORT if src == 'export' else (RUL[src]['ruled'] + ' ' + RUL[src].get('says', ''))
    assert text in hay, (src, text)
    return {'src': src, 'text': text, 'who': 'export' if src == 'export' else who}
LABEL = {'export': 'Your comment, Friday 2 October, 14:55', 'his': 'Your words, verbatim, as the rulings store quotes them',
         'store': 'The ruling, as the rulings store words it (not your verbatim words)'}

def rows(prefix, verdict, parts=None):
    out = [r for r in A['rows'] if r['check'].startswith(prefix) and r['verdict'] == verdict and (parts is None or r['part'] in parts)]
    assert out, (prefix, verdict, parts)
    return out

CALLS = [
 dict(id='click-ring', title='A click draws the focus ring on pages built from parts',
      words=[said('export', 'I need to impress on you that we never have a focus state unless the user is using keybord controls.')],
      rulings=['s314-D1', 's313-D71'], rows=rows('C02 ', 'break'),
      does='The parts pass on their own showroom pages. A page built from parts gets canon\'s rule that hides the ring after a click, but not the script that tells a click from a Tab: that script lives only inside each part\'s own snippet. Measured on the fenced templates: on sign-in, create and edit, and settings, clicking into a field draws the 2px blue ring; on the dashboard and list pages, the rows-per-page select does. Any built page made the same way will do the same. Two parts fail on their own too: the filter bar\'s chip remove button, and the video seek bar (the browser\'s own ring).',
      rec='Move the four-line click-or-Tab script into one shared behaviour file that every composed page loads (as the chart engine is shared), and fix the two parts: the chip\'s remove button and the seek bar get the same pointer rule the fields have.'),
 dict(id='outline-dark', title='In dark, the outline button\'s border is white while its words are soft white',
      words=[said('s313-D60', "'Yes, the ink in dark as well'")],
      rulings=['s313-D39', 's313-D60'], rows=rows('C19a', 'break'),
      does='The outline button\'s border reads one token (the strong action border), which is pure white #FFFFFF in dark. Its label reads the ink, #E1E1E1 since you softened it. So in dark the border and the words are two colours, in the button and in the five parts that carry it.',
      rec='Point the outline button\'s border at the ink, in both modes, at the token. One change; every part that binds it follows.'),
 dict(id='stat-card', title='Two parts still draw the old stat card, with the filled triangle',
      words=[said('s309-D3', "'1. Moving to metric is probably a good idea but the arrow must be the the right RAG ink'"), said('s310-D1', "'the rhin arrow from the icon assets'")],
      rulings=['s308-D42', 's309-D3', 's310-D1'], rows=rows('C11 ', 'break'),
      does='The stat-led hero and the stats band still compose the stat card\'s own drawing (and the band one KPI tile), with the filled triangle arrow, not Metric with the thin direction arrow.',
      rec='Rebuild both on Metric (its with-trend and without-trend readings). Then the Stat-card snippet has nothing left that needs it (question 8).'),
 dict(id='own-buttons', title='Eight parts draw their own primary button instead of using the button',
      words=[said('ds-032', "'if these are just all buttons from different components they should all be using the one button atom to build from.")],
      rulings=['ds-032', 's314-D28'], rows=rows('C20', 'break'),
      does='Action bar, confirmation, drawer, empty state, hero, the hero variants, modals and the confirm pop-up each repaint the primary button with their own copy of its rules. Most bind the button\'s own tokens, so they look the same today, but each copy can drift, and the empty state\'s already has: its hover is its own mix (70% of the fill), not the button\'s hover. Finding 7 on this afternoon\'s page named the empty state with the confirmation; only the confirmation was fixed.',
      rec='One lane moves the eight onto the button part (the empty state first, because its hover already differs), and brings you a before/after picture of each that changes.'),
 dict(id='nav-icon', title='Four navs keep the outline icon on the current page',
      words=[said('s262-D3', "its icon switches to the library's selected (-active) variant", 'store')],
      rulings=['s262-D3'], rows=rows('C18 ', 'break'),
      does='The side nav and the plain tab bar swap to the filled icon on the current page (the top nav\'s items have no icon). The side nav copied into three app shells (side nav, nav rail, multi-column) does not swap, and nor does the tab bar\'s floating island.',
      rec='Give the three app shells the side nav\'s two-icon swap, and the island the same swap the plain tab bar has.'),
 dict(id='toast', title='Toasts stack; your rule is one at a time',
      words=[said('s272-D25', 'assert exactly one toast node in the live region', 'store')],
      rulings=['s272-D25'], rows=rows('C07 ', 'break'),
      does='Each new toast is added to the live region and none is removed, so two in a row stack.',
      rec='A new toast replaces the one on screen (or waits until it leaves). The words "one at a time" go in the toast\'s rule so the check can read them.'),
 dict(id='download-link', title='Two parts still download from a link',
      words=[said('s272-D2', 'Links navigate only. A download becomes a button, and document-row / links / footer all change.', 'store')],
      rulings=['s272-D2'], rows=rows('C06', 'break'),
      does='The links part shows "download your statement (PDF)" as a link and as an icon link. The document row\'s second form makes the whole row a download link. The footer is clean.',
      rec='Show downloads as buttons: drop the download examples from the links part, and make the document row\'s second form a button row (or drop it; it is marked proposed).'),
 dict(id='apollo-copy', title='Three parts say Apollo in product copy',
      words=[said('s261-D8', "Any copy a user of the product can read says HSBC; 'Apollo' names the design system in OUR record and must not surface as product copy in a snippet, a showroom page or a review pane.", 'store')],
      rulings=['s261-D8'], rows=rows('C10', 'break'),
      does='"See how Apollo can work for your business" (call to action), "Apollo\'s own products" (feature grid, twice), and "© 2026 Apollo" plus "Apollo is the reference implementation…" (the big footer).',
      rec='HSBC in all five places, matching the app footer\'s "© HSBC Group 2026. All rights reserved."'),
 dict(id='help-wrap', title='Help text still wraps in four places',
      words=[said('export', "The help text, it shouldn't wrap and tbh you have elaborated too much here, the text should be short if you neeed extra information wrap it up in a help popover, tooltip or something")],
      rulings=['s314-D11'], rows=rows('C14', 'break'),
      does='Measured at 1280px in the cloud: the form layout\'s sort-code help, the tags field\'s help, and one line each on the sign-in and settings pages run to two lines. Create and edit, the page you named, is clean now.',
      rec='Cut each to one line and put the rest behind the field\'s help tip. And say yes to the drafted rule (question 12) so the check holds every field to it, not one page.'),
 dict(id='rail-label', title='The side nav rail\'s hover label floats with no edge',
      words=[said('s313-D58', "'only the mega menu has a border on the bottom edge because it bleeds off the edge anyway, the rest of the floating surfaces all have borders all round'")],
      rulings=['s313-D58'], rows=rows('C01', 'break'),
      does='When the side nav is a rail, hovering a row floats its label beside it with a shadow and no border at all. The tooltip and the rail flyout both have the edge.',
      rec='Give the label the floating edge all round, as the tooltip has.'),
 dict(id='rest-word', title='Eleven part trees still call the rest state "default"',
      words=[said('s313-D18', "'Each part's own word, initial names it'")],
      rulings=['s313-D18'], rows=rows('C16a', 'break'),
      does='Accordion, button, date picker, dropdown, text input, notification, pagination, slider, table, tabs and tooltip all start at "default". Modals and the split button already say "closed", the switch "off", the checkbox "unchecked", Metric "ready".',
      rec='Proposed words, for you to strike: accordion collapsed · date picker closed · dropdown closed · tooltip hidden · tabs and pagination the first tab or page selected · button, text input, slider, table and notification rest (no better word comes from their markup). Set when the cohort is ratified, as you said.'),
 dict(id='tag-words', title='Four trees still name pieces by their tag',
      words=[said('s313-D17', "'Plain words, set by hand per part'")],
      rulings=['s313-D17'], rows=rows('C16b', 'break'),
      does='Pagination calls its pieces ul, li, li-2, li-3 and a; the notification has strong, span and a; the accordion a span; tabs a p. Your yes to the pagination tree was given on its "words are plain".',
      rec='Plain words, by hand: pagination list, controls item, page item, gap item, page link; notification title, body, link; accordion marker; tabs panel text.'),
 dict(id='folded-parts', title='Three parts you folded into others still stand as their own parts',
      words=[said('s308-D6', "'Rework: Slider's two-handle form'"), said('s307-D51', "'Make the transaction row a variant of list items; show me the other eight as pictures'"), said('s308-D4', "'Rework: a variant of list items'")],
      rulings=['s308-D6', 's307-D51', 's308-D4'], rows=rows('C21', 'break'),
      does='The range slider, the transaction row and the standing order row each keep their own meta and snippet and still offer themselves for a role (input, record list), so a build can still pick them. The range slider\'s merge is drafted; the two rows wait on the list-items variants.',
      rec='Until each merge lands, take the role off the three so nothing new is built on them; the merges stay on their open rows.'),
]

QUESTIONS = [
 dict(id='q-active-bar', title='Is a field\'s own active bar a focus state?', rulings=['s314-D1'], rows=rows('C03', 'unclear'),
      q='Clicking into a text field draws its active bar (the 4px line under it) in 16 parts. Is that the focus state you said should never show without the keyboard, or is it the field saying "you are typing here"?',
      rec='Keep the bar: it marks where your words will go, not where the keyboard is.', opts=['Keep the bar', 'Keyboard only, like the ring']),
 dict(id='q-alpha', title='Does "state changes only" reach dimmed text?', rulings=['ds-026', 's305-D11'], rows=rows('C05', 'unclear'),
      q='Your September rule keeps transparency for state changes. In Common the muted labels became a solid grey, but in the other three themes 82 parts still dim labels, captions and notes with transparency. Should those take a solid ink too?',
      rec='Yes, a solid secondary ink in every theme, one part at a time, starting with the labels you read most (Metric, side nav, data grid).', opts=['Yes, solid ink everywhere', 'Common only, as now']),
 dict(id='q-float-buttons', title='Do floating buttons and edge sheets carry the floating edge?', rulings=['s313-D58'], rows=rows('C01', 'unclear'),
      q='The floating add button and back to top float with a shadow and no edge. The drawer and the overlay side nav are sheets fixed to the screen edge, like the mega menu (one inner edge, or none). The tab bar\'s island uses the divider grey, visible in light. Which of these count as floating surfaces?',
      rec='Sheets fixed to an edge keep their inner edge only, like the mega menu; floating buttons and the island take the floating edge all round.', opts=['As recommended', 'All of them all round']),
 dict(id='q-auth-frame', title='Does the sign-in page carry the frame?', rulings=['s314-D21', 's272-D92'], rows=rows('C13a', 'unclear'),
      q='You said every page template carries the app frame. Your September rule for sign-in says "navigation = absent". The page has no masthead and no footer. Which wins?',
      rec='No navigation, but keep the footer: the legal line belongs on every page.', opts=['No nav, keep the footer', 'No frame at all', 'Full frame']),
 dict(id='q-settings-words', title='What are the amended settings words?', rulings=['s314-D20', 's272-D91'], rows=rows('C13g', 'unclear'),
      q='You chose "sections sit on rules; the settings wording is amended". The rule still reads "sections are grouped on card surfaces"; the new words were drafted, not given. Take the draft?',
      rec='Take it: "sections sit on rules as named regions, never on card surfaces".', opts=['Take the draft', 'My own words (comment)']),
 dict(id='q-template-when', title='Do the template choice rules still matter?', rulings=['s272-D86', 's272-D87', 's272-D88', 's272-D89', 's272-D90', 's272-D91', 's272-D92', 's272-D84'], rows=rows('C13h', 'unclear'),
      q='In September you ratified a rule for when each page template is the right one. Eight of the ten fenced templates carry none on their meta. Since builds now ignore templates, do they need them?',
      rec='Keep the rules, for designers choosing an example; a build never reads them.', opts=['Keep them for designers', 'Drop them']),
 dict(id='q-pending', title='The pending roundel or the chip?', rulings=['s314-D15', 's314-D26'], rows=rows('C22', 'unclear'),
      q='The confirmation part now carries the amber pending roundel (your call 15 comment). Your call 26 click said no pending kind, the chip carries it. Which stays?',
      rec='The amber roundel, as the conductor recommended at #314.', opts=['The amber roundel', 'The chip only']),
 dict(id='q-stat-card', title='Retire the stat card\'s drawing?', rulings=['s309-D3'], rows=rows('C11 ', 'unclear'),
      q='Once the hero and the stats band move to Metric (call 3), nothing needs the Stat-card drawing. Retire it, keeping the name as an alias?',
      rec='Retire the drawing; the alias keeps resolving to Metric.', opts=['Retire the drawing', 'Keep it']),
 dict(id='q-range-calendar', title='Does the date range picker use the calendar too?', rulings=['s307-D49'], rows=rows('C21', 'unclear'),
      q='You said the date picker uses the calendar part. The date range picker still draws its own month grid. Same rule?',
      rec='Yes: one calendar, with a range mode.', opts=['Yes, one calendar', 'No']),
 dict(id='q-legend-note', title='Can a showroom note name Apollo?', rulings=['s261-D8'], rows=rows('C10', 'unclear'),
      q='The legend\'s showroom note says "the only round components in Apollo". It explains the system, it is not product copy, but your rule reaches "a showroom page". Change it?',
      rec='Change it to "in this library".', opts=['Change it', 'Leave it']),
 dict(id='q-tick-dark', title='What colour is the big tick in dark?', rulings=['s313-D61', 's313-D35'], rows=rows('C19b', 'unclear'),
      q='In dark the confirmation tick is pure white, which is neither the ink your click named ("The big tick follows") nor the green your comment kept ("confirmations can stay green"), and you asked for its own review page. Until then, which?',
      rec='Leave it until its own review page; build that page.', opts=['Wait for its page', 'The ink now', 'Green now']),
 dict(id='q-help-rule', title='The help text rule, drafted for you', rulings=['s314-D11'], rows=rows('C14', 'break'),
      q='Drafted at #314 from your call 11: "Help text under a field is one short line and never wraps at the field\'s width. Anything longer goes behind the field\'s help tip or a popover the field opens." Take it as the rule for every field?',
      rec='Take it.', opts=['Take it', 'My own words (comment)']),
]
COSMETIC = [r for r in A['rows'] if r['verdict'] == 'cosmetic']

def esc(s): return html.escape(str(s), quote=True)
def parts_of(rs): return sorted({r['part'] for r in rs})
def ev_li(rs, n=14):
    seen, out = set(), []
    for r in rs:
        for e in r['evidence']:
            if e in seen: continue
            seen.add(e); out.append('<li><code>%s</code> <span class="pn">%s</span></li>' % (esc(e), esc(r['part'])))
    more = len(out) - n
    return ''.join(out[:n]) + ('<li>… and %d more in audit.json</li>' % more if more > 0 else '')

def chips(opts, rec):
    b = []
    for i, o in enumerate(opts):
        b.append('<button type="button" class="chip" data-v="%s">%s%s</button>' % (esc(o), esc(o), '<em>Recommended</em>' if i == 0 else ''))
    b.append('<button type="button" class="chip" data-v="None of these (comment)">None of these (say below)</button>')
    return ''.join(b)

def call_html(c, n, kind):
    words = ''.join('<p class="quote">“%s”<small>%s</small></p>' % (esc(w['text'].strip("'")), LABEL[w['who']]) for w in c.get('words', []))
    rs = c['rows']; ps = parts_of(rs)
    if kind == 'break':
        opts = ['Fix it as recommended', 'Leave it as it is']
        body = ('<p class="q">%s</p>%s<div class="facts"><p><b>What the source does.</b> %s</p><p class="pl"><b>Parts (%d):</b> %s</p></div>'
                '<p class="rec">Recommended: %s</p>') % (esc(c['title']), words, esc(c['does']), len(ps), esc(', '.join(ps)), esc(c['rec']))
        rec = 'Fix it as recommended'
    else:
        opts = c['opts']
        body = '<p class="q">%s</p><p class="lead2">%s</p><p class="pl"><b>Parts (%d):</b> %s</p><p class="rec">Recommended: %s</p>' % (esc(c['title']), esc(c['q']), len(ps), esc(', '.join(ps[:30]) + (' …' if len(ps) > 30 else '')), esc(c['rec']))
        rec = opts[0]
    tech = '<details class="tech"><summary>Technical</summary><ol><li>Rulings: %s.</li>%s</ol></details>' % (
        esc(' · '.join('%s (%s)' % (r, RUL[r]['status'].split(' ')[0].strip(' —').lower()) for r in c['rulings'])),
        '<li>Evidence (file:line):<ul class="ev">%s</ul></li>' % ev_li(rs))
    return ('<div class="call" data-id="%s" data-q="%s" data-rec="%s"><p class="cnum">%s %d</p>%s<div class="chips">%s</div>'
            '<label class="field"><span>Your comment</span><textarea data-f="note"></textarea></label><div class="stamp"></div>%s</div>') % (
        esc(c['id']), esc(('%d. %s' if kind == 'break' else 'Q%d. %s') % (n, c['title'])), esc(rec), 'Break' if kind == 'break' else 'Question', n, body, chips(opts, rec), tech)

C = A['counts']['by_verdict']
breaks_n = sum(len(c['rows']) for c in CALLS)
assert breaks_n == C['break'], (breaks_n, C['break'])
unclear_n = sum(len(c['rows']) for c in QUESTIONS if c['id'] != 'q-help-rule')
assert unclear_n == C['unclear'], (unclear_n, C['unclear'])
inv = A['inventory']
CSS = open(os.path.join(ROOT, 'notes/_REVIEW-314-the-borders-the-switch-family-the-templates-2026-10-02-v1.html')).read()
CSS = CSS[CSS.index('<style>') + 7: CSS.index('</style>')]
CSS += """
.facts p{font-size:15px;line-height:1.6;color:var(--g8);margin:0 0 .6rem}
.facts b,.pl b{font-weight:500;color:var(--fg)}
.pl{font-size:13px;color:var(--g7);margin:0 0 var(--s2)}
.lead2{font-size:16px;line-height:1.6;color:var(--g8);max-width:44em}
.pn{color:var(--g6);font-size:12px;margin-left:.4rem}
ul.ev{list-style:none;padding:0;margin:.4rem 0 0}
ul.ev li{margin:0 0 4px}
.sumt td.n{font-variant-numeric:tabular-nums;text-align:right;width:7em}
.call .quote{font-size:16px;margin:0 0 var(--s2)}
"""
cos_li = ''.join('<li><b>%s</b>: %s <code>%s</code></li>' % (esc(r['part']), esc(r['note'][:220]), esc(r['evidence'][0])) for r in COSMETIC)
glance = ''.join('<tr><td class="n">%d</td><td><a href="#%s">%s</a></td><td class="n">%d</td></tr>' % (i + 1, c['id'], esc(c['title']), len(parts_of(c['rows']))) for i, c in enumerate(CALLS))
calls_html = ''.join(call_html(c, i + 1, 'break') for i, c in enumerate(CALLS))
q_html = ''.join(call_html(c, i + 1, 'q') for i, c in enumerate(QUESTIONS))
NOTCHECKED = [
 'Hit areas (the 44px target) and contrast pairs: render-measured gates already own them; not re-run here.',
 'The tooltip on an icon-only button (September rule, option 2): the store keeps "option 2" but not the option\'s words, so there was nothing to check against.',
 'The other three themes\' overrides: dark checks read the base theme (Mono) and each snippet\'s own dark values; Common, Console and Supercharge overrides were not traced.',
 'The showroom generator (its theme picker labels and its focus token): it is not a part.',
 'The bento dashboard and the wizard: parked or owed to their own lanes, so recorded as not judged.',
 'About 275 other rulings that govern parts but say nothing visible or structural that a grep or a parse can test (records, graph edges, chart engine internals, release and process rulings).',
]
nc = ''.join('<li>%s</li>' % esc(x) for x in NOTCHECKED)
SCRIPT = CSS_SCRIPT = open(os.path.join(ROOT, 'notes/_REVIEW-314-the-borders-the-switch-family-the-templates-2026-10-02-v1.html')).read()
SCRIPT = SCRIPT[SCRIPT.index('<script>') + 8: SCRIPT.index('</script>')]
SCRIPT = SCRIPT.replace("review-314-borders-switch-templates-v1", "audit-315-library-v1").replace(
    "notes/_REVIEW-314-the-borders-the-switch-family-the-templates-2026-10-02-v1.html", PAGE_PATH).replace(
    "Session 314 · The borders, the switch family, the templates · comments", "# Session 315 · The library against your rulings · answers").replace(
    "review-314-borders-switch-templates.txt", "audit-315-library-answers.md").replace("{type:'text/plain'}", "{type:'text/markdown'}").replace(
    "Exported as a text file", "Exported as a markdown file").replace(
    "      L.push(el.dataset.q);", "      L.push('## '+el.dataset.q);")
SCRIPT = SCRIPT.replace("var asked=calls.filter(function(el){ return el.dataset.id!=='page'; });", "var asked=calls;")
# the glance table here is static; drop the 314 page's generated one
SCRIPT = re.sub(r"  // the at-a-glance table.*?\n  \}\);\n", "  var tb={children:[]};\n", SCRIPT, flags=re.S)
assert 'audit-315-library-v1' in SCRIPT and PAGE_PATH in SCRIPT
page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Library against rulings</title>
<style>{CSS}</style>
</head><body>
<nav class="toc"><div class="wrap">
  <a href="#summary">Summary</a><a href="#breaks">Breaks</a><a href="#questions">Your questions</a><a href="#cosmetic">Small things</a><a href="#notchecked">Not checked</a>
</div></nav>
<header id="top">
  <div class="wrap grid">
    <div>
      <p class="label">Session 315 · audit page · The library against your rulings</p>
      <h1>Every part read against what you ruled. {len(CALLS)} things break a ruling; {len(QUESTIONS)} need your word.</h1>
      <p class="sub">Each break has a recommended fix, which is a recommendation, not a ruling. Click once, or say more in the box.</p>
    </div>
    <div class="meta">
      <span>Friday 2 October 2026, late evening</span>
      <span>Read from the tree at 853d7f56. Nothing in the library was changed.</span>
      <span>Two checks were renders in the cloud (a click on every control; every help line measured). The rest are reads of the source, with the file and line.</span>
      <span>Your words are quoted from the rulings store or your #314 answers, never retold.</span>
    </div>
  </div>
</header>
<section id="summary">
  <div class="wrap">
    <p class="label">At a glance</p>
    <h2>{inv['metas']} parts, {len(A['rulings_checked'])} rulings, {A['counts']['rows']} checks.</h2>
    <div class="scroll"><table class="ctab sumt"><tbody>
      <tr><td>Parts in the library (metas)</td><td class="n">{inv['metas']}</td></tr>
      <tr><td>Parts with their own snippet</td><td class="n">{inv['snippets']}</td></tr>
      <tr><td>Rulings checked (of {inv['rulings_in_store']} in the store)</td><td class="n">{len(A['rulings_checked'])}</td></tr>
      <tr><td>Checks run (part × ruling)</td><td class="n">{A['counts']['rows']}</td></tr>
      <tr><td><b>Breaks a ruling</b>, in {len(CALLS)} calls below</td><td class="n">{C['break']}</td></tr>
      <tr><td><b>Unclear</b>, in {len(QUESTIONS) - 1} questions below (question {len(QUESTIONS)} is a drafted rule)</td><td class="n">{C['unclear']}</td></tr>
      <tr><td>Small things (cosmetic)</td><td class="n">{C['cosmetic']}</td></tr>
      <tr><td>Clean</td><td class="n">{C['clean']}</td></tr>
      <tr><td>Not judged (parked or owed to their own lane)</td><td class="n">{C['not-judged']}</td></tr>
    </tbody></table></div>
    <div class="scroll"><table class="ctab"><thead><tr><th>#</th><th>The break</th><th>Parts</th></tr></thead><tbody>{glance}</tbody></table></div>
  </div>
</section>
<section id="breaks" class="grey">
  <div class="wrap">
    <p class="label">01–{len(CALLS):02d} · Where the source breaks a ruling</p>
    <h2>{len(CALLS)} breaks, most-felt first. Each says what the part does, where, and a fix.</h2>
    {calls_html}
  </div>
</section>
<section id="questions">
  <div class="wrap">
    <p class="label">Your questions · where the rulings leave it open</p>
    <h2>Where your words do not settle it, the question is yours.</h2>
    {q_html}
  </div>
</section>
<section id="cosmetic" class="grey">
  <div class="wrap">
    <p class="label">Small things · no call needed</p>
    <h2>{len(COSMETIC)} small things a fixing lane can pick up.</h2>
    <ul class="plain">{cos_li}</ul>
  </div>
</section>
<section id="notchecked">
  <div class="wrap">
    <p class="label">What this audit did not check</p>
    <h2>A check that found nothing is not proof of absence. These were not checked at all.</h2>
    <ul class="plain">{nc}</ul>
  </div>
</section>
<footer><div class="wrap">Session 315 · {PAGE_PATH} · built by lane LA from notes/_lanes/315/LA/audit.json (build_page.py). Report: notes/_subreports/2026-10-02-315-LA.md.</div></footer>
<div class="bar" role="region" aria-label="Your decisions"><div class="in">
  <b>Your decisions</b><span id="count">0 answered</span><span class="msg" id="msg">Saves in this browser as you go</span>
  <button type="button" class="pri" id="copy">Copy as text</button><button type="button" id="export">Export</button><button type="button" id="clear">Clear</button>
</div></div>
<script>{SCRIPT}</script>
</body></html>
"""
open(OUT, 'w').write(page)
A['calls'] = [{'n': i + 1, 'id': c['id'], 'title': c['title'], 'rulings': c['rulings'], 'his_words': c.get('words', []), 'parts': parts_of(c['rows']),
               'what_the_source_does': c['does'], 'recommendation': c['rec'], 'evidence': sorted({e for r in c['rows'] for e in r['evidence']})} for i, c in enumerate(CALLS)]
A['questions'] = [{'n': i + 1, 'id': c['id'], 'title': c['title'], 'rulings': c['rulings'], 'question': c['q'], 'recommendation': c['rec'], 'parts': parts_of(c['rows'])} for i, c in enumerate(QUESTIONS)]
json.dump(A, open(os.path.join(HERE, 'audit.json'), 'w'), indent=1, ensure_ascii=False)
print('page', PAGE_PATH, len(page), 'bytes; calls', len(CALLS), 'questions', len(QUESTIONS), 'break rows', breaks_n, 'unclear rows', unclear_n)
