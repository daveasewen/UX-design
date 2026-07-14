# End-to-end proof run — checklist

*Walk ONE real screen through the whole line, by hand. You are the conveyor.*
*Goal: scope → standards-compliant hi-res prototype, with the gate catching ≥1 real thing.*

**The screen:** Review & confirm a payment.  *(Swap for any small, real screen you can get.)*
**Why this one:** small, high-stakes, exercises your gates — PII masking, error states, amount contrast.

---

## Before you start
- [ ] Get the existing screen (design, screenshot, or live URL)
- [ ] Confirm the build is green: `cd knowledge && python3 _build_all.py`
- [ ] Canon to hand — gated snippets are your build *materials* for now

## ① Order desk — write the spec  *(you + Claude, ~45 min)*
Turn the screen into checkable criteria. **This list IS the gate at ③ (the spine).**

**The job:** "confirm I'm paying the right person the right amount before I commit."

**Riskiest assumptions — test these:**
- [ ] User trusts the amount is right → is the amount the most prominent element?
- [ ] User can spot a wrong payee → are payee name + masked account both shown?
- [ ] User understands fees before committing → is the fee shown pre-Confirm?

**States present:**
- [ ] Loading (fee / balance fetching)
- [ ] Error — insufficient funds
- [ ] Error — payment failed / network
- [ ] Zero fee shown explicitly (not blank)
- [ ] Very long payee name wraps / truncates cleanly

**Standards — your gates check these:**
- [ ] Account number masked ••••1234 (PII)
- [ ] Amount meets AA contrast + size token; not colour-only emphasis
- [ ] All text AA contrast — light AND dark
- [ ] Visible focus on every control (`focus/ring`)
- [ ] Confirm = primary, not destructive; one primary action only
- [ ] Hit targets ≥24px (≥44px touch)
- [ ] Reduced-motion honoured if anything animates
- [ ] Only canon components / tokens — no invented hexes

**Out:** save as `spec.md`. Keep it — ③ runs against it.

## ② Moulding machines — generate  *(by hand for now)*
- [ ] Produce 2–3 versions on ONE meaningful axis (e.g. how much fee detail shows)
- [ ] Build from your gated snippets (already compliant) — or Figma Make
- [ ] *Later: this becomes a model call behind your API. Same input, automated.*

## ③ QA + rulebook — gate
- [ ] Run each candidate through the build gates (contrast · dark-surface · token-fidelity · a11y)
- [ ] Check each against the ① spec by hand (states present? account masked?)
- [ ] Reject any that fail — the line stops. **Write down what failed.**

## Taste gate — you, ~20 sec
- [ ] Pick the nicest survivor (they're all already accessible + valid)

## ④ Finished product — prototype + handoff
- [ ] Export the chosen screen as a hi-res, standards-compliant prototype
- [ ] One-page handoff: tokens used · states · WCAG criteria met

---

## Done when ✅
- [ ] One real screen went end-to-end
- [ ] The ① criteria were literally the ③ checks
- [ ] **The gate caught ≥1 thing a human would've missed** ← your first signal from *outside* the system

## Who's who (until the harness exists)
- **You** = the conveyor (carry artifacts between stations)
- **Claude** = the worker at each station
- **`_build_all.py`** = the inspector
- Doing this by hand is how you'll spec the harness — every handoff is a future API contract.

## When Sutherland lands
- Stations ① (spec) and ③ (gate) **don't change** — they're durable.
- Only the **materials** at ② swap: gated snippets → Sutherland React components.
- Your finesse + token fixes flow back **into** Sutherland (it has neither nailed yet).
