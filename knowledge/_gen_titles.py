#!/usr/bin/env python3
"""_gen_titles.py — mechanise the two wrap-time session titles (#120, residual ⓪).

WHY: runbook step 4b (`_RUNBOOK-capture-ritual.md:413-437`) has always delivered two names at
wrap — RENAME (retrospective, chat-only, RULED #28) and NEXT SESSION TITLE (forward, written to
the top of `GOOD-MORNING.md`, gated BLOCKING by `_capture_gate.py`'s TITLE_LINE_RE/TITLE_CAP_TAPE,
RULED #60-D8). Both were hand-authored prose every session — Dave's #119 post-wrap ask: derive
them MECHANICALLY from artefacts already on disk, so "chat delivery" becomes a paste of this
script's stdout, never a fresh prose recall of the session.

INPUTS (both already exist, nothing new to maintain):
  - the ★ LATEST banner in `GOOD-MORNING.md` (blockquoted `> ## ★ LATEST — ... **#N** ...`,
    the outgoing session's own summary of itself) → RENAME's raw material.
  - the top `residual → #<N+1>:` bullet in the same file → NEXT-TITLE's raw material (the single
    biggest thing left, which is what a forward title is FOR).

OUTPUT: two ready-to-use lines, printed to stdout, AND a receipt file
`knowledge/_gen_titles_receipt.json` (session-owned generated artefact, same class as
`_rehearsal_log_append`'s log — the wrap gate's only witness that RENAME was generated this
session, since RENAME itself is never written into GOOD-MORNING.md, RULED #28).

  python3 knowledge/_gen_titles.py --session 120           # derive + print + write receipt
  python3 knowledge/_gen_titles.py --session 120 --check   # print only, no receipt write
  python3 knowledge/_gen_titles.py --selftest              # mutation-tested bites

Refuses loud and named when its inputs are missing or unparsable — never guesses, never
silently falls back to a placeholder (repo rule: a parse helper that cannot parse REFUSES;
[[a-crash-is-not-a-fail]]).
"""
import argparse
import json
import os
import re
import sys
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GM = os.path.join(ROOT, "GOOD-MORNING.md")
RECEIPT = os.path.join(HERE, "_gen_titles_receipt.json")

TITLE_CAP_TAPE = 120  # same cap _capture_gate.py enforces on TITLE THE NEXT CHAT (#60-D8);
                       # applied to BOTH derived lines here — one mechanism, not two rules.

BANNER_RE = re.compile(r"^>\s*##\s*★\s*LATEST\s*—.*$", re.M)
SESSION_NO_RE = re.compile(r"\*\*#(\d+)\*\*")
RESIDUAL_RE = re.compile(r"^>\s*\*\*residual\s*→\s*#(\d+):\*\*\s*(.*)$", re.M)
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")


class TitleDeriveError(Exception):
    """Refuses loud and named — never a silent placeholder."""


def _tape(text):
    """Cheap, dependency-free tape measure (chars), consistent with the cap's own unit
    intent (a bound on the LABEL's size, not a token-exact count) — mirrors the advisory
    fallback already accepted elsewhere in this toolchain when the real gauge isn't the
    point of the check."""
    return len(text)


def extract_banner_line(gm_text):
    m = BANNER_RE.search(gm_text)
    if not m:
        raise TitleDeriveError(
            "no `> ## ★ LATEST —` banner line found in GOOD-MORNING.md — cannot derive RENAME "
            "without it. Ritual step 2 writes this banner before titling can run.")
    return m.group(0)


def extract_session_no(banner_line):
    m = SESSION_NO_RE.search(banner_line)
    if not m:
        raise TitleDeriveError(
            f"banner line has no **#N** session marker — cannot derive RENAME's session number. "
            f"Line: {banner_line!r}")
    return int(m.group(1))


def extract_headline(banner_line):
    """The first bolded clause after the em-dash divider that FOLLOWS the **#N** session
    marker (the banner's parenthetical opens with a second ' — ' before **#N**, e.g.
    '★ LATEST — 2026-08-07 (Fri **#119**, ... — ✅ **headline**)' — the divider that matters
    is the one after the marker, never the first one on the line). Refuses if the shape isn't
    there rather than falling back to the whole banner (which would blow the tape cap
    silently)."""
    marker = SESSION_NO_RE.search(banner_line)
    if not marker:
        raise TitleDeriveError(
            f"banner line has no **#N** session marker — cannot anchor the headline search. "
            f"Line: {banner_line!r}")
    after_marker = banner_line[marker.end():]
    if " — " not in after_marker:
        raise TitleDeriveError(
            f"banner line has no ' — ' divider after the **#N** marker — cannot isolate "
            f"a headline. Remainder: {after_marker!r}")
    tail = after_marker.split(" — ", 1)[1]
    m = BOLD_RE.search(tail)
    if not m:
        raise TitleDeriveError(
            f"no bolded clause found after the banner's ' — ' divider — cannot derive a "
            f"headline. Tail: {tail!r}")
    headline = m.group(1).strip()
    # strip nested markdown the bold clause may carry (backtick code spans, inner bold)
    headline = re.sub(r"`([^`]*)`", r"\1", headline)
    headline = headline.strip(" *")
    if not headline:
        raise TitleDeriveError(f"headline extracted empty from tail: {tail!r}")
    return headline


def extract_top_residual(gm_text, session_no):
    """The first ⬛ bullet under `residual → #<session_no + 1>:` — the single biggest open
    item, which is what a forward title exists to name. The residual line is ADDRESSED TO
    the INCOMING session (`residual → #N+1`), so the wrapping session N expects N+1 here.
    ⚠ OFF-BY-ONE FIXED #121: this check compared found_no == session_no, which forced the
    #120 wrap to declare --session 121 to pass, which then minted NEXT-TITLE #122 for a
    session whose residual said #121 — the receipt and the GM header disagreed by one.
    Refuses if the residual doesn't name session_no + 1 (a stale residual would silently
    mis-title the wrong future session)."""
    m = RESIDUAL_RE.search(gm_text)
    if not m:
        raise TitleDeriveError(
            "no `> **residual → #N:**` line found in GOOD-MORNING.md — cannot derive "
            "NEXT-TITLE without it.")
    found_no, rest = int(m.group(1)), m.group(2)
    if found_no != session_no + 1:
        raise TitleDeriveError(
            f"residual line names #{found_no}, but --session {session_no} was declared — "
            f"a wrap at #{session_no} expects the residual addressed to #{session_no + 1}. "
            f"Refusing rather than mis-titling; re-check which session is running.")
    if "⬛" not in rest:
        raise TitleDeriveError(
            f"residual → #{found_no} line has no ⬛ bullet — cannot find a top item. "
            f"Text: {rest!r}")
    after = rest.split("⬛", 1)[1]
    # stop at the next ⬛ item (' · ⬛ ') if present, else take the rest of the line
    after = after.split(" · ⬛", 1)[0]
    m2 = BOLD_RE.search(after)
    if not m2:
        raise TitleDeriveError(f"top residual bullet has no bolded clause: {after!r}")
    item = m2.group(1).strip()
    item = re.sub(r"`([^`]*)`", r"\1", item)
    # trim to the label-like prefix: up to the first colon, else first ~12 words
    if ":" in item:
        item = item.split(":", 1)[0]
    else:
        words = item.split()
        item = " ".join(words[:12])
    # strip a leading circled-number marker (⓪①②… U+2460-U+24FF, counts as \w to Python's re
    # so a generic non-word strip misses it) or any other single leading glyph + space.
    item = re.sub(r"^[①-⓿]\s*", "", item)
    item = re.sub(r"^[^\w(]+\s*", "", item).strip()
    if not item:
        raise TitleDeriveError(f"top residual item reduced to empty after trimming: {after!r}")
    return item


def derive(gm_text, session_no=None):
    """Returns (rename_line, next_title_line, meta). Pure — the selftest bites this."""
    banner_line = extract_banner_line(gm_text)
    banner_session = extract_session_no(banner_line)
    n = session_no if session_no is not None else banner_session
    headline = extract_headline(banner_line)
    rename_target = f"Apollo - #{banner_session}: {headline.lower()}"
    rename_line = f"RENAME THIS SESSION → `{rename_target}`"

    residual_item = extract_top_residual(gm_text, n)
    next_no = n + 1
    next_target = f"Apollo - #{next_no}: {residual_item.lower()}"
    next_title_line = f"NEXT SESSION TITLE → `{next_target}`"

    for label, line in (("RENAME", rename_line), ("NEXT-TITLE", next_title_line)):
        t = _tape(line)
        if t > TITLE_CAP_TAPE:
            raise TitleDeriveError(
                f"{label} line measures {t} tape, cap {TITLE_CAP_TAPE} (RULED #60-D8, applied "
                f"to both derived lines here) — shorten the source headline/residual bullet, "
                f"never truncate blindly at generation time.")

    meta = {"banner_session": banner_session, "declared_session": n, "next_session": next_no}
    return rename_line, next_title_line, meta


def write_receipt(rename_line, next_title_line, meta):
    payload = {
        "rename": rename_line,
        "next_title": next_title_line,
        "meta": meta,
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
    }
    with open(RECEIPT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
        f.write("\n")
    return RECEIPT


# ---------------------------------------------------------------- selftest
_FIXTURE_GM = """\
> **TITLE THE NEXT CHAT →** `placeholder`
> ## ★ LATEST — 2026-08-07 (Fri **#119**, some conductor — ✅ **THE WIRING SEAM IS CLOSED: stuff BUILT + WIRED, 4 BITES GREEN** · ✅ **OTHER THING**)
>
> **residual → #120:** ⬛ **⓪ MECHANISE TITLING (Dave, #119 post-wrap): do the thing** · ⬛ **① second item**
"""


def selftest():
    fails = []

    # control: well-formed fixture derives cleanly
    try:
        rename, next_title, meta = derive(_FIXTURE_GM, session_no=119)
        if "#119" not in rename or "wiring seam is closed" not in rename.lower():
            fails.append(f"control: RENAME derived wrong: {rename!r}")
        if "#120" not in next_title or "mechanise titling" not in next_title.lower():
            fails.append(f"control: NEXT-TITLE derived wrong: {next_title!r}")
    except TitleDeriveError as e:
        fails.append(f"control: well-formed fixture REFUSED — should have derived: {e}")

    # bite 1: no banner line at all -> named refusal, not a crash, not a placeholder
    mutant = _FIXTURE_GM.replace("> ## ★ LATEST — 2026-08-07", "> not a banner")
    try:
        derive(mutant, session_no=120)
        fails.append("bite 1: missing banner did NOT refuse")
    except TitleDeriveError as e:
        if "no `> ## ★ LATEST" not in str(e):
            fails.append(f"bite 1: refused but with the wrong named cause: {e}")

    # bite 2: no bolded headline after the divider -> named refusal
    mutant = _FIXTURE_GM.replace(
        "— ✅ **THE WIRING SEAM IS CLOSED: stuff BUILT + WIRED, 4 BITES GREEN** · ✅ **OTHER THING**)",
        "— plain text with no bold clause at all)")
    try:
        derive(mutant, session_no=120)
        fails.append("bite 2: missing bold headline did NOT refuse")
    except TitleDeriveError as e:
        if "no bolded clause" not in str(e):
            fails.append(f"bite 2: refused but with the wrong named cause: {e}")

    # bite 3: residual line names a DIFFERENT session than declared -> refuses, never mistitles
    mutant = _FIXTURE_GM.replace("residual → #120:", "residual → #999:")
    try:
        derive(mutant, session_no=119)
        fails.append("bite 3: mismatched residual session did NOT refuse")
    except TitleDeriveError as e:
        if "names #999" not in str(e):
            fails.append(f"bite 3: refused but with the wrong named cause: {e}")

    # bite 4: over the tape cap -> refuses rather than silently truncating
    mutant = _FIXTURE_GM.replace(
        "✅ **THE WIRING SEAM IS CLOSED: stuff BUILT + WIRED, 4 BITES GREEN**",
        "✅ **" + ("VERY LONG HEADLINE TEXT THAT WILL EXCEED THE TAPE CAP " * 4) + "**")
    try:
        derive(mutant, session_no=119)
        fails.append("bite 4: over-cap headline did NOT refuse")
    except TitleDeriveError as e:
        if "cap" not in str(e):
            fails.append(f"bite 4: refused but with the wrong named cause: {e}")

    # bite 5 (mutation control on the control itself): corrupt the derive() logic in a way
    # that would make bite 1 pass for the wrong reason — prove the assertion isn't vacuous by
    # checking the well-formed fixture actually still derives when we DON'T mutate it (this
    # is the paired positive already exercised by the control above; re-stated here so a
    # reader sees the negative bites are contrasted against a live positive, not a stub).
    try:
        derive(_FIXTURE_GM, session_no=119)
    except TitleDeriveError as e:
        fails.append(f"bite 5 (control re-check): unmutated fixture now refuses too: {e}")

    if fails:
        print(f"selftest: {len(fails)} failure(s)")
        for f in fails:
            print(f"  ⛔ {f}")
        return 1
    print("selftest: control derives correctly + 4 named refusals bite + control re-check green ✓")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--session", type=int, default=None,
                     help="declared session number titling now (SESSION_N pattern)")
    ap.add_argument("--check", action="store_true", help="print only, do not write the receipt")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(selftest())

    if not os.path.exists(GM):
        print(f"❌ REFUSED: {GM} not found", file=sys.stderr)
        sys.exit(1)
    with open(GM, encoding="utf-8") as f:
        gm_text = f.read()

    try:
        rename_line, next_title_line, meta = derive(gm_text, session_no=args.session)
    except TitleDeriveError as e:
        print(f"❌ REFUSED: {e}", file=sys.stderr)
        sys.exit(1)

    print(rename_line)
    print(next_title_line)
    if not args.check:
        path = write_receipt(rename_line, next_title_line, meta)
        print(f"— receipt written → {os.path.relpath(path, ROOT)} "
              f"(the wrap gate's witness that both lines were generated this session, since "
              f"RENAME itself is never written into GOOD-MORNING.md, RULED #28)")


if __name__ == "__main__":
    main()
