---
name: a-crash-is-not-a-fail
description: "A check that raises reports nothing about ANY check — measured #58, when one bare comma in prose took the whole 39-check wrap gate down with a traceback."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d995d8c6-ccb3-4d8d-8ed1-4a30f00a4f9f
  modified: 2026-07-30T21:25:01.958Z
sources: [cowork-import]
imported_at: 2026-09-16T03:13:39Z
---

**A CRASH IS NOT A FAIL.** A failing check reports and the run continues; a crashing one reports
**nothing, about anything**, and the session cannot tell a broken gate from a clean one.

**Measured #58:** `_capture_gate.py`'s `ABS_TERM_RE` used `([\d,]+)`, which matches a **bare comma**.
A prose MENTION in the banner — *"…no band was written before the job, and that is a LAPSE…"* —
parsed as the `job` term, `_n(",")` raised a bare `ValueError`, and the whole **39-check wrap** died
with a traceback instead of a verdict. The gate had been green minutes earlier; nothing about the
crash said which check was even running.

**How to apply:** (1) number groups require a **leading digit** (`(\d[\d,]*)`), which also fixes the
USE-vs-MENTION half for free — `search` walks past a mention with no number after it; (2) parse
helpers **fail loud and NAMED**, never a bare exception from inside a check; (3) add the offending
shape as a **fixture** and mutation-test both arms, or the fix is an assertion
([[gate-must-quote-what-it-forbids]]).

⚠ **Residual, declared not fixed:** a prose mention *followed by a number* still wins. **Scope is what
saves USE vs MENTION; syntax cannot.** Declaring the residual is the point — a half-fix reported as a
fix is the [[assertion-propagation-gap]] class.


