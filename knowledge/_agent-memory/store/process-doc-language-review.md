---
name: process-doc-language-review
description: Method + reusable tool for HITL language review of governance/process docs — flag wooly/recall-hole/misplaced/unsourced/stale/contradiction/tighten language; Swiss dossier where Claude pre-flags and Dave tags/comments/adds-own/exports
metadata: 
  node_type: memory
  type: project
  originSessionId: 9198cb85-9dfa-4c53-9cee-f263380a387c
---

Started 2026-07-03: after the "unmistakably HSBC" recall-hole ([[register-inference-ramp]]), Dave called for a sweep of ALL process/governance docs for wooly language + misplaced guidance. **Method** = Claude's speed (pre-flag findings) + Dave's judgment (tag / comment / add his own) — the project's own "automate around the taste call" turned inward. He reads and finesses; the dossier is scaffolding, not a verdict.

**Tool:** `_REVIEW-DOSSIER-charter_2026-07-03.html` (repo root) — Swiss / International Style (swiss-design-system skill; matches the north-star aesthetic Dave liked), a **reusable template** (swap the `FINDINGS[]` array + doc name per doc). Tags: WOOLY · RECALL-HOLE · MISPLACED · UNSOURCED · STALE · CONTRADICTION · TIGHTEN (accent colour carries ONE meaning = severity). Dave sets status (Agree/Reword/Disagree/Defer/Needs-source) + comment, can re-tag a mis-call, and **ADD HIS OWN findings** (location/tag/quote/note). Export → a markdown block he pastes back to Claude to enact. Autosaves to localStorage.

Charter specimen = **8 findings**, incl. TWO real contradictions tonight's §9 edit introduced: F4 (§3 "invent freely" vs §9 foundational-curbs-held) and F5 (§8 T3 "primitives recalled / no gate" vs §9 leashed expressive) — so §3 and §8 need reconciling to §9.

**CHARTER DONE 2026-07-04:** Dave reviewed the dossier, agreed all 8/8, enacted into `_FIXED-FLEX-CHARTER.md` (commit `071a62d`); decision record + rollback refs at `knowledge/_RECONCILIATION-charter-language.md` (git = rollback: revert the commit, REVERT lines hold pre-change wording). The method + tool are PROVEN end-to-end (flag → navigate → decide/diff → export register → enact → commit). Dossier `_REVIEW-DOSSIER-charter_2026-07-03.html` still uncommitted (kept as the working template — commit when rolling out). NB F2 carried a Dave question (does expressive innovate within cardinals?) — answered 2026-07-04: yes on framing (retrieval makes cardinals a hard wall; "Lovable/Make but curbed"), but DELIVERY depends on the named-not-built divergence machinery + the "HSBC-ness" provenance work ([[register-inference-ramp]] OPEN).

**Rollout — COLD-START TRIO DONE 2026-07-04** (charter + AGENTS + README now mutually consistent, the real win): charter F1-8 (`071a62d`), AGENTS A1-5 (`93b3857`), README R1-5 (`7f6a021`); registers `_RECONCILIATION-{charter,AGENTS,README}-language.md`. Propagation catches proved the method compounds (charter §9 edit → AGENTS A1/A2; ADR-0005 two-machine dissolution → README R4). 3 commits ahead of origin, Dave to push. NEXT (if resumed) = ADRs + runbooks → `_CONFIDENCE` + tiering docs. **FOLLOW-UP OWED:** refresh `knowledge/_NEXT-SESSION.md` (still 06-20 vintage — the pointer's fixed, the target isn't); carry the `~20-second` reword into the north-star mock if ever revised. Generated `_*` audit files OUT of scope. Same tool, swap the findings array. Relates [[working-style-divergent]].
