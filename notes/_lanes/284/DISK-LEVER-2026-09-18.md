# #284 — THE DISK LEVER THAT #283 SAID DID NOT EXIST

provenance: 284 · 2026-09-18 · conductor Fable 5.1
status: FINDING, acted on by Dave at the #284 opener (session ended by the act itself)

## What #283 recorded
`_HANDOFF-134` § THE DISK, item 4: "NOT fixable from inside. NOT fixable from his Mac." Options given:
thumbs-down feedback, or wait for the rebuild that fires at 100%.

## What is actually true
The Cowork VM disk (`/sessions`, persistent ext4, 9.8 GB) is a bundle stored on Dave's Mac under
`~/Library/Application Support/Claude/`. Quitting the app and trashing that bundle forces the same
rebuild the record saw twice (#233, the night before #282) — deliberately, without hitting 100%.

Dave surfaced it by pasting a web how-to (reddit r/ClaudeAI 1rlc71n; anthropics/claude-code issue
37581). Neither the bundle's exact filename nor its size was verified from inside the sandbox —
the sandbox cannot read that folder. Dave was told to identify it by size (gigabytes), not name.

## What the wipe costs
Nothing durable: repo on the Mac + pushed at `2345543e`; memory in the cloud store; skills a
read-only mount. Lost: pip installs, tokenizer cache, `/tmp/gitshim` — all of which die on every
rebuild already. The session performing the wipe ends; #284 reopens cold on `_HANDOFF-134`.

## State at the moment of the act
- `_seam.py`: FILL 135,364 real / 3 turns · boot 80,882 (NINTH post-diet reading over 70,000) ·
  `/sessions` 98.7%, 127,716 KB free · own scratch removed 2/2.
- No lane cut. The 40 logo masters remain #284's first move, unchanged.
- Two instrument appends dirty (`notes/_REHEARSAL-LOG.jsonl`, `notes/_dream/_GRADE-DECISIONS.jsonl`),
  same class as #282/#283 — policy still Dave's.
- CI `gates` run 35341072505 on `2345543e`: completed, failure — inherited per its own commit message.

## Not ruled
- Whether the seam's "no render lane over 90%" is ADVISORY or BLOCKING — still Dave's.
- Whether a bundle wipe becomes a standing chore at some disk threshold — a question, not a ruling.
