---
name: desk-rulings-2026-07-02
description: "Evening desk session — 5 GOOD-MORNING rulings closed (push, all-caps, Univers dissolved, gradient parked, icon advisory-first); what stays open"
metadata: 
  node_type: memory
  type: project
  originSessionId: 853991f1-817e-48de-b3ba-f150a0ff3b99
---

Evening session 2026-07-02, Dave went through the GOOD-MORNING desk in sequence:

1. **Push** — keep palette commit + push all; sandbox has no GitHub creds so DAVE runs `git push origin master` (verify: 17 ahead at session end). Palette provenance de facto accepted for this palette; wider ADR-0005 ruling still open.
2. **All-caps** — canon-wide + hard gate; ENACTED same session (see [[type-rule-sentence-case]]).
3. **Univers Next (type26-001)** — DISSOLVED: premise wrong, store already carries "Univers Next for HSBC"; RESOLVED with receipts; only residual = Sutherland fixture spot-check at next touch.
4. **Text-on-gradient (type26-015)** — PARKED to component-finessing pass, docketed with mot-007 in `_PROMOTION-QUEUE.md`; interim: no gradient-hero generation, gradient surfaces text-free.
5. **Icon 4.5:1 (icon-015)** — advisory-first ruled AND built (`_build_icon_contrast_delta.py`, step 12/18). Evidence: 0 declared dead-zone (promotion free for icon/* pairs).
6. **RAG ROUNDEL POLICY (same eve, ruled):** roundel vs surface ≥3:1 · internal mark vs roundel fill ≥4.5:1 (small-text analogue) · **dark mode = WHITE roundel + BLACK mark** (icon+label carry meaning). Encoded in the delta advisory (§3 roundel leg + §4 mark-vs-roundel). All dark dead-zones dissolve structurally. ONE light fail: success tint-knockout 3.98 → white mark. ⚠ NEW OPEN: **amber warning roundel fails 3:1 in light** (1.69 white / 1.60 tint) — darker amber, outline, or exemption = Dave's call; kin to [[dark-rag-token-gaps]] gap #3.
7. **Dual-live data palettes (same eve, ruled + enacted):** 50 supporting primitives moved into colour.json (`color/supporting/<family>/<1-5>`, contrast receipts kept) — PREFERRED for new work; legacy `color/data-vis/*` annotated old-projects-only. Series assignment still V7 (proposals file stays holding pen for roles).

**LATE RULINGS, SAME EVE:** (a) **amber = EXEMPT** — warning roundel's light 3:1 fail is accepted convention; internal-mark contrast is the priority, icon+label suffice (encoded in delta check, reported-never-failed). (b) **Implementation tranche ENACTED**: Notifications success mark → white + inline amber mark → #333 + dark white-shape/black-mark policy proper (supersedes 06-24 interim); Input-fields rag symbols de-hardcoded (currentColor + --mark, knocks to page); Confirmation dark --success → white via driftAllow (page-cutout tick reads black). Delta advisory: active-treatment tracking, 0 fails. Build 18/18, bites 16/16. AWAITING Dave's visual review of the live HTML (Notifications, Input-fields, Confirmation) — sandbox chromium wouldn't launch (env papercut, log it to [[robustness-portability]]).

**VISUAL REVIEW PASSED (end of session):** Notifications + Confirmation pass clean; Input-fields passed after three review fixes (interactive tail icons — "icons in an input are usually clickable"; dark error border → full red, white no longer overlays the red bar; text true-centred at REST 10/10, off-centre-while-active accepted, text never moves). Input-fields flagged [[supercharge-codename]] candidate. icon-015 tail = gate promotion + mark tokenisation, deferred to supercharge. Session ended 22 commits ahead, all gates green.

**Still open after this session:** THE PUSH (Dave's, 22 ahead) · V6 proposals · V7 series pick (palette primitives now live — natural next) · colleague chase (calibration = #1 unlock) · ADR-0005 provenance ruling · icon-016/017 size tensions · register at 11 items. Fable metered from the 7th — judgment-dense items first.

**DESK PICKUP (same date, next session):** V6 derivations **SHELVED** (Dave: "interesting test, forget the derivations for now" — charter §4 roles stand, values stay in pen unpromoted). V7 **DEFERRED** pending proper renders; his idea = surface A/B/C as build-time options when a run detects a chart (parked in [[generation-mechanism-ideas]] idea 3). **Push method RULED:** single-writer — Claude commits, Dave pushes, terminal only, GitHub Desktop retired (see [[git-push-method]]). Root cause of old lock conflicts found: sandbox delete-guard left stale .git locks after my commits; deletion now enabled, locks cleaned, fsck clean.

**DESK PICKUP RULINGS (all enacted + committed, ahead 24):**
- **ADR-0005 CLOSED** — premise was WRONG: this is an **AGENCY machine with company access**, not a home machine (correct any "home machine" references). Real brand values cleared to live in the repo; AGENTS.md two-machine rule rewritten; calibration materials may land here. **History purge DEFERRED** (accepted risk, private repo; revisit on visibility/host change). Residual watch-item (not ruled): repo syncs to Dave's PERSONAL GitHub (daveasewen/UX-design).
- **icon-016/017 RULED** — full 12–48 size range permitted "for now, prune if we have to"; toolkit export stays operative; no gate encoding; [REVIEW] tags kept as revisit-if-refresh-settles.
- **icon-015 4.5:1 PROMOTED to blocking** — Dave: "icons alone should have the small-text equivalent contrast at least." Declared icon/* pairs → 4.5:1 in `_validate_snippets.py` check 3 (context 'icon' added to `_contrast_utils`); pictograms + RAG stay 3:1 (roundel policy untouched). Dead-zone bite (icon/default on data-vis blue-3, 3.66/3.45) permanent in test_gates → suite 17/17; sweep cost 0; delta advisory continues as the exhaustive watchdog. Remaining icon-015 tail = mark tokenisation only (supercharge).
- **Colleague chase draft delivered** (calibration ask, paste-ready). Full build 18/18 green after enactment.

**2026-07-03 DESK CLEARING (7 rulings, all ENACTED, commits 0d63d27 + cc79501):**
(1) cost-0 typography gates **STRAIGHT TO BLOCKING** (Dave's explicit override of
advisory-first) — no-italics/no-text-shadow/raw-red-text = snippet-gate check 6,
var(--error) role route stays legal, 3 bite-tests (suite 20/20). (2) [RECORDED]/
[PROCESS] tags **BLESSED** (documented in gen_rules_index.py). (3) copy-014 meta
titles **OUT OF ENGINE SCOPE**. (4) col25-011 **token store governs** — text/secondary
= Grey 7 stays, re-check at 2026 grey specs. (5) col25-016 **2026 wins outright** —
chart-red ban superseded, col26-013 governs both vintages. (6) col25-008 B&W-photo
ban **carries interim** (silence ≠ withdrawal), closes at refresh re-cut.
(7) webf-017 Common Toolkit — PROBED same session: create.hsbc links to Figma
**HSBC-Common-Library (SuVpEaqQcXDP3CYkFKBIeE), MCP needs per-file EDIT access
(denied)**; the Gaps-and-edits branch (Cgbtrmfp15ruNFkIAClpkI) re-verified fully
MCP-reachable. Dave to check Common-Library-vs-branch lineage; request editor if
new content. GOTCHA: create.hsbc session EXPIRES mid-session (login wall returns
logged-out shells to fetch silently — check a known-good marker string, not just
status 200). Register 341→339, REVIEW 38→34, BLOCKING 53→54. Desk now clear
except: **col25-018 blue/400 fix** (real token work) · V7 (deferred) ·
colleague/calibration wait.
