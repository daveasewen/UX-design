# 2026-07-21 — RAG completion (R-D20), the glyph-contrast sharpening (R-D6 A′), and the decision-graph question

*Narrative dossier (capture ritual step 1b). WHAT lives in the ledgers + `_LIVE-STATE`; this is the WHY/HOW.
Both-way links: `_proforma/_RAG-DECISIONS.md` (R-D20, R-D6 A′) · `_LIVE-STATE.md` LATEST DELTA (2026-07-21) ·
`docs/decisions/ADR-0007` + `notes/_STATE-MACHINE-TARGET.md` (the decision-graph target this session reopened).
Opened as a good-morning; became three linked things — a token completion, a rule reconciliation, and a
structural question about the record system itself.*

---

## Thread 1 — completing the RAG sets (R-D20)

**Why it was queued.** The evening-5 handoff had reframed the mislabelled "red tuner": Mono's status *signal*
colours were already ruled (breach red `#B92F1E`, watch amber `#F0B13A`, info blue `#5F92B9`, success green
R-D18). The genuine open work was to finish `error`/`warning`/`information` the way R-D18 finished `success` —
**not** to re-decide the signal colours (that would have been the binned-misstep trap the handoff warned about).

**How it went.** CONSULT first (the standing guard against retreading settled ground), which confirmed the shape
and surfaced the constraints that mattered: col26-008/009 (supporting palette is status-only, never text), the
severity order, and — importantly — R-D6 (glyph contrast by role). Surveyed the proven success tuner and the
token store: each set's `-background` and `-glyph` slots already held ruled Mono values; only two things per set
were actually open — the **message tint** (still Legacy) and the **bare role** (still aliased to a Legacy
primitive). So the tuner cloned the success one to three sets, locking glyph + fill, exposing only the tints.

**Dave's rulings on the live controller.** error `#F1E0DC`/`#2C120D` · warning `#F6E5CC`/`#3C2C13` · information
`#D6E3EC`/`#092131`. The one real judgement call the tuner surfaced: the warning **dark** tint — amber goes
muddy/brown as lightness drops, and Dave lifted the seed (`#261700`→`#3C2C13`) to keep it reading amber. This is
the value of a live tuner over static swatches: the failure mode (brown) is only visible in motion.

**The one non-mechanical decision in execution — Notifications.** The bare-role rebind rippled into the snippet
gate (7 surfaces drifted, exactly as the success rebind hit 7). Six were unambiguous Mono surfaces → swept. But
**Notifications is flagged DO-NOT-CONVERT** in `_STYLE-PROVENANCE.md` §A-AUTH: it's an Apollo *Legacy reference*
(its `#A8000B` is legitimate Legacy red; no Mono notification canon exists yet). Blindly sweeping it would have
destroyed a deliberate record. Instead: extended its existing `driftAllow` waiver to cover the R-D20 roles, with
a reason citing the ruling — honouring "do not convert" without fighting the gate. Proper long-term fix = retag
to the Legacy theme (a future build). This is the kind of thing that separates a mechanical sweep from a
judgement one, and why the sweep wasn't delegated blind.

**Landed.** Build green 37/37; committed `1a5bc94`. Unblocks Alert/Banner/Toast.

---

## Thread 2 — R-D6 A′: the glyph-contrast sharpening

**Why it came up.** Dave questioned whether the amber glyph "passing accessibility" contradicted a rule he
remembered — that contrast only bites when a glyph carries meaning *alone* (an arrow beside a percentage). He was
right: that's R-D6 Ruling A, almost verbatim his original words. Verified against the rule text + the numbers
rather than answering from memory (the amber glyph `#C58900` = 3.02:1 on white, clearing the 3:1 non-text floor;
the bright fill `#F0B13A` = 1.90:1, which is *why* a darker glyph value exists at all — perceptibility of the
shape, not colour carrying meaning). The tuner had used the 3:1 bar, not 4.5, so nothing shipped contradicted it.

**The sharpening Dave then made (A′).** *"The only coloured icons are the statuses, and the warning roundel has a
black exclamation mark — even here there's enough contrast. So the only glyphs that need to conform to the
contrast rule are ones where meaning is carried exclusively by the glyph, like an arrow and a figure."* Reflected
back and confirmed firm before recording (the standing reflect-back discipline). Black-on-amber = 11.06:1, ample.

**Why it mattered beyond the one rule.** It resolved a *standing tension* in the corpus: `icon-011` reads "icons
need 4.5 in all instances, labelled or not," which looks like it contradicts the RAG 3:1 floor. A′ bounds
`icon-011`'s live scope to the meaning-exclusive glyph, and *subsumes* the older R-D3 amber roundel-leg exemption
(that 1.9:1 "failure" was never real — colour was never the channel). Recorded in three places: R-D6 A′ (canonical
home), a scope note on `{#icon-011}`, and folded into `{#icon-015}` so it regenerates into `_RECONCILIATION.md`.

**A process catch.** First tried to hand-edit `_RECONCILIATION.md` directly — it's *generated* from REVIEW-tagged
rules, so the rebuild wiped the edit. Correct mechanism: edit the rule (icon-015), let the register regenerate.
Committed `1bb09f9`.

---

## Thread 3 — the structural question: should the decision records be a graph?

**Dave's prompt.** Reconciling icon-011 ↔ icon-015 ↔ R-D6 ↔ R-D3 by hand was archaeology. His question: is there
a better structure — replicate decisions across records so there's nothing to reconcile, or better recall /
tagging / a map / a KG?

**What the desk research found (internal + external).** This is **already decided**: ADR-0007 ratified a
*temporal decision-graph, lightweight-first* — typed edges, one source of truth, generated views, a staleness
gate. Slice 1 is built (`_build_live_state.py`). The half that would have caught today's tangle before Dave asked
— **typed edges between records + a reconciliation view/gate** — was designed and never built, because the edge
convention was never authored. So rulings still cross-reference in *prose* ("refines icon-013", "subsumes R-D3"),
which is exactly why recall = keyword search (consult) and reconciliation = manual. A July-2026 external scan
confirmed the pattern hasn't moved and sharpened two points: *"structure is where the truth lives — what got
superseded, what reconciliation exists because consistency was deferred"*, and the named anti-pattern *"tool
temptation: buying graph tooling before clarifying use cases → expensive emptiness."*

**The judgement, option by option.**
- **Replicate across records — rejected.** That's the rot engine: more copies to sync; it's what produced the
  stale "backlog A" and the memory-only "R-D15". Denormalise only in generated *views*, never in source.
- **Tag / recall / a map — the high-value slice.** IDs already exist (R-D*, ADR-*, `{#id}`); what's missing is
  typed edges as front-matter, from which a map falls out for free.
- **KG (graph DB) — the north-star, not now.** ADR-0007's load-bearing line, echoed by the scan: the graph is
  just a queryable view over well-recorded edges; the discipline of writing the edge at ruling-time prevents
  rot, not the storage engine. Text-based KG gets 80%.

**The concrete missing slice (the next build):** (1) a typed-edge convention on ~35 decision nodes
(`refines · supersedes · subsumes · bounds · conflicts-with · verified-by` + status + validation); (2) a
generator producing the LIVE/DEAD/OPEN ledger + a **reconciliation view** (auto-surface any conflicts-with edge
with no resolution) + a per-node "what touches this" map; (3) a **conflict gate** — A bounds/conflicts B with no
recorded resolution → build flags it. That turns today's manual reconciliation automatic; icon-011 vs R-D6 would
have lit up on its own.

**Routing decision.** Tasked to **Fable, fresh session** — it fits the canon's Fable use ("big, high-stakes,
hands-off, I need to trust this"; wrong taxonomy = corpus-wide rot; Dave won't hand-review 35 nodes' edges). Two
guardrails held: genuine conflicts the audit surfaces are **queued for Dave's ruling, not auto-resolved**
(promotion is Dave's, routing rule 2); and it runs **cold**, not from this loaded session (rule 6). Open sub-call,
cheap to defer: Fable authors all edges in one sweep vs stops at spec+gate and hands edge-authoring to Sonnet —
decided *after* the audit shows how subtle the edges are. Pinned as the next-session focus.

---

## Resolved state / still open
- **RAG:** all four sets complete + Mono; Alert/Banner/Toast unblocked. Theme-provenance gate still **advisory**
  (58 foreign hexes / 67 files — parked archived-file cleanup, not this ruling). `tabs/active` + `progress/complete`
  still unruled (archived consumers). Notifications retag-to-Legacy is a future build.
- **Rules:** R-D6 A′ recorded + reconciled corpus-wide; the mark-vs-roundel mechanisation (icon-015 tail b) still
  deferred to supercharge.
- **Structure:** the decision-graph edge convention is the pinned next build (Fable). ADR-0007's unbuilt generator
  half finally has a concrete trigger.
