# CI template — run the Apollo gates on your own project

Two files sit beside this one:

- `gates.yml` — a GitHub Actions workflow. Copy it to `.github/workflows/gates.yml` in your repo.
- `run-gates.py` — the runner it calls. It also works on your laptop.

Unzip the Apollo pack somewhere in your repository. The workflow expects it at `apollo/`; if you
put it elsewhere, change `APOLLO_PACK` at the top of `gates.yml`.

Try it locally first:

```
python3 apollo/designer-skills-v3/ci-template/run-gates.py --list
python3 apollo/designer-skills-v3/ci-template/run-gates.py
```

## What runs

The pack ships `_MANIFEST.json`, and every gate in it carries a verdict that was measured by
actually running it outside the design system's own repository. The runner reads that list, so it
never runs a check that is known not to work away from home.

| | |
|---|---|
| **36 gates** | run on plain Python, no installs. These are the `gates` job. |
| **3 gates** | drive a real browser (`playwright`) to measure rendered geometry and colour: descender clipping, hit-area size, and control contrast in every state. These are the `render` job. |
| **8 gates** | are not in the pack at all. They only make sense inside the design system's own repo, and each one is named with its reason in `_MANIFEST.json`. |

Most of these gates check the design system itself — the tokens, the component contracts, the
reference markup, the canon CSS you build against. That is the point: if you change a token or
edit a snippet, the gates tell you what you broke.

Three of them grade **your** work rather than the pack's, and they have nothing to look at until
you give them something: `_validate_css_governed.py`, `_validate_no_hardcode.py` and
`_validate_radius.py`. They will pass loudly with a population of zero until your work is where
they look. A green that graded nothing is not the same as a green that graded something, and the
runner prints the difference.

## What blocks, and what does not

A gate reports one of three things:

- **pass** — it ran and found nothing. Exit 0.
- **FAIL** — it ran and found something. Exit 1. **This fails the build.**
- **COULD-NOT-ASK** — it could not reach something it needs, and says which thing on a line
  beginning `COULD-NOT-ASK:`. Exit 77. **This does not fail the build.**

The third one matters. A check that cannot run is not a check that passed, and it is not a check
that failed either — pretending otherwise is how a suite goes quietly blind. Refusals are printed
in full, with their reasons, and counted separately in the summary line.

A gate that times out or is missing counts as a failure. It never said why it could not answer.

## If something is already red on day one

Run it once before you wire up CI. Some gates may be red the moment you unzip the pack, because
they are reporting debt that already exists — a type binding that has drifted, a token fork that
is not yet in the ledger. That is real, and it is not caused by anything you did.

You have two honest options. Fix them, which is what the gate is asking for. Or record a
baseline and fix them over time:

```
python3 apollo/designer-skills-v3/ci-template/run-gates.py --write-baseline gate-baseline.json
```

Commit that file, and add `--baseline gate-baseline.json` to the workflow step. Every gate still
runs and every failure is still printed — but only failures that are **not** in the baseline fail
the build. It is a ratchet: when a gate starts passing, take it out of the file. The list should
only ever get shorter, and because it is a file in your repo, a reviewer can see it grow if it
ever does.

This is not the same as silencing a check. The check runs, the output is there, and the exception
is written down where someone can argue with it.

## Turning a check off

**Delete the step.** That is the honest way, and it is the only way this template supports.

Do not add `continue-on-error: true` to a step you want to stop worrying about. The step still
runs, still fails, and the workflow still reports success — so the red is real, invisible, and
permanent. Six months later nobody remembers the check exists. If a check is not earning its
place, remove it and let the diff say so, where a reviewer can see it.

If you want to keep a gate running but not blocking while you work through a backlog, say that
out loud in the step name — for example `Run the Apollo gates (advisory while we clear the
backlog)` — and put a date or an issue number in the comment above it. An exception with an
owner and an end is a decision. An unlabelled `continue-on-error` is a leak.

## Running it by hand

```
python3 apollo/designer-skills-v3/ci-template/run-gates.py            # the fast ones
python3 apollo/designer-skills-v3/ci-template/run-gates.py --browser  # the three browser ones
python3 apollo/designer-skills-v3/ci-template/run-gates.py --pack path/to/pack
```

The runner finds the pack by looking for `_MANIFEST.json` beside it and then upwards. If it
cannot find it, pass `--pack` or set `APOLLO_PACK`.
