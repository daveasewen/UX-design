# #273 — the address and the registry

provenance: 273 · 2026-09-15
status: observed

*Spine entry: `_LIVE-STATE.md` § ⏱ LATEST DELTA — 2026-09-15 (#273). Ledger: `knowledge/_rulings.json`
§ `s273-D1`…`s273-D4` (and `s272-D93`, enacted here). Handoff:
`_HANDOFF-124-the-address-and-the-registry.md`. His words, verbatim and in order:
`notes/_lanes/273/DAVE-RULINGS-2026-09-15.md`. Lane reports:
`notes/_lanes/273/roles-drift/REPORT.md` · `notes/_lanes/273/list-vs-card/REPORT.md` ·
`notes/_lanes/273/when-registry/REPORT.md`.*

---

## The arc in one sentence

A drift that two previous sessions had measured and deliberately declined to fix got fixed; the one
decision Dave refused to make on the spot turned out to be the session's most durable ruling; and
underneath both sat a red that existed only because a green gate had been quoted in another gate's
place.

---

## 1. The opener: a posture became an arm, in two words

`s272-D93` had been inscribed at #272 as three figures — 180,000 working, ~220,000 tolerated,
256,000 hard — and **no code had moved**. That was deliberate: the #272 wrap said so in its own
banner, because turning a tolerance into a gate arm on an inference is a behavioural change a
session may not make.

Dave's answer was two words: *"1. advisory arm"*.

`4294b60` wired exactly that and nothing more. `gauge.TOLERATED_TK = 220_000`; `STOP_LINE_TK` stayed
`180_000`; the walls were untouched; `_checkin.py`'s budget line learned to say **TOLERATED** between
the two figures and **PAST TOLERANCE** above. It was driven at 170K / 195K / 220K / 230K with an 8/8
selftest block, because an arm that is never driven is an assertion.

**Why it matters beyond the number:** this session then ran past 180,000 and closed at 196,588 — so
#273 is the first session in the project's history to be graded by an arm it enacted that same
morning. The reading is TOLERATED rather than a breach, and it says so because he said so, not
because a wrap decided to be generous with itself.

## 2. The park that cost nothing

*"i cant get access to the common library specs right now, we'll have to park it."*

The HSBC Common Toolkit ingestion has been carried as an open item since #270 and blocks `P-270-1`
(the dropdown cut-off of 5, ruled from his memory and provisional until Figma confirms it). It went
into `knowledge/_parked.json` as **`P-273-1`**, tripwire on a `knowledge/guidelines` commit.

The small lesson: a blocked item with a tripwire is cheaper than a blocked item on a carry list,
because the register fires on the event that unblocks it. The carry still ages; the tripwire is what
actually notices.

## 3. The roles drift: three answers in one click, and one refusal

`knowledge/_roles_drift.py` (selftest 12/12) measured what #270 and #271 had both reported without
fixing: **108 role memberships in `roles.json`, 24 component metas carrying `provides`, 84 silent,
4 roles with no provider at all.** `notes/_REVIEW-roles-drift-2026-09-15-v1.html` put four questions
to Dave, and his export came back **RD-1 a · RD-2 a · RD-4 a · RD-3 null**.

Three of those became `s273-D1`…`s273-D3`. `s273-D1` — the address — was enacted at `0d98a34` by
`knowledge/_enact_s273_d1_address.py`: `provides: <role>` written onto **84 metas by textual span,
reconstruction-proven per file**. The drift instrument then read **108/108 agree, 0 silent, 0 roles
at zero**, and `gen_kg_roles_desk.py --land --ratified s270-D2` took `providesRole` from **24 to 108**
across **207 edges / 85 metas**.

**The dead-end worth recording:** the same regen rewrote `Chart-boxplot`'s `yieldsTo` `$note` and
**dropped a hand-added `span.cols` sentence**. The field is generator-owned, so the sentence was
always living somewhere a generator would eventually overwrite. It is declared rather than quietly
restored, because the right repair — if the sentence mattered — is to put it on the meta, and that
is not a wrap's call.

## 4. RD-3: the refusal that produced the best ruling

RD-3 asked whether the `when` field-name list should be closed. He declined to answer it and said
why:

> *"I need to understand the implications of this, maybe closing the list was a bad idea, I have a
> feeling this will reoccur, lets explore"*

The conductor did not re-ask. It explored three fence shapes and brought them back, and his answer
to those was:

> *"1. is thsi a candidate for an N-gram? probably over engineering"*

⇒ **`s273-D4`: the list is a REGISTRY, not a whitelist.** `knowledge/when-fields.json` stays the one
home; the resolver still refuses a name it has never seen; but a lane **may add** a name, provided it
arrives with a definition and an example and is listed in that lane's report. And the n-gram question
answered itself: **no new instrument was built.** The existing advisory `_near_dupes.py` gets pointed
at the registry's definitions at verify time, which is the whole of the mechanism.

**The shape of the lesson:** a question that comes back `null` with a sentence attached is not a
deferral — it is a redirection. The sentence named the real worry (*"this will reoccur"*) and the
ruling answers that worry rather than the question as originally posed. Re-asking the original
question would have got a worse answer.

`5f0c97f` then defined the **13 names by textual span** and amended `$description` **by addition**,
taking the resolver from **FAIL(20) to FAIL(6)**.

## 5. The red underneath: a green gate quoted in another gate's place

`_validate_roles_resolve.py` went **FAIL(6) → FAIL(20) at `b46ea90`** — #272's fifteen inscribed
`when` predicates had used **13 field names that existed in no registry**, spread over 9 metas.

The reason nobody saw it is the part worth keeping: **`_validate_kg.py OK` had been reported, and
the resolver was never run.** Two gates, one of which says nothing about the other's subject. The
class is already inscribed — [[no-gate-parses-the-artefact]] — and this is its cleanest instance yet,
because the false comfort was not a bug in any gate; it was a substitution made while writing a
receipt.

The remaining **FAIL(6)** is #261's `data-grid` `with`-slug reds, inherited and not new.

## 6. LIST vs CARD: the line nobody draws

*"If the list vs card blocks anything lets do that too"* — and it did block, because `record-list`'s
gates are inside `s273-D2`'s pass-two scope. `s273-D3` pulled `P-272-1` forward and the lane ran in
parallel (`783a8d9`, `notes/_PROPOSAL-list-vs-card-2026-09-15-v1.html`).

The finding is a negative one and it is the useful kind: across **13 external design systems, none
draws the list/card boundary on how many fields a row carries.** The predicates that are actually
load-bearing are **surface**, **record-level actions**, and **same-shape set**. GOV.UK's summary card
is the one genuine list-card precedent in the sample.

The lane also **corrected the brief it was given**: `cards` does provide `arrangement`, and only
`account-card` is `$not-a-provider`. A lane that corrects its own premise is worth more than a lane
that agrees with it.

**LC-1…LC-4 are on the page and not one is ruled.** LC-1 (option a) would need exactly one new field,
`actions`.

---

## Resolved state

- `s272-D93` **enacted** as an advisory arm; constants untouched (`4294b60`).
- `s273-D1` **enacted**: 84 metas addressed, drift 108/108, `providesRole` 24 → 108 (`0d98a34`).
- `s273-D3` **enacted** as research: the list-vs-card proposal page exists (`783a8d9`).
- `s273-D4` **enacted**: 13 registry names defined, resolver FAIL(20) → FAIL(6) (`5f0c97f`).
- `P-273-1` parked with a tripwire on `knowledge/guidelines`.

## Still open, and his

LC-1…LC-4 · the `example` key on the 13 new registry entries (26 legacy entries lack it) · the four
near-dupe pairs (`records`/`rows` · `entry`/`content` · `exits`/`destinations` · `steps`/`parts`) ·
the 6 `data-grid` `with`-slug reds · the `input` sub-roles (27 providers, `$extension`) ·
`P-272-2`…`P-272-4` · `s273-D2`'s authoring pass two (49 silent providers, 8 roles, one Opus lane per
role) · and his mid-turn ask, *"Id really like to get this nailed then go back to the presentation:
_PROPOSAL-kg-entity-and-edge-gaps-2026-09-14-v1.html"*, whose zero-counts are now stale for roles at
minimum and must be **regenerated from the graph, never hand-corrected**.
