#!/usr/bin/env python3
"""
gen_canon_bento.py — compile the BENTO structural grammar into canon.css (s217-D2, #217).

THE MINT STEP. `tokens/layout.json` -> `layout/bento/*` is the parameter store; the four
themes diverge on ONE of them (gutter), carried in their own override sets. This generator
turns that store into the AUTO-BENTO block of canon/canon.css:

  * the parameter surface — custom properties on the CONTAINER, seeded from the theme-minted
    token vars, so a theme override reaches every bento with no per-component wiring;
  * the span vocabulary — `data-c` / `data-r` on tiles, CHILD-scoped so a nested bento's
    tiles are never re-spanned by the outer bento's rules;
  * the responsive bands — CONTAINER queries, compiled as CONCRETE LITERALS because a
    container-query condition cannot read a custom property (s200-D1 mint-time derivation:
    the number is decided here, not resolved at runtime).

WHY A GENERATOR AND NOT HAND-WRITTEN CSS: the band literals are the exact case the
"generated, never hand-copied" principle exists for — they cannot be var()s, so if they were
hand-typed the store and the stylesheet would be two sources for one number, and only the
stylesheet would be true. Here the store is the only source.

⚠ RADIUS MODEL (s217-D2, Dave's words): the theme radius token applies to each bento's OUTER
CONTAINER, never the individual tiles — `border-radius/container` on `.c-bento`, plus
`overflow:hidden`. The clip is not decoration: without it the square tile corners poke
through the rounded container edge and the treatment does not read at all.

⚠ THE ASPECT THRESHOLDS ARE PHOTOGRAPHY-ONLY (s217-D2, in as many words). `span_for()` is the
photography derivation. Card spans are AUTHORED — wiring the thresholds onto cards would
silently re-lay-out every card wall. `emphasise()` applies to both: it is POSITION, not
preference.

✅ THE SQUARING PASS IS **RATIFIED** by `s217-D3` — *for the DASHBOARD and BROCHUREWARE roles*
(#217, Dave: "is very cool", with gallery exempted in the same breath). `square_wall()` below is
the mechanism; it mints NOTHING into canon.css — it only rewrites the `data-c`/`data-r` a
generator was about to emit. **GALLERY IS EXEMPT**: orphans are acceptable there, the requirement
is only a layout appropriate to portrait and landscape images. Ask `role_policy(role)["squaring"]`
— never re-decide it in a page generator.

✅ AND IT RUNS ON **NESTED** WALLS TOO — `s217-D7` extends the same ratification to the inner
bentos of a dashboard (Dave: "BTW inner bentos should run the squaring pass"). An inner wall is
squared at ITS OWN column dial, never the page's — see `inner_ladder()`. ⛔ THE CLASS FIX IS
`square_nested_wall()`: a bento-of-bentos mints BOTH levels in one call, because the #217 defect
was never a wrong pass, it was a generator that hand-wrote `data-c="1"` and never ASKED. Two call
sites re-open exactly that hole one level down.

⚠ EXEMPT FROM SQUARING IS NOT EXEMPT FROM THE ASPECT MAPPING. They are DIFFERENT MECHANISMS:
`span_for()`'s portrait two-row threshold (s217-D2) runs for every photography bento whatever its
role. Turning squaring off in gallery must leave the portrait/landscape mapping exactly where it
was — that mapping IS the "appropriate layout" the role asks for.

ROLES (s217-D3), compiled from `layout/bento/$roles` into `[data-bento-role=…]` rules:
  * **dashboard** — theme radius on each inner bento's CONTAINER, tiles square, 1px spacing
    INSIDE the inner walls. ⚠ The outer wall of a bento-of-bentos keeps the theme gutter; a
    blanket 1px would collapse the very structure the role describes.
  * **brochureware** — the TILES carry the radius and the spacing; the container is square.
  * **gallery** — as brochureware, plus the generous caption space and no squaring.
The grammar is IDENTICAL in all four themes. Console is only the theme where the difference is
VISIBLE, because its radius token is non-zero.

THE SQUARING ALGORITHM, in full
-------------------------------
The defect: a tile wall whose last row is partly empty, or whose tall tiles hang below an
otherwise straight bottom edge — an "orphaned compartment". CSS cannot fix this; `dense`
packing back-fills holes but cannot invent or resize a tile, and a JS/CSS hack would be a
runtime patch on a mint-time problem. So it is decided here, once, in the span vocabulary.

  1 · PLACEMENT SIMULATION. `place()` reproduces the CSS grid auto-placement algorithm for
      `grid-auto-flow: row dense` with definite spans: for each tile in order, reset the cursor
      to row 1 and take the first free rectangle scanning rows then columns. This is the same
      order the browser uses, so the simulated occupancy IS the rendered occupancy.
  2 · THE RECTANGLE TEST. A wall is square iff, over rows 1..R (R = last row reached), NO cell
      is empty. That single test catches both failure shapes at once — a ragged last row leaves
      holes in row R, and a hanging tall tile leaves holes beside it.
  3 · EVERY BAND, NOT JUST FULL WIDTH. The test runs over the whole COLUMN LADDER the compiled
      bands produce (6 → 3 → 2 → 1 for a default instance; an instance dialled to 3 columns has
      the ladder 3 → 2 → 1). Each band is simulated with the spans the band rules actually leave
      in force: `data-c` clamped to the band's column count, and at ONE column every `data-r`
      forced to 1. ⚠ A wall square at 6 columns and ragged at 3 is the SAME defect, later.
  4 · TAIL REPAIR, SCORED. Only the LAST k tiles may be re-spanned, k running 0,1,2,… to
      `tail_cap`. Every assignment is tested and the winner is chosen by an ORDERED cost —
      (portraits flattened, tail size k, tiles disturbed, enumeration index) — so the answer is
      deterministic: same wall in, same wall out, always. The search stops the moment a
      zero-flatten answer exists, so the common case never enumerates the wide tails.
  5 · PORTRAIT IS PREFERRED, NOT LOCKED, AND IT OUTRANKS THE SMALL TAIL. A tile the aspect rule
      made two rows tall offers its TALL candidates first, and the cost function puts flattened
      portraits ahead of tail size — a LARGER tail that keeps a portrait tall beats a smaller
      one that flattens it. ⚠ A squaring pass that answers Dave's second question by silently
      undoing his first has fixed nothing. Locking portraits outright was measured to make three
      tile counts in 2..40 unsolvable, so the preference is strong, not absolute.
  6 · REFUSAL IS NAMED, NEVER SILENT. Some walls cannot be rectangles at every band — three
      tiles at six columns is the smallest case, and no span assignment fixes it. `square_wall`
      returns `squared: False` with the band and hole count that beat it. A generator must
      print that residual rather than ship a wall it believes is square.

MEASURED (#217, this file's own numbers, not an estimate): over n = 2..40 tiles, mixed
portrait/landscape with the ruled rhythm, **38 of 39 counts square at all four bands** — the one
refusal is n = 3, which is impossible, not unlucky. That sweep is the WORST CASE (every wall
carries portraits, so the search widens the tail before it settles) and costs ~2.9 s per wall;
the real pages are far cheaper — the nine walls of the #217 demo page square in 2.9 s TOTAL.

Usage:
  python3 knowledge/canon/gen_canon_bento.py             # write the AUTO-BENTO block
  python3 knowledge/canon/gen_canon_bento.py --check     # verify in-sync (build gate)
  python3 knowledge/canon/gen_canon_bento.py --selftest  # bite test
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
# s219-D5 (Q3): the canon generators SHIP with the designer pack, and a designer who
# reaches for one is warned first. NO-OP IN THIS REPO — the guard looks for the pack's
# own _MANIFEST.json marker, which only an unzipped pack has. Same bytes both sides.
from _helpgate import pack_gate as _pack_gate; _pack_gate(__file__, name=__name__, what='the canon bento layer')
import json, os, re, sys

HERE  = os.path.dirname(os.path.abspath(__file__))
KNOW  = os.path.dirname(HERE)
TOK   = os.path.join(KNOW, "tokens")
CANON = os.path.join(HERE, "canon.css")
START = "/* ===== AUTO-BENTO START ====="
END   = "/* ===== AUTO-BENTO END ===== */"
ANCHOR = "/* ===== AUTO-COMPONENTS START ====="


class BentoStoreError(RuntimeError):
    """Named refusal: the bento parameter store is missing or malformed."""


def store():
    """The `layout/bento` group. Fails LOUD and NAMED — a missing group must not
    silently compile a bento with no parameters (a-crash-is-not-a-fail)."""
    d = json.load(open(os.path.join(TOK, "layout.json")))
    try:
        return d["layout"]["bento"]
    except KeyError as e:
        raise BentoStoreError(
            "tokens/layout.json has no layout/bento group — s217-D2's parameter store is "
            f"missing ({e}); refusing to emit a grammar with no parameters.")


def roles():
    """The `$roles` metadata block (s217-D3). Fails LOUD and NAMED: a bento compiled with no
    role table would silently ship the s217-D2 grammar under three role names."""
    b = store()
    try:
        return b["$roles"]
    except KeyError as e:
        raise BentoStoreError(
            "layout/bento has no $roles group — s217-D3's role table is missing (%s); refusing "
            "to emit a role grammar with no roles." % e)


def role_policy(role=None):
    """-> the ROLE's policy dict: `radius` (container|tile), `spacing` (tight|theme),
    `squaring` (bool). ⚠ THE ONE PLACE a generator asks 'does this wall get squared?' — an
    inline `if role == "gallery"` in a page generator is a second source for a ruled fact.
    An unknown role is a NAMED refusal, never a quiet fall-back to the default: a typo'd role
    that silently renders as `dashboard` is the mutation arm's whole point."""
    r = roles()
    role = role or r["$default"]
    if role not in r or role.startswith("$"):
        raise BentoStoreError(
            "unknown bento role %r — s217-D3 rules exactly %s. A misspelt role must refuse, "
            "not fall back to the default." % (role, sorted(k for k in r if not k.startswith("$"))))
    return r[role]


# --- CAPTION SPACE: the mint-time derivation (s217-D3 + s200-D1) -----------------------------
# The store carries ONE number, the block height. These are the composite metrics it was derived
# FROM, restated here so the line allowance can be derived BACK OUT of it — and so a change to
# the number moves the clamp with it. ⚠ If these ever disagree with canon/type.css the selftest
# says so by name; they are not free-floating constants.
CAP_PAD_BLOCK = 12   # padding-block, one 4px rung above the shipped 8 (s217-D3 derivation)
CAP_GAP       = 2    # the gap between description and licence lines, as shipped
CAP_LEGAL     = 12   # .t-cm-legal — 12px, line-height 1
CAP_LINE      = 16   # .t-ed-caption — 12/16


def caption_space():
    """-> (space_px, description_lines). The store's number, and the clamp DERIVED from it."""
    raw = store()["caption-space"]["$value"]
    space = int(float(str(raw).replace("px", "")))
    lines = (space - 2 * CAP_PAD_BLOCK - CAP_GAP - CAP_LEGAL) // CAP_LINE
    if lines < 1:
        raise BentoStoreError(
            "layout/bento/caption-space is %s — too small to hold even one description line "
            "above its licence line; the ruled space and its clamp cannot both be true." % raw)
    return space, lines


def params():
    """{name: value} for the BUILD-TIME halves — bands + span derivation.
    The CSS-valued halves (columns/gutter/padding/row-unit/packing) are NOT read here:
    they reach the stylesheet as `var(--layout-bento-*)`, which is what lets the theme
    cascade override the gutter without this generator knowing the themes exist."""
    b = store()
    bands, spans = b["$bands"], b["$spanDerivation"]
    return {
        "columns": int(b["columns"]["$value"]),
        "band_wide": int(bands["wide"]),
        "band_mid": int(bands["mid"]),
        "band_narrow": int(bands["narrow"]),
        "aspect3": float(spans["aspectThreeColumn"]),
        "aspect2": float(spans["aspectTwoColumn"]),
        "aspect_tall": float(spans["aspectTwoRow"]),
        "emph_every": int(spans["emphasisEvery"]),
        "emph_from": int(spans["emphasisFrom"]),
    }


# ---------------------------------------------------------------- build-time span derivation
def span_for(w, h, p=None):
    """PHOTOGRAPHY ONLY (s217-D2). -> (cols, rows) from the image's own aspect ratio.
    Card spans are authored; do not call this on a card."""
    p = p or params()
    if not w or not h:
        return (1, 1)
    ar = float(w) / float(h)
    if ar >= p["aspect3"]:
        return (3, 1)
    if ar >= p["aspect2"]:
        return (2, 1)
    if (1.0 / ar) >= p["aspect_tall"]:
        return (1, 2)
    return (1, 1)


def emphasise(span, i, p=None):
    """POSITION, not preference. `i` is the 1-based tile index. Every Nth tile from the
    ruled offset is promoted to 2x2 — but only if it is not already taller than one row
    (promoting a `tall` tile would destroy the aspect the derivation just assigned)."""
    p = p or params()
    c, r = span
    if p["emph_every"] <= 0:
        return (c, r)
    if (i - p["emph_from"]) % p["emph_every"] == 0 and r == 1:
        return (2, 2)
    return (c, r)


# ---------------------------------------------------------------- the squaring pass (RATIFIED)
# ✅ RATIFIED s217-D3 for dashboard + brochureware; GALLERY IS EXEMPT. See the module docstring.
SQUARE_CANDIDATES = ((1, 1), (2, 1), (1, 2), (2, 2), (3, 1))


def band_ladder(p=None):
    """The COLUMN COUNTS a wall actually renders at, widest first.

    Derived from the compiled bands, not guessed: the band block rewrites `--bento-cols-now`
    to min(3, columns) / 2 / 1. An instance dialled to fewer columns than canon's default has
    a SHORTER ladder — a 3-column inner bento never renders at 6, so squaring it against 6
    would refuse walls that are perfectly rectangular everywhere they are ever seen."""
    p = p or params()
    out = []
    for c in (int(p["columns"]), min(3, int(p["columns"])), 2, 1):
        if c >= 1 and c not in out:
            out.append(c)
    return tuple(out)


def band_clamp(spans, cols):
    """The spans the COMPILED BAND RULES leave in force at `cols` columns — not the authored
    ones. `data-c` above the band's column count is rewritten to the column count, and at one
    column every `data-r` is rewritten to 1. Simulating the authored spans instead would model
    a layout the browser never renders."""
    return [(min(c, cols), 1 if cols == 1 else r) for (c, r) in spans]


def place(spans, cols):
    """CSS `grid-auto-flow: row dense` auto-placement, simulated.

    -> (rows_used, holes, occupancy). `spans` must already be band-clamped. The cursor resets
    to row 1 for every tile (that is what `dense` means), and the first free rectangle scanning
    rows-then-columns wins — the browser's own order, so this occupancy IS the rendered one."""
    occ = []

    def ensure(r):
        while len(occ) <= r:
            occ.append([False] * cols)

    def fits(r, c, cs, rs):
        for rr in range(r, r + rs):
            ensure(rr)
            row = occ[rr]
            for cc in range(c, c + cs):
                if row[cc]:
                    return False
        return True

    for (cs, rs) in spans:
        cs = max(1, min(cs, cols))
        rs = max(1, rs)
        r = 0
        while True:
            hit = None
            for c in range(0, cols - cs + 1):
                if fits(r, c, cs, rs):
                    hit = c
                    break
            if hit is not None:
                for rr in range(r, r + rs):
                    ensure(rr)
                    for cc in range(hit, hit + cs):
                        occ[rr][cc] = True
                break
            r += 1
    return len(occ), sum(1 for row in occ for v in row if not v), occ


def is_rectangular(spans, ladder=None, p=None):
    """-> (ok, failing_cols, holes). The rectangle test at EVERY band in the ladder."""
    ladder = ladder or band_ladder(p)
    for cols in ladder:
        rows, holes, _ = place(band_clamp(spans, cols), cols)
        if holes:
            return (False, cols, holes)
    return (True, None, 0)


def _square_pool(span):
    """Candidate spans for one tail tile, BEST FIRST. A portrait-derived tile (1 column, 2
    rows) offers its tall candidates first — s217-D2's two-row threshold is the answer to
    Dave's portrait question, and the squaring pass must not quietly undo it."""
    if span == (1, 2):
        return [(1, 2), (2, 2), (1, 1), (2, 1), (3, 1)]
    return [span] + [c for c in SQUARE_CANDIDATES if c != span]


# HOW BADLY A SUBSTITUTION CROPS THE PICTURE. Every re-span puts an image in a compartment its
# aspect did not ask for, and object-fit:cover pays for the difference. The pass minimises this
# total, so it reaches for the cheap swaps first and only makes an expensive one when nothing
# else squares the wall. ⚠ NOT a preference dial: the numbers are ordinal, and their only job is
# to rank substitutions against each other.
_PENALTY_TALL = {(1, 2): 0, (2, 2): 1, (1, 1): 2, (2, 1): 4, (3, 1): 6}
_PENALTY_WIDE = {(1, 1): 1, (2, 2): 1, (2, 1): 1, (3, 1): 2, (1, 2): 4}


def _span_penalty(orig, new):
    """0 for "leave it alone", rising with how much the substitution crops.

    A PORTRAIT laid on its side (1,2) -> (2,1) is the worst thing this pass can do to a
    photograph, and a LANDSCAPE squeezed into a one-column two-row slot is nearly as bad —
    object-fit crops it to a sliver. Both are 4+; the square-ish and wide swaps are 1-2."""
    if orig == new:
        return 0
    table = _PENALTY_TALL if orig == (1, 2) else _PENALTY_WIDE
    return table.get(new, 6)


def square_wall(spans, ladder=None, tail_cap=6, p=None):
    """✅ RATIFIED s217-D3 (dashboard + brochureware). Re-span the LAST tiles so the wall is an exact rectangle
    at every band. Deterministic, mint-time, no JS and no CSS hack.

    -> (spans, report). `report` carries `squared`, `adjusted` (how many tail tiles moved),
    `changed` [(index, before, after)], `rows` {cols: row count} and, on refusal, the band and
    hole count that beat it. ⚠ A caller MUST print a refusal: a wall believed square and
    shipped ragged is the defect recurring with a green banner over it."""
    import itertools
    spans = [tuple(s) for s in spans]
    ladder = ladder or band_ladder(p)
    n = len(spans)
    # ⚠ EXHAUSTIVE, AND SCORED — not first-past-the-post. Every assignment of every tail up to
    # `tail_cap` is tested, and the winner is chosen by an ORDERED cost:
    #     (total crop penalty, tail size k, tiles disturbed, enumeration index).
    # THE PICTURES OUTRANK THE SMALL TAIL — a larger tail that leaves every photograph in a
    # compartment its aspect can live with beats a smaller one that lays a portrait on its side.
    # MEASURED on the 15-tile Foundations wall: first-past-the-post turned two portraits into
    # 2x1 letterboxes at k=3, while k=4 costs less crop overall. A squaring pass that answers
    # Dave's second question by silently undoing his first has fixed nothing.
    # The search stops the moment a zero-penalty answer exists, so the common case is fast.
    best = None                      # (cost, k, trial)
    for k in range(0, min(tail_cap, n) + 1):
        head, tail = spans[:n - k], spans[n - k:]
        for idx, combo in enumerate(itertools.product(*[_square_pool(s) for s in tail])):
            trial = head + list(combo)
            if not is_rectangular(trial, ladder)[0]:
                continue
            crop = sum(_span_penalty(a, b) for a, b in zip(tail, combo))
            moved = sum(1 for a, b in zip(tail, combo) if a != b)
            cost = (crop, k, moved, idx)
            if best is None or cost < best[0]:
                best = (cost, k, trial)
        if best is not None and best[0][0] == 0:
            break
    if best is not None:
        cost, k, trial = best
        changed = [(i, spans[i], trial[i]) for i in range(n) if spans[i] != trial[i]]
        rows = {c: place(band_clamp(trial, c), c)[0] for c in ladder}
        return trial, {"squared": True, "adjusted": k, "changed": changed,
                       "cost": cost, "rows": rows, "ladder": ladder, "reason": None}
    ok, cols, holes = is_rectangular(spans, ladder)
    return spans, {"squared": False, "adjusted": 0, "changed": [],
                   "rows": {c: place(band_clamp(spans, c), c)[0] for c in ladder},
                   "ladder": ladder,
                   "reason": ("no assignment of the last %d tile(s) makes %d tiles rectangular at "
                              "every band — %d hole(s) remain at %d columns"
                              % (min(tail_cap, n), n, holes, cols or ladder[0]))}


def square_wall_for_role(spans, role=None, ladder=None, tail_cap=6, p=None):
    """THE ROLE-AWARE ENTRY POINT (s217-D3) — and the ONLY place a generator should ask whether
    a wall gets squared. `role_policy(role)["squaring"]` decides; gallery is exempt.

    -> (spans, report). An exempt wall is returned UNTOUCHED, with `exempt: True` and its measured
    raggedness reported honestly (`holes`, `at_cols`) rather than hidden. ⚠ `squared` is left TRUE
    for an exempt wall only when it happens to be rectangular anyway — a caller must branch on
    `exempt`, not on `squared`, or it will print a refusal for a wall that was ruled ragged-tolerant."""
    pol = role_policy(role)
    ladder = ladder or band_ladder(p)
    if not pol["squaring"]:
        ok, cols, holes = is_rectangular(spans, ladder)
        return list(spans), {
            "squared": ok, "exempt": True, "role": role or roles()["$default"],
            "adjusted": 0, "changed": [], "ladder": ladder, "holes": holes, "at_cols": cols,
            "rows": {c: place(band_clamp(spans, c), c)[0] for c in ladder},
            "reason": None if ok else
            "RAGGED-TOLERANT by s217-D3 (role=gallery): %d hole(s) at %d columns, and that is "
            "ACCEPTABLE — the requirement is only an appropriate layout for portrait and "
            "landscape images." % (holes, cols or ladder[0])}
    out, rep = square_wall(spans, ladder=ladder, tail_cap=tail_cap, p=p)
    rep["exempt"] = False
    rep["role"] = role or roles()["$default"]
    return out, rep


# ------------------------------------------------------- the squaring pass, NESTED (s217-D7)
def inner_ladder(cols=None, p=None):
    """The COLUMN LADDER a NESTED wall renders at — its OWN column dial, never canon's default.

    An inner bento is dialled to fewer columns than the page default (three, typically), so it
    is never seen at six. Squaring it against six would refuse walls that are exact rectangles
    at every width they are ever rendered at. Ask here; do not hand-build the ladder."""
    p = p or params()
    return band_ladder(p if cols is None else dict(p, columns=int(cols)))


def square_inner_wall(spans, role=None, cols=None, ladder=None, tail_cap=6, p=None):
    """✅ s217-D7 — THE SQUARING PASS FOR A NESTED WALL. Same ratified pass, same role policy,
    run at the INNER instance's ladder rather than the page's.

    -> (spans, report), with `nested: True` and `cols` on the report so a caller printing a
    residual can say WHICH wall refused. Gallery stays exempt (s217-D3/D5) — the policy is read
    from the role, exactly as at the top level, never re-decided here."""
    ladder = ladder or inner_ladder(cols, p)
    out, rep = square_wall_for_role(spans, role, ladder=ladder, tail_cap=tail_cap, p=p)
    rep["nested"] = True
    rep["cols"] = int(cols) if cols is not None else int((p or params())["columns"])
    return out, rep


def square_nested_wall(groups, role=None, outer_spans=None, outer_cols=None, inner_cols=None,
                       tail_cap=6, p=None):
    """✅ s217-D7 — **THE ONE ENTRY POINT FOR A BENTO-OF-BENTOS.** Mints the OUTER wall of group
    tiles AND every INNER wall in a single call, so a consumer cannot square one level and leave
    the other on its authored literals.

    ⛔ WHY ONE CALL AND NOT TWO. The #217 defect was not that the pass was wrong — it was that a
    generator hand-wrote `data-c="1"` and never ASKED. Splitting the two levels across two call
    sites re-creates exactly that opportunity: the outer wall gets squared because it is the one
    Dave's screenshot showed, and the inner walls quietly keep their authored spans. A consumer
    that calls this once has no un-asked level left.

      groups       — a list of inner walls, each a list of that wall's `(cols, rows)` spans.
      outer_spans  — the outer tile span per group; defaults to one cell per group, which is
                     what "the group IS a tile of the outer wall" means.
      outer_cols   — the outer instance's column dial (None = canon's default).
      inner_cols   — the inner instances' column dial: one int for all, or a list per group.

    -> (outer_spans, [inner_spans per group], report). `report` carries `outer`, `inner` (a list
    of reports), `squared` (True only when EVERY level squared or is exempt) and `refusals`, a
    list of named reasons. ⚠ A caller MUST print `refusals` — a nested wall believed square and
    shipped ragged is the #217 defect recurring one level down."""
    groups = [list(g) for g in groups]
    n = len(groups)
    outer_in = [tuple(s) for s in (outer_spans if outer_spans is not None else [(1, 1)] * n)]
    if len(outer_in) != n:
        raise BentoStoreError(
            "square_nested_wall: %d group(s) but %d outer span(s) — the outer wall's tiles ARE "
            "the groups, so the two lists cannot differ." % (n, len(outer_in)))
    if inner_cols is None or isinstance(inner_cols, int):
        icols = [inner_cols] * n
    else:
        icols = list(inner_cols)
        if len(icols) != n:
            raise BentoStoreError(
                "square_nested_wall: %d group(s) but %d inner column dial(s)." % (n, len(icols)))
    out_spans, out_rep = square_wall_for_role(
        outer_in, role, ladder=inner_ladder(outer_cols, p), tail_cap=tail_cap, p=p)
    out_rep["level"] = "outer"
    if not (out_rep.get("squared") or out_rep.get("exempt")):
        out_spans = outer_in       # REFUSED and said why — never silently shipped as squared
    inner_out, inner_reps, refusals = [], [], []
    if not (out_rep.get("squared") or out_rep.get("exempt")):
        refusals.append("outer wall: %s" % out_rep.get("reason"))
    for i, g in enumerate(groups):
        gs, grep = square_inner_wall(g, role, cols=icols[i], tail_cap=tail_cap, p=p)
        grep["level"] = "inner"
        grep["group"] = i + 1
        if not (grep.get("squared") or grep.get("exempt")):
            gs = list(g)
            refusals.append("inner group %d: %s" % (i + 1, grep.get("reason")))
        inner_out.append(gs)
        inner_reps.append(grep)
    return out_spans, inner_out, {"outer": out_rep, "inner": inner_reps,
                                  "squared": not refusals, "refusals": refusals,
                                  "role": out_rep.get("role")}


# ---------------------------------------------------------------- CSS emission
def role_css(p):
    """The `[data-bento-role=…]` block (s217-D3). ROLE IS AN ATTRIBUTE ON THE INSTANCE — no new
    class, no JavaScript, and nothing here reaches a bento that does not name a role."""
    R = roles()
    space, lines = caption_space()
    tight = R["dashboard"]["tightSpacing"]
    L = []
    A = L.append
    A("")
    A("/* ---- ROLES (s217-D3) --------------------------------------------------------------")
    A("   The role decides WHERE THE RADIUS SITS, WHAT THE SPACING IS, and (build-time) whether")
    A("   the squaring pass runs. `data-bento-role` on the instance — an attribute, not a class,")
    A("   so an instance can carry its own dials and its role independently. No JavaScript.")
    A("   ⚠ THE GRAMMAR IS THE SAME IN ALL FOUR THEMES. Console is only where you can SEE it,")
    A("   because its radius token is non-zero; elsewhere the same rules resolve to 0.")
    A("   ⚠ SPECIFICITY: these rules are (0,2,0). A per-instance dial written as a bare class is")
    A("   (0,1,0) and the role would beat it — declare instance dials as `.c-bento.my-wall{…}`.")
    A("   ⛔ THE SQUARING POLICY IS NOT HERE and cannot be: it rewrites spans at mint time.")
    A("   Ask canon/gen_canon_bento.role_policy(role)['squaring']. */")
    A("")
    A("/* DASHBOARD — s217-D2's model. Radius on the CONTAINER, tiles square, tiles at %s. */" % tight)
    A('.c-bento[data-bento-role="dashboard"]{')
    A("  --bento-radius:var(--border-radius-container);")
    A("  --bento-gutter:%s;" % tight)
    A("  overflow:hidden;   /* the clip is what makes the container radius read at all */")
    A("}")
    A("/* ⛔ THERE IS NO `border-radius:0` RULE FOR DASHBOARD TILES, DELIBERATELY, and it took two")
    A("   gates to learn why. Canon gives a tile no radius in the first place, so 'tiles stay")
    A("   square' needs no declaration — and writing one would (a) trip the radius gate, whose")
    A("   whole reason is that a literal `border-radius:0` freezes a component square in every")
    A("   theme (ADR-0010), and (b) out-specify `.c-bento{border-radius:var(--bento-radius)}` for")
    A("   a tile that is ALSO a bento, squaring off exactly the inner containers whose radius IS")
    A("   the dashboard role. MEASURED #217, both ways. */")
    A("/* ⚠ THE OUTER WALL OF A BENTO-OF-BENTOS KEEPS THE THEME GUTTER. Dave's dashboard is tight")
    A("   inner walls inside a generously spaced outer, so `%s everywhere` would collapse exactly" % tight)
    A("   the structure the role exists to describe. The condition is STRUCTURAL, not a second")
    A("   role name: a dashboard whose tiles are themselves bentos IS the outer wall. */")
    A('.c-bento[data-bento-role="dashboard"]:has(> .c-bento__grid > .c-bento){')
    A("  --bento-gutter:var(--layout-bento-gutter);")
    A("}")
    A("")
    A("/* BROCHUREWARE + GALLERY — the TILES carry the radius and the spacing (s217-D3). */")
    A('.c-bento[data-bento-role="brochureware"],')
    A('.c-bento[data-bento-role="gallery"]{')
    A("  --bento-radius:0px;")
    A("  --bento-gutter:var(--layout-bento-gutter);")
    A("  /* ⛔ NO CLIP HERE. With the radius on the tiles there is nothing to clip, and a clip")
    A("     would silently crop anything a tile paints outside its own box. */")
    A("  overflow:visible;")
    A("}")
    A('.c-bento[data-bento-role="brochureware"] > .c-bento__grid > .c-bento__tile,')
    A('.c-bento[data-bento-role="gallery"] > .c-bento__grid > .c-bento__tile{')
    A("  border-radius:var(--border-radius-container);")
    A("  overflow:hidden;   /* the tile is the rounded box now, so the tile does the clipping */")
    A("}")
    A("")
    A("/* GALLERY CAPTION SPACE (s217-D3, ruled 'more generous'). SPACE ONLY — canon declares no")
    A("   face, no size and no colour here; typography is out of scope (s217-D2's not_in_scope).")
    A("   DERIVED AT MINT TIME (s200-D1) from layout/bento/caption-space = %dpx:" % space)
    A("     %d padding-block x2 + %d description line(s) x %d + %d gap + %d licence line = %dpx"
      % (CAP_PAD_BLOCK, lines, CAP_LINE, CAP_GAP, CAP_LEGAL, space))
    A("   The clamp is DERIVED FROM THE SPACE, never carried as a second token, so the two")
    A("   cannot disagree. */")
    A('.c-bento[data-bento-role="gallery"] .c-bento__caption{')
    A("  --bento-caption-space:var(--layout-bento-caption-space);")
    A("  --bento-caption-lines:%d;" % lines)
    A("  min-height:var(--bento-caption-space);")
    A("  padding-block:%dpx;" % CAP_PAD_BLOCK)
    A("  box-sizing:border-box;")
    A("}")
    return L


def bento_css():
    p = params()
    n = p["columns"]
    L = []
    A = L.append
    A(START)
    A("   Generated from knowledge/tokens/layout.json (layout/bento) by canon/gen_canon_bento.py.")
    A("   MINTED s217-D2 (#217, Dave, 2026-08-23) from Dave's four per-theme tuner exports.")
    A("   Do NOT hand-edit between the AUTO-BENTO markers — edit the token store and re-run.")
    A("")
    A("   THE PARAMETER SURFACE is custom properties on the CONTAINER, seeded from the theme-")
    A("   minted token vars. Per-instance values override them, and that is exactly how NESTING")
    A("   carries a different parameter set per level (s217-D2: 'three 1px-gutter bentos inside a")
    A("   40px-gutter outer'). Prefer a DECLARED rule over a style=\"\" attribute: an inline")
    A("   custom property is invisible to every instrument that reads the document, and an")
    A("   inline name beats container queries outright.")
    A("")
    A("   ⚠ TWO NAMES FOR THE COLUMN COUNT, ON PURPOSE. `--bento-columns` is the INSTANCE dial;")
    A("   `--bento-cols-now` is what the grid actually reads and what the bands rewrite. If the")
    A("   bands rewrote the instance dial, a per-instance column count set inline would make")
    A("   every band inert — silently, at one viewport, in one theme. */")
    A(".c-bento{")
    A("  /* every parameter is RE-DECLARED here, never inherited: a nested bento must start from")
    A("     its theme's values, not from whatever its parent bento was tuned to. */")
    A("  --bento-columns:       var(--layout-bento-columns);")
    A("  --bento-gutter:        var(--layout-bento-gutter);        /* THE ONLY per-theme divergence */")
    A("  --bento-outer-padding: var(--layout-bento-outer-padding);")
    A("  --bento-row-unit:      var(--layout-bento-row-unit);")
    A("  --bento-packing:       var(--layout-bento-packing);")
    A("  /* s217-D2: the theme radius sits on the CONTAINER, never the tiles. */")
    A("  --bento-radius:        var(--border-radius-container);")
    A("")
    A("  /* the wall is its own container, so the bands below answer the WALL, not the window —")
    A("     which is also what makes a bento work as a tile of another bento. */")
    A("  container-type:inline-size; container-name:bento;")
    A("  padding:var(--bento-outer-padding);")
    A("  border-radius:var(--bento-radius);")
    A("  /* ⛔ NOT decoration. Without the clip the square tile corners poke through the rounded")
    A("     container edge and the console treatment does not read. Probe the CLIP, not the radius. */")
    A("  overflow:hidden;")
    A("  min-width:0;")
    A("}")
    A(".c-bento__grid{")
    A("  --bento-cols-now:var(--bento-columns);   /* re-declared so a band above cannot inherit down */")
    A("  display:grid;")
    A("  grid-template-columns:repeat(var(--bento-cols-now),minmax(0,1fr));")
    A("  /* ⚠ FIXED rows. With intrinsic rows the tallest content sizes every row and the span")
    A("     vocabulary renders invisible (MEASURED #217, Foundations photography bento). */")
    A("  grid-auto-rows:var(--bento-row-unit);")
    A("  gap:var(--bento-gutter);")
    A("  grid-auto-flow:var(--bento-packing);")
    A("  min-width:0;")
    A("}")
    A("/* THE SPAN VOCABULARY. Child-combinator throughout: `.c-bento__grid .c-bento__tile`")
    A("   would reach a NESTED bento's tiles from the outer grid and re-span them. */")
    A(".c-bento__grid > .c-bento__tile{grid-column:span 1; grid-row:span 1; min-width:0; margin:0;}")
    for i in range(1, n + 1):
        A('.c-bento__grid > .c-bento__tile[data-c="%d"]{grid-column:span %d;}' % (i, i))
    for i in range(1, 4):
        A('.c-bento__grid > .c-bento__tile[data-r="%d"]{grid-row:span %d;}' % (i, i))
    A("/* a bento that is a tile of another bento: both classes, each level with its own dials */")
    A("/* ⛔ THE STRETCH AND THE FILL ARE ONE FIX, AND SHIPPING HALF OF IT IS THE DEFECT.")
    A("   `height:100%` makes a nested bento fill its cell, so a row of groups reads as one band.")
    A("   But its OWN grid has FIXED rows, is top-aligned, and does not grow with it — so the")
    A("   moment two nested bentos in the same row have different natural heights, the shorter")
    A("   one is a rounded container with a DEAD BAND under its last row. The tiles stop, the")
    A("   container carries on: the group reads with a rounded top and a FLAT BOTTOM, and the")
    A("   dead band reads as an orphan gap. MEASURED #217 in the matrix explorer's dashboard —")
    A("   a 360px cell holding a 240px grid — and INVISIBLE in the roles demo, whose nested walls")
    A("   happen to be the same height. So: flex the nested bento, let its grid take the slack,")
    A("   and let the rows grow into it. `minmax(<unit>,1fr)` keeps the row unit as the FLOOR —")
    A("   the fixed-row discipline that makes the span vocabulary visible is untouched, rows only")
    A("   grow when the parent has already stretched the container past its content. */")
    A(".c-bento__tile.c-bento{height:100%; display:flex; flex-direction:column;}")
    A(".c-bento__tile.c-bento > .c-bento__grid{")
    A("  flex:1 1 auto;")
    A("  grid-auto-rows:minmax(var(--bento-row-unit),1fr);")
    A("}")
    A("")
    A("/* RESPONSIVE BANDS — the CONTAINER decides. Concrete literals: a container-query")
    A("   condition cannot read a custom property, so these numbers are compiled from")
    A("   layout/bento/$bands rather than referenced. Dave unified the 800/820 export")
    A("   discrepancy to 820 for all four themes (s217-D2). */")
    for width, cols in ((p["band_wide"], min(3, n)), (p["band_mid"], 2), (p["band_narrow"], 1)):
        A("@container bento (max-width:%dpx){" % width)
        A("  .c-bento__grid{--bento-cols-now:%d;}" % cols)
        over = [i for i in range(1, n + 1) if i > cols]
        if over:
            sel = ", ".join('.c-bento__grid > .c-bento__tile[data-c="%d"]' % i for i in over)
            A("  %s{grid-column:span %d;}" % (sel, cols))
        if cols == 1:
            A('  .c-bento__grid > .c-bento__tile[data-r]{grid-row:span 1;}')
        A("}")
    A("")
    A("/* SPAN DERIVATION is BUILD-TIME, not runtime — canon/gen_canon_bento.py exposes it as")
    A("   span_for(w,h) / emphasise(span,i). ⚠ PHOTOGRAPHY ONLY for the aspect rules:")
    A("     aspect >= %.2f -> %d columns" % (p["aspect3"], 3))
    A("     aspect >= %.2f -> %d columns" % (p["aspect2"], 2))
    A("     inverse aspect >= %.2f -> 2 rows" % p["aspect_tall"])
    A("     otherwise -> 1 x 1")
    A("   then every %dth tile from tile %d is promoted to 2x2 (position, not preference)." % (p["emph_every"], p["emph_from"]))
    A("   CARD SPANS ARE AUTHORED — only the rhythm applies to them (s217-D2). */")
    L.extend(role_css(p))
    A("")
    A("/* SQUARING is a BUILD-TIME policy of the role (s217-D3) and cannot be expressed in CSS —")
    A("   it rewrites data-c/data-r before the wall is written. dashboard: ON · brochureware: ON ·")
    A("   gallery: OFF (ragged-tolerant). Ask role_policy(role)['squaring']. */")
    A(END)
    return "\n".join(L)


def render():
    """The full canon.css text with the AUTO-BENTO block current."""
    existing = open(CANON).read()
    block = bento_css()
    if START in existing and END in existing:
        return re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _m: block, existing, flags=re.S)
    if ANCHOR not in existing:
        raise BentoStoreError("canon.css has no AUTO-COMPONENTS anchor — refusing to guess a home.")
    return existing.replace(ANCHOR, block + "\n\n" + ANCHOR, 1)


def main():
    if "--check" in sys.argv:
        cur = open(CANON).read()
        if cur != render():
            print("AUTO-BENTO block is STALE — re-run gen_canon_bento.py", file=sys.stderr)
            return 1
        print("AUTO-BENTO in sync with tokens/layout.json (layout/bento).")
        return 0
    out = render()
    open(CANON, "w").write(out)
    p = params()
    print("Wrote AUTO-BENTO into %s" % CANON)
    print("  columns=%d  bands=%d/%d/%d  aspect=%.2f/%.2f/%.2f  rhythm=every %d from %d"
          % (p["columns"], p["band_wide"], p["band_mid"], p["band_narrow"],
             p["aspect3"], p["aspect2"], p["aspect_tall"], p["emph_every"], p["emph_from"]))
    print("  gutter/padding/row-unit/packing reach CSS as var(--layout-bento-*) — theme-cascaded.")
    space, lines = caption_space()
    R = roles()
    print("  roles (s217-D3): %s" % " · ".join(
        "%s radius=%s spacing=%s squaring=%s" % (k, v["radius"], v["spacing"],
                                                 "on" if v["squaring"] else "OFF")
        for k, v in R.items() if not k.startswith("$")))
    print("  gallery caption space %dpx -> %d description line(s) DERIVED (s217-D3 + s200-D1)"
          % (space, lines))
    return 0


def selftest():
    """9 bites: store · photography derivation · rhythm · nesting scope · band literals ·
    placement simulator · rectangle test · squaring pass (incl. its named refusal) · ladder."""
    p = params()
    assert p["columns"] == 6 and (p["band_wide"], p["band_mid"], p["band_narrow"]) == (1100, 820, 520), \
        "bite 1 FAIL: store does not carry s217-D2's parameters — %r" % p
    assert span_for(1600, 200, p) == (3, 1), "bite 2a FAIL: 8:1 should span 3 columns"
    assert span_for(1600, 500, p) == (2, 1), "bite 2b FAIL: 3.2:1 should span 2 columns"
    assert span_for(1000, 1600, p) == (1, 2), "bite 2c FAIL: portrait should span 2 rows"
    assert span_for(1600, 1067, p) == (1, 1), "bite 2d FAIL: 1.5:1 is below the 2.6 threshold"
    assert span_for(None, None, p) == (1, 1), "bite 2e FAIL: unknown dimensions must not crash"
    assert emphasise((1, 1), 1, p) == (2, 2), "bite 3a FAIL: tile 1 is the first promotion"
    assert emphasise((1, 1), 7, p) == (2, 2), "bite 3b FAIL: every 6th from 1 -> 7"
    assert emphasise((1, 1), 4, p) == (1, 1), "bite 3c FAIL: tile 4 is not on the rhythm"
    assert emphasise((1, 2), 7, p) == (1, 2), "bite 3d FAIL: a tall tile keeps its derived aspect"
    css = bento_css()
    assert ".c-bento__grid > .c-bento__tile" in css and ".c-bento__grid .c-bento__tile{" not in css, \
        "bite 4 FAIL: a descendant-scoped span rule would re-span a NESTED bento's tiles"
    assert "@container bento (max-width:820px)" in css, "bite 5a FAIL: 820 band not compiled"
    assert "var(--bento-columns)" in css and "--bento-cols-now:3" in css, "bite 5b FAIL: band/instance dials conflated"
    assert "overflow:hidden" in css and "var(--border-radius-container)" in css, \
        "bite 5c FAIL: container radius or its clip missing (s217-D2)"
    # --- bite 6: the placement simulator reproduces `dense`, including the back-fill ----------
    rows, holes, _ = place([(2, 2), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1)], 3)
    assert (rows, holes) == (3, 0), \
        "bite 6a FAIL: dense back-fill not simulated — the 1x1s must fill the column BESIDE the " \
        "2x2, not queue below it (got rows=%d holes=%d)" % (rows, holes)
    rows, holes, _ = place([(1, 2), (1, 1)], 3)
    assert (rows, holes) == (2, 3), \
        "bite 6b FAIL: a hanging tall tile must leave holes beside it — rows=%d holes=%d" % (rows, holes)
    assert band_clamp([(6, 2)], 2) == [(2, 2)] and band_clamp([(6, 2)], 1) == [(1, 1)], \
        "bite 6c FAIL: band clamping must model what the COMPILED band rules leave in force"

    # --- bite 7: the rectangle test must be able to FAIL, and at the right band --------------
    ok, cols, holes = is_rectangular([(1, 1)] * 7, (6, 3, 2, 1), p)
    assert not ok and holes > 0, "bite 7a FAIL: seven 1x1 tiles at six columns are NOT a rectangle"
    ok, _, _ = is_rectangular([(1, 1)] * 6, (6, 3, 2, 1), p)
    assert ok, "bite 7b FAIL: six 1x1 tiles at six columns ARE a rectangle at every band"
    ok, cols, _ = is_rectangular([(2, 1)] * 3, (6, 3, 2, 1), p)
    assert not ok and cols == 3, \
        "bite 7c FAIL: three 2-wide tiles are square at 6 and ragged at 3 — the test must catch " \
        "the NARROW band, or the defect just moves (got ok=%s cols=%s)" % (ok, cols)

    # --- bite 8: the squaring pass — squares, keeps portraits tall, refuses BY NAME ----------
    derived = [emphasise(span_for(1600, 1067, p), i, p) for i in range(1, 15)]
    assert not is_rectangular(derived, (6, 3, 2, 1), p)[0], \
        "bite 8a FAIL: the 14-tile fixture must be ragged BEFORE the pass or it proves nothing"
    squared, rep = square_wall(derived, (6, 3, 2, 1), p=p)
    assert rep["squared"] and is_rectangular(squared, (6, 3, 2, 1), p)[0], \
        "bite 8b FAIL: the pass did not square a 14-tile wall — %r" % rep["reason"]
    assert squared[:len(squared) - rep["adjusted"]] == derived[:len(derived) - rep["adjusted"]], \
        "bite 8c FAIL: the pass moved a tile that is NOT in the tail"
    again, rep2 = square_wall(derived, (6, 3, 2, 1), p=p)
    assert again == squared and rep2["adjusted"] == rep["adjusted"], \
        "bite 8d FAIL: the pass is not deterministic — same wall, two answers"
    tall = [emphasise(span_for(1065, 1600, p), i, p) for i in range(2, 14)]
    assert tall.count((1, 2)) == len(tall), "bite 8e FAIL: portrait fixture is not all two-row"
    st, rt = square_wall(tall, (6, 3, 2, 1), p=p)
    assert rt["squared"] and st.count((1, 2)) >= len(tall) - rt["adjusted"], \
        "bite 8f FAIL: the pass demoted portraits it did not have to — %r" % st
    _, r3 = square_wall([(1, 1)] * 3, (6, 3, 2, 1), p=p)
    assert not r3["squared"] and "hole" in (r3["reason"] or ""), \
        "bite 8g FAIL: three tiles at six columns CANNOT square — the refusal must be named, " \
        "not a silently ragged wall (%r)" % r3

    # --- bite 9: the ladder follows the INSTANCE, not canon's default ------------------------
    assert band_ladder(p) == (6, 3, 2, 1), "bite 9a FAIL: default ladder is not 6/3/2/1"
    assert band_ladder(dict(p, columns=3)) == (3, 2, 1), \
        "bite 9b FAIL: a 3-column instance never renders at 6 — squaring it against 6 would " \
        "refuse walls that are rectangular everywhere they are ever seen"

    # --- bite 10: THE ROLES (s217-D3) — policy table, refusal, and the compiled rules ---------
    assert role_policy("dashboard")["radius"] == "container", \
        "bite 10a FAIL: dashboard must put the radius on the CONTAINER (s217-D3)"
    assert role_policy("brochureware")["radius"] == "tile" and \
        role_policy("gallery")["radius"] == "tile", \
        "bite 10b FAIL: brochureware and gallery put the radius on the TILES (s217-D3)"
    assert role_policy("dashboard")["squaring"] and role_policy("brochureware")["squaring"], \
        "bite 10c FAIL: s217-D3 RATIFIED the squaring pass for dashboard and brochureware"
    assert not role_policy("gallery")["squaring"], \
        "bite 10d FAIL: gallery is RAGGED-TOLERANT — squaring it would enforce a rule Dave " \
        "exempted it from in the same breath he ratified it"
    assert role_policy(None)["radius"] == role_policy("dashboard")["radius"], \
        "bite 10e FAIL: the default role is not dashboard"
    try:
        role_policy("dashbored")
        raise AssertionError("bite 10f FAIL: a misspelt role fell back to the default instead of "
                             "refusing — a typo that renders as `dashboard` is undetectable")
    except BentoStoreError:
        pass
    assert '.c-bento[data-bento-role="dashboard"]{' in css and \
           '.c-bento[data-bento-role="gallery"] > .c-bento__grid > .c-bento__tile' in css, \
        "bite 10g FAIL: the role rules did not compile into canon"
    assert '.c-bento[data-bento-role="dashboard"]:has(> .c-bento__grid > .c-bento){' in css, \
        "bite 10h FAIL: no outer-wall carve-out — a dashboard whose tiles are BENTOS would take " \
        "the 1px inner spacing on its outer wall and Dave's bento-of-bentos would collapse"
    # the tile-radius rules must be CHILD-scoped, or an outer brochureware would round a nested
    # bento's tiles through it
    import re as _re
    for sel, _d in _re.findall(r"([^{}\n]*data-bento-role[^{}]*)\{([^{}]*)\}", css):
        if "c-bento__tile" in sel:
            assert "> .c-bento__grid > .c-bento__tile" in sel, \
                "bite 10i FAIL: %r reaches tiles by descent — it would re-style a NESTED " \
                "bento's tiles from the outer wall" % sel.strip()

    # ⚠ STATED AS AN ABSENCE, ON PURPOSE. Canon gives a tile no radius, so the dashboard's
    # "tiles stay square" needs no rule — and a literal `border-radius:0` here would both trip
    # the radius gate (ADR-0010: a literal 0 freezes a component square in every theme) and
    # out-specify the container radius on a tile that is ALSO a bento, squaring off the inner
    # walls the role exists to round. Both were MEASURED at #217.
    for _sel, _decls in _re.findall(r"([^{}\n]*data-bento-role[^{}]*)\{([^{}]*)\}", css):
        if "c-bento__tile" in _sel:
            assert "border-radius:0" not in _decls.replace(" ", ""), \
                "bite 10i2 FAIL: %r squares a tile with a LITERAL radius. Canon already gives " \
                "tiles no radius; the literal only adds a gate red and a cascade trap." % _sel.strip()

    # --- bite 10j: EVERY COMMENT IN THE EMITTED BLOCK CLOSES ---------------------------------
    # MEASURED #217, and it cost a probe run: a single `/*` emitted without its `*/` swallowed
    # the next TWO declarations — `--bento-radius` and `--bento-gutter:1px` — and the stylesheet
    # still PARSED. Nothing was invalid, nothing warned, the dashboard role simply had no
    # spacing and no radius, in all four themes. A generator that writes comments by hand needs
    # a gate on the comments, not care ([[gate-dont-patch]]).
    depth, i = 0, 0
    while i < len(css) - 1:
        if css[i:i + 2] == "/*":
            depth += 1
            i += 2
            continue
        if css[i:i + 2] == "*/":
            depth -= 1
            assert depth >= 0, "bite 10j FAIL: a stray `*/` at offset %d in the emitted block" % i
            i += 2
            continue
        i += 1
    assert depth == 0, \
        "bite 10j FAIL: %d comment(s) in the emitted AUTO-BENTO block were opened and never " \
        "closed. An unterminated `/*` swallows the declarations that follow it and the " \
        "stylesheet still parses — the rule simply is not there, silently, in every theme." % depth

    # --- bite 11: the caption space, and the clamp DERIVED from it ---------------------------
    space, lines = caption_space()
    assert space == 86 and lines == 3, \
        "bite 11a FAIL: s217-D3's caption space is 86px -> 3 description lines; got %r/%r" \
        % (space, lines)
    assert space > 62, \
        "bite 11b FAIL: the ruled space (%d) is not MORE GENEROUS than the 62px shipped" % space
    assert "var(--layout-bento-caption-space)" in css and "--bento-caption-lines:3" in css, \
        "bite 11c FAIL: the caption space did not reach canon, or the clamp was not derived"
    assert 'data-bento-role="gallery"] .c-bento__caption' in css and \
        "font-size" not in css.split("c-bento__caption", 1)[1].split("}", 1)[0], \
        "bite 11d FAIL: the caption rule declares a TYPE property — s217-D3 rules the SPACE " \
        "only; typography is out of scope"

    # --- bite 12: role-aware squaring — gallery exempt, and the exemption REPORTED ------------
    rag = [(1, 1)] * 7
    _, dash = square_wall_for_role(rag, "dashboard", (6, 3, 2, 1), p=p)
    assert dash["squared"] and not dash["exempt"], \
        "bite 12a FAIL: dashboard must be squared (s217-D3 ratified it)"
    out, gal = square_wall_for_role(rag, "gallery", (6, 3, 2, 1), p=p)
    assert gal["exempt"] and out == rag, \
        "bite 12b FAIL: a gallery wall was re-spanned — the exemption is not being honoured"
    assert "RAGGED-TOLERANT" in (gal["reason"] or ""), \
        "bite 12c FAIL: an exempt ragged wall must report its raggedness as ACCEPTABLE by name, " \
        "not stay silent (%r)" % gal["reason"]
    # ⚠ EXEMPT FROM SQUARING IS NOT EXEMPT FROM THE ASPECT MAPPING — different mechanisms.
    assert span_for(1000, 1600, p) == (1, 2), \
        "bite 12d FAIL: the portrait two-row mapping moved — gallery's squaring exemption must " \
        "not disable s217-D2's aspect derivation, they are DIFFERENT MECHANISMS"

    # --- bite 13: s217-D7 — THE NESTED PASS, and the class fix that makes it unskippable -------
    # The measured #217 case, one level down: three cards (2x1, 1x1, 1x1) in a three-column inner
    # wall leave the second row two-thirds empty. This is the assertion that the inner level is
    # ASKED at all.
    orphan = [(2, 1), (1, 1), (1, 1)]
    ok3, cols3, holes3 = is_rectangular(orphan, inner_ladder(3, p), p)
    assert not ok3 and holes3 == 2 and cols3 == 3, \
        "bite 13a FAIL: the measured inner-group orphan (2x1,1x1,1x1 at 3 columns) no longer " \
        "reads as 2 holes — got ok=%r cols=%r holes=%r; the mutation this pass exists to fix " \
        "must be reproducible or the bite proves nothing" % (ok3, cols3, holes3)
    fixed, rep13 = square_inner_wall(orphan, "dashboard", cols=3, p=p)
    assert rep13["squared"] and not rep13["exempt"] and rep13["nested"] and rep13["cols"] == 3, \
        "bite 13b FAIL: square_inner_wall did not square the measured orphan (%r)" % rep13
    assert is_rectangular(fixed, inner_ladder(3, p), p)[0], \
        "bite 13c FAIL: the squared inner wall %r is still ragged at its own ladder" % (fixed,)
    # ⚠ THE INNER LADDER IS THE INNER INSTANCE'S, NOT THE PAGE'S. A three-column inner bento is
    # never rendered at six, and squaring it against six would refuse a perfectly good wall.
    assert 6 not in inner_ladder(3, p) and inner_ladder(3, p)[0] == 3, \
        "bite 13d FAIL: a 3-column inner wall was given canon's default ladder %r" \
        % (inner_ladder(3, p),)
    # THE ONE ENTRY POINT: both levels minted in a single call, and the outer wall squared too.
    o, inn, nrep = square_nested_wall([orphan, [(2, 2), (1, 1), (1, 1)], orphan],
                                      "dashboard", outer_cols=2, inner_cols=3, p=p)
    assert nrep["squared"] and not nrep["refusals"], \
        "bite 13e FAIL: square_nested_wall refused the demo shape — %r" % nrep["refusals"]
    assert is_rectangular(o, inner_ladder(2, p), p)[0], \
        "bite 13f FAIL: the OUTER wall of the bento-of-bentos is ragged (%r)" % (o,)
    for i, gs in enumerate(inn):
        assert is_rectangular(gs, inner_ladder(3, p), p)[0], \
            "bite 13g FAIL: inner group %d is ragged at its own ladder (%r) — s217-D7 rules the " \
            "pass runs on nested walls" % (i + 1, gs)
    # GALLERY STAYS EXEMPT ONE LEVEL DOWN TOO (s217-D3/D5). The exemption is a ROLE POLICY, and a
    # nested wall must not acquire squaring merely by being nested.
    gout, grep13 = square_inner_wall(orphan, "gallery", cols=3, p=p)
    assert grep13["exempt"] and gout == orphan, \
        "bite 13h FAIL: a nested GALLERY wall was re-spanned — s217-D7 extends the pass to inner " \
        "walls, it does not revoke the gallery exemption"

    print("gen_canon_bento selftest OK (13 bites: store · photography spans · rhythm · nesting "
          "scope · bands · placement sim · rectangle test · squaring pass + named refusal · "
          "ladder · roles + refusal + child scoping · caption space + derived clamp · "
          "role-aware squaring with the gallery exemption · s217-D7 NESTED squaring + the "
          "one-call entry point)")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        sys.exit(main())
