# Robustness & portability — a hard requirement

*Drafted 2026-07-01 after a session where the governance worked but the **tooling** nearly sank it. The synthesis engine is meant to be portable — used by people who are not us, on their own machines. If they trip over plumbing before they reach the value, the governance is moot. This is the bar that plumbing has to clear.*

---

## The principle

**The tool owns the plumbing; the user never sees it.** Everything the operator had to do by hand this session — start a server, diagnose a deadlock, cache-bust a URL, kill a port, restart threaded — is a support ticket waiting to happen. A portable tool dies of a thousand papercuts, and we hit six in ten minutes. Zero-config is not a nicety here; it is the product.

## The visual-QA loop is a CORE stage, not a side-channel

The single biggest thing this session proved: **render → critique → fix → re-render is the craft gate**, and it's what separates "structurally correct but untidy" from "shippable". (Governance gets the *vocabulary* right; the QA loop gets the *finish* right — different jobs, see `_FIXED-FLEX-CHARTER.md`.) We got there via duct tape (a hand-run `python3 -m http.server` + the Claude-in-Chrome extension). That duct tape **proved the loop is valuable and must not ship as-is.**

The product must OWN this stage:
- a **bundled, tested renderer** — the right browser engine with its system deps baked in, so it can't segfault on someone's machine;
- **automatic fresh fetches** — content-hashed or no-cache, so an edit is always what's rendered (no manual cache-bust);
- **bounded timeout + retry + a visible fallback** — a render step must never silently hang for 45s; if it can't render, it says so and degrades gracefully;
- **no server, no ports, no terminal** — the render surface is managed in-process or as a supervised service the user never touches;
- the loop is **automated**: build → render → self-critique → fix → re-render → human, with the machine catching the craft misses (padding, collisions, spacing) *before* the human sees them.

## Papercuts we hit — the "must NEVER surface to the user" list

| Friction we hit | The user must never… | The product must instead… |
|---|---|---|
| Run a local server by hand | open a terminal | manage the preview/render surface itself |
| Single-thread server **deadlock** (page never idles) | diagnose a hang | serve robustly (threaded/in-process) — deadlock is impossible by design |
| **Cache** served the old file → manual `?v=N` | know caching exists | fresh-fetch every render (content hash / no-store) |
| `file://` blocked by the browser tool | understand URL schemes | render over a scheme the engine can actually reach |
| Sandbox renderer **segfaults** (exit 139) | care where it renders | ship a renderer with deps baked + a fallback path |
| Screenshot compositor renders a correct DOM as a dark/inverted PNG (aarch64 headless shell, 2026-07-02 — DOM verified white via computed styles) | doubt a correct page | trust chain for renders: screenshot + computed-style probe must agree, or the render step reports itself unreliable |
| Extension **"document idle"** flakiness (45s timeout) | retry blindly / wait | bounded wait + retry + a clear failure, never a silent hang |
| Git **index-lock** friction (earlier sessions) | clear `.git/index.lock` | robust VCS handling, or surface none of it |
| Missing licensed **font** → fallback render | install fonts | inject/bundle the brand font into the render context |

Every row is a place a real user would get stuck, blame the tool, and leave.

## Broader: environment fragility is the enemy

This is bigger than rendering. Across the project the fragile bits have all been *environmental*, not conceptual: the renderer, the server, git locks, the font, the sandbox itself. The governance model (curbs, retrieval, registers) is sound — it's the ground it runs on that shifts. **A portable product has to make the ground solid and invisible**, or people bounce off the plumbing before they ever feel the governance working.

## Acceptance bar (how we'll know it's portable)

- A new user, on a clean machine, gets from "brief" to "rendered, critiqued screen" with **zero manual environment steps**.
- No step can **silently hang**; every failure is bounded, explained, and recoverable.
- The render/QA loop runs **the same way every time** regardless of host (no per-machine yak-shave).
- The user never sees a port, a cache flag, a segfault, a lock file, or a URL scheme.

---

*Related: `_FIXED-FLEX-CHARTER.md` (the QA loop = the craft gate), memory `sandbox-html-rendering` (the current duct-tape recipe + its gotchas — the exact things this requirement must engineer away).*
