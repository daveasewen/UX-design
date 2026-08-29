# #223 POST-WRAP capture brief — for the Opus post-wrap sub

Conductor: Fable, IN the 200–256K conditional band (declared in chat, probe GREEN 4/4 twice) —
this capture is MECHANICAL enactment; every disposition stays open for #224.

## THE POST-WRAP STRATUM (events after wrap commit 97bd458 — capture these, rule NOTHING)

1. **APCA parked** — already committed (709c132): W-262 + notes/_briefs/2026-08-28-223-apca-research-parked.md. Done; just verify it's in the record.

2. **DAVE'S COPILOT RETEST HAPPENED — the W-244 acceptance event, outcome AMBIGUOUS.** His words,
   verbatim, in chat: "worked pretty well, the token count didn't work as far as I could see,
   tiktoken definitely didn't install it was blocked by the company security, but I used GPT Sol
   wrote its own code and seems to have fixed it. we might have to port it back."
   - ⚠ UNKNOWN which pack he tested (v1.0.1 or v1.0.2) — the v1.0.2 purepy fallback exists
     precisely so tiktoken is not needed; "token count didn't work" is either (a) he tested the
     old pack, or (b) a new v1.0.2 failure class. NOBODY KNOWS YET. Record both readings, decide neither.
   - Evidence staged: Dave will copy the GPT-modified pack folder into the project folder
     (suggested name _incoming-copilot-pack); a forensics sub then diffs it against the shipped
     _MANIFEST.json shas, extracts GPT's code, classifies, prices the port-back, files a decision
     surface for Dave at the #224 opener.
   - MINT a store row for this (next free W-id, owner claude, state open, opened 223, home this
     brief): title names the Copilot-retest forensics + port-back; closes_when = the pack folder
     has arrived, the forensics report is filed identifying every GPT-touched file and which pack
     version was tested, and Dave has ruled port-back / already-fixed-in-v1.0.2 / drop.

3. **CI: billing FIXED (Dave), re-run of run #454 triggered from Dave's Chrome by the conductor.**
   At brief time: Status "In progress"; the release job finished 15s with an exit-1 annotation
   (the #221 read-back precedent says that exact shape was the ADVISORY ship-list-drift step of a
   SUCCEEDED job — do NOT assert either way). The conductor reads the final verdict in Chrome and
   relays in chat; the sandbox cannot reach the API (404, private repo). Record: instant-death era
   #443–#454 was GitHub BILLING, diagnosed this session, fixed by Dave today. Your own wrap commit
   will trigger a fresh fully-billed run — note that the NEXT session's opener owes ITS read-back.

## DO-NOT-RULE — absolute
- Do NOT close, or change the state of, W-244 — the retest outcome is ambiguous and its
  disposition is #224's, with the forensics in hand.
- Do NOT declare the retest passed or failed; record Dave's words and both readings.
- Do NOT write knowledge/_rulings.json. No roster/release/theme dispositions. The parked lists stay parked.

## MECHANICS
- This is a POST-WRAP FOLLOW-UP capture (the #221 "post-wrap: the CI read-back homed" / #219
  "wrap follow-up" precedent), NOT a second full wrap. Follow the capture runbook's post-wrap
  shape if it defines one; otherwise: home the stratum above in the right records (GOOD-MORNING
  stratum/carry conventions per the runbook), mint the store row, regen chain, commit, push.
- Commit: fresh printf msgfile (NO '#N date —' prefix on line 1), SESSION_N=223,
  knowledge/_RUNBOOK-git-commit.md dance, --all-dirty after accounting every path, push, read the
  subject back from git log -1 and quote it.
- One step per bash call (~178s wall). rm works. tiktoken installed sandbox-side.
- STUB back: commit sha + subject verbatim, the minted W-id, any gate refusals honestly repaired,
  and the current GOOD-MORNING next-session title line if the runbook's tooling regenerated it.
