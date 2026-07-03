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
10. ✅ `foundations-and-identity/Tone_of_Voice.html` + 9 subpages → `tone-of-voice.md`
    UPGRADED to engine era (tov-001…051, 2026-07-02). THE REGISTER SOURCE: intelligent-wit
    gradient = the temperature dial with a receipt (tov-016 [REVIEW] — charter band-mapping
    is Dave's ruling); FK readability numbers (70+/grade ≤7 + per-artefact table); web copy
    numerics (<15-word sentences, ≤3 sentences/para); ~8 lint-list families (formal→human
    ×17, hedges, throat-clearers, hard-sell, euphemisms, coded language, subjective
    adjectives, spam triggers — canon pre-swept, 0 signals); greetings/sign-off matrix by
    LOB; neuro-024 RECONCILED (literalness partition, F2). DISCOVERY: Copywriting is a hub
    of 4 sub-resources, NOT descended — queued below as item 10a. Raw snapshots:
    `_sources/tone-of-voice/` (before-and-afters interactive = partial capture, accepted).
10a. ✅ **Copywriting family** — all 4 pages → `copywriting.md` (copy-001…059,
    2026-07-02). THE COMPONENT-MICROCOPY LAYER: per-component antiPattern harvest
    mapped (its F1) — Buttons, Links (next ★), Notifications, Modal, Progress
    tracker, Input-fields (supercharge), Dropdown country selectors. Fixture-data
    formats receipted (currency-no-space, minus-before-unit, DD Month YYYY, 24h
    clock). Strongest new gate candidate: copy-016 no-full-stops-in-microcopy
    (exact, cost-0, pre-swept clean); 1 canon signal found total (Selection-controls
    ampersand, copy-022 — fix at next touch). 1 [REVIEW]: copy-014 meta-title
    start-case exemption vs sentence-case/all-caps gates. Preferred terms (~120
    pairs) + Chinese list + HK-Legal regional labelling captured VERBATIM in
    `_sources/tone-of-voice/` for retrieval-not-recall. Raw snapshots:
    editorial-style-guide.txt, preferred-terms.txt, preferred-terms-chinese.txt,
    regional-labelling.txt.
11. ✅ `foundations-and-identity/colour.html` + 3 subpages (brand-colours, illustration,
    data-visualisation) → `colour-usage.md` UPGRADED to engine era (col25-001…020,
    2026-07-02) with the 2025→2026 DELTA MAP. HEADLINE (F1): **blue/400 (#4587A7) =
    illustration blue-5 verbatim** — the dark-RAG/focus-ring leak receipted at value
    level; published UI blue = RAG #305A85 (= blue/600); fix = derive from blue/600
    (col25-018 REVIEW). Token store = 2025 standard value-exact (F2, provenance
    receipt). 3 more REVIEWs: text/secondary Grey 7 vs page's Grey-8-only
    (col25-011) · red-in-charts vintage FLIP (col25-016) · B&W-photo ban carry
    (col25-008, low). Raw: `_sources/colour-2025/`.
12. ✅ all 7 pages → `visual-assets.md` (va25-001…027, 2026-07-02). **TIER 1 COMPLETE.**
    Queue mis-tiered it: visual-assets.html is a UX application standard — imagery
    budget per page-type (va25-003, the imagery calm-ceiling), empty-state/
    confirmation asset-type consistency (va25-005), icon SEMANTIC-fit (va25-007),
    masthead logo behaviour contract (va25-015 → Headers), avatar rounding =
    code-mask-on-square (va25-013). no-genAI ban proven VINTAGE-STABLE (va25-018 ↔
    photo26-002). F1: Logos/Photography "2025" pages already refresh-contaminated —
    page vintage labels can't be trusted; brand-refresh-assets.md stays operative on
    overlaps. 0 new REVIEWs. Raw: `_sources/visual-assets-2025/`.
    DISCOVERED (→ Tier 2/3): video sub-standards ×6 (creative/media-types/patterns/
    subject/technical/interactive) · favicon guidelines · photography type standards
    ×5 (cinematic, landscape-aerial, studio, products-lifestyle, textures) · hexagon
    subpages (Iconic/Open/Cropped + graphic-treatments — treatments fills the bra26
    "coming soon" gap) · brand architecture · identifiers · third-party
    relationships · Brand Effect Model · visualising-climate-ambitions.

## Tier 2 — processes + digital guidance (after T1, per-tranche decision)

### Done
13. ✅ `processes-and-tools/Design-Standards.html` + `Toolkits.html` +
    `Component-Libraries.html` → `design-system-processes.md` (dsp-001…013, 2026-07-03).
    The three-layer model = our architecture, named by the source (F1); provenance
    retention is upstream policy (F2). DISCOVERED (→ below): standards anatomy/process ·
    toolkit anatomy/process.
14. ✅ `processes-and-tools/Naming.html` → `naming.md` (nam-001…018, 2026-07-03). Two
    cost-0 sweep candidates: nam-001 possessive `HSBC's`+name, nam-002 all-caps names
    (advisory-first, Dave may straight-to-block). Key documents are staff-only — source
    boundary. DISCOVERED: Naming a chatbot · WeChat Standards · social media standards.
15. ✅ `processes-and-tools/Digital_Governance.html` → `digital-governance.md`
    (gdea-001…008, 2026-07-03). gdea-003: certified reuse is EXEMPT from re-approval —
    the institutional argument for the certified-component model; audit→fix→RETEST +
    named risk acceptance mirrors the known-signature discipline (F2).

### Queued
The **Common Toolkit** — RULED 2026-07-03 (Dave): his "Gaps and edits" branch
`Cgbtrmfp15ruNFkIAClpkI` is faithful → USE IT as the source (prior use was ad hoc, this
pass is rigorous). Library index = "HSBC Common Toolkit (MCP)" via `search_design_system`
(component sets in On Light/On Dark pairs, guide frames `00 …`, semantic-color variables
incl. `(depricate)` families); branch file metadata exposes only a Cover page, so survey
via library search + the create.hsbc toolkit pages as enumeration skeleton. NOTE: an
earlier session left a probe-results text node on the branch Cover — Dave to delete. ·
`accessibility/digital-accessibility-framework.html` · `accessibility/testing-and-auditing.html` ·
`accessibility/creating-accessible-content.html` ·
`platforms-and-channels/presentations.html` + `introduction-to-document-accessibility.html` +
`accessible-pdf-requirements.html` · `email.html` · `web/design-toolkits.html` ·
`app/design-toolkits.html` · `web/sharepoint-accessibility-guidelines.html` ·
`accessibility/communication/…scenario-4-digital-content` (exact URL TBD — hub captured
2026-07-02; likely WCAG/neuro overlap, low priority) ·
DISCOVERED 2026-07-03: Design Standards anatomy · Design Standards process · Design
Toolkit anatomy · Design Toolkit process · Naming a chatbot · WeChat Standards · social
media standards (hashtag approval).

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
