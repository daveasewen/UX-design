# #240 — the derived band, the roster diet, and the receipt that made V2 legal

```
provenance: 240 · 2026-09-02
status: observed
```

*Both-way links: spine entry `_LIVE-STATE.md` § ⏱ LATEST DELTA #240 · record `GOOD-MORNING.md` § ★ LATEST
#240 · ledger `knowledge/_rulings.json` § `s240-D1` · `s240-D2` · `s240-D3` · carries `_CARRIES.md`
§ `## residual → #241` · brief `notes/_briefs/2026-09-02-240-delegated-wrap-brief.md` (`W-385`).*

⚠ **Scope of this dossier, stated first so nothing in it is read as more than it is.** It was written at
the WRAP SUB'S seat from the conductor's brief, the repo, and the three ruling records. Dave's words are
**chat testimony relayed by the brief and quoted inside each ruling's `says` field** — they are not
repo-verifiable and are attributed, never asserted. The roster diet happened outside git entirely.

---

## 1. The shape: a session that could not afford its own work

#240 opened on the question #239's wrap put first — the boot band — and it ran for one morning with a
FABLE conductor and **no lane at all**.

That is the finding, not an apology. The window read **FILL 135,020 real @ 21 turns** after the opener
and the memory compaction. The standing measurement in `knowledge/_RUNBOOK-context-gauge.md`
§ MEASURED, NOT RULED prices a lane at **≈19K of conductor FILL all-in** (n=5, #238), and the advisory
stop line is **150,929**. 135,020 + 19,000 lands past it before the lane has returned anything. So the
conductor ruled the questions and **carried every build**, which is why the #240 record is three
inscriptions and a diet rather than a lane report.

★ **The lesson generalises, and it is why the n=5 figure was worth writing down:** a delegation decision
became arithmetic instead of instinct. That is added to the runbook at this wrap as the #240 datapoint,
beside #239's route price.

## 2. The boot band: Dave asked for the figure before he ruled

The #239 wrap filed his mid-turn paste verbatim-in-substance — *"derive the band, shrink-only ceiling,
shrink first"* — as `notes/_briefs/2026-09-02-240-boot-band-derive-brief.md`. At #240 it was answered in
two rulings, and the ORDER of the exchange is the part a ledger line cannot carry.

**He did not accept the mechanism on description.** His reply was *"I'd be interested in the figure
before committing"* — so the derived band was computed and shown first: **75,672 ± 641** over the last
seven first-turn `message.usage` readings (#234–#240). Only then: *"okay do it, lets get this off our
plate."*

⇒ **`s240-D1` — the band is DERIVED, never typed.** The drift gate computes mean ± measured spread from
the last **n=7** readings in `notes/_GAUGE-LOG.md` at check time. A step change beyond the spread goes
red; slow drift never needs a re-base, because there is no constant to re-base.
`BOOT_FIRSTTURN_TK`/`_ERR` cease to be the comparison. ⚠ **n=7 is the PROPOSED window, not a constant he
chose** — that distinction is inside the ruling's own text and must survive into the build.

**The second half was a correction, not an extension.** A ceiling of **77,000** was floated and he
refused it in his own units: *"that seems high we were comfortably riding on around 56k before, 77k
seems a lot."* The re-frame that survived is the type-composites ratchet applied to boot:

⇒ **`s240-D2` — ONE typed ceiling stays beside the derived band, SHRINK-ONLY, and its value is the FIRST
POST-DIET BOOT.** Read at #241's opener. ⛔ **No number was chosen at #240**, and anyone who types one
before that reading has invented Dave's number.

**The dead end worth recording:** the instinct at this point is to move `BOOT_FIRSTTURN_TK` — the
constant is nineteen thousand tokens away from the last six measured boots and the drift line says so
every wrap. That would have been the `s208-D1` re-base, and it is exactly what both rulings make
unnecessary: the answer was to retire the COMPARISON, not to correct the number. Nothing in code moved
at #240, and the drift line will keep declaring **+19,307** against **56,749 ± 1,154** until `W-386`
lands. **A ruling that reads as enacted is the pitfall this dossier exists to flag.**

## 3. The roster diet: "Disabled" did not work, removal did

`s228-D6` says shrink first. The half nobody had tested was whether *turning a connector off* removes
its cost.

It does not. Dave **REMOVED** the Figma connector outright — its MCP disconnected mid-session and its
tools went with it — and switched **computer use OFF**. `MEMORY.md` was compacted **21,064 → 12,454
bytes** (**6,104 → 3,509 cl100k**), with the pre-compaction index kept VERBATIM at memory
`hook-overflow-2026-09-02-240.md` so nothing was deleted, only moved.

⚠ **(NON-REPO: Cowork auto-memory.)** None of this is in git, none of it is visible to any gate, and the
wrap sub neither wrote nor read it back. The figures are the conductor's, attributed.

## 4. The claim that is NOT a measurement, and why it is written as a claim

There is a staircase in `notes/_GAUGE-LOG.md`:

> **57.7K #211 → 63K #212 → 67K #218 → 70K #220 → 75K #222 → 79K #224 → ~76K since**

`MEMORY.md` accounts for **≈8.5K** of the first-turn figure, and that share is MEASURED (#233). The rest
was **read off the conductor's own boot** and attributed to the connector roster, Cowork's base prompt,
the Artifact tool and three control stacks.

⛔ **That attribution is a CLAIM.** It is plausible, it is the reason the diet happened, and it has no
receipt. The decomposition of boot into sub-parts is precisely what `ds-025` item 1 says stays dark.
**#241's first turn is the measurement** — one reading, post-diet, against the same instrument. Until it
exists, the diet's effect is a prediction and the record says so in every home it appears in.

★ The general form: *a good reason to act is not evidence that the action worked.* The diet was right to
do on his judgment; claiming its size before measuring it would have been the #109 defect in a new coat.

## 5. The polarity receipt: the answer was a question about growth

Lane F (#239) closed 44 of 48 escapes by class and then reported something it could not fix: **all 30
frozen R1 rows are claimed by exactly one node, so there is no legal form for a NEW or a RETIRED
polarity.** Six of verifier V's seven green controls read FALSE-RED as a consequence, and a V2 launched
into that state would have re-reported them as regressions.

The proposal was a per-node receipt. Dave's first response was not yes or no but a scaling question —
*"wont this just bloat over time as we grow that KG, maybe explain this for me in simpler terms"* — and
the explanation that satisfied him is the shape of the answer: **one pointer per node**, so the KG grows
only as fast as he rules. Then: *"okay do it, lets get this off our plate."*

⇒ **`s240-D3`** — a polarity's receipt may point at an R1 row **OR** at a `knowledge/_rulings.json` id.
A node born after R1 carries a **`$seed`** receipt naming the ruling that created it. A retired node
**keeps its row**, carries **`retiredBy`** naming the ruling that retired it, and **drops out of
everything GENERATED from the KG**. The quote rule is untouched: every polarity still traces to
something Dave ruled — only the anchor widens.

**Consequence, stated because it is the point:** the six FALSE-RED controls become legal under this form,
and **V2 may run** — but only after the build lands. `W-374` still closes at ESCAPED 0 and stands at 4.

## 6. And the small one: why thirty rows

Asked and answered in chat: **30 is what the #236 R1 principles survey FOUND**
(`notes/_subreports/assets/2026-09-02-236-R1-principles-survey/tensions.json`). It is a count of the
material, not a limit anyone chose. Recorded here because "why is it thirty" is the kind of question
that gets re-asked every few sessions when the answer lives only in a chat.

## 7. Where it stands, and what is still open

**Resolved.** Three rulings inscribed via `_inscribe_ruling.py` at the conductor's seat, store **328 →
331**, reconstruction proof PASSED ×3, every id read back from the file at the wrap. The roster is cut.

**Open, and carried at age 0 in `_CARRIES.md` § `## residual → #241`:**

1. **The boot-band BUILD** (`W-386`) — `s240-D1` + `s240-D2` are ruled, not built. The ceiling's VALUE is
   read at #241's opener and is Dave's.
2. **The polarity-receipt BUILD** (`W-387`) — schema + validator, a two-file commit with the
   `SCHEMA_SHA256` pin. **V2 is gated on it.**
3. **Two `s203-D1` CI read-backs** — `4fb75f6` and this wrap's push, route capped at the run page plus
   one JS grep.
4. **The boot attribution** — a claim until #241's first turn measures it.
5. **The `--plant` runbook line** — `--session N` required, output never piped; #240's probe was planted
   and never quizzed, and its file carries no verdict.

⛔ **Nothing above was enacted at #240.** `BOOT_FIRSTTURN_TK` is byte-untouched, no schema line was
written, no `W-` row was closed, and the four UNRULED escapes are exactly where lane F left them.
