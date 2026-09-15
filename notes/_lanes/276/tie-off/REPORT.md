# Lane TO — tie off the loose ends: 17 WCAG criteria + the authored pass on six components (#276, P-274-2 + P-274-3/s275-D5)

READ-ONLY on the corpus. **Nothing landed.** `knowledge/compliance/rules/` still holds 38 rules,
`knowledge/components/` still holds 138 metas with 0 `obeys` blocks between them, `_rule_nodes.json`
still carries 19 `cites` nulls, `meta.schema.json` is untouched, `_rulings.json` is untouched. The one
file this lane wrote inside `knowledge/` is `_validate_lane_ownership.py` — Dave's "1. fix", and it is
inert (exit 0, prints, blocks nothing).

Deliverables: `_build_rules.py` · `proposed-rules/` (17) · `dry-run.json` · `_author_metas.py` ·
`proposed-metas/` (6) · `meta.schema.diff` · `_mutate.py` (18 mutants) · `_build_page.py` ·
`tie-off-decisions-2026-09-15.json` · `REVIEW-tie-off-2026-09-15-v1.html` · `_drive_page.py` ·
`screenshot.png` · `knowledge/_validate_lane_ownership.py` · this report.

---

## 1. The headline figures

| | measured |
|---|---|
| criteria proposed | **17** (`proposed-rules/`, schema-valid, 0 failures) |
| W3C fetches | **17 OK / 0 failed** — every `title` and `level` off the page, none from memory |
| `cites` nulls today | **19** across **17** distinct criteria |
| nulls that would resolve with the 17 present | **19 → 0** |
| `sc:` nodes in the corpus | **38 → 55** |
| severities proposed | 12 serious · 5 minor · **0 critical** |
| levels as W3C states them | **9 A · 5 AA · 3 AAA** |
| check types proposed | 11 manual · 6 semi-automated · 0 automated |
| metas authored | **6** (four named in the brief + 2 extensions) |
| authored citations | **67** — 55 `rule:` + 12 `ux:` — every one with a sentence |
| extras flagged | **3 obvious** (chart-line, chart-pie, chart-bar) + a named weak tier |

**The one thing the brief got wrong, and it matters for D-2: there are THREE AAA criteria in the 17,
not one.** The brief named 2.4.13 Focus Appearance. Measured off the W3C pages, **1.4.8 Visual
Presentation** and **3.1.4 Abbreviations** are Level AAA too. All three are graded `minor` here,
following the corpus's own pattern (2.3.3 and 2.4.8 are its existing AAA rules and both are minor), and
whether an AA-minimum corpus may hold them at all is D-2 — now a three-way question, not a one-way one.

---

## 2. PART A — the 17 criteria, and the fetch receipts

Every page fetched 2026-09-15 with the web fetch tool, `https://www.w3.org/WAI/WCAG22/Understanding/<slug>.html`,
all **HTTP 200** (the tool returns the rendered page; a non-200 surfaces as a refusal, and none did).
`title` and `level` were read off the `# Understanding [SC n.n.n]<Title> (Level X)` heading of each page.

| SC | slug fetched | status | title (W3C) | level (W3C) | severity (ours) | check (ours) |
|---|---|---|---|---|---|---|
| 1.2.3 | audio-description-or-media-alternative-prerecorded | 200 | Audio Description or Media Alternative (Prerecorded) | A | serious | manual |
| 1.2.4 | captions-live | 200 | Captions (Live) | AA | serious | manual |
| 1.3.3 | sensory-characteristics | 200 | Sensory Characteristics | A | serious | manual |
| 1.4.2 | audio-control | 200 | Audio Control | A | serious | semi-automated |
| 1.4.5 | images-of-text | 200 | Images of Text | AA | serious | manual |
| 1.4.8 | visual-presentation | 200 | Visual Presentation | **AAA** | minor | manual |
| 2.4.13 | focus-appearance | 200 | Focus Appearance | **AAA** | minor | semi-automated |
| 2.5.1 | pointer-gestures | 200 | Pointer Gestures | A | serious | manual |
| 2.5.2 | pointer-cancellation | 200 | Pointer Cancellation | A | serious | manual |
| 2.5.3 | label-in-name | 200 | Label in Name | A | serious | semi-automated |
| 3.1.1 | language-of-page | 200 | Language of Page | A | serious | semi-automated |
| 3.1.2 | language-of-parts | 200 | Language of Parts | AA | minor | semi-automated |
| 3.1.4 | abbreviations | 200 | Abbreviations | **AAA** | minor | manual |
| 3.2.2 | on-input | 200 | On Input | A | serious | manual |
| 3.2.4 | consistent-identification | 200 | Consistent Identification | AA | serious | manual |
| 3.3.7 | redundant-entry | 200 | Redundant Entry | A | minor | manual |
| 3.3.8 | accessible-authentication-minimum | 200 | Accessible Authentication (Minimum) | AA | serious | manual |

**0 fetches failed. 0 rules marked UNFETCHED.**

Shape notes, each measured against the corpus rather than asserted:

- **`applies_to` is `[]` on all 17.** It is DERIVED by `knowledge/compliance/_build_compliance_kg.py`
  from the metas' `accessibility.relatedSC`, and **0 of 138 metas names any of these 17 criteria today**
  (measured). Writing a guess in would be exactly the invented edge s274-D12 refused.
- **`external_automatable_refs` is `[]` on all 17,** for `_import_axe_rules.py` to fill from the vendored
  snapshot. Measured, applying that importer's own `tag_to_sc` rule to `axe-core-rules-snapshot.json`
  (axe-core 4.12.1): it would attach **6 refs across 4 of the 17** — 1.4.2 `no-autoplay-audio`,
  2.5.3 `label-content-name-mismatch`, 3.1.1 `html-has-lang`/`html-lang-valid`/`html-xml-lang-mismatch`,
  3.1.2 `valid-lang`. Not one was hand-typed.
- **The three WCAG 2.2 additions — 2.4.13, 3.3.7, 3.3.8 — and only those three** carry
  `"9.<sc> (pending EN 301 549 alignment to WCAG 2.2)"`, the exact clause 2.5.7 already carries.
  `wcag_versions` is `["2.2"]` for those three and nothing else.
- **`internal_policy_ref` is byte-identical to the corpus's own sentence**, read out of
  `wcag-2.5.7-dragging-movements.json` and asserted equal in a bite, never retyped.

### The dry run — 19 → 0

```
python3 notes/_lanes/276/tie-off/_build_rules.py --dry-run notes/_lanes/276/tie-off/dry-run.json
→ cites edges 51 · resolved today 32 · null today 19 · distinct SC missing 17
  sc: nodes in corpus 38 → 55
  nulls that would resolve 19 · nulls that would remain 0 · remaining_sc []
```

SIMULATION ONLY: `gen_kg_rules.py` was **not** run and `_rule_nodes.json` was not touched. The lookup
mirrors `gen_kg_rules.py:sc_ids()` — glob `knowledge/compliance/rules/*.json`, take each file's `sc` —
so it is the generator's own resolution rule re-executed, not a re-implementation of it.

Nulls by criterion (19 across 17 — 1.3.3 and 1.4.8 are each cited twice):
`1.3.3 x2 · 1.4.8 x2 · 1.2.3 · 1.2.4 · 1.4.2 · 1.4.5 · 2.4.13 · 2.5.1 · 2.5.2 · 2.5.3 · 3.1.1 · 3.1.2 ·
3.1.4 · 3.2.2 · 3.2.4 · 3.3.7 · 3.3.8`. The three AAA criteria account for **4 of the 19** — so D-2
option (b) leaves 4 permanent nulls and option (c) leaves 3.

### Severity — our grade, with the reasoning

Full sentences are in `_build_rules.py:WHY_SEVERITY` and printed in the review page's own table. The
pattern read off the corpus first: **every AAA rule in it is `minor`** (2.3.3, 2.4.8, 2.5.5);
**`critical` is three rules only** (2.1.1 Keyboard, 2.1.2 No Keyboard Trap, 4.1.2 Name/Role/Value);
`minor` otherwise goes to narrow AA rules (1.3.5, 2.4.5) and to the obsolete 4.1.1. Applying it:

- **serious (12):** 1.2.3, 1.2.4, 1.3.3, 1.4.2, 1.4.5, 2.5.1, 2.5.2, 2.5.3, 3.1.1, 3.2.2, 3.2.4, 3.3.8
- **minor (5):** 1.4.8 (AAA), 2.4.13 (AAA), 3.1.4 (AAA), 3.1.2 (narrow AA), 3.3.7 (friction, not a barrier)
- **critical (0)**

Four are genuinely arguable and are flagged as such on the page (D-1 option c): **1.4.2** has a case for
`critical` (Conformance Requirement 5 makes it interfere with the whole page), and **3.3.8** is the
strongest case in the batch; **3.1.1** and **3.3.7** have a case in each direction.

---

## 3. PART B — the authored pass

### The field: one, `edges.obeys`

Proposed as a new **edge type inside the existing `edges` object**, not a new top-level property.
`edges` is the KG parse layer built for typed, resolvable node references; `rule:` (landed #274,
s274-D8) and `ux:` (landed #275, s275-D4) are both live node kinds. Adding a top-level `obeys` would be
a second home for a fact `edges` already knows how to hold.

```
"edges": {
  "$obeys-contract": "AUTHORED, not inferred (P-274-3 + s275-D5, lane TO #276). …",
  "obeys": [ { "ref": "rule:ctkb-002", "$why": "…one line, written by reading the rule and this meta together…" } ]
}
```

`$why` is **required** by the diff. That is the whole of s274-D12 and s269-D5: the durable route is
authored, and an edge with no sentence attached is inference wearing a ref.

The diff (`meta.schema.diff`, **not applied**) adds a **scoped** `definitions.obeysEdge` rather than
widening the shared `definitions.edge` ref pattern — so `containedBy` still cannot point at a rule.
`properties` keeps its 34 keys.

**Validated both ways:** the six proposed metas produce **1 schema error each (6 total) against the LIVE
schema** — proving the diff is required, not decorative — and **0 errors against the proposed schema**.
The six live metas still validate clean against the live schema (0 errors): they were never opened for
writing.

### The six components

| component | spec file (filename join) | rules | laws | which laws |
|---|---|---|---|---|
| tags | common-toolkit-tags-chips.md | 9 | 2 | pr-fitts, pr-hick |
| tags-input | common-toolkit-tags-chips.md | 5 | 2 | pr-fitts, pr-speed-accuracy |
| notifications | common-toolkit-notifications.md | 17 | 2 | pr-hick, pr-graphical-perception |
| links | common-toolkit-links.md | 16 | 3 | pr-fitts, pr-hick, pr-speed-accuracy |
| button | common-toolkit-buttons.md | 14 | 3 | pr-fitts, pr-hick, pr-speed-accuracy |
| icon-button | common-toolkit-buttons.md | 6 | 2 | pr-fitts, pr-speed-accuracy |

**55 rule citations + 12 law citations = 67 entries.**

**Which extensions the specs cover — the brief asked me to say which:**

- **`tags-input` YES.** The chips half of the tags spec (ctkt-016…029) is the pills spec, and five of its
  clauses are about the chip *object* rather than about selection/toggle/response behaviour:
  ctkt-019 (anatomy incl. the destructive action), ctkt-021 (icons all-or-nothing), ctkt-026 (dynamic
  width, 8px, no truncation, wrap preserving radius), ctkt-027 (wrap, never horizontal scroll),
  ctkt-029 (44x44 over the whole chip). Those five bind the field's committed values directly.
- **`icon-button` YES.** ctkb-011 *names* icon-only as one of the buttons spec's three structural
  variations and supplies the blessed icon list. Its set is a strict **subset** of Button's (asserted in
  a bite): it never claims a rule Button itself does not obey.
- **`split-button` NO.** The buttons spec says nothing about a caret trigger or a two-target control.
  Authoring it would be a judgement call, not a filename join.

**Coverage against the spec files:** notifications takes all 17 of its file; button all 14; links all 15
**plus one declared cross-file rule**; tags + tags-input take 14 of the 23 in the shared tags-and-chips
file, with no overlap between them.

**The one cross-file citation, declared in its own `$why`:** `links` obeys `rule:ctkb-004` — the
buttons-vs-links boundary, which the buttons spec states from the other side ("for less prominent
actions, we use text links"). A bite asserts this is the *only* entry in all 55 whose spec file differs
from its component's.

**A finding, not a gap:** the 9 tags-chips rules nobody claims (ctkt-016, 017, 018, 020, 022, 023, 024,
025, 028) are the **selection / toggle / response pill** rules, and **there is no pill component in
`knowledge/components/`**. `segmented-control`, `selection-controls`, `status-indicator` and `tab-bar`
mention pills in prose; none is the component the spec describes. Worth a word at some point; not this
lane's to decide.

### The method, and what it is not

Every `rule:` id came from a **filename join** on `knowledge/guidelines/_rules-index.json`
(`r["file"] == "common-toolkit-<x>.md"`). **Not one came from a regex over rule prose.** P-274-3 records
why: the regex route produced va25-013 matching "Avatar" and "Badge".

Every `ux:` id is one of the **six grade-A laws** s269-D5 names, read out of `principles.json` by
`grade == "A"` at selftest time rather than retyped: `pr-fitts`, `pr-hick`, `pr-steering`, `pr-klm`,
`pr-speed-accuracy`, `pr-graphical-perception`. Note `pr-steering` and `pr-klm` bind **none** of the six
components, and I did not invent a reason for them to.

Each proposed meta is a **byte-for-byte copy of the live meta with exactly one span inserted**, proved
by cutting the span back out and comparing to the original, byte for byte, in both directions. No
existing JSON was re-serialised.

---

## 4. The flagged extras — ranked (Dave's "flag any extra you think are applicable")

The strong signal is the one the six above have: **a guideline file that IS the component**.

| # | component | signal | rules | why |
|---|---|---|---|---|
| 1 | **chart-line** | `data-visualisation-line-charts.md` | 11 | The file is the component. Identical signal, zero judgement. |
| 2 | **chart-pie** | `data-visualisation-pie-charts.md` | 11 | Same. Needs one word on whether `chart-donut` shares the file the way `icon-button` shares the buttons spec. |
| 3 | **chart-bar** | `data-visualisation-bar-charts.md` | 10 | Same. And `data-visualisation.md` sits above all three with **19 family-level rules** binding every chart component. |

**That is the whole of the filename-join route.** Of 34 guideline files, exactly **7** are named after a
component: the four common-toolkit ones (claimed here) and the three data-visualisation ones. After the
charts this route is exhausted — every further binding is a judgement call.

**Below the line — the weak tier, shown so the difference is visible rather than asserted.** Rule prose
name-matches, counted: `links 27 · button 16 · notifications 10 · table 9 · hero 8 · tags 8 ·
confirmation 6 · modals 4 · accordion 3 · summary 3 · banner 3 · dropdown 3 · avatar 2 · tooltip 2`.
The top three of those are components already authored here — and `avatar 2` is `va25-013` and
`va25-016`, i.e. **the exact false positive s274-D12 refused**. One of `modals`' four is `ctkn-011`, a
*notifications* rule that merely mentions modals. This tier is a reading list, never an edge.

---

## 5. PART C — the lane-ownership guard (his "fix")

`knowledge/_validate_lane_ownership.py` — reads `YOU ARE #(\d+)` from `_CHAIN.md`, lists
`git diff --cached --name-only`, warns on any staged path under `notes/_lanes/<M>/` where M != N.

**ADVISORY BY DECLARATION: exit 0 always, nothing blocked.** I read his "1. fix" back as *"make it
impossible"* and deliberately did **not** do that — making it impossible requires ruling one-seat vs
own-lane-only, and that rule is his. **No ruling was inscribed.** The blocking tier is D-6.

78 lines total: 58 lines of code plus the 12-line provenance docstring and the repo's 7-line helpgate
preamble. The brief said <= 60; I held the code to 58 rather than strip the provenance to hit a number.

```
python3 knowledge/_validate_lane_ownership.py --selftest
  OK   — session parsed out of the _CHAIN.md line shape
  OK   — own lane passes, two foreign lanes warn, non-lane path ignored
  OK   — unreadable _CHAIN.md means no session and NO false warning
selftest: 3/3

python3 knowledge/_validate_lane_ownership.py
LANE OWNERSHIP: OK — no staged path under another session's lane (this is #276).
```

---

## 6. The review page

`REVIEW-tie-off-2026-09-15-v1.html` — 40,307 bytes, **6 decisions**, **60 measured figures**, every
integer substituted at build time from `dry-run.json`, from the two builders' own tables, or counted
over `knowledge/`. No number is typed into the HTML or into `tie-off-decisions-2026-09-15.json`.

Adapted from lane RP's `_build_page.py` (#275): same house CSS, same label pattern (**no
`text-transform`** — nam-002), same localStorage + export + clear behaviour, same refusal if the page's
export is ever copied over the builder input. One CSS line added and declared in place: `code` wraps,
because this page prints a full W3C Understanding URL in code voice and an unbroken 90-character token
pushed the document past 390px.

**No `srcdoc` iframe is used** — this page renders no component previews, so the #261 bake-`type.css`-
into-the-srcdoc clause has nothing to apply to. The label-crop half of #261 is enforced and driven.

The decisions: **D-1** the 17 severities as a batch · **D-2** the three AAA criteria · **D-3** the field
name and shape · **D-4** the six authored metas · **D-5** the flagged extras · **D-6** the guard's tier.
Recommendation first on every one; (a) is the recommendation in all six.

### The page was driven, not just built ([[art-director-reviews-lane-output-268]])

```
source knowledge/_render/seat_env.sh && python3 notes/_lanes/276/tie-off/_drive_page.py
  ok  font loaded (HSBC_MtUnivers_Latin)                                    True
  ok  0 console errors / warnings / page errors                             0 messages, 0 bad, 0 page errors
  ok  descenders intact on the tight boxes (_validate_demo_page clause)     33 elements / 8 selectors · worst clip 0.00px
  ok  no element crops its own content                                      []
  ok  no text-transform:uppercase (nam-002)                                 []
  ok  no ALL-CAPS runs in visible text (nam-002)                            []
  ok  export is the RK shape {page, at, decisions:[{id, choice, note}]}
  ok  localStorage round-trips the choice and the note across a reload
  ok  390px: no horizontal scroll                                           {"s": 390, "c": 390}
  ok  light: accent #DA1A00, 0 crop, 0 overflow (s151-D1)
  ok  dark:  accent #F6604C, 0 crop, 0 overflow (s151-D1)
DRIVE PASS
```

**The driver caught two real defects on the first run and they were fixed, not waived:** eleven ALL-CAPS
emphasis words in my own prose (nam-002), and a 480px document width at the 390px viewport caused by the
unbroken W3C URL. Then the full-page screenshot and two element crops were **reviewed by eye** — the
rules table reads correctly, the three AAA levels are marked in the accent, and every severity carries
its reasoning in the last column.

---

## 7. Gates

| gate | result |
|---|---|
| `python3 knowledge/_validate_kg.py` | **OK** — 139 metas checked, every ref parses+resolves, every null carries a note, `gen_kg_edges.py` idempotent-clean (unchanged: this lane landed nothing) |
| `_build_rules.py --selftest` | **15/15 bites green** |
| `_author_metas.py --selftest` | **17/17 bites green** |
| `_validate_lane_ownership.py --selftest` | **3/3 green** |
| `_mutate.py` (18 mutants) | **ALL 18 MUTANTS CAUGHT**, 0 survivors, both baselines PASS |
| schema validation of all 17 rules | **0 failures** against `knowledge/compliance/rule.schema.json` (jsonschema) |
| schema validation of the 6 metas | **6 errors against the LIVE schema** (the diff is required) · **0 against the proposed schema** · the 6 live metas still **0** |
| `_drive_page.py` | **DRIVE PASS** — 11/11 checks, both themes |
| `git status` | only `notes/_lanes/276/` and `knowledge/_validate_lane_ownership.py` are mine (see §8) |

### The mutants

```
BASELINE rules  red=[] crashed=False — PASS
BASELINE metas  red=[] crashed=False — PASS
  M1  rules  an AAA criterion is graded serious                              -> RED 7
  M2  rules  the pending-EN clause stamped on every rule                     -> RED 5
  M3  rules  an eighteenth criterion smuggled in                             -> RED 1,10
  M4  rules  2.4.13 demoted to AA                                            -> RED 7
  M5  rules  the internal policy sentence retyped                            -> RED 9
  M6  rules  the file id stops matching the W3C page slug                    -> RED 4
  M7  rules  applies_to guessed instead of derived                           -> RED 13
  M8  rules  a 2.2 addition claims to have existed in 2.1                    -> RED 6
  M9  rules  a rule graded critical                                          -> RED 8
  M10 rules  the dry run counts a null as resolved without the sc present    -> RED 11
  M11 rules  external_automatable_refs hand-typed                            -> RED 14
  M12 rules  OUT repointed at the live compliance corpus                     -> RED 15
  M13 metas  a regex-style false positive admitted (va25-013)                -> RED 3,5
  M14 metas  a ux: ref that is not one of the six grade-A laws               -> RED 10
  M15 metas  an authored $why emptied                                        -> RED 11
  M16 metas  the splice eats a byte instead of purely inserting              -> RED 14
  M17 metas  icon-button claims a rule Button does not obey                  -> RED 3,9
  M18 metas  one $why reused verbatim on two components                      -> RED 12
ALL 18 MUTANTS CAUGHT
```

**M16 survived the first run and exposed a real hole**: the original additivity bite used a
prefix/suffix walk, and an insertion whose first character matches the character it displaces slides
straight past it. The bite was replaced with an exact reconstruction in both directions. A mutation test
proving the clause, doing its job.

---

## 8. Ownership, and what this lane did not touch

`git status` before the commit:

```
 M notes/_REHEARSAL-LOG.jsonl          <- NOT MINE by intent: _checkin.py appends to it
 M notes/_dream/_GRADE-DECISIONS.jsonl <- NOT MINE by intent: same
?? knowledge/_validate_lane_ownership.py
?? notes/_lanes/276/
```

The two modified `.jsonl` files are the side effect of running `knowledge/_checkin.py` (the mandatory
gauge). They are **left unstaged** — this lane commits only `notes/_lanes/276/` and the one guard file.
Declared here rather than quietly swept in.

`__pycache__/` under the lane is a build artefact of `_build_page.py` importing the two builders; it is
not committed.

---

## 9. What is Dave's, and what a land lane would do next

Nothing on the review page is a ruling and none is inscribed here.

1. **D-1…D-6** on `REVIEW-tie-off-2026-09-15-v1.html`, exported as JSON the way RP's page did.
2. On a "go", a **land lane**: copy `proposed-rules/*.json` into `knowledge/compliance/rules/`, apply
   `meta.schema.diff` by textual span, splice the six `obeys` blocks into the live metas the same way
   (the splice is already proved additive), then re-run
   `python3 knowledge/gen_kg_rules.py --land --ratified <the new ruling id>` and
   `python3 knowledge/_build_kg_explorer.py`. The 19 nulls become 19 edges **with no change to the
   generator** — that is what the dry run measures.
3. **P-274-2 and P-274-3 both discharge** at that point; P-274-1 (edit mode) is untouched and stays
   parked, per Dave's "park it has a tripwire".
4. D-5 (a) would make the charts the next authored pass, and then the filename-join route is spent.

## 10. Gauge at close

`python3 knowledge/_checkin.py` at this seat: **207,610 cl100k-estimate THROUGHPUT** for this lane's own
conversation (161 transcript records). That is throughput, not FILL — a delegated lane cannot read the
conductor's `message.usage`, and the two objects are never summed or converted. My own remaining budget
at close was ~14.6M of 15M tokens, so resident context was never near a stop line.

WARNING **`/sessions` disk is 96.2% full** (363,264 KB free) and `_checkin.py` flags it as a STOP-class
condition: at 100% no session boots. Reported here because it is a measured finding of this seat, not
because it is this lane's to fix.
