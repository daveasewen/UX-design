# 2026-07-20 — Pre-flight for the Mono alignment sweep (why we did NOT sweep)

*Solo / self-conductor. Opened as a good-morning; became a pre-flight + record-repair session that
deliberately produced **zero canon edits**. Spine line: `_LIVE-STATE.md` LATEST DELTA (evening 3).
Both-way links: `knowledge/_STYLE-PROVENANCE.md` §A-AUTH (the WHAT), this file (the WHY/HOW).*

## The arc

**Opened to run the Mono alignment sweep** (39 `align` items → Mono values, regen `_review`, flip the
theme-provenance gate to blocking). Dave's steer changed the shape: *"there was a lot of context rot on
the last session, be careful, I don't want to lose anything."* → treat it as a pre-flight, not a charge.

**Finding 1 — nothing was lost, but I had to prove it.** The GOOD-MORNING COMMIT STATE was itself stale
(it pointed at `a1b9fbb` as unpushed; in fact three later commits — `8373a97`, `4e5b1b6`, `3abe167` —
were already pushed and the 88-component rulings were *complete*). Reconciled the tally to 88 across
three durable sources: the decisions JSON (21 clustered verdicts), the generator's `SINGLETON_RULINGS`
dict (20 singletons), and the counts block. `align = 39` = 27 snippets + 1 `_review` (reconciled
tab/stepper) + 11 `_proforma`.

**Finding 2 — the real rot: a stale list inside the durable record.** `_STYLE-PROVENANCE.md`'s mid-doc
"backlog A (19 snippets)" predated round 3. It named Hero / Navigations / Progress-tracker / Tabs as
align targets — all four were *archived* in round 3 — and listed Notifications, which is *keep-legacy*
(its `#A8000B` is correct Legacy red). A sweep run from that paragraph would have wrongly re-homed five
components and destroyed the one legacy reference. Fix: marked it superseded (struck-through, kept for
audit), wrote **§A-AUTH** as the authoritative worklist, and pointed it at the generator as machine
source of truth. One file changed; build stayed green 37/37.

**Finding 3 — teal→green is not a find/replace, so it waited.** Inspected every `#00847F`: two roles —
a `--s` success-colour var and the `#i-success` SVG (filled circle + **white** tick). The Mono target is
`rag/success-glyph #4A9568` (dark), ideally *tokenised* not hardcoded. But the white tick trips
**type26-013** (white type is red-only) — it likely should be **black**, like `on-success`. That's a
ruling-shaped sub-decision, not a mechanical swap. Judgment call: don't rush a canon edit at the tail of
a nervous, soon-to-close session — hand it to the fresh Sonnet session as a turnkey brief instead.

**What I got wrong (Dave caught both).** (1) Misdiagnosed the git lock as "GitHub Desktop is open" — it
was the sandbox **delete-guard** leaving a 0-byte `index.lock` after my own `git status`/`git add`; the
`_RUNBOOK-git-commit.md` clear-with-`mv` procedure exists precisely for this and I improvised instead.
(2) Improvised the handoff from memory hooks rather than running `_RUNBOOK-capture-ritual.md`. Both are
the same failure — reconstructing a *procedure* from memory instead of reading its runbook. Corrected:
re-read both runbooks and ran them by the book. New feedback memory: `feedback-read-the-runbook`.

## Resolved state / still open

- **LANDED:** record de-risked (§A-AUTH), handoff + this dossier written, `_LIVE-STATE` restamped. No
  canon/token/component change. Build green 37/37.
- **OPEN → fresh Sonnet session (turnkey brief in GOOD-MORNING §C):** teal→green on Masthead + T2–9
  (with the tick-colour sub-decision ruled first); grey inks via the grey-tint check; regen `_review`;
  all red (`rag/error`, `tabs/active`, `progress/complete`) held for a live tuner; then gate → blocking.
