# `#220`-readings-capsule — three readings of Dave's capsule-chord correction

session: `#220` · 2026-08-27
window: bento lane — the parked capsule correction
sub index: `readings-capsule`
brief: `notes/_briefs/2026-08-27-220-readings-capsule-correction.md`
tokens: `UNMEASURED` — a sub cannot read its own `message.usage`; the conductor's panel is the
only place this spend is real.

## VERDICT

**DONE.** `reviews/CORRECTION-READINGS-2026-08-27-v1.html` is built, live, console theme, with
all three conductor-defined readings rendered **light and dark side by side** — 9 dial-sets × 2
modes = **18 live specimens**, every one of them the artefact's own `.br-spec` / `.bm-stage`
markup and stylesheet copied out of `showroom/_foundations/bento-rails.html`, with only the dials
changed. Nothing was enacted: my only repo write is the deliverable plus this report and its
evidence directory. Render-verified in-sandbox at **1180 and 480**, with the canvas font probe
green against **both** controls.

The page turned up more than it was asked to. Measuring the specimens rather than looking at them
found **the same defect Dave rejected, live and shipping today, in a chord member none of the
three readings removes** — the dark-grey capsule caption, in console dark, resolves to exactly
the page ground behind it. And the structural reason all of these got through is that **no rule
anywhere compares a caption's ground to the ground behind it**; the ruled 4.5:1 floor governs
*ink on its ground*, never *ground on ground*. Those findings are on the page in plain prose and
are the sharpest input to whichever reading Dave picks.

COUNTS: findings `9` · ruling-shaped `6` · UNPROVEN `3`

## What was done

**Region 1 — `reviews/CORRECTION-READINGS-2026-08-27-v1.html`** (56,854 bytes, new, `-v1`).

Page order: the BEFORE (the rejected card, live, with Dave's words verbatim) → Reading A →
Reading B → Reading C → *What the pixels say* (the measured findings) → *Where the three
disagree* (comparison table) → *Not decided here* (the mono line) → footer (the enactment site).

| Section | Dial-sets | Specimens |
|---|---|---|
| BEFORE — the rejected card | capsule · cap white · page `page` | 2 |
| A — white leaves the ramp | capsule/grey · capsule/darkgrey · corners/transparent | 6 |
| B — white is fenced | capsule/white on `grey` (legal) · capsule/white on `page` (refused) | 4 |
| C — the tile re-forms | capsule/grey · corners/transparent · **capsule/transparent** (the shape that would never exist) | 6 |

Method, as briefed: the specimen markup is the rejected card's own `<figure>` lifted verbatim
from `showroom/_foundations/bento-rails.html:806-807`, the same real photograph
(`eyeem-100014108-180570836-w1600.jpg`) with its real alt text and licence line on every
specimen, and the specimen CSS copied between explicit `COPIED-FROM-ARTEFACT START/END` markers.
Canon does the rest — the page links `knowledge/canon/canon.css`, so the bento container, grid,
role rules and the ruled 86px gallery caption space come from canon, not from a re-drawing.

**One deliberate markup change, declared:** the artefact carries `data-apollo-theme="console"` on
`.br-spec` itself and `data-theme` on `<body>`. To stand light and dark side by side on one page
the theme attribute is lifted one level up — `.rd-panel[data-apollo-theme="console"]` wrapping
`.rd-panel-bd[data-theme="light|dark"]` wrapping the untouched `.br-spec`. This is **required**,
not cosmetic: canon's console dark selector is
`[data-apollo-theme="console"] [data-theme="dark"]` (canon.css:22210-22211) — console must be the
ancestor and dark the descendant. Leaving `data-apollo-theme` on `.br-spec` inside a dark panel
would re-declare console **light** tokens on that element and silently kill dark mode. It also
puts the `--bm-*` substitutions on a *child* of the themed element, which is the arrangement the
artefact's own measured note (bento-rails.html:49-54) calls deterministic.

**Region 2 — this report** and `notes/_subreports/assets/2026-08-27-220-readings-capsule/`.

**Generator named, per the brief.** No repo generator was run. The page was emitted by
`/var/tmp/rd220/build.py` — **(NON-REPO: sandbox-local `/var/tmp/rd220/`, `s191-D2`)** — which
writes **exactly one path**, `reviews/CORRECTION-READINGS-2026-08-27-v1.html`. Its source is
banked as `assets/…/build.py.txt` because the sandbox does not survive the window.
`_capture_gate.py --selftest` was **not** run.

**Fence honoured.** `_bento_edit_rails.json`, every generator, every showroom page,
`_rulings.json`, `_state.json`, memory and git were all left alone. `git status` at hand-off
shows my deliverable as the only `??` I put there.

## Findings

1. **THE BIG ONE — the rejected picture is already shipping, in a member none of the three
   readings removes.** In console **dark**, the dark-grey caption ground and the page ground
   behind it both resolve `rgb(26,26,26)` — *identical*. The capsule therefore draws no edge at
   all: rounded on top, cut off square at the bottom, caption floating. That is the exact picture
   Dave rejected, in a **ruled** chord member (`s219-D3(3)` chord one), on the rails page today.
   Probe: `assets/…/measured-grounds-1180.txt`, the "dark grey" / mode `Dark` row
   (`capBg rgb(26,26,26)` vs `pageBg rgb(26,26,26)`). Seen:
   `assets/…/finding-1-darkgrey-vanishes-in-dark.png`.

2. **Reading B's verdict flips between light and dark.** In console dark, `white`
   (`--surface-raised`) and `lightest grey` (`--surface-subtle`) **both** resolve `rgb(31,31,31)`.
   So B's own legal case — a white caption over a grey page ground — is fine in light and
   **broken in dark**, while the pairing B refuses is broken in light and **fine in dark**. B is
   therefore not one rule per pairing; it is one rule per pairing *per mode*. Probe: the
   "over a grey page ground" rows. Seen: `assets/…/finding-2-reading-B-flips-in-dark.png`.

3. **The rejected card is not broken in dark.** Its caption resolves `rgb(31,31,31)` against a
   `rgb(26,26,26)` page and the capsule reads normally. The defect Dave saw is **light-mode
   only** for that member — which bears directly on whether an unconditional removal (Reading A)
   is the right shape. Seen: `assets/…/before-the-rejected-card.png`.

4. **THE STRUCTURAL CAUSE — nothing in the system compares a ground to the ground behind it.**
   The ruled floor (`s219-D3(2)`, X4: *"every ground on offer has to be readable, anything under
   4.5:1 is not offered"*) is `$ink_rule.floor: 4.5` in `_bento_edit_rails.json` and it gates
   **ink against its own ground**. Ground-against-ground has no floor, no gate and no rule. That
   is the single condition under which all three collisions in findings 1-3 are legal. Probe:
   `_bento_edit_rails.json` → `constraints.$ink_rule`.

5. **The fence that should have caught this card is structurally inert for these chords.** X1
   (from P2) is, verbatim in the manifest, `"capBg may not equal bentoBg unless it is
   transparent"`. Every console-gallery default sets `bentoBg: transparent`, so X1 has nothing to
   compare against and can never fire on a chord specimen. It is not that X1 was wrong about this
   card — X1 cannot see it. Probe: `_bento_edit_rails.json` → `legality[0]`, and
   `defaults`/gallery/console `bentoBg`.

6. **Read strictly, Reading C does not refuse the card Dave rejected.** C's condition is
   *"if there is no background colour on the caption"*. The rejected caption has one — white — so
   the condition never fires, and capsule + white on a white page stays legal and stays broken. C
   only catches it if *"no background colour"* is read as *"no ground you can actually see"*.
   This is on the page, in prose, in its own note.

7. **Reading C's "cohesive capsule" has no machinery today.** A gallery tile deliberately paints
   no ground (`bento-rails.html:457-466`, `.bm-gtile{background:transparent}`, with a MEASURED
   note explaining why). So a genuinely ground-less caption clipped inside a *filled* capsule
   cannot be expressed with today's dials: what renders as a cohesive capsule **is** a caption
   ground. The specimen on the page is the honest one (capsule + lightest grey) and the gap is
   surfaced as question 5 below rather than papered over.

8. **The approved artefact uses a type composite that does not exist.** `bento-rails.html` sets
   `class="t-ed-heading-5"` on every chord card's `<h4>`; `grep -c "t-ed-heading-5"
   knowledge/canon/type.css` → **0**. The real set tops out at `.t-ed-heading-4`. Those headings
   are falling back to UA defaults on the live Foundations page. Not mine to fix, not touched —
   my page uses `.t-ed-heading-4`.

9. **Concurrency note, not a defect.** `knowledge/_render/_bento_edit_rails.json` carries an
   mtime inside my window (a sibling `#220` lane), but is **absent from `git status`** — it was
   regenerated to byte-identical content, not edited. Flagged because my brief names it
   DO-NOT-TOUCH and I want it on record that I did not touch it. Other in-window modifications
   (`_graph-mark-observations.jsonl`, `_REHEARSAL-LOG.jsonl`, `_GRADE-DECISIONS.jsonl`,
   `notes/_briefs/*`, `notes/_subreports/2026-08-27-220-charts-sparkline.md`) are sibling lanes'.

## RULING-SHAPED QUESTIONS

*(All six are Dave's. Nothing below is decided, and the page states in its own footer that
nothing on it is enacted.)*

1. **Which reading is the correction?** (a) A — white leaves the capsule's list of caption
   grounds, unconditionally. (b) B — white stays and is refused only where the ground behind is
   white or the page. (c) C — a ground-less caption re-forms the tile into one of exactly two
   shapes. All three are drawn live on the page; this is the question it exists to ask, and
   findings 1-4 are the input I would want him to have before answering. **No recommendation
   offered** — the brief's whole point is that we never build the likeliest reading.

2. **What does "no background colour on the caption" mean?** (a) No ground token set —
   `capBg: transparent`. (b) No ground you can actually *see*, whatever token is set. This single
   word decides whether Reading C refuses the card that prompted it (finding 6) or leaves it
   standing. It is the cheapest question on this list and the one that changes the most.

3. **Is the rule per pairing, or per pairing per mode?** Finding 2 shows B's verdict flipping
   between light and dark. (a) Evaluate per mode — honest, and doubles the legality table.
   (b) Refuse a pairing if it collides in *either* mode — one table, stricter, and it would take
   white off grey pages that look perfectly good in light.

4. **Does the dark-grey-on-dark-page collision (finding 1) get fixed by this ruling, or is it a
   separate defect?** (a) Same ruling — whichever reading wins is written about *grounds
   colliding*, and it sweeps all three cases. (b) Separate — this correction is about white, and
   the dark-grey case gets its own pass. ⚠ Under (b), Reading A ships a chord in which the
   surviving dark member is broken in dark mode.

5. **Does Reading C's "cohesive capsule" need the TILE to paint a ground?** (a) Yes — new
   machinery: the gallery tile takes a ground, and the caption inside it genuinely has none.
   That reverses a MEASURED decision (finding 7) and would change what the legality rule compares
   against. (b) No — today's caption-ground rendering *is* the cohesive capsule, and C is only
   about which of the two shapes is allowed. (b) is far cheaper; (a) is closer to the literal
   words "cohesive capsule".

6. **Should X1 be repaired regardless of which reading wins?** It cannot fire on any console
   gallery chord (finding 5). (a) Repair it to compare against the *effective* ground —
   caption, then wall, then page — which is Reading B's machinery arriving anyway. (b) Leave it;
   the winning reading supersedes it. ⚠ Under (b) a proposed rule stays on the rails page reading
   as a live fence while being structurally inert.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN:** this sub's own token spend — a sub cannot read `message.usage`. Price to prove:
  the conductor's panel, ~0 tk.
- **UNPROVEN:** whether the same ground-on-ground collisions occur in **mono, legacy and
  supercharge**. Only **console** was measured, because the brief scoped the page to console and
  the chords are console-scoped by `s219-D3(3)`. Given finding 4 (no rule governs ground vs
  ground anywhere), I would expect collisions elsewhere. Price to prove: one render pass over the
  4 themes × 2 modes × 4 caption grounds × 3 page grounds — ~96 measured pairs, one script,
  ~8-10K tk.
- **UNPROVEN:** the page in a **real browser on Dave's Mac**. It is verified in the sandbox
  headless shell at 1180 and 480 only. Price to prove: the runbook's Claude-in-Chrome fallback,
  ~2K tk. ⚠ `-webkit-line-clamp` and `@container` are both in play and both are copied from the
  artefact, so a divergence would be the artefact's too.
- **CLAIMED — nothing.** Every mechanical statement above quotes a probe or a file and line.

## Evidence

`notes/_subreports/assets/2026-08-27-220-readings-capsule/`

- `measured-grounds-1180.txt` — the full probe: the canvas font triple with **both** controls
  (target/uf/ufor all `346.88`; DejaVu `375.39`; nonexistent `301.07` — target differs from both,
  so this is the real HSBC cut and not a silent fallback), then all 18 specimens with resolved
  caption ground, ink, page ground, tile radius, overflow, column count and wall width. This is
  the file findings 1-3 are read out of.
- `before-the-rejected-card.png` — the BEFORE, light and dark (finding 3).
- `finding-1-darkgrey-vanishes-in-dark.png` — finding 1, seen.
- `finding-2-reading-B-flips-in-dark.png` — finding 2, seen.
- `reading-C-the-shape-that-would-never-exist.png` — the capsule + ground-less caption, struck but
  deliberately **not** dimmed (a demonstration you dim is a demonstration you cannot see).
- `build.py.txt` — the sandbox-local generator, banked because `/var/tmp` does not survive.

**Render-verify, driven not asserted.** At 1180 **and** 480: every `.c-bento__grid` resolves
**1 column**, every wall is **360px**, all **9 pairs** have both cells in the **same** container
band (a pair in two different bands would compare layout while claiming to compare mode — the
`ds-054` class rule, which is why `.rd-pair` cells are capped at 420px), **0** broken images,
**0** horizontal overflow, 18 specimens, 8 sections. Caption height **86px** on every specimen —
canon's ruled gallery caption space, so the copy really is running through canon. Capsule
specimens: tile radius `20px` + `overflow:hidden`, image box `0px`. Corners specimens: tile `0px`
+ `overflow:visible`, image box `20px`. Tree clean: `ls -a knowledge/assets/fonts/_desktop/TTF |
grep -c '^\.uuid'` → **0**.

**Colour law untouched.** No red, no yellow, no green anywhere on the page — the two-red law and
the mono error ink camp are not involved. Refusal is carried by weight, a strike and a printed
reason, copied from the explorer's own disabled-option vocabulary. Type is `.t-cm-*` / `.t-ed-*`
throughout (see finding 8 for the composite I could *not* copy).

REPLAY-THESE: `notes/_subreports/2026-08-27-220-readings-capsule.md` §Findings 1, 2 and 4 (~900 tk)
· `notes/_subreports/2026-08-27-220-readings-capsule.md` §RULING-SHAPED QUESTIONS, all six (~800 tk)
