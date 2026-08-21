# LANE R receipt — the four-theme review surface for the 43 wave 3–6 components

> ⛔ **DATED PERIOD RECORD, NOT A LIVE HOME.** Written 2026-08-21 by the #213 LANE R sub (Opus).
> The store stays the one live home (`knowledge/_state.json`, `knowledge/_rulings.json`).
> **Nothing here is a ruling, and nothing the page produces is a ruling.** The page's decision
> controls write to `localStorage` and to a copy-paste textarea — they touch no repo file.

| governance | value |
|---|---|
| serves | `notes/_briefs/2026-08-21-213-c1-residual-survey-v1.md` § 6, lane **R** (fire first) — the (b2) residual |
| fences | `notes/_briefs/2026-08-21-213-mine-burn-fanout-brief-v1.md` § FENCES |
| rows this unblocks | `W-63` · `W-71` · `W-72` · `W-73` · `W-74` (open, dave) · `W-75`…`W-84` (parked, dave) |
| files this lane OWNS | `reviews/REVIEW-213-wave-components-four-theme-v1.html` (NEW) · `knowledge/_render/gen_review_213_wave_components.py` (NEW) · this receipt (NEW) · `reviews/outputs/s213-laneR/*.png` (NEW, **gitignored**) |
| files this lane did NOT touch | every snippet, every meta, every showroom page, canon, tokens, the store, the spine, any `_lanes.json`, `GOOD-MORNING.md`, `_LIVE-STATE.md`, `MEMORY.md`, `_CHAIN.md` |

---

## 0 · THE HEADLINE

**Dave owed his eye on 43 components and had no surface to give it on. He has one now, and not one
byte of component markup was re-drawn to build it.**

Every specimen on the page is a live `<iframe>` of the component's **own generated showroom page**
(`showroom/<slug>.html`), which itself `srcdoc`-mounts the gated reference snippet. The review page
owns nothing but chrome: the theme broadcast, the question prose, and the decision controls. That is
[[specimen-starts-from-reference]] obeyed structurally rather than by discipline — there is no copy
of the markup for a hand-rolled defect to creep into, because there is no copy.

The theme broadcast is not a re-implementation of the cascade either. `gen_showroom.py:314` already
registers `window.addEventListener('hashchange', initFromHash)`, and `initFromHash` re-reads
`#theme=<attr>&m=<light|dark>&w=<px>` and re-applies `html[data-apollo-theme]` + `body[data-theme]`
to the inner frame. The review page therefore re-themes 43 specimens by assigning a new **fragment**
to `iframe.src` — a same-document fragment navigation. No reload, no cross-origin script access, no
second copy of the theme logic anywhere.

---

## 1 · THE COMPONENT LIST — DERIVED, NOT INHERITED

The survey said "43". [[premise-ages-faster-than-rule]] — so it was re-derived from the store rows
and the lane receipts, then every member was probed on disk.

**Step 1 — the rows.** `knowledge/_state.json` parsed for `W-62`, `W-63`, `W-71`…`W-74`, `W-75`…`W-84`.
Their own titles carry the counts, verbatim:

| row | state / owner | count its title declares |
|---|---|---|
| `W-63` | open · dave | "wave-3 **NINE** components BUILT PROPOSED-NOT-RULED" |
| `W-74` | open · dave | "wave-4 **heavy 7** BUILT PROPOSED-NOT-RULED (calendar tree cascader splitter qr-code carousel image-block)" |
| `W-79` | parked · dave | "wave-5 Layer-2 **ELEVEN** organisms BUILT PROPOSED (3 shells + 6 templates + 2 lock-ups)" |
| `W-84` | parked · dave | "wave-6 Layer-2 **SIXTEEN** P3 organisms BUILT PROPOSED (4 shells + 5 templates + 7 lock-ups)" |

**9 + 7 + 11 + 16 = 43.** The umbrella rows (`W-74`, `W-79`, `W-84`) agree with their per-lane
children (`W-71`/`W-72`/`W-73`; `W-75`…`W-78`; `W-80`…`W-83`), so the count is corroborated twice.

**Step 2 — the names**, taken from the lane receipts' own `## 1 · FILE LIST` sections, not from
inference: `notes/_receipts/2026-08-20-209-wave3-lane{A,B,C}-*.md` and
`notes/_receipts/2026-08-20-210-wave{4,5,6}-lane{A,B,C,D}-*.md` (14 receipts).

**Step 3 — the probe.** Every one of the 43 was checked for its three artefacts:

```
for each name:  knowledge/snippets/<Name>.reference.html
                knowledge/components/<slug>.meta.json
                showroom/<slug>.html
→ 43/43 present on all three.  0 missing.
```

Re-run by the generator itself at build time: the emitted HTML's 43 `data-base="../showroom/…"`
values, 43 snippet join keys and 43 receipt join keys were each re-resolved against the filesystem
after generation — **0 missing showroom pages, 0 missing snippets, 0 missing receipts** (the single
"missing receipt" the check reported on the first run was *this file*, which did not yet exist).

**MEASURED COUNT: 43.** The survey's figure holds.

---

## 2 · WHAT THE PAGE DOES

| feature | how, and the fence it answers |
|---|---|
| **Specimens** | 43 lazy-mounted iframes of `showroom/<slug>.html`. Mounted on first open of the card's `<details>`, so the page is cheap until Dave opens something. ⛔ **No component markup is copied.** |
| **Four themes × light/dark** | Global segmented controls broadcast `#theme=…&m=…` to every OPEN specimen at once. All four themes, both modes, driven and proven (§3). |
| **Responsive** | A width segment (390 / 768 / 1280 / Full) sets both the outer iframe width and the showroom's own `w=` slider, so a phone check is one click, per [[review-live-variant-spread]]. The review page's own chrome reflows to a single column at 900px and to phone at 640px. |
| **Decision control** | Per component: **Promote / Rework / Delete / Defer** plus a free-text box, per [[feedback-live-controller]]. Persisted to `localStorage` only. |
| **Export** | One button emits Dave's rulings as plain pasteable text, grouped by wave, each line carrying the component name, its slug and its store row as small-print join keys — and a closing list of what he has NOT yet ruled. |
| **The questions, in plain prose** | Every component card carries its own open questions **as sentences**, mined verbatim-in-substance from the lane receipts' `$decisionsForDave` sections. IDs appear only as small-print join keys (row, snippet path, receipt path) — never as the decision surface, per [[feedback-decisions-in-plain-prose]]. |
| **"Rule once" blocks** | Five cross-cutting blocks (wave-3 restraints · wave-4 gate findings · shells · templates · lock-ups) collect the questions that are **one ruling with many symptoms** — the breakpoint scale, the brand mark, the artefact class, the missing `composes` schema edge, the three inherited target-size shortfalls, the type-ramp gap. Dave rules those once, not 43 times. |

**Question coverage — COUNTED, not estimated.** 92 questions live structurally in the metas'
`$decisionsForDave`, spread across only 15 of the 43 metas; the other **28 metas carry no
`$decisionsForDave` at all**, so their questions live *only* in receipt prose and would have been
invisible to anyone reading the metas. The page carries **172 questions in total — 145 attached to
individual components, 27 in the five rule-once blocks**.

⚠ *These four figures were re-counted off the generator's own data after this receipt first carried
estimates (111 / 24 / 135 / 26). The estimates were wrong. [[planning-estimate-is-not-a-measurement]]
— probe:*
```
python3 -c "import sys;sys.path.insert(0,'knowledge/_render');import gen_review_213_wave_components as g;
print(sum(len(c['qs']) for c in g.COMPONENTS), sum(len(v['items']) for v in g.CROSS.values()))"
→ 145 27
```

⚠ **This is a CONDENSATION, not a transcript** — see residual 2.

---

## 3 · RENDER-VERIFY — DRIVEN, NOT CLAIMED

Environment per `knowledge/_RUNBOOK-render-verify.md`, **with the correction the gate-red receipt
records**: `notes/_receipts/2026-08-21-213-gate-red-repairs.md:369–371` says the runbook's
`/var/tmp/chromelibs` is empty this session and Chromium dies on `libXdamage.so.1`. Confirmed again
here — the working path is `/var/tmp/chromelibs-s213e2/root/usr/lib/aarch64-linux-gnu`.

```bash
export PYTHONPATH=/var/tmp/pylibs:$PYTHONPATH
export PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-s213e2
export FONTCONFIG_FILE=/var/tmp/fonts-s213e2.conf
export TMPDIR=/var/tmp
export LD_LIBRARY_PATH=/var/tmp/chromelibs-s213e2/root/usr/lib/aarch64-linux-gnu
```

### What was DRIVEN (headless Chromium, `--allow-file-access-from-files`, real HSBC face)

| driven | result |
|---|---|
| page loads from `file://`, 43 cards present | ✅ `article.cmp` count = **43**; `PAGE ERRORS: none` |
| **`file://` sub-frames actually load** (the real risk in a local review page) | ✅ every opened iframe reports its showroom title, e.g. `Calendar · Apollo showroom`, and the showroom's OWN inner frame is reachable |
| theme broadcast reaches the **deepest** frame | ✅ all 5 test specimens went `mono/light` → `console/dark` on one click |
| **all four themes × both modes**, on `template-dashboard` | ✅ `mono/light` `mono/dark` `legacy/light` `legacy/dark` `console/light` `console/dark` `supercharge/light` `supercharge/dark` — **8/8**, each screenshotted |
| width preset | ✅ `390px | src=…&w=390` — outer width and inner slider both follow |
| **phone responsive** at 390 × 900 viewport | ✅ `document.scrollWidth > clientWidth` = **false** — no horizontal page scroll |
| decision control + export | ✅ radio + note recorded, counter went to 1, export text emitted with the component name, slug, row, verdict and the note, plus "NOT YET RULED (42 of 43)" |

### What was SEEN (not just measured)

`reviews/outputs/s213-laneR/` (**gitignored** — `.gitignore:52 outputs/`):
`r213-mono-light.png` · `r213-console-dark.png` · `r213-phone.png` ·
`spec-{mono,legacy,console,supercharge}-{light,dark}.png`.

Looked at, by eye: `spec-legacy-light.png` renders the dashboard template with the **brand-red**
primary button; `spec-supercharge-dark.png` renders the same template on the dark ground with a
neutral primary and the green/coral spark inks. **The four themes are visibly different, in a live
frame, in this page.** The wave-5/6 lane-B receipts declared console/legacy/supercharge **UNPROVEN
by render** for all their pages — §C·1 residual **(c6)**. That residual is now discharged for the
templates and shells that were opened; it is discharged *by construction* for the rest, since every
card uses the identical mechanism.

### THE BITE — shown FAILING on a mutant ([[mutation-tests-the-clause-not-the-feature]])

Bite: *"switching the theme control re-themes the deepest specimen frame."*
Mutant: **15 bytes** — `frag()` made to return `""` instead of `"#" + p.join("&")`, so no fragment is
ever assigned and the showroom never hears `hashchange`.

```
PASS  BITE theme-broadcast-reaches-the-specimen: expected console/dark, got console/dark   [REVIEW-213-…-v1.html]
FAIL  BITE theme-broadcast-reaches-the-specimen: expected console/dark, got mono/light     [_s213laneR-MUTANT-tmp.html]
```

⚠ **The mutant was re-run IN `reviews/` deliberately.** The first mutant run lived in `/var/tmp`,
where `../showroom/` resolves to nothing — it returned `NOFRAME`, which would have been a
**confounded** fail (wrong relative path, not the mutation). Re-run in the same directory as the
real page, with only the 15-byte delta differing, it returns `mono/light`: the specimen **loads
fine** and simply never re-themes. That is the clause failing, and nothing else.
The mutant file was moved out of `reviews/` immediately (`mv`, per the no-`rm` sandbox rule);
`ls reviews/ | grep -i mutant` → nothing left.

---

## 4 · CLAIM TABLE — every claim carries a probeable token (`s182-D1`)

| # | claim | probe |
|---|---|---|
| 1 | 43 components, measured not inherited | §1; `article.cmp` count = 43; generator asserts `total == 43` and dies otherwise |
| 2 | all 43 have snippet + meta + showroom page | §1 step 3; post-generation re-resolve of all 129 join keys → 0 missing |
| 3 | no component markup is copied into the review page | `grep -c 'cn-' reviews/REVIEW-213-*.html` counts only the class names inside *question prose*; the page contains 43 `<iframe>` and **0** `srcdoc`/inlined specimens |
| 4 | the theme mechanism is the showroom's own, not a second copy | `gen_showroom.py:309–315` (`initFromHash` + `hashchange`); the review page's `frag()` writes only a fragment |
| 5 | four themes × light/dark all reach the specimen | §3, 8/8 driven, 8 screenshots |
| 6 | the theme claim can FAIL | §3 bite, unconfounded mutant |
| 7 | no horizontal page scroll at 390px | §3, measured `false` |
| 8 | the page writes nothing to the repo | its only persistence is `localStorage`; export is a `<textarea>` + `execCommand('copy')` |
| 9 | the page is regenerable | `python3 knowledge/_render/gen_review_213_wave_components.py` → same file, byte-stable |
| 10 | question prose is sourced from the receipts | every card names its source receipt as a join key; §2 coverage figures |

---

## 5 · WHAT STAYS UNPROVEN / RESIDUALS — declared, not smoothed

1. **Only 5 of 43 specimens were opened in the drive, plus `template-dashboard` for the eight-way
   theme sweep.** Every card uses the *identical* generated mechanism, so this is a **bounded**
   verification (`s172-D3`, depth cap 1) — but "all 43 render correctly in all four themes" is
   **NOT** proven and is not claimed. The honest claim is: *the surface works, and six components
   were seen through it.* ⚠ Some Layer-2 pages are tall; the 760px iframe crops them and Dave will
   scroll inside the frame, or use the showroom's own **Open ↗** button.
2. **The question prose is a CONDENSATION of the receipts, in this sub's words.** It is faithful to
   the receipts' substance and each card names its source file, but it is not a verbatim transcript
   — where a question turns on an exact figure, the figure was carried across; where it turned on
   long reasoning, the reasoning was compressed. ⛔ **If Dave rules on a question, the receipt is
   the authority, not this page.**
3. **The five "rule once" blocks are this sub's GROUPING, not a ruled taxonomy.** They assert that
   e.g. the breakpoint scale is one question with seven symptoms. That reading comes from the
   receipts' own words ("the biggest one, and it spans the wave") but the grouping itself is
   PROPOSED.
4. **No gate or validator was run.** This lane built a review artefact; it edited no snippet, no
   meta, no token, no canon. `_validate_*` was neither run nor needed. **Which serial steps this
   work obligates: NONE.** No registry entry, no `MIGRATED_SNIPPETS`, no `CATEGORIES`, no KG node,
   no showroom regen. The one thing it *does* obligate is a **store doc-row** for the two new files
   ([[forgotten-document-class]]) — proposed in §7, the conductor's to mint.
5. **`localStorage` is per-browser and per-origin.** If Dave opens the page in a different browser
   or clears site data, his in-progress notes are gone. He should export before closing. A
   server-backed alternative was not built and would be out of scope for a review artefact.
6. **The page's own chrome is deliberately NOT themed.** It is a neutral review surface so the
   specimens carry the only theme signal on screen. That is a judgement, and it is visible.
7. **Fence deviation, declared:** one **read-only** git command was run — `git check-ignore -v` — to
   confirm `reviews/outputs/` is ignored before writing PNGs there. No mutating git command of any
   kind. Named rather than hidden.
8. **The runbook's `/var/tmp/chromelibs` line is stale for a second consecutive lane** (E2 hit it,
   this lane hit it). That is a runbook correction, the conductor's, not a ruling — see §7.

---

## 6 · PITFALLS THIS LANE WAS WARNED ABOUT, AND WHAT HAPPENED

- **#202, "three hand-rolled pages invented three defects."** Answered structurally: there is no
  hand-rolled markup on this page at all. This is the strongest available form of that lesson.
- **#184, dangling `var()` renders SILENT BLACK.** No token was edited, so the class cannot bite
  here — but a render was driven anyway, in all four themes, both modes.
- **#104 / #171, self-comparing asserts pass on their own mutants.** The bite was driven against a
  real mutant *and* the first mutant run was **rejected as confounded** rather than banked.
- **#210, the regen serial set is ordered.** This lane obligates **no** serial step (§5 item 4).
- **[[premise-ages-faster-than-rule]].** "43" was re-derived from the store and the receipts before
  a line of the page was written, not inherited from the survey.

---

## 7 · HANDOFF TO THE CONDUCTOR — what this lane could not do

1. ⬛ **Mint the store doc-row** for `reviews/REVIEW-213-wave-components-four-theme-v1.html` +
   `knowledge/_render/gen_review_213_wave_components.py` ([[forgotten-document-class]]; the doc-row
   gate is wired blocking). PROPOSED body: *"#213 lane R four-theme review surface over the 43 wave
   3–6 components; live showroom iframes, no re-drawn markup; per-component promote/rework/delete
   control with paste-back export; unblocks W-63, W-71…W-74, W-75…W-84."* Owner: claude.
   Closes when: Dave has ruled the 43.
2. ⬛ **Runbook correction, second sighting:** `knowledge/_RUNBOOK-render-verify.md` names
   `/var/tmp/chromelibs` for `LD_LIBRARY_PATH`; it is empty and Chromium dies on `libXdamage.so.1`.
   Both #213 lanes that rendered hit it. The working recipe is a **per-session** `chromelibs-<sess>`
   path — the runbook should say so rather than naming one directory. A runbook line, not a ruling.
3. ⬛ **The rows this page is meant to close** stay OPEN/PARKED until Dave has actually looked:
   `W-63` · `W-71` · `W-72` · `W-73` · `W-74` open; `W-75`…`W-84` parked. **This receipt must not be
   cited as evidence that any of the 43 is settled.**
4. ℹ️ **`reviews/outputs/s213-laneR/*.png` are gitignored** — they are evidence for this sitting, not
   repo artefacts. Regenerate from `/var/tmp/s213laneR/{probe,spec,bite}.py` (NON-REPO: sandbox,
   this session only; the recipes are quoted in §3).

---

## 8 · FOR DAVE, IN ONE PARAGRAPH

Open `reviews/REVIEW-213-wave-components-four-theme-v1.html`. It lists the forty-three things that
were built for you across four waves and never shown to you. Each one has a short plain-English list
of what is still undecided about it, a **Show the live specimen** button that drops the real thing
into the page, and four buttons — promote, rework, delete, defer — plus a box to say why. The theme
and light/dark controls at the top switch every open specimen at once, so you can see the same
component in Mono, Legacy, Console and Supercharge without leaving the page. When you are done, press
**Export rulings** and paste the text back. Five yellow **Rule once** panels sit above the components
— those are the questions where one answer settles many components at a time (the breakpoint scale,
the brand mark, whether templates are really "components"), and they are probably worth reading
first.
