---
name: tier2-ingestion-progress
description: "Tier 2 create.hsbc ingestion — tranches 1+2a+2b DONE 2026-07-03 (register 365); desk batch RULED+ENACTED same day (axf-001 2.2 AA declared, sweep six wired, CA-6 into Links ★); NEXT = 7 role pages + Common Toolkit rigorous pass"
metadata: 
  node_type: memory
  type: project
  originSessionId: 92c4157b-06ce-43bc-bc2d-25ca2e16de23
---

Tier 2 ingestion OPENED 2026-07-03 (Dave: "ingest as much appropriate content as possible").

**Done (queue items 13–16, register 339→345, commits f2433b7 + 5461591):**
- `design-system-processes.md` dsp-001…013 (standards→toolkits→component libraries; the
  source names OUR architecture; certification + token-binding as upstream policy)
- `naming.md` nam-001…018 (2 cost-0 sweep candidates: nam-001 possessive `HSBC's`+name,
  nam-002 all-caps names — advisory-first, unswept)
- `digital-governance.md` gdea-001…008 (gdea-003 certified-reuse EXEMPTION = institutional
  case for certified components)
- `accessibility-framework.md` axf-001…012 — **axf-001 [REVIEW] on Dave's desk: HSBC bar
  is WCAG 2.2 AA, our audit baseline is 2.1 AA + partial 2.2 → gate re-baseline ruling.**

**Common Toolkit RULED (Dave 2026-07-03):** his Gaps-and-edits branch `Cgbtrmfp15ruNFkIAClpkI`
is faithful → THE source; prior use was ad hoc, this pass must be rigorous. Figma MCP works
(full HSBC seat): library = "HSBC Common Toolkit (MCP)" via `search_design_system` (On
Light/On Dark component-set pairs, `00 …` guide frames, semantic-color vars incl.
`(depricate)`); branch file metadata shows only a Cover page → survey via library search +
create.hsbc toolkit pages as skeleton. Debris: an old session pasted probe results as a text
node on the branch Cover — Dave to delete.

**SAME DAY, continued (queue 17–18, register 345→365, commit 7234c47):**
- `accessibility-visual-design.md` avd-001…009 (sweep candidate avd-006 banned alt
  prefixes; VD-9 = unmeasured gate axis: focused-vs-unfocused pixel delta ≥3:1)
- `accessibility-content-authoring.md` aca-001…020 (duplicates xref'd to avd-*, destiny
  carried ONCE — the F4 rule for remaining role pages; aca-003/004/005 cost-0 screen-gate
  candidates; aca-014…017 = Video-player criteria contract; CA-6 Links external-link gap →
  `_COMPONENT-GAPS.md`, Dave to rule at the Links ★ pass)

**Desk batch RULED + ENACTED 2026-07-03 (commit 9e280e6):**
- **axf-001 CLOSED** — declare-now-mechanise-later: declared bar = WCAG 2.2 AA,
  per-criterion map in `_A11Y-AUDIT.md` (2.5.7 already passing via Reorder, 2.5.8
  already enforced; **2.4.11 queued to the render-based sweep work**, kin of VD-9;
  3.2.6/3.3.7/3.3.8 routed to journey criteria contracts).
- **Sweep six enacted:** BLOCKING = nam-001 + avd-006-prefix + aca-004 bare-link
  (snippet gate check 7) + aca-003 unique-title (compose gate check 8, canon screens
  only). ADVISORY = nam-002 (D) + aca-007 (E) + aca-005 (F) + avd-006 role-suffix (G —
  4 live signals: Cards `aria-label="Example link"`, fix at Cards revisit then
  promote). All bite-tested (gates 24/24, advisory 10/10).
- **CA-6 RULED IN the Links ★ pass**, bundled with :visited.

**Role pages tranche 1 DONE 2026-07-03 (commit 5dd3306, register 365→388):**
interaction-designers → aid-001…021 + client-side-developers → acd-001…036 (64k page,
DOM-split capture method: hide code/nav, show parts in groups, get_page_text per group;
sanitize =/;/cookie/URLs to pass the output filter). NEW DESK BATCH pending Dave:
aid-009 (target-size default 44 — gate upgrade advisory<44) + acd-009 (ems-vs-px,
canon all-px token-scale ruling) + 8 cost-0 candidates (skip-link, lang keep-true,
pinch-zoom, up-event, onchange, aria-required, inputmode, paste-block) — one sitting.
CD-13 strengthens check-G (role-suffix) promotion once Cards "Example link" fixed.

**Role pages tranche 2 DONE 2026-07-03 (commit 129a747, register 388→390):** IA →
aia-001…004 (3/4 dups; keeper aia-002 heading out-of-context descriptiveness 2.4.6) +
QA/CX → aqa-001…014 (METHOD page: staged gates + independent UAT + fix-or-justify +
ship-with-LOGGED-deficiencies = engine receipts at source; STRATEGY pull-quotes for
transformation strand; aqa-003 = UI libraries held to guidelines+recommendations too —
canon-bar confirmation for next desk discussion).

**ROLE PAGES COMPLETE 2026-07-03 (commit e7cc86d):** manager trio → amr-001…008
(combined file, all BS 8878 PROCESS). STRATEGY GOLD: amr-005 = decision-receipt
discipline at source (recognise/consider/justify/RECORD → one lifecycle policy) +
amr-007 Statement contract (public face of logged-deficiencies, no-certificates) —
transformation-strand pull-quotes with aqa-008/013. VINTAGE TELL: "later in 2014"
survives live → framework pages are LAYERED VINTAGES (2014 base + 2024 patches),
per-section vintage sniffing needed. BS 8878 16 steps ≈ pipeline frame (note for
promenaut strategy pack). All 9 role files: avd aca aid acd aia aqa amr.

**Standards hub DONE 2026-07-03 (commit c528fdc, register 391):** Accessibility_Standards
+ 3 subpages → axs-001…007 = THE AUTHORITATIVE 2.2 ADOPTION MAP, validates the axf-001
ruling line-for-line; aid-009 two-receipted ("44×44 takes priority"); **VD-9 numerics:
focus ≥2px + ≥3:1 vs unfocused** (render-axis spec); 4.1.1 = Recommendation-not-dropped;
vintage anchors 2013/2019/2024. creating-accessible-content = video hub, no rules;
stale old-path queue dups pruned. A11Y SUBTREE FULLY INGESTED.

**PM desk batch RULED + ENACTED 2026-07-03 (commit 9deb095, register 391→389):**
aid-009 = fail<24 (blocking, either-dimension) / advisory<44 — chip-dismiss fixed via
hit-area expander, 5 real sub-44 targets surfaced (revisit pile) · cost-0 ×8 wired as
advisory checks H–O (live: skip-link missing on ALL 5 screens; 8 email inputs w/o
autocomplete = supercharge evidence; K/L calibrated, no false positives) · acd-009 =
rem-for-ALL queued as STANDALONE task (NOT supercharge-gated), px documented interim ·
aqa-003 affirmed (library bar in gate-doc header). Gates 25/25 + advisory 19/19 bite.
PRECEDENT: `[RULED …]` tag deindexes a rule (register 391→389, axf-001 precedent).

**Queued next:** channels pages DEFERRED to a CHEAP-MODEL session post-meter-reset
(presentations, document-a11y, pdf, email, web/app design-toolkits, sharepoint,
scenario-4) — Dave's meter ruling 2026-07-03 (67% used, Fable reserved for judgment
work) · Common Toolkit tranche 1 (see [[common-toolkit-survey]]) · discovered:
standards/toolkit anatomy+process ×4, chatbot naming, WeChat, social standards.

**Gotchas:** create.hsbc nav RESTRUCTURED — old `/accessibility/…` 404s; a11y tree lives at
`/processes-and-tools/accessibility/…`; queue paths corrected, verify before capture. Login
marker "Hello David" still the session check. Key-document PDFs are staff downloads —
capture on demand. See [[ingestion-sprint-2026-07-02]] for the capture method.
