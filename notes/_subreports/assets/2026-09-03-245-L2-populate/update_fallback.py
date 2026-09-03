#!/usr/bin/env python3
"""
update_fallback.py — #245 L2-populate, s245-D5. Writes `behaviour.fallback` into the 14 interactive
L2 metas ONLY where jsoff_render.py PROVED the reading (verdict PROVEN in jsoff-render.json); the
rest stay `null` + `$unproven: ["fallback"]`. Every one of the 14 gets `$fallbackRender`, a
$-prefixed provenance note (the schema's `patternProperties ^\\$` allows it) saying PROVEN/UNPROVEN
by the JS-off render and what was seen. The fallback SENTENCES below are the MEASURED readings —
each clause maps to a named assertion in jsoff-render.txt — not the #238 candidates copied.

Same textual-span discipline as migrate_metas.py (reconstruction-proved, schema-validated).
  python3 update_fallback.py --dry-run | --write
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from migrate_metas import value_span, key_indent, REPO, SCHEMA  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "jsoff-render.json"), encoding="utf-8"))
EVID = "notes/_subreports/assets/2026-09-03-245-L2-populate/jsoff-render.json"

PROVEN_TEXT = {
 "amount-input": "A native text input: `inputmode=decimal` is an attribute and stays; typed characters are kept verbatim (no stripping, no en-GB grouping, no two-decimal normalisation); no is-completed weight and no message on blur.",
 "anchor-nav": "Fragment links still jump — they are real `href=\"#…\"` links and each section carries `scroll-margin-top:56px`; the authored `aria-current` stays where the markup put it and never moves.",
 "date-picker": "The text input works as a native field (DD/MM/YYYY typed by hand); the tail button does nothing and the panel never opens (`aria-expanded` stays false); no on-blur validation message, even for an impossible date.",
 "date-range-picker": "Both fields work as native text inputs; neither tail button opens the panel; no per-field and no pair validation on blur.",
 "form-layout": "The form submits natively (a GET; `novalidate` is authored, so native constraint validation is off as well); no per-field errors, no error summary, no sort-code masking.",
 "secure-entry": "Six independent inputs; no auto-advance, no paste or typing distribution, no verify state; `autocomplete=one-time-code` (an attribute) stays on the first cell.",
 "stepper": "Only the panel the markup authors as current is shown; Next and Back do nothing; no announcement. The dots-to-line collapse is a container query (CSS, 520px) and still fires.",
 "tab-bar": "Each item is a native `<a>` and takes keyboard focus; the authored `aria-current` stands; clicking another item moves nothing — the active pill stays where the markup put it.",
 "textarea": "A native textarea: vertical-only resize is CSS and holds; the counter does not move, no warn weight, no announcement.",
 "time-picker": "The text input works as a native field (HH:MM typed by hand); the tail button does nothing and the list never opens; no on-blur validation message.",
 "tree": "Every branch renders in the open or closed state the markup authors (collapsed groups hidden by CSS); no keyboard model, no expand or collapse on click, no lazy load.",
}
SEEN = {
 "calendar": "the live grid's <tbody id=cal-body> is EMPTY (innerHTML length 0) and #cal-title is a blank &nbsp; — the days are script-rendered, so the candidate 'server-authored buttons' is FALSE; next-month and the live region do nothing",
 "command-palette": "the specimen authors the palette OPEN (role=dialog visible, combobox aria-expanded=true), so 'cannot open' is not measurable on the snippet; Ctrl+K adds nothing, typing does not filter (5 options before and after)",
 "file-upload": "the 'Browse files' <button> is script-wired and opens NO chooser JS-off; the <label for=fu-input> DOES open the native chooser; nothing stages, no progress bar, no announcement — a different reading from the candidate's conditional, not the candidate",
}


def main(write):
    import jsonschema
    V = jsonschema.Draft7Validator(json.load(open(SCHEMA, encoding="utf-8")))
    n_set = n_null = 0
    for slug, v in R["verdicts"].items():
        p = os.path.join(REPO, "knowledge/components/%s.meta.json" % slug)
        raw = open(p, encoding="utf-8").read(); obj = json.loads(raw)
        b = dict(obj["behaviour"]); assert "script" in b and b["fallback"] is None, slug
        asserts = v["asserts"]; failed = v["failed"]
        if v["verdict"] == "PROVEN":
            b["fallback"] = PROVEN_TEXT[slug]; b.pop("$unproven", None)
            b["$fallbackRender"] = ("PROVEN by JS-off render #245 (2026-09-03): %d/%d named assertions held, JavaScript disabled at the context, "
                                    "page.goto(file://) — %s · jsoff-%s-{before,after}.png" % (asserts, asserts, EVID, slug))
            n_set += 1
        else:
            b["$unproven"] = ["fallback"]
            b["$fallbackRender"] = ("UNPROVEN by JS-off render #245 (2026-09-03) — %s. %d/%d assertions held; failed: %s. %s · jsoff-%s-{before,after}.png"
                                    % (SEEN[slug], asserts - len(failed), asserts, "; ".join(failed), EVID, slug))
            n_null += 1
        # rebuild the object so key order is script/partial/events/fallback/$note/$unproven/$fallbackRender
        order = ["script", "partial", "events", "fallback", "$note", "$unproven", "$fallbackRender"]
        new = {k: b[k] for k in order if k in b}
        s, e = value_span(raw, "behaviour"); ind = key_indent(raw, s)
        body = json.dumps(new, indent=2, ensure_ascii=False)
        body = "\n".join((" " * ind + ln) if k else ln for k, ln in enumerate(body.splitlines()))
        out = raw[:s] + body + raw[e:]
        assert out[:s] + raw[s:e] + out[s + len(body):] == raw, slug
        o2 = json.loads(out); want = dict(obj); want["behaviour"] = new; assert o2 == want, slug
        errs = list(V.iter_errors(o2)); assert not errs, (slug, [x.message for x in errs])
        print("%s %-18s %-8s fallback=%s" % ("WRITE" if write else "DRY  ", slug, v["verdict"], "SET" if new["fallback"] else "null"))
        if write: open(p, "w", encoding="utf-8").write(out)
    print("proven/set %d · unproven/null %d · of %d" % (n_set, n_null, len(R["verdicts"])))


if __name__ == "__main__":
    main("--write" in sys.argv)
