# LANE IN2 — BRIEF — inscribe Dave's six ASK answers; teach the generator to keep his answers
#280 · 2026-09-16 · conductor (Fable 5.1) · **model: opus** · bash root `/sessions/intelligent-serene-curie/mnt/UX-design/`

## Input — his export, verbatim: `notes/_lanes/280/inscribe-active/DAVE-EXPORT-ask-2026-09-16.json` (20:23Z). Read lane IN's `REPORT.md` + `BRIEF.md` in this dir first: the twin/defect mechanics, the `ruled` ledger in `knowledge/_icon_nodes.json`, the exporter-defect section in `knowledge/_ICON-GAPS.md`, selftest + mutants.

## The conductor's reading of the six (check it against the JSON; if the JSON says otherwise, the JSON wins and say so)
1. **electricity** — twin `electricity-active`; `electricity-active-2` is mislabeled (its own icon; the smiley) → defect list.
2. **employee-banking-solution** — twin `…-active-2`; `…-active` is the right picture under a wrong name (`name-only`) → defect list as a NAME defect, not a missing-inactive.
3. **financial-health-check** — same shape as 2.
4. **reward** — same shape as 2.
5. **jade-lifestyle** — STILL OPEN (`choice: open`, twin null). Inscribe NOTHING; record his note verbatim on the base's null (*"jade-lifestyle-active-2 - think is the most likely the correct icon"*) so the record carries his lean without a default.
6. **traditional-chinese-medicine** — twin `…-active` (ticked; *"correct twin, but mislabeled"*); `…-active-2` flagged: *"this is the correct icon"* — i.e. `-active-2` is the true TCM drawing, its own icon; the base + `-active` pair is a mislabel of something else → BOTH the pair (name defect) and `-active-2` (own icon, needs inactive) go to the defect list, his words verbatim.

## Do
- Land 1–4 and 6 as lane IN did (textual spans, `$ruled` provenance, `ruled` ledger 19 → 24, `unresolved` shrinks accordingly), 5 as a note on the null. Extend the selftest one bite per base; selftest, `gen_kg_icons.py --selftest`, `_mutate.py`, `_validate_kg.py` all green. Append the defect entries to the `_ICON-GAPS.md` section with his words.
- **The generator:** `gen_kg_icons.py --land` would wipe every ruled default (IN's finding). Teach it to read the node file's `ruled` ledger (or the two export JSONs — pick the one that survives a regen, say which and why) so a regen preserves Dave's answers; add a selftest bite proving a regen keeps all 14 and drops none. Do NOT run `--land` for real; prove it with a dry-run or a copy under scratch that is deleted after. `/sessions` at 99% — never copy `knowledge/`, scratch under `/sessions/intelligent-serene-curie/mnt/outputs/in2/`, removed at the end.

## Report — `notes/_lanes/280/inscribe-active/REPORT-IN2.md` + `notes/_subreports/2026-09-16-280-IN2-inscribe-ask.md`; update `_state.json` row `W-280in` to closed (his export received) via the store's own API, add `W-280in2` for the generator work, close condition = selftest bite proves regen keeps his answers. Plain prose first.
Commit via `SESSION_N=280 SHOWROOM_ACK=1 bash knowledge/_git_commit.sh --reconciled <fresh msgfile> <paths…> < /dev/null`, msgfile `/tmp/_msg-280-IN2-$(date +%s).txt`, bare subject `#280 lane IN2: five more twins landed, jade-lifestyle left open, the generator keeps his answers`. Regenerate `_CHAIN.md` if needed. Locks → `mv` to `.git/_orphan-locks/`. Never `git stash` / `gen_kg_edges.py` / `_build_all.py`. Do not push. Return: report path, sha, plain-prose section.
