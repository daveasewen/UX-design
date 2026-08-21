# LANE R4 — probe hygiene (P-3/P-6 crash→refuse) + error-solid.svg pipeline attempt (#211 wave 1)

*Sonnet lane, brief `notes/_briefs/2026-08-21-211-findings-repair-wave1-v1.md` § LANE R4.
Nothing in this receipt is a ruling. Own fence: the two probe scripts named below + one svg.
No `git commit`, no `git checkout`, no `_build_all.py` — none run.*

## Summary

(a) **FIXED** — `probe_dangling_var_pixel.py` (P-3) and `probe_input_trim_enactment.py` (P-6)
now refuse with rc=77 + a named `COULD-NOT-ASK:` line when chromium cannot actually launch,
instead of crashing with an uncaught traceback at rc=1. Driven both masked and unmasked; the
unmasked output is byte-identical before/after.

(b) **STOPPED, NOT REPAIRED** — `error-solid.svg` is still empty. The repo's icon-source
pipeline (`knowledge/assets/icons/_export-icons.py`) requires a `FIGMA_TOKEN` secret that is
not present in this environment, and even with one, the script has no single-icon mode — it
re-exports the ENTIRE catalogue (all groups, all icons, `icons.manifest.json`), which is wider
than this lane's fence (one svg). Per the brief's explicit instruction, the file was left
untouched rather than improvised. Detail and evidence below.

## Claim table (s182-D1 — every claim carries a probeable token)

| # | claim | probeable token (command → expected) | driven / UNPROVEN |
|---|---|---|---|
| 1 | Before the fix, P-3 CRASHED (rc=1, uncaught traceback) when chromium was found on disk but could not launch (missing shared libs) | reproduced by unsetting `LD_LIBRARY_PATH` with `PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-s197` set — traceback ending `playwright._impl._errors.TargetClosedError: BrowserType.launch: ... error while loading shared libraries: libXdamage.so.1` → `RC=1` (captured pre-fix, this session) | **DRIVEN** |
| 2 | Before the fix, P-6 crashed identically, same class, same trigger | same env, `python3 knowledge/_probe_registry/probe_input_trim_enactment.py --check` → same `TargetClosedError` traceback → `RC=1` (captured pre-fix, this session) | **DRIVEN** |
| 3 | Root cause: `_browser_env()` in both probes only proves a binary FILE exists at an expected layout path; it never proves the binary can launch — so a launch-time exception in `drive()` (P-3) / `measure()` (P-6) was uncaught | read `_browser_env()` (both files, ~line 154/168): the function returns `({"executable_path": hits[0]}, None)` the moment `globmod.glob(...)` finds a hit — no launch probe | **DRIVEN** (code read + reproduced) |
| 4 | AFTER the fix, P-3 refuses rc=77 with a named reason when chromium is found but cannot launch | `unset LD_LIBRARY_PATH; PYTHONPATH=/var/tmp/pylibs PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-s197 TMPDIR=/var/tmp python3 knowledge/_probe_registry/probe_dangling_var_pixel.py --check` → first line `COULD-NOT-ASK: P-3 dangling-var PIXEL test — NOT-IN-THIS-ENVIRONMENT: chromium was found at '.../headless_shell' but could not launch (TargetClosedError: ...)`. `RC=77` | **DRIVEN** |
| 5 | AFTER the fix, P-6 refuses rc=77 identically | same env, `python3 knowledge/_probe_registry/probe_input_trim_enactment.py --check` → `COULD-NOT-ASK: P-6 text-box-trim enactment canary — NOT-IN-THIS-ENVIRONMENT: chromium was found at '.../headless_shell' but could not launch ...`. `RC=77` | **DRIVEN** |
| 6 | The other chromium-absent shape (playwright package itself not importable) already refused rc=77 before AND after — untouched by this fix | `unset PYTHONPATH PLAYWRIGHT_BROWSERS_PATH LD_LIBRARY_PATH; python3 knowledge/_probe_registry/probe_dangling_var_pixel.py --check` → `COULD-NOT-ASK: ... playwright is not importable ...` `RC=77`; same for P-6 | **DRIVEN** |
| 7 | AFTER the fix, unmasked (working browser) P-3 output is byte-identical to a second unmasked run, findings=0, rc=0 — the fix changed nothing about what is measured | `PYTHONPATH=/var/tmp/pylibs PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-s197 LD_LIBRARY_PATH=/var/tmp/chromelibs/root/usr/lib/aarch64-linux-gnu TMPDIR=/var/tmp python3 knowledge/_probe_registry/probe_dangling_var_pixel.py --check` run twice → `diff` of the two captures → empty (identical); both end `PROBE P-3 — findings=0`, `RC=0` | **DRIVEN** |
| 8 | AFTER the fix, unmasked P-6 output is likewise byte-identical run-to-run, findings=0, rc=0 | same env, `python3 knowledge/_probe_registry/probe_input_trim_enactment.py --check` run twice → `diff` empty; both end `PROBE P-6 — findings=0`, `RC=0` | **DRIVEN** |
| 9 | The fix does not regress the deeper plant-then-detect selftests | unmasked env, `python3 knowledge/_probe_registry/probe_dangling_var_pixel.py --selftest` → `✅ P-3 selftest PASS`, `RC=0`; `python3 knowledge/_probe_registry/probe_input_trim_enactment.py --selftest` → `✅ P-6 selftest PASS` (GREEN/FIRE/both REFUSAL arms all hold), `RC=0` | **DRIVEN** |
| 10 | `error-solid.svg` is still empty (no `<path>`), untouched by this lane | `wc -c knowledge/assets/icons/status-icons/error-solid.svg` → `103` bytes (shell only: `<svg .../>\n</svg>\n`), unchanged before/after this session | **DRIVEN** |
| 11 | The icon-source pipeline cannot produce the icon in this environment: no `FIGMA_TOKEN` | `python3 knowledge/assets/icons/_export-icons.py` → `Set FIGMA_TOKEN env var (token needs file_content:read scope).` `RC=1`; `env \| grep -i figma` → empty | **DRIVEN** |
| 12 | The pipeline has no single-icon mode — its writable region is the whole catalogue, wider than this lane's fence | read `_export-icons.py` (91-171): `main()` walks the ENTIRE Figma "Export board" (`EXPORT_BOARD = "13244:4171"`), batch-exports ALL groups, and overwrites `icons.manifest.json` — no icon-name / group filter argument exists | **DRIVEN** (code read) |
| 13 | The empty export is not new local corruption — `error-solid.svg` has been byte-identical-empty since the very first commit that added it, and the manifest's own record shows the pipeline captured zero fills for this icon at generation time | `git log --follow -p --all -- knowledge/assets/icons/status-icons/error-solid.svg` → first commit `de776e4` (2026-06-17) already adds the file with no `<path>`; `grep -A6 '"slug": "error-solid"' knowledge/assets/icons/icons.manifest.json` → `"fillMode": "baked", "fills": []` | **DRIVEN** |
| 14 | Network to `api.figma.com` is reachable from this sandbox (the blocker is credential, not connectivity) | `curl -sI https://api.figma.com` → `HTTP/2 302` to `https://www.figma.com/developers` | **DRIVEN** |

## What was driven vs what stays UNPROVEN

- DRIVEN: the crash reproduction (masked), the refusal (masked, post-fix), the byte-identical
  unmasked comparison, both probes' full `--selftest` suites, the pipeline's actual refusal
  message, its full-catalogue scope (read), the git history of the empty file, and network
  reachability to Figma.
- UNPROVEN / not attempted: whether a *credentialed* run of `_export-icons.py` against the live
  "Gaps and edits" Figma branch would produce a non-empty `error-solid.svg` today. The manifest
  evidence (item 13) suggests the SOURCE NODE itself may have been empty at the 2026-06-17
  export — i.e. this may be a Figma-side authoring gap, not a re-run-fixable local defect — but
  that is a hypothesis, not measured, since no token was available to test it. **Priced TODO:**
  whoever holds a `FIGMA_TOKEN` for this file should re-run `_export-icons.py` (accepting the
  full-catalogue write, or first patching in a single-icon filter) and diff `error-solid.svg`
  against today's empty state; if it is STILL empty, the fix belongs in Figma ("Error Solid"
  node on the Export board), not in this repo.
- I did NOT explore the connected Figma MCP tools (`mcp__Figma__*` / `mcp__8fbfe982...`) as an
  alternate route to the icon. That MCP session's Figma access is not verified to point at this
  repo's specific file key (`Cgbtrmfp15ruNFkIAClpkI`, "Gaps and edits" branch) or node
  (`13244:4171` → status-icons → Error Solid), and improvising a fetch path the brief did not
  name risks producing a substitute the pipeline itself never certified. Named here as a route
  NOT taken, priced for whoever picks this up next, not silently declined.

## Probe deltas by number

- P-3: untouched by this lane's measurement logic. Unmasked: findings=0 before and after
  (byte-identical). This lane's brief scope is P-3/P-6 refusal hygiene only — no threshold or
  measurement changed.
- P-6: same — findings=0 unmasked before/after, byte-identical.
- P-7: not touched by this lane (brief names it untouched; confirmed — this lane's fence never
  reached `probe_container_self_query.py`).
- P-8: not this lane's fence (LANE R1's).

## `git status --short` — verbatim at close

```
 M knowledge/_119-sweep-recheck.json
 M knowledge/_probe_registry/probe_dangling_var_pixel.py
 M knowledge/_probe_registry/probe_input_trim_enactment.py
 M knowledge/gen_token_ramp.py
 M knowledge/snippets/Button.reference.html
 M knowledge/snippets/Chart-butterfly-h.reference.html
 M knowledge/snippets/Template-dashboard.reference.html
 M knowledge/snippets/Template-detail.reference.html
 M knowledge/snippets/Template-list-index.reference.html
 M notes/_REHEARSAL-LOG.jsonl
 M notes/_dream/_GRADE-DECISIONS.jsonl
?? notes/_briefs/2026-08-21-211-findings-repair-wave1-v1.md
```

Named, path by path:
- `knowledge/_probe_registry/probe_dangling_var_pixel.py` — **mine** (part (a) fix).
- `knowledge/_probe_registry/probe_input_trim_enactment.py` — **mine** (part (a) fix).
- `knowledge/_119-sweep-recheck.json`, `knowledge/gen_token_ramp.py`,
  `knowledge/snippets/Button.reference.html`,
  `knowledge/snippets/Chart-butterfly-h.reference.html`,
  `knowledge/snippets/Template-dashboard.reference.html`,
  `knowledge/snippets/Template-detail.reference.html`,
  `knowledge/snippets/Template-list-index.reference.html` — **a sibling's** (shape matches LANE
  R1's `gen_token_ramp` generator fix + regen fence named in the programme brief; not touched by
  this lane, reported not repaired here).
- `notes/_REHEARSAL-LOG.jsonl`, `notes/_dream/_GRADE-DECISIONS.jsonl` — **not this lane's**;
  origin not investigated (outside fence — reported, not touched).
- `notes/_briefs/2026-08-21-211-findings-repair-wave1-v1.md` — the generated brief itself
  (untracked at mint), not this lane's to stage.
- `knowledge/assets/icons/status-icons/error-solid.svg` — **absent from this list because it
  was NOT touched** (still empty, still matches HEAD).

## Consequences / pitfalls (mandatory, Dave #165)

- **What could recur:** the same class — a `_browser_env()`-style lookup that proves a FILE
  exists but not that it LAUNCHES — could exist in any OTHER render-driven probe or gate built
  against the same `_LAYOUTS`/glob pattern (P-3 and P-6 share the pattern verbatim; the class
  note in `_RUNBOOK-render-verify.md`'s `_browser_env` cross-reference in P-3's own docstring
  suggests this shape was hand-copied). **Not swept this lane** — only the two named probes were
  in fence. If a future probe crashes the same way, check for this exact shape first
  (launch-time exception uncaught outside the file-existence check).
- **What this repair does NOT fix:** it does not make chromium launchable in this sandbox — it
  only ensures that when it CANNOT launch, the probe says so honestly (rc=77) instead of
  crashing (rc=1). A CI job with correctly staged `LD_LIBRARY_PATH` (per the render job's own
  install step) will never hit this refusal path at all; it is purely a hygiene fix for the
  degraded-environment case.
- **Class it belongs to:** [[a-crash-is-not-a-fail]] — the same class the docstrings in both
  probes already declare and half-cover (they handle "playwright not importable" and "no binary
  file found" as refusals, but the actual crash trigger — "binary found, cannot launch" — was
  unhandled). This lane closes the gap in the SAME convention already used two lines above it in
  each file, not a new one.
- **error-solid.svg — what recurs if forced:** hand-drawing a substitute path (explicitly
  forbidden by the brief) would create a THIRD divergence from the design source — the manifest
  would still say `"fills": []` while the file on disk carried a shape nobody in Figma drew,
  which is exactly the kind of silent, unattributable drift the two-store / write-once rulings
  exist to prevent. Left empty and reported is the honest state.
- **P-7/P-8 promotion, the do-not-rule item on the append list:** untouched; this lane never
  reached that question.

## Priced returns for DO-NOT-RULE items brushed

- None of the generated DO-NOT-RULE rows (store `state=open, owner=dave`, or rulings carrying an
  `open` field) were brushed by this lane's two repairs.
- Human-appended list: "⛔ A do-not-rule list cannot fence a GENERATOR" applies directly to part
  (b) — `_export-icons.py`'s writable region (the WHOLE icon catalogue) is named above (claim
  12) precisely because it is wider than this lane's fence, and the lane STOPPED rather than run
  it, per that instruction.

## Sub spend

Single-lane run, no sub-delegation issued from within this lane (I am the lane, not a
conductor). Token spend for this lane: approximately 60K tokens (research + two code edits +
masked/unmasked driven verification of both probes' `--check` and `--selftest`, plus the icon
pipeline investigation and git-history read). `n=1` (no further sub-agents spawned).
