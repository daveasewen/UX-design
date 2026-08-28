#!/usr/bin/env python3
"""_encoder_home.py — the ONE place this pack finds an EXACT `cl100k_base` token count.

WHY THIS EXISTS (`s222-D2`, then `s222-D3`, Dave, #222). On the first live Copilot-bridge
session the chain inscription refused, correctly, because `tiktoken` could not fetch its
encoding file: the designer's machine could not reach `openaipublic.blob.core.windows.net`.
The refusal was right and the situation was wrong. Dave: *"I need this to work out of the box
for the designers."* So the encoding DATA now ships inside the pack (`_encoder-cache/`, see its
README) — that was `s222-D2`. Then the second half of the same stumble: the `tiktoken` WHEEL
itself still had to come from PyPI, and a machine that cannot reach one host often cannot reach
the other. Dave chose option B: *"how about we do B"* — a PURE-PYTHON encoder over the SAME
vendored data, used ONLY when `import tiktoken` fails. That is `s222-D3`, and it is the second
half of this module.

THE TWO ENGINES, AND THE ONE RULE THAT ORDERS THEM.

  1. `tiktoken cl100k_base` — the real library. It WINS whenever it is importable, because it is
     a Rust extension and it is roughly two orders of magnitude faster. Nothing about the
     `s222-D2` path changed: `TIKTOKEN_CACHE_DIR` is pointed at the vendored data with
     `os.environ.setdefault`, so a designer's own value still wins.
  2. `purepy cl100k_base (exact, equality-gated)` — this module's own encoder, ~200 lines of
     stdlib Python over the SAME vendored `_encoder-cache/` file. It runs ONLY when
     `import tiktoken` raises. It is not an approximation and it is not an estimate: it
     reproduces the real pipeline — cl100k's pretokenizer regex, the byte-pair merges in rank
     order, and `tiktoken`'s special-token semantics — and it ships with an EQUALITY GATE
     (`--equality-gate`) that drives both engines over a real corpus and refuses on the first
     divergent token.

⛔ THE ENGINE IS NAMED IN EVERY OUTPUT, NEVER SILENT (`s222-D3`, load-bearing). `count()` returns
`(tokens, engine)` and every line this module prints says which engine produced the number. A
fallback that measured silently would be the ds-021 defect wearing a better disguise: a figure
whose method is unstated is exactly what this whole gate family exists to prevent. In particular
this module does NOT install itself into `sys.modules` under the name `tiktoken` — that would
make the fallback invisible to every caller that reports its engine, which is the one thing the
ruling forbids.

⛔ THE NO-ESTIMATE PRINCIPLE IS UNTOUCHED. Both engines need the vendored data. If it is missing,
renamed, or the wrong size, this module says so LOUD AND BY NAME on stderr, naming the exact path
it looked for, and then gets out of the way so the existing refusal fires exactly as it does
today. There is no path through here that turns an estimate into a measurement, and no path that
returns an unlabelled number.

ONE HOME, RESOLVED FROM WHERE THIS FILE SITS. Like the rest of Memento's machinery, this module
does not know its own absolute location and does not need to: it walks up from `__file__`
looking for a `_encoder-cache/` directory that actually contains the data file. That is why it
works both at `memento-package/machinery/` and at
`memento-package/claude-plugin/memento/machinery/`, which sit at different depths.

⚠ THE FILENAME IS A CACHE KEY, NOT A HASH OF THE CONTENT. `tiktoken` looks the data up at
`$TIKTOKEN_CACHE_DIR/<sha1 of the URL it would have downloaded>`. Renaming the file breaks it.
The pure-Python engine reads the same file directly, so a rename breaks both engines identically
— which is correct: one file, one failure mode, one refusal.

⚠ INTEGRITY, AND WHAT THIS MODULE DELIBERATELY DOES NOT RE-CHECK ON EVERY IMPORT. At import
this checks that the file EXISTS and that its SIZE is right — cheap, and it catches the two
realistic corruptions (missing, truncated). It does NOT sha256 1.6 MB on every process start.
`tiktoken` itself verifies the content hash of anything it reads from the cache
(`tiktoken_ext/openai_public.cl100k_base()` passes `expected_hash=`); the pure-Python engine
does NOT (a full hash on every cold start is the cost this fallback cannot afford), so for the
purepy path the honest statement is that same-size scrambled bytes would be caught by the
equality gate and by `--check`'s own 4-token assertion, not at load. `verify(deep=True)` /
`--check` does the full sha256 on demand.

USAGE
    # as a library — the pack's own entry points do this, once, at import
    import _encoder_home; _encoder_home.ensure()

    # THE DISPATCH — the one call that measures. Returns (tokens, engine-name).
    n, engine = _encoder_home.count("some text")

    # the check a designer runs — this is the § Before you start check
    python3 memento-package/machinery/_encoder_home.py --check

    # the equality gate — both engines, a real corpus, refuses on the first divergence
    python3 memento-package/machinery/_encoder_home.py --equality-gate

    # the timings behind the "tiktoken is RECOMMENDED, not required" claim
    python3 memento-package/machinery/_encoder_home.py --timings
"""
import base64
import hashlib
import os
import re
import sys
import time
import unicodedata

ENCODING_NAME = "cl100k_base"
CACHE_DIRNAME = "_encoder-cache"
BLOB_URL = ("https://openaipublic.blob.core.windows.net/encodings/"
            "cl100k_base.tiktoken")
# = sha1(BLOB_URL). Measured, not copied by eye — see `_encoder-cache/README.md`, and the
# assertion in --check re-derives it rather than trusting this line.
DATA_FILENAME = "9b5ad71b2ce5302211f9c61530b329a4922fc6a4"
DATA_BYTES = 1681126
# tiktoken's OWN expected hash for this blob, not one we invented.
DATA_SHA256 = "223921b76ee99bde995b7ff738513eef100fb51d18c93597a113bcffe865b2a7"

ENV_VAR = "TIKTOKEN_CACHE_DIR"
MARKER = "ENCODER-HOME:"          # every line this module prints starts with it, so a log
                                  # reader can find it without parsing prose.

# ⛔ THE TWO ENGINE NAMES. `s222-D3` requires that every output line naming an engine names the
# FALLBACK DISTINCTLY. These two strings are the vocabulary; nothing else may name an engine.
# ⚠ Neither contains the word ESTIMATE, deliberately: both are exact cl100k measurements, and
# a downstream tier-classifier that reads "ESTIMATE" out of a method string (the #82-D1
# vocabulary) must classify BOTH of these as the cl100k tier, not as a guess.
ENGINE_TIKTOKEN = "tiktoken cl100k_base"
ENGINE_PUREPY = "purepy cl100k_base (exact, equality-gated)"

# cl100k_base's special tokens, verbatim from `tiktoken_ext.openai_public.cl100k_base()`.
SPECIAL_TOKENS = {
    "<|endoftext|>": 100257,
    "<|fim_prefix|>": 100258,
    "<|fim_middle|>": 100259,
    "<|fim_suffix|>": 100260,
    "<|endofprompt|>": 100276,
}

_ANNOUNCED = False                # loud once per process, not once per call
_PUREPY_ANNOUNCED = False


# ------------------------------------------------------------------------------ resolution
def search_roots():
    """The directories this module will look in for `_encoder-cache/`, nearest first.

    Every ancestor of this file, so the same module resolves correctly from
    `memento-package/machinery/` (one hop up) and from
    `memento-package/claude-plugin/memento/machinery/` (three hops up)."""
    d = os.path.dirname(os.path.abspath(__file__))
    roots = []
    while True:
        roots.append(d)
        parent = os.path.dirname(d)
        if parent == d:
            return roots
        d = parent


def candidates():
    """Every path this module WOULD accept, nearest first. A refusal names these, so that
    'it could not find it' is never a claim the reader has to take on trust."""
    return [os.path.join(r, CACHE_DIRNAME, DATA_FILENAME) for r in search_roots()]


def locate():
    """(path, None) for the first candidate that exists, else (None, the list it tried)."""
    tried = candidates()
    for p in tried:
        if os.path.isfile(p):
            return p, None
    return None, tried


def verify(deep=False):
    """(ok, reason, path). `reason` is a full sentence naming the path either way.

    `deep=True` adds the sha256. The cheap arms are existence and size, which is what
    `ensure()` runs at import — see the module docstring for why that is enough there."""
    path, tried = locate()
    if path is None:
        return False, ("no vendored %s data found. Looked for a file named %r in a %r "
                       "directory at, nearest first: %s"
                       % (ENCODING_NAME, DATA_FILENAME, CACHE_DIRNAME,
                          ", ".join(tried))), None
    size = os.path.getsize(path)
    if size != DATA_BYTES:
        return False, ("the vendored %s data at %s is %d bytes; it must be %d. A file of the "
                       "wrong size is a truncated or replaced file, not encoder data."
                       % (ENCODING_NAME, path, size, DATA_BYTES)), path
    if deep:
        h = hashlib.sha256(open(path, "rb").read()).hexdigest()
        if h != DATA_SHA256:
            return False, ("the vendored %s data at %s has sha256 %s; tiktoken's own expected "
                           "hash for this blob is %s. The bytes are not the encoder data."
                           % (ENCODING_NAME, path, h, DATA_SHA256)), path
        return True, ("the vendored %s data at %s is present, %d bytes, sha256 %s — tiktoken's "
                      "own expected hash." % (ENCODING_NAME, path, size, h)), path
    return True, ("the vendored %s data is at %s (%d bytes)."
                  % (ENCODING_NAME, path, size)), path


# ------------------------------------------------------------------------------ the one hook
def ensure(announce=True):
    """Point `tiktoken` at the vendored data. Returns (ok, note). Never raises, never writes.

    THE THREE OUTCOMES, ALL DECLARED:
      1. The designer already set `TIKTOKEN_CACHE_DIR` — we do not touch it. `setdefault` is
         the whole contract: their environment wins, and we say that we stood aside.
      2. The vendored data resolves — `TIKTOKEN_CACHE_DIR` is set to its directory, and the
         pack measures with the real encoder on a machine with no network at all.
      3. The vendored data does not resolve — a LOUD, NAMED line on stderr and `ok=False`.
         Nothing is silenced: the existing measurement refusal downstream still fires, and
         now the reader has been told which path was tried before it did.

    ⚠ THIS FUNCTION DOES NOT CHOOSE AN ENGINE, AND IT NEVER LOADS THE PURE-PYTHON ONE. It only
    makes the DATA reachable, for both engines. Engine choice happens in `count()`, once, and
    says which engine it picked. Keeping the two apart is why `ensure()` stays cheap enough to
    run at import in every process."""
    global _ANNOUNCED
    pre = os.environ.get(ENV_VAR)
    if pre:
        return True, ("%s was already set to %r in this environment — the pack stood aside "
                      "and did not consult its vendored copy." % (ENV_VAR, pre))

    ok, reason, path = verify()
    if not ok:
        if announce and not _ANNOUNCED:
            _ANNOUNCED = True
            sys.stderr.write(
                "%s ⛔ %s\n"
                "%s    Token measurement will fall back, and anything that refuses to run on "
                "an estimate WILL refuse. That refusal is correct — it is not caused by this "
                "message, it is explained by it.\n"
                "%s    Fix: restore the file above from a clean copy of the pack, or set %s "
                "yourself to a directory that holds it.\n"
                % (MARKER, reason, MARKER, MARKER, ENV_VAR))
        return False, reason

    os.environ[ENV_VAR] = os.path.dirname(path)   # pre is falsy here, so this IS the setdefault
    return True, ("%s set to %s (vendored, no network needed). %s"
                  % (ENV_VAR, os.path.dirname(path), reason))


# ==============================================================================================
# THE PURE-PYTHON ENGINE (`s222-D3`). Everything from here to `count()` runs ONLY when
# `import tiktoken` has already failed.
# ==============================================================================================
#
# ⚠ WHY THIS IS A HAND-BUILT PRETOKENIZER AND NOT cl100k's REGEX PASTED IN. cl100k's pattern is
#
#     '(?i:[sdmt]|ll|ve|re)|[^\r\n\p{L}\p{N}]?+\p{L}++|\p{N}{1,3}+| ?[^\s\p{L}\p{N}]++[\r\n]*+
#      |\s++$|\s*[\r\n]|\s+(?!\S)|\s
#
# and it uses two things Python's stdlib `re` does not have: Unicode general-category classes
# (`\p{L}`, `\p{N}`) and POSSESSIVE quantifiers (`?+`, `++`, `{1,3}+`, `*+`). The `regex` package
# has both — and installing it would reintroduce exactly the dependency this ruling exists to
# remove. So the pattern is TRANSLATED, and the translation is justified term by term rather
# than asserted:
#
#   `\p{L}` / `\p{N}`  → character classes built HERE from `unicodedata.category()`, which is
#                        the same General_Category data the Rust engine consults. Built once per
#                        process (~0.2 s, measured) and only when this engine is actually used.
#   `?+` in alt 2      → plain `?`. The optional class EXCLUDES letters, so if it matches at i
#                        then `\p{L}+` cannot match at i either: the backtrack a plain `?` would
#                        allow can never succeed, so greedy and possessive agree.
#   `++`, `{1,3}+`     → plain `+` / `{1,3}` wherever NOTHING follows in that alternative — with
#                        no following term there is nothing to backtrack for.
#   `[^\s\p{L}\p{N}]++` → plain `+`: the term after it is `[\r\n]*`, and `\r`/`\n` are `\s`, so
#                        they are excluded from the class and giving a character back can never
#                        help the following term.
#   `\s++$`            → `\s+\Z`. Two changes: the quantifier, as above, and — load-bearing —
#                        Python's `$` also matches BEFORE a final newline, while the Rust `$`
#                        this pattern was written for means end-of-text only. `\Z` is Python's
#                        end-of-text. Using `$` here silently mis-splits every file that ends
#                        in "\n\n", which is most of them.
#
# The remaining alternatives (`'(?i:…)`, `\s*[\r\n]`, `\s+(?!\S)`, `\s`) carry no possessive
# quantifier and translate character for character. Alternation is leftmost-first in both
# engines, so ORDER is preserved exactly as written.
#
# ⬛ DECLARED RESIDUAL, not hidden: `unicodedata` follows the Unicode version of the running
# interpreter and the Rust engine follows its own. A codepoint that is a letter in one version
# and unassigned in the other would pretokenize differently in the two engines. That is why the
# equality gate exists and why it is run over a real corpus rather than trusted — and it is why
# this module states its interpreter's Unicode version in `--equality-gate` output.

_CLASS_CACHE = {}


def _category_ranges(first_letter):
    """Contiguous codepoint ranges whose Unicode general category starts with `first_letter`.

    ★ MEASURED FROM THE INTERPRETER, NOT TYPED INTO THE FILE. A hard-coded range table would be
    a claim about Unicode that nothing checks, and it would be wrong on some other Python."""
    out, start, cat = [], None, unicodedata.category
    for cp in range(sys.maxunicode + 1):
        if cat(chr(cp))[0] == first_letter:
            if start is None:
                start = cp
        elif start is not None:
            out.append((start, cp - 1))
            start = None
    if start is not None:
        out.append((start, sys.maxunicode))
    return out


def _class_body(first_letter):
    """The inside of a `[...]` for one general category, e.g. `\\U00000041-\\U0000005a…`."""
    if first_letter not in _CLASS_CACHE:
        _CLASS_CACHE[first_letter] = "".join(
            ("\\U%08x" % a) if a == b else ("\\U%08x-\\U%08x" % (a, b))
            for a, b in _category_ranges(first_letter))
    return _CLASS_CACHE[first_letter]


def build_pattern():
    """cl100k_base's pretokenizer, translated to stdlib `re`. See the block comment above for
    the term-by-term justification of every difference from the published pattern."""
    letter, number = _class_body("L"), _class_body("N")
    return re.compile(
        r"'(?i:[sdmt]|ll|ve|re)"
        r"|[^\r\n" + letter + number + r"]?[" + letter + r"]+"
        r"|[" + number + r"]{1,3}"
        r"| ?[^\s" + letter + number + r"]+[\r\n]*"
        r"|\s+\Z"
        r"|\s*[\r\n]"
        r"|\s+(?!\S)"
        r"|\s")


def load_ranks(path):
    """{token bytes: rank} from the vendored `.tiktoken` file — `base64 rank` per line.

    Refuses LOUD on a line it cannot parse rather than skipping it: a rank table with holes
    produces confident wrong numbers, which is the one outcome worse than no number."""
    ranks = {}
    with open(path, "rb") as f:
        for lineno, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                token, rank = line.split()
                ranks[base64.b64decode(token)] = int(rank)
            except Exception as ex:                            # noqa: BLE001 — named below
                raise ValueError(
                    "%s line %d is not `<base64> <rank>` (%s: %s). The vendored %s data is "
                    "corrupt; this engine refuses rather than encode with a partial table."
                    % (path, lineno, type(ex).__name__, ex, ENCODING_NAME))
    if not ranks:
        raise ValueError("%s parsed to zero merge ranks — that is not encoder data." % path)
    return ranks


class PurePyEncoding(object):
    """cl100k_base, in stdlib Python. Same data file, same pipeline, same numbers.

    ⚠ `encode()` reproduces `tiktoken.Encoding.encode()`'s DEFAULTS exactly, including the part
    people forget: with no `allowed_special`, a special token appearing literally in the text is
    a `ValueError`, not five ordinary tokens. Callers that wrap `encode()` in a try/except and
    fall back on failure must see the SAME failure from both engines, or the fallback changes
    behaviour on exactly the inputs nobody tests."""

    def __init__(self, ranks, pattern=None, special_tokens=None):
        self.ranks = ranks
        self.pat = pattern if pattern is not None else build_pattern()
        self.special_tokens = dict(SPECIAL_TOKENS if special_tokens is None else special_tokens)
        self._decoder = None
        self._cache = {}
        self._special_re = re.compile(
            "|".join(re.escape(s) for s in sorted(self.special_tokens, key=len, reverse=True))
        ) if self.special_tokens else None

    # ---- the merge loop
    def _bpe(self, piece):
        """The byte-pair merges, in rank order, exactly as tiktoken performs them.

        Repeatedly merge the ADJACENT PAIR WITH THE LOWEST RANK until no adjacent pair is in the
        table. O(n²) in the length of the piece, which is fine: pretokenized pieces are short
        (the pattern caps runs of digits at 3 and splits on every class boundary), and whole
        pieces are memoised by the caller, so real text merges each distinct piece once."""
        parts = [piece[i:i + 1] for i in range(len(piece))]
        get = self.ranks.get
        while len(parts) > 1:
            best_rank, best_i = None, -1
            for i in range(len(parts) - 1):
                r = get(parts[i] + parts[i + 1])
                if r is not None and (best_rank is None or r < best_rank):
                    best_rank, best_i = r, i
            if best_rank is None:
                break
            parts[best_i:best_i + 2] = [parts[best_i] + parts[best_i + 1]]
        try:
            return [self.ranks[p] for p in parts]
        except KeyError as ex:
            # Every single byte 0x00-0xff has a rank in cl100k, so this is unreachable with
            # intact data. It is kept because a corrupt table must fail LOUD, not silently
            # drop a token and return a number that is merely too small.
            raise ValueError(
                "%s: no rank for the byte sequence %r after merging %r — the vendored merge "
                "table is incomplete." % (ENCODING_NAME, ex.args[0], piece))

    def encode_ordinary(self, text):
        """Token ids, treating any special-token text as ordinary text.
        Mirrors `tiktoken.Encoding.encode_ordinary`."""
        out, get, cache = [], self.ranks.get, self._cache
        for m in self.pat.finditer(text):
            piece = m.group().encode("utf-8")
            rank = get(piece)
            if rank is not None:
                out.append(rank)
                continue
            merged = cache.get(piece)
            if merged is None:
                merged = cache[piece] = self._bpe(piece)
            out.extend(merged)
        return out

    def encode(self, text, allowed_special=frozenset(), disallowed_special="all"):
        """Token ids, with `tiktoken.Encoding.encode()`'s special-token contract.

        `allowed_special="all"` permits every special token; a set permits those. Anything in
        `disallowed_special` that appears in the text raises `ValueError` — and by default
        `disallowed_special` is "all", meaning every special token NOT explicitly allowed."""
        if allowed_special == "all":
            allowed = set(self.special_tokens)
        else:
            allowed = set(allowed_special)
        if disallowed_special == "all":
            disallowed = set(self.special_tokens) - allowed
        else:
            disallowed = set(disallowed_special)
        if disallowed:
            hit = re.compile("|".join(re.escape(s) for s in
                                      sorted(disallowed, key=len, reverse=True))).search(text)
            if hit is not None:
                raise ValueError(
                    "Encountered text corresponding to disallowed special token %r.\n"
                    "If you want this text to be encoded as a special token, pass it to "
                    "`allowed_special`, e.g. `allowed_special={%r, ...}`.\n"
                    "If you want this text to be encoded as normal text, disable the check for "
                    "this token by passing `disallowed_special=(enc.special_tokens_set - {%r})`."
                    % (hit.group(), hit.group(), hit.group()))
        if not allowed:
            return self.encode_ordinary(text)
        splitter = re.compile("|".join(re.escape(s) for s in
                                       sorted(allowed, key=len, reverse=True)))
        out, pos = [], 0
        for m in splitter.finditer(text):
            out.extend(self.encode_ordinary(text[pos:m.start()]))
            out.append(self.special_tokens[m.group()])
            pos = m.end()
        out.extend(self.encode_ordinary(text[pos:]))
        return out

    def decode(self, tokens):
        """Bytes back to text, lossily on invalid UTF-8 (`errors='replace'`), like tiktoken's
        `decode`. Only used to SHOW a reader where two engines diverged — never to measure."""
        if self._decoder is None:
            self._decoder = {v: k for k, v in self.ranks.items()}
            for s, i in self.special_tokens.items():
                self._decoder[i] = s.encode("utf-8")
        return b"".join(self._decoder[t] for t in tokens).decode("utf-8", "replace")


_PUREPY = None
_PUREPY_ERROR = None


def purepy_encoding():
    """The pure-Python encoding, built once per process. (encoding, None) or (None, reason).

    ⚠ Building it reads the 1.6 MB vendored table and derives the Unicode classes — ~0.5 s,
    measured. That is why it is lazy: a process with `tiktoken` installed never pays it."""
    global _PUREPY, _PUREPY_ERROR
    if _PUREPY is not None or _PUREPY_ERROR is not None:
        return _PUREPY, _PUREPY_ERROR
    ok, reason, path = verify()
    if not ok:
        _PUREPY_ERROR = reason
        return None, reason
    try:
        _PUREPY = PurePyEncoding(load_ranks(path))
    except Exception as ex:                                    # noqa: BLE001 — named below
        _PUREPY_ERROR = ("the vendored %s data at %s would not build a pure-Python encoder "
                         "(%s: %s)." % (ENCODING_NAME, path, type(ex).__name__, ex))
        return None, _PUREPY_ERROR
    return _PUREPY, None


# ------------------------------------------------------------------------------ the dispatch
class MeasurementRefused(Exception):
    """No engine could measure. Raised, never swallowed, never replaced by a guess."""


def engine(announce=True):
    """Which engine a measurement taken RIGHT NOW would use, WITHOUT measuring.

    Returns `ENGINE_TIKTOKEN` or `ENGINE_PUREPY`, or raises `MeasurementRefused`. ★ Exists so a
    caller can NAME the engine in a header before it starts counting, rather than discovering it
    from the first number."""
    global _PUREPY_ANNOUNCED
    ensure()
    try:
        import tiktoken                                        # noqa: F401 — presence probe
        return ENGINE_TIKTOKEN
    except Exception as ex:                                    # noqa: BLE001 — named below
        tiktoken_reason = "%s: %s" % (type(ex).__name__, ex)
    enc, reason = purepy_encoding()
    if enc is None:
        raise MeasurementRefused(
            "neither engine can measure %s here. `tiktoken` is not importable (%s), and the "
            "pure-Python fallback cannot load its data: %s"
            % (ENCODING_NAME, tiktoken_reason, reason))
    if announce and not _PUREPY_ANNOUNCED:
        _PUREPY_ANNOUNCED = True
        sys.stderr.write(
            "%s ⚠ `tiktoken` is not importable here (%s). Measuring with the pack's own "
            "engine: %s. This is an EXACT cl100k_base count, not an estimate — it is the same "
            "data file and the same pipeline, and `--equality-gate` is what proves it. It is "
            "slower; `pip install tiktoken` makes it fast again.\n"
            % (MARKER, tiktoken_reason, ENGINE_PUREPY))
    return ENGINE_PUREPY


def count(text, announce=True):
    """★ THE DISPATCH. (tokens, engine-name) — an EXACT cl100k_base count, engine always named.

    THE ORDER IS THE RULING (`s222-D3`):
      1. real `tiktoken` whenever it imports — it is the fast one, and it wins on speed alone;
      2. otherwise this module's pure-Python engine over the SAME vendored data — exact, named
         distinctly, and equality-gated;
      3. otherwise `MeasurementRefused`. There is no third tier here and there is deliberately
         no estimate: a caller that wants to fall back to a byte divisor must do so itself, in
         the open, with its own label.

    ⚠ The two engines agree on FAILURES as well as on numbers: `tiktoken`'s `encode()` raises on
    an unescaped special token, and so does this one."""
    which = engine(announce=announce)
    if which == ENGINE_TIKTOKEN:
        import tiktoken
        return len(tiktoken.get_encoding(ENCODING_NAME).encode(text)), which
    enc, _reason = purepy_encoding()
    return len(enc.encode(text)), which


# ==============================================================================================
# THE EQUALITY GATE (`s222-D3`, requirement 1). Built BEFORE the engine and developed against.
# ==============================================================================================
# ⚠ WHAT MAKES THIS A GATE AND NOT A DEMO. It drives BOTH engines over real text and compares
# the TOKEN SEQUENCES, not the counts — two different sequences can share a length, and a gate
# that compared only counts would pass a pretokenizer that is wrong in compensating ways. It
# refuses on the FIRST divergence, naming the file, the token index, and the decoded text either
# side of it. And it carries an adversarial suite of its own, so it still has teeth when it is
# pointed at a corpus of tidy ASCII markdown.

_ADVERSARIAL = [
    "", " ", "  ", "\n", "\r\n", "\n\n\n", "   \n   ", "a\n", "a \n", "a  ", "a   \n\n  b",
    "trailing spaces   ", "trailing newline\n", "ends with two\n\n", "\n leading", "  \n  \n  ",
    "don't", "DON'T", "it's it'S IT'S", "we'll we've we're we'd", "'s'd'm't'll've're", "x'y",
    "123", "1234", "12345678901234567890", "3.14159", "-42", "١٢٣", "٤٥٦٧", "Ⅻ", "½", "²³",
    "héllo", "naïve café", "中文字符测试", "日本語テスト", "한국어", "Ελληνικά", "Русский",
    "العربية", "עברית", "🎉🎊", "👨‍👩‍👧‍👦", "🇬🇧🇺🇸", "ﷺ", "ǅ", "ᾼ", "\U0001d400\U0001d7ce",
    "  \t\t  \n\r\n \t", "\t\ta", "\v\f\x85\xa0", "  　", "​", "﻿", "\x7f",
    "!!!???...", "***---___", "((()))", "a  b", "a b", "word1 word2\tword3",
    "CamelCase snake_case kebab-case", "https://example.com/a?b=c#d",
    "```python\ndef f(x):\n    return x\n```", "| a | b |\n|---|---|\n| 1 | 2 |",
    "★★★ ⛔ ✅ ⚠ · — – …", "⬛ tape (cl100k ESTIMATE)", "**11,032 real — the unit is THE WHOLE FILE**",
]

_CORPUS_EXTS = (".md", ".txt", ".py", ".sh", ".json", ".yml", ".yaml", ".html", ".css",
                ".js", ".toml", ".cfg", ".ini")
_CORPUS_SKIP_DIRS = {".git", "__pycache__", "node_modules", CACHE_DIRNAME}


def corpus_files(roots=None):
    """The pack's own text files — the natural corpus, because it is the text this pack will
    actually be asked to measure. `roots=None` means "the pack this file lives in"."""
    if roots is None:
        _path, _tried = locate()
        roots = [os.path.dirname(os.path.dirname(os.path.abspath(_path)))] if _path else \
                [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]
    out = []
    for root in roots:
        if os.path.isfile(root):
            out.append(root)
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in _CORPUS_SKIP_DIRS]
            for name in sorted(filenames):
                if name.endswith(_CORPUS_EXTS):
                    out.append(os.path.join(dirpath, name))
    return sorted(set(out))


def _first_divergence(a, b, enc, label):
    """A sentence naming WHERE two token sequences part company, with decoded context."""
    n = min(len(a), len(b))
    for i in range(n):
        if a[i] != b[i]:
            lo = max(0, i - 6)
            return ("%s: token %d differs — tiktoken says %d, purepy says %d. Context "
                    "(tiktoken) %r vs (purepy) %r."
                    % (label, i, a[i], b[i], enc.decode(a[lo:i + 6]), enc.decode(b[lo:i + 6])))
    return ("%s: the sequences agree for %d tokens and then differ in LENGTH — tiktoken %d, "
            "purepy %d. Tail (tiktoken) %r vs (purepy) %r."
            % (label, n, len(a), len(b), enc.decode(a[n:n + 12]), enc.decode(b[n:n + 12])))


def equality_gate(roots=None, out=None, encoding_override=None, max_files=None):
    """Drive BOTH engines over the corpus + the adversarial suite. Returns (rc, summary).

    rc 0 = every token identical. rc 1 = a divergence, named. rc 2 = COULD-NOT-RUN, because a
    gate that cannot reach its reference engine must say so rather than pass.

    ⚠ COULD-NOT-RUN IS NOT A PASS. This gate needs the REAL tiktoken as its reference; on a
    machine that has none there is nothing to compare against, and reporting green there would
    be the exact "instrument without a consumer" defect this house has a rule about."""
    out = out or sys.stdout
    try:
        import tiktoken
    except Exception as ex:                                    # noqa: BLE001 — named below
        out.write("%s ⛔ EQUALITY GATE COULD-NOT-RUN — the reference engine is not here. "
                  "`import tiktoken` raised %s: %s. This gate compares the pack's pure-Python "
                  "engine AGAINST real tiktoken; with no reference there is nothing to compare, "
                  "and a green here would be a claim about nothing. Run "
                  "`pip install tiktoken` and re-run.\n" % (MARKER, type(ex).__name__, ex))
        return 2, "COULD-NOT-RUN (no reference engine)"
    ensure()
    try:
        ref = tiktoken.get_encoding(ENCODING_NAME)
    except Exception as ex:                                    # noqa: BLE001 — named below
        out.write("%s ⛔ EQUALITY GATE COULD-NOT-RUN — tiktoken imported but could not load "
                  "%s (%s: %s).\n" % (MARKER, ENCODING_NAME, type(ex).__name__, ex))
        return 2, "COULD-NOT-RUN (reference encoder unloadable)"

    enc = encoding_override
    if enc is None:
        enc, reason = purepy_encoding()
        if enc is None:
            out.write("%s ⛔ EQUALITY GATE COULD-NOT-RUN — the pure-Python engine will not "
                      "build: %s\n" % (MARKER, reason))
            return 2, "COULD-NOT-RUN (fallback engine unbuildable)"

    out.write("%s equality gate — %s vs %s\n" % (MARKER, ENGINE_TIKTOKEN, ENGINE_PUREPY))
    out.write("%s   interpreter Unicode %s · Python %d.%d.%d\n"
              % (MARKER, unicodedata.unidata_version, *sys.version_info[:3]))

    # ---- arm 1: the adversarial suite, ALWAYS, whatever the corpus looks like
    for i, case in enumerate(_ADVERSARIAL):
        a, b = ref.encode_ordinary(case), enc.encode_ordinary(case)
        if a != b:
            out.write("%s ⛔ EQUALITY GATE FAILED on adversarial case %d %r\n%s    %s\n"
                      % (MARKER, i, case, MARKER,
                         _first_divergence(a, b, ref, "adversarial[%d]" % i)))
            return 1, "FAILED (adversarial case %d)" % i

    # ---- arm 2: special-token semantics must fail the SAME WAY in both engines
    for case in ("<|endoftext|>", "a<|endoftext|>b", "<|endofprompt|>", "<|fim_prefix|>"):
        ra = rb = None
        try:
            ra = ref.encode(case)
        except Exception as ex:                                # noqa: BLE001
            ra = "RAISE:%s" % type(ex).__name__
        try:
            rb = enc.encode(case)
        except Exception as ex:                                # noqa: BLE001
            rb = "RAISE:%s" % type(ex).__name__
        if ra != rb:
            out.write("%s ⛔ EQUALITY GATE FAILED on special-token case %r — tiktoken %r, "
                      "purepy %r\n" % (MARKER, case, ra, rb))
            return 1, "FAILED (special-token case %r)" % case
        allowed = "all"
        if ref.encode(case, allowed_special=allowed) != enc.encode(case,
                                                                   allowed_special=allowed):
            out.write("%s ⛔ EQUALITY GATE FAILED on allowed-special case %r\n" % (MARKER, case))
            return 1, "FAILED (allowed-special case %r)" % case

    # ---- arm 3: the real corpus
    files = corpus_files(roots)
    if max_files:
        files = files[:max_files]
    chars = 0
    tokens = 0
    t_ref = t_pp = 0.0
    checked = 0
    for path in files:
        try:
            text = open(path, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue
        if not text:
            continue
        t0 = time.time(); a = ref.encode_ordinary(text); t_ref += time.time() - t0
        t0 = time.time(); b = enc.encode_ordinary(text); t_pp += time.time() - t0
        checked += 1
        chars += len(text)
        tokens += len(a)
        if a != b:
            out.write("%s ⛔ EQUALITY GATE FAILED\n%s    %s\n"
                      % (MARKER, MARKER, _first_divergence(a, b, ref, path)))
            return 1, "FAILED (%s)" % path

    summary = ("%d adversarial cases · %d files · %s characters · %s tokens — every token "
               "identical" % (len(_ADVERSARIAL), checked, format(chars, ","),
                              format(tokens, ",")))
    out.write("%s ✅ EQUALITY GATE PASSED — %s\n" % (MARKER, summary))
    if t_ref and t_pp:
        out.write("%s    over that corpus: %s %.2fs · %s %.2fs (%.0f× slower)\n"
                  % (MARKER, ENGINE_TIKTOKEN, t_ref, ENGINE_PUREPY, t_pp, t_pp / t_ref))
    return 0, summary


# ------------------------------------------------------------------------------ the timings
def timings(paths=None, out=None):
    """Requirement 5 of `s222-D3`: performance MEASURED, not assumed. Times both engines over
    real pack artefacts and prints a table. Returns rc."""
    out = out or sys.stdout
    ensure()
    try:
        import tiktoken
        ref = tiktoken.get_encoding(ENCODING_NAME)
    except Exception as ex:                                    # noqa: BLE001
        ref = None
        out.write("%s ⚠ no reference engine (%s: %s) — timing the fallback ALONE. The "
                  "comparison column will be blank, and that is a declared gap, not a zero.\n"
                  % (MARKER, type(ex).__name__, ex))
    t0 = time.time()
    enc, reason = purepy_encoding()
    build_s = time.time() - t0
    if enc is None:
        out.write("%s ⛔ %s\n" % (MARKER, reason))
        return 1
    out.write("%s cold start of %s: %.2fs (ranks + Unicode classes, once per process)\n"
              % (MARKER, ENGINE_PUREPY, build_s))
    if paths is None:
        paths = [p for p in corpus_files() if p.endswith((".md", ".txt"))]
        paths = sorted(paths, key=lambda p: -os.path.getsize(p))[:5]
    out.write("%-52s %10s %12s %12s\n" % ("artefact", "chars", "tiktoken", "purepy"))
    for path in paths:
        try:
            text = open(path, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue
        if ref is not None:
            t0 = time.time(); ref.encode_ordinary(text); a = time.time() - t0
        else:
            a = None
        t0 = time.time(); enc.encode_ordinary(text); b = time.time() - t0
        out.write("%-52s %10s %12s %11.3fs\n"
                  % (os.path.basename(path)[:52], format(len(text), ","),
                     ("%.3fs" % a) if a is not None else "—", b))
    return 0


# ------------------------------------------------------------------------------ the check
def check(stream=None):
    """The out-of-the-box check, end to end. Exit code 0 iff this machine can measure tokens
    EXACTLY right now — with either engine, and it says which.

    ⚠ This drives the whole path rather than reporting on it: it re-derives the cache key from
    the URL, verifies the vendored bytes deeply, sets the variable, then actually ENCODES a
    string through the real dispatch. A check that stopped at 'the file is there' would pass on
    a pack whose encoder never loads [[mutation-tests-the-clause-not-the-feature]]."""
    out = stream or sys.stdout
    key = hashlib.sha1(BLOB_URL.encode()).hexdigest()
    if key != DATA_FILENAME:
        out.write("%s ⛔ the cache key derived from the URL is %s, but this pack ships %s. "
                  "tiktoken will never find the vendored file under that name.\n"
                  % (MARKER, key, DATA_FILENAME))
        return 1
    ok, reason, _path = verify(deep=True)
    out.write("%s %s\n" % (MARKER, reason))
    if not ok:
        out.write("%s ⛔ REFUSED — this pack cannot measure tokens out of the box.\n" % MARKER)
        return 1
    ok, note = ensure()
    out.write("%s %s\n" % (MARKER, note))
    try:
        n, which = count("the quick brown fox")
    except MeasurementRefused as ex:
        out.write("%s ⛔ REFUSED — %s\n" % (MARKER, ex))
        return 1
    except Exception as ex:                                    # noqa: BLE001 — named below
        out.write("%s ⛔ REFUSED — the vendored data is present but no engine would measure "
                  "with it (%s: %s).\n" % (MARKER, type(ex).__name__, ex))
        return 1
    if n != 4:
        out.write("%s ⛔ REFUSED — %s measured 'the quick brown fox' as %d tokens, not 4. "
                  "That is not %s.\n" % (MARKER, which, n, ENCODING_NAME))
        return 1
    out.write("ENCODER OK — engine: %s — %d tokens, measured with the encoder data inside this "
              "pack (no download, no environment variable to set).\n" % (which, n))
    if which == ENGINE_PUREPY:
        out.write("%s   `tiktoken` is not installed here, so this pack measured with its own "
                  "engine. The count is EXACT, not an estimate — `--equality-gate` is what "
                  "proves that, and it needs `tiktoken` present to run. `pip install tiktoken` "
                  "is RECOMMENDED: it is several times faster.\n" % MARKER)
    return 0


def selftest():
    """Bites that FAIL when this module stops doing its job. Each one plants the condition.

    Returns `(fails, could_not_run)` — TWO lists, deliberately. A bite that could not be driven
    is not a bite that passed and it is not a bite that failed; collapsing the two grades is how
    an un-run check comes to read as evidence [[a-crash-is-not-a-fail]]. The equality-gate arms
    below need real `tiktoken` as their reference, so on a machine that has none they land in
    the second list and the exit code says 2, never 0.

    ⚠ Every arm restores the environment it disturbed — a selftest that leaves
    `TIKTOKEN_CACHE_DIR` set would hand a false green to whatever runs next."""
    fails = []
    could_not_run = []
    saved = os.environ.get(ENV_VAR)

    def restore():
        if saved is None:
            os.environ.pop(ENV_VAR, None)
        else:
            os.environ[ENV_VAR] = saved

    # 1. THE CACHE KEY. If this drifts, everything else here is theatre.
    if hashlib.sha1(BLOB_URL.encode()).hexdigest() != DATA_FILENAME:
        fails.append("the vendored filename is not sha1(BLOB_URL) — tiktoken cannot find it")

    # 2. THE POSITIVE — the data resolves and the variable gets set from nothing.
    os.environ.pop(ENV_VAR, None)
    ok, note = ensure()
    if not ok:
        fails.append("ensure() could not resolve the vendored data: %s" % note)
    elif not os.environ.get(ENV_VAR):
        fails.append("ensure() reported success but %s is not set" % ENV_VAR)
    elif not os.path.isfile(os.path.join(os.environ[ENV_VAR], DATA_FILENAME)):
        fails.append("%s was set to %r, which does not hold %s"
                     % (ENV_VAR, os.environ[ENV_VAR], DATA_FILENAME))

    # 3. THE DESIGNER'S ENV WINS. setdefault, not assignment — the whole point of the ruling's
    #    "no hand-set env var" is that we ADD a default, never overrule a choice.
    os.environ[ENV_VAR] = "/var/tmp/_encoder_home_selftest_designers_own"
    ok, note = ensure()
    if os.environ[ENV_VAR] != "/var/tmp/_encoder_home_selftest_designers_own":
        fails.append("ensure() OVERWROTE a designer's own %s — setdefault means they win" % ENV_VAR)
    if not ok or "stood aside" not in note:
        fails.append("ensure() did not DECLARE that it stood aside for a pre-set %s" % ENV_VAR)

    # 4. THE REFUSAL BITES, AND IT NAMES THE PATH. Planted by pointing the resolver at a
    #    directory with no cache in it — a green arm 2 above proves this arm is not vacuous.
    os.environ.pop(ENV_VAR, None)
    real_file = os.path.abspath(__file__)
    try:
        globals()["__file__"] = "/var/tmp/_encoder_home_selftest_nowhere/machinery/_x.py"
        ok, reason, path = verify()
        if ok:
            fails.append("verify() found vendored data under a directory that has none")
        if DATA_FILENAME not in (reason or "") or CACHE_DIRNAME not in (reason or ""):
            fails.append("the refusal does not NAME the file and directory it looked for: %r"
                         % reason)
        ok2, note2 = ensure(announce=False)
        if ok2:
            fails.append("ensure() reported OK with no vendored data present")
        if os.environ.get(ENV_VAR):
            fails.append("ensure() set %s even though it found nothing — a variable pointing "
                         "at nothing is worse than none" % ENV_VAR)
    finally:
        globals()["__file__"] = real_file
        restore()

    # 5. A WRONG-SIZE FILE IS NOT ENCODER DATA. Planted as a real file on disk.
    import tempfile
    d = tempfile.mkdtemp(prefix="_encoder_home_selftest_")
    os.makedirs(os.path.join(d, "machinery"), exist_ok=True)
    os.makedirs(os.path.join(d, CACHE_DIRNAME), exist_ok=True)
    open(os.path.join(d, CACHE_DIRNAME, DATA_FILENAME), "wb").write(b"truncated")
    try:
        globals()["__file__"] = os.path.join(d, "machinery", "_x.py")
        ok, reason, path = verify()
        if ok:
            fails.append("verify() accepted a 9-byte file as the encoder data")
        if "bytes" not in (reason or "") or str(DATA_BYTES) not in (reason or ""):
            fails.append("the wrong-size refusal does not state the expected size: %r" % reason)
    finally:
        globals()["__file__"] = real_file
        restore()

    # ---------------------------------------------------------------- `s222-D3` arms
    ensure()
    enc, reason = purepy_encoding()

    # 6. THE FALLBACK ENGINE EXISTS AND MEASURES. A dispatch whose second arm was never driven
    #    is an instrument without a consumer.
    if enc is None:
        fails.append("the pure-Python engine will not build from the vendored data: %s" % reason)
    else:
        if len(enc.encode("the quick brown fox")) != 4:
            fails.append("the pure-Python engine does not measure 'the quick brown fox' as 4")

        # 7. THE ENGINE IS NAMED, AND THE TWO NAMES ARE DISTINCT. `s222-D3`'s "never silent".
        if ENGINE_PUREPY == ENGINE_TIKTOKEN or "purepy" not in ENGINE_PUREPY:
            fails.append("the fallback engine is not named distinctly from tiktoken")
        if "ESTIMATE" in ENGINE_PUREPY or "ESTIMATE" in ENGINE_TIKTOKEN:
            fails.append("an EXACT engine name contains the word ESTIMATE — a tier classifier "
                         "reading that word would grade an exact count as a guess")

        # 8. ⛔ THE MUTATION, BOTH WAYS — CORRUPT A MERGE RANK AND THE EQUALITY GATE MUST FIRE.
        #    This is the arm that makes the word "exact" checkable rather than decorative
        #    [[mutation-tests-the-clause-not-the-feature]]. It is skipped, LOUDLY, when there is
        #    no reference engine to compare against — never silently passed.
        try:
            import tiktoken                                    # noqa: F401
            have_ref = True
        except Exception:
            have_ref = False
        if not have_ref:
            could_not_run.append(
                "the equality-gate mutation arms (intact ⇒ green · corrupted rank ⇒ fires ⇒ "
                "green again) need real `tiktoken` as their reference, and it is not importable "
                "here. Not run, therefore not passed — `pip install tiktoken` and re-run to "
                "drive them.")
        else:
            import io
            rc_green, _ = equality_gate(roots=[os.path.abspath(__file__)],
                                        out=io.StringIO(), encoding_override=enc)
            if rc_green != 0:
                fails.append("the equality gate does not pass on an INTACT engine — every "
                             "other arm here is meaningless until it does")
            # plant the corruption: swap the ranks of two real merges so the merge ORDER
            # changes without the table gaining or losing an entry.
            victim = b" the"
            other = b" and"
            if victim not in enc.ranks or other not in enc.ranks:
                fails.append("the mutation arm's victim merges are not in the table — the "
                             "planted condition would be vacuous")
            else:
                keep_v, keep_o = enc.ranks[victim], enc.ranks[other]
                keep_cache = enc._cache
                try:
                    enc.ranks[victim], enc.ranks[other] = keep_o, keep_v
                    enc._cache = {}
                    buf = io.StringIO()
                    rc_red, _ = equality_gate(roots=[os.path.abspath(__file__)],
                                              out=buf, encoding_override=enc)
                    if rc_red != 1:
                        fails.append("a CORRUPTED merge rank did not fire the equality gate "
                                     "(rc %s) — the gate cannot see the thing it exists to "
                                     "see" % rc_red)
                    elif "EQUALITY GATE FAILED" not in buf.getvalue():
                        fails.append("the equality gate fired but did not SAY it failed")
                finally:
                    enc.ranks[victim], enc.ranks[other] = keep_v, keep_o
                    enc._cache = keep_cache
            # and back to green — a gate that stays red after the mutation is undone is
            # reporting on its own footprint, not on the engine.
            rc_again, _ = equality_gate(roots=[os.path.abspath(__file__)],
                                        out=io.StringIO(), encoding_override=enc)
            if rc_again != 0:
                fails.append("the equality gate did not return to GREEN after the corruption "
                             "was undone — it is reporting on its own state")

    # 9. THE DISPATCH PREFERS tiktoken WHEN IT IS THERE. Planted by asking `engine()` in an
    #    environment where tiktoken imports; the purepy branch is proven by the fresh-stage
    #    proof runs, which is the only honest place to prove it.
    try:
        import tiktoken                                        # noqa: F401
        if engine(announce=False) != ENGINE_TIKTOKEN:
            fails.append("tiktoken is importable but the dispatch did not choose it — the "
                         "ruling says the real library wins on speed whenever it is there")
    except ImportError:
        pass
    restore()
    return fails, could_not_run


def main(argv):
    if "--selftest" in argv:
        fails, could_not_run = selftest()
        for f in fails:
            print("FAIL: %s" % f)
        for c in could_not_run:
            print("COULD-NOT-RUN: %s" % c)
        print("_encoder_home selftest: %d failure(s), %d could-not-run — cache key · "
              "resolution · designer's env wins · refusal names the path · wrong size refused · "
              "fallback engine measures · engine named distinctly · equality gate fires on a "
              "corrupted rank and returns green · tiktoken wins when present"
              % (len(fails), len(could_not_run)))
        if fails:
            return 1
        return 2 if could_not_run else 0
    if "--equality-gate" in argv:
        rest = [a for a in argv if not a.startswith("--")]
        rc, _summary = equality_gate(roots=rest or None)
        return rc
    if "--timings" in argv:
        rest = [a for a in argv if not a.startswith("--")]
        return timings(rest or None)
    if "--check" in argv or not argv:
        return check()
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
