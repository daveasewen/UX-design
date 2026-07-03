# Accessibility for content authors — CA standards (ingested)

*Source: create.hsbc → Processes and tools → accessibility → digital-accessibility-framework →
`accessibility-for-content-authors.html`, captured 2026-07-03 via Dave's authenticated
session (login-walled; ADR-0005 provenance applies). Engine-era format. Second of the 9 role
pages (axf-006). Source structure kept: CA-1…19 STANDARDS/GUIDELINES/RECOMMENDATION as
published; several checkpoints duplicate the VD set — recorded here with xrefs, destiny
carried ONCE (on the avd-* rule) to keep the sweep queue honest. Source note: content
authors work late in projects, often post-QA — "vital that content authors check their own
work" (self-check duty again).*

## Structure + titles (rules)

- **CA-1 — structure content with lists and headings** (SC 1.3.1 A): relationships
  conveyed by presentation must be programmatically determinable. [ADVISORY — snippet
  gate already checks semantic markup/ARIA; composition layer must keep heading
  hierarchy when assembling screens] {#aca-001}
- **CA-2 — content order must be logical** (SC 1.3.2 A): meaningful sequence
  programmatically determinable. [ADVISORY — composition-layer rule; DOM order =
  reading order in canon, keep it that way when composing] {#aca-002}
- **CA-3 — unique, concise page/frame/iframe titles** (SC 2.4.2 A + 4.1.2 A): first
  thing a speech-output user hears. [ADVISORY — screen-gate candidate: composed screens
  must carry a unique descriptive <title>; cost-0 check] {#aca-003}

## Links (rules)

- **CA-4 — link text uniquely describes the target** (SC 2.4.4 A): unique link/nav text,
  in context; audio-labelled repeats ("Info", "Add to favourites") must be made unique.
  [ADVISORY — microcopy rule; bans bare "click here"-class links; joins the copywriting
  vocabulary] {#aca-004}
- **CA-5 — repeated links to one target are ONE link** (SC 1.1.1 + 2.4.4 A): adjacent
  image + text with the same target combine into a single actionable element. [ADVISORY —
  canon Cards already enact this (single-link card patterns); composition check
  candidate for assembled screens] {#aca-005}
- **CA-6 — links leaving the window/site/app say so** (SC 2.4.4 A): warn before opening
  elsewhere + name where it opens. [ADVISORY — Links canon has no external-link variant
  marked; REVIEW-adjacent for the Links ★ pass, logged in F2] {#aca-006}

## Copy (rules)

- **CA-7 — no sensory-only instructions** (SC 1.3.3 A): "above"/"below" acceptable;
  "button on the right" banned — AT reflows location. [ADVISORY — copy sweep candidate
  (directional-phrase regex, needs judgment for false positives)] {#aca-007}
- **CA-8 — colour-only meaning ban** = VD-1 verbatim (SC 1.4.1 A), incl. the data-vis
  hatching + deuteranopia/protanopia palette guidance. [RECORDED — duplicate; destiny
  carried on avd-001] {#aca-008}
- **CA-9 (guideline) — expand abbreviations** (SC 3.1.4 AAA): explain at first use
  and/or glossary; avoid GMT/HKT/USD-style abbreviations even on small screens; mark up
  as `<abbr title="…">`. [ADVISORY — copy + snippet rule; currency/time abbreviations
  are live in our Table/List-items demo copy — F3] {#aca-009}

## Non-text + text design (rules)

- **CA-10 — purpose-alt for all non-text elements** = VD-7 verbatim (SC 1.1.1 A) incl.
  the banned "Image of/Link to/Picture of/Add button" prefixes. [RECORDED — duplicate;
  destiny + sweep candidate carried on avd-006] {#aca-010}
- **CA-11 — text contrast 4.5:1 / 3:1 large** = VD-2 verbatim (SC 1.4.3 AA) incl. the
  text-over-image scrim clause. [RECORDED — duplicate; destiny on avd-002] {#aca-011}
- **CA-12 — no images of text** = VD-4 verbatim (SC 1.4.5 AA). [RECORDED — duplicate;
  destiny on avd-004] {#aca-012}
- **CA-20 (guideline) — UI components + graphical objects ≥3:1 non-text contrast**
  (SC 1.4.11 AA, WCAG 2.1). [RECORDED — our stack already BLOCKS stricter: declared
  icon/* pairs at 4.5:1 (icon-015 promotion), UI components at 3:1 via the surface/
  indicator audits; source floor is the 3:1 we started from] {#aca-013}

## Audio-video + multimedia (rules)

- **CA-13 — transcripts for all audio and video** (SC 1.2.3 A): podcasts, silent video
  (visual description), sound video (dialogue + music + effects + visuals); delivered as
  accessible RTF/PDF, clearly linked from the video page, WITH a backlink from transcript
  to the video page (search-engine entry path). [ADVISORY — Video-player component
  contract item; the backlink detail is easily lost] {#aca-014}
- **CA-14 — captions for ALL video, including live** (SC 1.2.2 A + 1.2.4 AA); Appendix A
  (not on this page) covers cost-effective delivery. [ADVISORY — Video-player contract:
  captions control is present in canon; keep it mandatory in composition] {#aca-015}
- **CA-15 — audio description for pre-recorded video** (SC 1.2.5 AA) unless the audio
  track already carries all information; unreasonable-cost cases (e.g. multi-language)
  go to Global Marketing Digital Approvals. [ADVISORY — Video-player contract item]
  {#aca-016}
- **CA-16 — no autoplay audio** (SC 1.4.2 A): the source's own detail line is blunt —
  "Do not play audio automatically (this includes video with an audio track)."
  [ADVISORY — Video-player + Hero contract: canon autoplays nothing; keep it gated in
  composition] {#aca-017}
- **CA-17 (guideline) — visual cues accompany all audio alerts** (SC 1.3.3 A): new-
  message/error/overtype audio cues need visual equivalents; haptics don't count
  (device support varies). [ADVISORY — Notifications canon is visual-first already;
  binds any future sound design] {#aca-018}
- **CA-18 (recommendation) — metadata for media alternatives** (beyond WCAG): metadata
  associates accessible alternates with content and helps users locate alternative
  media. [RECORDED] {#aca-019}
- **CA-19 — flicker minimised** = VD-6 verbatim (SC 2.3.1 A, PEAT named). [RECORDED —
  duplicate; destiny on avd-007] {#aca-020}

## Findings

- **F1 — the CA set is the copy-side gate stack:** aca-003 (unique titles) and aca-004/
  005 (link discipline) are cost-0 screen-gate candidates; aca-007 (directional
  phrases) and avd-006 (alt prefixes) join the copy sweep queue. Video rules
  (aca-014…017) form a ready-made Video-player criteria contract for its next ★ pass.
- **F2 — CA-6 exposes a Links canon gap:** no external-link/new-window marking variant
  exists in the reviewed Links snippet. Logged to `_COMPONENT-GAPS.md` candidate list —
  Dave to rule whether it joins the Links ★ pass (Links is next ★ per
  component-review-program).
- **F3 — CA-9 vs live demo copy:** Table/List-items demos use USD/GBP-style
  abbreviations without `<abbr>`; harmless in demos but the rule binds composed screens
  — worth a line in the composition runbook rather than a snippet change.
- **F4 — duplicates are structural:** the framework repeats checkpoints per role
  (VD/CA overlap on 1.4.1, 1.4.3, 1.4.5, 1.1.1, 2.3.1) — expect the same in the
  remaining 7 role pages; keep carrying destiny once and xref, or the register
  double-counts the sweep queue.
