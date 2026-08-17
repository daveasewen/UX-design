# Apollo-on-Claude — architecture brief (#194, worker)

**Status: FLOATED — nothing here is ruled.** Written by a #194 worker session at Dave's ask
("spec this out as a worker, leave receipts for a conductor window"). Every decision below is
DAVE'S; the conductor window presents, it does not pick. Store row: `W-34`.

## Exec summary (read this, skip the rest until the sitting)

Apollo keeps its FULL functionality; Claude becomes the interface. The shape is three layers:
Apollo's engine (store, rulings, gates, generators) runs as **an MCP server we own**; Apollo's
working judgment (when to gate, how to present spreads, capture ritual) ships as **skills in a
plugin**; Apollo's visible surface (dashboards, variant spreads, review overlays, live
controllers) renders as **artifacts** that call the MCP tools live. Nothing in the engine is
dumbed down and nothing locks us into Claude — the same MCP server could front a standalone
app later.

Market context (researched #194, sources in the session transcript): Claude's plugin
marketplace is live at scale; Skills 2.0 (Q1 2026) ships executable scripts inside skills;
Anthropic's own frontend-design skill (277K+ installs) sells "better than average design" —
Apollo's pitch is the enforced upgrade of that premise. No shipped design plugin enforces a
design system with gates; that is the gap.

## The split (proposed, not ruled)

**Layer 1 — MCP server ("the engine").** Owns: `_state.json` store access, `_rulings.json`
reads (writes stay behind `_inscribe_ruling.py` — the only writer, unchanged), gate execution
(`check_gate`-style tools wrapping the existing gate scripts), theme/token generation, render
proofs. The repo's existing Python IS the implementation; the MCP server is a thin tool
surface over it, not a rewrite. Versioned as releases, same discipline as designer-skills
packs (packs are RELEASES — never auto-sync to live).

**Layer 2 — plugin skills ("the judgment").** Discover / Create / Craft / Dispatch as
skills; the capture ritual; review-presentation conventions (live spreads, light/dark,
responsive, decision controllers). Skills call Layer 1 tools; they hold no state.

**Layer 3 — artifacts ("the surface").** Progress dashboard, variant spreads, review
overlays, live tuners — persistent HTML views calling Layer 1 on load. The review layer is
already ruled a product feature; this is its delivery vehicle.

## Decisions owed to Dave (the conductor's sitting agenda)

1. **Is this a lane at all, and at what priority?** It competes with the standing-44 triage,
   the B3 return-with-numbers, and the ds-0NN reconciliation (this session's own titled item,
   not opened on Dave's word).
2. **Public shape.** Marketplace listing vs private plugin. Public copy stays abstract —
   sells "lovable on rails", never gate/token mechanics (standing positioning rule).
3. **Boundary of the engine.** Which gates are exposed as tools first? Proposal: start with
   read-only (store queries, ruling lookups, contrast checks) before any writing tool exists.
4. **Naming/branding.** Crescent mark is Apollo-only; whether the plugin carries it.
5. **The Memento question.** The session-governance machinery (chain, wrap, gauge) is
   entangled with the design system in one repo. Does the plugin ship design-Apollo only,
   or is Memento itself part of the product? (Recommend: design-Apollo only, first release.)

## Proposed lane divvy (for the conductor window)

- **Lane A (Opus sub):** engine inventory — enumerate which existing scripts become MCP
  tools, read-only first; deliverable = a tool manifest with per-tool inputs/outputs.
- **Lane B (Opus sub):** skills drafting — Discover/Create/Craft/Dispatch skill skeletons
  from the existing designer-skills-v2 pack; deliverable = draft SKILL.md set, NOT released.
- **Lane C (conductor's seat):** artifact prototype — one dashboard artifact calling a
  stubbed MCP tool, to give Dave something to rule on by eye.
- **DO-NOT-RULE list for any sub:** priority (D1), public shape (D2), engine boundary (D3),
  branding (D4), Memento scope (D5), and anything touching `_rulings.json`. Subs report;
  the conductor replays reports in-window.

## Consequences and pitfalls (mandatory, Dave #165)

(a) **A writing MCP tool is a new inscription path** — if any tool ever writes rulings or
store rows, `_inscribe_ruling.py`/`_state.add()` must remain the only writers underneath,
or the single-writer invariant silently dies. Read-only first is the fence.
(b) **Quota inversion applies**: users' Claude quota pays for inference; heavy gate runs
through chat are 5–10× the cost of running them locally. The MCP server should run gates
server-side and return verdicts, not stream gate internals through the model.
(c) **A plugin release is a generator** — auto-syncing repo state into a released pack
recreates the exact class the packs-are-RELEASES rule fences. Release = explicit, versioned,
Dave's word.
(d) **Artifacts cache reads** — a stale-looking dashboard will be a support question, not a
bug; the artifact must show its data's as-of.
(e) **This brief itself can rot** — it cites #194 market research; premises (marketplace
mechanics, Skills 2.0 behaviour) age faster than the rule and must be re-verified at build
time, not trusted from here.

## Pricing (planning estimates, NOT measurements — no standard applied yet)

Sitting: words only, one window segment. Lane A ~1 sub-window. Lane B ~1 sub-window.
Lane C ~10–15K in-window. All PICKED figures; re-price at the conductor's opener with
`_checkin.py` numbers in hand.

## Receipts

- This file: `notes/_briefs/2026-08-17-194-apollo-on-claude-brief.md` (store row `W-34`).
- Research trail: #194 session transcript (web sources on marketplace/Skills 2.0/frontend-design installs).
- Nothing ruled, nothing inscribed, no push. The titled ds-0NN item was NOT opened — declared.
