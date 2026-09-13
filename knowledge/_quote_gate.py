#!/usr/bin/env python3
"""_quote_gate.py — THE QUOTE DOOR: "are these Dave's words, verbatim?" (#269, ADVISORY).

WHY (ruled: "test against Dave's OWN WORDS" — the conflated-fix law; research
`_RESEARCH-ngram-lookups-2026-09-13-v1.html`, Dave's "go for it" 2026-09-13): a lane, a
wrap or a deck card presents a sentence as Dave's and nothing checks it. Memory is a
reconstruction; the record is the quote. Probed at #269: "six month project" → 0 hits,
"6 month project" → 2. The paraphrase drifted a single word and no instrument saw it.

WHAT IT DOES: exact-phrase lookup (a word-n-gram lookup, brute-force — the corpus is
~25 MB and one pass is ~0.1 s, so no suffix array is built) over the Memento index that
`_memento_search.py` already reads. Each phrase is either FOUND — with record id,
file and section line — or NOT FOUND, with the NEAREST real phrase: the record sharing
the most word-bigrams with the query, and the longest run of words they have in common.

ADVISORY BY RULING SHAPE: exit 0 always, marker `QUOTE-GATE ADVISORY`. `--strict` makes a
miss exit 1 — nothing in the repo calls it strict; wiring it into `_capture_gate.py` is
a gate change and is Dave's, not this file's. This door NEVER writes.

Normalisation (both sides): lowercase · curly quotes → straight · runs of whitespace →
one space · a trailing full stop on the phrase ignored. Nothing else — "six" ≠ "6" on
purpose; that difference IS the finding.

Usage:
  python3 knowledge/_quote_gate.py "6 month project may become 6 weeks"
  python3 knowledge/_quote_gate.py "phrase one" "phrase two" --json
  python3 knowledge/_quote_gate.py --file notes/_DEMO-SLIDES-apollo-2026-09-12-v7.html
        # checks every quoted span (“…” or "…") of 4+ words found in the file
  python3 knowledge/_quote_gate.py "phrase" --strict     # exit 1 on a miss
  python3 knowledge/_quote_gate.py --selftest
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _search_core as core
import _ngram as ng

INDEX_PATH = os.path.join(HERE, "_memento-index.json")
MARK = "QUOTE-GATE ADVISORY"
MIN_WORDS = 4  # shorter spans are not quotes, they are vocabulary

_QUOTES = {"“": '"', "”": '"', "‘": "'", "’": "'", " ": " "}


def norm(s):
    for k, v in _QUOTES.items():
        s = s.replace(k, v)
    s = re.sub(r"\s+", " ", s.lower()).strip()
    return s.rstrip(".")


def words(s):
    return re.findall(r"[a-z0-9']+", s)


def bigrams(ws):
    return set(zip(ws, ws[1:]))


def record_text(r):
    return norm(" ".join(str(r.get(k, "")) for k in ("head", "text")))


def longest_common_run(a, b):
    """Longest contiguous run of words shared by word lists a and b."""
    best, best_i = 0, 0
    prev = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best:
                    best, best_i = cur[j], i
        prev = cur
    return a[best_i - best:best_i]


def build_vocab(texts):
    vocab = set()
    for t in texts:
        vocab.update(words(t))
    return ng.Vocabulary(vocab)


def check_phrase(records, phrase, texts=None, vocab=None):
    q = norm(phrase)
    texts = texts if texts is not None else [record_text(r) for r in records]
    hits = [i for i, t in enumerate(texts) if q in t]
    out = {"phrase": phrase, "found": bool(hits)}
    if hits:
        out["records"] = [{"id": records[i]["id"], "file": records[i].get("file"),
                           "line": records[i].get("line")} for i in hits[:5]]
        out["count"] = len(hits)
        return out
    qw = words(q)
    qb = bigrams(qw)
    best, best_score = None, 0
    for i, t in enumerate(texts):
        if not qb:
            break
        s = 0
        for a, b in qb:
            if a + " " + b in t:
                s += 1
        if s > best_score:
            best, best_score = i, s
    if best is not None and best_score:
        run = longest_common_run(qw, words(texts[best]))
        out["nearest"] = {"id": records[best]["id"], "file": records[best].get("file"),
                          "line": records[best].get("line"),
                          "shared_bigrams": f"{best_score} of {len(qb)}",
                          "longest_common_run": " ".join(run)}
    if vocab is not None:
        # words the corpus has never used — a typo, or a word that is yours not his
        unknown = [w for w in qw if len(w) >= 4 and w not in vocab]
        if unknown:
            out["unknown_words"] = {w: [c for c, _, _ in vocab.nearest(w)] for w in unknown}
    return out


def spans_from_file(path):
    raw = open(path, encoding="utf-8").read()
    raw = re.sub(r"<[^>]+>", " ", raw)  # HTML tags → space; leaves the copy
    for k, v in _QUOTES.items():
        raw = raw.replace(k, v)
    spans = []
    for m in re.finditer(r'"([^"\n]{12,400})"', raw):
        s = m.group(1).strip()
        if len(words(norm(s))) >= MIN_WORDS:
            spans.append(s)
    seen, uniq = set(), []
    for s in spans:
        if norm(s) not in seen:
            seen.add(norm(s)); uniq.append(s)
    return uniq


def report(results, as_json=False):
    if as_json:
        print(json.dumps({"marker": MARK, "results": results}, indent=2, ensure_ascii=False))
        return
    found = [r for r in results if r["found"]]
    missed = [r for r in results if not r["found"]]
    print(f"{MARK} — {len(found)} verbatim · {len(missed)} not in the record")
    for r in found:
        first = r["records"][0]
        more = f" (+{r['count'] - 1} more)" if r["count"] > 1 else ""
        print(f"  ✅ \"{r['phrase']}\"\n       {first['id']} · {first['file']}:{first['line']}{more}")
    for r in missed:
        print(f"  ❌ \"{r['phrase']}\"")
        n = r.get("nearest")
        if n:
            print(f"       nearest {n['id']} · {n['file']}:{n['line']} · bigrams {n['shared_bigrams']}"
                  f"\n       longest run in common: \"{n['longest_common_run']}\"")
        else:
            print("       no record shares even two adjacent words with it")
        for w, sugg in (r.get("unknown_words") or {}).items():
            print(f"       \"{w}\" is not a word the record uses" + (f" — did you mean {', '.join(sugg)}?" if sugg else ""))


# ------------------------------------------------------------------ selftest
def selftest():
    """Every bite can FAIL — green-by-construction is not a test."""
    fails = []

    def bite(name, cond):
        print(f"[{'OK' if cond else 'FAIL'}] {name}")
        if not cond:
            fails.append(name)

    recs = [
        {"id": "R-1", "kind": "x", "file": "a.md", "line": 10, "head": "estimate",
         "text": "lets say something like a 6 month project may become 6 weeks or even less"},
        {"id": "R-2", "kind": "x", "file": "b.md", "line": 20, "head": "cheap",
         "text": "“keep them if they are cheap” he said,  twice"},
        {"id": "R-3", "kind": "x", "file": "c.md", "line": 30, "head": "other", "text": "nothing here"},
    ]
    texts = [record_text(r) for r in recs]
    r = check_phrase(recs, "6 month project may become 6 weeks", texts)
    bite("verbatim phrase is FOUND with id+file+line",
         r["found"] and r["records"][0] == {"id": "R-1", "file": "a.md", "line": 10})
    r = check_phrase(recs, "six month project may become 6 weeks", texts)
    bite("paraphrase (six vs 6) is NOT found", not r["found"])
    bite("…and names the nearest record", r.get("nearest", {}).get("id") == "R-1")
    bite("…with the longest common run", r["nearest"]["longest_common_run"] == "month project may become 6 weeks")
    r = check_phrase(recs, "Keep them if they are cheap.", texts)
    bite("curly quotes, case, double spaces and a full stop are normalised", r["found"] and r["count"] == 1)
    r = check_phrase(recs, "zebra crossing at dawn", texts)
    bite("a phrase sharing no bigram has no nearest", not r["found"] and "nearest" not in r)
    vocab = build_vocab(texts)
    r = check_phrase(recs, "6 month projct may become 6 weeks", texts, vocab)
    bite("a misspelt word is named with 'did you mean'", r.get("unknown_words") == {"projct": ["project"]})
    r = check_phrase(recs, "6 month project may become 6 weeks", texts, vocab)
    bite("a verbatim hit carries no unknown words", r["found"] and "unknown_words" not in r)
    # mutation: the finder must be able to go red — a corrupted normaliser would find the paraphrase
    bite("mutation: 'six'≠'6' is preserved by norm()", norm("six") != norm("6"))
    # file span extraction
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write('<p>He said “keep them if they are cheap” and "no" and <b>"a 6 month project may become 6 weeks"</b></p>')
        p = f.name
    spans = spans_from_file(p)
    os.unlink(p)
    bite("--file extracts 4+ word quoted spans only (2 of 3)", len(spans) == 2)
    # the door never writes: no open(..., 'w') in this module outside selftest's tempfile
    src = open(__file__, encoding="utf-8").read().split("def selftest")[0]
    bite("door has no write path", "open(" in src and '"w"' not in src and "'w'" not in src)
    print("quote-gate selftest:", "FAIL " + ", ".join(fails) if fails else "OK")
    return 1 if fails else 0


def main():
    argv = sys.argv[1:]
    if "--selftest" in argv:
        sys.exit(selftest())
    as_json = "--json" in argv
    strict = "--strict" in argv
    phrases = []
    files = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--file":
            i += 1
            if i >= len(argv):
                raise SystemExit("quote-gate: --file needs a path")
            files.append(argv[i])
        elif a.startswith("--"):
            if a not in ("--json", "--strict"):
                raise SystemExit(f"quote-gate: unknown flag {a} — see --help")
        else:
            phrases.append(a)
        i += 1
    for p in files:
        if not os.path.exists(p):
            raise SystemExit(f"quote-gate: no such file {p}")
        phrases += spans_from_file(p)
    if not phrases:
        raise SystemExit("quote-gate: nothing to check — give a phrase, or --file <path> with quoted spans. See --help.")
    records = core.load_records_or_refuse(INDEX_PATH, "quote-gate")["records"]
    texts = [record_text(r) for r in records]
    vocab = build_vocab(texts)
    results = [check_phrase(records, p, texts, vocab) for p in phrases]
    report(results, as_json)
    if strict and any(not r["found"] for r in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
