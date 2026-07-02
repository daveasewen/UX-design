# Create.hsbc ingestion queue — standing workstream

*Mapped 2026-07-02 via Dave's authenticated session (nav-hub crawl; no sitemap.xml exists).
Ruling (Dave, 2026-07-02): everything is potentially valuable for the "designer in a box" and
may shape the flex dials — but STAGED: standards + foundations first, decisions per tranche.
Provenance stance: distillations tracked in repo with provenance headers; raw page text never
stored (ADR-0005 open item carries the wider ruling). Every ingested rule gets a stable ID
(`{#prefix-nnn}`) and enforcement-destiny tag; `_rules-index.json` is generated from these.*

Status: ☐ queued · ◐ partial · ✅ ingested · ✖ skipped (reason)

## Tier 1 — standards + foundations (rule-bearing; ingest first)

### Done
- ✅ `foundations-and-identity/data-visualisation-foundations.html` → `data-visualisation.md`
- ✅ …`/bar-charts.html`, `/pie-charts.html`, `/line-chart.html` → companions
- ✅ `brand-refresh/colour.html` + `colour/brand-palette.html` + `colour/supporting-palette.html`
  → `colour-standards-2026.md`
- ✅ `foundations-and-identity/illustration.html` + `illustration/style.html`
  → `illustration-standards.md`
- ◐ `platforms-and-channels/Accessibility_Standards.html` — thin page, captured (WCAG 2.2 AA
  basis, matches ADR-0004); merge into `digital-accessibility-standards.md` provenance note
- ◐ `foundations-and-identity/typography.html` — `typography-usage.md` exists; verify which
  version it distilled, re-check against the 2026 refresh page

### Queue (engine-relevance order)
1. ✅ `foundations-and-identity/icons-and-pictograms.html` + `…/Icons.html` +
   `…/pictograms.html` → `icons.md` (UPGRADED to engine era, 17 rules) + `pictograms.md`
   (new, 14 rules). Resolved col26-007 (4.5:1 icons / 3:1 pictograms / 3:1 indicators by
   asset class); 3 new [REVIEW]s: icon 4.5:1 gate delta, 12px-xsmall vs 16px floor,
   36-vs-48 max; pictograms flagged as component-library gap
2. ✅ `foundations-and-identity/motion.html` + `motion/motion-specifications.html` →
   `motion-standards.md` (7 rules). Headline: "deliberate not playful/bouncy" tension with
   our promoted spring physics → mot-007 [REVIEW], noted in `_PROMOTION-QUEUE.md`; >5s
   play/pause rule (WCAG 2.2.2 class) is a clean gate candidate; easing values are
   AE-toolkit-locked (not on the page)
3. ✖ `foundations-and-identity/calls-to-action--ctas-.html` — RE-TIERED 2026-07-02: it's a
   marketing CTA framework (mindset/channel/metrics), not component rules; 4 subpages moved
   to Tier 3. The legacy `calls-to-action.md` (Figma toolkit) remains the component-side
   source; its upgrade will come from the digital toolkits, not this page
4. ✅ `brand-refresh/typography.html` → `typography-standards-2026.md` (9 rules). HEADLINES:
   core typeface is now **Univers Next for HSBC** (+MYing Hei, Univers Next Arabic) — token
   store says Univers → type26-001 [REVIEW], Dave's call; **no uppercase OR italics, sentence
   case** — house rule + G5 all-caps check now brand-source-backed (informs the all-caps
   desk ruling); red type never except toolkit use-cases; ≤2 fonts + bold option. Subpages
   queued: `typography/typefaces.html`, `typography/creative-headlines.html`.
   ✅ `typography/specification.html` ingested same day (type26-010…021): min sizes
   (Latin 12pt/6pt captions, Chinese 14pt), type colour = black/grey/white ONLY, kerning/
   leading numbers, no-justify/no-hyphenate, bilingual mechanics (1:0.85, weight step-up).
   2 NEW reconciliation items: text-on-gradient ban vs charter §4 expressive heroes
   (type26-015!) and leading ratio vs its own examples (type26-016)
   ✅ Subpages ingested 2026-07-02 eve (actual names: `typography/typefaces.html` +
   `typography/creative-headlines.html` under brand-refresh) → type26-022…029. Three
   2025↔2026 DELTAS: centre-align now legitimate (type26-025), subtle overlays permitted
   (type26-026), magnetic-headline construct replaces big-light/small-bold vocabulary
   (type26-029); Ultra Light weight question (type26-023). SAME session: the 2025
   foundations typography family (`foundations-and-identity/typography.html` +
   creative-headline/placement/latin-languages/app_type_scale) → `typography-usage.md`
   UPGRADED to engine era (type25-001…022); 3 cost-0 gate candidates (no-italics,
   no-text-shadow, red-text-role) logged as type25-020
5. ✅ `platforms-and-channels/web/web-foundations.html` + 6 subpages → `web-foundations.md`
   (webf-001…035, 2026-07-02 eve). Elevation levels 0–3 taxonomy; TScale/RScale receipts
   match the store exactly; DISCOVERY: `responsive-forms` redirects to an "Elements and
   patterns" stub — element standards now live in the **Common Toolkit** (webf-017 access
   decision, covers app too); body-leading contradiction (webf-031) feeds type26-016
6. ✅ `platforms-and-channels/app/app-foundations.html` + 3 subpages → `app-foundations.md`
   (appf-001…008, 2026-07-02 eve). Dark-mode + elevation are word-for-word WEB MIRRORS;
   app-specific substance = single type scale (=TScale:1) + iOS Dynamic Type (appf-002)
7. ✅ accessibility hub + `Neurodiversity-Guidelines.html` + 15 subpages +
   `communication.html` → `neurodiversity.md` (neuro-001…045, 2026-07-02 eve). First
   NUMERIC calm-ceiling caps (hero ≤30% height, bright ≤20% screen, ≤2 column layouts,
   ≥20px section whitespace, ≤4 sentences/para, ≤240 chars/sentence, page-length caps) →
   fixed/flex sober-register defaults (neuro-042); :visited RULED (neuro best practice
   adopted, implement at Links touch); small-type cluster RULED dormant-to-refresh
   (neuro-041). DISCOVERY: `communication.html` is a hub of 7 scenario subpages, NOT
   descended — scenario 4 (digital content) added to Tier 2
8. ✅ `processes-and-tools/generative-ai-and-our-brand.html` → `generative-ai-brand.md`
   (8 rules + 2 strategy findings). Data-vis explicitly in gen-AI governance scope; two
   checkpoints (brand review before creation, Living Wall before publication); "avoid
   synthetic-looking output" = the gates' pitch, stated as un-mechanised taste (gai-008
   strategy REVIEW → digital-experience-transformation). Group AI policy pages are
   staff-only Confluence — permanently out of ingestion reach
9. ✅ `brand-refresh/logos.html` + `photography.html` + `creative-hexagons.html` →
   `brand-refresh-assets.md` (logo26/photo26/hex26/bra26, 2026-07-02 eve). HEADLINES:
   **no gen-AI / CGI / mixed-media imagery** (photo26-002 — pipeline-critical: library
   retrieval only, never synthesis); logo ≥1× per journey (journey-gate candidate);
   Masterbrand variant selection rules (dark = full colour negative); hexagon DELTAS —
   Iconic now smaller, Cropped reduced to 1-/2-edge crops (3-/4-edge RETIRED, audit
   legacy hexagon assets); graphic-treatments guidance "coming soon" (source gap)
10. ☐ `foundations-and-identity/Tone_of_Voice.html` — register/flex-dial shaping (charter)
11. ☐ `foundations-and-identity/colour.html` — the 2025 standard (parallel-valid "until
    further notice"; ingest for the delta map old→new)
12. ☐ `foundations-and-identity/visual-assets.html` · `Logos.html` · `photography.html` ·
    `video.html` · `mnemonic.html` · `Creative-hexagons.html` · `sound-identity.html` —
    2025 foundations, lower component relevance

## Tier 2 — processes + digital guidance (after T1, per-tranche decision)
`accessibility/communication/…scenario-4-digital-content` (exact URL TBD — hub captured
2026-07-02; likely WCAG/neuro overlap, low priority) · the **Common Toolkit** (webf-017 —
access decision Dave; now the home of element/pattern standards incl. forms, web AND app) ·
`processes-and-tools/Design-Standards.html` · `Component-Libraries.html` · `Toolkits.html` ·
`accessibility/digital-accessibility-framework.html` · `accessibility/testing-and-auditing.html` ·
`accessibility/creating-accessible-content.html` · `Naming.html` · `Digital_Governance.html` ·
`platforms-and-channels/presentations.html` + `introduction-to-document-accessibility.html` +
`accessible-pdf-requirements.html` · `email.html` · `web/design-toolkits.html` ·
`app/design-toolkits.html` · `web/sharepoint-accessibility-guidelines.html`

## Tier 3 — channels + articles (flex-shaping context; ingest on demand)
ATM/touchscreens · metaverse-VR a11y · conversational banking · branches · cards · events ·
merchandise · social · QR · podcasts · airport programme · partnerships · B2B · WPB ·
MasterbrandCampaigns · marketing-resources · Legacy-standards · newsfeed articles ·
`sustainability-and-the-transition-to-net-zero.html` · about-us pages

## Legacy distillations (pre-engine era — no destiny tags, no rule IDs)

24 guideline files predate the engine-era format (`accessibility.md`, `brand-principles.md`,
`calls-to-action.md`, `colour-usage.md`, `icons.md`, `logos.md`, `platform-web.md`,
`platform-app.md`, `tone-of-voice.md`, `typography-usage.md`, `imagery.md`, `motion`-adjacent
files, etc.). They produce no rules-index entries and no gate failures — by design. When their
source page comes up in the queue, the job is **upgrade, not fresh ingestion**: verify against
the live site (they may be stale — OCR/token-file era), add destiny tags + IDs, keep anything
the site no longer says as explicitly-marked local canon.

## Method (per page)
Capture via authenticated Chrome session → distill EVERY rule (no summarising-away) with
enforcement destiny + stable rule ID → provenance header (URL, date, version if shown) →
xref to existing guidelines/charter/gates → source contradictions logged as [REVIEW], never
resolved silently → regenerate rules index → batch commit. New subpage links discovered
during ingestion get appended to the tier lists here.

## Source questions raised (for Create Direct / Dave)
1. Text+icons 4.5:1 (brand palette page) vs graphics 3:1 (supporting palette page) — which
   governs icons? (`colour-standards-2026.md` [REVIEW])
2. Grey-palette specs "available soon" — recheck cadence?
3. Pie-emphasis exception has no illustration-side content — intended?
