#!/usr/bin/env python3
"""build_page.py — lane H3 (#313, cloud) — writes the Assembly / Studio proposal page.

Output: notes/_PROPOSAL-313-H3-assembly-and-studio-2026-10-01-v1.html
Inputs it draws from (read, not copied): notes/_lanes/312/H/H1/FINDINGS.md (the matrix research),
notes/_lanes/312/H/H2/PROPOSAL-modes-2026-10-01.md and calls.json (the modes proposal), the F review
page (the decisions bar: copy, export, clear, saves in the browser) and the #280 contact sheet's shots.

Run from the repo root: PYTHONDONTWRITEBYTECODE=1 python3 notes/_lanes/313/H3/build_page.py
Pure stdlib; writes one file; nothing under knowledge/ is touched.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "notes" / "_PROPOSAL-313-H3-assembly-and-studio-2026-10-01-v1.html"
KEY = "proposal-313-H3-assembly-and-studio-v1"
PATH = "notes/_PROPOSAL-313-H3-assembly-and-studio-2026-10-01-v1.html"

# ----------------------------------------------------------------------------- drawings

def wire(kind, col, w=220, h=140):
    """A dashboard wireframe for one matrix cell. kind: bands | tiles | feed; col: counts | items."""
    g = []
    g.append(f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" fill="var(--card)" stroke="var(--g3)"/>')
    g.append(f'<rect x="10" y="10" width="{w-20}" height="10" fill="var(--g2)"/>')  # page header
    g.append(f'<rect x="10" y="26" width="70" height="6" fill="var(--g3)"/>')        # filters
    y0 = 40
    if kind == "bands":
        bh = (h - y0 - 10 - 2 * 6) / 3
        for i in range(3):
            y = y0 + i * (bh + 6)
            g.append(f'<rect x="10" y="{y:.1f}" width="{w-20}" height="{bh:.1f}" fill="none" stroke="var(--g3)"/>')
            g.append(f'<rect x="16" y="{y+5:.1f}" width="46" height="5" fill="var(--g5)"/>')  # band title
            if col == "counts":
                g.append(f'<text x="16" y="{y+bh-6:.1f}" font-size="14" font-weight="500" fill="var(--fg)" font-family="Helvetica,Arial,sans-serif">{[7,3,12][i]}</text>')
                g.append(f'<rect x="60" y="{y+bh-12:.1f}" width="{w-80}" height="4" fill="var(--g3)"/>')
            else:
                for r in range(2):
                    ry = y + 14 + r * 8
                    g.append(f'<rect x="16" y="{ry:.1f}" width="{w-32}" height="4" fill="var(--g3)"/>')
                    g.append(f'<rect x="{w-30}" y="{ry-1:.1f}" width="12" height="6" fill="var(--accent)" opacity=".7"/>')
    elif kind == "tiles":
        cols, rows = 3, 2
        tw = (w - 20 - (cols - 1) * 6) / cols
        th = (h - y0 - 10 - (rows - 1) * 6) / rows
        for r in range(rows):
            for c in range(cols):
                x = 10 + c * (tw + 6); y = y0 + r * (th + 6)
                g.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{tw:.1f}" height="{th:.1f}" fill="none" stroke="var(--g3)"/>')
                g.append(f'<rect x="{x+5:.1f}" y="{y+5:.1f}" width="{tw*0.5:.1f}" height="4" fill="var(--g5)"/>')
                if col == "counts":
                    g.append(f'<text x="{x+5:.1f}" y="{y+th-7:.1f}" font-size="13" font-weight="500" fill="var(--fg)" font-family="Helvetica,Arial,sans-serif">{[7,3,12,4,2,9][r*cols+c]}</text>')
                else:
                    for k in range(2):
                        g.append(f'<rect x="{x+5:.1f}" y="{y+14+k*7:.1f}" width="{tw-10:.1f}" height="3" fill="var(--g3)"/>')
    elif kind == "feed":
        y = y0
        for h_i in range(3):
            g.append(f'<rect x="10" y="{y}" width="40" height="5" fill="var(--g5)"/>'); y += 9
            for r in range(2):
                g.append(f'<rect x="10" y="{y}" width="{w-20}" height="4" fill="var(--g3)"/>')
                if col == "items":
                    g.append(f'<rect x="{w-24}" y="{y-1}" width="12" height="6" fill="var(--accent)" opacity=".7"/>')
                y += 8
            y += 4
    return f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-hidden="true">{"".join(g)}</svg>'


def cell(kind, col, tag="", note="", struck=False):
    cls = "mcell" + (" struck" if struck else "") + (" rec" if tag.startswith("Recommended") else "")
    tagh = f'<span class="mtag">{tag}</span>' if tag else ""
    strike = '<span class="mstrike" aria-hidden="true"></span>' if struck else ""
    colname = {"counts": "Counts first", "items": "Items first"}[col]
    return f'<div class="{cls}"><span class="mcol">{colname}</span>{tagh}<div class="mwire">{wire(kind, col)}{strike}</div><p class="mnote">{note}</p></div>'


def svg_engine():
    """One engine, two laws."""
    return """
<svg viewBox="0 0 960 470" width="100%" role="img" aria-labelledby="eng-t">
<title id="eng-t">One engine in the middle, Assembly on the left where a red stops the build, Studio on the right where a red becomes a label; promotion runs from Studio back to Assembly on your word, and three named triggers move work from Assembly into Studio.</title>
<g font-family="Helvetica Neue,Helvetica,Arial,sans-serif">
<text x="480" y="16" text-anchor="middle" font-size="11" fill="var(--g7)">into Studio on three named triggers only: the brief leaves decisions open · a gate refuses · you ask in words</text>
<path d="M290 86 C290 22, 670 22, 670 86" fill="none" stroke="var(--g7)" stroke-dasharray="5 4" marker-end="url(#ah)"/>
<g transform="translate(0,46)">
<!-- engine -->
<rect x="360" y="40" width="240" height="250" fill="var(--g1)" stroke="var(--g3)"/>
<text x="480" y="30" text-anchor="middle" font-size="11" letter-spacing="1.5" fill="var(--g6)">ONE ENGINE · SAME IN BOTH</text>
<rect x="380" y="60" width="200" height="54" fill="var(--card)" stroke="var(--g3)"/><text x="480" y="83" text-anchor="middle" font-size="15" fill="var(--fg)">Canon</text><text x="480" y="102" text-anchor="middle" font-size="11" fill="var(--g6)">tokens · snippets · metas</text>
<rect x="380" y="128" width="200" height="54" fill="var(--card)" stroke="var(--g3)"/><text x="480" y="151" text-anchor="middle" font-size="15" fill="var(--fg)">Gates</text><text x="480" y="170" text-anchor="middle" font-size="11" fill="var(--g6)">every one runs in both modes</text>
<rect x="380" y="196" width="200" height="54" fill="var(--card)" stroke="var(--g3)"/><text x="480" y="219" text-anchor="middle" font-size="15" fill="var(--fg)">The record</text><text x="480" y="238" text-anchor="middle" font-size="11" fill="var(--g6)">a place, not a mode · your word writes it</text>
<!-- assembly -->
<rect x="30" y="40" width="270" height="250" fill="var(--card)" stroke="var(--fg)" stroke-width="1.5"/>
<text x="165" y="30" text-anchor="middle" font-size="11" letter-spacing="1.5" fill="var(--fg)">APOLLO ASSEMBLY · THE DEFAULT</text>
<text x="50" y="72" font-size="13" fill="var(--g7)">What a red does</text>
<circle cx="62" cy="96" r="6" fill="var(--accent)"/><rect x="78" y="90" width="150" height="12" fill="var(--fg)"/><text x="153" y="100" text-anchor="middle" font-size="10" fill="var(--bg)" letter-spacing="1">STOP · THE BUILD FAILS</text>
<text x="50" y="136" font-size="13" fill="var(--g7)">What the output is</text>
<rect x="50" y="146" width="90" height="60" fill="var(--g1)" stroke="var(--g3)"/><rect x="58" y="154" width="74" height="6" fill="var(--g3)"/><rect x="58" y="166" width="74" height="30" fill="var(--g2)"/>
<text x="152" y="166" font-size="13" fill="var(--fg)">Canon. Shippable.</text><text x="152" y="184" font-size="11" fill="var(--g6)">one recommended output</text>
<text x="50" y="236" font-size="13" fill="var(--g7)">Where it may live</text>
<text x="50" y="256" font-size="12" fill="var(--fg)">The resolving stores and the ship set.</text>
<!-- studio -->
<rect x="660" y="40" width="270" height="250" fill="var(--card)" stroke="var(--fg)" stroke-width="1.5" stroke-dasharray="6 4"/>
<text x="795" y="30" text-anchor="middle" font-size="11" letter-spacing="1.5" fill="var(--fg)">APOLLO STUDIO · ON A TRIGGER</text>
<text x="680" y="72" font-size="13" fill="var(--g7)">What a red does</text>
<circle cx="692" cy="96" r="6" fill="var(--accent)"/><rect x="708" y="90" width="206" height="12" fill="none" stroke="var(--accent)"/><text x="811" y="100" text-anchor="middle" font-size="10" fill="var(--accent)" letter-spacing="1">LABEL · THE GATE'S OWN WORDS</text>
<text x="680" y="136" font-size="13" fill="var(--g7)">What the output is</text>
<rect x="680" y="146" width="80" height="60" fill="var(--g1)" stroke="var(--g3)" stroke-dasharray="3 3"/><rect x="688" y="154" width="64" height="6" fill="var(--g3)"/><rect x="688" y="166" width="30" height="30" fill="var(--g2)"/><rect x="722" y="166" width="30" height="30" fill="none" stroke="var(--accent)" stroke-dasharray="2 2"/>
<text x="770" y="166" font-size="11" fill="var(--fg)">A proposal, marked not-canon</text><text x="770" y="184" font-size="11" fill="var(--g6)">many, each wearing its reds</text>
<text x="680" y="236" font-size="13" fill="var(--g7)">Where it may live</text>
<text x="680" y="256" font-size="12" fill="var(--fg)">Outside the stores: the proposals folders,</text><text x="680" y="272" font-size="12" fill="var(--fg)">the promotion queue, the matrix pages.</text>
<!-- engine feeds both -->
<line x1="360" y1="165" x2="302" y2="165" stroke="var(--g7)" marker-end="url(#ah)"/>
<line x1="600" y1="165" x2="658" y2="165" stroke="var(--g7)" marker-end="url(#ah)"/>
<!-- promotion: studio -> assembly (solid red, under) -->
<path d="M795 290 C795 380, 165 380, 165 290" fill="none" stroke="var(--accent)" stroke-width="1.5" marker-end="url(#ahr)"/>
<text x="480" y="334" text-anchor="middle" font-size="12" fill="var(--accent)" font-weight="500">back to Assembly by promotion only</text>
<text x="480" y="384" text-anchor="middle" font-size="11" fill="var(--g7)">what crosses is a ruling, on your word, through the one sanctioned inscriber · the Studio file never crosses · Assembly re-composes from what was promoted</text>
</g></g></svg>"""


def svg_door_lever():
    def frame(x0, title, body, rec=False):
        stroke = "var(--accent)" if rec else "var(--g3)"
        return (f'<rect x="{x0}" y="20" width="300" height="190" fill="var(--card)" stroke="{stroke}" stroke-width="{1.5 if rec else 1}"/>'
                f'<text x="{x0+14}" y="42" font-size="11" letter-spacing="1.5" fill="{"var(--accent)" if rec else "var(--g6)"}">{title}</text>' + body)
    # door
    door = ('<circle cx="60" cy="110" r="5" fill="var(--fg)"/>'
            '<line x1="65" y1="110" x2="110" y2="110" stroke="var(--g7)"/>'
            '<path d="M110 110 L160 70" stroke="var(--g7)" fill="none" marker-end="url(#ah)"/><path d="M110 110 L160 150" stroke="var(--g7)" fill="none" marker-end="url(#ah)"/>'
            '<rect x="165" y="58" width="110" height="24" fill="var(--g1)" stroke="var(--g3)"/><text x="220" y="74" text-anchor="middle" font-size="11" fill="var(--fg)">Assembly</text>'
            '<rect x="165" y="138" width="110" height="24" fill="var(--g1)" stroke="var(--g3)" stroke-dasharray="3 3"/><text x="220" y="154" text-anchor="middle" font-size="11" fill="var(--fg)">Studio</text>'
            '<text x="30" y="190" font-size="11" fill="var(--g7)">You choose before the brief is read.</text>')
    lever = ('<circle cx="380" cy="110" r="5" fill="var(--fg)"/>'
             '<line x1="385" y1="110" x2="600" y2="110" stroke="var(--fg)" stroke-width="1.5"/>'
             '<text x="470" y="98" font-size="11" fill="var(--fg)">Assembly, always</text>'
             '<path d="M490 110 L520 150 L600 150" stroke="var(--g7)" fill="none" stroke-dasharray="3 3" marker-end="url(#ah)"/>'
             '<text x="528" y="166" font-size="11" fill="var(--g7)">Studio, when asked</text>'
             '<text x="350" y="190" font-size="11" fill="var(--g7)">No front door; one switch, pulled by hand.</text>')
    both = ('<circle cx="660" cy="110" r="5" fill="var(--fg)"/>'
            '<line x1="665" y1="110" x2="690" y2="110" stroke="var(--g7)"/>'
            '<path d="M705 95 L720 110 L705 125 L690 110z" fill="var(--g1)" stroke="var(--g7)"/><text x="705" y="88" text-anchor="middle" font-size="9" fill="var(--g6)">the brief</text>'
            '<line x1="720" y1="110" x2="925" y2="110" stroke="var(--fg)" stroke-width="1.5"/>'
            '<text x="728" y="99" font-size="10" fill="var(--fg)">Assembly · default</text>'
            '<text x="925" y="99" text-anchor="end" font-size="9" fill="var(--g7)">a gate refuses · you ask</text>'
            '<path d="M705 125 L705 155 L905 155" stroke="var(--g7)" fill="none" stroke-dasharray="3 3"/>'
            '<path d="M870 110 L885 155" stroke="var(--g7)" fill="none" stroke-dasharray="3 3"/>'
            '<text x="712" y="172" font-size="9" fill="var(--g7)">two decisions left open → Explore offered</text>'
            '<text x="925" y="168" text-anchor="end" font-size="9" fill="var(--fg)">Studio</text>'
            '<path d="M915 155 L915 118" stroke="var(--accent)" stroke-width="1.5" fill="none" marker-end="url(#ahr)"/>'
            '<text x="928" y="195" text-anchor="end" font-size="11" fill="var(--g7)">Back only by promotion, in red.</text>')
    return ('<svg viewBox="0 0 960 230" width="100%" role="img" aria-label="Three drawings: a door chosen before the brief, a lever pulled mid-work, and both together with Assembly the default">'
            '<g font-family="Helvetica Neue,Helvetica,Arial,sans-serif">'
            + frame(20, "A · DOOR ONLY", door) + frame(330, "B · LEVER ONLY", lever) + frame(640, "C · BOTH · RECOMMENDED", both, rec=True) +
            '</g></svg>')


def svg_mark():
    return '''
<svg viewBox="0 0 960 300" width="100%" role="img" aria-label="A Studio page carries its mode in the provenance receipt and on its root; the receipt gate refuses it in Assembly and lists its unhashed regions in Studio">
<g font-family="Helvetica Neue,Helvetica,Arial,sans-serif">
<!-- the page -->
<rect x="30" y="20" width="400" height="260" fill="var(--card)" stroke="var(--g3)"/>
<text x="46" y="44" font-size="11" letter-spacing="1.5" fill="var(--g6)">THE PAGE, AS A FILE</text>
<text x="46" y="70" font-family="Menlo,Consolas,monospace" font-size="12" fill="var(--fg)">&lt;html data-apollo-theme="console"</text>
<text x="46" y="88" font-family="Menlo,Consolas,monospace" font-size="12" fill="var(--accent)" font-weight="500">      data-apollo-mode="studio"&gt;</text>
<rect x="46" y="102" width="368" height="150" fill="var(--g1)" stroke="var(--g3)"/>
<text x="58" y="122" font-family="Menlo,Consolas,monospace" font-size="11" fill="var(--g7)">#provenance-receipt</text>
<text x="58" y="140" font-family="Menlo,Consolas,monospace" font-size="11" fill="var(--fg)">pack    v1.0.14</text>
<text x="58" y="156" font-family="Menlo,Consolas,monospace" font-size="11" fill="var(--accent)" font-weight="500">mode    studio          ← one new field</text>
<text x="58" y="178" font-family="Menlo,Consolas,monospace" font-size="11" fill="var(--fg)">region  top-nav      sha256 3f9a…  hashed</text>
<text x="58" y="194" font-family="Menlo,Consolas,monospace" font-size="11" fill="var(--fg)">region  kpi-row      sha256 b1c0…  hashed</text>
<text x="58" y="210" font-family="Menlo,Consolas,monospace" font-size="11" fill="var(--fg)">region  exposure     sha256 77de…  hashed</text>
<text x="58" y="226" font-family="Menlo,Consolas,monospace" font-size="11" fill="var(--accent)" font-weight="500">region  approvals    —              proposal: "no canon list fits"</text>
<text x="46" y="272" font-size="11" fill="var(--g6)">The hash rows exist today. The mode field and the unhashed kind are the proposal.</text>
<!-- gate reading it, two laws -->
<line x1="432" y1="150" x2="500" y2="150" stroke="var(--g7)" marker-end="url(#ah)"/>
<text x="468" y="138" text-anchor="middle" font-size="10" fill="var(--g6)">the receipt gate</text>
<rect x="510" y="40" width="420" height="100" fill="var(--card)" stroke="var(--fg)" stroke-width="1.5"/>
<text x="526" y="62" font-size="11" letter-spacing="1.5" fill="var(--fg)">READ IN ASSEMBLY</text>
<circle cx="534" cy="92" r="6" fill="var(--accent)"/><text x="548" y="96" font-size="13" fill="var(--fg)">Refused: a studio-marked page cannot ship.</text>
<text x="548" y="118" font-size="11" fill="var(--g6)">One branch in a gate that already parses the receipt.</text>
<rect x="510" y="160" width="420" height="120" fill="var(--card)" stroke="var(--fg)" stroke-width="1.5" stroke-dasharray="6 4"/>
<text x="526" y="182" font-size="11" letter-spacing="1.5" fill="var(--fg)">READ IN STUDIO</text>
<rect x="528" y="200" width="12" height="12" fill="none" stroke="var(--accent)"/><text x="548" y="211" font-size="13" fill="var(--fg)">Lists the unhashed regions, by name, with the reason.</text>
<text x="548" y="232" font-size="11" fill="var(--g6)">Nothing hidden; the page says on its face which parts are canon.</text>
<text x="548" y="262" font-size="11" fill="var(--g6)">The mark a custom glyph carries today, widened to regions.</text>
</g></svg>'''


def svg_switch():
    gates = [("receipt", "g"), ("compose", "g"), ("icons", "r"), ("a11y", "g"), ("geometry", "r"), ("tokens", "n"), ("snippets", "g")]
    def column(x0, title, studio):
        out = [f'<text x="{x0}" y="42" font-size="11" letter-spacing="1.5" fill="var(--fg)">{title}</text>']
        y = 70
        stopped = False
        for name, v in gates:
            col = {"g": "var(--g5)", "r": "var(--accent)", "n": "var(--g3)"}[v]
            out.append(f'<text x="{x0}" y="{y+4}" font-size="12" fill="{"var(--g5)" if stopped else "var(--fg)"}">{name}</text>')
            if v == "n" and stopped:
                out.append(f'<circle cx="{x0+110}" cy="{y}" r="6" fill="var(--g3)"/><text x="{x0+126}" y="{y+4}" font-size="11" fill="var(--g5)">never ran</text>')
            elif v == "n":
                out.append(f'<circle cx="{x0+110}" cy="{y}" r="6" fill="none" stroke="var(--g6)"/><line x1="{x0+106}" y1="{y-4}" x2="{x0+114}" y2="{y+4}" stroke="var(--g6)"/><line x1="{x0+114}" y1="{y-4}" x2="{x0+106}" y2="{y+4}" stroke="var(--g6)"/>')
                out.append(f'<text x="{x0+126}" y="{y+4}" font-size="11" fill="var(--g7)">could not ask · a refusal in both modes</text>')
            elif v == "g":
                out.append(f'<circle cx="{x0+110}" cy="{y}" r="6" fill="{"var(--g3)" if stopped else col}"/>')
                if stopped: out.append(f'<text x="{x0+126}" y="{y+4}" font-size="11" fill="var(--g5)">never ran</text>')
            else:
                out.append(f'<circle cx="{x0+110}" cy="{y}" r="6" fill="{"var(--g3)" if stopped else col}"/>')
                if not studio and not stopped:
                    out.append(f'<rect x="{x0+126}" y="{y-7}" width="150" height="14" fill="var(--fg)"/><text x="{x0+201}" y="{y+4}" text-anchor="middle" font-size="10" fill="var(--bg)" letter-spacing="1">STOP · EXIT 1</text>')
                    stopped = True
                elif studio:
                    out.append(f'<rect x="{x0+126}" y="{y-7}" width="290" height="14" fill="none" stroke="var(--accent)"/><text x="{x0+132}" y="{y+4}" font-size="10" fill="var(--accent)">label → receipt: "{ {"icons": "glyph not in the library, line 212", "geometry": "part 3 off its own size by 6px"}[name] }"</text>')
            y += 26
        if studio:
            out.append(f'<text x="{x0}" y="{y+14}" font-size="12" fill="var(--fg)">exit 0 · the page comes back wearing two labels</text>')
        else:
            out.append(f'<text x="{x0}" y="{y+14}" font-size="12" fill="var(--fg)">exit 1 · the page does not come back</text>')
        return "".join(out)
    return ('<svg viewBox="0 0 960 300" width="100%" role="img" aria-label="The same seven gates run twice: in Assembly the first red stops the run; in Studio every gate runs and each red becomes a label written into the receipt; a gate that could not ask refuses in both">'
            '<g font-family="Helvetica Neue,Helvetica,Arial,sans-serif">'
            '<rect x="20" y="20" width="440" height="270" fill="var(--card)" stroke="var(--fg)" stroke-width="1.5"/>'
            '<rect x="490" y="20" width="450" height="270" fill="var(--card)" stroke="var(--fg)" stroke-width="1.5" stroke-dasharray="6 4"/>'
            + column(40, "RUN-GATES · ASSEMBLY (TODAY'S ONLY LAW)", False) + column(510, "RUN-GATES --MODE STUDIO (PROPOSED)", True) +
            '</g></svg>')


def svg_promotion():
    return '''
<svg viewBox="0 0 960 345" width="100%" role="img" aria-label="Three picks with sentences on the same axis become a candidate ruling on a review page; your word makes it law; Assembly reads the law, never the picks">
<g font-family="Helvetica Neue,Helvetica,Arial,sans-serif">
<text x="30" y="30" font-size="11" letter-spacing="1.5" fill="var(--g6)">STUDIO · EXPLORE</text>
<rect x="30" y="44" width="150" height="90" fill="var(--card)" stroke="var(--g3)" stroke-dasharray="4 3"/><text x="105" y="66" text-anchor="middle" font-size="12" fill="var(--fg)">matrix · brief 1</text><rect x="46" y="76" width="118" height="40" fill="var(--g1)"/><rect x="86" y="80" width="36" height="32" fill="none" stroke="var(--accent)" stroke-width="1.5"/><text x="105" y="126" text-anchor="middle" font-size="10" fill="var(--g7)">pick: three bands · "in this order"</text>
<rect x="200" y="44" width="150" height="90" fill="var(--card)" stroke="var(--g3)" stroke-dasharray="4 3"/><text x="275" y="66" text-anchor="middle" font-size="12" fill="var(--fg)">matrix · brief 2</text><rect x="216" y="76" width="118" height="40" fill="var(--g1)"/><rect x="256" y="80" width="36" height="32" fill="none" stroke="var(--accent)" stroke-width="1.5"/><text x="275" y="126" text-anchor="middle" font-size="10" fill="var(--g7)">pick: three bands · a sentence</text>
<rect x="370" y="44" width="150" height="90" fill="var(--card)" stroke="var(--g3)" stroke-dasharray="4 3"/><text x="445" y="66" text-anchor="middle" font-size="12" fill="var(--fg)">matrix · brief 3</text><rect x="386" y="76" width="118" height="40" fill="var(--g1)"/><rect x="426" y="80" width="36" height="32" fill="none" stroke="var(--accent)" stroke-width="1.5"/><text x="445" y="126" text-anchor="middle" font-size="10" fill="var(--g7)">pick: three bands · a sentence</text>
<text x="275" y="160" text-anchor="middle" font-size="11" fill="var(--g7)">each pick is a row in the picks file: axis · value · the cells it beat · your sentence, or "click"</text>
<!-- to candidate -->
<path d="M275 168 L275 190" stroke="var(--g7)" marker-end="url(#ah)"/>
<rect x="100" y="196" width="340" height="56" fill="var(--card)" stroke="var(--fg)"/><text x="275" y="218" text-anchor="middle" font-size="12" fill="var(--fg)">a candidate ruling on a review page</text><text x="275" y="238" text-anchor="middle" font-size="11" fill="var(--g6)">"dashboards default to three bands" · the three picks as its evidence</text>
<path d="M440 224 L470 224" stroke="var(--g7)" marker-end="url(#ah)"/>
<rect x="480" y="196" width="130" height="56" fill="var(--accent)"/><text x="545" y="228" text-anchor="middle" font-size="13" fill="#fff" font-weight="500">your word</text>
<path d="M610 224 L660 224" stroke="var(--g7)" marker-end="url(#ah)"/>
<rect x="670" y="196" width="260" height="56" fill="var(--g1)" stroke="var(--fg)" stroke-width="1.5"/><text x="800" y="218" text-anchor="middle" font-size="12" fill="var(--fg)">law · the ruling store</text><text x="800" y="238" text-anchor="middle" font-size="11" fill="var(--g6)">through the one sanctioned inscriber, as today</text>
<text x="800" y="30" font-size="11" letter-spacing="1.5" fill="var(--g6)" text-anchor="middle">ASSEMBLY</text>
<rect x="670" y="44" width="260" height="90" fill="var(--card)" stroke="var(--fg)" stroke-width="1.5"/><text x="800" y="70" text-anchor="middle" font-size="12" fill="var(--fg)">Compose reads the law</text><text x="800" y="90" text-anchor="middle" font-size="11" fill="var(--g6)">three bands becomes its default</text><text x="800" y="110" text-anchor="middle" font-size="11" fill="var(--g6)">it never reads the picks file</text>
<path d="M800 196 L800 142" stroke="var(--g7)" marker-end="url(#ah)"/>
<!-- the barred shortcut -->
<path d="M520 90 L665 90" stroke="var(--g5)" stroke-dasharray="3 3"/><line x1="590" y1="78" x2="602" y2="102" stroke="var(--accent)" stroke-width="2"/><line x1="602" y1="78" x2="590" y2="102" stroke="var(--accent)" stroke-width="2"/>
<text x="592" y="70" text-anchor="middle" font-size="10" fill="var(--g7)">a pick never walks straight in</text>
<!-- the direct path for one output -->
<text x="30" y="290" font-size="11" letter-spacing="1.5" fill="var(--g6)">THE OTHER PATH · ONE OUTPUT, NO RULING</text>
<text x="30" y="310" font-size="12" fill="var(--fg)">The picked cell is itself a page: it goes to Assembly's Adapt or Check as an output with a pick behind it, and the gates block from there.</text><text x="30" y="328" font-size="12" fill="var(--fg)">One pick changes one output at once; the law changes only by accumulation and your word.</text>
</g></svg>'''


def svg_order():
    steps = [("1", "The mark", "one field in the receipt, one attribute on the root, one branch in the receipt gate"),
             ("2", "The switch", "a mode flag on the pack's runner; the tier carried in the manifest"),
             ("3", "The rename", "on-canon → Assembly, freestyle → Studio in the contract; the projections regenerate"),
             ("4", "The thin skills", "Adapt, Sketch, Hand off: each a page, none needed for the modes to be real"),
             ("5", "Explore", "the matrix: axis finder, renderer, picks file, promotion page · the first live test is the CEO overview")]
    out = ['<svg viewBox="0 0 960 190" width="100%" role="img" aria-label="Build order if every call goes your way: the mark, the switch, the rename, the thin skills, then Explore"><g font-family="Helvetica Neue,Helvetica,Arial,sans-serif">',
           '<line x1="40" y1="50" x2="800" y2="50" stroke="var(--g3)"/>']
    for i, (n, t, d) in enumerate(steps):
        x = 40 + i * 190
        out.append(f'<circle cx="{x}" cy="50" r="14" fill="{"var(--accent)" if i < 2 else "var(--card)"}" stroke="var(--fg)" stroke-width="1.5"/>')
        out.append(f'<text x="{x}" y="55" text-anchor="middle" font-size="12" fill="{"#fff" if i < 2 else "var(--fg)"}" font-weight="500">{n}</text>')
        out.append(f'<text x="{x-14}" y="90" font-size="14" fill="var(--fg)">{t}</text>')
        words = d.split(); lines, cur = [], ""
        for w in words:
            if len(cur) + len(w) > 30: lines.append(cur); cur = w
            else: cur = (cur + " " + w).strip()
        lines.append(cur)
        for j, ln in enumerate(lines):
            out.append(f'<text x="{x-14}" y="{110+j*15}" font-size="11" fill="var(--g7)">{ln}</text>')
    out.append('<text x="40" y="24" font-size="11" letter-spacing="1.5" fill="var(--g6)">SMALLEST FENCE FIRST · THE TWO IN RED MAKE THE MODES REAL; THE REST ARE SKILLS</text>')
    out.append('</g></svg>')
    return "".join(out)


# ----------------------------------------------------------------------------- the calls

def call(cid, n, title, q, rec, chips, rec_chip=None):
    rec_chip = rec_chip or rec
    ch = []
    for c in chips:
        em = "<em>Recommended</em>" if c == rec_chip else ""
        v = c if c != "None of these (say below)" else "None of these (comment)"
        ch.append(f'<button type="button" class="chip" data-v="{v}">{c}{em}</button>')
    return f'''
    <div class="call" data-id="{cid}" data-q="{n}. {title}" data-rec="{rec}">
      <p class="q">{q}</p>
      <p class="rec">Recommended: {rec}.</p>
      <div class="chips">{"".join(ch)}</div>
      <label class="field"><span>Your comment</span><textarea data-f="note"></textarea></label>
      <div class="stamp"></div>
    </div>'''


# ----------------------------------------------------------------------------- the page

CSS = r'''
:root{--accent:#DA1A00;--fg:#000;--bg:#fff;--g1:#F3F3F3;--g2:#EDEDED;--g3:#D7D8D6;--g5:#9B9B9B;--g6:#767676;--g7:#545454;--g8:#333;--card:#fff;--code:#F3F3F3;
  --s1:.5rem;--s2:1rem;--s3:1.5rem;--s4:2rem;--s5:3rem;--s6:4rem;--s7:6rem;--max:1180px}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--accent:#FF6A55;--fg:#F2F2F2;--bg:#0E0E0E;--g1:#1A1A1A;--g2:#262626;--g3:#3A3A3A;--g5:#8A8A8A;--g6:#A3A3A3;--g7:#BDBDBD;--g8:#D6D6D6;--card:#141414;--code:#1F1F1F}}
:root[data-theme="dark"]{--accent:#FF6A55;--fg:#F2F2F2;--bg:#0E0E0E;--g1:#1A1A1A;--g2:#262626;--g3:#3A3A3A;--g5:#8A8A8A;--g6:#A3A3A3;--g7:#BDBDBD;--g8:#D6D6D6;--card:#141414;--code:#1F1F1F}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:16px;line-height:1.7;color:var(--fg);background:var(--bg);-webkit-font-smoothing:antialiased;overflow-x:hidden;padding-bottom:64px}
.wrap{max-width:var(--max);margin:0 auto;padding:0 32px}
.label{font-size:12px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);display:flex;gap:10px;align-items:center;margin:0 0 var(--s3);line-height:1.5}
.label::before{content:"";width:20px;height:1px;background:var(--accent);flex:none}
p{margin:0 0 var(--s2)}
code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.86em;background:var(--code);padding:.08em .35em;overflow-wrap:anywhere}
nav.toc{position:sticky;top:0;z-index:50;background:var(--bg);border-bottom:1px solid var(--g2)}
nav.toc .wrap{display:flex;gap:var(--s2);align-items:center;height:52px;overflow-x:auto;scrollbar-width:none;padding-left:200px}
nav.toc .wrap::-webkit-scrollbar{display:none}
nav.toc a{font-size:13px;letter-spacing:.04em;color:var(--g6);text-decoration:none;white-space:nowrap}
nav.toc a:hover{color:var(--fg)}
header{padding:var(--s6) 0 var(--s5);border-bottom:1px solid var(--g2)}
header .grid{display:grid;grid-template-columns:2fr 1fr;gap:var(--s5);align-items:end}
h1{font-size:57px;font-weight:200;line-height:1.06;margin:0}
.sub{font-size:24px;font-weight:300;line-height:1.4;margin:var(--s3) 0 0;max-width:30em}
.meta{font-size:13px;line-height:1.7;color:var(--g7)}
.meta span{display:block}
h2{font-size:34px;font-weight:300;line-height:1.18;margin:0 0 var(--s3)}
section{padding:var(--s6) 0;border-bottom:1px solid var(--g2)}
section.grey{background:var(--g1)}
.lead{font-size:21px;font-weight:300;line-height:1.5;max-width:34em}
.lead a,.facts a,.sub3 a{color:inherit}
.fig{margin:var(--s3) 0 var(--s2);background:var(--card);border:1px solid var(--g3);padding:var(--s2)}
section.grey .fig{background:var(--card)}
.fig svg{display:block;max-width:100%}
.fig figcaption{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--g6);line-height:1.5;margin-top:var(--s1)}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--g3);border:1px solid var(--g3);margin:var(--s3) 0 var(--s2)}
.pair.three{grid-template-columns:1fr 1fr 1fr}
.pair figure{margin:0;background:var(--card);padding:var(--s2);display:flex;flex-direction:column;gap:var(--s1);min-width:0}
.pair figcaption{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--g6);line-height:1.5}
.pair img{display:block;width:100%;height:auto;border:1px solid var(--g2);background:#fff}
.pair a{display:block}
.facts{margin:var(--s3) 0 0;padding:0;list-style:none}
.facts li{display:grid;grid-template-columns:150px 1fr;gap:var(--s3);padding:var(--s2) 0;border-top:1px solid var(--g3);font-size:15px;line-height:1.6;color:var(--g8)}
.facts li:last-child{border-bottom:1px solid var(--g3)}
.facts .k{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--g6);line-height:1.5;padding-top:3px}
.facts li b{font-weight:500;color:var(--fg)}
.call{border:1px solid var(--g3);background:var(--card);padding:var(--s3);margin-top:var(--s3)}
.call .q{font-size:21px;font-weight:300;line-height:1.35;margin:0 0 var(--s1)}
.call .rec{font-size:14px;color:var(--g7);margin:0 0 var(--s2)}
.chips{display:flex;gap:.4rem;flex-wrap:wrap;margin-bottom:var(--s2)}
.chip{font:inherit;font-size:12px;letter-spacing:.06em;padding:.5rem .8rem;border:1px solid var(--g3);background:var(--bg);color:var(--g8);cursor:pointer;border-radius:0;text-align:left;line-height:1.35}
.chip:hover{border-color:var(--fg);color:var(--fg)}
.chip.on{background:var(--fg);color:var(--bg);border-color:var(--fg)}
.chip em{font-style:normal;display:block;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin-top:2px}
.chip.on em{color:var(--bg)}
.field{display:flex;flex-direction:column;gap:.3rem}
.field span{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--g6);font-weight:500;line-height:1.5}
.field textarea{font:inherit;font-size:15px;line-height:1.5;color:var(--fg);background:var(--g1);border:0;border-bottom:1px solid var(--g3);padding:.6rem .75rem;min-height:4.5rem;resize:vertical;width:100%;border-radius:0}
section.grey .field textarea{background:var(--bg)}
.field textarea:focus{outline:none;border-bottom-color:var(--accent)}
.stamp{font-size:11px;color:var(--g6);margin-top:.4rem;min-height:1em}
.bar{position:fixed;left:0;right:0;bottom:0;z-index:99;background:#000;color:#fff;font-size:12px;letter-spacing:.04em;border-top:1px solid #333}
.bar .in{max-width:var(--max);margin:0 auto;padding:.6rem 32px;display:flex;align-items:center;gap:1rem;flex-wrap:wrap}
.bar b{font-weight:500}
.bar button{font:inherit;font-size:11px;letter-spacing:.1em;text-transform:uppercase;padding:.5rem .9rem;border:1px solid #767676;background:transparent;color:#fff;cursor:pointer;border-radius:0;line-height:1.4}
.bar button:hover{border-color:#fff}
.bar button.pri{background:#DA1A00;border-color:#DA1A00}
.bar .msg{color:#B7B7B7;flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
details.tech{font-size:13px;color:var(--g7);margin-top:var(--s2)}
details.tech summary{cursor:pointer;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--fg);font-weight:500;padding:var(--s1) 0}
details.tech ol{padding-left:1.6em;margin:var(--s2) 0 0}
details.tech li{margin:0 0 8px;line-height:1.6;overflow-wrap:anywhere}
footer{padding:var(--s5) 0;font-size:12px;color:var(--g6)}
.ctab{width:100%;border-collapse:collapse;font-size:14px;line-height:1.45;margin:var(--s3) 0 var(--s2);min-width:720px}
.ctab th,.ctab td{text-align:left;padding:.55rem .6rem;border-bottom:1px solid var(--g3);vertical-align:top}
.ctab th{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--g6);font-weight:500}
.ctab td.n{font-variant-numeric:tabular-nums;white-space:nowrap}
.ctab a{color:var(--fg)}
.ctab td.st{color:var(--g6);white-space:nowrap}
.ctab td.dim{color:var(--g6)}
.ctab.axes{min-width:640px}
.scroll{overflow-x:auto;max-width:100%}
.quote{border-left:2px solid var(--accent);padding:.2rem 0 .2rem 1rem;margin:0 0 var(--s3);font-size:18px;font-weight:300;line-height:1.5;max-width:40em}
.quote small{display:block;font-size:12px;color:var(--g6);margin-top:.3rem}
.spec{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;background:var(--g3);border:1px solid var(--g3);margin:var(--s3) 0 var(--s2)}
.spec .cell{padding:var(--s3);min-width:0;background:var(--card)}
.spec .cap{font-size:11px;letter-spacing:.12em;text-transform:uppercase;line-height:1.5;margin:0 0 var(--s2);color:var(--g6)}
.spec h3{font-size:21px;font-weight:300;line-height:1.3;margin:0 0 .4rem}
.spec p{font-size:14px;line-height:1.55;color:var(--g8);margin:0 0 .5rem}
.spec.four{grid-template-columns:repeat(4,1fr)}
.spec.three{grid-template-columns:repeat(3,1fr)}
.have,.miss{display:inline-block;width:10px;height:10px;margin-right:8px;vertical-align:-1px}
.have{background:var(--fg)}
.miss{border:1px dashed var(--accent)}
.tier{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;color:var(--g6);display:block;margin-top:.5rem;overflow-wrap:anywhere}
.modehead{display:grid;grid-template-columns:1fr 1fr;gap:1px;margin:var(--s3) 0 0}
.modehead div{padding:var(--s2) var(--s3);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--fg);border:1px solid var(--fg)}
.modehead div+div{border-style:dashed}
.spec.subm{margin-top:1px}
/* the matrix */
.matrix{display:grid;grid-template-columns:120px 1fr 1fr;gap:1px;background:var(--g3);border:1px solid var(--g3);margin:var(--s3) 0 var(--s2)}
.matrix>div{background:var(--card);min-width:0}
.matrix .ax{padding:var(--s2);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--g6);line-height:1.5;display:flex;align-items:flex-end}
.matrix .ax.row{align-items:center}
.matrix .ax b{display:block;font-size:14px;letter-spacing:0;text-transform:none;color:var(--fg);font-weight:400;line-height:1.3}
.matrix .corner{background:var(--g1)}
.mcell{padding:var(--s2);position:relative}
.mcell.rec{outline:2px solid var(--accent);outline-offset:-2px}
.mcell.struck svg{opacity:.35}
.mwire{position:relative}
.mcol{display:none}
.mstrike{position:absolute;inset:0;background:linear-gradient(to top right,transparent calc(50% - .5px),var(--g6) 50%,transparent calc(50% + .5px))}
.mtag{display:block;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin-bottom:.4rem;line-height:1.4;min-height:1.4em}
.mnote{font-size:12px;line-height:1.5;color:var(--g7);margin:.5rem 0 0;min-height:2.6em}
ul.plain{margin:var(--s2) 0 0;padding-left:1.2em;font-size:15px;color:var(--g8)}
ul.plain li{margin:0 0 .6rem}
@media(max-width:760px){
  .wrap{padding:0 16px}
  nav.toc .wrap{padding-left:180px}
  body{padding-bottom:112px}
  .bar .in>b{display:none}
  header{padding-top:72px}
  header .grid{grid-template-columns:1fr;gap:var(--s3)}
  h1{font-size:38px}.sub{font-size:19px}h2{font-size:27px}.lead{font-size:18px}
  .pair,.pair.three{grid-template-columns:1fr}
  .spec,.spec.four,.spec.three{grid-template-columns:1fr}
  .modehead{grid-template-columns:1fr}
  .facts li{grid-template-columns:1fr;gap:4px}
  .call{padding:var(--s2)}
  .bar .in{padding:.55rem 16px;gap:.5rem}
  .bar .msg{flex-basis:100%;order:3}
  section{padding:var(--s5) 0}
  .matrix{grid-template-columns:1fr}
  .matrix .ax.col{display:none}
  .matrix .corner{display:none}
  .mcol{display:block;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--g6);margin-bottom:.3rem}
  #glance-table{min-width:0}
  #glance-table thead{display:none}
  #glance-table tr{display:grid;grid-template-columns:2.2em 1fr;border-bottom:1px solid var(--g3);padding:.5rem 0}
  #glance-table td{border:0;padding:.15rem .3rem}
  #glance-table td.n{grid-row:1 / span 3}
  #glance-table td:nth-child(3)::before{content:"Recommended: ";color:var(--g6)}
  #glance-table td:nth-child(4)::before{content:"Your answer: "}
}
@media print{.bar,nav.toc,#rv-back{display:none}body{padding-bottom:0}}
'''

SHOTS = "_lanes/280/layout-matrix/shots/"

def page():
    H = []
    a = H.append
    a(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Assembly and Studio</title>
<meta name="description" content="Apollo proposal: Apollo Assembly and Apollo Studio as two laws on one engine, the eight sub-modes, the matrix Explore would draw, and the path from a pick to a ruling. Thirteen calls with recommendations; nothing decided.">
<style>{CSS}</style>
</head>
<body>
<a id="rv-back" href="../index.html" target="_self" style="position:fixed;top:12px;left:12px;z-index:2147483647;background:#000;color:#fff;font:500 13px/1 'Helvetica Neue',Helvetica,Arial,sans-serif;letter-spacing:.04em;padding:10px 14px;text-decoration:none;border-radius:2px;box-shadow:0 1px 4px rgba(0,0,0,.25)">&larr; All review pages</a>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="var(--g7)"/></marker><marker id="ahr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="var(--accent)"/></marker></defs></svg>

<nav class="toc" aria-label="Sections"><div class="wrap">
  <a href="#glance">Glance</a>
  <a href="#words">Your words</a>
  <a href="#engine">Two laws</a>
  <a href="#have">What exists</a>
  <a href="#door">Door or lever</a>
  <a href="#submodes">Sub-modes</a>
  <a href="#mark">The mark</a>
  <a href="#switch">The switch</a>
  <a href="#explore">Explore</a>
  <a href="#precedent">The precedent</a>
  <a href="#picks">Pick to law</a>
  <a href="#places">Places</a>
  <a href="#order">Build order</a>
  <a href="#house">Housekeeping</a>
</div></nav>

<header id="top">
  <div class="wrap grid">
    <div>
      <p class="label">Session 313 · proposal · Apollo Assembly and Apollo Studio · v1</p>
      <h1>One engine, two laws. Assembly builds what ships; Studio explores what might, every gate still running.</h1>
      <p class="sub">Your Sunday idea drawn out: the two modes, the eight sub-modes, the door and the lever, the matrix Explore would make, and the road a pick takes to become law. Thirteen calls, a recommendation on each. Nothing is decided.</p>
    </div>
    <div class="meta">
      <span>Thursday 1 October 2026 · built in the cloud, from the research of lanes H1 and H2</span>
      <span>Every claim about the tree was checked against it tonight at <code>cdf17a12</code>. Where a file lives only on your Mac, the page says so.</span>
      <span>An idea drawn is not a ruling. Nothing is built or written into the record until you answer.</span>
    </div>
  </div>
</header>

<section id="glance">
  <div class="wrap">
    <p class="label">At a glance · every call and its recommendation</p>
    <h2>If you take every recommendation, this is what you are saying.</h2>
    <p class="lead">One row per call, in page order. The answer column fills as you click. Each row jumps to its drawing.</p>
    <div class="scroll"><table class="ctab" id="glance-table"><thead><tr><th>#</th><th>The call</th><th>Recommended</th><th>Your answer</th></tr></thead><tbody></tbody></table></div>
  </div>
</section>

<section id="words" class="grey">
  <div class="wrap">
    <p class="label">00 · Where this comes from · your words, Sunday 27 September</p>
    <h2>Two ideas noted in one morning and never worked. This page works them.</h2>
    <p class="quote">"the mode selection the first bifurcation would be 'Apollo assembly' and 'Apollo studio' with sub-modes below. What do you think? Can we expand on this"<small>10:54 BST. At 10:58 you kept the names and said Launchpad names the Gen-UI strand. At 11:07: "We might keep simulator for something else."</small></p>
    <p class="quote">"could it actually be built into apollos decision mechanism" … "Okay add the note"<small>10:35 to 10:43 BST, on a matrix of options for a brief with a recommendation on it.</small></p>
    <p class="quote">"this isn't Apollo its a dot-to-dot book"<small>Friday 19 September, on seeing the one-shot path trace a template. The matrix is one answer to that sentence: the agent shows its decisions instead of tracing someone else's.</small></p>
    <p class="lead">The eight sub-mode names (Compose, Adapt, Check, Hand off; Explore, Sketch, Propose, Review) were the seat's list that morning, not yours. They are on this page as a proposal, with a call of their own.</p>
    <details class="tech"><summary>Technical</summary><ol>
      <li>The two Sunday receipts (<code>notes/_receipts/2026-09-27-304-sq-assembly-studio-modes.md</code> and <code>…-sq-permutation-matrix.md</code>) are on your Mac and are not committed: neither is in the clone this page was built from. The quotes above are as lane H2 and the lane H brief carried them from those receipts; the 10:58 line is their reading, not a verbatim quote, and is written here as such.</li>
      <li>The dot-to-dot sentence is in the tree: <code>notes/_lanes/288/DAVE-RULINGS-2026-09-19.md</code>, line 55.</li>
      <li>Research this page draws: <code>notes/_lanes/312/H/H1/FINDINGS.md</code> (the matrix, 21 sources) and <code>notes/_lanes/312/H/H2/PROPOSAL-modes-2026-10-01.md</code> with <code>calls.json</code> (the modes). Both were written for this page.</li>
    </ol></details>
  </div>
</section>

<section id="engine">
  <div class="wrap">
    <p class="label">01 · What a mode is</p>
    <h2>A mode is a law setting on one engine. Same canon, same gates, same record. Four things change and nothing else.</h2>
    <p class="lead">This is not a new idea for Apollo. It is the third naming of one the record already made: on 19 June you decided a two-tier model, canon gated and shipping, exploration ungated as a menu of options, joined by a promotion path that moves nothing without your word. The pack already makes every Copilot declare a lane in its first reply, on-canon or freestyle, and never change lanes silently. What Assembly and Studio add is the missing half: freestyle today runs no gates at all. Studio keeps every gate running and changes what a red does.</p>
    <figure class="fig">{svg_engine()}<figcaption>One engine, two laws · what a red does · what the output is called · where it may live · who moves it across</figcaption></figure>
    <ul class="facts">
      <li><span class="k">A red</span><span><b>Assembly:</b> a blocking gate blocks, as today. <b>Studio:</b> every gate still runs and a red becomes a label on the output, in the gate's own words, with the file and line.</span></li>
      <li><span class="k">The name</span><span><b>Assembly:</b> shippable, canon. <b>Studio:</b> a proposal, marked not-canon in its receipt and on its root.</span></li>
      <li><span class="k">The home</span><span><b>Assembly:</b> the resolving stores and the ship set. <b>Studio:</b> outside them, in the places the June model already named (the showcases folder, the token proposals folder, the promotion queue) and now the matrix pages.</span></li>
      <li><span class="k">The crossing</span><span>Only promotion, only on your words, only through the one sanctioned inscriber. A Studio file never walks into Assembly; a ruling does, and Assembly re-composes from what was promoted.</span></li>
      <li><span class="k">The test</span><span>Freestyle today is Studio with the gates switched off. The proposal switches them back on and changes what a red does. If that sentence is wrong, the whole page is.</span></li>
    </ul>
    <details class="tech"><summary>Technical</summary><ol>
      <li>The June model: <code>knowledge/_PROMOTION-QUEUE.md</code> lines 3–14, "decided 2026-06-19, Dave"; the fence sentence learned 2026-07-02 is on line 14: "Token proposals live in <code>tokens/_proposals/</code> — OUTSIDE the resolving stores — until Dave's sign-off physically moves them in. A <code>$confidence</code> tag is not a fence; the store boundary is the fence." Both folders exist in the tree tonight; <code>knowledge/tokens/_proposals/</code> holds 6 files.</li>
      <li>The lane declaration: <code>apollo-spider/cold-start/DESIGN-CONTRACT.md</code> rule 1, read tonight in the base clone: "Declare the lane, in your first reply … on-canon … or freestyle. On-canon is the default. Freestyle happens only when the designer asks for it in words. Never change lanes silently." Rule 4 makes a non-Apollo skill used for design output freestyle that must be declared and named.</li>
      <li>The inscriber: <code>knowledge/_inscribe_ruling.py</code>, "THE ONLY SANCTIONED WAY TO APPEND A RULING". The store, <code>knowledge/_rulings.json</code>, holds 913 rows tonight (counted in the clone).</li>
    </ol></details>
  </div>
</section>

<section id="have" class="grey">
  <div class="wrap">
    <p class="label">02 · What the tree already has, and the two pieces it does not · measured tonight</p>
    <h2>Four of the six parts exist. The two that do not are small, and they are the whole proposal.</h2>
    <p class="lead">Filled squares are in the tree tonight, with the file. Dashed squares are missing. The engine already has two laws for one check: it just picks the law by the check's age, never by the work's purpose.</p>
    <div class="spec three">
      <div class="cell"><p class="cap"><span class="have"></span>Have · the two tiers</p><h3>Canon and exploration, with promotion</h3><p>Decided 19 June. Gated references ship; showcases are "NOT canon, NOT gated", "a recorded menu of options". A treatment enters canon in three steps, "only when Dave explicitly blesses it".</p><span class="tier">knowledge/_PROMOTION-QUEUE.md</span></div>
      <div class="cell"><p class="cap"><span class="have"></span>Have · the lane</p><h3>Declared per reply, on-canon the default</h3><p>The pack's contract makes every Copilot say which lane it is in before it builds, and never change lanes silently. A lever, declared out loud; not a door.</p><span class="tier">apollo-spider/cold-start/DESIGN-CONTRACT.md · rule 1</span></div>
      <div class="cell"><p class="cap"><span class="have"></span>Have · the advisory tier</p><h3>171 build steps: 82 block, 67 abort, 22 advise</h3><p>And 475 prose rules indexed as 62 blocking, 323 advisory, 34 review, 56 taste. "New checks enter at the advisory tier and earn promotion to blocking by being bite-tested." The promotion direction exists as a flag on two advisory gates.</p><span class="tier">knowledge/_build_all.py · guidelines/_rules-index.json · ADR-0005 §5</span></div>
      <div class="cell"><p class="cap"><span class="have"></span>Have · the receipt</p><h3>A composed page carries a receipt the gate re-hashes</h3><p>Pack version and one row per spliced region with the hash of the page's own bytes, so "did you invent this?" is a comparison, not a judgement. A custom glyph already marks itself with a reason the gate reads as a decision.</p><span class="tier">knowledge/_validate_receipt.py · _validate_icons.py (data-bespoke)</span></div>
      <div class="cell"><p class="cap"><span class="miss"></span>Missing · the demotion direction</p><h3>No way to run a blocking gate as a label</h3><p>Two advisory gates can be made to block with a flag; nothing can make a blocking gate advise. The pack's runner knows three verdicts, pass, FAIL, COULD-NOT-ASK, and nothing about tier: a gate is advisory in the pack only because its script happens to exit 0.</p><span class="tier">apollo-spider/ci-template/run-gates.py · the five advisory validators' headers</span></div>
      <div class="cell"><p class="cap"><span class="miss"></span>Missing · gates in freestyle</p><h3>Freestyle runs no gates at all</h3><p>The contract's second lane is where the gates stop. The pack's own skills already say the gap out loud: "Green gates are not a pass", and a draft is "a candidate for review, not adopted canon". What is missing is the law that keeps the gates running when the work is a proposal.</p><span class="tier">DESIGN-CONTRACT.md rule 1 · skills/check-against-design-system · skills/draft-a-new-pattern</span></div>
    </div>
    <details class="tech"><summary>Technical</summary><ol>
      <li>Route counts by <code>ast</code> over <code>ROUTE_ROWS</code> in <code>knowledge/_build_all.py</code> at <code>cdf17a12</code>: 171 rows, GATE 82, ABORT 67, ADVISORY 22. Lane H2 counted 167 = 78/67/22 on the same file the night before; four GATE rows landed since. Rules: <code>knowledge/guidelines/_rules-index.json</code>, 475 rows by <code>destiny</code>: ADVISORY 323, BLOCKING 62, TASTE 56, REVIEW 34 (unchanged from H2).</li>
      <li>The advisory validators' own words: <code>_validate_advisory.py</code> "they annotate, they never block"; <code>_validate_geometry.py</code> and <code>_validate_own_size.py</code> carry <code>--strict</code> (3 mentions each); <code>_validate_theme_provenance.py</code>, <code>_validate_hidden_display.py</code>, <code>_validate_edge_extremity.py</code> have no <code>--strict</code> at all (0 mentions). The promotion direction is on two of six; the demotion direction is on none.</li>
      <li>The runner: <code>apollo-spider/ci-template/run-gates.py</code> docstring line 2, "report three verdicts: pass, FAIL, COULD-NOT-ASK"; lines 18–20 make COULD-NOT-ASK "a refusal, not a failure". H2 read the shipped v1.0.14 manifest at your seat (57 gate verdicts, fields gate·invocation·population·selftest·third_party·verdict·why, no tier); that folder (<code>notes/_lanes/305/V2/cold/</code>) is not in the clone and was not re-read tonight.</li>
      <li>ADR-0005 §5: <code>docs/decisions/ADR-0005-ratify-knowledge-engine-pivot.md</code> line 35.</li>
    </ol></details>
  </div>
</section>

<section id="door">
  <div class="wrap">
    <p class="label">03 · Door, lever, or both · your call</p>
    <h2>Both. Assembly by default; the lever moves only on three named triggers; the way back is promotion.</h2>
    <p class="lead">A door alone asks you to know which mode you need before the brief has been read. A lever alone leaves the agent to decide when to pull it. Both together: the brief is the door, and the lever has names on it. Three outside precedents each run a launch setting and a mid-work switch together: Claude Code's permission modes, Figma's Dev Mode statuses, GitHub's protected branches, where the same checks run everywhere and are required only where the work is going.</p>
    <figure class="fig">{svg_door_lever()}<figcaption>Three shapes · the recommended one has a diamond for the brief, a default line for Assembly, three named triggers down, and one red road back</figcaption></figure>
    <ul class="facts">
      <li><span class="k">The door</span><span>Is the brief, not a question. The brief skill already records every skipped question as "a decision left open". Two or more decisions left open is the cue to offer Studio's Explore, in the reply, before building. A brief that settles everything starts in Assembly and says so.</span></li>
      <li><span class="k">The lever in</span><span>Two triggers: a gate refuses (Sketch or Propose offered in the refusal's own words), or you ask in words (today's rule for freestyle, kept). The agent names the move in its reply and marks the output.</span></li>
      <li><span class="k">The lever out</span><span>Promotion only. A Studio output is not carried across; a ruling is, and Assembly re-composes. The store-boundary fence from July, applied to modes.</span></li>
      <li><span class="k">The precedent that fits best</span><span>GitHub's protected branch. Assembly is the protected branch, Studio is every other branch, promotion is the merge, and the review is yours.</span></li>
    </ul>
{call("door", 1, "Door, lever or both", "How does work get into Studio, and back?", "Both: Assembly by default, the lever by named triggers, the way back by promotion only", ["Both, Assembly by default", "A door at the start only", "A lever mid-work only", "None of these (say below)"], rec_chip="Both, Assembly by default")}
    <details class="tech"><summary>Technical</summary><ol>
      <li>The skip rule: <code>apollo-spider/skills/grill-me/SKILL.md</code>, "A skipped question is not a wrong answer. It is a decision left open", read tonight.</li>
      <li>Outside precedents fetched by H2 on 2026-10-01: Claude Code "Configure permissions" (<code>defaultMode</code> at launch, changed mid-session; "Permission rules are enforced by Claude Code, not by the model"); Figma "Dev Mode statuses" (Ready for dev set "while editing designs or in Dev Mode", an automatic Changed state); GitHub "About protected branches" (required status checks "must have a successful, skipped, or neutral status"). H2's second pass re-fetched the Claude Code page only; the other two are as its first pass read them.</li>
      <li>The Claude Code line is the one that matters for the build: a mode written only in skill prose is a wish; the runner has to hold it. Hence the switch in 06.</li>
    </ol></details>
  </div>
</section>

<section id="submodes" class="grey">
  <div class="wrap">
    <p class="label">04 · The sub-modes · your call</p>
    <h2>Four of the eight already exist under other names. Two are thin. One is a naming. One is the matrix.</h2>
    <p class="lead">Each sub-mode put against the pack skill that does it today, the law its gates run under, and what it makes. Filled square: a skill exists. Dashed: none yet. None of the missing four is needed for the modes to be real; the mark and the switch are.</p>
    <div class="modehead"><div>Apollo Assembly · gates block · one recommended output · shippable</div><div>Apollo Studio · gates advise and label · many outputs · proposals marked not-canon</div></div>
    <div class="spec subm">
      <div class="cell"><p class="cap"><span class="have"></span>Compose</p><h3>From a brief to a page whose every region hashes to canon</h3><p>The brief skill, then generate-from-canon ("compose, never trace"; "Only what exists"; a Gaps list when something is missing). This is the pack as shipped. Missing: nothing.</p></div>
      <div class="cell"><p class="cap"><span class="miss"></span>Explore</p><h3>The permutation matrix</h3><p>Two named axes found from the brief, six cells rendered, one recommended with a sentence from the brief, one foil, a struck cell shown struck, every cell wearing its reds as labels. Drawn in 07. Missing: the whole thing; the #280 layout matrix is the hand-built precedent.</p></div>
      <div class="cell"><p class="cap"><span class="miss"></span>Adapt</p><h3>Change an existing output within the rules</h3><p>Compose starting from a receipt instead of a brief; the receipt re-hash is the whole test (a region that stops hashing is an edit that left canon). The layout dials already have this shape. Missing: a small skill.</p></div>
      <div class="cell"><p class="cap"><span class="miss"></span>Sketch</p><h3>A fast, loose page that says which parts are canon</h3><p>Today's freestyle, governed: all gates run, none block; the receipt marks every region that does not hash as a proposal. The change to the five rules is one word: "never invent" becomes "never invent silently". Missing: the governed freestyle.</p></div>
      <div class="cell"><p class="cap"><span class="have"></span>Check</p><h3>The machine's verdict, in the gate's words</h3><p>check-with-gates and check-against-design-system, which already call themselves two halves of one act. "Say why it fails" is how every gate reports. Missing: nothing.</p></div>
      <div class="cell"><p class="cap"><span class="have"></span>Propose</p><h3>A candidate for the library, outside the stores</h3><p>draft-a-new-pattern already calls itself "the creative mode" and makes "a candidate for review, not adopted canon"; signing its token manifest "turns a sketch into a candidate". Output lands in the proposals folder or the promotion queue. Missing: nothing in the skill; the queue's review pass has been owed since July.</p></div>
      <div class="cell"><p class="cap"><span class="miss"></span>Hand off</p><h3>What leaves, and what does not</h3><p>generate-from-canon already outputs React or HTML; the pack gates govern the pack, not a handoff. Missing: a skill that names what leaves (code, specs, tokens, the receipt). On the seat's reading, Launchpad is Hand off at runtime; that is a call in 10, not a fact.</p></div>
      <div class="cell"><p class="cap"><span class="have"></span>Review</p><h3>Your sentence, which is what gets inscribed</h3><p>usability-review for the heuristic pass ("a screen can be perfectly conformant and perfectly gated and still be confusing"), and pages like this one for your eye. Gates: none; the output is a sentence and it goes to the record. Missing: nothing.</p></div>
    </div>
    <p class="lead" style="margin-top:var(--s3)">Are Check and Review one thing seen from two sides? The pack's own skills say no. Check is the machine's verdict on construction and it can be green while the thing is wrong. Review is a person's verdict on the thing, and its output is a sentence, not a pass. Their outputs go to different places: a Check verdict goes back to the page, a Review sentence goes to the record.</p>
{call("submodes", 2, "The eight sub-modes", "Does the list of eight stand?", "The eight stand", ["The eight stand", "Fold Check into Review", "Fold Adapt into Compose", "A different list (say below)"])}
    <details class="tech"><summary>Technical</summary><ol>
      <li>Skill phrases read tonight in the base clone's <code>apollo-spider/skills/*/SKILL.md</code>: generate-from-canon "compose, never trace", rule 1 "Only what exists"; draft-a-new-pattern line 8 "The creative mode", line 84 "a candidate for review, not adopted canon", line 76 "sketch into a candidate"; check-against-design-system "Green gates are not a pass"; usability-review "perfectly conformant and perfectly gated and still be confusing".</li>
      <li>Adapt's shape: <code>knowledge/_render/_bento_edit_rails.json</code> and the #248 edit mode.</li>
      <li>Explore's precedent: <code>notes/_lanes/280/layout-matrix/REPORT.md</code>; the research: H1's findings §3–§6.</li>
    </ol></details>
  </div>
</section>

<section id="mark">
  <div class="wrap">
    <p class="label">05 · The mark on Studio work · your call</p>
    <h2>One field in the receipt and one attribute on the page root, read by the gate that already parses the receipt. A tag is not a fence; the gate is.</h2>
    <p class="lead">Your July lesson, in the promotion queue's own words: "A $confidence tag is not a fence; the store boundary is the fence." So the mark is not a folder convention or a comment. It is a field the receipt gate reads, with two laws: in Assembly a studio-marked page is refused, so nothing from Studio ships by accident; in Studio the same gate lists the regions that do not hash, by name and reason, instead of refusing.</p>
    <figure class="fig">{svg_mark()}<figcaption>The page as a file · the receipt rows that exist · the one new field · the same gate reading it under each law</figcaption></figure>
    <ul class="facts">
      <li><span class="k">Cost</span><span>One field, one attribute, one branch in a gate that exists. The hash rows, the pack version and the re-hash are all in the tree today.</span></li>
      <li><span class="k">What it stops</span><span>Studio becoming the place reds go to hide. A Studio output cannot ship; the promotion queue is a visible list; and nothing advisory becomes law without a bite test and your word.</span></li>
      <li><span class="k">The unhashed kind</span><span>A region that does not hash carries a kind and a reason: proposal (no canon fits) or bespoke (the word a custom glyph already uses). Same mark, widened from one glyph to a region.</span></li>
    </ul>
{call("mark", 3, "The mark on Studio work", "How is a Studio output marked?", "In the receipt and on the page root, read by the receipt gate", ["Receipt field and root attribute, read by the gate", "A folder convention only", "No mark", "None of these (say below)"], rec_chip="Receipt field and root attribute, read by the gate")}
    <details class="tech"><summary>Technical</summary><ol>
      <li><code>knowledge/_validate_receipt.py</code>: "the page carries a receipt, and the gate's first act is to PARSE it"; the key is a content hash of the page's own region bytes; "a receipt is valid against the pack version it was minted from, never across cuts", which is why <code>pack</code> rides in the receipt and why <code>mode</code> can ride beside it.</li>
      <li><code>knowledge/_validate_icons.py</code> lines 12–19: <code>&lt;svg data-bespoke="reason"&gt;</code> marks "a deliberately custom shape".</li>
      <li>The root attribute sits beside <code>data-apollo-theme</code>, which every composed page carries today.</li>
    </ol></details>
  </div>
</section>

<section id="switch" class="grey">
  <div class="wrap">
    <p class="label">06 · The law switch · your call</p>
    <h2>A mode flag on the pack's runner, with the tier carried in the manifest. In Studio a red becomes a label; a gate that could not look stays a refusal in both.</h2>
    <p class="lead">This is the one mechanical change, and it is the direction the engine does not have: run a blocking gate as a label. Today the runner infers a gate's law from its exit code and knows nothing of tier. The flag puts the law where Claude Code puts its permission modes, in the runner, not in prose, and the manifest says which tier each gate is so the runner reads it instead of guessing.</p>
    <figure class="fig">{svg_switch()}<figcaption>The same seven gates, two laws · left: the first red stops the run · right: every gate runs and each red is written into the receipt in the gate's words</figcaption></figure>
    <ul class="facts">
      <li><span class="k">Could not ask</span><span>Stays a refusal in both modes. A gate that could not look is not a label; it is a hole, and the runner already prints it in full.</span></li>
      <li><span class="k">Not a second runner</span><span>A second runner for Studio is a second pack by another name, and the pack is one bake from one commit, byte-identical.</span></li>
      <li><span class="k">The generate skill</span><span>One paragraph at the top. In Assembly, unchanged. In Studio the Gaps list is not a stop; it is Propose's intake, and every gap becomes a marked region. "Only what exists" is not relaxed; a gap is shown rather than refused.</span></li>
    </ul>
{call("switch", 4, "The law switch in the pack's runner", "How does the pack learn the second law?", "A mode flag on the runner, the tier carried in the manifest", ["A mode flag on the runner, tier in the manifest", "A second runner for Studio", "No change: Studio runs only in the repo", "None of these (say below)"], rec_chip="A mode flag on the runner, tier in the manifest")}
    <details class="tech"><summary>Technical</summary><ol>
      <li>Proposed shape: <code>run-gates.py --mode assembly|studio</code>, assembly the default. In studio a FAIL is written as a label into the page's receipt and the runner exits 0 for it; COULD-NOT-ASK keeps its refusal. The per-gate verdict in the manifest gains <code>tier</code>.</li>
      <li>Unproven (H2 said so and nothing tonight changes it): whether the runner can carry a per-gate tier without changing the manifest generator under <code>knowledge/_release/</code>. Asserted from reading, not from a build.</li>
      <li><code>apollo-spider/</code> is job G's folder; <code>gates.yml</code> says "To turn a check off, DELETE ITS STEP. Do not add continue-on-error to hide a red." The switch respects that: no step is turned off, the law of a red changes.</li>
    </ol></details>
  </div>
</section>

<section id="explore">
  <div class="wrap">
    <p class="label">07 · Explore · the matrix as a map, drawn on your CEO brief · your calls</p>
    <h2>Two axes the brief leaves open, six cells, one struck, one recommended with the brief's own sentence, one foil that is what Assembly would have shipped unasked.</h2>
    <p class="lead">The axes are the decisions the agent would otherwise make silently. The research says four things that shape the build: the box blows up, so cut it to two axes before you look; several alternatives side by side beat one at a time, for the quality of the result and for the honesty of the feedback; the known failure is a matrix drawn after the pick to justify it, so render before recommending and cite the brief; and picks become taste only by accumulation. Below, the axis finder's pass over your CEO brief, then the grid it makes.</p>
    <div class="scroll"><table class="ctab axes"><thead><tr><th>Decision the agent would make silently</th><th>Does the brief settle it?</th><th>Verdict</th></tr></thead><tbody>
      <tr><td>Density</td><td class="dim">Yes: "Desktop first, comfortable density."</td><td>Closed. Listed with the sentence; never re-asked.</td></tr>
      <tr><td>Order of the three questions</td><td class="dim">Yes: "in this order"</td><td>Closed.</td></tr>
      <tr><td>Inventing a component</td><td class="dim">Yes: "Don't invent components, variants, colours or icons"</td><td>Closed. A fence, not an axis.</td></tr>
      <tr><td><b>Overview structure</b>: three bands · tile wall · feed</td><td>No. The brief says what must be answerable "without scrolling", not how.</td><td><b>Open, rank 1.</b> Structure: it changes what is where.</td></tr>
      <tr><td><b>Emphasis of "what needs my attention"</b>: counts first · items first</td><td>No. "each one leading to the record they can act on" constrains, does not settle.</td><td><b>Open, rank 2.</b> Emphasis: it changes what the eye lands on.</td></tr>
      <tr><td>Exposure visual: bars by region · map · table</td><td>No. "by region and currency, with a way to drill through"</td><td>Open, rank 3. Shown as a slice of the picked cell, not a third dimension.</td></tr>
      <tr><td>Drill mechanism · filter placement</td><td class="dim">Partly.</td><td>Left to Assembly's defaults, and the page says so.</td></tr>
    </tbody></table></div>
    <div class="matrix">
      <div class="corner"></div>
      <div class="ax col"><span><b>Counts first</b>a tile with the number of pending approvals</span></div>
      <div class="ax col"><span><b>Items first</b>the approvals themselves, each a row that opens</span></div>
      <div class="ax row"><span><b>Three bands</b>one per question, stacked</span></div>
      {cell("bands", "counts", "Runner-up", "If the approvals list proves too tall for the fold at 1440. The one fact a render settles and prose cannot.")}
      {cell("bands", "items", "Recommended", "The CEO wants three things “in this order” and must “answer the three questions without scrolling”: bands are the order made visible, and “each one leading to the record they can act on” is met by showing the records, not a number about them.")}
      <div class="ax row"><span><b>Tile wall</b>a grid of tiles, bento</span></div>
      {cell("tiles", "counts", "Foil · Assembly's default", "What a bare dashboard prompt lands on: it answers “how many” and defers “which” to a click. The datum every other cell is scored against.")}
      {cell("tiles", "items", "", "Live. Tiles with rows inside; the order of the three questions is weakest here.")}
      <div class="ax row"><span><b>Feed</b>one ranked stream under three headings</span></div>
      {cell("feed", "counts", "Struck", "A feed is item-led by nature; “counts first” has nothing to be first of. Shown struck, with this sentence: the strike is the evidence the axes were real.", struck=True)}
      {cell("feed", "items", "", "Live. The stream answers “what needs my attention” best and “can we fund our plans” worst.")}
    </div>
    <ul class="facts">
      <li><span class="k">Held constant</span><span>Everything not on an axis: the dashboard set as it stands, comfortable density, light mode, 1440 for the grid. Two cells that differ on several things at once are a sample, not a map.</span></li>
      <li><span class="k">The slice</span><span>On the picked cell only: exposure as bars by region against a map. Bars recommended, because the brief's drill is to "positions and limits", which are rows; a map with no geography in the data is decoration.</span></li>
      <li><span class="k">The four guards</span><span>Render before recommending. Cite the brief's sentence, or the cell cannot be the recommendation. Always one foil, the datum where one exists. Record the runner-up beside the pick.</span></li>
      <li><span class="k">The honest limit</span><span>Your six rounds on the workers in overalls: a matrix of figure kind would very likely have taken rounds one and two together; rounds three to six were edits to the chosen figure, where a grid is noise. The matrix compresses the choice of kind, not the tuning of the chosen one.</span></li>
      <li><span class="k">The axis list</span><span>Ten named axes to start from, not a blank page: structure, emphasis, order (a tested list from the layout-solver literature), and the ones your own briefs have turned on: density, rhythm, the list-or-card line, chart form per question, drill mechanism, filter placement, figure kind. Three or four values each. A finish axis (a radius, a token value) is never a matrix axis; it is a tuner.</span></li>
    </ul>
{call("matrix-when", 5, "When Explore draws a matrix", "When does the agent draw one?", "As standard when a brief leaves two structure or emphasis decisions open; never for a tuning pass", ["As standard, when two axes are open", "Only when you ask for one", "None of these (say below)"], rec_chip="As standard, when two axes are open")}
{call("matrix-size", 6, "The size of the grid", "How big is a matrix allowed to be?", "Six cells working size, nine the ceiling, a third axis as slices of the picked cell", ["Six working, nine the ceiling", "Nine as standard", "Let the agent decide each time", "None of these (say below)"], rec_chip="Six working, nine the ceiling")}
{call("struck", 7, "Cells the axes cannot make", "What happens to a cell two values cannot share?", "Shown struck, with the reason", ["Shown struck, with the reason", "Dropped silently", "None of these (say below)"])}
{call("axes", 8, "The axis list", "Where do the axes come from?", "The ten drawn here as the starting vocabulary, yours to edit; a settled axis is never re-asked", ["The ten here, yours to edit", "Let the agent find axes fresh each time", "None of these (say below)"], rec_chip="The ten here, yours to edit")}
    <details class="tech"><summary>Technical</summary><ol>
      <li>The brief: <code>notes/_briefs/2026-09-19-288-test-brief-ceo-international-banking.md</code>; every quoted sentence was found in it tonight. The axis finder's pass and the grid are H1's §7, re-drawn here; the cell wireframes are drawings, not renders (no seat tonight). The first render is call 13's job.</li>
      <li>Research behind the four guards (H1 §1–§4, 21 sources named and dated): Zwicky's box and Ritchey's cross-consistency assessment (strike by value pairs, not cell by cell); Heller et al. 2014 on the blow-up and Tomiyama's post-hoc misuse; Pugh's datum; Sobek, Ward and Liker 1999 on keeping the runner-up alive; Tohidi et al. CHI 2006 (one design gets higher ratings and less criticism than the same design among three); Dow et al. 2010 (parallel beat serial: 445.0 v 397.9 clicks per million, 24.4 v 21.7 expert rating); Scout CHI 2020 (structure, emphasis, order); Luminate CHI 2024 (a model can name axes from a brief; forty cells is a writer's instrument, not a designer's).</li>
      <li>Cell count: the choice-overload meta-analyses (Scheibehenne et al. 2010, mean effect "virtually zero"; Chernev et al. 2015, four moderators) say the risk is set complexity, not count. Labelled axes with everything else constant are the cure. Midjourney's four-up and v0's three variants are samples; Stable Diffusion's X/Y/Z plot and Figma's variant sets are maps.</li>
      <li>Whether the #246/#258 cold runs actually landed on the "tile wall × counts first" foil is checkable in <code>reviews/COLDRUN-258-*.html</code>; H1 did not check it and neither did tonight.</li>
      <li>The ten-axis vocabulary exists nowhere as a file yet; H1 said a lane should not mint it. It is drawn here for your edit.</li>
    </ol></details>
  </div>
</section>

<section id="precedent" class="grey">
  <div class="wrap">
    <p class="label">08 · The precedent · the matrix that got a ruling where four sketches had not</p>
    <h2>Mid-September you refused a fifth sketch of the explorer's layout. A 3 × 2 grid of rendered cells was ruled the same day.</h2>
    <p class="lead">Layout by row, dimension by column, one sentence each, nothing to answer. The six pictures are the ones the lane rendered then, straight from the repo. This is the hand-built case of what Explore would do by method: two named axes, every cell real, the default kept in the corner, the pick made by eye.</p>
    <div class="pair three">
      <figure><figcaption>Force · 2D · the default</figcaption><a href="{SHOTS}kg-118-force-2d-light.png"><img src="{SHOTS}kg-118-force-2d-light.png" alt="The knowledge graph explorer laid out by force in two dimensions: one red hub with families fanning out"></a></figure>
      <figure><figcaption>Strata · 2D</figcaption><a href="{SHOTS}kg-118-strata-2d-light.png"><img src="{SHOTS}kg-118-strata-2d-light.png" alt="The explorer as three horizontal bands with the constitution as bedrock below"></a></figure>
      <figure><figcaption>Shells · 2D</figcaption><a href="{SHOTS}kg-118-shells-2d-light.png"><img src="{SHOTS}kg-118-shells-2d-light.png" alt="The explorer as concentric shells in two dimensions"></a></figure>
      <figure><figcaption>Force · 3D</figcaption><a href="{SHOTS}kg-118-force-3d-light.png"><img src="{SHOTS}kg-118-force-3d-light.png" alt="The force layout lifted into three dimensions and turned"></a></figure>
      <figure><figcaption>Strata · 3D · the floors</figcaption><a href="{SHOTS}kg-118-strata-3d-light.png"><img src="{SHOTS}kg-118-strata-3d-light.png" alt="The three layers as translucent plates stacked in three dimensions"></a></figure>
      <figure><figcaption>Shells · 3D</figcaption><a href="{SHOTS}kg-118-shells-3d-light.png"><img src="{SHOTS}kg-118-shells-3d-light.png" alt="The shells layout in three dimensions"></a></figure>
    </div>
    <ul class="facts">
      <li><span class="k">What it had</span><span>Two named axes (layout, dimension), six real cells of the same graph, the default pixel for pixel in the corner, one sentence per cell.</span></li>
      <li><span class="k">What it lacked</span><span>A recommendation with a reason from a brief, a foil named as foil, a struck cell, and a pick record. Explore adds those four.</span></li>
    </ul>
    <details class="tech"><summary>Technical</summary><ol>
      <li><code>notes/_lanes/280/layout-matrix/REPORT.md</code> and the contact sheet <code>MATRIX-2026-09-16.html</code>; the six shots are the ones that sheet embeds (<code>shots/kg-118-*-light.png</code>, 23 shots committed). Explorer v1.18, 2026-09-16.</li>
    </ol></details>
  </div>
</section>

<section id="picks">
  <div class="wrap">
    <p class="label">09 · From a pick to a law · your calls</p>
    <h2>A pick is a choice under one brief. A ruling is law. Different records, different writers, one door between them: a review page and your word.</h2>
    <p class="lead">The ruling store's every field is yours: who ruled, your words verbatim, what it governs. A pick has none of that shape, so picks never go there; the store's own form refuses them. They go in a file of their own, one row per matrix, and when the same value wins on the same axis three times with a sentence each, the system writes a candidate ruling onto a review page with the three picks as its evidence. You rule in prose; the inscriber inscribes; only then does Assembly read it as a default.</p>
    <figure class="fig">{svg_promotion()}<figcaption>Three picks with sentences · a candidate on a review page · your word · law · Assembly reads the law and never the picks</figcaption></figure>
    <ul class="facts">
      <li><span class="k">The pick row</span><span>Matrix, date, brief, the two axes with all their values, the recommended cell, the picked cell, the cells it was preferred to, your sentence verbatim or "click" if none, any axis you rejected with your words, and the promotion state.</span></li>
      <li><span class="k">Why the losers too</span><span>Storing the comparison, not only the winner, is what a preference model could later be fitted to, if the record grows; and it is what lets the audit "did the recommendation win?" be run per matrix, which is the honesty measure of the axis finder over time.</span></li>
      <li><span class="k">Clicks</span><span>A click-only run of three does not trigger. Three clicks are three tastes with no reason, and a reasonless law is what the record exists to prevent. The #272 separation, where 79 accepted-by-click were named as clicks, is the precedent.</span></li>
      <li><span class="k">A rejected axis</span><span>"The question was wrong" goes to the axis list as a note against that axis, never to the store.</span></li>
    </ul>
{call("picks", 9, "Where a pick is kept", "Where does a pick live, and is a click recorded?", "Its own file beside the matrix pages; clicks recorded as clicks; never the ruling store", ["Its own file; clicks recorded as clicks", "Only picks with a sentence are recorded", "In the ruling store", "None of these (say below)"], rec_chip="Its own file; clicks recorded as clicks")}
{call("threshold", 10, "When picks become a candidate ruling", "How many picks before a candidate ruling is put to you?", "Three picks with a sentence, on the same value of the same axis, onto a review page", ["Three, with sentences", "Every pick goes to a review page", "Five, with sentences", "Never automatically; only when you ask", "None of these (say below)"], rec_chip="Three, with sentences")}
    <details class="tech"><summary>Technical</summary><ol>
      <li>The store's shape, read by H1 at the s311-D2 row: id · ruled · date · by ("Dave") · says (verbatim, with where) · governs · evidence · status. Every field his.</li>
      <li>Proposed home for the picks file: a JSONL beside the matrix pages (<code>notes/_matrices/</code>) or <code>knowledge/_picks.jsonl</code>; the location is yours, named in call 9's comment if you have a view. Assembly's composer never reads it; it reads rulings. The ruling's <code>evidence</code> field points at the picks.</li>
      <li>The lineage of "store the comparison": Bradley and Terry 1952; Christiano et al. 2017. Conjoint analysis needs dozens of choices per respondent; Apollo has one respondent making one pick per brief, hence counting first, a model later if ever.</li>
    </ol></details>
  </div>
</section>

<section id="places" class="grey">
  <div class="wrap">
    <p class="label">10 · What is a place, not a mode · your calls</p>
    <h2>The record, the pack and Launchpad are places. Simulator is held, as you said.</h2>
    <p class="lead">Your line on the Sunday: the record is a place, not a mode. The tree is already built that way: both modes read it, only the inscriber writes it, and promotion is the only path in. The pack is one bake from one commit; the mode is a setting on how the pack is used, never a second pack. Launchpad has moved on since the Sunday: it is now a real folder, an A2UI catalogue over MCP with the gates offered as a service, built this week.</p>
    <div class="spec four">
      <div class="cell"><p class="cap">The record</p><h3>A place</h3><p>Rulings, the state store, the knowledge graph and its explorer, the showroom. Both modes read it; only your word writes it.</p></div>
      <div class="cell"><p class="cap">The pack</p><h3>A place</h3><p>One bake, byte-identical, from one commit. Assembly and Studio are two ways of using it, carried by one flag on its runner.</p></div>
      <div class="cell"><p class="cap">Launchpad</p><h3>A runtime of Hand off · proposed</h3><p>It runs in someone else's product with no designer watching, over MCP, with the gates as a service. On that reading it is the strictest consumer of Assembly, not a third mode. This is the call most likely to be wrong, because the strand is yours and route B was ruled with other things in mind.</p></div>
      <div class="cell"><p class="cap">Simulator</p><h3>Held</h3><p>"We might keep simulator for something else." The seat's reading that it is a stage every output passes through stays a reading, on the page only because you may want to assign the name now.</p></div>
    </div>
{call("launchpad", 11, "Launchpad's place", "Is Launchpad a mode, or a runtime of one?", "A runtime of Hand off, with the strictest gates of the three", ["A runtime of Hand off", "A third mode beside Assembly and Studio", "None of these (say below)"])}
{call("simulator", 12, "Simulator", "What does the name Simulator do?", "Hold the name, as you said", ["Hold the name", "The stage every output passes through, from any mode", "A Studio sub-mode for prototyping", "None of these (say below)"], rec_chip="Hold the name")}
    <details class="tech"><summary>Technical</summary><ol>
      <li>Launchpad in the tree tonight: <code>apollo-launchpad/README.md</code> ("The proof of concept of Apollo as an A2UI catalogue over MCP (route B)"; "Nothing here is in the pack's ship set"; the name "never appears on shared material"); <code>catalogue/</code> built and proven at #312 lane C1 (17 dashboard parts, A2UI v0.9.1); gates as a service (C3) and the chooser (C4) are tonight's cloud lanes, per <code>notes/_lanes/312/C/SPEC-launchpad-day-one.md</code> §7.</li>
      <li>Route B and the Launchpad name: <code>notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html</code>, ruled at the 27 September sitting (the rulings are in the store under s305; not repeated here).</li>
      <li>"the record is a place, not a mode" and the Simulator line are from the Sunday receipt as H2 carried them; the receipt is not in the clone (see 00).</li>
    </ol></details>
  </div>
</section>

<section id="order">
  <div class="wrap">
    <p class="label">11 · If every call goes your way · the build order, and the first live test · your call</p>
    <h2>Smallest fence first. The mark and the switch make the modes real in two small changes; everything after is a skill.</h2>
    <figure class="fig">{svg_order()}<figcaption>Five steps · the two in red are the proposal; three, four and five are skills that follow</figcaption></figure>
    <p class="lead">The first live matrix should be a brief whose answer is known well enough to check the recommender against. The CEO overview is that brief: the axis finder's pass is already drawn above, the foil is what the cold runs produce, and the runner-up is the one fact a render settles. Your drawing of the workers would be the wrong first test; it is a tuning problem dressed as a choice.</p>
{call("first-test", 13, "The first live matrix", "Which brief does Explore run on first, rendered?", "The CEO overview brief, rendered at 1440: the answer is known enough to check the recommender against", ["The CEO overview brief, rendered", "The next real brief that comes in", "Not yet", "None of these (say below)"], rec_chip="The CEO overview brief, rendered")}
    <details class="tech"><summary>Technical</summary><ol>
      <li>Build order per H2 §5 and §7: the mark (receipt field + root attribute + one branch in <code>_validate_receipt.py</code>), the switch (<code>run-gates.py --mode</code>, tier in the manifest), the contract rename (on-canon → Assembly, freestyle → Studio; "Never invent" reads "Never invent silently" in Studio; <code>gen_projections.py</code> regenerates CLAUDE.md, AGENTS.md and the Copilot boot from the one source), then skills as needed. Explore's own order per H1 §8: static grid with pick and sentence → lock and re-roll on one axis → combine (Pugh's hybrid round) last.</li>
      <li>Owners if ruled: <code>apollo-spider/</code> is job G's; the manifest generator is under <code>knowledge/_release/</code>; the receipt gate is under <code>knowledge/</code>. Explore has no owner yet.</li>
      <li>Nothing on this page is inscribed; the store was not written. If you rule, the rulings are inscribed from your export's verbatim words, as tonight's were.</li>
    </ol></details>
  </div>
</section>

<section id="house" class="grey">
  <div class="wrap">
    <p class="label">12 · Housekeeping · found tonight, not fixed · nothing to answer</p>
    <h2>Four things the page could not do from the cloud, said plainly.</h2>
    <ul class="plain">
      <li>The two Sunday receipts with your verbatim words are on your Mac and not in the repo. The page quotes them through lane H2's reading. Committing them is a one-line job for the seat.</li>
      <li>The matrix cells in 07 are wireframe drawings, not renders; the first render is call 13. The six pictures in 08 are real, from the repo.</li>
      <li>The v1.0.14 cold-verifier manifest H2 read (57 verdicts, no tier field) is not in the clone and was not re-read. The runner's three verdicts were.</li>
      <li>Lane H2's route count (167 = 78/67/22) moved to 171 = 82/67/22 overnight; four blocking rows landed. The page carries tonight's number.</li>
    </ul>
  </div>
</section>

<footer><div class="wrap" style="display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap">
  <span>Apollo · proposal · Assembly and Studio · v1 · 2026-10-01 · session 313 lane H3 · built from lanes H1 and H2 (#311)</span>
  <span>An idea drawn is not a ruling. Nothing stands until you say.</span>
</div></footer>

<div class="bar" role="region" aria-label="Your decisions"><div class="in">
  <b>Your decisions</b><span id="count">0 of 13 answered</span><span class="msg" id="msg">Saves in this browser as you go</span>
  <button type="button" class="pri" id="copy">Copy as text</button><button type="button" id="export">Export</button><button type="button" id="clear">Clear</button>
</div></div>

<script>
(function(){{
  var KEY='{KEY}';
  var PATH='{PATH}';
  var state={{}};
  try{{ state=JSON.parse(localStorage.getItem(KEY)||'{{}}')||{{}}; }}catch(e){{ state={{}}; }}
  function save(){{ try{{ localStorage.setItem(KEY, JSON.stringify(state)); }}catch(e){{}} refresh(); }}
  function now(){{ var d=new Date(),p=function(n){{return (n<10?'0':'')+n;}}; return d.getFullYear()+'-'+p(d.getMonth()+1)+'-'+p(d.getDate())+' '+p(d.getHours())+':'+p(d.getMinutes()); }}
  var calls=[].slice.call(document.querySelectorAll('.call'));
  var asked=calls.filter(function(el){{ return el.dataset.id!=='page'; }});
  function has(s){{ return s && (s.v || (s.note||'').trim()); }}
  var tb=document.querySelector('#glance-table tbody');
  asked.forEach(function(el){{
    var sec=el.closest('section'), q=el.dataset.q, n=q.split('.')[0], t=q.slice(n.length+1).trim();
    var tr=document.createElement('tr');
    tr.innerHTML='<td class="n"></td><td><a></a></td><td></td><td class="st"></td>';
    tr.children[0].textContent=n; tr.children[1].firstChild.textContent=t; tr.children[1].firstChild.href='#'+(sec?sec.id:'');
    tr.children[2].textContent=el.dataset.rec; tr.dataset.id=el.dataset.id;
    tb.appendChild(tr);
  }});
  function refresh(){{
    var n=0;
    calls.forEach(function(el){{
      var s=state[el.dataset.id]||{{}};
      if(el.dataset.id!=='page' && has(s)) n++;
      [].forEach.call(el.querySelectorAll('.chip'),function(c){{ c.classList.toggle('on', c.dataset.v===s.v); c.setAttribute('aria-pressed', c.dataset.v===s.v?'true':'false'); }});
      el.querySelector('.stamp').textContent = s.at ? 'saved '+s.at : '';
    }});
    [].forEach.call(tb.children,function(tr){{
      var s=state[tr.dataset.id]||{{}}, el=document.querySelector('.call[data-id="'+tr.dataset.id+'"]'), recChip=el.querySelector('.chip em'), recV=recChip?recChip.parentNode.dataset.v:el.dataset.rec;
      tr.children[3].textContent = s.v ? (s.v===recV ? 'Recommended' : s.v) : ((s.note||'').trim() ? 'Comment only' : 'Not answered');
    }});
    document.getElementById('count').textContent = n+' of '+asked.length+' answered';
  }}
  calls.forEach(function(el){{
    var id=el.dataset.id, s=state[id]||{{}};
    var ta=el.querySelector('textarea'); if(ta) ta.value=s.note||'';
    el.addEventListener('click',function(e){{
      var b=e.target.closest('.chip'); if(!b) return;
      var cur=state[id]||{{}}; cur.v=(cur.v===b.dataset.v)?'':b.dataset.v; cur.at=now(); state[id]=cur; save();
    }});
    el.addEventListener('input',function(e){{
      if(!e.target.dataset || e.target.dataset.f!=='note') return;
      var cur=state[id]||{{}}; cur.note=e.target.value; cur.at=now(); state[id]=cur; save();
    }});
  }});
  function text(){{
    var L=['Session 313 · Assembly and Studio · comments','','Page: '+PATH,'Copied: '+now(),''];
    calls.forEach(function(el){{
      var id=el.dataset.id, s=state[id]||{{}}, rec=el.dataset.rec||'', recChip=el.querySelector('.chip em'), recV=recChip?recChip.parentNode.dataset.v:rec;
      L.push(el.dataset.q);
      L.push('   Recommended: '+rec);
      L.push('   Chose: '+(s.v? s.v+(s.v===recV?' (the recommendation)':' (not the recommendation)') : 'not answered'));
      L.push('   Comment: '+((s.note||'').trim()? s.note.trim() : 'none'));
      L.push('');
    }});
    return L.join('\\n');
  }}
  window.__reviewText=text;
  function msg(t){{ document.getElementById('msg').textContent=t; }}
  function fallback(t){{
    var ta=document.createElement('textarea'); ta.value=t; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select();
    try{{ document.execCommand('copy'); msg('Copied. Paste it into the chat'); }}catch(e){{ msg('Copy blocked. Use Export instead'); }}
    ta.remove();
  }}
  document.getElementById('copy').onclick=function(){{
    var t=text();
    try{{ if(navigator.clipboard && navigator.clipboard.writeText){{ navigator.clipboard.writeText(t).then(function(){{msg('Copied. Paste it into the chat');}},function(){{fallback(t);}}); }} else fallback(t); }}catch(e){{ fallback(t); }}
  }};
  document.getElementById('export').onclick=function(){{
    try{{
      var blob=new Blob([text()],{{type:'text/plain'}}), a=document.createElement('a');
      a.href=URL.createObjectURL(blob); a.download='proposal-313-H3-assembly-and-studio.txt';
      document.body.appendChild(a); a.click(); setTimeout(function(){{ URL.revokeObjectURL(a.href); a.remove(); }},500);
      msg('Exported as a text file');
    }}catch(e){{ msg('Export blocked. Use Copy as text'); }}
  }};
  document.getElementById('clear').onclick=function(){{
    if(!confirm('Clear every answer on this page?')) return;
    state={{}}; save(); [].forEach.call(document.querySelectorAll('.call textarea'),function(t){{t.value='';}}); msg('Cleared');
  }};
  refresh();
}})();
</script>
</body></html>
''')
    return "".join(H)


if __name__ == "__main__":
    html = page()
    OUT.write_text(html, encoding="utf-8")
    print(OUT.relative_to(ROOT), len(html.encode()), "bytes", html.count('class="call"'), "calls")
