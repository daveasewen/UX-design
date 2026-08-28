# `#222` — `s222-D2` enacted: the designer pack measures tokens OUT OF THE BOX

session: `#222` · 2026-08-28 · model: Opus · one lane
brief: `notes/_briefs/2026-08-28-222-encoder-vendoring-brief.md`
ruling: `s222-D2` (Dave, 2026-08-28) — read from `knowledge/_rulings.json` at HEAD, not from the brief
region: `apollo-spider/gumdrop/**` (the Gumdrop seed) · `apollo-spider/FIRST-SESSION.md` ·
`apollo-spider/build-designer-pack.sh` · `memento-package/machinery/_capture_gate.py` and its
plugin mirror
⛔ **NOT touched:** `apollo-spider/dist/` · `knowledge/_rulings.json` (read only) ·
`knowledge/_state.json` · any gate file · no commit, no push, no bake, no `_build_all.py`

**COUNTS:** files added 3 · files edited 5 · gates re-run 8 (8 green, 1 pre-existing advisory
non-zero) · gate files edited **0** · proof directions driven both ways 2 · counterfactual driven 1
· new selftest bites 5 · UNPROVEN 2 · COULD-NOT-RUN 1 · ruling-shaped questions 2

---

## ⓪ THE PREMISE, REPLAYED FIRST

At HEAD `d4e69d0` + dirty. Baselines taken **before** the first edit, so a regression would show:

| instrument | baseline |
|---|---|
| `knowledge/_validate_package_delta.py` | `0 failure(s)` |
| `knowledge/_release/_gate_pack_docs.py --stage` (reconstructed stage) | `45 finding(s)`, ADVISORY, exit 0 |
| `knowledge/_release/_gate_release_audit.py --manifest-check` | PASS, byte-identical at `3f7a63a39e86` |
| `knowledge/_release/_gate_frozen_release.py` | PASS, 3 arms, no frozen surface moved |

**Two brief premises did not survive the replay, and both are named here rather than worked
around:**

1. ⛔ **The token-measuring entry point is NOT in `apollo-spider/`.** The brief scopes the work to
   the stage. Grepped twice — `tiktoken` case-insensitively across the whole stage, then
   `get_encoding|cl100k|encoding_for_model` — and the stage contains **no code that measures
   tokens at all**: only prose in `FIRST-SESSION.md`, `build-designer-pack.sh` and two comments.
   The thing that refused on Dave's machine is `memento-package/machinery/_capture_gate.py`'s
   `measure_tokens`, called by the verbatim `_gen_chain.py` — i.e. the **frozen** package surface
   guarded by `_validate_package_delta.py` and by Dave's `#64` boundary. The pack's
   `memento-package/` is assembled from **two** sources, per `_gen_pack_manifest.py`'s
   `SEED_PREFIXES` (`apollo-spider/gumdrop/` → `memento-package/`) plus the repo's own frozen
   `memento-package/machinery/`. Enacting the ruling in the stage alone is impossible; the lane
   had to reach the shim, legally.
2. ⛔ **There is no "import-smoke gate".** The brief names one to re-run. Probed twice —
   `import-smoke|import_smoke` across the repo excluding `.git`/`dist`, then
   `importable|runnable|py_compile|compileall` across `knowledge/_release/*.py` and
   `knowledge/_gate*.py`. **No match anywhere**, including in the two #221/#220 subreports the
   brief cites as its origin. The nearest real instrument is the **import arm inside
   `_gen_pack_manifest.py`'s gate probe** (`--probe`), which grades each packed gate
   `RUNNABLE` / needs-dep / repo-bound. `--selftest` (195 bites) was run in its place and is
   green. [[unmatched-grep-is-not-an-absence]] — the probe is named so the absence is checkable.

**#221 lane C and #220 L4 replayed before building** (`notes/_subreports/2026-08-27-221-laneC.md`
§1 F5 · `-220-audit-L4.md` F5). Lane C already moved `pip install tiktoken` into
§ Before you start as **required**, with the network-host warning, and already replaced the L4
"Optional" prose. **Nothing from that fix was re-issued.** This lane edits the same section but in
the opposite direction: lane C made the requirement honest, this lane removes the *reason* it bit.
The `tape (cl100k ESTIMATE)` display word (lane C F7, re-graded, left standing as a published unit
label) is likewise **untouched** — the generated `_CHAIN.md` still carries it and stdout still says
`tiktoken cl100k_base`, exactly as lane C documented.

---

## ① THE MECHANISM AS BUILT

**The data.** `apollo-spider/gumdrop/_encoder-cache/9b5ad71b2ce5302211f9c61530b329a4922fc6a4` —
1,681,126 bytes, sha256 `223921b76ee99bde995b7ff738513eef100fb51d18c93597a113bcffe865b2a7`,
byte-identical to the material the brief supplied. Two facts were **measured, not assumed**:

- the filename is `sha1(https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken)`
  — re-derived in Python, and re-derived again inside `--check` so a future rename cannot pass;
- that sha256 is **tiktoken's own `expected_hash`** for this blob (read out of the installed
  `tiktoken_ext.openai_public.cl100k_base` source). So the integrity anchor is the library's, not
  one this lane invented — and scrambled bytes are rejected by tiktoken itself.

`_encoder-cache/README.md` beside it carries what it is, what it mirrors, bytes, sha256, the MIT
licence note, why the filename must not change, and the one command that checks it.

**The one helper.** `apollo-spider/gumdrop/machinery/_encoder_home.py` → packs to
`memento-package/machinery/_encoder_home.py`. It resolves `_encoder-cache/` by walking **up from
its own file** (the house idiom: machinery resolves its homes from where the FILE sits), verifies
presence and size, then `os.environ.setdefault("TIKTOKEN_CACHE_DIR", …)`. `setdefault` is the whole
contract — a designer's own value wins, and the helper *says* it stood aside when that happens.
`--check` drives the whole path end to end rather than reporting on it (re-derive the cache key →
deep sha256 → set the variable → import tiktoken → actually encode a string → assert 4 tokens);
`--selftest` plants five conditions: cache key, resolution, designer's-env-wins, refusal-names-the-
path, wrong-size-refused.

**The route in.** `memento-package/machinery/_capture_gate.py` — both packed copies — gains a
module-level bootstrap that calls the helper **once, at import**, before anything below asks for an
encoder. `_gen_chain.py` needs no edit at all: it imports the shim, so it inherits the bootstrap.
Three properties of that block are deliberate and declared in place:

- it is **not a ported name**, so `_validate_package_delta.py` arm 2 (AST source-segment hashing of
  the declared ported functions/constants) still compares byte-identical text. **No ported function
  or constant was edited, and no gate file was touched.**
- the import is **optional by design**: this file has two homes, the pack (where the helper and the
  cache ride beside it) and this repo (where neither does — Apollo measures through its own gauge).
  A hard import would ship an unimportable machinery file, which is the v1.0.0 defect. Absence is
  recorded in `_ENCODER_HOME_NOTE` and readable via the new `encoder_home_note()`, not swallowed.
- it **searches** for the helper — beside itself and under `machinery/` of each ancestor — so the
  plugin mirror at `memento-package/claude-plugin/memento/machinery/` (three levels deeper) reaches
  the **single** copy instead of getting a second one. Driven: the mirror's shim returns
  `(4, 'tiktoken cl100k_base')` with egress dead.

**The refusal is untouched, and now names the path.** No tier, label or refusal string changed.
When the vendored file is gone the helper writes a loud `ENCODER-HOME: ⛔ …` block to stderr naming
every candidate path it tried and stating that the downstream refusal is *explained* by it, not
*caused* by it — then gets out of the way so `_gen_chain.py`'s existing MEASUREMENT REFUSAL fires
verbatim and writes nothing.

---

## ② PROOF — DRIVEN, NOT REASONED

Fresh stage at `/var/tmp/spider-final/Apollo-Spider-vnext/`, built from the finished files by
replaying `SEED_PREFIXES` by hand (`apollo-spider/gumdrop/.` → `memento-package/`, plus the frozen
`memento-package/machinery/` and `claude-plugin/`). Every run below used:

```
env -u TIKTOKEN_CACHE_DIR -u DATA_GYM_CACHE_DIR \
    https_proxy=http://127.0.0.1:9 HTTPS_PROXY=http://127.0.0.1:9 http_proxy=http://127.0.0.1:9 \
    TMPDIR=/var/tmp/spider-final/emptytmp
```

`TMPDIR` points tiktoken's *default* cache (`gettempdir()/data-gym-cache`) at an empty directory;
`/tmp/data-gym-cache`, `/var/tmp/data-gym-cache` and `~/.cache/tiktoken` were all confirmed absent.
The proxy port is dead, so any network read raises.

**A — OUT OF THE BOX, all green:**

| # | command (from the pack root) | result |
|---|---|---|
| A1 | `python3 memento-package/machinery/_encoder_home.py --check` | `tiktoken OK — 4 tokens, measured with the encoder data inside this pack (no download, no environment variable to set).` rc=0 |
| A2 | `python3 memento-package/machinery/_gen_chain.py` | `✅ _CHAIN.md: 888 tiktoken cl100k_base · … fixed point in 2 pass(es)` rc=0 |
| A3 | `python3 memento-package/machinery/_gen_chain.py --check` | `✅ _CHAIN.md is FRESH — byte-matches the live chain` rc=0 |
| A4 | `python3 memento-package/_state.py` | `items 0 · live 0 · conditioned 0 · UNCONDITIONED 0` rc=0 |

A2/A3 required `GOOD-MORNING.md` and `_LIVE-STATE.md`, written into the stage from
FIRST-SESSION §4b's own skeletons — i.e. the designer's state at step 4c, which is where Dave's
failure happened.

**B — THE MUTATION (vendored file moved aside, identical environment):**

```
mv memento-package/_encoder-cache/9b5ad71b2ce5302211f9c61530b329a4922fc6a4 /var/tmp/spider-final/moved-aside
```

| # | command | result |
|---|---|---|
| B1 | `…/_encoder_home.py --check` | names every candidate path, then `ENCODER-HOME: ⛔ REFUSED — this pack cannot measure tokens out of the box.` **rc=1** |
| B2 | `…/_gen_chain.py` | 3 `ENCODER-HOME:` lines naming the file, then `✗ _CHAIN.md NOT generated — the token measurer is running on the ESTIMATE fallback … This is a MEASUREMENT REFUSAL` **rc=1**, and **`_CHAIN.md` was not written** |

**C — THE COUNTERFACTUAL (why this is the thing that fixed it).** The same stage rebuilt with
`FIRST-SESSION.md` and both `_capture_gate.py` copies restored from `git show HEAD:` and the
vendored files deleted — i.e. the pack **as it ships today** — under the identical broken-egress
environment reproduces Dave's failure exactly: `✗ _CHAIN.md NOT generated — … MEASUREMENT REFUSAL`,
rc=1, no file. Same environment, two shapes, opposite outcomes. That is the measurement.

---

## ③ GATE VERDICTS (after; every one also has a before, in ⓪)

| gate | verdict |
|---|---|
| `knowledge/_validate_package_delta.py` | **0 failure(s)** — verbatim set identical both copies · shim provenance clean both chains · copies identical · no unknown files |
| `knowledge/_validate_package_delta.py --selftest` | all bites pass (its four mutation arms still fire) |
| `knowledge/_release/_gen_pack_manifest.py --selftest` | 195 bites, **0 fail** |
| `knowledge/_release/_gate_release_audit.py --manifest-check` | **PASS** — byte-identical to a fresh generation at `3f7a63a39e86` |
| `knowledge/_release/_gate_release_audit.py --pack` | **PASS** — `Apollo-Spider-v1.0.1.zip` still matches the manifest (v1.0.0 correctly SKIPPED as frozen history) |
| `knowledge/_release/_gate_release_audit.py --drift` | ADVISORY, exit 1 — **pre-existing**: manifest at `3f7a63a`, HEAD 15 commits later. Unchanged by this lane; re-cut is Dave's |
| `knowledge/_release/_gate_frozen_release.py` | **PASS** — 3 arms, no frozen surface moved (`dist/` untouched) |
| `knowledge/_release/_gate_ci_template.py` | **PASS** |
| `knowledge/_release/_gate_pack_docs.py --stage` | **45 findings, ADVISORY, exit 0 — identical to the baseline of 45.** Measured against a stage built from `git show HEAD:` docs: this lane adds **zero** net findings. The two its first draft did raise (a path inside the tiktoken wheel, and a helper path written pack-relative) were both fixed before this run |
| `apollo-spider/gumdrop/machinery/_encoder_home.py --selftest` | 0 failures, 5 arms — run in the repo **and** in the packed position |

**`_validate_package_delta.py` was NOT edited, and its legal route turned out NOT to be
ruling-shaped.** See ⑤ Q1 for the route that *would* have been, and why it was not taken.

---

## ④ FILES TOUCHED (for the conductor's reconcile)

**Added (3):**
- `apollo-spider/gumdrop/_encoder-cache/9b5ad71b2ce5302211f9c61530b329a4922fc6a4` — 1,681,126 B,
  sha256 `223921b76ee99bde995b7ff738513eef100fb51d18c93597a113bcffe865b2a7`
- `apollo-spider/gumdrop/_encoder-cache/README.md`
- `apollo-spider/gumdrop/machinery/_encoder_home.py`

**Edited (5):**
- `memento-package/machinery/_capture_gate.py` — bootstrap block + `encoder_home_note()` + one
  docstring paragraph declaring the non-port. No ported name touched.
- `memento-package/claude-plugin/memento/machinery/_capture_gate.py` — byte-identical copy of the
  above (arm 3 verified).
- `apollo-spider/FIRST-SESSION.md` — § Before you start rewritten (the vendored data, the new
  check, "no download and no environment variable"); Step 4c gains the blocked-network note.
- `apollo-spider/build-designer-pack.sh` — the generated pack README's "What you need installed"
  and "What is in here" now state the vendoring and the wheel-still-from-PyPI edge.
- `apollo-spider/gumdrop/_GUMDROP-MANIFEST.md` — new section documenting the vendored encoder as
  the one thing in the cut that is not an Apollo copy (#185 forgotten-document class).

**Deliberately NOT edited:** `knowledge/_capture_gate.py` (Apollo's own measurer — out of the
ruling's scope, and touching it would have put arm 2 in play for no benefit) · `_gen_chain.py` in
any copy · every gate file · `knowledge/_state.json` (no row minted — `W-244` is Dave's and the
filed-report row is the conductor's per `s218-D7`) · `apollo-spider/dist/`.

---

## ⑤ RULING-SHAPED QUESTIONS → DAVE / CONDUCTOR

**Q1 — Should the helper instead be a delta-audited COPY inside the frozen package?** The route
this lane took keeps `_encoder_home.py` in the **Gumdrop seed**, which is outside
`_validate_package_delta.py`'s glob entirely, so no gate changed and no frozen surface grew. The
alternative — `knowledge/_encoder_home.py` copied verbatim into both `memento-package/machinery/`
copies, added to `VERBATIM_SET` and `KNOWN_FILES` — is arguably *purer* against Dave's `#64`
boundary ("copies only, and every copy is delta-audited"), because the helper would then be
audited. **It is also the ruling-shaped one:** it grows the frozen package's file set, and the
gate documents a remedy route only for arm 2's re-port, not for admitting a new file. Per the
brief's fence I did **not** take it and did **not** weaken the gate. If Dave wants the helper
delta-audited, that is a decision plus a two-commit dance (land `knowledge/_encoder_home.py`,
then copy + extend the allowlist).

**Q2 — Should the shim→helper dependency be DECLARED in the generator's closure?** The shim finds
the helper by searching, which is why the plugin mirror needs no second copy — proven live. But
`_gen_pack_manifest.py` carries a `DOOR_COMPANIONS` table for exactly this shape ("a packed door
travels with its builder") because *"nothing static can read"* a runtime dependency, and my import
is `importlib.util`, so the static `import_closure` cannot see it either. Declaring
`("_capture_gate.py", "_encoder_home.py", …)` would make the generator **refuse** if a future cut
ever dropped the helper. Adding a row to that table is release machinery and is priced, not done.

---

## ⑥ WHAT `W-244`'s REMEDY HALF STILL NEEDS

`W-244` closes when *"Dave rules whether v-next ships the 1.7MB cl100k_base encoding file inside
the pack (release surface is his), and the FIRST-SESSION.md offline remedy is written either way."*

- **half 2 — the remedy — is written.** § Before you start, Step 4c, the pack README and the
  Gumdrop manifest all now state the vendored path, the check command, and the honest wheel edge.
- **half 1 is RULED (`s222-D2` says yes) but NOT BAKED.** What remains is release mechanics, all of
  it Dave's word under `s219-D4(2)`: commit the tree → `_gen_pack_manifest.py --probe --commit
  <sha>` then `--manifest --commit <sha>` → `build-designer-pack.sh --dry-run --out-dir /var/tmp/…
  --commit <sha>` → Dave's eye on `reviews/RELEASE-SPIDER-*.html` → ratify → `--release`.
- **Size:** the pack grows by 1,681,126 B — manifest totals `39,767,327` → ~`41,448,453` B before
  compression; the encoding data is text-ish and compresses, so the zip grows by rather less. The
  bake will state the real figure and folds it back into Dave's page automatically.
- `W-244` was **not touched** (Dave's row).

---

## ⑦ REPLAY-THESE (verifier — exact commands)

```sh
# --- premise
sha256sum apollo-spider/gumdrop/_encoder-cache/9b5ad71b2ce5302211f9c61530b329a4922fc6a4
#  -> 223921b76ee99bde995b7ff738513eef100fb51d18c93597a113bcffe865b2a7
python3 -c "import hashlib;print(hashlib.sha1(b'https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken').hexdigest())"
#  -> 9b5ad71b2ce5302211f9c61530b329a4922fc6a4   (the filename IS the cache key)

# --- no regressions (all green before this lane, all green after)
python3 knowledge/_validate_package_delta.py                      # 0 failure(s)
python3 knowledge/_validate_package_delta.py --selftest           # all bites pass
python3 knowledge/_release/_gen_pack_manifest.py --selftest       # 195 bites, 0 fail
python3 knowledge/_release/_gate_release_audit.py --manifest-check # PASS
python3 knowledge/_release/_gate_release_audit.py --pack           # PASS
python3 knowledge/_release/_gate_frozen_release.py                 # PASS, no frozen surface moved
python3 knowledge/_release/_gate_ci_template.py                    # PASS

# --- the new instrument, both in the repo and in the packed position
python3 apollo-spider/gumdrop/machinery/_encoder_home.py --selftest   # 0 failures, 5 arms
python3 apollo-spider/gumdrop/machinery/_encoder_home.py --check      # tiktoken OK — 4 tokens

# --- build the packed layout (SEED_PREFIXES replayed by hand)
S=/var/tmp/replay/Apollo-Spider-vnext; rm -rf /var/tmp/replay; mkdir -p "$S" /var/tmp/replay/emptytmp
cp apollo-spider/FIRST-SESSION.md "$S/"; cp -r apollo-spider/.github "$S/"
mkdir -p "$S/memento-package"
cp -r apollo-spider/gumdrop/. "$S/memento-package/"
cp -r memento-package/machinery memento-package/claude-plugin "$S/memento-package/"
cp memento-package/README.md memento-package/WHAT-MEMENTO-IS.md "$S/memento-package/"
find "$S" -name __pycache__ -type d -exec rm -rf {} + ; rm -f "$S/memento-package/_CHAIN.md"
# then write GOOD-MORNING.md and _LIVE-STATE.md into "$S/memento-package/" from
# FIRST-SESSION.md §4b's two skeletons, verbatim.

# --- DIRECTION A: out of the box, egress dead, no env var
cd "$S"
B="env -u TIKTOKEN_CACHE_DIR -u DATA_GYM_CACHE_DIR https_proxy=http://127.0.0.1:9 HTTPS_PROXY=http://127.0.0.1:9 http_proxy=http://127.0.0.1:9 TMPDIR=/var/tmp/replay/emptytmp"
$B python3 memento-package/machinery/_encoder_home.py --check    # rc 0, "tiktoken OK — 4 tokens…"
$B python3 memento-package/machinery/_gen_chain.py               # rc 0, "✅ _CHAIN.md: 888 tiktoken cl100k_base"
$B python3 memento-package/machinery/_gen_chain.py --check       # rc 0, FRESH

# --- DIRECTION B: the mutation
mv memento-package/_encoder-cache/9b5ad71b2ce5302211f9c61530b329a4922fc6a4 /var/tmp/replay/aside
rm -f memento-package/_CHAIN.md; find . -name __pycache__ -type d -exec rm -rf {} +
$B python3 memento-package/machinery/_encoder_home.py --check    # rc 1, names every path tried
$B python3 memento-package/machinery/_gen_chain.py               # rc 1, MEASUREMENT REFUSAL, no file
ls memento-package/_CHAIN.md                                     # must NOT exist
mv /var/tmp/replay/aside memento-package/_encoder-cache/9b5ad71b2ce5302211f9c61530b329a4922fc6a4

# --- the plugin mirror reaches the ONE helper from three levels deeper
$B python3 -c "import importlib.util as u; s=u.spec_from_file_location('cg','memento-package/claude-plugin/memento/machinery/_capture_gate.py'); m=u.module_from_spec(s); s.loader.exec_module(m); print(m.measure_tokens('the quick brown fox'))"
#  -> (4, 'tiktoken cl100k_base')

# --- pack-docs advisory: this lane must add ZERO findings
python3 knowledge/_release/_gate_pack_docs.py --stage "$S" | tail -2   # 45 finding(s), exit 0
```

---

## ⑧ UNPROVEN / COULD-NOT-RUN — declared and priced

1. **COULD-NOT-RUN — the manifest has never been regenerated with these files present.**
   `_gen_pack_manifest.py --probe/--manifest/--stage` all read a **named commit** via `git archive`,
   and the fence forbids committing. So the arms that would grade the new files —
   `import_closure`, `companion_closure`, the seed-map **collision** refusal, and the gate probe —
   have not been driven over them. Two of these were checked by hand instead and are stated as
   such: neither `_encoder_home.py` nor `_encoder-cache/` collides with a name in the frozen
   `memento-package/`, so the seed map cannot refuse on collision; and the group matchers are
   prefix-based (`p.startswith("apollo-spider/gumdrop/")`), so both new paths are inside the
   `gumdrop` group by construction. **The conductor must re-run `--probe --commit <new sha>` and
   `--manifest --commit <new sha>` after the commit and read the closure block.** Until then,
   "the pack will carry these files" is a construction argument, not a measurement.
2. **UNPROVEN — a real designer machine.** Everything here was driven in this Linux sandbox with
   egress broken by proxy. That is a faithful model of Dave's blocked host, but it is not a
   Windows/macOS corporate laptop behind a TLS-inspecting proxy, and it is not VS Code + Copilot.
   The `s222-D2` fix should be confirmed on the same machine that produced the original refusal.
3. **UNPROVEN — corruption that preserves the byte count.** Import-time verification is existence +
   size (deliberately: a full sha256 of 1.6 MB on every process start buys nothing, because
   tiktoken re-checks the content hash itself). Same-size scrambled bytes are therefore caught by
   *tiktoken*, which falls through to the network and then to the existing refusal — correct, but
   the `ENCODER-HOME:` line will not be the one that names it. `--check` and `verify(deep=True)`
   do the full hash on demand. Declared in the module docstring.
