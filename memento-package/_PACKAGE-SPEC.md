provenance: #64 Fable conductor · 2026-07-31 · status: scaffold (Dave's separation constraint applied at birth)

# Memento package — spec and boundary

**What ships:** the clean Memento machinery — the chain/boot mechanism, retrieval
(`_memento_search.py` shape), the capture ritual, and the record-guarding gates — packaged for
**GitHub Copilot in VS Code** (org-push delivery, no marketplace) and a **Claude plugin**
(IN scope per Dave's #63 redirect; `create-cowork-plugin` skill exists for the Cowork side).
**What never ships:** anything Apollo — fonts, compliance content, design-system gates, tokens.

## ⛔ The boundary (Dave, live at the #64 opener: "its own folder… don't cause problems for Apollo")

- This folder is the package's only home in this repo. **Nothing in Apollo reads it; no Apollo
  gate globs it; no Apollo file MOVES into it — copies only, and every copy is delta-audited.**
- New gates for this surface get wired explicitly here if ever needed (gate-glob-scope rule);
  Apollo's gates stay exactly as wide as their globs.
- Lifting this folder to its own repo later is a one-move job and likely the distribution end
  state — **Dave's call, not taken here.**

## The boot rule — Dave's shape, #64 live (wording converged in-session; ledger entry at wrap)

On the first **"good morning"**: **check for a chain.**

- **Chain exists** → continue as normal — just pick up the chain (read it, orient, work; the
  wrap writes the chain the next "good morning" reads). The mechanism the source project
  lives by, unchanged.
- **No chain** → the **orientation prose** (explain Memento to the user — what it is, how it
  works; the one-pager's content), then **one two-option question:**
  1. *"Do you have a project you want us to work on together?"* — existing project without a
     chain → survey it, inscribe the first chain from what's found.
  2. *"What would you like to start on today?"* — a completely new, un-started project →
     start the record from nothing.

Design note (why this beat the earlier draft): the agent detects the one thing it CAN detect
mechanically (the chain's presence) and ASKS the one thing it can't (the user's intent) —
no silent surveying, one decision, the user's hands on the fork. Greeting = the named trigger.

## Packaging order (from the #64 divvy, stability gate CLOSED #64)

Stability evidence, quoted at close: ① CI run #209 — the wired survey step GREEN (full-workflow
green awaits the post-font-fix push, declared) · ② gate-5 matrix ratified (43/2/2 of 47) ·
③ capture phase 2 ratified (30/30; ds-022's #58 cross-check CLOSED by live re-run) · ④ all five
matrices ratified + mover count reconciled (43/1/1 of 45).

1. **Delta audit** of `notes/2026-07-25-claude-code-orchestration-survey.md` — **BASE, never
   current truth** (Dave's #62 caveat): re-verify every claim; the boot artefact to port is now
   `_CHAIN.md` + retrieval, not §A. Opens #65 in a clean window.
2. Ledger D4′ sequence.
3. Copilot-in-VS-Code package — **⬛ GATED ON D6: Dave's own access pre-check, still OWED.**
4. Claude plugin.
5. The one-pager (voice pass owed) fronts the package docs.
