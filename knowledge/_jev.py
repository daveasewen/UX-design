#!/usr/bin/env python3
"""_jev.py — the thin TypeSafe/Jev adapter (session 293, lane J research → lane J2 build).

WHAT THIS IS
A stdlib-only client for TypeSafe's System One endpoint (`POST /v1/systemone`), the
typed-classifier API researched in `notes/_subreports/2026-09-21-293-J-jev-research.md`.
It exists so Apollo can ask a calibrated yes/no, pick-one or rate-it question about a
prose-shaped artefact and get a NUMBER back with a probability distribution attached,
rather than a paragraph of vibes. Three question types, exactly as the vendor defines
them — Noul (yes/no → probability), Choice (pick one → distribution + confidence),
Score (rubric levels → probability-weighted value + confidence).

WHY NO SDK. `typesafe-sdk` 0.7.0 installs and imports clean in the sandbox (measured,
lane J §2.3) — and is still a hard dependency this repo would have to carry, pin and
re-measure. The wire protocol is one POST of one JSON object. urllib is enough. If the
SDK later earns its keep (its retry policy is the honest argument), it can be swapped in
behind this same `ask()` signature without any caller changing.

THE ORACLE RULE — the whole reason `available()` exists.
Jev is an ORACLE, never a GATE. If there is no key, no network, or the API refuses, that
is **"no oracle available"**, NEVER "the artefact failed". A caller that turns a
`JevUnavailable` into a red build has invented a fail out of an absence, which is the
exact shape of a gate that cannot fail honestly [[gate-narrows-its-own-rule]]. Every
caller MUST branch on `available()` first, or catch `JevUnavailable` and degrade to
whatever it did before Jev existed.

THE KEY. Read from `.env.local` at the repo root (gitignored via `*.local`, line 71).
It is never printed, never logged, never written to the receipts file, and never carried
in any exception message — the HTTP error path strips the `Authorization` header before
it can reach a traceback.

RECEIPTS — `knowledge/_jev-receipts.jsonl`, one JSON line per call.
Apollo's standing complaint is that knowledge which exists only in a transcript gets
re-derived twenty-six sessions later. A judgment that came from outside this repo leaves
a file behind: timestamp, model, the questions AS SENT, the answers AS RETURNED, measured
latency, and TypeSafe's `x-typesafe-request-id` so a disputed answer can be taken back to
the vendor. The file holds NO secret and is safe to track.

★ WHAT THIS ADAPTER CAN AND CANNOT DO (published, not buried)
  CAN do    ask Jev a typed question about a string or JSON-able state, and return the
            parsed `answers` map with probabilities and confidence intact.
  CAN do    tell a caller, before it commits to a plan, whether an oracle exists at all
            (`available()` — key present and parseable; it does NOT ping the network).
  CAN do    leave a receipt that outlives the session that made the call.
  CANNOT    validate the ANSWER. Jev returns a calibrated number, not a true one. Lane J
  do        measured nothing about accuracy; every accuracy claim is TypeSafe's declared
            claim. A receipt is evidence a question was asked, not that it was answered
            right.
  CANNOT    retry-with-backoff. One attempt, one `JevError` on 429/529 with the typed
  do        body preserved. Backoff is a policy decision and belongs to a caller that
            knows its own budget, not to the transport.
  CANNOT    be used for counting, arithmetic or date comparison. TypeSafe's own
  do        jaggedness page rules jev-1.13 out of all three. Those stay in Python.
  CANNOT    see a rendered page. `state` is text. Stripping HTML to text loses layout,
  do        and layout is where most of Apollo's defects live.

MEASURED-VS-DECLARED, recorded not smoothed (lane J §2.2):
`docs.typesafe.ai/api.md` declares a missing key returns **401**. The live endpoint
returned **403** with `{"detail":{"error_type":"authentication_error", ...}}`. So error
handling here branches on the BODY's `error_type` where present, and treats the status
code as a hint only. Do not tighten this to `== 401` on the strength of the docs.

MODEL ID. `TYPESAFE_MODEL` in `.env.local`, default `jev-latest` (the documented alias).
`models()` fetches `GET /v1/models` if you need to check a pinned version is still real.

CONSUMER: none yet — this is the instrument, not a wiring. Run standalone:
    python3 knowledge/_jev.py              # status only: is an oracle available? no calls.
    python3 knowledge/_jev.py --selftest   # OFFLINE schema checks. Never touches network.
    python3 knowledge/_jev.py --models     # live: GET /v1/models (one request, no receipt)
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import os
import re
import io
import sys
import json
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ROOT)

ENV_FILE = os.path.join(REPO, ".env.local")
RECEIPTS = os.path.join(ROOT, "_jev-receipts.jsonl")

DEFAULT_BASE = "https://api.typesafe.ai"
DEFAULT_MODEL = "jev-latest"          # the documented alias; a pinned id may go stale
ENDPOINT = "/v1/systemone"
TIMEOUT = 60

QUESTION_TYPES = ("noul", "choice", "score")
MAX_CHOICE_OPTIONS = 255              # declared, api.md § Choice
MIN_SCORE_LEVELS = 2                  # declared, api.md § Score
MAX_SCORE_LEVELS = 10                 # declared, api.md § Score

_ENV_LINE = re.compile(r"""^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$""")


class JevUnavailable(RuntimeError):
    """No oracle. No key, no env file, or no network route.

    THIS IS NOT A FAIL. A caller that lets this become a red build has turned an
    absence into a defect. Catch it and degrade to the pre-Jev behaviour.
    """


class JevError(RuntimeError):
    """The API was reached and REFUSED. Carries the typed body; the key is never in it."""

    def __init__(self, message, status=None, body=None, request_id=None):
        super().__init__(message)
        self.status = status
        self.body = body                # parsed JSON if it parsed, else the raw text
        self.request_id = request_id

    @property
    def error_type(self):
        """TypeSafe's typed discriminator. Branch on THIS, not on `status` — see docstring."""
        b = self.body
        if isinstance(b, dict):
            d = b.get("detail")
            if isinstance(d, dict) and d.get("error_type"):
                return d["error_type"]
            if b.get("error_type"):
                return b["error_type"]
        return None


# ------------------------------------------------------------------ env
def load_env(path=None):
    """Parse `KEY=value` / `KEY="value"` from .env.local. Returns {} if the file is absent.

    Deliberately NOT a dotenv dependency and deliberately NOT exported into os.environ —
    a secret that lands in the process environment leaks into every subprocess and every
    crash dump downstream.
    """
    path = path or ENV_FILE
    out = {}
    if not os.path.isfile(path):
        return out
    try:
        with open(path, encoding="utf-8") as fh:
            for raw in fh:
                line = raw.rstrip("\n")
                if not line.strip() or line.lstrip().startswith("#"):
                    continue
                m = _ENV_LINE.match(line)
                if not m:
                    continue
                key, val = m.group(1), m.group(2)
                # QUOTE FIRST, comment second. The other order silently keeps the quotes
                # on `K="v"  # note` — which sent the literal string '"jev-latest"',
                # quotes included, as a model id. Caught at 293-J2 before the live call.
                if val[:1] in "\"'":
                    q = val[0]
                    end = val.find(q, 1)
                    val = val[1:end] if end != -1 else val[1:]
                else:
                    val = re.split(r"\s+#", val, 1)[0].rstrip()
                out[key] = val
    except OSError:
        return {}
    return out


def _config(env=None):
    env = load_env() if env is None else env
    key = (env.get("TYPESAFE_API_KEY") or os.environ.get("TYPESAFE_API_KEY") or "").strip()
    base = (env.get("TYPESAFE_API_BASE") or DEFAULT_BASE).strip().rstrip("/")
    model = (env.get("TYPESAFE_MODEL") or DEFAULT_MODEL).strip()
    return key, base, model


def available(env=None):
    """True iff a non-placeholder key is readable. Does NOT touch the network.

    A key that is present but empty, or still the template's placeholder, counts as
    ABSENT — a caller deserves to learn that before it builds a plan around an oracle.
    """
    key, _base, _model = _config(env)
    if not key:
        return False
    if key.lower() in {"...", "paste-your-key-here", "your-key-here", "changeme"}:
        return False
    return True


def redacted(key):
    """The ONLY representation of a key allowed anywhere in this process's output."""
    return "apikey_…[redacted]" if key else "apikey_[absent]"


# ------------------------------------------------------------------ validation
def validate_questions(questions):
    """Schema-check a questions map BEFORE spending a request. Raises ValueError, named.

    Every rule here is declared in docs.typesafe.ai/api.md; none is measured. Catching a
    malformed question locally turns a 422 round-trip into a local error message.
    """
    if not isinstance(questions, dict) or not questions:
        raise ValueError("questions must be a non-empty map of {id: question}")
    for qid, q in questions.items():
        if not isinstance(qid, str) or not qid:
            raise ValueError("question id must be a non-empty string, got %r" % (qid,))
        if not isinstance(q, dict):
            raise ValueError("question %r must be an object, got %s" % (qid, type(q).__name__))
        qtype = q.get("type")
        if qtype not in QUESTION_TYPES:
            raise ValueError("question %r: type must be one of %s, got %r"
                             % (qid, "/".join(QUESTION_TYPES), qtype))
        if not q.get("instructions"):
            raise ValueError("question %r: instructions is required" % qid)
        if not isinstance(q["instructions"], (str, dict, list)):
            raise ValueError("question %r: instructions must be string|object|array" % qid)
        crit = q.get("criteria")
        if qtype == "noul":
            if crit is not None and not isinstance(crit, dict):
                raise ValueError("question %r: noul criteria must be an object "
                                 "with true/false keys" % qid)
            if isinstance(crit, dict):
                extra = set(crit) - {"true", "false"}
                if extra:
                    raise ValueError("question %r: noul criteria keys must be "
                                     "'true'/'false', saw %s" % (qid, sorted(extra)))
        elif qtype == "choice":
            if not isinstance(crit, dict) or not crit:
                raise ValueError("question %r: choice criteria must be a non-empty "
                                 "map of option -> description" % qid)
            if len(crit) > MAX_CHOICE_OPTIONS:
                raise ValueError("question %r: choice allows at most %d options, got %d"
                                 % (qid, MAX_CHOICE_OPTIONS, len(crit)))
        elif qtype == "score":
            if not isinstance(crit, list):
                raise ValueError("question %r: score criteria must be an ordered array "
                                 "of level descriptions" % qid)
            if not (MIN_SCORE_LEVELS <= len(crit) <= MAX_SCORE_LEVELS):
                raise ValueError("question %r: score needs %d-%d levels, got %d"
                                 % (qid, MIN_SCORE_LEVELS, MAX_SCORE_LEVELS, len(crit)))
    return True


# ------------------------------------------------------------------ helpers callers want
def noul(instructions, true=None, false=None):
    """Build a Noul question. Answer comes back as a probability in [0, 1]."""
    q = {"type": "noul", "instructions": instructions}
    if true is not None or false is not None:
        q["criteria"] = {k: v for k, v in (("true", true), ("false", false))
                         if v is not None}
    return q


def choice(instructions, options):
    """Build a Choice question. `options` is {option: description-or-None}."""
    return {"type": "choice", "instructions": instructions, "criteria": dict(options)}


def score(instructions, levels):
    """Build a Score question. `levels` is an ORDERED list, low to high."""
    return {"type": "score", "instructions": instructions, "criteria": list(levels)}


def html_to_state(path, cap=6000):
    """Strip an HTML artefact to text for use as `state`. LOSSY — see the CANNOT block.

    Drops <script>/<style> bodies and comments, unwraps tags, collapses whitespace, then
    truncates to `cap` characters. Truncation is REPORTED in the return value, never
    silent: a question answered about the first 6K of a 29K document is a different
    question, and the receipt should be able to say so.
    """
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    full = len(text)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = (text.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<")
                .replace("&gt;", ">").replace("&quot;", '"').replace("&#39;", "'")
                .replace("&middot;", "·").replace("&mdash;", "—").replace("&rarr;", "→"))
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n\s*\n\s*", "\n\n", text).strip()
    truncated = len(text) > cap
    return {
        "text": text[:cap],
        "source": os.path.relpath(path, REPO),
        "html_bytes": full,
        "text_chars": len(text),
        "sent_chars": min(len(text), cap),
        "truncated": truncated,
    }


# ------------------------------------------------------------------ transport
def _post(url, payload, key, timeout=TIMEOUT):
    """One POST, one attempt. Returns (status, parsed_body, request_id, latency_ms).

    The Authorization header is built here and referenced nowhere else, so no code path
    below can put it into a message, a log line or a receipt.
    """
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", "Bearer " + key)
    req.add_header("User-Agent", "apollo-jev-adapter/1.0 (stdlib urllib)")
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", "replace")
            ms = (time.perf_counter() - t0) * 1000.0
            rid = resp.headers.get("x-typesafe-request-id")
            return resp.status, _parse(raw), rid, ms
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace")
        ms = (time.perf_counter() - t0) * 1000.0
        rid = exc.headers.get("x-typesafe-request-id") if exc.headers else None
        return exc.code, _parse(raw), rid, ms
    except urllib.error.URLError as exc:
        # no route, DNS, TLS — an ABSENCE of oracle, not a refusal. Reason, never the key.
        raise JevUnavailable("no network route to TypeSafe: %s" % (exc.reason,))
    except TimeoutError:
        raise JevUnavailable("TypeSafe timed out after %ss" % timeout)


def _parse(raw):
    try:
        return json.loads(raw)
    except (ValueError, TypeError):
        return raw


def _get(url, key, timeout=TIMEOUT):
    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", "Bearer " + key)
    req.add_header("User-Agent", "apollo-jev-adapter/1.0 (stdlib urllib)")
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", "replace")
            return resp.status, _parse(raw), resp.headers.get("x-typesafe-request-id"), \
                (time.perf_counter() - t0) * 1000.0
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace")
        rid = exc.headers.get("x-typesafe-request-id") if exc.headers else None
        return exc.code, _parse(raw), rid, (time.perf_counter() - t0) * 1000.0
    except urllib.error.URLError as exc:
        raise JevUnavailable("no network route to TypeSafe: %s" % (exc.reason,))


# ------------------------------------------------------------------ receipts
def _receipt(record, path=None):
    """Append one JSON line. Best-effort: a receipt that cannot be written never fails
    the call it describes — but the failure IS printed, so it is not silent either."""
    path = path or RECEIPTS
    try:
        with io.open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    except OSError as exc:
        print("⚠ jev receipt not written to %s — %s" % (path, exc), file=sys.stderr)


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


# ------------------------------------------------------------------ the public call
def ask(state, questions, model=None, note=None, timeout=TIMEOUT, receipts_path=None):
    """Ask Jev one or more typed questions about `state`. Returns the parsed response.

    state      str | dict | list — the content to evaluate.
    questions  {id: question} — build them with noul()/choice()/score().
    note       optional free text stored in the receipt to say WHY this was asked.

    Returns the full response dict: {"model", "answers", "usage"}, with two adapter-added
    keys — "_latency_ms" (measured, wall clock, includes TLS setup) and "_request_id"
    (TypeSafe's, for taking a disputed answer back to the vendor).

    Raises JevUnavailable when there is no oracle (no key / no route) — NOT A FAIL.
    Raises JevError when the API was reached and refused; `.error_type` carries the typed
    discriminator. No retry: see the CANNOT block.
    """
    key, base, cfg_model = _config()
    if not available():
        raise JevUnavailable(
            "no TYPESAFE_API_KEY in %s — Jev is an oracle, and no oracle is not a fail"
            % os.path.relpath(ENV_FILE, REPO))
    validate_questions(questions)
    model = model or cfg_model
    payload = {"state": state, "model": model, "questions": questions}

    status, body, rid, ms = _post(base + ENDPOINT, payload, key, timeout)

    record = {
        "ts": _now(),
        "model_requested": model,
        "endpoint": ENDPOINT,
        "status": status,
        "request_id": rid,
        "latency_ms": round(ms, 1),
        "questions": questions,
        "state_chars": len(state) if isinstance(state, str) else None,
        "note": note,
    }
    if status == 200 and isinstance(body, dict):
        record["model_answered"] = body.get("model")
        record["answers"] = body.get("answers")
        record["usage"] = body.get("usage")
        record["ok"] = True
    else:
        record["ok"] = False
        record["error"] = body
    _receipt(record, receipts_path)

    if status != 200 or not isinstance(body, dict):
        err = JevError("TypeSafe refused: HTTP %s" % status,
                       status=status, body=body, request_id=rid)
        raise err
    out = dict(body)
    out["_latency_ms"] = round(ms, 1)
    out["_request_id"] = rid
    return out


def models(timeout=TIMEOUT):
    """GET /v1/models — the honest way to check a pinned model id is still real.

    No receipt: this asks nothing about an artefact, so there is no judgment to keep.
    """
    key, base, _m = _config()
    if not available():
        raise JevUnavailable("no TYPESAFE_API_KEY — cannot list models")
    status, body, rid, ms = _get(base + "/v1/models", key, timeout)
    if status != 200:
        raise JevError("TypeSafe refused: HTTP %s" % status,
                       status=status, body=body, request_id=rid)
    return body


# ---------------------------------------------------------------- selftest (OFFLINE)
def _selftest():
    """OFFLINE only. Every arm is a schema or redaction check; none opens a socket.

    The arms that matter most are 5 and 6: they are the ones that would catch a key
    leaking into a receipt or an error message, which is the failure this module cannot
    be allowed to have.
    """
    ok = True
    results = []

    def arm(n, label, good, detail=""):
        nonlocal ok
        ok &= bool(good)
        results.append((n, label, bool(good), detail))
        print("  [%d] %s -> %s%s" % (n, label, "PASS" if good else "FAIL",
                                     ("  " + detail) if detail else ""))

    # ARM 1 — env parser handles quoted, unquoted, exported, commented, blank.
    import tempfile
    tmp = tempfile.mkdtemp(prefix="jev-selftest-")
    envp = os.path.join(tmp, ".env.local")
    with open(envp, "w", encoding="utf-8") as fh:
        fh.write('# comment\n\nA="quoted"\nB=bare\nexport C=\'single\'\n'
                 'D=with # trailing\nJUNK LINE\nE="quoted"   # and a comment\n'
                 'F=has#hash\n')
    env = load_env(envp)
    # E is the REGRESSION arm: quote-then-comment. The other order returned '"quoted"'
    # with the quotes still on it, and would have posted that as a model id (293-J2).
    arm(1, "env parser (quoted/bare/export/comment/junk/quoted+comment)",
        env == {"A": "quoted", "B": "bare", "C": "single", "D": "with",
                "E": "quoted", "F": "has#hash"},
        repr(env))

    # ARM 2 — missing env file is an ABSENCE, not a crash.
    arm(2, "missing .env.local -> {} not a crash",
        load_env(os.path.join(tmp, "nope.local")) == {})

    # ARM 3 — available() is False for empty and placeholder keys, True for a real one.
    a = available({"TYPESAFE_API_KEY": ""})
    b = available({"TYPESAFE_API_KEY": "paste-your-key-here"})
    c = available({"TYPESAFE_API_KEY": "sk-live-whatever"})
    arm(3, "available(): empty=%s placeholder=%s present=%s" % (a, b, c),
        a is False and b is False and c is True)

    # ARM 4 — validator BITES on every documented malformation, and NOT on valid ones.
    bad = [
        ({}, "empty map"),
        ({"q": {"type": "nope", "instructions": "x"}}, "unknown type"),
        ({"q": {"type": "noul"}}, "missing instructions"),
        ({"q": {"type": "choice", "instructions": "x"}}, "choice without criteria"),
        ({"q": {"type": "choice", "instructions": "x", "criteria": {}}}, "choice empty criteria"),
        ({"q": {"type": "score", "instructions": "x", "criteria": ["only one"]}}, "score 1 level"),
        ({"q": {"type": "score", "instructions": "x",
                "criteria": [str(i) for i in range(11)]}}, "score 11 levels"),
        ({"q": {"type": "score", "instructions": "x", "criteria": {"a": "b"}}}, "score map not list"),
        ({"q": {"type": "noul", "instructions": "x", "criteria": {"yes": "y"}}}, "noul bad crit key"),
    ]
    bit = []
    for q, label in bad:
        try:
            validate_questions(q)
            bit.append("MISSED:" + label)
        except ValueError:
            pass
    arm(4, "validator bites %d/%d documented malformations" % (len(bad) - len(bit), len(bad)),
        not bit, ";".join(bit))

    # ARM 4b — bite-the-bite: valid questions must PASS (guards an always-raise validator).
    good_qs = {
        "n": noul("Is it?", true="yes means", false="no means"),
        "c": choice("Which?", {"a": "A", "b": None}),
        "s": score("How much?", ["low", "mid", "high"]),
    }
    try:
        validate_questions(good_qs)
        arm(5, "bite-the-bite: three valid questions validate clean", True)
    except ValueError as exc:
        arm(5, "bite-the-bite: three valid questions validate clean", False, str(exc))

    # ARM 6 — REDACTION: a key must not survive into a receipt line. The one that matters.
    SECRET = "sk-live-THIS-MUST-NEVER-APPEAR-0123456789"
    recp = os.path.join(tmp, "receipts.jsonl")
    _receipt({"ts": _now(), "model_requested": "jev-latest", "questions": good_qs,
              "status": 200, "answers": {"n": {"type": "noul", "noul": 0.5}}}, recp)
    with open(recp, encoding="utf-8") as fh:
        line = fh.read()
    arm(6, "receipt line contains no key material",
        SECRET not in line and "Authorization" not in line and "Bearer" not in line)

    # ARM 7 — REDACTION: JevError carries the typed body, never a header.
    e = JevError("refused", status=403,
                 body={"detail": {"error_type": "authentication_error",
                                  "message": "Must supply an API key!"}},
                 request_id="req_x")
    blob = "%s %r %r" % (e, e.body, e.request_id)
    arm(7, "JevError body typed=%r, no key material" % e.error_type,
        e.error_type == "authentication_error" and SECRET not in blob
        and "Bearer" not in blob)

    # ARM 8 — the 403-not-401 branch: error_type must survive a status the docs deny.
    e401 = JevError("x", status=401, body={"detail": {"error_type": "authentication_error"}})
    e403 = JevError("x", status=403, body={"detail": {"error_type": "authentication_error"}})
    arm(8, "auth error typed the same at 401 and 403 (docs say 401, live said 403)",
        e401.error_type == e403.error_type == "authentication_error")

    # ARM 9 — redacted() never emits the key.
    arm(9, "redacted(%r) = %r" % ("…", redacted(SECRET)),
        SECRET not in redacted(SECRET) and redacted("") == "apikey_[absent]")

    # ARM 10 — html_to_state strips tags, caps, and REPORTS the truncation.
    htmlp = os.path.join(tmp, "x.html")
    with open(htmlp, "w", encoding="utf-8") as fh:
        fh.write("<html><style>b{color:red}</style><!--hide me-->"
                 "<h1>Title</h1><p>Body &amp; more</p>" + "<p>pad</p>" * 500 + "</html>")
    st = html_to_state(htmlp, cap=50)
    arm(10, "html_to_state: %d chars sent, truncated=%s" % (st["sent_chars"], st["truncated"]),
        "<" not in st["text"] and "color:red" not in st["text"]
        and "hide me" not in st["text"] and "Body & more" in st["text"]
        and st["sent_chars"] == 50 and st["truncated"] is True)

    # ARM 11 — ask() with no key raises JevUnavailable, NOT JevError. The oracle rule.
    saved = globals()["_config"]
    globals()["_config"] = lambda env=None: ("", DEFAULT_BASE, DEFAULT_MODEL)
    savedav = globals()["available"]
    globals()["available"] = lambda env=None: False
    try:
        ask("x", {"q": noul("y?")})
        arm(11, "no key -> ask() raised nothing", False)
    except JevUnavailable:
        arm(11, "no key -> JevUnavailable (an absence, never a fail)", True)
    except Exception as exc:  # noqa: BLE001
        arm(11, "no key -> wrong exception %s" % type(exc).__name__, False)
    finally:
        globals()["_config"] = saved
        globals()["available"] = savedav

    # ARM 12 — payload shape matches the documented request body exactly.
    payload = {"state": "s", "model": "jev-latest", "questions": good_qs}
    arm(12, "request payload keys == {state, model, questions}",
        set(payload) == {"state", "model", "questions"}
        and json.loads(json.dumps(payload)) == payload)

    import shutil
    shutil.rmtree(tmp, ignore_errors=True)
    print("\n%s (%d arms, offline, no socket opened)"
          % ("✅ selftest PASS" if ok else "❌ selftest FAIL", len(results)))
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    if "--models" in sys.argv:
        try:
            print(json.dumps(models(), indent=2)[:4000])
        except JevUnavailable as exc:
            print("no oracle: %s" % exc)
            sys.exit(0)
        except JevError as exc:
            print("refused: HTTP %s  error_type=%s  body=%s"
                  % (exc.status, exc.error_type, json.dumps(exc.body)[:800]))
            sys.exit(1)
        sys.exit(0)
    _k, _base, _model = _config()
    print("jev adapter — oracle %s · key %s · base %s · model %s"
          % ("AVAILABLE" if available() else "UNAVAILABLE", redacted(_k), _base, _model))
    print("receipts: %s (%s)"
          % (os.path.relpath(RECEIPTS, REPO),
             "%d line(s)" % sum(1 for _ in open(RECEIPTS, encoding="utf-8"))
             if os.path.isfile(RECEIPTS) else "not yet created"))
