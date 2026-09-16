# Tone of voice — brand guidance (ingested)

*Source: create.hsbc → Foundations and identity → `Tone_of_Voice.html` + 9 subpages,
captured 2026-07-02 via Dave's authenticated session (login-walled; ADR-0005 clearance).
Engine-era format — SUPERSEDES the 2026-06-18 RAG-era summary of the hub page. Raw
snapshots + capture-status table: `guidelines/_sources/tone-of-voice/`. Source vintage:
pre-refresh authoring (COVID-era examples, Twitter-280 reference) — expect the 2026
refresh to re-cut this family; per the living-standard stance, deltas ≠ defects.
The Copywriting sub-family (Editorial style guide ~43k chars, Preferred terms ×2,
Regional labelling) was ingested 2026-07-02 as its own engine-era file —
`copywriting.md` (copy-001…059), the component-microcopy layer promised at F8.*

## Scope note — this is the register dial's source

This standard is the text-side twin of the neurodiversity layout numbers: it defines
**what the voice is** (four principles), **how far expressiveness may travel per
situation** (the intelligent-wit gradient — the empirical basis for the fixed/flex
charter's register *temperature* dial), and **deterministic, checkable copy rules**
(readability scores, sentence/paragraph caps, banned-phrase lists). Per ADR-0005 §5,
new checks enter at ADVISORY and earn promotion by bite-testing. Most of the word-list
rules are precisely statable lint lists — the "fluff with somewhere to bite" case from
the guidance-ingestion thread. Canon swept 2026-07-02: 0 'click' signals, 0 hedge
phrases — the lists arrive at cost 0.

Tag note: [RECORDED] and [PROCESS] rules below are deliberately NON-indexed (kin of
[IN FORCE]) — out-of-engine channels (print/SMS/social) and workflow guidance, kept
for completeness and delta-mapping. BLESSED by Dave 2026-07-03 — canon vocabulary,
documented in `gen_rules_index.py`.

## The four principles (the register frame)

- **The HSBC voice = four principles: Human, Insightful, Confident, Intelligent wit.**
  Together they are the brand's verbal identity — "customers should be able to
  recognise us by how we write and speak" the same way they spot the palette and logo.
  [TASTE — register frame; the vocabulary of the voice itself, all generated copy
  inherits] {#tov-001}
- **The voice does not change by channel; the mechanics do.** "Our voice doesn't
  change, regardless of whether we're writing a letter, email, text or tweet" — channel
  rules (below) tune length and structure, never identity. [TASTE — register frame;
  fixed identity, flex mechanics — direct charter §3 kin] {#tov-002}
- **Voice ownership: anything signed by HSBC (website, UI, brochures, T&Cs) is written
  AS HSBC** — mass communications signed by a person on behalf of the brand still write
  as the brand. [IN FORCE for the engine — all generated copy is brand-signed]
  {#tov-003}

## Human — voice mechanics

- **Say 'we' and 'you'.** First person plural for the bank, second person for the
  reader. "We're writing to you about your current account", never "Today HSBC is
  communicating to all current account customers". [ADVISORY-derivable — third-person
  self-reference scan ("HSBC is/has/will" outside legal contexts)] {#tov-004}
- **Use contractions — single contractions only.** I'm, we'll, you're, can't, won't,
  don't. **Never double contractions** ('wouldn't've', 'shouldn't've'). Writing words
  out in full is allowed for deliberate emphasis ("I will"). [ADVISORY-derivable —
  double-contraction regex is exact; contraction *presence* is TASTE] {#tov-005}
- **Formal→human word substitutions** (merged principles-page + FAQ tables, 17 pairs):
  advise/inform→tell · assist→help · cease→stop · commence→start · continue→carry on ·
  converse→talk · endeavour→try · enquire/request→ask · ensure→make sure · funds→money ·
  obtain/receive→get · provide→give · require→need · therefore→so.
  [ADVISORY-derivable — lint list on generated copy; flag, don't auto-replace
  (legal/product-name contexts exist)] {#tov-006}
- **Plain English, no financial or legal jargon; familiar words wherever possible.**
  Readability is framed as an inclusion measure (age, education, ESL, text-reader
  users, ADD/autism/dyslexia/dyspraxia). [TASTE at generation + tov-008/009 make it
  measurable] {#tov-007}
- **Readability floor: Flesch-Kincaid 70+ / grade ≤7 (reading age 11) as the general
  bar for all writing.** Source calibration: Harry Potter ≈ the bar; Time magazine ≈
  grade 12. [ADVISORY-derivable — FK is deterministic and computable at generation
  time; English-only formula, see Findings F3] {#tov-008}
- **Readability targets by artefact type** (Flesch Reading Ease): internal email
  60–70+ · customer email 60–70+ · customer letter 60+ · social 70+ · report 50+ ·
  technical report 45+ · T&Cs 40+. [ADVISORY-derivable — per-artefact thresholds; the
  T&C/report relaxations = the flex band] {#tov-009}
- **Active voice, not passive.** "We'll send you a closing statement", not "a closing
  statement will be sent". Passive hides the actor and cools the tone.
  [ADVISORY-derivable — passive-construction scan; allow deliberate exceptions]
  {#tov-010}

## Insightful — structure

- **Main point first. Only what the reader needs to know.** What you think the key
  point is and what the reader needs aren't always the same — decide what matters to
  *them* before writing. [TASTE at generation; composition-level kin of neuro-004
  front-loading] {#tov-011}
- **Summary subheadings that carry the key message** — skimmable by design; explicitly
  motivated by a11y (screen-reader navigation, dyslexia/autism) as well as time-poor
  readers. Headings should summarise ("Tougher markets, tighter margins"), not label
  ("Outlook"). [ADVISORY-derivable in part (heading presence/cadence); heading *quality*
  is TASTE] {#tov-012}
- **If something is changing, always say why** — especially unwelcome news; reasons in
  **≤2 sentences**, no regulation or internal-process detail. [ADVISORY-derivable —
  content-contract check at generation ("change" copy must carry a because-clause)]
  {#tov-013}

## Confident — commitment language

- **No hedging: banned commitment-hedge phrases** — 'we're committed to', 'we
  endeavour to', 'we aim to', 'The Board is committed to'. Say what we're doing: "We're
  asking you for this information to protect you…". Hedges "make us appear unreliable
  and non-committal". [ADVISORY-derivable — exact phrase lint list] {#tov-014}
- **Always say what happens next — even when it's 'nothing'.** Every message that
  shares information ends with what to expect; "even if no more action is needed, be
  sure to say that clearly." [ADVISORY-derivable — content-contract check; pairs with
  the confirmation/success gap-pattern] {#tov-015}

## Intelligent wit — THE TEMPERATURE DIAL

- **Wit is a flourish, not a register.** Source, explicitly: "it's more of a flourish
  than something we use throughout – it works best in headlines or when we're giving
  good news." Gradient as stated: **advertising/marketing = dial up · good news +
  headlines = home turf · functional messages = "quite subtle" · important/clear-and-
  straightforward messages = don't distract · difficult situations (bereavement,
  pandemic) = zero.** This is the fixed/flex temperature dial with a source receipt —
  see Findings F1. [RATIFIED — mapping in _FIXED-FLEX-CHARTER §4b ratified as-is
  by Dave 2026-08-21 (`s212-D3`, knowledge/_rulings.json), adopted provisionally
  2026-07-02: expressive = wit ON surface-scoped · balanced = subtle ·
  sober = zero-with-warmth. A future build-time temperature control would be a
  new ruling, not a reopening] {#tov-016}
- **Specific beats generic: use references that resonate with the named audience**
  (UHNW legacy framing vs student 'pop into a branch'). No two audiences the same.
  [TASTE at generation — audience parameter feeds example selection] {#tov-017}
- **No clichés or stock expressions** ("24 hours a day, 7 days a week" = "a cliché any
  bank could use"). Fresh perspective instead. [ADVISORY-derivable — starter cliché
  lint list, grow by review] {#tov-018}
- **Colloquialisms show local expertise — BUT functional messages stay literal.**
  Source, verbatim: "neurodiverse readers may interpret language very literally. So
  stick to clear, unambiguous phrases in functional messages, or when telling readers
  to take an action." Reconciles neuro-024 — see Findings F2. [TASTE — register
  calibration; colloquialism licence is expressive-band only, functional/action copy =
  literal band] {#tov-019}
- **Transcreation, not translation** for colloquial content; local sense check;
  if a colloquialism won't translate, simplify. [PROCESS — out of engine scope,
  recorded] {#tov-020}

## Inclusive language

- **Don't define the audience too narrowly** — readers have overlapping identities
  (race, nationality, orientation, gender identity, parenthood, neurodiversity,
  disability, ESL). [TASTE at generation] {#tov-021}
- **Gender-neutral defaults: no gendered titles when unknown (use 'Hello [Name]');
  -person job titles (chairperson, businessperson, police officer); gender-neutral
  social roles ('parents/caregivers', not 'mothers'); they/them until told
  otherwise.** [ADVISORY-derivable — gendered-title + -man/-woman suffix lint]
  {#tov-022}
- **Coded-language ban list**: blacklist/whitelist → blocklist/allowlist ·
  master-/slave- → primary/secondary · 'long time no see' → 'it's been a while' ·
  'ethnic' as qualifier → name the actual group/market · 'illegal immigrants' →
  'undocumented person'. [ADVISORY-derivable — exact lint list; NB blocklist/allowlist
  is already house code-style] {#tov-023}
- **No umbrella terms (BAME, BME, catch-all 'Asian'); name communities properly;
  capitalise Black as ethnic/cultural adjective (AP style).** [ADVISORY-derivable —
  term list] {#tov-024}
- **Vary example names and cultural references in placeholders, pre-populated fields,
  and scenario copy** across cultures, backgrounds, faiths. ENGINE-CRITICAL: this is a
  rule about *generated fixture data* — our snippet/gallery placeholder names are in
  scope. [ADVISORY-derivable — fixture-name diversity check; see Findings F8]
  {#tov-025}
- **People-first language: person with a disability · has epilepsy, never 'is an
  epileptic' · never 'suffers from' · 'a reader over 65', never 'elderly'.** Identity-
  first accepted where communities choose it (autistic, Deaf); person-first when
  unsure. [ADVISORY-derivable — phrase lint list] {#tov-026}

## Situation playbooks

- **Unwelcome news: MORE human, not more formal.** Formality under stress is named as
  a misconception that "harms the customer experience". Readability stays at grade ≤7;
  don't dress bad news as good news or force a positive. [TASTE — register
  calibration; sober register keeps warmth, stress ≠ stiffness] {#tov-027}
- **Sorry once, early, plainly — and only for things we control.** "We're sorry for
  the mistake." Banned insincere apologies: 'we apologise for any inconvenience
  caused' · 'please accept our sincerest apologies' · 'regretfully, mistakes were
  made'. No apology for regulatory/market changes. [ADVISORY-derivable — apology
  lint list + apology-count check] {#tov-028}
- **No throat-clearing openers**: 'It has come to our attention…' · 'Following a
  recent review…' · 'As you'll be aware…'. Main point early; for very bad news a
  one-line preparatory frame is allowed ("We're writing to let you know that…") — and
  the main message may sit in the heading/subject itself. [ADVISORY-derivable —
  opener lint list; see Findings F5 for the lead-vs-frame reconciliation] {#tov-029}
- **Unwelcome news ends with options + a warm route in**: when the change hits, what
  impact, what to do with questions, alternatives (switchable accounts, nearby
  branches), prominent placement, never an abrupt ending. [TASTE + content-contract
  kin of tov-015] {#tov-030}
- **Sensitive subjects: no euphemisms.** 'Has died', not 'passed away'; the person's
  name, not 'the deceased'/'your late husband'. Plain and warm, not sentimental
  ("insincere coming from a bank"); euphemisms are also a literalness barrier
  (neuro-024 receipt). [ADVISORY-derivable — euphemism lint list] {#tov-031}
- **Internal comms: same standards + Smart Brevity numbers — updates <300 words,
  paragraphs 1–2 sentences, open with "What's new" / "Why it matters", sentences <25
  words, subheading every 3–4 paragraphs.** [ADVISORY-derivable — all five are
  countable] {#tov-032}
- **Good news: no self-congratulation.** Banned: 'you'll be delighted to know' +
  subjective adjectives 'amazing', 'fantastic', 'brilliant' ("salesy and
  presumptuous"). Let the benefit speak. [ADVISORY-derivable — lint list] {#tov-033}
- **Calls to action: one message per communication; open AND close with the CTA;
  signpost with action headings ('What to do now'); consequences stated as fact, not
  threat; specific deep links, not homepages; numbers + hours in body text, never
  small print; avoid asterisks/small print generally.** [ADVISORY-derivable in part
  (CTA-position, asterisk scan); ENGINE-relevant to the action-bar + CTA patterns]
  {#tov-034}
- **Hard-sell ban list**: 'simply' (as in 'simply visit') · 'Did you know…?' ·
  'remember'/'don't forget' · 'Hurry!' · 'Free!' · 'Dear Valued Customer'.
  [ADVISORY-derivable — exact lint list] {#tov-035}
- **Process guidance: soften imperatives ('You'll need to…'), warm form-field labels
  ('Your details', not 'Account holder's details'; 'Please tell us', not 'Please
  indicate'), steps in the customer's question-order, say where they are in the
  process.** ENGINE-CRITICAL: form-label warmth + progress-location are component
  rules (Input-fields, Progress trackers). [ADVISORY-derivable — label-pattern lint;
  cross-index to components] {#tov-036}
- **Forms & attachments: first person; active; ≤2 enclosures; label variable parts
  (page/section refs); summary paragraph atop long documents; pre-populate what we
  know; boxes not lines; return-checklist; benefit-framed instructions.**
  [ADVISORY-derivable in part; forms-component kin] {#tov-037}

## Channel mechanics

- **Device-agnostic language: 'select', never 'click'; never describe UI visually.**
  Writing must work on desktop, mobile, tablet. Canon swept 2026-07-02: 0 signals.
  [BLOCKING-derivable — exact, cost-0, kin of the all-caps gate; enters ADVISORY per
  ADR-0005 §5] {#tov-038}
- **Email: subject carries the why in <8 words; spam-trigger words avoided ('Free',
  'Email', 'Buy', 'Cash', '100%', 'Income'); two-scroll length cap; CTA at open and
  close.** [ADVISORY-derivable — countable] {#tov-039}
- **Letters: open with a summarising heading; signed by a person who can respond
  directly, else a team.** [RECORDED — print channel, engine-adjacent] {#tov-040}
- **Social: character limits are limits not targets; no stock responses; name people;
  always say what happens next on enquiries.** [RECORDED — social channel out of
  engine scope; vintage: pre-rebrand "Twitter/280"] {#tov-041}
- **Texts: brutal edit; one action per message; explain why if space allows.**
  [RECORDED — SMS channel, engine-adjacent] {#tov-042}
- **Web/PDF: sentences <15 words; ≤3 sentences per paragraph; F-pattern layout
  awareness (key content top-left, never bottom-right); more subheadings than print;
  subheadings summarise the paragraph below.** ENGINE-CRITICAL: these are the copy
  numbers for every generated screen. [ADVISORY-derivable — countable at generation;
  the sober register's text-density numbers, joining neuro's ≤4 sentences/para and
  ≤240 chars/sentence — see Findings F6 for the delta] {#tov-043}
- **Greetings/sign-offs matrix by line of business**: Retail letter 'Dear [first
  name]'/'Yours sincerely' · Retail email 'Hello'/'Thanks' · Retail text 'Hi [first
  name]'/'Thanks or thank you' · PB + CMB/GBM letter 'Dear [preferred name]'/'Yours
  sincerely' · PB + CMB/GBM email 'Hello'/'Thank you' · PB + CMB/GBM text 'Dear
  [preferred name]'/'Thank you'. Team sign-offs ('Your HSBC Advance Team') unless a
  named person can respond directly. Name unknown → drop the salutation entirely.
  [ADVISORY-derivable — template contract for generated comms surfaces] {#tov-044}

## Formality scale + markets

- **The voice sits mid-scale on formality — never slang, never old-fashioned — so it
  can adapt per market.** Named calibrations: Australia = most informal · France/
  Argentina = more traditional (vous/vos) · India/Malaysia = "a few degrees towards
  formal" (social hierarchy). Clarity always outranks the local adjustment.
  [TASTE — register calibration; the market/locale axis of the temperature dial —
  a parameter, not a new register] {#tov-045}
- **No idioms where non-native speakers may miss them**: 'get started', not 'get the
  ball rolling'. Local spelling/terminology honoured (cheque/check; Secure Key/
  Security Device HK). [ADVISORY-derivable — idiom lint list seed; third neuro-024
  receipt] {#tov-046}

## Process (recorded, engine-adjacent)

- **Brief-first: audience / channel / know / feel / do — "only start writing when you
  have the answers."** Direct kin of our criteria-contract (①scoping). The 'feel'
  axis (informed/inspired/valued/reassured — never confused/angry/ignored) is a
  usable generation parameter. [RECORDED + cross-index to _RUNBOOK-criteria-contract]
  {#tov-047}
- **Review feedback splits into content / structure / tone**; customer-facing copy
  gets Compliance (customer protection + not-misleading) and Legal review; 2–3 days
  per round. [RECORDED — governance receipt for the harness's human-gate tiering]
  {#tov-048}

## Receipts (evidence, not rules)

- **£1.2m saved on one letters→texts project (£381k mailing alone); 6× response
  rate; £89,212 from rewriting 15 letters** — tone of voice as bottom-line case.
  Useful for the transformation-strategy strand. {#tov-049}
- **"Legal… prefer when we do": plain language is the *lower*-risk option** — jargon,
  passive voice and dense paragraphs are where legal trouble lives. Kills the
  "compliance wants formal" objection at source. {#tov-050}
- **Lead with bad news: readers "don't want to dig"; burying it reads as defensive
  and gets missed.** {#tov-051}

## Findings

- **F1 — The temperature dial has its source.** tov-016's wit gradient (marketing →
  good-news/headlines → functional-subtle → important-zero → difficult-zero) + tov-045's
  mid-scale formality anchor + tov-027's stress-≠-stiffness rule together give the
  fixed/flex charter's *register temperature* dial an empirical, quotable basis.
  → RULED (provisional) 2026-07-02: mapping enacted at `_FIXED-FLEX-CHARTER.md` §4b
  (expressive = wit ON surface-scoped · balanced = subtle · sober = zero-with-warmth;
  locale = parameter). tov-016 stays REVIEW-tagged — Dave flagged it may need
  adjusting once a separate build-time temperature control exists.
- **F2 — neuro-024 reconciled.** Literalness now has THREE tone-of-voice receipts:
  tov-019 (colloquialisms never in functional/action copy), tov-031 (euphemism ban),
  tov-046 (idiom ban for ESL). The tension queued at ingestion (brand wit vs neuro
  literalness) resolves cleanly: **expressive licence is surface-scoped (headlines,
  good-news, marketing), literalness is function-scoped (actions, instructions,
  warnings)** — not a contradiction, a partition. → `_RECONCILIATION.md` entry.
- **F3 — Readability is computable.** FK scoring (tov-008/009) is deterministic —
  textstat-class implementation, zero render cost. English-only formula; bilingual
  surfaces need the locale axis anyway (tov-045). → gate candidate: ADVISORY
  readability check on generated copy blocks, per-artefact thresholds from tov-009.
- **F4 — Three cost-0 lint families arrive pre-swept.** Device-agnostic 'click'
  (tov-038, 0 canon signals), hedge phrases (tov-014, 0 signals), hard-sell list
  (tov-035). Same playbook as all-caps: encode → advisory → bite-test → promote.
  tov-038 is the strongest BLOCKING candidate (exact match, no false-positive
  surface).
- **F5 — Internal tension, reconciled reading.** FAQ says "lead with the bad news"
  (tov-051); how-to allows a preparatory frame for very bad news (tov-029). Read
  together: the main point lands in sentence one either way — framed ("We're writing
  to let you know that X") or bare (X) — and never buried. No review item needed.
- **F6 — Web copy numbers vs neuro numbers, small delta.** tov-043 says ≤3 sentences/
  paragraph (web); neuro caps say ≤4 sentences/paragraph. Tighter rule wins per our
  precedence convention (both ADVISORY; flag at 4, fail nothing yet). Sentence caps
  don't conflict (<15 words ≈ well under 240 chars).
- **F7 — Vintage.** Pre-refresh authoring throughout (COVID examples, Twitter 280,
  2021-dated worked examples). The refresh's tone re-cut (if any) lands via the
  reconciliation register; these IDs are stable for delta-mapping.
- **F8 — Component cross-index.** tov-025 (fixture-name diversity) touches gallery
  fixtures; tov-036 (label warmth, progress location) → Input-fields + Progress
  trackers; tov-034 (CTA open/close, no small print) → action-bar gap-pattern +
  Buttons; tov-044 (greetings matrix) → any comms-surface pattern; tov-015 (say
  what happens next) → confirmation/success gap-pattern. DELIVERED 2026-07-02:
  `copywriting.md` deepens every one of these — see its F1 antiPattern harvest map
  (copy-030…048, per-component).
- **F9 — Trivial source inconsistency.** Drop-in clinics "weekly" (faqs.html) vs
  "fortnightly" (howitworks.html). Noted in `_sources/`, no action.

## Coverage

| Page | Captured | Distilled |
|---|---|---|
| Tone_of_Voice.html (hub) | ✅ | tov-001…003 frame |
| ourtoneofvoice.html (principles) | ✅ | tov-004…020 |
| Everythingtoeveryone.html (inclusive) | ✅ | tov-021…026 |
| Whyitmatters.html | ✅ | tov-049 receipts |
| Copywriting.html | ✅ hub + 4 subpages | `copywriting.md` copy-001…059 |
| howitworks.html | ✅ | tov-047…048 |
| beforeandafters.html | ◐ interactive, 'before' only | examples, none needed |
| How-to-guides.html | ✅ | tov-027…044 |
| tone-of-voice-training.html | ◐ stub/course | none (training content) |
| faqs.html | ✅ | tov-045…046, 050…051 |
