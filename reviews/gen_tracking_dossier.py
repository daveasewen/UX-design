#!/usr/bin/env python3
"""gen_tracking_dossier.py — letter-spacing / tracking: evidence dossier.

WHY THIS EXISTS
  Dave, 2026-07-18: "research on the effect of letter spacing on readability … I want this
  to be the most well crafted set of Typography rules."

  Today the canon governs letter-spacing NOWHERE. `canon/type.css` declares no
  letter-spacing on any composite; the token store carries a letter-spacing ramp that is
  ZERO at every size except font-00; and 24 hardcoded values live loose in the corpus.
  The only rule on the books is {#type26-018} — "no wide kerning that breaks legibility;
  not too tight either" — tagged [TASTE], with no number. That is the same shape dv-019
  had before it got its 135°, and col26-020 had before it got its 0.72.

STRUCTURE — evidence is TIERED, and the tier is part of the record
  Sheets that mix "replicated experimental finding" with "what typographers say" produce
  rules nobody can later audit. Each finding below carries its tier. Where the evidence is
  contested it is written as contested, including where that is inconvenient.

WHAT IT DELIBERATELY DOES NOT DO
  It proposes no promoted values. Every number is a CANDIDATE for Dave's ruling, and the
  thresholds this system actually enforces have all come from what Dave could SEE
  (dv-019's 135°, col26-020's 0.72) — not from literature. The literature's job here is to
  say where to point the specimen, not to set the number.

Usage:  python3 reviews/gen_tracking_dossier.py
Then:   python3 knowledge/_review/_make_review.py reviews/TRACKING-DOSSIER-2026-07-18.html
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reviews", "TRACKING-DOSSIER-2026-07-18.html")

# ---------------------------------------------------------------- the medium question
# Dave, 2026-07-18: "what the display was — I suspect screens and print might be different
# especially for astigmatism." He was right, and it cuts at the dossier's foundation.
MEDIUM = [
    ("Zorzi 2012 &mdash; the dyslexia headline &mdash; was <b>PRINT</b>.",
     "Times-Roman, <b>14 point</b>, inter-letter spacing widened by <b>2.5pt on a 14pt body</b> "
     "&mdash; about <b>18% of body size</b>, i.e. roughly <code>+0.18em</code>. Paper. Serif face. "
     "Italian and French children aged 8&ndash;14.",
     "That is <b>50% above WCAG 1.4.12's 0.12em ceiling</b>, on paper, in a serif, with children. "
     "The distance to a 14px Univers label on an emissive screen is enormous. The finding may still "
     "hold on screen &mdash; but nothing in that study says so, and I presented it yesterday as "
     "though it did."),

    ("Butterick is a <b>PRINT</b> typographer. So is type26-016.",
     "The 5&ndash;12% caps range comes from book and document typography. Our own brand rule states "
     "tracking in <b>InDesign thousandths-of-an-em</b> and leading in <b>points</b> "
     "(&quot;50pt &rarr; 53pt&quot;) &mdash; it is a print specification that was never re-derived "
     "for screen.",
     "Both are still useful, but as <b>inherited practice</b>, not screen evidence. Contradiction 1 "
     "gets more interesting: maybe the token store zeroed the ramp because nobody could say what the "
     "print numbers meant digitally."),

    ("Halation is <b>SCREEN-SPECIFIC</b> &mdash; and it is the mechanism behind col26-020.",
     "Print and e-ink <b>reflect</b> light; displays <b>emit</b> it. Emitted light from bright "
     "letterforms scatters within the eye and blooms across the boundary into the dark ground. "
     "Paper does not do this. Level&nbsp;Access put it plainly: white text on pure black creates "
     "&quot;a visual fuzzing effect for people with astigmatism called halation&quot; &mdash; and "
     "<b>&quot;automated contrast-ratio checkers would not detect a problem&quot;</b>.",
     "<b>That is your badge, described by an accessibility body, three years before you saw it.</b> "
     "It also independently confirms the thing that made col26-020 worth writing: the effect does "
     "not fold into the contrast gate. Our rule was right and is better-founded than we knew."),

    ("Prevalence is high enough to change the priority.",
     "WHO: refractive errors account for <b>43% of global visual impairment</b>. In a UK study of "
     "11,000+ spectacle wearers, <b>47.4%</b> had astigmatism of 0.75D or greater in at least one "
     "eye. Roughly <b>half the population</b> has at least 0.5D. Halation is reported as worst on "
     "body text at <b>14&ndash;16px</b>.",
     "14&ndash;16px is exactly the band col26-020(c) governs, and exactly where the retrofit's 100 "
     "declarations sit. Under ADR-0004 this stops being a refinement and becomes a "
     "<b>mainstream legibility case</b>."),

    ("&#9888; The method caveat &mdash; thresholds observed by one pair of eyes.",
     "0.72 and 135&deg; were both fixed by what you could see, on your screen. That has been the "
     "right call &mdash; it is why they are gateable at all. But halation severity varies with the "
     "observer's own refraction, and with panel type, brightness and subpixel rendering.",
     "Not an argument against the method &mdash; an argument for <b>recording the conditions</b>. "
     "A threshold with its display, brightness and observer noted can be re-tested later; one "
     "without them cannot be distinguished from a preference. Cheap to add now, impossible to "
     "reconstruct afterwards."),
]

# ---------------------------------------------------------------- evidence
# (tier, tier_class, finding, detail, what it implies for us)
EVIDENCE = [
    ("SETTLED", "s",
     "Capitals need +5&ndash;12% tracking. Lowercase does not. <span class='med'>PRINT-DERIVED</span>",
     "Butterick states it as a hard CSS range: <code>0.05em</code>&ndash;<code>0.12em</code> for "
     "all-caps and small-caps, &quot;particularly important at small sizes&quot;. Capitals are "
     "spaced to sit beside lowercase; set together they read too tight. This is the least "
     "contested statement in the whole of typographic practice.",
     "We already do this &mdash; four tranches carry <code>.05em</code> on uppercase runs, dead "
     "centre of the range. <b>But see contradiction 4: those runs should not be uppercase at all.</b>"),

    ("SETTLED", "s",
     "Tracking should tighten as size rises &mdash; optical sizing. <span class='med'>BOTH</span>",
     "At large sizes the gaps between glyphs grow faster than the strokes, so display type "
     "&quot;drifts apart&quot; at the spacing that suits body text. The inverse holds below "
     "~9pt, where extra tracking keeps counters distinct. Apple ships this as two physical "
     "fonts &mdash; SF&nbsp;Pro&nbsp;Text under ~20px, SF&nbsp;Pro&nbsp;Display above, the "
     "Display cut tracked tighter.",
     "This is a <b>ramp</b>, not a constant &mdash; tracking is a function of size, exactly like "
     "the weight rule col26-020(c) turned out to be. Our token store has the ramp and sets it to "
     "zero at every step."),

    ("SETTLED", "s",
     "WCAG 1.4.12 is a survival requirement, not a design target. <span class='med'>SCREEN</span>",
     "Level AA. Content must lose no meaning or function when the USER overrides letter-spacing "
     "to <code>0.12em</code> (plus line-height 1.5, word-spacing 0.16em, paragraph 2em). "
     "It does not ask us to ship 0.12em. It asks that nothing breaks when someone else sets it.",
     "<b>Directly gateable</b>, and currently ungated. If we ship negative tracking the jump to "
     "0.12em is larger, so tight display type raises overflow risk in exactly the components "
     "with least slack. A gate can re-render at the 1.4.12 values and diff for clipping."),

    ("CONTESTED", "c",
     "For general readers, wider tracking does not speed reading &mdash; and can slow it. <span class='med'>SCREEN &mdash; eye-tracking</span>",
     "Reading speed peaks at or near a font's designed spacing and falls off in BOTH directions. "
     "The 2020 Frontiers study found wider spacing shortened fixation durations for everyone, "
     "yet <b>lowered</b> words-per-minute for fast readers &mdash; it cut word-skipping and added "
     "fixations. Slower readers benefited more. Wider spacing also pushes text further into "
     "peripheral vision, where acuity is worse; that partly cancels the crowding relief.",
     "Kills any &quot;more air = more readable&quot; instinct. Positive tracking on body text needs "
     "a specific justification (caps, small size, reverse) &mdash; it is not a free improvement."),

    ("CONTESTED", "c",
     "Dyslexia: real effect in the headline study, poor replication since. <span class='med'>PRINT</span>",
     "Zorzi et al. (PNAS 2012) found extra-large spacing roughly doubled accuracy and raised "
     "speed >20% in dyslexic children 8&ndash;14, with no training &mdash; attributed to abnormal "
     "sensitivity to crowding. <b>The study was PRINT</b> &mdash; Times-Roman 14pt, spacing widened "
     "2.5pt on a 14pt body (~<code>+0.18em</code>). Later work has struggled to reproduce it; one "
     "study found no effect on accuracy, comprehension or speed in either dyslexic or typical "
     "readers. The 2020 slow-reader finding is consistent with a real but narrower effect.",
     "<b>Handle honestly.</b> Two separate problems: replication is weak, AND the medium is wrong "
     "&mdash; paper, serif, children, at a tracking 50% above WCAG&#39;s ceiling. Nothing in it "
     "speaks to a 14px sans label on an emissive screen. The defensible position stays "
     "<i>user-adjustable</i> spacing &mdash; which 1.4.12 already requires &mdash; not shipping "
     "wide tracking by default."),

    ("PRACTITIONER", "p",
     "Reverse type reads tighter than it is; open the tracking to compensate. <span class='med'>SCREEN</span>",
     "Consistent practitioner advice, not experimental: light-on-dark letterforms bloom into the "
     "surrounding dark, closing the apparent gaps. Standard remedy is to open tracking, increase "
     "leading, and <i>reduce</i> weight. The same sources give a third lever &mdash; dim the text "
     "from <code>#FFF</code> toward <code>#CCC</code>&ndash;<code>#D4D4D4</code> to cut the bloom.",
     "<b>This is {#col26-020} again, from the other side.</b> Same phenomenon Dave observed on the "
     "badge. Our rule has two levers (ground chroma, ground luminance); the literature offers two "
     "more &mdash; <b>text luminance</b> and <b>tracking</b>. Both are candidates to extend it."),

    ("TENSION", "t",
     "Reverse-type practice says LIGHTER weight. Our col26-020(c) says Medium minimum.",
     "Practitioner guidance for reversed type is to drop weight, because bloom thickens strokes. "
     "col26-020(c), from Dave's own observation, sets Medium (500) as the floor at 12&ndash;16px "
     "and Light (300) at 20px.",
     "<b>Probably not a real conflict &mdash; probably a size split.</b> The reverse-type advice is "
     "written for display sizes; col26-020(c) was observed at 12&ndash;20px, and its weights already "
     "FALL as size rises. Read together they may be one curve. <b>Worth testing, not worth "
     "resolving on paper.</b>"),
]

# ---------------------------------------------------------------- our own contradictions
CONTRA = [
    ("1", "The token store flattens the brand rule to zero.",
     "<code>tokens/typography.json</code> &rarr; <code>letter-spacing</code> is <b>0 at every "
     "size</b> except <code>font-00</code> = &minus;1. But brand {#type26-016} specifies Latin "
     "headlines at <b>&minus;15 to &minus;30</b> tracking and body at <b>&minus;5 to &minus;10</b> "
     "&mdash; InDesign thousandths-of-an-em, i.e. <code>&minus;0.015</code> to "
     "<code>&minus;0.030em</code> and <code>&minus;0.005</code> to <code>&minus;0.010em</code>. "
     "The tokens do not carry the brand standard; they erase it.",
     "Reconcile. Either the export dropped it or the brand rule was never applied digitally."),

    ("2", "Authors are hand-applying the brand rule the tokens don't carry.",
     "<code>Headers</code>, <code>Hero</code>, <code>Navigations</code>, <code>Account-card</code> "
     "and <code>DataViz</code> all set <code>&minus;.01em</code> or <code>&minus;.015em</code> by "
     "hand &mdash; squarely inside type26-016's headline range. Somebody knew the rule and applied "
     "it manually because the system offered no way to inherit it.",
     "Evidence FOR the ramp being real. Retrieval-not-recall: the value is right, the mechanism "
     "is missing."),

    ("3", "The composites are silent, so 24 values float free.",
     "<code>canon/type.css</code> declares <b>no letter-spacing on any composite</b>. So every "
     "tracking decision in the library is a hardcoded local override &mdash; 24 of them, seven "
     "distinct values, governed by nothing. Butterick's own advice is that letterspacing belongs "
     "<i>in the style definition</i>.",
     "This is the same gap the TYPE-002 retrofit exists to close, one property over. Whatever "
     "shape the tracking rule takes, it belongs ON the composites."),

    ("4", "&#9888; Four files carry uppercase past a BLOCKING gate.",
     "<code>Tranche-3</code> (&times;2), <code>-5</code>, <code>-6</code>, <code>-8</code> contain "
     "<code>text-transform:uppercase</code>. {#type26-019} bans uppercase outside acronyms "
     "brand-wide &mdash; <b>on a dyslexia rationale</b> &mdash; and was promoted from advisory to "
     "<b>blocking</b> by Dave's 2026-07-02 ruling. It doesn't fire because "
     "<code>_validate_snippets.py</code> globs <code>snippets/*.reference.html</code> only. "
     "<b><code>_proforma/</code> is outside its scope.</b>",
     "<b>A gate blind-spot, not a design question</b> &mdash; same class as the type gate reporting "
     "clean on the badge that motivated it, and Cards scoring 9/9 in June. Found incidentally while "
     "grepping for tracking. Fix is independent of every ruling on this sheet."),
]

# ---------------------------------------------------------------- questions
QUESTIONS = [
    ("T1", "Is tracking a ramp, or a constant?",
     "The optical-size evidence says tracking is a function of size &mdash; negative at display, "
     "zero through body, positive below ~12px. That makes it a per-step token, like line-height. "
     "The alternative is one value plus named exceptions (caps, reverse). "
     "<b>[ per-size ramp / constant + exceptions ]</b>"),

    ("T2", "Whose numbers &mdash; brand's, or observed?",
     "type26-016 already gives numbers (&minus;15/&minus;30 headline, &minus;5/&minus;10 body) but "
     "they are print numbers, and this system's enforced thresholds have all come from what you "
     "could see on screen. Adopt the brand numbers as the digital ramp, or cut a specimen and pick "
     "the way you picked 0.72 and 135&deg;? "
     "<b>[ adopt brand / observe on specimen / brand as start, confirm by eye ]</b>"),

    ("T3", "Does col26-020 gain a tracking leg &mdash; and a text-luminance leg?",
     "The reverse-type literature describes your badge effect exactly, and offers two levers you "
     "don't have: <b>open the tracking</b>, and <b>dim the text off pure white</b>. Both fit "
     "&quot;reduce the extremity of the edge&quot; without adding contrast. "
     "<b>[ extend col26-020 / keep separate / specimen it first ]</b>"),

    ("T4", "Do we gate WCAG 1.4.12 survival?",
     "Distinct from every other question here: not what we ship, but whether we break when a user "
     "overrides to 0.12em. Testable by re-rendering at the 1.4.12 values and diffing for clipping "
     "&mdash; and it gets sharper if we adopt negative tracking. "
     "<b>[ build the gate / log as debt ]</b>"),

    ("T5", "How do we speak about dyslexia and spacing?",
     "The headline study is strong and the replications are weak. Given ADR-0004 the temptation is "
     "to claim the benefit. The defensible line is user-adjustability &mdash; 1.4.12 &mdash; rather "
     "than shipping wide tracking on a contested finding. Your call, and you have standing here "
     "that the literature doesn't. "
     "<b>[ user-adjustable only / ship wider small-text tracking / specimen it on yourself ]</b>"),

    ("T7", "Do observed thresholds start carrying their conditions?",
     "Prompted by your own question. 0.72 and 135&deg; were fixed by eye, on your screen &mdash; "
     "and halation severity varies with the observer&#39;s refraction and with panel, brightness "
     "and subpixel rendering. Recording display + brightness + observer alongside each observed "
     "number costs a line; reconstructing it afterwards is impossible. It would also let a future "
     "session tell an observed threshold from a preference. "
     "<b>[ add to the ruling template / not worth it ]</b>"),

    ("T6", "The uppercase blind-spot &mdash; confirm the fix.",
     "Four <code>_proforma</code> files breach a blocking rule the gate cannot see. Two parts: "
     "de-cap the instances, and widen <code>_validate_snippets.py</code>'s scope so "
     "<code>_proforma/</code> is covered. Note the interlock: de-capping removes the "
     "<code>.05em</code> caps tracking with it, so contradiction 4 partly dissolves contradiction 3. "
     "<b>[ confirm both / de-cap only / separate session ]</b>"),
]

CSS = """<style>
:root{--ink:#1c1c1c;--mut:#6b6b6b;--line:#e4e4e4;--red:#db0011;--set:#0b7a34;--con:#b25000;
      --pra:#3b5f8a;--ten:#8a1f1f;}
*{box-sizing:border-box}
body{font-family:"Univers Next for HSBC","Helvetica Neue",Arial,sans-serif;color:var(--ink);
  margin:0;padding:40px;max-width:1120px;line-height:1.5;background:#fafafa}
h1{font-size:32px;font-weight:300;margin:0 0 4px}
h2{font-size:20px;font-weight:500;margin:44px 0 4px;padding-top:16px;border-top:2px solid var(--ink)}
.sub{color:var(--mut);font-size:14px;margin:0 0 24px}
.lead{font-size:15px;background:#fff;border:1px solid var(--line);border-left:3px solid var(--red);
  padding:16px 20px;margin:20px 0}
.card{background:#fff;border:1px solid var(--line);padding:18px 22px;margin:14px 0}
.tier{display:inline-block;font-size:10px;letter-spacing:.06em;text-transform:none;
  font-weight:500;padding:3px 9px;color:#fff;margin-bottom:8px}
.t-s{background:var(--set)}.t-c{background:var(--con)}.t-p{background:var(--pra)}
.t-t{background:var(--ten)}
.med{font-size:10px;font-weight:500;letter-spacing:.05em;color:#fff;background:#6b6b6b;padding:2px 7px;margin-left:8px;vertical-align:middle;white-space:nowrap}
.find{font-size:16px;font-weight:500;margin:0 0 8px}
.detail{font-size:14px;margin:0 0 12px}
.imp{font-size:13.5px;background:#fbfbfb;border-left:2px solid var(--line);padding:9px 14px;margin:0}
.imp b:first-child{color:var(--ink)}
code{font-family:ui-monospace,Menlo,monospace;font-size:11.5px;background:#f2f2f2;padding:1px 5px;
  border-radius:3px}
table{width:100%;border-collapse:collapse;background:#fff;margin:12px 0;font-size:13px}
th,td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-weight:500;font-size:11px;letter-spacing:.04em;color:var(--mut);background:#f4f4f4}
.rules{background:#fff;border:1px solid var(--line);padding:4px 20px 16px;margin:16px 0}
.rules li{margin:16px 0;font-size:14px}
.ask{width:150px;background:#fffdf5}
.spec{background:#fff;border:1px solid var(--line);padding:16px 22px;margin:14px 0;font-size:15px}
.foot{color:var(--mut);font-size:12px;margin-top:44px;border-top:1px solid var(--line);padding-top:12px}
.num{font-size:22px;font-weight:300;color:var(--mut);margin-right:10px}
</style></head><body>"""


def build():
    h = []
    A = h.append
    A('<!doctype html><html lang="en"><head><meta charset="utf-8">')
    A('<meta name="viewport" content="width=device-width, initial-scale=1">')
    A("<title>Letter-spacing &mdash; evidence dossier</title>")
    A(CSS)

    A("<h1>Letter-spacing &mdash; what the evidence supports</h1>")
    A('<p class="sub">Apollo SDS &middot; 2026-07-18 &middot; evidence dossier, tiered by strength. '
      "Nothing proposed for promotion.</p>")

    A('<div class="lead"><b>The gap.</b> The canon governs letter-spacing <b>nowhere</b>. '
      "<code>canon/type.css</code> declares none on any composite. The token store carries a "
      "letter-spacing ramp set to <b>zero at every size</b> but one. Twenty-four hardcoded values "
      "float loose in the corpus. The only rule on the books is <code>{#type26-018}</code> "
      "&mdash; <i>&quot;no wide kerning that breaks legibility; not too tight either&quot;</i> "
      "&mdash; tagged <code>[TASTE]</code>, with no number.<br><br>"
      "That is precisely the shape <code>dv-019</code> had before its 135&deg; and "
      "<code>col26-020</code> had before its 0.72: a real perceptual rule that cannot be enforced "
      "because nobody pinned a number to it.</div>")

    A('<div class="lead"><b>How to read the tiers.</b> Mixing replicated experiment with '
      "&quot;what typographers say&quot; produces rules nobody can audit later. Each finding "
      "carries its tier, and the contested ones are written as contested &mdash; including where "
      "that is inconvenient for us. <b>The literature&#39;s job is to say where to point the "
      "specimen, not to set the number.</b> Every threshold this system enforces came from what "
      "you could see.</div>")

    # ---- §1 the medium question (Dave's catch — reframes everything below)
    A("<h2>1 &middot; The medium question</h2>")
    A('<p class="sub">Dave, on reading the first cut: <i>&quot;what the display was &mdash; I '
      "suspect screens and print might be different, especially for astigmatism.&quot;</i> "
      "<b>Correct, and it cuts at the foundation of the section below.</b> Most of the classical "
      "typographic authority here is print-derived, and the single strongest experimental finding "
      "turns out to be print too. This section comes first because it changes how the evidence "
      "below should be read.</p>")
    for title, detail, implies in MEDIUM:
        A('<div class="card">')
        A(f'<p class="find">{title}</p>')
        A(f'<p class="detail">{detail}</p>')
        A(f'<p class="imp"><b>For us: </b>{implies}</p>')
        A("</div>")

    # ---- §2 evidence
    A("<h2>2 &middot; The evidence</h2>")
    A('<p class="sub">Each finding carries its <b>medium</b> alongside its tier &mdash; '
      "print-derived, screen-derived, or both. <b>Print provenance is not a disqualification</b> "
      "&mdash; it is a reason to specimen the value rather than adopt it.</p>")
    labels = {"s": "SETTLED", "c": "CONTESTED", "p": "PRACTITIONER &mdash; not experimental",
              "t": "TENSION WITH OUR OWN RULE"}
    for tier, cls, finding, detail, implies in EVIDENCE:
        A('<div class="card">')
        A(f'<span class="tier t-{cls}">{labels[cls]}</span>')
        A(f'<p class="find">{finding}</p>')
        A(f'<p class="detail">{detail}</p>')
        A(f'<p class="imp"><b>For us: </b>{implies}</p>')
        A("</div>")

    # ---- §2 contradictions
    A("<h2>3 &middot; Four contradictions already in our system</h2>")
    A('<p class="sub">Found by grepping the repo before going outside. All four are independent of '
      "what the research says.</p>")
    for n, title, body, action in CONTRA:
        A('<div class="card">')
        A(f'<p class="find"><span class="num">{n}</span>{title}</p>')
        A(f'<p class="detail">{body}</p>')
        A(f'<p class="imp"><b>Action: </b>{action}</p>')
        A("</div>")

    # ---- §3 what a rule could look like
    A("<h2>4 &middot; The shape a rule would take</h2>")
    A('<p class="sub">Not a proposal &mdash; a sketch of what the evidence would support, so §5 has '
      "something concrete to argue with. <b>No number here is promoted.</b></p>")
    A("<table><thead><tr><th>Context</th><th>Direction</th><th>Candidate range</th>"
      "<th>Rests on</th></tr></thead><tbody>")
    rows = [
        ("Display / headline (32px+)", "tighter", "&minus;0.015 to &minus;0.030em",
         "brand type26-016 headline leg + optical sizing (SETTLED)"),
        ("Body / editorial (14&ndash;20px)", "very slightly tighter", "0 to &minus;0.010em",
         "brand type26-016 body leg; general reading evidence says do not widen (CONTESTED)"),
        ("Component small (12&ndash;14px)", "neutral to slightly open", "0 to +0.010em",
         "small-size counter separation (SETTLED); magnitude unobserved"),
        ("Any all-caps run", "open", "+0.05 to +0.12em",
         "Butterick (SETTLED) &mdash; <b>but type26-019 says these should not exist</b>"),
        ("Reverse on dark / chroma", "open", "unquantified",
         "practitioner only (PRACTITIONER); would extend col26-020"),
    ]
    for ctx, direction, rng, rests in rows:
        A(f"<tr><td><b>{ctx}</b></td><td>{direction}</td><td><code>{rng}</code></td>"
          f"<td style='font-size:12px;color:#6b6b6b'>{rests}</td></tr>")
    A("</tbody></table>")

    A('<div class="spec"><b>The one thing I would build next, if you want a number.</b> '
      "A tracking ladder specimen in the shape that has worked twice now: one ground, one size, "
      "tracking stepped across a range, and you mark the first step that reads clean &mdash; the "
      "way 0.72 and 135&deg; were both fixed. Two ladders would cover most of this: a "
      "<b>display ladder</b> (32px, 0 to &minus;0.03em) and a <b>reverse ladder</b> (14px on "
      "<code>surface/digital-black</code>, 0 to +0.03em). The second is the one that would extend "
      "col26-020.</div>")

    # ---- §4 questions
    A("<h2>5 &middot; To rule</h2>")
    A('<ol class="rules">')
    for code, title, body in QUESTIONS:
        A(f"<li><b>{code} &mdash; {title}</b> {body}</li>")
    A("</ol>")

    A('<p class="foot">Generated by <code>reviews/gen_tracking_dossier.py</code> &middot; '
      "evidence tiered and sourced; contested findings recorded as contested &middot; repo "
      "contradictions found by grep before searching outside &middot; <b>nothing promoted</b> "
      "&mdash; promotion is Dave&#39;s alone &middot; sandbox has no Univers, so any tracking you "
      "judge must be judged on your screen with the real face.</p>")
    A("</body></html>")

    with open(OUT, "w") as f:
        f.write("\n".join(h))
    print(f"wrote {os.path.relpath(OUT, ROOT)} — {len(EVIDENCE)} findings, "
          f"{len(CONTRA)} contradictions, {len(QUESTIONS)} questions")


if __name__ == "__main__":
    build()
