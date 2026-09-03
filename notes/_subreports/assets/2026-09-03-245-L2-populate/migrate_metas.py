#!/usr/bin/env python3
"""
migrate_metas.py — #245 L2-populate. Applies the 20 L2 proposals (s245-D1…D5) to the LIVE
knowledge/components/<slug>.meta.json files BY ADDITION, as a TEXTUAL SPAN REPLACEMENT of the
`"behaviour"` value only — the same discipline as `_inscribe_ruling.py` (18 of the 20 metas do
not round-trip through json.dumps, so a load→mutate→dump would reformat whole files).

  python3 migrate_metas.py --dry-run     # prove every span, write nothing
  python3 migrate_metas.py --write

Per meta: the old prose value is kept VERBATIM under `$note` (ADR-0017); `script`/`partial`/
`events` come from the proposal; `fallback` is the proposal's value (6 passive: settled by prose +
probe; 14 interactive: null + `$unproven: ["fallback"]` — settled LATER by the JS-off render,
s245-D5, via update_fallback.py, never on a reading).

PROOF per file: (1) exactly one top-level `"behaviour"` key; (2) removing the new span and
re-inserting the old span gives back the ORIGINAL BYTES `==`; (3) the result parses and equals the
original object with only `behaviour` replaced; (4) the new `behaviour` validates against
knowledge/components/meta.schema.json (Draft 7).
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
MIG = os.path.join(REPO, "notes/_subreports/assets/2026-09-02-238-B-L2-behaviour-address/behaviour-migration.json")
SCHEMA = os.path.join(REPO, "knowledge/components/meta.schema.json")


def value_span(text, key):
    """(start, end) of the VALUE of top-level `"key"` — string-aware depth scan."""
    depth = 0; in_str = False; esc = False; i = 0; hits = []
    needle = '"%s"' % key
    while i < len(text):
        c = text[i]
        if in_str:
            if esc: esc = False
            elif c == "\\": esc = True
            elif c == '"': in_str = False
            i += 1; continue
        if c == '"':
            if depth == 1 and text.startswith(needle, i):
                j = i + len(needle)
                while text[j] in " \t\r\n": j += 1
                if text[j] == ":":
                    hits.append(j + 1)
            in_str = True
        elif c in "[{": depth += 1
        elif c in "]}": depth -= 1
        i += 1
    if len(hits) != 1:
        raise SystemExit("REFUSED: %d top-level %r keys, expected 1" % (len(hits), key))
    s = hits[0]
    while text[s] in " \t\r\n": s += 1
    # scan the value
    depth = 0; in_str = False; esc = False; j = s
    if text[s] == '"':
        in_str = True; j = s + 1
        while True:
            c = text[j]
            if esc: esc = False
            elif c == "\\": esc = True
            elif c == '"': return s, j + 1
            j += 1
    while True:
        c = text[j]
        if in_str:
            if esc: esc = False
            elif c == "\\": esc = True
            elif c == '"': in_str = False
        elif c == '"': in_str = True
        elif c in "[{": depth += 1
        elif c in "]}":
            depth -= 1
            if depth == 0: return s, j + 1
        j += 1


def key_indent(text, start):
    ls = text.rfind("\n", 0, start) + 1
    return len(text[ls:]) - len(text[ls:].lstrip(" "))


def main(write):
    import jsonschema
    schema = json.load(open(SCHEMA, encoding="utf-8"))
    validator = jsonschema.Draft7Validator(schema)
    items = json.load(open(MIG, encoding="utf-8"))["items"]
    done = 0
    for it in items:
        p = os.path.join(REPO, it["meta"])
        raw = open(p, encoding="utf-8").read()
        obj = json.loads(raw)
        if obj.get("behaviour") != it["old"]:
            print("SKIP %s: live behaviour != proposal's `old` (already migrated?)" % it["slug"]); continue
        s, e = value_span(raw, "behaviour")
        assert json.loads(raw[s:e]) == it["old"], it["slug"]
        new = dict(it["proposed"])
        # s245-D4: events kept, optional, GENERATED (measured) — the proposal's list is the measurement
        ind = key_indent(raw, s)
        body = json.dumps(new, indent=2, ensure_ascii=False)
        body = "\n".join((" " * ind + ln) if k else ln for k, ln in enumerate(body.splitlines()))
        out = raw[:s] + body + raw[e:]
        # proofs
        assert out[:s] + raw[s:e] + out[s + len(body):] == raw, "reconstruction failed " + it["slug"]
        o2 = json.loads(out)
        want = dict(obj); want["behaviour"] = new
        assert o2 == want, "object drift " + it["slug"]
        errs = sorted(validator.iter_errors(o2), key=lambda x: list(x.path))
        assert not errs, (it["slug"], [x.message for x in errs])
        print("%s %-18s span %d→%d bytes, indent %d, fallback=%s, unproven=%s" % (
            "WRITE" if write else "DRY  ", it["slug"], e - s, len(body), ind,
            "null" if new["fallback"] is None else "set", new.get("$unproven", [])))
        if write:
            open(p, "w", encoding="utf-8").write(out)
        done += 1
    print("%d/20 %s" % (done, "written" if write else "would write"))
    return 0 if done == 20 else 1


if __name__ == "__main__":
    sys.exit(main("--write" in sys.argv))
