# #222 sub brief — enact `s222-D3` option B: the pure-Python exact fallback encoder

conductor: Fable, #222, 2026-08-28. Sub: Opus, one lane. Successor to the `s222-D2` lane —
read that lane's brief AND filed report FIRST, they are your ground:
`notes/_briefs/2026-08-28-222-encoder-vendoring-brief.md` ·
`notes/_subreports/2026-08-28-222-encoder-vendoring.md`.
⚠ AGE BRACKETS: written TODAY at #222, HEAD `36754e2` + a dirty regenerated
`_pack_manifest.json`/`_pack_gate_probe.json` (conductor's, post-commit probe — leave them).
Replay premises at HEAD anyway.

## THE RULING (read `s222-D3` from the store — 266 entries)

Dave: *"need to get this release fixed before we do any thing else, how about we do B"*.
Build: a pure-Python BPE encoder over the SAME vendored data file
(`apollo-spider/gumdrop/_encoder-cache/9b5ad71b…`), used ONLY when `import tiktoken` fails.
Requirements, all load-bearing:
1. **EXACT** — byte-identical token counts to real tiktoken. Ships with an **equality gate**:
   drives both engines over a real corpus (the pack's own text files are the natural one) and
   refuses on the first divergence, mutation-tested BOTH ways (corrupt a merge rank ⇒ gate fires;
   restore ⇒ green).
2. **NAMED** — every output line that today says which engine ran (`tiktoken cl100k_base`) must
   name the fallback distinctly (e.g. `purepy cl100k_base (exact, equality-gated)`); never silent.
3. **ONLY on import failure** — real tiktoken wins whenever importable (speed); the helper
   `_encoder_home.py` is the ONE HOME for this dispatch, extend it there, nowhere else.
4. **Refusal kept** — missing/corrupt data file ⇒ the existing loud named refusal, both engines.
5. **Performance measured, not assumed** — time both engines over the pack chain + the largest
   packed text; report the numbers. (Conductor's expectation: sub-second at pack sizes; if you
   measure worse than ~30s on any real pack artefact, name it as a finding.)
6. Docs: `FIRST-SESSION.md` §Before-you-start — `pip install tiktoken` becomes RECOMMENDED
   (faster), no longer required for the session to survive the night; the out-of-the-box check
   must pass with tiktoken absent. `build-designer-pack.sh` prose likewise.

## PROOF — same discipline as the s222-D2 lane

Fresh stage copy in `/var/tmp`, broken egress (`https_proxy=http://127.0.0.1:9`), AND tiktoken
made unimportable for the run (venv without it, or a first-on-path shadow module that raises
ImportError — say which and why): §Before-you-start check green via the fallback (engine named),
chain generation green via the fallback, counts equal to a tiktoken run of the same stage.
Mutations: data file aside ⇒ refusal; rank corrupted ⇒ equality gate fires.

## FENCE + PITFALLS — the s222-D2 brief's lists apply VERBATIM

Plus: do not touch the conductor's dirty `_pack_manifest.json`/`_pack_gate_probe.json`; the
frozen `memento-package/` copies may gain the dispatch ONLY via the same delta-legal shim route
the prior lane proved (new-names-only, AST arm untouched) — if that route cannot carry it, STOP
and return. tiktoken's own encoder applies a special-tokens regex and cl100k's pretokenizer
pattern — your implementation must reproduce the REAL pipeline (pretokenize regex + BPE merges),
not BPE alone; the equality gate is what makes this claim honest, so build the gate FIRST and
develop against it.

## REPORT

`notes/_subreports/2026-08-28-222-fallback-encoder.md` — repo-template COUNTS, REPLAY-THESE,
RULING-SHAPED QUESTIONS. Mint rows for your own new documents via `_state.py`. Chat stub:
verdict · files · both proof runs (commands + outcomes) · the timing table · equality-gate corpus
size + verdict · gate verdicts · COULD-NOT-RUN.
