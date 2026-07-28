# _GAUGE-LOG — session pre-flight/post-mortem measurements

provenance: local_e79e89ee-51cb-4a74-bf95-b7cf3e303af9 · 2026-07-27
status: observed

*Contract (runbook step 2f, GM-D5(a)): APPEND-ONLY · one block per session, chronological ·
#### 2026-07-28 #27

> **pre-flight:** fill ~30% + job 15–17% + wrap 8% = ~53% AMBER-projected · reserve 15% ring-fenced *(fill = 16.1% chain MEASURED 32,179 tk + ~7 harness inferred + read-render overhead; job priced 14–17% at the fenced scope after a mid-survey re-price from 20–25%, forked to Dave and re-ruled — both announced in-chat)*
> *(Session #27, 2026-07-28, **Opus solo** (conductor, effort max; delegation deliberately NOT taken — one snippet + one registry edit), Dave live. Arc: floor measured → retrieval-first on the ADR-0015-A2 contract → survey found the queue's job description wrong twice → **STOP, re-price, fork** → Dave ruled interaction-only with DV-D07 fenced, after refusing the first option-select as mechanism-shaped and asking for it in plain words → enact → build red on TWO counts (my own `--shadow`, caught by ds-018's advisory C2; plus stale showroom) → both fixed → `[72/72]` → 4-way mutation control → render-proof + bite → inscriptions → wrap. Closed 🟡 **Amber ESTIMATE**, reserve untouched.
> **PACE (perishable, replaces Tue ~13:35):** panel Tue 14:25 BST — week 66.3% elapsed · All 63% ⇒ **0.95×** (behind, narrowing three panels running) · **Fable 79% ⇒ 1.19× — further AHEAD; 0.62× rationed to the Thu 23:00 reset**. Opus counts to All ⇒ this window was the pace-correct spend; MORE-WINDOWS still holds for All.)*
> **★ THE LESSON, for the next reader:** the queue said *"28 `<title>`→`data-tip`"*. Both halves were wrong — 27 marks, and it was never a rename but a four-part contract whose missing `tabindex` would have left the popover mouse-only while the dropped `<title>` took the accessible name with it. **A queue line describes a job; only the canon describes the contract.** Survey the canon consumer before believing the queue's verb.
> **section-usage #27 (observed, self-report):** GM HDR:C LATEST:C PRIOR:R DOFIRST:C A:C C1:C C2:C C2b:R C3:U C4:R C4b:U C5:U STRATA:C · LS HDR:R LANES:C SPIN:U DELTAS:C WEBFONT:U LIVE:R LIFECYCLE:U DEAD:U OPEN:R TARGETS:U SPINOFFS:U
> **section-sizes #27 (tiktoken cl100k_base):** GM HDR:1178 LATEST:1239 PRIOR:1054 DOFIRST:2297 A:4208 C1:842 C2:1076 C2b:484 C3:181 C4:1204 C4b:256 C5:84 STRATA:1167 · LS HDR:255 LANES:872 SPIN:1794 DELTAS:2651 WEBFONT:604 LIVE:4928 LIFECYCLE:973 DEAD:432 OPEN:4361 TARGETS:577 SPINOFFS:444 · totals GM:15271 LS:17891
> **consult-receipts #27:** "consumes manifest universal default opt-out ADR-0015-A2" → lane:lane-2-apollo-charts · gm:DOFIRST · ledger:two-lanes-the-m-set-splits-chart-jobs-lose-their-m-codes-202 ; "chart scatter behaviour partial consumes data-tip toolbar table spine" → DV-D10 · DV-D13 · dv-017 · dv-line-004
> *(⚠ **neither door indexes `docs/decisions/`** — ADR-0015 § Amendment 2, the contract this session enacted, had to be read direct. The ds-016 shape: a live, in-force document retrieval cannot see. Price it.)*
>
measurements only (pre-flight estimate vs closed band, overrun + cause) · NOT in the cold-start
read chain. This file exists so the throttle's 15% reserve can be re-derived from data (Half 0b).
Blocks below moved VERBATIM from `GOOD-MORNING.md` §C strata at the first 2f roll (session #15).*

> **⚠ BLOCK FORMS — exactly TWO are legal, and `_build_memento_index.py` REFUSES any other:**
> `#### YYYY-MM-DD #N` = a session · `#### META — <title>` = a finding about this file.
> *(#30 wrote an audit block in neither form. The index builder refused — correctly — and because
> the wrap gate does not run the build, `_build_all.py` stayed RED across two wraps and both of them
> committed over it. ds-024, repaired #32.)*

#### 2026-07-27 #6

> **pre-flight:** fill 30% + job 20% + wrap 5% = 55% AMBER · reserve 15% ring-fenced
> *(Session #6, 2026-07-27. ⚠ **The job term was for a BUILD that Dave then cancelled** in favour of
> capture-plus-ruling; the capture ran instead and cost more than the build would have been allowed.
> Closed 🔴 **~62% RED**. **The overrun is RECORDED, per the throttle's own instruction to record every
> overrun so the 15% can be re-derived from something.** Two honest causes: three ruling rounds arrived
> mid-ritual, each cheap, none priced — **the ~10%-floor failure mode the runbook says is gone, recurring
> in a new costume** — and I did not surface the Amber→Red crossing; **Dave asked "getting warm btw"
> before I said it**, which is the one thing the band rule exists to prevent.)*

#### 2026-07-27 #7

> **[SUPERSEDED — kept for the record] pre-flight:** fill 30% + job 15% + wrap 5% = 50% AMBER · reserve 15% ring-fenced
> *(Session #7, 2026-07-27. Closed 🟡 **~60% AMBER, at the boundary**. **Overrun +5, and it was
> SELF-INFLICTED, not a discovery:** the byte-cap detour (a comment block that restated the ruling's arc
> inside a file whose header forbids exactly that) cost the difference. **Recorded per the throttle's own
> instruction to log every overrun so the 15% can eventually be re-derived from something.** The fork
> fired correctly and mid-flight this time — priced at ~55% fill, the render would have landed ~70% RED,
> and Dave chose flush. ⚠ The three-term projection was accurate to within 5 points here; **that is n=1
> and does not vindicate it.**)*

#### 2026-07-27 #8

> **pre-flight:** fill 30% + job 20% + wrap 5% = 55% AMBER · reserve 15% ring-fenced
> *(Session #8, 2026-07-27. Closed 🟡 **~55% AMBER**, **on plan** — the first window in four to close
> inside its projected band. **No overrun to record.** The mid-flight fork fired on an unplanned finding
> at ~48%: naming ds-019's overriding rule was priced at ~8% ⇒ **~61% RED**, and Dave chose **log-and-stop**
> rather than spend the reserve. ⚠ **n=1 again, and the band held for an unheroic reason** — the job was
> stopped early, not estimated well. Do not read this as the three-term rule vindicated.
> ⚠ **PACE UNREAD:** Dave was asked for the plan-panel figures and the window closed before they arrived,
> so posture ran on Friday's `inferred` 0.65× pro-rata / Fable 0.55×. **Ask again at the next opener.**)*

#### 2026-07-27 #12

> **pre-flight:** fill 12% + job 30% + wrap 5% = 47% AMBER · reserve 15% ring-fenced
> *(Session #12, 2026-07-27. Closed 🔴 **~72% RED. Overrun +25, and it is the largest recorded** —
> **but the whole excess is TWO UNPLANNED FINDINGS, both forked to Dave at the moment they appeared,
> and both of which he chose to absorb.** Finding 1 (the B-D4 non-collision) *reduced* scope and was
> reported without a stop. Finding 2 (`--muted` in C2's blast radius) was priced and forked — Dave took
> option (a), narrow. **The third overrun source was NOT forked and should have been:** C2's first run
> found three more instances, and I fixed one and wrote up two without re-pricing. ⚠ **That is the fork
> rule failing in the one case it exists for — a finding arriving mid-enactment, when stopping is most
> expensive and most necessary.** Also: Dave said *"im going round in circles"* at ~55% — **the circling
> was real and I had not named it.** The unlock, when it came, was one sentence: *a token value is a
> one-line reversible edit, not architecture.* **Say that earlier next time.**
> ⚠ **PACE:** Dave reported the plan panel *"has barely changed since the last reading"* (Friday-inferred
> 0.64× pro-rata, Fable 0.53×) ⇒ **still behind pace; posture stays MORE WINDOWS, not longer ones** —
> which this session did the opposite of.)*

#### 2026-07-27 #13

> **pre-flight:** fill 20% + job 25% + wrap 5% = 50% AMBER · reserve 15% ring-fenced
> *(Session #13, 2026-07-27. Closed 🟡 **~68% AMBER-high — but the +18 was PRICED MID-SESSION, not
> overrun**: at ~50% Dave chose "full ritual" from a stated fork (full = +15–18 → ~68 vs light = +10
> → ~60). The fork rule working as ruled. Findings en route: brief's numbers stale (GM 840→910 in a
> day — which IS the diagnosis) · Parked innocent, stratum stack guilty · both folded into the
> proposal before ruling, no re-price needed as the job was diagnosis.)*

#### 2026-07-27 #14 — HOLE, no stratum written

*(gap line added 2026-07-28 #22 per P1(b) — recorded, not reconstructed. #14 enacted GM-D5(a)'s own
step 2f (`113eefc`) yet wrote no stratum of its own; its gauge story lives only in its banner
(`_GM-ARCHIVE.md` § Batch 2026-07-27) + git. The absence was unflagged until dream-pass 3 found it.)*

#### 2026-07-27 #15

> **pre-flight:** fill 41% + job 13% + wrap 5% = 59% AMBER · reserve 15% ring-fenced
> *(Session #15, 2026-07-27, phase-2 W1, Fable solo. Fill MEASURED per D9 by summing served reads of the
> mandated set (brief · ledger · runbook 2e/2f · full GM · gauge canon). The full pass priced ~20% under the
> script-move method; Dave took the SPLIT at the ~66% Red projection — the fork fired BEFORE start, as ruled
> — job re-priced ~13%. Closed 🟡 ~55% ESTIMATE, on plan, no overrun: both unplanned findings (build-kill
> mechanism · STAND-004 contradiction) were absorbed inside the price as inscriptions, not chases.
> **PACE (perishable, replaces 18:45):** panel 19:35 BST — session bucket 15% (resets +2h07) · All models
> 39% ⇒ 0.71× pro-rata · Fable 33% ⇒ 0.60× · catch-up to Thu 23:00: All 1.36× · Fable 1.50×. Behind,
> improving. Posture: MORE WINDOWS — W2 on Fable is on-posture, and Dave pre-licensed it in-window.)*
>

#### 2026-07-27 #16

> **pre-flight:** fill 45% + job ~12% + wrap 5% = ~62% RED-edge · reserve 15% ring-fenced
> *(Session #16, 2026-07-27, phase-2 W2, Fable solo. Fill MEASURED per D9 after the mandated reads
> (brief · ledger · runbook 2/2c/2e/2f · band table · full GM + LS at open). Projection straddled the
> Red line ⇒ fork put to Dave PRE-START; he ruled RUN WHOLE with a findings watch. No unplanned finding
> moved the band — four script aborts cost ~4 calls, absorbed in price. Closed 🔴 ~63% ESTIMATE,
> ~1–2 pts over projection, reserve untouched.
> **PACE (perishable, replaces 19:35):** panel 20:16 BST — All 41% ⇒ 0.74× · Fable 37% ⇒ 0.67× ·
> catch-up to Thu 23:00 All 1.33× / Fable 1.42× — behind, improving, gap NARROWING. MORE-WINDOWS holds.)*

#### 2026-07-27 #17

> **pre-flight:** fill 30% + job 22% + wrap 6% = 58% AMBER · reserve 15% ring-fenced
> *(Session #17, 2026-07-27, Fable solo, Dave live. Opened for §C·2; Dave reframed to Memento hardening
> at ~32%. AMBER crossing announced at ~44% (M1's first live use, mid-ruling); in-window enactment
> trimmed at the crossing — M11/M12 file edits moved to the brief. One script abort (wrong-shape §A
> hash probe) — nothing written, convention recovered, re-run green. Closed 🟡 ~60% ESTIMATE, boundary,
> reserve untouched.
> **PACE (perishable):** panel 21:21 BST — All 43% ⇒ 0.77× · Fable 41% ⇒ 0.73× · catch-up All 1.29× /
> Fable 1.34× — behind, narrowing all day. MORE-WINDOWS holds; the M-set window is Opus (All bucket).)*
>

#### 2026-07-27 #18

> **pre-flight:** fill 24% + job 20% + wrap 8% = 52% AMBER · reserve 15% ring-fenced
> *(Session #18, 2026-07-27, Opus solo effort MAX, Dave live — the routing #17 ruled. Floor MEASURED
> per D9 at the opener: read chain 32,759 tk = 16.4% (GM 12,780 + LS 16,063 + brief 2,389 + band-table
> slice 1,527), harness UNMEASURED on top ⇒ ~23–24%. **The brief's own 35–45% price did not fit**:
> 60% RED − 24% floor − 6% wrap = ~30 points of job. Forked PRE-START with three cuts; Dave took the
> cheap-first re-cut. One further fork mid-window (M10's block already crossed) — re-priced, ruled
> ADVISORY, no band change. Closed 🟡 ~52% ESTIMATE, reserve untouched.
> **PACE (perishable, replaces 21:21):** panel 21:56 BST — All 45% ⇒ 0.80× · Fable 44% ⇒ 0.78× ·
> catch-up to Thu 23:00 All 1.26× / Fable 1.28× — behind, narrowing. MORE-WINDOWS holds; this window
> was Opus (All bucket) per the #17 trust ruling.)*
>
> **CORRECTION (append-only, dream-pass-3 P1(c), ruled 2026-07-28, enacted #22):** this block's closed
> band (🟡 ~52%) equals its own pre-flight arithmetic; the session's final chat message to Dave said
> **🟡 ~62%, RED edge (estimate)** — after the commit it reports. Both figures were ESTIMATES and
> nothing measured the window, so they **cannot be adjudicated**; the record now carries both rather
> than silently disagreeing with the chat. (Transcript `local_9ecbcf40`, final wrap message.)

*(rolled 2026-07-28 #20 per 2f. ⚠ #19 wrote no stratum — its gauge story lives in its banner; recorded as a gap, not reconstructed.)*
#### 2026-07-28 #20

> **pre-flight:** fill 22% + job 28% + wrap 8% = 58% AMBER · reserve 15% ring-fenced *(fill = 15.2% chain measured + ~7 harness inferred; job priced LIVE mid-window, not at opener — the honest account is the paragraph below)*
> *(Session #20, 2026-07-28, Fable solo, Dave live. Opened titled for the ex-M4a/M4b/M5 build; the survey found the injected-behaviour architecture (~45%), Dave re-cut the frame — TWO LANES, M-codes retired off chart jobs — and the fork + inscriptions took the window to Amber before M5's first line. Deferral = HIS pick per his own no-new-builds-at-Amber rule; no build artefact started past Amber. Closed 🟡 ~55–58% ESTIMATE, reserve untouched.
> **PACE (perishable):** NO fresh panel this window — Mon 21:56 stands (All 0.80× · Fable 0.78×, behind-narrowing); ask at #21's opener.)*
>

#### 2026-07-28 #21
> **pre-flight:** fill 22% + job 14% + wrap 8% = 44% GREEN · reserve 15% ring-fenced *(fill = 15.3% chain MEASURED 30,624 tk + ~7 harness inferred; job = M5 solo per brief §11, priced at the opener)*
> *(Session #21, 2026-07-28, Fable solo, Dave live. Opened on the #20 title and ran to spec: mover built + bitten + wired, runbook pointed, this wrap = the mover's first live fire. No unplanned findings; no fork needed. Closed 🟢 ~44% ESTIMATE, reserve untouched.
> **PACE (perishable, replaces Mon 21:56):** panel Tue 09:09 BST — week 63.2% elapsed · All 50% ⇒ 0.79× · Fable 52% ⇒ 0.82× · catch-up to Thu 23:00 = All 1.36× / Fable 1.30× — behind, narrowing. MORE-WINDOWS holds.)*
#### 2026-07-28 #22

> **pre-flight:** fill ~22% + job 10% + wrap 8% = 40% GREEN-projected · reserve 15% ring-fenced *(fill = 15.4% chain MEASURED 30,710 tk + ~7 harness inferred; job = dream-pass-3 enactment, priced at the opener)*
> *(Session #22, 2026-07-28, Fable solo, Dave live. The beat ran to spec — P1–P6, per-item receipts, ONE commit `681cfac` — then Dave ruled M9 PROMOTE in-window (enacted same hour) and chose wrap over starting lane-1 step 2 at Amber. The projection under-read the fill: the mandated spine reads (LS ~17K tk + runbook + proposals + ledger) cost more than the inferred floor suggests — recorded as a cause, not excused. **Closed 🟡 ~55–58% ESTIMATE** (band from the remaining-budget table), reserve untouched; one fork (proceed-vs-wrap), put to Dave, he took wrap per his own no-new-builds-at-Amber rule.
> **PACE (perishable, replaces Tue 09:09):** panel Tue 10:25 BST — week 63.9% elapsed · All 53% ⇒ 0.83× · Fable 58% ⇒ 0.91× · catch-up to Thu 23:00 = All 1.30× / Fable 1.16× — behind, narrowing fast. MORE-WINDOWS holds.)*
#### 2026-07-28 #23

> **pre-flight:** fill ~28% + job 12–15% + wrap 8% = ~48–51% AMBER-projected · reserve 15% ring-fenced *(fill = 15.5% chain MEASURED 31,094 tk + ~7 harness inferred + read-render overhead; job = lane 1 step 2, priced at the opener)*
> *(Session #23, 2026-07-28, Fable solo, Dave live. Ran to spec: retrieval → option-select (3 picks, all recommended, read-back before build) → build `[64/64]` → wrap. One mid-flight re-price at the design beat (~38–40%, announced); the Amber crossing announced at build-close per M1, wrap chosen. Closed 🟡 **~58% ESTIMATE** (band from the remaining-budget table), reserve untouched, no unplanned forks.
> **PACE (perishable, replaces Tue 10:25):** panel Tue 11:18 BST — week 64.5% elapsed · All 55% ⇒ 0.85× · Fable 62% ⇒ 0.96× · catch-up to Thu 23:00 = All 1.27× / Fable 1.07× — Fable nearly on pace, All still behind; MORE-WINDOWS holds.)*
> **section-usage #23 (observed, self-report):** GM HDR:C LATEST:C PRIOR:R DOFIRST:C A:C C1:C C2:R C2b:R C3:R C4:C C4b:R C5:R STRATA:C · LS HDR:R SPIN:R DELTAS:C WEBFONT:R LIVE:R LIFECYCLE:R DEAD:R OPEN:R TARGETS:R SPINOFFS:R
> **section-sizes #23 (tiktoken cl100k_base):** GM HDR:1074 LATEST:799 PRIOR:1117 DOFIRST:2125 A:4208 C1:929 C2:1076 C2b:484 C3:181 C4:1204 C4b:256 C5:84 STRATA:632 · LS HDR:255 SPIN:1794 DELTAS:2242 WEBFONT:604 LIVE:4928 LIFECYCLE:965 DEAD:432 OPEN:4361 TARGETS:577 SPINOFFS:444 · totals GM:14169 LS:16602
#### 2026-07-28 #24

> **pre-flight:** fill ~28% + job 15–20% + wrap 8% = ~51–56% AMBER-projected · reserve 15% ring-fenced *(fill = 15.5% chain MEASURED 30,998 tk — the run's first fall — + ~7 harness inferred + read-render overhead; job = lane 1 step 3 O1′, priced at the opener)*
> *(Session #24, 2026-07-28, Fable solo, Dave live. Ran to spec: retrieval → design read-back + option-select ×4 (all recommended picks — the lanes-pilot promotion) → promotion pair → build `[67/67]` → wrap. The Amber crossing announced at build-close per M1, wrap chosen. Closed 🟡 **~57% ESTIMATE** (band from the remaining-budget table), reserve untouched, no unplanned forks. One mover refusal (blockquote-prefix anchor) caught by all-or-nothing, nothing written, corrected run clean — the #22 lesson holding as designed.
> **PACE (perishable, replaces Tue 11:18):** panel Tue 11:50 BST — week 64.8% elapsed · All 57% ⇒ 0.88× · **Fable 66% ⇒ 1.02× — ON PACE, first time this week** (0.78→0.91→0.96→1.02) · catch-up to Thu 23:00 = All 1.22× / Fable 0.97× — MORE-WINDOWS holds for All only; Fable spends at pace, no catch-up posture.)*
> **section-usage #24 (observed, self-report):** GM HDR:C LATEST:C PRIOR:R DOFIRST:C A:C C1:C C2:R C2b:R C3:R C4:C C4b:R C5:R STRATA:C · LS HDR:R LANES:C SPIN:R DELTAS:C WEBFONT:R LIVE:R LIFECYCLE:R DEAD:R OPEN:R TARGETS:R SPINOFFS:R
> **section-sizes #24 (tiktoken cl100k_base):** GM HDR:1032 LATEST:847 PRIOR:862 DOFIRST:2126 A:4208 C1:782 C2:1076 C2b:484 C3:181 C4:1204 C4b:256 C5:84 STRATA:882 · LS HDR:255 LANES:674 SPIN:1794 DELTAS:2221 WEBFONT:604 LIVE:4928 LIFECYCLE:965 DEAD:432 OPEN:4361 TARGETS:577 SPINOFFS:444 · totals GM:14024 LS:17255
#### 2026-07-28 #25

> **pre-flight:** fill ~30% + job 17–22% + wrap 8% = ~55–60% AMBER-projected · reserve 15% ring-fenced *(fill = 15.8% chain MEASURED 31,504 tk + ~7 harness inferred + read-render overhead; job re-priced 15–20%→17–22% at the "and this" scope-in, announced in-chat)*
> *(Session #25, 2026-07-28, Fable solo, Dave live. Ran to spec: survey → design read-back + option-select ×3 (all recommended) + mid-flight scope-in → build `[72/72]` → records flip (records FIRST, view, ⛔ line — routing check green pre-wrap) → wrap. Amber announced at build-close per M1. Closed 🟡 **~57% ESTIMATE** (band from the remaining-budget table), reserve untouched; the one unplanned finding (archive contract falsified by the corpus) was absorbed at minutes-cost, said in the banner, no fork needed.
> **PACE (perishable, replaces Tue 11:50):** panel Tue ~12:55 BST — week 65.4% elapsed · All 59% ⇒ 0.90× · **Fable 70% ⇒ 1.07× — AHEAD of pace, first time this week** (0.91→0.96→1.02→1.07) · to Thu 23:00: All 1.19× · Fable 0.87× — MORE-WINDOWS holds for All only; Fable now spends DELIBERATELY, not in catch-up.)*
> **section-usage #25 (observed, self-report):** GM HDR:C LATEST:C PRIOR:R DOFIRST:C A:C C1:C C2:R C2b:R C3:R C4:C C4b:R C5:R STRATA:C · LS HDR:R LANES:C SPIN:R DELTAS:C WEBFONT:R LIVE:R LIFECYCLE:R DEAD:R OPEN:R TARGETS:R SPINOFFS:R
> **section-sizes #25 (tiktoken cl100k_base):** GM HDR:999 LATEST:952 PRIOR:1001 DOFIRST:2132 A:4208 C1:820 C2:1076 C2b:484 C3:181 C4:1204 C4b:256 C5:84 STRATA:8 · LS HDR:255 LANES:727 SPIN:1794 DELTAS:2336 WEBFONT:604 LIVE:4928 LIFECYCLE:965 DEAD:432 OPEN:4361 TARGETS:577 SPINOFFS:444 · totals GM:13405 LS:17423
> **consult-receipts #25:** "modular search index adapters memento consult" → R-D5 · T-D1 · open-001 ; "band table amber threshold remaining budget" → runbook:context-gauge:the-floor-is-measured-never-assumed-and-this-is-the-only-cop ; "lane routing check blocking records" → lane:lane-1-memento
>
>
>
>
>

#### 2026-07-28 #26 — GAP, stratum written but never reached this file

> Audited #30 (2026-07-28). The stratum exists in `_GM-ARCHIVE.md` (rolled WHOLE by #27's wrap).
> Not recovered here: recovering it is a judgement about which half is the post-mortem, and #30 ran
> out of budget to do it verbatim. **Recorded as a gap so it stays visible** (2f/P1(b)).

#### 2026-07-28 #28 — RECOVERED at #30's audit

> **Provenance:** copied verbatim from `_GM-ARCHIVE.md` (Batch 2026-07-28 #29), where #29's wrap rolled
> the WHOLE stratum instead of splitting it per step 2f. The archive copy is left untouched — verbatim
> discipline outranks tidiness; this file is the authoritative dataset, the archive is a convenience copy.

> **pre-flight:** fill 17% + job 25% + wrap 8% = 50% AMBER-projected · reserve 15% ring-fenced *(floor MEASURED at the opener: GM 15,985 + LS 17,977 = 33,962 tk = 17.0%; harness ~7 pts inferred on top. Job priced 20–25% for "amend + three cheap gates", then **RE-PRICED DOWN mid-flight** when Dave's answers removed two of the three — forked to him with the numbers, he re-picked. Both announced in-chat.)*
> **CLOSED: 🟡 AMBER ~58–62% (ESTIMATE, unconfirmed out-of-band) — at the RED boundary; reserve untouched.** Overrun cause: not the job. The WRAP ran long — the 2c EXIT CHECK found three Dave-owed items with no standing home, the mover refused two anchors, and the compactable budget took four passes to clear 12K.
> **PACE (perishable, replaces Tue 14:25): NOT RE-READ THIS WINDOW** — the 14:25 panel was already ~1h stale at the opener; a fresh reading was asked for and not supplied, so this window spent against an unknown. ⚠ #29 must ask again — no gate can see it.
> **★ THE LESSON, for the next reader:** DV-D02 said horizontal bar was excluded; `Chart-bar:387` had carried `dv-fit` since the day it was built. **When a rule and its implementation disagree, do not assume the implementation is the defect** — check which one Dave actually ruled. The mirror-image failure landed in the same window: I read a grep COUNT and inferred a mechanism's state from it. **A count is not a measurement of the thing you care about.** Full arc: the 1b dossier.
> **section-usage #28 (observed, self-report):** GM HDR:C LATEST:C PRIOR:R DOFIRST:C A:C C1:R C2:C C2b:U C3:U C4:C C4b:U C5:U STRATA:C · LS HDR:R LANES:C SPIN:R DELTAS:C WEBFONT:R LIVE:R LIFECYCLE:R DEAD:R OPEN:R TARGETS:R SPINOFFS:R
> **section-sizes #28 (tiktoken cl100k_base):** GM HDR:1378 LATEST:1627 PRIOR:1412 DOFIRST:2310 A:4208 C1:842 C2:1157 C2b:484 C3:181 C4:1435 C4b:256 C5:84 STRATA:1276 · LS HDR:255 LANES:872 SPIN:1794 DELTAS:3045 WEBFONT:604 LIVE:4928 LIFECYCLE:973 DEAD:432 OPEN:4361 TARGETS:577 SPINOFFS:444 · totals GM:16650 LS:18285
> **consult-receipts #28:** "DV-D02 fit-to-width control cartesian charts exclusion lockup horizontal bar" → DV-D02 · DV-D10 · DV-D14 · R-D6 · T-D15 ; "fetch DV-D02 verbatim" → DV-D02 ; "fetch T-D15 verbatim" → T-D15 ; "chart title rule presence vs content" → none — the doors do not index `knowledge/guidelines/` rule TEXT by phrase, found by grep: dv-006 · dv-007 · dv-bar-001
> *(★ retrieval earned its keep: T-D15 came back UNBIDDEN and was what Dave raised two messages later. ⚠ The title rule needed a GREP — neither door indexes `docs/decisions/` (§C·4).)*

#### 2026-07-28 #29 — ROLLED at #30's wrap (late; #29's own wrap did not roll it)

> **pre-flight:** fill 17% + job 25% + wrap 8% = 50% AMBER-projected · reserve 15% ring-fenced *(floor MEASURED at the opener: GM 16,200 + LS 18,285 = 34,485 tk = 17.2%; harness ~7 pts inferred on top. Job re-priced TWICE mid-flight — the `set_content` finding, then the sweep turning a one-chart proof into a corpus question — both announced in-chat and both forked to Dave, who re-scoped on the second.)*
> **CLOSED: 🔴 RED ~68–72% (ESTIMATE, unconfirmed out-of-band) — reserve INTACT.** Overrun cause: the job was priced for one chart and one instrument; it cost four instrument corrections and a sweep. Dave was offered the reduced wrap at the Red boundary and **ruled full ritual**.
> **PACE (perishable, replaces Tue 14:25 — Dave supplied it at the opener, as #28 asked): Tue 17:40 — All 65% used vs 68.3% week elapsed = 0.95× (behind, 1.10× catch-up to Thu 23:00) · Fable 79% = 1.16× (ahead, 0.66× — ration).** Opus counts to All, which is why this window was Opus.
> **★ THE LESSON:** every correction came from **one measurement disagreeing with another**, never from reasoning about the code. **A single instrument agreeing with itself is not evidence — build the second one.** Arc: the 1b dossier.
> **section-usage #29 (observed, self-report):** GM HDR:C LATEST:C PRIOR:R DOFIRST:C A:R C1:R C2:U C2b:U C3:U C4:R C4b:U C5:U STRATA:C · LS HDR:R LANES:R SPIN:U DELTAS:C WEBFONT:R LIVE:R LIFECYCLE:U DEAD:U OPEN:U TARGETS:U SPINOFFS:U
> **section-sizes #29 (tiktoken cl100k_base):** GM HDR:1116 LATEST:1048 PRIOR:1664 DOFIRST:2474 A:4208 C1:842 C2:1157 C2b:484 C3:181 C4:1435 C4b:256 C5:84 STRATA:994 · LS HDR:255 LANES:872 SPIN:1794 DELTAS:3578 WEBFONT:604 LIVE:4928 LIFECYCLE:973 DEAD:432 OPEN:4361 TARGETS:577 SPINOFFS:444 · totals GM:15943 LS:18818
> **consult-receipts #29:** "axis text collision cropping clipped descender SVG text render proof" → DV-D15 · DV-D14 · T-D12 · DV-D10 · T-D9 ; "text cropping collision render proof getBBox axis label" → lane:lane-2-apollo-charts · gm:DOFIRST · ls:LIVE
> *(⚠ **the governing facts were NOT in either returned set** — ds-005 and `_validate_descender_clip.py`'s `text-box-edge` scope came from GREP. **Second instance of #28's gap**: the doors do not index rule TEXT by phrase, nor `docs/decisions/` — §C·4.)*

#### META — GAPS FOUND AT #30's AUDIT — sessions with no block in this file (P1(b))

> **#9 · #10 · #11 · #19** — absent, and absent WITHOUT a HOLE line, so nothing here records whether a
> stratum was ever written. **Not inferred either way** — the dataset simply cannot say. #14 is the
> counter-example: its absence WAS flagged, which is why #14 is countable and these four are not.
> ⚠️ **This file declares itself APPEND-ONLY and chronological (header, above). #27's block sits at
> line 7, above the #6→#25 run — prepended by #28's wrap.** Left in place, not re-sorted.
> Registered as **ds-022** in `knowledge/_DS-IMPROVEMENTS.md`: no gate reads this file, so step 2f's
> split is discipline with no receipt. [born #30 · guards: this line · until: ds-022 is ruled]

#### 2026-07-28 #30

> **pre-flight:** fill 27% + job 15% + wrap 10% = 52% AMBER-projected · reserve 15% ring-fenced *(fill = the floor MEASURED at the opener: 34,925 tk by the gate's unit, **54,458 CHARGED = 27.2%** — and the gap between those two numbers IS this session's first finding, ds-021. Job re-priced ONCE: opened as read-the-chain-and-pick, became a ritual audit on Dave's word, then a wrap on his word; both announced. ⚠ **This very line failed the wrap gate on its first write** — I wrote "floor/audit/wrap" instead of the canonical fill/job/wrap and the parser read the 27% floor as the whole fill, then correctly called AMBER a mis-read of GREEN. The gate was right; the stamp was prose. Fixed here.)*
> **CLOSED: 🟡 AMBER (ESTIMATE, unconfirmed out-of-band) — reserve INTACT.** No overrun: the audit came in at price; the wrap was the only unbudgeted beat and Dave called it.
> **PACE: NONE THIS WINDOW.** Asked at the opener per #29's instruction; Dave handed off before supplying a reading. **Last known is Tue 17:40 (All 65% = 0.95×, behind · Fable 79% = 1.16×, ration) and it is now stale.** Recorded as absent rather than carried forward — perishable readings are replaced, never stacked (2f retirement table).
> **★ THE LESSON:** **a measurement can be careful, repeated, gated, and still be in the wrong unit.** Five sessions measured the floor honestly with tiktoken and none of them measured the thing the window charges for. The gate was never wrong — it was precise about a proxy. ⚠ And the sibling: **the ritual's own output is not evidence the ritual ran.** #29's COMMIT STATE described a commit that did not exist, and the wrap gate passed, because no check reads `git log` or `_GAUGE-LOG.md`.
> **section-usage #30 (observed, self-report):** GM HDR:C LATEST:C PRIOR:R DOFIRST:R A:C C1:R C2:U C2b:U C3:U C4:R C4b:U C5:U STRATA:C · LS HDR:R LANES:R SPIN:U DELTAS:C WEBFONT:U LIVE:R LIFECYCLE:U DEAD:U OPEN:U TARGETS:U SPINOFFS:U
> **> **section-sizes #30 (tiktoken cl100k_base):** GM HDR:1363 LATEST:1050 PRIOR:1111 DOFIRST:2474 A:4208 C1:842 C2:1157 C2b:484 C3:181 C4:1435 C4b:256 C5:84 STRATA:8 · LS HDR:255 LANES:872 SPIN:1794 DELTAS:3646 WEBFONT:604 LIVE:4928 LIFECYCLE:973 DEAD:432 OPEN:4361 TARGETS:577 SPINOFFS:444 · totals GM:14653 LS:18886**
> **consult-receipts #30:** none — the window audited the ritual against its own runbook and gates, so retrieval was `_RUNBOOK-capture-ritual.md` + `_capture_gate.py` + `_RUNBOOK-context-gauge.md` read direct, plus greps of `_GAUGE-LOG.md`/`_GM-ARCHIVE.md`. **Honest negative:** the doors index records, not procedure — "was step 2f run?" is not a question `_memento_search.py` can answer, and that is the same shape as #28's and #29's misses.
#### 2026-07-28 #31

> **pre-flight:** fill 27.5% + job ~10% + wrap 10% = ~47% AMBER-projected · reserve 15% ring-fenced *(fill = floor MEASURED at the opener in BOTH units: 35,079 tk cl100k = 17.5% by the gate's unit, ~55.1K charged = 27.5% actual, harness on top; job = the throttle rulings, chat-shaped, no build. ⚠ The projection already exceeded the 45 ceiling this session went on to rule — recorded, not excused. The ENACT build was then priced ~15–20 and REFUSED at ~50% fill by the fresh stop line: forked to #32. That refusal is the ceiling's first enforcement, applied to its own author.)*
> **CLOSED: 🔴 RED-edge ~62% (ESTIMATE, unconfirmed out-of-band) — reserve intact.** Overrun cause: the wrap began AT the stop line (60 − wrap) and cost more than its 10-pt price — rulings inscription + first dual-unit bookkeeping. This block is itself the next point in ds-023 (c)'s overrun dataset.
> **PACE (perishable, replaces Tue 17:40): Tue ~19:15 — All 66% vs ~69.2% elapsed = 0.95× (behind; catch-up 1.10× to Thu 23:00) · Fable 80% = 1.16× (RATION; 0.65× from here).** This window was Fable (rulings = open judgment); #32's enact is Opus-shaped.
> **★ THE LESSON:** a ceiling ruled mid-session governs that same session — and the second banner-vs-git falsification in two sessions (`__tmp_moved.html` "untracked" → tracked again one commit later) says the check is `git ls-files`, never prose. Unit pairs this window: GM ×1.563 · LS ×1.540 (Read-tool vs tiktoken; file-diversity still n=2).
> **section-usage #31 (observed, self-report):** GM HDR:C LATEST:C PRIOR:R DOFIRST:R A:C C1:U C2:U C2b:U C3:U C4:R C4b:U C5:U STRATA:C · LS HDR:R LANES:U SPIN:U DELTAS:C WEBFONT:U LIVE:U LIFECYCLE:U DEAD:U OPEN:R TARGETS:U SPINOFFS:U
> **section-sizes #31 (tiktoken cl100k_base):** GM HDR:1170 LATEST:792 PRIOR:1113 DOFIRST:2474 A:4208 C1:842 C2:1157 C2b:484 C3:181 C4:1435 C4b:256 C5:84 STRATA:8 · LS HDR:255 LANES:872 SPIN:1794 DELTAS:3339 WEBFONT:604 LIVE:4928 LIFECYCLE:973 DEAD:432 OPEN:4361 TARGETS:577 SPINOFFS:444 · totals GM:14204 LS:18579 *(measured pre-stratum)*
> **consult-receipts #31:** none — the window's questions were procedural + state-shaped: direct reads of `_RUNBOOK-capture-ritual.md` · `_gm_move.py` docstring · ds-021/022/023 ledger blocks, plus `git log`/`git ls-files` receipts. Honest negative: no design question was open that the doors index.
