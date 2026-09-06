# PREMISE PROBE — brief template (MODEL-ROUTING rule 7, added #250 2026-09-06)

> Runs BEFORE a canon-touching build lane. Opus 5, cold. Rules nothing, builds nothing, writes ONE
> file (the report). Its job is to break the brief's premise before a lane spends 150K on it
> (#244: lane built 0/4 correctly because the brief measured the wrong thing).

Fill the five lines. If you cannot fill line 3, the build is not ready to brief.

1. **PREMISE** — the one sentence the build lane assumes true. *(e.g. "a 3.7 KB comment shave clears both byte caps")*
2. **CONSEQUENCE IF FALSE** — what the lane would build wrongly, and what it costs to find out after.
3. **PROOF COMMAND** — the command(s) whose pasted output proves or breaks the premise. Run-before-cite: no output, no claim.
4. **MUTATION** — the change that SHOULD make the proof fail (mutation-tests-the-clause). If nothing fails, the proof is not a proof.
5. **RULINGS IN SCOPE** — `grep _rulings.json` ids the premise touches; the probe reads them and lists them on a `CITES:` line.

**Report:** `notes/_subreports/<date>-<n>-PROBE-<topic>.md` per `notes/_subreports/_TEMPLATE.md` (`COUNTS:` line PARSED — exact shape; `CITES:` line beside it, advisory). Price every option the conductor named; state the strongest case AGAINST the option that looks easiest; recommend nothing.

**Brief hygiene (Fable 5.1 / Opus 5 loops):** batch independent reads in one turn · Edit, never Write, on existing files · never `_build_all.py`.
