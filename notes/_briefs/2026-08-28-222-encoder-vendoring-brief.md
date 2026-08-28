# #222 sub brief — enact `s222-D2`: the pack measures tokens OUT OF THE BOX (vendored encoder data)

conductor: Fable, #222, 2026-08-28. Sub: Opus, one lane.
⚠ AGE BRACKETS: every premise here was written TODAY at #222 against HEAD `d4e69d0`+dirty.
Replay each at HEAD anyway — the #221 lesson is that a brief's premises age invisibly.

## THE RULING (read `s222-D2` from `knowledge/_rulings.json` yourself — 265 entries)

Dave, off the FIRST LIVE Copilot-bridge session, where the chain inscription refused because
tiktoken's encoder data could not fetch: **"I need this to work out of the box for the designers."**
Enact: the next pack release VENDORS the `cl100k_base` encoding data inside the pack, and the
pack's own token-measuring entry points resolve it automatically — no download, no hand-set env
var, no reachable blob host. **The no-estimate principle is untouched**: if even the vendored data
cannot load, the refusal stays loud and named. Declared scope edge: `pip install tiktoken` (the
wheel) remains the one documented install step — wheel vendoring is NOT this lane.

## MATERIALS

- The encoding file, verified loading from a plain dir this morning:
  `_to_delete/_tiktoken-cache/9b5ad71b2ce5302211f9c61530b329a4922fc6a4` (1,681,126 bytes;
  filename = sha1 of `https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken`,
  which is what tiktoken's cache lookup keys on). Record its sha256 in your report and beside the
  vendored copy.
- The stage: `apollo-spider/` (`gumdrop/`, `skills/`, `ci-template/`, `FIRST-SESSION.md`,
  `build-designer-pack.sh`). ⛔ `apollo-spider/dist/` is FROZEN HISTORY — untouchable, no bake.
- Doc sites that teach the old failure: `FIRST-SESSION.md` §Before-you-start (lines ~33–59) and
  step 4 (~281–286), `build-designer-pack.sh:288`, and whatever `.github/copilot-instructions.md`
  / `.github/prompts/*.md` in the stage say about tiktoken — grep, don't assume the list is these.

## THE MECHANISM — ONE HOME, CLASS NOT CASE

1. Vendor the data file into the stage at a location the packed layout carries (your call where —
   somewhere under the memento/gumdrop machinery it ships with), under its sha1 cache name, with a
   small README beside it: what it is, the URL it mirrors, sha256, and the licence note (tiktoken
   is MIT; this is its public encoding data).
2. **ONE helper** (one home, WRITE-ONCE) that every pack entry point measuring tokens routes
   through: `os.environ.setdefault("TIKTOKEN_CACHE_DIR", <vendored dir resolved relative to the
   pack>)` before `get_encoding` — setdefault so a designer's own env still wins. FIND the real
   consumers by grep (`get_encoding|cl100k|tiktoken`) across the whole stage including skills and
   ci-template; route them all through the helper. An entry point you miss is the same stumble
   shipping twice.
3. Keep the refusal path: vendored file missing/corrupt ⇒ the existing loud MeasurementRefused
   form, now naming the vendored path it tried.
4. Docs: rewrite the §Before-you-start check so the expected out-of-the-box result is
   `tiktoken OK` with NO network and NO env var; keep an honest note that the wheel itself still
   comes from PyPI.

## PROOF — DRIVE IT, DON'T REASON IT

- Fresh copy of the stage into `/var/tmp/` (ENOSPC class: use /var/tmp). With
  `TIKTOKEN_CACHE_DIR` **unset**, global caches moved aside (`/sessions/*/tmp/data-gym-cache`,
  `~/.cache`…), and egress broken for the process (`https_proxy=http://127.0.0.1:9
  HTTPS_PROXY=http://127.0.0.1:9`), the §Before-you-start check and the chain-inscription step
  must BOTH succeed via the vendored file. Then the mutation: move the vendored file aside, same
  broken egress ⇒ the named refusal fires. Both directions, measured.
- Re-run whatever pack gates read the stage (`_gate_release_audit.py`, `_gate_pack_docs.py`,
  `_validate_package_delta.py`, the import-smoke gate) — ⚠ `_validate_package_delta.py` GUARDS
  the frozen package surface: if adding the file requires the ledger/authorized route, follow the
  gate's OWN documented route citing `s222-D2`; ⛔ if the legal route is itself ruling-shaped,
  STOP and return that to the conductor — never weaken the gate.

## FENCE

`knowledge/_rulings.json` READ ONLY · no commit, no push, no bake, no `_build_all.py`, no
`git checkout` · `apollo-spider/dist/` untouched · no advisory promoted · no row of Dave's
touched — mint rows ONLY for your own new documents via `knowledge/_state.py` (and note: `W-244`
is Dave's; leave it, the conductor reconciles it) · version don't overwrite (`-vN`) · mv not rm
outside the granted mount.

## PITFALLS (Dave #165 — mandatory)

(a) call-boundary kill ~178s: drive steps individually; `pip install tiktoken
--break-system-packages` first in any fresh check. (b) `_capture_gate.py --selftest` writes
`knowledge/_CAPTURE-GATE.md`; restore via `git show HEAD:…` if it fires. (c) an unmatched grep is
not an absence — name every probe, search twice. (d) a crash is not a fail: refusals loud and
named; could-not-run graded COULD-NOT-RUN. (e) the L4/Lane-C v-next fixes already touched this
terrain — replay `notes/_subreports/2026-08-27-221-laneC.md` and `-220-audit-L4.md` REPLAY/fix
lists BEFORE building, so you don't re-issue what #221 already landed in the stage (the #221
divvy's own defect, do not repeat it).

## REPORT

`notes/_subreports/2026-08-28-222-encoder-vendoring.md` — COUNTS in the repo template form,
REPLAY-THESE, RULING-SHAPED QUESTIONS. Chat gets a stub: verdict · files touched · both proof
directions with the exact commands · gate verdicts · what W-244's remedy half still needs · any
COULD-NOT-RUN.
