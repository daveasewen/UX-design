# Good morning, Dave ☕

*Briefing — written end of 2026-07-17, session **"Tranche 8 + reconciliation + icon normalisation."***
*Read: **§A Orientation** (skip if you're already in context) → **§B This session** → **§C Queue**.*
*Then `_LIVE-STATE.md` (the live/dead/open ledger) → the decision files it points to.*

---

# §A · ORIENTATION — the whole project in one page
*(Standing section, kept in every handoff from 2026-07-17 on, at Dave's request: "orientate a new starter —
wider context helps." Update it when the shape of the project changes, not every session.)*

## What Apollo is
A **governed design-system engine** for agentic UI generation. The bet: *generation is a commodity* — the value
is the layer around any generator. Two principles run through everything:
- **Retrieval, not recall.** Brand values are retrieved from token stores, so generated work can't drift off-brand.
- **Verification = enforcement.** Judgment is encoded as **blocking gates**; "done" is withheld until they pass.
  If a rule isn't gated, assume it will be broken (proved repeatedly — see §C).

Tagline: **"lovable on rails."** Four product phases: **Discover** (ingest/research) → **Create** (generation —
what's being built now) → **Craft** (review/edit — the review-overlay docs ARE this) → **Dispatch** (handoff to eng).

## The three libraries = ONE skeleton, three modes
Not three codebases. One component skeleton; **modes are token-override sets**. Adding a library = adding a mode,
**never forking components**. Radius is the worked example (`--radius:0` in mono; UI/SC override it).
- **Apollo mono** — the monochrome base (square, near-black primary, colour = meaning only). *"Pro-forma" is just
  a descriptive name for Apollo mono — same thing* (Dave 2026-07-17; the split caused a real duplication bug).
- **Apollo UI** — the new branded HSBC library (rounding returns, red returns as primary accent).
- **Apollo SC** — Supercharge, the prior branded work ("keep the ideas, don't copy the solutions").

## Where things live
```
knowledge/            THE ENGINE
  tokens/             DTCG token stores (typography, spacing, semantic-colour…) — the retrieval source
  snippets/           38 gated reference components = CANON (the promoted, reviewed set)
  components/*.meta.json   per-component CRITERIA (token bindings, contrast pairs, ARIA, states, anti-patterns)
  canon/              canon.css (GENERATED from snippets — never hand-retype) + type.css (type composites)
  _proforma/          Apollo mono tranches T1–T8 + Masthead + DataViz  ← the in-flight build surface
  _review/            review-overlay copies (+ _make_review.py). Gates never scan here.
  _validate_*.py      the gates; orchestrated by _build_all.py
  _RUNBOOK-*.md       the method written down, so a cold agent can operate the engine
reviews/              consumable outputs: ITINERARY (the 124-item plan) · NAV-PATTERN-CATALOG · REVIEW-* · PLAN-*
_LIVE-STATE.md        what's LIVE / DEAD / OPEN — read this second, always
MODEL-ROUTING.md      which model for which work
```

## The one command that matters
```
python3 knowledge/_build_all.py     # 26 steps, all gates, exits non-zero on any failure
```
That is the single command to trust the KB. Gates in force: a11y · contrast · state-contrast · icon-source ·
coverage · integrity · **DEF-003** no-JS-motion · **DEF-004** no-hardcoded-styling · **DEF-005** 4px grid ·
pro-forma universal · DataViz.

## Rules that actually bite
- **Survey before build** — grep `snippets/` + `components/*.meta.json` + existing tranches BEFORE building
  anything; declare *mining* vs *building fresh*. (Skipping this duplicated Tab-bar + Stepper in T8.)
- **Type composites are mandatory** — all component text uses `type.css` composites (`.t-cm-*` single-line,
  `.t-ed-*` wrapping), never raw font shorthand. *(Currently aspirational — see the retrofit in §C.)*
- **Icons: real assets only** — every glyph maps to a real file in `assets/icons/` + the manifest. Never invent;
  provisional glyphs must be flagged and logged. **Filenames are not trustworthy** — render-verify before binding
  (several are mislabelled/inverted — see `knowledge/_ICON-GAPS.md`).
- **4px grid** everywhere (DEF-005). **Sentence case** everywhere. **Square corners** in mono (roundels — badges,
  avatars, dots — are the carve-out). **Red = primary-action accent, once per screen** (brand modes only).
- **ATOMISE** — build at the true atomic level and compose up.
- **Derivation governance** — the engine never derives-and-promotes. **Promotion to canon is Dave's alone.**
  DS errors get logged (`_ICON-GAPS.md` / `_DS-IMPROVEMENTS.md`) and we move on.

## How we work
- **Review loop:** every doc/component ships as a **clean source + a REVIEW copy** (`_make_review.py <file>`).
  Dave comments via the overlay and exports a numbered edit-prompt. **Edits always apply to the clean source;
  the review copy is regenerated, never hand-edited.**
- **Dave commits via GitHub Desktop.** Hand him ONE paste-ready commit; don't commit from the sandbox
  (`.git` lock contention). Keep Desktop closed during any terminal git work.
- **Comms:** exec summary + numbered next steps first, detail below (Dave is dyslexic and time-poor).
- **Renders:** in-sandbox Playwright works (recipe in memory `sandbox-html-rendering` — needs
  `NODE_TLS_REJECT_UNAUTHORIZED=0` + non-root libs). No Univers font in-sandbox, so renders verify **layout,
  not brand type**. HTML is what Dave reviews; PNGs are the agent's own check.
- **Known external blocker:** the create.hsbc **webfont licence** needs renewing — not Dave's to action.

---

# §B · THIS SESSION (2026-07-17, long)

**Tranche 8 built + gated** — BottomTabBar (classic + the Neo-net floating pill), InPageNav, FooterNav,
RelatedLinks, journey Stepper. Full build green; 13 new real icons wired.

**Then a significant find:** T8 **duplicated components that already existed** — `Tab-bar.reference.html`
(with both a standard bar AND the pills variant) and the circular Stepper inside Tranche-1. Nothing was lost in
the cloud→folder migration (every cloud Artifact is in the repo, and the repo is ahead); the cause was **not
surveying `snippets/` before building.** Root-caused, rules saved, and it motivated the whole enforcement queue.

**Reconciled candidates built** (non-destructive, in `knowledge/_review/`, nothing overwritten):
`Reconciled-tab-and-stepper-2026-07-17.html` + its REVIEW copy — Stepper (T1 circular + collapse, made
interactive per T8) and Tab bar (canon line→filled swap + sliding pill, Neo-net aesthetic, independent AI island).
**Two review rounds applied** (9 edits total), all gates green.

**Icon source library normalised to 18×18** (Dave ruled: fix at source). 69 off-canvas files — 53 lossless
viewBox retags, 16 scale-to-fit wrappers preserving path data byte-intact; 6 deliberate non-square marks left
alone. Library now 652 × 18×18. Build green 26/26, before/after renders identical.

**Asset defects logged** in `knowledge/_ICON-GAPS.md`: `social-facebook.svg` is an *Instagram* glyph,
`social-youtube.svg` is *WhatsApp* (use the `-2` variants), and the `payment` `-active` pair is **inverted**
(`payment-active.svg` is the OUTLINE). Caught only by render-verifying — gates check the file exists, not what's in it.

**Library audit:** **44 components** built for Apollo mono (T1–T8 = 42, + Masthead, + DataViz kit). Only
**one is off-plan — the Masthead** (no row in the 124-item itinerary; decide whether it's its own row or folds
under Header). Coverage ≈ 40/124, approximate.

---

# §C · QUEUE (numbered, actionable)

1. **Dave's Tranche 8 comments** — he has them ready; they were deferred to today.
2. **TYPE RETROFIT — the big one, and a genuine gap.** Measured yesterday: **0 of 50** component files use a
   type composite; **0** link `type.css`; raw font decls everywhere (canon.css 113, T8 43, T1 25, T6 23).
   Type was *promoted* but the library was never *rebound* to it. Scope ≈ the grid retrofit. **Edit the snippets
   and regenerate canon.css — never hand-retype.** Then gate it (`_validate_type_composites.py`). Full spec in
   `_LIVE-STATE.md`. **Needs a fresh session — don't start this at a session tail.**
3. **Component index + duplicate-guard** — auto-generated "what exists" table (status/variants/path) read at
   cold-start, plus a blocking gate refusing a new component whose name/pattern already exists without an
   explicit reconcile/supersede. This is the fix for the T8 duplication; the audit in §B took a script plus
   manual disambiguation and *still* isn't exact — that's the argument for it.
4. **Icon 4px render-scale** — sanctioned scale **12/16/20/24/32/36/40/44**, tie the icon box to the type
   grid-slot, gate it, retrofit ~50 off-grid usages. (Prerequisite — the 18×18 source normalisation — is DONE.)
5. **Reconciled candidates: rule where they land** — promote into canon/`_proforma` and retire the duplicates,
   or leave as candidates. Promotion is your call.
6. **Rule-16 docs for T8** (Swiss dossier + KB model doc) — deliberately not assumed.
7. **DataViz** — still 🟡 parked, needs your in-browser pass.

> **UNCOMMITTED — a lot.** Tranche-8 + review copy · both reconciled candidates + review copies · **69 normalised
> icon assets** · `_ICON-GAPS.md` · `_LIVE-STATE.md` · GOOD-MORNING. Review the icon diff with
> `git diff --stat knowledge/assets/icons/`. A paste-ready commit message is in the last chat message.

> Opener: **"Title this chat: Type retrofit — bind the library to the ramp."**
