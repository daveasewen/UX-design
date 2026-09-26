"""Seat 304-F build. Copies the house CSS (both style blocks) and the decisions overlay from the
Apollo-MCP v2 proposal page, generates the roadmap dependency diagram (wide + tall SVG), and writes
notes/_PLAN-304-roadmap-and-weekend-runs-2026-09-26-v1.html. Run from the repo root."""
import os, html
ROOT = os.getcwd()
HERE = os.path.join(ROOT, 'notes/_lanes/304/F')
HOUSE = os.path.join(ROOT, 'notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html')
SRC = os.path.join(HERE, 'page.src.html')
OUT = os.path.join(ROOT, 'notes/_PLAN-304-roadmap-and-weekend-runs-2026-09-26-v1.html')

def rep(s, a, b):
    assert s.count(a) == 1, a[:70]
    return s.replace(a, b)

house = open(HOUSE, encoding='utf-8').read()
# house CSS: the first two <style> blocks (base + v2 additions)
i = house.index('<style>'); j = house.index('</style>', i) + 8
k = house.index('<style>', j); l = house.index('</style>', k) + 8
css = house[i:j] + '\n' + house[k:l]
# overlay: from the marker comment to the end of its script
m = house.index("<!-- ===== DAVE'S DECISIONS")
n = house.index('</script>', m) + 9
overlay = house[m:n]
overlay = rep(overlay, "page:'proposal-apollo-mcp-v2', title:'Apollo-MCP, proposal v2', path:'notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html'",
              "page:'plan-304-roadmap-v1', title:'The roadmap and the weekend runs, plan v1', path:'notes/_PLAN-304-roadmap-and-weekend-runs-2026-09-26-v1.html'")
overlay = rep(overlay, "copied from the story proposal v2 (#289) at #304", "copied from the Apollo-MCP proposal v2 (#304 lane M) by seat F")
overlay = rep(overlay, "skip:function(el){ return el.id==='tech' || el.id==='sources'; }", "skip:function(el){ return el.id==='tech'; }")

# ---------------- the diagram ----------------
# columns (time) and rows (tracks)
COLS = ['Sat night', 'Sunday', 'Monday', 'Tue 29 Sep', 'Week of 29th', 'October']
ROWS = ['Build health', 'The record', 'The pack', 'Apollo-MCP']
# id: (col, row, title, sub, kind)  kind: go (no ruling, black) | his (red edge) | ms (milestone, grey)
B = {
 'r1':  (0, 0, 'Run 1', 'CI sees to step 146', 'go'),
 'ci5': (3, 0, 'Your five CI calls', 'schema, badge, forks', 'his'),
 'cig': (4, 0, 'CI green', 'first time since 3 Sep', 'ms'),
 'r2':  (0, 1, 'Run 2', 'store tells the truth', 'go'),
 'r6':  (2, 1, 'Run 6', 'six pages for Tuesday', 'go'),
 'sit': (3, 1, 'Your sitting', 'ten calls, one hour', 'his'),
 'seat':(5, 1, 'Mac seat + ceiling', 'wraps legal again', 'ms'),
 'r3':  (1, 2, 'Run 3', 'five rulings enacted', 'go'),
 'r4':  (2, 2, 'Run 4', 'v1.0.14 candidate, scored', 'go'),
 'cut': (3, 2, 'Cut v1.0.14', 'frozen gate, your machine', 'his'),
 'flip':(4, 2, 'Blocking flips', '44px, 24px, geometry', 'his'),
 'r5':  (0, 3, 'Run 5', 'MCP catalogue probe', 'go'),
 'mcp': (3, 3, 'MCP decisions', 'its six, plus the shape', 'his'),
 'poc': (5, 3, 'MCP proof of concept', 'steps 1 to 4, then live', 'ms'),
}
# (from, to, route): row = straight along the row · L = along the source row, then down/up just before the target
# · U = drop into the gap below the source row, along it, then up into the target · V = same column, straight down
E = [('r1','r4','L'),('r2','r4','L'),('r1','ci5','row'),('r2','r6','row'),('r6','sit','row'),('r3','cut','U'),('r4','cut','row'),
     ('sit','cut','V'),('r5','mcp','row'),('mcp','poc','row'),('ci5','cig','row'),('cut','flip','row'),('sit','seat','row'),
     ('r1','r3','L'),('r2','r3','L')]

def esc(s): return html.escape(s, quote=True)

def box_style(kind):
    if kind == 'go':  return 'fill="#000" stroke="#000"', '#fff', '#D7D8D6'
    if kind == 'his': return 'fill="#fff" stroke="#DA1A00" stroke-width="1.5"', '#000', '#545454'
    return 'fill="#F3F3F3" stroke="#D7D8D6"', '#000', '#545454'

def wide():
    LX, TOP, CW, RH, W, H = 118, 44, 163, 96, 152, 58
    out = ['<svg class="wide" viewBox="0 0 1100 440" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Roadmap dependency diagram">',
           '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#767676"/></marker></defs>']
    for c, name in enumerate(COLS):
        x = LX + c*CW
        out.append('<text x="%d" y="18" font-size="12" letter-spacing="1.2" fill="#767676">%s</text>' % (x, esc(name.upper())))
        out.append('<line x1="%d" y1="26" x2="%d" y2="430" stroke="#EDEDED"/>' % (x-8, x-8))
    for r, name in enumerate(ROWS):
        y = TOP + r*RH + H/2
        out.append('<text x="0" y="%d" font-size="12" letter-spacing="1.2" fill="#767676">%s</text>' % (y+4, esc(name.upper())))
    pos = {}
    for k,(c,r,t,s,kind) in B.items():
        x = LX + c*CW; y = TOP + r*RH; pos[k] = (x,y)
    # edges first (under boxes)
    for a,b,rt in E:
        (x1,y1),(x2,y2) = pos[a],pos[b]
        sx, sy = x1+W, y1+H/2; ex, ey = x2, y2+H/2
        if rt == 'row':
            d = 'M%d,%d L%d,%d' % (sx,sy,ex,ey)
        elif rt == 'L':
            xl = ex - 10
            d = 'M%d,%d L%d,%d L%d,%d L%d,%d' % (sx,sy,xl,sy,xl,ey,ex,ey)
        elif rt == 'U':
            gy = y1 + H + (RH - H)/2; xl = ex - 10; bx = x1 + W/2
            d = 'M%d,%d L%d,%d L%d,%d L%d,%d L%d,%d' % (bx,y1+H,bx,gy,xl,gy,xl,ey,ex,ey)
        else:  # V
            d = 'M%d,%d L%d,%d' % (x1+W/2,y1+H,x2+W/2,y2)
        out.append('<path d="%s" fill="none" stroke="#767676" stroke-width="1" marker-end="url(#ah)"/>' % d)
    for k,(c,r,t,s,kind) in B.items():
        x,y = pos[k]; st, tc, sc = box_style(kind)
        out.append('<rect x="%d" y="%d" width="%d" height="%d" %s/>' % (x,y,W,H,st))
        out.append('<text x="%d" y="%d" font-size="14" font-weight="500" fill="%s">%s</text>' % (x+10,y+24,tc,esc(t)))
        out.append('<text x="%d" y="%d" font-size="12" fill="%s">%s</text>' % (x+10,y+43,sc,esc(s)))
    out.append('</svg>')
    return '\n'.join(out)

def tall():
    # one column in time order; consecutive arrows; dependencies written as text
    order = sorted(B.items(), key=lambda kv:(kv[1][0], kv[1][1]))
    deps = {}
    for a,b,_ in E: deps.setdefault(b, []).append(B[a][2])
    X, W, H, GAP = 12, 376, 74, 16
    y = 8; out_boxes = []; col_seen = None
    items = []
    for k,(c,r,t,s,kind) in order:
        if c != col_seen:
            items.append(('hdr', COLS[c], y)); y += 22; col_seen = c
        items.append(('box', (k,t,s,kind,deps.get(k,[])), y)); y += H + GAP
    total = y
    out = ['<svg class="tall" viewBox="0 0 400 %d" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Roadmap dependency diagram, narrow">' % total,
           '<defs><marker id="ah2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#767676"/></marker></defs>']
    prev = None
    for kind0, payload, yy in items:
        if kind0 == 'hdr':
            out.append('<text x="%d" y="%d" font-size="11" letter-spacing="1.2" fill="#767676">%s</text>' % (X, yy+12, esc(payload.upper())))
            continue
        k,t,s,kind,dl = payload; st, tc, sc = box_style(kind)
        if prev is not None:
            out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#D7D8D6" marker-end="url(#ah2)"/>' % (X+W/2, prev, X+W/2, yy-2))
        out.append('<rect x="%d" y="%d" width="%d" height="%d" %s/>' % (X,yy,W,H,st))
        out.append('<text x="%d" y="%d" font-size="14" font-weight="500" fill="%s">%s</text>' % (X+10,yy+22,tc,esc(t)))
        out.append('<text x="%d" y="%d" font-size="12" fill="%s">%s</text>' % (X+10,yy+42,sc,esc(s)))
        if dl:
            out.append('<text x="%d" y="%d" font-size="12" fill="%s">%s</text>' % (X+10,yy+60,sc,esc('needs ' + ', '.join(dl))))
        prev = yy + H
    out.append('</svg>')
    return '\n'.join(out)

page = open(SRC, encoding='utf-8').read()
page = rep(page, '<!--CSS-->', css)
page = rep(page, '<!--DIAG-->', wide() + '\n' + tall())
page = rep(page, '<!--OVERLAY-->', overlay)
open(OUT, 'w', encoding='utf-8').write(page)
print('wrote', OUT, len(page), 'bytes')
