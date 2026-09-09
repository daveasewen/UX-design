# #264 — two glyph twins, a mis-twinning gate arm, and eight `-active` glyphs derived by geometry

provenance: 264 · 2026-09-09
status: observed

*The WHY/HOW dossier for session #264 (Apollo). Its terse counterparts: the ★ LATEST banner in
`GOOD-MORNING.md`, the ⏱ LATEST DELTA in `_LIVE-STATE.md`, the three rulings `s264-D1` … `s264-D3`
in `knowledge/_rulings.json`, and the filed report `notes/_subreports/2026-09-09-264-W-wrap.md`.
Both-way links: this file is named on the banner's ⓪ SHAPE line and in the delta's WHY line.*

---

## 1. The session opened on two carries and both of them were wrong

The #264 opener put three things to Dave: the Stat card arrow seat, the `/goal` bite-test, and the
sidebar chart glyph. He answered the first one immediately — ***"I thought this was ruled"*** — and
he was right.

The evidence was already in the repo when the #263 wrap wrote the carry. `s263-D1`'s `governs` list
names `knowledge/snippets/Stat-card.reference.html` alongside `Kpi-tile.reference.html`, and the
P-01 recommendation Dave ACCEPTed says, verbatim, **"Stat card moves with it, always."** The #263
wrap READ that `governs` list, wrote *"a `governs` list is a scope, not an answer to a question he
was never put"*, and carried the item anyway. The #264 opener then repeated it.

★ **The lesson is narrow and cheap: a carry that survives a wrap on the strength of the wrap's own
doubt is worth one grep of the ruling it doubts.** The doubt was well-formed — a `governs` list
really is a scope — but the recommendation's own text settles it, and reading the recommendation
costs one call. The carry is STRUCK in `_CARRIES.md` § `residual → #265` with that receipt, by
ADDITION, the original wording standing verbatim beneath it (`s183-D1` / `s188-D2`).

The second carry was worse: it was **false**. It claimed the sidebar's `chart` line glyph was
"hand-baked rather than the library's". Reading the twelve `<symbol>`s in
`knowledge/snippets/Sidebar-nav.reference.html` against `knowledge/assets/icons/` by **path data**
showed every one of them is a library asset, byte-for-byte. Nothing in the sidebar is locally drawn.

What was actually wrong was the **twinning**:

- **Spending** rested on `data-chart` and went current on `insight-active` — a lightbulb. A
  different concept entirely.
- **Transfers** rested on `balance-transfer` (arrows over a coin) and went current on
  `transfer-active` (arrows in a disc), so **the shape changed on selection**. `balance-transfer`
  has no `-active` twin in the library at all.

⇒ The claim was retracted and struck; the repair became two rulings.

## 2. Why the fix was a gate arm rather than two edits

Dave's instruction was two sentences: ***"1. okay fix them 2. do it"*** — the first the repair, the
second the generalisation.

Repairing two rows would have left the class open. The same defect had already produced a third
instance nobody had noticed, and the only reason we found the first two was that somebody happened
to read the nav family during a wrap. So the pairing rule went into `knowledge/_validate_icons.py`
as a **TWIN ARM**: every `.ic-line` / `.ic-fill` pair in a snippet is resolved to library slugs, and
the fill must be the line's `-active` (or `-active-badge`). **MIS-TWINNED is BLOCKING.**

Two design choices in that arm are worth recording because they are the difference between a gate
that runs and a gate that gets disabled:

1. **A line glyph with no twin in the library is REPORTED, not FAILED.** `balance-transfer` is in
   that state. That is a fact about the library's coverage, not a defect in the page that uses it,
   and a gate that conflates the two would fail honest pages.
2. **The bite-test was driven, not asserted.** `mut_mistwinned_icon` is registered in
   `knowledge/_tests/test_gates.py` and was driven **RED → GREEN in-process**, on ONE 93 MB copy —
   the suite's own harness copytrees ≈5 GB and ENOSPCs at 89% disk. ★ That in-process pattern is
   the reusable part: the suite being unrunnable here is a DISK fact, not a capability fact, and a
   single-case in-process drive fits.

The arm earned itself on its first run: **Tab-bar's Insights row carried `insight` in BOTH slots**,
so its "current" state was the line glyph. Fixed to `insight-active` under `s262-D3` in the same
commit (`3d7def7`), together with four App-shell / Command-palette snippets moving
`balance-transfer` → `transfer` at rest.

## 3. The experiment: deriving a filled glyph from a line glyph

`balance-transfer` having no twin raised the general question — the library has line glyphs with no
`-active` partner, and drawing each one by hand is the expensive answer. Dave: ***"go, lets see
whatcha got"***.

The method (Skia path ops, `skia-python`; its `libEGL` / `libGL` / `libglvnd` / `libGLX` /
`libOpenGL` extracted without root the `chromium-in-sandbox-recipe` way):

```
S  = silhouette        contours filled and unioned
B  = S − erode(S, 1.25)    the outline band
I  = L − B                 interior ink (counters, inner detail)
A1 = S − I                 variant 1
A2 = S − silhouette(I)     variant 2
```

⚠ **The order that mattered was CALIBRATION FIRST.** Ten human-drawn line/fill pairs already in the
library were run through the derivation before anything was shown to Dave: **7 landed within
tolerance**; `card`, `alert` and `insight` are **designer EDITS no rule recovers**; `settings` needs
A2. Publishing thirteen orphan candidates without that control would have been a demo, not a
measurement — and the three known misses are what let the review page say honestly which failures
are the method's and which are the drawing's.

Thirteen orphans went to `notes/_REVIEW-264-active-glyphs.html` (`notes/_lanes/264-active-gen.py`,
`264-active-page.py`, `3722f26`) and **nothing entered the library before he graded them.**

## 4. His grade, and the class hiding inside the five rejections

`s264-D3`: eight A1 twins ACCEPTED into the library — cheque, finances, document-report, newspaper,
device-mobile, online-banking, presentation, add-circle — written as `<slug>-active.svg` with a
**`$derived`** annotation in `icons.manifest.json` (`$total` 658 → 666; the icon gate's glyph count
750 → 758). ⛔ **A generated twin is not a Figma export and the manifest is not allowed to pretend
otherwise** — that is the whole job of `$derived`.

The five rejections came with reasons, and read together the reasons are ONE class rather than five
tastes:

- *"balance-transfer → neither — the whole card should be filled not just the top, but the overlap
  exclusion are need to be kept"*
- *"tax → neither — the document icon half should be filled, if you look at teh document icon as a
  guide"*
- *"workspace → neither — we have to fill teh otehr part of teh icon too"*
- *"digital-statements → neither — need both parts filled"*
- *"global-money → neither — thsi is quite ahard one to get right"*

★ **The class: icons made of TWO BODIES with an overlap exclusion.** The derivation fills only the
front body, because the rear body's contour is not closed on its own — the front's outline is doing
double duty as the rear's edge, so the silhouette step drops it.

## 5. The second pass — and the one glyph the class does not contain

Dave: ***"have another go"***. `notes/_lanes/264-active-gen2.py`:

- silhouette = the **holes of the EXTERIOR** of (L ∪ grow(frontSil, gap 1.0)) — i.e. find the
  enclosed regions by asking what the outside cannot reach, rather than by closing contours;
- **fronts are the rings whose SEALING GAINS AREA** (> 3 px², raster-counted at 16× **for
  classification only** — the geometry stays vector; the raster is a decision aid, never the
  output);
- open bodies are morphologically closed.

**balance-transfer, tax, workspace and digital-statements now fill.** Four of the five.

⛔ **`global-money` does not, and the reason is structural rather than a tuning gap: it is ONE
CONNECTED INK PIECE.** The arrows touch the meridians, so there is no second body to find — nothing
in the drawing separates a front from a rear. It is a **drawing** problem, not a derivation problem,
and no amount of morphology reaches it. His grade — *"thsi is quite ahard one to get right"* — was
about the glyph, and it turns out to have been about its topology.

Dave, closing: ***"no time for this now, but we can return to it another time because we are getting
somewhere"***. ⇒ the four stay **UNGRADED** on `notes/_REVIEW-264-active-glyphs-2.html`, nothing
further entered the library, and **that sentence was appended to `s264-D3`'s `evidence`**
(`--amend-evidence`) rather than left in chat — a `LATER` that arrives with a sentence is a reading,
and the reading belongs on the ruling.

## Resolved state, and what is still open

**Resolved.** Sidebar-nav wears `data-chart`/`data-chart-active` and `transfer`/`transfer-active`
(`9bfacb9`). Mis-twinning is a BLOCKING gate arm with a registered, driven bite-test (`3d7def7`).
Eight derived `-active` glyphs are in the library and declared derived (`c7247c2`). The two opening
carries are STRUCK with receipts.

**Open, and Dave's.** The `/goal` bite-test — ruled *"do it"* at this session's opener and **NOT
STARTED**. The four ungraded twins, and whether `global-money` gets DRAWN. Whether a gate report
should be refused at commit when its own tree does not match HEAD (#263's finding). #241's
midnight-wrap question, age 22. And what to do about ritual step 3 now that four consecutive
delegated wrap seats have been unable to write memory — at #264 the conductor wrote the hook
himself before delegating, which is the first time the limit was handled in front rather than
discovered at the seat.
