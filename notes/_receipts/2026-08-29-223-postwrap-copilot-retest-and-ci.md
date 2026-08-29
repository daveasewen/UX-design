# #223 POST-WRAP — Dave's Copilot retest, the CI billing diagnosis, and the APCA park

provenance: 223 · 2026-08-29
status: observed

*Written by the #223 post-wrap capture sub against the brief
`notes/_briefs/2026-08-28-223-postwrap-capture-brief.md`. Events AFTER the wrap commit
`97bd458`. ⛔ **Nothing here is ruled.** Every disposition below is `#224`'s, with Dave's word
and the forensics in hand. `knowledge/_rulings.json` is untouched by this pass — `git status`
is the proof.*

---

## ① DAVE'S COPILOT RETEST HAPPENED — the `W-244` acceptance event, and its outcome is AMBIGUOUS

**His words, verbatim, in chat (2026-08-29):**

> "worked pretty well, the token count didn't work as far as I could see, tiktoken definitely
> didn't install it was blocked by the company security, but I used GPT Sol wrote its own code
> and seems to have fixed it. we might have to port it back."

**What is KNOWN from that sentence, and nothing beyond it:** the pack ran on his company
machine ("worked pretty well") · **tiktoken did not install — blocked by company security**,
which is the `W-244` premise hitting for real a second time · the **token count did not work**
as far as he could see · **GPT wrote replacement code inside his copy of the pack** and, on his
reading, fixed it · he raises **porting it back** as a possibility, not a decision.

⚠ **THE DECISIVE UNKNOWN: WHICH PACK VERSION HE TESTED. NOBODY KNOWS YET.** The v1.0.2 pack
exists precisely so tiktoken is *not* needed — `s222-D2` vendored the encoder and `s222-D3`
enacted a pure-Python exact fallback. So "the token count didn't work" has **two live readings
and this receipt refuses to pick one**:

- **Reading (a) — HE TESTED v1.0.1.** Then the failure is the *already-fixed* class: v1.0.1
  had no vendored encoder and no fallback, so a security-blocked tiktoken is exactly the
  predicted stumble, and v1.0.2 already answers it. The port-back would then be unnecessary,
  and the real finding is a **distribution** one — he was holding the old pack.
- **Reading (b) — HE TESTED v1.0.2.** Then this is a **NEW failure class**: the vendored
  encoder and/or the purepy fallback did not do their job on a real locked-down corporate
  machine, and the bake's central claim is not yet earned in the field. GPT's code would then
  be evidence about what the fallback got wrong.

**Neither reading is preferred here.** The evidence that discriminates them is the pack folder
itself, which Dave is staging (see below) — a version string and a sha comparison settle it in
one pass, and guessing before that pass is the exact shape of a confident false inscription.

**The evidence route, as Dave and the conductor staged it:** Dave copies the GPT-modified pack
folder into the project folder (suggested name `_incoming-copilot-pack`). A forensics sub then
(i) diffs every file against the shipped `_MANIFEST.json` shas to identify **which pack version
was tested** and **every GPT-touched file**, (ii) extracts and classifies GPT's replacement
code, (iii) prices the port-back, and (iv) files a decision surface for Dave at the `#224`
opener. **Row: `W-263`.**

⛔ **`W-244` IS NOT CLOSED AND ITS STATE IS UNCHANGED BY THIS PASS.** The retest is its
acceptance event, but an ambiguous acceptance closes nothing; the disposition is `#224`'s.
⛔ **And this receipt does not declare the retest passed or failed.** "Worked pretty well" with
a broken token count and a third-party patch is not a verdict either way — it is a reading Dave
gave of a machine only he can see.

---

## ② CI — the instant-death era was GITHUB BILLING; Dave fixed it, run #454 was re-run

- **Diagnosis, this session:** the runs that died instantly across **#443–#454** were failing on
  **GitHub billing**, not on repo state. That is the cause of the un-answerable CI read-back the
  `#223` COMMIT STATE block declared blocked ("it cannot be answered until the billing red is
  cleared").
- **Dave cleared the billing today (2026-08-29)**, and the conductor triggered a **re-run of
  run #454** from Dave's signed-in Chrome.
- **State AT BRIEF TIME, and it is not a verdict:** run status **"In progress"**; the `release`
  job had finished in **15s carrying an exit-1 annotation**. ⚠ **The `#221` read-back precedent
  says that exact shape was the ADVISORY ship-list-drift step of a job that SUCCEEDED** — and a
  run-page annotation is not a job verdict. ⛔ **This receipt asserts NEITHER outcome**; the
  conductor reads the final verdict in Chrome and relays it in chat (`s203-D1`).
- **The sandbox cannot read it** — the Actions API returns 404 for this private repo from here,
  so no verdict in this receipt could be first-hand.
- ⬛ **OWED AT THE `#224` OPENER: this commit's own read-back.** The post-wrap commit that lands
  this receipt triggers the **first fully-billed run since the fix** — the first CI signal in
  twelve runs that is about the repo rather than about an account. Its verdict is the next
  session's to read and inscribe.

---

## ③ APCA — parked, and already in the record

Verified in git, not asserted: commit **`709c132`** (2026-08-29 10:03) carries
`notes/_briefs/2026-08-28-223-apca-research-parked.md` — the `08-28` stem is the session's date
key, the commit landed `08-29` — and store row **`W-262`** (state `parked`, owner claude,
opened 223). Dave's instinct — *"this seems better than WCAG"* — is recorded there with the
five scoped research sections and his own close condition. **No action is owed on it by anyone
until he asks**; it is parked, not queued.

---

## What this pass did NOT do

No ruling written · `knowledge/_rulings.json` untouched · **no row closed, reworded or
re-scoped, of anyone's** · `W-244` state unchanged · no roster, release or theme disposition ·
the parked lists stay parked. This is a POST-WRAP FOLLOW-UP capture (`#221`/`#219` precedent),
not a second wrap: `GOOD-MORNING.md` gains a post-wrap addendum line under its ★ LATEST banner
(step 5b) and nothing else; the `size:` stamp, the banner stack and the strata are the `#223`
wrap's and are untouched.
