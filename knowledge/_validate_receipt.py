#!/usr/bin/env python3
"""
_validate_receipt.py — the PROVENANCE RECEIPT gate (s235-D2). The first thing
`_validate_screen.py <path>` does with a composed page.

WHY THIS EXISTS. `_detect_retrieval.py` (#231) can tell a SPLICE from a PARAPHRASE by
statistics — shingle fidelity against the snippet corpus — and it is a good instrument, but
it is an INFERENCE: it grades structure and reports a probability-shaped verdict. Dave, on
rA Q4: *"I always lean to real solutions not patches, and mechanical over inference."*
`s234-D6` is that leaning made architecture — **the page carries a receipt, and the gate's
first act is to PARSE it, so "did you invent this?" is a COMPARISON, not a judgement.**

THE KEY IS A CONTENT HASH — `s235-D1`, Dave at #235 on rC Q1. Not the filename, not the
slug: *"filenames and slugs can be renamed without the page changing"*. So the receipt
identifies each spliced region by `sha256` of THE PAGE'S OWN REGION BYTES, and this gate
re-hashes those bytes and compares. The accepted cost, priced by rC and taken with the
ruling: the hash moves on every regen serial, so **a receipt is valid against the pack
version it was minted from, never across cuts.** That is why `pack` rides in the receipt.

⛔ HASH THE SPLICED BYTES, NEVER THE REFERENCE FILE. If this gate hashed
`knowledge/snippets/<Name>.reference.html` and compared that to the receipt, every page
would pass — the reference is identical for a faithful splice and an invented paraphrase
alike, because it is not the thing under test. The subject is the region IN THE PAGE.

------------------------------------------------------------------------------- THE SHAPE

A generated page carries, in `<head>`, BESIDE `#token-manifest` and never inside it (the
`#token-manifest` precedent — the regex that proves it is
`knowledge/gen_component_partials.py:301`):

    <script type="application/json" id="provenance-receipt">
    {
      "$schema": "apollo/provenance-receipt/1",
      "pack": "1.0.5",
      "retrievalSet": null,
      "$retrievalSetNote": "rC Q4 (the retrieval-set membership marker) is OPEN — null, not invented.",
      "regions": [
        {"region": "Stat-card#1", "snippet": "Stat-card", "kind": "markup",
         "source": "knowledge/snippets/Stat-card.reference.html",
         "hash": "sha256:…", "bytes": 1234,
         "variant": {...}, "props": {...},
         "script": "knowledge/canon/dv-behaviour.js" | null}
      ]
    }

and marks each spliced region in its own bytes, in the HTML-comment marker grammar
`gen_component_partials.py` already uses for AUTO-BEHAVIOUR blocks:

    <!-- ===== APOLLO-SPLICE <region> START (source=<path> kind=<markup|style>) ===== -->
    …the spliced bytes…
    <!-- ===== APOLLO-SPLICE <region> END ===== -->

THE HASHED BYTES ARE DEFINED HERE AND ONLY HERE (`region_bytes`): everything strictly
between the START marker's closing `-->` and the `<!--` that opens the END marker, encoded
UTF-8, hashed sha256, no normalisation of any kind. The generator
(`knowledge/gen_provenance_receipt.py`) IMPORTS these functions rather than re-implementing
them, so the mint and the check can never drift apart — the [[no-gate-parses-the-artefact]]
remedy: one parse, in the consumer's grammar, shared.

--------------------------------------------------------------------------- WHAT IT CHECKS

  0. receipt PARSES              absent ⇒ FAIL:NO-RECEIPT (a NAMED refusal, exit 1)
                                 unparseable ⇒ FAIL:RECEIPT-UNPARSEABLE (never a traceback —
                                 [[a-crash-is-not-a-fail]])
  1. every receipted region is PRESENT in the page   ⇒ FAIL:REGION-MISSING
  2. every present region RE-HASHES to its receipt   ⇒ FAIL:HASH-MISMATCH, named by region
                                 slug AND the first differing byte offset against the source
                                 file when the source is readable, so the reader is pointed
                                 at the edit rather than told a number changed
  3. every SPLICE MARKER in the page is RECEIPTED    ⇒ FAIL:REGION-UNRECEIPTED (a region the
                                 receipt does not mention is provenance-free; a receipt that
                                 only covers what suits it is not a receipt)
  4. the declared behaviour address is LOADED        ⇒ FAIL:BEHAVIOUR-NOT-LOADED when the
                                 receipt names a `script` the page neither inlines (an
                                 AUTO-BEHAVIOUR block of that name) nor pulls in via
                                 <script src>. `script: null` reports NO-BEHAVIOUR-DECLARED
                                 — a state, not a failure: `meta.schema.json:197` still types
                                 `behaviour` as "optional behavioural notes" (object|array|
                                 string), so most metas have no ADDRESS to declare. Typing it
                                 is `s234-D5` and belongs to L2; this gate READS what is
                                 there today and never promotes prose to an address.
  5. the pack version is REPORTED, never enforced    — a receipt is valid against the pack it
                                 was minted from (s235-D1); comparing it to some "current"
                                 pack would red every archived page, which is not this gate's
                                 question.

------------------------------------------------------------------------------- VOCABULARY

ADR-0016. Its register grades PROVEN / CLAIMED / UNPROVEN and its finding is that **CLAIMED
is not a soft PROVEN** — the state our three worst defects hid in. The output vocabulary
here is that principle at gate scale:

  PASS                        measured, and it held
  FAIL:<reason>               measured, and it did not
  UNPROVEN:<what would prove it>   NOT measured — printed in full, never rounded into PASS

`UNPROVEN` lines do not fail the run on their own (they are honest gaps, not defects), but
they are printed above the verdict and counted in it, so a green is never quoted without
them. `retrievalSet: null` is the standing one: rC Q4 is open, and this gate will not invent
a membership marker to fill it.

EXIT CODES (the pack's convention — `check-with-gates/SKILL.md` § "Reading a verdict")
  0   PASS
  1   FAIL — including NO-RECEIPT. ⛔ 77/COULD-NOT-ASK was considered and REJECTED for the
      missing-receipt case: 77 is "the question was never asked", and a runner may legitimately
      report it apart from red. A page with no receipt HAS been asked and cannot answer — the
      brief's "never a silent pass" forbids any code an aggregator might read as not-red.
  2   REFUSED — bad arguments, unreadable path.

USAGE
  python3 knowledge/_validate_receipt.py <page.html> [more.html …] [--quiet] [--json]
  python3 knowledge/_validate_receipt.py --selftest      # bite-test (ADR-0005 §5)
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

# --------------------------------------------------------------- the shared primitives
# ONE home for the marker grammar and the hash. The generator imports these; nothing
# re-implements them. (A second implementation is how a mint and a check drift.)

RECEIPT_ID = "provenance-receipt"
RECEIPT_RE = re.compile(r'<script[^>]*id="%s"[^>]*>(.*?)</script>' % RECEIPT_ID, re.S)

SPLICE_START_RE = re.compile(
    r'<!--\s*=====\s*APOLLO-SPLICE\s+(?P<region>\S+)\s+START(?P<attrs>[^>]*?)=====\s*-->')
SPLICE_END_TMPL = "<!-- ===== APOLLO-SPLICE %s END ===== -->"
SPLICE_END_RE_TMPL = r'<!--\s*=====\s*APOLLO-SPLICE\s+%s\s+END\s*=====\s*-->'

SCHEMA = "apollo/provenance-receipt/1"


def splice_marker_start(region, source, kind):
    return ('<!-- ===== APOLLO-SPLICE %s START (source=%s kind=%s) ===== -->'
            % (region, source, kind))


def splice_marker_end(region):
    return SPLICE_END_TMPL % region


def sha256_of(text):
    """sha256 of `text` as UTF-8 bytes, prefixed. No normalisation — the bytes are the key."""
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def region_bytes(html, region):
    """THE DEFINITION of a spliced region's bytes: everything strictly between the START
    marker's closing `-->` and the `<!--` opening the END marker. Returns (text, span) or
    (None, None) when the region is not marked, and raises nothing — a malformed pair is
    reported by the caller as a named failure, never as a traceback."""
    for m in SPLICE_START_RE.finditer(html):
        if m.group("region") != region:
            continue
        end = re.search(SPLICE_END_RE_TMPL % re.escape(region), html[m.end():])
        if not end:
            return None, None
        a = m.end()
        b = m.end() + end.start()
        return html[a:b], (a, b)
    return None, None


def marked_regions(html):
    """Every region NAME the page marks, in document order (duplicates preserved so an
    accidental double-splice of one id is visible rather than silently deduped)."""
    return [m.group("region") for m in SPLICE_START_RE.finditer(html)]


def parse_receipt(html):
    """(receipt|None, error|None). Never raises on malformed input."""
    m = RECEIPT_RE.search(html)
    if not m:
        return None, "NO-RECEIPT"
    raw = m.group(1)
    try:
        obj = json.loads(raw)
    except Exception as e:                                   # [[a-crash-is-not-a-fail]]
        return None, "RECEIPT-UNPARSEABLE — %s" % re.sub(r"\s+", " ", str(e))[:120]
    if not isinstance(obj, dict):
        return None, "RECEIPT-MALFORMED — top level is %s, expected object" % type(obj).__name__
    if not isinstance(obj.get("regions"), list):
        return None, "RECEIPT-MALFORMED — no `regions` array"
    return obj, None


# ------------------------------------------------------------------ behaviour addressing

AUTO_BEHAVIOUR_RE = re.compile(
    r'<!--\s*=====\s*AUTO-BEHAVIOUR\s+(?P<name>\S+)\s+START[^>]*=====\s*-->')
SCRIPT_SRC_RE = re.compile(r'<script[^>]+src="([^"]+)"')


def behaviour_loaded(html, address):
    """Is `address` (e.g. 'knowledge/canon/dv-behaviour.js') actually loaded by this page?
    TWO legal forms, both mechanical:
      inline  — an AUTO-BEHAVIOUR block whose NAME is the address's stem (this is how a
                snippet carries a behaviour today; gen_component_partials.py injects it)
      linked  — a <script src> whose path ends with the address's basename
    Returns (True, how) or (False, None)."""
    stem = os.path.splitext(os.path.basename(address))[0]
    base = os.path.basename(address)
    for m in AUTO_BEHAVIOUR_RE.finditer(html):
        if m.group("name") == stem:
            return True, "inline AUTO-BEHAVIOUR %s block" % stem
    for src in SCRIPT_SRC_RE.findall(html):
        if src.split("?")[0].rstrip("/").endswith(base):
            return True, '<script src="%s">' % src
    return False, None


# ------------------------------------------------------------------------------ the gate

def first_diff_offset(a, b):
    n = min(len(a), len(b))
    for i in range(n):
        if a[i] != b[i]:
            return i
    return n if len(a) != len(b) else None


def _source_region(r):
    """Re-cut the region from the file the receipt NAMES, for the first-differing-offset
    hint ONLY.

    ⛔ THIS IS NEVER HASHED AND NEVER DECIDES A VERDICT. Comparing the receipt to the
    reference file is exactly the defect the docstring's ⛔ names — every page would pass.
    The verdict is already settled by the time this runs (the hashes disagreed); all this
    does is point the reader at the byte that moved instead of handing them two digests.
    It is soft-imported and every failure path returns None, so a gate run never depends on
    the generator being present (the shipped pack may carry the gate and not the mint)."""
    source, select, kind = r.get("source"), r.get("select"), r.get("kind") or "markup"
    if not source:
        return None
    path = None
    for cand in (source, os.path.join(REPO, source), os.path.join(HERE, source)):
        if os.path.isfile(cand):
            path = cand; break
    if not path:
        return None
    try:
        src = open(path, encoding="utf-8").read()
        gen = __import__("gen_provenance_receipt")          # lazy: no cycle at import time
        if kind == "markup" and select:
            return gen.extract_element(src, select)[0]
        if kind == "style":
            return gen.extract_style(src)[0]
        if kind == "behaviour" and r.get("behaviour"):
            return gen.extract_behaviour(src, r["behaviour"])[0]
    except Exception:
        return None
    except SystemExit:
        return None
    return None


def check(path):
    """-> (verdict_lines, fails, unproven). `fails` non-empty ⇒ the page is red."""
    lines, fails, unproven = [], [], []
    try:
        html = open(path, encoding="utf-8").read()
    except Exception as e:
        return ["FAIL:UNREADABLE — %s (%s)" % (path, e)], ["UNREADABLE"], []

    receipt, err = parse_receipt(html)
    if receipt is None:
        marks = marked_regions(html)
        detail = ("the page marks %d APOLLO-SPLICE region(s) and receipts none of them"
                  % len(marks)) if marks else \
                 ("no <script type=\"application/json\" id=\"%s\"> block in the document; "
                  "mint one with `python3 knowledge/gen_provenance_receipt.py --mint %s`"
                  % (RECEIPT_ID, os.path.basename(path)))
        lines.append("FAIL:%s — %s" % (err, detail))
        return lines, [err.split(" ")[0]], []

    pack = receipt.get("pack")
    lines.append("- pack: %s (REPORTED, not enforced — s235-D1: a receipt is valid against "
                 "the pack it was minted from)" % (pack if pack else "UNDECLARED"))
    if receipt.get("$schema") != SCHEMA:
        unproven.append("UNPROVEN:schema — receipt declares $schema=%r, this gate parses %r; "
                        "a matching $schema would prove the two agree on field meanings"
                        % (receipt.get("$schema"), SCHEMA))
    if receipt.get("retrievalSet") is None:
        unproven.append("UNPROVEN:retrievalSet — null (rC Q4, the retrieval-set membership "
                        "marker, is OPEN and was not invented here); a ruled membership "
                        "marker carried in the receipt would prove which retrieval set the "
                        "page was built from")

    regions = receipt["regions"]
    receipted = []
    for i, r in enumerate(regions):
        if not isinstance(r, dict) or not r.get("region"):
            fails.append("RECEIPT-MALFORMED")
            lines.append("FAIL:RECEIPT-MALFORMED — regions[%d] has no `region` id" % i)
            continue
        receipted.append(r["region"])
        rid = r["region"]
        want = r.get("hash")
        text, _span = region_bytes(html, rid)
        if text is None:
            fails.append("REGION-MISSING")
            lines.append("FAIL:REGION-MISSING — `%s` is receipted but the page carries no "
                         "matching APOLLO-SPLICE START/END pair" % rid)
            continue
        if not want:
            unproven.append("UNPROVEN:%s — region present but the receipt declares no hash; "
                            "re-minting the receipt would prove the bytes" % rid)
            continue
        got = sha256_of(text)
        if got != want:
            comparand = _source_region(r)
            hint = ""
            if comparand is not None:
                off = first_diff_offset(text.strip(), comparand.strip())
                if off is not None:
                    ctx = re.sub(r"\s+", " ", text.strip()[max(0, off - 28):off + 28])
                    hint = (" — first differing byte at offset %d of the region, near …%s…"
                            % (off, ctx))
                else:
                    hint = (" — the region's bytes still match %s, so the RECEIPT is stale: "
                            "re-mint it" % r.get("source"))
            if not hint:
                hint = (" — region is %d bytes now; the receipt was minted over different "
                        "bytes" % len(text))
            fails.append("HASH-MISMATCH")
            lines.append("FAIL:HASH-MISMATCH — `%s` (%s) does not match its receipt%s. "
                         "receipt %s / page %s"
                         % (rid, r.get("snippet") or "?", hint, want[:19] + "…", got[:19] + "…"))
            continue
        note = "✅ %s (%s, %d bytes)" % (rid, r.get("kind") or "?", len(text))
        addr = r.get("script")
        if addr:
            ok, how = behaviour_loaded(html, addr)
            if ok:
                note += " · behaviour %s LOADED (%s)" % (addr, how)
            else:
                fails.append("BEHAVIOUR-NOT-LOADED")
                lines.append("FAIL:BEHAVIOUR-NOT-LOADED — `%s` declares script `%s`, and the "
                             "page neither inlines an AUTO-BEHAVIOUR block of that name nor "
                             "loads it with <script src>" % (rid, addr))
                continue
        elif (r.get("kind") or "markup") == "markup":
            # only a MARKUP region can carry a behaviour; saying NO-BEHAVIOUR-DECLARED of a
            # style or behaviour region is noise that trains the reader to skim the line.
            note += " · behaviour NO-BEHAVIOUR-DECLARED"
        lines.append("- " + note)

    for rid in marked_regions(html):
        if rid not in receipted:
            fails.append("REGION-UNRECEIPTED")
            lines.append("FAIL:REGION-UNRECEIPTED — the page splices `%s` and the receipt "
                         "does not mention it" % rid)
    return lines, fails, unproven


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    quiet = "--quiet" in argv
    as_json = "--json" in argv
    if not args:
        print("REFUSED: _validate_receipt.py needs at least one page path.\n"
              "  python3 knowledge/_validate_receipt.py <page.html> [more.html …]")
        return 2
    for p in args:
        if not os.path.isfile(p):
            print("REFUSED: not a file — %s" % p)
            return 2
    red = False
    out = {}
    for p in args:
        lines, fails, unproven = check(p)
        red = red or bool(fails)
        out[p] = {"fails": fails, "unproven": unproven, "lines": lines}
        if as_json:
            continue
        print("## %s" % p)
        for ln in lines:
            if not quiet or ln.startswith("FAIL"):
                print("  " + ln)
        for u in unproven:
            print("  " + u)
        print("  verdict: " + ("PASS" if not fails else
                               "FAIL:" + ",".join(sorted(set(fails))))
              + (" (+%d UNPROVEN)" % len(unproven) if unproven else ""))
    if as_json:
        print(json.dumps(out, indent=1))
    print("\nRESULT: " + ("PASS ✅" if not red else "FAIL ❌"))
    return 1 if red else 0


# --------------------------------------------------------------------------- bite-test
def selftest():
    """ADR-0005 §5 — every arm must be able to FAIL, and be SHOWN failing here.
    [[mutation-tests-the-clause-not-the-feature]]: each arm drives `check()` on a real
    temporary file, not on an internal helper."""
    import tempfile
    ok = True

    def arm(label, html, expect_fail, expect_unproven=None):
        nonlocal ok
        d = tempfile.mkdtemp()
        p = os.path.join(d, "arm.html")
        open(p, "w", encoding="utf-8").write(html)
        lines, fails, unproven = check(p)
        got = ",".join(sorted(set(fails))) or "PASS"
        good = (got == expect_fail)
        if expect_unproven is not None:
            good = good and any(expect_unproven in u for u in unproven)
        ok = ok and good
        print(("  ✅ " if good else "  ❌ ") + label + " -> " + got +
              (" | unproven=%d" % len(unproven) if unproven else ""))
        if not good:
            for ln in lines:
                print("       " + ln)

    body = '<p class="x">hello</p>'
    def page(region_body, hsh, extra_head="", extra_body="", script=None, pack="1.0.5",
             retrieval=None):
        rec = {"$schema": SCHEMA, "pack": pack, "retrievalSet": retrieval,
               "regions": [{"region": "Demo#1", "snippet": "Demo", "kind": "markup",
                            "source": "knowledge/snippets/Demo.reference.html",
                            "hash": hsh, "bytes": len(region_body), "script": script}]}
        return ("<!DOCTYPE html><html><head>"
                '<script type="application/json" id="token-manifest">{"vars":{}}</script>'
                '<script type="application/json" id="%s">%s</script>%s</head><body>%s\n%s\n%s%s'
                "</body></html>"
                % (RECEIPT_ID, json.dumps(rec), extra_head,
                   splice_marker_start("Demo#1", "knowledge/snippets/Demo.reference.html",
                                       "markup"),
                   region_body, splice_marker_end("Demo#1"), extra_body))

    # the region's bytes are "\n" + body + "\n" (see page(): marker, newline, body, newline)
    good_hash = sha256_of("\n" + body + "\n")
    arm("A  faithful splice", page(body, good_hash), "PASS")
    arm("B  ONE BYTE changed inside the region",
        page(body.replace("hello", "hellp"), sha256_of("\n" + body + "\n")), "HASH-MISMATCH")
    arm("C  no receipt at all",
        "<!DOCTYPE html><html><head></head><body>%s</body></html>" % body, "NO-RECEIPT")
    arm("D  receipt present but not JSON",
        '<html><head><script type="application/json" id="%s">{not json</script></head>'
        "<body></body></html>" % RECEIPT_ID, "RECEIPT-UNPARSEABLE")
    arm("E  receipted region absent from the page",
        '<html><head><script type="application/json" id="%s">%s</script></head><body></body>'
        "</html>" % (RECEIPT_ID, json.dumps(
            {"$schema": SCHEMA, "pack": "1.0.5", "regions": [
                {"region": "Ghost#1", "hash": "sha256:0", "kind": "markup"}]})),
        "REGION-MISSING")
    arm("F  page splices a region the receipt never mentions",
        page(body, sha256_of("\n" + body + "\n"),
             extra_body="\n" + splice_marker_start("Extra#1", "x", "markup") + "\nzz\n"
                        + splice_marker_end("Extra#1")),
        "REGION-UNRECEIPTED")
    arm("G  behaviour declared, not loaded",
        page(body, sha256_of("\n" + body + "\n"), script="knowledge/canon/dv-behaviour.js"),
        "BEHAVIOUR-NOT-LOADED")
    arm("H  behaviour declared AND inlined",
        page(body, sha256_of("\n" + body + "\n"), script="knowledge/canon/dv-behaviour.js",
             extra_body="\n<!-- ===== AUTO-BEHAVIOUR dv-behaviour START (dataviz) ===== -->"
                        "\n<script>0</script>\n"
                        "<!-- ===== AUTO-BEHAVIOUR dv-behaviour END ===== -->"),
        "PASS")
    arm("I  retrievalSet null is UNPROVEN, not a pass and not a fail",
        page(body, sha256_of("\n" + body + "\n")), "PASS", expect_unproven="retrievalSet")
    print("SELFTEST: " + ("PASS ✅" if ok else "FAIL ❌"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main(sys.argv[1:]))
