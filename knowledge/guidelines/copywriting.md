# Copywriting — editorial style, preferred terms, regional labelling (ingested)

*Source: create.hsbc → Foundations and identity → Tone_of_Voice → `Copywriting/` family
(4 pages: `Editorial_Style_Guide.html` ~43k chars + `Preferred-terms.html` +
`Chinesepreferredterms.html` + `regional-labelling.html`), captured 2026-07-02 via
Dave's authenticated session (fetch-all method, zero blocked slices). Raw snapshots:
`guidelines/_sources/tone-of-voice/editorial-style-guide.txt`, `preferred-terms.txt`,
`preferred-terms-chinese.txt`, `regional-labelling.txt`. Owners per page: Global
Content discipline (style guide + preferred terms), Content Design team (Chinese
list, internal-use), **HSBC HK Legal (regional labelling — compliance-sensitive)**.
Queue item 10a — the component-microcopy layer promised by tone-of-voice F8.*

## Scope note — the per-component antiPattern layer

Where `tone-of-voice.md` set the register (what the voice is, how far wit travels),
this family sets the **surface mechanics**: literal sections for Buttons, CTAs, Links,
Error messages, Modals, Progress trackers, Hint/Help text, Alt text, Sort options,
plus the fixture-data formats (numbers, currencies, dates, times, phone numbers) every
generated screen needs. Most rules here are exact and countable — the same
cost-0 profile as the all-caps and select/click families. Canon pre-swept 2026-07-02:
**1 signal total** (ampersand in Selection-controls copy, copy-022); 'click' appears
only inside JS event-listener code, which is out of tov-038's copy scope; date/time
fixtures already conform. Per ADR-0005 §5, new checks enter at ADVISORY and earn
promotion by bite-testing. Preferred terms are consumed by RETRIEVAL from the raw
snapshot, not by memorised summary — the fixed/flex charter's retrieval-not-recall
rule applied to vocabulary.

## Global style mechanics

- **UK English is the global standard** — –ise not –ize, colour, fulfil, instalment;
  Oxford Dictionary of English for spelling queries. US English only for US-local
  content for a US-local audience. [ADVISORY-derivable — -ize/-or spelling lint with
  US-locale exemption; locale is a parameter (tov-045)] {#copy-001}
- **Plain English; avoid idiomatic local phrases** (global audience, ESL,
  accessibility); simple, widely recognised words; short sentences and paragraphs.
  Receipt-level restatement of tov-007/046 with the style guide as second source.
  [TASTE at generation — existing lint families carry the checkable part] {#copy-002}
- **Abbreviations: acronyms/initialisms all caps, no full stops or spaces** (HSBC,
  NATO); better-known-than-full-name may stand alone (PDF); otherwise write out first,
  short version in brackets after; don't expect customers to remember acronyms across
  multi-page journeys (usability-testing receipt); Latin abbreviations ie/eg/etc
  lowercase, no stops. [ADVISORY-derivable — punctuated-abbreviation lint (e.g. /
  i.e. / F.A.Q. patterns)] {#copy-003}
- **'An' before vowel-SOUND initialisms** — first letter F, H, L, M, N, R, S or X
  takes 'an' ('an NI number', 'an HSBC credit card', never 'a HSBC').
  [ADVISORY-derivable — exact article-initialism check] {#copy-004}
- **Active voice; passive rarely and deliberately** — passive's one licence: not
  assigning the do-er (used e.g. to avoid blaming the customer, see copy-035).
  Extends tov-010 with the licence cases. [ADVISORY-derivable — same passive scan,
  licence-aware] {#copy-005}
- **Contraction avoid-list (fuller than tov-005):** That'd · It'd · Could've ·
  Must'n've · Should've · That'll · Wouldn't've. Note this bans some *single*
  contractions, extending tov-005's double-contraction ban. [ADVISORY-derivable —
  exact list, merge into the tov-005 lint] {#copy-006}
- **Collective nouns take singular verbs for organisations** ('HSBC is', 'the FCA
  is'); exceptions: sports teams and police take plural (market-dependent).
  [ADVISORY-derivable — 'HSBC are/have' scan is exact; general case is grammar
  judgment] {#copy-007}
- **Hyphens: compound adjectives before a noun (long-term investments); not after the
  noun (for the long term); never with -ly adverbs; ranges NEVER use hyphens/dashes —
  use 'to'** ('Monday to Friday, 08:00 to 20:00', '£4,000 to £10,000'; screen readers
  may not read a hyphen out). [ADVISORY-derivable — range-hyphen scan is exact; the
  rest is grammar judgment] {#copy-008}
- **'That' (essential clause) vs 'which' (extra detail).** [TASTE — grammar judgment,
  flag-only] {#copy-009}
- **Gender: 'chair' not 'chairman'; male/female not man/woman as adjectives; never
  generic 'he' — they/them.** Second source for tov-022's lint family.
  [ADVISORY-derivable — existing gendered-language lint] {#copy-010}
- **Bold sparingly — avoid in body copy.** Screen readers don't distinguish bold
  (meaning conveyed only by weight is lost — risk exposure); bold blocks confuse some
  neurodiverse readers; over-use makes readers skip. Alternatives: front-load the key
  info, single quotes, headings/bullets/steps. ENGINE: generated body/fixture copy in
  scope; component headings are design-system weight, not copy bold.
  [ADVISORY-derivable — strong/b-inside-body-copy scan on generated content blocks]
  {#copy-011}

## Capitalisation

- **Sentence case for sentences, headings and headlines; capitalise proper nouns
  (specific people, places, job titles, HSBC products); common nouns lowercase; no
  capital after colons/semicolons; prefer common nouns over product names.** The
  style-guide statement of the sentence-case regime — brand-source receipt for the
  canon-wide sweep + blocking gate enacted 2026-07-02. Capitalisation is functional:
  clarity, skimmability, tone ("peppering our writing with capital letters makes it
  feel formal, self-important"). [ADVISORY — receipt for the enacted sentence-case
  gate; proper-noun allowlist mechanism at copy-053] {#copy-012}
- **NEVER capitalise whole words** — "no matter how big the font or short the word";
  screen readers announce letter-by-letter; dyslexia differentiation receipt. Third
  brand-source receipt for the enacted all-caps blocking gate (with type26 no-uppercase
  and the desk ruling). [ADVISORY — receipt for enacted G5 all-caps gate] {#copy-013}
- **Title case banned for headlines** ("hard to read… overly formal and old
  fashioned. Not our tone at all") — **ONE exception: meta titles (browser/SEO
  titles) use start case with pipe separators** ('Current Accounts | Everyday Banking
  – HSBC UK'). Meta titles are not a canon surface today; if they ever enter the
  engine, the sentence-case and all-caps gates need a scoped exemption.
  [REVIEW — gate-scope ruling: pre-register the meta-title exemption (or rule meta
  titles permanently out of engine scope) — Dave, cheap] {#copy-014}
- **Product naming register: prefer common nouns** ('our app', not 'the HSBC Mobile
  Banking app'); **HSBC prefix is never mandatory** (Global Brand + Global Brand Legal
  confirmed — no trademark requirement in any scenario); prefix only where ambiguity
  exists or for a deliberate hero moment; over-use is self-promotional AND an a11y
  burden (screen-reader navigation of prefixed lists). [TASTE at generation —
  naming register; fixture-label rule for product names in lists] {#copy-015}

## Punctuation

- **No full stops in: headings · field labels · button names · lists · navigational
  constructions** (unless >1 sentence); no full stop after titles (Mr Thomas).
  ENGINE-CRITICAL: exact, cost-0 check across every generated component's microcopy —
  the strongest new blocking candidate in this family (kin of all-caps and
  select/click). Pre-swept: 0 canon signals. [ADVISORY-derivable — component-microcopy
  full-stop check; promotion candidate after bite-test] {#copy-016}
- **Exclamation marks: rare** — designates surprise/humour/shock, "rare that this
  will be appropriate for HSBC content". Pre-swept: 0 signals. [ADVISORY-derivable —
  count check on generated copy] {#copy-017}
- **'%' symbol, never 'per cent'; no space** (23%). [ADVISORY-derivable — exact]
  {#copy-018}
- **No bracket plurals** ('Select item(s)' → 'Select items' — plural includes one).
  Pre-swept: 0 (only `String(s)` in JS code). [ADVISORY-derivable — exact]
  {#copy-019}
- **Avoid slashes — use 'and'/'or'; if unavoidable, space both sides** (a11y);
  lowercase after a slash except proper nouns ('Countries / regions will benefit…').
  [ADVISORY-derivable — slash-spacing + post-slash-case scan] {#copy-020}
- **Quotation marks: double = verbatim quotes only; single = emphasis AND UI
  navigation references** ("Select 'Cancel' to exit", "Go to 'Offers'") —
  accessibility team receipt: screen readers handle single quotes fine (slight pitch
  change). Quotes-within-quotes = single. Punctuation inside the quote iff the quote
  completes the statement. ENGINE: the single-quote UI-reference convention is the
  house pattern for help/error copy that names buttons or menu items.
  [ADVISORY-derivable in part — double-quotes-around-UI-names scan; rest is grammar
  judgment] {#copy-021}
- **'And' over ampersand; '&' only in CTAs, table headings, or tight space**;
  'Terms & Conditions' keeps its ampersand as a document title (preferred-terms
  cross-receipt: 'T&Cs' only at absolute space minimum). Pre-swept: **1 canon
  signal** — Selection-controls 'Accept terms & conditions' (lowercase running copy,
  not a document title → should be 'terms and conditions'). Fix at next
  Selection-controls touch. [ADVISORY-derivable — ampersand-in-copy scan; 1 signal
  logged] {#copy-022}

## Numbers, currencies, date and time (fixture-data formats)

- **Digits, not words, in digital copy** (1, 2, 3) — scanning + tight-space receipt;
  conversational text may write out 1–9. [ADVISORY-derivable — heuristic, flag-only;
  fixture-data rule] {#copy-023}
- **Thousands commas above 999** (1,000.00 · 50,000,000); localise (Indian numbering:
  first comma after 3 digits then every 2 — 1,00,000; lakh/crore vocabulary); large
  amounts may suffix million/billion/trillion or m/bn/tn when tight ('£50 bn').
  [ADVISORY-derivable — number-format fixture check; locale parameter] {#copy-024}
- **Currency symbol/code BEFORE the amount, NO space** (£500, GBP500 — "a space could
  result in the amount being dropped into a different line"); **codes not symbols when
  multiple currencies share a symbol** (eg $); **minus sign before the entire unit**
  (-£10.00, overdrafts likewise); currency names sentence case (pound, euro, yen).
  ENGINE-CRITICAL: Account-card, Table, transaction-list and payment fixtures.
  [ADVISORY-derivable — exact fixture-format check] {#copy-025}
- **Dates: DD Month YYYY, no ordinals** (1 October 2016); US + Philippines: Month DD,
  YYYY; tight space: 3-letter months (1 Oct 2016); date ranges keep all digits (1985
  to 1986); days written in full, else Mon–Sun 3-letter — never MON, never 'MON.'.
  Canon fixtures already conform ('19 June 2026', '30 Jun 2026').
  [ADVISORY-derivable — date-format fixture check; locale parameter] {#copy-026}
- **Time: 24-hour clock default** (19:56; '20:00 to 06:30'); 12-hour allowed where
  market-prevalent — lowercase am/pm, colon separator (10:25am), ranges with 'to' not
  dashes (JAWS/NVDA receipt); 'midnight'/'midday' wording can beat 00:00/12pm;
  prefer 23:59/11:59pm over ambiguous midnight. [ADVISORY-derivable — time-format
  fixture check; locale parameter] {#copy-027}
- **Phone numbers: global format `+ country code (0) area code number`**
  (+44 (0)20 7991 8888); regional formats for local copy (US hyphenation); no-space
  variants where tap-to-dial matters; position at sentence end for tappability.
  [ADVISORY-derivable — fixture format; mobile-surface note] {#copy-028}
- **Fractions: numeric in tight spaces; spelled out where space allows** — screen
  readers may read '3/4' as 'three, forward slash, four'. [ADVISORY-derivable —
  minor fixture rule] {#copy-029}

## Component microcopy — the antiPattern harvest

- **Buttons: sentence case · no full stops · concise · action verbs (Save, Apply,
  Send) · precise about the action ('Cancel' not 'Delete' for a recurring payment) ·
  preferred terms · NEVER generic 'Find out more'/'Click here' · marketing contexts
  communicate the value of selecting · no jargon · accessible name always matches the
  visible label.** Stakes named by source: unclear labels → anxiety → wrong financial
  decisions → regulatory/reputational risk. ENGINE-CRITICAL → Button antiPatterns.
  Pre-swept: 0 generic-label signals. [ADVISORY-derivable — button-label lint:
  generic-label list + case + punctuation + label/name match] {#copy-030}
- **CTAs: instruction clear for scan-readers**; source examples: Apply now · Continue
  · Download application form · Activate your card · Back to 'Accounts'. Joins tov-034
  (one message, open+close placement). [TASTE at generation + copy-030's lint carries
  the checkable part] {#copy-031}
- **Links: describe the action/destination or document title ('Go to online
  banking') · ≤8 words · no 'Click here' · no end punctuation · download links ALWAYS
  state document type, best practice adds file size · links = navigation + low-priority
  actions, buttons = high-priority actions.** ENGINE-CRITICAL → Links (next ★
  component) antiPatterns — every clause is countable. [ADVISORY-derivable —
  link-label checks: word count, generic-label list, end punctuation, download-type
  suffix] {#copy-032}
- **Bullet lists: start with a capital, NO full stop at end; one sentence per bullet
  max** (split, or commas/dashes); numbered steps when order matters; a
  list-of-links may drop bullets (design feature, not content). → Lists + numbered
  steps in gap-patterns. [ADVISORY-derivable — list-item punctuation check, cost-0]
  {#copy-033}
- **Green ticks highlight benefits/features, two modes:** with bold heading (heading:
  capital start, no full stop; body: capital start, full stop) or without heading
  (capital start, no full stop). → benefits-list pattern; tick icon must come from the
  library per the icon-source rule. [ADVISORY-derivable — pattern contract +
  icon-gate xref] {#copy-034}
- **Error/feedback messages (error · information · warning · success): lead with the
  clear solution — what to do next, not what went wrong; error codes inside a sentence,
  never as title or in brackets ('…quote the error code GH-444.'); keep the tone human
  ('being human', contractions); own our faults ('We're currently trying to fix the
  issue'), passive allowed only to avoid blaming the customer; optional 'please'
  opener; apologise ONLY when it's HSBC's fault or we explained badly — never for
  wrong passwords or 403s** (testing receipt: customers don't expect it; it just adds
  word count). Source 403 wording: "We can't show you this content. You may not be
  authorised to see it." ENGINE-CRITICAL → Notifications antiPatterns; extends
  tov-028's apology rules to the component surface. [ADVISORY-derivable —
  apology-scope lint + error-code-placement check] {#copy-035}
- **Warnings: state the issue AND its effect on the user** ('You won't be able to
  access your accounts between…', not 'Our service will be unavailable between…');
  urgency may scale with seriousness but stays human/conversational; **never 'Warning'
  as the heading** — the heading explains the issue. → Notifications antiPatterns.
  [ADVISORY-derivable — heading-label check is exact; impact-framing is judgment]
  {#copy-036}
- **Success messages: join the customer in the moment** — positive language,
  celebrate (account opened), explain what happens next. Component-side receipt for
  tov-015 → confirmation/success gap-pattern (Batch B, in build).
  [TASTE at generation + tov-015's content contract carries the check] {#copy-037}
- **Modals: title clear + descriptive — never bare 'Are you sure?'; title works
  WITH the CTA options (don't rely on 'submit'/'cancel'); title never repeats the body
  copy; body = succinct clarification; concise despite the extra room** (space is an
  opportunity for tone, not length). ENGINE-CRITICAL → Modal antiPatterns.
  [ADVISORY-derivable — modal-title lint: 'Are you sure' exact, title/body duplication
  check, default-CTA-label check] {#copy-038}
- **Progress trackers: present tense for ongoing ('Processing') · past tense for done
  ('Sent') · past-tense verb, never 'X complete' ('Actioned', not 'Action complete') ·
  descriptive nouns for no-action steps ('Payment details', 'Confirmation') · verbs
  for input/edit steps ('Review', 'Confirm').** ENGINE-CRITICAL → Progress-tracker
  antiPatterns. [ADVISORY-derivable — '-complete'-suffix lint is exact; tense checks
  heuristic] {#copy-039}
- **Hint/placeholder text: DEFAULT IS EMPTY.** Use only where the value is clear —
  data-entry formats ('0.00', 'dd/mm/yyyy', 'eg High Street', example@email.com).
  Never: important info (hint disappears on select; contrast + cognitive/memory a11y),
  'test@email.com', real-looking example names ('Sarah'), 'Please type in…', 'Blank',
  'Text field', or repeating the field label. Error messages catch the edge cases
  instead. ENGINE-CRITICAL → Input-fields antiPatterns (supercharge queue).
  [ADVISORY-derivable — placeholder-content lint; several exact don'ts] {#copy-040}
- **Help text: aim for one sentence; never hyperlinks that take users away from
  completing the form.** → Input-fields/forms antiPatterns. [ADVISORY-derivable —
  link-inside-form-help check is exact] {#copy-041}
- **Contextual help: supplementary only — basic instructions always immediately
  visible; only task-relevant additions; no spatial/visual directions ('Click the
  button on the right' fails responsive layouts AND screen readers).** Extends the
  tov-038 device-agnostic family with a spatial-direction ban. [ADVISORY-derivable —
  spatial-direction lint list ('on the right', 'above', 'below' in instruction copy)]
  {#copy-042}
- **Alt text needed iff the image is more than decorative** — test: "does the copy
  make sense without the image?"; graphs, QR codes and screenshots always need it.
  Component-side receipt for the a11y gate's decorative-image logic; buttons carry
  accessible names matching labels (copy-030). [ADVISORY — a11y-gate receipt, already
  enforced render-side] {#copy-043}
- **FAQs: first ask whether FAQs should exist at all** ("could copy or design
  improvements remove the need?"); 'Frequently asked questions' in full — 'FAQs' only
  where space is limited; plain language, first person, one topic per question,
  concise. → Accordion/FAQ pattern. [ADVISORY-derivable — label-form check + TASTE on
  the existence question] {#copy-044}
- **Footnotes: reference from the body; important info belongs upfront, not in
  footnotes; markers = asterisk, numbers or symbols — NEVER mixed; numbers for
  T&C-class recurring reference; single asterisk only (never a double asterisk),
  asterisk only if one footnote on the page.** [ADVISORY-derivable — mixed-marker + double-asterisk checks
  are exact] {#copy-045}
- **Superscript: next to its related word (or sentence-end if whole-sentence); always
  BEFORE punctuation; two on one word separated by a comma (Insurance1,2).**
  [ADVISORY-derivable — placement check] {#copy-046}
- **Sort options: label pattern 'Sort by: [option]' ('Sort by: most popular'); each
  option concise, describing the effect of selecting it.** → Table/Dropdown sort
  affordances. [ADVISORY-derivable — exact label pattern] {#copy-047}

## Voice and pronouns on UI surfaces

- **'Your', not 'my', in app content** ('Manage your account', never 'Manage my
  account' — consistency receipt); **more 'you' than 'we'**; no 'At HSBC, we
  understand…'; don't put words in the customer's mouth ('You'll be delighted to
  know…' — "presumptuous"). Extends tov-004/tov-033 to nav/menu label convention.
  ENGINE: any 'My accounts'-style label is an antiPattern. [ADVISORY-derivable —
  my-prefix label scan + we/you ratio heuristic] {#copy-048}
- **HSBC is singular** ('HSBC is', never 'HSBC are'); 'an HSBC…', never 'a HSBC…'
  (aitch = vowel sound, see copy-004). [ADVISORY-derivable — two exact checks]
  {#copy-049}
- **Banking-channel vocabulary: mobile banking / online banking / telephone banking
  defined and sentence-cased generically; 'HSBC Online Banking' / 'HSBC Mobile Banking
  app' capitalised only WITH the HSBC prefix; generic use preferred for tone. App
  stores: App Store (iOS) · Google Play (Android) · AppGallery (Huawei); generic 'app
  store' only where unambiguous.** [ADVISORY-derivable — term lint; fixture naming]
  {#copy-050}

## Preferred terms (retrieval-not-recall)

- **The core preferred-terms table (~120 what-we-say/what-we-don't pairs) is ingested
  VERBATIM at `_sources/tone-of-voice/preferred-terms.txt` — the engine consumes it by
  retrieval, never from memory.** Highest-value exact pairs seeding the term lint:
  **log on / log off** (never log in, sign in, log out — 2 words, sentence case, noun
  AND verb) · **select never click** (tov-038's brand receipt) · email not e-mail
  ('Email' not 'Email address' as a field label) · dropdown (one word) · PIN not 'PIN
  number' · 'for example' not eg (except tables/diagrams — ESL receipt) · adviser not
  advisor · Direct Debit (brand, capitalised) · Mastercard · date of birth · first
  name / last name (never Christian name, surname, forename) · every 2 weeks (not
  fortnightly — reading-age receipt) · one-time payment written in full (OTP clashes
  with one-time password) · 'a year'/'per year' (not p.a.; 'pa' only when tight —
  screen readers may voice it as a word) · payments vs transfers are DIFFERENT (all
  payments are transfers, not vice versa) · outside the UK (not abroad/overseas —
  Payment Account Directive receipt in EU/UK). Market variants (freeze card UK ·
  Mobile Security Key HK · share trading India · U.S. locally) are locale parameters,
  not new rules. Pre-swept: 0 canon signals across the seed list.
  [ADVISORY-derivable — term-pair lint family, retrieval-backed; grow by review]
  {#copy-051}
- **Form-field vocabulary from the table: address · contact details · date of birth ·
  employer · income · occupation · marital status · required information (never
  'mandatory information') · Email (as label).** ENGINE-CRITICAL → Input-fields
  label fixtures. [ADVISORY-derivable — field-label term check] {#copy-052}
- **The sentence-case regime's allowlist lives in the preferred terms: Open Banking
  (Title Case, explicitly 'not Sentence case') · Direct Debit · Digital Secure Key ·
  proper-noun product names.** The sentence-case gate should consult the
  preferred-terms list as its proper-noun allowlist rather than growing a private
  one. [ADVISORY — gate-mechanism note; xref sentence-case gate + copy-012]
  {#copy-053}
- **Internal comms terms** (How We Succeed · How We Lead · Our Leadership Principles ·
  six principles in sentence case). [RECORDED — internal-comms channel, out of engine
  scope] {#copy-054}

## Chinese preferred terms 中文規範字表

- **Internal-use list by the Content Design team; Traditional Chinese, Hong Kong
  digital platforms; ~50 use/don't-use character pairs captured verbatim** (brand:
  滙豐 not 匯豐 · 恒生 not 恆生; services, system and wrong-character families with
  usage-distinction notes). Explicitly preference-not-correctness ("只涉及品牌或地區
  使用偏好，不涉及字型對錯"). [RECORDED — locale layer beyond current engine scope;
  the tov-045 locale axis consumes it by retrieval when bilingual surfaces arrive
  (type26 bilingual mechanics already ingested)] {#copy-055}

## Regional labelling (compliance-critical — HSBC HK Legal owned)

- **Hong Kong, Macau and Taiwan must NEVER read as countries/states/nations in any
  text, map or graphic** — the overarching principle when no specific example covers
  the case. Lists mixing them with countries use 'countries and territories' /
  'countries and regions' / 'markets'; preferred new-copy label = 'Country / region';
  'mainland China' for parallel mentions (lowercase mainland mid-sentence); HK/Macau
  in China-less country lists → 'Hong Kong SAR'/'Macau SAR' or classify the list
  first ('in the following markets: …'); Taiwan in China-less lists → classify the
  list first; never PRC or ROC. Fixed-dial per the charter: compliance rules have no
  flex band. [ADVISORY-derivable — exact term/label checks; compliance-sensitive,
  candidate for early promotion] {#copy-056}
- **Country selectors and similar dropdowns are labelled 'Country / region'
  (or 'countries and regions') — never bare 'Country'; form labels: Place of birth ·
  Place of issue · Jurisdiction of tax residence · Nationality (country / region /
  territory) — never 'Country of birth' / 'Country of issue' / 'Country of tax
  residence'.** ENGINE-CRITICAL → Dropdown + Input-fields fixtures.
  [ADVISORY-derivable — exact label check on selector/field fixtures] {#copy-057}
- **No flag pictures or emojis, in any circumstance.** Joins the icon-source gate's
  scope (a flag glyph could otherwise slip in as fixture decoration).
  [ADVISORY-derivable — flag-asset scan; icon-gate xref] {#copy-058}
- **Chinese Do/Don't labelling terms (Traditional + Simplified) captured verbatim**,
  including 台湾地区 for the mainland-China market only; T&C contradictions go to
  Asia Pacific/local legal. [RECORDED — locale layer, compliance-sensitive; retrieval
  source captured] {#copy-059}

## Findings

- **F1 — The antiPattern harvest map.** copy-030→Button · copy-031→action-bar/CTA ·
  copy-032→Links (next ★) · copy-033/034→Lists + benefits pattern · copy-035/036/037→
  Notifications + confirmation/success gap-pattern · copy-038→Modal · copy-039→
  Progress tracker · copy-040/041/052→Input-fields (supercharge) · copy-042→tooltips/
  contextual help · copy-044→Accordion · copy-047→Table/Dropdown sort · copy-048→nav
  labels · copy-057→Dropdown country selectors. Wiring these into per-component
  antiPattern blocks is generation-time work — same mechanism as the tranche-injected
  leading-trim notes, not a canon rebuild.
- **F2 — Pre-sweep: one real signal.** 'Accept terms & conditions' in
  Selection-controls (copy-022) — fix at next component touch, not worth a standalone
  tranche. Everything else already conforms: 0 full-stop button labels, 0 'My …'
  labels, 0 am/pm or wrong-format dates, 0 log-in/e-mail/PIN-number/bracket-plural
  signals. The 'click' matches are JS `addEventListener('click')` — code, not copy;
  tov-038's 0-signal status stands (scope note: the check must exclude script/attr
  contexts, which the current sweep did).
- **F3 — Strongest new gate candidate: copy-016** (no full stops in
  headings/labels/buttons/lists). Exact, cost-0, pre-swept clean, no false-positive
  surface identified. Same promotion path as all-caps: encode → advisory →
  bite-test → promote. copy-051's log-on family and copy-057's 'Country / region'
  label are the next two.
- **F4 — One REVIEW item this tranche: copy-014** (meta-title start-case exemption
  vs the sentence-case/all-caps gates). Cheap ruling: either pre-register the
  exemption or rule meta titles out of engine scope.
- **F5 — The sentence-case gate gets its allowlist mechanism** (copy-053): consult
  preferred terms for proper-noun exceptions (Open Banking, Direct Debit) instead of
  maintaining a parallel list. Small gate refactor, logged not built.
- **F6 — Fixture-data formats now have receipts** (copy-023…029): currency-before-
  amount-no-space, minus-before-unit, DD Month YYYY, 24-hour clock, 'to' ranges.
  Current canon fixtures conform; the check pays for itself at generation time when
  fixtures are synthesized per-screen.
- **F7 — Retrieval-not-recall gets its exemplar** (copy-051/055/059): ~170 term pairs
  across three languages is exactly the vocabulary scale the charter said should be
  retrieved, not memorised. The raw snapshots are the canonical lookup surface.
- **F8 — Vintage markers.** FCA cash-machines note dated 2018; selfie research 2020;
  'Twitter' absent here (unlike tone-of-voice pages); all four pages undated. Same
  pre-refresh vintage as the parent family — deltas ≠ defects; IDs stable for the
  refresh delta-map.
- **F9 — Source trivia, capture-faithful, no action.** Style-guide typos ('thigs',
  'typcally', 'consideratons', 'professsion', 'abouthow'); '4:00GMT' example
  contradicts its own zero-padded 24-hour examples; 'Startup' row header capitalised
  against its own note. Noted here so nobody "fixes" the raw snapshots.

## Coverage

| Page | Captured | Distilled |
|---|---|---|
| Copywriting/Editorial_Style_Guide.html | ✅ full (43k) | copy-001…050 |
| Copywriting/Preferred-terms.html | ✅ full (18k, table) | copy-051…054 |
| Copywriting/Chinesepreferredterms.html | ✅ full | copy-055 |
| Copywriting/regional-labelling.html | ✅ full | copy-056…059 |
