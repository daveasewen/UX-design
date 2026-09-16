#!/usr/bin/env python3
"""_splice.py — build the FOUR proposed metas for #277 lane LA by TEXTUAL SPAN
insertion into the live component metas, and write WHYS.md from the same data.

⛔ NOTHING UNDER knowledge/ IS WRITTEN. This script READS the four live metas and
WRITES only under notes/_lanes/277/land/. Run it again and it reproduces the
proposals byte-for-byte; lane LL re-runs it rather than trusting a pasted file.

WHY A SPLICE AND NOT `json.dump` (the _inscribe_ruling.py discipline, #179):
a `json.load` -> `edges["obeys"] = [...]` -> `json.dump` round trip reformats every
line the serializer's defaults disagree with — escape style, indent width,
ensure_ascii, the one-object-per-line style these chart metas are hand-kept in.
The diff then buries 87 real additions inside hundreds of spurious ones. So the
insertion here is a SPAN OF TEXT into the live bytes, and it is PROVEN BY
RECONSTRUCTION, not by trust:

    R1 RECONSTRUCT — removing exactly the inserted span from the new text must give
                     back the ORIGINAL BYTES, `==` on the raw string.
    R2 PARSES      — the new text must json.loads, and must equal the live object
                     plus exactly one key, edges.obeys, of the expected length.
    R3 GROUNDED    — ⛔ THE ONE THAT MATTERS. Every `$why` carries anchors: exact
                     substrings of the LIVE meta it is authored against. Each is
                     grepped in the live bytes, its line number recorded, and a
                     MISSING anchor REFUSES the build, loudly, by name. Two
                     sentences failed the conductor's Fable check on 2026-09-16 for
                     naming a mechanism that was not in the file; this is the check
                     that makes that unrepeatable. A "!needle" anchor asserts an
                     ABSENCE and is checked the same way.
    R4 COUNTS      — the per-component split must equal _whys.EXPECTED (s277-D1/D2/D3).
    R5 NO-OBEYS    — the live meta must not already carry edges.obeys (this lane
                     mints the block; it does not merge into one).

Usage:
  python3 notes/_lanes/277/land/_splice.py            # build proposals + WHYS.md
  python3 notes/_lanes/277/land/_splice.py --check    # prove only, write nothing
"""
import importlib.util
import json
import sys
from pathlib import Path

LANE = Path(__file__).resolve().parent
REPO = LANE.parents[3]
LIVE = REPO / "knowledge" / "components"
OUT = LANE / "proposed-metas"
WHYS = LANE / "WHYS.md"

_s = importlib.util.spec_from_file_location("_whys", LANE / "_whys.py")
W = importlib.util.module_from_spec(_s)
_s.loader.exec_module(W)


class SpliceRefused(RuntimeError):
    """LOUD AND NAMED. A refusal that reads like a success is how bad data lands."""


def edges_open_index(text):
    """Index of the `{` that opens the top-level `edges` object, found by SCANNING.

    A regex would match `"edges"` inside a $note one day. This takes the last
    `"edges"` key at object depth 1 and then its own `{`."""
    hits = [i for i in range(len(text)) if text.startswith('"edges":', i)
            and text[i - 3:i] == "\n  "]
    if len(hits) != 1:
        raise SpliceRefused(f"REFUSED (structure) - found {len(hits)} top-level `edges` keys, need 1.")
    return text.index("{", hits[0])


def grep(text, needle):
    """(line_no, ...) 1-based lines on which `needle` occurs in the raw bytes."""
    return [n for n, ln in enumerate(text.splitlines(), 1) if needle in ln]


def check_anchors(stem, text, entries):
    """R3. Every anchor grepped in the LIVE bytes; refuse on a miss, by name."""
    hits, missing = {}, []
    for ref, why, anchors in entries:
        for a in anchors:
            if a.startswith("!"):
                needle, want = a[1:], False
            else:
                needle, want = a, True
            lines = grep(text, needle)
            if bool(lines) != want:
                missing.append((ref, a, "present but asserted ABSENT" if lines else "NOT IN THE FILE"))
            hits[(ref, a)] = lines
    if missing:
        msg = "\n".join(f"    {stem} {ref}  anchor {a!r}  -> {reason}" for ref, a, reason in missing)
        raise SpliceRefused(
            f"REFUSED (grounded) - {len(missing)} anchor(s) do not hold against the LIVE "
            f"{stem}.meta.json. A `$why` may only name a mechanism that is in the file.\n{msg}")
    return hits


def compose(text, entries):
    """Return (new_text, at, span). Serializes ONLY the obeys block; every other
    byte of the live file is carried through untouched by construction."""
    obeys = [{"ref": ref, "$why": why} for ref, why, _ in entries]
    block = json.dumps({"obeys": obeys}, indent=2, ensure_ascii=False)
    inner = block.splitlines()[1:-1]            # drop the wrapper `{` and `}`
    body = "\n".join("  " + ln for ln in inner)  # edges' children sit at indent 4
    span = "\n" + body + ","
    at = edges_open_index(text) + 1
    return text[:at] + span + text[at:], at, span


def build(stem, entries, write):
    src = LIVE / f"{stem}.meta.json"
    text = src.read_text(encoding="utf-8")
    live = json.loads(text)

    if "obeys" in live.get("edges", {}):                                     # R5
        raise SpliceRefused(f"REFUSED (no-obeys) - live {stem} already carries edges.obeys; "
                            f"this lane mints the block and does not merge into one.")

    n_file = sum(1 for r, _, _ in entries if r.split(":")[1].startswith(("dv-line-", "dv-pie-", "dv-bar-")))
    n_fam = len(entries) - n_file
    want = W.EXPECTED[stem]
    if (n_file, n_fam) != want:                                              # R4
        raise SpliceRefused(f"REFUSED (counts) - {stem} is {n_file}+{n_fam}, expected {want[0]}+{want[1]}.")

    hits = check_anchors(stem, text, entries)                                # R3

    new, at, span = compose(text, entries)
    if new[:at] + new[at + len(span):] != text:                              # R1
        raise SpliceRefused(f"REFUSED (reconstruct) - removing the span from {stem} "
                            f"does not give back the original bytes.")
    got = json.loads(new)                                                    # R2
    obeys = got["edges"].pop("obeys")
    if got != live:
        raise SpliceRefused(f"REFUSED (parses) - {stem} differs from the live object by more "
                            f"than edges.obeys.")
    if len(obeys) != len(entries) or any(set(e) != {"ref", "$why"} for e in obeys):
        raise SpliceRefused(f"REFUSED (parses) - {stem}'s spliced obeys is not the authored list.")

    if write:
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / f"{stem}.meta.json").write_text(new, encoding="utf-8")
    return dict(stem=stem, n_file=n_file, n_fam=n_fam, span=len(span), at=at,
                live_lines=text.count("\n") + 1, hits=hits)


def whys_md(results):
    rows = []
    for stem in ("chart-line", "chart-pie", "chart-bar", "chart-donut"):
        r = next(x for x in results if x["stem"] == stem)
        for ref, why, anchors in W.COMPONENTS[stem]:
            cite = []
            for a in anchors:
                lines = r["hits"][(ref, a)]
                if a.startswith("!"):
                    cite.append(f"**ABSENT** `{a[1:]}` — 0 hits in the live file")
                else:
                    ln = ", ".join(f"L{n}" for n in lines)
                    cite.append(f"`{a}` — {ln}")
            rows.append((stem, ref.split(":", 1)[1], why, "<br>".join(cite)))

    def esc(s):
        return s.replace("|", "\\|")

    out = [
        "# WHYS — the 87 authored `$why` sentences, each against the string in the LIVE meta it rests on",
        "#277 · 2026-09-16 · lane LA · **PROPOSED — nothing under `knowledge/` is written**",
        "",
        "This table is GENERATED by `_splice.py` from `_whys.py`, so the sentence graded here and the",
        "sentence in `proposed-metas/` are one string. The line numbers are MEASURED against the live",
        "`knowledge/components/<stem>.meta.json` at build time by grepping the raw bytes — a sentence",
        "whose anchor does not grep REFUSES the build and never reaches this table.",
        "",
        "Two anchors are NEGATIVE (`ABSENT`): `chart-line` -> `dv-line-001` rests on chart-line carrying",
        "**no** `data-domain-min` antiPattern where chart-bar carries one, and `chart-bar` -> `dv-bar-008`",
        "rests on chart-bar declaring **no** projected variant. An absence is checkable exactly as a",
        "presence is, and both are checked.",
        "",
        "| # | component | rule | `$why` | the exact string in the LIVE meta it rests on (grep hit + line) |",
        "|---:|---|---|---|---|",
    ]
    for i, (stem, rule, why, cite) in enumerate(rows, 1):
        out.append(f"| {i} | `{stem}` | `{rule}` | {esc(why)} | {esc(cite)} |")
    out += ["", "## Counts", "",
            "| component | rule-file citations | family citations | total |", "|---|---:|---:|---:|"]
    tot = 0
    for r in results:
        out.append(f"| `{r['stem']}` | {r['n_file']} | {r['n_fam']} | {r['n_file'] + r['n_fam']} |")
        tot += r["n_file"] + r["n_fam"]
    out.append(f"| **all four** | | | **{tot}** |")
    out += ["",
            "`chart-donut` carries **0 family citations by ruling**: s277-D3 attaches the 19 family rules to",
            "chart-bar / chart-line / chart-pie only, and s277-D2 gives the donut the pie FILE. Not widened.",
            ""]
    return "\n".join(out)


def main():
    write = "--check" not in sys.argv
    results = [build(s, W.COMPONENTS[s], write)
               for s in ("chart-line", "chart-pie", "chart-bar", "chart-donut")]
    for r in results:
        print(f"  {r['stem']:<12} {r['n_file']:>2} file + {r['n_fam']:>2} family "
              f"= {r['n_file'] + r['n_fam']:>2}  | span {r['span']} chars inserted at byte {r['at']} "
              f"| R1 reconstruct OK · R2 parses OK · R3 anchors OK")
    total = sum(r["n_file"] + r["n_fam"] for r in results)
    print(f"  TOTAL {total} obeys edges, every one with an authored $why grounded in the live file.")
    if write:
        WHYS.write_text(whys_md(results), encoding="utf-8")
        print(f"  wrote {OUT}/ (4 metas) and {WHYS}")
    else:
        print("  --check: nothing written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
