#!/usr/bin/env python3
"""Launchpad step four — the ranker seam (spec § 7).

`rank(eligible, context, switch)`:
  * switch "off" (the default, s305-D47 "switch off by default") returns the evaluator's order untouched and
    never imports knowledge/_jev.py (s294-D10: nothing may require Jev);
  * switch "on" may only RE-ORDER the eligible list, never add to it or drop from it, under a time limit;
    on any failure, a slow answer or an answer that is not a re-ordering, it falls back to the rules' order
    and says so in `fallback`.
Tonight the on-branch is a stub that raises with the two words "step six" (the proposal's step six is Jev
side by side); `_jev.py` is not called anywhere.
"""
import time

TIME_LIMIT_MS = 200  # [spec] the seam's budget for a ranker answer; the spec names a limit, not a number


def _ranker_stub(slugs, context):
    raise NotImplementedError("step six")


RANKER = _ranker_stub


def rank(eligible, context, switch="off"):
    """`eligible` is the evaluator's ordered list of slugs. Returns (ordered_slugs, ranker_record)."""
    rules = list(eligible)
    if switch != "on":
        return rules, {"switch": "off", "answer": None, "fallback": "rules-order"}
    t0 = time.perf_counter()
    try:
        answer = RANKER(list(rules), dict(context))
    except Exception as e:  # the stub raises tonight; a real ranker may fail too
        return rules, {"switch": "on", "answer": None, "fallback": "rules-order",
                       "error": "%s: %s" % (type(e).__name__, e)}
    ms = (time.perf_counter() - t0) * 1000
    if ms > TIME_LIMIT_MS:
        return rules, {"switch": "on", "answer": None, "fallback": "rules-order", "error": "over time limit"}
    if sorted(answer or []) != sorted(rules):
        return rules, {"switch": "on", "answer": list(answer or []), "fallback": "rules-order",
                       "error": "not a re-ordering of the eligible list"}
    return list(answer), {"switch": "on", "answer": list(answer), "fallback": None}
