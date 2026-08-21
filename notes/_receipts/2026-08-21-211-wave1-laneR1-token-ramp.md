# LANE R1 receipt — `gen_token_ramp` comment defect (P-8's generator cause)

**Session** #211 findings-repair wave 1 · **lane** R1 (Opus) · **brief** `notes/_briefs/2026-08-21-211-findings-repair-wave1-v1.md`
**Repo HEAD at lane open** `fc6b35d` · **NO COMMITS MADE** (conductor's serial) · **no `git checkout`** · **no `_build_all.py`**

> ⛔ **NOTHING IN THIS RECEIPT IS A RULING.** Every DO-NOT-RULE item this lane brushed is returned PRICED, below.

---

## HEADLINE

**P-8: 58 findings in 9 files → 12 findings in 4 files.** All **46** `COMMENTED-OUT` findings are gone;
the **12 `ABSENT`** findings are a DIFFERENT SHAPE in four files OUTSIDE this lane's fence — reported, not touched.
The generator was fixed **at cause** (it could not see HTML comments), mutation-tested, and the repair was
**driven in a browser against the HEAD version as a control**: `.cap` computed `opacity` **1 → 0.44**.

---

## ⛔ THE REGION QUESTION, ANSWERED BEFORE THE REGEN (the brief's precondition)

The brief required: *"NAME in your receipt which file REGIONS `gen_token_ramp` rewrites; regen only those.
If it owns more than the AUTO-TOKENS blocks, STOP and return the region list instead."*

**It owns exactly one region per file: the `AUTO-TOKENS START … AUTO-TOKENS END` block.** This was not read off
the source and asserted — it was **measured on all 147 target files, twice** (dry-run before writing, and again
after), by hashing each file with the AUTO-TOKENS block *stripped out* and comparing:

| what was measured | before write | after write |
|---|---|---|
| target files in scope (`snippets/*.reference.html` + `_proforma/*.html`) | 147 | 147 |
| files whose full bytes change | 5 | 5 |
| **files whose NON-AUTO-TOKENS bytes change** | **0** | **0** |

⚠ **A `diff` of the five files LOOKS like it moves prose, and it does not.** The old block had been injected
*into the middle of a prose comment*, severing it; removing the block rejoins the comment's two halves, so the
tail appears as `+` in one hunk and `-` in another. Net: **byte-identical outside the block**. The assertion
above (`strip_block(new) == strip_block(old)`, per file) is the statement that survives the diff's appearance.

**Probeable token:**
```
python3 - <<'EOF'
import importlib.util,sys,os,hashlib,subprocess
sys.path.insert(0,os.path.abspath('knowledge'))
s=importlib.util.spec_from_file_location("g","knowledge/gen_token_ramp.py")
g=importlib.util.module_from_spec(s); s.loader.exec_module(g)
bad=[]
for p in g.targets():
    old=subprocess.run(["git","show","HEAD:"+str(p.relative_to(os.getcwd()))],capture_output=True,text=True).stdout
    if not old: continue
    if g.strip_block(old)!=g.strip_block(p.read_text()): bad.append(p.name)
print("files whose NON-AUTO-TOKENS bytes changed:",len(bad),bad)
EOF
```
→ **`files whose NON-AUTO-TOKENS bytes changed: 0 []`**

---

## THE DEFECT, AT CAUSE

`render()` located its injection point with `re.search(r"<style[^>]*>\n?", html)` over the **raw** text. In five
files the first LITERAL `<style>` sits inside a prose comment — `Button.reference.html:45`:

```
<!-- TYPE-001 · canon type composites. MUST come BEFORE the component <style> below: `.btn` is …
```

The generator appended the entire `:root{}` alpha ramp after that literal `<style>` **text**, i.e. **inside the
comment**. Three consequences, each measured:

1. The ramp is **not CSS**. Every `var(--alpha-NN)` in those files fell to *invalid at computed-value time*.
2. It was **idempotent over its own defect** — `--check` reported `147 already in sync` **forever**. A generator
   that re-derives the same wrong answer cannot report drift [[ritual-output-is-not-evidence]].
3. It **severed the prose comment**, so the comment's tail (`-->`, the `<link>`, the real `<style>`) ended up
   *inside the style element* — which is why an HTML parser found `AUTO-TOKENS` in `<!-- -->` and never in `<style>`.

**The fix** (`knowledge/gen_token_ramp.py`): a length-preserving `mask_comments()` blanks every HTML comment
(an unterminated `<!--` masks to EOF, as a browser reads it); **both** the injection point **and** the set
detector `sets_referenced()` now read the masked copy; and `render()` carries a **post-condition** that refuses
(`TokenRampError`) if the block it just built would land inside a comment.

⚠ **The detector was changed too, and that is deliberate — it is the same class.** A `var(--alpha-60)` written
only in prose is not a reference. **Blast radius measured before adopting it: identical, 5 files, byte-identical
output either way.** Fixing one face of a class and not the other is [[conflated-fix-guarantees-recurrence]].

---

## CLAIM TABLE (`s182-D1` — every mechanical claim carries a probeable token)

| # | claim | probeable token | verdict |
|---|---|---|---|
| 1 | The generator owned only the AUTO-TOKENS block; regen changed nothing else | the block above → `0 []` | ✅ DRIVEN |
| 2 | Before the fix, the generator reported the broken tree as clean | `git stash`-free: at HEAD `python3 knowledge/gen_token_ramp.py --check` → `0 file(s) DRIFTED … 147 already in sync.` rc=0 | ✅ DRIVEN (baseline captured pre-edit) |
| 3 | After the fix, the generator SEES the drift | `python3 knowledge/gen_token_ramp.py --check` (post-fix, pre-write) → `5 file(s) DRIFTED (5 with block, 0 block-removed), 142 already in sync.` rc=1 | ✅ DRIVEN |
| 4 | The regen is idempotent | `python3 knowledge/gen_token_ramp.py --check` (post-write) → `0 file(s) DRIFTED … 147 already in sync.` **rc=0** | ✅ DRIVEN |
| 5 | Selftest green, with 4 new comment bites | `python3 knowledge/gen_token_ramp.py --selftest` → `gen_token_ramp selftest: 6 bites GREEN + 4 comment bites (#211) GREEN` rc=0 | ✅ DRIVEN |
| 6 | The AUTO-TOKENS block is now in a `<style>` ELEMENT and in NO comment — asked of an **HTML parser**, not grep | `html.parser` over each of the 5: `in <style>` **0→1**, `in <!-- -->` **1→0** (all five) | ✅ DRIVEN |
| 7 | The declarations are live **CSS** — asked of a **CSS parser** (`tinycss2`) over HTML-parsed `<style>` text only | `--alpha-*` declarations live: **BEFORE 2 → AFTER 122**; parse errors 0 both tiers | ✅ DRIVEN |
| 8 | The references resolve **in the browser**, with the HEAD file as control | chromium `getComputedStyle(:root)`: ramp rungs resolving **0 → 24** in all 5; dangling reference sites **46 → 0** | ✅ DRIVEN |
| 9 | A real consumer's computed style changed | `.cap { opacity: var(--alpha-44) }` computed **`1` (HEAD, initial — ramp dead) → `0.44` (NOW)** | ✅ DRIVEN |
| 10 | Injected probe element resolves the ramp through the live cascade | `rgba(0,0,0,var(--alpha-60))` computes **`rgba(0, 0, 0, 0)` (HEAD) → `rgba(0, 0, 0, 0.6)` (NOW)**, all 5 files | ✅ DRIVEN |
| 11 | The five files still render — layout unbroken | chromium: `.btn` elements **16 = 16**, `body.scrollHeight` **697 = 697** HEAD vs NOW; screenshot read | ✅ DRIVEN |
| 12 | The licensed face actually paints (canvas probe, **not** `fonts.check`) | `measureText('HHHH')` @32px: aliased **92.4375** vs monospace **77.0625** → `differs: true`, both tiers | ✅ DRIVEN |
| 13 | P-8 delta | `python3 knowledge/_probe_registry/probe_dangling_var_text.py --check` → `PROBE P-8 — findings=12` (was 58) | ✅ DRIVEN |
| 14 | P-7 did not move | `python3 knowledge/_probe_registry/probe_container_self_query.py --check` → `PROBE P-7 — findings=6` (premise table: 6) | ✅ DRIVEN |
| 15 | ★ The ds-018 **C2 gate is BLIND to this class** and was green over it | drove C2's own `css_of()` on HEAD text of all 5: **`24 decl / 0 dangling`** — it read the commented-out declarations as reachable | ✅ DRIVEN |
| 16 | The C2 gate's 12 live failures are NOT this lane's | all 12 are `ABSENT` in Template-`confirmation`/`empty`/`error`/`settings`; the 5 repaired files score `0 dangling` under C2 at **both** tiers (claim 15) | ✅ DRIVEN |

### Mutation matrix — the CLAUSE, not the feature [[mutation-tests-the-clause-not-the-feature]]

| mutant | selftest rc | verdict |
|---|---|---|
| M1 — injection point reads RAW text (the #211 defect restored) | 1 | ✅ BITES |
| M2 — post-condition disabled | **0** | ⛔ **SURVIVES — declared below** |
| M3 — detector no longer comment-masked | 1 | ✅ BITES |
| M4 — unterminated `<!--` no longer masks to EOF | 1 | ✅ BITES |
| M5 — `mask_comments` stops preserving length (index misalignment) | 1 | ✅ BITES |
| M1+M2 — primary fix reverted AND backstop off | 1 | ✅ BITES (via the direct `in_comment(out6, …)` assertion) |

⚠ **M2 SURVIVES AND THAT IS DECLARED, NOT SMOOTHED.** The post-condition is a **redundant backstop**: with the
primary fix in place nothing can reach it, so removing it alone changes no observable behaviour. It is covered
*in composite* — M1 alone is caught **by the post-condition firing**, and M1+M2 together is caught by the
selftest's own `in_comment` assertion. To bite M2 in isolation would need a case where the injection point is
legal but the block still lands in a comment, and I could not construct one. **An unbitten guard is an honest
UNPROVEN, not a pass.**

---

## PREMISE CORRECTION — the brief's own figure was wrong, and it is corrected by MEASUREMENT

The brief (and the W-45 manifest note it was copied from) says *"Button, with 46 declarations commented out"*.
**Measured, that is wrong on both halves** [[premise-ages-faster-than-rule]]:

| the brief said | measured |
|---|---|
| Button has 46 declarations commented out | Button carried **1** of the 46 P-8 findings (`--alpha-44` on `.cap`) |
| — | **46** is the five-file total of dangling reference **SITES**, not declarations, and not Button's |
| — | **120 declarations** were dead (the 24-rung ramp `--alpha-04..96` × 5 files); Button now carries 26 (24 generated + 2 local) |

**Per-file P-8 findings, before → after:**

| file | before | kind | after |
|---|---|---|---|
| `Template-list-index.reference.html` | 15 | COMMENTED-OUT | **0** |
| `Template-dashboard.reference.html` | 12 | COMMENTED-OUT | **0** |
| `Template-detail.reference.html` | 11 | COMMENTED-OUT | **0** |
| `Chart-butterfly-h.reference.html` | 7 | COMMENTED-OUT | **0** |
| `Button.reference.html` | 1 | COMMENTED-OUT | **0** |
| `Template-settings.reference.html` | 4 | ABSENT | **4** — outside fence |
| `Template-confirmation.reference.html` | 4 | ABSENT | **4** — outside fence |
| `Template-error.reference.html` | 3 | ABSENT | **3** — outside fence |
| `Template-empty.reference.html` | 1 | ABSENT | **1** — outside fence |
| **total** | **58 in 9 files** | | **12 in 4 files** |

★ **Two instruments agreed independently.** P-8 counts 46 COMMENTED-OUT findings from TEXT; the browser's own
CSSOM counted **46** unresolvable reference sites at HEAD (1 + 7 + 12 + 11 + 15). Same number, different grammar.

★ **Why Button's hover still worked at HEAD:** Button **locally declares `--alpha-68`** (twice — light + dark
blocks) outside the generated block, so `.btn.primary:hover` survived. Its *only* casualty was `.cap`'s
`opacity: var(--alpha-44)` — a **44% text fade that has been rendering at 100% opacity**, on a caption,
invisibly. That is the [[dangling-dataviz-var-renders-silent-black]] shape: wrong, quietly, forever.

---

## WHAT WAS DRIVEN vs WHAT STAYS UNPROVEN

**DRIVEN** (chromium `chromium_headless_shell-1234` @ `/var/tmp/pw-browsers-s197`, playwright reused read-only
from `/var/tmp/pylibs`, `TMPDIR=/var/tmp`, canvas probe per `_RUNBOOK-render-verify.md`):
- HTML parse · CSS parse (`tinycss2`) · rendered `getComputedStyle` · injected-probe cascade resolution ·
  hover state driven · layout invariants · font paint · screenshots **rendered AND read**.
- Screenshots (NON-REPO, session outputs mount): `laneR1-Button-HEAD.png`, `laneR1-Button-NOW.png`,
  `laneR1-Button-hover-{HEAD,NOW}.png`. Drive harness: `(NON-REPO: /var/tmp/drive211/probe.py)` — a one-off
  lane harness, deliberately not homed in-repo (`s191-D2` marker carried in its header).

**UNPROVEN — each a priced TODO, none smoothed:**
1. **M2 (the post-condition) is unbitten in isolation.** ~15 min to attempt a constructed case; may be
   genuinely unreachable, in which case the honest answer is "backstop, covered only in composite".
2. **Only Button was rendered and looked at.** The other four were proven by computed style, not by eye.
   The four are template organisms in Dave's eye queue (`W-77`, `W-82` neighbourhood) — **their appearance
   will now differ** (alpha is live where it was dead). ⚠ **This is the repair working, not a regression** —
   but it is a visual change to artefacts awaiting Dave's eye, and he should be told before he looks.
   Price: ~10 min to render the four before/after pairs if the conductor wants them for his queue.
3. **No `_build_all.py` run** (hard fence). The two steps that consume this generator (`--check`, `--selftest`)
   were driven standalone, both rc=0. The other ~125 steps are UNRUN by this lane.
4. **`_proforma/*.html` (12 of the 147 targets) were in scope for the generator but did not change** —
   proven in sync, not proven by render.

---

## ⚠ THE FINDING THE CONDUCTOR NEEDS TODAY

**The ds-018 C2 gate — `_validate_property_resolves.py`, `BLOCKING`, promoted by `s121-D1`, whose entire job is
"a `var()` that resolves to NOTHING" — was GREEN over this defect for its whole life.** It strips *CSS* comments
(`/* */`, line 93, with the right instinct in its own comment: *"or a commented-out example counts as a use"*)
but has **no notion of HTML comments**. Its `<style>`-chunk regex matched the literal `<style>` inside the prose
comment, so the 24 dead declarations counted as reachable. Driven, both tiers: `24 decl / 0 dangling`.

Same shape as [[no-gate-parses-the-artefact]] and [[green-tests-cannot-see-scope]]: **the gate for the class did
not parse the artefact in the consumer's grammar.** ⛔ **NOT WIRED — PRICED** (a repair never dials or extends a
gate; derivation governance): add HTML-comment blanking to `_validate_property_resolves.py:css_of()`, reusing the
now-proven `mask_comments()`, plus a mutation bite. **~30–40 min, one file, needs a blast-radius run first**
because it may surface further findings across all 147 files.

**AND: C2 `--strict` is RED ON THE CURRENT TREE — 12 failures, rc=1 — and it is a BLOCKING `GATE` step in
`_build_all.py` (step at line 388/772).** Those 12 are exactly P-8's ABSENT-12, in four files this lane may not
touch. **They pre-date wave 1 and this lane did not cause them** (claim 16) — but the build cannot go green
until someone repairs them. **Nobody in wave 1 owns those four files.** That is the conductor's call.

---

## ⛔ DO-NOT-RULE ITEMS THIS LANE BRUSHED — RETURNED PRICED, NOTHING SETTLED

| item | how this lane brushed it | returned as |
|---|---|---|
| **P-7 / P-8 promotion or park** (`W-85`, ADVISORY on Dave's word #210) | P-8 went 58 → 12 by repair | **Repair ≠ promotion. Not proposed.** P-8 remains ADVISORY and is **still not green** (12 stand). Promotion is Dave's. |
| **ANY threshold, constant or count in gates** (`s208-D1` rider) | none moved | **Nothing dialed.** The one numeral I touched is the selftest's own label, ADDED to, never trimmed: `6 bites GREEN` is preserved verbatim and `+ 4 comment bites (#211) GREEN` appended. That is a strengthening, declared, not a re-base. |
| **The 34 proposed organisms + REVIEW-210 pages** (his eye queue — do not touch, do not "improve") | 4 of the 5 regenerated files are Layer-2 templates in that queue | **Only the machine-owned AUTO-TOKENS region was rewritten — 0 human-authored bytes changed** (claim 1). No design content read, judged or altered. ⚠ Their *rendering* changes; flagged in UNPROVEN #2. |
| **The 12 ABSENT vars** (`--header`/`--fborder`/`--error`/`--error-tint`/`--success`/`--success-tint`/`--warning`/`--warning-tint`) | measured, named, left alone | **REPORTED, NEVER TOUCHED** — outside this lane's fence, in four files (`Template-confirmation`/`-empty`/`-error`/`-settings`) belonging to `W-82`. This is the #210 `--muted` shape unrepaired in four more files. **Price: ~30 min** to declare them in both theme blocks per file — but the values are **colour choices** (`--error-tint`, `--warning`, `--success`) and the two-red law + grey-tint check make that **Dave's**, not a mechanical repair. |
| **ds-005 class choice** | not reached | untouched |

---

## CONSEQUENCES / PITFALLS (mandatory, Dave #165)

**What could recur:**
1. **A generator that cannot read its target's grammar will re-make this hole — so I CHECKED THE THREE SIBLINGS
   RATHER THAN PRICING THE CHECK.** `gen_token_ramp` is the *fourth* injection type; AUTO-PARTIAL (CSS),
   AUTO-BEHAVIOUR (JS) and AUTO-MARKUP (HTML) in `knowledge/gen_component_partials.py` inject into the same files.
   **Read-only, nothing touched. Result: all three are STRUCTURALLY IMMUNE to this exact defect** — each replaces
   text between an **explicit marker pair that must already exist in the consumer**
   (`AUTO_RE`/`BEHAVIOUR_RE`/`AUTO_MARKUP_RE`, lines 85/90/121), so a human decided the injection site. None
   locates an anchor by structural search the way `<style>` was located. **Residual, named:** if a human ever
   places a marker pair inside an HTML comment, the same shape returns — hand-authored, not generator-made.
   ⚠ **BUT THE SAME CLASS IS LIVE IN ITS CONTRACT CHECKER**, one layer along:
   `gen_component_partials.py:199 declared_value()` does `re.search(re.escape(var) + r'\s*:\s*([^;]+);', html)`
   over the **RAW** html, and line 222 fails only when it returns `None`. **A `--var: value;` sitting inside an
   HTML comment therefore satisfies the "is it declared" contract** — exactly what C2 did, in a second
   instrument. ⛔ **NOT TOUCHED — outside this lane's fence. PRICED: ~20 min** (blank comments before the
   search, plus one mutation bite), and it wants the same blast-radius run as the C2 extension.
2. **A generator idempotent over its own defect reports "in sync" forever.** `--check` was rc=0 across every
   session since the block landed. **The class: a generator's self-check tests agreement with itself, never
   correctness.** The post-condition added here is the pattern that breaks it — assert a property of the
   OUTPUT, not equality with the last output.
3. **Any consumer whose prose mentions `<style>`, `<!--` or a `var(--…)` name is now handled — but only for
   THIS generator.**

**What this repair does NOT fix:**
- The 12 ABSENT findings (four files, outside fence, blocking C2).
- The C2 gate's HTML-comment blindness (priced, not wired) — **so this class can still be reintroduced by hand
  and no gate will see it.** The generator can no longer create it; a human editor still can.
- Any *other* var class: cascade-scope dangling (P-8's own declared blind spot), wrong-value resolution, or
  dead-but-declared properties.
- Anything in `_proforma/` beyond "in sync" — unrendered.

**Which class this belongs to:** [[no-gate-parses-the-artefact]] (first gate must parse in the consumer's
grammar) compounded with [[dangling-dataviz-var-renders-silent-black]] one layer up — the generator *wrote* the
dangling reference rather than a human, and thirteen-plus gates plus the one gate built for exactly this class
all reported green. [[green-tests-cannot-see-scope]].

---

## `git status --short` — READ BACK VERBATIM AT LANE CLOSE

```
 M knowledge/_119-sweep-recheck.json
 M knowledge/_probe_registry/probe_dangling_var_pixel.py
 M knowledge/_probe_registry/probe_input_trim_enactment.py
 M knowledge/gen_token_ramp.py
 M knowledge/snippets/Button.reference.html
 M knowledge/snippets/Chart-butterfly-h.reference.html
 M knowledge/snippets/Date-picker.reference.html
 M knowledge/snippets/Drawer.reference.html
 M knowledge/snippets/Form-layout.reference.html
 M knowledge/snippets/Template-dashboard.reference.html
 M knowledge/snippets/Template-detail.reference.html
 M knowledge/snippets/Template-list-index.reference.html
 M notes/_REHEARSAL-LOG.jsonl
 M notes/_dream/_GRADE-DECISIONS.jsonl
?? notes/_briefs/2026-08-21-211-findings-repair-wave1-v1.md
?? notes/_receipts/2026-08-21-211-wave1-laneR1-token-ramp.md
?? notes/_receipts/2026-08-21-211-wave1-laneR4-probe-hygiene.md
```

⚠ **The three sibling paths appeared DURING this lane, not at its open** — R3's `Date-picker` and `Drawer`
first, then `Form-layout` between my second-to-last and last read. Lanes R3/R4 were live alongside me. **The
tree is shared; this listing is a moment, not a state** [[conclusions-are-debt-s129-d5]] — re-read it at the
conductor's serial, do not carry mine forward.

**Every path attributed — mine, a sibling's, or pre-existing:**

| path | whose |
|---|---|
| `knowledge/gen_token_ramp.py` | **MINE** — the fix |
| `knowledge/snippets/Button.reference.html` | **MINE** — AUTO-TOKENS region only |
| `knowledge/snippets/Chart-butterfly-h.reference.html` | **MINE** — AUTO-TOKENS region only |
| `knowledge/snippets/Template-dashboard.reference.html` | **MINE** — AUTO-TOKENS region only |
| `knowledge/snippets/Template-detail.reference.html` | **MINE** — AUTO-TOKENS region only |
| `knowledge/snippets/Template-list-index.reference.html` | **MINE** — AUTO-TOKENS region only |
| `knowledge/_probe_registry/probe_dangling_var_pixel.py` | **LANE R4's** (P-3 rc=77 hygiene) |
| `knowledge/_probe_registry/probe_input_trim_enactment.py` | **LANE R4's** (P-6 rc=77 hygiene) |
| `knowledge/snippets/Date-picker.reference.html` | **LANE R3's** |
| `knowledge/snippets/Drawer.reference.html` | **LANE R3's** |
| `knowledge/snippets/Form-layout.reference.html` | **LANE R3's** (the named input snippet) |
| `knowledge/_119-sweep-recheck.json` | **PRE-EXISTING** — dirty at lane open, before I ran anything |
| `notes/_REHEARSAL-LOG.jsonl` | **PRE-EXISTING** — dirty at lane open |
| `notes/_dream/_GRADE-DECISIONS.jsonl` | **PRE-EXISTING** — dirty at lane open |
| `?? notes/_briefs/2026-08-21-211-…-v1.md` | the conductor's brief |
| `?? notes/_receipts/…-laneR4-probe-hygiene.md` | **LANE R4's** receipt |

**No gate I ran wrote a tracked audit file.** `_validate_property_resolves.py --strict` and
`_validate_proforma.py` were both run; neither appears above. **NO COMMITS. NO `git checkout`. NO `_build_all.py`.**

**Environment change, declared:** `pip install tinycss2 --break-system-packages` in the sandbox (needed for the
CSS-parse proof). Sandbox-only, nothing in the repo. Root fs was at **100% (85M free)** — Playwright and the
browser were **reused read-only** from `/var/tmp/pylibs` and `/var/tmp/pw-browsers-s197`; **nothing was
downloaded**.

---

## SUB SPEND

⛔ **NOT MEASURABLE FROM INSIDE THE LANE — and it is declared UNKNOWN rather than estimated**
[[feedback-measuring-tool-must-not-guess]]. A sub cannot read its own `message.usage`; the conductor takes the
figure from the sub's usage record for the `subs N tokens (n=…)` line at wrap. What I *can* report as a shape,
labelled as such: **~30 tool calls**, one browser session reused across all renders, no `_build_all` run, two
PNGs read.
