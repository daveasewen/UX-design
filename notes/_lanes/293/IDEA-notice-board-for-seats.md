# Idea, not a lane — a notice board for concurrent seats

provenance: 293, Jev side-quest worker seat (Fable 5.1) · 2026-09-21 · **NOT ENACTED, NOT SCHEDULED**

⛔ Touches boot, so it is a post-Friday-25th lane under Dave's standing word: *"any analysis is fine
but any changes with impact will need to be made after the presentations and demos."*

## His question, verbatim

> we have techniques like leaving receipts, memento etc... this might seem like an odd qusetion but
> could we have a notice board or something for agents

## Why — it was needed today and happened by hand

#293 ran TWO seats at once: the conductor (dream-backlog work, then the wrap) and this worker seat
(Jev lanes J…J7). Coordination happened by (a) Dave relaying between chats ("the wrap is picking
them up") and (b) this seat leaving `notes/_lanes/293/J3/_FOR-THE-NEXT-WRAP.md` — a notice-board
post without a board. The wrap found it only because Dave said to look.

**The gap the existing instruments leave:** handoffs are SERIAL (session → next session); memento is
RETRIEVAL (the past, on request); receipts are AFTER THE FACT. None is present tense — who is live
now, what they are touching, what they need.

## The shape proposed in chat

- `_BOARD.jsonl` at the repo root, append-only (safe for two writers), plus `knowledge/_board.py`
  with `post · read · claim · expire`.
- A post is one line: `who` (seat + lane) · `what` (a sentence) · `touching` (paths) · `needs`
  (a sentence or nothing) · `expires` (a time, or "at wrap") · `ts`.
- Every seat reads the board at boot **right after the handoff** and at every seam check.
- The wrap sweeps expired posts into its receipts and clears the board.

## Three uses it would have paid for today

1. **Claims.** "Seat B is committing — hands off git for ten minutes." The stranded-lock class
   solved by a sentence. [[git-lock-mv-not-rm]]
2. **Hand-ups.** "J3 finished after your commit; three untracked paths, please sweep." What the
   `_FOR-THE-NEXT-WRAP.md` did, findable without being told to look.
3. **Questions to the room.** "Which cold brief is the demo's? Nobody has named it to the record"
   (HANDOFF-143 owed item 4) — parked for whoever can answer instead of dying in one seat's window.

## Rules so it does not become another haystack

- Posts EXPIRE. The board is never read for history.
- Nothing on the board is a ruling or a receipt; a post that matters is PROMOTED by the wrap into a
  handoff line or a subreport, then cleared.
- Committed or local? Open. If committed, it is a machine append named in the commit body like
  `_graph-mark-observations.jsonl`; if local, it is gitignored and two seats on one mount share it.
  His call.
- Boot cost: a board read must stay small — cap the file, expire aggressively — the boot ceiling is
  70,000 and already breached (HANDOFF-143).

## Ruling-shaped questions — QUESTIONS PUT, nothing inscribed

1. Build it after the 25th?
2. Committed machine-append or gitignored local file?
3. Does a claim on the board BLOCK (a seat refuses git while another's claim is live) or ADVISE?
4. Who clears — the wrap only, or any seat on expiry?
