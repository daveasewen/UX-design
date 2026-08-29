# W-263 forensics — the Copilot pack Dave tested, 2026-08-29

*Sub-report for session #224. Evidence-only: this file rules nothing.*

---

## VERDICT

**Dave tested v1.0.2**, and the version question is settled by sha, not by inference: all **34**
files that differ between v1.0.1 and v1.0.2 match the **v1.0.2** sha in his pack (v1.0.1: **0**),
and all **6** files that v1.0.2 added — including the `s222-D2` vendored encoder cache and
`s222-D3`'s `_encoder_home.py` — are present with matching shas.

**But it is not a new failure class either.** The s222-D2/s222-D3 machinery was present, and it
**worked**: I reproduced Dave's corp-blocked condition and the pure-Python fallback engaged, named
itself, and returned an exact cl100k count. His own generated `_CHAIN.md` is stamped at the
**cl100k tier**, which is only reachable through an encoder — proof it ran on his machine.

What actually failed is a **vocabulary collision**. "The token count" Dave was looking for is the
**session fuel gauge** (how full is this chat), and the pack has never shipped one — it is a
DECLARED GAP, written into `_RUNBOOK-context-gauge.md`. The pack's token counting measures **file
sizes**, and that worked fine. GPT-Sol did not fix the encoder; it **closed the declared gap** by
discovering the runbook's premise is now false.

> ⚠ **The premise the pack ships is stale.** `_RUNBOOK-context-gauge.md:42` asserts *"Copilot in
> VS Code does not expose a token count to itself. There is no reading to take."* GPT-Sol found
> that it does. That sentence is the port-back.

---

## EVIDENCE

### Reference artefacts (re-measured, not trusted)

| artefact | expected | measured | verdict |
|---|---|---|---|
| `apollo-spider/dist/Apollo-Spider-v1.0.2.zip` | 19,850,657 B · sha256 `3a7fe297140862b7…` | 19,850,657 B · `3a7fe297140862b706f83c072e52be1a8c0af5145c6f8b5a516d198ce9f287b6` | ✅ MATCH |
| `apollo-spider/dist/Apollo-Spider-v1.0.1.zip` | (from `git log` 9f58516: `c8934ebd6330…`) | `c8934ebdb63306526223f8478561ccd3e18f502b4db01746c0f468ba6e6923d1` | ✅ MATCH |

### ⛔ The manifest premise in my brief was WRONG — name the field, probe the row

The brief said the shipped `_MANIFEST.json` "carries per-file shas". **It does not.** Its schema is
`apollo-designer-pack-manifest/1` and its top-level fields are exactly:

`carries · commit · commit_date · excluded · gate_probe · groups · import_closure ·
open_questions · pack · ruling · schema · slug · totals · version`

`groups[]` rows carry `{group, key, paths[], files, bytes}` — **paths and byte totals only, no
digest field of any kind**. Probe run: `grep -o '"[a-z_]*sha[a-z0-9_]*"' _MANIFEST.json` → **zero
matches** (the only `sha`-ish strings in the file are the prose words "shape"/"share").

So I did not use the manifest as the sha baseline. **I built my own**: extracted the shipped
v1.0.2 zip and hashed every real file (1,652 rows), which is stronger evidence anyway. The
manifest's `totals` (`files: 1647`, `bytes: 41,678,300`, `pack_files: 1649`) is a *count*, and a
count is not a measurement — I did not lean on it.

### The two staged copies are one piece of evidence, not two

`_incoming-copilot-pack.zip` extracted to `/var/tmp/incoming-pack/`, and the untracked repo-root
`Apollo-Spider-v1.0.2/` (git status: `?? Apollo-Spider-v1.0.2/`) were hashed independently:

**1,676 / 1,676 files identical, 0 differing, 0 only-in-either.** The repo-root directory is
byte-for-byte Dave's own unzip of the same zip. Nothing is lost by treating the zip as primary.

### Entry accounting (macOS junk counted, then excluded)

| | count |
|---|---|
| total extracted entries | 3,540 |
| `__MACOSX/` entries | 1,792 |
| AppleDouble `._*` files | 1,722 |
| `.DS_Store` | 1 |
| **real files compared** | **1,676** |

All `__MACOSX/`, `._*` and `.DS_Store` entries are macOS Archive Utility artefacts, not GPT's work,
and are excluded from every bucket below.

### The sha buckets — incoming vs shipped v1.0.2

| bucket | count |
|---|---|
| **UNCHANGED** (sha matches v1.0.2) | **1,644** |
| **MODIFIED** (path in shipped, sha differs) | **8** |
| **ADDED** (path not in shipped) | **24** |
| **MISSING** (in shipped, absent from incoming) | **0** |

Shipped baseline 1,652 files; incoming 1,676. Nothing was deleted from the pack.

### The version discriminator test

| test | result |
|---|---|
| incoming files matching a **v1.0.1** sha | 1,604 |
| incoming files matching a **v1.0.2** sha | **1,644** |
| files changed between v1.0.1 → v1.0.2 | 34 |
| …of those, incoming matches **v1.0.2** | **34** |
| …of those, incoming matches **v1.0.1** | **0** |
| …neither / absent | 0 / 0 |
| files **added** in v1.0.2 | 6 |
| …present in incoming with matching sha | **6 / 6** |

The 6 v1.0.2-only files, all present and sha-matched:

```
knowledge/_gate_artefact_fresh.py
knowledge/_gate_inline_style_parse.py
knowledge/_validate_wiring.py
memento-package/_encoder-cache/9b5ad71b2ce5302211f9c61530b329a4922fc6a4   ← s222-D2 vendored data
memento-package/_encoder-cache/README.md
memento-package/machinery/_encoder_home.py                                ← s222-D3 purepy engine
```

**Unambiguous. Not a judgement call, not an inference from a version string** — 34/34 on the
discriminating set with a clean zero on the alternative.

### ⚠ NOT ONE `.py` FILE WAS MODIFIED OR ADDED

Every one of the 8 MODIFIED and 24 ADDED paths is `.css`, `.js`, `.json`, `.html` or `.md`. The
entire `memento-package/machinery/` tree — `_encoder_home.py`, `_capture_gate.py`, `_gen_chain.py`
— sits in the 1,644 UNCHANGED bucket, sha-identical to what we shipped.

**There is no GPT-written Python in this pack.** Whatever "Sol wrote its own code" means, it did
not land as code in the artefact Dave staged. (See GPT'S CODE below — it landed as *configuration*.)

---

## GPT'S CODE

### What the 8 MODIFIED files actually are — genuine design work, not the fix

All 8 are ordinary Copilot session output on the design system. None touch token counting:

| file | change |
|---|---|
| `knowledge/canon/canon.css` | search-field `.boxed` gains `border-radius:var(--border-radius-control)` (×2 sites); `.cn-chart-line .dv-title` gains `color:var(--ink); opacity:1` |
| `knowledge/canon/dv-behaviour.js` | `tipAt()` takes a `source` arg and re-parents the tooltip into the active `cn-chart-*` host |
| `knowledge/components/search-field.meta.json` | adds `"radius": "border-radius/control"` |
| `knowledge/snippets/Chart-line.reference.html` | mirrors the `dv-title` full-ink change |
| `knowledge/snippets/Filter-toolbar-bar.reference.html` | mirrors the boxed-search radius |
| `knowledge/snippets/Search-field.reference.html` | mirrors radius + adds `--border-radius-control` to both theme blocks and the `vars` map |
| `memento-package/_CHAIN.md` | starter stub → **generated** chain (chat #16) |
| `memento-package/_state.json` | `items: []` → **2 closed worklist rows** |

This is competent work — the token-role wiring and the snippet/meta/canon mirroring are done
correctly and consistently across all three surfaces.

### The 24 ADDED files

- **19 gate/audit outputs** under `knowledge/` (`_A11Y-GATE.md` 152 KB, `_DATAVIZ-GATE.md`,
  `_SNIPPET-AUDIT.md`, `_RADIUS-GATE.md`, …) — these are *generated artefacts*, evidence the gates
  were actually run on his machine.
- **`dashboards/international-banking-dashboard.canon.html`** (38,807 B) — his actual deliverable.
- **`memento-package/GOOD-MORNING.md`**, **`_LIVE-STATE.md`**, **`machinery/_memento-index.json`** —
  the capture ritual ran.
- **`.vscode/settings.json`** (217 B) — ★ **this is the fix.**

### ★ The fix, in full — it is three lines of JSON

`.vscode/settings.json`:

```json
{
  "github.copilot.chat.agentDebugLog.fileLogging.enabled": true,
  "github.copilot.chat.summarizeAgentConversationHistory.enabled": true,
  "github.copilot.chat.summarizeAgentConversationHistoryThreshold": 220000
}
```

**Classification: not a token counter. A telemetry tap.** It does not replace, duplicate or compete
with `s222-D2`/`s222-D3` — those measure *text* in cl100k; this reads the **server's own reported
usage for the live session** out of Copilot's agent debug log (`main.jsonl`). It is the Copilot
equivalent of Apollo's ruled `message.usage` path: **REAL tokens, absolute, not an estimate.**

The provenance is in his own worklist. `memento-package/_state.json`, row **`W-17`**, home
`.vscode/settings.json`, `closed_by` *"chat #16 — post-reload debug log and exact input-token
verification, 2026-08-29"*:

> "Copilot agent debug-file logging now persists server-reported usage in main.jsonl; GPT-5.6 Sol
> reported 144,266 input tokens on the verification turn. Automatic conversation compaction remains
> configured at 220,000 tokens."

And `_LIVE-STATE.md` carries the readings:

> - GPT-5.6 Sol reported **144,266 input tokens** on the verification turn, of which **143,657 were cached**.
> - The configured automatic-compaction threshold remains **220,000** tokens: **75,734** of headroom remained.
> - The model's maximum prompt is **271,997** tokens: **127,731** of hard prompt headroom remained.

Three numbers, an absolute budget, and a declared threshold — this is a **fuel gauge**, in exactly
the shape Apollo rules one.

⚠ **UNPROVEN here:** I cannot verify from this sandbox that those three VS Code setting keys exist
or behave as described — no network, no Copilot. The readings above are GPT-Sol's report as
transcribed into Dave's state files, not something I measured.

---

## WHY OUR FALLBACK DID/DIDN'T ENGAGE

**It engaged. It worked. It was never the problem.**

I simulated Dave's corp-blocked machine by shadowing the module with a `tiktoken.py` that raises
`ImportError`, then drove the pack's own check against **his** copy:

```
########## tiktoken BLOCKED (Dave's corp condition)
ENCODER-HOME: ⚠ `tiktoken` is not importable here (ImportError: blocked by corporate
  security (simulated)). Measuring with the pack's own engine: purepy cl100k_base
  (exact, equality-gated). …
ENCODER OK — engine: purepy cl100k_base (exact, equality-gated) — 4 tokens, measured
  with the encoder data inside this pack (no download, no environment variable to set).
```

And the gate's cascade, same condition:

```
tokens= 10  method= purepy cl100k_base (exact, equality-gated)
tier  = cl100k
degraded= False
```

The `s222-D3` branch in `_capture_gate.measure_tokens()` is correctly wired — on the
`import tiktoken` failure path it reaches `encoder_home_module().count(text)` *before* any byte
divisor, and only falls to `bytes/N ESTIMATE (tiktoken absent)` if the encoder home is unresolvable.
It was resolvable. I also checked the second copy at
`memento-package/claude-plugin/memento/machinery/_capture_gate.py`, which has no `_encoder_home.py`
beside it — **it still resolves**, walking up to the `machinery/` copy, and also returns
`tier= cl100k`. No latent defect there.

**Independent corroboration from his own artefact:** the `_CHAIN.md` he generated is stamped
`1,129 tape (cl100k ESTIMATE)`. Per `_gen_chain.py`'s `_UNIT_WORDS`, `"cl100k": "tape (cl100k
ESTIMATE)"` — the word ESTIMATE there labels *cl100k as an estimate of real Claude tokens*, and it
is the **cl100k tier**, not the `"estimate": "bytes ESTIMATE"` tier. That stamp is unreachable
without a working encoder. With pip blocked, only the purepy engine could have produced it.
**s222-D2 and s222-D3 both did their job on a real locked-down corporate machine.**

### So what did Dave see fail?

The gauge that was never shipped. Probe: `find` for `_checkin*`, `*gauge*`, `*_tokens.py` across
the pack returns only `_RUNBOOK-context-gauge.md`, `knowledge/gen_snippet_tokens.py` and
`knowledge/canon/gen_canon_tokens.py` — **no `_checkin.py`, no `_gauge_tokens.py`.** That is
deliberate and documented; `_capture_gate.py`'s `_real_gauge()` says so:

> "a `knowledge/` module that is NOT in this package and is not going to be (it is Apollo-side
> budget machinery)"

and the runbook says it to the designer's face at line 42:

> "**Copilot in VS Code does not expose a token count to itself.** There is no reading to take. …
> Shipping it would ship an instrument that returns a confident wrong number, which is worse than
> none. So this is a **declared gap**, and the substitute is an **estimate tier**."

Dave asked the pack how full the session was, got "cannot measure, here is a posture", and read
that as *the token count didn't work*. It is the `#202` class again — **the same words naming two
different instruments**, with every assert green.

---

## PORT-BACK PRICE

*Recommendation only. The disposition is Dave's.*

The port-back is **cheap and worth it**, but it is not the port-back the brief anticipated. Nothing
about the encoder needs porting — that machinery is already better than what GPT has. What needs
porting is the **discovery that our declared gap is closeable**.

### Tier 1 — the premise correction (RECOMMENDED, small)

The pack currently ships a false statement to every designer who opens it.

| file | site | work |
|---|---|---|
| `memento-package/runbooks/_RUNBOOK-context-gauge.md` | **lines 40–63** (`## ⚠ What cannot be measured here`), incl. the tier table at line 51 where **measured** reads *"not available in this environment"* | rewrite ~24 lines: the measured tier now HAS an instrument |
| `.github/copilot-instructions.md` | **line 134** — *"is honest about what cannot be measured here"* | one line |
| `FIRST-SESSION.md` | § Before you start (near the `pip install tiktoken` step, ~line 35) | add the settings step |
| `.vscode/settings.json` | — | **new file, 3 keys** — ship it, so the tap is on by default |

**~30 lines across 3 edits + 1 new 217 B file.** This is the whole of GPT's actual contribution and
it is high-value: it converts the runbook's weakest section (a declared gap and three prose
postures) into a real reading, and it makes the gauge a **throttle** rather than a vibe — which is
the thing that runbook opens by insisting on.

Note the runbook's downstream sections assume no number exists: **lines 65–121** (`## The three
postures`, `## The trigger, in two tiers`) are built on judging posture from observables. They are
not *wrong* with a number available, but they become the fallback path rather than the main one.
Re-framing them is a further ~57 lines — **optional, and I would defer it** to a second pass once
the reading is proven on Dave's machine.

### Tier 2 — a `main.jsonl` reader (OPTIONAL, defer)

⚠ **Do not expect this to drop into the existing REAL-tier hook.** `_real_gauge()` wants a module
exposing `count(text) -> (n, "real")` — a *per-text* counter. `main.jsonl` gives *session
cumulative usage*. They are different instruments answering different questions, and wiring the
session figure into `measure_tokens()` would be a category error of exactly the kind
`_capture_gate.py` spends 80 lines of docstring guarding against.

The honest shape is a **new, separate** `memento-package/machinery/_session_fill.py`: locate the
active `main.jsonl`, read the last request record, report `input_tokens · cached · threshold ·
ceiling` with the source named. Rough price **~120–200 lines plus a locator that survives VS Code's
log-path layout**, and it is the risky part — the path is undocumented, version-fragile, and I could
not verify any of it from here.

**Recommendation: ship Tier 1 now, park Tier 2 behind one question to Dave** — does he want the
agent reading his debug log automatically, or is him quoting the three numbers from the Copilot UI
enough? Tier 1 already gets him a real reading; Tier 2 only saves him the copy-paste, and buys a
fragile dependency to do it.

### What is NOT worth porting

- Anything touching `_encoder_home.py`, the vendored cache, or the purepy engine. **Proven working
  under the exact failure condition.** GPT's fix does not overlap them at all.
- The 8 modified design files — those are Dave's session output, and whether they land in canon is
  a separate design question, not a forensics one. (They look correct, and `_state.json` W-01
  records a Chrome verification pass behind them.)

---

## REPLAY-THESE

```bash
# 1 — reference zip sha (expect 3a7fe297140862b706f83c072e52be1a8c0af5145c6f8b5a516d198ce9f287b6)
sha256sum apollo-spider/dist/Apollo-Spider-v1.0.2.zip

# 2 — the manifest carries NO per-file shas (expect: only "shape"/"share" prose hits)
unzip -p apollo-spider/dist/Apollo-Spider-v1.0.2.zip Apollo-Spider-v1.0.2/_MANIFEST.json \
  | grep -o '"[a-z_]*sha[a-z0-9_]*"' | sort | uniq -c

# 3 — s222-D2/D3 present in Dave's pack with v1.0.2 shas (expect 2 rows, matching the shipped zip)
unzip -l _incoming-copilot-pack.zip | grep -E '_encoder_home.py|9b5ad71b2ce5302211f9c61530b329a4922fc6a4'

# 4 — ★ THE HEADLINE: purepy engages under a blocked tiktoken (expect "ENCODER OK — engine: purepy")
mkdir -p /var/tmp/noteko && printf 'raise ImportError("blocked")\n' > /var/tmp/noteko/tiktoken.py
cd Apollo-Spider-v1.0.2 && PYTHONPATH=/var/tmp/noteko python3 \
  memento-package/machinery/_encoder_home.py --check 2>&1 | tail -2

# 5 — the stale premise, verbatim (expect the "does not expose a token count" line at 42)
sed -n '40,52p' Apollo-Spider-v1.0.2/memento-package/runbooks/_RUNBOOK-context-gauge.md
```

---

## RESIDUAL

1. **GPT-Sol's actual reasoning is not in the artefact.** The pack carries the *result* (3 settings
   keys) and Dave's *transcription* of the readings, but not the chat. If the exact `main.jsonl`
   schema matters for Tier 2, that needs Dave's Copilot session or a look at the file itself.
   **Unproven, and cheap for him to settle.**
2. **The three VS Code setting keys are unverified.** No network, no Copilot in this sandbox. I am
   reporting them as *found in his settings file and described in his state file*, not as
   *confirmed to work*. What would settle it: Dave confirming the log populates, or one look at a
   real `main.jsonl`.
3. **`271,997` and `220,000` are GPT-Sol's figures, transcribed.** Reported, not measured by me.
   The model-ceiling figure in particular is a register number whose column I cannot name.
4. **I did not run the pack's gates** against the 8 modified design files, so I cannot say whether
   his canon edits would pass our CI. Out of scope for the version question, and it is a real
   follow-on if those changes are ever considered for port-back.
5. **Why he thought the count failed is inference from strong circumstantial evidence** — the
   vocabulary collision fits every fact (working encoder, cl100k-stamped chain, W-17 titled
   "Activate the 220k context guard", a runbook that says "no reading to take"), but Dave saying
   *"yes, I meant the session gauge"* is what would close it, and one question does that.

---

*Sub: forensics, session #224 / W-263. Ruled nothing. Repo writes: this file only.
Both pack copies and `apollo-spider/` untouched; no git operations beyond `status` and `log`.*
