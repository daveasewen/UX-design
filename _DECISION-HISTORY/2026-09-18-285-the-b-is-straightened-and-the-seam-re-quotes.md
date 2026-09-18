# #285 — the B is straightened, the seam re-quotes, and the connector answer comes by act

provenance: 285 · 2026-09-18
status: observed

*The WHY and the HOW of #285. The WHAT lives in the terse records: `_LIVE-STATE.md` § ⏱ LATEST
DELTA #285 · `GOOD-MORNING.md` § ★ LATEST · `_CARRIES.md` § `residual → #286` ·
`_HANDOFF-136-the-b-is-straightened-and-the-connector-answer-comes-by-act.md` · the seven filed
reports under `notes/_subreports/2026-09-18-285-*.md`. His words, verbatim and never paraphrased:
`notes/_lanes/285/DAVE-RULINGS-2026-09-18.md`. The ledger is pointed at as UNCHANGED, which is the
honest link when nothing was inscribed: `knowledge/_rulings.json` stays at **620**.*

---

## 1. The session opened by falsifying the session before it

#284 closed with a headline: *the 40 per-size logo masters are drawn and Dave accepted them by
eye.* His word off the contact sheet had been **"the sheet is good BTW"**, and the #284 wrap
wrote that acceptance into the banner, the delta, the carry set, the sign-off register and the
cloud store.

#285 opened with him looking at the same sheet again and saying **"the scaling is wonky"**.

The first move was wrong, and it is worth recording because it is a class. The conductor read
"wonky" as a **contact-sheet layout bug** — `transform: scale(4)` does not reserve layout, so a
4× panel overlaps its neighbours, and that is a real defect of that page. It is also the cheapest
available explanation, and it explains the symptom without touching the artefact. Dave did not
accept it. He came back with a **4× crop of the wordmark itself**:

> *"Maybe we misunderstand each other on the logo scaling, see image the word mark is distorted,
> look at the B"*

★ **The lesson is not "the conductor guessed wrong".** It is that a cheap explanation which
covers the symptom is the most dangerous kind, because it retires the question. The crop is what
made the question un-retireable: it showed the defect at a magnification where prose could not
argue with it.

## 2. There were two causes, and the one nobody named was the worse one

Lane LM2 went to `snap_wordmark()` in `knowledge/assets/logos/_gen_masters.py` and found the
named cause immediately: the old code marked every on-path node taking part in a straight `H`/`V`
segment **inside** curved glyphs (S, B, C) and rounded it to whole pixels, while leaving the
cubic **control points** scaled only. A bowl leaves the stem at exactly such a node. Move the
node half a pixel, leave its handle behind, and the curve kinks at the join and flattens on the
way out. That is the lumpy counter in Dave's crop.

Then it found the cause the task had not named, and it was larger:

```
kx = (W - Lx) / (R - L)        ky = capH / (B - T)
```

Two scale factors, used on the two axes. Measured per step, `kx/ky` reads
**1.0039 / 0.9949 / 1.0436 / 0.9949 / 0.9896**. At h=32 the wordmark was drawn **4.4% wider than
it was tall** — a genuine horizontal stretch of every glyph in the lockup, entirely independent
of any snapping.

⛔ **The part that matters for the record is why #284 could not see it.** That lane's own probes
counted anti-aliased pixels and stem runs. **Neither instrument can see an aspect error.** The
lane was not careless; it was measuring the thing it had built an instrument for, and the defect
lived in a dimension the instrument had no axis for
[[instrument-without-a-consumer]] in reverse — a consumer with no instrument.

★ **So #284's acceptance was not a lie and was not a mistake of judgement. It was a claim about
the world published at the resolution the session could measure**, and Dave's eye had a higher
resolution than the probe. That is why this wrap STRIKES the carry rather than quietly updating
it: `s183-D1`'s strike form exists for exactly the case where a claim was corrected, and
`s188-D2` requires the strike to name the session that proved it false and where the correction
is inscribed. Both are named on the struck line.

## 3. The fix was a subtraction, not an addition

`quantise_runs()` was **deleted** — 32 lines, and with it the H's whole-pixel / stem-pairing
ladder. `snap_wordmark()` was rewritten from 43 lines to 30 as a **rigid move**: one uniform
scale `s = h/85` — deliberately the same factor the hexagon is drawn at, so the lockup
relationship stays exact — plus one translation `(dx, dy)` applied to every coordinate the path
model yields, **nodes and control points alike**, through the existing `coords()` iterator.

No coordinate moves relative to any other coordinate. The wordmark that comes out is the wordmark
that went in, at a different size and place. The tally keys changed to `rigid_nodes` /
`rigid_controls` / `snapped_nodes`, and `snapped_nodes` is `0` **so that the report can assert
it** — the assertion is the point of the key existing.

⚠ **The H was not exempted.** The task allowed keeping the H's whole-pixel snapping if it could be
justified; the lane did not take the exemption, because a lockup with one rigid element and one
snapped element is two coordinate systems in one drawing.

## 4. The verifier is why the commit lane was cut, and his enthusiasm is not

Lane V ran adversarially: every claim of LM2 and SC tested against the live files by running the
thing or parsing the file, **no claim accepted from either lane's prose**. **16/16 PASS**, with
the decisive one — claim 6, that the wordmark is one uniform scale and one translation over nodes
AND control points, with no per-node snapping and no `kx≠ky` — carrying a **max residual of
5.4e-5 px** against the Figma source. Two caveats travel with it (one a wording matter on the
width claim, one a sub-pixel property inherited from the source rather than manufactured by the
lane); neither is a defect, and both are carried rather than smoothed.

Dave's response to the regenerated masters, the STANDING block and the 16/16 was
**"excellent work!"**.

⛔ **That sentence is enthusiasm and it is not a ruling** (`s271-D4`), and the record says so in
every place it appears. The commit lane was cut **on the verifier's pass**, not on that line. His
acceptance came separately and in a form that cannot be mistaken for anything else: a numbered
answer to a numbered question — **"2. accept"** — which is why the eye-half of `W-285lm` is closed
and the registration half is not.

## 5. The messy-middle finding, and the smallest possible thing to do about it

He pasted a research note on the *lost in the middle* phenomenon with three words: **"Is thre
anything here we can use"**. The conductor's read, which he then approved with **"Okay this sound
good."**, was deliberately narrow:

- **tactic 1 — front-load the rules and re-quote the constraints at the tail — is usable here;**
- output-priming is API-only and not available in Cowork;
- context hygiene and retrieval-first are already the chain's own rules, so they are not a finding.

Then: **"go on both this and: yes to the seam re-quoting the standing constraints"**.

★ **Why the seam and not the handoff.** Everything a session reads at its opener — handoff,
chain, check-in, the memory index, about 80K — becomes **the middle** of the context the moment
work starts. A standing rule inscribed in the handoff is, by the end of the first lane, sitting
exactly where U-shaped attention is weakest. `_seam.py` already runs *before every lane is cut
and after every lane lands*. Re-quoting the constraints at its **tail** puts them at the recency
end, every time, for the price of 246 tokens. The block prints LAST, after SCRATCH, and the
docstring says it must not be moved above it — because its position **is** the mechanism.

⛔ **And the file it quotes is a DRAFT.** `knowledge/_standing.md` says so in its own header.
Eight lines were drafted **from the record**, each with its receipt in parentheses; the seam
re-quotes them and **never inscribes them**. The wording of those eight is Dave's, line by line,
and `W-285sc` is open on exactly that. A constraint that a lane drafted and an instrument recites
is not a ruling, however often it gets printed.

## 6. The connector question was answered by an act

#284 carried an open item — *which connectors does Apollo need* — asked and unanswered. It was
the stated precondition of a boot experiment.

He answered it without a sentence. Asked about context management, he showed the setup
(**"this is how the setup stand now"**, **"I havnt touched anything and computer use is off"**),
kept deep-research after asking **"but deep research might be useful no? is it big"** — a skill
costs its description only, about 80 tokens — and then **set the built-in Browser's seventeen
tools to BLOCKED in Tool permissions.** The `mcp__Claude_Browser__*` server dropped out of the
conductor's tool set inside the same session.

★ **That is a cleaner experiment than the one that was asked for.** One variable, changed by the
person whose window it is, against a boot figure measured the same day: **80,863 real**. #286's
first move is therefore a **measurement, not a lane** — read boot cold at the opener and compare.
Skills stay untouched **by design**, so that if the reading moves, the cause is not ambiguous; a
second run follows only if the first one moves.

⚠ The boot ceiling does not move either way. `BOOT_CEILING_TK` is 70,000 and SHRINK-ONLY; today's
80,863 is the **tenth** post-diet reading over it. The remedy is to cut the boot, and this is the
first session in ten to have an actual lever aimed at it.

## 7. The delegation rule, measured from the other side

#284's largest open item was Dave's own sentence about delegation — everything delegated, the
conductor an orchestrator and judgment layer — recorded as ruling-shaped and **not inscribed**.
#284 measured the lapse: four in-seat lane jobs, one actual lane.

#285 is the counter-measurement, and it was taken at this wrap seat from the conductor's own
transcript rather than asserted:

| lane | seat | what it did |
|---|---|---|
| LM2 | `Agent`, opus, depth 1 | regenerate the 40 masters |
| SC | `Agent`, opus, depth 1 | the seam's standing-constraints tail |
| V | `Agent`, opus, depth 1 | adversarial verification of LM2 + SC |
| C | `Agent`, opus, depth 1 | the commit (`b99d092c`) |
| C2 | `Agent`, opus, depth 1 | the showroom re-sync commit (`ff354475`) |
| P | `Agent`, opus, depth 1 | the push attempt + CI read-back |
| W | `Agent`, opus, depth 1 | this ritual (on its second attempt) |

**No lane work was done in seat.** The conductor's in-seat tool output was three seam reads, one
tiktoken measure, two directory listings, four image reads (his screenshots) and one shot read.

★★ **The price, both sides, because only both sides make it an argument.** The seven lane replies
cost the conductor's window **3,382 cl100k in total** — the `s218-D7` stub contract doing exactly
what it was ruled to do — against **≈738,851 real of sub FILL** across the seven seats. Roughly
0.5% of the work's context passed through the window that decides.

⛔ **This does not close the carry.** His sentence is still ruling-shaped and still uninscribed;
one session's obedience is evidence that the shape is affordable, not a rule that it is required.

## 8. Three things that went wrong, and what each one is evidence of

**(a) The push refused, correctly.** Lane P ran `bash knowledge/_git_commit.sh --push` — the only
sanctioned push path — and got:

> `✗ push refused: tree not clean — commit first (s133-D2; rehearsal log excluded per s137-D1).`

The three dirty paths belonged to other lanes (the rulings-file edit and the C / C2 subreports).
The lane was forbidden to commit, so it stopped and said so. ★ **A lane that refuses to widen its
own scope to clear its own blocker is the lane contract working**, and it is why this wrap
inherited a clean question rather than a mystery.

**(b) `W-285lm2` was refused by the store's id pattern.** `_state.add()` returned
`REFUSED: W-285lm2: id does not match '^(?:W-[0-9]{1,3}[a-z]{0,2}|G[0-9]{1,2}[a-z]?)$'` — the
pattern allows at most two trailing lowercase letters and **no digit after them**. The row became
`W-285lm`. This is a finding, not a defect to fix at a wrap: the brief named an id the store
cannot hold, and the store said so loudly rather than coercing it.

**(c) A wrap sub died mid-ritual.** #285's first wrap sub reached five reads and **90,605 real**,
then took `API Error: Can't reach the API server — check your internet or DNS (ENOTFOUND)` at
**14:52:22Z** and stopped, eleven usage records in.

✅ It had written nothing. `notes/_lanes/285/W/` was empty when the retry opened and the tree
stood exactly as the lanes had left it.

⛔ **That is luck, and the record should say so rather than enjoy it.** `_gm_move.py` guarantees
all-or-nothing **per transaction**; nothing guarantees it across the ritual. A sub that died
after a 2c move and before its receipts were read back would hand its successor a half-rolled
banner with green receipts nobody had read — the #166 stale-msgfile shape arriving through a
different door. Whether the ritual owes a **resume contract** — a written marker of which steps
have landed — is ruling-shaped and is not inscribed here.

## 9. The seventh gate fail was ours, and the shape will recur

Seven blocking gate fails stood when this ritual opened; six stand at its close.

Six are inherited and carried in the `#243` declared-not-a-wrap form — the boot-drift **CEILING
BREACH** (seven post-diet readings over 70,000) and **five boot double-counts** (#243, #264,
#272, #273, #274). Every one is another session's append-only testimony in `notes/_GAUGE-LOG.md`,
and **a wrap may not repair an inherited gate fail**: the ceiling's remedy is to cut the boot,
never to raise the literal, and raising it is Dave's word alone.

The seventh was this seat's own. `ds-021 (C)` fired:

> `` `knowledge/_seam.py` counts tokens (cl100k) and is NOT in MEASURERS — an UNREGISTERED measurer ``

Lane SC had given the seam a counting site (`standing_tokens()`) in **this session's own commit**
`b99d092c`, and nothing registered it. It is entered here as **`estimate-only`** — it encodes with
tiktoken cl100k only, never calls `_gauge_tokens.count()`, has no API path, and its figure is
never a FILL or budget claim — following the `_compose_slice.py` precedent set at the #270 wrap.
⛔ **A declaration, not a ruling.**

★ **The general form is the thing worth keeping: a lane that adds a counter adds a gate
obligation, and the gate finds out at the wrap.** The registry exists because the last
unregistered measurer went twenty-seven sessions unnoticed; it caught this one inside a day,
which is the registry earning its place.

## 10. What is resolved, and what is still open

**Resolved, with receipts:**

- the wordmark distortion — regenerated, verified 16/16, **accepted**: *"2. accept"*
  (`b99d092c`, `ff354475`);
- the showroom's 108 stale pages — re-synced on his *"1. go"* (`ff354475`), one line per page,
  `:is(` → `:where(`, verified by **decoding all 108** rather than sampling; and the `138 v 108`
  puzzle is **explained, not inherited**: 138 = 137 generator-owned + `index.html`, so
  108 ⊂ 137 ⊂ 138;
- the seam's standing-constraints tail, built and verified;
- `ds-021 (C)` on `_seam.py`, registered.

**Still open, and every one of them is his:**

1. the **wording of the eight lines** in `knowledge/_standing.md` (DRAFT, row `W-285sc`);
2. **how** the accepted masters get registered in `_logo_nodes.json`, behind the
   `gen_kg_icons.py` fence (row `W-285lm`);
3. the `_gauge_tokens.py` **256,000 wording fix**, carried from #284;
4. the **delegation rule** — his own sentence, measured obeyed today, still uninscribed;
5. the **boot ceiling**, at its tenth breach, with a lever finally aimed at it;
6. whether the ritual owes a **resume contract** after a mid-ritual sub death;
7. whether `_seam.py`'s SCRATCH arm should stop deleting a lane's own `/tmp` working files;
8. everything on `_HANDOFF-130`…`-135` that today did not touch.

⛔ **Nothing above was inscribed. `knowledge/_rulings.json` counts 620 at the open and 620 at the
close**, verified at this seat by `json.load` over the `rulings` list rather than restated from a
brief.

---

*Both-way links: `_LIVE-STATE.md` § ⏱ LATEST DELTA #285 · `GOOD-MORNING.md` § ★ LATEST #285 ·
`_HANDOFF-136-the-b-is-straightened-and-the-connector-answer-comes-by-act.md` ·
`knowledge/_rulings.json` (UNCHANGED at 620) · `notes/_lanes/285/DAVE-RULINGS-2026-09-18.md` ·
`notes/_subreports/2026-09-18-285-W-wrap.md` and the six lane reports beside it ·
`notes/_lanes/285/W/WRAP-REPORT.md` (the EXIT CHECK and the `s271-D4` re-read).*
