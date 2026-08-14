# PLAN — #172 "back on track" · 2026-08-14 · v1

**Goal (Dave's words):** get back to creating components at the weekend / next week. Between now
and then: (A) enact the Memento changes from the borrowed-instruments brief, (B) wire the tokens +
atomic system ready for component building, (C) label everything on the dashboard as Apollo vs
Memento.

**Posture:** fresh quota week (weekly 4% · Fable 6% at opener) — delegation is cheap in QUOTA.
Session window is the binding constraint per window as usual. Subs = Opus, explicitly, always.

---

## A. Memento changes — the borrowed-instruments brief (B2 → B1 → B3)

Source: `_BRIEF-borrowed-instruments-2026-08-12-v2.md`. Status at survey: RULED-TO-EXPLORE,
nothing enacted. Order is dependency-driven and MUST NOT be reordered: **B2 → B1 → B3** (B3's
grades need B1 as their refresh consumer — a grade with no re-checker is an instrument without a
consumer).

### Today (#172)
1. **Enact B2 — regenerated plan block** at lane seams (`_checkin.py --block`, six lines,
   GENERATE-NEVER-INHERIT). No Dave-gate blocks this. Opus sub builds; conductor verifies by
   RE-READING the emitted block against state, and runs both mutation tests (corrupt SOURCE mtime
   → reject; hand-edited block → detected).
2. **Put the five Dave-gates to Dave** (plain prose, recommendations attached) so B1/B3 unblock
   for the next passes: §5 fork (recommend **B-then-review**) · Tier-1 carve-out (recommend NO for
   now — narrowest surface) · gardener findings cap N (proposal 10) · queue cap Q (proposal 15) +
   pause rule · refresh cadence (recommend: rides the dream-pass, weekly-ish, no hard schedule).

### Next window
3. **Build B1 — gardener** (`knowledge/_gardener.py` + pinned-Opus lane), only AFTER caps/carve-out
   are ruled. All six hard fences are BLOCKS. Mutation tests (a)–(d) run before any live pass.
   First live pass files findings to `notes/_dream/` ONLY.

### After one full dream-pass cycle
4. **B3 — map grades**, per the fork as ruled. If B-then-review: sidecar `_MEMORY-GRADES.json` +
   the ★★/⛔ boot alert line (cost measured in real tokens before it's permanent), then the fork
   RETURNS to Dave with numbers. It is a deferral with a return date, not a disappearance.

### Dependencies
- B2 blocks nothing and is blocked by nothing → do first.
- B1 blocked by: cap N ruling, Tier-1 carve-out ruling.
- B3 blocked by: §5 fork ruling + B1 existing + one measured dream-pass cycle.

### Pitfalls (replayed, per the brief's register + standing law)
- **P-order:** building B3 before B1 mints ~90 unconsumed instruments. Strict order.
- **P-premise:** the brief was authored against #163 HEAD `f2e1409`; re-verify HEAD, byte counts,
  `notes/_dream/` listing before enacting. Premises age faster than rules.
- **P-write-scope:** gardener writes ANYWHERE but the proposals file = BLOCK, driven to a named
  refusal in a test harness before first live run — never inscribe a fence you didn't try to cross.
- **P-self-ruling:** conductor must not decide anything in §7's DO-NOT-RULE list. Sub briefs carry
  the DO-NOT-RULE list verbatim + the B2 block.
- **P-band:** if the boot alert line lands in the chain, its real-token cost is measured and
  declared — the boot band (56,158 ±849, s171-D1) is watched, not silently drifted.
- **P-green:** every new check must be shown ABLE to fail (mutation-test the clause, then drive
  the feature on real data).

---

## B. Tokens + atomic system → ready for component building (weekend / next week)

Ruled foundations already in place: ATOMISE (atoms → molecules → organisms per `meta.schema`,
Dave 2026-07-14) · Mono = the component library (#164) · three-axis model params·variants·slots
(113/114 rows enacted) · palette tier enacted #158 · four themes, test per theme.

### The blockers between here and "build a new component" (in order)
1. **tooltip.tip** — the last open three-axis row, already staged for Dave. Needs his ruling, then
   enactment. Small.
2. **The value-level aesthetic leg of the three-axis wave is UNSEEN** — Dave's-eye item. Build the
   live review page (specimens alive, full variant spread, light/dark + responsive) so the weekend
   session can start with a look, not a build.
3. **Base red 30** (`rag/text/on-dark`, #FFFFFF on #F6604C, 3.14:1) — the ONE base gating fail,
   unadjudicated. Two-red law + mono-error-ink precedents constrain the fix space. Dave rules.
4. **Component-scaffold path:** a thin `atoms-first` scaffold: pick component → resolve tokens
   (⛔ a token NAME is not an ADDRESS — resolve against the ledger, #108) → meta.schema entry →
   per-theme render-proof harness (`goto("file://…")`, never `set_content()`). This is the "wiring"
   deliverable: when it exists, a new component build starts from a green scaffold instead of
   archaeology.
5. **Readiness checklist generated, not asserted:** gates green on the token surfaces the new
   component touches; type-composite ratchet respected (debt may only shrink); DEF-005 grid gate.

### Sequencing
- This session: items 1–3 put to Dave (rulings) + scope the scaffold (item 4) into a sub brief.
- Next window (or a second window today, quota is cheap): Opus sub builds the scaffold + the
  aesthetic-leg review page.
- Weekend: Dave's-eye day — aesthetic leg, tooltip.tip readback, red 30 — then FIRST NEW COMPONENT
  through the scaffold as its live test.

### Pitfalls (replayed)
- **P-theme:** four themes means four proofs per surface; a single-theme green is not a green.
- **P-rolled-up:** building a molecule before its atoms recreates the debt ATOMISE exists to stop.
- **P-address:** `--pri-hover` class — a token name that resolves differently per theme; consult
  the fork ledger, never assume the name is the address.
- **P-render:** render sandbox is fresh EVERY session (~4 calls, price it); builds >45s wall get
  chunked `--range/--resume`.
- **P-scope:** the scaffold is wiring, not new design law — any new token/tier it seems to need
  goes to `_DS-IMPROVEMENTS.md`, promotion is Dave's.

---

## C. Dashboard — label everything Apollo vs Memento

Survey: `knowledge/_state.json` = 37 items (`W-*` worklist + `G*` provisional set), no
project/category field exists. `knowledge/gen_dashboard.py` → `dashboard/index.html`, generated
never hand-edited.

### Recommendation (mechanism)
Add **`project: "apollo" | "memento"`** to each of the 37 items in `_state.json`, plus a
**presence gate** so every NEW item must declare one (the brief's own law for added fields — and
the gate is driven to a named refusal on a plantable missing-field case before it counts).
Apollo/Memento is a judgment call, not derivable from existing fields — so storing it is
legitimate (the #165 "don't store derivables" rule does not bite). `gen_dashboard.py` then renders
the label as **text on every card + a filter/group control** — never hue alone (red/yellow are
problem hues; blue/green stable, but label with WORDS regardless).

### Proposed assignments (Dave skims, corrects by eye — shown on the rendered page, not as codes)
- **Apollo** (design system / product): W-0b encode-wave · W-0c build candidates · W-0d #67 wave ·
  W-01 ds-018 · W-02 dv-legend ceiling · W-03 ds-012(b) · W-04 DV-D16 · W-05 instrument-fit ·
  W-06 ds-016 · W-07 ds-017 · G9 ds-023 · G11 DS-018 · G12 tone-of-voice · G13b menu-search glyph ·
  G14 icon-button dark · G15 DV-D13 donut · G16 dataviz enactment call · G17 RAG status.
- **Memento** (process / instruments): W-08 still-owed set · W-09 delegation topology · W-10
  per-gate test plan · W-11 2c-roll deadlock · W-12 #57 dossier · W-13 /tmp runbook · W-14 Dave's
  founding principle · W-15 ledger §#59 · W-16 unhomed pair · G1–G8 · G10 · G18.
- Ambiguous, Dave calls: **W-14** (founding principle — filed Memento as process-law; could be
  Apollo-vision) · **G12** (tone-of-voice — filed Apollo as product voice; could be charter/process).

### Pitfalls (replayed)
- **P-joinkey:** the `#166` label strings in `_build_all.py` are JOIN KEYS — the new field touches
  `_state.json` only; `_build_all.py` untouched.
- **P-serializer:** round-trip `_state.json` byte-identical BEFORE writing; insertion is textual
  or asserted-equal on all untouched entries (the s171 splice-point lesson: valid JSON ≠ right
  location — entry count + prior-entries-compared-equal assert).
- **P-partialbuild:** do NOT run `_build_all.py` to "check" — regenerate the dashboard via its own
  generator only; the full-build verdict rides CI on push.
- **P-gate-consumer:** the presence gate must actually be RUN by something (wire into the gate
  suite that already runs) and driven to a refusal once, first-hand.
- **P-cap:** `_state.json` body 400ch cap is an open item (7/37 over) — this change must not
  worsen it; new field is short.

---

## Today's running order (#172), with the carried lane honoured
1. Dave rules the decision batch (below) — one message, plain prose.
2. Opus sub 1: **B2 plan block** build + mutation tests.
3. Opus sub 2: **dashboard project-label** build + presence gate + regenerated page, presented
   live for Dave's eye.
4. Conductor: scope the **component-scaffold sub brief** (lane B item 4) for the next window.
5. Carried lane "#172 verify the audit's downstream consumers": the day's pushes give CI the
   full-build verdict — read it back on the push receipt rather than spending a lane; declared,
   not dropped.
6. Wrap EARLY (stop line 150,929 FILL; wrap costs 42–49K; open by ~100–105K).

## The decision batch for Dave (everything above that is his)
1. §5 fork: A / B / **B-then-review (recommended)**.
2. Tier-1 carve-out: in or out (recommend OUT for now).
3. Gardener cap N (10 proposed) · queue cap Q (15 proposed) + the pause rule.
4. Refresh cadence (recommend: rides the dream-pass, no hard schedule).
5. Dashboard mechanism: `project` field + presence gate (recommended) — then skim the 37
   assignments on the rendered page.
6. tooltip.tip (staged) · base red 30 — can land weekend if today is full.
