#!/usr/bin/env python3
"""_ngram.py — n-gram helpers for the Memento doors (#269, research
`_RESEARCH-ngram-lookups-2026-09-13-v1.html`, Dave's "go for it" 2026-09-13).

A LIBRARY, not a door: pure Python, no third-party import, no I/O of its own, nothing
written. Three tools, each the smallest thing that does its job at this corpus size
(~25 MB, ~2.2K records — a dict built in seconds beats a suffix array here):

  word bigrams   — `bigram_index(texts)` → {"a b": {record ids}};  `phrase_score(q, text)`
                   counts how many of a query's adjacent word pairs a text keeps ADJACENT,
                   so "six weeks" outranks a record that has "six" on line 3 and "weeks" on
                   line 90. (Phrase-aware RANKING inside the shipped door is NOT wired —
                   `_search_core.py` / `_memento_search.py` are pinned byte-identical to the
                   memento-package by `_validate_package_delta.py`, and a pack change is a
                   release. Dave's.)
  char trigrams  — `Vocabulary(words)`; `.nearest(word)` maps a misspelt word to the
                   corpus's real words by trigram overlap, ties broken by edit distance,
                   so "ratifed" → "ratified". Used by `_quote_gate.py` for "did you mean".
  shingles       — `shingles(text, k)` + `jaccard(a, b)` for near-duplicate detection,
                   used by `_near_dupes.py` (the dream-pass candidate list).

Consumers import it beside them (`sys.path.insert(0, HERE)`); it is NOT in the pack ship
list and must not be until Dave rules the retrieval question in the #220 addendum.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import re
from collections import defaultdict

WORD_RE = re.compile(r"[a-z0-9']+")


def words(s):
    return WORD_RE.findall(s.lower())


# ------------------------------------------------------------------ word bigrams
def bigrams(ws):
    return list(zip(ws, ws[1:]))


def bigram_index(texts_by_id):
    """{id: text} → {"a b": set(ids)}."""
    idx = defaultdict(set)
    for rid, t in texts_by_id.items():
        for a, b in set(bigrams(words(t))):
            idx[a + " " + b].add(rid)
    return idx


def phrase_score(query, text):
    """(kept, total) — how many of the query's adjacent word pairs stay adjacent in text."""
    qb = set(bigrams(words(query)))
    if not qb:
        return 0, 0
    tb = set(bigrams(words(text)))
    return len(qb & tb), len(qb)


# ------------------------------------------------------------------ char trigrams
def trigrams(word):
    w = f" {word} "
    return {w[i:i + 3] for i in range(len(w) - 2)}


def edit_distance(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


class Vocabulary:
    """The words a corpus actually uses, indexed by character trigram."""

    def __init__(self, wordlist):
        self.words = set(w for w in wordlist if len(w) >= 3)
        self.by_tri = defaultdict(set)
        for w in self.words:
            for t in trigrams(w):
                self.by_tri[t].add(w)

    def __contains__(self, w):
        return w in self.words

    def nearest(self, word, k=3, min_overlap=0.5):
        """[(candidate, overlap, edit_distance)] best first; [] if nothing overlaps enough.
        An exact vocabulary word returns itself alone — nothing to correct."""
        word = word.lower()
        if word in self.words:
            return [(word, 1.0, 0)]
        qt = trigrams(word)
        if not qt:
            return []
        counts = defaultdict(int)
        for t in qt:
            for w in self.by_tri.get(t, ()):
                counts[w] += 1
        cands = []
        for w, c in counts.items():
            ov = c / len(qt | trigrams(w))  # Jaccard on trigram sets
            if ov >= min_overlap * 0.5:     # loose pre-filter; edit distance decides
                cands.append((w, round(ov, 2), edit_distance(word, w)))
        cands.sort(key=lambda x: (x[2], -x[1], x[0]))
        cands = [c for c in cands if c[2] <= max(1, len(word) // 4)]
        return cands[:k]


# ------------------------------------------------------------------ shingles
def shingles(text, k=8):
    ws = words(text)
    if len(ws) < k:
        return {" ".join(ws)} if ws else set()
    return {" ".join(ws[i:i + k]) for i in range(len(ws) - k + 1)}


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


# ------------------------------------------------------------------ selftest
def selftest():
    fails = []

    def bite(name, cond):
        print(f"[{'OK' if cond else 'FAIL'}] {name}")
        if not cond:
            fails.append(name)

    bite("phrase_score keeps adjacency: 'six weeks' in 'six weeks on the clock'",
         phrase_score("six weeks", "six weeks on the clock") == (1, 1))
    bite("…and refuses split words: 'six … weeks' apart scores 0 of 1",
         phrase_score("six weeks", "six days and two weeks") == (0, 1))
    idx = bigram_index({"r1": "amber on white", "r2": "white on amber"})
    bite("bigram_index is ordered: 'amber on' → r1 only", idx["amber on"] == {"r1"})
    v = Vocabulary(["ratified", "ratifies", "rationed", "salutation", "mutation", "descender",
                    "descenders", "chromium", "chromatic", "the"])
    bite("nearest: ratifed → ratified", v.nearest("ratifed")[0][0] == "ratified")
    bite("nearest: salutaton → salutation", v.nearest("salutaton")[0][0] == "salutation")
    bite("nearest: chromuim → chromium (edit distance breaks the trigram tie)",
         v.nearest("chromuim")[0][0] == "chromium")
    bite("nearest: a real word returns itself, distance 0", v.nearest("descender") == [("descender", 1.0, 0)])
    bite("nearest: nonsense returns nothing", v.nearest("zzqxv") == [])
    a = shingles("one two three four five six seven eight nine ten", 4)
    b = shingles("one two three four five six seven eight nine eleven", 4)
    bite("shingles/jaccard: one changed word of ten scores between 0.5 and 0.9",
         0.5 < jaccard(a, b) < 0.9)
    bite("jaccard of disjoint sets is 0", jaccard({"a"}, {"b"}) == 0.0)
    bite("mutation: edit_distance('kitten','sitting') == 3", edit_distance("kitten", "sitting") == 3)
    print("ngram selftest:", "FAIL " + ", ".join(fails) if fails else "OK")
    return 1 if fails else 0


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    print(__doc__)
