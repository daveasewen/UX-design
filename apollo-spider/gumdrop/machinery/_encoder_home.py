#!/usr/bin/env python3
"""_encoder_home.py — the ONE place this pack finds its VENDORED `cl100k_base` encoder data.

WHY THIS EXISTS (`s222-D2`, Dave, #222). On the first live Copilot-bridge session the chain
inscription refused, correctly, because `tiktoken` could not fetch its encoding file: the
designer's machine could not reach `openaipublic.blob.core.windows.net`. The refusal was right
and the situation was wrong. Dave: *"I need this to work out of the box for the designers."*
So the encoding data now SHIPS INSIDE THE PACK (`_encoder-cache/`, see its README), and this
module is the single home of the knowledge that connects the two.

WHAT IT DOES, IN ONE LINE. Before anything in this pack asks `tiktoken` for an encoder, this
module points `TIKTOKEN_CACHE_DIR` at the vendored directory — with `os.environ.setdefault`, so
**a designer who has set their own `TIKTOKEN_CACHE_DIR` still wins**. It downloads nothing, it
writes nothing, and it never touches a file.

⛔ WHAT IT MUST NEVER DO — THE NO-ESTIMATE PRINCIPLE IS UNTOUCHED. This module makes the real
measurement REACHABLE; it never makes a failure quieter. If the vendored file is missing,
renamed, or the wrong size, this module says so LOUD AND BY NAME on stderr, naming the exact
path it looked for, and then gets out of the way so the existing refusal fires exactly as it
does today. A machine that cannot load even the vendored data still gets the refusal, never a
guess. There is no path through here that turns an estimate into a measurement.

ONE HOME, RESOLVED FROM WHERE THIS FILE SITS. Like the rest of Memento's machinery, this module
does not know its own absolute location and does not need to: it walks up from `__file__`
looking for a `_encoder-cache/` directory that actually contains the data file. That is why it
works both at `memento-package/machinery/` and at
`memento-package/claude-plugin/memento/machinery/`, which sit at different depths.

⚠ THE FILENAME IS A CACHE KEY, NOT A HASH OF THE CONTENT. `tiktoken` looks the data up at
`$TIKTOKEN_CACHE_DIR/<sha1 of the URL it would have downloaded>`. Renaming the file breaks it.

⚠ INTEGRITY, AND WHAT THIS MODULE DELIBERATELY DOES NOT RE-CHECK ON EVERY IMPORT. At import
this checks that the file EXISTS and that its SIZE is right — cheap, and it catches the two
realistic corruptions (missing, truncated). It does NOT sha256 1.6 MB on every process start.
It does not have to: `tiktoken` itself verifies the content hash of anything it reads from the
cache (`tiktoken_ext/openai_public.cl100k_base()` passes `expected_hash=`), so scrambled bytes
are rejected by the library and fall through to the existing refusal rather than producing a
wrong number. `verify(deep=True)` / `--check` does the full sha256 when you want it stated.

USAGE
    # as a library — the pack's own entry points do this, once, at import
    import _encoder_home; _encoder_home.ensure()

    # as a check a designer can run — this is the § Before you start check
    python3 memento-package/machinery/_encoder_home.py --check
"""
import hashlib
import os
import sys

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

_ANNOUNCED = False                # loud once per process, not once per call


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
    """
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


# ------------------------------------------------------------------------------ the check
def check(stream=None):
    """The out-of-the-box check, end to end. Exit code 0 iff this machine can measure tokens
    with the REAL encoder right now. Prints what it did, in the order it did it.

    ⚠ This drives the whole path rather than reporting on it: it re-derives the cache key from
    the URL, verifies the vendored bytes deeply, sets the variable, then actually ENCODES a
    string. A check that stopped at 'the file is there' would pass on a pack whose encoder
    never loads [[mutation-tests-the-clause-not-the-feature]]."""
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
        import tiktoken
    except Exception as ex:                                   # noqa: BLE001 - named below
        out.write("%s ⛔ REFUSED — the vendored data is fine, but the `tiktoken` package is "
                  "not installed here (%s: %s). Run `pip install tiktoken`. The wheel is the "
                  "one install step this pack still needs; the DATA is already inside it.\n"
                  % (MARKER, type(ex).__name__, ex))
        return 1
    try:
        n = len(tiktoken.get_encoding(ENCODING_NAME).encode("the quick brown fox"))
    except Exception as ex:                                   # noqa: BLE001 - named below
        out.write("%s ⛔ REFUSED — tiktoken is installed and the vendored data is present, but "
                  "the encoder still would not load (%s: %s).\n" % (MARKER, type(ex).__name__, ex))
        return 1
    if n != 4:
        out.write("%s ⛔ REFUSED — the encoder loaded but measured 'the quick brown fox' as %d "
                  "tokens, not 4. That is not %s.\n" % (MARKER, n, ENCODING_NAME))
        return 1
    out.write("tiktoken OK — %d tokens, measured with the encoder data inside this pack "
              "(no download, no environment variable to set).\n" % n)
    return 0


def selftest():
    """Bites that FAIL when the module stops doing its job. Each one plants the condition.

    ⚠ Every arm restores the environment it disturbed — a selftest that leaves
    `TIKTOKEN_CACHE_DIR` set would hand a false green to whatever runs next."""
    fails = []
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

    return fails


def main(argv):
    if "--selftest" in argv:
        fails = selftest()
        for f in fails:
            print("FAIL: %s" % f)
        print("_encoder_home selftest: %d failure(s) — cache key · resolution · designer's env "
              "wins · refusal names the path · wrong size refused" % len(fails))
        return 1 if fails else 0
    if "--check" in argv or not argv:
        return check()
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
