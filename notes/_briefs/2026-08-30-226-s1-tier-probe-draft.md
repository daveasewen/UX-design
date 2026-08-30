# DRAFT — W-273 S1: the tier probe stops lying (UNWIRED, awaiting Dave)

**Status: DRAFT. Nothing in this file is landed.** The patch below was driven as a function
object against the real modules at #226 (transcript inside); no repo `.py` changed. Enacting
it is one commit on Dave's word — S1 is first on the W-273 strip list and **saves 0 tokens:
its whole value is that it makes every other number's tier label true.**

## The defect, driven live at #226 (not recited from W-273)

`_capture_gate._tier_probe()` measures the one-character string `"x"`. `_gauge_tokens.count()`
returns `(cached_value, "real")` on a cache hit, and `"x"` has been in `.token-cache.json`
(6,909 rows) since forever — so the probe answers "real" **regardless of whether the API is
reachable**. At this seat, with the key present but the API unreachable from the sandbox:

```
_tier_probe() says: real          <- the lie
count(novel nonce): cl100k-estimate  <- what a real measurement actually gets
```

Consequence (W-273's finding, confirmed): `measurement_tier()` stamps `real` on numbers that
are cl100k system-wide. Sub-report receipt: `notes/_subreports/2026-08-30-225-context-system-review.md`.
The #226 wrapper-pricing sub reproduced the same root as a **negative wrapper** (a `real`
slice figure larger than the whole file's tiktoken figure) — `notes/_subreports/2026-08-30-226-wrapper-diet-pricing.md`.

## The patch (two files, both minimal)

### 1. `knowledge/_capture_gate.py` — probe a NONCE, hold the verdict per process

Replace the body of `_tier_probe()`:

```python
_PROBE_VERDICT = None   # module-level, beside _TIERS_SEEN


def _tier_probe():
    """The tier a measurement of NOVEL text taken RIGHT NOW would use — WITHOUT recording it.

    ⛔ RE-DESIGNED (#226, W-273 S1): the old probe measured "x" — permanently cached — so
    count()'s cache-hit branch answered "real" regardless of API reachability. The probe now
    measures a NONCE (cache-miss by construction), so the answer is the tier a real
    measurement would actually get. Price, declared: ONE ~10-token API call per process when
    the API is reachable. The verdict is held per-process — reachability within one process
    run is one fact, and a probe per call would turn a health check into a metronome.
    The snapshot/restore of _TIERS_SEEN stays: a health probe is not a measurement.
    """
    global _PROBE_VERDICT
    if _PROBE_VERDICT is not None:
        return _PROBE_VERDICT
    snapshot = set(_TIERS_SEEN)
    try:
        nonce = "tier-probe nonce " + os.urandom(16).hex()
        _PROBE_VERDICT = _tier_of(measure_tokens(nonce)[1])
        return _PROBE_VERDICT
    finally:
        _TIERS_SEEN.clear()
        _TIERS_SEEN.update(snapshot)
```

### 2. `knowledge/_gauge_tokens.py` — the probe must not seed the cache

A successful real probe would write its nonce into `.token-cache.json` (one junk row per
process, forever, in a content-keyed cache). Add a keyword to `count()`:

```python
def count(text: str, allow_api: bool = True, _cache_write: bool = True) -> tuple[int, str]:
```

and guard the write at the cache-store site:

```python
            c[h] = n
            if _cache_write:
                try:
                    with open(CACHE, "w", encoding="utf-8") as f:
                        json.dump(c, f)
                except Exception:
                    pass          # a cache that cannot write is slow, not wrong
```

The probe's `measure_tokens` path then needs the nonce call to pass `_cache_write=False`
through `gauge.count` — smallest wiring: `_tier_probe` calls
`gauge.count(nonce, _cache_write=False)` directly and maps via `_tier_of` on the method
string, rather than going through `measure_tokens`. (Driven proof below used the
`measure_tokens` path with the write accepted-then-erased; the landing shape should use the
direct call so no erasure is ever needed.)

## Proof transcript (#226, this seat, fake `urlopen` — no real network)

```
A: old probe (API dead): real   <- the lie
A: new probe (API dead): cl100k <- the truth
B: new probe (API ok):   real   | network calls: 1
C: calls after 2 more probes: 1 (1 = held per process) | _TIERS_SEEN untouched: True
D: cache rows: 6910 -> the one fake-real row was identified and REMOVED (rows back to 6909);
   the _cache_write=False kwarg removes this class at the root
```

## Pitfalls, replayed — not hand-waved

1. **A per-process API call is a new spend.** ~10 tokens per process that asks for a tier,
   only when reachable. Builds that spawn many processes pay it many times. If that is too
   dear, the alternative is a TTL file beside the cache — priced, not built.
2. **A probe that reaches the network can now FAIL slow** (20s timeout in `count()`) where the
   old one failed instantly-and-wrong. A build step calling `measurement_tier()` on a dead
   network waits one timeout, once per process.
3. **Selftests that relied on the "x" cache hit** to see `real` without a key will flip to
   cl100k under the new probe — every consumer of `measurement_tier()` /
   `measurement_degraded()` should be re-driven at the landing commit (grep: `_tier_probe`,
   `measurement_tier`, `measurement_degraded`).
4. **Numbers already stamped `real` that were cl100k stay wrong in frozen records.** This
   patch stops the bleeding; it re-prices nothing retroactively. Which stamped figures get
   re-measured is S1's follow-on and Dave's call (the re-base sitting already carries one).

## What enacting looks like

One commit: the two-file patch + a selftest arm (old-lie shape: cached short string + dead
API ⇒ probe must NOT say real) + re-drive of the consumers in pitfall 3. Nothing else moves —
no threshold, no tier vocabulary, no cache format.
