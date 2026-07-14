# Payments journey — semi-structured interview guide
*For the depth chat with the colleague close to the journey. ~25–30 min.*
*Doubles as a first prototype of the guided-JTBD intake lane — note what works to run, what feels clunky.*

**How to run it:** same backbone every time, but follow the threads. The probes (→) are there so depth stays consistent however the conversation flows. **Capture evidence, not opinion** — tag every answer as `[FACT]`, `[ASSUMPTION]` (anything "we thought / everyone felt"), or `[EVIDENCE → where]`.

---

## 0. Framing — say this first (~1 min)
> "I'm not reviewing the work or anyone's decisions. I'm trying to reconstruct what a solid discovery *would* have defined for the payments journey, so we can spot what might bite us after go-live — and build a lightweight way to avoid that next time. Mostly I want what's actually happening, not the polished version."

---

## A. Current state & pain  *(ground truth — spend the most time here)*
1. Where is the payments journey right now — shipped, in build, live to whom?
   - → What's the current scope vs what was originally intended?
2. What's actually going wrong or feeling hard right now?
   - → "Slow" / "messy" — slow *where*, measured *how*? Can you put a number or example on it?
   - → Where's the rework concentrated — which steps or screens keep getting redone?
   - → Any complaints, escalations, drop-off, or support load you can point to?
> *Buys: the real failure the rigor would have caught — the spine of the proof.*

## B. Success & the disagreement
3. Was there ever a definition of "done" or "good" for this — a target or metric?
   - → If not: what do people *now* say it should have been?
4. You mentioned lots of opinions — what do people actually disagree about?
   - → Who wants what, and why? Where are the fault lines?
   - → When there's a clash, how does it get resolved today — who decides?
> *Buys: the reconstructed spec, and proof that the disagreement IS the missing criteria.*

## C. Users & the job
5. Who is this journey primarily for, and what are they trying to get done?
   - → What's the actual job — what does a good outcome look like *for them*?
6. The 1–2 test customers — who are they, and how representative of the real base?
   - → What might we be missing by testing only on them?
> *Buys: the JTBD seed; flags if the test base is too narrow to trust.*

## D. Assumptions
7. What are we treating as obviously true that nobody's actually checked?
   - → On users, on demand, on the tech, on how people pay today?
   - → If one of those assumptions turned out wrong, which would hurt most?
> *Buys: the riskiest-assumptions list — the heart of the gap report.*

## E. Evidence & constraints
8. What are decisions currently based on — research, analytics, tickets, competitor parity, or instinct?
   - → Is there any data we already hold that we haven't really used?
9. What are the hard constraints? (it's payments — there will be)
   - → Regulatory, security, PII / data-masking, existing rails, tech limits?
> *Buys: secondary evidence to ingest, plus the "constitution" — the non-negotiable gates.*

## Close — the artefact ask
> "Could you share anything concrete — tickets, analytics, a deck, a Slack thread, the original brief if there is one? I'd rather work from real material than memory."

And: "Who else holds a strong opinion on this? I want to send them a 5-minute version to map where everyone stands." *(→ feeds the questionnaire)*

---

## Quick capture template (use live)
| # | Note | Tag | Follow-up / artefact to chase |
|---|---|---|---|
| | | FACT / ASSUMPTION / EVIDENCE | |

*After the chat, the FACTs + EVIDENCE rebuild the spec; the ASSUMPTIONs become the riskiest-assumptions list; the pain in §A becomes the "what would've bitten us after go-live" payoff.*
