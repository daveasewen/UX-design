# Compaction and fill — research brief

**Worker task, conductor-worker construction. 2026-07-31.**
Scope: `knowledge/_checkin.py`, the live session transcript, and Anthropic's public docs.
Transcript examined: `d995d8c6-ccb3-4d8d-8ed1-4a30f00a4f9f.jsonl` (this session), plus its three
`subagents/agent-*.jsonl` children, all under
`/sessions/quirky-lucid-hawking/mnt/.claude/projects/-Users-daviewen-...-cs60kt/`.

---

## Executive summary (read this first)

1. **Q1 — yes, `_checkin.py` measures the wrong object, but NOT via subagent contamination.**
   It sums every record in the session's own top-level `.jsonl` except three meta types. That log
   contains this session's full turn history — including every `thinking` block ever emitted and
   the raw message envelope (`id`/`model`/`usage`/`stop_reason`) — none of which is what the *next*
   API call actually resends. The **subagent-contamination hypothesis is REFUTED**: subagent
   internals are not inlined; only their small final `tool_result` (~2–3K tokens) lands in the
   parent transcript. Anthropic's own docs confirm this by design.

2. **Q2 — no compaction occurred this session, and the evidence is conclusive, not circumstantial.**
   Every one of the 209 assistant turns' `usage.iterations` is `type: "message"`; zero are
   `type: "compaction"`. The real per-turn input-token total is strictly increasing across the
   whole session with no drop >10% anywhere. Compaction is documented (both Claude Code's
   client-side auto-compact and the raw API's `compact_20260112` beta) and, when it fires, is
   detectable — it leaves a distinct marker. It left none here.

3. **Q3 — fill is not just derivable, it's already sitting in the transcript, unused.**
   Every `assistant` record's `message.usage` carries `input_tokens` +
   `cache_creation_input_tokens` + `cache_read_input_tokens` — Anthropic's own real-tokenizer count
   of exactly what was sent to the model for that call. Summed, these three fields
   (`total_input_tokens`, Anthropic's own documented formula) give a **direct, non-proxy fill
   reading for every turn in the session**, no cl100k re-tokenization needed. Reading it off the
   last assistant turn in this session's transcript right now gives **285,311 real input tokens**
   — already past the 200,000 working budget and past the 256,000 hard ceiling named in `_CHAIN.md`.
   The ±8,000 harness/system-prompt hole (`ds-025` item 1) is **effectively closed for the total**,
   though not decomposable into its sub-parts (see Q3 for the precise claim).

---

## Q1 — is `_checkin.py` measuring the wrong object?

### What it sums, exactly

Read in full: `knowledge/_checkin.py`. The mechanism:

```python
TRANSCRIPT_GLOB = "/sessions/*/mnt/.claude/projects/*/*.jsonl"
...
hits = glob.glob(TRANSCRIPT_GLOB)
...
return max(hits, key=os.path.getmtime)
```

then, per line:

```python
payload = rec.get("message", rec)
by_type[kind] = by_type.get(kind, 0) + len(enc.encode(json.dumps(payload)))
```

for every record whose `type` is **not** in `META_TYPES = ("queue-operation", "last-prompt", "mode")`.

Two things worth flagging that the docstring doesn't say plainly:

- **The docstring claims it measures "the conversation half — user / assistant / attachment
  records" (`CONV_TYPES`), but `CONV_TYPES` is never referenced in `main()`.** The actual filter is
  "everything except the three META_TYPES." In this transcript that happens to equal exactly
  `{assistant, user, attachment}` (confirmed below), so the claim is currently true by coincidence,
  not by code — a new record type that isn't one of the three META_TYPES would be silently summed
  in, undocumented.
- **It tokenizes `rec["message"]` wholesale**, which for an `assistant` record includes `id`,
  `model`, `stop_reason`, `stop_sequence`, `stop_details`, and — the ironic part — the entire
  `usage` object (see Q3). It is paying tape to encode the exact field that would answer its own
  question, and counting that encoding as "conversation."

### Where the transcript comes from, and Anthropic's own warning about parsing it

Confirmed by running the glob directly: it matches exactly **one** file —
`.../d995d8c6-ccb3-4d8d-8ed1-4a30f00a4f9f.jsonl` — because the pattern has exactly two `*` segments
after `projects/` and does not cross the extra `subagents/` directory boundary the three child
transcripts live under. Empirically verified, not just reasoned about:

```
CHOSEN: .../d995d8c6-ccb3-4d8d-8ed1-4a30f00a4f9f.jsonl
```

Running the script live mid-task: `421 records`, `MEASURED 365,776 tape` (assistant 272,774 / user
69,816 / attachment 23,186) — up from the brief's cited 389 records / 338,887 tape, because the
session kept running between when that figure was taken and now.

Anthropic's own docs (`code.claude.com/docs/en/sessions.md`, "Where transcripts are stored")
say plainly:

> "By default, transcripts are stored as JSONL at `~/.claude/projects/<project>/<session-id>.jsonl`...
> Each line is a JSON object for a message, tool use, or metadata entry. **The entry format is
> internal to Claude Code and changes between versions, so scripts that parse these files directly
> can break on any release.** To build on session data, use `/export` or the script interfaces
> instead."

`_checkin.py` does the thing this page warns against. That's not disqualifying — the script already
labels its output as an unverified proxy — but it's a citable reason the record-type set could shift
under it without warning.

### Record types actually present, and what each is

```
209  assistant
131  user
 37  last-prompt
 22  attachment
 15  queue-operation
  7  mode
```

- `queue-operation` — e.g. `{"type":"queue-operation","operation":"enqueue",...,"content":"good morning"}`
- `last-prompt` — `{"type":"last-prompt","lastPrompt":"good morning",...}`
- `mode` — `{"type":"mode","mode":"normal",...}`
- `attachment` — e.g. `{"attachment":{"type":"deferred_tools_delta","addedNames":["TaskCreate",...]}}`
  — Claude Code announcing newly-loaded deferred tool schemas (the same mechanism visible in this
  very conversation's system-reminders).

None of these three META_TYPES, nor `attachment`, contains a `system` record. **`ds-025` item 1
("boot never measured... no `system` record type exists") STANDS, confirmed again on this session's
own transcript** — this reproduces a finding already recorded at
`notes/_MEMENTO-DECISIONS.md:1560–1563` (session #52/#53), not a new one. What's new below (Q3) is
a different route to the same number that doesn't need a `system` record to exist.

### `isSidechain` — checked directly, not inferred

```
grep -o '"isSidechain":[a-z]*' → 362 hits, ALL "isSidechain":false
```

362 = exactly `assistant(209) + user(131) + attachment(22)`, i.e. every non-meta record carries the
field and every one of them is `false`. No sidechain/subagent record is inlined in this transcript.

### ★ Critical check: are subagent windows summed into this session's figure? REFUTED.

Three `Agent` tool_use calls found, at lines 76, 319, 419 (the third is this very task — no
`tool_result` yet, because I haven't returned). For the two that have completed:

```
tool_use line 76  -> tool_result at line 80,  message.content JSON chars = 8,157   (~2–3K tokens)
tool_use line 319 -> tool_result at line 320, message.content JSON chars = 10,168  (~2–3K tokens)
```

Each subagent's **own** transcript is a separate file under `subagents/agent-*.jsonl` (129–250
records each), outside the glob `_checkin.py` uses. What crosses back into the parent's transcript
is only the bounded final report — matching the Agent tool's own contract ("it will return a single
message back to you"). This is confirmed by Anthropic's documentation, not just by this transcript:

> **Subagent** (glossary.md): "A specialized AI assistant that **runs in its own context window**
> with a custom system prompt, specific tool access, and independent permissions. It works on a
> delegated task and **returns a summary to the main conversation**. Use subagents to keep large
> explorations out of your primary context or to run parallel research."

> (how-claude-code-works.md, "Manage context with skills and subagents"): "**Subagents get their own
> fresh context, completely separate from your main conversation. Their work doesn't bloat your
> context. When done, they return a summary. This isolation is why subagents help with long
> sessions.**"

**Plain statement for the record: the 365,776-tape figure does NOT include anything that was never
in the conductor's context via subagent inlining.** The overshoot is real but comes from a different
mechanism (below), and the subagents' own 200K+ overshoots are a *separate, non-overlapping* budget
problem, not a double-count baked into the conductor's number.

### So what IS inflating the cumulative figure, if not subagents?

Breaking the 365,776 down by content-block type (not just top-level record type):

```
thinking blocks:        165,784 tape across 76 blocks   (45% of the whole measured figure)
assistant tool_use:      48,085 tape
assistant text:           3,960 tape
user tool_result:        68,166 tape
user text:                   328 tape
[message-envelope overhead not attributable to content: ~55,000 tape — id/model/usage/stop_reason]
```

`thinking` blocks are ~45% of everything `_checkin.py` counts. Whether that's an over-count relative
to what's actually resident is **model-generation-dependent**, and this matters for what the fix
should be (see Q2/Q3): some generations strip old thinking blocks from context, some retain and bill
them. `_checkin.py` treats all 76 blocks as equally "real" regardless.

---

## Q2 — compaction: documented behaviour, and did it happen here

### What's documented (quoted, not paraphrased, with source)

**Claude Code's automatic compaction** — `code.claude.com/docs/en/how-claude-code-works.md`,
section "When context fills up":

> "Claude Code manages context automatically as you approach the limit. **It clears older tool
> outputs first, then summarizes the conversation if needed.** Your requests and key code snippets
> are preserved; detailed instructions from early in the conversation may be lost. Put persistent
> rules in CLAUDE.md rather than relying on conversation history."
>
> "If a single file or tool output is so large that context refills immediately after each summary,
> Claude Code stops auto-compacting after a few attempts and shows an error instead of looping."
> (→ "Auto-compaction stops with a thrashing error", troubleshooting.md)

`code.claude.com/docs/en/glossary.md`, **Compaction**:

> "Automatic summarization of your conversation when the context window approaches its limit. Older
> tool outputs are cleared first, then the conversation is summarized. **Project-root CLAUDE.md and
> auto memory survive compaction and reload from disk; instructions given only in conversation may
> be lost.** Run `/compact` to trigger manually, optionally with a focus like `/compact focus on the
> API changes`."

Third-party (DeepWiki, reverse-engineered from the Claude Code changelog — **not** an Anthropic
source, cited as corroboration only): "Auto-compaction triggers when token usage reaches
approximately 98% of the effective context window." WebSearch's synthesis of the interactive
`code.claude.com/docs/en/context-window` page (not independently re-verified against the raw page,
which is a JS-hydrated widget that would not fully render through the fetch tool) adds: the exact
trigger threshold "is not officially published and has shifted across releases," and `/compact`
"preserves the system prompt, the project-root CLAUDE.md, unscoped rules, and auto-memory," dropping
path-scoped rules and nested CLAUDE.md files until re-read.

**Is it announced / detectable from inside a running session?** Two separate mechanisms exist:

- The **raw API beta** (`compact-2026-01-12`, `platform.claude.com/docs/en/build-with-claude/compaction`,
  fetched in full) is explicitly, structurally detectable: a triggered compaction inserts a
  `{"type": "compaction", "content": "<summary>"}` content block into the response, can set
  `stop_reason: "compaction"` (with `pause_after_compaction`), and always reports a
  `{"type": "compaction", "input_tokens": ..., "output_tokens": ...}` entry in `usage.iterations`
  when one fires — quoted in full below (Q3), because this same `usage.iterations` field is what
  answers Q3.
- Whether **Claude Code's own client-side auto-compact** uses this exact API primitive internally,
  or manages the message array itself, is **not stated** in the pages I could reach. I could not
  find a primary-source sentence confirming a routine, always-on, in-transcript "announcement" the
  moment ordinary (non-thrashing) auto-compact succeeds — only the thrashing/error path is
  explicitly documented as user-visible. **Flagged UNPROVEN rather than guessed.**
- One concrete, non-hypothetical detection path exists regardless of which mechanism Claude Code
  uses: `/branch`'s naming behaviour. `sessions.md`: "As of v2.1.198 this also applies after
  [compaction](/docs/en/how-claude-code-works#when-context-fills-up); earlier versions fell back to
  the literal name `Branched conversation` instead of **looking past the compaction summary** to the
  original first prompt." This confirms Claude Code's own internals can locate a compaction
  boundary programmatically — i.e. it is a real, addressable artifact, not an invisible rewrite.

### Did THIS session compact? No — checked three independent ways, not asserted

1. **Record-type scan**: no `summary`/`compaction` value anywhere in the `type` field across all 421
   records (six types total, listed in Q1).
2. **Text-content grep**: `grep -ico "compact"` → 25 hits, all inside `user` records — every one is
   this repo's own MEMORY.md text about the *GM banner compaction ritual*
   (`gm-banner-compaction.md`), an unrelated naming collision, not a session-compaction event.
   Quoted example (line 14): *"the compactable cap is aimed at cold-start cost, and #33 cut the
   chain out from under it"* — GM-banner vocabulary, not context-window vocabulary.
3. **The authoritative check** (this is the one that actually proves it, not just fails to disprove
   it): every `assistant` record's `message.usage.iterations` array was inspected. Across all 209
   assistant turns:

   ```
   distinct iteration types seen: {'message'}
   compaction iterations found: 0
   ```

   And the real per-turn total (`input_tokens + cache_creation_input_tokens + cache_read_input_tokens`,
   Q3's formula) is **strictly increasing, zero drops greater than 10% anywhere in 209 turns**:

   ```
   every 25th sample: [61582, 94784, 134945, 166357, 191334, 208926, 228079, 254092, 277131]
   min 61,582 · max 285,311
   ```

   A real compaction fire would show up here as a sharp drop (old content replaced by a short
   summary) or a `compaction`-typed iteration. Neither appears once. **This session has not
   compacted, stated plainly as a finding, not a null result.**

---

## Q3 — can fill be derived?

### The formula the brief anticipated (record-type filtering of cl100k tape) — works, but is second-best

If forced to derive fill from re-tokenizing the cumulative log, the classification would be:

- **Count**: `user` text, `tool_result` content, `tool_use` content, `attachment` records.
- **Exclude**: the three META_TYPES (already excluded); message-envelope fields (`id`, `model`,
  `usage`, `stop_reason`, `stop_details` — never resent as input, ~55K tape of noise in this
  session alone); `thinking` blocks from turns outside the live tool-use arc, **conditionally** —
  see below.
- **Still unresolved even with this filter**: whether to keep or drop old `thinking` blocks depends
  on model generation, and that dependency is itself model-specific and non-trivial to encode.

### The better formula: read what Anthropic already computed, in Claude's real tokenizer

Every `assistant` record's `message.usage` already carries the real answer. Confirmed against
Anthropic's own documentation (`platform.claude.com/docs/en/build-with-claude/prompt-caching`,
"Tracking cache performance" / "Understanding the token breakdown" — fetched in full):

> "`cache_creation_input_tokens`: Number of tokens written to the cache when creating a new entry.
> `cache_read_input_tokens`: Number of tokens retrieved from the cache for this request.
> `input_tokens`: Number of input tokens which were not read from or used to create a cache (that
> is, tokens after the last cache breakpoint)... **To calculate total input tokens:
> `total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens`**"

And, critically for the ±8,000 hole: "**Prompt caching references the entire prompt - tools,
system, and messages (in that order)** up to and including the block designated with cache_control."
The system prompt and tool schemas are part of what gets cached and counted — this is not a proxy
that only sees conversation, it is the real API's own accounting of the entire call, harness
included.

**Applied to this session** (`message.usage` field, sampled directly from the transcript, no
re-tokenization):

```
FIRST assistant turn (line 8):  input=2  cache_creation=41,857  cache_read=19,723  → TOTAL_IN = 61,582
LAST  assistant turn (line 419): input=2  cache_creation=1,715  cache_read=283,594 → TOTAL_IN = 285,311
```

**The first-turn figure is, in effect, the true boot cost** — that call's input is system prompt +
tool schemas + MEMORY.md + CLAUDE.md + the first user turn ("good morning", ~2 tokens) and nothing
else; there is no prior conversation to inflate it. Measured directly: **61,582 real tokens**, not
the inherited "~17–20,000 est ±8,000" figure carried in `_LIVE-STATE.md` and `ds-025` since session
#37. That inherited figure is now falsified by direct measurement, by a wide margin (61,582 is
outside even the top of a 20,000±8,000 band by more than double).

**The last-turn figure is the live answer to "how hot are we now": 285,311 real tokens** — already
42.6% over the 200,000 working budget and 29,311 tokens past the 256,000 "past this, everything
goes badly" ceiling named in `_CHAIN.md`. This is not a projection; it is what the API actually
charged for the most recent completed call.

Cross-check against `_checkin.py`'s own cumulative cl100k figure: 365,776 tape vs 285,311 real
tokens at the same point in the session ≈ **1.28×** over-count from the cumulative/proxy method —
real, but far less dramatic than "339K cumulative, unknown fill" made it sound, and the true number
was *worse* relative to budget than the working assumption, not better (285K is already past both
lines Dave was warned about).

**Robustness property worth stating plainly**: this method does not need to know whether compaction
fired. If it had, the very next `usage` block would already reflect the shorter, post-compaction
prompt — the API's own accounting absorbs the event automatically. No separate compaction-detection
step is a prerequisite for the fill number to be correct; Q2's check was for *this brief's*
purposes, not because the Q3 formula depends on it.

### Applied to the three subagents (bonus finding, not asked for but load-bearing)

Same method run against the three `subagents/agent-*.jsonl` files:

```
agent-a3a29a0ccc0e10c8a.jsonl: first=31,199   last=215,959   (147 assistant turns, 0 compaction iterations)
agent-a425a76ef0394cc25.jsonl: first=31,012   last=237,123   (172 assistant turns, 0 compaction iterations)
agent-afcb1e872d1a14ca0.jsonl: first=30,515   last=216,998   ( 80 assistant turns, 0 compaction iterations)
```

**All three subagents' real last-turn fill exceeded 200,000** — not "two of three" as the
cumulative-tape self-reports (121,464 / 243,258 / 221,989) suggested. I have not matched which file
corresponds to which of those three self-reported numbers (no timestamp/identity cross-reference was
done), so I'm not asserting a specific pairing — but the two SETS disagree on the headline count (2
of 3 vs 3 of 3 over budget), and the real-token method is the one backed by Anthropic's own
per-call accounting, not a re-tokenization. Also notable: for at least one pairing the real number
is *higher* than the cumulative cl100k figure, not lower — cumulative tape is not reliably an
over-estimate of real fill; it can undercount too, depending on content mix.

### What remains genuinely unobservable

- **Decomposing the 61,582/30,515–31,199 first-turn totals into their sub-parts** (system prompt
  alone vs. tool schemas alone vs. MEMORY.md alone) is still not possible from this data. The
  `usage` field gives the sum for that call, not a breakdown by prompt section. Isolating the
  harness component specifically would need either a second data point (e.g. a session/subagent
  with materially less memory/CLAUDE.md content, to subtract) or an Anthropic-side tool this repo
  doesn't have access to.
- **`ds-025` item 1, precisely restated**: the concern was "we've been pricing the boot/front-load
  against an unmeasured, inherited ~17–20K estimate." That concern is now closed — the total is
  measured, directly, at 61,582 for this session. The narrower question "how much of that 61,582 is
  harness-only, isolated from memory/CLAUDE.md" is **still unobservable**, and that narrower
  question is a different, smaller claim than what `ds-025` item 1 was actually blocking. Dave
  should rule which claim he needs before this is called closed.
- **The exact per-model thinking-block retention rule for `claude-sonnet-5` specifically** — I found
  primary-source text classifying "Opus 4.5 and models numbered 4.6 and higher" as retaining prior
  thinking blocks by default, and Sonnet 5 is later than Sonnet 4.6 in the lineage, so it almost
  certainly falls in the "retained" camp — but no fetched page named `claude-sonnet-5` by that exact
  string in the preservation rule. Flagged as strong-but-not-completely-nailed-down, and it does not
  matter for the Q3 formula above (the `usage` field already bakes in whatever the true policy is —
  this uncertainty only matters if someone tries to derive fill by re-tokenizing content instead of
  reading `usage`).
- **Whether Claude Code's own client-side auto-compact is announced in the transcript on an ordinary
  (non-thrashing) success** — not found in the pages fetched; see Q2. Does not block the Q3 formula
  (see robustness property above), but is a real gap if the goal is specifically "detect that
  compaction happened," independent of measuring fill.

---

## Appendix — methodology notes

- All raw counts above were produced by ad hoc Python against the transcript files directly (not by
  editing or running any repo script other than the unmodified `knowledge/_checkin.py`, run once
  as-is to reproduce its own live output). No repo file other than this brief was written.
- The `platform.claude.com/docs/en/build-with-claude/thinking` page (the main "Thinking" overview,
  which holds the full "Thinking and the context window" / "Thinking block preservation by model"
  section) could not be fully retrieved — it hydrates via JS and the fetch tool returned only the
  nav chrome for that specific page, confirmed by grepping the saved fetch output for "stripped"
  and finding zero matches. The sibling "Extended thinking (legacy)" and "Thinking in tool and
  multi-turn workflows" pages fetched cleanly and are quoted above; the specific per-model table on
  the main overview page is the one piece of documentation I could not pull a verbatim quote from
  despite two attempts (direct fetch, then `.md`-suffix fetch + grep on the saved file, which hit an
  unrelated tool-side "line too long" limitation on both attempts).
