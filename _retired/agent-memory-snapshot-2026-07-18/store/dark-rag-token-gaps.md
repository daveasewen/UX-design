---
name: dark-rag-token-gaps
description: "Token-store finding — dark rag/information + focus/ring alias a MISSING color/blue/400 and resolve to an illustration colour; success/warning don't darken; Dave wants to revisit"
metadata: 
  node_type: memory
  type: project
  originSessionId: 29f62e34-4096-4e20-9fcc-10f2a34ec864
---

**FOUND 2026-06-24 (Dave asked to trace dark-mode colours; flagged to REVISIT).** Dark colours resolve from primitives via a per-mode `$alias` on each semantic token in `tokens/semantic-colour.json` (baked `$value` = resolved hex from `tokens/colour.json`).

**FIXED 2026-06-24 (gap #1):** added `color/blue/400` = #4587A7 to `tokens/colour.json` (blue ramp now 100/400/600). The dangling alias is resolved (0 dangling) and `rag/information` [dark] + `focus/ring` [dark] now resolve to a real UI blue primitive instead of borrowing the illustration palette — ZERO value change, so all ~24 focus-ring snippets + the 3 info-accent snippets (Status-indicator/List-items/Notifications) are untouched. Token store 635→636 leaves; build green.

**The gaps:**
1. **[FIXED] Dangling alias → illustration leak.** `rag/information` [dark] and `focus/ring` [dark] aliased **`color/blue/400` which did NOT exist**; baked `#4587A7` = `color/illustration/blue-5`. Fixed by adding the primitive (above). NOTE the value #4587A7 white-on-it is still only 4.0:1, so it works as an ACCENT (border/icon/focus/dot) but NOT as a solid FILL with white text — the Global notification dark fill therefore uses blue/600 #305A85 via a scoped snippet `driftAllow`. REMAINING token gap: no dedicated dark **rag-SURFACE** token for solid status banners.
2. **Sparse dark blue UI ramp.** colour.json blue ramp = only `blue/100` #EBEFF4, `blue/600` #305A85, `blue/dark/blue-tint` #000D1B. No mid/dark UI blue → nothing legitimate to point a dark info/focus at.
3. **success/warning don't darken.** `rag/success` & `rag/warning` alias the SAME primitive in both modes (`color/green/600` #00847F, `color/amber/600` #FFBB33). (rag/error DOES darken: light color/red/600 #A8000B → dark color/primary #DB0011.)
4. **NOT leakage:** `data-vis/data-chart/*` aliasing `color/data-vis/*` is correct by design.

**PROVENANCE RECEIPTED 2026-07-02 (day session):** #4587A7 confirmed at source = **Blue 5 of the
LEGACY illustration palette** (create.hsbc `foundations-and-identity/colour/illustration0.html`,
Blue 4 Base = #63C2EF). The legacy page's own scope rule makes it illustration-only, so the leak
diagnosis is now source-backed, not inferred. Page is superseded by the 2026 unified supporting
palette; receipt recorded in `guidelines/illustration-standards.md` §Findings.

**POLICY RULED 2026-07-02 (eve, Dave) — reshapes this whole problem:** rag roundel vs surface ≥3:1; internal mark vs roundel fill ≥4.5:1; **dark mode = WHITE roundel + BLACK mark** (icon+label carry meaning). Consequence: the dark rag-accent dead zones DISSOLVE structurally (no coloured roundels in dark at all) — the dark-darkening question for rag ICONS becomes moot. Remaining from this memory's gaps: dark rag-SURFACE token for solid banners (gap #1 note) still open; **amber fails the roundel leg in LIGHT** (1.69 on white / 1.60 on tint, `_ICON-CONTRAST-DELTA.md` §3) — darker amber primitive would fix both this and gap #3's warning half. Implementation tranche pending Dave's HTML review (Notifications success mark → white, dark white-roundel structure, Input-fields hardcoded rag fills → tokens). See [[desk-rulings-2026-07-02]].

**2025-STANDARD RECEIPT (2026-07-02 late eve, colour-2025 ingest):** the CURRENT 2025 standard
(`colour/illustration.html`) also publishes #4587A7 as illustration Blue 5, and the 2025 RAG
palette publishes exactly ONE UI blue: **#305A85 ("useful information; usually no action
required") = `color/blue/600`** — sitting at /600 like its RAG siblings (red/amber/green all
match at /600). So the published-standard answer to gap #2 is: the RAG blue IS blue/600; any
dark-legible blue-400 must be DERIVED from it (charter §6), never imported from illustration.
Logged as **col25-018 [REVIEW]** in `colour-usage.md` (now engine-era with the 2025→2026 delta
map; token store proven value-exact vs 2025 standard = provenance receipt for ADR-0005).

**FIX PREPARED + HELD (2026-07-03, Dave: "hold for a render session"):** derivation
ladder computed from #305A85 (hue 210°/sat 47%): **#719ECC** passes ≥3:1 on ALL dark
surfaces incl. #474747; **#6293C6** all but #474747 (2.88); current #4587A7 fails
#404040/#474747. Blast radius measured: 24 snippet manifests + notifications/tabs
meta (inspect, hex appears in historical findings) + canon.css regen. All recorded
on col25-018 in `colour-usage.md` — the render session starts warm.

**RULED 2026-07-03 — LOGGED AND CLOSED (log-and-move-on):** Dave routed BOTH findings to the
new DS-improvements register per [[derivation-governance]] — `_DS-IMPROVEMENTS.md` **ds-001**
(dark UI blue; #4587A7 stands, #719ECC/#6293C6 unpromoted evidence) + **ds-002** (dark error
text; #DB0011 stands, #FF3D4C et al unpromoted). No token/component change. The 2
Selection-controls dark sweep fails are ds-002's signature (known-good = 36/38 + signature).
col25-018 closed in colour-usage.md. Historical detail below.

**RENDER SESSION 2026-07-03 — evidence LIVE, decisions staged:** built
`knowledge/_fitness-test/blue400-review.html` (live canon.css, candidate switcher, ring vs all
6 dark surfaces, in-situ components) — Dave to pick #719ECC (rec) vs #6293C6. AND a NEW gap
found while verifying the sweep's Selection-controls catch: **gap #5 — dark error TEXT
#DB0011 on #000000 = 4.02:1 AT REST** (label + message; light is fine, #A8000B on white 7.87).
rag/error DOES darken (gap #3's exception) but not far enough for TEXT; no published red sits
above #DB0011, so it's the same charter-§6 derivation call as blue: ladder at hue 355°/sat 100
= #FF3343 / **#FF3D4C (rec)** / #FF4D5A — TEXT only, graphics (border/mark/roundel) stay
#DB0011 (4.02 ≥ 3:1). Both decisions UNENACTED pending Dave. (The sweep's original "light
hover 4.02" label was a gate artifact — see [[gate-blindspot-state-contrast]]: the sweep was
clicking each snippet's own theme toggle; fixed 2026-07-03, re-swept 36/38 clean.)

**Interim fix applied (Dave's call):** in the Notifications snippet, dark mode uses the LIGHT rag accent values for stroke/surface + white icons for contrast. **REVISIT at token level:** either add a real dark UI blue primitive, or re-alias `color/blue/400` → `color/blue/600`; fixing it also fixes dark focus rings board-wide. Integrity gate does NOT currently catch dangling semantic→primitive aliases (only token-manifest var resolution) — candidate new check. Relates to [[token-collection-architecture]], [[gate-blindspot-state-contrast]], [[component-review-program]].
