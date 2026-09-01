# Brief — #233 delegated wrap (Opus): demo report-back, 1.0.5 diagnosis, dave-voice skill, boot levers

provenance: 233 · 2026-09-01 (evening, same date as #232) · conductor Fable, FILL ~172K real at
brief-cut (past the 150,929 advisory stop line, DECLARED at 154,726 with the probe quizzed GREEN
4/4 blind; `knowledge/_probe/session-233.json`) · row: MINT ONE for this brief at creation
(the #232 brief's W-337 is the pattern; `owner: dave`, `closes_when` = the wrap commit lands
with subject read back). SESSION_N=233.

## The job

Run the capture ritual per `knowledge/_RUNBOOK-capture-ritual.md`, final commit with `--wrap`,
`SESSION_N=233`. Tree at brief-cut: clean bar instrument appends (`notes/_REHEARSAL-LOG.jsonl`
excluded per s137-D1, `notes/_dream/_GRADE-DECISIONS.jsonl`), a render scratch dir
`knowledge/_render-233/` (DELETE it — it holds a copy of Dave's uploaded test output and is not
repo material; `git rm`-safe, never committed), and this brief. ⛔ NO PUSH — the conductor pushes
after you finish. ⛔ `outputs/p105/` and `outputs/syslibs/` are mount-side scratch, not repo.

## What happened today (chat-sourced — the conductor's own words, no sub-report exists)

1. **DEMO (W-308) — Dave's report-back: "went well".** 1.0.5 was not ready in time; **1.0.2
   carried the demo and the stakeholder was impressed.** Record W-308 as CLOSED-ON-DAVE'S-WORD
   in prose in the banner; ⛔ do NOT edit the row's state — that is a close and it is the
   conductor's at the next opener with the store open (DO-NOT-RULE below).
2. **Dave cold-tested v1.0.5 (`9fb07fa2`) after the demo. Ruling in chat, verbatim: "it waits
   for 06."** ⇒ 1.0.5 gets NO ratify word; fixes land in v1.0.6. Record as Dave's word, NOT as a
   `_rulings.json` id (the conductor inscribes at the #233/#234 opener). Q&A (grill-me) "worked
   well".
3. **Dave's test findings + the conductor's diagnosis, grounded in the unpacked proving zip:**
   ONE CLASS — the pack has NO BEHAVIOUR CONTRACT. `skills/generate-from-canon/SKILL.md` has
   zero mentions of script/JS/behaviour; rule 2 "copy the snippet" is read as markup+CSS. The
   JS-light principle exists only as `s116-D1` + ADR-0015 (`canon/dv-behaviour.js`), never in a
   skill. Three symptoms: (a) filter dropdowns — agent authored its own JS instead of the
   snippet's `<script>` (`Dropdown.reference.html:178`); reverting to the snippet's script
   fixed it; (b) line chart — no tooltips, not responsive = the JS-off fallback named in
   `chart-line.meta.json:85`; the output carries 22 `data-fx*` geometry attrs but never loads
   the partial, and `template-dashboard-bento.meta.json:129` "host no engine" compounds it;
   (c) bento grouping — first pass grouped nothing, second grouped by taste and patched with
   local overrides (`--bento-row-unit:460px` / `auto`, `cn-table` on stat-cards) that stripped
   the Trade/Accounts group's surface; the vocabulary (`tpl-group-kpi/-chart/-rail`) exists,
   the WHEN-to-group rule does not (meta schema can't express composition — its own
   `$composesNote`). Also SEEN in the conductor's render (light+dark, 1440, JS absent because
   `global-cash-trade.js` was not uploaded): dark mode drops every tile surface (CSS, not JS);
   "Dark mode" as the page's only primary button; FX warn status rendered before content.
   KPI 2×2 is the snippet's own layout, NOT a defect (conductor corrected himself).
4. **v1.0.6 direction (proposed by the conductor, NOT ruled):** behaviour rule beside rule 2 +
   a `_validate_behaviour.py` gate in check-with-gates + a grouping rule homed in
   `_bento_edit_rails.json` + a RETRIEVAL-SET CONTRACT with a provenance RECEIPT the gate
   checks. Dave: "we definitely have to think about how we need the retrieval to be strict,
   this is the factory mode we are trying to get nailed."
5. **Bento row-height — Dave FLOATED, explicitly "not saying this is correct":** rows sized by
   the largest item / step down to the next size / a rail carries the rule; worry = excess
   padding, "sometimes desirable, thorny". Conductor's read: fixed rows are the #217 MEASURED
   finding (intrinsic rows kill the span vocabulary), `s232-D3` keeps the three units forked;
   CSS-honest version = rail carries a LADDER, group declares a RUNG as a FLOOR
   (`minmax(rung, auto)`). Owed before any build: three renders side by side (fixed / floor /
   mis-rung) — Dave points or parks. Carry as FLOATED.
6. **Dave has MORE 1.0.5 observations not yet given** ("there's more but that's enough for
   now"). Carry as an open item, his.
7. **`dave-voice` skill SAVED** (account-wide, via save_skill): hybrid of ayghri/i-have-adhd —
   answer first, plain-prose why, ONE named next step, `**Technical** —` tier for ids/receipts.
   Dave: "I struggle with your verbosity sometimes but I also spot the occasional insight in
   the prose — let's try it your way." NON-REPO: home is the Cowork skills library
   (`s191-D2` marker: `(NON-REPO: Cowork skills library, skill id skill_01Cxbtc7rqNjZfm7qGm58EFN)`).
8. **Boot bloat, measured:** boot 78,392 real (23rd consecutive reading outside the s208-D1
   band). `MEMORY.md` 19.6KB ≈ 8.5K — compaction owed at the next opener. The rest is the
   PLUGIN ROSTER: the session booted with Figma's 12 skills + MCP instructions although Dave's
   plugin panel showed Figma/Design/PDF Viewer **Disabled**; after `save_skill` the skills
   list refreshed WITHOUT Figma. ⇒ roster is a live boot lever Dave controls; a "Disabled"
   badge may not propagate at boot. Re-base only after ~5 post-diet boots (#228 ruling).
9. **PARKED for the next session:** the AI-native SDLC playbook
   (`https://claude.com/blog/the-ai-native-sdlc-playbook` + academy course). Dave watched the
   video, thinks it may rhyme with our playbook; question to carry: what applies to a
   design-system FACTORY rather than a codebase.
10. **Render recipe — SEVENTH STRATUM for `_RUNBOOK-render-verify.md`:** the VM was REBUILT
    since #227 (disk 55%, `/var/tmp/pylibs` and `pw-browsers-220` GONE — the #227 orphan farms
    no longer exist). Fresh recipe OBSERVED end-to-end today: `pip install playwright` →
    `python3 -m playwright install chromium-headless-shell` (lands at
    `~/.cache/ms-playwright/chromium_headless_shell-1234`, exit non-zero on host-requirements
    as documented) → `ldd` shows ONLY `libXdamage.so.1` missing → `apt-get download
    libxdamage1` + `dpkg -x` to `<MOUNT>/outputs/syslibs` → `LD_LIBRARY_PATH` + `TMPDIR=/dev/shm`
    in the same call → RENDER OK, PNGs read by eye. Add the stratum (add, never trim).
11. **Memory step 3 (deferred from #232) RAN at this seat, conductor-written:**
    `designer-skills-packs-are-releases.md` § #233 + new `dave-voice-skill-and-boot-levers.md`
    + two MEMORY.md lines. Say so in the record; do not write memory yourself.

## Gauge lines for the record (state moments separately, never converted)

boot 78,392 real · check-in at Dave's "what's the temperature": FILL 154,726 real, 42 turns,
stop line 150,929 CROSSED and DECLARED at that moment (not late — Dave asked, the number was
given) · probe quizzed GREEN 4/4 blind at 154,726 (`last_check` in the probe file) · brief-cut
~172K real (conductor's estimate from turn deltas — label it ESTIMATE; the wrap sub reads the
real figure off `_checkin.py` at its own seat and quotes THAT) · subs 0 before this wrap sub
(this wrap sub's own spend is UNOBSERVABLE from its seat — declare). Effort band S–M, one
evening, no build lanes.

## DO-NOT-RULE

No `_rulings.json` writes (Dave's "it waits for 06" and W-308's close are BANKED for the
conductor's opener, not inscribed here). No memory writes. No W-row closes or re-words
(W-308 stays open in the store; mint ONLY this brief's own row). No push. No roster/version/
constant/band/floor/stop-line/wall moves. No `_gauge_tokens.py` re-base. No ratify claims —
1.0.5 is HELD, not refused, not ratified. No bento row-height decision of any kind. No claim
about what the SDLC playbook says (unread). No CI claims beyond `git rev-list --count
origin/master..HEAD` measured at your seat (it was 0 at the opener; #232 was pushed).

## Pitfalls — replayed

tiktoken FIRST · nothing survives a call boundary, ~178s wall · `TMPDIR=/dev/shm` or
mount-side, never `/var/tmp` · never pipe hashes/verdicts through tail/head · msgfile fresh +
unique under outputs, NO session prefix in the headline (T3 generates it) · banner discipline
`s214-D6`: chain toward 10–12K tape · regen serial ORDERED, ramp first, index LAST · read the
subject back after commit · roll order: age brackets FIRST, then NEW→1 · `knowledge/_render-233/`
must NOT be committed.

## Report

The ritual's artefacts are the report. Chat STUB back: wrap commit hash + subject as landed,
chain size, store/state counts read back, the s214-D5 cost line, and ⛔ BOTH TITLE LINES
(RENAME for #233, NEXT-TITLE for #234 — suggested: `Apollo - #234: the 1.0.6 brief — behaviour
contract, strict retrieval, and Dave's remaining 1.0.5 observations`) verbatim.
