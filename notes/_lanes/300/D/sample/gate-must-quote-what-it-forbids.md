---
name: gate-must-quote-what-it-forbids
description: "★★ A gate must QUOTE the defect it reports, so its own message is a member of the class it polices — USE vs MENTION is unreachable by syntax; only SCOPE makes such a check safe"
metadata: 
  node_type: memory
  type: feedback
  provenance: session-51 · 2026-07-30
  status: ruled
  originSessionId: 3ac606fc-48a9-4015-8ed0-e4fa741ca7fc
  modified: 2026-07-30T11:52:13.424Z
sources: [cowork-import]
imported_at: 2026-09-16T03:15:28Z
---

RULED #51 (`notes/_MEMENTO-DECISIONS.md` § ★ #51, dossier
`_DECISION-HISTORY/2026-07-30-the-gate-that-must-quote-what-it-forbids.md`).

Building `BARE_TOKEN_RE`, the self-bite control fired on its first run **and was right to**.
The warn must quote the offending figure — a gate that will not name what it found teaches
nothing and gets routed around — so the message necessarily *contains* a member of the class
the regex bans. The regex sees a match and cannot tell **mention** from **use**.

**Why:** the available green was to launder the message. That would have satisfied one control
by breaking the one above it — a false fix that reads as a pass, and one that guts the gate
while looking like tidying. ★ **A syntactic ban can never be made safe by being made cleverer.
What makes it safe is SCOPE.**

**How to apply:**

- When a check's own output trips it, do **not** widen the regex and do **not** edit the message.
  Prove the scope instead: the check reads one narrow surface, so its output is unreachable
  by construction.
- Replace the naive self-bite test with two: **(a) an INVERTED bite** — assert the message
  *still* contains the quoted defect, so a future "fix" that deletes the quotation FAILS
  instead of reading green; **(b) the real property** — the gate's own words, pasted *into*
  its scope, SHOULD flag. An exemption for the gate's own prose is how a rule stops applying
  to the thing that wrote it.
- ⚠ **This is why open 24 is HARDER than open 23, not easier.** Scope saves open 25; it cannot
  save a self-*measuring* sentence, because that sentence IS in scope. Argue this, don't just
  obey the warning.
- ★ Corollary found the same session: **a bare figure can silently unarm its neighbour.**
  `SIZE_A_RE` requires a unit word after the §A figure; the stamp had none, so the check
  matched nothing and its silence read as "nothing to check" rather than "cannot fire"
  [[unmatched-grep-is-not-an-absence]] [[silent-lookup-failure-class]].
- ★ And: **never invent a surface to satisfy a spec.** The spec said "GM/LS"; measured,
  `_LIVE-STATE.md` has no `size:` stamp. Scope to where the thing actually is, and write the
  re-point trigger into the comment [[gate-narrows-its-own-rule]].
- ★ **Mutation-test the suite.** Seven green controls mean nothing until mutants prove they can
  fail: a dead check, a deleted lookahead, a dropped narrowing — each must be caught. A suite
  that has never been made to fail is an assertion, not a proof.


