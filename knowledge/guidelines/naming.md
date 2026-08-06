# Naming — brand standards for product/service names (ingested)

*Source: create.hsbc → Processes and tools → `Naming.html`, captured 2026-07-03 via
Dave's authenticated session (login-walled; ADR-0005 provenance applies). Engine-era
format. Naming policy B.11.6 itself is staff-only (ghq.hsbc) — source boundary; this page
carries the public-to-staff distillation. The 10-stage application process is out of
engine scope ([PROCESS]) but the TEXT RULES bind any UI copy that carries product/service
names — several are cost-0 gate candidates kin to the sentence-case family.*

## Text rules (bind our generated copy)

- **Never possessive with product names** — "HSBC should not appear in the possessive
  form": never "HSBC's Credit Card" / "HSBC's Easy Invest"; write "An HSBC Credit Card" /
  "HSBC Easy Invest". [BLOCKING — GATED, RULED STRAIGHT TO BLOCKING 2026-07-03 (sweep-batch
  ruling; pre-swept 0 signals): snippet gate check 7, visible text + accessible-name
  attributes, bite-tested in `_tests/test_gates.py`] {#nam-001}
- **Names are never fully capitalised** — "CONNECTED MONEY" banned; capitalised first
  letters + lowercase ("Connected Money"). Action-suggesting multi-word names may close
  up (PayMe, InvestDirect). [ADVISORY — RULED 2026-07-03: enacted as advisory check D
  (`_validate_advisory.py`, single-word caps outside the acronym allowlist; multi-word
  runs already blocked by snippet gate check 4). Stays advisory: the allowlist is
  judgment (PAYE/HMRC-class acronyms are legitimate); NAMES keep Title Case where UI
  copy is sentence case] {#nam-002}
- **Lock-ups are maintained in text for business propositions** — always "HSBC Premier",
  "HSBC Advance"; the HSBC prefix protocol is HSBC + functional descriptor, with
  judgment to reduce repetition of "HSBC" in running text. [ADVISORY — vocabulary rule
  for copy carrying propositions] {#nam-003}
- **Labels over invented names for standard services** — "Live Chat" is a recognised
  label and needs no name ("Chat To Us" adds complexity). First question is always "is a
  name required?". [ADVISORY — microcopy vocabulary: use industry-standard labels; kin
  to the preferred-terms table in copywriting.md F1] {#nam-004}
- **Hashtags follow the same naming approach** (simple + descriptive) and are written
  with each word capitalised for readability (#ConnectedIsGood); hashtags have their own
  review/approval and regional-collision check. [RECORDED — social scope, out of engine
  surface] {#nam-005}
- **No new icon, logo or brand identity for a name** — names follow the current brand
  identity guidelines. [ADVISORY — bears on generation: a named product in a composed
  screen never gets an invented mark; kin to the icon-source rule] {#nam-006}
- **App names ≤ 13 characters including spaces**; app descriptor is a separate short
  text. [RECORDED — glossary constraint, relevant if we ever compose app-store surfaces]
  {#nam-007}

## Naming policy (recorded — out of engine scope)

- **Simple and descriptive, always** — names directly describe what the thing does
  ("HSBC Mobile Banking App"); abstract names (Jupiter, Hex, Lion, Momentum) and
  acronyms are banned ("acronyms aren't a name… would not gain approval"). Applies to
  everything incl. internal programmes, all regions/languages. [RECORDED] {#nam-008}
- **Portmanteaus banned** (HSBC FinTip) unless regulatory reason or competitive
  advantage; combined-language names banned outright (not inclusive, need explaining).
  [RECORDED] {#nam-009}
- **Avoid clichéd i/e prefixes** (iProduct, eService). [RECORDED] {#nam-010}
- **Translation discipline** — native speakers only, never Google Translate;
  transcreation (intent, style, tone, context) over literal translation; names must
  travel across languages/cultures. [RECORDED — pairs with the 3-language preferred-terms
  discipline in copywriting] {#nam-011}
- **Names must not mislead** — accurate reflection of the product/service, no stretch;
  "deliver what it says on the tin". [RECORDED] {#nam-012}
- **Out-of-application-scope name classes** (still follow guidelines + IP review):
  social/WeChat names, chatbots (own page), conversational banking, OSS, team names,
  fund names (own policy, not Brand-managed), brand/SPV names. [RECORDED] {#nam-013}
- **Best-practice canon** — liked: HSBC Easy Invest, Connected Money, Simple Pay, My
  Deal, Everyday Global Account, Easy Saving, My Investment, Business Express, Mortgage
  Direct, Premier Saver, Private Banking. Avoid: Lion, Consilium, Bank Quest, HSBC
  RedHex, HSBC FinTip, Momentum. [RECORDED — retrieval vocabulary if copy ever names
  products] {#nam-014}

## Process (recorded)

- **10-stage application** — guidelines review → background research (Global Approved
  Name list, HSBC Now, web, directories) → develop/shortlist 3 + optional testing →
  Brand IP risk deck → Legal ticket (5–10 days; searches at requestor's budget) →
  Digital/GDEA review (5–7 days; GDEA-ID issued) → application form V6 (older versions
  rejected) → marketing approver GCB3+ (5–7 days) → GlobalNameReview (5–10 days) →
  approve/reject/return (exceptions route: 4 weeks; Q1-2025 policy for strategic
  out-of-policy names; approved names join the global list). [PROCESS] {#nam-015}
- **Testing is not mandatory but valued** — comprehension over likeability ("we are not
  the consumer"); survey/canvass/agency. [PROCESS] {#nam-016}
- **Trade-mark reality** — most descriptive names are covered by the Masterbrand trade
  mark and need no separate registration; abstract names carry the IP cost/risk.
  [RECORDED — the policy's own economic argument] {#nam-017}
- **Contacts + key documents** — GlobalNameReview@hsbc.com · GDEA
  (group.digital.experience.accessibility@hsbc.com) · domain.central · HSBCnet approvals
  (e-commerce_product_information@hsbc.ca). Downloads (application V6, process overview,
  approved-name list XLSX, Brand IP risk, HSBCnet consistency, naming guardrails) are
  staff-only — source boundary, not captured. [RECORDED] {#nam-018}

## Findings

- **F1 — two cost-0 sweep candidates:** nam-001 (possessive `HSBC's` + name) and
  nam-002 (all-caps names) — both regex-detectable in snippets/copy. Advisory-first per
  the icon-015 precedent; Dave may straight-to-block like the typography trio.
- **F2 — names are Title Case inside sentence-case UI copy** (nam-002 vs type26-019):
  the sentence-case gate must NOT flag legitimate product-name capitals (it currently
  sweeps headings/labels, not names — no known conflict, but the tension is now on
  record).
- **F3 — discovered subpages (→ Tier 2/3 queue):** Naming a chatbot · WeChat Standards ·
  social media standards (hashtag approval) · brand architecture (already queued).
