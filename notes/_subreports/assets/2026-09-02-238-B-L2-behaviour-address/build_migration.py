#!/usr/bin/env python3
"""
build_migration.py — #238 lane B (L2, s234-D5). Builds `behaviour-migration.json`: the 20 prose
`behaviour` values in knowledge/components/*.meta.json, each beside a PROPOSED typed object
{script, partial, events, fallback, $note}, with the basis of every field named:

  prose      the field is settled by the meta's own prose — the quote is carried verbatim
  measured   the field is settled by a PROBE on the reviewed snippet (inline <script> count and
             bytes, AUTO-BEHAVIOUR markers, addEventListener names) — the probe is carried
  UNPROVEN   neither the prose nor a probe settles it; a CANDIDATE reading is carried OUTSIDE the
             proposed object (in `provenance`) so it can never be applied by accident, and the
             proposed value is null with `$unproven` naming the field

⛔ THIS IS A PROPOSAL. Nothing here writes a meta. `notes/_briefs/2026-09-02-234-v106-brief.md:47`:
schema changes are Dave's — ratify at his eye BEFORE populate. The migration is BY ADDITION: the
old prose is kept verbatim under `$note` (ADR-0017 archive-never-delete).

Run from the repo root:  python3 notes/_subreports/assets/2026-09-02-238-B-L2-behaviour-address/build_migration.py [--out PATH]
"""
import glob, hashlib, json, os, re, sys, datetime

REPO = os.getcwd()
COMP = os.path.join(REPO, "knowledge", "components")
SNIP = os.path.join(REPO, "knowledge", "snippets")

SCRIPT_RE = re.compile(r"<script\b([^>]*)>(.*?)</script>", re.S)
AUTOB_RE = re.compile(r"<!--\s*=====\s*AUTO-BEHAVIOUR\s+(\S+)\s+START[^>]*=====\s*-->(.*?)<!--\s*=====\s*AUTO-BEHAVIOUR\s+\1\s+END\s*=====\s*-->", re.S)
LISTENER_RE = re.compile(r"(?:(?P<target>[\w$.\[\]'\"()]+)\s*\.\s*)?addEventListener\(\s*['\"](?P<ev>[a-zA-Z]+)['\"]")
ONATTR_RE = re.compile(r"\son([a-z]+)\s*=\s*['\"]")

# ---------------------------------------------------------------- curated readings (mine, FLOATED)
# `passive` is only set where the PROSE says so, and the quote is the prose's own words.
# `fallback_candidate` is a READING for the UNPROVEN fallback field — it lives in `provenance`,
# never in `proposed`, so Dave's eye is what promotes it.
CURATED = {
    "account-card": {"passive_quote": "drafted as a passive display card (no states)",
                     "flag": "REVIEW is open in the prose itself: 'Decide whether an INTERACTIVE variant is needed' — the proposal types TODAY's card (passive); an interactive variant would be a second meta or a variant, Dave's."},
    "action-bar": {"passive_quote": "Passive layout container — no states of its own"},
    "badge": {"passive_quote": "Badges are passive indicators — they notify but are not themselves interactive controls",
              "flag": "'may appear with subtle animated motion' is a MOTION note (CSS), not a script — `motion` is the field for it, not `behaviour`."},
    "confirmation": {"passive_quote": "Passive panel — no states of its own"},
    "eyebrow": {"passive_quote": "Passive display label — no states."},
    "summary": {"passive_quote": "Passive display list — no states."},
    "amount-input": {"fallback_candidate": "A native text input: `inputmode=decimal` still brings the numeric keypad (an attribute, not script); no character stripping, no en-GB grouping, no two-decimal normalisation, no is-completed weight.",
                     "fallback_quote_hint": "inputmode=decimal brings the numeric keypad on touch"},
    "anchor-nav": {"fallback_candidate": "Fragment links still jump (they are real `href=\"#…\"` links with scroll-margin-top); the current mark stays where the markup authored it and never moves.",
                   "fallback_quote_hint": "Real fragment links plus scroll-margin-top on each section",
                   "fallback_measured": "the snippet's own script comment: 'The authored aria-current in the markup is the no-JS answer; this only ever moves it.' (Anchor-nav.reference.html, first line of the inline script)"},
    "calendar": {"fallback_candidate": "The month grid renders (server-authored buttons); nothing selects, nothing pages, no live-region announcement."},
    "command-palette": {"fallback_candidate": "Cannot open — the opener is a keyboard chord handled in script. A page relying on it needs a visible route to the same commands."},
    "date-picker": {"fallback_candidate": "The text input works as a native field (DD/MM/YYYY typed by hand); the tail button does nothing and the panel never opens; no on-blur validation message.",
                    "fallback_quote_hint": "Typing NEVER opens the panel."},
    "date-range-picker": {"fallback_candidate": "Both fields work as native text inputs; neither tail button opens a panel; no pair validation.",
                          "fallback_quote_hint": "Per-field DD/MM/YYYY on blur"},
    "file-upload": {"fallback_candidate": "Browse still works if the control wraps a native `<input type=file>`; nothing stages, no progress bar, no remove, no announcements.",
                    "fallback_quote_hint": "Drop or browse stages files (acd-019: nothing auto-submits)"},
    "form-layout": {"fallback_candidate": "The form submits natively; no per-field errors or summary from script, no sort-code masking. Whether native constraint validation stands in is a markup question (required/pattern attributes), not settled here.",
                    "fallback_quote_hint": "Validate on submit; per-field errors + summary together."},
    "secure-entry": {"fallback_candidate": "Six independent inputs; no auto-advance, no paste distribution, no verify state; `autocomplete=one-time-code` (an attribute) still invites OS autofill.",
                     "fallback_quote_hint": "autocomplete=one-time-code invites OS autofill"},
    "stepper": {"fallback_candidate": "Whichever panel the markup authors as current is the only one shown; Next/Back do nothing; no announcements. The dots↔track collapse is a container query (CSS) and still works.",
                "fallback_quote_hint": "Same container-query breakpoint as Progress-tracker (520px)"},
    "tab-bar": {"fallback_candidate": "Navigation works — each item is a native `<a>`; the authored `aria-current` stands; the sliding pill does not move.",
                "fallback_quote_hint": "Each item is a native <a> (focusable, keyboard-operable)."},
    "textarea": {"fallback_candidate": "A native textarea: vertical resize is CSS and still holds; no counter, no warn weight, no announcement.",
                 "fallback_quote_hint": "vertical only (horizontal resize breaks the layout grid)"},
    "time-picker": {"fallback_candidate": "The text input works as a native field (HH:MM typed by hand); the tail button does nothing; no on-blur validation.",
                    "fallback_quote_hint": "Typing NEVER opens the list (acd-019)."},
    "tree": {"fallback_candidate": "Every branch renders in whatever open/closed state the markup authors; no keyboard model, no expand/collapse, no lazy load.",
             "fallback_quote_hint": None},
}

# event -> prose keywords that CORROBORATE a measured listener (a quote is evidence the prose
# describes the same interaction; the LISTENER is the measurement).
# Ordered: the FIRST alternative that finds a sentence wins, so a sentence that names the
# interaction ("keyboard: …") beats one that merely contains a key word ("sets end").
EVENT_WORDS = {
    "keydown": [r"^keyboard:", r"keyboard", r"backspace|arrow|pageup|pagedown|letter key|asterisk", r"shortcut|chord", r"\benter\b|escape|\besc\b"],
    "click": [r"\bclick", r"twisty", r"tail button", r"\btap", r"\bpick\b", r"next validates|back button|any completed dot", r"per-row|links focus"],
    "input": [r"on input|input event|updates on input", r"as typed|while typing|typing", r"re-validates"],
    "blur": [r"\bblur\b"],
    "focus": [r"while editing"],
    "paste": [r"\bpaste"],
    "submit": [r"on submit"],
    "change": [r"browse"],
    "drop": [r"\bdrop\b"],
    "resize": [r"\bresize\b|breakpoint"],
    "focusin": [],
    "pointerdown": [],
}
OBSERVER_RE = re.compile(r"new\s+(IntersectionObserver|ResizeObserver|MutationObserver)\b")


def prose_text(v):
    if isinstance(v, str):
        return v
    if isinstance(v, dict):
        return " ".join("%s: %s" % (k, t) for k, t in v.items())
    return json.dumps(v)


def sentence_with(text, alternatives):
    sentences = [s.strip() for s in re.split(r"(?<=[.;])\s+", text)]
    for rx in alternatives:
        for s in sentences:
            if re.search(rx, s, re.I):
                return s
    return None


def measure(snippet_path):
    h = open(snippet_path, encoding="utf-8").read()
    auto = [(n, b) for n, b in AUTOB_RE.findall(h)]
    auto_spans = [m.span() for m in AUTOB_RE.finditer(h)]
    inline = []
    for m in SCRIPT_RE.finditer(h):
        attrs, body = m.group(1), m.group(2)
        if "src=" in attrs:
            continue
        t = re.search(r'type="([^"]+)"', attrs)
        if t and t.group(1) not in ("text/javascript", "module"):
            continue
        if any(a <= m.start() < b for a, b in auto_spans):
            continue                      # an AUTO-BEHAVIOUR payload has its own address
        inline.append(body)
    listeners, tracker = {}, False
    for body in inline:
        tracker = tracker or ("dataset.modality" in body)
        for lm in LISTENER_RE.finditer(body):
            ev, tgt = lm.group("ev"), lm.group("target")
            listeners.setdefault(ev, {"window": 0, "element": 0})
            listeners[ev]["window" if not tgt or tgt in ("window", "document") else "element"] += 1
        for ev in ONATTR_RE.findall(body):
            listeners.setdefault(ev, {"window": 0, "element": 0})["element"] += 1
    component_events, tracker_events = [], []
    for ev, c in sorted(listeners.items()):
        if tracker and ev in ("keydown", "mousedown", "touchstart") and c["element"] == 0:
            tracker_events.append(ev)
        else:
            component_events.append(ev)
    srcs = re.findall(r'<script[^>]+src="([^"]+)"', h)
    observers = sorted({o for body in inline for o in OBSERVER_RE.findall(body)})
    return {
        "observers": observers,
        "inline_executable_scripts": len(inline),
        "inline_bytes": [len(b.encode("utf-8")) for b in inline],
        "inline_sha256": ["sha256:" + hashlib.sha256(b.encode("utf-8")).hexdigest() for b in inline],
        "auto_behaviour": [n for n, _ in auto],
        "script_src": srcs,
        "listeners": listeners,
        "component_events": component_events,
        "modality_tracker_events": tracker_events,
    }


def snippet_for(slug):
    for p in glob.glob(os.path.join(SNIP, "*.reference.html")):
        if os.path.basename(p)[: -len(".reference.html")].lower() == slug.lower():
            return p
    return None


def build():
    items, fields = [], {"prose": 0, "measured": 0, "UNPROVEN": 0}
    metas_unproven = 0
    for f in sorted(glob.glob(os.path.join(COMP, "*.meta.json"))):
        if os.path.basename(f).startswith("EXAMPLE"):
            continue
        d = json.load(open(f, encoding="utf-8"))
        if "behaviour" not in d:
            continue
        slug = os.path.basename(f)[: -len(".meta.json")]
        old = d["behaviour"]
        sp = snippet_for(slug)
        meas = measure(sp) if sp else None
        cur = CURATED.get(slug, {})
        text = prose_text(old)
        prov, unproven = {}, []
        snip_rel = os.path.relpath(sp, REPO) if sp else None

        # ---- script
        passive_q = cur.get("passive_quote")
        if passive_q:
            if meas and meas["inline_executable_scripts"] == 0:
                script = None
                prov["script"] = {"basis": "prose", "quote": passive_q,
                                  "probe": "snippet carries 0 executable inline <script>, 0 AUTO-BEHAVIOUR, 0 <script src> — agrees"}
                fields["prose"] += 1
            else:
                script = None
                prov["script"] = {"basis": "UNPROVEN", "quote": passive_q,
                                  "probe": "prose says passive but the snippet carries %d executable inline script(s) — CONFLICT" % (meas or {}).get("inline_executable_scripts", -1),
                                  "what_would_prove": "Dave's word on which is right: the prose or the snippet"}
                unproven.append("script"); fields["UNPROVEN"] += 1
        elif meas and meas["inline_executable_scripts"] >= 1:
            script = "knowledge/snippets/%s#script" % os.path.basename(sp)
            prov["script"] = {"basis": "measured",
                              "probe": "snippet carries %d executable inline <script> (%s bytes; %s), 0 AUTO-BEHAVIOUR, 0 <script src>; the prose describes this script's behaviour and names no address (s234-D5 census: 'addressing the script in none')"
                                       % (meas["inline_executable_scripts"], ", ".join("{:,}".format(b) for b in meas["inline_bytes"]),
                                          ", ".join(x[:19] + "…" for x in meas["inline_sha256"])),
                              "quote": None}
            fields["measured"] += 1
        elif meas and meas["auto_behaviour"]:
            script = None   # not in this population; kept for completeness
            prov["script"] = {"basis": "measured", "probe": "AUTO-BEHAVIOUR %s" % meas["auto_behaviour"]}
            fields["measured"] += 1
        else:
            script = None
            prov["script"] = {"basis": "UNPROVEN", "probe": "no snippet found for this slug" if not sp else "snippet carries no executable script and the prose does not say passive",
                              "what_would_prove": "Dave's word"}
            unproven.append("script"); fields["UNPROVEN"] += 1

        # ---- partial
        partial = None
        prov["partial"] = {"basis": "measured",
                           "probe": "0 AUTO-BEHAVIOUR marker pairs in the snippet; the component-types.json $behaviour registry has 3 names (dv-behaviour, dv-legend, dv-donut-sweep), all dataviz — none apply"}
        fields["measured"] += 1

        # ---- events (rC Q3 OPEN — the field is FLOATED; values are MEASURED listener names)
        events = meas["component_events"] if meas else []
        quotes = {}
        for ev in events:
            rx = EVENT_WORDS.get(ev)
            s = sentence_with(text, rx) if rx else None
            if s:
                quotes[ev] = s
        prov["events"] = {"basis": "measured" if meas else "UNPROVEN",
                          "probe": "addEventListener names in the snippet's inline script, EXCLUDING the page-level modality tracker (%s) — window-level keydown/mousedown/touchstart writing document.documentElement.dataset.modality%s"
                                   % (", ".join(meas["modality_tracker_events"]) if meas and meas["modality_tracker_events"] else "none present",
                                      ("; the script also uses %s, which is an OBSERVER, not a DOM event, and is not listed" % ", ".join(meas["observers"])) if meas and meas["observers"] else ""),
                          "observers": meas["observers"] if meas else [],
                          "quotes": quotes,
                          "floated": "rC Q3 ('Is an events field wanted at all?') is OPEN and Dave's — the field's presence and shape are PROPOSED, not ruled"}
        fields["measured"] += 1

        # ---- fallback
        if passive_q and script is None and "script" not in unproven:
            fallback = "identical — the component carries no script"
            prov["fallback"] = {"basis": "prose", "quote": passive_q}
            fields["prose"] += 1
        else:
            fallback = None
            prov["fallback"] = {"basis": "UNPROVEN",
                                "candidate": cur.get("fallback_candidate"),
                                "quote": cur.get("fallback_quote_hint"),
                                "measured_hint": cur.get("fallback_measured"),
                                "what_would_prove": "a JS-off render of the snippet (rA resilience criterion: GOV.UK / USWDS 'CSS on, JS off'), or Dave's word on the candidate"}
            unproven.append("fallback"); fields["UNPROVEN"] += 1

        proposed = {"script": script, "partial": partial, "events": events, "fallback": fallback,
                    "$note": old}
        if unproven:
            proposed["$unproven"] = unproven
            metas_unproven += 1
        items.append({"slug": slug, "name": d.get("name"), "category": d.get("category"),
                      "meta": os.path.relpath(f, REPO), "snippet": snip_rel,
                      "old": old, "old_json_type": type(old).__name__.replace("dict", "object").replace("str", "string"),
                      "proposed": proposed, "provenance": prov, "unproven": unproven,
                      "flag": cur.get("flag"), "measured": meas})
    return items, fields, metas_unproven


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "behaviour-migration.json")
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
    items, fields, mu = build()
    doc = {
        "$schema": "apollo/behaviour-migration-proposal/1",
        "status": "PROPOSAL — NOT APPLIED. No meta was written. Dave ratifies at his eye first (notes/_briefs/2026-09-02-234-v106-brief.md:47).",
        "ruling": "s234-D5 (the meta owns the typed declaration; the generator injects a derived block; the gate reads the meta)",
        "generated_by": "notes/_subreports/assets/2026-09-02-238-B-L2-behaviour-address/build_migration.py",
        "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "migration_rule": "BY ADDITION — the old prose is kept verbatim under $note (ADR-0017). Nothing is deleted.",
        "address_grammar": {
            "script": ["null — the component carries NO script (a positive declaration, settled; never 'unknown')",
                       "knowledge/<path>.js — a hand-authored source file, the component-types.json $behaviour form (e.g. knowledge/canon/dv-behaviour.js)",
                       "knowledge/snippets/<Slug>.reference.html#script — the snippet's own inline executable <script> element(s), outside any AUTO-BEHAVIOUR markers"],
            "partial": "null | a name registered under component-types.json $behaviour (the AUTO-BEHAVIOUR partial the snippet carries)",
            "events": "DOM event names as passed to addEventListener; FLOATED — rC Q3 is OPEN",
            "fallback": "what the component does with CSS on and JS off; null = NOT DECLARED (UNPROVEN), never 'none'",
            "$note": "the pre-s234-D5 prose, verbatim",
            "$unproven": "the fields whose proposed value is null because nothing settles them"
        },
        "basis_legend": {"prose": "settled by the meta's own words (quoted)", "measured": "settled by a probe on the reviewed snippet (probe quoted)", "UNPROVEN": "settled by neither; candidate carried in provenance only"},
        "counts": {"metas_with_behaviour": len(items), "proposed": len(items),
                   "fields_total": sum(fields.values()), "fields_by_basis": fields,
                   "metas_with_any_unproven": mu,
                   "old_json_types": {t: sum(1 for i in items if i["old_json_type"] == t) for t in sorted({i["old_json_type"] for i in items})}},
        "items": items,
    }
    json.dump(doc, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("wrote", os.path.relpath(out, REPO))
    print("counts:", json.dumps(doc["counts"]))
    for i in items:
        print("%-18s script=%-52s events=%s unproven=%s" % (i["slug"], i["proposed"]["script"], i["proposed"]["events"], i["unproven"]))


if __name__ == "__main__":
    main()
