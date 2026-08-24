"""
_htmlmask.py — the ONE implementation of the HTML COMMENT MASK (#211 lanes R1/R6, W-92 residual).

THE CLASS THIS CLOSES: a raw-text reader satisfied by content that a BROWSER NEVER SEES.
`gen_token_ramp.py` (lane R1) found it first — a `var()` named only inside an HTML comment
counted as a reference, which silently killed 120 declarations and which ds-018's C2 gate was
green over for its whole life. `gen_component_partials.py` (lane R6) then met the same class in
its contract readers, and fixed it by COPYING the function, with the duplication declared in the
docstring: *"duplicated rather than imported: importing a sibling generator runs its help gate."*

⚠ THAT REASON WAS FALSE, and it is worth saying so rather than quietly deleting it: `help_gate`
is a NO-OP when a module is imported (`__name__ != "__main__"` returns immediately — see
`_helpgate.py`). What was true is the sharper thing: A GENERATOR SHOULD NOT IMPORT A SIBLING
GENERATOR, because that couples two build steps for one 15-line helper. The remedy for that is a
module with no side effects — this one — not a second copy.

⛔ WHY A COPY WAS A DEFECT AND NOT A CONVENIENCE (W-92, carried to #218): two byte-identical
implementations with NO GATE COMPARING THEM. A fix to one — an entity edge case, a CDATA rule, a
`<!-->` quirk — lands in one generator and not the other, and both selftests stay green, because
each drives its own copy. One implementation, two consumers, and the drift is not possible.

This module deliberately has NO side effects, no argv, and no entry point (same shape as
`_helpgate.py`): importing it can never run work, so it is safe from the #158 class by
construction. Its consumers' selftests drive it — `gen_token_ramp.py --selftest` and
`gen_component_partials.py --selftest` each assert the function they hold CAME FROM HERE, so
re-introducing a local copy goes RED instead of going unnoticed.
"""

COMMENT_OPEN, COMMENT_CLOSE = "<!--", "-->"


def mask_comments(html):
    """Blank every HTML comment's bytes, PRESERVING LENGTH and newlines (#211).

    Returned string is index-for-index aligned with the input, so an offset or span found in
    the mask addresses the same bytes in the original (`manifest_vars` relies on exactly that).
    An UNTERMINATED `<!--` masks to EOF, which is what a browser does — a generator that stopped
    at the missing `-->` would be guessing (ds-025).
    """
    out = list(html)
    i = 0
    while True:
        a = html.find(COMMENT_OPEN, i)
        if a < 0:
            return "".join(out)
        b = html.find(COMMENT_CLOSE, a + len(COMMENT_OPEN))
        end = len(html) if b < 0 else b + len(COMMENT_CLOSE)
        for k in range(a, end):
            if out[k] != "\n":
                out[k] = " "
        i = end


def selftest_mask():
    """The mask's OWN properties, in one place, so both consumers inherit the same bites.
    Returns a list of failure strings ([] = green). Called BY the consumers' selftests —
    a helper whose tests live only in one caller is half-tested [[green-tests-cannot-see-scope]].
    """
    fails = []
    for probe in ('<a><!-- x --><b>', '<a><!-- never closed', 'no comments here',
                  '<!--\nmulti\nline\n-->tail'):
        m = mask_comments(probe)
        if len(m) != len(probe):
            fails.append(f"mask_comments changed LENGTH on {probe!r} — every span offset a "
                         f"consumer takes from the mask would misaddress the original")
        if m.count("\n") != probe.count("\n"):
            fails.append(f"mask_comments ate a newline on {probe!r} — line numbers misalign")
    if "unterminated" in mask_comments('<style>x</style><!-- unterminated'):
        fails.append("an unterminated <!-- did not mask to EOF (a browser reads it as a comment)")
    if mask_comments('<b>live</b>') != '<b>live</b>':
        fails.append("mask_comments altered a document with no comments — it is over-reaching")
    if "dead" in mask_comments('<!-- dead --><b>live</b>'):
        fails.append("mask_comments left comment bytes readable — the whole #211 class is back")
    if "live" not in mask_comments('<!-- dead --><b>live</b>'):
        fails.append("mask_comments blanked LIVE bytes — the mask reaches past the comment")
    return fails
