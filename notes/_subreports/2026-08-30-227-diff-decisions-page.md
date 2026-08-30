# s227 · Diff decisions page — Dave works the diff with his hands

**COUNTS: cards 32 (findings 25 · ruling-shaped 7) · UNPROVEN 2**

Sub: Opus build sub, session #227, lane 5. Conductor: Fable seat.
⛔ No rulings, no commits, no store rows. One file created:

- `reviews/DASHBOARD-DIFF-DECISIONS-2026-08-30-v1.html` (64,060 bytes, self-contained)

Source, unmodified: `notes/_subreports/2026-08-30-227-dashboard-regen-diff.md`.

---

## 1. What it is

Dave's words: *"can you make … an html page so I can make the selections and leave comments
easier, then I can copy and paste a prompt to you."* So the page's **output is a prompt**, not a
report. Everything else on it exists to make that prompt easy to type.

- **25 finding cards** — A1–A3 (generation defects), B1–B14 (canon gaps), C1–C8 (Dave
  improvements). Each carries its id, classification, the report's own title sentence, the
  evidence quoted **with `file:line`**, and the report's proposed action where it has one.
  Nothing is summarised away; only the report's connective prose is trimmed.
- **7 ruling-shaped question cards** — `Q-A1 · Q-A2 · Q-A3 · Q-B3 · Q-B4 · Q-B7 · Q-B14`, in
  their own band, each linked back to the finding that raised it.
- **Two non-card sections carried through so nothing reads as more settled than it is:** the
  report's "inversion worth noticing" (§3c tail) sits as a plain note at the end of band C, and
  the four **declared unproven** items (U1–U4) sit in their own read-only band.

## 2. The one deliberate departure from the brief, declared

The brief specifies `Adopt / Park / Reject / Discuss` per card. Findings get exactly that.
**Questions get `Answer / Park / Discuss`** — "Adopt" and "Reject" are meaningless verbs against
*"which is it: 4, 1px or 2px?"*, and the comment box on a question card is relabelled
**"Your answer / ruling"**, because on those cards the comment *is* the answer. Serialisation
stays uniform: `<id> <VERB> — <comment>`. If the conductor wants the strict four everywhere,
it is a two-line change to `Q_OPTS`.

## 3. The prompt it produces

Proven by execution (see §4), worst case shown:

```
APOLLO #227 — dashboard regen diff, my decisions
Source: notes/_subreports/2026-08-30-227-dashboard-regen-diff.md
Page: reviews/DASHBOARD-DIFF-DECISIONS-2026-08-30-v1.html
Findings decided 5/25 · questions answered 1/7

FINDINGS
A1 ADOPT — yes — wrap it, and kill the re-declarations
B5 PARK
B12 DISCUSS — how do we gate this?
C8 REJECT — stopgap, not the fix

QUESTIONS
Q-B4 ANSWER — 2px. mine.

NOTES ON UNDECIDED
B9 (no decision) — no decision but note the 1280 measure

UNDECIDED: A2, A3, B1, B3, B4, B6, B7, B8, B9, B10, B11, B13, B14, C1, C2, C3, C4, C5, C6, C7
UNANSWERED: Q-A1, Q-A2, Q-A3, Q-B3, Q-B7, Q-B14
```

Multi-line comments are collapsed to one line so the format stays one-line-per-finding.
A comment left on an **undecided** card is not lost — it surfaces under `NOTES ON UNDECIDED`.

**Three copy tiers, in order:** `navigator.clipboard.writeText` → hidden-textarea
`document.execCommand("copy")` → select the visible `<pre>` and say
*"Copy blocked — text selected below, press Cmd/Ctrl+C"*. The `<pre#prompt>` is **always
rendered and always live**; the page says in its own words that this block is the real output
and the button is only a convenience. Pitfall 2 closed.

**Durability.** `localStorage` under one key, every read and write in `try/catch`; with storage
dead the page is fully functional and only loses refresh-survival. The page tells Dave, in the
"How this works" block, that the paste is the durable artefact and a cleared cache loses the
rest. Pitfall 3 closed.

## 4. Proof — the controller was EXECUTED, not just grepped

No headless browser (constraint), so instead the page's `<script>` was extracted and **run under
`node` against a ~40-line DOM shim** built from the real HTML's card list. This drives the actual
code path, not a re-implementation of it.

| probe | result |
|---|---|
| `node --check` on the page's script | SYNTAX OK |
| cards parsed back out of the HTML (stdlib `HTMLParser`) | **32** — findings **25**, questions **7** |
| class split | `defect 3 · gap 14 · improve 8 · question 7` — matches the report's COUNTS line exactly |
| duplicate card ids | none |
| every finding id present in the source `.md` | yes, all 25 |
| `Q:` markers in the source `.md` | 8 hits, of which 1 is the legend at line 12 → **7 real questions**, matching the 7 cards (lines 208·235·259·343·360·450·569 → A1·A2·A3·B3·B4·B7·B14) |
| controls built at runtime | 4 radios on every finding card, 3 on every question card, 1 textarea on all 32 — **121 inputs total**, as predicted |
| in-page assertion string | `25/25 findings rendered · 7/7 ruling-shaped questions rendered · all ids unique · matches the report's COUNTS line.` |
| decide 5 findings + 1 question | counts went `0/25 0/7` → `5/25 1/7`; chips read Adopt · Park · Reject · Discuss · Answer · Undecided |
| localStorage round trip | key written, 32 entries, `A1 = {"d":"adopt","c":"…"}` |
| all six filters | visible cards 32 · 31 (undecided) · 3 · 14 · 8 · 7, `aria-pressed` exclusive |
| Clear all | counts back to `0/25 0/7`, chips reset, storage rewritten |
| copy with **no** clipboard API and `execCommand` returning false | falls through to `Copy blocked — text selected below…`, `<pre>` still holds the full prompt |
| external resources (parsed, not text) | **none** — fully self-contained, no fonts, no scripts, no images |
| brace balance | CSS `{}` balanced · script brackets balanced · `<article>` 32/32, `<section>` 6/6, `<div>` 41/41, `<pre>` 35/35 |

Pitfall 1 closed twice over: the count is asserted **in-page** (visible line under the prompt,
turns red and says "Tell Claude" on mismatch) and **out-of-page** by the parse above.

## 5. UNPROVEN, declared

- **U1 · Nothing has been rendered.** No headless browser and no pip on a full disk, per the
  lane constraint. Layout, type sizes, colour and the light/dark flip are **unseen**. The logic
  is executed and proven; the *appearance* is not. Dave opening the file is the first render.
- **U2 · `label:has(input:checked)` is unverified in Dave's browser.** It tints the selected
  radio's pill. If `:has()` were unsupported the tint is simply absent — the card's colour chip
  and left border are set from JS via `data-state` and do not depend on it, so the "cards visibly
  change state" requirement degrades gracefully rather than failing. Not proven, but bounded.

## 6. REPLAY-THESE

```bash
# card counts + class split + id uniqueness, parsed from the page itself
python3 - <<'PY'
from html.parser import HTMLParser; import collections
P="reviews/DASHBOARD-DIFF-DECISIONS-2026-08-30-v1.html"
class C(HTMLParser):
    def __init__(s): super().__init__(convert_charrefs=True); s.c=[]
    def handle_starttag(s,t,a):
        d=dict(a)
        if t=="article" and "card" in (d.get("class") or "") and "data-id" in d:
            s.c.append((d["data-id"],d["data-kind"],d["data-class"]))
p=C(); p.feed(open(P,encoding="utf-8").read())
print(len(p.c), collections.Counter(x[1] for x in p.c), collections.Counter(x[2] for x in p.c))
print("dups:",[k for k,v in collections.Counter(x[0] for x in p.c).items() if v>1])
PY
# expect: 32 Counter({'finding':25,'question':7}) Counter({'gap':14,'improve':8,'question':7,'defect':3}) dups: []

# the source's own counts + the 7 real Q: markers (8 hits, one is the legend at line 12)
grep -n 'COUNTS' notes/_subreports/2026-08-30-227-dashboard-regen-diff.md
grep -n '`Q:`' notes/_subreports/2026-08-30-227-dashboard-regen-diff.md

# script parses
python3 -c "import re;open('/tmp/p.js','w').write(re.search(r'<script>(.*?)</script>',open('reviews/DASHBOARD-DIFF-DECISIONS-2026-08-30-v1.html',encoding='utf-8').read(),re.S).group(1))" && node --check /tmp/p.js

# self-contained: no external src/href
grep -o 'src="[^"#]*"' reviews/DASHBOARD-DIFF-DECISIONS-2026-08-30-v1.html   # only an ESCAPED example inside <code>
```

## 7. Note for the conductor, not a ruling

`git status --porcelain` on this mount showed **only** the new review page as untracked. The
`notes/_REHEARSAL-LOG.jsonl` modification declared in the diff report (§B14) is **not** in the
working tree now — either already reconciled or never landed here. Worth one look before the
wrap assumes either.
