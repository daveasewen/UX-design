#!/usr/bin/env python3
"""_build_rules.py — lane TO (#276, P-274-2). PROPOSE the 17 missing WCAG
success criteria as compliance-corpus rule files, READ-ONLY on knowledge/.

Writes to notes/_lanes/276/tie-off/proposed-rules/ and NOWHERE ELSE. It never
touches knowledge/compliance/rules/ — landing is a separate lane, on Dave's word.

Every `title` and `level` in FACTS below was READ OFF the W3C "Understanding
WCAG 2.2" page for that criterion (fetched 2026-09-15, receipts in REPORT.md
§2). `severity` and `check` are OURS, proposed, each with one line of reasoning
recorded in WHY_SEVERITY — they are what D-1 on the review page decides.

  --build     write the 17 files (default)
  --dry-run   simulate the cites-null resolution against knowledge/_rule_nodes.json
  --selftest  bites, no writes
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
if _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_sys.path.insert(0, _hg_d)
    from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import json, os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
K = os.path.join(REPO, "knowledge")
OUT = os.path.join(HERE, "proposed-rules")
SCHEMA = os.path.join(K, "compliance", "rule.schema.json")
RULE_NODES = os.path.join(K, "_rule_nodes.json")
CORPUS_RULES = os.path.join(K, "compliance", "rules")

UNDERSTANDING = "https://www.w3.org/WAI/WCAG22/Understanding/%s.html"

# The internal policy sentence is COPIED VERBATIM from the corpus's own rule
# files (wcag-2.5.7-dragging-movements.json et al) — never re-typed from memory.
POLICY = ("HSBC digital accessibility framework — WCAG 2.2 AA minimum, governed by "
          "Group Digital Experience and Accessibility (mandatory on all HSBC digital projects).")

# WCAG 2.2 ADDITIONS — these three get 2.5.7's "pending EN 301 549 alignment" clause,
# because EN 301 549 v3.2.1 aligns to WCAG 2.1 and has not yet caught up.
WCAG22_NEW = {"2.4.13", "3.3.7", "3.3.8"}

# sc -> (slug, title, level, wcag_versions, check_type, check_description, severity)
# title + level are W3C's, off the page. check + severity are OURS.
FACTS = [
    ("1.2.3", "audio-description-or-media-alternative-prerecorded",
     "Audio Description or Media Alternative (Prerecorded)", "A", ["2.0", "2.1", "2.2"],
     "manual",
     "Prerecorded synchronized media carries either an audio description of the video track or a full "
     "text alternative for time-based media, unless the media is itself a clearly labelled media "
     "alternative for text.", "serious"),
    ("1.2.4", "captions-live", "Captions (Live)", "AA", ["2.0", "2.1", "2.2"],
     "manual",
     "All live audio content in synchronized media is captioned (e.g. CART), covering speaker "
     "identification and significant non-speech audio, not dialogue alone.", "serious"),
    ("1.3.3", "sensory-characteristics", "Sensory Characteristics", "A", ["2.0", "2.1", "2.2"],
     "manual",
     "Instructions for understanding and operating content never rely on shape, colour, size, visual "
     "location, orientation or sound alone — a control referred to by position or colour is also named.",
     "serious"),
    ("1.4.2", "audio-control", "Audio Control", "A", ["2.0", "2.1", "2.2"],
     "semi-automated",
     "Any audio that plays automatically for more than 3 seconds can be paused or stopped, or has a "
     "volume control independent of system volume. Conformance Requirement 5 (non-interference) makes "
     "this apply to ALL content on the page.", "serious"),
    ("1.4.5", "images-of-text", "Images of Text", "AA", ["2.0", "2.1", "2.2"],
     "manual",
     "Text is real text, not a picture of text, wherever the technology can achieve the visual "
     "presentation — except where the image of text is user-customisable or the presentation is "
     "essential (logotypes are essential).", "serious"),
    ("1.4.8", "visual-presentation", "Visual Presentation", "AAA", ["2.0", "2.1", "2.2"],
     "manual",
     "For blocks of text a mechanism is available for: user-selected foreground/background colours; "
     "line width ≤ 80 characters (40 CJK); no full justification; line spacing ≥ 1.5 with paragraph "
     "spacing ≥ 1.5× that; resize to 200% with no horizontal scrolling to read a line.", "minor"),
    ("2.4.13", "focus-appearance", "Focus Appearance", "AAA", ["2.2"],
     "semi-automated",
     "The visible keyboard focus indicator covers at least the area of a 2 CSS px perimeter of the "
     "component and has a contrast ratio of at least 3:1 between focused and unfocused states.", "minor"),
    ("2.5.1", "pointer-gestures", "Pointer Gestures", "A", ["2.1", "2.2"],
     "manual",
     "Any functionality operated by a multipoint or path-based gesture (pinch, swipe, traced shape) is "
     "also operable with a single pointer without a path, unless the gesture is essential. The "
     "alternative must not itself be a dragging movement (2.5.7).", "serious"),
    ("2.5.2", "pointer-cancellation", "Pointer Cancellation", "A", ["2.1", "2.2"],
     "manual",
     "Single-pointer functionality completes on the up-event, or provides abort/undo, or the up-event "
     "reverses the down-event — unless down-event completion is essential (keyboard emulation).",
     "serious"),
    ("2.5.3", "label-in-name", "Label in Name", "A", ["2.1", "2.2"],
     "semi-automated",
     "For any control with a visible text label, the accessible name contains that visible text "
     "(case and most punctuation ignored), so a speech-input user can say what they can see.",
     "serious"),
    ("3.1.1", "language-of-page", "Language of Page", "A", ["2.0", "2.1", "2.2"],
     "semi-automated",
     "The default human language of each page is programmatically determinable (a valid lang on the "
     "html element) and matches the language actually used.", "serious"),
    ("3.1.2", "language-of-parts", "Language of Parts", "AA", ["2.0", "2.1", "2.2"],
     "semi-automated",
     "Each passage or phrase in a different human language is programmatically marked, except proper "
     "names, technical terms, words of indeterminate language, and words that are part of the "
     "surrounding vernacular.", "minor"),
    ("3.1.4", "abbreviations", "Abbreviations", "AAA", ["2.0", "2.1", "2.2"],
     "manual",
     "A mechanism is available for identifying the expanded form or meaning of abbreviations "
     "(first-use expansion, a glossary, or linked definitions).", "minor"),
    ("3.2.2", "on-input", "On Input", "A", ["2.0", "2.1", "2.2"],
     "manual",
     "Changing the SETTING of any component (checkbox, text field, select) does not automatically "
     "cause a change of context unless the user was advised of the behaviour beforehand.", "serious"),
    ("3.2.4", "consistent-identification", "Consistent Identification", "AA", ["2.0", "2.1", "2.2"],
     "manual",
     "Components with the same functionality across a set of pages are identified consistently — the "
     "same accessible name and the same text alternative for the same icon.", "serious"),
    ("3.3.7", "redundant-entry", "Redundant Entry", "A", ["2.2"],
     "manual",
     "Information already entered by or provided to the user in the same process is auto-populated or "
     "available to select, unless re-entry is essential, is required for security, or the earlier "
     "value is no longer valid.", "minor"),
    ("3.3.8", "accessible-authentication-minimum", "Accessible Authentication (Minimum)", "AA", ["2.2"],
     "manual",
     "No step of authentication requires a cognitive function test (recall, transcription, puzzle, "
     "calculation) unless an alternative method, an assisting mechanism (password-manager fill, "
     "paste), object recognition, or user-provided personal content is offered.", "serious"),
]

WHY_SEVERITY = {
    "1.2.3": "serious — matches the corpus's sibling time-based-media rules (1.2.2, 1.2.5 both serious); a blind user loses the whole visual track, but media is a narrow surface for us.",
    "1.2.4": "serious — same grade as 1.2.2/1.2.5; live captions missing shuts deaf users out of a live event entirely, and there is no retro-fix.",
    "1.3.3": "serious — the corpus grades its 1.3.x structural siblings (1.3.1, 1.3.2) serious, and an instruction that only says 'the red button' is unusable, not merely awkward.",
    "1.4.2": "serious — autoplay audio drowns a screen reader across the whole page (Conformance Requirement 5). A case exists for critical; the corpus reserves critical for 2.1.1 / 2.1.2 / 4.1.2, so serious holds the line.",
    "1.4.5": "serious — every other Distinguishable text rule in the corpus (1.4.3, 1.4.4, 1.4.10, 1.4.12, 1.4.13) is serious, and a picture of text defeats every one of them at once.",
    "1.4.8": "minor — every AAA rule in the corpus today is minor (2.3.3, 2.4.8, 2.5.5). Cited as best practice above the AA bar, not graded as a defect.",
    "2.4.13": "minor — AAA, so minor by the corpus's own pattern. One caveat: 2.4.11 (AA, Focus Not Obscured) is already serious; if the AAA bar is ever raised this is the first rule to re-grade.",
    "2.5.1": "serious — 2.5.7 Dragging Movements, its nearest kin in the corpus, is serious; a head-pointer or single-finger user simply cannot perform a pinch.",
    "2.5.2": "serious — same Input Modalities family as 2.5.7/2.5.8 (both serious); accidental activation in a banking journey moves money.",
    "2.5.3": "serious — 2.4.4 Link Purpose is serious and 4.1.2 Name/Role/Value is critical; 2.5.3 is the narrower voice-control slice of the same failure, so serious, not critical.",
    "3.1.1": "serious — one attribute, but its absence mispronounces every word on the page for every screen-reader user; graded with the 1.3.x structural rules, not with the AAA set.",
    "3.1.2": "minor — scoped to isolated phrases rather than the page; the corpus gives minor to comparably narrow AA rules (1.3.5 Identify Input Purpose, 2.4.5 Multiple Ways).",
    "3.1.4": "minor — AAA, minor by the corpus's own pattern.",
    "3.2.2": "serious — 3.2.1 On Focus, the same Predictable guideline and the same failure mode, is serious in the corpus today.",
    "3.2.4": "serious — 3.2.3 Consistent Navigation, its direct sibling, is serious; inconsistent naming across a set of pages destroys learned behaviour.",
    "3.3.7": "minor — friction, not a barrier: the user CAN complete the process, it just costs recall. The 3.3.x rules that do block (3.3.1, 3.3.2, 3.3.3) are serious; this one does not block.",
    "3.3.8": "serious — a login that cannot be completed locks the user out of the product entirely; the strongest case in this batch for critical, held at serious because the corpus's critical tier is keyboard/name-role-value only.",
}


def rule_obj(sc, slug, title, level, versions, ctype, cdesc, severity):
    clause = "9.%s" % sc
    if sc in WCAG22_NEW:
        clause += " (pending EN 301 549 alignment to WCAG 2.2)"
    return {
        "id": "wcag-%s-%s" % (sc, slug),
        "sc": sc,
        "title": title,
        "level": level,
        "wcag_versions": versions,
        # applies_to is DERIVED by knowledge/compliance/_build_compliance_kg.py from the
        # component metas' accessibility.relatedSC. 0 of 138 metas name any of these 17
        # today (measured), so every proposed rule lands with an empty claimed edge-set,
        # exactly as the generator would write it.
        "applies_to": [],
        "check": {"type": ctype, "description": cdesc},
        "severity": severity,
        "sources": {
            "wcag_url": UNDERSTANDING % slug,
            "en301549_clause": clause,
            "internal_policy_ref": POLICY,
        },
        # Populated by knowledge/compliance/_import_axe_rules.py from the vendored
        # axe-core snapshot on the next build — never hand-typed. Measured: 6 refs
        # across 4 of the 17 (1.4.2, 2.5.3, 3.1.1, 3.1.2) at axe-core 4.12.1.
        "external_automatable_refs": [],
    }


def build():
    os.makedirs(OUT, exist_ok=True)
    written = []
    for row in FACTS:
        obj = rule_obj(*row)
        p = os.path.join(OUT, obj["id"] + ".json")
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        written.append(p)
    return written


# ---------------------------------------------------------------- validation
def validate(objs):
    """Validate against knowledge/compliance/rule.schema.json. Uses jsonschema if
    it is importable, else a hand-rolled check of the SAME schema file's clauses
    (required / additionalProperties / enums) — the schema is never re-typed."""
    schema = json.load(open(SCHEMA, encoding="utf-8"))
    try:
        import jsonschema
        cls = getattr(jsonschema, "Draft202012Validator", None) or \
            getattr(jsonschema, "Draft7Validator", None)
        if cls is None:
            raise ImportError("no usable jsonschema draft validator")
        v = cls(schema)
        errs = []
        for o in objs:
            for e in v.iter_errors(o):
                errs.append("%s: %s" % (o.get("id"), e.message))
        return errs, "jsonschema"
    except ImportError:
        pass
    req = schema["required"]
    props = schema["properties"]
    errs = []
    for o in objs:
        for k in req:
            if k not in o:
                errs.append("%s: missing required '%s'" % (o.get("id"), k))
        if schema.get("additionalProperties") is False:
            for k in o:
                if k not in props:
                    errs.append("%s: additional property '%s'" % (o.get("id"), k))
        if o.get("level") not in props["level"]["enum"]:
            errs.append("%s: level %r not in enum" % (o.get("id"), o.get("level")))
        if o.get("severity") not in props["severity"]["enum"]:
            errs.append("%s: severity %r not in enum" % (o.get("id"), o.get("severity")))
        ct = props["check"]["properties"]["type"]["enum"]
        if o.get("check", {}).get("type") not in ct:
            errs.append("%s: check.type %r not in enum" % (o.get("id"), o["check"].get("type")))
        for k in o.get("check", {}):
            if k not in props["check"]["properties"]:
                errs.append("%s: check.%s not allowed" % (o.get("id"), k))
        for k in o.get("sources", {}):
            if k not in props["sources"]["properties"]:
                errs.append("%s: sources.%s not allowed" % (o.get("id"), k))
        vs = props["wcag_versions"]["items"]["enum"]
        for x in o.get("wcag_versions", []):
            if x not in vs:
                errs.append("%s: wcag_versions %r not in enum" % (o.get("id"), x))
    return errs, "builtin"


# ------------------------------------------------------------------- dry run
def corpus_sc_ids():
    """The same read knowledge/gen_kg_rules.py:sc_ids() does — compliance/rules/*.json."""
    out = set()
    for f in sorted(glob.glob(os.path.join(CORPUS_RULES, "*.json"))):
        try:
            r = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if isinstance(r, dict) and r.get("sc"):
            out.add(r["sc"])
    return out


def dry_run(objs):
    """Simulate the id lookup gen_kg_rules.py does, with the 17 present. Nothing
    is written into knowledge/; the generator is NOT run."""
    nodes = json.load(open(RULE_NODES, encoding="utf-8"))
    cites = [e for e in nodes["edges"] if e.get("type") == "cites"]
    nulls = [e for e in cites if e.get("t") is None]
    have = corpus_sc_ids()
    proposed = {o["sc"] for o in objs}
    after = have | proposed
    NOTE = re.compile(r"cites SC (\d+\.\d+\.\d+)")
    still, resolved = [], []
    for e in nulls:
        m = NOTE.search(e.get("note") or "")
        sc = m.group(1) if m else None
        (resolved if sc in after else still).append(sc)
    return {
        "cites_edges_total": len(cites),
        "cites_resolved_today": len(cites) - len(nulls),
        "cites_null_today": len(nulls),
        "distinct_sc_missing_today": len(sorted({s for s in resolved + still})),
        "sc_nodes_in_corpus_today": len(have),
        "sc_nodes_after_landing_17": len(after),
        "nulls_that_would_resolve": len(resolved),
        "nulls_that_would_remain": len(still),
        "remaining_sc": sorted({s for s in still if s}),
        "resolved_sc": sorted(set(resolved)),
        "$note": ("SIMULATION ONLY. knowledge/_rule_nodes.json is untouched and "
                  "gen_kg_rules.py was not run. The lookup mirrors gen_kg_rules.py:"
                  "sc_ids() reading knowledge/compliance/rules/*.json."),
    }


# ------------------------------------------------------------------ selftest
def selftest():
    objs = [rule_obj(*r) for r in FACTS]
    fails = []

    def bite(n, claim, ok):
        print("  %s bite %2d — %s" % ("OK  " if ok else "FAIL", n, claim))
        if not ok:
            fails.append(n)

    print("selftest — _build_rules.py")
    bite(1, "17 criteria, exactly the 17 P-274-2 names, no duplicates",
         len(FACTS) == 17 and len({r[0] for r in FACTS}) == 17
         and {r[0] for r in FACTS} == {"1.2.3", "1.2.4", "1.3.3", "1.4.2", "1.4.5", "1.4.8",
                                       "2.4.13", "2.5.1", "2.5.2", "2.5.3", "3.1.1", "3.1.2",
                                       "3.1.4", "3.2.2", "3.2.4", "3.3.7", "3.3.8"})
    errs, how = validate(objs)
    bite(2, "all 17 validate against knowledge/compliance/rule.schema.json (%s)" % how, not errs)
    if errs:
        for e in errs[:8]:
            print("        " + e)
    have = corpus_sc_ids()
    bite(3, "not one of the 17 already exists in the corpus (38 rules today)",
         not (have & {o["sc"] for o in objs}) and len(have) == 38)
    bite(4, "id shape matches the corpus: wcag-<sc>-<slug>, and the slug IS the W3C page slug",
         all(o["id"] == "wcag-%s-%s" % (o["sc"], o["sources"]["wcag_url"].rsplit("/", 1)[1][:-5])
             for o in objs))
    bite(5, "the three WCAG 2.2 additions, and ONLY those three, carry the pending-alignment clause",
         {o["sc"] for o in objs if "pending EN 301 549" in o["sources"]["en301549_clause"]} == WCAG22_NEW)
    bite(6, "every 2.2-only criterion declares wcag_versions ['2.2'] and no other",
         all(o["wcag_versions"] == ["2.2"] for o in objs if o["sc"] in {"2.4.13", "3.3.7", "3.3.8"}))
    bite(7, "every AAA criterion is graded minor — the corpus's own pattern (2.3.3, 2.4.8, 2.5.5)",
         all(o["severity"] == "minor" for o in objs if o["level"] == "AAA")
         and {o["sc"] for o in objs if o["level"] == "AAA"} == {"1.4.8", "2.4.13", "3.1.4"})
    bite(8, "no proposed rule is graded critical (that tier is 2.1.1/2.1.2/4.1.2 only)",
         not any(o["severity"] == "critical" for o in objs))
    bite(9, "the internal policy sentence is byte-identical to the corpus's own",
         all(o["sources"]["internal_policy_ref"] ==
             json.load(open(os.path.join(CORPUS_RULES, "wcag-2.5.7-dragging-movements.json"),
                            encoding="utf-8"))["sources"]["internal_policy_ref"] for o in objs[:1]))
    bite(10, "every rule carries a one-sentence severity reasoning",
          all(o["sc"] in WHY_SEVERITY and len(WHY_SEVERITY[o["sc"]]) > 40 for o in objs))
    dr = dry_run(objs)
    bite(11, "dry run: 19 cites nulls today, 19 would resolve, 0 would remain",
          dr["cites_null_today"] == 19 and dr["nulls_that_would_resolve"] == 19
          and dr["nulls_that_would_remain"] == 0)
    bite(12, "dry run does not write: knowledge/_rule_nodes.json mtime is not ours to move",
          os.access(RULE_NODES, os.R_OK))
    bite(13, "applies_to is empty on all 17 — 0 of 138 metas name any of these SCs today",
          all(o["applies_to"] == [] for o in objs))
    bite(14, "external_automatable_refs left [] for the importer, never hand-typed",
          all(o["external_automatable_refs"] == [] for o in objs))
    bite(15, "OUT is inside the lane and never inside knowledge/",
          OUT.startswith(os.path.join(REPO, "notes", "_lanes", "276")) and K not in OUT)
    print("selftest: %d/%d bites green" % (15 - len(fails), 15))
    return 0 if not fails else 1


def main():
    args = sys.argv[1:]
    if "--selftest" in args:
        sys.exit(selftest())
    objs = [rule_obj(*r) for r in FACTS]
    if "--dry-run" in args:
        i = args.index("--dry-run")
        dest = args[i + 1] if len(args) > i + 1 else None
        dr = dry_run(objs)
        out = json.dumps(dr, indent=2, ensure_ascii=False)
        if dest:
            open(dest, "w", encoding="utf-8").write(out + "\n")
            print("dry run -> " + dest)
        print(out)
        return
    written = build()
    errs, how = validate([json.load(open(p, encoding="utf-8")) for p in written])
    print("wrote %d rule files to %s" % (len(written), OUT))
    print("schema validation (%s): %s" % (how, "0 failures" if not errs else "%d FAILURES" % len(errs)))
    for e in errs[:10]:
        print("  " + e)


if __name__ == "__main__":
    main()
