#!/usr/bin/env python3
"""Type-binding BLAST-RADIUS gate — guards knowledge/canon/type.css.

THE PROBLEM (raised 2026-07-18, T-D12 §5 / _LIVE-STATE open-001). The type-binding
mechanism (Dave ruling T-D9) binds a component to a composite by APPENDING its selector
to the composite's selector list. type.css is linked GLOBALLY, so every appended selector
becomes a global rule: `h2`, `.label`, `.status`, `.chip` now apply to EVERY snippet that
links the file. It holds today only because component CSS loads second — load order doing
safety-critical work across ~460 selectors, with no gate. `.tag` (14px vs 12px) is the
first collision; it will not be the last. Wanted BEFORE the remaining ~690 TYPE-002 bind.

This does NOT reopen T-D9. The mechanism is ruled; this is its missing guard-rail.

WHAT IT CHECKS. Every selector appended to a composite list must be REGISTERED in
knowledge/canon/_type-bindings.json with its acknowledged blast radius (the exact gated
files it matches). The gate recomputes the real radius and FAILS on:
  1. UNREGISTERED  — a selector appended to a composite but absent from the registry
                     (a new global binding must be a conscious, recorded act).
  2. ESCAPED       — a registered selector now matches a file NOT in its acknowledged set
                     (its blast radius grew — namespace it, or --update and review the diff).
  3. UNWAIVED-BARE — a NEW pure-bare-element (e.g. h2) or scoped-element (e.g. `.seg button`)
                     selector without waived:true (structural risk; must be acknowledged).
A SHRINKING radius never fails (fewer files is safe); the report notes it so the registry
can be tidied. Corpus = snippets/*.html + _proforma/*.html (same as the sibling gates).

Registered waived-debt entries are DEBT to burn down (namespace them), not a licence to add
more. Priority burndown: h2 (25 files) in the non-/1 reviewed batch, where pixels move.

Usage:  python3 knowledge/_validate_type_blast_radius.py            # validate (the gate)
        python3 knowledge/_validate_type_blast_radius.py --update   # re-seed registry from
                                                                     # current state, then REVIEW the diff
Writes _TYPE-BLAST-GATE.md; exits non-zero on any fail."""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import re, glob, os, sys, json, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
TYPECSS = os.path.join(HERE, "canon", "type.css")
REGPATH = os.path.join(HERE, "canon", "_type-bindings.json")
REPORT  = os.path.join(HERE, "_TYPE-BLAST-GATE.md")

COMPOSITE = re.compile(r'^\.t-(cm|ed)-')          # the composites themselves — not bindings
STRUCT    = re.compile(r'^(:root|\[data-theme|@supports|\*)')

def appended_selectors():
    """Every selector appended to a composite list in type.css (comments stripped)."""
    css = re.sub(r'/\*.*?\*/', '', open(TYPECSS).read(), flags=re.S)
    out, seen = [], set()
    for selraw, _ in re.findall(r'([^{}]+)\{([^{}]*)\}', css):
        for s in (x.strip() for x in selraw.split(',')):
            if not s or s in seen: continue
            if COMPOSITE.match(s) or STRUCT.match(s) or '::' in s: continue
            seen.add(s); out.append(s)
    return out

def corpus():
    return (sorted(glob.glob(os.path.join(HERE, "snippets", "*.html")))
            + sorted(glob.glob(os.path.join(HERE, "_proforma", "*.html"))))

def _classes(txt):
    o = set()
    for c in re.findall(r'class="([^"]*)"', txt): o.update(c.split())
    return o

def matches(selector, html, classes):
    """Approximate but conservative descendant match: every simple part must be present."""
    for p in selector.split():
        if p.startswith('.'):
            if not all(c in classes for c in p.split('.') if c): return False
        else:
            m = re.match(r'^([a-zA-Z][a-zA-Z0-9]*)(\..*)?$', p)
            if not m or not re.search(r'<' + m.group(1) + r'[\s/>]', html): return False
            if m.group(2) and not all(c in classes for c in m.group(2).split('.') if c):
                return False
    return True

def kind(selector):
    parts = selector.split()
    if len(parts) == 1 and re.match(r'^[a-zA-Z][a-zA-Z0-9]*$', selector):
        return "pure-bare-element"
    last = parts[-1]
    if re.match(r'^[a-zA-Z]', last) and not last.startswith('.'):
        return "scoped-element"
    return "class"

def radius(selector, files, idx, clsidx):
    return sorted(os.path.basename(f) for f in files if matches(selector, idx[f], clsidx[f]))

def build_state():
    files = corpus()
    idx = {f: open(f).read() for f in files}
    clsidx = {f: _classes(idx[f]) for f in files}
    state = {}
    for s in appended_selectors():
        state[s] = {"kind": kind(s), "files": radius(s, files, idx, clsidx)}
    return files, state

def do_update():
    files, state = build_state()
    reg = json.load(open(REGPATH))
    old = {b["selector"]: b for b in reg["bindings"]}
    bindings = []
    for s in sorted(state, key=lambda x: (-len(state[x]["files"]), x)):
        b = {"selector": s, "kind": state[s]["kind"], "files": state[s]["files"]}
        if state[s]["kind"] in ("pure-bare-element", "scoped-element"):
            b["waived"] = True
        if s in old and old[s].get("note"): b["note"] = old[s]["note"]
        bindings.append(b)
    reg["bindings"] = bindings
    reg["_generated"] = datetime.date.today().isoformat()
    open(REGPATH, "w").write(json.dumps(reg, indent=2) + "\n")
    print("↻ re-seeded %s from current state (%d bindings). REVIEW THE DIFF before committing."
          % (os.path.relpath(REGPATH, HERE), len(bindings)))
    return 0

def main():
    if "--update" in sys.argv:
        return do_update()
    reg = json.load(open(REGPATH))
    registered = {b["selector"]: b for b in reg["bindings"]}
    files, state = build_state()

    fails, notes, rows = [], [], []
    for s in sorted(state, key=lambda x: (-len(state[x]["files"]), x)):
        k = state[s]["kind"]; now = set(state[s]["files"])
        reg_e = registered.get(s)
        status = "PASS"
        if reg_e is None:
            fails.append("UNREGISTERED: `%s` (%s) is appended to a composite but not in the "
                         "registry — a new global binding must be recorded. `--update` then review." % (s, k))
            status = "FAIL·unregistered"
        else:
            declared = set(reg_e.get("files", []))
            escaped = now - declared
            if escaped:
                fails.append("ESCAPED: `%s` now matches %s — outside its acknowledged radius. "
                             "Namespace it, or `--update` and review the diff." % (s, sorted(escaped)))
                status = "FAIL·escaped"
            if k in ("pure-bare-element", "scoped-element") and not reg_e.get("waived"):
                fails.append("UNWAIVED-BARE: `%s` (%s) needs waived:true + a note — bare/scoped-element "
                             "selectors carry structural blast risk." % (s, k))
                status = "FAIL·unwaived"
            if declared - now:
                notes.append("shrunk: `%s` no longer matches %s (safe; tidy the registry with --update)."
                             % (s, sorted(declared - now)))
        rows.append((len(now), k, s, status, sorted(now)))

    # a registered selector that has vanished from type.css entirely — advisory tidy note
    for s in registered:
        if s not in state:
            notes.append("stale: `%s` is in the registry but no longer appended in type.css (tidy with --update)." % s)

    rows.sort(key=lambda r: (-r[0], r[1], r[2]))
    lines = ["# Type-binding blast-radius gate — guards canon/type.css", "",
             "Every selector appended to a composite list is a GLOBAL rule. Registry: "
             "`canon/_type-bindings.json`. Corpus: snippets + _proforma (%d files)." % len(files), "",
             "| radius | kind | selector | status |", "|---:|---|---|---|"]
    for n, k, s, st, _f in rows:
        lines.append("| %d | %s | `%s` | %s |" % (n, k, s, st))
    lines += ["", "## Findings", ""]
    if fails:
        lines += ["- ✗ " + f for f in fails]
    else:
        lines.append("- ✓ every appended selector is registered and within its acknowledged blast radius.")
    if notes:
        lines += ["", "## Housekeeping (non-gating)", ""] + ["- " + n for n in notes]
    lines += ["", "---",
              "Guard-rail for the T-D9 binding mechanism (T-D12 §5). Waived entries are DEBT to "
              "burn down (namespace them) — priority `h2` (25 files) in the non-/1 batch. This gate "
              "does NOT reopen T-D9."]
    open(REPORT, "w").write("\n".join(lines) + "\n")

    for n, k, s, st, _f in rows:
        print("  [%s] %-13s %s (%d)" % ("PASS" if st == "PASS" else "FAIL", k, s, n))
    if fails:
        print("\n❌ type-binding blast-radius gate FAILED — see knowledge/_TYPE-BLAST-GATE.md")
        for f in fails: print("     -", f)
        return 1
    print("\n✅ type-binding blast-radius gate passed (%d appended selector(s), corpus %d files)."
          % (len(state), len(files)))
    return 0

if __name__ == "__main__":
    sys.exit(main())
