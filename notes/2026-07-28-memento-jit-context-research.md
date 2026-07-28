# Memento × JIT context — research survey and a floated shape

**Date:** 2026-07-28 (stamped from `date`) · **Register: FLOATED — research + options, nothing ruled, nothing enacted.**

```
provenance: notes/_receipts/2026-07-28-memento-jit-research-worker.md · 2026-07-28
status: floated
```
*(Fields added by the conductor at reconcile, 2026-07-28 — the worker declared the register in prose
but not in the machine-readable field the gate reads, so the gate FAILed the file. Transcribed from
the note's own "Register: FLOATED", not re-judged. The worker's session id was never recorded, so
provenance points at its receipt, which is the retrievable record.)*
**Origin:** Dave's idea, opener 2026-07-28: *"Claude uses a 'progressive reveal' 'JIT' 'lazy loading' technique for MCP tools… I wondered if we could improve the memento context management using similar techniques, perhaps having a separate search tool working with 'good morning'."*
**Context gauge at authoring: 🟡 AMBER ~46% (ESTIMATE).** Amber-authored ⇒ skim-check quoted numbers before trusting.
**Path per ds-017:** this note + one `_FUTURE-STATE.md` entry (same commit). No GM/§C edit — §C is at cap and this is unruled.

---

## 1. The idea, reflected back

Thin the always-loaded Memento chain down to an index + the rules that govern behaviour, and stand up a
search/retrieval front-end over everything else, so section bodies load only when a session actually needs
them — the same move the platform's Tool Search Tool makes for tool definitions. **Confirm or correct this
reading before anything gets ruled.**

## 2. The pattern, as shipped by Anthropic (OBSERVED, fetched 2026-07-28)

**Tool Search Tool** ([platform doc](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool), [engineering post](https://www.anthropic.com/engineering/advanced-tool-use)):
tool definitions are sent but marked `defer_loading: true`; context initially holds only the search tool +
a hand-picked eager set. Claude searches (regex or BM25 over names/descriptions/arg names), the API expands
only the 3–5 matches into full definitions. Their numbers: a five-server setup = ~55K tk of definitions
up front; tool search cuts that ~85%+ (worked example: ~77K → ~8.7K). Selection accuracy *degrades past
30–50 loaded tools* and search restores it: Opus 4 49%→74%, Opus 4.5 79.5%→88.1% on MCP evals. Guidance:
**"keep your 3–5 most frequently used tools non-deferred"** + a system-prompt line listing what categories
exist so the model knows to search.

**Agent SDK tool search** ([doc](https://code.claude.com/docs/en/agent-sdk/tool-search)): on by default;
the agent gets "a summary of available tools" (an index, not bodies); `auto:N` activates deferral when
definitions exceed N% of the window (default 10%). **After compaction evicts discovered tools, the agent
just searches again** — eviction is safe because retrieval is cheap and repeatable.

**Two siblings in the same release** ([advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)):
*Programmatic Tool Calling* — orchestrate in code so intermediate results never enter context (avg
43,588 → 27,297 tk, −37%); *Tool Use Examples* — show usage patterns instead of hoping schema implies them
(72%→90% parameter accuracy). Both are the same doctrine: **context receives conclusions, not working.**

## 3. What others do (OBSERVED via search, 2026-07-28)

- **Agent Skills' three-level progressive disclosure** ([overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), [structure guide](https://atlan.com/know/ai-agent/ai-agent-skills/skill-md-file-explained/)):
  L1 metadata ~100 tk/skill always loaded (a *menu*) → L2 SKILL.md body <5K tk on trigger → L3 bundled
  resources only when referenced. ~90% baseline reduction at 10 skills. This is the cleanest published
  template for tiering a *document corpus*, not just tools.
- **Anthropic context engineering** ([post](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)):
  agents keep **lightweight identifiers** (paths, queries, links) and load data just-in-time; *progressive
  disclosure through exploration* (file sizes, naming, timestamps carry signal). **Claude Code is explicitly
  a HYBRID: CLAUDE.md eagerly dropped in up front, glob/grep for everything else.** Compaction + structured
  note-taking (external memory re-injected later) are the companion moves.
- **MemGPT/Letta** ([paper](https://arxiv.org/abs/2310.08560)): OS-style memory hierarchy — main context
  (RAM) / recall storage / archival storage — with explicit paging functions (`archival_memory_search`,
  `core_memory_append`) the agent calls to move data between tiers. The academic ancestor of all of this.
- **Manus** ([lessons post](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)):
  **the file system as "the ultimate context"** — unlimited, persistent, agent-operable; compression must be
  *restorable* (drop a document's body, keep its path); **recitation** — rewrite a `todo.md` at the context
  tail so goals stay in recent attention; stable prompt prefixes for KV-cache economics.
- **Community:** session-memory search layers over Claude Code exist (e.g. [claude-mem](https://docs.claude-mem.ai/context-engineering)) — low-confidence pointer, not vetted.

## 4. Where Memento already is (the convergence is not flattery — most of the stack exists)

| Published pattern | Memento's existing organ |
|---|---|
| L1 metadata menu (Skills) | `MEMORY.md` one-line hooks → files on demand |
| Lightweight identifiers, JIT load | GM ★ POINTERS block ("canon lives at the target, one line each") |
| Search front-end over corpus | `knowledge/_consult.py` (corpus DISCOVERED since ds-009) |
| "Quote it, never recall it" | band-table grep rule; trust-the-spine |
| Compaction with restorable archive | 2c/2d banner rolls → `_GM-ARCHIVE`/`_LIVE-STATE-ARCHIVE`, verbatim |
| Structured note-taking / external memory | the entire repo: ledgers, briefs, `_DECISION-HISTORY/` |
| Sleep-time consolidation | dream-pass lane (proven ×2) |
| Recitation of goals | §C queue re-read each session |
| `auto:N` deferral threshold | M10's 28,000 tk chain threshold (ADVISORY) |
| Eviction is safe, re-search | Amber spine-flush → fresh window re-reads chain |

**The gap:** the chain contract already rules *"everything beyond the chain is RETRIEVAL"* — but the chain
itself is still **eager end-to-end**. The published pattern says the eager set should be the *duties and the
menu*, not the reference bodies.

## 5. The measured target (numbers from GM header + strata, 2026-07-27, tiktoken cl100k)

- Read chain **29.7K tk** ≈ GM 13.2K (incl. §A 4.21K) + LS ~16.1K. Cold floor measured 16.4% chain-only,
  ~23–24% with harness. **A fresh window buys ~78%, not 100% — the ~22% transaction fee.**
- **`_LIVE-STATE` standing body = 12,694 tk vs 1,422 tk in all three deltas** — the single fat eager region,
  already identified (#18) as what arms M10's block. It is *reference*, not duty.
- INFERRED (~3.53 B/tk corpus constant, unmeasured for LS specifically): an LS index of one-liners ≈
  60–80 entries ≈ **~1.0–1.5K tk**. Deferring the LS standing body behind it ⇒ chain ~29.7K → **~18–19K**,
  cold floor ~23–24% → **~18–19%: ~5–6 points of every window back**. Under the weekly-bank model the fee
  cut compounds across every window opened that week. **ESTIMATE — measure at enactment, not before ruling
  but before trusting.**

## 6. Floated shape (options, Dave rules; none started)

**Principle first — the line the tool-search guidance draws: DUTIES EAGER, REFERENCE DEFERRED.**
Rules that bind *unprompted behaviour* (throttle/M1, routing announcement, capture ritual, flag-concerns,
§A identity) can never be JIT — you cannot search for a duty you don't know you have. Reference state
(LS standing body, §C·2–5 detail, PRIOR banner, ledger content) is exactly what JIT is for.

- **O1 — cheap, no new tool:** give `_LIVE-STATE` a generated INDEX head (one line per entry, stable IDs);
  chain contract reads the index, bodies fetched by grep/`sed -n` on ID. The mover is M5-adjacent.
- **O2 — the "separate search tool":** extend `_consult.py` into `memento-search` over GM sections + LS +
  archives + briefs + decision-history, stable section IDs, BM25 unnecessary — the platform's own regex
  variant is literally grep. Ships with a **reachability gate** (every deferred section indexed or build
  fails — the ds-009/STAND-002 pattern) and **fail-loud on miss** (the ds-016 lesson; never a silent empty).
- **O3 — watch the platform:** memory tool / compaction / context-editing exist server-side but aren't
  Cowork knobs (observed 2026-07-21, gauge memory). If Cowork ever exposes them, O1/O2 artefacts are the
  right substrate already. No action.
- **The M10 symmetry, for free:** 28K stops being only a warn — it becomes the **demotion trigger**
  (chain over threshold ⇒ fattest reference section moves behind the index), the exact analogue of
  `auto:N`. Turns a thermometer into a valve — same arc as the gauge's own history.

## 7. Risks — flagged unprompted, and they are OUR defect classes

1. **JIT moves weight from the bloat side to the miss side.** Memento's signature defect is the *silent
   lookup failure* (ds-016: 265 rules invisible to the index; ds-018's arc). More retrieval = more miss
   surface. **The miss-side gates must strengthen BEFORE the eager set thins** — reachability gate +
   fail-loud are prerequisites, not accessories.
2. **A deferred duty dies silently** (the M7-suppressor shape: the check that would have been suppressed
   forever). Hence the principle in §6 — misclassify one duty as reference and it vanishes politely.
3. **The win assumes most reference is unread most sessions — UNMEASURED.** Instrument first: one line in
   the wrap ritual logging *which chain sections were actually cited this session* (cheap, M-set-adjacent).
   If sessions turn out to touch most of LS anyway, JIT buys latency + tool-calls and little else.
4. **Weakest joint, named:** the ~5–6-point saving in §5 is arithmetic on one measured week and an
   INFERRED index size; the accuracy-gain analogy (tool *selection* ⇒ stale-*reading* reduction) is
   directionally argued, not evidenced. Treat §5 as sizing, not a promise.

## 8. Suggested next steps (not started, in order)

1. Dave confirms/corrects the §1 reading; rules whether this enters the board (it displaces — §C at cap).
2. Cheap instrumentation first: section-usage line in the wrap (measures §7.3 before any surgery).
3. If ruled GO: O1 before O2 (index + IDs is M5-adjacent and pays even if O2 never lands); O2 rides the
   existing `_consult.py` rather than a new tool; gates land in the same window as the first deferral.

## 9. ADDENDUM 2026-07-28 (same day) — Dave's response + the code-vs-prose refinement

**Dave, verbatim:** *"1. your reading is right, but I guess I was wondering if we can make it even more
efficient, would by modularizing the 'search functionality' and making more code than prose help.
2. cool idea 3. I'll go with your instinct but I just want memento working better before working on
apollo again."* **Firmness of the priority: pending read-back (asked in-window) — nothing in this
section is a ruling.**

**Q1 answered — yes to both, with one line drawn: CODE FOR THE STATE TIER, PROSE FOR THE ORIENTATION TIER.**

- **Modular search:** split `_consult.py` into a CORE (index + query + fail-loud contract, **two-stage:
  return IDs + one-liners, fetch bodies as a separate step** — the `tool_reference`→expansion lesson
  from §2) plus corpus ADAPTERS: DS-decisions (exists since ds-009) and Memento (GM sections · LS
  entries · archives · briefs · ledgers). One retrieval spine, three customers — it also serves the
  KG forcing function Dave floated 2026-07-27.
- **More code than prose — where it pays, receipts already on the books:** the state tier has been
  trending to code all month: §A hash pinned in `section_a_digest()` CODE, not a comment (#17/#18) ·
  M8's bite — *"a fixture written from a comment is a fixture written from recall"* · the
  `born/guards/until` tags are a LATENT SCHEMA hand-written in prose (OBSERVED on GM §C worklist items;
  LS presumed similar — verify at build). Formalising: LS entries become structured records; the index
  AND the human-readable view are both GENERATED — the engine's own canon.css doctrine (generate, don't
  retype) applied to its memory. Prose stops being the spine and becomes a view; the prose-drift class
  closes by construction.
- **Where prose stays:** §A why-framing, banner narrative, verbatim rulings. The three registers are
  never flattened; provenance, hedges and quotes are the confident-false-inscription guards and they
  live in prose. **Data carries STATE; prose carries WHY.**

**Sequencing under "Memento before Apollo" (instinct, delegated by Dave):**
M-set build window UNCHANGED and first (M4a·M4b·M5 — M5's mover is load-bearing for any restructure;
scope not fattened: a ruled sequence is not a ruled fit) → §7.3 instrumentation rides a wrap → **O1′**
LS schema + generated index/view → **O2′** modular memento-search + its gates → Apollo (§C·1) resumes.
Each window priced at its own opener, not here.

## Sources

[Tool search tool — platform docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool) · [Advanced tool use — Anthropic engineering](https://www.anthropic.com/engineering/advanced-tool-use) · [Tool search — Agent SDK](https://code.claude.com/docs/en/agent-sdk/tool-search) · [Effective context engineering — Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) · [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) · [SKILL.md loading levels — Atlan](https://atlan.com/know/ai-agent/ai-agent-skills/skill-md-file-explained/) · [MemGPT paper](https://arxiv.org/abs/2310.08560) · [Manus context-engineering lessons](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) · [claude-mem (unvetted)](https://docs.claude-mem.ai/context-engineering)
