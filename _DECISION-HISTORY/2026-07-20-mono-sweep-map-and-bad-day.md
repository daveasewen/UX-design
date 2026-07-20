# 2026-07-20 (evening 4) — the precise Mono teal→green sweep map, and a bad-day failure lesson

*Dated from `date` (2026-07-20 22:26 BST). This session opened as a good-morning and was meant to run
the teal→green Mono sweep. It did NOT: I flailed, Dave corrected me repeatedly, and we agreed to capture
and go fresh. **Zero files were edited — clean tree, HEAD `dc41468`.** Two things are worth keeping: the
precise, verified sweep map (so the next session executes in one pass), and the failure-mode lesson.
Both-way link: spine = `GOOD-MORNING.md` §C·1; the architecture it rests on = `GOOD-MORNING.md` §A +
`tokens/themes/_themes.json` + `_STYLE-PROVENANCE.md`.*

---

## The failure arc — why the day went west (the WHY, for a cold reader)

Opened good-morning, read the handoff (it was correct), picked the teal→green sweep. Then Dave showed a
tuner screenshot with green `#6AB887` and said "pretty sure this was the decision." Instead of anchoring
on the **spine** (the token store = Apollo Mono base) I started **mining the decision prose** for the
"real" green, and surfaced three competing values:

- `#6AB887` — R-D13 "healthy" status *fill*. Ruled on a tuner but **never promoted to a token**. Dead/superseded.
- `#2B7E4F` / `#4A9568` — `rag/success-glyph` (and the bare `rag/success` role tracks it). **In the token store.**
- `#5DAC7B` / `#43AD6F` — `rag/success-background`. **In the token store.**

I treated these as competing authorities and kept re-deriving the architecture from fragments. Dave had
to restate it repeatedly. **Root cause: recall over retrieval.** The ingested-Legacy decision docs carry
competing and dead values (the ingest tokenisation is "rubbish", Dave's word); reading them as authority
is the trap. The spine — the DTCG token store, resolved under the active theme — is the single source of
truth. "Retrieval, not recall" (GOOD-MORNING §A) is exactly the rule I broke.

**The corrected frame (Dave, reaffirmed several times — it was already in GOOD-MORNING §A):**
- Origin: we **ingested Apollo Legacy** (the Figma common library) to seed tokens; that tokenisation is rubbish.
- We are building a **new architecture: Apollo Mono is the base — the spine. The semantic tokens ARE Mono.**
- Legacy / Console / Supercharge are **override sets** stacked on the spine. Nothing hardcodes a theme colour;
  components **bind a semantic role**, the active theme's override decides the hex.
- Roadmap: **normalise to Mono → build out the 124 components → then style the other three themes.**
  The teal→green sweep is a slice of "normalise to Mono."

---

## THE SWEEP MAP — verified, ready to execute (the WHAT + HOW)

**Scope:** 9 `_proforma` files — `Masthead-interactive` + `Tranche-2…9`. **Tranche-1 has no teal.**
Source of truth for the drift = the theme-provenance gate report `knowledge/_THEME-PROVENANCE-GATE.md`
(teal `#00847F` counts: T2/T3/T4/T5 = 3 each; T6/T7/T8/T9/Masthead = 2 each).

**The 9 files are NOT uniform** (a blind find-replace would be wrong — this is the session's real find):

### Change 1 — the `--success` vars (ALL 9 files, both theme blocks)
In the `[data-theme="light"]` block (≈ line 23) and `[data-theme="dark"]` block (≈ line 30):
- `--success:#00847F` → light **`#2B7E4F`**, dark **`#4A9568`**  (= `rag/success`, R-D18 Mono green)
- `--success-t:#E5F2F2` (light) → **`#DCEDE3`**;  `--success-t:#001615` (dark) → **`#12291D`**  (= `rag/success-tint`)

### Change 2 — the `#i-success` symbol (ONLY Tranche-2, 3, 4, 5)
These four still hardcode the badge:
`<circle cx="9" cy="9" r="9" fill="#00847F"/> <path d="M7.21594 13.553…Z" fill="white"/>`
**Migrate to the pattern the newer files already use** (Tranche-6/7/8/9/Masthead) — identical path, tokenised fills:
`<circle cx="9" cy="9" r="9" fill="currentColor"/> <path d="M7.21594 13.553…Z" style="fill:var(--mark)"/>`
→ Tranche-6/7/8/9/Masthead need **no symbol change** (already migrated).

### The mechanism (so the migration is understood, not copied blind)
From Tranche-6 CSS: `.f-msg.is-ok .f-dot{ color:var(--success); --mark:var(--page); }`
The dot's **circle = `currentColor` = `--success`** (green); the **tick = `--mark` = `--page`** (knocks
to the page colour, so light = white tick, dark = `#1A1A1A` tick). No hardcoded ink; the tick is a
theme-following knock-out. This is the small-dot realisation of the RAG roundel behaviour.

### OPEN sub-decision for the executor (don't blind-pick)
Dark `--success`: **green `#4A9568`** (small-dot treatment — matches the aligned `snippets/Status-indicator`,
whose dark `--success` is `#4A9568`) **vs. white `#FFFFFF`** (the big-roundel policy from
`snippets/Confirmation`, where a large confirmation roundel flips white with a knock-out tick).
The `.f-dot` here is a **small inline status dot**, so the recommendation is **green `#4A9568`** (as above),
NOT the white flip. Eyeball once against Status-indicator before committing; it's a one-line call.

### HELD — do NOT touch in this sweep
All reds (`--err`, `#A8000B`, `#DB0011`), `--warn` (`#FFBB33` + its `#333`/`--mark` marks), `--info` (navy):
error/warning/information are the **held RAG set** (R-D17), awaiting the red tuner. Also owed Mono values:
`tabs/active` + `progress/complete` (R-D19). Leave every one.

### After the edits
1. Regenerate the `_review` copies via `_make_review.py` (derivative — never hand-edit).
2. Run `python3 knowledge/_build_all.py` — expect green; the theme-provenance gate teal count in the swept
   files should go **2–3 → 0**.
3. This is Sonnet-tier mechanical work once the map is in hand.

---

## SPINE DRIFT FLAGS — separate from the sweep (for the token/spine session, NOT the component sweep)

- **`text/on-success` = `#000000` aliased to `color/black`** — a non-Mono primitive (ingest cruft). Apollo
  Mono ink is **digital black `color/mono/4` = `#1A1A1A`**; every other Mono ink aliases `color/mono/*`.
  Should be corrected to alias `color/mono/4`. **Does NOT block the sweep** — the roundel uses `--mark=--page`,
  not `on-success`. A spine tidy to do with the red/spine work.
- **`#6AB887` (R-D13 "healthy" fill) was ruled but never tokenised** and competes with the tokenised
  `rag/success` family. It is **superseded/dead** — the token store wins. Consider tombstoning the R-D13
  healthy-green prose so it stops confusing readers (it confused this session).

---

## THE LESSON (durable)

**Trust the spine, don't mine the prose.** The token store (DTCG, resolved under the active theme = Apollo
Mono base) is the single source of truth. The ingested-Legacy decision docs carry competing and dead values;
reading them as authority is how this day went west. Retrieval, not recall — applied to the one session that
forgot it. Mirrored to `GOOD-MORNING.md` §A rules + memory `feedback-trust-the-spine-not-the-prose`.
