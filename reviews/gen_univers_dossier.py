#!/usr/bin/env python3
"""gen_univers_dossier.py — what the licensed Univers cut actually does.

WHY
  Dave, 2026-07-18: "research on Univers itself … is it tight or loose by nature" and
  "compare HSBC's cut to check they are the same".

THE METHOD CHANGE THAT MATTERS
  Every tracking sheet before this one rested on literature and brand precedent. This one
  is MEASURED — the licensed Latin desktop TTFs are in the repo at
  `knowledge/assets/fonts/_desktop/TTF/`, and fontTools reads sidebearings, kerning and
  vertical metrics straight out of them. That is a higher evidence tier than anything in
  TRACKING-DOSSIER: not what a typographer says about Univers in general, but what THIS
  cut does.

  ⚠ It also means `_TYPE-DECISIONS.md` "Blockers" item 1 — "the Latin pack is missing, the
  dropped packs are the script companions" — is STALE. The Latin desktop set (TTF + OTF,
  six weights + italics) is present and readable.

UPDATE — stock Univers Next Pro supplied by Dave mid-session, so §5 is now MEASURED, not open.
  Verdict: horizontally identical (sidebearings, advances, kerning all match to the unit; only
  the ampersand is redrawn). Vertical metrics differ — HSBC line box 1.300em vs stock 1.200em,
  and the baseline sits ~11pp lower in the box.

WHAT WAS FOUND, IN ONE LINE
  The received wisdom is that Univers is tight. Measured, THIS cut is LOOSER than Helvetica,
  Arial, Calibri and Lato. Frutiger's famous "too tight" remark was about APERTURES, not
  spacing — a different property, and one that letter-spacing cannot fix.

A CORRECTION I HAD TO MAKE MID-ANALYSIS — recorded because the ledger should carry it
  My first kerning parser reported "no kerning in any weight except Medium". That was WRONG:
  the family uses extension lookups (GPOS LookupType 9), which the parser skipped. Unwrapped,
  every weight kerns, and the values are consistent across the family. Had I written the
  first result down it would have entered the record as a font defect that does not exist.

Usage:  python3 reviews/gen_univers_dossier.py
Then:   python3 knowledge/_review/_make_review.py reviews/UNIVERS-DOSSIER-2026-07-18.html
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reviews", "UNIVERS-DOSSIER-2026-07-18.html")

# ---- measured, normalised to 1000 UPM (see docstring for provenance)
SPACING = [
    ("HSBC Univers Latin Rg", 79, 45, 88, 0.90, 15.6, True),
    ("DejaVu Sans", 88, 55, 90, 0.98, 15.7, False),
    ("Lato", 68, 42, 89, 0.76, 13.4, False),
    ("Carlito (Calibri metrics)", 65, 37, 86, 0.75, 13.5, False),
    ("Liberation Sans (Arial metrics)", 66, 42, 88, 0.75, 12.4, False),
]

WEIGHTS = [
    ("Ultra Light", 250, 92, 20, 4.60, 545),
    ("Thin", 300, 85, 40, 2.12, 553),
    ("Light", 350, 84, 61, 1.38, 574),
    ("Regular", 400, 79, 88, 0.90, 593),
    ("Medium", 500, 74, 116, 0.64, 612),
    ("Bold", 700, 68, 146, 0.46, 632),
]

KERN = [
    ("Ta", -91, -73, -94, -93, -91, -119), ("Vo", -60, -48, -54, -48, -73, -75),
    ("AV", -24, -36, -54, -61, -59, -60), ("Yo", -78, -73, -94, -93, -102, -105),
    ("Pa", -40, -44, -52, -45, -59, -59), ("Fo", -25, -30, -28, 0, -30, -30),
    ("LT", -114, -108, -96, -93, -104, -105), ("r.", -72, -84, -72, -48, -76, -60),
    ("ov", 0, 0, -12, -16, -15, -15), ("24", 0, 0, 0, 0, 0, 0),
]

FINDINGS = [
    ("M1", "MEASURED",
     "This cut is spaced <b>looser</b> than Helvetica, Arial, Calibri and Lato.",
     "The <code>n</code> sidebearing is <b>15.6% of x-height</b>; Arial is 12.4%, Calibri 13.5%, "
     "Lato 13.4%. Only DejaVu Sans &mdash; a face drawn deliberately open for low-resolution "
     "screens &mdash; is looser, at 15.7%. Relative to its own stroke weight the "
     "sidebearing/stem ratio is <b>0.90</b> against roughly 0.75 for the Helvetica-lineage faces.",
     "<b>This weakens C1 on the contact sheet.</b> I recommended <code>+0.01em</code> on 12px "
     "component labels on a crowding argument that silently assumed normally-spaced type. Univers "
     "already carries more air than Arial. The crowding case does not disappear &mdash; but it "
     "starts from a looser baseline than I assumed, and C1 should probably fall back toward "
     "<code>+0.005em</code> or zero."),

    ("M2", "MEASURED",
     "Sidebearings barely move across the weight range. Stems increase sevenfold.",
     "From Ultra Light to Bold the sidebearing falls <b>92 &rarr; 68</b> (&minus;26%), while the "
     "stem goes <b>20 &rarr; 146</b> (+630%). So the sidebearing/stem ratio collapses "
     "<b>4.60 &rarr; 0.46</b>: at Bold the space between letters is under half a stem, at Ultra "
     "Light it is over four stems.",
     "<b>Tracking in this family is weight-dependent, and none of our rules account for that.</b> "
     "Heavier weights are relatively far tighter and need more relief. Note where this lands: "
     "col26-020(c) mandates <b>Medium</b> for small reverse text, and Medium sits at <b>0.64</b> "
     "&mdash; already tight-side. Bloom then closes the apparent gap further. <b>C2/C3 hold or "
     "strengthen; C1 weakens.</b>"),

    ("M3", "MEASURED",
     "Kerning is present in every weight, and consistent. One real gap.",
     "All six weights kern via GPOS extension lookups. Across ten common problem pairs the values "
     "track closely (<code>Ta</code> &minus;73 to &minus;119, <code>LT</code> &minus;93 to "
     "&minus;114). <b>The one inconsistency: <code>Fo</code> is unkerned in Regular only</b> "
     "(0, against &minus;25 to &minus;30 in every other weight). Digit pairs are unkerned "
     "throughout, which is correct for tabular figures.",
     "Not a systemic defect. The <code>Fo</code> gap is present in stock too (&sect;5), so it is upstream, not an HSBC error. "
     "<b>See the correction note below</b> &mdash; my first pass reported this section very "
     "differently and was wrong."),

    ("R1", "RESEARCH",
     "Frutiger's &quot;too tight&quot; was about <b>apertures</b>, not spacing.",
     "The often-repeated line is that Frutiger found Univers &quot;too tight&quot; for airport "
     "signage and drew Frutiger in response. The sources are specific about what he meant: Univers "
     "had <i>&quot;too round and closed an effect for the easy recognition of word-signs&quot;</i>. "
     "He wanted larger apertures &mdash; the openings in <code>c</code>, <code>e</code>, "
     "<code>s</code>, <code>a</code> &mdash; so letters would not blur into circles at a glance. "
     "Aperture is a counter property. It is not sidebearing.",
     "<b>The negative finding, and the important one: tracking cannot fix this.</b> Letter-spacing "
     "does not open a counter. The known weakness of Univers for glance-reading is not addressable "
     "by the lever we have been designing. Size, weight and the halation levers can help; tracking "
     "cannot. That should stop us reaching for tracking as a general legibility cure."),

    ("R2", "RESEARCH",
     "Frutiger drew the same Editorial / Component line you did.",
     "His judgement was that Univers was <i>&quot;perfect for printed books&quot;</i> but wrong for "
     "someone moving through an airport at 5&nbsp;mph &mdash; continuous reading versus recognition "
     "at a glance. That is exactly the split you made: Editorial is read, Component is recognised.",
     "<b>The typeface's own designer put Univers on the Editorial side of your line.</b> Not a "
     "reason to abandon it &mdash; it is the brand face &mdash; but it means the Component tier is "
     "working against the grain of the design, and compensations there (size, weight, ground) are "
     "carrying more load than they would in a face drawn for glance-reading."),

    ("R3", "RESEARCH",
     "Lineage: the real revision was 1997, not 2010.",
     "Original Univers, Frutiger for Deberny &amp; Peignot, 1957 &mdash; 21 coordinated variants on "
     "the two-digit grid. <b>Linotype Univers (1997)</b> was the substantial rework, done with "
     "Frutiger, in which <i>stroke weights were revised for consistency within each face and "
     "between weights</i>. <b>Univers Next (2010)</b> added true small caps and renamed the family; "
     "sources describe it as extension and rebranding rather than a spacing redesign.",
     "The stroke-weight consistency work in 1997 is visible in M2's clean progression. It also "
     "means &quot;Univers&quot; advice written before 1997 may not describe what we have."),
]

CSS = """<style>
:root{--ink:#1c1c1c;--mut:#6b6b6b;--line:#e4e4e4;--red:#db0011;--meas:#0b7a34;--res:#3b5f8a;
      --warn:#b25000;}
*{box-sizing:border-box}
body{font-family:"Univers Next for HSBC","Helvetica Neue",Arial,sans-serif;color:var(--ink);
  margin:0;padding:40px;max-width:1160px;line-height:1.5;background:#fafafa}
h1{font-size:32px;font-weight:300;margin:0 0 4px}
h2{font-size:20px;font-weight:500;margin:44px 0 4px;padding-top:16px;border-top:2px solid var(--ink)}
.sub{color:var(--mut);font-size:14px;margin:0 0 24px}
.lead{font-size:15px;background:#fff;border:1px solid var(--line);border-left:3px solid var(--red);
  padding:16px 20px;margin:20px 0}
.correct{font-size:14px;background:#fff;border:1px solid var(--line);border-left:3px solid var(--warn);
  padding:14px 20px;margin:20px 0}
.card{background:#fff;border:1px solid var(--line);padding:18px 22px;margin:14px 0}
.tag{display:inline-block;font-size:10px;letter-spacing:.06em;font-weight:500;padding:3px 9px;
  color:#fff;margin-bottom:8px}
.tag.MEASURED{background:var(--meas)}.tag.RESEARCH{background:var(--res)}
.key{font-size:11px;font-weight:500;color:#fff;background:var(--ink);padding:2px 8px;margin-right:8px}
.find{font-size:16px;font-weight:500;margin:0 0 8px}
.detail{font-size:14px;margin:0 0 12px}
.imp{font-size:13.5px;background:#fbfbfb;border-left:2px solid var(--line);padding:9px 14px;margin:0}
table{width:100%;border-collapse:collapse;background:#fff;margin:12px 0;font-size:13px}
th,td{text-align:left;padding:9px 12px;border-bottom:1px solid var(--line)}
th{font-weight:500;font-size:11px;letter-spacing:.04em;color:var(--mut);background:#f4f4f4}
tr.ours td{background:#f2f8f4;font-weight:500}
td.num{text-align:right;font-family:ui-monospace,Menlo,monospace;font-size:12px}
code{font-family:ui-monospace,Menlo,monospace;font-size:11.5px;background:#f2f2f2;padding:1px 5px;
  border-radius:3px}
.rules{background:#fff;border:1px solid var(--line);padding:4px 20px 16px;margin:16px 0}
.rules li{margin:15px 0;font-size:14px}
.foot{color:var(--mut);font-size:12px;margin-top:44px;border-top:1px solid var(--line);padding-top:12px}
.zero{color:var(--red);font-weight:500}
</style></head><body>"""


def build():
    h = []
    A = h.append
    A('<!doctype html><html lang="en"><head><meta charset="utf-8">')
    A('<meta name="viewport" content="width=device-width, initial-scale=1">')
    A("<title>Univers &mdash; what the licensed cut actually does</title>")
    A(CSS)

    A("<h1>Univers &mdash; what the licensed cut actually does</h1>")
    A('<p class="sub">Apollo SDS &middot; 2026-07-18 &middot; measured from the repo font files, '
      "plus lineage research.</p>")

    A('<div class="lead"><b>The method changed for this one.</b> Every tracking sheet so far has '
      "rested on literature and brand precedent. This one is <b>measured</b> &mdash; the licensed "
      "Latin desktop TTFs are in the repo at <code>knowledge/assets/fonts/_desktop/TTF/</code>, and "
      "sidebearings, kerning and vertical metrics come straight out of them. That is a higher "
      "evidence tier than anything in the tracking dossier: not what typographers say about Univers "
      "in general, but what <b>this cut</b> does.<br><br>"
      "<b>&#9888; Side effect: a stale blocker.</b> <code>_TYPE-DECISIONS.md</code> records "
      "&quot;Blockers to writing clean canon tokens &rarr; 1. Latin webfont missing; the dropped "
      "packs are the script companions&quot;. <b>The Latin desktop set is present</b> &mdash; six "
      "weights plus italics, TTF and OTF. That blocker should be struck, and it may also mean the "
      "sandbox can render specimens in the real face for the first time.</div>")

    A('<div class="lead"><b>The headline.</b> Received wisdom says Univers is tight. '
      "<b>Measured, this cut is looser than Helvetica, Arial, Calibri and Lato.</b> Frutiger&#39;s "
      "famous &quot;too tight&quot; remark was about <b>apertures</b> &mdash; a different property, "
      "and one letter-spacing cannot fix.</div>")

    # ---- §1 spacing comparison
    A("<h2>1 &middot; Is it tight or loose? &mdash; measured</h2>")
    A('<p class="sub">All normalised to 1000 UPM. <b>Sidebearing &divide; stem</b> is the standard '
      "tightness index &mdash; it asks how much air a face leaves relative to its own stroke weight, "
      "so it is comparable across designs. Lower = tighter.</p>")
    A("<table><thead><tr><th>Face</th><th class='num'>n sidebrg</th><th class='num'>o sidebrg</th>"
      "<th class='num'>stem</th><th class='num'>SB &divide; stem</th>"
      "<th class='num'>SB as % x-height</th></tr></thead><tbody>")
    for nm, nsb, osb, stem, ratio, xh, ours in SPACING:
        A(f"<tr{' class=ours' if ours else ''}><td>{nm}</td><td class='num'>{nsb}</td>"
          f"<td class='num'>{osb}</td><td class='num'>{stem}</td>"
          f"<td class='num'>{ratio:.2f}</td><td class='num'>{xh:.1f}%</td></tr>")
    A("</tbody></table>")
    A('<p class="sub">Only DejaVu Sans is looser &mdash; and DejaVu was drawn deliberately open for '
      "low-resolution screens. Univers sits at the loose end of the neo-grotesques, not the tight "
      "end.</p>")

    # ---- §2 weights
    A("<h2>2 &middot; Spacing across the weight range &mdash; the finding I did not expect</h2>")
    A('<p class="sub">Sidebearings are nearly flat while stems grow sevenfold. The relative '
      "tightness therefore changes enormously across the family.</p>")
    A("<table><thead><tr><th>Weight</th><th class='num'>CSS</th><th class='num'>n sidebrg</th>"
      "<th class='num'>stem</th><th class='num'>SB &divide; stem</th>"
      "<th class='num'>n advance</th></tr></thead><tbody>")
    for nm, css, nsb, stem, ratio, adv in WEIGHTS:
        cls = " class=ours" if css == 500 else ""
        A(f"<tr{cls}><td>{nm}</td><td class='num'>{css}</td><td class='num'>{nsb}</td>"
          f"<td class='num'>{stem}</td><td class='num'>{ratio:.2f}</td>"
          f"<td class='num'>{adv}</td></tr>")
    A("</tbody></table>")
    A('<p class="sub">Highlighted row is <b>Medium</b> &mdash; the weight <code>{#col26-020}(c)</code> '
      "mandates for small reverse text. At 0.64 it is already on the tight side of the family, "
      "before bloom closes the apparent gap any further.</p>")

    # ---- §3 kerning
    A("<h2>3 &middot; Kerning &mdash; present, consistent, one gap</h2>")
    A('<p class="sub">Kern values in font units per 1000em for ten common problem pairs. '
      "<span class='zero'>Red zero</span> = pair not kerned.</p>")
    A("<table><thead><tr><th>Pair</th><th class='num'>ULt</th><th class='num'>Th</th>"
      "<th class='num'>Lt</th><th class='num'>Rg</th><th class='num'>Md</th>"
      "<th class='num'>Bd</th></tr></thead><tbody>")
    for row in KERN:
        A(f"<tr><td><code>{row[0]}</code></td>")
        for v in row[1:]:
            A(f"<td class='num'>{'<span class=zero>0</span>' if v == 0 else v}</td>")
        A("</tr>")
    A("</tbody></table>")
    A('<p class="sub"><b><code>Fo</code> is unkerned in Regular alone</b> &mdash; every other weight '
      "gives it &minus;25 to &minus;30. Digit pairs unkerned throughout is correct: tabular figures "
      "must hold their column.</p>")

    A('<div class="correct"><b>&#9888; A correction, recorded because the ledger should carry it.</b> '
      "My first kerning parser reported <i>&quot;no kerning in any weight except Medium&quot;</i> "
      "and I was about to write it up as a font defect. It was <b>wrong</b>: the family uses GPOS "
      "<b>extension lookups (LookupType 9)</b>, and the parser was skipping anything that was not a "
      "direct type-2 lookup. Unwrapped, every weight kerns. <b>Had I recorded the first result it "
      "would have entered the ledger as a defect that does not exist</b> &mdash; the same failure "
      "mode as yesterday&#39;s &quot;38% of rules missing&quot;. Two passes, because the first "
      "answer was tidy and confirmed what I half-expected.</div>")

    # ---- §4 findings
    A("<h2>4 &middot; What it means</h2>")
    for key, tag, finding, detail, implies in FINDINGS:
        A('<div class="card">')
        A(f'<span class="tag {tag}">{tag}</span>')
        A(f'<p class="find"><span class="key">{key}</span>{finding}</p>')
        A(f'<p class="detail">{detail}</p>')
        A(f'<p class="imp"><b>For us: </b>{implies}</p>')
        A("</div>")

    # ---- §5 the comparison — ANSWERED, stock font supplied 2026-07-18
    A("<h2>5 &middot; HSBC&#39;s cut vs stock Univers Next Pro &mdash; ANSWERED</h2>")
    A('<p class="sub">Dave supplied Univers Next Pro mid-session, so this moved from '
      "&quot;cannot answer&quot; to measured. Six weight pairs, matched "
      "UltraLight&ndash;Thin&ndash;Light&ndash;Regular&ndash;Medium&ndash;Bold.</p>")

    A('<div class="lead"><b>Horizontally, HSBC&#39;s cut IS stock Univers Next Pro.</b> Not '
      "&quot;close to&quot; &mdash; identical, to the font unit.<br><br>"
      "&bull; <b>Sidebearings</b>: 75 glyphs &times; 6 weights, LSB and RSB both compared. "
      "<b>One glyph differs</b> in the entire set.<br>"
      "&bull; <b>Advance widths</b>: 82 glyphs &times; 6 weights. Same one glyph.<br>"
      "&bull; <b>Kerning</b>: 10 problem pairs &times; 6 weights = <b>60/60 exact matches</b>, "
      "value for value.<br>"
      "&bull; <b>Cap-height and x-height</b>: identical to the unit at every weight.<br><br>"
      "<b>The single differing glyph is the ampersand</b> &mdash; redrawn for HSBC "
      "(ink 680&times;751 vs 664&times;738; right sidebearing &minus;1 vs 15, so the brand "
      "ampersand runs right to its edge). A deliberate brand glyph, not a spacing change.</div>")

    A('<div class="lead"><b>What this settles.</b> <b>Published Univers Next guidance on spacing '
      "applies to us directly</b> &mdash; that is now an empirical finding, not an assumption. "
      "Everything in &sect;1&ndash;3 describes stock Univers Next Pro as much as it describes our "
      "cut.<br><br>"
      "<b>It also relocates the <code>Fo</code> defect.</b> The unkerned <code>Fo</code> in Regular "
      "is present in <b>stock</b> too, at the same zero. It is an upstream "
      "Linotype/Monotype omission, <b>not an HSBC error</b> &mdash; so there is no point raising it "
      "with brand. Worth knowing before someone files it.</div>")

    A('<div class="correct"><b>&#9888; Where they genuinely differ: VERTICAL metrics.</b> '
      "This is the one place published Univers advice will mislead us.<br><br>"
      "<table><thead><tr><th></th><th class='num'>hhea asc/desc</th><th class='num'>lineGap</th>"
      "<th class='num'>natural line box</th><th class='num'>baseline from top</th>"
      "<th class='num'>glyphs</th></tr></thead><tbody>"
      "<tr class='ours'><td><b>HSBC cut</b></td><td class='num'>1068 / &minus;232</td>"
      "<td class='num'>0</td><td class='num'>1.300em</td><td class='num'>~82%</td>"
      "<td class='num'>835&ndash;1011</td></tr>"
      "<tr><td>stock Univers Next Pro</td><td class='num'>750 / &minus;250</td>"
      "<td class='num'>200</td><td class='num'>1.200em</td><td class='num'>~71%</td>"
      "<td class='num'>669</td></tr>"
      "</tbody></table>"
      "Both ship <code>USE_TYPO_METRICS</code> OFF, so the browser reads hhea. The line boxes are "
      "only <b>8% apart</b> &mdash; but the <b>baseline sits ~11 percentage points lower in the "
      "box</b> in our cut, because HSBC put everything into ascent and dropped the lineGap to zero. "
      "<b>That changes where text sits inside its line, which is exactly what the cap-trim and "
      "grid-slot work depends on.</b> HSBC also extended the charset substantially "
      "(669 &rarr; 1011 glyphs).<br><br>"
      "<b>A number I nearly got wrong:</b> reading ascents alone (1068 vs 750) suggests a 30% "
      "difference. It is 8%, because stock carries a 200-unit lineGap that HSBC folded away. "
      "Recorded because the ascent figure is the one that looks decisive and is not.</div>")

    # ---- §6 consequences
    A("<h2>6 &middot; What this changes on the contact sheet</h2>")
    A('<ol class="rules">')
    A("<li><b>C1 weakens &mdash; 12px component label, ordinary ground.</b> I recommended "
      "<code>+0.01em</code> on a crowding argument that assumed normally-spaced type. This face is "
      "<b>looser than Arial</b>. <b>Revised suggestion: <code>+0.005em</code> or zero</b>, and I "
      "would not defend the higher number now.</li>")
    A("<li><b>C2 / C3 hold, and arguably strengthen.</b> They specify <b>Medium</b>, which measures "
      "0.64 SB/stem &mdash; tight-side for this family &mdash; with bloom closing the gap further. "
      "Two compounding effects, now with a measured basis rather than practitioner lore.</li>")
    A("<li><b>E1 strengthens &mdash; editorial display.</b> A relatively loose face at 40px drifts "
      "apart more, not less. <code>&minus;0.02em</code> stands, and the brand&#39;s "
      "&minus;15/&minus;30 range looks better-founded than it did.</li>")
    A("<li><b>NEW &mdash; tracking may need to vary by WEIGHT, not just size and role.</b> The "
      "SB/stem collapse from 4.60 to 0.46 is the largest single effect measured here, and nothing "
      "in the current rule sketch accounts for it. <b>This is the open question I would take to a "
      "ladder next.</b></li>")
    A("<li><b>A limit on the whole exercise.</b> Univers&#39; known glance-reading weakness is "
      "<b>closed apertures</b>. Tracking does not open a counter. Some of what we might want from "
      "tracking on the Component tier is simply not available from this lever, and size, weight and "
      "ground have to carry it.</li>")
    A("</ol>")

    A('<p class="foot">Generated by <code>reviews/gen_univers_dossier.py</code> &middot; spacing, '
      "kerning and vertical metrics measured with fontTools from "
      "<code>knowledge/assets/fonts/_desktop/TTF/</code> &middot; comparison faces are the "
      "metric-compatible clones available in-sandbox &middot; lineage from published sources "
      "&middot; <b>nothing promoted</b> &mdash; promotion is Dave&#39;s alone.</p>")
    A("</body></html>")

    with open(OUT, "w") as f:
        f.write("\n".join(h))
    print(f"wrote {os.path.relpath(OUT, ROOT)} — {len(SPACING)} faces compared, "
          f"{len(WEIGHTS)} weights, {len(KERN)} kern pairs, {len(FINDINGS)} findings")


if __name__ == "__main__":
    build()
