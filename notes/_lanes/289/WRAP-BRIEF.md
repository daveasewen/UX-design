# #289 wrap brief — cut by the conductor (Fable 5.1) at Dave's "wrap", 2026-09-20

provenance: 289 · 2026-09-19 → 2026-09-20 (the session opened Saturday 19th and ran through Sunday 20th — a DATE SPLIT, the #241 shape: declare it, re-date nothing)
status: brief (every figure here is DECLARED; the wrap seat re-measures and publishes both readings where they differ)

## The session in one line

Dave supplied the deck's arc (his board), ruled the strand map, then wrote the story himself in seven beats on the car-plant analogy; the conductor ran homework lanes that dated the library build-out (32 → ~38 → 137; the 30 June / 7 July "robots" experiment), three deck recuts (v8 → v9 → v10, now 12 slides on his beats), two proposal pages, a decisions-and-comments overlay on every page he rules from, and seven line-drawn 3D illustrations in the gearbox idiom (books, brain ×6 passes, arm, line scene, callipers, open catalogue). Nothing inscribed; nothing committed until this wrap.

## Dave's words

ALL in `notes/_lanes/289/DAVE-RULINGS-2026-09-19.md` and `notes/_lanes/289/DAVE-RULINGS-2026-09-20.md` — quote, never paraphrase. His board is `notes/_lanes/289/DAVE-ARC-BOARD-2026-09-19.png`; his brain reference `notes/_lanes/289/illustration/DAVE-REF-brain-side-view.png`. Stock images he sent (top-view brain, four robot-arm wireframes) were NOT filed, by his word ("I wouldn't copy this in any way").

## What was built (all uncommitted, all in the tree)

- Decisions overlay: `notes/_lanes/289/decisions-overlay/inject.py` — injected into `notes/_STRAND-MAP-2026-09-19.html`, `notes/_lanes/288/T/template-quality-review.html`, `notes/_PROPOSAL-apollo-story-2026-09-19-v1.html`, `…-2026-09-20-v2.html`. Exports `DAVE-RULINGS-<date>-<page>.md`; he used it three times.
- Decks: `notes/_DEMO-SLIDES-apollo-2026-09-19-v8.html` (13 → 11 slides, superseded), `…-2026-09-20-v9.html` (12, his seven beats + gearbox/books/brain), `…-2026-09-20-v10.html` (12, + line scene on s5, callipers on s8, five-up anatomy on s10, strip cut to five) — **v10 is the working deck**. Renders in `notes/_lanes/289/deck/render-v9/`, `render-v10/`. Briefs `notes/_lanes/289/deck/BRIEF-*.md`; fragments `G1–G3.html` (G3's dropped KPI/scorecard/ask slides kept for a later deck).
- Proposals: `notes/_PROPOSAL-apollo-story-2026-09-19-v1.html` (conductor's outline, ruled on by Dave), `…-2026-09-20-v2.html` (his seven beats in his words; the plant-is-the-board table; the record dated). **v3 owed** — premise as beat zero, both framings (three roles / five constituents).
- Illustrations, `notes/_lanes/289/illustration/`: `books.html` (v1 curved spine kept as `books-v1.html`; straight edges now), `brain.html` (passes preserved as `brain-v1…v5.html`; v6 = traced reference, two mirrored hemispheres, full width; his word "good for now"), `arm.html`, `line.html` (two arms either side of a conveyor), `callipers.html`, `catalogue.html` (open book). Each with rest/orbit PNGs. Contact sheets `contact*.png`.
- Homework reports: `notes/_subreports/2026-09-19-289-H1-library-buildout-numbers.md`, `…-H2-library-buildout-story.md`, `2026-09-20-289-H3-agentic-loops-experiment.md`. Illustration reports `…-I1…I6-*.md`. Deck reports `…-D1-deck-v9.md`, `…-D2-deck-v10.md`. Deck lane reports `2026-09-19-289-G1…G3-deck-v8.md`.
- Ruled at the strand map (verbatim in the 09-19 file): the 25th is INTERNAL, "still very important" → Rice-grade rehearsal, internal room · "Do it" on strands 01–06 = By-Friday items only · index sharded by strand + age (conductor's option, his pick) · Can-wait list = Later.
- The library figure as he wants it said: 36 (Figma count, his word) → 137 = 125 components + 12 templates, on 8 foundations; 101 new; "we see this growing". Repo says 32 reviewed on 06-18 (H1) — publish both.
- The premise (his, 09-20): dev got fast; design became the bottleneck; "how do we speed up design?" was the first experiment. Beat zero, not yet in any page.
- The two framings (his, 09-20): visual metaphors as parts of the system (five: knowledge/books, proficiency/brain, parts/gears, tools/arm, process/line) AND the parts of the metaphor (three roles: inventory, assembly engineer, inspector). "No harm in exploring both … assets first." v10 carries both.

## Lanes — all `Agent`, depth 1, model opus, none in seat (declared sub tokens from the harness)

G1 78,761 · G2 89,550 · G3 79,757 · H1 92,862 · H2 121,782 · H3 144,365 · I1 brain p1 170,303 · I2 books 138,012 · brain p2 190,078 · brain p3 139,509 · books p2 79,291 · brain p4 175,900 · brain p5 208,874 · brain p6 119,767 · D1 v9 181,410 · I3 arm 167,467 · I4 line 171,600 · I5 callipers 165,135 · D2 v10 157,008 · I6 catalogue 142,331. Sum declared ≈ 2.81M (n=20). Publish `_checkin.read_fill` alongside — two definitions, both published.

## Gauge, declared

Conductor FILL not read at the seat (Dave: "you're getting hot" — the wrap was called on his read, not the gauge's). The wrap seat reads it. Boot: `_checkin.py` ran at the opener with `--no-block` (output not captured to a file — declare as unread). The seam's stop line stands; if FILL is past it, publish the overrun as #288 did.

## Declared by the conductor, carry forward verbatim

- `git checkout --` and `rm` are blocked on the mount ("Operation not permitted"): the strand map / template review were re-injected by regex strip instead; stray trial PNGs (`var-*.png` in illustration/, `crop.png` in outputs) could not be deleted — move to `_to_delete/289-strays/` with `mv`, never `rm`.
- Playwright/Chromium was installed in the sandbox per `chromium-in-sandbox-recipe` (needs `NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt` for the download this time — add to the recipe memory) and used for every render.
- Two files were dirty at open and are NOT this session's: `notes/_lanes/288/DAVE-RULINGS-2026-09-19.md` (+ lines after #288's commit), `notes/_REHEARSAL-LOG.jsonl`, `notes/_dream/_GRADE-DECISIONS.jsonl`, `knowledge/_graph-mark-observations.jsonl`, `_LIVE-STATE.md` (dream pass 13 committed `dcf17ade` at 2026-09-20 "Dave absent" — a scheduled fire landed mid-session; read its delta before writing ours).
- Deck lane flags not yet acted on: s4–s8 are five white cards in a row (rhythm flattened); callipers fill half their card; the gearbox scale bar rides into the s10 Parts cell; brain frame a hair heavier than the gearbox's.
- Illustration caveats: brain top/front views still narrower than a real brain (traced profile is tall); line scene's far arm can read as floating at yaw extremes; callipers jaws read wedge-like.

## Ruling-shaped, NOT inscribed (rulings stay at their count unless his word says "inscribe" — it did not, all session)

1. The seven beats in his words — the deck's copy. v10 carries them.
2. Three roles over five constituents at the top level — he agrees three is simpler, "the 5 explain more fully"; both explored, neither ruled.
3. The ask — "I need to work with my colleagues on this request"; draft slot stands.
4. The inventory slide should be an open book / "or maybe just a page from a catalogue with a grid of the parts, image description etc" — the page variant is OWED, first job of #290.
5. Research: another group's, Dave alongside, "definitely a problem we have to solve" — on the ask slide as owed.
6. Swiss taste-guarantee: still parked (#288).
7. Everything on `_HANDOFF-130…139` not closed. Strike NOTHING without a receipt. Closed today with receipts: the deck structure is GIVEN (his board + seven beats — #139's "wave 2 blocked on his structure" is unblocked); which Friday the 25th is — INTERNAL, his word 09-19.

## Owed to #290, in order

1. Catalogue PAGE illustration (flat sheet, grid of parts with image + description, gearbox idiom) → replaces books on v10 s6.
2. Proposal v3: premise as beat zero; both framings side by side; the seven beats; the record.
3. Deck v11: the D2 flags (rhythm, callipers scale, scale-bar strip), robots slide on dark, his slide-by-slide read of v10.
4. The week's plan from the strand map: Monday overview-dashboard definition + first cold one-shot; Thursday rehearsal; recorded fallback.
5. Index sharding (his pick) — not started.

## Ritual

Run `knowledge/_RUNBOOK-capture-ritual.md` in full, every step in order, as #288's W2 did (`notes/_subreports/2026-09-19-288-W2-wrap.md` is the model). Handoff `_HANDOFF-140-<slug>.md` outranks `_CHAIN.md`; it does NOT replace `_HANDOFF-130…139`. Declare the date split (#241 shape). Wrap-memory hook at `notes/_lanes/289/WRAP-MEMORY-HOOK.md`. Commit ONLY via `knowledge/_git_commit.sh`; then push, and read CI back into the report. Title for the next chat: `Apollo - #290: the story is his and the plant has seven drawings`.
