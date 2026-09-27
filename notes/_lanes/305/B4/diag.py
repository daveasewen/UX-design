"""#305 B4: the skill's steps, before and now, as inline SVG (wide and tall). Steps read off the old skill
(blob ed25805c, '## Procedure') and the candidate skill (apollo-spider/skills/generate-from-canon/SKILL.md)."""
OLD = [('0 · Brief', 'which theme?'), ('1 · Find', 'search the list'), None, ('2 · Read', 'the contract'),
       ('2a · Model', 'the data'), ('3 · Compose', ''), ('4 · Gaps', ''), ('5 · Prove', 'run the gates'), ('6 · Drive', 'work controls')]
NEW = [('0 · Brief', 'which theme?'), ('1 · Ask the graph', 'the reader'), ('2 · Decide parts', 'a table, by rule'), ('3 · Read', 'the contract'),
       ('4 · Model', 'the data'), ('5 · Compose', ''), ('6 · Gaps', ''), ('7 · Prove', 'run the gates'), ('8 · Drive', 'and measure')]
NEWMARK = {1, 2}
STYLE = ('<style>.b{fill:var(--white);stroke:var(--grey-5);stroke-width:1}.bn{fill:var(--white);stroke:var(--accent);stroke-width:2.5}'
         '.gp{fill:none;stroke:var(--grey-5);stroke-dasharray:4 4}.t{fill:var(--black);font-size:13px;font-weight:500}'
         '.s{fill:var(--grey-7);font-size:12px}.h{fill:var(--grey-6);font-size:11px;letter-spacing:.12em;text-transform:uppercase}'
         '.ha{fill:var(--accent);font-size:11px;letter-spacing:.12em;font-weight:500}.ln{stroke:var(--grey-3);stroke-width:1}'
         '.rp{stroke:var(--accent);stroke-width:1.5;stroke-dasharray:3 3;fill:none}</style>')
def box(x, y, w, h, step, new=False):
    if step is None:
        return f'<rect class="gp" x="{x}" y="{y}" width="{w}" height="{h}"/><text class="s" x="{x+w/2}" y="{y+h/2+4}" text-anchor="middle">no step</text>'
    a, b = step
    out = f'<rect class="{"bn" if new else "b"}" x="{x}" y="{y}" width="{w}" height="{h}"/>'
    ty = y + (h/2 - 4 if b else h/2 + 5)
    out += f'<text class="t" x="{x+12}" y="{ty}">{a}</text>'
    if b: out += f'<text class="s" x="{x+12}" y="{ty+18}">{b}</text>'
    return out
def wide():
    W, G, H, X0 = 114, 8, 62, 16
    vw = X0*2 + 9*W + 8*G
    o = [f'<svg class="wide" viewBox="0 0 {vw} 250" role="img" aria-label="The skill steps before and now: the reader and the decision table come in as steps 1 and 2">', STYLE]
    o.append('<text class="h" x="16" y="22">Before · the v1.0.13 skill</text>')
    o.append(f'<line class="ln" x1="{X0}" y1="{36+H/2}" x2="{vw-X0}" y2="{36+H/2}"/>')
    for i, st in enumerate(OLD): o.append(box(X0 + i*(W+G), 36, W, H, st))
    o.append('<text class="ha" x="16" y="150">NOW · THE CANDIDATE SKILL (SHIPS AT THE V1.0.14 CUT)</text>')
    o.append(f'<line class="ln" x1="{X0}" y1="{164+H/2}" x2="{vw-X0}" y2="{164+H/2}"/>')
    for i, st in enumerate(NEW): o.append(box(X0 + i*(W+G), 164, W, H, st, i in NEWMARK))
    x1 = X0 + 1*(W+G) + W/2
    o.append(f'<path class="rp" d="M{x1} {36+H} L{x1} {164}"/>')
    o.append(f'<text class="s" x="{x1+6}" y="{36+H+30}">replaced</text>')
    o.append('</svg>'); return ''.join(o)
def tall():
    W, H, G, Y0 = 158, 52, 8, 44
    o = [f'<svg class="tall" viewBox="0 0 340 {Y0 + 9*(H+G) + 4}" role="img" aria-label="The skill steps before and now, in two columns">', STYLE]
    o.append('<text class="h" x="8" y="24">Before</text><text class="ha" x="182" y="24">NOW</text>')
    for i, st in enumerate(OLD): o.append(box(8, Y0 + i*(H+G), W, H, st))
    for i, st in enumerate(NEW): o.append(box(176, Y0 + i*(H+G), W, H, st, i in NEWMARK))
    o.append('</svg>'); return ''.join(o)
open('notes/_lanes/305/B4/diag-wide.svg.txt', 'w').write(wide())
open('notes/_lanes/305/B4/diag-tall.svg.txt', 'w').write(tall())
print('diagrams written')
