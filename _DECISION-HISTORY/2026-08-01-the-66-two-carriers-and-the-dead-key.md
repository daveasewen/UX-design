provenance: local_c5fcffa2-b38f-4181-bcef-0f0523b4a495 · 2026-08-01
status: observed

# #66 — Two carriers for one boot rule, and the key that was never wired

*Fable solo Cowork conductor + 4 Sonnet subs, Dave live all day (Sat). Ledger rows: § ★ #66
D1–D7. Commits `7246466 · bd79c6c · 82175fd · 768b508 · 383fe89 · 8ec89d9 · 9c8dda7` + wrap.*

## Arc 1 — Memento closes its #66 queue in the first hour

The voice pass owed since #63 discharged in one beat: the one-pager read back in six blocks,
Dave ruled it verbatim ("its good as is, i like it"). The interesting decision was downstream —
the dist zip no longer matched the tree, and Dave's "yea just version" was read (declared, not
laundered) as cut-v0.1.1-keep-v0.1, consistent with his standing version-don't-overwrite rule.

The Claude-plugin flavour then went from scoped to shipped inside the same morning because Dave
priced the risk himself: build now, before the colleague's Copilot verdict, accepting that a rule
proven wrong later gets corrected in two carriers (#66-D3's declared risk). The build's one real
finding: `_gen_chain.py` resolves its project as the script's grandparent directory
(`ROOT = dirname(HERE)`), so verbatim machinery cannot run from a plugin install dir — hence the
plugin's step-0 self-install of `machinery/` into the project, after which the two flavours are
byte-identical at runtime. Dave installed it and proved first-boot on his own machine within the
hour — the fastest UNPROVEN→PROVEN this project has recorded.

## Arc 2 — Apollo wakes: one ruling unlocked four moves

Dave picked the conductor's split: rule scatter geometry (his numbers, `--control`'s own
specification), sub the instrument fixes and the CTRL sweep, serve the radius tuner. Findings:

- The instrument fixes re-denominated the corpus: 78 findings → 30, and the survivors changed
  meaning — donut's phantom self-collisions were instrument noise; bar/combo's overruns survived
  the fix and are therefore REAL. The sub also corrected the record's own prescription
  ("compose getCTM()" is insufficient — screen-CTM inverse-multiply is the correct composition)
  and flagged it as a refinement rather than silently substituting. Replay held.
- The CTRL sweep's first run surfaced 8 genuine sub-24px targets — the gate paid for itself the
  hour it went loud. 553 selectors entered scope; unknown ARIA roles now fail by name.
- The `$?`-after-pipe trap bit the conductor twice in one session (proof "exit 1" that was the
  browser lib missing; gate "exit 0" that was tail's). Both caught by re-running unpiped.
  The lesson is already a memory ★; this session upgraded it from "known" to "still biting".

## Arc 3 — Dave's key-behaviour report, run to root

Dave reported the key-filtering "doesn't work" and described the correct interaction: text half
isolates, swatch toggles, invisible hit areas. Three-layer diagnosis, each proven:

1. The interaction he described IS the ruled model — DV-D11, his own 07-24 signoff
   (`reviews/LEGEND-ISOLATE-TOGGLE-PROTOTYPE-2026-07-24-v5.5.html`), implemented in
   `dv-legend.js` and PROVEN live standalone (isolate announce + 0.12 fade + checkbox toggle +
   44px ::before hit expander).
2. Scatter specifically was never wired: dead static `ul.dv-legend`, no registry subscription —
   and the migration gate certified the gap green by classifying a present static legend as
   "no legend" (matched-grep-≠-presence, now fixed with a total partition + loud finding;
   deliberately red on scatter until the migration enacts).
3. What Dave actually clicked was the review doc's iframes — which traverse `../` on `file://`,
   which Chrome blocks, which silently serves the JS-off fallback. The conductor had labelled
   that dead state "working key". A CLAIMED, caught by the person it was presented to.

The remedies became law the same hour: review pair mandatory, specimens copied same-directory
and tested in the review's own context (`_RUNBOOK-review-doc.md`, hard-lessons section).

## Arc 4 — Rulings by screenshot, and the two-register default

The review pack had radio buttons but no export — Dave screenshotted his selections. The gap was
owned and inscribed. His rulings: A2 permanent in the STRICT form (every member declares,
absence fails loud — supersedes the universal default he originally pencilled), sparkline sheds
its 16,661 B inert block, scatter's key connects, dv-lockup shape approved. All four deliberately
UNENACTED: D1 changes `gen_component_partials.py` semantics, so the wave runs D1→D2→D3 at #67
with fresh room, D4 scoped after. Separately he ruled the two-register review default (plain
prose first, `<details>` fold) — canon `_RUNBOOK-review-doc.md`, exemplar the v2 pack.

## Dead ends and corrections

- Hand-rolled a `git add` once mid-session and hit the index lock — `_git_commit.sh` exists for
  exactly this; used it for all seven commits after.
- The single-series scatter screenshot appeared half-empty — animation caught mid-sweep, not
  data loss; verified numerically against the file rather than re-shooting.
- The review doc's "click a key row — it dims" instruction was asserted from standalone testing,
  not tested in the doc's own context. See Arc 3; now impossible to repeat legally.

## Resolved state · still open

Resolved: Memento #66 queue (voice pass · v0.1.1 · plugin, first-boot proven) · scatter geometry
×3 rulings enacted+green · instrument fixes (corpus 30, trustworthy) · CTRL sweep live ·
legend gate loud · two-register default canon.
Open: the #67 enact wave (D1→D2→D3 + D4 scoping) · render-triage 30 + a11y 8 (Dave's, on
trustworthy instruments now) · colleague's Copilot verdict · plugin's second tester · CI
full-green glance · radius tuner numbers (served again, no verdict) · memento v0.2 gate
extraction (floated, price-before-start).
