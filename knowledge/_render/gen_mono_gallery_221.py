# CANONICAL HOME: knowledge/_render/gen_mono_gallery_221.py (s191-D2). Writes exactly ONE file:
#   reviews/MONO-GALLERY-DEFAULT-2026-08-27-v1.html
#
# WHAT IT IS: a DECISION SURFACE for Dave's eye — #221, the mono gallery default. It RULES NOTHING.
# s220-D2 (3) leaves mono's gallery default EXPRESSLY OPEN and this page keeps it that way: the mono
# column is a CANDIDATE, a reading of Dave's conditional sentence, drawn beside the console RULED
# default and beside what mono ships today, in both modes.
#
# THE SENTENCE (Dave, 2026-08-27, conditional): "there are no rounded corners in mono but I think
# they share the same neutral ramp so the colours can be the same if this is true."
# Two premises, both VERIFIED AT BUILD TIME against the repo's own resolver — never quoted from
# memory. If either stops holding, the page renders the truth annotated instead of the claim
# ([[premise-ages-faster-than-rule]]):
#   (a) mono shares the neutral ramp — --color-neutral-5 must resolve identically in mono and
#       console (the s220-D1 CAPTION_GROUND_MINTS calibration, #313131), and every token the
#       transparent-caption treatment actually consumes must resolve identically too.
#   (b) no rounded corners in mono — --border-radius-container must resolve 0 in mono, both modes
#       (mono is the BASE theme; console's 20px is the #199 override).
#
# ⛔ NOTHING IS RE-DRAWN. Specimen markup and specimen CSS are COPIED from
# showroom/_foundations/bento-rails.html by way of the #220 banked source
# notes/_subreports/assets/2026-08-27-220-default-switch/build.py.txt — the `.cdl-` chrome names
# come WITH the copy ([[specimen-starts-from-reference]]).
#
# ⛔ NO DIAL IS TYPED. The console card reads gen_foundations_217.GALLERY_SETTINGS['console'] (the
# shipped RULED default); the mono TODAY card reads GALLERY_SETTINGS['mono'] (guarded against its
# own receipt — expressly open means it must NOT have moved); the CANDIDATE is derived: mono today
# with exactly the dial pair the console ruling names. The build REFUSES if the candidate differs
# from today on anything but capBg, or from console's ruled pair at all.
#
# ⛔ THE NOT-RULED STATUS IS MACHINE-READ, NOT ASSERTED IN PROSE. chord_refusals() returns the X6
# scope refusal for mono/gallery — identically for mono's SHIPPED state and for the candidate — so
# it is the chord scope saying "Dave's word needed", and the page quotes it verbatim.
import html as html_mod
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(REPO, 'reviews', 'MONO-GALLERY-DEFAULT-2026-08-27-v1.html')
ARTEFACT = os.path.join(REPO, 'showroom', '_foundations', 'photography.html')
RAILS_ART = os.path.join(REPO, 'showroom', '_foundations', 'bento-rails.html')
CANON_CSS = os.path.join(REPO, 'knowledge', 'canon', 'canon.css')
sys.path.insert(0, HERE)
import gen_bento_matrix_217 as matrix          # noqa: E402
import gen_bento_roles_217 as roles            # noqa: E402
import gen_foundations_217 as found            # noqa: E402

MODES = ('light', 'dark')
DAVE = ('there are no rounded corners in mono but I think they share the same neutral ramp so '
        'the colours can be the same if this is true')
PAIR_FILE = 'eyeem-100014108-180570836-w1600.jpg'
STRIP_FILES = (
    'gettyimages-1336692652-w1600.jpg',
    'gettyimages-2190197969-144dpi-w1600.jpg',
    'gettyimages-1498039805-w1600.jpg',
    'stocksy-6629948-w1600.jpg',
)


def esc(s):
    return html_mod.escape(str(s), quote=True)


# ---------------------------------------------------------------- COLOUR MATHS (copied, #220 bank)
def _srgb_lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hex2rgb(h):
    h = h.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def lum(rgb):
    r, g, b = [_srgb_lin(v) for v in rgb]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def rgbstr(h):
    r, g, b = hex2rgb(h)
    return 'rgb(%d,%d,%d)' % (r, g, b)


# ---------------------------------------------------------------- LENGTH RESOLUTION
def resolve_len(tok, theme, mode, depth=4):
    """Follow a var() chain through the theme's own parsed token table. Lengths only — colours go
    through matrix.resolve_token, which refuses non-hex by design. Returns None if dangling."""
    v = matrix.theme_tokens(theme, mode).get(tok)
    while v and v.startswith('var(') and depth > 0:
        inner = v[4:-1].split(',')[0].strip()
        v = matrix.theme_tokens(theme, mode).get(inner)
        depth -= 1
    return v


# ---------------------------------------------------------------- THE THREE STATES, DERIVED
CONSOLE = dict(found.GALLERY_SETTINGS['console'])
TODAY = dict(found.GALLERY_SETTINGS['mono'])
TODAY_REC = dict(found.RECEIPT_ROLE_DEFAULTS['gallery']['mono'])
if TODAY != TODAY_REC:
    raise SystemExit('build: mono/gallery moved (%s vs %s) — s220-D2 (3) leaves it EXPRESSLY '
                     'OPEN, so the TODAY card of this page would be wrong. Stop and look.'
                     % (TODAY, TODAY_REC))
if (CONSOLE['rounding'], CONSOLE['capBg']) != ('corners', 'transparent'):
    raise SystemExit('build: console gallery ships %s/%s — this page claims the s220-D2 RULED '
                     'default (corners/transparent) and may not misquote it.'
                     % (CONSOLE['rounding'], CONSOLE['capBg']))

CAND = dict(TODAY)
CAND.update({'rounding': CONSOLE['rounding'], 'capBg': CONSOLE['capBg']})
CAND_MOVED = sorted(d for d in CAND if CAND[d] != TODAY[d])
if CAND_MOVED != ['capBg']:
    raise SystemExit('build: the candidate differs from mono-today on %s — the reading is ONE '
                     'dial (capBg grey -> transparent; rounding is already corners). A candidate '
                     'that moves more than the reading is a different proposal.' % CAND_MOVED)

# The dial-law drive: each mono state must pass the same legality functions the #220 page drove.
REACH = matrix.capbg_for('gallery', 'mono')
for name, st in (('today', TODAY), ('candidate', CAND)):
    if st['capBg'] not in REACH:
        raise SystemExit('build: mono %s capBg %r is not reachable (%s)'
                         % (name, st['capBg'], REACH))
    if not matrix.caption_legal(st['capBg'], st['bentoBg']):
        raise SystemExit('build: mono %s refused by P2/X1' % name)
    if not matrix.capsule_legal(st['rounding'], st['capBg'], st['keylines']):
        raise SystemExit('build: mono %s refused by P3/X2' % name)

# ⛔ THE X6 SCOPE, MACHINE-READ. It must fire for BOTH mono states (it is the chord's console-only
# scope, i.e. "not ruled yet") — if it ever fires for one and not the other, or stops firing, the
# ground under this page has moved and the page must not guess at it.
REF_TODAY = matrix.chord_refusals('rounded', 'mono', 'gallery', TODAY)
REF_CAND = matrix.chord_refusals('rounded', 'mono', 'gallery', CAND)
REF_CONSOLE = matrix.chord_refusals('rounded', 'console', 'gallery', CONSOLE)
if REF_CONSOLE:
    raise SystemExit('build: the rounded chord refuses console\'s own RULED default: %s'
                     % REF_CONSOLE)
if not (REF_TODAY and REF_TODAY == REF_CAND):
    raise SystemExit('build: the X6 chord scope reads differently for mono today (%s) and the '
                     'candidate (%s) — this page quotes it as the shared NOT-RULED receipt and '
                     'may not, if they differ.' % (REF_TODAY, REF_CAND))
X6_QUOTE = REF_TODAY[0]

# ---------------------------------------------------------------- PREMISE (a) — the neutral ramp
CONSUMED = ('--color-neutral-5', '--background-default', '--text-secondary')
A_ROWS = []
A_OK = True
for tok in CONSUMED:
    for mode in MODES:
        mono_v = matrix.resolve_token(tok, 'mono', mode)
        cons_v = matrix.resolve_token(tok, 'console', mode)
        same = mono_v == cons_v
        A_OK = A_OK and same
        A_ROWS.append((tok, mode, mono_v, cons_v, same))
MINT_MONO = matrix.CAPTION_GROUND_MINTS.get(('mono', 'dark', 'darkgrey'), {})
MINT_CONS = matrix.CAPTION_GROUND_MINTS.get(('console', 'dark', 'darkgrey'), {})
MINT_SAME = (MINT_MONO.get('primitive') == MINT_CONS.get('primitive') == 'color/neutral/5')
A_OK = A_OK and MINT_SAME
SC_N5 = matrix.resolve_token('--color-neutral-5', 'supercharge', 'dark')

# ---------------------------------------------------------------- PREMISE (b) — no rounded corners
RADIUS = {}
B_OK = True
for th in ('mono', 'console'):
    for mode in MODES:
        RADIUS[(th, mode)] = resolve_len('--border-radius-container', th, mode)
for mode in MODES:
    B_OK = B_OK and (RADIUS[('mono', mode)] in ('0', '0px'))
if not all(RADIUS.values()):
    raise SystemExit('build: --border-radius-container dangles somewhere: %s' % RADIUS)

# canon.css byte-receipts — displayed on the page, and their absence is displayed too.
_canon = io.open(CANON_CSS, encoding='utf-8').read()
B_RECEIPTS = [
    ('--border-radius-default: 0;', 'the base declaration every theme inherits'),
    ('--border-radius-container: var(--border-radius-default);',
     'container radius follows the default at the base'),
    ('Mono is the base (no block)', 'the AUTO-THEMES header: mono has NO override block at all'),
    ('--border-radius-container: 20px;', 'console&rsquo;s #199 override — the rounded corner'),
]
B_RECEIPT_ROWS = [(s, why, s in _canon) for s, why in B_RECEIPTS]

# ---------------------------------------------------------------- THE ARTEFACT, ASSERTED (copied)
_art = io.open(ARTEFACT, encoding='utf-8').read()
_sel = '[data-apollo-theme="console"] ' + found.TILE
ENACTED_CSS = [
    '%s{border-radius:0;}' % _sel,
    '%s .px-open{border-radius:0; overflow:visible;}' % _sel,
    '%s .px-img{border-radius:var(--border-radius-container,0px); overflow:hidden;}' % _sel,
    '%s .px-cap{background:transparent; color:var(--text-secondary,#545454);}' % _sel,
]
_missing = [c for c in ENACTED_CSS if c not in _art]
if _missing:
    raise SystemExit('build: the enacted console rules are NOT in %s — %r. A comparison against a '
                     'stale artefact is a claim, not evidence.' % (ARTEFACT, _missing[:1]))
_rails = io.open(RAILS_ART, encoding='utf-8').read()

# ---------------------------------------------------------------- SPECIMENS (from the ledger)
ROWS, _resid = roles.read_photos()
if _resid.get('missing_derivative_file') or (_resid.get('specimen') or {}).get('missing_pinned'):
    raise SystemExit('build: the pinned specimen set is incomplete: %s' % _resid)
BY_FILE = {r['file']: r for r in ROWS}
for f in (PAIR_FILE,) + STRIP_FILES:
    if f not in BY_FILE:
        raise SystemExit('build: %s is not in the pinned s217-D1 specimen set' % f)


def tile(row):
    return ('\n      <figure class="c-bento__tile bm-tile bm-gtile " data-c="1" data-r="1" '
            'data-ragged="1,1" data-square="1,1"><span class="bm-imgbox"><img class="bm-img" '
            'src="../knowledge/assets/photography-web/%s" alt="%s" loading="lazy" width="%s" '
            'height="%s"></span><figcaption class="c-bento__caption bm-cap">'
            '<span class="bm-desc t-ed-caption">%s</span>'
            '<span class="bm-lic t-cm-legal">%s</span></figcaption></figure>\n'
            % (esc(row['file']), esc(row['desc']), row['w'] or '', row['h'] or '',
               esc(row['desc']), esc(row['licence'])))


def spec(dials, row, probe=''):
    """One live gallery specimen, driven by the explorer's own stage attributes. COPIED.
    ⛔ EVERY ATTRIBUTE COMES FROM A DIAL DICT — not one of them is a literal here."""
    return ('<div class="br-spec" data-probe="%s"><div class="bm-stage" data-type="gallery" '
            'data-page-bg="page" data-spacing="%s" data-keylines="%s" data-bento-bg="%s" '
            'data-mode="bento" data-edge="%s" data-rounding="%s" data-cap-bg="%s">'
            '<div class="bm-page-ground"><div class="bm-pane" data-pane="gallery">'
            '<div class="c-bento bm-wall bm-gallery cdl-wall" data-bento-role="gallery">'
            '<div class="c-bento__grid">%s</div></div></div></div></div></div>'
            % (probe, dials['spacing'], dials['keylines'], dials['bentoBg'], dials['edge'],
               dials['rounding'], dials['capBg'], tile(row)))


def cell(dials, mode, theme, row, probe=''):
    return ('<div class="cdl-panel" data-apollo-theme="%s">'
            '<div class="cdl-panel-bd" data-theme="%s">%s</div></div>'
            % (theme, mode, spec(dials, row, probe)))


def ground_of(word, theme, mode):
    if word == 'transparent':
        return (matrix.resolve_token('--background-default', theme, mode),
                'transparent &rarr; the page shows through')
    return (matrix.caption_ground_hex(word, theme, mode),
            matrix.caption_ground_token(word, theme, mode))


def ink_of(word, theme, mode):
    tok = matrix.ink_for(word if word != 'transparent' else 'page')
    return matrix.resolve_token(tok, theme, mode), tok


def nums(dials, theme, mode):
    g, glab = ground_of(dials['capBg'], theme, mode)
    ink, itok = ink_of(dials['capBg'], theme, mode)
    r = ratio(hex2rgb(ink), hex2rgb(g))
    rad = RADIUS.get((theme, mode)) or resolve_len('--border-radius-container', theme, mode)
    radlab = ('the picture takes the container radius, which %s resolves to <b>%s</b> &mdash; %s'
              % (theme, rad, 'square' if rad in ('0', '0px') else 'rounded'))
    rows = [
        ('Image rounding', '<b>%s</b> &mdash; %s' % (dials['rounding'], radlab)
         if dials['rounding'] == 'corners'
         else '<b>%s</b> &mdash; the whole tile rounds and clips' % dials['rounding']),
        ('Caption ground', '<b>%s</b> &middot; %s' % (dials['capBg'], glab)),
        ('What the caption sits on', '%s &middot; %s' % (rgbstr(g), g)),
        ('Caption ink', '%s &middot; %s &middot; <b>%.2f:1</b> &mdash; %s the ruled %s:1 floor'
         % (itok, rgbstr(ink), r, 'CLEARS' if r >= matrix.CONTRAST_FLOOR else 'BELOW',
            matrix.CONTRAST_FLOOR)),
    ]
    out = ['<dl class="cdl-nums">']
    for k, v in rows:
        out.append('<div class="cdl-num"><dt class="t-cm-legal">%s</dt>'
                   '<dd class="t-cm-figure-6">%s</dd></div>' % (k, v))
    out.append('</dl>')
    return ''.join(out)


def lines(items):
    return ('<ul class="cdl-lines">'
            + ''.join('<li class="t-ed-body-small">%s</li>' % i for i in items) + '</ul>')


def verdict(ok):
    return ('<span class="cdl-verdict t-cm-legal" data-ok="%s">%s</span>'
            % ('yes' if ok else 'no', 'VERIFIED AT HEAD' if ok else 'FALSE AT HEAD'))


# ---------------------------------------------------------------- CSS
CSS = r"""
/* ===========================================================================
   REVIEW PAGE — the MONO gallery default CANDIDATE. #221. RULES NOTHING.
   ⛔ THE SPECIMEN STYLES BELOW ARE COPIED, NOT RE-DRAWN. Everything between the
   COPIED-FROM-ARTEFACT markers is lifted from showroom/_foundations/bento-rails.html
   by way of the #220 banked source notes/_subreports/assets/2026-08-27-220-default-switch/
   build.py.txt, so a specimen on this page renders through exactly the rules that
   render it there. The `.cdl-` chrome names come WITH the copy.
   ⛔ EVERY var() CARRIES A LITERAL FALLBACK — a custom property that fails to resolve
   renders silent black and no gate catches it.
   ⛔ NEUTRAL HUES ONLY IN THE CHROME. No red, no yellow, no green anywhere on this page:
   the two-red law and the mono error ink camp are untouched by it.
   =========================================================================== */
html,body{margin:0;}
body{background:var(--background-default,#FFFFFF);}
.cdl{
  --page:      var(--background-default,#FFFFFF);
  --surface-2: var(--surface-subtle,#F0F0F0);  /* fallback re-derived from canon.css --surface-subtle (#221 drift-gate catch) */
  --line:      var(--border-subtle,#D7D8D6);
  --line-2:    var(--border-strong,#808080);
  --ink:       var(--text-default,#1A1A1A);
  --ink-2:     var(--text-secondary,#545454);
  --sp-1:4px; --sp-2:8px; --sp-3:12px; --sp-4:16px; --sp-5:24px; --sp-6:32px; --sp-7:48px;
  background:var(--page,#FFFFFF); color:var(--ink,#1A1A1A); -webkit-font-smoothing:antialiased;
}
.cdl *{box-sizing:border-box;}
.cdl, .cdl-head{color:var(--text-default,#1A1A1A);}

.cdl-head{padding:var(--sp-5,24px) var(--sp-6,32px); border-bottom:1px solid var(--line,#D7D8D6);}
.cdl-head h1{margin:0 0 var(--sp-2,8px);}
.cdl-head p{margin:0 0 6px; color:var(--ink-2,#545454); max-width:88ch;}
main{padding:var(--sp-6,32px); max-width:1180px;}
.cdl-sec{margin:0 0 var(--sp-7,48px); border-top:1px solid var(--line,#D7D8D6);
  padding-top:var(--sp-5,24px);}
.cdl-sec:first-of-type{border-top:0; padding-top:0;}
.cdl-sec h2{margin:0 0 var(--sp-2,8px);}
.cdl-sec h3{margin:var(--sp-5,24px) 0 var(--sp-2,8px);}
.cdl-sec p{margin:0 0 var(--sp-3,12px); color:var(--ink-2,#545454); max-width:84ch;}
.cdl-sec p b, .cdl-lines b{color:var(--ink,#1A1A1A); font-weight:500;}
.cdl-kicker{color:var(--ink-2,#545454); text-transform:uppercase; letter-spacing:0.14em;
  margin:0 0 var(--sp-2,8px); display:flex; align-items:center; gap:var(--sp-2,8px);}
.cdl-kicker::before{content:''; width:20px; height:1px; background:var(--line,#D7D8D6);}
.cdl-quote{border-left:3px solid var(--ink,#1A1A1A); padding:var(--sp-3,12px) var(--sp-4,16px);
  margin:0 0 var(--sp-3,12px); max-width:84ch;}
.cdl-quote p{margin:0; color:var(--ink,#1A1A1A);}
.cdl-quote .cdl-attrib{margin-top:6px; color:var(--ink-2,#545454);}
.cdl-note{border:1px solid var(--line,#D7D8D6); border-left-width:4px;
  padding:var(--sp-3,12px) var(--sp-4,16px); margin:var(--sp-4,16px) 0 0; max-width:84ch;}
.cdl-note p{margin:0 0 var(--sp-2,8px);}
.cdl-note p:last-child{margin:0;}
.cdl-open{border-left:3px solid var(--text-default,#1A1A1A); padding-left:var(--sp-3,12px);}
.cdl-foot{border-top:1px solid var(--line,#D7D8D6); padding-top:var(--sp-4,16px);
  color:var(--ink-2,#545454); max-width:96ch;}
.cdl-foot p{margin:0 0 var(--sp-2,8px);}
.cdl-lines{margin:0 0 var(--sp-3,12px); padding:0; list-style:none; display:flex;
  flex-direction:column; gap:6px;}
.cdl-lines li{max-width:80ch; color:var(--ink-2,#545454);}

/* ---- the premise receipts. Verdict chips are NEUTRAL — ink on page with a border, never a hue:
   a decision surface may not colour-code its own verdicts on Dave's problem hues.
   ⚠ CHROME REPAIR OVER THE COPY, seen in this page's own render: the #220 source styled its
   table <th class="t-cm-legal"> and column heads with `t-ed-heading-4` — a composite type.css does not define
   (headings run 1–4) — and bare <th class="t-cm-legal">, so both fell to the browser's serif. Specimens are
   untouched; the chrome here uses composites that exist. ---- */
.cdl-verdict{display:inline-block; border:1px solid var(--ink,#1A1A1A);
  padding:2px 8px; text-transform:uppercase; letter-spacing:0.1em;
  color:var(--ink,#1A1A1A); white-space:nowrap;}
.cdl-verdict[data-ok="no"]{background:var(--ink,#1A1A1A); color:var(--page,#FFFFFF);}
.cdl-receipt{border:1px solid var(--line,#D7D8D6); padding:var(--sp-4,16px);
  margin:0 0 var(--sp-4,16px);}
.cdl-receipt h3{margin:0 0 var(--sp-2,8px); display:flex; gap:var(--sp-3,12px);
  align-items:baseline; flex-wrap:wrap;}

/* ---- THE TRIO. Same cap discipline as the #220 pair: every `.c-bento` is
   container-type:inline-size, so canon's responsive bands answer the WALL's width. Capped at
   420px the wall lands under canon's 520px band at every viewport, so all three columns resolve
   ONE column each and are never compared across a layout band (ds-054). ---- */
.cdl-pair{display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,420px));
  gap:var(--sp-5,24px); align-items:start; margin:var(--sp-4,16px) 0;}
/* ⚠ auto-fit counts repetitions by the definite MAX track size (css-grid 7.2.3.2) — at 420px
   max a 1116px row fits TWO, and the third card of a trio wraps under the first. SEEN in this
   page's own render, then fixed: the trio caps the track at 348px so three fit at full width
   and the cap discipline (wall under canon's 520px band) is preserved. */
.cdl-trio{grid-template-columns:repeat(auto-fit,minmax(300px,348px));}
.cdl-col{margin:0; min-width:0;}
.cdl-col-hd{margin:0 0 6px; color:var(--ink,#1A1A1A);}
/* ⛔ HEIGHT-LOCKED, carried from the #220 ladder: sub-lines that wrap differently push the cards
   to different vertical origins, and a trio compared at different origins reads as three
   different cards. */
.cdl-col-sub{margin:0 0 var(--sp-2,8px); color:var(--ink-2,#545454); min-height:4em;}
.cdl-panel{border:1px solid var(--line,#D7D8D6);}
.cdl-col[data-cand="1"] .cdl-panel{border:1px dashed var(--line-2,#808080);}
.cdl-panel-bd{background:var(--background-default,#FFFFFF); color:var(--text-default,#1A1A1A);
  padding:var(--sp-3,12px);}
.cdl-panel-bd .br-spec{color:var(--text-default,#1A1A1A);}

.cdl-nums{margin:var(--sp-3,12px) 0 0; display:flex; flex-direction:column; gap:0;
  border-top:1px solid var(--line,#D7D8D6);}
/* ⛔ ROWS HEIGHT-LOCKED — same reason, one level down (the #220 fix, kept). */
.cdl-num{display:grid; grid-template-columns:minmax(120px,44%) 1fr; gap:var(--sp-3,12px);
  padding:7px 0; border-bottom:1px solid var(--line,#D7D8D6); min-height:5.2em;}
.cdl-num dt{margin:0; color:var(--ink-2,#545454); text-transform:uppercase;
  letter-spacing:0.08em;}
.cdl-num dd{margin:0; color:var(--ink,#1A1A1A); overflow-wrap:anywhere;}

/* ---- the STRIP: the candidate across more photographs. Capped at 260px the wall lands in the
   same single-column band as the trio, so nothing is compared across a responsive band. ---- */
.cdl-opts{display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,260px));
  gap:var(--sp-4,16px); align-items:start; margin:var(--sp-4,16px) 0;}
.cdl-opt{margin:0; min-width:0;}
/* ⛔ HEIGHT-LOCKED AND CLAMPED, seen in this page's own render: the four labels wrap 2–4 lines,
   so unclamped cards start at four different origins and the strip cannot be scanned as one row
   (the #220 ladder defect, one level up). Three lines, floor to match. */
.cdl-opt-cap{color:var(--ink-2,#545454); margin:0 0 6px; min-height:4.2em;
  display:-webkit-box; -webkit-line-clamp:3; -webkit-box-orient:vertical; overflow:hidden;}
.cdl-opt-tag{color:var(--ink,#1A1A1A); text-transform:uppercase; letter-spacing:0.12em;
  margin:0 0 4px;}

.cdl-table{width:100%; border-collapse:collapse; margin-top:var(--sp-3,12px);
  table-layout:fixed;}
.cdl-table th, .cdl-table td{border-bottom:1px solid var(--line,#D7D8D6);
  padding:8px 10px; text-align:left; vertical-align:top; white-space:normal;
  overflow-wrap:anywhere; color:var(--ink-2,#545454);}
.cdl-table th{color:var(--ink-2,#545454); text-transform:uppercase; letter-spacing:0.08em;
  font-weight:500;}
.cdl-table td:first-child{color:var(--ink,#1A1A1A);}
.cdl-scroll{overflow-x:auto; border:1px solid var(--line,#D7D8D6);}
.cdl-code{border:1px solid var(--line,#D7D8D6); padding:var(--sp-3,12px);
  overflow-x:auto; margin:var(--sp-3,12px) 0; color:var(--ink,#1A1A1A);}
.cdl-code pre{margin:0; white-space:pre-wrap; color:var(--ink,#1A1A1A);}

/* =====================================================================================
   COPIED-FROM-ARTEFACT START — showroom/_foundations/bento-rails.html
   (via notes/_subreports/assets/2026-08-27-220-default-switch/build.py.txt)
   ===================================================================================== */
.br-spec{border:1px solid var(--border-subtle,#D7D8D6);}
/* the specimen stage is the EXPLORER'S stage — same class, same attributes, same stylesheet. */
.br-spec .bm-stage{border:0; margin-top:0;}
.br-spec .bm-page-ground{padding:var(--sp-4,16px);}
.br-spec .bm-gtile{grid-column:span 1 !important; grid-row:span 1 !important;}

/* ---- the `--bm-*` surface the specimen stage reads. Declared on `.br-spec`, which is a CHILD
   of the element carrying the theme — substituting on a child is deterministic in every state
   probed, where substituting on the themed element itself has disagreed (measured 2026-08-22). */
.br-spec{--bm-line:var(--border-subtle,#D7D8D6); --bm-line-2:var(--border-strong,#808080);
  --bm-ink:var(--text-default,#1A1A1A); --bm-ink-2:var(--text-secondary,#545454);
  --bm-page:var(--background-default,#FFFFFF);
  --bm-grey:var(--surface-subtle,#F0F0F0);
  --bm-white:var(--surface-raised,#FFFFFF);
  --bm-darkgrey:var(--surface-digital-black,#1A1A1A);
  --bm-ink-rev:var(--text-reverse,#FFFFFF);
  --bm-radius-ctl:var(--border-radius-control,0px);
  --bm-container-radius:var(--border-radius-container,0px);}

/* ---- the stage ---- */
.bm-stage{border:1px solid var(--bm-line,#D7D8D6); margin-top:var(--sp-4,16px);}
.bm-page-ground{padding:var(--sp-5,24px);}
.bm-stage[data-page-bg="grey"] .bm-page-ground{background:var(--bm-grey,#F0F0F0);}
.bm-stage[data-page-bg="white"] .bm-page-ground{background:var(--bm-white,#FFFFFF);}
.bm-stage[data-page-bg="page"] .bm-page-ground{background:var(--bm-page,#FFFFFF);}
.bm-pane{display:none;}
.bm-stage[data-type="gallery"] .bm-pane[data-pane="gallery"]{display:block;}

/* ---- the WALL grounds ---- */
.bm-stage[data-bento-bg="grey"] .c-bento.bm-wall{background:var(--bm-grey,#F0F0F0);}
.bm-stage[data-bento-bg="white"] .c-bento.bm-wall{background:var(--bm-white,#FFFFFF);}
.bm-stage[data-bento-bg="darkgrey"] .c-bento.bm-wall{background:var(--bm-darkgrey,#1A1A1A);}
.bm-stage[data-bento-bg="transparent"] .c-bento.bm-wall{background:transparent;}
/* INK FOLLOWS THE EFFECTIVE GROUND — a transparent caption has no ground of its own, so its ink
   is the ink of the ground that actually paints behind it: the wall's. (s219-D3(2)/(5)) */
.bm-stage[data-bento-bg="darkgrey"][data-cap-bg="transparent"] .bm-cap{
  color:var(--bm-ink-rev,#FFFFFF);}

/* ---- SPACING — one declared rule per ruled stop. A value off the rail has no rule. ---- */
.bm-stage[data-spacing="40"] .c-bento.bm-wall{--bento-gutter:40px;}
/* keylines at the open spacings: a plain 1px tile border. */
.bm-stage[data-keylines="on"]:not([data-spacing="1"]) .bm-wall > .c-bento__grid > .bm-tile{
  border:1px solid var(--bm-line,#D7D8D6);}

/* ---- INSTANCE DIALS. `.c-bento.` in the selector is DELIBERATE: canon's role rules are (0,2,0),
   a bare class is (0,1,0) and the role rule would beat it — silently, in one theme, at one width. */
.c-bento.bm-gallery{--bento-columns:4; --bento-row-unit:240px;}
.c-bento.cdl-wall{--bento-columns:1; --bento-row-unit:240px;}

/* ---- tile CONTENT ---- */
.bm-tile{margin:0; display:flex; flex-direction:column; min-width:0; overflow:hidden;
  background:var(--tertiary-background-default,#FFFFFF);}
/* ⛔ A GALLERY TILE PAINTS NO GROUND, and that is what makes this whole question real. The picture
   supplies its own ground, so the CAPTION's immediate ground is the wall. */
.bm-gtile{background:transparent;}
.bm-imgbox{display:block; flex:1 1 auto; min-height:0; overflow:hidden;}
.bm-img{display:block; width:100%; height:100%; object-fit:cover;
  background:var(--surface-subtle,#F0F0F0);}
.bm-cap{padding-inline:var(--sp-3,12px); color:var(--bm-ink-2,#545454); display:flex;
  flex-direction:column; gap:2px; justify-content:center;}
.bm-desc{display:-webkit-box; -webkit-line-clamp:var(--bento-caption-lines,3);
  -webkit-box-orient:vertical; overflow:hidden;}

/* ---- CAPTION GROUNDS. The caption's IMMEDIATE ground is the tile, which takes the bento
   background — so these two are what the legality rule compares. ---- */
.bm-stage[data-cap-bg="grey"] .bm-cap{background:var(--bm-grey,#F0F0F0);}
.bm-stage[data-cap-bg="white"] .bm-cap{background:var(--bm-white,#FFFFFF);}
.bm-stage[data-cap-bg="transparent"] .bm-cap{background:transparent;}
/* THE DARK CAPTION GROUND and its reversed-out ink: two declarations, ONE decision — the second
   follows the first in the stylesheet, so a designer cannot set them inconsistently. s219-D3(3). */
.bm-stage[data-cap-bg="darkgrey"] .bm-cap{background:var(--bm-darkgrey,#1A1A1A);
  color:var(--bm-ink-rev,#FFFFFF);}
.bm-stage[data-cap-bg="grey"] .bm-cap,
.bm-stage[data-cap-bg="white"] .bm-cap{color:var(--bm-ink-2,#545454);}

/* ---- IMAGE ROUNDING (gallery). `capsule` rounds and clips the whole tile so caption and
   image are one block. Six classes/attributes because canon's gallery tile rule is (0,4,0).
   ⛔ NOTE FOR THIS PAGE: `corners` reads --border-radius-container THROUGH THE THEME — 20px under
   console, 0 under mono — so the SAME rule squares mono's corner. Nothing per-theme is added. ---- */
.bm-stage[data-rounding="corners"] .c-bento[data-bento-role="gallery"] >
  .c-bento__grid > .c-bento__tile.bm-gtile{border-radius:0; overflow:visible;}
.bm-stage[data-rounding="corners"] .c-bento[data-bento-role="gallery"] >
  .c-bento__grid > .c-bento__tile.bm-gtile .bm-imgbox{
  border-radius:var(--bm-container-radius,0px); overflow:hidden;}
.bm-stage[data-rounding="capsule"] .c-bento[data-bento-role="gallery"] >
  .c-bento__grid > .c-bento__tile.bm-gtile{
  border-radius:var(--bm-container-radius,0px); overflow:hidden;}
/* =====================================================================================
   COPIED-FROM-ARTEFACT END
   ===================================================================================== */

/* =====================================================================================
   THE ENACTED s220-D1 CAPTION MINT — emitted by gen_bento_matrix_217.caption_mint_rules() at
   build time and asserted byte-present in showroom/_foundations/bento-rails.html. No card on
   this page selects a darkgrey ground, but the copied stylesheet environment ships WITH the
   mint, and a copy that drops part of its source is a transcription.
   ===================================================================================== */
__MINT_CSS__

@media (max-width:820px){
  main{padding:var(--sp-5,24px) var(--sp-4,16px);}
}
@media (prefers-reduced-motion: reduce){
  .cdl *,.cdl *::before,.cdl *::after{transition-duration:.01ms !important;
    animation-duration:.01ms !important;}
}
"""
MINT_CSS = matrix.caption_mint_rules()
_mint_missing = [ln for ln in MINT_CSS.splitlines()
                 if ln.strip().startswith('[') and ln not in _rails]
if _mint_missing:
    raise SystemExit('build: the enacted caption mint is NOT in %s — %r'
                     % (RAILS_ART, _mint_missing[:1]))
CSS = CSS.replace('__MINT_CSS__', MINT_CSS)

BOTH_OK = A_OK and B_OK

# ---------------------------------------------------------------- BODY
P = []
w = P.append

w('<!doctype html>')
w('<html lang="en" data-apollo-theme="mono">')
w('<head>')
w('<meta charset="utf-8">')
w('<meta name="viewport" content="width=device-width, initial-scale=1">')
w('<title>Mono gallery default — CANDIDATE, not ruled</title>')
w('<!-- #221 decision surface. RULES NOTHING. The mono column is a CANDIDATE reading of '
  'Dave\'s conditional sentence; both of its premises are verified at build time against the '
  'repo\'s own resolver. Specimen markup and CSS COPIED from showroom/_foundations/'
  'bento-rails.html via the #220 banked source. -->')
w('<link rel="stylesheet" href="../knowledge/canon/type.css">')
w('<link rel="stylesheet" href="../knowledge/canon/canon.css">')
w('<style>%s</style>' % CSS)
w('</head>')
w('<body data-theme="light" class="cdl">')

w('<header class="cdl-head">')
w('<p class="cdl-kicker t-cm-legal">Apollo &middot; #221 &middot; CANDIDATE &mdash; '
  'READING OF DAVE&rsquo;S WORDS, NOT RULED</p>')
w('<h1 class="t-ed-heading-2">Mono&rsquo;s gallery default &mdash; a candidate for your eye</h1>')
w('<p class="t-ed-body">Your sentence was conditional, so this page checks the condition first '
  'and then draws what it implies: <b>square-cornered image + transparent caption</b>, beside '
  'console&rsquo;s ruled default and beside what mono ships today, in both modes. '
  '<b>Nothing here is enacted.</b> Mono&rsquo;s default stays expressly open until your word.</p>')
w('<p class="t-cm-legal">Every colour, radius and dial on this page is read out of the repo at '
  'build time. Nothing is typed. The candidate is drawn with <b>exactly the dial pair the '
  'console ruling names</b> &mdash; mono&rsquo;s own radius token is what squares the corner.</p>')
w('</header>')
w('<main>')

# ---- 1 · THE SENTENCE AND ITS TWO PREMISES ------------------------------------------------
w('<section class="cdl-sec">')
w('<p class="cdl-kicker t-cm-legal">1 &middot; What you said, checked</p>')
w('<h2 class="t-ed-heading-3">One conditional sentence, two premises, both verified</h2>')
w('<div class="cdl-quote"><p class="t-ed-body">&ldquo;%s&rdquo;</p>'
  '<p class="cdl-attrib t-cm-legal">Dave, 2026-08-27 &mdash; conditional, not a ruling</p>'
  '</div>' % DAVE)

w('<div class="cdl-receipt">')
w('<h3><span class="t-ed-heading-4">Premise A &mdash; &ldquo;they share the same neutral '
  'ramp&rdquo;</span> %s</h3>' % verdict(A_OK))
w('<p class="t-ed-body-small">Mono and console resolve <b>identical values</b> for the neutral-5 '
  'calibration point and for every token the transparent-caption treatment actually consumes, in '
  'both modes &mdash; resolved through canon&rsquo;s own cascade at build time. The s220-D1 '
  'caption mints for mono and console point at the <b>same DNA-tier primitive</b>, '
  '<code>color/neutral/5</code>%s. Supercharge is the one theme on a different ramp '
  '(<code>%s</code>, the warm swap) &mdash; mono is not.</p>'
  % (' &mdash; CONFIRMED' if MINT_SAME else ' &mdash; <b>NO LONGER TRUE</b>', SC_N5))
w('<div class="cdl-scroll"><table class="cdl-table">'
  '<thead><tr><th class="t-cm-legal">Token</th><th class="t-cm-legal">Mode</th><th class="t-cm-legal">Mono</th><th class="t-cm-legal">Console</th><th class="t-cm-legal">Same?</th></tr>'
  '</thead><tbody>')
for tok, mode, mv, cv, same in A_ROWS:
    w('<tr><td><code>%s</code></td><td class="t-cm-figure-6">%s</td>'
      '<td class="t-cm-figure-6">%s</td><td class="t-cm-figure-6">%s</td>'
      '<td class="t-cm-figure-6"><b>%s</b></td></tr>'
      % (tok, mode, mv, cv, 'SAME' if same else 'DIFFER'))
w('</tbody></table></div>')
w('</div>')

w('<div class="cdl-receipt">')
w('<h3><span class="t-ed-heading-4">Premise B &mdash; &ldquo;there are no rounded corners in '
  'mono&rdquo;</span> %s</h3>' % verdict(B_OK))
w('<p class="t-ed-body-small">Mono is the <b>base theme</b> &mdash; it has no override block in '
  'canon.css at all &mdash; and the base resolves <code>--border-radius-container</code> through '
  '<code>--border-radius-default</code> to <b>%s</b> in both modes. Console&rsquo;s <b>%s</b> is '
  'the #199 override. So the rounded-corner rule, applied unchanged in mono, draws a '
  '<b>square</b> corner: the theme&rsquo;s own token does it, no carve-out needed.</p>'
  % (RADIUS[('mono', 'light')], RADIUS[('console', 'light')]))
w('<div class="cdl-scroll"><table class="cdl-table">'
  '<thead><tr><th class="t-cm-legal">canon.css receipt</th><th class="t-cm-legal">What it says</th><th class="t-cm-legal">Present at HEAD?</th></tr>'
  '</thead><tbody>')
for s, why, present in B_RECEIPT_ROWS:
    w('<tr><td><code>%s</code></td><td class="t-ed-body-small">%s</td>'
      '<td class="t-cm-figure-6"><b>%s</b></td></tr>'
      % (esc(s), why, 'PRESENT' if present else 'ABSENT'))
w('</tbody></table></div>')
w('<p class="t-cm-legal">Resolved container radius: mono light <b>%s</b> &middot; mono dark '
  '<b>%s</b> &middot; console light <b>%s</b> &middot; console dark <b>%s</b>.</p>'
  % (RADIUS[('mono', 'light')], RADIUS[('mono', 'dark')],
     RADIUS[('console', 'light')], RADIUS[('console', 'dark')]))
w('</div>')

if BOTH_OK:
    w('<p class="t-ed-body">Both premises hold at HEAD, so the condition in your sentence is '
      'met: <b>the colours can be the same.</b> The candidate below uses no colour of its own '
      '&mdash; the same tokens, resolving to the same values, under mono&rsquo;s square '
      'corner.</p>')
else:
    w('<p class="t-ed-body"><b>At least one premise does NOT hold at HEAD</b> &mdash; the '
      'tables above carry the truth. The candidate is still drawn below, but it is built on '
      'the repo as it actually is, and the failed premise is marked where it bites.</p>')
w('</section>')

# ---- 2 & 3 · THE TRIOS -------------------------------------------------------------------
_sub_console = ('The s220-D2 RULED default: rounded-corner image (20px), caption on the page. '
                'The reference, not the question.')
_sub_cand = ('CANDIDATE &mdash; the same dial pair under mono: the radius token is 0, so the '
             'corner is square. NOT RULED. This is the question.')
_sub_today = ('What mono ships today, unruled: square image, caption on its own grey block. '
              'The before.')
PAIR_ROW = BY_FILE[PAIR_FILE]
for i, mode in enumerate(MODES):
    w('<section class="cdl-sec">')
    w('<p class="cdl-kicker t-cm-legal">%d &middot; %s mode</p>'
      % (i + 2, 'Light' if mode == 'light' else 'Dark'))
    w('<h2 class="t-ed-heading-3">%s &mdash; console&rsquo;s ruling, the mono candidate, and '
      'mono today</h2>' % ('Light' if mode == 'light' else 'Dark'))
    w('<p class="t-ed-body">Same photograph, same markup, same width. The console card and the '
      'candidate share <b>the same two dials</b> (<code>rounding: corners</code>, '
      '<code>capBg: transparent</code>); the only thing that separates them is the theme&rsquo;s '
      'radius token. The candidate and today differ on <b>one dial</b>: <code>capBg</code>.</p>')
    w('<div class="cdl-pair cdl-trio">')
    w('<figure class="cdl-col"><h3 class="cdl-col-hd t-ed-heading-4">CONSOLE &mdash; RULED '
      'DEFAULT</h3><p class="cdl-col-sub t-ed-body-small">%s</p>%s%s</figure>'
      % (_sub_console, cell(CONSOLE, mode, 'console', PAIR_ROW, 'con-%s' % mode),
         nums(CONSOLE, 'console', mode)))
    w('<figure class="cdl-col" data-cand="1"><h3 class="cdl-col-hd t-ed-heading-4">MONO &mdash; '
      'CANDIDATE, NOT RULED</h3><p class="cdl-col-sub t-ed-body-small">%s</p>%s%s</figure>'
      % (_sub_cand, cell(CAND, mode, 'mono', PAIR_ROW, 'cand-%s' % mode),
         nums(CAND, 'mono', mode)))
    w('<figure class="cdl-col"><h3 class="cdl-col-hd t-ed-heading-4">MONO &mdash; TODAY</h3>'
      '<p class="cdl-col-sub t-ed-body-small">%s</p>%s%s</figure>'
      % (_sub_today, cell(TODAY, mode, 'mono', PAIR_ROW, 'today-%s' % mode),
         nums(TODAY, 'mono', mode)))
    w('</div>')
    if mode == 'dark':
        w('<div class="cdl-note"><p class="t-ed-body-small"><b>The console card and the '
          'candidate resolve the same colours in both modes.</b> That is premise A doing the '
          'work: the caption ink and the page it sits on come from the same neutral primitives, '
          'so the only visible difference between the two cards is the corner &mdash; 20px '
          'under console, square under mono.</p></div>')
    w('</section>')

# ---- 4 · THE CANDIDATE ACROSS MORE PHOTOGRAPHS -------------------------------------------
w('<section class="cdl-sec">')
w('<p class="cdl-kicker t-cm-legal">4 &middot; The candidate, across the set</p>')
w('<h2 class="t-ed-heading-3">The same candidate on four more pinned photographs</h2>')
w('<p class="t-ed-body">A transparent caption lives or dies by what the pictures above it do, '
  'so here is the candidate on four more photographs from the ratified s217-D1 specimen set '
  '&mdash; portrait and landscape, busy bottoms and quiet ones &mdash; light row then dark '
  'row.</p>')
for mode in MODES:
    w('<h3 class="t-ed-heading-4">%s</h3>' % ('Light' if mode == 'light' else 'Dark'))
    w('<div class="cdl-opts">')
    for f in STRIP_FILES:
        r = BY_FILE[f]
        w('<figure class="cdl-opt"><p class="cdl-opt-tag t-cm-legal">CANDIDATE</p>'
          '<p class="cdl-opt-cap t-ed-body-small">%s</p>%s</figure>'
          % (esc(r['desc']),
             cell(CAND, mode, 'mono', r, 'strip-%s-%s' % (f.rsplit('.', 1)[0], mode))))
    w('</div>')
w('</section>')

# ---- 5 · WHAT WOULD MOVE, AND WHAT THE CODE SAYS ------------------------------------------
w('<section class="cdl-sec">')
w('<p class="cdl-kicker t-cm-legal">5 &middot; What would move</p>')
w('<h2 class="t-ed-heading-3">One dial &mdash; and the code already knows it is your word</h2>')
w(lines([
    '<b>capBg: grey &rarr; transparent.</b> That is the entire candidate. '
    '<code>rounding</code> is already <code>corners</code> in mono today, and with the radius '
    'token at 0 it draws square either way.',
    '<b>No per-theme carve-out is needed.</b> The candidate is console&rsquo;s ruled dial pair, '
    'unchanged; mono&rsquo;s own <code>--border-radius-container: 0</code> squares the corner '
    'through the very same rule that rounds console&rsquo;s.',
    '<b>The dial state is legal and reachable today</b> &mdash; it passes the same legality '
    'functions the #220 page drove (P2/P3, and <code>transparent</code> is in mono '
    'gallery&rsquo;s reachable set %s).' % ', '.join('<code>%s</code>' % c for c in REACH),
    '<b>If you say the word,</b> the enactment shape already exists: a supersession layer over '
    'your #219 receipt in <code>role_defaults_219.py</code>, exactly as console&rsquo;s was '
    'done &mdash; the receipt itself is never edited.',
]))
w('<div class="cdl-note"><p class="t-ed-body-small"><b>The NOT-RULED status is the '
  'code&rsquo;s, not this page&rsquo;s.</b> Asked for the rounded chord in mono gallery, the '
  'repo answers &mdash; identically for what mono ships today and for this candidate:</p>'
  '<p class="t-ed-body-small">&ldquo;%s&rdquo;</p>'
  '<p class="t-cm-legal">gen_bento_matrix_217.chord_refusals(&lsquo;rounded&rsquo;, '
  '&lsquo;mono&rsquo;, &lsquo;gallery&rsquo;, &hellip;) &mdash; read at build time</p></div>'
  % esc(X6_QUOTE))
w('</section>')

# ---- 6 · NOT DECIDED HERE ----------------------------------------------------------------
w('<section class="cdl-sec">')
w('<p class="cdl-kicker t-cm-legal">6 &middot; Not decided here</p>')
w('<h2 class="t-ed-heading-3">What this page does not settle</h2>')
w('<div class="cdl-open">')
w(lines([
    '<b>Mono&rsquo;s gallery default.</b> Expressly open (s220-D2 (3)) and still open. The '
    'candidate above is a reading of one conditional sentence, drawn for your eye. Your word '
    'rules it &mdash; this page cannot and does not.',
    '<b>The rounded chord&rsquo;s scope.</b> X6 keeps it console-only today; extending it to '
    'mono is part of the same word.',
    '<b>Everything else.</b> No token, no default, no generator, no artefact moved to make '
    'this page. Console&rsquo;s ruled default is quoted, not touched.',
]))
w('</div>')
w('</section>')

w('<div class="cdl-foot">')
w('<p class="t-cm-legal">#221 &middot; decision surface only &mdash; NOTHING ENACTED. Specimen '
  'markup and CSS copied from <code>showroom/_foundations/bento-rails.html</code> via the #220 '
  'banked source; console&rsquo;s enacted rules asserted byte-present in '
  '<code>showroom/_foundations/photography.html</code>; premises resolved through '
  '<code>gen_bento_matrix_217</code> at build time. Photographs: the pinned s217-D1 specimen '
  'set, by name.</p>')
w('</div>')
w('</main>')
w('</body></html>')

html_out = '\n'.join(P)
for bad in ('#DA1A00', '#F6604C'):
    if bad in html_out:
        raise SystemExit('build: a two-red hex (%s) appears in this page' % bad)
io.open(OUT, 'w', encoding='utf-8').write(html_out)
print('WROTE %s (%d bytes)' % (OUT, os.path.getsize(OUT)))
print('  premise A (shared neutral ramp): %s' % ('VERIFIED' if A_OK else 'FALSE AT HEAD'))
print('  premise B (no rounded corners in mono): %s' % ('VERIFIED' if B_OK else 'FALSE AT HEAD'))
print('  radii: %s' % {k: v for k, v in sorted(RADIUS.items())})
print('  candidate moves %s from today; shares %s with the console ruling'
      % (CAND_MOVED, ['capBg', 'rounding']))
print('  X6 fires identically for today and candidate: %s' % bool(REF_TODAY == REF_CAND))
