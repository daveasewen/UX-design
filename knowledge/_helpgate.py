#!/usr/bin/env python3
"""
_helpgate.py — the ONE remedy for the GENERATORS-WRITE-BY-DEFAULT class (#158).

The class (homed in `_FUTURE-STATE.md` § "COPIED UP AT #153's 2d EXIT CHECK",
born #150, unfixed through #157): a generator does its work — and its WRITES —
before it has looked at argv. `python3 knowledge/gen_showroom.py --help` at #157
therefore rewrote `showroom/`; an unrecognised argv entry was silently taken as a
snippet-name FILTER because there was no argv contract at all. Every `_build_*`,
`_validate_*` and `gen_*` script that emits an audit file shared the defect: at
#158 a runtime write-probe measured **52 scripts that attempted a repo write on a
bare `--help`**, 14 of them at MODULE level (before any `main()` even exists).

The remedy is one line at the TOP of each entry point, before the module's own
work can run:

    from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

`help_gate` answers `-h` / `--help` with the module docstring and exits 0 — so the
help path can never reach a write. It is a NO-OP when the module is imported as a
library (`__name__ != "__main__"`), so importers like gen_showroom -> gen_theme_cascade
are unaffected.

The gate that keeps it there: `knowledge/_validate_help_gate.py` (AST — it parses
the consumer's grammar: every entry-point script must call the guard among its
opening statements, before any other executable statement).

This module deliberately has NO side effects of its own.

--------------------------------------------------------------------------------
SIBLING LEG — `write_gate`: the NO-ARGS write freedom (#158 residual ⑤).

`help_gate` closes the `--help` path. Its sibling leg is the BARE invocation:
`python3 knowledge/_audit_props_axes.py` with no argv at all silently overwrote
a dated, session-stamped review artefact, because its output path was an argparse
DEFAULT rather than a stated intention. Same class, other door: the script did
work — and WRITES — that argv never asked for.

The remedy is the same shape, one line at the TOP of the entry point, directly
after the help gate:

    from _helpgate import write_gate as _write_gate; _write_gate(__file__)

`write_gate` REFUSES a bare no-args invocation, LOUD and NAMED (a marker string
`REFUSED (write-gate)`, exit 2, on stderr) and tells the caller which flag makes
the write intentional. It is a no-op the moment argv carries ANY argument — so
`--help`, the script's real flags, and the explicit `--write` all proceed, and no
existing invocation that stated its intention is affected.

Scripts whose no-args write is their DESIGNED contract are NOT gated (that would
break a documented workflow); they stay off the wiring list deliberately.

--------------------------------------------------------------------------------
THIRD LEG — `pack_gate`: the CANON-GENERATOR WARNING, IN A SHIPPED PACK ONLY
(#219 N1, `s219-D5` Q3).

Dave ruled that the canon generators SHIP with the designer pack — "v3 is the
working engine, the gates are in the pack too" — and that a designer who reaches
for one gets an explicit warning first. His framing, kept verbatim because it is
the whole argument: *"Shipping them means a designer can change a token and
re-mint canon. It also means they can produce canon that never passed a gate."*

⛔ THE CONSTRAINT THAT PICKED THIS DESIGN. The pack's own audit compares every
shipped file to the repo blob it came from (`_gen_pack_manifest.check_pack`), so
the copy in the zip must be BYTE-IDENTICAL to the copy in the repo. A warning
injected at bake time, or a stager-written wrapper standing in front of a renamed
original, both break that: the audit would either go red or have to be taught an
exception, and an audit with an exception carved into it is the thing it was
built to replace. So there is ONE copy of each generator, byte-identical
everywhere, and the WARNING IS CONDITIONAL ON WHERE IT FINDS ITSELF RUNNING.

The condition is the pack's own marker: a `_MANIFEST.json` carrying the pack
manifest's schema, sitting beside a `knowledge/` directory. That file exists only
in an unzipped pack — the stager writes it — and never in this repo. So in the
repo `pack_gate` walks up, finds no marker, and returns: behaviour unchanged,
provably, on the same bytes.

The escape hatch is a stated intention, exactly like `write_gate`'s: pass
`--i-understand` and the generator runs.
"""
import os
import sys

FLAGS = ("-h", "--help", "--usage")

WRITE_FLAG = "--write"
REFUSAL_MARKER = "REFUSED (write-gate)"

PACK_MARKER = "_MANIFEST.json"
PACK_SCHEMA_PREFIX = "apollo-designer-pack-manifest"
PACK_FLAG = "--i-understand"
PACK_REFUSAL_MARKER = "REFUSED (pack-gate)"


def help_gate(doc, name="__main__", file=None):
    """Exit 0 with usage text when argv asks for help. No-op on import."""
    if name != "__main__":
        return
    if not any(a in FLAGS for a in sys.argv[1:]):
        return
    text = (doc or "").strip()
    if not text:
        text = "%s — no module docstring." % (file or sys.argv[0])
    sys.stdout.write(text + "\n")
    sys.exit(0)


def write_gate(file=None, flag=WRITE_FLAG, writes=None, name="__main__"):
    """Refuse a BARE (no-argv) invocation of a script that writes. No-op on import.

    Fails LOUD and NAMED: marker `REFUSED (write-gate)`, exit 2, stderr. Never
    silently skips — the only silent path is "argv carried an argument", i.e. the
    caller stated an intention.
    """
    if name != "__main__":
        return
    if sys.argv[1:]:
        return
    who = os.path.basename(file or sys.argv[0] or "<script>")
    target = (" It would overwrite: %s." % writes) if writes else ""
    sys.stderr.write(
        "✖ %s: %s WRITES FILES and was invoked with NO ARGUMENTS.%s\n"
        "  A bare run is not a stated intention (#158 write-by-default class, no-args leg).\n"
        "  Pass %s to confirm the write, or pass the script's real arguments"
        " (%s --help for the contract).\n" % (REFUSAL_MARKER, who, target, flag, who))
    sys.exit(2)


def pack_root(start):
    """The unzipped-pack root above `start`, or None if there is not one.

    The marker is `_MANIFEST.json` beside `knowledge/`, and the file must actually BE a pack
    manifest — the schema is read, not assumed. Anything unreadable is treated as "not a
    marker" and the walk continues: a guard that raises on a stray JSON file would break every
    generator it is supposed to protect [[a-crash-is-not-a-fail]] — this leg fails OPEN, and
    the pack audit is what proves the marker is there.
    """
    d = os.path.dirname(os.path.abspath(start))
    while True:
        marker = os.path.join(d, PACK_MARKER)
        if os.path.isfile(marker) and os.path.isdir(os.path.join(d, "knowledge")):
            try:
                import json
                with open(marker, encoding="utf-8") as f:
                    if str(json.load(f).get("schema", "")).startswith(PACK_SCHEMA_PREFIX):
                        return d
            except Exception:
                pass
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def pack_gate(file=None, flag=PACK_FLAG, name="__main__", what=None):
    """Warn — and REFUSE — when a canon generator is run inside a shipped pack. No-op here.

    Returns the pack root when it proceeded inside a pack (so a caller can say so), None when
    it was a no-op. Exits 2 with the warning when the flag is absent.
    """
    if name != "__main__":
        return None
    root = pack_root(file or sys.argv[0])
    if root is None:                      # not in a pack — this is the repo, nothing changes
        return None
    who = os.path.basename(file or sys.argv[0] or "<script>")
    subject = what or "canon"
    if flag in sys.argv[1:]:
        # CONSUMED, not passed on. The generators below have their own argv contracts and one
        # of them (#157) treated an unrecognised argument as a snippet FILTER — an acknowledgement
        # flag that survived into that parse would silently change what got minted.
        sys.argv = [a for a in sys.argv if a != flag]
        sys.stderr.write(
            "⚠ pack-gate: %s is re-minting %s inside the Apollo pack at %s, and you passed %s.\n"
            "  Run the gates afterwards — %s is what tells you whether what you just minted "
            "still passes.\n" % (who, subject, root, flag, "ci-template/run-gates.py"))
        return root
    sys.stderr.write(
        "✖ %s: %s MINTS %s, and you are inside a shipped Apollo pack (%s).\n"
        "\n"
        "  Read this once. Changing a token and re-minting canon can produce canon that never\n"
        "  passed a gate. The generators are here because this pack is the working engine and\n"
        "  not a baked copy of one — but the canon in your hands right now is canon that was\n"
        "  gated, and the moment you re-mint it that is no longer true of the new file.\n"
        "\n"
        "  If you mean it:  %s %s <the script's own arguments>\n"
        "  Then, always:    python3 ci-template/run-gates.py\n"
        % (PACK_REFUSAL_MARKER, who, subject, root, who, flag))
    sys.exit(2)
