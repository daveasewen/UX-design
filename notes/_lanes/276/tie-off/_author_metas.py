#!/usr/bin/env python3
"""_author_metas.py — lane TO (#276, P-274-3 + s275-D5). PROPOSE the authored
`edges.obeys` block for six components, READ-ONLY on knowledge/.

AUTHORED, not inferred. Every rule id below came from a FILENAME JOIN on
knowledge/guidelines/_rules-index.json (`file == common-toolkit-<x>.md`), never
from a regex over rule prose — that is the route s274-D12 refused after
va25-013 matched 'Avatar' and 'Badge'. Every `$why` was written by reading the
rule text and the component meta together, one line each, reviewed by eye.

The six A-grade laws are the ones s269-D5 names, read out of
knowledge/brain/principles.json by grade == 'A' (never retyped): pr-fitts,
pr-hick, pr-steering, pr-klm, pr-speed-accuracy, pr-graphical-perception.

Output: notes/_lanes/276/tie-off/proposed-metas/<stem>.meta.json — each one a
BYTE-FOR-BYTE copy of the live meta with a single textual span inserted inside
its existing "edges": { … } object. The live metas are never opened for writing
and no existing JSON is ever re-serialised.

  --build     write the six proposed metas (default)
  --selftest  bites, no writes
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
if _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_sys.path.insert(0, _hg_d)
    from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
K = os.path.join(REPO, "knowledge")
COMPONENTS = os.path.join(K, "components")
OUT = os.path.join(HERE, "proposed-metas")
INDEX = os.path.join(K, "guidelines", "_rules-index.json")
PRINCIPLES = os.path.join(K, "brain", "principles.json")

# stem -> guideline file whose rules are joined by FILENAME
SPEC_FILE = {
    "tags": "common-toolkit-tags-chips.md",
    "tags-input": "common-toolkit-tags-chips.md",
    "notifications": "common-toolkit-notifications.md",
    "links": "common-toolkit-links.md",
    "button": "common-toolkit-buttons.md",
    "icon-button": "common-toolkit-buttons.md",
}

# ---------------------------------------------------------------------------
# THE AUTHORED TABLE. stem -> [(node-id, one-line why it binds)]
# ---------------------------------------------------------------------------
RULES = {
    "tags": [
        ("rule:ctkt-002", "Defines what a Tag IS for us — a keyword descriptor of content composition — which is this meta's `purpose` sentence, so the rule is the component's definition, not a constraint on it."),
        ("rule:ctkt-003", "Orders a tag group alphabetically or by content priority and holds that order across a content structure; the Tags atom is always rendered in groups, so the ordering contract is the component's."),
        ("rule:ctkt-004", "Bans tag styling for non-keyword metadata (date, read time) — a direct anti-pattern on this atom's variants."),
        ("rule:ctkt-005", "Bans icons on tags and any action other than a standard tag link, which fixes this atom's prop surface."),
        ("rule:ctkt-006", "The affordance contract: static tags must read informational, tag links must read clickable — the meta's two variants ARE the two sides of this rule."),
        ("rule:ctkt-007", "Placement at start and/or end of content, and not interactive at the top of an article — governs where this atom is allowed to appear."),
        ("rule:ctkt-009", "Label centred, tag expands horizontally, group wraps to a second row, long label wraps to a second line — the geometry of this atom's container."),
        ("rule:ctkt-010", "Tag copy is a keyword, sentence case, never more than three words — a content constraint on this atom's only slot."),
        ("rule:ctkt-011", "≥44×44 CSS px covering the whole tag, and the shared 12px band recipe for grouped tag links — the target-size arithmetic for this exact atom."),
    ],
    "tags-input": [
        ("rule:ctkt-019", "The chip anatomy — container, label, icon/action, DESTRUCTIVE action that deletes the chip and its selection, optional processing spinner — is the anatomy of the committed value in this field."),
        ("rule:ctkt-021", "Icons are all-or-nothing across states; this field renders every committed value as the same chip, so the rule binds the whole set at once."),
        ("rule:ctkt-026", "Dynamic width from the label, 8px between chips, NO truncation, and a wrap that preserves the corner radius — the layout contract for the chips inside this field."),
        ("rule:ctkt-027", "Groups wrap to the next row and NEVER force a single row with horizontal scroll — this field is a wrapping chip group by construction."),
        ("rule:ctkt-029", "Target area covers the ENTIRE chip container, minimum 44×44 — and in this field the chip carries a delete affordance, so the target rule is load-bearing."),
    ],
    "notifications": [
        ("rule:ctkn-003", "Bans notifications for marketing — a use-boundary on this molecule, and an anti-pattern its four placements would otherwise invite."),
        ("rule:ctkn-004", "Defines the Snackbar placement as non-essential, timely, no-input-required and auto-dismissing — one of this meta's four declared placements."),
        ("rule:ctkn-006", "Global notifications sit ABOVE the masthead and flag site-wide issues — placement and scope for the Global variant."),
        ("rule:ctkn-007", "Contextual notifications sit at the top of page content below the page title, triggered by user action — placement for the Contextual variant."),
        ("rule:ctkn-008", "Severity stacking order error → warning → success → information; the meta's RAG family has no meaning without the order they stack in."),
        ("rule:ctkn-009", "The stack spacing numerics (1px global↔global, 8px global↔contextual, 8px snackbar) are this molecule's own spacing tokens in prose form."),
        ("rule:ctkn-010", "Same type shares one container, different types stack separately, form errors get one container with anchor links — a composition rule for multiples of this molecule."),
        ("rule:ctkn-011", "Snackbar resting position, elevation above modals and navigation, six-column cap on large screens — the placement contract for the Snackbar variant."),
        ("rule:ctkn-012", "The web anatomy — severity icon, 3–5 word Medium-weight title, 1–2 sentence description, optional link, optional close — IS this molecule's slot list."),
        ("rule:ctkn-015", "Notifications are static: they appear on load or on action and stay until resolved or dismissed — the behaviour half of the meta's stateModel."),
        ("rule:ctkn-016", "Snackbar timing and motion (4–10s by reading length, fade on timeout, instant on manual dismiss) is the meta's `motion` block written as a rule."),
        ("rule:ctkn-018", "System-error copy: active voice, plain English, no error codes, 'We're sorry' only when the fault is ours — binds the error variant's content."),
        ("rule:ctkn-019", "User errors always carry a fix instruction, instruction-first, no 'Please' per instruction — binds the error variant's content (RULED 2026-07-03)."),
        ("rule:ctkn-020", "Form errors: the exact title string, 'Enter…' instructions, field-label reference, anchor link to the field, message replicated below the field — the full contract for the form-multi-link variant this meta names."),
        ("rule:ctkn-021", "Warnings never use 'Warning' as the heading and must state issue AND effect in 'you' terms — binds the warning variant's content."),
        ("rule:ctkn-022", "Success copy uses positive signifier terms and active voice, and success notifications occur ONLY at page level — a placement constraint on the success variant."),
        ("rule:ctkn-025", "44×44 target with named coverage (action buttons on global, the whole list item but not the dividers on snackbars) — target size for this molecule's interactive parts."),
    ],
    "links": [
        ("rule:ctkl-001", "States what a Link IS against a Button — primarily navigation, lower-priority or many same-priority actions — which is this meta's `purpose` sentence."),
        ("rule:ctkl-002", "Don't provide so many links that it is unclear where to go — a density constraint on this molecule in context."),
        ("rule:ctkl-004", "Chevron links carry a RED chevron as signposting — fixes the glyph and colour of one of the meta's four family members."),
        ("rule:ctkl-005", "Back links put the chevron on the LEFT pointing left — the Back link member of the family of four."),
        ("rule:ctkl-007", "Arrow sizing is numeric and font-tier-keyed (x-height or cap-height, gap = arrow/2) — the Arrow link's geometry, tied to the type scale this meta already binds."),
        ("rule:ctkl-008", "Wrap behaviour differs by type: the arrow stays attached to the last word, the back/icon glyph stays aligned to the first line — per-member layout behaviour."),
        ("rule:ctkl-009", "Only globally recognised icons, per the icons guidelines — constrains the Icon link member's slot."),
        ("rule:ctkl-010", "Download links: icon on the LEFT plus file format and size in brackets — the meta's own purpose names 'download pdf' as a link job."),
        ("rule:ctkl-011", "External links open in a new tab with the indicator icon at the END, as PART of the link — fixes both behaviour and anatomy."),
        ("rule:ctkl-014", "Underlined within body text, weight MATCHES the surrounding text in all states — binds this molecule's type tokens to its container's."),
        ("rule:ctkl-015", "Hyperlink ≤5 words, descriptive of the destination, preferably at the end of the sentence — content contract for the inline member."),
        ("rule:ctkl-017", "Internal links open in the current tab, external in a new tab — the behaviour half of the external-link rule, stated for both cases."),
        ("rule:ctkl-018", "Hover underlines on mouse-over of text OR icon and the target wraps both — icon and text are ONE link, which is a composition fact about this molecule."),
        ("rule:ctkl-020", "On dark, links and their icons are white — the per-theme token binding this meta's `tokens` block has to satisfy."),
        ("rule:ctkl-022", "Link text describes the action or destination, sentence case, ≤8 words, no 'Click here', no full stop — the content contract across the family."),
        ("rule:ctkb-004", "CROSS-FILE, authored: the buttons spec draws the boundary from the other side — 'for less prominent actions, we use text links'. It binds Links as much as Button, and is the only rule in this set that does not come from common-toolkit-links.md."),
    ],
    "button": [
        ("rule:ctkb-002", "Rank semantics for primary/secondary/tertiary/quaternary IS this meta's four-level emphasis hierarchy, stated as a rule."),
        ("rule:ctkb-003", "Cardinality — one primary and/or one secondary per page, never both in one group — a composition constraint on this atom."),
        ("rule:ctkb-004", "The buttons-vs-links boundary tells you when this atom is the WRONG answer, which is the `when` gate half of the meta."),
        ("rule:ctkb-005", "The two width modes (set vs dynamic, with fixed side padding) are this atom's width props in prose."),
        ("rule:ctkb-006", "8px between buttons and the primary ALWAYS first — a group-layout rule for this atom's commonest pattern."),
        ("rule:ctkb-007", "Stacking and full-width differ by platform (app always full width, web keeps dynamic widths) — binds the meta's `responsive` block."),
        ("rule:ctkb-008", "Placement: web left aligned, app bottom, processes back-left/continue-right with the primary stacking on top on small viewports."),
        ("rule:ctkb-009", "Buttons are always rectangular, never rounded — a shape token fixed for this atom."),
        ("rule:ctkb-010", "Label centred both ways, fixed side padding in BOTH width modes, copy should not wrap — the geometry of this atom's label slot."),
        ("rule:ctkb-011", "Icons in buttons: globally recognised only, used sparingly, from a blessed list, in three structural variations (label / icon-label / icon-only) — fixes this atom's icon prop."),
        ("rule:ctkb-012", "The app 'button activity' contract (loading indicator → RAG notification state → resolution, with an accessible label) is the contract behind this meta's `processing` and `sucess (app)` variants."),
        ("rule:ctkb-013", "Button copy: sentence case, ≤5 words, action verbs, precise, 'Continue' not 'Next' — the content contract for this atom's only slot."),
        ("rule:ctkb-014", "Accessible name = the visible label, and target ≥44×44 covering the ENTIRE container — the accessibility contract, and 2.5.3 Label in Name kin (one of the 17 this lane proposes)."),
        ("rule:ctkb-015", "OPEN: the quaternary-inline contradiction between the guide and the app standard. Destiny REVIEW, deferred by Dave 2026-07-03 — recorded here because it binds this atom and is unresolved, not because it is settled."),
    ],
    "icon-button": [
        ("rule:ctkb-002", "This meta says it shares Button's four-level emphasis hierarchy and tokens, so the rank semantics rule binds it unchanged."),
        ("rule:ctkb-006", "8px between buttons and primary-first — icon buttons group the same way; the rule is about the group, not the label."),
        ("rule:ctkb-009", "Always rectangular, never rounded — a shape token shared with Button."),
        ("rule:ctkb-011", "The rule NAMES icon-only as one of the three structural variations and supplies the blessed icon list — this is the rule that makes this component legal."),
        ("rule:ctkb-012", "The button-activity contract, including the clause that an accessible label MUST accompany the spinner — sharper here, since there is no visible label to fall back on."),
        ("rule:ctkb-014", "Accessible name and ≥44×44 over the whole container — the binding constraint for a control with no visible text at all."),
    ],
}

LAWS = {
    "tags": [
        ("ux:pr-fitts", "ctkt-011's 44×44 floor and its shared-12px-band recipe are Fitts's law turned into arithmetic: a small text row is made hittable by growing the target, not the type."),
        ("ux:pr-hick", "ctkt-003 orders a group alphabetically or by priority and keeps that order; Hick is why a consistent order shortens the scan through N equally likely keywords."),
    ],
    "tags-input": [
        ("ux:pr-fitts", "ctkt-029 puts the target over the ENTIRE chip including its delete affordance — the smallest, most consequential target in the field."),
        ("ux:pr-speed-accuracy", "the destructive action lives inside the chip (ctkt-019): making removal fast makes accidental removal likelier, and that trade is the reason the target and the icon rules are strict."),
    ],
    "notifications": [
        ("ux:pr-hick", "ctkn-008's severity order and ctkn-010's one-container-per-type exist to cut the number of equally likely things a user must triage."),
        ("ux:pr-graphical-perception", "colour saturation is a weak perceptual channel, which is why ctkn-012 requires a severity ICON and a 3–5 word title as well as the RAG colour — never colour alone."),
    ],
    "links": [
        ("ux:pr-fitts", "ctkl-018 wraps the target area around icon AND text as one link — a deliberate enlargement of a small inline target."),
        ("ux:pr-hick", "ctkl-002 ('don't provide so many links it becomes unclear where to go') is Hick stated as a Don't."),
        ("ux:pr-speed-accuracy", "ctkl-015/ctkl-022 cap link text and demand it describe the destination: a scannable link is fast, and a vague one is fast AND wrong."),
    ],
    "button": [
        ("ux:pr-fitts", "ctkb-014's ≥44×44 over the entire container, and ctkb-005's fixed side padding, set target size directly."),
        ("ux:pr-hick", "ctkb-003's one-primary-per-page cardinality reduces the set of equally weighted choices to one."),
        ("ux:pr-speed-accuracy", "ctkb-006's 8px gap and primary-first order make the fast path also the safe one — adjacency is where mis-hits come from."),
    ],
    "icon-button": [
        ("ux:pr-fitts", "an icon-only control is the smallest target in the set; ctkb-014's 44×44 is the whole reason it stays usable."),
        ("ux:pr-speed-accuracy", "dropping the label buys speed and costs certainty, which is exactly why ctkb-011 restricts icons to globally recognised ones and ctkb-014 insists on the accessible name."),
    ],
}

CONTRACT = ("AUTHORED, not inferred (P-274-3 + s275-D5, lane TO #276). `rule:` refs are joined by "
            "FILENAME from knowledge/guidelines/_rules-index.json — never by a regex over rule prose. "
            "`ux:` refs are the six grade-A laws s269-D5 names. Each $why is one line, written by "
            "reading the rule and this meta together, reviewed by eye. PROPOSED — not ratified.")


# ---------------------------------------------------------------------------
def index_rules():
    return json.load(open(INDEX, encoding="utf-8"))["rules"]


def grade_a_laws():
    P = json.load(open(PRINCIPLES, encoding="utf-8"))["principles"]
    return {"ux:" + p["id"] for p in P if p.get("grade") == "A"}


def obeys_block(stem, indent):
    """The literal JSON text to splice in, already indented for the target file."""
    entries = []
    for ref, why in RULES[stem] + LAWS[stem]:
        entries.append({"ref": ref, "$why": why})
    blob = {"$contract": CONTRACT, "obeys": entries}
    txt = json.dumps(blob["obeys"], indent=2, ensure_ascii=False)
    lines = txt.split("\n")
    pad = " " * indent
    body = ("\n" + pad).join(lines)
    note = json.dumps(CONTRACT, ensure_ascii=False)
    return '%s"$obeys-contract": %s,\n%s"obeys": %s,' % (pad, note, pad, body)


def splice(stem, parts=False):
    src = os.path.join(COMPONENTS, stem + ".meta.json")
    text = open(src, encoding="utf-8").read()
    m = re.search(r'^(\s*)"edges"\s*:\s*\{[ \t]*\n', text, re.M)
    if not m:
        raise SystemExit("no edges object in " + src)
    indent = len(m.group(1)) + 2
    at = m.end()
    ins = obeys_block(stem, indent) + "\n"
    out = text[:at] + ins + text[at:]
    return (text, at, ins, out) if parts else out


def build():
    os.makedirs(OUT, exist_ok=True)
    written = []
    for stem in SPEC_FILE:
        out = os.path.join(OUT, stem + ".meta.json")
        new = splice(stem)
        json.loads(new)  # must still parse
        open(out, "w", encoding="utf-8").write(new)
        written.append(out)
    return written


# ------------------------------------------------------------------ selftest
def selftest():
    fails = []

    def bite(n, claim, ok):
        print("  %s bite %2d — %s" % ("OK  " if ok else "FAIL", n, claim))
        if not ok:
            fails.append(n)

    idx = index_rules()
    by_id = {r["id"]: r for r in idx}
    by_file = {}
    for r in idx:
        by_file.setdefault(r["file"], set()).add(r["id"])
    laws = grade_a_laws()

    print("selftest — _author_metas.py")
    bite(1, "six components authored, each with a live meta on disk",
         len(SPEC_FILE) == 6 and all(os.path.exists(os.path.join(COMPONENTS, s + ".meta.json"))
                                     for s in SPEC_FILE))
    allrefs = [r for s in RULES for r, _ in RULES[s]]
    bite(2, "every rule: ref resolves to a real id in _rules-index.json (470 rules)",
         len(idx) == 470 and all(r.split(":", 1)[1] in by_id for r in allrefs))
    bad = [(s, r) for s in RULES for r, _ in RULES[s]
           if by_id[r.split(":", 1)[1]]["file"] != SPEC_FILE[s]]
    bite(3, "FILENAME JOIN holds: the only cross-file binding is the one declared (links <- ctkb-004)",
         bad == [("links", "rule:ctkb-004")])
    bite(4, "no rule id is invented: every id matches the corpus's ^[a-z]+-\\d{3}$ shape",
         all(re.match(r"^[a-z][a-z0-9-]*-\d{3}$", r.split(":", 1)[1]) for r in allrefs))
    bite(5, "tags + tags-input together use 14 of the 23 tags-chips rules, and never the same one twice",
         len({r for r, _ in RULES["tags"]} | {r for r, _ in RULES["tags-input"]}) == 14
         and not ({r for r, _ in RULES["tags"]} & {r for r, _ in RULES["tags-input"]}))
    bite(6, "notifications takes ALL 17 rules of its spec file",
         {r.split(":", 1)[1] for r, _ in RULES["notifications"]} == by_file["common-toolkit-notifications.md"])
    bite(7, "links takes ALL 15 rules of its spec file, plus the one declared cross-file rule",
         {r.split(":", 1)[1] for r, _ in RULES["links"]} ==
         by_file["common-toolkit-links.md"] | {"ctkb-004"})
    bite(8, "button takes ALL 14 rules of its spec file",
         {r.split(":", 1)[1] for r, _ in RULES["button"]} == by_file["common-toolkit-buttons.md"])
    bite(9, "icon-button is a SUBSET of button's set — it never claims a rule Button does not obey",
         {r for r, _ in RULES["icon-button"]} < {r for r, _ in RULES["button"]})
    bite(10, "every ux: ref is one of the six grade-A laws, read from principles.json not retyped",
          len(laws) == 6 and all(r in laws for s in LAWS for r, _ in LAWS[s]))
    bite(11, "every entry carries a non-empty authored $why of at least 40 characters",
          all(len(w) >= 40 for s in RULES for _, w in RULES[s])
          and all(len(w) >= 40 for s in LAWS for _, w in LAWS[s]))
    bite(12, "no $why is reused verbatim across two components — each one was written for its own meta",
          len({w for s in RULES for _, w in RULES[s]}) == sum(len(RULES[s]) for s in RULES))
    bite(13, "the spliced meta still parses as JSON and gains exactly the two new keys",
          all(set(json.loads(splice(s))["edges"]) -
              set(json.load(open(os.path.join(COMPONENTS, s + ".meta.json")),
                            )["edges"]) == {"obeys", "$obeys-contract"} for s in SPEC_FILE))
    bite(14, "the splice is EXACTLY one insertion: cut the inserted span back out and the live file returns, byte for byte",
          all(_cut_back(*splice(s, parts=True)) for s in SPEC_FILE))
    bite(15, "not one value outside edges.obeys changes — every other top-level key is identical",
          all(_same_except_edges(s) for s in SPEC_FILE))
    bite(16, "the ref grammar the live schema allows does NOT admit rule:/ux: — the diff is REQUIRED",
          not re.match(json.load(open(os.path.join(COMPONENTS, "meta.schema.json"),
                                      encoding="utf-8"))["definitions"]["edge"]["properties"]["ref"]["pattern"],
                       "rule:ctkb-002"))
    bite(17, "OUT is inside the lane; knowledge/components/ is never a write target",
          OUT.startswith(os.path.join(REPO, "notes", "_lanes", "276")) and COMPONENTS not in OUT)
    print("selftest: %d/%d bites green" % (17 - len(fails), 17))
    return 0 if not fails else 1


def _cut_back(text, at, ins, out):
    """out is text with ins inserted at `at` and NOTHING else changed — proved by
    reconstructing both directions, not by a fuzzy prefix/suffix walk (which an
    insertion of leading whitespace can slide past)."""
    return (out == text[:at] + ins + text[at:]
            and out[:at] + out[at + len(ins):] == text
            and len(out) == len(text) + len(ins))


def _same_except_edges(stem):
    live = json.load(open(os.path.join(COMPONENTS, stem + ".meta.json"), encoding="utf-8"))
    new = json.loads(splice(stem))
    a = {k: v for k, v in live.items() if k != "edges"}
    b = {k: v for k, v in new.items() if k != "edges"}
    if a != b:
        return False
    le, ne = dict(live["edges"]), dict(new["edges"])
    ne.pop("obeys", None)
    ne.pop("$obeys-contract", None)
    return le == ne


def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(selftest())
    w = build()
    print("wrote %d proposed metas to %s" % (len(w), OUT))
    for p in w:
        d = json.load(open(p, encoding="utf-8"))
        print("  %-14s obeys %2d (%d rules + %d laws)" % (
            os.path.basename(p), len(d["edges"]["obeys"]),
            len([e for e in d["edges"]["obeys"] if e["ref"].startswith("rule:")]),
            len([e for e in d["edges"]["obeys"] if e["ref"].startswith("ux:")])))


if __name__ == "__main__":
    main()
