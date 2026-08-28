# `_encoder-cache/` — the vendored `cl100k_base` encoder data

**What this is.** One file: the `cl100k_base` byte-pair-encoding table that `tiktoken` uses to
count tokens. It is `tiktoken`'s own published data, mirrored here so that **this pack measures
tokens out of the box** — no download, no `TIKTOKEN_CACHE_DIR` set by hand, no reachable host.

| | |
|---|---|
| file | `9b5ad71b2ce5302211f9c61530b329a4922fc6a4` |
| mirrors | `https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken` |
| bytes | `1681126` |
| sha256 | `223921b76ee99bde995b7ff738513eef100fb51d18c93597a113bcffe865b2a7` |
| licence | MIT — `tiktoken` (openai/tiktoken). This is that project's public encoding data. |

**Why the filename looks like that.** It is not a hash of the file. `tiktoken` keys its cache on
the **sha1 of the URL** it would otherwise download from, and looks the file up at
`$TIKTOKEN_CACHE_DIR/<sha1-of-url>`. Measured, not assumed:

    python3 -c "import hashlib; print(hashlib.sha1(b'https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken').hexdigest())"
    9b5ad71b2ce5302211f9c61530b329a4922fc6a4

So the filename **must not be changed**. Rename it and `tiktoken` will not find it, will try the
network, and — on a machine that cannot reach that host — the chain generator will refuse.

**The sha256 above is `tiktoken`'s own expected hash**, not one we invented: inside the installed
`tiktoken` package, `cl100k_base()` passes
`expected_hash="223921b76ee99bde995b7ff738513eef100fb51d18c93597a113bcffe865b2a7"`. If the bytes
here ever stop matching it, `tiktoken` itself rejects the cached copy and falls through to the
network — which is the correct, loud behaviour, not a silent wrong answer.

**Nothing reads this directory by hand.** One helper resolves it:
`memento-package/machinery/_encoder_home.py`. Every part of this pack that measures tokens goes
through that helper, and the helper is the only place the path is written down. To check the
whole path end to end:

    python3 memento-package/machinery/_encoder_home.py --check

**Two engines read this one file.** `tiktoken` reads it through its own cache lookup, and — when
`tiktoken` cannot be imported at all — the helper's own pure-Python `cl100k_base` encoder reads it
directly (`s222-D3`). Same data, same merges, same numbers; the helper's `--equality-gate` is what
makes "same numbers" a checked claim rather than a promise. One consequence worth stating: rename
or damage this file and **both** engines fail, identically and loudly. One file, one failure mode,
one refusal.

**What is still an install step.** The `tiktoken` *wheel* itself (`pip install tiktoken`) still
comes from PyPI, and it is RECOMMENDED — it is several times faster than the pure-Python engine.
Vendoring the wheel is a different question and is deliberately not done here.
