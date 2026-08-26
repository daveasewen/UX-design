---
name: check-with-gates
description: Run Apollo's own executable gates against work in progress — contrast, token binding, type composites, icon provenance, accessibility targets, hardcoded values — and read the verdict honestly. Use to prove a design conforms rather than assert it. The mechanical half of check-against-design-system.
---

# Check with gates

This pack ships the same executable checks Apollo runs on itself: **36 gates that run
away from Apollo's repo**, plus 3 more that need a browser installed. They are the
difference between "this looks right" and "this measured right".

Run them on your own work. They are fast, they name the file and the line, and they tell
you what to do.

## Start with the runner

The pack ships one command that runs the whole set and counts the verdicts for you:

```
python3 apollo/designer-skills-v3/ci-template/run-gates.py --list   # what will run
python3 apollo/designer-skills-v3/ci-template/run-gates.py          # run them
python3 apollo/designer-skills-v3/ci-template/run-gates.py --browser  # + the playwright three
```

It reads the pack's own `_MANIFEST.json` to know which gates travel, so it never runs one
that is known not to work outside Apollo's repo, and it reports pass / FAIL /
COULD-NOT-ASK separately instead of collapsing them into red and green.

**Use the runner for the sweep; use the individual scripts below for the loop you're in.**
When one gate goes red you want to re-run *that* gate on *that* file every few seconds,
not the whole set. The table is for that.

⚠ **Take a baseline before you start.** Run the runner once on the freshly-unzipped pack,
before you've written anything, and keep the output. Most of these gates grade the design
system itself, so some of them may already be red at the version you were given — that is
Apollo's business, not yours. What matters is **the difference your work makes**: a gate
that was green and is now red is yours; a gate that was red before you arrived is not, and
chasing it wastes a day. If you don't know which is which, you can't read any of it.

## Which script answers which question

Everything runs from the pack root with plain `python3`. No install, no arguments unless
shown.

| your question | run |
|---|---|
| **Is this screen I composed sound?** — hex, local redefinitions, undefined classes, invented icons, reduced-motion, target size, all in one pass | `python3 knowledge/_validate_screen.py path/to/your-screen.html` |
| **Have I hardcoded spacing, radius or border width?** | `python3 knowledge/_validate_no_hardcode.py` |
| **Is my motion in CSS where it belongs, not in JS?** | `python3 knowledge/_validate_css_governed.py` |
| **Is every border-radius token-bound?** | `python3 knowledge/_validate_radius.py` |
| **Are my icons real library glyphs?** | `python3 knowledge/_validate_icons.py <Name>` |
| **Accessibility: focus, reduced-motion, target size** | `python3 knowledge/_validate_a11y.py` |
| **Do the tokens I named actually exist and resolve?** | `python3 knowledge/_validate_binds_resolve.py`, `python3 knowledge/_validate_property_resolves.py` |
| **Am I using type composites, not raw font values?** | `python3 knowledge/_validate_type_composites.py` |
| **Did another theme's colour leak in?** | `python3 knowledge/_validate_theme_provenance.py`, `python3 knowledge/_validate_legacy_leak.py` |
| **Contrast, token fidelity, ALL-CAPS, copy — the full snippet contract** | `python3 knowledge/_validate_snippets.py` |
| **Real contrast in real rendered hover/pressed states** | `python3 knowledge/_validate_state_contrast.py` — needs playwright |

`knowledge/` holds the rest. Any gate will tell you what it does:
`python3 knowledge/_validate_<name>.py --help`.

## How a gate finds your work

Only one gate takes a path. The others **look in a fixed place**, so getting your file
seen means putting it where the gate looks. Pick the route that matches what you're
making.

**Route A — you composed a screen from canon.** Hand the path over directly:

```
python3 knowledge/_validate_screen.py my-work/payment-summary.html
```

This is the main road, and the one to reach for first. It runs the composition checks,
the icon-provenance check and the accessibility check on that file and nothing else.

**Route B — you're working up styling in a tranche.** Create `knowledge/_proforma/` and
put your HTML there, with a `<div id="icon-manifest">` block in it (that marker is how
these gates recognise a tranche file). Then run `_validate_no_hardcode.py`,
`_validate_css_governed.py` and `_validate_radius.py`. They will grade every file in that
folder.

**Route C — you're proposing a component for the library.** Put it at
`knowledge/snippets/<Name>.reference.html` and run the whole snippet set. Be warned: this
route holds you to Apollo's full authoring contract — a `#token-manifest` block declaring
every var you use and the token behind it, plus light and dark blocks resolving them.
`_validate_snippets.py` and `_validate_coverage.py` will red until you've written it.
**That red is a contract you haven't signed yet, not a defect in your design.** If you
are not contributing a component, don't use this route — use A.

## Reading a verdict: three outcomes, not two

Every gate exits with a number, and there are **three** answers, not two.

- **`0` — pass.** But read the line that comes with it. `passed (0 tranche file(s))` is a
  gate that graded *nothing* and exited green; `passed (1 tranche file(s))` graded your
  work. A green over an empty set is not evidence about your design, and quoting it as
  one is the easiest way to fool yourself in this whole pack.
- **`1` — FAIL.** A real, measured failure. The gate names the file, the declaration and
  the fix.
- **`77` — COULD-NOT-ASK.** The gate could not reach something it needed — usually a
  browser it needs to measure rendered pixels — and says so on its first line, starting
  `COULD-NOT-ASK:`. **This is not a pass and it is not a failure. The question was never
  asked.** If you report a design as gated when a gate refused, you have reported
  something that was never checked. Say which gate could not ask, and why, in the same
  breath as the greens.

(`2` means you called it wrong — bad arguments.)

One trap worth naming: if you pipe a gate into `tail` or `head`, the exit code you see
belongs to `tail`, not to the gate. Run it plainly, or check `${PIPESTATUS[0]}`.

## When it goes red

**Fix at cause. Never edit the gate.**

A gate is Apollo's rule made executable. Changing it so your file passes doesn't make
your file right — it makes the rule stop protecting everyone else, silently, forever.
Same for deleting your file out of the folder the gate looks in.

Work the red like this:

1. **Read the whole message.** These gates say what is wrong, where, and what to do:
   *"`padding:18px` — raw px; use a token"*, *"16x16 is under the 24 floor (2.5.8) —
   enlarge, add a hit-expander, or claim an exception"*. The fix is usually in the text.
2. **Find the token, don't invent one.** Names live in `knowledge/tokens/*.json` and
   resolve in `knowledge/canon/canon.css`. Grep the stylesheet for the family you want —
   `--padding-`, `--gap-`, `--border-radius-`, `--border-width-`.
3. **Change the source, re-run the same gate**, and keep going until it's green over a
   population that isn't zero.
4. **If you genuinely disagree with the rule**, that is a design conversation, not a code
   change. Some gates take an explicit, documented exception marker
   (`data-a11y-target-exception`, `data-bespoke="reason"`) — an exception you can read
   later is legitimate; a gate you quietly loosened is not.
5. **If a gate reds on something that isn't yours** — a check about Apollo's own build
   machinery — you've picked up a gate that never left home. Eight of them stayed behind
   for exactly that reason, each named with its measured reason in the pack's root
   `_MANIFEST.json`. The runner won't call them; a hand-run might.

## The same gates run in CI

`ci-template/gates.yml` is a GitHub Actions workflow that calls the same
`run-gates.py` you've been running by hand. Copy it to `.github/workflows/gates.yml` in
your own repo and the whole set runs on every push — including the three browser-backed
gates, which CI installs a browser for even when your laptop can't.
`ci-template/README.md` covers where to put the pack, what blocks, what only advises, and
how to turn a check off honestly (delete the step — never hide it behind
`continue-on-error`).

Read the gate list from the runner, never from here. It, this skill and the workflow all
drive the same scripts on purpose; a list copied into a third place is how that guarantee
gets broken.

Local runs are for the loop you're in. CI is the record.

## Working with check-against-design-system

The two skills are halves of one review.

- **`check-with-gates`** proves the mechanical half: contrast maths, token existence,
  icon provenance, target sizes, hardcoded values. Definitive, and cheap.
- **`check-against-design-system`** does the half no gate can: was this the right
  component, does the layout obey the rails, do the states make sense, is the copy right.

Run the gates first. Then bring the verdicts — quoted, with their populations, and with
any COULD-NOT-ASK named — into the review. A design-system review that reports gate
results it didn't run is exactly the drift the gates exist to catch.

*Experimental.*
