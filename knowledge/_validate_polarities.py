#!/usr/bin/env python3
"""
_validate_polarities.py — THE POLARITY GATE (s238-D7): five refusals in the build and at the
commit seam, a derivation of the polarity status / edges / defaults declaration, and the ONLY
sanctioned writer for the polarity home.

THE HOME (s238-D1, declared #238-P — the P1 plan names no path, so it is `knowledge/brain/`):
  knowledge/brain/principles.json   the R1 register, seeded byte-for-byte (grades A/B/C/D/L; the
                                    s237-D1 names are DERIVED here, never re-typed there)
  knowledge/brain/polarities.json   the 30 polarity nodes — N typed parties, typed out-links
  knowledge/brain/stubs.json        declared stubs: a party that is a phrase, not a register node
  knowledge/brain/schema/polarity.schema.json   the consumer's grammar — READ by this gate,
                                    PINNED by sha256 and by the floors below (#239 lane F)
  knowledge/brain/_generated/       polarity-status.json · polarity-edges.json ·
                                    defaults-declaration.txt — GENERATED, content-fresh-checked

THE FIVE REFUSALS (s238-D7), each LOUD, NAMED, rc != 0, NOTHING WRITTEN:
  R1  a party or link ref that does not resolve against the LIVE registers
      (R1-DANGLING — nothing there, or (#239) a resolvedBy whose target's status text says
       OPEN / PARKED / DEFERRED / FORKED · R1-SUPERSEDED — the `superseded_by` field or (#239)
       supersession written in the store's prose · R1-SELF-PARTY · R1-CIRCULAR ·
       R1-WRONG-REGISTER · R1-UNDECLARED-STUB)
  R2  an untyped link (R2-UNTYPED — key absent, null, or a link that is not an object ·
      R2-UNKNOWN-TYPE — a fifth type is NOT ruled, refused)
  R3  a judgement text field of any name on a node — the only judgement is a typed link to a
      knowledge/_rulings.json id (R3-JUDGEMENT-FIELD — also (#239) a note / mediating_variable /
      stub phrase that is not VERBATIM in the frozen register, and free text at the top level ·
      R3-QUOTE-TOO-LONG · R3-NOTE-TOO-LONG · R3-QUOTE-NOT-VERBATIM — also (#239) an empty,
      under-floor or UNVERIFIABLE quote · R3-QUOTE-MISSING — (#239) a resolvedBy with no quote)
  R4  an authored edge file — pairwise edges exist only under _generated/ with a content-
      freshness check (R4-RETIRED-GENERATED — (#242, s240-D3) a node carrying `retiredBy` whose id
      still appears in a file under _generated/ · R4-AUTHORED-GENERATED — also (#239) a clock that is not ISO-8601 UTC, in
      the future, before the R1 asset, or differing across the three files · R4-AUTHORED-EDGES ·
      R4-STRAY-FILE — (#239) every entry at every level is listed: dotfiles, schema/, _generated/,
      __pycache__, *.tmp, symlinks, a file where a directory should be)
  R5  a typed status (R5-TYPED-STATUS) — status is DERIVED with a clock (s238-D3, s237-D9)
Plus the schema refusals the same grammar implies (S-PARSE · S-SHAPE · S-ID · S-MIN-PARTIES ·
S-ROLE · S-DUP-ID · S-DUP-PARTY · S-STUB-SHAPE · S-DUP-STUB · S-ONE-SIDED · S-SCHEMA ·
S-FORMAT-CHAR · S-SOURCE · S-RECEIPT · SCHEMA-PIN-MISMATCH · SCHEMA-LOOSENED ·
SCHEMA-KEYWORD-UNSUPPORTED) and the freshness verdicts (MISSING-GENERATED · STALE-GENERATED,
remedy: --write). A CRASH IS NOT A FAIL: any exception inside the gate is caught and NAMED
(S-SHAPE, with the exception class and the JSON path it was walking) — the build and the seam
promise "the refusal is NAMED above", and it is.

#239 LANE F — THE CLASSES V FOUND, CLOSED (V = notes/_subreports/2026-09-02-238-V-polarity-verifier.md):
  Q1  "live" for R1 is more than one field: a resolvedBy to a ruling superseded in PROSE, or
      whose status says OPEN/PARKED/DEFERRED/FORKED, is refused (V's (b); (c) a machine `state`
      field in the store is RULING-SHAPED and not built here).
  Q2  the schema is PINNED: its sha256 (SCHEMA_SHA256) and the floors of the five refusals
      (SCHEMA_FLOORS) live in code; a schema that loosens a floor is refused AND the floor is
      applied regardless; a schema may only tighten.
  Q3  the quote oracle is not the node's to name: sources[].path must be on SOURCE_ALLOW (the
      frozen R1 register), sources[].id must be a row in it, every frozen row is claimed by
      exactly one node (the migration receipt, verified), and a resolvedBy needs a VERIFIED quote.
  Q4  the clock is checked: ISO-8601 UTC, not in the future (skew CLOCK_SKEW_S), not before the
      R1 asset's date, identical across the three derived files.
  Q5  free text is bounded and verified: note / mediating_variable / stub phrase verbatim from
      the frozen register; $description and $migration shape-fixed; sources[].id/path patterned;
      any Unicode Cf/Cc/Co character in any string refused (S-FORMAT-CHAR); words are counted
      with those characters as separators.
  Q6  the home is a closed directory at EVERY level: dotfiles, schema/, _generated/, __pycache__,
      *.tmp and symlinks are listed and refused; `.DS_Store` is ignored ONLY when its bytes carry
      the Finder magic (a JSON file wearing that name is refused).
  Q7  crashes are named (S-SHAPE catch-all, S-PARSE on a bad byte, hash-guarded memberships).
  Q8  the two hatches: an absent home in the SOURCE repo (knowledge/_rulings.json present) is
      a refusal (rc 1), not COULD-NOT-ASK; 77 stays for a shipped pack (no store, no home). The
      seam's POLARITY_BRAIN_DIR redirect is DECLARED and the tree's own home is gated too.
  argv the flags are a contract: --dry-run with --write, or --check with --write, is rc 2.

#242 LANE P — THE RECEIPT WIDENS (s240-D3, Dave, 2026-09-02). The quote rule stands (every polarity
traces to something Dave ruled); the ANCHOR may be an R1 register row OR a knowledge/_rulings.json
id, and it is ONE POINTER PER NODE:
  `sources`    the migration's form — a frozen R1 register row (allow-list + bijection, Q3 #239)
  `$seed`      a node BORN AFTER R1 — the ruling id that created it (the R1 alternative, not its
               companion: BOTH is S-SOURCE, NEITHER is S-SOURCE, an id not in the store is
               R1-DANGLING). `sources` therefore leaves the schema's `required`; the floor moves
               into code (check_receipt), so nothing is loosened.
  `retiredBy`  a node RETIRED — the ruling id that retired it. The node KEEPS its row (so no frozen
               row is orphaned) and DROPS OUT of everything generated: derive() never sees it, and
               a retired id still present under _generated/ is R4-RETIRED-GENERATED.
This is the legal form lane F (#239) found missing for a NEW or a RETIRED polarity — its RULING-
SHAPED 4. Retirement is ADDITIVE to the birth receipt, not a second one (declared, #242-P).

#242 LANE P2 — the two gaps the adversarial verifier (V2) drove, closed:
  DROPS OUT = EVERY BYTE, not every row. `delta_vs_237T.cause` was a hardcoded literal naming
              pl-22 and pl-02 whether or not they were live, so a retired node stayed in
              polarity-status.json with the gate GREEN — and the selftest CERTIFIED it. The prose
              is now DERIVED from the live rows (delta_cause()), the leak check scans the whole
              file (id_in_raw_text()), and the arm is re-pointed: a retired id ANYWHERE under
              _generated/ is R4-RETIRED-GENERATED. With nothing retired the bytes do not move.
  THE WIDENING IS FLOORED. Re-adding `sources` to the schema's `required` reads as a TIGHTENING
              (the superset floor passes) and silently makes every `$seed` node S-SCHEMA. The new
              `excludes` floor kind pins it: a schema may tighten a REFUSAL, never a PERMISSION.

#243 LANE Q — THE SIX CONTROLS ARE PERMANENT (s243-D1, Dave, 2026-09-03). #239 Q3 STANDS: a node
may not name its own oracle. Lane F's six green controls in the LITERAL shape (100, 225, 248, 321,
326, and 235's invented phrase) are CORRECTLY refused and stay red; their s240-D3 legal forms — the
receipt is the ruling id (`$seed`) that made the node, or rows are RETIRED (`retiredBy`) rather than
deleted — are named GREEN arms in --selftest, each PAIRED with its literal shape as a RED arm by
refusal name. Shapes are lane P's (#242) verbatim; nothing reinvented. Out of scope: 241/243/245/301.

DERIVED, WITH A CLOCK (s238-D3): every generated file carries `generated_at` and a
`content_sha256` over its body. `--check` re-derives with the ON-DISK clock and compares BYTES
(never mtime — the `index_freshness_check` discipline); a file lacking the header or failing its
own sha was HAND-WRITTEN and is refused as R4, which is a different verdict from STALE.
The status rules are a port of 237-T's `_derive_sort.py` (R-OBLIGATION first, then R-RESOLVED,
then R-OPEN); the open rows' RULE K / RULE D fields are COPIED from 237-T's open-tensions.json
and stay FLOATED. The `Defaults used:` declaration follows s238-D5: declared ONLY when a default
bent away from the conservative side; the T asset carries no per-row conservative marker, so the
rule is printed and every row is UNPROVEN (nothing is declared).

THE WRITER (`--add-polarity FILE` / `--add-stub FILE`) is TEXTUAL and PROVEN BY RECONSTRUCTION,
as `_inscribe_ruling.py` does: removing the inserted span must give back the original bytes,
the result must parse to exactly one more entry equal to the one submitted, and the whole gate
must pass on the resulting text BEFORE a byte is written. A refusal leaves every file untouched.

CONSUMERS (a gate without a consumer is not a gate — s238-D7's last sentence):
  knowledge/_build_all.py STEPS      `--check` (GATE) and `--selftest` (ABORT), appended
  knowledge/_git_commit.sh           `--check` before staging (POLARITY_ACK declares a gap;
                                     POLARITY_BRAIN_DIR is DECLARED and the tree's home still gated)
  knowledge/_test_git_commit.py      the seam harness stubs + drives this gate's line

Usage:
  python3 knowledge/_validate_polarities.py --check                 # the gate (build + commit seam)
  python3 knowledge/_validate_polarities.py --write                 # refusals, then (re)generate
  python3 knowledge/_validate_polarities.py --selftest              # control + every refusal arm,
                                                                    #   on a copy of the REAL rows
  python3 knowledge/_validate_polarities.py --add-polarity e.json --dry-run|--write
  python3 knowledge/_validate_polarities.py --add-stub s.json --dry-run|--write
  ... --brain DIR   (or env POLARITY_BRAIN_DIR)  point at another home (fixtures, selftest)
Exit: 0 pass · 1 refusal/failure · 2 argv · 77 COULD-NOT-ASK (an input outside this tree).
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import copy
import datetime
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import traceback
import unicodedata

import _could_not_ask as cna  # noqa: E402 - after the help gate's path insert

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DEFAULT_BRAIN = os.path.join(HERE, "brain")
RULINGS = os.path.join(HERE, "_rulings.json")
OPEN_DEFAULTS_REL = "notes/_subreports/assets/2026-09-02-237-T-tensions-schema/open-tensions.json"
OPEN_DEFAULTS = os.path.join(REPO, OPEN_DEFAULTS_REL)
T_SORT_FIGURE = ("6 · 3 · 21", "notes/_subreports/assets/2026-09-02-237-T-tensions-schema/tension-sort.json")

# s240-D3 (#242 lane P2, closing V2's finding 3): `delta_vs_237T.cause` WAS a hardcoded string that
# named pl-22 and pl-02 whether or not they were live — so retiring them left their ids in
# polarity-status.json while the gate stayed GREEN, and the ruling's own words ("drops out of
# EVERYTHING generated from the KG") were not literally true. The prose is now DERIVED: each clause
# is keyed by the node it is about and is emitted ONLY while that node is live, and the r1 id in it
# is a LOOKUP against the derived row, not a re-typed literal (s234-D1: generation, never copy).
# ⚠ WITH BOTH NODES LIVE THE JOINED TEXT IS BYTE-IDENTICAL TO THE OLD LITERAL — the three generated
# files do not move, which is the probe that this is a de-hardcoding and not a content edit.
DELTA_CLAUSES = (
    ("pl-22", "{id} ({r1}) carries resolvedBy s217-D8, whose id sat in apollo_touch (237-T "
              "finding 2: a genuine resolution whose id sits in the wrong field)."),
    ("pl-02", "{id}'s s217-D5 is typed `touches` (UNPROVEN — see the migration receipt)"),
)
DELTA_FIGURE = ("the 6 · 9 · 15 figure quoted in s238-D6 — the naive variant that would have closed "
                "four rows wrongly — is not reproduced, by design.")

# Q3 (#239): THE SOURCE ALLOW-LIST — where a node's words may come from. Today the frozen R1
# register only (ADR-0017); a second register is RULING-SHAPED (Dave's), not this file's.
R1_TENSIONS_REL = "notes/_subreports/assets/2026-09-02-236-R1-principles-survey/tensions.json"
SOURCE_ALLOW = (R1_TENSIONS_REL,)

HOME_FILES = ("principles.json", "polarities.json", "stubs.json")
SCHEMA_NAME = "polarity.schema.json"
SCHEMA_REL = os.path.join("schema", SCHEMA_NAME)
GEN_DIR = "_generated"
GEN_FILES = ("polarity-status.json", "polarity-edges.json", "defaults-declaration.txt")
GEN_HEADER = "GENERATED — do not hand-edit (knowledge/_validate_polarities.py --write)"
ALLOWED_TOP = set(HOME_FILES) | {"schema", GEN_DIR}
TOP_KEYS = ("$description", "$migration", "polarities")
MIGRATION_KEYS = ("from", "sha256", "by", "receipts")
DSSTORE_MAGIC = b"\x00\x00\x00\x01Bud1"     # Finder's own file, gitignored — ignored ONLY by its bytes

# FLOATED figures (#239 lane F, declared in the report; Dave's to move):
DESCRIPTION_MAX_WORDS = 120   # polarities.json $description (the real one is 100 words)
RECEIPT_MAX_WORDS = 60        # each $migration.receipts[] line (the real longest is ~45)
CLOCK_FMT = "%Y-%m-%dT%H:%M:%SZ"
CLOCK_SKEW_S = 3600           # a generated_at this far ahead of now is a hand edit (V's Q4)

# s237-D1 — the five grade names. DERIVED from the ruling id quoted here; principles.json keeps
# the R1 letters and is never re-typed (s234-D1: generation chain, never copy chain).
GRADE_NAMES = {"A": "REPLICATED", "B": "STUDIED", "C": "PRACTISED", "D": "DEBUNKED", "L": "OBLIGATION"}
OBLIGATION_GRADE = "L"

STUB_ID = re.compile(r"^st-[a-z0-9]+(?:-[a-z0-9]+)*$")
ASCII_ID_PAT = r"^[A-Za-z0-9][A-Za-z0-9._-]*$"
ASCII_ID = re.compile(ASCII_ID_PAT)
POLARITY_ID_PAT = r"^pl-[0-9]{2,}$"
POLARITY_ID = re.compile(POLARITY_ID_PAT)
SOURCE_PATH_PAT = r"^[A-Za-z0-9_][A-Za-z0-9_./-]*$"
LINK_TYPES = ("resolvedBy", "explainedBy", "challengedBy", "touches")
ROLES = ("side_a", "side_b", "side_c")
NOT_LIVE = re.compile(r"\b(OPEN|PARKED|DEFERRED|FORKED)\b", re.I)
SEP_CATEGORIES = {"Cf", "Cc", "Zs", "Zl", "Zp"}        # word separators for words()
BAD_CATEGORIES = {"Cf", "Co"}                          # + Cc except \t \n \r: refused in any string

SCHEMA_KEYWORDS = {"$schema", "$id", "title", "description", "type", "additionalProperties",
                   "required", "properties", "items", "enum", "pattern", "minItems", "minLength",
                   "maxWords", "minWords", "x-refusals", "x-vocabulary"}

# Q2 (#239): THE PIN. sha256 of knowledge/brain/schema/polarity.schema.json — a schema edit must
# move this constant in the same commit (V's Q2 (b)); SCHEMA_FLOORS below is (c).
SCHEMA_SHA256 = "c2c165ac126d878d8cb9d8548ac1fba2d765724667bf410dfbcca611372243e4"
# THE FLOORS: (pointer into the schema, keyword, kind, floor). kind: min = the schema's value must
# be >= floor · max = <= floor · eq = == floor · keys = `properties` has EXACTLY these keys ·
# superset = `required` carries at least these · excludes = `required` carries NONE of these (the
# floor on a PERMISSION — #242 lane P2, V2's finding 4). A looser schema is SCHEMA-LOOSENED and the
# floor is applied to the data regardless; a tighter one is honoured (the schema still drives the
# check) — EXCEPT a "tightening" that would legislate away a permission the ruling granted, which
# `excludes` pins: #239's whole point was that a schema edit cannot move a refusal, and s240-D3's
# `$seed` needs the same protection in the other direction.
SCHEMA_FLOORS = (
    ("", "type", "eq", "object"),
    ("", "additionalProperties", "eq", False),
    # s240-D3 (#242): `sources` leaves `required` because a node born after R1 carries `$seed`
    # instead. The floor does NOT weaken: EXACTLY ONE of {sources, $seed} is enforced in code
    # (check_receipt) — one pointer per node — so "neither" and "both" are still refusals.
    ("", "required", "superset", ["id", "parties", "mediating_variable", "links"]),
    # …and it CANNOT COME BACK by a schema edit (#242 lane P2, V2 finding 4): re-adding `sources`
    # to `required` reads as a TIGHTENING, passes the superset floor, and silently makes every
    # `$seed` node S-SCHEMA — the permission s240-D3 granted, legislated away in one word.
    ("", "required", "excludes", ["sources"]),
    ("", "properties", "keys", ["id", "parties", "mediating_variable", "links", "sources",
                                "$seed", "retiredBy"]),
    ("properties.$seed", "type", "eq", "string"),
    ("properties.$seed", "pattern", "eq", ASCII_ID_PAT),
    ("properties.$seed", "maxWords", "max", 1),
    ("properties.retiredBy", "type", "eq", "string"),
    ("properties.retiredBy", "pattern", "eq", ASCII_ID_PAT),
    ("properties.retiredBy", "maxWords", "max", 1),
    ("properties.id", "type", "eq", "string"),
    ("properties.id", "pattern", "eq", POLARITY_ID_PAT),
    ("properties.parties", "type", "eq", "array"),
    ("properties.parties", "minItems", "min", 2),
    ("properties.parties.items", "type", "eq", "object"),
    ("properties.parties.items", "additionalProperties", "eq", False),
    ("properties.parties.items", "required", "superset", ["ref", "role"]),
    ("properties.parties.items", "properties", "keys", ["ref", "role", "note"]),
    ("properties.parties.items.properties.ref", "type", "eq", "string"),
    ("properties.parties.items.properties.ref", "pattern", "eq", ASCII_ID_PAT),
    ("properties.parties.items.properties.role", "type", "eq", "string"),
    ("properties.parties.items.properties.role", "enum", "eq", list(ROLES)),
    ("properties.parties.items.properties.note", "type", "eq", "string"),
    ("properties.parties.items.properties.note", "maxWords", "max", 15),
    ("properties.mediating_variable", "type", "eq", "string"),
    ("properties.mediating_variable", "minLength", "min", 1),
    ("properties.mediating_variable", "maxWords", "max", 25),
    ("properties.links", "type", "eq", "array"),
    ("properties.links.items", "type", "eq", "object"),
    ("properties.links.items", "additionalProperties", "eq", False),
    ("properties.links.items", "required", "superset", ["type", "ref"]),
    ("properties.links.items", "properties", "keys", ["type", "ref", "quote"]),
    ("properties.links.items.properties.type", "type", "eq", "string"),
    ("properties.links.items.properties.type", "enum", "eq", list(LINK_TYPES)),
    ("properties.links.items.properties.ref", "type", "eq", "string"),
    ("properties.links.items.properties.ref", "pattern", "eq", ASCII_ID_PAT),
    ("properties.links.items.properties.quote", "type", "eq", "string"),
    ("properties.links.items.properties.quote", "minWords", "min", 3),
    ("properties.links.items.properties.quote", "maxWords", "max", 15),
    ("properties.sources", "type", "eq", "array"),
    ("properties.sources", "minItems", "min", 1),
    ("properties.sources.items", "type", "eq", "object"),
    ("properties.sources.items", "additionalProperties", "eq", False),
    ("properties.sources.items", "required", "superset", ["path", "id"]),
    ("properties.sources.items", "properties", "keys", ["path", "id"]),
    ("properties.sources.items.properties.path", "type", "eq", "string"),
    ("properties.sources.items.properties.path", "minLength", "min", 1),
    ("properties.sources.items.properties.path", "maxWords", "max", 1),
    ("properties.sources.items.properties.path", "pattern", "eq", SOURCE_PATH_PAT),
    ("properties.sources.items.properties.id", "type", "eq", "string"),
    ("properties.sources.items.properties.id", "minLength", "min", 1),
    ("properties.sources.items.properties.id", "maxWords", "max", 1),
    ("properties.sources.items.properties.id", "pattern", "eq", ASCII_ID_PAT),
)


class Refused(Exception):
    """⚠ LOUD AND NAMED. `.name` is the refusal's name; `.detail` says where and what."""

    def __init__(self, name, detail):
        super().__init__(f"{name} — {detail}")
        self.name, self.detail = name, detail


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_text(s):
    return sha256_bytes(s.encode("utf-8"))


def words(s):
    """Word count with every Unicode format/control/space character as a separator (Q5: an
    invisible join cannot make 44 words count as one)."""
    return len("".join(" " if unicodedata.category(ch) in SEP_CATEGORIES else ch
                       for ch in str(s)).split())


def bad_chars(s):
    """[(offset, codepoint, name)] of the characters refused in any string of the home."""
    out = []
    for i, ch in enumerate(s):
        cat = unicodedata.category(ch)
        if cat in BAD_CATEGORIES or (cat == "Cc" and ch not in "\t\n\r"):
            out.append((i, ord(ch), unicodedata.name(ch, cat)))
    return out


def now_clock():
    return datetime.datetime.now(datetime.timezone.utc).strftime(CLOCK_FMT)


def rel(path):
    return os.path.relpath(path, REPO) if path.startswith(REPO) else path


# ============================================================================================
# LOADING — parse in the consumer's grammar (JSON), every failure NAMED
# ============================================================================================
def read_text(path):
    with open(path, "rb") as f:
        raw = f.read()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as e:
        raise Refused("S-PARSE", f"{rel(path)} is not UTF-8: {e.reason} at byte {e.start} — the home is "
                                 f"parsed in the consumer's grammar and a byte outside it is refused")


def parse_json(text, what):
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise Refused("S-PARSE", f"{what} does not parse as JSON: {e}")


def load_home(brain, overrides=None):
    """Texts + parsed objects of the three home files, the schema and the rulings store.
    `overrides` maps a home filename to replacement TEXT (the writer validates in memory)."""
    overrides = overrides or {}
    home = {"brain": brain, "text": {}, "obj": {}}
    for name in HOME_FILES:
        path = os.path.join(brain, name)
        if name in overrides:
            text = overrides[name]
        elif os.path.isfile(path):
            text = read_text(path)
        else:
            raise Refused("S-SHAPE", f"{name} is absent from the home {brain}")
        home["text"][name] = text
        home["obj"][name] = parse_json(text, name)
    schema_path = os.path.join(brain, SCHEMA_REL)
    if not os.path.isfile(schema_path):
        raise Refused("S-SHAPE", f"schema absent: {schema_path}")
    home["schema_text"] = read_text(schema_path)
    home["schema"] = parse_json(home["schema_text"], SCHEMA_NAME)
    if not os.path.exists(RULINGS):
        raise Refused("S-SHAPE", f"knowledge/_rulings.json absent at {RULINGS}")
    rulings = parse_json(read_text(RULINGS), "_rulings.json")
    if not isinstance(rulings, dict) or not isinstance(rulings.get("rulings"), list):
        raise Refused("S-SHAPE", "_rulings.json has no `rulings` list")
    home["rulings"] = {}
    for r in rulings["rulings"]:
        if isinstance(r, dict) and isinstance(r.get("id"), str):
            home["rulings"][r["id"]] = r
    home["prose_superseded"] = prose_supersessions(home["rulings"])
    return home


def _ruling_prose(r):
    return " ".join(str(r.get(k, "")) for k in ("status", "ruled", "says"))


def prose_supersessions(rulings):
    """Q1 (#239): {ruling id: 'by whom / how'} for every ruling the STORE'S PROSE calls
    superseded — the `superseded_by` field is on 1 of 328 rows, the word is on more. Two
    readings: (a) another ruling's status/ruled/says says `supersedes … <id>`; (b) the ruling's
    own `status` field says `superseded`. FLOATED as a reading, declared in the #239-F report."""
    out = {}
    for rid, r in rulings.items():
        if re.search(r"\bsuperseded\b", str(r.get("status", "")), re.I):
            out[rid] = f"its own status says superseded: {str(r.get('status'))[:90]!r}"
    for yid, y in rulings.items():
        prose = _ruling_prose(y)
        for m in re.finditer(r"\bsupersed(?:es|ing)\b[^.;]{0,80}?\b([A-Za-z]+[0-9]*-[A-Za-z0-9]+)\b", prose):
            target = m.group(1)
            if target in rulings and target != yid and target not in out:
                out[target] = f"{yid} says {m.group(0)[:90]!r}"
    return out


def load_register():
    """The frozen R1 register (Q3's oracle): (rows_by_id, row_text_by_id, raw_bytes, generated_date)."""
    path = os.path.join(REPO, R1_TENSIONS_REL)
    if not os.path.isfile(path):
        raise Refused("S-SOURCE", f"the frozen R1 register {R1_TENSIONS_REL} does not exist here — every "
                                  f"node's words are verified against it (ADR-0017); restore it")
    with open(path, "rb") as f:
        raw = f.read()
    try:
        obj = json.loads(raw.decode("utf-8"))
    except Exception as e:  # noqa: BLE001
        raise Refused("S-SOURCE", f"{R1_TENSIONS_REL} does not parse: {type(e).__name__}: {e}")
    rows = obj.get("tensions") if isinstance(obj, dict) else None
    if not isinstance(rows, list):
        raise Refused("S-SOURCE", f"{R1_TENSIONS_REL} has no `tensions` list")
    by_id, texts = {}, {}
    for r in rows:
        if isinstance(r, dict) and isinstance(r.get("id"), str):
            by_id[r["id"]] = r
            texts[r["id"]] = " ".join(str(v) for v in r.values() if isinstance(v, str))
    gen = obj.get("generated") if isinstance(obj, dict) else None
    return by_id, texts, raw, (gen if isinstance(gen, str) else None)


# ============================================================================================
# THE SCHEMA — a small reader of draft-2020-12 core + the house `maxWords`/`minWords`. It REFUSES
# a keyword it does not implement, refuses a schema that LOOSENS a pinned floor (and applies the
# floor regardless), and refuses a schema whose sha256 has moved without the pin (Q2, #239).
# ============================================================================================
def _walk_schema(schema, pointer):
    cur = schema
    for step in [s for s in pointer.split(".") if s]:
        if not isinstance(cur, dict) or step not in cur:
            return None
        cur = cur[step]
    return cur if isinstance(cur, dict) else None


def schema_pin_and_floors(schema_text, schema):
    """(fails, effective_schema). The effective schema is the on-disk one with every loosened
    floor put back, so the data-level refusal still fires by its own name."""
    fails = []
    if sha256_text(schema_text) != SCHEMA_SHA256:
        fails.append(("SCHEMA-PIN-MISMATCH",
                      f"schema/{SCHEMA_NAME} sha256 {sha256_text(schema_text)[:16]}… is not the pinned "
                      f"{SCHEMA_SHA256[:16]}… — a schema edit must move SCHEMA_SHA256 in "
                      f"knowledge/_validate_polarities.py in the same commit (#239 lane F, V's Q2)"))
    if not isinstance(schema, dict):
        return fails + [("S-SCHEMA", f"schema/{SCHEMA_NAME} is not an object")], {"type": "object"}
    eff = copy.deepcopy(schema)
    for pointer, kw, kind, floor in SCHEMA_FLOORS:
        node = _walk_schema(eff, pointer)
        where = f"schema{('.' + pointer) if pointer else ''}.{kw}"
        if node is None:
            fails.append(("S-SCHEMA", f"{where}: the schema has no object at {pointer!r} — malformed"))
            continue
        have = node.get(kw)
        loose = False
        if kw == "pattern" and isinstance(have, str):
            try:
                re.compile(have)
            except re.error as e:
                fails.append(("S-SCHEMA", f"{where}: {have!r} is not a valid regex ({e}) — malformed schema"))
        if kind == "eq":
            loose = have != floor
            if have is not None and type(have) is not type(floor):
                fails.append(("S-SCHEMA", f"{where}: {have!r} is a {type(have).__name__} where this gate reads a "
                                          f"{type(floor).__name__} (e.g. a `type` list) — malformed schema"))
        elif kind == "min":
            loose = not isinstance(have, int) or isinstance(have, bool) or have < floor
        elif kind == "max":
            loose = not isinstance(have, int) or isinstance(have, bool) or have > floor
        elif kind == "superset":
            loose = not isinstance(have, list) or not set(floor) <= set(have)
        elif kind == "excludes":
            loose = isinstance(have, list) and bool(set(floor) & set(have))
        elif kind == "keys":
            loose = not isinstance(have, dict) or set(have) != set(floor)
        if loose:
            if kind == "excludes":
                back = sorted(set(floor) & set(have if isinstance(have, list) else []))
                fails.append(("SCHEMA-LOOSENED",
                              f"{where}: {back!r} is back in `required`, which the pinned floor EXCLUDES "
                              f"(#242 lane P2, s240-D3) — it reads as a tightening, but it legislates away "
                              f"the RECEIPT WIDENING Dave ruled: every node born after R1 carries `$seed` "
                              f"and no `sources`, so this one word would make every one of them S-SCHEMA. "
                              f"A schema may only tighten a REFUSAL, never a PERMISSION; the floor is "
                              f"applied regardless"))
                node[kw] = [k for k in have if k not in set(floor)]
                continue
            fails.append(("SCHEMA-LOOSENED",
                          f"{where}: {have!r} loosens the pinned floor {floor!r} (s238-D7; #239 lane F, "
                          f"V's Q2) — a schema may only tighten; the floor is applied regardless"))
            if kind == "keys":
                node[kw] = {k: v for k, v in (have.items() if isinstance(have, dict) else [])
                            if k in floor}
                for k in floor:
                    node[kw].setdefault(k, {})
            elif kind == "superset":
                node[kw] = sorted(set(floor) | (set(have) if isinstance(have, list) else set()))
            else:
                node[kw] = floor
    return fails, eff


def schema_keywords_supported(schema, path="schema"):
    if isinstance(schema, dict):
        for k, v in schema.items():
            if k not in SCHEMA_KEYWORDS and path.split(".")[-1] != "properties":
                raise Refused("SCHEMA-KEYWORD-UNSUPPORTED",
                              f"{path}.{k}: this gate does not implement that keyword — implement "
                              f"it or remove it; an ignored keyword is an unenforced rule")
            if k == "properties":
                if not isinstance(v, dict):
                    raise Refused("S-SCHEMA", f"{path}.properties is not an object (malformed schema)")
                for pk, pv in v.items():
                    schema_keywords_supported(pv, f"{path}.properties.{pk}")
            elif k == "items":
                schema_keywords_supported(v, f"{path}.items")


def schema_validate(inst, schema, path, out):
    """Append (keyword, path, detail, instance) for every violation. Pure."""
    if not isinstance(schema, dict):
        out.append(("schema", path, "the schema node here is not an object", inst))
        return
    t = schema.get("type")
    if t == "object":
        if not isinstance(inst, dict):
            out.append(("type", path, f"expected object, got {type(inst).__name__}", inst))
            return
        props = schema.get("properties", {})
        if not isinstance(props, dict):
            out.append(("schema", path, "`properties` is not an object", inst))
            return
        for r in schema.get("required", []):
            if r not in inst:
                out.append(("required", f"{path}.{r}", f"required key {r!r} is missing", None))
        if schema.get("additionalProperties") is False:
            for k in inst:
                if k not in props:
                    out.append(("additionalProperties", f"{path}.{k}",
                                f"key {k!r} is not in the schema (allowed: {sorted(props)})", inst[k]))
        for k, v in inst.items():
            if k in props:
                schema_validate(v, props[k], f"{path}.{k}", out)
    elif t == "array":
        if not isinstance(inst, list):
            out.append(("type", path, f"expected array, got {type(inst).__name__}", inst))
            return
        if "minItems" in schema and len(inst) < schema["minItems"]:
            out.append(("minItems", path, f"{len(inst)} item(s), minimum {schema['minItems']}", inst))
        if "items" in schema:
            for i, v in enumerate(inst):
                schema_validate(v, schema["items"], f"{path}[{i}]", out)
    elif t == "string":
        if not isinstance(inst, str):
            out.append(("type", path, f"expected string, got {type(inst).__name__}", inst))
            return
        if "enum" in schema and inst not in schema["enum"]:
            out.append(("enum", path, f"{inst!r} is not one of {schema['enum']}", inst))
        if "pattern" in schema:
            try:
                ok = re.search(schema["pattern"], inst) is not None
            except re.error as e:
                out.append(("schema", path, f"schema pattern {schema['pattern']!r} is not a valid "
                                            f"regex ({e}) — malformed schema", inst))
                ok = True
            if not ok:
                out.append(("pattern", path, f"{inst[:60]!r} does not match {schema['pattern']}", inst))
        if "minLength" in schema and len(inst) < schema["minLength"]:
            out.append(("minLength", path, f"shorter than {schema['minLength']}", inst))
        if "maxWords" in schema and words(inst) > schema["maxWords"]:
            out.append(("maxWords", path, f"{words(inst)} words, maximum {schema['maxWords']}", inst))
        if "minWords" in schema and words(inst) < schema["minWords"]:
            out.append(("minWords", path, f"{words(inst)} word(s), minimum {schema['minWords']}", inst))
    elif t is not None:
        out.append(("schema", path, f"schema type {t!r} is not one this gate reads", inst))


def name_violation(kw, path, detail, inst=None):
    """Map a schema violation to the refusal NAME s238-D7 / the schema's x-refusals promise."""
    leaf = path.rsplit(".", 1)[-1]
    if kw == "additionalProperties":
        if "status" in leaf.lower():
            return "R5-TYPED-STATUS"
        return "R3-JUDGEMENT-FIELD"
    if kw == "type" and re.search(r"\.links\[\d+\]$", path):
        return "R2-UNTYPED"             # a link that is not an object carries no type at all
    if leaf == "type" and ".links[" in path:
        if kw == "required" or (kw == "type" and inst is None):
            return "R2-UNTYPED"
        return "R2-UNKNOWN-TYPE"
    if kw == "maxWords" and leaf == "quote":
        return "R3-QUOTE-TOO-LONG"
    if kw == "minWords" and leaf == "quote":
        return "R3-QUOTE-NOT-VERBATIM"  # an under-floor quote is not a receipt (Q3)
    if kw == "maxWords" and leaf == "note":
        return "R3-NOTE-TOO-LONG"
    if kw == "maxWords":
        return "R3-JUDGEMENT-FIELD"     # mediating_variable, sources[].id/path: a paragraph is a judgement
    if kw == "pattern" and leaf in ("ref", "id", "path"):
        return "S-ID"
    if kw == "minItems" and leaf == "parties":
        return "S-MIN-PARTIES"
    if leaf == "role" and (kw == "enum" or (kw == "type" and inst is None)):
        return "S-ROLE"
    return "S-SCHEMA"


# ============================================================================================
# THE REFUSALS
# ============================================================================================
def _sniff_edges(path):
    """True when a JSON file carries a top-level key ending in `edges` (an authored edge list)."""
    try:
        obj = json.loads(read_text(path))
    except Exception:  # noqa: BLE001
        return False
    return isinstance(obj, dict) and any(isinstance(k, str) and k.lower().endswith("edges") for k in obj)


def _is_finder_dsstore(path):
    try:
        with open(path, "rb") as f:
            return f.read(len(DSSTORE_MAGIC)) == DSSTORE_MAGIC
    except OSError:
        return False


def check_home_dir(brain):
    """R4 — the home is a CLOSED directory AT EVERY LEVEL (Q6, #239): three homes, the schema dir
    with exactly one schema, the generated dir with only the derived three. Every entry is listed
    — dotfiles, __pycache__, *.tmp, symlinks — and anything else is a second stored shape (s238-D1)
    or an authored edge list. Returns (fails, notes)."""
    fails, notes = [], []
    if not os.path.isdir(brain):
        raise Refused("S-SHAPE", f"home directory absent: {brain}")

    def stray(where, path, name, inside_generated=False):
        if os.path.islink(path):
            fails.append(("R4-STRAY-FILE", f"{where} is a SYMLINK — the home is a closed directory of "
                                           f"regular files; a commit would carry the link, not the words"))
            return
        if os.path.isdir(path):
            fails.append(("R4-STRAY-FILE", f"{where}/ is a directory that is not part of the home "
                                           f"(delete it; __pycache__ and the like included)"))
            return
        if name == ".DS_Store" and _is_finder_dsstore(path):
            notes.append(f"{where} ignored — Finder metadata by its bytes (gitignored, never read)")
            return
        edges = os.path.isfile(path) and _sniff_edges(path)
        if inside_generated:
            fails.append(("R4-STRAY-FILE", f"{where} is not one of the derived files ({', '.join(GEN_FILES)}) — "
                                           f"nothing under the generated path may be authored (s238-D7 refusal 4)"))
            if edges:
                fails.append(("R4-AUTHORED-EDGES", f"{where} carries an `edges` key — pairwise edges are "
                                                   f"DERIVED (s238-D1); delete it and run --write"))
            return
        if edges:
            fails.append(("R4-AUTHORED-EDGES", f"{where} carries an `edges` key outside a derived file — "
                                               f"pairwise edges are DERIVED (s238-D1); delete it and run --write"))
            return
        fails.append(("R4-STRAY-FILE", f"{where} is not one of the homes ({', '.join(HOME_FILES)}), "
                                       f"schema/{SCHEMA_NAME} or {GEN_DIR}/ — a second stored shape for the "
                                       f"same concept is refused (s238-D1); dotfiles and *.tmp included"))

    for name in sorted(os.listdir(brain)):
        path = os.path.join(brain, name)
        if os.path.islink(path):
            stray(name, path, name)
            continue
        if name in HOME_FILES:
            if not os.path.isfile(path):
                fails.append(("R4-STRAY-FILE", f"{name} is not a regular file"))
            continue
        if name == "schema":
            if not os.path.isdir(path):
                fails.append(("R4-STRAY-FILE", f"schema is not a directory"))
                continue
            seen = sorted(os.listdir(path))
            for sub in seen:
                if sub == SCHEMA_NAME and os.path.isfile(os.path.join(path, sub)) \
                        and not os.path.islink(os.path.join(path, sub)):
                    continue
                stray(f"schema/{sub}", os.path.join(path, sub), sub)
            continue
        if name == GEN_DIR:
            if not os.path.isdir(path):
                fails.append(("R4-STRAY-FILE", f"{GEN_DIR} is a file, not the derived directory — "
                                               f"delete it and run --write"))
                fails.append(("MISSING-GENERATED", f"{GEN_DIR}/{' · '.join(GEN_FILES)} are absent because "
                                                   f"{GEN_DIR} is not a directory — run --write once it is"))
                continue
            for sub in sorted(os.listdir(path)):
                sp = os.path.join(path, sub)
                if sub in GEN_FILES and os.path.isfile(sp) and not os.path.islink(sp):
                    continue
                stray(f"{GEN_DIR}/{sub}", sp, sub, inside_generated=True)
            continue
        stray(name, path, name)
    return fails, notes


def check_strings(obj, where, fails):
    """Q5 — no invisible / format / control character in ANY string of the home."""
    if isinstance(obj, str):
        bad = bad_chars(obj)
        if bad:
            i, cp, nm = bad[0]
            fails.append(("S-FORMAT-CHAR", f"{where}: U+{cp:04X} ({nm}) at offset {i}"
                                           f"{' (+%d more)' % (len(bad) - 1) if len(bad) > 1 else ''} — "
                                           f"an invisible character is refused in every string of the home "
                                           f"(it hides words from every count and every eye)"))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            check_strings(k, f"{where}.<key {k[:30]!r}>", fails)
            check_strings(v, f"{where}.{k}", fails)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            check_strings(v, f"{where}[{i}]", fails)


def check_stubs(stubs_obj, register_text):
    fails = []
    if not isinstance(stubs_obj, dict) or not isinstance(stubs_obj.get("stubs"), list):
        return [("S-SHAPE", "stubs.json must be an object with a `stubs` list")]
    for k in stubs_obj:
        if k not in ("$description", "stubs"):
            fails.append(("R3-JUDGEMENT-FIELD", f"stubs.json top level: unexpected key {k!r}"))
    seen_ids, seen_phrases = set(), set()
    for i, s in enumerate(stubs_obj["stubs"]):
        where = f"stubs[{i}]"
        if not isinstance(s, dict) or set(s) != {"id", "phrase"}:
            fails.append(("S-STUB-SHAPE", f"{where}: a stub is EXACTLY {{id, phrase}} and nothing "
                                          f"else (got {sorted(s) if isinstance(s, dict) else type(s).__name__})"))
            continue
        sid, phrase = s["id"], s["phrase"]
        if not isinstance(sid, str) or not STUB_ID.match(sid):
            fails.append(("S-STUB-SHAPE", f"{where}: id {sid!r} must be a string matching {STUB_ID.pattern}"))
        if not isinstance(phrase, str) or words(phrase) == 0:
            fails.append(("S-STUB-SHAPE", f"{where}: phrase must be a non-empty string with at least one "
                                          f"visible word"))
        else:
            if words(phrase) > 15:
                fails.append(("R3-JUDGEMENT-FIELD", f"{where}: phrase is {words(phrase)} words — a "
                                                    f"stub is a phrase, not a paragraph (max 15)"))
            if register_text is not None and phrase not in register_text:
                fails.append(("R3-JUDGEMENT-FIELD", f"{where}: phrase {phrase[:60]!r} is not VERBATIM in "
                                                    f"the frozen R1 register — a stub is a phrase the "
                                                    f"register already says (s238-D1); a phrase nothing can "
                                                    f"check is a judgement (Q5, #239)"))
        if isinstance(sid, str):
            if sid in seen_ids:
                fails.append(("S-DUP-STUB", f"{where}: duplicate stub id {sid!r}"))
            seen_ids.add(sid)
        if isinstance(phrase, str):
            if phrase in seen_phrases:
                fails.append(("S-DUP-STUB", f"{where}: duplicate stub phrase {phrase!r}"))
            seen_phrases.add(phrase)
    return fails


def check_principles(pr_obj):
    if not isinstance(pr_obj, dict) or not isinstance(pr_obj.get("principles"), list):
        return [("S-SHAPE", "principles.json must be an object with a `principles` list")], {}
    fails, reg = [], {}
    for i, p in enumerate(pr_obj["principles"]):
        if not isinstance(p, dict) or not isinstance(p.get("id"), str):
            fails.append(("S-SHAPE", f"principles[{i}] has no string id"))
            continue
        if p["id"] in reg:
            fails.append(("S-DUP-ID", f"principles.json: duplicate id {p['id']!r}"))
        if p.get("grade") not in GRADE_NAMES:
            fails.append(("S-SHAPE", f"principles[{i}] {p['id']}: grade {p.get('grade')!r} is not "
                                     f"one of {sorted(GRADE_NAMES)} (s237-D1)"))
        reg[p["id"]] = p
    return fails, reg


def check_migration_receipt(pol, register_raw):
    """Q5/Q3 — $description and $migration are SHAPE-FIXED and the receipt is VERIFIED, not decorative."""
    fails = []
    desc = pol.get("$description")
    if not isinstance(desc, str) or words(desc) == 0:
        fails.append(("R3-JUDGEMENT-FIELD", "polarities.json $description must be a non-empty string"))
    elif words(desc) > DESCRIPTION_MAX_WORDS:
        fails.append(("R3-JUDGEMENT-FIELD", f"polarities.json $description is {words(desc)} words, maximum "
                                            f"{DESCRIPTION_MAX_WORDS} (FLOATED, #239) — a header, not an essay"))
    mig = pol.get("$migration")
    if not isinstance(mig, dict):
        return fails + [("S-RECEIPT", "polarities.json $migration must be an object {from, sha256, by, receipts}")]
    if set(mig) != set(MIGRATION_KEYS):
        extra = sorted(set(mig) - set(MIGRATION_KEYS))
        fails.append(("R3-JUDGEMENT-FIELD" if extra else "S-RECEIPT",
                      f"polarities.json $migration keys {sorted(mig)} are not exactly {list(MIGRATION_KEYS)} — "
                      f"a receipt is shape-fixed; a nested map under it is a judgement field by another door"))
    if mig.get("from") != R1_TENSIONS_REL:
        fails.append(("S-RECEIPT", f"$migration.from {str(mig.get('from'))[:80]!r} is not the frozen R1 register "
                                   f"{R1_TENSIONS_REL} (the only source on the allow-list, Q3 #239)"))
    elif register_raw is not None and mig.get("sha256") != sha256_bytes(register_raw):
        fails.append(("S-RECEIPT", f"$migration.sha256 {str(mig.get('sha256'))[:16]}… does not match the frozen "
                                   f"register's bytes ({sha256_bytes(register_raw)[:16]}…) — the receipt is "
                                   f"verified, not decorative"))
    by = mig.get("by")
    if not isinstance(by, str) or not re.match(SOURCE_PATH_PAT, by):
        # the generator's NAME is provenance prose, patterned like a path; the data lineage that is
        # verified is `from` + `sha256` above (a stand-in repo need not carry the generator)
        fails.append(("S-RECEIPT", f"$migration.by {str(by)[:80]!r} is not a repo-relative path shape"))
    rec = mig.get("receipts")
    if not isinstance(rec, list) or not all(isinstance(x, str) for x in rec):
        fails.append(("S-RECEIPT", "$migration.receipts must be a list of strings"))
    else:
        for i, x in enumerate(rec):
            if words(x) > RECEIPT_MAX_WORDS:
                fails.append(("R3-JUDGEMENT-FIELD", f"$migration.receipts[{i}] is {words(x)} words, maximum "
                                                    f"{RECEIPT_MAX_WORDS} (FLOATED, #239)"))
    return fails


def check_receipt(nid, node, rulings):
    """s240-D3 (#242 lane P) — THE RECEIPT IS ONE POINTER PER NODE.

    Every polarity traces to something Dave ruled; the ANCHOR widens from the R1 register row to
    an R1 row OR a knowledge/_rulings.json id:
      `sources`     the migration's form — a frozen R1 register row (verified elsewhere: allow-list,
                    row exists, bijection)
      `$seed`       a node BORN AFTER R1 — the ruling id that created it
      `retiredBy`   a node RETIRED — the ruling id that retired it; the node keeps its row and
                    drops out of everything generated (enforced in derive() + retired_leaks())
    BOTH birth receipts on one node is refused (S-SOURCE); NEITHER is refused (S-SOURCE); a receipt
    id that is not in the store is refused (R1-DANGLING). `retiredBy` is ADDITIVE — it is not a
    second birth receipt, so a $seed node may also be retired.
    """
    fails = []
    seed = node.get("$seed")
    src = node.get("sources")
    has_src = isinstance(src, list) and len(src) > 0
    has_seed = isinstance(seed, str) and seed.strip() != ""
    if has_src and has_seed:
        first_id = src[0].get("id") if isinstance(src[0], dict) else "?"
        fails.append(("S-SOURCE", f"{nid}: carries BOTH an R1 receipt (sources[0].id {str(first_id)[:40]!r}) "
                                  f"and a $seed ruling receipt {seed[:40]!r} — THE RECEIPT IS ONE POINTER PER NODE "
                                  f"(s240-D3): a node came from the R1 register or from a ruling, never from both"))
    elif not has_src and not has_seed:
        fails.append(("S-SOURCE", f"{nid}: carries NO receipt — every polarity traces to something Dave ruled "
                                  f"(s240-D3): name the frozen R1 row in `sources` or, for a node born after R1, "
                                  f"the knowledge/_rulings.json id that created it in `$seed`"))
    for key in ("$seed", "retiredBy"):
        v = node.get(key)
        if v is None or not isinstance(v, str):
            continue        # absent is legal; a non-string is named by the schema walk
        if v not in rulings:
            fails.append(("R1-DANGLING", f"{nid}.{key} {v[:40]!r} is not a knowledge/_rulings.json id — the "
                                         f"receipt names a ruling that does not exist (s240-D3); a receipt that "
                                         f"points at nothing is a judgement wearing an id"))
    return fails


def retired_map(home):
    """{node id: the ruling id that retired it} — s240-D3's drop-out set, with its receipt."""
    try:
        nodes = home["obj"]["polarities.json"]["polarities"]
    except (KeyError, TypeError):
        return {}
    if not isinstance(nodes, list):
        return {}
    return {n["id"]: n["retiredBy"] for n in nodes
            if isinstance(n, dict) and isinstance(n.get("id"), str) and isinstance(n.get("retiredBy"), str)}


def live_nodes(home_nodes):
    """The nodes the derivation sees: a retired node keeps its row here and DROPS OUT of everything
    generated from the KG (s240-D3)."""
    return [n for n in home_nodes if not (isinstance(n, dict) and isinstance(n.get("retiredBy"), str))]


def check_polarities(home, register):
    """R1 · R2 · R3 · R5 and the schema refusals over polarities.json. Returns (fails, resolved)
    where resolved[pl-id] = list of party dicts with a DERIVED `kind` (+ `grade`)."""
    fails = []
    rows_by_id, row_texts, register_raw, _ = register
    pol = home["obj"]["polarities.json"]
    sfails, schema = schema_pin_and_floors(home["schema_text"], home["schema"])
    fails += sfails
    schema_keywords_supported(schema)
    if not isinstance(pol, dict) or not isinstance(pol.get("polarities"), list):
        return fails + [("S-SHAPE", "polarities.json must be an object with a `polarities` list")], {}
    for k in pol:
        if k not in TOP_KEYS:
            fails.append(("R3-JUDGEMENT-FIELD", f"polarities.json top level: unexpected key {k!r}"))
    fails += check_migration_receipt(pol, register_raw)
    check_strings(pol, "polarities.json", fails)
    check_strings(home["obj"]["stubs.json"], "stubs.json", fails)
    check_strings(home["obj"]["principles.json"], "principles.json", fails)
    all_rows_text = " \n ".join(row_texts.values())
    st_fails = check_stubs(home["obj"]["stubs.json"], all_rows_text)
    fails += st_fails
    # only a stub named in a refusal stops being a party target — one bad stub must not make the
    # other fourteen dangle (a one-fault, seventeen-refusal read was noise, #239)
    bad_stub_ix = {int(m.group(1)) for _, d in st_fails for m in [re.match(r"stubs\[(\d+)\]", d)] if m}
    stubs = {s.get("id") for i, s in enumerate(home["obj"]["stubs.json"].get("stubs", []))
             if isinstance(s, dict) and isinstance(s.get("id"), str) and i not in bad_stub_ix} \
        if isinstance(home["obj"]["stubs.json"], dict) and isinstance(home["obj"]["stubs.json"].get("stubs"), list) else set()
    pr_fails, reg = check_principles(home["obj"]["principles.json"])
    fails += pr_fails
    rulings = home["rulings"]
    prose_sup = home["prose_superseded"]
    nodes = pol["polarities"]
    pol_ids = [n.get("id") for n in nodes if isinstance(n, dict) and isinstance(n.get("id"), str)]
    pol_id_set = set(pol_ids)
    seen = set()
    resolved = {}
    claims = {}          # frozen row id -> [node ids]
    props = schema.get("properties", {})
    for i, node in enumerate(nodes):
        where = f"polarities[{i}]"
        if not isinstance(node, dict):
            fails.append(("S-SHAPE", f"{where} is not an object"))
            continue
        nid = node.get("id") if isinstance(node.get("id"), str) else f"<{where}>"
        if nid in seen:
            fails.append(("S-DUP-ID", f"{where}: duplicate polarity id {nid!r}"))
        seen.add(nid)
        # R5 / R3 BEFORE the schema walk, so the refusal is named precisely, not "extra key"
        for k in node:
            if k not in props:
                if "status" in k.lower():
                    fails.append(("R5-TYPED-STATUS", f"{nid}: key {k!r} — status is DERIVED with a "
                                                     f"clock (s238-D3), never typed on a node"))
                else:
                    fails.append(("R3-JUDGEMENT-FIELD", f"{nid}: key {k!r} — a node carries no "
                                                        f"free-text judgement of any name; its only "
                                                        f"judgement is a typed link (s238-D7)"))
        viol = []
        schema_validate(node, schema, nid, viol)
        for kw, path, detail, inst in viol:
            if kw == "additionalProperties" and path.count(".") == 1:
                continue    # already named above at node level
            fails.append((name_violation(kw, path, detail, inst), f"{path}: {detail}"))
        # s240-D3 (#242) — THE RECEIPT: one pointer per node (an R1 row OR a ruling id), and every
        # receipt id resolves in the store. Asked BEFORE the source pointers so "no receipt" is
        # named as itself and not as an absent `sources` key.
        fails += check_receipt(nid, node, rulings)
        # Q3 — the SOURCE pointers: on the allow-list, a real row, claimed once
        sources = node.get("sources") if isinstance(node.get("sources"), list) else []
        hays = []
        for j, s in enumerate(sources):
            if not isinstance(s, dict) or not isinstance(s.get("path"), str) or not isinstance(s.get("id"), str):
                continue      # named by the schema walk
            sw = f"{nid}.sources[{j}]"
            if s["path"] not in SOURCE_ALLOW:
                fails.append(("S-SOURCE", f"{sw}.path {s['path'][:80]!r} is not on the source allow-list "
                                          f"{list(SOURCE_ALLOW)} — a node may not name its own oracle (Q3, "
                                          f"#239); a second register is Dave's"))
            elif s["id"] not in rows_by_id:
                fails.append(("S-SOURCE", f"{sw}.id {s['id'][:40]!r} is not a row of {s['path']}"))
            else:
                claims.setdefault(s["id"], []).append(nid)
                hays.append(row_texts[s["id"]])
        # R1 — every ref resolves against the LIVE registers
        parties = node.get("parties") if isinstance(node.get("parties"), list) else []
        roles = {p.get("role") for p in parties if isinstance(p, dict) and isinstance(p.get("role"), str)}
        if len(parties) >= 2 and len(roles) < 2:
            fails.append(("S-ONE-SIDED", f"{nid}: every party stands on {sorted(roles)} — a polarity is "
                                         f"a pull between two true things (s238-D4); parties must span "
                                         f"at least two sides"))
        seen_refs = set()
        kinds = []
        for j, p in enumerate(parties):
            if not isinstance(p, dict) or not isinstance(p.get("ref"), str):
                continue
            ref = p["ref"]
            pw = f"{nid}.parties[{j}]"
            if ref in seen_refs:
                fails.append(("S-DUP-PARTY", f"{pw}: {ref!r} appears twice on one node"))
            seen_refs.add(ref)
            # Q5 — a note is a VERBATIM gloss from the node's source row, or it is a judgement
            note = p.get("note")
            if isinstance(note, str) and hays and not any(note in h for h in hays):
                fails.append(("R3-JUDGEMENT-FIELD", f"{pw}.note {note[:60]!r} is not a verbatim substring of "
                                                    f"the node's source row — a note that the register does "
                                                    f"not say is a judgement wearing a gloss (Q5, #239)"))
            if not ASCII_ID.match(ref):
                kinds.append(None)
                continue          # named by the schema pattern walk (S-ID)
            if ref == nid:
                fails.append(("R1-SELF-PARTY", f"{pw}: a polarity may not be its own party"))
                kinds.append(None)
            elif ref in pol_id_set or POLARITY_ID.match(ref):
                fails.append(("R1-CIRCULAR", f"{pw}: {ref!r} is a polarity — a polarity as a party "
                                             f"of a polarity is not ruled (s238-D1 parties are "
                                             f"principle / obligation / ruling / stub)"))
                kinds.append(None)
            elif ref in reg:
                g = reg[ref].get("grade")
                kinds.append({"ref": ref, "role": p.get("role"),
                              "kind": "obligation" if g == OBLIGATION_GRADE else "principle",
                              "grade": g, "grade_name": GRADE_NAMES.get(g)})
            elif ref in stubs:
                kinds.append({"ref": ref, "role": p.get("role"), "kind": "stub", "grade": None,
                              "grade_name": None})
            elif ref.startswith("st-"):
                fails.append(("R1-UNDECLARED-STUB", f"{pw}: {ref!r} is spelled like a stub but is "
                                                    f"not declared in stubs.json"))
                kinds.append(None)
            elif ref in rulings:
                if rulings[ref].get("superseded_by"):
                    fails.append(("R1-SUPERSEDED", f"{pw}: ruling {ref!r} is superseded by "
                                                   f"{rulings[ref]['superseded_by']!r} — not live; "
                                                   f"point at the successor"))
                    kinds.append(None)
                else:
                    kinds.append({"ref": ref, "role": p.get("role"), "kind": "ruling", "grade": None,
                                  "grade_name": None})
            else:
                fails.append(("R1-DANGLING", f"{pw}: {ref!r} resolves to nothing — not a "
                                             f"principles.json row, not a stubs.json stub, not a "
                                             f"knowledge/_rulings.json id"))
                kinds.append(None)
        # Q5 — the mediating variable is CARRIED from the source row, verbatim
        mv = node.get("mediating_variable")
        if isinstance(mv, str) and hays and not any(mv in h for h in hays):
            fails.append(("R3-JUDGEMENT-FIELD", f"{nid}.mediating_variable {mv[:60]!r} is not a verbatim "
                                                f"substring of the node's source row — descriptive text the "
                                                f"register does not say is a judgement (Q5, #239)"))
        links = node.get("links") if isinstance(node.get("links"), list) else []
        seen_links = set()
        for j, l in enumerate(links):
            if not isinstance(l, dict) or not isinstance(l.get("ref"), str):
                continue      # named by the schema walk (R2-UNTYPED for a non-object link)
            ref = l["ref"]
            lw = f"{nid}.links[{j}]"
            ltype = l.get("type") if isinstance(l.get("type"), str) else None
            key = (ltype, ref)
            if key in seen_links:
                fails.append(("S-DUP-PARTY", f"{lw}: duplicate link {key!r}"))
            seen_links.add(key)
            if not ASCII_ID.match(ref):
                continue
            if ref == nid or ref in pol_id_set or POLARITY_ID.match(ref):
                fails.append(("R1-CIRCULAR", f"{lw}: {ref!r} is a polarity — a polarity→polarity "
                                             f"link is not ruled; pairwise edges are DERIVED, "
                                             f"never authored (s238-D1)"))
            elif ref in reg or ref in stubs or ref.startswith("st-") or ref.startswith("pr-"):
                fails.append(("R1-WRONG-REGISTER", f"{lw}: {ref!r} is a principle/stub id — links "
                                                   f"are RULING links (s238-D6); principles are "
                                                   f"parties, not link targets"))
            elif ref in rulings:
                r = rulings[ref]
                if r.get("superseded_by"):
                    fails.append(("R1-SUPERSEDED", f"{lw}: ruling {ref!r} is superseded by "
                                                   f"{r['superseded_by']!r} — not live; "
                                                   f"point at the successor"))
                elif ltype == "resolvedBy":
                    # Q1 (#239): "live" is more than one field — a resolvedBy CLOSES a polarity
                    if ref in prose_sup:
                        fails.append(("R1-SUPERSEDED", f"{lw}: ruling {ref!r} is superseded in the store's "
                                                       f"PROSE ({prose_sup[ref]}) — not live for a resolvedBy; "
                                                       f"point at the successor or type it `touches`"))
                    m = NOT_LIVE.search(str(r.get("status", "")))
                    if m:
                        fails.append(("R1-DANGLING", f"{lw}: ruling {ref!r} does not resolve against the LIVE "
                                                     f"register (sub-form NOT-LIVE): its status text says "
                                                     f"{m.group(1)!r} ({str(r.get('status'))[:70]!r}) — a "
                                                     f"resolvedBy may cite only a settled ruling; type it "
                                                     f"`touches` or wait for Dave (Q1, #239)"))
            else:
                fails.append(("R1-DANGLING", f"{lw}: {ref!r} is not a knowledge/_rulings.json id"))
        # R3 — quotes are RECEIPTS: verbatim from the node's source row on the allow-list; a
        # resolvedBy needs one (Q3, #239). Verified, never "declared UNVERIFIED and passed".
        fails += check_quotes_verbatim(nid, links, hays)
        resolved[nid] = kinds
    # Q3 — the migration receipt is a BIJECTION: every frozen row is claimed by exactly one node
    for rid, owners in sorted(claims.items()):
        if len(owners) > 1:
            fails.append(("S-SOURCE", f"frozen row {rid!r} is claimed by {owners} — one row, one node "
                                      f"(the r1_id pointer drives the derived status; two claimants would "
                                      f"copy one row's defaults onto another)"))
    unclaimed = sorted(set(rows_by_id) - set(claims))
    if unclaimed and not any(n == "S-SHAPE" for n, _ in fails):
        fails.append(("S-SOURCE", f"frozen row(s) {unclaimed[:6]}{'…' if len(unclaimed) > 6 else ''} "
                                  f"({len(unclaimed)}) are claimed by no node — the migration is one row, "
                                  f"one node ($migration is its receipt). RETIRING a polarity does NOT delete "
                                  f"its row: the node keeps its row and carries `retiredBy` naming the ruling "
                                  f"that retired it (s240-D3), and drops out of everything generated"))
    return fails, resolved


QUOTE_NOTES = []


def check_quotes_verbatim(nid, links, hays):
    fails = []
    for j, l in enumerate(links):
        if not isinstance(l, dict):
            continue
        q = l.get("quote")
        lw = f"{nid}.links[{j}]"
        if q is None:
            if l.get("type") == "resolvedBy":
                fails.append(("R3-QUOTE-MISSING", f"{lw}: a resolvedBy carries no quote — it CLOSES the "
                                                  f"polarity and needs a verbatim receipt from the source "
                                                  f"row (Q3, #239); touches may stay quote-free"))
            continue
        if not isinstance(q, str):
            continue      # named by the schema walk
        if words(q) == 0:
            fails.append(("R3-QUOTE-NOT-VERBATIM", f"{lw}.quote is empty — an empty receipt is found in "
                                                   f"every text and justifies nothing"))
            continue
        if not hays:
            fails.append(("R3-QUOTE-NOT-VERBATIM", f"{lw}.quote {q[:50]!r}… cannot be verified — no source "
                                                   f"row on the allow-list is reachable for {nid}; an "
                                                   f"unverifiable quote is not a receipt (Q3, #239)"))
            continue
        if not any(q in h for h in hays):
            fails.append(("R3-QUOTE-NOT-VERBATIM",
                          f"{lw}.quote: {q[:60]!r}… is not a verbatim substring of the "
                          f"node's source row — a paraphrase is a judgement wearing quote marks"))
    return fails


# ============================================================================================
# THE DERIVATION — status (with a clock), edges (pairwise view), the defaults declaration
# ============================================================================================
STATUS_RULES = {
    "R-OBLIGATION": ">=1 party resolves to a principles.json row whose grade is L (= OBLIGATION, "
                    "s237-D1; a node type no principle can outrank, s237-D2) -> settled-by-obligation. "
                    "Applied FIRST.",
    "R-RESOLVED": ">=1 link typed resolvedBy whose ref is a live ruling in knowledge/_rulings.json "
                  "-> resolved. (237-T's R-RESOLVED read how_it_resolves prose for an id; the typed "
                  "link IS that citation, migrated.)",
    "R-OPEN": "the complement.",
    "RULE-K/RULE-D": "knowable_how / disposition / ask_when / factory_default are COPIED per open row "
                     "from 237-T's open-tensions.json, FLOATED — the four ask-whens are Dave's "
                     "(s238-D3); this file rules nothing. `factory_default` is the GRILL's sense of "
                     "default (value used because nothing was asked), not s219-D3's shipped option.",
}
EDGE_RULE = ("for each polarity, for each unordered pair of parties on DIFFERENT sides whose refs both "
             "resolve to principles.json rows (principle or obligation) -> one edge carrying the "
             "polarity id and its mediating variable. Same-side pairs produce NO edge (237-T finding 4: "
             "tn-19's three persuasion principles are one side). Stubs and rulings produce NO edge "
             "(237-T finding 3: an edge needs a register node at both ends). This is a VIEW: the node "
             "is the home (s238-D1).")
DECLARE_RULE = ("D-DECLARE (s238-D5): a polarity's factory default is DECLARED iff it BENT AWAY FROM THE "
                "CONSERVATIVE SIDE — not all of them, not on demand.")


def open_defaults_rows():
    """The 237-T proposals, keyed by tn-id. Raises FileNotFoundError when the asset is unreachable."""
    with open(OPEN_DEFAULTS, "rb") as f:
        raw = f.read()
    obj = json.loads(raw.decode("utf-8"))
    return {r["id"]: r for r in obj.get("rows", [])}, sha256_bytes(raw)


def canonical(body):
    return json.dumps(body, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def render_json(body, generated_at):
    doc = {"$header": GEN_HEADER, "generated_at": generated_at,
           "content_sha256": sha256_text(canonical(body))}
    doc.update(body)
    return json.dumps(doc, indent=1, ensure_ascii=False) + "\n"


def render_txt(body_lines, generated_at):
    body = "\n".join(body_lines) + "\n"
    return (f"{GEN_HEADER}\ngenerated_at: {generated_at}\ncontent_sha256: {sha256_text(body)}\n"
            f"---\n{body}")


def delta_cause(rows_by_id):
    """`delta_vs_237T.cause`, DERIVED from the LIVE rows (s240-D3, #242 lane P2).

    A clause is emitted only while the node it is about still has a derived row, so a RETIRED node
    takes its own id out of the prose as well as out of the rows — the drop-out is every BYTE of
    every generated file, not just every row. With both nodes live the result is byte-identical to
    the literal this replaced (selftest arm: DELTA-PROSE BYTE-IDENTITY)."""
    parts = []
    for nid, tmpl in DELTA_CLAUSES:
        row = rows_by_id.get(nid)
        if row is None:
            continue                      # retired (or absent): its clause goes with it
        parts.append(tmpl.format(id=nid, r1=row.get("r1_id")))
    if parts and not parts[-1].endswith("."):
        parts[-1] = parts[-1] + ", so " + DELTA_FIGURE
    else:
        parts.append(DELTA_FIGURE[0].upper() + DELTA_FIGURE[1:])
    return " ".join(parts)


def _first_source_id(node):
    s = node.get("sources")
    if isinstance(s, list) and s and isinstance(s[0], dict) and isinstance(s[0].get("id"), str):
        return s[0]["id"]
    return None


def derive(home, resolved, defaults, defaults_sha, generated_at):
    """Return {filename: text} for the three generated files, at the given clock.

    s240-D3 (#242): a RETIRED node (one carrying `retiredBy`) keeps its row in polarities.json and
    DROPS OUT HERE — it produces no status row, no edge and no defaults line. The drop-out is the
    ruling's own words ("drops out of everything generated from the KG"), so it happens at the one
    place every generated file is derived, not per file."""
    # NOTE: nothing about the retired set is WRITTEN into the derived bodies — with zero retired
    # nodes the three files are byte-identical to #239's, so the derivation did not move. The one
    # prose position that used to name node ids regardless (`delta_vs_237T.cause`) is now DERIVED
    # from the live rows too — see delta_cause() and V2's finding 3.
    nodes = live_nodes(home["obj"]["polarities.json"]["polarities"])
    rows, edges = [], []
    counts = {"settled-by-obligation": 0, "resolved": 0, "open": 0}
    kind_counts = {"principle": 0, "obligation": 0, "ruling": 0, "stub": 0}
    n_with_edges = 0
    for node in nodes:
        nid = node["id"]
        kinds = [k for k in resolved.get(nid, []) if k]
        for k in kinds:
            kind_counts[k["kind"]] += 1
        obl = [k["ref"] for k in kinds if k["kind"] == "obligation"]
        resolving = [l["ref"] for l in node.get("links", []) if l.get("type") == "resolvedBy"]
        if obl:
            status = "settled-by-obligation"
        elif resolving:
            status = "resolved"
        else:
            status = "open"
        counts[status] += 1
        r1_id = _first_source_id(node)
        row = {"id": nid, "r1_id": r1_id, "status_derived": status,
               "obligation_parties": obl, "resolving_links": resolving,
               "parties": kinds, "links": node.get("links", []),
               "mediating_variable": node.get("mediating_variable")}
        if status == "open":
            d = defaults.get(r1_id)
            if d is None:
                row["proposal"] = "ABSENT — no row in open-tensions.json for this polarity"
                row["factory_default"] = None
            else:
                row["factory_default"] = d.get("factory_default_proposed")
                row["disposition"] = d.get("disposition")
                row["ask_when"] = d.get("ask_when")
                row["knowable_by_factory"] = d.get("knowable_by_factory")
                row["knowable_how"] = d.get("knowable_how")
                row["question_proposed"] = d.get("question_proposed")
                row["register"] = d.get("register", "FLOATED — proposed, never ruled")
        rows.append(row)
        reg_parties = [k for k in kinds if k["kind"] in ("principle", "obligation")]
        made = 0
        for a in range(len(reg_parties)):
            for b in range(a + 1, len(reg_parties)):
                pa, pb = reg_parties[a], reg_parties[b]
                if pa["role"] == pb["role"]:
                    continue
                edges.append({"polarity": nid, "from": pa["ref"], "to": pb["ref"],
                              "from_kind": pa["kind"], "to_kind": pb["kind"],
                              "mediating_variable": node.get("mediating_variable")})
                made += 1
        if made:
            n_with_edges += 1
    edges.sort(key=lambda e: (e["polarity"], e["from"], e["to"]))
    status_body = {
        "rules": STATUS_RULES,
        "counts": counts,
        "party_kinds": kind_counts,
        "delta_vs_237T": {
            "237-T_sort": T_SORT_FIGURE[0], "237-T_source": T_SORT_FIGURE[1],
            "this_derivation": f"{counts['settled-by-obligation']} · {counts['resolved']} · {counts['open']}",
            "cause": delta_cause({r["id"]: r for r in rows}),
        },
        "inputs": {"open_defaults": {"path": OPEN_DEFAULTS_REL, "sha256": defaults_sha}},
        "rows": rows,
    }
    edges_body = {
        "rule": EDGE_RULE,
        "counts": {"edges": len(edges), "polarities_with_edges": n_with_edges,
                   "polarities_without_edges": len(nodes) - n_with_edges,
                   "parties_not_edgeable": kind_counts["stub"] + kind_counts["ruling"]},
        "edges": edges,
    }
    open_rows = [r for r in rows if r["status_derived"] == "open"]
    absent = [r for r in open_rows if r.get("factory_default") is None]
    lines = [
        "DEFAULTS DECLARATION (s238-D5) — the `Defaults used:` lines the grill would carry.",
        "RULE " + DECLARE_RULE,
        "SENSE: `factory_default` is the GRILL's default (the value used because nothing was asked),",
        "       not s219-D3's shipped-option default — two senses already exist, so the field is named.",
        f"SOURCE OF \"WHICH SIDE IS CONSERVATIVE\": {OPEN_DEFAULTS_REL} (sha256 {defaults_sha[:16]}…)",
        "       carries NO per-row field for it. Its generator's docstring (_derive_open_table.py)",
        "       asserts every factory_default_proposed \"takes the conservative side\" — prose, not a",
        "       per-row datum. RULE APPLIED: bent = UNKNOWN for every row => nothing can be declared",
        "       as bent => 0 declared; every open row is UNPROVEN until the conservative side is",
        "       carried as data (Dave's).",
        f"open polarities: {len(open_rows)} · declared: 0 · UNPROVEN: {len(open_rows) - len(absent)} · "
        f"no proposal in the source: {len(absent)}",
        "Defaults used:",
        f"  (none — 0 of {len(open_rows)} bent from the conservative side; see UNPROVEN)",
        "UNPROVEN (conservative side not carried as data; the default text stays FLOATED in the source",
        "          and in polarity-status.json, it is NOT declared here):",
    ]
    for r in open_rows:
        if r.get("factory_default") is None:
            lines.append(f"  {r['id']} ({r['r1_id']}) NO PROPOSAL — {r.get('proposal')}")
        else:
            lines.append(f"  {r['id']} ({r['r1_id']}) {r.get('disposition')} — ask when: {r.get('ask_when')}")
    return {
        "polarity-status.json": render_json(status_body, generated_at),
        "polarity-edges.json": render_json(edges_body, generated_at),
        "defaults-declaration.txt": render_txt(lines, generated_at),
    }, counts, kind_counts, len(edges), len(open_rows)


# ============================================================================================
# FRESHNESS — content, never mtime; hand-written is a different verdict from stale
# ============================================================================================
def check_clock(name, gen_at, floor_date):
    """Q4 (#239): the clock is a CLOCK — ISO-8601 UTC, not in the future, not before the R1 asset."""
    if not isinstance(gen_at, str):
        raise Refused("R4-AUTHORED-GENERATED", f"{GEN_DIR}/{name}: generated_at is not a string — hand-written")
    try:
        t = datetime.datetime.strptime(gen_at, CLOCK_FMT).replace(tzinfo=datetime.timezone.utc)
    except ValueError:
        raise Refused("R4-AUTHORED-GENERATED", f"{GEN_DIR}/{name}: generated_at {gen_at[:40]!r} is not an "
                                               f"ISO-8601 UTC clock ({CLOCK_FMT}) — a derived file carries a "
                                               f"clock (s238-D3); this one was hand-written")
    now = datetime.datetime.now(datetime.timezone.utc)
    if (t - now).total_seconds() > CLOCK_SKEW_S:
        raise Refused("R4-AUTHORED-GENERATED", f"{GEN_DIR}/{name}: generated_at {gen_at} is in the future "
                                               f"(now {now.strftime(CLOCK_FMT)}, skew allowed {CLOCK_SKEW_S}s) "
                                               f"— a clock nobody could have derived at was hand-written")
    if floor_date:
        try:
            fl = datetime.datetime.strptime(floor_date[:10], "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc)
        except ValueError:
            fl = None
        if fl and t < fl:
            raise Refused("R4-AUTHORED-GENERATED", f"{GEN_DIR}/{name}: generated_at {gen_at} is before the "
                                                   f"R1 asset's own date {floor_date} — nothing could derive "
                                                   f"from a register that did not exist yet")


def read_generated(brain, name, floor_date=None):
    """(generated_at, text) or raises Refused MISSING / R4-AUTHORED-GENERATED."""
    path = os.path.join(brain, GEN_DIR, name)
    if not os.path.exists(path):
        raise Refused("MISSING-GENERATED", f"{GEN_DIR}/{name} is absent — run: python3 "
                                           f"knowledge/_validate_polarities.py --write")
    text = read_text(path)
    if name.endswith(".json"):
        try:
            obj = json.loads(text)
        except json.JSONDecodeError as e:
            raise Refused("R4-AUTHORED-GENERATED", f"{GEN_DIR}/{name} does not parse ({e}) — a "
                                                   f"generated file that does not parse was hand-"
                                                   f"written; delete it and run --write")
        if not isinstance(obj, dict) or obj.get("$header") != GEN_HEADER:
            raise Refused("R4-AUTHORED-GENERATED", f"{GEN_DIR}/{name} lacks the header "
                                                   f"{GEN_HEADER!r} — an AUTHORED file at a generated "
                                                   f"path (s238-D7 refusal 4); delete it and run --write")
        gen_at = obj.get("generated_at")
        body = {k: v for k, v in obj.items() if k not in ("$header", "generated_at", "content_sha256")}
        if obj.get("content_sha256") != sha256_text(canonical(body)):
            raise Refused("R4-AUTHORED-GENERATED", f"{GEN_DIR}/{name}: content_sha256 does not match "
                                                   f"its own body — the file was HAND-EDITED after "
                                                   f"generation (s238-D7 refusal 4); delete it and run "
                                                   f"--write")
        check_clock(name, gen_at, floor_date)
        return gen_at, text
    lines = text.split("\n")
    if len(lines) < 4 or lines[0] != GEN_HEADER or not lines[1].startswith("generated_at: ") \
            or not lines[2].startswith("content_sha256: ") or lines[3] != "---":
        raise Refused("R4-AUTHORED-GENERATED", f"{GEN_DIR}/{name} lacks the generated header block — "
                                               f"an AUTHORED file at a generated path (s238-D7 "
                                               f"refusal 4); delete it and run --write")
    body = "\n".join(lines[4:])
    if lines[2][len("content_sha256: "):] != sha256_text(body):
        raise Refused("R4-AUTHORED-GENERATED", f"{GEN_DIR}/{name}: content_sha256 does not match its "
                                               f"own body — HAND-EDITED after generation (s238-D7 "
                                               f"refusal 4); delete it and run --write")
    gen_at = lines[1][len("generated_at: "):]
    check_clock(name, gen_at, floor_date)
    return gen_at, text


def id_in_raw_text(nid, text):
    """Does this node id appear ANYWHERE in a generated file's bytes? (s240-D3, #242 lane P2.)

    ⚠ THIS IS THE LEAK CHECK V2 ASKED FOR, and it only became honest once `delta_vs_237T.cause`
    stopped being a hardcoded literal (delta_cause()). Until then a raw scan refused a CORRECTLY
    derived file, which is why lane P read rows only — a narrowing that let a retired pl-02 sit in
    polarity-status.json with the gate green. Word-bounded so `pl-02` does not match `pl-020`."""
    return re.search(r"(?<![A-Za-z0-9_-])" + re.escape(nid) + r"(?![A-Za-z0-9_-])", text) is not None


def generated_node_ids(name, text):
    """The node ids a generated file NAMES AS A ROW — read STRUCTURALLY. Kept beside
    id_in_raw_text() so a refusal can say WHICH position leaked: a derived row is a derivation bug,
    a raw-text-only hit is prose that was not derived from the live set."""
    try:
        if name == "polarity-status.json":
            return {r.get("id") for r in json.loads(text).get("rows", []) if isinstance(r, dict)}
        if name == "polarity-edges.json":
            return {e.get("polarity") for e in json.loads(text).get("edges", []) if isinstance(e, dict)}
    except (json.JSONDecodeError, AttributeError, TypeError):
        return set()
    return set(re.findall(r"^\s+(" + POLARITY_ID_PAT.strip("^$") + r") \(", text, re.M))


def freshness(brain, home, resolved, defaults, defaults_sha, floor_date=None):
    fails, notes, clocks = [], [], {}
    retired = retired_map(home)
    for name in GEN_FILES:
        try:
            gen_at, on_disk = read_generated(brain, name, floor_date)
        except Refused as r:
            fails.append((r.name, r.detail))
            continue
        clocks[name] = gen_at
        # s240-D3 (#242): a retired node DROPS OUT of everything generated. The freshness compare
        # below would say STALE; this says WHY by name, so the reader is not left to infer it.
        # The scan is ANYWHERE in the file's bytes, not just its rows (#242 lane P2, V2 finding 3):
        # "everything generated" is every BYTE, and every position in these three files is derived.
        named_rows = generated_node_ids(name, on_disk)
        for rid, by in sorted(retired.items()):
            in_row = rid in named_rows
            if in_row or id_in_raw_text(rid, on_disk):
                where = ("as a derived ROW" if in_row
                         else "in its text (not as a row — a leak a row-only check cannot see)")
                fails.append(("R4-RETIRED-GENERATED",
                              f"{GEN_DIR}/{name} still names {rid!r} {where}, a node RETIRED by ruling "
                              f"{by!r} — a retired node keeps its row in polarities.json and DROPS OUT of "
                              f"everything generated from the KG (s240-D3); run: python3 "
                              f"knowledge/_validate_polarities.py --write"))
        fresh, *_ = derive(home, resolved, defaults, defaults_sha, gen_at)
        if fresh[name] != on_disk:
            fails.append(("STALE-GENERATED", f"{GEN_DIR}/{name} does not match a fresh derivation "
                                             f"(content compared at its own clock {gen_at}) — run: "
                                             f"python3 knowledge/_validate_polarities.py --write"))
        else:
            notes.append(f"{GEN_DIR}/{name} fresh (generated_at {gen_at}, content byte-identical)")
    if len(clocks) == len(GEN_FILES) and len(set(clocks.values())) > 1:
        fails.append(("R4-AUTHORED-GENERATED", f"the three derived files carry different clocks {clocks} — "
                                               f"--write stamps them together; one was hand-edited"))
    return fails, notes


# ============================================================================================
# THE GATE — one entry point for the build, the seam, the writer and every selftest arm
# ============================================================================================
def print_refusals(fails, brain):
    print(f"⛔ POLARITY GATE REFUSED — {len(fails)} refusal(s) over {brain} (nothing written):")
    for name, detail in fails:
        print(f"   ⛔ REFUSED ({name}) — {detail}")


def source_repo_here():
    """Q8 (#239): the SOURCE repo carries the live store; a shipped pack never does (it is on the
    pack's excluded list). This is the honest discriminator — not `knowledge/`, which the pack ships."""
    return os.path.isfile(RULINGS)


def run_checks(brain, overrides=None):
    """Everything before freshness: (fails, home, resolved, register, dir_notes). Every crash
    inside is NAMED (Q7): S-SHAPE with the exception class — a crash is not a fail."""
    fails, notes, home, resolved, register = [], [], None, {}, None
    try:
        df, notes = check_home_dir(brain)
        fails += df
        home = load_home(brain, overrides)
        register = load_register()
        pf, resolved = check_polarities(home, register)
        fails += pf
    except Refused as r:
        fails.append((r.name, r.detail))
    except Exception as e:  # noqa: BLE001 — Q7: the catch-all names the crash instead of printing it
        tb = traceback.extract_tb(e.__traceback__)
        site = f"{os.path.basename(tb[-1].filename)}:{tb[-1].lineno} in {tb[-1].name}" if tb else "?"
        fails.append(("S-SHAPE", f"the gate could not finish reading {rel(brain)}: {type(e).__name__}: "
                                 f"{str(e)[:120]} (at {site}) — an input of a shape this gate does not "
                                 f"read; a crash is not a fail, so it is named here"))
    return fails, home, resolved, register, notes


def gate(brain, write=False, overrides=None, quiet=False):
    """The whole contract. Returns rc. Prints. Never raises on a refusal."""
    say = (lambda *a, **k: None) if quiet else print
    QUOTE_NOTES.clear()
    if not os.path.isdir(brain):
        if source_repo_here():
            # Q8 (#239): in the SOURCE repo an absent home is a MUTATION (a deleted knowledge/brain/
            # or a redirect to nowhere), never an environment fact — a refusal, rc 1, named.
            print_refusals([("S-SHAPE", f"home directory {rel(brain)} does not exist — this is the source "
                                        f"repo (knowledge/_rulings.json is here), so an absent home is a "
                                        f"mutation, not COULD-NOT-ASK (Q8, #239): restore knowledge/brain/ "
                                        f"or point --brain / POLARITY_BRAIN_DIR at a real home")], brain)
            return 1
        # #173 / #193 — the honest third verdict: the INPUT is not here (a shipped pack does not
        # carry knowledge/brain/), so the question is unaskable, not failed. Spelled so the pack
        # classifier's `_unshipped_subject` reads it as REPO-BOUND (a "does not exist" + the path).
        return cna.refuse(os.path.join(rel(brain), "polarities.json"),
                          f"the polarity home {rel(brain)}/ does not exist here — knowledge/brain/ is a repo "
                          f"resource a shipped pack does not carry, so the five refusals cannot be asked. "
                          f"Run from the source repo.")
    fails, home, resolved, register, dir_notes = run_checks(brain, overrides)
    if fails:
        print_refusals(fails, brain)
        return 1
    try:
        defaults, defaults_sha = open_defaults_rows()
    except FileNotFoundError:
        return cna.refuse("knowledge/brain/_generated/polarity-status.json",
                          f"the five refusals PASSED on {brain}, but the defaults declaration derives "
                          f"from {OPEN_DEFAULTS_REL}, which does not exist here (it lives outside "
                          f"knowledge/; a shipped pack does not carry it). Freshness is UNASKED, not "
                          f"passed. Run from the source repo.")
    floor_date = register[3]
    nodes = home["obj"]["polarities.json"]["polarities"]
    if write:
        texts, counts, kinds, n_edges, n_open = derive(home, resolved, defaults, defaults_sha, now_clock())
        gen_dir = os.path.join(brain, GEN_DIR)
        if os.path.exists(gen_dir) and not os.path.isdir(gen_dir):
            print_refusals([("R4-STRAY-FILE", f"{GEN_DIR} exists and is not a directory — nothing is blown "
                                              f"away; delete it and run --write")], brain)
            return 1
        os.makedirs(gen_dir, exist_ok=True)
        # an AUTHORED file at a generated path is refused even by --write: nothing is blown away
        for name in GEN_FILES:
            if os.path.exists(os.path.join(gen_dir, name)):
                try:
                    read_generated(brain, name, floor_date)
                except Refused as r:
                    if r.name == "R4-AUTHORED-GENERATED":
                        fails.append((r.name, r.detail))
        if fails:
            print_refusals(fails, brain)
            return 1
        for name in GEN_FILES:
            tmp = os.path.join(gen_dir, "." + name + ".tmp")
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(texts[name])
            os.replace(tmp, os.path.join(gen_dir, name))
        say(f"WROTE {len(GEN_FILES)} generated file(s) under {rel(gen_dir)}/ "
            f"(generated_at {json.loads(texts['polarity-status.json'])['generated_at']})")
    ff, notes = freshness(brain, home, resolved, defaults, defaults_sha, floor_date)
    _, counts, kinds, n_edges, n_open = derive(home, resolved, defaults, defaults_sha, "clock-held")
    n_links = sum(len(n.get("links", [])) for n in nodes)
    by_type = {}
    for n in nodes:
        for l in n.get("links", []):
            by_type[l["type"]] = by_type.get(l["type"], 0) + 1
    retired = retired_map(home)
    n_seed = sum(1 for n in nodes if isinstance(n.get("$seed"), str))
    say(f"polarity gate (s238-D7): home {rel(brain)} · "
        f"rows {len(nodes)} (live {len(nodes) - len(retired)} · retired {len(retired)}) · "
        f"parties {sum(kinds.values())} "
        f"(principle {kinds['principle']} · obligation {kinds['obligation']} · ruling {kinds['ruling']} · "
        f"stub {kinds['stub']}) · stubs declared {len(home['obj']['stubs.json']['stubs'])} · "
        f"links {n_links} by type " + " ".join(f"{k}={v}" for k, v in sorted(by_type.items()))
        + " · refusals asked: R1 R2 R3 R4 R5 — none fired")
    n_quotes = sum(1 for n in nodes for l in n.get("links", []) if isinstance(l.get("quote"), str))
    say(f"  quotes {n_quotes}: verbatim against their source rows in {R1_TENSIONS_REL} — {n_quotes} verified "
        f"(an unverifiable quote is refused, never declared — Q3 #239) · schema pinned {SCHEMA_SHA256[:12]}… "
        f"+ {len(SCHEMA_FLOORS)} floors · receipt $migration verified")
    say(f"  receipts (s240-D3): ONE pointer per node — R1 register row {len(nodes) - n_seed} · "
        f"$seed ruling id {n_seed} · retiredBy {len(retired)}"
        + (f" ({', '.join(f'{k}→{v}' for k, v in sorted(retired.items()))}, dropped from every "
           f"generated file)" if retired else ""))
    for k, v in STATUS_RULES.items():
        say(f"  RULE {k}: {v}")
    say(f"  status derived: settled-by-obligation {counts['settled-by-obligation']} · resolved "
        f"{counts['resolved']} · open {counts['open']}   (237-T at its clock: {T_SORT_FIGURE[0]})")
    say(f"  RULE EDGES: {EDGE_RULE}")
    say(f"  edges derived: {n_edges}")
    say(f"  {DECLARE_RULE}  open {n_open} · declared 0 · UNPROVEN {n_open} (conservative side not "
        f"carried as data)")
    for n in dir_notes:
        say(f"  ⚠ {n}")
    for n in notes:
        say(f"  ✓ {n}")
    if ff:
        print_refusals(ff, brain)
        return 1
    say("✓ polarity gate GREEN — five refusals asked and none fired; generated files content-fresh")
    return 0


# ============================================================================================
# THE WRITER — textual append into the home, proven by reconstruction (the _inscribe_ruling shape)
# ============================================================================================
def _array_bounds(text, key):
    """(open_index, close_index) of the `key` array, found by a string-aware depth scan."""
    start = text.index(f'"{key}"')
    i = text.index("[", start)
    depth, in_str, esc = 0, False, False
    for j in range(i, len(text)):
        c = text[j]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
            continue
        if c == '"':
            in_str = True
        elif c in "[{":
            depth += 1
        elif c in "]}":
            depth -= 1
            if depth == 0:
                return i, j
    raise Refused("S-SHAPE", f"could not find the close of the `{key}` array")


def compose_append(text, key, entry):
    """(new_text, at, span). Serialises ONLY the new entry; every other byte is carried through."""
    open_i, close = _array_bounds(text, key)
    inside = text[open_i + 1:close]
    body = json.dumps(entry, indent=1, ensure_ascii=False)
    body = "\n".join(" " + ln for ln in body.splitlines())
    if inside.strip() == "":
        span, at = "\n" + body + "\n", open_i + 1
    else:
        last_brace = open_i + 1 + inside.rindex("}")
        span, at = ",\n" + body, last_brace + 1
    return text[:at] + span + text[at:], at, span


def add_entry(brain, which, entry, write):
    """which ∈ {'polarity','stub'}. Returns rc; prints the proof or the refusal."""
    fname, key = ("polarities.json", "polarities") if which == "polarity" else ("stubs.json", "stubs")
    path = os.path.join(brain, fname)
    if not os.path.isfile(path):
        print(f"⛔ REFUSED (S-SHAPE) — {rel(path)} does not exist. Nothing written.")
        return 1
    try:
        original = read_text(path)
        new_text, at, span = compose_append(original, key, entry)
    except Refused as r:
        print(f"⛔ REFUSED ({r.name}) — {r.detail}. File untouched.")
        return 1
    if new_text[:at] + new_text[at + len(span):] != original:            # the reconstruction proof
        print("⛔ REFUSED (NOT-TEXTUAL) — removing the inserted span does not give back the original "
              "bytes; something reformatted the file (the #179 defect). File untouched.")
        return 1
    try:
        after = json.loads(new_text)
    except json.JSONDecodeError as e:
        print(f"⛔ REFUSED (S-PARSE) — the composed text does not parse: {e}. File untouched.")
        return 1
    before_n = len(json.loads(original)[key])
    if len(after[key]) != before_n + 1 or after[key][-1] != entry:
        print("⛔ REFUSED (ROUND-TRIP) — the result does not carry exactly one more entry equal to the "
              "one submitted. File untouched.")
        return 1
    # THE WHOLE GATE, on the resulting text, BEFORE a byte is written. The derived files are
    # EXPECTED to read stale against the appended home (nothing has re-derived them yet), so that
    # one verdict is folded into the write step; every other refusal stands and stops the append.
    buf, old = io.StringIO(), sys.stdout
    sys.stdout = buf
    try:
        rc = gate(brain, write=False, overrides={fname: new_text}, quiet=True)
    finally:
        sys.stdout = old
    only_stale = rc == 1 and _only_stale(brain, {fname: new_text})
    if rc != 0 and not only_stale:
        print(buf.getvalue(), end="")
        print(f"⛔ the gate REFUSED the home as it would stand after this append (rc {rc}) — see "
              f"the refusals above. File untouched.")
        return 1
    print(f"✓ append proven textual: {fname} +{len(span)} bytes at byte {at}; reconstruction == "
          f"original; parses to {before_n + 1} entries; the five refusals pass on the result"
          + ("; the derived files will re-derive on --write" if only_stale else ""))
    if not write:
        print("  (dry run — nothing written; pass --write to write and regenerate)")
        return 0
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(new_text)
    os.replace(tmp, path)
    print(f"WROTE {rel(path)}; regenerating the derived files:")
    return gate(brain, write=True)


def _only_stale(brain, overrides):
    """True when the ONLY refusals over the overridden home are STALE-GENERATED (expected: the
    append has not been derived yet)."""
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        fails, home, resolved, register, _ = run_checks(brain, overrides)
        if fails:
            return False
        defaults, sha = open_defaults_rows()
        ff, _ = freshness(brain, home, resolved, defaults, sha, register[3])
        return bool(ff) and all(n == "STALE-GENERATED" for n, _ in ff)
    except Exception:  # noqa: BLE001
        return False
    finally:
        sys.stdout = old


# ============================================================================================
# SELFTEST — control + one arm per refusal + extras, ALL driven through gate() (the same entry
# point the build and the commit seam call) on a COPY of the REAL rows. Every arm must go RED
# by its NAME; a crash is not a fail. Arms marked V<n> replay lane V's #238 attacks (#239 lane F).
# ============================================================================================
ZWSP = "\u200b"


def _copy_brain(src, dst):
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", ".*.tmp"))


def _mutate_json(path, fn):
    obj = json.loads(read_text(path))
    fn(obj)
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(obj, indent=1, ensure_ascii=False) + "\n")


def _rewrite(path, fn):
    t = read_text(path)
    with open(path, "w", encoding="utf-8") as f:
        f.write(fn(t))


def _run_gate_captured(brain, write=False, overrides=None):
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        try:
            rc = gate(brain, write=write, overrides=overrides)
        except Exception:               # a crash is not a fail — surface it as one, named
            rc = -1
            buf.write("TRACEBACK\n" + traceback.format_exc())
    finally:
        sys.stdout = old
    return rc, buf.getvalue()


def _tree_hashes(root):
    out = {}
    for dp, _dn, fns in os.walk(root):
        for fn in fns:
            p = os.path.join(dp, fn)
            if os.path.islink(p):
                out[os.path.relpath(p, root)] = "link:" + os.readlink(p)
                continue
            with open(p, "rb") as f:
                out[os.path.relpath(p, root)] = sha256_bytes(f.read())
    return out


def selftest(real_brain):
    if not os.path.isdir(real_brain):
        print(f"⛔ REFUSED (S-SHAPE) — --selftest needs a real home to copy; {rel(real_brain)} does not exist")
        return 1
    results = []          # (n, arm, expected, rc, named?, ok, note)
    tmp_root = tempfile.mkdtemp(prefix="polarity-selftest-", dir="/dev/shm" if os.path.isdir("/dev/shm") else None)
    try:
        _selftest_arms(real_brain, tmp_root, results)
    finally:
        shutil.rmtree(tmp_root, ignore_errors=True)     # V finding 16: on EVERY path
    print("=" * 100)
    print("_validate_polarities.py --selftest — every arm drives gate() on a copy of the REAL rows")
    print("=" * 100)
    print(f"{'#':>3}  {'result':6}  {'expect':6}  {'rc':>4}  {'named':5}  arm")
    fails = 0
    for n, name, expect, rc, named, ok, note in results:
        if not ok:
            fails += 1
        print(f"{n:>3}  {'PASS' if ok else 'FAIL':6}  {expect:6}  {str(rc):>4}  {('yes' if named else '-'):5}  {name}")
        if note and (not ok or note.startswith("SKIPPED")):
            print("        " + note.replace("\n", "\n        "))
    red_arms = [r for r in results if r[2] == "red"]
    red_ok = [r for r in red_arms if r[5]]
    green_arms = [r for r in results if r[2] == "green"]
    new_arms = [r for r in results if r[1].startswith("V") or "(#239" in r[1]]
    p242_arms = [r for r in results if "#242" in r[1] or r[1].startswith("s240-D3")]
    p243_arms = [r for r in results if "#243" in r[1] or "s243-D1" in r[1]]
    print("-" * 100)
    print(f"arms {len(results)} · red arms {len(red_arms)} (went red by name {len(red_ok)}/{len(red_arms)}) · "
          f"green arms {len(green_arms)} · no-fire/77 arms {len(results) - len(red_arms) - len(green_arms)} · "
          f"new #239 arms {len(new_arms)} · new #242 (s240-D3 receipt) arms {len(p242_arms)} · "
          f"new #243 (s243-D1 six controls) arms {len(p243_arms)} · failures {fails}")
    if fails:
        print(f"✗ selftest FAILED — {fails} arm(s)")
        return 1
    print("✓ selftest OK — control green; every refusal arm red by its name; nothing written on refusal")
    return 0


def _selftest_arms(real_brain, tmp_root, results):
    global SCHEMA_SHA256, RULINGS, OPEN_DEFAULTS, check_stubs   # moved in-process by four arms, restored in finally

    def arm(name, expect, mutate, must_name=None, write=False, must_not=None, must_detail=None):
        """Copy the REAL brain, apply `mutate(copy_dir)`, drive gate(--check) on it.
        `must_detail` (#243 Q2, V3 finding 1): a red arm may also pin the CLAUSE — a substring of the
        refusal's detail text — so a family name shared by several clauses cannot mask the loss of
        the one the arm was written for."""
        n = len(results) + 1
        d = os.path.join(tmp_root, f"arm{n:03d}")
        _copy_brain(real_brain, d)
        try:
            mutate(d)
        except Exception as e:  # noqa: BLE001
            results.append((n, name, expect, None, False, False, f"mutation setup crashed: {e!r}"))
            return
        after_mut = _tree_hashes(d)
        rc, out = _run_gate_captured(d, write=write)
        after = _tree_hashes(d)
        crashed = "TRACEBACK" in out or "Traceback (most recent" in out
        names = set(re.findall(r"REFUSED \(([A-Za-z0-9-]+)\)", out))
        wanted = [must_name] if isinstance(must_name, str) else list(must_name or [])
        named = bool(wanted) and all(w in names for w in wanted)
        unwanted = must_not in names if must_not else False
        if expect == "green":
            ok = rc == 0 and not crashed and not unwanted
            note = "" if ok else out[-600:]
        else:
            untouched = (after == after_mut)
            detailed = (must_detail is None) or (must_detail in out)
            ok = (rc == 1) and named and detailed and not crashed and untouched and not unwanted
            note = ("" if ok else f"rc={rc} named={named} (names={sorted(names)} wanted={wanted}) "
                                  f"detailed={detailed} (must_detail={must_detail!r}) "
                                  f"crashed={crashed} untouched={untouched} :: " + out[-500:])
        results.append((n, name, expect, rc, named, ok, note))
        return d

    def pol(fn):
        return lambda d: _mutate_json(os.path.join(d, "polarities.json"), fn)

    def stubs(fn):
        return lambda d: _mutate_json(os.path.join(d, "stubs.json"), fn)

    def schema(fn):
        return lambda d: _mutate_json(os.path.join(d, SCHEMA_REL), fn)

    def both(*fns):
        return lambda d: [f(d) for f in fns]

    def wfile(relpath, text, mode="w"):
        def _w(d):
            p = os.path.join(d, relpath)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, mode, **({} if "b" in mode else {"encoding": "utf-8"})) as f:
                f.write(text)
        return _w

    # ---- CONTROL ------------------------------------------------------------------------------
    arm("CONTROL: the real 30 rows, untouched", "green", lambda d: None)

    # ---- R1 -----------------------------------------------------------------------------------
    arm("R1 dangling PARTY ref (pr-does-not-exist)", "red",
        pol(lambda o: o["polarities"][0]["parties"].append({"ref": "pr-does-not-exist", "role": "side_b"})),
        "R1-DANGLING")
    arm("R1 dangling LINK ref (s999-D9)", "red",
        pol(lambda o: o["polarities"][0]["links"].append({"type": "touches", "ref": "s999-D9"})),
        "R1-DANGLING")
    rulings_now = json.loads(read_text(RULINGS))["rulings"]
    store = {r["id"]: r for r in rulings_now if isinstance(r, dict) and isinstance(r.get("id"), str)}
    superseded = [r["id"] for r in rulings_now if isinstance(r, dict) and r.get("superseded_by")]
    if superseded:
        arm(f"R1 link to a SUPERSEDED ruling ({superseded[0]}, real store)", "red",
            pol(lambda o: o["polarities"][0]["links"].append({"type": "touches", "ref": superseded[0]})),
            "R1-SUPERSEDED")
        arm(f"R1 PARTY that is a superseded ruling ({superseded[0]})", "red",
            pol(lambda o: o["polarities"][0]["parties"].append({"ref": superseded[0], "role": "side_b"})),
            "R1-SUPERSEDED")
    else:
        results.append((len(results) + 1, "R1 superseded ruling arm", "red", None, False, False,
                        "no ruling in knowledge/_rulings.json carries `superseded_by` — the arm cannot "
                        "be driven on real data; UNPROVEN, not passed"))
    # V30 — superseded in PROSE only (no field); V31/V32 — status text OPEN/PARKED/…; both real-store
    prose = prose_supersessions(store)
    prose_only = sorted(k for k in prose if not store[k].get("superseded_by"))
    if prose_only:
        tgt = "s200-D2" if "s200-D2" in prose_only else prose_only[0]
        arm(f"V30 R1 resolvedBy a ruling superseded in the store's PROSE only ({tgt}) (#239 Q1)", "red",
            pol(lambda o: o["polarities"][2]["links"].append(
                {"type": "resolvedBy", "ref": tgt, "quote": "Chart hover latency and skeleton states"})),
            "R1-SUPERSEDED")
    else:
        results.append((len(results) + 1, "V30 R1 prose-superseded arm", "red", None, False, False,
                        "no ruling is superseded in prose without the field — UNPROVEN, not passed"))
    not_live = sorted(k for k, r in store.items() if NOT_LIVE.search(str(r.get("status", "")))
                      and not r.get("superseded_by") and k not in prose)
    if not_live:
        tgt2 = "gauge-band" if "gauge-band" in not_live else not_live[0]
        arm(f"V31 R1 resolvedBy a ruling whose status says OPEN/PARKED/DEFERRED/FORKED ({tgt2}) (#239 Q1)", "red",
            pol(lambda o: o["polarities"][2]["links"].append(
                {"type": "resolvedBy", "ref": tgt2, "quote": "Chart hover latency and skeleton states"})),
            "R1-DANGLING")
        arm(f"V31-control: the SAME ruling as `touches` is fine — only a resolvedBy closes (#239 Q1)", "green",
            both(pol(lambda o: o["polarities"][2]["links"].append({"type": "touches", "ref": tgt2})),
                 lambda d: _run_gate_captured(d, write=True)))
    else:
        results.append((len(results) + 1, "V31 R1 not-live arm", "red", None, False, False,
                        "no ruling's status carries OPEN/PARKED/DEFERRED/FORKED — UNPROVEN, not passed"))
    arm("R1 SELF-PARTY (pl-01 lists itself)", "red",
        pol(lambda o: o["polarities"][0]["parties"].append({"ref": "pl-01", "role": "side_b"})),
        "R1-SELF-PARTY")
    arm("R1 CIRCULAR polarity→polarity LINK (pl-01 → pl-02)", "red",
        pol(lambda o: o["polarities"][0]["links"].append({"type": "touches", "ref": "pl-02"})),
        "R1-CIRCULAR")
    arm("R1 CIRCULAR polarity as a PARTY of another (pl-02 on pl-01)", "red",
        pol(lambda o: o["polarities"][0]["parties"].append({"ref": "pl-02", "role": "side_b"})),
        "R1-CIRCULAR")
    arm("R1 link to a PRINCIPLE id (wrong register)", "red",
        pol(lambda o: o["polarities"][0]["links"].append({"type": "touches", "ref": "pr-fitts"})),
        "R1-WRONG-REGISTER")
    arm("R1 undeclared STUB (st-not-declared)", "red",
        pol(lambda o: o["polarities"][0]["parties"].append({"ref": "st-not-declared", "role": "side_b"})),
        "R1-UNDECLARED-STUB")
    arm("R1 a declared stub REMOVED from stubs.json (pl-05's party dangles)", "red",
        stubs(lambda o: o["stubs"].__delitem__(next(i for i, s in enumerate(o["stubs"])
                                                    if s["id"] == "st-input-validation-and-security"))),
        "R1-UNDECLARED-STUB")
    homoglyph = "pr-jakobs-law".replace("a", "а")     # Cyrillic а — looks identical, is not ASCII
    assert homoglyph != "pr-jakobs-law", "selftest setup: the homoglyph mutation produced no change"
    arm("R1 homoglyph ref (Cyrillic а in pr-jakobs-law) — non-ASCII id", "red",
        pol(lambda o: o["polarities"][1]["parties"].append({"ref": homoglyph, "role": "side_b"})),
        "S-ID")

    # ---- R2 -----------------------------------------------------------------------------------
    arm("R2 UNTYPED link (type key absent)", "red",
        pol(lambda o: o["polarities"][0]["links"].append({"ref": "s116-D1"})),
        "R2-UNTYPED")
    arm("V200 R2 UNTYPED link that is a bare string (#239 misnamed→named)", "red",
        pol(lambda o: o["polarities"][0]["links"].append("s116-D1")), "R2-UNTYPED")
    arm("V201 R2 UNTYPED link with type null (#239 misnamed→named)", "red",
        pol(lambda o: o["polarities"][0]["links"].append({"type": None, "ref": "s116-D1"})), "R2-UNTYPED")
    arm("V202 R2 link type is a LIST — named, no crash (#239 Q7)", "red",
        pol(lambda o: o["polarities"][0]["links"].append({"type": ["touches"], "ref": "s116-D1"})),
        "R2-UNKNOWN-TYPE")
    arm("R2 UNKNOWN (fifth) link type `relatedTo`", "red",
        pol(lambda o: o["polarities"][0]["links"].append({"type": "relatedTo", "ref": "s116-D1"})),
        "R2-UNKNOWN-TYPE")
    arm("R2 link type wrong case `ResolvedBy`", "red",
        pol(lambda o: o["polarities"][0]["links"].append({"type": "ResolvedBy", "ref": "s116-D1"})),
        "R2-UNKNOWN-TYPE")
    arm("R2 link type empty string", "red",
        pol(lambda o: o["polarities"][0]["links"].append({"type": "", "ref": "s116-D1"})),
        "R2-UNKNOWN-TYPE")

    # ---- R3 -----------------------------------------------------------------------------------
    arm("R3 judgement field `how_it_resolves` on a node", "red",
        pol(lambda o: o["polarities"][0].__setitem__("how_it_resolves", "Never trade them at the same layer.")),
        "R3-JUDGEMENT-FIELD")
    arm("R3 judgement field of ANOTHER name (`verdict`)", "red",
        pol(lambda o: o["polarities"][3].__setitem__("verdict", "aesthetics wins")),
        "R3-JUDGEMENT-FIELD")
    arm("R3 judgement smuggled into a link `quote` (16 words)", "red",
        pol(lambda o: o["polarities"][0]["links"].append(
            {"type": "touches", "ref": "s116-D1", "quote": " ".join(["word"] * 16)})),
        "R3-QUOTE-TOO-LONG")
    arm("R3 judgement smuggled into a party `note` (16 words)", "red",
        pol(lambda o: o["polarities"][0]["parties"][0].__setitem__("note", " ".join(["word"] * 16))),
        "R3-NOTE-TOO-LONG")
    arm("R3 judgement field inside a PARTY object (`why`)", "red",
        pol(lambda o: o["polarities"][0]["parties"][0].__setitem__("why", "because")),
        "R3-JUDGEMENT-FIELD")
    arm("R3 stub with a third key (`rationale`)", "red",
        stubs(lambda o: o["stubs"][0].__setitem__("rationale", "x")),
        "S-STUB-SHAPE")
    arm("R3 link quote PARAPHRASED (not verbatim in the source row)", "red",
        pol(lambda o: o["polarities"][0]["links"][0].__setitem__("quote", "the two-red law is a Von Restorff budget")),
        "R3-QUOTE-NOT-VERBATIM")
    arm("V230 R3 party note that is a 14-word verdict, not verbatim in the source row (#239 Q5)", "red",
        pol(lambda o: o["polarities"][0]["parties"][0].__setitem__(
            "note", "Jakob must always win in Apollo because Dave rules by eye and prefers familiarity")),
        "R3-JUDGEMENT-FIELD")
    arm("V231 R3 note of 44 visible words joined by U+200B — counted AND the character refused (#239 Q5)", "red",
        pol(lambda o: o["polarities"][0]["parties"][0].__setitem__(
            "note", ZWSP.join(["Jakob", "must", "always", "win", "in", "Apollo", "because", "Dave", "rules", "by", "eye"] * 4))),
        ["R3-NOTE-TOO-LONG", "S-FORMAT-CHAR"])
    arm("V232 R3 mediating_variable of 300 words (#239 Q5: maxWords 25 FLOATED + verbatim)", "red",
        pol(lambda o: o["polarities"][0].__setitem__(
            "mediating_variable", " ".join(["Jakob wins and Von Restorff loses in every Apollo review."] * 30))),
        "R3-JUDGEMENT-FIELD")
    arm("V232b R3 mediating_variable rewritten (short, not verbatim in the source row) (#239 Q5)", "red",
        pol(lambda o: o["polarities"][0].__setitem__("mediating_variable", "Jakob wins, always")),
        "R3-JUDGEMENT-FIELD")
    arm("V233 R3 sources[0].id that is a 300-word verdict (#239 Q5: patterned + maxWords 1)", "red",
        pol(lambda o: o["polarities"][3]["sources"][0].__setitem__(
            "id", " ".join(["aesthetics wins over usability in Apollo, always."] * 30))),
        ["S-ID", "R3-JUDGEMENT-FIELD"])
    arm("V234 R3 stub phrase that is a 15-word verdict — not verbatim in the register (#239 Q5)", "red",
        stubs(lambda o: o["stubs"].append({"id": "st-dense-tables-win",
                                           "phrase": "dense financial tables must always beat whitespace in "
                                                     "Apollo because Dave prefers density everywhere"})),
        "R3-JUDGEMENT-FIELD")
    arm("V22 R3/S stub whose phrase is one U+200B (visually empty) (#239 Q5)", "red",
        stubs(lambda o: o["stubs"].append({"id": "st-zwsp", "phrase": ZWSP})),
        ["S-STUB-SHAPE", "S-FORMAT-CHAR"])
    arm("V82 R3 $migration gains a nested `verdicts` map (#239 Q5: shape-fixed)", "red",
        pol(lambda o: o["$migration"].__setitem__("verdicts", {"pl-01": "Jakob wins in Apollo"})),
        "R3-JUDGEMENT-FIELD")
    arm("V83 R3 $description replaced by 500 words of verdict (#239 Q5: maxWords FLOATED)", "red",
        pol(lambda o: o.__setitem__("$description", " ".join(["Aesthetics must win over usability."] * 100))),
        "R3-JUDGEMENT-FIELD")
    arm("V246 S-RECEIPT $migration.sha256 = 64 zeros — the receipt is verified (#239 Q5)", "red",
        pol(lambda o: o["$migration"].__setitem__("sha256", "0" * 64)), "S-RECEIPT")
    arm("V247 S-RECEIPT $migration.from = a path that does not exist (#239 Q5)", "red",
        pol(lambda o: o["$migration"].__setitem__("from", "notes/does-not-exist.json")), "S-RECEIPT")

    # ---- Q3 — THE QUOTE ORACLE ----------------------------------------------------------------
    arm("V220 R3 sources repointed at _rulings.json + 13 words OF THE RULING as the quote (#239 Q3)", "red",
        pol(lambda o: (o["polarities"][0].__setitem__("sources", [{"path": "knowledge/_rulings.json", "id": "s238-D7"}]),
                       o["polarities"][0]["links"][0].__setitem__("quote", "A gate that is not a consumer of every commit is not a gate"))),
        ["S-SOURCE", "R3-QUOTE-NOT-VERBATIM"])
    arm("V300 R3 sources repointed at polarities.json itself + its own words as the quote (#239 Q3)", "red",
        pol(lambda o: (o["polarities"][0].__setitem__("sources", [{"path": "knowledge/brain/polarities.json", "id": "pl-01"}]),
                       o["polarities"][0]["links"][0].__setitem__("quote", " ".join(o["polarities"][0]["mediating_variable"].split()[:8])))),
        ["S-SOURCE", "R3-QUOTE-NOT-VERBATIM"])
    arm("V222 R3 paraphrase + source pointer broken (path → nowhere): UNVERIFIABLE is refused (#239 Q3)", "red",
        pol(lambda o: (o["polarities"][0]["sources"][0].__setitem__("path", "notes/no-such-file.json"),
                       o["polarities"][0]["links"][0].__setitem__("quote", "the two-red law is a Von Restorff budget"))),
        ["S-SOURCE", "R3-QUOTE-NOT-VERBATIM"])
    arm("V93 S-ID sources[0].id with a fullwidth digit (tn-0１) — the pointer cannot be laundered (#239 Q3)", "red",
        pol(lambda o: o["polarities"][0]["sources"][0].__setitem__("id", "tn-0１")),
        ["S-ID", "R3-QUOTE-NOT-VERBATIM"])
    arm("V223 R3 resolvedBy with quote \"\" (#239 Q3)", "red",
        pol(lambda o: o["polarities"][0]["links"].append({"type": "resolvedBy", "ref": "s116-D1", "quote": ""})),
        "R3-QUOTE-NOT-VERBATIM")
    arm("V224 R3 resolvedBy with the one-word quote \"the\" (#239 Q3: minWords 3 FLOATED)", "red",
        pol(lambda o: o["polarities"][0]["links"].append({"type": "resolvedBy", "ref": "s116-D1", "quote": "the"})),
        "R3-QUOTE-NOT-VERBATIM")
    arm("V400 R3 resolvedBy with NO quote at all — a resolvedBy needs a receipt (#239 Q3)", "red",
        pol(lambda o: o["polarities"][0]["links"].append({"type": "resolvedBy", "ref": "s116-D1"})),
        "R3-QUOTE-MISSING")
    arm("V400-control: a `touches` with no quote stays legal (#239 Q3)", "green",
        both(pol(lambda o: o["polarities"][0]["links"].append({"type": "touches", "ref": "s116-D1"})),
             lambda d: _run_gate_captured(d, write=True)))
    arm("V401 S-SOURCE pl-04's source id swapped to tn-02 — one row, one node (#239 Q3)", "red",
        pol(lambda o: o["polarities"][3]["sources"][0].__setitem__("id", "tn-02")), "S-SOURCE")
    arm("V402 S-SOURCE pl-01's body duplicated under pl-31 — the row is claimed twice (#239 Q3)", "red",
        pol(lambda o: o["polarities"].append(dict(o["polarities"][0], id="pl-31"))), "S-SOURCE")
    arm("V244 S-SOURCE all 30 rows deleted — 30 frozen rows claimed by no node (#239 Q3)", "red",
        pol(lambda o: o.__setitem__("polarities", [])), "S-SOURCE")
    arm("V225 S-SOURCE a source path outside the repo (/etc/hostname) (#239 Q3)", "red",
        pol(lambda o: o["polarities"][0]["sources"].append({"path": "/etc/hostname", "id": "x"})),
        ["S-ID", "S-SOURCE"])

    # ---- Q5 — FORMAT CHARACTERS EVERYWHERE ------------------------------------------------------
    arm("S-FORMAT-CHAR a soft hyphen (U+00AD) inside a party ref (#239 Q5)", "red",
        pol(lambda o: o["polarities"][0]["parties"][0].__setitem__("ref", "pr-jakobs\u00ad-law")),
        "S-FORMAT-CHAR")
    arm("S-FORMAT-CHAR a right-to-left override (U+202E) in $description (#239 Q5)", "red",
        pol(lambda o: o.__setitem__("$description", o["$description"] + "\u202e")), "S-FORMAT-CHAR")
    arm("S-FORMAT-CHAR a NUL (U+0000) in a stub phrase (#239 Q5)", "red",
        stubs(lambda o: o["stubs"][0].__setitem__("phrase", o["stubs"][0]["phrase"] + "\x00")), "S-FORMAT-CHAR")

    # ---- R4 -----------------------------------------------------------------------------------
    arm("R4 AUTHORED file at the generated path (no header)", "red",
        wfile(os.path.join(GEN_DIR, "polarity-edges.json"),
              json.dumps({"edges": [{"from": "pr-fitts", "to": "pr-hick"}]}, indent=1) + "\n"),
        "R4-AUTHORED-GENERATED")

    def hand_edited_generated(d):
        p = os.path.join(d, GEN_DIR, "polarity-status.json")
        obj = json.loads(read_text(p))
        obj["rows"][0]["status_derived"] = "resolved"        # header kept, body changed by hand
        with open(p, "w", encoding="utf-8") as f:
            f.write(json.dumps(obj, indent=1, ensure_ascii=False) + "\n")
    arm("R4 generated file HAND-EDITED under its header (self-sha breaks)", "red",
        hand_edited_generated, "R4-AUTHORED-GENERATED")
    arm("R4 AUTHORED edge file beside the homes (knowledge/brain/edges.json)", "red",
        wfile("edges.json", json.dumps({"edges": []}) + "\n"), "R4-AUTHORED-EDGES")
    arm("R4 STRAY second shape beside the homes (polarities-v2.json)", "red",
        wfile("polarities-v2.json", "{}\n"), "R4-STRAY-FILE")
    arm("R4 AUTHORED file INSIDE _generated/ beside the derived three", "red",
        wfile(os.path.join(GEN_DIR, "polarity-edges-extra.json"), json.dumps({"edges": []}) + "\n"),
        "R4-STRAY-FILE")

    def txt_hand_edited(d):
        _rewrite(os.path.join(d, GEN_DIR, "defaults-declaration.txt"),
                 lambda t: t.replace("Defaults used:\n", "Defaults used:\n  pl-01 — converge on mechanism\n"))
    arm("R4 defaults-declaration.txt HAND-EDITED (a default declared by hand)", "red",
        txt_hand_edited, "R4-AUTHORED-GENERATED")
    # V's six open edges of the closed directory (Q6)
    arm("V210 R4 dotfile `.edges.json` at the brain top — dotfiles are LISTED (#239 Q6)", "red",
        wfile(".edges.json", json.dumps({"edges": [{"from": "pr-fitts", "to": "pr-hick"}]}) + "\n"),
        "R4-AUTHORED-EDGES")
    arm("V211 R4 dotfile inside _generated/ (#239 Q6)", "red",
        wfile(os.path.join(GEN_DIR, ".authored-edges.json"), json.dumps({"edges": []}) + "\n"),
        "R4-STRAY-FILE")
    arm("V212 R4 a half-written `.polarity-edges.json.tmp` inside _generated/ (#239 Q6)", "red",
        wfile(os.path.join(GEN_DIR, ".polarity-edges.json.tmp"), '{"edges": [1]}\n'), "R4-STRAY-FILE")
    arm("V213 R4 an authored edge list under schema/ — schema/ is LISTED (#239 Q6)", "red",
        wfile(os.path.join("schema", "edges.json"), json.dumps({"edges": [{"from": "pr-fitts", "to": "pr-hick"}]}) + "\n"),
        "R4-AUTHORED-EDGES")
    arm("V214 R4 a second schema under schema/ — exactly one schema (#239 Q6)", "red",
        wfile(os.path.join("schema", "polarity.schema.v2.json"), '{"minItems": 1}\n'), "R4-STRAY-FILE")
    arm("V216 R4 __pycache__/ under the home (#239 Q6)", "red",
        wfile(os.path.join("__pycache__", "edges.json"), json.dumps({"edges": []}) + "\n"), "R4-STRAY-FILE")

    def symlink_home(d):
        p = os.path.join(d, "polarities.json")
        shutil.move(p, os.path.join(d, "..", f"moved-{os.path.basename(d)}.json"))
        os.symlink(os.path.join(d, "..", f"moved-{os.path.basename(d)}.json"), p)
    arm("V403 R4 polarities.json replaced by a SYMLINK to a file outside the home (#239 Q6)", "red",
        symlink_home, "R4-STRAY-FILE")

    def gen_is_a_file(d):
        shutil.move(os.path.join(d, GEN_DIR), os.path.join(d, "..", f"gen-{os.path.basename(d)}"))
        with open(os.path.join(d, GEN_DIR), "w", encoding="utf-8") as f:
            f.write("authored\n")
    arm("V217 R4 _generated is a FILE — named at --check (#239 Q6/Q7)", "red", gen_is_a_file, "R4-STRAY-FILE")
    arm("V217w R4 _generated is a FILE — --write refuses by name, no crash, nothing written (#239 Q7)", "red",
        gen_is_a_file, "R4-STRAY-FILE", write=True)
    arm("Q6 `.DS_Store` with Finder's magic bytes is IGNORED, declared (#239 Q6)", "green",
        wfile(".DS_Store", DSSTORE_MAGIC + b"\x00" * 32, mode="wb"))
    arm("Q6 a JSON edge list wearing the name `.DS_Store` is refused (#239 Q6)", "red",
        wfile(".DS_Store", json.dumps({"edges": []}) + "\n"), "R4-AUTHORED-EDGES")

    # ---- R5 -----------------------------------------------------------------------------------
    arm("R5 typed `status` on a node", "red",
        pol(lambda o: o["polarities"][0].__setitem__("status", "open")), "R5-TYPED-STATUS")
    arm("R5 typed status under another spelling (`derivedStatus`)", "red",
        pol(lambda o: o["polarities"][0].__setitem__("derivedStatus", "resolved")), "R5-TYPED-STATUS")

    # ---- SCHEMA EXTRAS -------------------------------------------------------------------------
    arm("S 1 party (minItems 2)", "red",
        pol(lambda o: o["polarities"][0].__setitem__("parties", o["polarities"][0]["parties"][:1])),
        "S-MIN-PARTIES")
    arm("S DUPLICATE party (same ref twice on pl-01)", "red",
        pol(lambda o: o["polarities"][0]["parties"].append(dict(o["polarities"][0]["parties"][0]))),
        "S-DUP-PARTY")
    arm("S DUPLICATE polarity id", "red",
        pol(lambda o: o["polarities"].append(dict(o["polarities"][0]))), "S-DUP-ID")
    arm("S unicode polarity id (fullwidth digit)", "red",
        pol(lambda o: o["polarities"][0].__setitem__("id", "pl-0１")), "S-ID")
    arm("S party role outside the enum (`side_d`)", "red",
        pol(lambda o: o["polarities"][0]["parties"][0].__setitem__("role", "side_d")), "S-ROLE")
    arm("V42 S party role null — named S-ROLE (#239 misnamed→named)", "red",
        pol(lambda o: o["polarities"][0]["parties"][0].__setitem__("role", None)), "S-ROLE")
    arm("V44 S party role is an OBJECT — named, no crash (#239 Q7)", "red",
        pol(lambda o: o["polarities"][0]["parties"][0].__setitem__("role", {"side": "a"})), "S-SCHEMA")
    arm("V203 S party ref is a LIST — named, no crash (#239 Q7)", "red",
        pol(lambda o: o["polarities"][0]["parties"].append({"ref": ["pr-fitts"], "role": "side_c"})), "S-SCHEMA")
    arm("V204 S stub id is a LIST — named, no crash (#239 Q7)", "red",
        stubs(lambda o: o["stubs"].append({"id": ["st-x"], "phrase": "x"})), "S-STUB-SHAPE")
    arm("V250 S sources item without `path` on a node with a quote — named, no crash (#239 Q7)", "red",
        pol(lambda o: o["polarities"][0].__setitem__("sources", [{"id": "tn-01"}])), "S-SCHEMA")
    arm("V251 S sources[0].path is an int — named, no crash (#239 Q7)", "red",
        pol(lambda o: o["polarities"][0]["sources"][0].__setitem__("path", 5)), "S-SCHEMA")
    arm("S ONE-SIDED: every party on side_a (no pull)", "red",
        pol(lambda o: [p.__setitem__("role", "side_a") for p in o["polarities"][0]["parties"]]),
        "S-ONE-SIDED")
    arm("S mediating_variable empty", "red",
        pol(lambda o: o["polarities"][0].__setitem__("mediating_variable", "")), "S-SCHEMA")
    # (#242, s240-D3): `sources` is no longer `required` in the schema — the floor moved into code.
    # Deleting it leaves the node with NO receipt, which is S-SOURCE, not S-SCHEMA.
    arm("S sources missing — no receipt at all (s240-D3 re-cut of the #239 S-SCHEMA arm)", "red",
        pol(lambda o: o["polarities"][0].__delitem__("sources")), "S-SOURCE")
    arm("S polarities.json does not parse", "red",
        lambda d: open(os.path.join(d, "polarities.json"), "a").write("{"), "S-PARSE")
    arm("V252 S polarities.json carries one non-UTF-8 byte — S-PARSE, no traceback (#239 Q7)", "red",
        lambda d: open(os.path.join(d, "polarities.json"), "wb").write(
            open(os.path.join(d, "polarities.json"), "rb").read().replace(b"pr-jakobs-law", b"pr-jakobs-l\xe1w", 1)),
        "S-PARSE")

    # ---- Q2 — THE SCHEMA IS PINNED: sha + floors; a loosening is refused AND the floor still bites
    arm("V110 SCHEMA parties.minItems 2→1 + a one-party row: LOOSENED named, S-MIN-PARTIES still fires (#239 Q2)", "red",
        both(schema(lambda s: s["properties"]["parties"].__setitem__("minItems", 1)),
             pol(lambda o: o["polarities"][0].__setitem__("parties", o["polarities"][0]["parties"][:1]))),
        ["SCHEMA-LOOSENED", "S-MIN-PARTIES", "SCHEMA-PIN-MISMATCH"])
    arm("V111 SCHEMA enum widened with a fifth type + a relatedTo link (#239 Q2)", "red",
        both(schema(lambda s: s["properties"]["links"]["items"]["properties"]["type"]["enum"].append("relatedTo")),
             pol(lambda o: o["polarities"][0]["links"].append({"type": "relatedTo", "ref": "s116-D1"}))),
        ["SCHEMA-LOOSENED", "R2-UNKNOWN-TYPE"])
    arm("V112 SCHEMA parties.items.additionalProperties true + a `why` on a party (#239 Q2)", "red",
        both(schema(lambda s: s["properties"]["parties"]["items"].__setitem__("additionalProperties", True)),
             pol(lambda o: o["polarities"][0]["parties"][0].__setitem__("why", "because Jakob wins in Apollo"))),
        ["SCHEMA-LOOSENED", "R3-JUDGEMENT-FIELD"])
    arm("V310 SCHEMA sources.items.additionalProperties true + a `judgement` on a source (V's TOTAL escape) (#239 Q2)", "red",
        both(schema(lambda s: s["properties"]["sources"]["items"].__setitem__("additionalProperties", True)),
             pol(lambda o: o["polarities"][0]["sources"][0].__setitem__("judgement", "Jakob wins in Apollo"))),
        ["SCHEMA-LOOSENED", "R3-JUDGEMENT-FIELD"])
    arm("V311 SCHEMA sources.minItems 0 + sources [] + a paraphrased quote (#239 Q2/Q3)", "red",
        both(schema(lambda s: s["properties"]["sources"].__setitem__("minItems", 0)),
             pol(lambda o: (o["polarities"][0].__setitem__("sources", []),
                            o["polarities"][0]["links"][0].__setitem__("quote", "the two-red law is a Von Restorff budget")))),
        ["SCHEMA-LOOSENED", "R3-QUOTE-NOT-VERBATIM"])
    arm("V312 SCHEMA note.maxWords 500 + a 64-word note (#239 Q2)", "red",
        both(schema(lambda s: s["properties"]["parties"]["items"]["properties"]["note"].__setitem__("maxWords", 500)),
             pol(lambda o: o["polarities"][0]["parties"][0].__setitem__(
                 "note", " ".join(["Jakob wins in Apollo because Dave prefers familiar chrome."] * 8)))),
        ["SCHEMA-LOOSENED", "R3-NOTE-TOO-LONG"])
    arm("V113 SCHEMA root additionalProperties true + a `verdict` on a node (#239 Q2)", "red",
        both(schema(lambda s: s.__setitem__("additionalProperties", True)),
             pol(lambda o: o["polarities"][0].__setitem__("verdict", "Jakob wins"))),
        ["SCHEMA-LOOSENED", "R3-JUDGEMENT-FIELD"])
    arm("SCHEMA a new property `verdict` ADDED to the schema + used on a node — the key set is pinned (#239 Q2)", "red",
        both(schema(lambda s: s["properties"].__setitem__("verdict", {"type": "string"})),
             pol(lambda o: o["polarities"][0].__setitem__("verdict", "Jakob wins"))),
        ["SCHEMA-LOOSENED", "R3-JUDGEMENT-FIELD"])
    arm("SCHEMA description-only edit — the sha PIN alone fires (#239 Q2 (b))", "red",
        schema(lambda s: s.__setitem__("title", "Polarity node (edited)")),
        "SCHEMA-PIN-MISMATCH", must_not="SCHEMA-LOOSENED")
    arm("V256 SCHEMA `properties` is a list — named S-SCHEMA, no crash (#239 Q7)", "red",
        schema(lambda s: s.__setitem__("properties", [])), "S-SCHEMA")
    arm("V257 SCHEMA id.pattern is an invalid regex — named S-SCHEMA, no crash (#239 Q7)", "red",
        schema(lambda s: s["properties"]["id"].__setitem__("pattern", "^pl-[")), "S-SCHEMA")
    arm("SCHEMA: a keyword this gate does not implement (maxItems) is REFUSED, never silently ignored", "red",
        schema(lambda s: s["properties"]["parties"].__setitem__("maxItems", 9)), "SCHEMA-KEYWORD-UNSUPPORTED")
    # BITE THE BITE, re-cut (#239): the schema still DRIVES the check — a TIGHTER schema is honoured.
    # The pin is moved in-process to the mutant's sha (the same act a real commit must perform).
    kept_pin = SCHEMA_SHA256
    d_t = os.path.join(tmp_root, "schema-tightened")
    _copy_brain(real_brain, d_t)
    _mutate_json(os.path.join(d_t, SCHEMA_REL), lambda s: s["properties"]["parties"].__setitem__("minItems", 3))
    try:
        SCHEMA_SHA256 = sha256_text(read_text(os.path.join(d_t, SCHEMA_REL)))
        rc_t, out_t = _run_gate_captured(d_t)
    finally:
        SCHEMA_SHA256 = kept_pin
    ok = rc_t == 1 and "S-MIN-PARTIES" in out_t and "SCHEMA-LOOSENED" not in out_t and "TRACEBACK" not in out_t
    results.append((len(results) + 1, "BITE-THE-BITE (#239 re-cut): schema TIGHTENED to minItems 3 with the pin "
                                      "moved — the real 2-party rows are refused S-MIN-PARTIES: the schema still "
                                      "drives; only loosening is refused", "red", rc_t, "S-MIN-PARTIES" in out_t,
                    ok, "" if ok else out_t[-400:]))

    # ---- s240-D3 (#242 lane P) — THE RECEIPT: an R1 ROW **OR** A RULING ID, ONE POINTER PER NODE -
    # Every refusal below is driven BOTH WAYS: a GREEN CONTROL that must pass and a BREAK ARM that
    # must go RED BY NAME. The green controls are the legal form lane F (#239) found missing.
    _real_pol = json.loads(read_text(os.path.join(real_brain, "polarities.json")))["polarities"]
    _seed_parties = [{k: v for k, v in p.items() if k != "note"} for p in _real_pol[0]["parties"]]
    SEED_RULING = "s240-D3"          # the ruling this receipt enacts — a real id in the real store

    def seed_node(**over):
        """A polarity BORN AFTER R1: no frozen row to cite, so its receipt is the ruling id."""
        n = {"id": "pl-31", "parties": copy.deepcopy(_seed_parties),
             "mediating_variable": "target count", "links": [], "$seed": SEED_RULING}
        n.update(over)
        return n

    arm("s240-D3 GREEN CONTROL: a NEW polarity born after R1 carries `$seed` = a real ruling id and "
        "NO `sources` — the legal form #239-F RULING-SHAPED 4 was missing (#242 lane P)", "green",
        pol(lambda o: o["polarities"].append(seed_node())), None, write=True)
    arm("s240-D3 BREAK ARM: `$seed` names s999-D9, absent from knowledge/_rulings.json (#242)", "red",
        pol(lambda o: o["polarities"].append(seed_node(**{"$seed": "s999-D9"}))), "R1-DANGLING")
    arm("s240-D3 BREAK ARM: BOTH receipts on one node — its R1 `sources` AND a `$seed` (the receipt "
        "is ONE POINTER PER NODE) (#242)", "red",
        pol(lambda o: o["polarities"][0].__setitem__("$seed", SEED_RULING)), "S-SOURCE")
    arm("s240-D3 BREAK ARM: NEITHER receipt — a node with no `sources` and no `$seed` (#242)", "red",
        pol(lambda o: o["polarities"].append(
            {k: v for k, v in seed_node(id="pl-32").items() if k != "$seed"})), "S-SOURCE")
    arm("s240-D3 GREEN CONTROL: a node RETIRED by a real ruling id — it KEEPS its row and the "
        "derivation is re-run without it (#242)", "green",
        pol(lambda o: o["polarities"][-1].__setitem__("retiredBy", SEED_RULING)), None, write=True)
    arm("s240-D3 BREAK ARM: a RETIRED node whose id still appears under _generated/ — "
        "R4-RETIRED-GENERATED by name, not just STALE (#242)", "red",
        pol(lambda o: o["polarities"][-1].__setitem__("retiredBy", SEED_RULING)),
        ["R4-RETIRED-GENERATED", "STALE-GENERATED"])
    arm("s240-D3 BREAK ARM: `retiredBy` names s999-D9, absent from knowledge/_rulings.json (#242)", "red",
        pol(lambda o: o["polarities"][-1].__setitem__("retiredBy", "s999-D9")), "R1-DANGLING")
    arm("s240-D3 BREAK ARM: `$seed` removed from the SCHEMA's properties — the key set is pinned, so "
        "the receipt cannot be legislated away by a schema edit (#242 Q2)", "red",
        schema(lambda s: s["properties"].__delitem__("$seed")),
        ["SCHEMA-LOOSENED", "SCHEMA-PIN-MISMATCH"])

    # ---- #242 lane P2 — V2's FINDING 3, CLOSED. This position used to be a GREEN CONTROL asserting
    # that a retired id sitting in `delta_vs_237T.cause` was "not a leak" — the selftest CERTIFIED
    # the leak. `delta_cause()` now derives that prose from the live rows and the check scans the
    # whole file, so the arm is RE-POINTED: a retired id ANYWHERE under _generated/ is RED BY NAME.
    # Driven BOTH WAYS in one arm: (1) retire pl-02, --write, and its id is gone from every BYTE of
    # all three files; (2) plant it back in the PROSE ONLY, self-consistently, where the ROW check
    # is blind — and the gate must still refuse R4-RETIRED-GENERATED by name.
    LEAK_PROSE = ("pl-02's s217-D5 is typed `touches` — the hardcoded literal #242 lane P2 removed, "
                  "replanted here so the arm names the position, not the accident.")
    d_l = os.path.join(tmp_root, "prose-only-leak")
    _copy_brain(real_brain, d_l)
    _mutate_json(os.path.join(d_l, "polarities.json"),
                 lambda o: next(n for n in o["polarities"] if n.get("id") == "pl-02")
                 .__setitem__("retiredBy", SEED_RULING))
    rc_lw, _out_lw = _run_gate_captured(d_l, write=True)
    _status_p = os.path.join(d_l, GEN_DIR, "polarity-status.json")
    gone_everywhere = [n for n in GEN_FILES
                       if not id_in_raw_text("pl-02", read_text(os.path.join(d_l, GEN_DIR, n)))]
    _obj = json.loads(read_text(_status_p))
    _gen_at = _obj["generated_at"]
    _body = {k: v for k, v in _obj.items() if k not in ("$header", "generated_at", "content_sha256")}
    _body["delta_vs_237T"]["cause"] = LEAK_PROSE
    _rewrite(_status_p, lambda _t: render_json(_body, _gen_at))
    row_blind = "pl-02" not in generated_node_ids("polarity-status.json", read_text(_status_p))
    rc_l, out_l = _run_gate_captured(d_l)
    named_l = "R4-RETIRED-GENERATED" in set(re.findall(r"REFUSED \(([A-Za-z0-9-]+)\)", out_l))
    ok = (rc_lw == 0 and len(gone_everywhere) == len(GEN_FILES) and row_blind
          and rc_l == 1 and named_l and "Traceback (most recent" not in out_l)
    results.append((len(results) + 1,
                    "s240-D3 LEAK ARM (#242 lane P2, V2 finding 3): pl-02 retired → --write and its id "
                    "is gone from every BYTE of all three generated files; replanted in the derivation's "
                    "PROSE ONLY (self-consistent sha, invisible to the ROW check) → R4-RETIRED-GENERATED "
                    "BY NAME. A retired id anywhere under _generated/ is a leak",
                    "red", rc_l, named_l, ok,
                    "" if ok else f"write_rc={rc_lw} gone_from={gone_everywhere} row_blind={row_blind} "
                                  f"rc={rc_l} named={named_l} :: {out_l[-400:]}"))

    # ---- #242 lane P2 — V2's FINDING 4, CLOSED: THE WIDENING IS FLOORED. Re-adding `sources` to the
    # schema's `required` reads as a TIGHTENING (the superset floor passes) and silently makes every
    # `$seed` node S-SCHEMA. The pin is moved HONESTLY to the mutant's sha — exactly what a real
    # two-file schema edit does — so this is a floor check on the SCHEMA TEXT, not the pin.
    d_x = os.path.join(tmp_root, "required-sources-back")
    _copy_brain(real_brain, d_x)
    _mutate_json(os.path.join(d_x, SCHEMA_REL), lambda s: s["required"].append("sources"))
    _mutate_json(os.path.join(d_x, "polarities.json"), lambda o: o["polarities"].append(seed_node()))
    kept_pin_x = SCHEMA_SHA256
    try:
        SCHEMA_SHA256 = sha256_text(read_text(os.path.join(d_x, SCHEMA_REL)))
        rc_x, out_x = _run_gate_captured(d_x)
    finally:
        SCHEMA_SHA256 = kept_pin_x
    names_x = set(re.findall(r"REFUSED \(([A-Za-z0-9-]+)\)", out_x))
    ok = (rc_x == 1 and "SCHEMA-LOOSENED" in names_x and "SCHEMA-PIN-MISMATCH" not in names_x
          and "S-SCHEMA" not in names_x and "Traceback (most recent" not in out_x)
    results.append((len(results) + 1,
                    "s240-D3 FLOOR ARM (#242 lane P2, V2 finding 4): `sources` put BACK into the schema's "
                    "`required` with the pin moved honestly — SCHEMA-LOOSENED by name (a schema may tighten "
                    "a REFUSAL, never a PERMISSION), and the floor is APPLIED REGARDLESS, so the legal "
                    "`$seed` node beside it is NOT S-SCHEMA",
                    "red", rc_x, "SCHEMA-LOOSENED" in names_x, ok,
                    "" if ok else f"rc={rc_x} names={sorted(names_x)} :: {out_x[-400:]}"))

    # THE DROP-OUT PROOF — the ruling's own words: a retired node "keeps its row and drops out of
    # everything generated from the KG". Driven both ways in one arm: --check names the leak,
    # --write regenerates, the row survives in polarities.json and appears in NO generated file.
    d_r = os.path.join(tmp_root, "retired-dropout")
    _copy_brain(real_brain, d_r)
    _mutate_json(os.path.join(d_r, "polarities.json"),
                 lambda o: o["polarities"][-1].__setitem__("retiredBy", SEED_RULING))
    retired_id = json.loads(read_text(os.path.join(d_r, "polarities.json")))["polarities"][-1]["id"]
    rc_before, out_before = _run_gate_captured(d_r)
    rc_w, _out_w = _run_gate_captured(d_r, write=True)
    rc_after, _out_after = _run_gate_captured(d_r)
    still_in = [n for n in GEN_FILES
                if retired_id in generated_node_ids(n, read_text(os.path.join(d_r, GEN_DIR, n)))]
    kept_row = re.search(r"\b" + re.escape(retired_id) + r"\b",
                         read_text(os.path.join(d_r, "polarities.json"))) is not None
    ok = (rc_before == 1 and "R4-RETIRED-GENERATED" in out_before and rc_w == 0 and rc_after == 0
          and not still_in and kept_row)
    results.append((len(results) + 1,
                    f"s240-D3 DROP-OUT PROOF (#242): {retired_id} retired → --check names "
                    f"R4-RETIRED-GENERATED · --write regenerates · the node KEEPS its row in "
                    f"polarities.json and appears in NONE of the three generated files",
                    "green", rc_after, True, ok,
                    "" if ok else f"before={rc_before} write={rc_w} after={rc_after} still_in={still_in} "
                                  f"kept_row={kept_row} :: {out_before[-300:]}"))

    # THE WRITER carries the new receipt too — #239-F's green-controls (d)/(e) and V's 100/326.
    d_s = os.path.join(tmp_root, "add-polarity-seed")
    _copy_brain(real_brain, d_s)
    buf, old = io.StringIO(), sys.stdout
    sys.stdout = buf
    try:
        rc_seed_dry = add_entry(d_s, "polarity", seed_node(), write=False)
        rc_seed = add_entry(d_s, "polarity", seed_node(), write=True)
    finally:
        sys.stdout = old
    rc_seed_chk, _ = _run_gate_captured(d_s)
    n_after = len(json.loads(read_text(os.path.join(d_s, "polarities.json")))["polarities"])
    ok = rc_seed_dry == 0 and rc_seed == 0 and rc_seed_chk == 0 and n_after == 31
    results.append((len(results) + 1, "s240-D3 ADD-POLARITY (#242): a BRAND-NEW polarity with a `$seed` "
                                      "receipt is accepted by the writer (dry-run then --write), 31 rows, "
                                      "gate green after — #239-F green control (e), which had no legal form",
                    "green", rc_seed_chk, True, ok,
                    "" if ok else f"dry={rc_seed_dry} wr={rc_seed} chk={rc_seed_chk} n={n_after} :: {buf.getvalue()[-400:]}"))

    # ---- s243-D1 (#243 lane Q) — THE SIX CONTROLS, PORTED. #239 Q3 stands: a node may not name its
    # own oracle. Lane F (#239) wrote six green controls in the LITERAL shape (100, 225, 248, 321,
    # 326, and 235's invented phrase); lane P (#242) drove each LITERALLY (red, correctly) and in its
    # s240-D3 LEGAL FORM (green) — notes/_subreports/assets/2026-09-03-242-lane-P-polarity-receipt/
    # _drive_six_controls.py. Dave ruled (s243-D1) the legal forms are PERMANENT NAMED GREEN ARMS here,
    # each PAIRED with its literal shape as a RED arm by refusal name. Every shape below is lane P's
    # verbatim (V's own, from lane F's _wave{1,2,3}.py); nothing is reinvented. 120 (links-empty-array)
    # was never red and needs no pair. 225's literal shape is ALREADY the named red arm V225 above
    # (S-ID + S-SOURCE) and its two-receipts shape is the s240-D3 BOTH-receipts break arm — neither
    # is duplicated; the 225 green arm names both. The writer arms (321, 326) drive add_entry(), the
    # entry point V attacked, not gate() — a refusal must leave every byte as the mutation left it.
    Q = "(#243 s243-D1)"
    # #243 Q2 (V3 finding 1): the S-SOURCE family names seven clauses; the three LITERAL arms below
    # pin the one s243-D1 says STANDS — the Q3 allow-list — by its detail text, so removing that
    # clause alone FAILS them instead of letting the row-exists clause answer in its place.
    ALLOW_CLAUSE = "is not on the source allow-list"
    V_PARTIES = [{"ref": "pr-fitts", "role": "side_a"}, {"ref": "pr-hick", "role": "side_b"}]
    NEW31 = {"id": "pl-31", "parties": copy.deepcopy(V_PARTIES), "mediating_variable": "target count",
             "links": [], "sources": [{"path": "notes/nowhere.json", "id": "tn-31"}]}
    NEW31_SEED = dict({k: v for k, v in NEW31.items() if k != "sources"}, **{"$seed": SEED_RULING})
    GOOD = {"id": "pl-90", "parties": copy.deepcopy(V_PARTIES), "mediating_variable": "target count",
            "links": [], "sources": [{"path": "selftest", "id": "x"}]}
    GOOD_SEED = dict({k: v for k, v in GOOD.items() if k != "sources"}, **{"$seed": SEED_RULING})
    ALLSTUB = {"id": "pl-40",
               "parties": [{"ref": "st-brand-palette", "role": "side_a"},
                           {"ref": "st-consistency-of-investment-across-a-journey", "role": "side_b"}],
               "mediating_variable": "x", "links": [], "sources": [{"path": "x", "id": "y"}]}
    ALLSTUB_SEED = dict({k: v for k, v in ALLSTUB.items() if k != "sources"}, **{"$seed": SEED_RULING})
    _real_ids = {n["id"] for n in _real_pol}

    def writer_arm(name, expect, prep, entry, must_name=None, want_rows=None, post=None, must_detail=None):
        """arm(), but the driver is THE WRITER (add_entry --write) — the entry point 321 and 326
        attacked. Red: rc 1, named, no crash, every byte as prep() left it. Green: rc 0, the gate
        green after, the row count as expected, and post(d) -> (ok, note) if given."""
        n = len(results) + 1
        d = os.path.join(tmp_root, f"arm{n:03d}")
        _copy_brain(real_brain, d)
        try:
            prep(d)
        except Exception as e:  # noqa: BLE001
            results.append((n, name, expect, None, False, False, f"mutation setup crashed: {e!r}"))
            return
        before = _tree_hashes(d)
        buf, old = io.StringIO(), sys.stdout
        sys.stdout = buf
        try:
            try:
                rc = add_entry(d, "polarity", copy.deepcopy(entry), write=True)
            except Exception:           # a crash is not a fail — surface it as one, named
                rc = -1
                buf.write("TRACEBACK\n" + traceback.format_exc())
        finally:
            sys.stdout = old
        out = buf.getvalue()
        after = _tree_hashes(d)
        crashed = "TRACEBACK" in out or "Traceback (most recent" in out
        names = set(re.findall(r"REFUSED \(([A-Za-z0-9-]+)\)", out))
        wanted = [must_name] if isinstance(must_name, str) else list(must_name or [])
        named = bool(wanted) and all(w in names for w in wanted)
        if expect == "green":
            rows = len(json.loads(read_text(os.path.join(d, "polarities.json")))["polarities"])
            rc_chk, out_chk = _run_gate_captured(d)
            p_ok, p_note = post(d) if post else (True, "")
            ok = rc == 0 and rc_chk == 0 and not crashed and (want_rows is None or rows == want_rows) and p_ok
            note = "" if ok else (f"rc={rc} chk={rc_chk} rows={rows} post={p_ok} {p_note} :: "
                                  f"{out[-400:]} :: {out_chk[-300:]}")
        else:
            untouched = after == before
            detailed = (must_detail is None) or (must_detail in out)
            ok = rc == 1 and named and detailed and not crashed and untouched
            note = ("" if ok else f"rc={rc} named={named} (names={sorted(names)} wanted={wanted}) "
                                  f"detailed={detailed} (must_detail={must_detail!r}) "
                                  f"crashed={crashed} untouched={untouched} :: " + out[-500:])
        results.append((n, name, expect, rc, named, ok, note))
        return d

    def reindent2(d):
        p = os.path.join(d, "polarities.json")
        _rewrite(p, lambda t: json.dumps(json.loads(t), indent=2, ensure_ascii=False) + "\n")

    # 100 — row31-no-stub-fictional-source
    arm(f"100 LITERAL {Q}: V's 31st row (pr-fitts/pr-hick) cites a FICTIONAL R1 path notes/nowhere.json "
        f"— the node names its own oracle; S-SOURCE at --write, nothing written — #239 Q3 stands", "red",
        pol(lambda o: o["polarities"].append(copy.deepcopy(NEW31))), "S-SOURCE", write=True,
        must_detail=ALLOW_CLAUSE)
    arm(f"100 LEGAL {Q}: the SAME 31st row with `$seed` = {SEED_RULING} in place of `sources` — --write green",
        "green", pol(lambda o: o["polarities"].append(copy.deepcopy(NEW31_SEED))), None, write=True)

    # 225 — sources-path-absolute-outside-repo. #243 Q2 (V3 finding 3): lane Q's 225 LEGAL was
    # `seed_node(id="pl-33")`, i.e. arm 104 under another id. Now the three drives of
    # six-controls-s240-D3.txt § [225] run on ONE node of 225's own shape: pl-33 (pr-steering/pr-klm,
    # parties no other arm uses) whose receipt IS V225's foreign one, `/etc/hostname`; then that node
    # with the foreign receipt AND a `$seed`; then the same node reduced to the ONE legal receipt.
    # V225 (row 0 + a SECOND, foreign receipt) and arm 106 (row 0's R1 row + `$seed`) stay as they are.
    FOREIGN33 = {"id": "pl-33", "parties": [{"ref": "pr-steering", "role": "side_a"},
                                            {"ref": "pr-klm", "role": "side_b"}],
                 "mediating_variable": "target count", "links": [],
                 "sources": [{"path": "/etc/hostname", "id": "x"}]}
    FOREIGN33_BOTH = dict(copy.deepcopy(FOREIGN33), **{"$seed": SEED_RULING})
    FOREIGN33_SEED = dict({k: v for k, v in FOREIGN33.items() if k != "sources"}, **{"$seed": SEED_RULING})
    arm(f"225 LITERAL {Q}: a NEW node pl-33 whose ONLY receipt is the foreign path /etc/hostname (V225's "
        f"receipt, verbatim) — S-ID + S-SOURCE (allow-list) at --write, nothing written", "red",
        pol(lambda o: o["polarities"].append(copy.deepcopy(FOREIGN33))), ["S-ID", "S-SOURCE"], write=True,
        must_detail=ALLOW_CLAUSE)
    arm(f"225 TWO RECEIPTS {Q}: the SAME pl-33 carrying the foreign `sources` AND `$seed` = {SEED_RULING} — "
        f"S-SOURCE (BOTH receipts: ONE POINTER PER NODE), nothing written", "red",
        pol(lambda o: o["polarities"].append(copy.deepcopy(FOREIGN33_BOTH))), "S-SOURCE", write=True,
        must_detail="carries BOTH")
    arm(f"225 LEGAL {Q}: the SAME pl-33 reduced to ONE legal receipt — the foreign `sources` gone, "
        f"`$seed` = {SEED_RULING} — --write green", "green",
        pol(lambda o: o["polarities"].append(copy.deepcopy(FOREIGN33_SEED))), None, write=True)

    # 235 — orphan-stub-declared-never-used. #243 Q2 (V3 finding 2): the LEGAL phrase is read from the
    # R1 FILE — not from load_register(), the gate's own haystack, which made the arm its own oracle —
    # and it lies INSIDE ONE field (row 0's `the_pull`), so it is a register phrase, not a join artefact.
    _r1_path = os.path.join(REPO, R1_TENSIONS_REL)
    _r1_row0 = json.loads(read_text(_r1_path))["tensions"][0]
    _verbatim4 = " ".join(_r1_row0["the_pull"].split()[:4])

    def _orphan_verbatim_stub(d):
        fields = [k for k, v in _r1_row0.items() if isinstance(v, str) and _verbatim4 in v]
        if fields != ["the_pull"] or _verbatim4 not in read_text(_r1_path):
            raise RuntimeError(f"{_verbatim4!r} is not inside exactly one field of R1 row 0 (fields={fields}) "
                               f"— the arm's oracle is the FILE, not the gate")
        _mutate_json(os.path.join(d, "stubs.json"),
                     lambda o: o["stubs"].append({"id": "st-orphan-verbatim", "phrase": _verbatim4}))
    arm(f"235 LITERAL {Q}: an orphan stub whose phrase is INVENTED ('an orphan phrase') — not verbatim in the "
        f"R1 register; R3-JUDGEMENT-FIELD", "red",
        stubs(lambda o: o["stubs"].append({"id": "st-orphan-phrase", "phrase": "an orphan phrase"})),
        "R3-JUDGEMENT-FIELD")
    arm(f"235 LEGAL {Q}, lane F's #239 form (a): an orphan stub — declared, never used — whose phrase is VERBATIM "
        f"from ONE field of the first R1 row, read from the R1 FILE ({_verbatim4!r}) — green", "green",
        _orphan_verbatim_stub)

    # 248 — node-all-parties-are-stubs
    arm(f"248 LITERAL {Q}: a node whose BOTH parties are declared stubs cites source path 'x' — S-SOURCE at "
        f"--write, nothing written", "red",
        pol(lambda o: o["polarities"].append(copy.deepcopy(ALLSTUB))), "S-SOURCE", write=True,
        must_detail=ALLOW_CLAUSE)
    arm(f"248 LEGAL {Q}: the SAME all-stub node with `$seed` = {SEED_RULING} — --write green", "green",
        pol(lambda o: o["polarities"].append(copy.deepcopy(ALLSTUB_SEED))), None, write=True)

    # 321 — writer-append-into-empty-array (DELETED is refused; RETIRED is the legal form)
    writer_arm(f"321 LITERAL {Q}: all 30 rows DELETED, then the writer appends a `$seed` node — 30 frozen rows "
               f"claimed by no node; S-SOURCE, file untouched", "red",
               pol(lambda o: o.__setitem__("polarities", [])), GOOD_SEED, "S-SOURCE")
    _rc321 = []

    def _retire_all_and_write(d):
        _mutate_json(os.path.join(d, "polarities.json"),
                     lambda o: [n.__setitem__("retiredBy", SEED_RULING) for n in o["polarities"]])
        _rc321.append(_run_gate_captured(d, write=True)[0])

    def _no_retired_id_generated(d):
        leaks_rows = sorted(_real_ids & set().union(*(
            generated_node_ids(n, read_text(os.path.join(d, GEN_DIR, n))) for n in GEN_FILES)))
        leaks_bytes = sorted(i for i in _real_ids
                             if any(id_in_raw_text(i, read_text(os.path.join(d, GEN_DIR, n))) for n in GEN_FILES))
        ok = _rc321 == [0] and not leaks_rows and not leaks_bytes
        return ok, f"retire_write_rc={_rc321} leaks_rows={leaks_rows} leaks_bytes={leaks_bytes}"
    writer_arm(f"321 LEGAL {Q}: all 30 rows RETIRED (`retiredBy` = {SEED_RULING}) and --write green, then the "
               f"writer appends the `$seed` node — 31 rows KEPT in polarities.json, no retired id in any "
               f"row or byte under _generated/", "green",
               _retire_all_and_write, GOOD_SEED, want_rows=31, post=_no_retired_id_generated)

    # 326 — writer-on-2-space-indented-file (the format tolerance was never the thing refused)
    writer_arm(f"326 LITERAL {Q}: polarities.json re-indented to 2 spaces, the writer's entry cites 'selftest' "
               f"as its source — S-SOURCE, file untouched", "red", reindent2, GOOD, "S-SOURCE",
               must_detail=ALLOW_CLAUSE)
    writer_arm(f"326 LEGAL {Q}: the SAME 2-space file, the SAME entry with `$seed` = {SEED_RULING} — writer "
               f"green, 31 rows, gate green after", "green", reindent2, GOOD_SEED, want_rows=31)

    # ---- Q4 — THE CLOCK ------------------------------------------------------------------------
    def future_clock(d):
        for n in ("polarity-status.json", "polarity-edges.json"):
            _rewrite(os.path.join(d, GEN_DIR, n), lambda t: re.sub(r'"generated_at": "\d{4}', '"generated_at": "2099', t, 1))
        _rewrite(os.path.join(d, GEN_DIR, "defaults-declaration.txt"), lambda t: re.sub(r"generated_at: \d{4}", "generated_at: 2099", t, 1))
    arm("V70 R4 generated_at in 2099 on all three derived files — a future clock is a hand edit (#239 Q4)", "red",
        future_clock, "R4-AUTHORED-GENERATED")
    arm("V71 R4 generated_at \"banana\" (#239 Q4)", "red",
        lambda d: _rewrite(os.path.join(d, GEN_DIR, "polarity-status.json"),
                           lambda t: re.sub(r'"generated_at": "[^"]*"', '"generated_at": "banana"', t, 1)),
        "R4-AUTHORED-GENERATED")
    arm("Q4 R4 generated_at before the R1 asset's date (1999) (#239 Q4)", "red",
        lambda d: [_rewrite(os.path.join(d, GEN_DIR, n), lambda t: re.sub(r'"generated_at": "\d{4}', '"generated_at": "1999', t, 1))
                   for n in ("polarity-status.json", "polarity-edges.json")]
        + [_rewrite(os.path.join(d, GEN_DIR, "defaults-declaration.txt"), lambda t: re.sub(r"generated_at: \d{4}", "generated_at: 1999", t, 1))],
        "R4-AUTHORED-GENERATED")
    arm("Q4 R4 one file's clock moved one second — the three clocks must agree (#239 Q4)", "red",
        lambda d: _rewrite(os.path.join(d, GEN_DIR, "polarity-edges.json"),
                           lambda t: re.sub(r'"generated_at": "([^"]*)(\d)Z"',
                                            lambda m: f'"generated_at": "{m.group(1)}{(int(m.group(2)) + 1) % 10}Z"', t, 1)),
        "R4-AUTHORED-GENERATED")

    # ---- FRESHNESS -----------------------------------------------------------------------------
    def stale(d):
        # a REAL edit to the home (a new touches link) with no --write: the derived files go stale
        _mutate_json(os.path.join(d, "polarities.json"),
                     lambda o: o["polarities"][5]["links"].append({"type": "touches", "ref": "s116-D1"}))
    arm("FRESHNESS: home edited, generated files not re-derived → STALE", "red", stale, "STALE-GENERATED")
    arm("FRESHNESS: a generated file deleted → MISSING", "red",
        lambda d: os.remove(os.path.join(d, GEN_DIR, "polarity-edges.json")), "MISSING-GENERATED")

    # ---- Q7 — THE CATCH-ALL, proven by mutation: a check that RAISES is named, never a traceback
    kept_cs = check_stubs

    def exploding(*a, **k):
        raise TypeError("selftest: a deliberate crash inside the gate")
    d_x = os.path.join(tmp_root, "crash")
    _copy_brain(real_brain, d_x)
    try:
        check_stubs = exploding
        rc_x, out_x = _run_gate_captured(d_x)
    finally:
        check_stubs = kept_cs
    ok = rc_x == 1 and "REFUSED (S-SHAPE)" in out_x and "TypeError" in out_x and "TRACEBACK" not in out_x \
        and "Traceback (most recent" not in out_x
    results.append((len(results) + 1, "Q7 (#239): a check that RAISES inside gate() is NAMED S-SHAPE with its "
                                      "exception class — a crash is not a fail", "red", rc_x,
                    "REFUSED (S-SHAPE)" in out_x, ok, "" if ok else out_x[-400:]))

    # ---- WRITE PATH ----------------------------------------------------------------------------
    d_w = os.path.join(tmp_root, "write-refused")
    _copy_brain(real_brain, d_w)
    _mutate_json(os.path.join(d_w, "polarities.json"),
                 lambda o: o["polarities"][0].__setitem__("status", "open"))
    gen_before = _tree_hashes(os.path.join(d_w, GEN_DIR))
    rc, out = _run_gate_captured(d_w, write=True)
    gen_after = _tree_hashes(os.path.join(d_w, GEN_DIR))
    ok = rc == 1 and "R5-TYPED-STATUS" in out and gen_before == gen_after
    results.append((len(results) + 1, "WRITE: --write on a refused home writes NOTHING (hashes equal)",
                    "red", rc, "R5-TYPED-STATUS" in out, ok, "" if ok else out[-400:]))

    d_s = os.path.join(tmp_root, "write-stale-then-fresh")
    _copy_brain(real_brain, d_s)
    stale(d_s)
    rc1, _ = _run_gate_captured(d_s)                       # stale → red
    rc2, out2 = _run_gate_captured(d_s, write=True)        # write → green
    rc3, _ = _run_gate_captured(d_s)                       # check → green, idempotent
    ok = rc1 == 1 and rc2 == 0 and rc3 == 0
    results.append((len(results) + 1, "WRITE: stale → --write → fresh (rc 1 → 0 → 0)", "green",
                    rc3, True, ok, "" if ok else f"rc {rc1},{rc2},{rc3} :: {out2[-300:]}"))
    # the clock is HELD by --check: two writes differ only in generated_at
    t1 = read_text(os.path.join(d_s, GEN_DIR, "polarity-status.json"))
    rc4, _ = _run_gate_captured(d_s, write=True)
    t2 = read_text(os.path.join(d_s, GEN_DIR, "polarity-status.json"))
    strip = lambda t: re.sub(r'"generated_at": "[^"]*"', '"generated_at": "X"', t)
    ok = rc4 == 0 and strip(t1) == strip(t2)
    results.append((len(results) + 1, "WRITE: determinism — two writes differ only in generated_at",
                    "green", rc4, True, ok, "" if ok else "bodies differ"))

    # ---- THE TEXTUAL WRITER (--add-*) ------------------------------------------------------------
    # Q3 makes every frozen row claimed, so the green ADD arm first DROPS pl-30 (no --write) and
    # re-adds its row as pl-31: the append is proven textual and the gate is green after. A brand-
    # new polarity needs a second register on the allow-list — RULING-SHAPED, reported by #239-F.
    d_a = os.path.join(tmp_root, "add-polarity")
    _copy_brain(real_brain, d_a)
    _mutate_json(os.path.join(d_a, "polarities.json"), lambda o: o["polarities"].pop())
    orig = read_text(os.path.join(d_a, "polarities.json"))
    last = json.loads(read_text(os.path.join(real_brain, "polarities.json")))["polarities"][-1]
    good = dict(last, id="pl-31")
    buf, old = io.StringIO(), sys.stdout
    sys.stdout = buf
    try:
        rc_dry = add_entry(d_a, "polarity", good, write=False)
        untouched = read_text(os.path.join(d_a, "polarities.json")) == orig
        rc_wr = add_entry(d_a, "polarity", good, write=True)
    finally:
        sys.stdout = old
    new = read_text(os.path.join(d_a, "polarities.json"))
    # reconstruction on the REAL written file, computed INDEPENDENTLY of the writer: the new text
    # must be <common prefix> + <one span> + <common suffix> with prefix + suffix == the original
    p = 0
    while p < len(orig) and p < len(new) and orig[p] == new[p]:
        p += 1
    s = len(orig) - p
    recon_ok = (len(new) > len(orig) and new[:p] + new[len(new) - s:] == orig
                and len(json.loads(new)["polarities"]) == 30 and json.loads(new)["polarities"][-1] == good)
    rc_chk, _ = _run_gate_captured(d_a)
    ok = rc_dry == 0 and untouched and rc_wr == 0 and recon_ok and rc_chk == 0
    results.append((len(results) + 1, "ADD-POLARITY: pl-30 dropped then re-added as pl-31 — dry-run leaves bytes; "
                                      "--write = original + one span; 30 rows; gate green after (#239: every "
                                      "frozen row is claimed)", "green", rc_chk, True, ok,
                    "" if ok else f"dry={rc_dry} untouched={untouched} wr={rc_wr} recon={recon_ok} chk={rc_chk} :: {buf.getvalue()[-400:]}"))

    d_b = os.path.join(tmp_root, "add-polarity-refused")
    _copy_brain(real_brain, d_b)
    bad = dict(good, id="pl-98", status="open")
    orig_b = _tree_hashes(d_b)
    buf, old = io.StringIO(), sys.stdout
    sys.stdout = buf
    try:
        rc_bad = add_entry(d_b, "polarity", bad, write=True)
    finally:
        sys.stdout = old
    ok = rc_bad == 1 and "R5-TYPED-STATUS" in buf.getvalue() and _tree_hashes(d_b) == orig_b
    results.append((len(results) + 1, "ADD-POLARITY: an entry with a typed status is REFUSED by name, "
                                      "nothing written", "red", rc_bad, "R5-TYPED-STATUS" in buf.getvalue(), ok,
                    "" if ok else buf.getvalue()[-400:]))

    d_u = os.path.join(tmp_root, "add-polarity-unverifiable")
    _copy_brain(real_brain, d_u)
    orig_u = _tree_hashes(d_u)
    unver = {"id": "pl-91", "parties": [{"ref": "pr-fitts", "role": "side_a"}, {"ref": "pr-hick", "role": "side_b"}],
             "mediating_variable": "target count",
             "links": [{"type": "resolvedBy", "ref": "s116-D1", "quote": "this quote exists nowhere"}],
             "sources": [{"path": "selftest", "id": "x"}]}
    buf, old = io.StringIO(), sys.stdout
    sys.stdout = buf
    try:
        rc_u = add_entry(d_u, "polarity", unver, write=True)
    finally:
        sys.stdout = old
    ok = rc_u == 1 and "S-SOURCE" in buf.getvalue() and "R3-QUOTE-NOT-VERBATIM" in buf.getvalue() \
        and _tree_hashes(d_u) == orig_u
    results.append((len(results) + 1, "V324 ADD-POLARITY: an entry whose quote has no reachable source is REFUSED "
                                      "(S-SOURCE + R3-QUOTE-NOT-VERBATIM), nothing written (#239 Q3)", "red", rc_u,
                    "S-SOURCE" in buf.getvalue(), ok, "" if ok else buf.getvalue()[-400:]))

    d_c = os.path.join(tmp_root, "add-stub")
    _copy_brain(real_brain, d_c)
    orig_c = read_text(os.path.join(d_c, "stubs.json"))
    orig_c_hash = _tree_hashes(d_c)
    buf, old = io.StringIO(), sys.stdout
    sys.stdout = buf
    try:
        # a phrase the frozen register SAYS (tn-15's side_b carries it) — Q5: a stub is verbatim
        rc_st = add_entry(d_c, "stub", {"id": "st-brand-colours", "phrase": "Brand colours frequently fail contrast"}, write=True)
        rc_st_bad = add_entry(d_c, "stub", {"id": "st-bad", "phrase": "x", "why": "y"}, write=True)
        rc_st_z = add_entry(d_c, "stub", {"id": "st-zwsp", "phrase": ZWSP}, write=True)
    finally:
        sys.stdout = old
    new_c = read_text(os.path.join(d_c, "stubs.json"))
    ok = (rc_st == 0 and len(json.loads(new_c)["stubs"]) == len(json.loads(orig_c)["stubs"]) + 1
          and rc_st_bad == 1 and "S-STUB-SHAPE" in buf.getvalue()
          and rc_st_z == 1 and "S-FORMAT-CHAR" in buf.getvalue()
          and len(json.loads(read_text(os.path.join(d_c, "stubs.json")))["stubs"]) == len(json.loads(orig_c)["stubs"]) + 1)
    results.append((len(results) + 1, "ADD-STUB: a verbatim phrase appended textually; 3-key stub REFUSED (S-STUB-SHAPE); "
                                      "V328 the U+200B phrase REFUSED (S-FORMAT-CHAR), nothing written", "green",
                    rc_st, True, ok, "" if ok else buf.getvalue()[-500:]))

    # ---- CLI: the SAME entry point via subprocess, rc observed from the process --------------
    d_cli = os.path.join(tmp_root, "cli-red")
    _copy_brain(real_brain, d_cli)
    _mutate_json(os.path.join(d_cli, "polarities.json"),
                 lambda o: o["polarities"][0]["links"].append({"ref": "s116-D1"}))
    me = os.path.abspath(__file__)
    r_green = subprocess.run([sys.executable, me, "--check", "--brain", real_brain], capture_output=True, text=True)
    r_red = subprocess.run([sys.executable, me, "--check", "--brain", d_cli], capture_output=True, text=True)
    r_env = subprocess.run([sys.executable, me, "--check"], capture_output=True, text=True,
                           env=dict(os.environ, POLARITY_BRAIN_DIR=d_cli))
    ok = (r_green.returncode == 0 and r_red.returncode == 1 and "R2-UNTYPED" in r_red.stdout
          and r_env.returncode == 1 and "R2-UNTYPED" in r_env.stdout)
    results.append((len(results) + 1, "CLI: `--check` rc 0 on the real home, rc 1 + R2-UNTYPED on the mutant "
                                      "(via --brain AND via POLARITY_BRAIN_DIR)", "green", r_green.returncode,
                    True, ok, "" if ok else (r_green.stdout + r_red.stdout + r_env.stdout)[-500:]))
    r_bare = subprocess.run([sys.executable, me], capture_output=True, text=True)
    r_junk = subprocess.run([sys.executable, me, "--wat"], capture_output=True, text=True)
    ok = r_bare.returncode == 2 and r_junk.returncode == 2 and "REFUSED" in (r_junk.stdout + r_junk.stderr)
    results.append((len(results) + 1, "CLI: bare and unknown argv refuse with rc 2 (argv contract, #208 class)",
                    "red", r_junk.returncode, ok, ok, "" if ok else (r_bare.stdout + r_junk.stdout + r_junk.stderr)[-300:]))
    # V A1/A2 — contradictory KNOWN flags are a contract violation too (#239)
    d_av = os.path.join(tmp_root, "argv")
    _copy_brain(real_brain, d_av)
    ep = os.path.join(tmp_root, "entry.json")
    with open(ep, "w", encoding="utf-8") as f:
        json.dump(good, f)
    h0 = _tree_hashes(d_av)
    r_a1 = subprocess.run([sys.executable, me, "--add-polarity", ep, "--dry-run", "--write", "--brain", d_av],
                          capture_output=True, text=True)
    r_a2 = subprocess.run([sys.executable, me, "--check", "--write", "--brain", d_av], capture_output=True, text=True)
    r_a3 = subprocess.run([sys.executable, me, "--check", "--selftest", "--brain", d_av], capture_output=True, text=True)
    ok = (r_a1.returncode == 2 and r_a2.returncode == 2 and r_a3.returncode == 2 and _tree_hashes(d_av) == h0
          and "REFUSED (argv)" in r_a1.stderr and "REFUSED (argv)" in r_a2.stderr)
    results.append((len(results) + 1, "V-A1/A2 CLI: `--dry-run --write`, `--check --write`, `--check --selftest` refuse "
                                      "rc 2 and write nothing (#239 argv contract)", "red", r_a1.returncode, ok, ok,
                    "" if ok else (r_a1.stderr + r_a2.stderr + r_a3.stderr)[-400:]))

    # ---- THE THIRD VERDICT (#193) vs THE SOURCE-REPO MUTATION (#239 Q8) ------------------------
    r_abs = subprocess.run([sys.executable, me, "--check", "--brain", os.path.join(tmp_root, "no-such-home")],
                           capture_output=True, text=True)
    ok = r_abs.returncode == 1 and "REFUSED (S-SHAPE)" in r_abs.stdout and "does not exist" in r_abs.stdout \
        and cna.MARKER not in r_abs.stdout
    results.append((len(results) + 1, "V-D1 (#239 Q8): home ABSENT in the SOURCE repo (the store is here) → rc 1 "
                                      "S-SHAPE, never 77 — the build and the seam both stop", "red", r_abs.returncode,
                    "REFUSED (S-SHAPE)" in r_abs.stdout, ok, "" if ok else r_abs.stdout[-300:] + r_abs.stderr[-300:]))
    # the pack shape: NO store → 77 + COULD-NOT-ASK naming the path (pack classifier reads REPO-BOUND)
    kept_r = RULINGS
    try:
        RULINGS = os.path.join(tmp_root, "no-such-rulings.json")
        rc77, out77 = _run_gate_captured(os.path.join(tmp_root, "no-such-home"))
    finally:
        RULINGS = kept_r
    ok = rc77 == cna.EXIT and out77.startswith(cna.MARKER) and "does not exist" in out77
    results.append((len(results) + 1, "COULD-NOT-ASK: home absent AND no store (a shipped pack) → rc 77 + marker "
                                      "naming the path (pack classifier reads it as REPO-BOUND)", "77", rc77, ok, ok,
                    "" if ok else out77[-300:]))
    # the declaration source (a notes/ asset) taken away: refusals still asked FIRST (a real red
    # stays red), then 77 on a clean home — proven by pointing OPEN_DEFAULTS at nothing in-process
    kept = OPEN_DEFAULTS
    try:
        OPEN_DEFAULTS = os.path.join(tmp_root, "no-such-open-tensions.json")
        d77 = os.path.join(tmp_root, "src-absent-clean")
        _copy_brain(real_brain, d77)
        rc_a, out_a = _run_gate_captured(d77)
        d77b = os.path.join(tmp_root, "src-absent-red")
        _copy_brain(real_brain, d77b)
        _mutate_json(os.path.join(d77b, "polarities.json"),
                     lambda o: o["polarities"][0].__setitem__("status", "open"))
        rc_b, out_b = _run_gate_captured(d77b)
    finally:
        OPEN_DEFAULTS = kept
    ok = rc_a == cna.EXIT and cna.MARKER in out_a and rc_b == 1 and "R5-TYPED-STATUS" in out_b
    results.append((len(results) + 1, "COULD-NOT-ASK: declaration source absent → 77 on a clean home, but a "
                                      "real refusal is STILL rc 1 first (the refusal path is not swallowed)",
                    "77", rc_a, ok, ok, "" if ok else f"rc {rc_a}/{rc_b} :: {out_a[-200:]} :: {out_b[-200:]}"))
    # the selftest's own cleanup path (V finding 16): an absent home is a named refusal, no tempdir left
    r_sa = subprocess.run([sys.executable, me, "--selftest", "--brain", os.path.join(tmp_root, "no-such-home")],
                          capture_output=True, text=True)
    ok = r_sa.returncode == 1 and "REFUSED (S-SHAPE)" in r_sa.stdout and "Traceback" not in r_sa.stderr
    results.append((len(results) + 1, "SELFTEST on an absent home refuses by name, no traceback (#239, V finding 16)",
                    "red", r_sa.returncode, "REFUSED (S-SHAPE)" in r_sa.stdout, ok, "" if ok else r_sa.stdout[-200:] + r_sa.stderr[-200:]))

    # ---- WIRING PRESENCE (declared skip when a surface is unreachable) --------------------------
    build = os.path.join(HERE, "_build_all.py")
    seam = os.path.join(HERE, "_git_commit.sh")
    harness = os.path.join(HERE, "_test_git_commit.py")
    if os.path.exists(build) and os.path.exists(seam) and os.path.exists(harness):
        bt, st_, ht = read_text(build), read_text(seam), read_text(harness)
        ok_b = ('"_validate_polarities.py", ["--check"]' in bt and '"_validate_polarities.py", ["--selftest"]' in bt)
        seam_lines = [ln for ln in st_.splitlines() if not ln.lstrip().startswith("#")
                      and "python3 knowledge/_validate_polarities.py --check" in ln]
        ok_s = len(seam_lines) >= 1
        ok_h = 'write(os.path.join(know, "_validate_polarities.py")' in ht
        # V-D2 (#239 Q8): the seam DECLARES a POLARITY_BRAIN_DIR redirect and still gates the tree's own home
        ok_d2 = ("polarity gate: REDIRECTED to" in st_ and "unset POLARITY_BRAIN_DIR" in st_)
        ok = ok_b and ok_s and ok_h and ok_d2
        results.append((len(results) + 1, "WIRING: STEPS has --check + --selftest rows; _git_commit.sh invokes "
                                          "--check on a live line, DECLARES a POLARITY_BRAIN_DIR redirect and gates the "
                                          "tree's own home (V-D2, #239); the seam harness stubs it", "green",
                        0 if ok else 1, True, ok, "" if ok else f"build={ok_b} seam={ok_s} harness={ok_h} d2={ok_d2}"))
    else:
        results.append((len(results) + 1, "WIRING presence", "green", 0, True, True,
                        "SKIPPED (declared): a wiring surface is not on disk here — not a pass, not a fail"))


# ============================================================================================
# ARGV — a contract, not a membership test (#208 class): unknown tokens refuse, rc 2; and so do
# contradictory KNOWN ones (#239: `--dry-run --write` wrote, `--check --write` wrote)
# ============================================================================================
FLAGS = {"--check": 0, "--write": 0, "--selftest": 0, "--dry-run": 0,
         "--add-polarity": 1, "--add-stub": 1, "--brain": 1}
USAGE = ("usage: --check | --write | --selftest | --add-polarity FILE (--dry-run|--write) | "
         "--add-stub FILE (--dry-run|--write)   [--brain DIR]  — exactly one mode, never two")


def _refuse_argv(msg):
    print(f"⛔ REFUSED (argv) — {msg}. {USAGE}", file=sys.stderr)
    return 2


def main(argv):
    if not argv:
        return _refuse_argv("no arguments: this script writes files under --write and refuses to guess")
    opts, i = {}, 0
    while i < len(argv):
        tok = argv[i]
        if tok not in FLAGS:
            return _refuse_argv(f"unknown argument {tok!r}")
        if tok in opts:
            return _refuse_argv(f"{tok} given twice")
        if FLAGS[tok]:
            if i + 1 >= len(argv):
                return _refuse_argv(f"{tok} needs a value")
            opts[tok] = argv[i + 1]
            i += 2
        else:
            opts[tok] = True
            i += 1
    adding = [k for k in ("--add-polarity", "--add-stub") if k in opts]
    modes = [k for k in ("--check", "--write", "--selftest") if k in opts]
    if adding:
        if len(adding) > 1 or "--check" in opts or "--selftest" in opts:
            return _refuse_argv(f"{' + '.join(sorted(adding + [m for m in modes if m != '--write']))} contradict "
                                f"each other — one mode per run")
        if ("--dry-run" in opts) == ("--write" in opts):
            return _refuse_argv("--add-* needs EXACTLY one of --dry-run or --write, stated (a dry run that "
                                "writes is the #239 V-A1 defect)")
    else:
        if "--dry-run" in opts:
            return _refuse_argv("--dry-run belongs to --add-polarity / --add-stub only")
        if len(modes) != 1:
            return _refuse_argv(f"{' + '.join(modes) if modes else 'nothing to do'} — exactly one of --check / "
                                f"--write / --selftest (a check that writes is the #239 V-A2 defect)")
    brain = opts.get("--brain") or os.environ.get("POLARITY_BRAIN_DIR") or DEFAULT_BRAIN
    brain = os.path.abspath(brain)
    if "--selftest" in opts:
        return selftest(brain)
    if adding:
        which = "polarity" if "--add-polarity" in opts else "stub"
        src = opts[adding[0]]
        try:
            entry = json.loads(read_text(src))
        except Exception as e:  # noqa: BLE001
            print(f"⛔ REFUSED (S-PARSE) — {src}: {e}", file=sys.stderr)
            return 2
        return add_entry(brain, which, entry, write="--write" in opts)
    if "--write" in opts:
        return gate(brain, write=True)
    return gate(brain, write=False)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
