# #159 — the four hunks, and the eye that closed them

provenance: 159 · 2026-08-12
status: observed

*Session #159, Wednesday 2026-08-12. FABLE conductor + this delegated OPUS wrap sub, Dave live.
**No ruling was made this session** — that is not a shortfall, it is the shape: #158 left three
residuals that could only be discharged by *reconciliation* and by *Dave's eye*, and both were
discharged. Spine entries: `GOOD-MORNING.md` ★ LATEST #159 · `_LIVE-STATE.md` ⏱ LATEST #159.
No new `knowledge/_rulings.json` entry — the count stands at 122.*

---

## 1. Why residual ① could not be closed by the obvious command

`gen_canon_components --check` had been RED since #158 with `rc=1`, and the obvious repair —
regenerate until it is green — was **precisely the repair that was forbidden**. Three of the four
hunks were places where `canon.css` was BEHIND ruled text that lived in a snippet comment, and one
was a place where `canon.css` was AHEAD (the `s157-D1` positive seat). A single blind regenerate
would have healed the fourth and **silently erased the ruled text in the other three**: the exit
code cannot tell the two directions apart, and the record cannot recover from the wrong one.

So the lane was run as **four hunks, five decisions**, each decided on its own merits:

- **(a) Tabs — the `s149-D1` badge comment.** The AMENDS clause (*"was light `#B92F1E` / dark
  `#CC4333`, white numeral"*) was added into `knowledge/snippets/Tabs.reference.html`'s `:root`
  comment. And here the interesting thing is what could NOT be done: **the generator never carries
  `:root` comments into the synthesized scope block at all**, so this clause can never appear in
  `canon.css` however the hunk is decided. That was accepted rather than engineered around — the
  ruled text lives at the SOURCE, and the artefact's silence about it is now a known property of
  the generator rather than an open red.
- **(b) Selection-controls — `--error-atom`.** Re-homed to the token manifest as
  `"--error-atom": "rag/error-ink"`, so canon emits `var(--rag-error-ink)` — the `s158`
  single-source form. The snippet keeps its per-mode literals so it still renders standalone; the
  two are not in conflict, they answer different questions.
- **(c)+(d) Selection-controls — three truncated comments.** Restored to their full ruled text:
  `s151-D1` clause 3, `s151-D3` legs 1 and 2, and `s151-D2` pick 1, including the specimen path
  `_review/atoms-reach-and-star-v1.html` and the measured contrast values. A truncated ruling reads
  as a complete one; that is the whole hazard.
- **(e) Amount-display.** The only hunk where the snippet was the newer truth — canon **accepted**
  the `s157-D1` positive seat via regenerate.

Verified at this wrap, not relayed: `python3 knowledge/canon/gen_canon_components.py --check`
returns **rc=0**, *"75 components in sync"*.

## 2. Residuals ② and ③ closed by the only instrument that could close them

#158 had ended with three visual changes nobody had looked at, and a fourth item — the white
8%/14% wash at medium — that was explicitly labelled a **reading of `s149-D1`'s text**, not a
ruling, and explicitly **vetoable once rendered**.

`_review/159-unseen-three-v1.html` was put in front of Dave live. His words: ***"these all look
good… this is great!"*** That approved, in one motion:

1. the `s149-D1` dark-ink banner **including** the wash-medium reading — **the veto was not
   exercised**, so residual ③ closes by approval rather than by expiry;
2. the `s158-D3` negative seat;
3. the supercharge-light pressed grey `#524842` → `#AA9B92`.

★ **These are sight-verified ENACTMENTS, not new rulings.** The distinction is worth the sentence:
the values were already ruled; what was missing was the confirmation that the enacted artefact
looks like the ruling. Recording this as "Dave ruled X" would launder a confirmation into a
decision, and the next session would inherit a ruling that never happened.

⚠ One thing was **floated and is not standing**: Dave said a larger review of the components may
tweak these later. That is a float. It is carried on the residual as a float and creates no
obligation on #160.

## 3. What was measured rather than inherited

- `_validate_palette_tier.py` — **rc=0** (4 themes, 3 palettes, 38 declared keys, 75 metas,
  75 manifests).
- `_validate_snippets.py` — **rc=1**, and the nine fails were **counted off the run by file**:
  Alert ×3, Badge ×2, Form-layout ×1, List-items ×3. Identical to the known set; **no new fail**.
  All nine await Dave's values and none is a gate defect.
- The disk: `/` at **98% (253 M free)**, `/sessions` at **100%**. This is the **fourth** ENOSPC
  instance against the carried runbook-correction item. tiktoken was fenced to
  `PYTHONPATH=/var/tmp/pylib` and every temp write went to `/var/tmp`. The fence is not a standing
  environmental fact and was re-measured, not inherited.

## 4. What is still open

The nine snippet fails (Dave's values), the floated larger component review, palette names/splits,
non-mono coloured monetary text, the no-args write-freedom leg, the `none`-unbound delta, and the
long tail of prior carries — all on the `residual → #160` list with their ages. **Nothing on that
list was ruled, re-prioritised or given a close condition by this wrap.**
