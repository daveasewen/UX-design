# #217 — Bento in the wild: testing the three-role taxonomy against practice

Research sub, session #217. Web research only — no canon edits, no rulings. Every claim below is
cited to a source that was actually fetched; anything I could not verify is marked **UNVERIFIED**.

---

## Exec summary — the verdict first

The three roles are **two-thirds confirmed and one-third mis-named**. Practice does split bento
into a marketing use and an in-app use, and the split is real and well documented. But the third
role — GALLERY — turns out not to be a bento at all in the wild. Photography walls run a
completely different algorithm from a span grid, and the profession has a name and an open-source
implementation for it.

**Brochureware is the safest of the three.** It is the origin of the trend and the dominant use
today. Apple's own CSS on the MacBook Air page puts an 18px radius on each tile, with a white
ground and its own shadow — radius and ground on the tile, exactly as the hypothesis says. Every
practitioner guide agrees on one uniform gutter of 16–24px on desktop, and says the effect dies
if you mix gutters or drop the radius.

**Dashboard is right about the role but has no published precedent for the flush part.** Bento
maps cleanly onto dashboard widgets — several sources say so explicitly. But I found no source
recommending near-zero internal spacing for a dashboard bento; mainstream dashboard guidance
runs the other way, warning that under about 12px gutter the cards visually merge. What does
exist is a *different* named precedent for the same shape logic: Apple's concentricity rule
(inner radius = parent radius − padding), and Apple's own inset-grouped list, which is a rounded
container holding flush rows separated by hairlines. So the pattern is real and Apple-sanctioned;
it is simply not filed under "bento" by anybody. That is a positioning question, not a defect.

**Gallery is the one that bends.** Flickr's justified layout — the canonical photo wall, open
source since 2016 — does not use spans at all. It packs photos into rows at their native aspect
ratio and then scales each row's height so the row justifies to the full container width. Ragged
right edges are exactly what it exists to eliminate. Only the final row is allowed to be short,
and Flickr calls those photos **widows**, returns a `widowCount`, and gives you a `showWidows`
switch to hide them. So the hypothesis is half right: raggedness is tolerated in galleries, but
only at the *bottom*, never at the sides — and even the bottom is an explicit, named,
switchable decision rather than something shrugged at.

**Two parts of the built system have better precedent than expected.** The every-Nth emphasis
rhythm is not an invention: Flickr ships `fullWidthBreakoutRowCadence`, "insert a full width box
every n rows", and gates it on the photo's aspect ratio being ≥ 1. And container-query bands per
tile are exactly what Steve McKinney's widely-cited bento build does, using container queries
rather than media queries specifically so each tile can switch its own aspect ratio.

**The biggest live risk is not layout, it is focus order.** Every serious source flags the same
trap: `grid-auto-flow: dense` reorders tiles visually while keyboard focus and screen readers
follow DOM order, which breaks WCAG 2.4.3 and 1.3.2. The published fix is to let spans do the
layout and reserve dense packing for non-interactive tiles.

**And one honest caution about the evidence itself.** Two credible-looking sources flatly
contradict each other on whether the famous SaaS sites still run bento homepages. One says
Linear, Vercel, Raycast and Cursor all do; the other says it checked live and only Apple,
Raycast, Amie and GitHub Copilot do. I probed three of them myself and could only confirm
Vercel. Treat the "everyone does bento" listicle claim as soft.

---

## Q1 — Does practice cluster into the three roles?

**Partly. The cluster line practice actually draws is different from Dave's.**

The line the sources draw is *parallel exploration vs sequential progression*. Landdding's
category breakdown puts it plainly: bento wins where "visitors will jump around — comparing
features, browsing work, or monitoring multiple metrics at once" and fails where the page exists
"to move users forward through a fixed sequence". By that cut, marketing pages, portfolios and
dashboards land in one family, and blogs, product listings and checkout flows land outside it
entirely.
([Landdding, May 2026](https://landdding.com/blog/bento-grid-design-by-website-category-where-the-pattern-wins))

**Marketing / brochureware.** Confirmed as the origin and the dominant case. Apple's product
pages and keynote slides made it mainstream around 2023.
([Superdesign](https://superdesign.dev/styles/bento-grid),
[medevel](https://medevel.com/bento-grid-is-not-masonry-heres-why-and-what-to-use-when-a-quick-guide-for-ui-ux-designers/))
SaaSFrame catalogued 43 bento sections from SaaS marketing sites.
([SaaSFrame](https://www.saasframe.io/blog/designing-bento-grids-that-actually-work-a-2026-practical-guide))

**Dashboard.** Confirmed as a role, in both marketing-of-dashboards and real app UI. Superdesign:
"One place the pattern translates beautifully: dashboards, where bento cells map one-to-one onto
widgets." Landdding names Datadog, Mixpanel and Linear's project views as in-app modular card
layouts (**UNVERIFIED** — I did not open those products). SaaSFrame describes the same mix: KPIs
as 2×1, funnels as 2×2, activity lists as 1×2.

**Gallery.** This is where the taxonomy strains. The sources treat photo walls as *masonry*, a
distinct family, not a bento: "Bento is curated hierarchy, masonry is a feed"
([Superdesign](https://superdesign.dev/styles/bento-grid)); "Masonry suits image galleries, while
bento suits dashboards" ([medevel](https://medevel.com/bento-grid-is-not-masonry-heres-why-and-what-to-use-when-a-quick-guide-for-ui-ux-designers/)).
And the actual photo-wall products use neither — Flickr uses justified rows (see Q3).

**What sits inside "gallery" that *is* bento**: portfolio and agency sites. Landdding argues
these are one of the strongest fits, because the lead project earns the biggest card and side
projects take compact slots, and because agencies mix media types with logos and awards on one
page. That is aspect-driven and photographic, but it is *curated hierarchy*, not a feed — it
behaves like brochureware, not like a photo wall.

### Where radius, gutters and grounds actually sit

- **Apple, brochureware — measured directly from their stylesheet.** `.tile-rounded{border-radius:18px}`,
  `.tile{...overflow:hidden;background-color:#fff}`, and an optional `.tile-shadow{box-shadow:8px 8px 16px 0 rgba(0,0,0,.08)}`.
  Radius, ground and shadow all live **on the tile**. The page's own 12-column grid runs a 40px
  column gap / 82px row gap at desktop, tightening to 24px and then 0.
  (fetched `https://www.apple.com/v/macbook-air/z/built/styles/main.built.css`, 2026-08-24)
- **Practitioner consensus for brochureware bento:** radius 20–28px, one uniform 16px gap, cell
  ground `#f5f5f7` light / `#161617` dark with a 1px `rgba(255,255,255,0.08)` border.
  "The radius (20 to 28px) plus a single consistent gap is what reads as bento. Mixed gaps or
  square corners and the effect dies." ([Superdesign](https://superdesign.dev/styles/bento-grid))
- **Steve McKinney's reference build:** `gap: 1rem`, tiles at `rounded-2xl` with a `ring`
  hairline, and an inner image container at `rounded-lg` with its own ring — i.e. a *nested*
  radius inside the tile, not a flush one.
  ([iamsteve](https://iamsteve.me/blog/bento-layout-css-grid))

---

## Q2 — Radius placement: is container-radius-with-flush-tiles a recognised pattern?

**Not under the bento name. Very much so under other names.**

Nobody writing about bento describes a rounded container with flush interior tiles. Every bento
recipe I read puts the radius on the tile.

But the *shape logic* Dave's dashboard role implies has first-class precedent, and it comes from
Apple itself. From the WWDC25 session transcript, verbatim:

> "There's a quiet geometry to how our shapes fit together, driven by concentricity. By aligning
> radii and margins around a shared center, shapes can comfortably nest within each other. … We
> use three shape types to build concentric layouts: fixed shapes have a constant corner radius.
> Capsules use a radius that's half the height of the container. And concentric shapes calculate
> their radius by subtracting padding from the parent's."

and, on the exact failure mode:

> "keep an eye out for corners that feel too pinched — or flared. They can create tension and
> break the sense of balance. One place this often shows up in is nested containers — like
> artwork in a card."

Apple also describes a **fallback radius** trick worth stealing: "use a concentric shape with a
fallback radius. The concentric value adapts when nested, and the fallback kicks in when the
component stands alone." That is precisely the nesting-with-per-instance-parameters problem.
([Apple WWDC25 — Get to know the new design system](https://developer.apple.com/videos/play/wwdc2025/356/))

The same rule is independently well documented in the wider community as **inner = outer −
padding**, with the geometric proof that the two arcs share a centre only when `p + r = R`
([Cloud Four](https://cloudfour.com/thinks/the-math-behind-nesting-rounded-corners/),
[dev.to](https://dev.to/sgbp/the-concentric-border-radius-rule-why-nested-rounded-corners-look-slightly-wrong-3hog),
[PV21](https://pv21design.pt/concentric-radius-nested-corners-done-right/)), typically
implemented as `calc(var(--radius) - var(--padding))`.

**The flush-children-in-a-rounded-container pattern also exists as a shipped Apple control:** the
inset grouped list. Apple's docs describe "a table view where the grouped sections are inset with
rounded corners", with "a continuous background color that extends from the section header,
around both sides of list items in the section, and down to the section footer", and rows
separated by hairline separators with configurable insets.
([UITableView.Style.insetGrouped](https://developer.apple.com/documentation/uikit/uitableview/style-swift.enum/insetgrouped),
[SwiftUI insetGrouped](https://developer.apple.com/documentation/swiftui/liststyle/insetgrouped))

Material 3 does *not* give a concentric rule of this kind. Its shape work went the other way —
a 10-step corner radius scale and 35 abstract shapes, with the stated intent of creating
"visual tension" by mixing radii, not resolving it.
([M3 corner radius scale](https://m3.material.io/styles/shape/corner-radius-scale) via search
summary; **UNVERIFIED** — the m3 page itself was not fetched, only the search digest and
secondary write-ups.)

---

## Q3 — Orphans, squaring and ragged edges

**The gallery prediction is half right, and the real practice is more disciplined than "tolerated".**

Flickr's justified layout is the canonical photo wall, in production since late 2011 and open
sourced in 2016. It "lays those photos out in a row sequentially using the maximum allowed height
and scaling the width proportionately, and if a row becomes longer than the viewport width,
reduces the height of that row and all the photos in it until the width is correct."
([code.flickr.com](https://code.flickr.net/2016/04/05/our-justified-layout-goes-open-source/))

Two things follow, and both matter here:

1. **Side raggedness is the enemy, not the aesthetic.** Every row is justified flush to both
   edges. What varies is row height, not row width. This is the opposite of masonry.
2. **Orphans have a name, a count and a switch.** The algorithm's output object literally
   contains `"widowCount": 0`, and `showWidows` (default `true`) controls whether trailing items
   that don't make a full row are returned at all: "If `false` they'll be omitted from the
   output." ([Flickr docs](https://flickr.github.io/justified-layout/),
   [README](https://github.com/flickr/justified-layout))

Third-party justified galleries expose the same decision as a first-class setting — hide the
incomplete last row, centre it, stretch it, or leave rows at exact height so they end where they
end. ([Justified Image Grid](https://justifiedgrid.com/features/automatic-justified-layout/), via
search digest; **partially UNVERIFIED** — page not fetched directly.)

**On the bento side the equivalent of squaring is `grid-auto-flow: dense`.** It "attempts to fill
in holes earlier in the grid, if smaller items come up later"
([MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/grid-auto-flow)), and both the reference
builds use it ([iamsteve](https://iamsteve.me/blog/bento-layout-css-grid),
[Superdesign](https://superdesign.dev/styles/bento-grid) — "the one property most tutorials
miss"). Note this is *backfill by reordering*, not *resizing to square off*. A mint-time squaring
pass that adjusts spans is a different and arguably safer instrument, because it does not
decouple visual order from DOM order (see Q7).

**Masonry is where raggedness genuinely lives**, and it is described as a feed aesthetic —
Pinterest, Behance, Dribbble — with an explicit accessibility warning attached: "logical content
order can get tricky, so it's not always friendly for screen readers."
([medevel](https://medevel.com/bento-grid-is-not-masonry-heres-why-and-what-to-use-when-a-quick-guide-for-ui-ux-designers/))

---

## Q4 — Spacing regimes: flush vs gapped

**Gapped is the published norm across every context I found, including dashboards.**

- Bento brochureware: desktop 16–24px, tablet 12–16px, mobile 12px, and "the gaps between boxes
  must be identical throughout the entire grid".
  ([SaaSFrame](https://www.saasframe.io/blog/designing-bento-grids-that-actually-work-a-2026-practical-guide))
- Bento recipe: one 16px gap everywhere; "ONE consistent gutter everywhere sells the 'tray' look".
  ([Superdesign](https://superdesign.dev/styles/bento-grid))
- Dashboards: 16px gap with 24px container padding as a starting point; 8px gap with 12px card
  padding for maximum density; below roughly 8–12px "tiles merge into an undifferentiated block"
  and users misread where one card ends. Grafana practice cited as 20px between rows, 10px
  between panels, on a 24-column grid. (search digests over
  [designmd](https://designmd.app/library/data-dense-dashboard),
  [MetricFire](https://www.metricfire.com/blog/7-best-practices-for-grafana-dashboard-design/),
  [Pencil & Paper](https://www.pencilandpaper.io/articles/ux-pattern-analysis-data-dashboards);
  **UNVERIFIED** at the primary-page level — these came from search summaries, not fetched pages.)

**Nothing I found advocates a 0–1px flush bento.** The nearest published nod is Superdesign's
passing description of a "mosaic grid" variant with "hairline gaps" — same structure, different
temperature — which shows the flush end of the range is at least recognised as a legitimate
skin of the same recipe. ([Superdesign](https://superdesign.dev/styles/bento-grid))

**But the platform is moving toward flush-with-keylines as a supported thing.** CSS gap
decorations extend `column-rule` to grid and flexbox and add `row-rule`, with `repeat()` syntax,
`*-rule-break`, `*-rule-outset` and `gap-rule-paint-order`. The explicit motivation is that
drawing separators between grid items currently requires "awkward workarounds with borders,
pseudo-elements, or background tricks" that are "accessibility-unfriendly" because they add DOM
elements. Available for developer trial in Chrome/Edge 139; spec is
[css-gaps-1](https://www.w3.org/TR/css-gaps-1/).
([Chrome for Developers](https://developer.chrome.com/blog/gap-decorations))

**4/8pt grid.** No source states a bento-specific gutter rule, but every number quoted anywhere
above — 8, 12, 16, 20, 24, 32, 40 — is a multiple of 4, and the two most-cited (16, 24) are
multiples of 8. The base-unit formula published for bento is
`card width = (base unit × columns) + (gutter × (columns − 1))`, with base units of 80/100/120px.
([SaaSFrame](https://www.saasframe.io/blog/designing-bento-grids-that-actually-work-a-2026-practical-guide))

---

## Q5 — Emphasis rhythm and aspect-driven spans

**In galleries: algorithmic, shipped, and with a cadence parameter. In bentos: hand-curated.**

Flickr's config includes `fullWidthBreakoutRowCadence` — "If you'd like to insert a full width
box every `n` rows you can specify it with this parameter. The box on that row will ignore the
`targetRowHeight`, make itself as wide as `containerWidth - containerPadding` and be as tall as
its aspect ratio defines. **It'll only happen if that item has an aspect ratio >= 1.**"
The engineer who open-sourced it calls it "my favorite" option and it is used on Flickr album
pages. ([Flickr docs](https://flickr.github.io/justified-layout/),
[code.flickr.com](https://code.flickr.net/2016/04/05/our-justified-layout-goes-open-source/))

That is an every-Nth emphasis rhythm *with an aspect-ratio guard*, in production, from 2016. It
is the single closest published precedent to the built system's rhythm feature.

The same config also carries the levers a mint-time pass would need: `targetRowHeight` (320
default), `targetRowHeightTolerance` (0.25 — "`0` would force rows to be the `targetRowHeight`
exactly and would likely make it impossible to justify"), `maxNumRows`, `forceAspectRatio`
(square everything, ignoring the inputs), and split `boxSpacing` for horizontal vs vertical.

**Bento practice is the opposite — curated, and deliberately capped.** The recipes prescribe
"exactly one 2×2 anchor cell", "one or two 2×1 wide cells, the rest 1×1; max 8 cells total"
([Superdesign](https://superdesign.dev/styles/bento-grid)); "most successful implementations use
between 4 and 8 cards. Below four, the layout feels sparse; above twelve, it becomes cluttered"
([Landdding](https://landdding.com/blog/bento-grid-design-by-website-category-where-the-pattern-wins)).
The stated principle is size = hierarchy: "The MOST important content gets the LARGEST box. This
isn't about position … it's about scale."
([SaaSFrame](https://www.saasframe.io/blog/designing-bento-grids-that-actually-work-a-2026-practical-guide))

I found **no** published algorithmic bento generator (treemap or packing based). The only
automation in the bento literature is `grid-auto-flow: dense`, which is backfill, not
composition. **UNVERIFIED / gap in the evidence** — a treemap-adjacent bento generator may exist
in academic or library form; I did not find one in this sweep.

---

## Q6 — What contradicts or complicates the taxonomy

**A live evidentiary conflict about the SaaS exemplars.** Landdding (May 2026) states "Linear,
Vercel, Raycast, and Cursor all use bento layouts on their homepages". Superdesign states the
opposite and claims to have checked: "A note on what is NOT here: Linear, Vercel, Cursor, Notion,
Reflect, and Framer all get cited in bento listicles, and none of them currently run bento
homepages", listing only Apple (MacBook Air), Raycast, Amie and GitHub Copilot as verified live.
My own probe on 2026-08-24: **vercel.com** serves `grid-cols-12` with mixed `col-span-8 / 6 / 3 / 1`
and two `row-span-2` — bento-shaped spans, so the "no bento" claim looks wrong for Vercel at
least. **linear.app** and **raycast.com** ship hashed class names, so my grep found nothing and
that is *not* evidence of absence. Net: the exemplar lists in bento listicles are unreliable;
verify any specific site before citing it to Dave.

**Bento demand may be plateauing.** Superdesign publishes a first-party metric from 208,000+ real
generations: bento fell from 1.55% of prompts in January 2026 to about 1.25% in May, "holding,
not exploding". That is one vendor's prompt telemetry, not the market, but it is at least a
measured number with a stated method.

**Anti-roles — three contexts where the pattern is reported to actively hurt:**
- *Editorial / news.* "A publication's homepage relies on strict hierarchy by date and prominence
  — modular layouts blur that signal rather than clarifying it." Size-hierarchy and
  time-hierarchy fight each other.
- *E-commerce listings.* Shoppers compare on consistent dimensions, so variable card sizes impair
  comparison; Landdding reports retailers reverting to uniform grids. (The quantitative claims
  there — "+31% time on page", "−14% conversion" — cite an unnamed 2025 analysis and should be
  treated as **UNVERIFIED**.)
- *Forms, checkout, onboarding.* Sequential progression; modular layout creates ambiguity about
  what to do next. ([Landdding](https://landdding.com/blog/bento-grid-design-by-website-category-where-the-pattern-wins))
- *Long-form content generally.* "If you find yourself truncating sentences to fit cells, the
  layout is winning and the message is losing." ([Superdesign](https://superdesign.dev/styles/bento-grid))

**A candidate fourth role: the mixed-media portfolio / agency wall.** Photographic and
aspect-driven like GALLERY, but curated and hierarchy-encoding like BROCHUREWARE, and it mixes
project images with capability cards, client logos and awards — "composite arrangements that look
awkward in almost any other layout".
([Landdding](https://landdding.com/blog/bento-grid-design-by-website-category-where-the-pattern-wins))
This is arguably where Dave's GALLERY role actually lives, with true photo walls (Flickr,
Unsplash-style) being a fourth thing outside bento entirely.

**10-foot / TV UI is a genuine counter-case.** Guidance is single rows of 5–7 large cards rather
than dense grids of 20+ thumbnails, a 60pt safe-area inset, and focus predictability — "as long
as the interface adheres to a clear grid-like logic, the movement of the focus tends to align
with user expectations". Variable spans and dense backfill work against that. (search digests
over [Oxagile](https://www.oxagile.com/article/tvos-focus-engine-navigation-guide/) and
[Purrweb](https://www.purrweb.com/blog/how-to-design-an-app-for-smart-tvs/); **UNVERIFIED** —
pages not fetched, and Apple's own tvOS HIG was not consulted.)

**"Equal cells = not a bento."** Worth holding as a definitional test for any generated output:
"If every cell is the same size you have a plain card grid wearing a trendy name, and you have
paid the complexity tax (spans, dense flow, responsive resets) for nothing."
([Superdesign](https://superdesign.dev/styles/bento-grid))

---

## Q7 — Accessibility and responsive notes worth stealing

**Reading order vs visual order is the headline risk.** Stated in near-identical terms by two
independent sources: "`grid-auto-flow: dense` and span juggling reorder cells visually while
screen readers and keyboard focus follow DOM order. If cells contain links or buttons, a
dense-packed bento makes focus jump around the page unpredictably (WCAG 2.4.3 Focus Order, 1.3.2
Meaningful Sequence)." The prescribed fix: "write DOM in reading order and let spans, not dense,
do the layout; reserve dense for non-interactive media tiles."
([Superdesign](https://superdesign.dev/styles/bento-grid); the reordering behaviour itself is
documented at [MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/grid-auto-flow).)

**Text over media needs a per-cell contrast check.** "Every such cell needs its own 4.5:1 check
(WCAG 1.4.3), and the trendy glass-blur cell over a photo is the most common failure. Fix: a
bottom scrim, rgba(0,0,0,0.55) to transparent, under any text on imagery."
([Superdesign](https://superdesign.dev/styles/bento-grid))

**Motion discipline.** The published contract is hover-only, `scale 1.02` plus a soft shadow,
200ms ease-out, "nothing autoplays"; and on Apple's own page, "motion rationed so only the hero
tiles animate". SaaSFrame adds: "Don't animate ALL properties. Choose 1-2 for performance."
Neither source mentions `prefers-reduced-motion` — **gap in the published guidance**, not a
finding that it doesn't matter.

**Container queries are safe to lean on.** Baseline widely available since August 2025 at around
92.6% support (search digest over
[LogRocket](https://blog.logrocket.com/container-queries-2026/) and
[Mantlr](https://mantlr.com/blog/css-container-queries-practical-guide-examples); **UNVERIFIED**
at primary level). More usefully, the reference bento build uses them per tile and gives a
concrete reason: "Managing this with @container queries applies the `aspect-ratio` in a better
way than @media queries." It also switches a tile's own title from column to row at `17.5rem`
container width. ([iamsteve](https://iamsteve.me/blog/bento-layout-css-grid))

**Responsive collapse.** Universal advice: reset spans at breakpoints or mobile becomes an
undifferentiated card stack; relax any fixed row height at one column or `overflow: hidden` will
silently clip cells; and reorder by importance rather than by desktop position. One source goes
further and says cut or merge cells at small sizes rather than stacking everything.
([Superdesign](https://superdesign.dev/styles/bento-grid),
[SaaSFrame](https://www.saasframe.io/blog/designing-bento-grids-that-actually-work-a-2026-practical-guide))
The reference build applies `grid-auto-rows: 1fr` only above 1280px, "a deliberate design choice
— achieving a true bento style layout on smaller screens is difficult with the space constraint".
([iamsteve](https://iamsteve.me/blog/bento-layout-css-grid))

**Two technical guards worth copying verbatim:** `minmax(0, 1fr)` instead of bare `1fr` so long
unbroken content can't blow out a track, and a fixed `grid-auto-rows` so row spans stay
predictable — "auto rows make 2×2 cells collapse unevenly".
([Superdesign](https://superdesign.dev/styles/bento-grid))

---

## WHERE THE HYPOTHESIS HOLDS / WHERE IT BENDS / WHAT'S MISSING

### Holds

**Brochureware, completely.** Radius and gutter on the tile, one uniform gutter, ground on the
tile — that is what Apple's own CSS does and what every practitioner guide prescribes. Apple's
18px is even inside the 20–28px band the community quotes, close enough to call the band real.

**The role split by intent.** The sources independently arrive at the same underlying axis Dave's
taxonomy encodes: parallel exploration (bento works) vs sequential progression (bento fails). The
three roles all sit on the parallel side.

**Size = hierarchy as the load-bearing principle.** Universal across sources, and stated as the
test of whether something is a bento at all.

**Aspect-ratio → span mapping.** Precedented in the strongest possible way: Flickr's algorithm
takes an array of *aspect ratios* as its primary input and derives all geometry from them.

**Every-Nth emphasis rhythm.** Precedented as `fullWidthBreakoutRowCadence`, with an
aspect-ratio guard, in a shipped open-source algorithm.

**Container-query bands.** Precedented in the reference build, for exactly the reason the built
system needs them (per-tile aspect switching), on a feature that is Baseline widely available.

### Bends

**"Gallery = bento with ragged edges tolerated."** Real photo walls do not use spans and do not
tolerate ragged *sides* — they justify every row to full width and vary row height instead.
Raggedness is confined to the last row, and even there it is a named, switchable decision
(`showWidows`) rather than an accepted look. If the built GALLERY role is a span grid, it is
doing something different from what Flickr, and the layout family it named, actually do.

**"Dashboard = near-zero (1px) internal spacing."** No published dashboard guidance supports it;
several sources warn against sub-12px gutters. The pattern is nonetheless real and Apple-shipped
under a different name (inset grouped lists), and the platform is adding first-class support for
keyline-in-gap (`row-rule`/`column-rule` for grid). So this reads as an *unusual but defensible
choice with no bento precedent*, rather than a documented dashboard convention.

**"Radius on the section container."** Same status. Concentricity gives it a rigorous rule
(inner = outer − padding) and Apple explicitly warns that nested containers are where pinched or
flared corners show up. But nobody frames this as a bento variant.

**"Squaring eliminates orphans."** Bento practice solves the hole problem by *reordering*
(`dense`), not by resizing. Squaring by span adjustment is arguably better — it keeps DOM order
intact and therefore keeps focus order intact — but it is not the industry method, so there is no
body of practice to lean on.

**The exemplar roster.** The commonly-cited SaaS bento sites do not reliably still run bentos.
Cite specific pages only after checking them.

### What's missing

- **No published algorithmic bento generator.** Nothing treemap-adjacent, nothing packing-based.
  The built system's mint-time pass appears to have no public counterpart in the bento literature.
- **No `prefers-reduced-motion` guidance in any bento source.** The motion contracts are all
  about duration and property count, never about the reduced-motion query.
- **Per-theme gutters (0 flush vs 24) have no precedent I could find.** The literature treats one
  uniform gutter as constitutive of the look and says mixed gutters kill it — but "mixed" there
  means mixed *within one grid*, which is not what per-theme gutters do. Nothing addresses gutter
  as a theme variable.
- **Nesting (bento-of-bentos) is essentially undiscussed.** The only nesting guidance anywhere is
  Apple's concentric-shape-with-fallback-radius, which is about a component that must work both
  nested and standalone — a direct analogue, but from controls, not layout.
- **Contradictory / soft evidence I could not settle:** whether Linear/Cursor/Notion run bentos;
  the quantitative conversion and time-on-page figures; Datadog/Mixpanel as in-app bento
  examples; Material 3's shape page (search digest only); tvOS specifics (Apple's own tvOS HIG
  not consulted).

---

## Implications for the built system — observations, not rulings

1. **The DASHBOARD role's flush/container-radius signature has no bento precedent but a strong
   Apple one.** An observation worth weighing: framing it as *concentric nesting* rather than as
   *a bento variant* would connect it to a rule Apple states explicitly and a formula the wider
   community already teaches — and would give the nested-radius derivation a citation.

2. **If the container carries the radius and tiles sit flush, concentricity implies the inner
   radius should be the container radius minus the gap, not zero or a fixed token.** At a 1px
   internal gap the difference is negligible; at any larger gap it is visible. Apple names the
   symptom as corners that "feel too pinched — or flared".

3. **A mint-time squaring pass that adjusts spans avoids the accessibility trap that
   `grid-auto-flow: dense` creates.** That is a genuine advantage over industry practice and
   might be worth stating as such — dense backfill is the published method and it is the one
   thing every source warns about.

4. **The GALLERY role may be two things.** The mixed-media portfolio wall (curated, hierarchical,
   bento-shaped) and the photography feed (justified rows, aspect-driven, widow-managed) behave
   differently. If the system serves both with one role, the justified-row family's parameters —
   target row height, tolerance, widow handling, box spacing split by axis — are the ones it
   would need and currently may not have.

5. **`fullWidthBreakoutRowCadence`'s aspect guard is worth noting beside the every-Nth rhythm.**
   Flickr only promotes an item to full-width if its aspect ratio is ≥ 1. An emphasis rhythm
   that promotes a portrait tile to a wide slot will crop or letterbox it.

6. **Orphan policy might deserve to be a parameter rather than a role property.** Flickr's design
   makes it a switch (`showWidows`) available in every context; the built system currently ties
   squaring to the dashboard and brochure roles. Both readings are defensible; the observation is
   only that the canonical implementation kept it orthogonal to layout family.

7. **Per-theme gutters of 0 and 24 sit at, and just past, the two ends of the published range.**
   Practitioners put the merge threshold around 8–12px and the isolation threshold around 32px.
   A 24px gutter is inside the band; a 0px gutter is outside it, which is exactly why the keyline
   does the work the gutter would otherwise do.

8. **CSS gap decorations are worth watching for the flush regime.** `row-rule` / `column-rule` on
   grid, with `repeat()` patterns and `*-rule-break: spanning-item`, would draw keylines between
   flush tiles without pseudo-elements or extra DOM. Developer-trial only in Chrome/Edge 139 as
   of the source's writing, so not shippable — but it is the standards-track answer to the exact
   thing the dashboard role is doing by hand.

9. **The container-query bands (1100/820/520) are on solid ground**, and the reference build
   suggests a second use for them the system may already exploit: switching a tile's internal
   layout (title stacking, image aspect) at its own width rather than the page's.

10. **"Equal cells = not a bento" is a testable output property.** If a mint-time pass ever
    squares a grid into uniformity, the result stops being a bento by the definition the
    literature uses.

---

## Sources fetched (primary reads)

1. https://developer.apple.com/videos/play/wwdc2025/356/ — Apple, WWDC25, concentricity + three shape types (full transcript)
2. https://www.apple.com/v/macbook-air/z/built/styles/main.built.css — Apple's live tile CSS (radius 18px, white ground, shadow)
3. https://flickr.github.io/justified-layout/ — full config table incl. `showWidows`, `fullWidthBreakoutRowCadence`, `targetRowHeightTolerance`
4. https://code.flickr.net/2016/04/05/our-justified-layout-goes-open-source/ — algorithm description and history
5. https://github.com/flickr/justified-layout — README, `widowCount` in output
6. https://superdesign.dev/styles/bento-grid — recipe, verified-live exemplars, a11y traps, prompt-share telemetry
7. https://www.saasframe.io/blog/designing-bento-grids-that-actually-work-a-2026-practical-guide — gutters, base-unit formula, card anatomy
8. https://iamsteve.me/blog/bento-layout-css-grid — reference build with container queries and dense flow
9. https://landdding.com/blog/bento-grid-design-by-website-category-where-the-pattern-wins — category fit and anti-roles
10. https://medevel.com/bento-grid-is-not-masonry-heres-why-and-what-to-use-when-a-quick-guide-for-ui-ux-designers/ — bento vs masonry distinction
11. https://developer.chrome.com/blog/gap-decorations — CSS gap decorations, `row-rule`/`column-rule`, css-gaps-1
12. https://developer.mozilla.org/en-US/docs/Web/CSS/grid-auto-flow — dense packing semantics
13. Live probes 2026-08-24: vercel.com (grid-cols-12, mixed col-spans, row-span-2), linear.app (hashed classes — inconclusive), raycast.com (hashed classes — inconclusive)

**Cited from search digests only (not fetched — treat as second-hand):** Cloud Four and dev.to on
the concentric formula; Apple `insetGrouped` docs; Material 3 corner radius scale; Grafana /
designmd / Pencil & Paper dashboard spacing; Justified Image Grid widow settings; LogRocket and
Mantlr on container-query baseline; Oxagile and Purrweb on tvOS/10-foot UI.
