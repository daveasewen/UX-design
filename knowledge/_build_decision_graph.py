#!/usr/bin/env python3
"""
Decision-graph generator + conflict gate (ADR-0012, proposed; extends ADR-0007 slice 1).

WHY: rulings cross-reference in prose, so reconciliation was manual archaeology (the icon-011
R-D6/R-D3 case, 2026-07-21). This walks TYPED edges and generates the views ADR-0007 designed:
a LIVE/AMENDED/DEAD/OPEN ledger, a reconciliation view (unresolved conflicts surface on their
own), and a per-node "what touches this" map.

SOURCES (in order):
  1. notes/_decision-graph-seed-2026-07-21.json  — the audited seed (judgment half, Fable session)
  2. (post-inscription) inline `Edges:` lines in ledgers + ADR headers + DV front-matter — the
     parser hook exists (`parse_inline_edges`) but inscription waits on ADR-0012 acceptance.

EDGE GRAMMAR (ADR-0012 §2/§3): type(target[, k=v…]) with types
  supersedes · refines · subsumes · bounds · conflicts-with · diverges-from · verified-by · relates
Aliases normalised here, never rewritten in source: Extends->refines, gated_by->verified-by,
governs->bounds, Relates->relates.

GATE SEMANTICS (ADR-0012 §6 — anti-laundering per ADR-0007 §5: consistency, never validity):
  --strict exits non-zero on: conflicts-with lacking `resolution` · resolution=open ·
  a structural-edge target that resolves to no known node/rule/anchor.
  `resolution=queued` NEVER fails the gate — queued conflicts are DAVE'S to rule (routing rule 2);
  they are surfaced loudly in the reconciliation view instead. diverges-from is intentional by
  definition and is listed, never flagged.

Writes knowledge/_DECISION-GRAPH.md + knowledge/_decision-graph.json.
Run:  python3 knowledge/_build_decision_graph.py [--strict] [--selftest]
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = os.path.join(ROOT, "notes", "_decision-graph-seed-2026-07-21.json")
OUT_MD = os.path.join(HERE, "_DECISION-GRAPH.md")
OUT_JSON = os.path.join(HERE, "_decision-graph.json")

STRUCTURAL = {"supersedes", "refines", "subsumes", "bounds", "conflicts-with", "diverges-from"}
# `enacted-by` PROMOTED #75 (Dave, 2026-08-01) into the EVIDENCE class — NOT structural.
# It backs a node; it never kills one. It is deliberately NOT folded into `verified-by`:
# ADR-0016's enactment register exists because "this was implemented" and "this was proven"
# must not be conflated (a CLAIMED enactment lies; an UNPROVEN one is honest). Collapsing
# the two would make that distinction unsayable in the graph. The other five unruled types
# found live at #75 (`amends`/`enables`/`sibling`/`carve-out`/`supersedes-mechanism`) were
# REWRITTEN into the ruled set with qualifiers, not promoted — ADR-0012 §2's own posture.
EVIDENCE = {"verified-by", "enacted-by"}
WEAK = {"relates"}
# The closed set. #75 (Dave): an edge type outside it is a LOUD NAMED FAILURE, never a
# silent store — see `check()` / code `unknown-edge-type`. Enumerating the offenders into
# STRUCTURAL was the rejected fix: it clears the six and lets the seventh walk in tomorrow,
# exactly as these six did (`scope-blindness-gate-vocabulary`: normalise once, fail loud on
# unknown, never enumerate).
RULED_TYPES = STRUCTURAL | EVIDENCE | WEAK
ALIASES = {"extends": "refines", "gated_by": "verified-by", "governs": "bounds"}
# targets that are legitimate endpoints without being seed nodes: guideline rules, files, methods
RULE_ID = re.compile(r"^[a-z]{2,6}\d{0,2}[a-z]?-\d{3}$")  # icon-011, col25-011, type26-013, dv-016, ctkb-015 …
FILEISH = re.compile(r"[/.]")


def load_seed():
    with open(SEED, encoding="utf-8") as f:
        seed = json.load(f)
    edges = []
    for e in seed.get("edges", []):
        e = dict(e)
        e["type"] = ALIASES.get(e["type"], e["type"])
        edges.append(e)
    return seed.get("nodes", {}), edges, seed.get("errata", [])


LEDGER_FILES = [
    os.path.join(ROOT, "knowledge", "_proforma", "_RAG-DECISIONS.md"),
    os.path.join(ROOT, "knowledge", "_proforma", "_TYPE-DECISIONS.md"),
    os.path.join(ROOT, "knowledge", "_proforma", "_BUTTON-DECISIONS.md"),
    os.path.join(ROOT, "knowledge", "_proforma", "_DATAVIZ-DECISIONS.md"),
]
# RULING 2 (2026-07-21 finishing pass): the 9 non-ledger edges are inscribed at
# SOURCE — in the file where that node actually lives — not in a ledger. Same
# `Edges:` grammar, same `_parse_ledger_file` walker (it's generic over headings
# + `{#id}` anchors), just pointed at these extra homes.
EXTRA_INLINE_FILES = [
    os.path.join(ROOT, "knowledge", "_FIXED-FLEX-CHARTER.md"),               # CHARTER.S9
    os.path.join(ROOT, "knowledge", "guidelines", "common-toolkit-buttons.md"),   # ctkb-015
    os.path.join(ROOT, "knowledge", "guidelines", "illustration-standards.md"),   # ill-007
    os.path.join(ROOT, "knowledge", "guidelines", "motion-standards.md"),         # mot-007
    os.path.join(ROOT, "knowledge", "guidelines", "typography-standards-2026.md"),# type26-015
    os.path.join(ROOT, "knowledge", "guidelines", "web-foundations.md"),          # webf-032
    # NOTE: DEF-006/DEF-005 and TYPE:2026-07-18:sat-ceiling already live in
    # _TYPE-DECISIONS.md, already in LEDGER_FILES above — no separate entry needed.
]
ADR_DIR = os.path.join(ROOT, "docs", "decisions")

QUAL_KEYS = ("scope", "claim", "resolution", "reason", "ref")
QUAL_KEY_RE = re.compile(r'(?:^|,\s*)(' + '|'.join(QUAL_KEYS) + r')=')
CALL_RE = re.compile(r'^([a-zA-Z][\w-]*)\((.*)\)$', re.DOTALL)
# Extended 2026-07-21 (finishing pass) to recognise the RULING-2 minted anchors
# (CHARTER.S9, DEF-006, TYPE:2026-07-18:sat-ceiling) alongside the original ledger IDs.
NODE_TOKEN = r'R-D\d+(?:\.\w+)?|T-D\d+|B-D\d+|DV-D\d+|CHARTER\.\w+|DEF-\d+|TYPE:[\w:.-]+'
BULLET_ID_RE = re.compile(r'^-\s+\*\*(DV-D\d+)\b')
PAREN_ID_RE = re.compile(r'\((' + NODE_TOKEN + r')\)')
ANY_ID_RE = re.compile(r'\b(' + NODE_TOKEN + r')\b')
# `{#ctkb-015}` style markdown attribute anchors — how guideline-rule REVIEW
# items carry their own id (ADR-0012 §1: "guideline rules `{#id}`"). Works on
# any line (heading or plain bullet), unlike the heading-only Paren/Any checks.
# Anchored at END OF LINE ONLY: the ledgers cite OTHER rules mid-prose in the
# same `{#id}` shape, backtick-wrapped (`` `{#dv-017}` ``, never the line's last
# token) — e.g. R-D3 says "`{#dv-017}`(a) permits...". Requiring end-of-line
# is what tells "this bullet's own anchor" apart from "a citation of some other
# rule in passing" (found live in `_RAG-DECISIONS.md`/`_TYPE-DECISIONS.md` while
# wiring this in — same class of trap as the ADR Status-prose one).
ANCHOR_HASH_RE = re.compile(r'\{#([a-zA-Z][\w.:-]*)\}\s*$')
EDGES_LINE_RE = re.compile(r'^\s*Edges:\s*(.+)$')
# `Node: ADR-0015-A1` — an EXPLICIT own-id declaration immediately above an `Edges:` line.
# The convention was already live in ADR-0015 (lines 97/154, authored #27) and the parser
# never learned it, so both sub-rulings' edges were attributed to the last `# ADR-NNNN`
# title in the file — which is how `amends(ADR-0015) → ADR-0015` became TWO SELF-LOOPS
# (F4 in the #71 receipt). Honoured for both attribution and registration as of #75.
NODE_LINE_RE = re.compile(r'^\s*Node:\s*(\S+)\s*$')
# ⚠ SCOPE OF REGISTRATION — narrower than "every id the scan can see", deliberately.
# ADR-0012 §1 calls guideline rules `{#id}` nodes, but §3 rules that they are NOT
# re-authored into the decision corpus: they stay in their guideline files and
# `_RECONCILIATION.md` is their generated register. `RULE_ID` below exists precisely
# to make them legitimate endpoints WITHOUT being seed nodes. Registering them here
# would have taken the rollup 83 → 196 (100 of the 113 new nodes were guideline rules)
# and quietly redefined what LIVE/DEAD/AMENDED counts — a scope change dressed as a
# bug fix. The defect Dave ruled on is RULINGS with no node, so registration is bound
# to the decision-ID vocabulary only. Guideline rules remain `RULE_ID` endpoints.
REGISTRABLE_ID_RE = re.compile(
    r'^(?:R-D\d+(?:\.\w+)?|T-D\d+|B-D\d+|DV-D\d+|ADR-\d{4}(?:-\w+)?|CHARTER\.\w+|DEF-\d+|TYPE:[\w:.-]+)$')
# A target that still carries a `,` or `)` after qualifier-stripping is MALFORMED — either a
# multi-target edge the grammar cannot express (F3: `sibling(button-sheet-v7, ADR-0009)`) or a
# whole comma-separated edge RUN swallowed into one target because the author used `, ` where
# the grammar wants ` · ` (F5, found #75 at `_TYPE-DECISIONS.md:1059` — T-D15 lost two
# `relates()` edges silently). Both were stored and counted as if fine.
MALFORMED_TARGET_RE = re.compile(r'[,)]')
ADR_TITLE_RE = re.compile(r'^#\s*(ADR-\d+)\b')
# ADR header native-syntax fields (RULING 1, 2026-07-21 finishing pass). Captures
# ONLY the text between the field's own bold label and the next bold label (or
# end of the header paragraph) — never the whole header block — so a `**Status:**`
# parenthetical that name-drops rule IDs in prose (ADR-0012's own header does this
# with R-D2/R-D7/R-D21) is never misread as an edge.
ADR_TOKEN = r'ADR-\d{4}'
HEADER_ID_RE = re.compile(r'\b(' + ADR_TOKEN + '|' + NODE_TOKEN + r')\b')
EXTENDS_FIELD_RE = re.compile(
    r'\*\*Extends:\*\*\s*(.*?)(?=\*\*Relates:\*\*|\*\*Method:\*\*|\*\*Status:\*\*|$)', re.DOTALL)
RELATES_FIELD_RE = re.compile(
    r'\*\*Relates:\*\*\s*(.*?)(?=\*\*Method:\*\*|\*\*Extends:\*\*|\*\*Status:\*\*|$)', re.DOTALL)


def _parse_call(tok):
    """Parse one `type(to[, k=v]*)` call. Handles nested parens in values (T-D8's
    claim carries them) and commas embedded in a qualifier's own text (R-D20's
    claim text contains a comma) by locating qualifier boundaries via the known
    key set rather than splitting blindly on ','."""
    m = CALL_RE.match(tok.strip())
    if not m:
        return None
    etype, inner = m.group(1), m.group(2)
    etype = ALIASES.get(etype, etype)
    key_matches = list(QUAL_KEY_RE.finditer(inner))
    if key_matches:
        to = inner[:key_matches[0].start()].strip().rstrip(",").strip()
    else:
        to = inner.strip()
    e = {"type": etype, "to": to}
    for i, km in enumerate(key_matches):
        start = km.end()
        end = key_matches[i + 1].start() if i + 1 < len(key_matches) else len(inner)
        e[km.group(1)] = inner[start:end].strip()
    return e


def parse_edges_line(text, from_node):
    """`text` is everything after 'Edges:' on one line — one or more
    ` · `-separated `type(target, k=v)` calls, all attributed to `from_node`."""
    edges = []
    for tok in re.split(r'\s*·\s*', text.strip()):
        if not tok:
            continue
        e = _parse_call(tok)
        if e is None:
            continue
        e["from"] = from_node
        edges.append(e)
    return edges


def _scan_current_node(line, current):
    """Track which node an upcoming `Edges:` line belongs to, walking a ledger
    top-down. Ledger sections are `## R-D21 — …` / `### Ruling A — … (R-D6.A)`
    style headings; DataViz's standing-decisions block is a flat bullet list
    (`- **DV-D01 · …**`). A heading that only *mentions* another node in passing
    (e.g. `## OPEN — carried out of R-D1`) can reassign `current` here, but that
    is harmless in practice: no `Edges:` line is ever inscribed inside such a
    section, only directly under the node's own heading/bullet.

    Extended 2026-07-21 (finishing pass, RULING 2) for the non-ledger homes:
    guideline REVIEW rules carry their id as a `{#ctkb-015}` markdown attribute
    anchor at the end of an ordinary bullet (not a heading), and the charter /
    pre-T-D type-ledger sections get a minted `(CHARTER.S9)` / `(TYPE:…)` tag
    appended to their own heading, same convention as `(R-D6.A)`. The anchor
    check runs on every line (heading or not) so it catches both shapes."""
    b = BULLET_ID_RE.match(line)
    if b:
        return b.group(1)
    h = ANCHOR_HASH_RE.search(line)
    if h:
        return h.group(1)
    if not line.startswith("#"):
        return current
    p = PAREN_ID_RE.search(line)
    if p:
        return p.group(1)
    a = ANY_ID_RE.search(line)
    if a:
        return a.group(1)
    return current


def _register(reg, nid, path, line_no, title=""):
    """Record an OWN-ID node declaration. ⚠ Deliberately NOT driven by
    `_scan_current_node`: that scan is built for ATTRIBUTION and its own docstring
    says a heading which merely *mentions* another node can reassign `current`,
    calling that "harmless in practice" because no `Edges:` line is ever inscribed
    in such a section. That premise licenses attribution and does NOT license
    registration — the same scan under a second purpose would mint junk nodes out
    of passing mentions. Registration therefore takes only unambiguous own-id
    shapes: a `Node:` line, a `- **DV-D01 …**` bullet, an end-of-line `{#id}`
    anchor, a `(R-D6.A)` paren tag, or an `# ADR-NNNN` title."""
    if not nid or nid in reg or not REGISTRABLE_ID_RE.match(nid):
        return
    reg[nid] = {"title": title.strip()[:120], "status": "accepted",
                "home": f"{os.path.relpath(path, ROOT)}:{line_no}"}


def _parse_ledger_file(path, reg=None):
    edges = []
    if not os.path.isfile(path):
        return edges
    current = None
    with open(path, encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.rstrip("\n")
            nl = NODE_LINE_RE.match(line)
            if nl:
                # An explicit `Node:` declaration wins over the heading walk and holds
                # until the next heading/declaration — this is what stops a sub-ruling's
                # edges being attributed to its parent (the F4 self-loop mechanism).
                current = nl.group(1)
                if reg is not None:
                    _register(reg, current, path, line_no)
            else:
                prev = current
                current = _scan_current_node(line, current)
                if reg is not None and current and current != prev:
                    if BULLET_ID_RE.match(line) or ANCHOR_HASH_RE.search(line) \
                            or (line.startswith("#") and PAREN_ID_RE.search(line)):
                        _register(reg, current, path, line_no, line.lstrip("#-* "))
                    elif line.startswith("#"):
                        # Heading-with-an-ID: own-id ONLY when the id opens the heading
                        # text ("## R-D23 — Tabs…"). An id appearing later in the line is
                        # a passing mention ("## OPEN — carried out of R-D1") and must not
                        # mint a node, per this function's docstring.
                        txt = line.lstrip("#").strip().lstrip("⭐★☆ ").strip()
                        a = ANY_ID_RE.match(txt)
                        if a and a.group(1) == current:
                            _register(reg, current, path, line_no, txt)
            m = EDGES_LINE_RE.match(line)
            if m and current:
                edges.extend(parse_edges_line(m.group(1), current))
    return edges


def _adr_header_text(lines, adr_title_idx):
    """The ADR header is the markdown paragraph right after the `# ADR-00NN`
    title: one or more soft-wrapped lines (no blank line between them) ending at
    the first blank line or EOF. Joining them with spaces gives one string to
    regex the `**Extends:**`/`**Relates:**` fields out of — this is what keeps a
    multi-line header (ADR-0012's own, 7 lines) working the same as a one-liner."""
    i = adr_title_idx + 1
    n = len(lines)
    while i < n and lines[i].strip() == "":
        i += 1
    header_lines = []
    while i < n and lines[i].strip() != "":
        header_lines.append(lines[i])
        i += 1
    return " ".join(header_lines)


def _parse_adr_header_fields(adr_id, header_text):
    """RULING 1 (2026-07-21 finishing pass): the 18 ADR→ADR/R-D edges are
    inscribed as native `**Extends:**` (→ refines) / `**Relates:**` (→ relates)
    header fields, not inline `Edges:` lines — matching how ADR-0012's own
    header already does it. Extracts ONLY the text between each field's own
    label and the next bold label (or end of the header paragraph), so prose
    elsewhere in the header (e.g. a `**Status:**` parenthetical that name-drops
    R-D2/R-D7/R-D21) is never in scope — the field boundary IS the guard, not a
    keyword blocklist."""
    edges = []
    em = EXTENDS_FIELD_RE.search(header_text)
    if em:
        for tok in HEADER_ID_RE.findall(em.group(1)):
            edges.append({"from": adr_id, "type": "refines", "to": tok})
    rm = RELATES_FIELD_RE.search(header_text)
    if rm:
        for tok in HEADER_ID_RE.findall(rm.group(1)):
            edges.append({"from": adr_id, "type": "relates", "to": tok})
    return edges


def _parse_adr_file(path, reg=None):
    """ADR headers carry native `Extends:`/`Relates:` relations — parsed
    per-field by `_parse_adr_header_fields` (RULING 1). Also still picks up any
    explicit inline `Edges:` line in the body (same grammar as the ledgers),
    for the rare case an ADR needs an edge type the header grammar can't say
    (e.g. `verified-by`, `diverges-from`) — none do yet, kept for symmetry."""
    edges = []
    if not os.path.isfile(path):
        return edges
    with open(path, encoding="utf-8") as f:
        lines = [l.rstrip("\n") for l in f]
    adr_id = None      # the file's ADR, for header-field edges
    current = None     # who an `Edges:` line belongs to — may be a sub-ruling
    # ⚠ ONE pass, not two. The previous two-pass shape ran the title loop to completion
    # first, so EVERY inline `Edges:` line in the file was attributed to the LAST title
    # seen — which is why ADR-0015's two sub-rulings amended their own parent (F4).
    for idx, line in enumerate(lines):
        t = ADR_TITLE_RE.match(line)
        if t:
            adr_id = current = t.group(1)
            if reg is not None:
                _register(reg, adr_id, path, idx + 1, line.lstrip("# ").strip())
            edges.extend(_parse_adr_header_fields(adr_id, _adr_header_text(lines, idx)))
            continue
        nl = NODE_LINE_RE.match(line)
        if nl:
            current = nl.group(1)
            if reg is not None:
                _register(reg, current, path, idx + 1)
            continue
        m = EDGES_LINE_RE.match(line)
        if m and current:
            edges.extend(parse_edges_line(m.group(1), current))
    return edges


def parse_inline_edges():
    """Post-inscription hook: parse `Edges: type(target, k=v) · …` lines from the
    4 decision ledgers + the RULING-2 non-ledger homes (charter, guideline files),
    plus every ADR's native `Extends:`/`Relates:` header fields (RULING 1) and any
    inline `Edges:` line it carries. This is the mechanical half of ADR-0012 §7 —
    reads what Sonnet's inscription pass wrote, in the SAME edge shape
    `load_seed()` produces, so `--verify` can diff the two sets directly."""
    edges = []
    reg = {}
    for path in LEDGER_FILES + EXTRA_INLINE_FILES:
        edges.extend(_parse_ledger_file(path, reg))
    if os.path.isdir(ADR_DIR):
        for fn in sorted(os.listdir(ADR_DIR)):
            if fn.startswith("ADR-") and fn.endswith(".md"):
                edges.extend(_parse_adr_file(os.path.join(ADR_DIR, fn), reg))
    return edges, reg


def classify(nodes, edges):
    """Lifecycle rollup: DEAD = whole-node supersedes inbound; AMENDED = claim-scoped supersedes
    inbound (invalidated-not-deleted); explicit node status wins where it says superseded."""
    inbound = {}
    for e in edges:
        inbound.setdefault(e.get("to"), []).append(e)
    state = {}
    for nid, meta in nodes.items():
        st = meta.get("status", "accepted")
        dead_hit = [e for e in inbound.get(nid, []) if e["type"] == "supersedes" and not e.get("claim")]
        claim_hits = [e for e in inbound.get(nid, []) if e["type"] == "supersedes" and e.get("claim")]
        if st == "superseded" or dead_hit:
            state[nid] = "DEAD"
        elif claim_hits or st == "amended":
            state[nid] = "AMENDED"
        elif st == "proposed":
            state[nid] = "OPEN"
        else:
            state[nid] = "LIVE"
    return state, inbound


def check(nodes, edges):
    """Gate findings: (severity, code, msg). severity ⚠ fails --strict; i is report-only."""
    findings = []
    known = set(nodes)
    for e in edges:
        t, to = e["type"], e.get("to", "")
        # ── #75, Dave: the CLASS fix. Edge `type` was an open string while every
        # protective mechanism below keys on closed-set membership, so an unknown type
        # fell outside all of them and was stored, counted and displayed as if fine.
        # Six such types (10 edges) accumulated unnoticed. Loud and NAMED, both ways.
        if t not in RULED_TYPES:
            findings.append(("⚠", "unknown-edge-type",
                             f"{e['from']} —{t}→ `{to}`: `{t}` is not in ADR-0012 §2's ruled set "
                             f"({', '.join(sorted(RULED_TYPES))}). Rewrite it with a ruled type + "
                             f"qualifiers, or amend ADR-0012 — do not add it to STRUCTURAL."))
        # A target still carrying `,` or `)` never parsed cleanly: a multi-target edge the
        # grammar cannot express, or a `, `-separated edge run swallowed whole. Silent
        # before #75 — the malformed target simply matched no node, and the type check
        # below let it through because these edges were unruled types too.
        if MALFORMED_TARGET_RE.search(to):
            findings.append(("⚠", "malformed-target",
                             f"{e['from']} —{t}→ `{to}`: target contains `,` or `)`. The grammar is "
                             f"ONE target per call, calls separated by ` · ` — split it. "
                             f"(A `, `-separated run silently collapses into a single target and "
                             f"DROPS every edge after the first.)"))
        # F4: `if src and tgt and src != tgt` is what the reference cookbook guards at
        # assembly and we did not. Loud rather than silently dropped — a self-loop means an
        # attribution bug upstream, and swallowing it hides the bug.
        if e["from"] == to:
            findings.append(("⚠", "self-loop",
                             f"{e['from']} —{t}→ itself. Usually mis-attribution: an `Edges:` line "
                             f"under a sub-ruling with no `Node:` declaration binds to its parent."))
        if t in STRUCTURAL and to not in known and not RULE_ID.match(to) and not FILEISH.search(to):
            # unresolvable structural target — allow named anchors ("X:Y" / "CHARTER.*") and
            # descriptive endpoints only for conflicts-with (the tension may be with a practice)
            if ":" not in to and "." not in to and t != "conflicts-with":
                findings.append(("⚠", "orphan-target",
                                 f"{e['from']} —{t}→ `{to}`: target resolves to no known node/rule/anchor."))
        if t == "conflicts-with":
            res = e.get("resolution")
            if not res:
                findings.append(("⚠", "conflict-unresolved",
                                 f"{e['from']} conflicts-with {to}: NO resolution recorded."))
            elif res == "open":
                findings.append(("⚠", "conflict-open",
                                 f"{e['from']} conflicts-with {to}: resolution=open."))
            elif res == "queued":
                findings.append(("i", "conflict-queued",
                                 f"{e['from']} conflicts-with {to} — QUEUED FOR DAVE: {e.get('claim', e.get('note', ''))[:100]}"))
    return findings


def what_touches(nodes, edges):
    adj = {}
    for e in edges:
        adj.setdefault(e["from"], {"out": [], "in": []})["out"].append(e)
        if e.get("to") in nodes:
            adj.setdefault(e["to"], {"out": [], "in": []})["in"].append(e)
    return adj


def fmt_edge(e, direction="out"):
    q = []
    for k in ("scope", "claim", "resolution", "reason", "ref"):
        if e.get(k):
            q.append(f"{k}={e[k]}")
    qs = f" ({'; '.join(q)})" if q else ""
    if direction == "out":
        return f"—{e['type']}→ {e.get('to')}{qs}"
    return f"{e['from']} —{e['type']}→{qs}"


def main():
    nodes, seed_edges, errata = load_seed()
    inline_edges, inline_nodes = parse_inline_edges()
    # ⚠ NODE REGISTRY — fixed #75 (Dave: "fix it in this session"). Until now `nodes` came
    # ONLY from the 2026-07-21 seed, while `edges` were parsed live from the ledgers. The
    # seed's edge list was maintained; its node list was not. Result: every ruling authored
    # after that audit had edges in the graph and NO NODE to hang them on — 14 edge sources
    # resolved to nothing, 9 of them real rulings (R-D22…R-D25, DV-D14, DV-D15, T-D15,
    # ADR-0013, ADR-0016). They could never appear in the LIVE/AMENDED/DEAD/OPEN rollup and
    # could never be marked dead or amended. ★ This is why a type-only fix banked nothing:
    # retyping `supersedes-mechanism` to `supersedes(dv-004, claim=…)` marks a node that
    # does not exist. Seed metadata WINS on collision — it is the curated half (titles,
    # explicit `status: proposed|superseded`); the scan only ADDS what the seed never knew.
    for nid, meta in inline_nodes.items():
        if nid not in nodes:
            nodes[nid] = meta
    # Merge, not concatenate: once an edge is inscribed inline it is the SAME edge as its
    # seed entry (that is what --verify checks), not a second one. Key on (from,type,to)+
    # qualifiers so a fully-inscribed corpus doesn't silently double every edge count.
    merged = {_edge_key(e): e for e in seed_edges}
    merged.update({_edge_key(e): e for e in inline_edges})
    edges = list(merged.values())
    state, inbound = classify(nodes, edges)
    findings = check(nodes, edges)
    adj = what_touches(nodes, edges)
    warns = [f for f in findings if f[0] == "⚠"]
    queued = [f for f in findings if f[1] == "conflict-queued"]
    diverges = [e for e in edges if e["type"] == "diverges-from"]

    by_state = {}
    for nid, st in state.items():
        by_state.setdefault(st, []).append(nid)

    L = ["# Decision graph — generated views (ADR-0012)", "",
         "*GENERATED by `_build_decision_graph.py` from the audited seed "
         "(`notes/_decision-graph-seed-2026-07-21.json`) — do not hand-edit. Consistency only, "
         "never validity (ADR-0007 §5): a clean graph is not a vouched one.*", "",
         f"**{len(nodes)} nodes · {len(edges)} edges · {len(warns)} gate warning(s) · "
         f"{len(queued)} conflict(s) queued for Dave · {len(diverges)} recorded deliberate divergence(s).**", ""]

    L.append("## ① Reconciliation view — conflicts + divergences")
    L.append("")
    if queued:
        L.append("### ★ QUEUED FOR DAVE (never auto-resolved)")
        for _, _, msg in queued:
            L.append(f"- 🟡 {msg}")
        L.append("")
    open_c = [f for f in findings if f[1] in ("conflict-unresolved", "conflict-open")]
    if open_c:
        L.append("### ⚠ UNRESOLVED (gate fails on these in --strict)")
        for _, _, msg in open_c:
            L.append(f"- ⚠ {msg}")
        L.append("")
    resolved = [e for e in edges if e["type"] == "conflicts-with" and e.get("resolution") in ("ruled", "interim", "deferred", "parked")]
    L.append(f"### Registered tensions with a recorded resolution ({len(resolved)})")
    for e in resolved:
        L.append(f"- {e['from']} ↔ {e['to']} — **{e['resolution']}**"
                 + (f" (ref: {e['ref']})" if e.get("ref") else "")
                 + (f" — {e.get('note','')[:90]}" if e.get("note") else ""))
    L.append("")
    L.append(f"### Deliberate divergences (intentional — the gate never flags these)")
    for e in diverges:
        L.append(f"- {e['from']} ⇹ {e['to']} — {e.get('reason','')[:140]}")
    L.append("")

    L.append("## ② Lifecycle ledger")
    L.append("")
    for st, label in (("LIVE", "LIVE"), ("AMENDED", "AMENDED — live with a dead claim (invalidated, not deleted)"),
                      ("DEAD", "DEAD — do not build on"), ("OPEN", "OPEN / proposed")):
        ids = sorted(by_state.get(st, []))
        if not ids:
            continue
        L.append(f"### {label} ({len(ids)})")
        for nid in ids:
            n = nodes[nid]
            extra = ""
            if st == "AMENDED":
                claims = [e.get("claim") for e in inbound.get(nid, []) if e["type"] == "supersedes" and e.get("claim")]
                if claims:
                    extra = f" — dead claim(s): {'; '.join(c for c in claims if c)}"
            if st == "DEAD":
                sups = [e["from"] for e in inbound.get(nid, []) if e["type"] == "supersedes"]
                if sups:
                    extra = f" — superseded by {', '.join(sups)}"
            L.append(f"- **{nid}** · {n.get('title','')}{extra}")
        L.append("")

    L.append("## ③ What-touches-this map (per node, inbound + outbound)")
    L.append("")
    for nid in sorted(adj, key=lambda x: (x.split("-")[0], x)):
        a = adj[nid]
        if not a["in"] and not a["out"]:
            continue
        L.append(f"**{nid}**")
        for e in a["out"]:
            L.append(f"  - {fmt_edge(e,'out')}")
        for e in a["in"]:
            L.append(f"  - ← {fmt_edge(e,'in')}")
        L.append("")

    L.append("## ④ Validation rollup (human-only; never derived)")
    vc = {}
    for nid, n in nodes.items():
        vc[n.get("validation", "unaudited")] = vc.get(n.get("validation", "unaudited"), 0) + 1
    L.append("")
    L.append(" · ".join(f"**{k}**: {v}" for k, v in sorted(vc.items())))
    if errata:
        L.append("")
        L.append("## ⑤ Errata (fix at next capture)")
        for e in errata:
            L.append(f"- **{e['id']}** — {e['what']}")
    L.append("")

    open(OUT_MD, "w", encoding="utf-8").write("\n".join(L))
    json.dump({"nodes": nodes, "edges": edges, "state": state,
               "findings": [{"sev": s, "code": c, "msg": m} for s, c, m in findings]},
              open(OUT_JSON, "w", encoding="utf-8"), indent=1)

    print(f"decision graph: {len(nodes)} nodes, {len(edges)} edges -> {os.path.relpath(OUT_MD, ROOT)}")
    print(f"  states: " + " · ".join(f"{k} {len(v)}" for k, v in sorted(by_state.items())))
    for sev, code, msg in findings:
        print(f"  {sev} [{code}] {msg[:110]}")
    return len(warns)


def _edge_key(e):
    return (e.get("from"), e.get("type"), e.get("to")) + tuple(e.get(k) for k in QUAL_KEYS)


def verify():
    """--verify / --diff: diff inline-parsed edges (what's actually inscribed)
    against the seed (the audited judgment) by (from, type, to) + qualifiers.
    Acceptance test per ADR-0012 §7: inscription is done when this is empty.
    Any remainder is either a real gap or a deliberate hold documented in the
    worker receipt (e.g. edges whose `from` has no ruled ledger-file home, or
    ADR edges left in native Extends:/Relates: syntax, not double-inscribed)."""
    seed_nodes, seed_edges, _ = load_seed()
    inline_edges, _reg = parse_inline_edges()
    seed_by_key = {_edge_key(e): e for e in seed_edges}
    inline_by_key = {_edge_key(e): e for e in inline_edges}
    seed_only = sorted(set(seed_by_key) - set(inline_by_key))
    inline_only = sorted(set(inline_by_key) - set(seed_by_key))
    matched = set(seed_by_key) & set(inline_by_key)

    print(f"decision graph --verify: seed {len(seed_edges)} edges · inscribed {len(inline_edges)} "
          f"edges parsed · {len(matched)} matched")
    if seed_only:
        print(f"  {len(seed_only)} edge(s) in SEED but NOT inscribed:")
        for k in seed_only:
            e = seed_by_key[k]
            print(f"    - {fmt_edge(e, 'in')} (from {e['from']})" if False else
                  f"    - {e['from']} —{e['type']}→ {e.get('to')} "
                  + "".join(f"{k}={e[k]} " for k in QUAL_KEYS if e.get(k)))
    if inline_only:
        print(f"  {len(inline_only)} edge(s) INSCRIBED but NOT in seed (unexpected — check for a typo "
              f"or an invented edge):")
        for k in inline_only:
            e = inline_by_key[k]
            print(f"    - {e['from']} —{e['type']}→ {e.get('to')} "
                  + "".join(f"{k}={e[k]} " for k in QUAL_KEYS if e.get(k)))
    if not seed_only and not inline_only:
        print("  ZERO mismatch — inscribed corpus == seed.")
    return len(seed_only) + len(inline_only)


def selftest():
    """Bite-test: an open conflict and an orphan structural target must each fail strict.
    #79 P6: extended with three finding codes `check()` has carried since #75/F4/F5 but
    that had ZERO selftest coverage before this -- unknown-edge-type (#75's own class
    fix), malformed-target (F5, a comma-run silently swallowing edges), self-loop (F4, a
    mis-attribution bug). Each new case pins the SPECIFIC finding code, not just "some
    warning fired", so a regression that silently disables ONE check cannot hide behind a
    DIFFERENT one firing on the same fixture."""
    nodes = {"A": {"title": "a"}, "B": {"title": "b"}}
    bad1 = [{"from": "A", "type": "conflicts-with", "to": "B"}]                    # no resolution
    bad2 = [{"from": "A", "type": "conflicts-with", "to": "B", "resolution": "open"}]
    bad3 = [{"from": "A", "type": "supersedes", "to": "GHOST"}]                    # orphan target
    ok = [{"from": "A", "type": "conflicts-with", "to": "B", "resolution": "queued"},
          {"from": "A", "type": "diverges-from", "to": "B", "reason": "intentional"}]
    for name, es, want in (("unresolved", bad1, True), ("open", bad2, True),
                           ("orphan", bad3, True), ("queued+diverge", ok, False)):
        warns = [f for f in check(nodes, es) if f[0] == "⚠"]
        fired = bool(warns)
        assert fired == want, f"selftest {name}: expected fire={want}, got {fired}"
        print(f"  selftest {name}: {'fires' if fired else 'green'} ✓")
    # #79 P6 -- three codes `check()` implements with no prior selftest coverage.
    bad_unknown = [{"from": "A", "type": "amends", "to": "B"}]           # #75: outside RULED_TYPES
    bad_malformed = [{"from": "A", "type": "relates", "to": "B, C"}]     # F5: comma-run silently swallowed
    bad_selfloop = [{"from": "A", "type": "refines", "to": "A"}]        # F4: mis-attribution self-loop
    for name, es, want_code in (
        ("unknown-edge-type", bad_unknown, "unknown-edge-type"),
        ("malformed-target", bad_malformed, "malformed-target"),
        ("self-loop", bad_selfloop, "self-loop"),
    ):
        codes = {f[1] for f in check(nodes, es) if f[0] == "⚠"}
        assert want_code in codes, f"selftest {name}: expected code {want_code!r} to fire, got {codes!r}"
        assert len(codes) == 1, f"selftest {name}: expected ONLY {want_code!r} to fire, got {codes!r}"
        print(f"  selftest {name}: fires `{want_code}` (only) ✓")

    print("selftest PASS — gate bites on unresolved/open/orphan/unknown-edge-type/"
          "malformed-target/self-loop; queued + diverges-from stay green")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--verify" in sys.argv or "--diff" in sys.argv:
        sys.exit(verify())
    warns = main()
    sys.exit(warns if "--strict" in sys.argv else 0)
