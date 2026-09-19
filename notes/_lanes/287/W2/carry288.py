#!/usr/bin/env python3
"""#287 wrap — build `_CARRIES.md` § `## residual → #288` from § `## residual → #287`.

ONE programmatic pass, the #261…#286 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) FOUR STRIKES, each carrying its receipt (`s183-D1` strike form, `s188-D2` receipt);
  (c) TWELVE new items in front, newest first.
⛔ Nothing is dropped, re-worded, re-ordered or truncated. `s225-D2` clause (i).

⚠ ONE THING THE SESSION CLOSED IS DELIBERATELY *NOT* STRUCK, and the reason is `s271-D4`'s own
warning that a wrong strike is worse than a stale item:

  · **#287's item ① "THE CONNECTOR LEVER READS −7,031 AND THE CEILING STILL STANDS"** records
    a reading AND a ceiling, and BOTH stay true: the reading is unchanged, and 74,120 is the
    twelfth breach of the same ceiling. What changed is the reading's STANDING — n=1 direction
    → n=2 measured effect — and a strike removes the headline, not the clause. The upgrade is
    said in NEW item ⑦ instead.

⚠ ALSO NOT STRUCK, each for a stated reason:
  · **#287's ⑤ (the seam's `INSEAT` arm and the picked 10,000)** — only the `_seam.py` DRAFT
    line was touched today; `INSEAT_WARN_TK` and the block's placement are untouched and his.
  · **#287's ⑨ (the cloud memory archive at 48,990 of 49,152 B)** — the cap did not move and
    what to do about it is still his.
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
CARRIES = os.path.join(ROOT, "_CARRIES.md")
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg  # the ONE definition of "a carry"

text = open(CARRIES, encoding="utf-8").read()
src = [l for l in text.split("\n") if l.startswith("> **residual → #287:**")]
assert len(src) == 1, len(src)
src = src[0]
before = len(cg._carry_items(src))

# ---- (a) ages -------------------------------------------------------------------------------
n_new = len(re.findall(r"\[NEW — 0(?=[,\]])", src))
aged = re.sub(r"\[(\d+)(?=[,\]])", lambda m: "[%d" % (int(m.group(1)) + 1), src)
aged = re.sub(r"\[NEW — 0(?=[,\]])", "[1", aged)
assert "[NEW — 0" not in aged

# ---- (b) FOUR strikes, each with its receipt --------------------------------------------------
STRIKES = [
 ("⬛ **② DAVE SPOKE TWICE AND NEITHER SENTENCE IS INSCRIBED — WHETHER THEY BECOME RULINGS IS "
  "HIS** [1, DAVE'S]",
  "⬛ ~~**② DAVE SPOKE TWICE AND NEITHER SENTENCE IS INSCRIBED — WHETHER THEY BECOME RULINGS IS "
  "HIS**~~ ⛔ **STRUCK AT THE #287 WRAP — BOTH SENTENCES ARE NOW RULINGS, AND THE STRIKE NAMES "
  "ITS RECEIPT (`s183-D1` strike form, `s188-D2` receipt).** His answer to the item as put was "
  "one word: ***\"inscribe\"*** (2026-09-19, `notes/_lanes/287/DAVE-RULINGS-2026-09-19.md`). Lane "
  "I inscribed both through the sanctioned writer `knowledge/_inscribe_ruling.py`, `--dry-run` "
  "then `--write`, **reconstruction proof PASSED on each with all other bytes identical** — no "
  "hand-edit was needed and none was made. **`knowledge/_rulings.json` 620 → 622**, verified at "
  "the #287 wrap seat by `json.load` over the `rulings` list: `s287-D1` and `s287-D2` both "
  "present, no duplicate. ★ **AND THE JOIN IS NAMED ON THE FACE OF `s287-D1` RATHER THAN "
  "SMOOTHED: reading #286's *\"okay go on everything\"* as ratification-AS-WRITTEN was the "
  "CONDUCTOR'S reading at #286, and the word that makes it HIS is *\"inscribe\"*, said on "
  "2026-09-19.** `notes/_RULINGS.html` was re-rendered in the same change (622 rulings, 160 "
  "sessions, `--check` FRESH). Receipts: `notes/_subreports/2026-09-19-287-I-rulings-inscribed.md` "
  "· commit `75a490cd`. The original item follows unedited. [1, DAVE'S]"),

 ("⬛ **③ THE MASTERS' FIELD KEY IS THE LANE'S SPELLING, NOT HIS — AND THE EXPLORER CANNOT SEE "
  "IT** [1, DAVE'S]",
  "⬛ ~~**③ THE MASTERS' FIELD KEY IS THE LANE'S SPELLING, NOT HIS — AND THE EXPLORER CANNOT SEE "
  "IT**~~ ⛔ **STRUCK AT THE #287 WRAP — BOTH HALVES ARE CLOSED, AND THE STRIKE NAMES ITS RECEIPT "
  "(`s183-D1` / `s188-D2`).** His words: ***\"keep `sizes` and rebuild.\"*** ⇒ **the key name is "
  "now HIS word** (it was lane R2's reading of the file's own plural vocabulary until this line) "
  "and it is inscribed in `s287-D2`; **and the explorer was rebuilt**, so something finally reads "
  "the field. Lane K put three new reads into `knowledge/_kg_explorer.template.html` — the aside "
  "row, INSPECT's RECORD listing each height as a link to its own master with geometry and "
  "digest, and a MASTERS tab drawing all five at their true heights — builder `VERSION 1.26 → "
  "1.27`. ✅ **Verified by PARSING the built page rather than eyeballing it: all 8 `logo:` nodes "
  "carry `sizes` with 5 keys, 40 entries byte-identical to `knowledge/_logo_nodes.json`, 8 nodes "
  "and 33 edges either side, and `_logo_nodes.json` was never written by that lane.** ⚠ **2,256 "
  "baked coordinates moved and 11 nodes appeared, and none of it is the field's** — the "
  "Constitution grew under the build's feet, declared in the lane's report and the builder's own "
  "version note. Receipts: "
  "`notes/_subreports/2026-09-19-287-K-explorer-shows-sizes.md` · `s287-D2` · `75a490cd`. The "
  "original item follows unedited. [1, DAVE'S]"),

 ("⬛ **④ THE 256,000 WORDING IS FIXED IN THE GAUGE AND 58 PROSE LOCATIONS ARE STILL OWED** "
  "[1, DAVE'S]",
  "⬛ ~~**④ THE 256,000 WORDING IS FIXED IN THE GAUGE AND 58 PROSE LOCATIONS ARE STILL OWED**~~ "
  "⛔ **STRUCK AT THE #287 WRAP — THE 58 ARE SWEPT ON HIS OWN WORD, AND THE STRIKE NAMES ITS "
  "RECEIPT (`s183-D1` / `s188-D2`).** He said ***\"do it\"*** to an opener that named exactly the "
  "58 locations, ratified runbook text and the `ruled` text of standing rulings included — which "
  "#286 said was his word alone. This is that word. Lane W re-ran lane G's own probe before and "
  "after: **58 → 42, and ZERO of the 42 assert that 256,000 is a wall.** The 42 are accounted for "
  "in five named classes — **16** are the correction's own words (matching by construction), "
  "**11** are Dave's inscribed ruling text ANNOTATED not rewritten, **2** name the live constant "
  "`BUDGET_HARD`, **3** are #286's record of the owed work now carrying an appended `⇒ ✅ SWEPT "
  "AT #287`, and **1** is a false positive on the retired `HARD_STOP` percentage constant, "
  "deliberately left alone. ⛔ **NO NUMBER MOVED** — `BUDGET_HARD` is still `256_000` and "
  "`STOP_LINE_TK` still `180_000`. ⛔ **Dave's `says` fields were NOT touched** (`gauge-band`, "
  "`s161-D1`, `s214-D2`, `s214-D4` stand exactly as inscribed), because `_inscribe_ruling.py` "
  "offers no `ruled` path and says so itself; the six annotations are appended clauses applied as "
  "byte-level span swaps carrying the inscriber's own proof discipline. ⚠ **ONE PIECE IS "
  "EXPRESSLY NOT DISCHARGED AND IS RE-MINTED AS A NEW ITEM: `knowledge/_seam.py`'s four printed "
  "\"HARD LINE BREACHED\" strings**, outside the ten-file prose list. Receipts: "
  "`notes/_subreports/2026-09-19-287-W-wall-wording-swept.md` · `75a490cd`. The original item "
  "follows unedited. [1, DAVE'S]"),

 ("⚠ **⑥ `knowledge/_seam.py` STILL CALLS `_standing.md` A DRAFT AT EVERY SEAM, AND THE LINE "
  "NUMBER IS DISPUTED** [1, DAVE'S]",
  "⚠ ~~**⑥ `knowledge/_seam.py` STILL CALLS `_standing.md` A DRAFT AT EVERY SEAM, AND THE LINE "
  "NUMBER IS DISPUTED**~~ ⛔ **STRUCK AT THE #287 WRAP — THE CLAIM IS AMENDED AND THE LINE NUMBER "
  "IS SETTLED, AND THE STRIKE NAMES ITS RECEIPT (`s183-D1` / `s188-D2`).** `s287-D1` made the "
  "ratification his, which is what licensed the edit. Lane I amended **only the first clause** "
  "and **the second half survives verbatim** — *\"the seam re-quotes, it never inscribes\"* — "
  "because that half was always true and a wording fix that deletes a true sentence is a "
  "different act. ⛔ **THE LINE NUMBER IS `:44`, NOT `:26`** — the #286 wrap brief said `:26`, "
  "`_HANDOFF-137`'s own second reading said `:44`, and lane I measured `:44` at its seat; **both "
  "readings were published at #286 and neither was rewritten, and the measurement is what "
  "settled it.** `_standing.md`'s header now cites `s287-D1` and *\"inscribe\"* while **keeping** "
  "the record that #286's reading was the conductor's. `python3 -m py_compile knowledge/_seam.py` "
  "passes. Receipts: `notes/_subreports/2026-09-19-287-I-rulings-inscribed.md` § 3 · `75a490cd`. "
  "The original item follows unedited. [1, DAVE'S]"),
]
for old, new in STRIKES:
    assert aged.count(old) == 1, f"headline did not match exactly once: {old[:70]!r}"
    aged = aged.replace(old, new)

# ---- (c) the session's TWELVE new items -------------------------------------------------------
# ⚠ ① IS LOAD-BEARING: `_gen_titles.py` derives NEXT-TITLE from the FIRST ⬛ bullet's bolded
#   clause on the banner's pointer line, and `title_generation_check()` is BLOCKING.
# ⚠ NO bare " · " inside an item (it is the carry set's own split token) and NO `[N]` bracket in
#   prose (it reads as a second age). Ages spelled in words.
NEWITEMS = [
 "⬛ **① THE STRAND MAP AND THE PATH TO FRIDAY THE 25TH** [NEW — 0, DAVE'S] — **his order at the "
 "wrap call, and it is #288's FIRST move.** Verbatim: *\"I want to return to the presentation "
 "soon, so I need to understand how the multiple strands of Apollo stand and I need a clear path "
 "to presenting something cohesive for friday the 25th\"*. ⇒ **A map of every live strand of "
 "Apollo — the designer pack and Spider, the bento canon and its template, the dashboards "
 "one-shot, the KG explorer and the rulings brain, the logo masters, and the presentation itself "
 "— each with its state and with what must land by FRIDAY 2026-09-25, six days from the ruling.** "
 "⛔ **This is a JUDGMENT beat before it is a build beat:** the conductor opens on it and one "
 "Opus lane produces the page, and per `anthropic-skills:dave-voice` a long-form deliverable is a "
 "**swiss-design-system HTML page, never a `.md`**. ⚠ **The presentation strand's own location "
 "is not established from this seat** — it is named in his sentence and must be FOUND (grep the "
 "handoffs and notes for *presentation*, *deck*, *David Rice*, *HSBC demo*) rather than assumed, "
 "which is the `#256` stray-provenance discipline applied to a strand. Receipt: "
 "`notes/_lanes/287/DAVE-RULINGS-2026-09-19.md` § at the wrap call.",

 "⬛ **② MONO'S 0 IS DOUBTED AND THE `s219-D3` GENERATION ARM IS TO BE BUILT** [NEW — 0, DAVE'S] "
 "— verbatim: *\"I'm not sure that 0 is right for mono, lets have a proper review and fix this: "
 "'The generation arm that would do that was ruled at #219 and never built.' and any other "
 "problem with this, I just need the one-shot design to not disappoint, however it is getting "
 "better all the time\"*. ⛔ **DOUBTED IS NOT OVERRULED — `s217-D2` still rules `layout/bento/"
 "gutter` 0 for mono and supercharge, and nothing in this carry changes a ruled value.** What is "
 "ordered is a **proper review**, the **BUILD of the `s219-D3` generation arm**, and *\"any other "
 "problem in that path\"* end to end. The arm's groundwork already exists and declares itself "
 "un-consumed: `knowledge/_render/_bento_edit_rails.json` carries `$groundwork_only` and has sat "
 "since #219. ⚠ **Mono's 0 must be read FROM SOURCE at the review, not from any report** — and "
 "all four themes rendered side by side for his eye is what the order implies. Receipts: "
 "`notes/_lanes/287/DAVE-RULINGS-2026-09-19.md` · "
 "`notes/_subreports/2026-09-19-287-X-spider-spacing-handoff-verified.md` §1–2.",

 "⬛ **③ THE BENTO TEMPLATE'S QUALITY IS TO BE REVIEWED, AND IT IS A SECOND REVIEW** [NEW — 0, "
 "DAVE'S] — verbatim: *\"I'm not sure about the quality of the template we need to look at this "
 "too\"*. ⛔ **The conductor's reading, marked as the conductor's: this is a SECOND lane, not a "
 "clause of the spacing review** — *\"too\"* is the word that separates them. The subject is "
 "`knowledge/snippets/Template-dashboard-bento.reference.html` and its meta, which already carry "
 "four `$awaitingDave` entries and two `$tokenGaps` unresolved since #231, plus a specificity "
 "trap the meta names in its own `antiPatterns`. ⚠ **A quality review is not a status ruling** — "
 "the status question is its own carry below.",

 "⬛ **④ THE OUTER AND INNER BENTO GUTTERS ARE TWO QUANTITIES — HIS CORRECTION OF THE LANE'S "
 "FRAMING** [NEW — 0, DAVE'S] — **the conductor framed lane X's finding as \"two ruled spacing "
 "sources disagree\" and Dave corrected the framing.** Verbatim: *\"The problem with the gutters "
 "it that they are deliberately different for the themes and the gutters are also different for "
 "the inner and outer bentos we essentially have a structural bento and embedded bentos or tile "
 "groupings\"*. ⇒ **There is NO contradiction to resolve by picking a winner: the OUTER "
 "(structural bento) gutter and the INNER (embedded bento or tile-group) gutter are two different "
 "quantities, each deliberately per-theme.** ⛔ **BOTH THE FRAMING AND THE CORRECTION STAND IN "
 "THE RULINGS FILE and the wrong one was NOT deleted** — a correction that erases what it "
 "corrects leaves no evidence the correction was needed. ⚠ **Whether `--layout-bento-gutter` "
 "(ruled 0 in mono, `s217-D2`) IS the structural gutter is still TO BE READ, not assumed** — "
 "that reading is the first beat of the review in item ②. Receipt: "
 "`notes/_lanes/287/DAVE-RULINGS-2026-09-19.md` § later in the session.",

 "⬛ **⑤ AN INLINE-STYLE RULE — PUT TO HIM AND NOT ANSWERED, AND THE ACTIONABLE NUMBER IS 88** "
 "[NEW — 0, DAVE'S] — **put to Dave at the wrap call and NOT answered, so it carries as a "
 "question and not as a state of the world** (`s271-D4`). His prompt: *\"we still seem to be "
 "writing a lot of inline styles BTW, which would be good to avoid\"*. Lane X classified the "
 "WHOLE population rather than sampling: **596 `style=\"` in `knowledge/snippets/`**, of which "
 "**62% is defensible** (data-driven bar lengths, token bindings, token-bound SVG fills) and "
 "⛔ **88 carry a raw px or rem with NO `var()`** — *\"that number, 88, is the census's "
 "actionable answer, not the 596\"*. ✅ **The showroom's 138 pages carry ZERO**, and "
 "`grep -rho 'style=\"--bento[^\"]*\"'` returns **zero hits repo-wide** against a rule stated in "
 "five places — the class that would actually hurt does not exist here. ⛔ **THERE IS NO RULING "
 "ON INLINE STYLES AT ALL across the 622** — only a generator-comment convention, obeyed "
 "everywhere and never inscribed. The cheapest move lane X names is **widening `DEF-004`'s "
 "population** (`knowledge/_validate_no_hardcode.py`, blocking, but scoped to pro-formas) from "
 "pro-formas to the snippet corpus — **a scope change, and his**. Receipt: "
 "`notes/_subreports/2026-09-19-287-X-spider-spacing-handoff-verified.md` §7.",

 "⬛ **⑥ TWO STATUSES FOR ONE TEMPLATE — PUT TO HIM AND NOT ANSWERED** [NEW — 0, DAVE'S] — **put "
 "at the wrap call and NOT answered** (`s271-D4`). `knowledge/components/template-dashboard-bento."
 "meta.json` `$status` reads **PROPOSED #231, NOT GATED, NOT RULED, NOT REGISTERED** and says "
 "*\"Dave's eye is owed\"*; **`showroom/index.json` — the one status surface the composition "
 "skill tells builders to search — reads `beta`**. ⛔ **A consumer following the skill's own "
 "instructions cannot discover that the template is unratified**, and *\"a skip is a yes\"* in "
 "that skill makes the template the SILENT DEFAULT for any dashboard request. ★ **The meta "
 "predicted this exact outcome in its own words** (*\"that is the serial's own behaviour, not a "
 "registration\"*) **and was right.** TWO decisions, not one: the template's actual status, and "
 "whether `showroom/index.json` gains a value that can say *proposed* — today the generator globs "
 "every snippet in and stamps `beta` regardless. Receipt: "
 "`notes/_subreports/2026-09-19-287-X-spider-spacing-handoff-verified.md` §5 and §8-Q5.",

 "⚠ **⑦ THE CONNECTOR LEVER IS NOW A MEASURED EFFECT AT n=2, AND THE CEILING TOOK ITS TWELFTH "
 "BREACH** [NEW — 0] — **the upgrade to the item that ages beside this one, said HERE rather than "
 "by striking that item**, because that headline records a reading and a ceiling that both stay "
 "true. **BOOT COLD 74,120 real against #286's 73,832 on the same setup — Δ +288**, two readings "
 "within 300 tokens of each other on a setup whose prior seven-reading spread was **11,526** "
 "wide. ⇒ **#286's OWN acceptance test — *\"two readings within a few hundred tokens of each "
 "other would make it measured\"* — is MET, and the −7,031 from blocking the built-in Browser's "
 "17 tools is a MEASURED EFFECT rather than a direction.** ★ **A session honouring an acceptance "
 "test written by the session that could not pass it is the shape worth keeping.** ⛔ **AND IT "
 "CHANGES NOTHING ABOUT THE CEILING: 74,120 is 4,120 over `BOOT_CEILING_TK` 70,000 — the TWELFTH "
 "post-diet reading over it, SHRINK-ONLY by `s240-D2` and `s241-D1`, and NOT a re-base.** ⚠ "
 "**The next lever is still unnamed** — boot is one undecomposed figure (`ds-025` item 1), dark "
 "from every mount, so no connector is ranked and no saving is stated. Receipt: "
 "`notes/_lanes/287/BOOT-COLD-2026-09-19.md`.",

 "⚠ **⑧ THE `subs` FIGURE AND THE FILL RULE ARE TWO DIFFERENT QUANTITIES, AND THE GAP IS 5,352** "
 "[NEW — 0] — found at the #287 wrap seat while verifying the conductor's declared lane spends, "
 "and **published rather than reconciled away**. Read with `_checkin.read_fill` — the ONE "
 "definition of FILL, input side only (`input_tokens` plus `cache_creation` plus `cache_read`) — "
 "the five lanes sum to **568,179**. The **573,531** the conductor declared, and that this log "
 "has carried since #284, is each seat's last-turn input side **plus that turn's "
 "`output_tokens`**. ⇒ **The difference is entirely the five lanes' final output, and it "
 "reconciles to the token on every one of the five.** ⛔ **Which definition the `subs` line means "
 "is ruling-shaped and is his** [[measure-dont-convert-units]]: the line's own contract says REAL "
 "Claude tokens as QUOTA, which argues for input-plus-output, while every FILL figure in the same "
 "block is `read_fill`'s input side — **two units in one stratum, and the stratum now says so.** "
 "★ **The conductor's declared FILL figures use `read_fill` and agree to the token**, so the "
 "split is confined to the `subs` line. Receipt: the #287 stratum and "
 "`notes/_subreports/2026-09-19-287-W2-wrap.md`.",

 "⚠ **⑨ A COMMIT LANE WROTE THREE OTHER LANES' STORE ROWS, AND DECLARED IT RATHER THAN LEAVING "
 "IT TO BE DISCOVERED** [NEW — 0] — `_gate_doc_rows.py` refuses a commit that stages a sub-report "
 "with no `knowledge/_state.json` row (`s218-D7`), and at lane C's open only lane K had one. Lane "
 "C wrote **`W-287i`, `W-287w` and `W-287c`** through `_state.py`'s module API — **never by "
 "hand-editing the store** — taking each `closes_when` from that lane's own filed verdict and "
 "re-wording nothing; the alternative was `DOC_ROW_ACK`, which in its own words *\"would have "
 "shipped three invisible documents to pass a gate\"*. ⛔ **A close-condition the conductor wants "
 "changed is HIS TO CORRECT, not to discover**, which is the whole reason the judgment is named. "
 "⚠ **And a related close is left open on purpose:** `W-286rb`'s `closes_when` asks for Dave to "
 "accept `sizes` as the field name and today he said *\"keep `sizes`\"* — **half the condition is "
 "met by his own word, and closing lane R2's row is the conductor's call, not a lane's.** "
 "Receipts: `notes/_subreports/2026-09-19-287-C-commit-and-push.md` §4 · "
 "`notes/_subreports/2026-09-19-287-K-explorer-shows-sizes.md` §5.",

 "⚠ **⑩ THE DASHBOARD WAS ALREADY 11,617 LINES STALE AGAINST ITS OWN SOURCE, AND IS NOW FRESH** "
 "[NEW — 0] — `dashboard/index.html` carries a **9,590-line diff** in this session's commit and "
 "**most of it is inherited**, measured rather than assumed: a regeneration from the **UNCHANGED "
 "`HEAD` `knowledge/_state.json`** alone moves **11,617 lines**, and lane W's seven row edits "
 "account for about **1,262** of the delta, most of that `gen_dashboard.py`'s own re-ranking "
 "cascade (it scores rows by prose scan and body length, so lengthening a `body` reorders the "
 "list). ⇒ **The committed dashboard had been stale against its own generator's input for "
 "several sessions and nothing reported it.** ✅ **It is FRESH now, and the fact is on the face of "
 "the commit message rather than buried.** ⛔ **RULING-SHAPED AND NOT INSCRIBED: nothing checks "
 "this file's freshness against its source** — there is no `--check` arm on `gen_dashboard.py` "
 "the way `_gen_chain.py` and `_render_rulings.py` have one, so the staleness was invisible until "
 "a lane happened to regenerate. Receipts: "
 "`notes/_subreports/2026-09-19-287-W-wall-wording-swept.md` §6 · "
 "`notes/_subreports/2026-09-19-287-C-commit-and-push.md` §2.",

 "⚠ **⑪ A 4.3 MB BEFORE-COPY SITS IN `_to_delete/287-K-before/` BECAUSE THE SANDBOX REFUSES "
 "`unlink`** [NEW — 0] — lane K wrote a **4,361,115-byte** plain copy of the pre-rebuild explorer "
 "as its evidence and could not delete it (`Operation not permitted` on `unlink` under the "
 "mounted repo, the #284 finding still standing). Lane C used the **#284/#286 `mv` precedent** — "
 "the same move it took with the 898 symlinks at #286 — so the copy left `notes/_lanes/287/K/` "
 "for a gitignored directory; **`.gitignore` was NOT edited and no path was excluded from "
 "staging.** ✅ **The 807 KB `.gz` IS committed**, which is the evidence in the form that was "
 "meant to be kept. ⛔ **`_to_delete/` IS AN ACCUMULATING SQUATTER ON A PERSISTENT DISK, and "
 "nothing empties it** — `4c` cleans `/var/tmp` and `~`, not a gitignored directory inside the "
 "repo; **what to do about it is his.** Receipt: "
 "`notes/_subreports/2026-09-19-287-C-commit-and-push.md` §3.",

 "⚠ **⑫ A GPT-6 HANDOFF FROM APOLLO SPIDER v1.0.13 WAS BROUGHT IN AND TESTED CLAIM BY CLAIM — 5 "
 "OF 6 VERIFIED, 1 PARTLY** [NEW — 0] — Dave brought it from his work machine with the posture "
 "stated in his own words: ***\"don't take it on face value, use your judgment, but what it did "
 "worked\"***. ✅ **The document is SAVED INTO THE REPO at "
 "`notes/_lanes/287/GPT-SPIDER-SPACING-HANDOFF-2026-09-18.md`** — ritual step 1's cited-uploads "
 "clause, because a chat-only attachment is an un-retrievable citation. Lane X tested only its "
 "**factual claims about our system**, at file:line, read-only, with no gate and no generator "
 "run. **VERIFIED: the template's 40/4 pin, `--layout-bento-gutter` resolving to 0, supercharge's "
 "unbound 2px, the four-column lead rule's receipt comment, the PROPOSED-versus-directed status.** "
 "**PARTLY: the 33 pass / 8 FAIL split** — the arithmetic is exact against v1.0.13's 41 RUNNABLE "
 "gates, but the attribution is roughly **3 screen-caused, 4 pack-baseline, 1 placement-dependent** "
 "and the agent **ran no `--baseline`**, so it could not separate its own failures from inherited "
 "debt. ⚠ **Its three findings we do NOT owe work on are named too:** *\"three passes examined "
 "zero subjects\"* is our runner's designed warning and the WP4 criterion is already met. ⛔ "
 "**Three of its five §9 decisions are ALREADY RULED and need implementing rather than deciding**; "
 "the two genuinely open are the `composes` schema edge (`meta.schema.json` has no seat for it, "
 "and a schema change is his) and the template status in item ⑥. ⚠ **Every RUNTIME claim is "
 "UNTESTED from this tree** — no browser in the lane, and the test-bed artefacts are on his work "
 "machine. Receipt: "
 "`notes/_subreports/2026-09-19-287-X-spider-spacing-handoff-verified.md`.",
]

body = aged[len("> **residual → #287:** "):]
newline = "> **residual → #288:** " + " · ".join(NEWITEMS) + " · " + body
after = len(cg._carry_items(newline))
print("carries: before %d (of which %d were [NEW — 0]) → after %d ; new items %d ; strikes %d"
      % (before, n_new, after, len(NEWITEMS), len(STRIKES)))

SECTION = "## residual → #288"
assert SECTION not in text, "section already exists"
anchor = "## residual → #287"
i = text.index(anchor)
if "--write" not in sys.argv:
    print("DRY — nothing written")
    sys.exit(0)
text = text[:i] + SECTION + "\n\n" + newline + "\n\n" + text[i:]
open(CARRIES, "w", encoding="utf-8").write(text)
print("WROTE", CARRIES)
