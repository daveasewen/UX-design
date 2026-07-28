# _GAUGE-LOG — session pre-flight/post-mortem measurements

provenance: local_e79e89ee-51cb-4a74-bf95-b7cf3e303af9 · 2026-07-27
status: observed

*Contract (runbook step 2f, GM-D5(a)): APPEND-ONLY · one block per session, chronological ·
measurements only (pre-flight estimate vs closed band, overrun + cause) · NOT in the cold-start
read chain. This file exists so the throttle's 15% reserve can be re-derived from data (Half 0b).
Blocks below moved VERBATIM from `GOOD-MORNING.md` §C strata at the first 2f roll (session #15).*

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

*(rolled 2026-07-28 #20 per 2f. ⚠ #19 wrote no stratum — its gauge story lives in its banner; recorded as a gap, not reconstructed.)*
