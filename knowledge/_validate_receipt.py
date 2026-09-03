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
  4b. THE META ADDRESS (s234-D5, #238 lane B) — the meta is the ONE HOME, and this gate reads
      it. For every MARKUP region the gate finds `knowledge/components/<slug>.meta.json` (the
      snippet stem, case-insensitively — the generate-from-canon SKILL's own rule) and reads
      `behaviour`:
        TYPED  (an object carrying `script`)  → the address is RESOLVED and then checked LOADED:
               `script: null`                            a positive "no script" — noted, never failed
               `knowledge/<path>.js`                     file must exist; loaded = AUTO-BEHAVIOUR block
                                                         of that stem, or <script src> of that basename
               `knowledge/snippets/<Slug>.reference.html#script`
                                                         the snippet's own inline executable <script>
                                                         element(s), outside AUTO-BEHAVIOUR markers;
                                                         loaded = the page carries EVERY one of them
                                                         BYTE-IDENTICAL (sha256, no normalisation —
                                                         the s235-D1 posture; a whitespace-shifted
                                                         copy is named in the hint, never passed)
               `partial: <name> | [<name>, …]`           each name must be registered in
                                                         component-types.json $behaviour (s245-D2: one
                                                         name, a list, or null); loaded = an
                                                         AUTO-BEHAVIOUR block per name
               ⇒ FAIL:BEHAVIOUR-ADDRESS-UNRESOLVABLE (grammar, missing file, snippet with no
                 inline script) · FAIL:BEHAVIOUR-NOT-LOADED · FAIL:BEHAVIOUR-PARTIAL-UNREGISTERED
               · FAIL:BEHAVIOUR-ADDRESS-FOREIGN when a #script names ANOTHER component's snippet
                 (shared behaviour is a registered partial, never a pointer into another file —
                 otherwise any page carrying the other component would satisfy the check)
               · FAIL:BEHAVIOUR-ADDRESS-DISAGREES when the receipt's own `script` names a
                 different address from the meta's — the receipt is a COPY, the meta is the home.
        PROSE  (pre-s234-D5 notes)  → ⛔ FAIL:BEHAVIOUR-PROSE (s245-D3, #245, the day the 20 were
               typed): a `behaviour` key that is still a string / list / object without `script`
               is a named BLOCK, not an UNPROVEN line — the meta is the one home and prose there
               addresses nothing. Population on the day of the ruling: 0 live metas (the 20 are
               typed; 116 carry no key). Before #245 this was one `UNPROVEN:behaviour-address` line.
        NONE   (no `behaviour` key)  → UNPROVEN, note `meta:NONE` — stays UNPROVEN until rC Q3 and
               the dataviz migration settle what 'none' means (s245-D3 rules PROSE only).
      ⛔ THE CHECK IS TWO-SIDED BY CONSTRUCTION (the L2 brief's pitfall 3, "a gate that checks
      the meta and not the page, or the reverse"): the META side is `resolve_address` (does what
      the meta names exist?) and the PAGE side is `address_loaded` (does the page carry it?), and
      a region passes only when both do. Selftest arms J–Z2 plant a defect on each side.
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
sys.path.insert(0, HERE)
from _htmlmask import mask_comments        # noqa: E402 — ONE comment mask (#218 W-92), never a copy

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


# ------------------------------------------------------------------ the META address (s234-D5)
# #238 lane B (L2). ONE home for the address grammar and its resolver: the generator
# (`gen_component_partials.py`, which derives the snippet's #behaviour-manifest block from the
# meta) IMPORTS these, the way the mint imports the marker grammar above. `ROOT` is the
# knowledge/ directory the addresses are resolved against; the selftest points it at a
# temporary tree so every arm drives real files.

ROOT = HERE
ADDRESS_RE = re.compile(
    r'^knowledge/(?:(?P<file>[^#\s]+\.js)|snippets/(?P<snippet>[^#\s/]+\.reference\.html)#script)$')
SCRIPT_EL_RE = re.compile(r'<script\b([^>]*)>(.*?)</script>', re.S)
AUTO_BEHAVIOUR_PAIR_RE = re.compile(
    r'<!--\s*=====\s*AUTO-BEHAVIOUR\s+(\S+)\s+START[^>]*=====\s*-->.*?'
    r'<!--\s*=====\s*AUTO-BEHAVIOUR\s+\1\s+END\s*=====\s*-->', re.S)
EXECUTABLE_TYPES = (None, "text/javascript", "module")


def inline_scripts(html, exclude_auto=True):
    """The document's inline EXECUTABLE <script> bodies, in order: no `src`, `type` absent or
    text/javascript or module (so #token-manifest / #behaviour-manifest / a receipt, all
    application/json, are never scripts). With `exclude_auto`, bodies inside an AUTO-BEHAVIOUR
    marker pair are skipped — those carry their own registry address and are not what
    `#script` denotes.

    ⛔ LOCATED in the comment-masked copy, SLICED from the original bytes (#211 lanes R6/R7,
    the `gen_component_partials.py` discipline): a <script> inside an HTML comment is dead and
    is never 'the snippet's script'; the AUTO-BEHAVIOUR markers ARE comments and are read RAW."""
    auto = [m.span() for m in AUTO_BEHAVIOUR_PAIR_RE.finditer(html)] if exclude_auto else []
    out = []
    for m in SCRIPT_EL_RE.finditer(mask_comments(html)):
        attrs = html[m.start(1):m.end(1)]
        if re.search(r'\bsrc\s*=', attrs):
            continue
        t = re.search(r'\btype\s*=\s*"([^"]*)"', attrs)
        if (t.group(1).strip() if t else None) not in EXECUTABLE_TYPES:
            continue
        if any(a <= m.start() < b for a, b in auto):
            continue
        out.append((html[m.start(2):m.end(2)], m.span(2)))
    return out


def snippet_file(name):
    """knowledge/snippets/<name>.reference.html, matched CASE-INSENSITIVELY on the stem (the
    SKILL's rule: 'summary' ↔ 'Summary.reference.html'). None when absent."""
    d = os.path.join(ROOT, "snippets")
    if not os.path.isdir(d):
        return None
    want = (name or "").lower().replace(".reference.html", "")
    for fn in sorted(os.listdir(d)):
        if fn.endswith(".reference.html") and fn[:-len(".reference.html")].lower() == want:
            return os.path.join(d, fn)
    return None


def meta_path_for(snippet_name):
    """knowledge/components/<slug>.meta.json for a snippet stem, case-insensitively; EXAMPLE-*
    metas are never a match. None when absent."""
    d = os.path.join(ROOT, "components")
    if not os.path.isdir(d) or not snippet_name:
        return None
    want = snippet_name.lower().replace(".reference.html", "")
    for fn in sorted(os.listdir(d)):
        if fn.endswith(".meta.json") and not fn.startswith("EXAMPLE") \
                and fn[:-len(".meta.json")].lower() == want:
            return os.path.join(d, fn)
    return None


def load_meta(path):
    """The meta as a dict, or None — never a traceback ([[a-crash-is-not-a-fail]])."""
    try:
        obj = json.load(open(path, encoding="utf-8"))
        return obj if isinstance(obj, dict) else None
    except Exception:
        return None


def typed_behaviour(meta):
    """The meta's TYPED behaviour object (s234-D5: an object carrying the `script` key), else
    None. Prose — a string, a list, or an object of notes with no `script` key — is not an
    address and is never promoted to one here."""
    b = (meta or {}).get("behaviour")
    return b if isinstance(b, dict) and "script" in b else None


def behaviour_state(meta):
    """TYPED | PROSE | NONE — what the meta says about behaviour, as a word the gate prints."""
    if meta is None:
        return "NO-META"
    if typed_behaviour(meta) is not None:
        return "TYPED"
    return "PROSE" if "behaviour" in meta else "NONE"


def registered_partials():
    """The $behaviour names component-types.json registers, name -> repo-relative source."""
    reg = {}
    p = os.path.join(ROOT, "component-types.json")
    try:
        ct = json.load(open(p, encoding="utf-8"))
    except Exception:
        return reg
    def walk(d):
        if isinstance(d, dict):
            for k, v in d.items():
                if k == "$behaviour" and isinstance(v, dict):
                    for n, b in v.items():
                        if isinstance(b, dict) and b.get("source"):
                            reg[n] = "knowledge/" + b["source"]
                else:
                    walk(v)
    walk(ct)
    return reg


def resolve_address(addr):
    """THE META SIDE. -> (kind, parts, err). kind 'file' | 'inline'; parts = [(label, text)]
    the address denotes; err = a named reason when it resolves to nothing. Never raises."""
    if not isinstance(addr, str):
        return None, [], "is not a string"
    m = ADDRESS_RE.match(addr)
    if not m:
        return None, [], ("is outside the address grammar (null | knowledge/<path>.js | "
                          "knowledge/snippets/<Slug>.reference.html#script)")
    if m.group("file"):
        path = os.path.join(ROOT, m.group("file"))
        if not os.path.isfile(path):
            return "file", [], "names a file that does not exist (%s)" % path
        try:
            return "file", [(addr, open(path, encoding="utf-8").read())], None
        except Exception as e:
            return "file", [], "names a file that cannot be read (%s)" % e
    sp = snippet_file(m.group("snippet"))
    if not sp:
        return "inline", [], "names a snippet that does not exist (%s)" % m.group("snippet")
    try:
        html = open(sp, encoding="utf-8").read()
    except Exception as e:
        return "inline", [], "names a snippet that cannot be read (%s)" % e
    bodies = inline_scripts(html)
    if not bodies:
        return "inline", [], ("names a snippet that carries NO inline executable <script> outside "
                              "AUTO-BEHAVIOUR markers — #script resolves to nothing")
    stem = os.path.basename(sp)[:-len(".reference.html")]
    return "inline", [("%s#script[%d]" % (stem, i), body) for i, (body, _s) in enumerate(bodies)], None


def foreign_script_address(addr, own_snippet_stem):
    """A `#script` address must name the component's OWN snippet: shared behaviour travels as a
    registered PARTIAL (component-types.json $behaviour), never as a pointer into another
    component's file — otherwise 'the page loads what the meta declares' is satisfied by any
    page that happens to carry the other component. -> the foreign stem, or None."""
    m = ADDRESS_RE.match(addr or "")
    if not m or not m.group("snippet") or not own_snippet_stem:
        return None
    stem = m.group("snippet")[:-len(".reference.html")]
    return stem if stem.lower() != own_snippet_stem.lower() else None


def _ws(s):
    return re.sub(r"\s+", " ", s).strip()


def address_loaded(html, addr, kind, parts):
    """THE PAGE SIDE. -> (ok, how, hint). `parts` come from resolve_address. For a file
    address the two legal forms are L1's (`behaviour_loaded`). For an inline address the page
    must carry EVERY resolved script body BYTE-IDENTICAL as an inline executable <script> —
    sha256, no normalisation (s235-D1's posture). The hint names what IS there when it is not."""
    if kind == "file":
        ok, how = behaviour_loaded(html, addr)
        return ok, how, ("" if ok else " — the page neither inlines an AUTO-BEHAVIOUR block of "
                                      "that stem nor loads it with <script src>")
    page = inline_scripts(html, exclude_auto=False)
    page_hashes = {sha256_of(b): i for i, (b, _s) in enumerate(page)}
    missing, hows = [], []
    for label, body in parts:
        h = sha256_of(body)
        if h in page_hashes:
            hows.append("%s inlined verbatim as page script #%d, %d bytes"
                        % (label, page_hashes[h] + 1, len(body.encode("utf-8"))))
        else:
            missing.append((label, body))
    if not missing:
        return True, "; ".join(hows), ""
    label, body = missing[0]
    hint = " — the page carries %d inline executable script(s), none hashing to %s (%d bytes)" % (
        len(page), label, len(body.encode("utf-8")))
    for i, (pb, _s) in enumerate(page):
        if _ws(pb) == _ws(body):
            hint += ("; page script #%d matches it AFTER whitespace normalisation, so the bytes "
                     "moved — copy the snippet's <script> verbatim (s235-D1: the bytes are the key)" % (i + 1))
            break
        off = first_diff_offset(pb, body)
        if off is None:
            continue
        # how much of the two is SHARED (common prefix + common suffix, never overlapping):
        # a near-copy shares almost everything, an unrelated script almost nothing
        suf = 0
        while suf < min(len(pb), len(body)) - off and pb[-1 - suf] == body[-1 - suf]:
            suf += 1
        if len(body) and (off + suf) / float(len(body)) >= 0.8:
            ctx = _ws(pb[max(0, off - 24):off + 24])
            hint += ("; page script #%d diverges from it at byte %d of %d and shares %d%% of its bytes, "
                     "near …%s… — an edited copy, not the snippet's script"
                     % (i + 1, off, len(body), int(100 * (off + suf) / len(body)), ctx))
            break
    return False, None, hint


def behaviour_verdict(html, r):
    """Steps 4 + 4b for ONE markup region. -> (note_suffix, fail_lines, fails, meta_state).
    The meta is read FIRST; the receipt's own `script` is a copy that must agree with it."""
    rid = r.get("region")
    receipt_addr = r.get("script")
    mpath = meta_path_for(r.get("snippet") or "")
    meta = load_meta(mpath) if mpath else None
    state = behaviour_state(meta)
    typed = typed_behaviour(meta)
    rel = os.path.relpath(mpath, os.path.dirname(ROOT)) if mpath else None
    fails, lines = [], []
    if state == "PROSE":
        # s245-D3 (#245): a `behaviour` key that is still prose BLOCKS, named. Dave's word on the
        # L2 recommendation ("take the recommendations"): "block a meta whose `behaviour` key is
        # still prose on the day the 20 are written". NONE / NO-META keep the UNPROVEN posture.
        fails.append("BEHAVIOUR-PROSE")
        lines.append("FAIL:BEHAVIOUR-PROSE — `%s`: meta %s carries a `behaviour` key that is still "
                     "pre-s234-D5 prose (%s), not a typed address (s245-D3, #245); type it — "
                     "`script` / `partial` / `fallback`, prose kept under `$note` — and regenerate"
                     % (rid, rel, type((meta or {}).get("behaviour")).__name__))
        return "", lines, fails, state
    if typed is None:
        # L1's check, unchanged: the receipt's own address, if it declares one
        if receipt_addr:
            ok, how = behaviour_loaded(html, receipt_addr)
            if ok:
                suffix = " · behaviour %s LOADED (%s)" % (receipt_addr, how)
            else:
                fails.append("BEHAVIOUR-NOT-LOADED")
                lines.append("FAIL:BEHAVIOUR-NOT-LOADED — `%s` declares script `%s`, and the "
                             "page neither inlines an AUTO-BEHAVIOUR block of that name nor "
                             "loads it with <script src>" % (rid, receipt_addr))
                suffix = ""
        else:
            suffix = " · behaviour NO-BEHAVIOUR-DECLARED"
        return suffix + " · meta:%s" % state, lines, fails, state
    addr = typed.get("script")
    if receipt_addr and receipt_addr != addr:
        fails.append("BEHAVIOUR-ADDRESS-DISAGREES")
        lines.append("FAIL:BEHAVIOUR-ADDRESS-DISAGREES — `%s`: the receipt says script `%s` but the "
                     "meta %s says `%s`; the meta is the one home (s234-D5) and the receipt is a "
                     "copy that drifted — re-mint it" % (rid, receipt_addr, rel, addr))
        return "", lines, fails, state
    suffix = ""
    foreign = foreign_script_address(addr, r.get("snippet"))
    if addr is None:
        suffix = " · behaviour meta:NO-SCRIPT (%s declares the component carries no script)" % rel
    elif foreign:
        fails.append("BEHAVIOUR-ADDRESS-FOREIGN")
        lines.append("FAIL:BEHAVIOUR-ADDRESS-FOREIGN — `%s`: meta %s declares script `%s`, which is "
                     "ANOTHER component's snippet (%s); a #script address names the component's own "
                     "snippet — shared behaviour is a registered partial" % (rid, rel, addr, foreign))
    else:
        kind, parts, err = resolve_address(addr)
        if err:
            fails.append("BEHAVIOUR-ADDRESS-UNRESOLVABLE")
            lines.append("FAIL:BEHAVIOUR-ADDRESS-UNRESOLVABLE — `%s`: meta %s declares script `%s`, "
                         "which %s" % (rid, rel, addr, err))
        else:
            ok, how, hint = address_loaded(html, addr, kind, parts)
            if ok:
                suffix = " · behaviour %s LOADED (%s; meta %s)" % (addr, how, rel)
            else:
                fails.append("BEHAVIOUR-NOT-LOADED")
                lines.append("FAIL:BEHAVIOUR-NOT-LOADED — `%s`: meta %s declares script `%s`, and "
                             "the page does not load it%s" % (rid, rel, addr, hint))
    # s245-D2: `partial` is `string | string[] | null` — normalised to a list here, each name
    # judged on its own (an unregistered name and an unloaded one are BOTH named, no first-obstacle).
    for partial in partial_names(typed):
        reg = registered_partials()
        if partial not in reg:
            fails.append("BEHAVIOUR-PARTIAL-UNREGISTERED")
            lines.append("FAIL:BEHAVIOUR-PARTIAL-UNREGISTERED — `%s`: meta %s declares partial `%s`, "
                         "which component-types.json does not register under $behaviour (has: %s)"
                         % (rid, rel, partial, sorted(reg) or "none"))
        elif not any(m.group("name") == partial for m in AUTO_BEHAVIOUR_RE.finditer(html)):
            fails.append("BEHAVIOUR-NOT-LOADED")
            lines.append("FAIL:BEHAVIOUR-NOT-LOADED — `%s`: meta %s declares partial `%s` and the page "
                         "carries no AUTO-BEHAVIOUR %s block" % (rid, rel, partial, partial))
        else:
            suffix += " · partial %s LOADED (AUTO-BEHAVIOUR block)" % partial
    return suffix, lines, fails, state


def partial_names(typed):
    """s245-D2: the meta's `partial` as a list of names — `null` → [], `"a"` → ["a"], `["a","b"]`
    → itself. ONE place, imported by gen_component_partials.py too, so the generator and the gate
    cannot disagree about what a list means (the #150 two-code-paths defect)."""
    p = (typed or {}).get("partial")
    if p is None:
        return []
    if isinstance(p, str):
        return [p] if p else []
    return [x for x in p if isinstance(x, str) and x]


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
    unmeasured = {}                                   # meta state -> [region ids] (step 4b)
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
        if (r.get("kind") or "markup") == "markup":
            # only a MARKUP region can carry a behaviour; saying anything about the script of a
            # style or behaviour region is noise that trains the reader to skim the line.
            # Steps 4 + 4b (s234-D5): the META is read first, the receipt's `script` is a copy.
            suffix, blines, bfails, state = behaviour_verdict(html, r)
            unmeasured.setdefault(state, []).append(rid)
            if bfails:
                fails += bfails
                lines += blines
                continue
            note += suffix
        elif r.get("script"):
            # a non-markup region carrying a script claim: L1's check, unchanged
            ok, how = behaviour_loaded(html, r["script"])
            if not ok:
                fails.append("BEHAVIOUR-NOT-LOADED")
                lines.append("FAIL:BEHAVIOUR-NOT-LOADED — `%s` declares script `%s`, and the "
                             "page neither inlines an AUTO-BEHAVIOUR block of that name nor "
                             "loads it with <script src>" % (rid, r["script"]))
                continue
            note += " · behaviour %s LOADED (%s)" % (r["script"], how)
        lines.append("- " + note)

    # 4b, the honest gap: a region whose meta carries PROSE (or nothing) has had NOTHING about
    # its script measured. One line per page, naming the regions — never silence, never green.
    # (PROSE left this set at s245-D3 — it is a named FAIL above now, not an unmeasured gap.)
    gap = {k: v for k, v in unmeasured.items() if k in ("NONE", "NO-META") and v}
    if gap:
        parts = ["%d with meta:%s (%s)" % (len(v), k, ", ".join(v)) for k, v in sorted(gap.items())]
        unproven.append("UNPROVEN:behaviour-address — %s: no typed behaviour address (s234-D5), so "
                        "whether the page must load a script for these regions was NOT measured; "
                        "typing the meta's `behaviour` (the L2 migration proposal) would prove it"
                        % "; ".join(parts))

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
             retrieval=None, snippet="Demo"):
        rec = {"$schema": SCHEMA, "pack": pack, "retrievalSet": retrieval,
               "regions": [{"region": "Demo#1", "snippet": snippet, "kind": "markup",
                            "source": "knowledge/snippets/%s.reference.html" % snippet,
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

    # ---- 4b: THE META ADDRESS (s234-D5, #238 lane B). A temporary knowledge tree so each arm
    # drives resolve_address (meta side) and address_loaded (page side) on REAL files.
    global ROOT
    saved_root = ROOT
    ROOT = tempfile.mkdtemp()
    for d in ("snippets", "components", "canon"):
        os.makedirs(os.path.join(ROOT, d))
    demo_js = "(function(){ var n = 1; document.title = 'demo ' + n; })();"
    snippet_html = ('<!DOCTYPE html><html><head></head><body>%s\n'
                    '<script type="application/json" id="token-manifest">{"vars":{}}</script>\n'
                    '<script>\n%s\n</script>\n</body></html>' % (body, demo_js))
    open(os.path.join(ROOT, "snippets", "Demo.reference.html"), "w", encoding="utf-8").write(snippet_html)
    open(os.path.join(ROOT, "canon", "demo.js"), "w", encoding="utf-8").write(demo_js)
    json.dump({"component-type": {"g": {"$behaviour": {"demo-b": {"source": "canon/demo.js"}}}}},
              open(os.path.join(ROOT, "component-types.json"), "w"))
    inline_addr = "knowledge/snippets/Demo.reference.html#script"
    inline_body = inline_scripts(snippet_html)[0][0]            # the exact bytes #script denotes
    carried = "\n<script>%s</script>" % inline_body

    def meta(behaviour, slug="demo"):
        obj = {"name": slug, "category": "atom", "purpose": "selftest", "provenance": {}}
        if behaviour is not ...:
            obj["behaviour"] = behaviour
        json.dump(obj, open(os.path.join(ROOT, "components", slug + ".meta.json"), "w"))

    gh = good_hash
    meta({"script": None, "partial": None, "fallback": "identical — the component carries no script"})
    arm("J  meta TYPED, script null (passive) — a positive 'no script', never a fail",
        page(body, gh), "PASS")
    meta({"script": inline_addr, "partial": None, "fallback": None})
    arm("K  meta address PRESENT (#script) and the page carries the snippet's script VERBATIM",
        page(body, gh, extra_body=carried), "PASS")
    arm("L  meta address PRESENT and the page carries NO script",
        page(body, gh), "BEHAVIOUR-NOT-LOADED")
    arm("M  meta address PRESENT and the page carries a ONE-BYTE tampered copy",
        page(body, gh, extra_body=carried.replace("n = 1", "n = 2")), "BEHAVIOUR-NOT-LOADED")
    arm("N  meta address PRESENT and the page carries a whitespace-shifted copy (bytes are the key)",
        page(body, gh, extra_body="\n<script>" + inline_body.replace(" ", "  ") + "</script>"),
        "BEHAVIOUR-NOT-LOADED")
    arm("N2 …and the page carries the script as application/json (data, not executable)",
        page(body, gh, extra_body='\n<script type="application/json">%s</script>' % inline_body),
        "BEHAVIOUR-NOT-LOADED")
    meta({"script": "knowledge/canon/demo.js", "partial": None, "fallback": None})
    arm("O  meta address PRESENT (file form) and the page loads it with <script src>",
        page(body, gh, extra_head='<script src="../canon/demo.js"></script>'), "PASS")
    arm("O2 meta address PRESENT (file form) and the page inlines an AUTO-BEHAVIOUR demo block",
        page(body, gh, extra_body="\n<!-- ===== AUTO-BEHAVIOUR demo START (g) ===== -->\n"
                                  "<script>0</script>\n<!-- ===== AUTO-BEHAVIOUR demo END ===== -->"),
        "PASS")
    arm("O3 meta address PRESENT (file form) and the page loads nothing",
        page(body, gh), "BEHAVIOUR-NOT-LOADED")
    meta({"script": "knowledge/canon/nope.js", "partial": None, "fallback": None})
    arm("P  meta address WRONG — names a file that does not exist",
        page(body, gh, extra_head='<script src="../canon/nope.js"></script>'), "BEHAVIOUR-ADDRESS-UNRESOLVABLE")
    meta({"script": "snippet:Demo.reference.html#script", "partial": None, "fallback": None})
    arm("Q  meta address WRONG — outside the grammar (node-id form)",
        page(body, gh, extra_body=carried), "BEHAVIOUR-ADDRESS-UNRESOLVABLE")
    meta({"script": "knowledge/snippets/Ghost.reference.html#script", "partial": None, "fallback": None}, slug="ghost")
    arm("Q2 meta address WRONG — #script on the component's own snippet, which does not exist",
        page(body, gh, extra_body=carried, snippet="Ghost"), "BEHAVIOUR-ADDRESS-UNRESOLVABLE")
    open(os.path.join(ROOT, "snippets", "Mute.reference.html"), "w", encoding="utf-8").write(
        '<html><body><script type="application/json" id="token-manifest">{}</script></body></html>')
    meta({"script": "knowledge/snippets/Mute.reference.html#script", "partial": None, "fallback": None}, slug="mute")
    arm("Q3 meta address WRONG — #script on the component's own snippet, which has no inline executable script",
        page(body, gh, extra_body=carried, snippet="Mute"), "BEHAVIOUR-ADDRESS-UNRESOLVABLE")
    meta({"script": inline_addr, "partial": None, "fallback": None})
    arm("R  receipt `script` DISAGREES with the meta (the copy drifted from the home)",
        page(body, gh, script="knowledge/canon/demo.js", extra_body=carried), "BEHAVIOUR-ADDRESS-DISAGREES")
    arm("R2 receipt `script` AGREES with the meta — no double jeopardy",
        page(body, gh, script=inline_addr, extra_body=carried), "PASS")
    meta({"keyboard": "Arrows move the highlight", "open": "A shortcut opens it"})
    arm("S  meta PROSE (pre-s234-D5, an object without `script`) — BLOCKS, named (s245-D3)",
        page(body, gh), "BEHAVIOUR-PROSE")
    meta("Arrows move the highlight; a shortcut opens it")
    arm("S2 meta PROSE as a bare string — BLOCKS too (s245-D3)",
        page(body, gh), "BEHAVIOUR-PROSE")
    meta(["Arrows move the highlight", "a shortcut opens it"])
    arm("S3 meta PROSE as a list — BLOCKS too (s245-D3)",
        page(body, gh), "BEHAVIOUR-PROSE")
    meta(...)
    arm("T  meta with NO behaviour key — UNPROVEN too (meta:NONE)",
        page(body, gh), "PASS", expect_unproven="meta:NONE")
    meta({"script": inline_addr, "partial": "ghost-partial", "fallback": None})
    arm("U  meta partial UNREGISTERED in component-types.json",
        page(body, gh, extra_body=carried), "BEHAVIOUR-PARTIAL-UNREGISTERED")
    meta({"script": "knowledge/canon/demo.js", "partial": "demo-b", "fallback": None})
    arm("V  meta partial REGISTERED and the page carries no AUTO-BEHAVIOUR block of that name",
        page(body, gh, extra_head='<script src="../canon/demo.js"></script>'), "BEHAVIOUR-NOT-LOADED")
    arm("W  meta partial REGISTERED and the page carries the AUTO-BEHAVIOUR demo-b block",
        page(body, gh, extra_head='<script src="../canon/demo.js"></script>',
             extra_body="\n<!-- ===== AUTO-BEHAVIOUR demo-b START (g) ===== -->\n<script>0</script>\n"
                        "<!-- ===== AUTO-BEHAVIOUR demo-b END ===== -->"), "PASS")
    meta({"script": "knowledge/canon/demo.js", "partial": ["demo-b"], "fallback": None})
    arm("W2 meta partial as a LIST of one registered name, block carried (s245-D2)",
        page(body, gh, extra_head='<script src="../canon/demo.js"></script>',
             extra_body="\n<!-- ===== AUTO-BEHAVIOUR demo-b START (g) ===== -->\n<script>0</script>\n"
                        "<!-- ===== AUTO-BEHAVIOUR demo-b END ===== -->"), "PASS")
    meta({"script": "knowledge/canon/demo.js", "partial": ["demo-b", "ghost-partial"], "fallback": None})
    arm("U2 meta partial LIST with one unregistered name — the ghost is named, the real one still judged",
        page(body, gh, extra_head='<script src="../canon/demo.js"></script>',
             extra_body="\n<!-- ===== AUTO-BEHAVIOUR demo-b START (g) ===== -->\n<script>0</script>\n"
                        "<!-- ===== AUTO-BEHAVIOUR demo-b END ===== -->"), "BEHAVIOUR-PARTIAL-UNREGISTERED")
    # X: the #script address must ignore an AUTO-BEHAVIOUR payload in the SNIPPET (it has its own
    # registry address) — a snippet whose only script is an injected block resolves to nothing.
    open(os.path.join(ROOT, "snippets", "Injected.reference.html"), "w", encoding="utf-8").write(
        '<html><body><!-- ===== AUTO-BEHAVIOUR demo-b START (g) ===== -->\n<script>%s</script>\n'
        '<!-- ===== AUTO-BEHAVIOUR demo-b END ===== --></body></html>' % demo_js)
    meta({"script": "knowledge/snippets/Injected.reference.html#script", "partial": None, "fallback": None}, slug="injected")
    arm("X  #script on a snippet whose only script is an AUTO-BEHAVIOUR payload resolves to nothing",
        page(body, gh, extra_body=carried, snippet="Injected"), "BEHAVIOUR-ADDRESS-UNRESOLVABLE")
    meta({"script": "knowledge/snippets/Injected.reference.html#script", "partial": "demo-b", "fallback": None}, slug="injected")
    arm("X2 …and with an unloaded partial declared too, BOTH defects are named (no first-obstacle-only)",
        page(body, gh, extra_body=carried, snippet="Injected"), "BEHAVIOUR-ADDRESS-UNRESOLVABLE,BEHAVIOUR-NOT-LOADED")
    # Y: the WRONG-TARGET arm — the meta points at ANOTHER snippet's script and the page carries
    # this snippet's; loaded is decided on the bytes the address denotes, not on 'some script'.
    open(os.path.join(ROOT, "snippets", "Other.reference.html"), "w", encoding="utf-8").write(
        "<html><body><script>\nwindow.other = true;\n</script></body></html>")
    meta({"script": "knowledge/snippets/Other.reference.html#script", "partial": None, "fallback": None})
    arm("Y  meta address WRONG — a #script pointing at ANOTHER component's snippet is FOREIGN, "
        "even when the page carries that other script",
        page(body, gh, extra_body=carried + "\n<script>\nwindow.other = true;\n</script>"),
        "BEHAVIOUR-ADDRESS-FOREIGN")
    meta({"script": "knowledge/snippets/DEMO.reference.html#script", "partial": None, "fallback": None})
    arm("Y2 …but the OWN snippet named in another case is not foreign (case-insensitive stems)",
        page(body, gh, extra_body=carried), "PASS")
    # Z: the helpers themselves — a commented-out script element is NOT an inline script, and
    # the live one is handed back as ORIGINAL bytes at its original span (locate-live/slice-raw)
    zdoc = "<!-- <script>dead()</script> -->\n<script>live()</script>"
    zs = zdoc.index("live()")
    if inline_scripts(zdoc) != [("live()", (zs, zs + 6))]:
        ok = False
        print("  ❌ Z  inline_scripts read a <script> inside an HTML comment as live, or lost the live one: %r"
              % inline_scripts(zdoc))
    else:
        print("  ✅ Z  inline_scripts ignores a commented-out <script> and keeps the live one, raw bytes")
    # Z2: a snippet whose ONLY executable script is commented out resolves to nothing (meta side)
    open(os.path.join(ROOT, "snippets", "Dead.reference.html"), "w", encoding="utf-8").write(
        "<html><body><!-- <script>dead()</script> --></body></html>")
    meta({"script": "knowledge/snippets/Dead.reference.html#script", "partial": None, "fallback": None}, slug="dead")
    arm("Z2 #script on a snippet whose only <script> sits inside an HTML comment resolves to nothing",
        page(body, gh, extra_body="\n<script>dead()</script>", snippet="Dead"), "BEHAVIOUR-ADDRESS-UNRESOLVABLE")
    ROOT = saved_root
    print("SELFTEST: " + ("PASS ✅" if ok else "FAIL ❌"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main(sys.argv[1:]))
